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
# This is explicit register evidence, not an ABI/implementation certificate.
# Keep the literal NID: helper names often deliberately have a different hash.
ALIASES = re.compile(r'\bAPS5_EXPORT\s*\(\s*"(?P<nid>[A-Za-z0-9+/\-]{11})"\s*,\s*(?P<target>[A-Za-z_]\w*)\s*\)')
COMMENTS = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/')
ASM_SYMBOL = re.compile(
    r'\bAPS5_(?:SIGNAL_)?ASM_FUNCTION\s*\(\s*"([A-Za-z_]\w*)"\s*\)'
)
ASM_SUFFIX = re.compile(r"_nid_disambig[0-9]+$")
SCHEMA = 4


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
            # Alias registrations are exact-NID evidence, not inferred names.
            # Do not evaluate or execute upstream sources or scripts.
            masked=COMMENTS.sub("",content)
            aliases=list(ALIASES.finditer(masked))
            assemblies=ASM_SYMBOL.findall(masked)
            identities=[(nid_for(name), name, False, False) for name in set(declarations)|set(definitions)]
            identities.extend((m["nid"],m["target"],True,False) for m in aliases)
            for symbol in assemblies:
                if symbol.endswith(("_nid_no_patch", "_nid_no_patch_cut")):
                    continue
                canonical=ASM_SUFFIX.sub("",symbol.removesuffix("_nid_postfix"))
                identities.append((nid_for(canonical),symbol,False,True))
            for nid,name,explicit_alias,assembly_seen in identities:
                key=(lib,nid)
                entry=observations.setdefault(key,{
                    "library":folder.name,"nid":key[1],
                    "declared":False,"definition_seen":False,
                    "throwing_marker":False,"nonthrowing_body_seen":False,
                    "build_config_present":build_file,
                    "export_registered":None,"build_verified":None,
                    "explicit_alias_seen":False,
                    "assembly_definition_seen":False,
                    "abi_verified":None,"runtime_validated":None,
                    "source_files":set()})
                if explicit_alias:
                    entry["explicit_alias_seen"] = True
                    entry["export_registered"] = True
                elif assembly_seen:
                    entry["assembly_definition_seen"] = True
                else:
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
    previous = None
    if summary.exists() and path.exists():
        previous=json.loads(summary.read_text(encoding="utf-8"))
        if previous.get("source_sha")==sha and previous.get("scanner_version")==SCHEMA:
            return previous
    scanned=scan_files(upstream)
    by_lib=defaultdict(Counter)
    counts=Counter()
    lines=[]
    for (lib,nid),row in sorted(scanned.items()):
        state=("definition_throwing" if row["throwing_marker"] and
               not row["nonthrowing_body_seen"] else
               "definition_nonthrowing_unvalidated" if row["nonthrowing_body_seen"] else
               "explicit_alias_no_visible_definition" if row["explicit_alias_seen"] else
               "assembly_definition_unvalidated" if row["assembly_definition_seen"] else
               "declaration_without_visible_definition")
        row["source_state"]=state
        row["source_commit"]=sha
        counts[state]+=1
        by_lib[lib][state]+=1
        lines.append(json.dumps(row,sort_keys=True))
    old_symbols = {}
    if previous:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                prior=json.loads(line)
                old_symbols[(prior["library"].casefold(), prior["nid"])]=prior
    new_symbols = {
        (r["library"].casefold(), r["nid"]):r
        for r in (json.loads(line) for line in lines)
    }
    added = sorted(set(new_symbols) - set(old_symbols))
    removed = sorted(set(old_symbols) - set(new_symbols))
    compare_fields = ("source_state","declared","definition_seen",
                      "throwing_marker","nonthrowing_body_seen",
                      "explicit_alias_seen","assembly_definition_seen",
                      "build_config_present","source_files")
    changed = sorted(key for key in set(new_symbols) & set(old_symbols)
                     if any(new_symbols[key].get(field) != old_symbols[key].get(field)
                            for field in compare_fields))
    first_snapshot = previous is None
    changes = {
        "schema_version": 1, "source_sha": sha,
        "previous_source_sha": previous.get("source_sha") if previous else None,
        "baseline_only": first_snapshot,
        "added": None if first_snapshot else len(added),
        "removed": None if first_snapshot else len(removed),
        "changed_source_classifications": None if first_snapshot else len(changed),
        "samples_added": [] if first_snapshot else [{"library":k[0],"nid":k[1]} for k in added[:80]],
        "samples_removed": [] if first_snapshot else [{"library":k[0],"nid":k[1]} for k in removed[:80]],
        "samples_changed": [] if first_snapshot else [{"library":k[0],"nid":k[1]} for k in changed[:80]],
        "note": "These are source-level identity or status changes only; function bodies, runtime behaviour and ABI correctness are not compared."
    }
    write_if_changed(root/"reports/anyps5-symbol-changes.json",
                     json.dumps(changes,indent=2,sort_keys=True)+"\n")
    meta={
        "scanner_version":SCHEMA,
        "source_sha":sha,
        "observed_library_nid_records":len(scanned),
        "states":dict(sorted(counts.items())),
        "per_library":{k:dict(sorted(v.items())) for k,v in sorted(by_lib.items())},
        "explicit_export_alias_records": sum(x["explicit_alias_seen"] for x in scanned.values()),
        "assembly_definition_records": sum(x["assembly_definition_seen"] for x in scanned.values()),
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
