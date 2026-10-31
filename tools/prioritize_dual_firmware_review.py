#!/usr/bin/env python3
"""Create evidence-only priorities; this tool never approves or implements code."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

VALID={"dual_3.20_and_13.60","confirmed_13.60_only"}

def prioritize(rows):
    counts=Counter()
    libraries=defaultdict(Counter)
    seen=set()
    shortlisted=[]
    for item in rows:
        key=(item["library"].casefold(),item["nid"])
        if key in seen:
            raise ValueError("Duplicate identity: "+str(key))
        seen.add(key)
        if (item.get("signature_verified") is not False or
            item.get("behaviour_verified") is not False or
            item.get("approved_for_auto_submit") is not False):
            raise ValueError("Unexpected verified or approved candidate")
        group=item.get("evidence_class")
        if group not in VALID or item.get("firmware_13_60_export_confirmed") is not True:
            counts["historical_or_unqualified"]+=1
            continue
        status=item.get("live_main_source_scan")
        if status=="upstream_source_symbol_observed":
            counts["source_symbol_already_observed"]+=1
            continue
        if status=="upstream_other_library_source_symbol_observed":
            counts["source_symbol_in_other_provider"]+=1
            continue
        if status!="no_direct_upstream_source_observation":
            raise ValueError("Unknown source scan state: "+str(status))
        rank=(0 if group=="dual_3.20_and_13.60" else 1,
              0 if item.get("public_sdk_header_name_observations") else 1,
              item["library"].casefold(),item["nid"])
        record=dict(item)
        record["research_priority"]="dual-source" if rank[0]==0 else "13.60-confirmed"
        record["next_evidence_requirements"]=[
            "verify original name/NID hashes and chosen system-library ownership",
            "complete live upstream main and open PR overlap scan",
            "only a fail-fast throwing placeholder; no guessed normal return",
            "pass compile, CTest, conventions and technical debt checks",
            "independent ABI required before claiming any returning behaviour",
        ]
        record["approved_for_auto_submit"]=False
        record["safe_to_submit_without_further_evidence"]=False
        shortlisted.append((rank,record))
        counts["priority_candidates"]+=1
        libraries[item["library"]][group]+=1
    shortlisted.sort(key=lambda row:row[0])
    ordered=[record for _,record in shortlisted]
    summary={"counts":dict(sorted(counts.items())),
             "by_library":{lib:dict(groups) for lib,groups in sorted(
                libraries.items(),key=lambda x:(-sum(x[1].values()),x[0].casefold()))},
             "automatic_approvals":0,"automatic_upstream_prs":0,
             "policy":"Provisional throwing placeholders may follow accepted AnyPS5 convention, but source dedup, complete live PR overlap, build and upstream review remain mandatory"}
    return ordered,summary

def report_md(ordered,summary,limit):
    lines=["# PS5 3.20 + 13.60 evidence investigation priorities","",
           "All records are unapproved. A missing direct source-text match is not proof of export absence.",
           "Full live open-PR overlap, provider ownership and build checks remain mandatory.", 
           "Exact guest ABI is needed to claim returning behaviour, not to propose an explicitly provisional always-throwing import placeholder.","",
           "## Classification","",
           "| Status | Count |","|---|---:|"]
    for name,count in summary["counts"].items():
        lines.append("| "+name+" | "+str(count)+" |")
    lines.extend(["","## Highest-volume libraries","","| Library | Dual-source | 13.60-only | Total |",
                  "|---|---:|---:|---:|"])
    for library,groups in list(summary["by_library"].items())[:30]:
        dual=groups.get("dual_3.20_and_13.60",0)
        recent=groups.get("confirmed_13.60_only",0)
        lines.append("| "+library+" | "+str(dual)+" | "+str(recent)+" | "+str(dual+recent)+" |")
    lines.extend(["","## Leading individual research targets","",
                  "| Library | Symbol | NID | Source class | SDK header hint |",
                  "|---|---|---|---|---|"])
    for item in ordered[:limit]:
        hints=item.get("public_sdk_header_name_observations") or {}
        lines.append("| "+item["library"]+" | "+item["name"]+" | "+item["nid"]+" | "+
                     item["evidence_class"]+" | "+("yes" if hints else "none")+" |")
    lines.extend(["","None of these are independently validated as guest ABI. Public SDK header names",
                  "and 3.20 forwarding entries do not establish the correct guest ABI or behaviour.",
                  "Merged upstream precedents #10068, #9990 and #9695 permit provisional parameterless throwing exports; all still require complete live overlap checks."])
    return "\n".join(lines)+"\n"

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    parser.add_argument("--summary",type=Path,required=True)
    parser.add_argument("--markdown",type=Path,required=True)
    parser.add_argument("--limit",type=int,default=75)
    args=parser.parse_args()
    if not 1<=args.limit<=200:
        parser.error("limit must be 1..200")
    with args.input.open(encoding="utf-8") as source:
        records=[json.loads(line) for line in source if line.strip()]
    if not records:
        raise ValueError("Empty evidence review source")
    ordered,summary=prioritize(records)
    for dest in (args.out,args.summary,args.markdown):
        dest.parent.mkdir(parents=True,exist_ok=True)
    with args.out.open("w",encoding="utf-8") as output:
        for record in ordered:
            output.write(json.dumps(record,sort_keys=True)+"\n")
    args.summary.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    args.markdown.write_text(report_md(ordered,summary,args.limit))
    print(json.dumps({"priority":len(ordered),"libraries":len(summary["by_library"]),
                      "automatic_approvals":0},sort_keys=True))

if __name__=="__main__":
    main()
