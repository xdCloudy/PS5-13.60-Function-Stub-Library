#!/usr/bin/env python3
"""Prepare a bounded source-backed, ABI-provisional WebCore throwing-export batch.

No return value or actual behaviour is implemented. Final live PR overlap,
upstream conventions and full build are handled separately by the workflow.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

from dual_firmware_review import identity, load_1360, safe_name

SHA = re.compile(r"^[0-9a-f]{40}$")
LIBRARY = "libSceNKWebKit"
OWNER = LIBRARY.casefold()
PREFIXES = ("_ZN7WebCore", "_ZNK7WebCore")


def commit(path: Path) -> str:
    sha = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"],
                                  text=True).strip()
    if not SHA.fullmatch(sha):
        raise ValueError("Unpinned Git commit")
    return sha


def nid_module(root: Path):
    script = root / "tools/nid_names.py"
    spec = importlib.util.spec_from_file_location("anyps5_nkwebkit_nids", script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def select(catalogue: dict, upstream: Path, nid_api, limit: int) -> tuple[list, dict]:
    if not 1 <= limit <= 60:
        raise ValueError("Batch bound must be 1..60")
    candidate_rows = []
    for (owner, nid), record in sorted(catalogue.items()):
        name = record.get("name")
        if (owner != OWNER or not isinstance(name, str)
                or not name.startswith(PREFIXES)
                or record.get("firmware_13_60_export_confirmed") is not True
                or record.get("name_status") != "verified_nid_binding"
                or record.get("scope") not in {
                    "existing_firmware_system_library",
                    "existing_upstream_placeholder_library"}
                or record.get("stub_assessment") != "throwing_stub_candidate_validation_required"
                or not safe_name(name, nid)
                or nid_api.compute_nid(name) != nid):
            continue
        candidate_rows.append({"name":name,"nid":nid,"library":record["library"]})
    if not candidate_rows:
        raise ValueError("No verified 13.60 WebCore candidates")

    # The official AnyPS5 NID tool checks exports across EVERY PRX provider.
    exported = {
        x["nid"] for x in nid_api.source_locations(
            {row["nid"] for row in candidate_rows})
    }
    # A declaration or a known symbol in another library is evidence of
    # existing ownership, even if not registered as a direct export yet.
    unused = [row for row in candidate_rows if row["nid"] not in exported]
    all_text = []
    for file in (upstream / "core/libs").rglob("*"):
        if (file.is_file() and not file.is_symlink()
                and file.suffix in {".cpp",".h",".hpp",".cc",".cxx"}):
            all_text.append(file.read_text(encoding="utf-8",errors="replace"))
    selected = []
    for row in unused:
        pat = re.compile(r"\b" + re.escape(row["name"]) + r"\b")
        if any(pat.search(text) for text in all_text):
            continue
        selected.append(row)
        if len(selected) >= limit:
            break
    if not selected:
        raise ValueError("All candidate WebCore exports already have source observations")
    report = {
        "candidate_rows":len(candidate_rows),
        "globally_existing_export_count":len(exported),
        "unused_nids":len(unused),
        "selected":len(selected),
        "all_providers_checked":True,
        "open_pr_overlap_checked_by_generator":False,
        "signature_or_behaviour_verified":False,
    }
    return selected, report


def render(upstream:Path, records:list[dict], apply:bool) -> list[str]:
    folder = upstream / "core/libs/prx" / LIBRARY
    source = folder / "Export.cpp"
    header = folder / "include/InventoryExports.hpp"
    umbrella = folder / (LIBRARY + ".hpp")
    debt = upstream / ("docs/dev/debt/" + LIBRARY + ".md")
    if not all(x.is_file() for x in (source,header,umbrella,debt)):
        raise ValueError("Missing established AnyPS5 provider files")
    old_source = source.read_text(encoding="utf-8")
    old_header = header.read_text(encoding="utf-8")
    old_debt = debt.read_text(encoding="utf-8")
    if any(re.search(r"\\b" + re.escape(row["name"]) + r"\\b", old_source)
           for row in records):
        raise ValueError("Candidate is already present in Export.cpp")
    if ('#include "prx/libSceNKWebKit/include/InventoryExports.hpp"'
            not in umbrella.read_text(encoding="utf-8")):
        raise ValueError("Header not reachable via library umbrella")
    if not old_header.rstrip().endswith("}"):
        raise ValueError("InventoryExports.hpp no longer ends in extern C closure")
    marker = "### PS5 13.60 WebCore fail-fast declarations"
    if marker in old_debt:
        raise ValueError("Batch already present in technical debt")
    names = [row["name"] for row in records]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate source symbol")
    definitions = (
        '#include "prx/libSceNKWebKit/include/InventoryExports.hpp"\n'
        '#include "prx/libc/include/General.hpp"\n\n'
        'extern "C" {\n\n'
    )
    for row in records:
        definitions += (
            "int APS5_VABI " + row["name"] + "() {\n"
            "    NotImplemented_nid_no_patch(__func__);\n"
            "}\n\n"
        )
    definitions += "}\n"
    declarations = "".join(
        "int APS5_VABI " + row["name"] + "();\n" for row in records
    )
    old_start, old_close = old_header.rsplit("}",1)
    expanded_header = old_start.rstrip() + "\n" + declarations + "\n}" + old_close
    audit = (
        "\n" + marker + "\n\n"
        "These parameterless declarations resolve imports only and immediately "
        "throw through NotImplemented_nid_no_patch. Exact ABI prototypes and "
        "behavior are unverified; the code never reads guest arguments or "
        "returns normally. These names and NIDs are observed as confirmed "
        "13.60 exports, independently rehashed with AnyPS5 NID tools.\n\n"
    )
    for row in records:
        audit += (
            "- ["+row["name"]+"]"
            "(../../../core/libs/prx/libSceNKWebKit/Export.cpp)"
            " (NID " + row["nid"] + ") - firmware 13.60 export-table "
            "identity; prototype/behavior unknown.\n"
        )
    if apply:
        source.write_text((old_source.rstrip() + "\n\n" if old_source.strip() else "") + definitions, encoding="utf-8")
        header.write_text(expanded_header,encoding="utf-8")
        debt.write_text(old_debt.rstrip()+"\n"+audit,encoding="utf-8")
    return [x.relative_to(upstream).as_posix() for x in (source,header,debt)]


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalogue",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--upstream",type=Path,required=True)
    parser.add_argument("--limit",type=int,default=40)
    parser.add_argument("--report",type=Path,required=True)
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    root, upstream=args.catalogue.resolve(),args.upstream.resolve()
    catalogue, scan_counts=load_1360(root)
    selected, stats=select(catalogue,upstream,nid_module(upstream),args.limit)
    files=render(upstream,selected,args.apply)
    output={
        "source":"xdCloudy/PS5-13.60-Function-Stub-Library",
        "catalogue_sha":commit(root),
        "anyps5_main_sha":commit(upstream),
        "library":LIBRARY,
        "symbols":selected,
        "files_changed":files,
        "candidate_selection":stats,
        "applied":args.apply,
        "abi_prototype_claimed":False,
        "normal_return_implemented":False,
        "official_open_pr_scanner_still_required":True,
    }
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"selected":len(selected),"main_sha":output["anyps5_main_sha"]}))


if __name__=="__main__":
    main()
