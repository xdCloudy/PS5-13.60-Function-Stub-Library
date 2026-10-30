#!/usr/bin/env python3
"""Scan AnyPS5 declarations and source bodies without guessing export/runtime validity."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess
from update_progress import nid_for, scan_source, write_if_changed

SYMBOL = re.compile(r"\bAPS5_VABI\s+([A-Za-z_]\w*)\s*\(")
SCHEMA = 1


def scan_files(upstream: Path):
    root=upstream/"core/libs/prx"
    observations={}
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        lib=folder.name.casefold()
        build_file=(folder/"CMakeLists.txt").is_file()
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in (".hpp",".h",".cpp",".cc",".cxx"):
                continue
            content=path.read_text(encoding="utf-8",errors="replace")
            rel=path.relative_to(upstream).as_posix()
            declarations=SYMBOL.findall(content)
            definitions=dict(scan_source(content)) if path.suffix in (".cpp",".cc",".cxx") else {}
            for name in set(declarations)|set(definitions):
                key=(lib,nid_for(name))
                entry=observations.setdefault(key,{
                    "library":folder.name,"nid":key[1],
                    "declared":False,"definition_seen":False,
                    "throwing_marker":False,"nonthrowing_body_seen":False,
                    "build_config_present":build_file,
                    "export_registered":None,"build_verified":None,
                    "abi_verified":None,"runtime_validated":None,
                    "source_files":set()})
                entry["declared"] |= name in declarations and path.suffix in (".hpp",".h")
                entry["definition_seen"] |= name in definitions
                entry["throwing_marker"] |= definitions.get(name)=="throwing_marker"
                entry["nonthrowing_body_seen"] |= definitions.get(name)=="source_definition"
                entry["source_files"].add(rel)
    for key in observations:
        observations[key]["source_files"]=sorted(observations[key]["source_files"])
    return observations


def build(root: Path, upstream: Path):
    root,upstream=root.resolve(),upstream.resolve()
    sha=subprocess.check_output(["git","-C",str(upstream),"rev-parse","HEAD"],
                                text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}",sha):
        raise ValueError("Missing upstream revision")
    path=root/"reports/anyps5-symbol-states.jsonl"
    summary=root/"reports/anyps5-symbol-states.json"
    if summary.exists() and path.exists():
        old=json.loads(summary.read_text(encoding="utf-8"))
        if old.get("source_sha")==sha and old.get("scanner_version")==SCHEMA:
            return old
    scanned=scan_files(upstream)
    by_lib=defaultdict(Counter)
    counts=Counter()
    lines=[]
    for (lib,nid),row in sorted(scanned.items()):
        state=("definition_throwing" if row["throwing_marker"] and
               not row["nonthrowing_body_seen"] else
               "definition_nonthrowing_unvalidated" if row["nonthrowing_body_seen"] else
               "declaration_without_visible_definition")
        row["source_state"]=state
        row["source_commit"]=sha
        counts[state]+=1
        by_lib[lib][state]+=1
        lines.append(json.dumps(row,sort_keys=True))
    meta={
        "scanner_version":SCHEMA,
        "source_sha":sha,
        "observed_library_nid_records":len(scanned),
        "states":dict(sorted(counts.items())),
        "per_library":{k:dict(sorted(v.items())) for k,v in sorted(by_lib.items())},
        "export_registration_verified":None,
        "build_verified":None,
        "runtime_validated":None,
        "note":"Definitions, declarations and build-file presence are distinct observations. No link-time export-registration, ABI or runtime verification is claimed."
    }
    write_if_changed(path,"\n".join(lines)+("\n" if lines else ""))
    write_if_changed(summary,json.dumps(meta,indent=2,sort_keys=True)+"\n")
    return meta


if __name__=="__main__":
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    cli.add_argument("--upstream-dir",type=Path,required=True)
    args=cli.parse_args()
    print(json.dumps(build(args.root,args.upstream_dir)["states"],indent=2))
