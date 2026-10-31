#!/usr/bin/env python3
"""Prepare a confirmed PS5 13.60 Remoteplay throwing import placeholder."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

from dual_firmware_review import load_1360, safe_name

LIBRARY = "libSceRemoteplay"
NAME = "sceRemoteplayGetClientInfo"
NID = "igQYjjcKOFo"
HEX = re.compile(r"^[0-9a-f]{40}$")


def head(path: Path) -> str:
    value = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"],
                                    text=True).strip()
    if not HEX.fullmatch(value):
        raise ValueError("Source not pinned to a Git commit")
    return value


def compute_tool(root: Path):
    file = root / "tools/nid_names.py"
    spec = importlib.util.spec_from_file_location("remoteplay_nid_tools", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check(catalogue: dict, upstream: Path, nids) -> dict:
    row = catalogue.get((LIBRARY.casefold(), NID))
    if (not row or row.get("name") != NAME
            or row.get("library") != LIBRARY
            or row.get("name_status") != "verified_nid_binding"
            or row.get("firmware_13_60_export_confirmed") is not True
            or row.get("scope") != "existing_firmware_system_library"
            or row.get("kind") != "defined_function_export"
            or row.get("stub_assessment") != "throwing_stub_candidate_validation_required"
            or not safe_name(NAME, NID)
            or nids.compute_nid(NAME) != NID):
        raise ValueError("13.60 identity is not qualified for a throwing placeholder")
    existing = nids.source_locations({NID})
    if existing:
        raise ValueError("NID is already registered in upstream AnyPS5: " + str(existing))
    pattern = re.compile(r"\b" + re.escape(NAME) + r"\b")
    for file in (upstream / "core/libs").rglob("*"):
        if (file.is_file() and not file.is_symlink()
                and file.suffix in {".cpp", ".cc", ".cxx", ".h", ".hpp"}
                and pattern.search(file.read_text(encoding="utf-8", errors="replace"))):
            raise ValueError("Existing source symbol: " + file.relative_to(upstream).as_posix())
    return {"name": NAME, "nid": NID, "library": LIBRARY,
            "guest_abi_verified": False, "normal_return": False}


def append(upstream: Path, apply: bool) -> list[str]:
    folder = upstream / "core/libs/prx" / LIBRARY
    source = folder / "Export.cpp"
    header = folder / "include/InventoryExports.hpp"
    umbrella = folder / (LIBRARY + ".hpp")
    debt = upstream / ("docs/dev/debt/" + LIBRARY + ".md")
    if not all(x.is_file() for x in (source, header, umbrella, debt)):
        raise ValueError("Existing upstream Remoteplay library layout has changed")
    old_source = source.read_text(encoding="utf-8")
    old_header = header.read_text(encoding="utf-8")
    old_debt = debt.read_text(encoding="utf-8")
    if NAME in (old_source + old_header + old_debt):
        raise ValueError("Export already known; refuse duplicate")
    if not old_header.rstrip().endswith("}"):
        raise ValueError("Export header closure has changed")
    if '#include "prx/libSceRemoteplay/include/InventoryExports.hpp"' not in umbrella.read_text(encoding="utf-8"):
        raise ValueError("Export header is not umbrella-reachable")
    definition = (
        '\n\nextern "C" {\n'
        'int APS5_VABI ' + NAME + '() {\n'
        '    NotImplemented_nid_no_patch(__func__);\n'
        '}\n}\n'
    )
    prefix, suffix = old_header.rsplit("}", 1)
    updated_header = prefix.rstrip() + "\nint APS5_VABI " + NAME + "();\n\n}" + suffix
    ledger = (
        "\n### Additional confirmed PS5 13.60 throwing imports\n\n"
        "- [" + NAME + "](../../../core/libs/prx/libSceRemoteplay/Export.cpp)"
        " (NID " + NID + ") - confirmed firmware 13.60 function export name/NID"
        " with independently recomputed hash. Exact guest signature and behavior"
        " are unknown. The declaration immediately throws through"
        " NotImplemented_nid_no_patch and never returns normally.\n"
    )
    if apply:
        source.write_text(old_source.rstrip() + definition, encoding="utf-8")
        header.write_text(updated_header, encoding="utf-8")
        debt.write_text(old_debt.rstrip() + "\n" + ledger, encoding="utf-8")
    return [path.relative_to(upstream).as_posix() for path in (source, header, debt)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root, upstream = args.catalogue.resolve(), args.upstream.resolve()
    records, _ = load_1360(root)
    row = check(records, upstream, compute_tool(upstream))
    paths = append(upstream, args.apply)
    report = {
        "catalogue_commit": head(root),
        "anyps5_commit": head(upstream),
        "source": "confirmed_firmware_13_60_export_table",
        "export": row,
        "files": paths,
        "applied": args.apply,
        "pr_overlap_verified": False,
        "build_test_verified": False,
        "abi_claimed": False,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"library": LIBRARY, "name": NAME, "nid": NID,
                      "applied": args.apply}))


if __name__ == "__main__":
    main()
