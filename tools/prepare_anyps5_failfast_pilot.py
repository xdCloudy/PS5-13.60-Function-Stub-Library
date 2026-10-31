#!/usr/bin/env python3
"""Prepare a tiny, provisional fail-fast export PR using existing AnyPS5 conventions.

The declarations are host-facing placeholders that always throw. They are NOT
claimed as verified guest ABI prototypes and MUST NOT return normally.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

from dual_firmware_review import identity, load_1360, load_320, safe_name

SHA = re.compile(r"^[a-f0-9]{40}$")
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
NID = re.compile(r"^[A-Za-z0-9+-]{11}$")
LIBRARY = "libSceJsc"


def revision(directory: Path) -> str:
    result = subprocess.check_output(
        ["git", "-C", str(directory), "rev-parse", "HEAD"], text=True
    ).strip()
    if not SHA.fullmatch(result):
        raise ValueError("Source is not pinned to a full Git commit")
    return result


def nid_tools(checkout: Path):
    path = checkout / "tools/nid_names.py"
    spec = importlib.util.spec_from_file_location("anyps5_nid_pilot", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def select(proposal: dict, historical: dict, confirmed: dict, nid_module,
           checkout: Path) -> list[dict]:
    if (proposal.get("schema_version") != 1
            or proposal.get("library") != LIBRARY
            or proposal.get("require_original_320") is not True
            or proposal.get("max_functions") != 3):
        raise ValueError("Unexpected pilot configuration")
    values = proposal.get("candidates")
    if not isinstance(values, list) or not 1 <= len(values) <= 3:
        raise ValueError("Pilot must contain 1-3 verified identities")
    root = checkout / "core/libs/prx" / LIBRARY
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Upstream pilot library does not exist")
    selected, seen = [], set()
    for value in values:
        if not isinstance(value, dict):
            raise ValueError("Malformed candidate")
        name, nid = value.get("name"), value.get("nid")
        if (not isinstance(name, str) or not NAME.fullmatch(name)
                or not isinstance(nid, str) or not NID.fullmatch(nid)
                or not safe_name(name, nid) or nid_module.compute_nid(name) != nid):
            raise ValueError("Candidate name/NID mismatch or unsafe symbol")
        key = identity(LIBRARY, nid)
        if key in seen:
            raise ValueError("Duplicate candidate")
        seen.add(key)
        older, newer = historical.get(key), confirmed.get(key)
        if (not older or older["name"] != name
                or not newer or newer.get("name") != name
                or newer.get("name_status") != "verified_nid_binding"
                or newer.get("kind") != "defined_function_export"
                or newer.get("firmware_13_60_export_confirmed") is not True
                or newer.get("scope") not in (
                    "existing_firmware_system_library",
                    "existing_upstream_placeholder_library")
                or newer.get("stub_assessment") !=
                    "throwing_stub_candidate_validation_required"):
            raise ValueError("Unqualified dual-firmware candidate: " + name)
        selected.append({"library":LIBRARY, "name":name, "nid":nid,
                         "historical_source":older["source_file"]})
    # Check whole source tree, not just the target module: colliding exports
    # from a different module need distinct treatment.
    located = nid_module.source_locations({row["nid"] for row in selected})
    if located:
        raise ValueError("Candidate already has an upstream export: " + str(located))
    # Reject any existing use of the candidate's C symbol even without an
    # APS5_VABI marker. Never overwrite or silently add a second definition.
    for file in (checkout / "core/libs").rglob("*"):
        if file.suffix not in (".h", ".hpp", ".cpp", ".cc", ".cxx") or not file.is_file():
            continue
        text = file.read_text(encoding="utf-8", errors="replace")
        if any(re.search(r"\b" + re.escape(row["name"]) + r"\b", text)
               for row in selected):
            raise ValueError("Existing source already references one of the symbols: " + str(file))
    return selected


def prepare(checkout: Path, selected: list[dict], apply: bool) -> list[str]:
    folder = checkout / "core/libs/prx" / LIBRARY
    source = folder / "FailFastExports.cpp"
    header = folder / "include/FailFastExports.hpp"
    umbrella = folder / "libSceJsc.hpp"
    cmake = folder / "CMakeLists.txt"
    debt = checkout / "docs/dev/debt/libSceJsc.md"
    for path in (source, header):
        if path.exists() or path.is_symlink():
            raise ValueError("Pilot source already exists; do not overwrite: " + str(path))
    if not umbrella.is_file() or not cmake.is_file() or not debt.is_file():
        raise ValueError("Missing library build or umbrella header")
    old_header = umbrella.read_text(encoding="utf-8")
    old_cmake = cmake.read_text(encoding="utf-8")
    old_debt = debt.read_text(encoding="utf-8")
    include = '#include "prx/libSceJsc/include/FailFastExports.hpp"\n'
    build = 'target_sources(libSceJsc PRIVATE FailFastExports.cpp)\n'
    if include in old_header or build in old_cmake:
        raise ValueError("Pilot already included; abort")
    decl = "#pragma once\n\n#include \"SceTypes.hpp\"\n\nextern \"C\" {\n\n"
    decl += "\n".join("int APS5_VABI " + row["name"] + "();" for row in selected)
    decl += "\n\n}\n"
    impl = '#include "prx/libSceJsc/include/FailFastExports.hpp"\n'
    impl += '#include "prx/libc/include/General.hpp"\n\nextern "C" {\n\n'
    for row in selected:
        impl += ("int APS5_VABI " + row["name"] + "() {\n"
                 "    NotImplemented_nid_no_patch(__func__);\n}\n\n")
    impl += "}\n"
    debt_intro = (
        "\n### Source-backed pending PS5 3.20 and 13.60 exports\n\n"
        "These provisional parameterless C++ declarations are for import-resolution "
        "only. Names/NIDs are independently observed in original 3.20 forwarders "
        "and confirmed 13.60 catalogue exports; signatures and behaviour are "
        "unverified. All throw through NotImplemented_nid_no_patch without "
        "accessing guest arguments or returning normally.\n\n"
    )
    debt_items = "".join(
        "- [" + row["name"] + "]"
        "(../../../core/libs/prx/libSceJsc/FailFastExports.cpp)"
        " (NID `" + row["nid"] + "`) - original 3.20 "
        "forwarder and 13.60 confirmed; prototype and behavior unverified.\n"
        for row in selected
    )
    if "### Source-backed pending PS5 3.20 and 13.60 exports" in old_debt:
        raise ValueError("Existing pilot debt ledger: refuse duplicate")
    if not apply:
        return [str(header), str(source), str(umbrella), str(cmake), str(debt)]
    header.write_text(decl, encoding="utf-8")
    source.write_text(impl, encoding="utf-8")
    umbrella.write_text(old_header.rstrip() + "\n\n" + include, encoding="utf-8")
    cmake.write_text(old_cmake.rstrip() + "\n" + build, encoding="utf-8")
    debt.write_text(old_debt.rstrip() + "\n" + debt_intro + debt_items, encoding="utf-8")
    return [str(path.relative_to(checkout).as_posix())
            for path in (header, source, umbrella, cmake, debt)]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--source-320", type=Path, required=True)
    p.add_argument("--upstream", type=Path, required=True)
    p.add_argument("--proposal", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    root, older, upstream = args.root.resolve(), args.source_320.resolve(), args.upstream.resolve()
    proposal = json.loads(args.proposal.read_text(encoding="utf-8"))
    historical, _ = load_320(older)
    confirmed, _ = load_1360(root)
    selected = select(proposal, historical, confirmed, nid_tools(upstream), upstream)
    files = prepare(upstream, selected, args.apply)
    report = {
        "source_revisions": {
            "original_3_20": revision(older),
            "catalogue_13_60": revision(root),
            "anyps5_upstream": revision(upstream),
        },
        "pilot_exports": selected,
        "modified_files": files,
        "generated": args.apply,
        "prototype_status": "unverified_host_fail_fast_placeholder",
        "runtime_behaviour": "NotImplemented_nid_no_patch; never normal-return",
        "automatically_approved_guest_abi": 0,
        "ready_for_merge_without_upstream_review": False,
        "open_pr_overlap_check_performed_here": False,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
