#!/usr/bin/env python3
"""Prepare conservatively gated AnyPS5 stub patches in a separate checkout.

Never supplies invented ABI prototypes. Reviewed ABI evidence is an external
input, intentionally excluded from this data-only catalogue.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import os
import json
from pathlib import Path
import re
import subprocess
import sys

from update_progress import load_inventory, nid_for
from candidate_overlap import check_candidates, save_report
from layout_patch import plan, apply_plan
from anyps5_metadata import scan_files

MAX_BATCH = 150
SAFE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PARAMS = re.compile(r"^[A-Za-z0-9_ ,*\[\]]{1,240}$")
REG = re.compile(r"\bAPS5_VABI\s+([A-Za-z_]\w*)\s*\(")


def git(cwd: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(cwd), *args],
                                   text=True, stderr=subprocess.PIPE).strip()


def inspect_existing(checkout: Path) -> set[tuple[str, str]]:
    """Reserve declarations, definitions, and literal NID exports in every library."""
    return set(scan_files(checkout))



def read_reviews(path: Path) -> list[dict]:
    if not path.is_file():
        raise ValueError("An external, explicitly reviewed ABI JSONL input is required")
    reviews = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if not all(k in r for k in ("library", "nid", "name",
                                   "return_type", "parameters", "abi_reviewed", "evidence")):
            raise ValueError("Missing reviewed ABI fields")
        if (r["abi_reviewed"] is not True or not str(r["evidence"]).startswith("https://")
                or r["return_type"] != "void" or not SAFE.fullmatch(r["name"])
                or not SAFE.fullmatch(r["library"]) or not PARAMS.fullmatch(r["parameters"])
                or nid_for(r["name"]) != r["nid"]):
            raise ValueError("Unsafe or unverified ABI review entry")
        reviews.append(r)
    return reviews


def choose(reviews: list[dict], known: dict, verified: set,
           occupied: set[tuple[str,str]], reserved: set[tuple[str,str]],
           max_stubs: int = 100) -> tuple[list[dict], list[dict]]:
    if not 1 <= max_stubs <= MAX_BATCH:
        raise ValueError("Batch must contain 1 to 150 exports")
    chosen, rejected = [], []
    seen_nids = set()
    occupied_nids = {nid for _, nid in occupied | reserved}
    for r in sorted(reviews, key=lambda x:(x["library"].casefold(),x["nid"])):
        key = (r["library"].casefold(), r["nid"])
        record = known.get(key)
        reason = None
        if key in occupied or key in reserved or r["nid"] in occupied_nids:
            reason = "already_covered_or_reserved"
        elif key in seen_nids:
            reason = "duplicate_in_input"
        elif not record or key not in verified or record.get("name") != r["name"]:
            reason = "not_a_strict_verified_catalogue_name"
        elif record.get("scope") not in ("existing_firmware_system_library",
                                         "existing_upstream_placeholder_library"):
            reason = "unsafe_ownership_scope"
        elif record.get("stub_assessment") != "throwing_stub_candidate_validation_required":
            reason = "not_assessed_eligible"
        elif not record.get("firmware_13_60_export_confirmed"):
            reason = "not_13_60_confirmed"
        elif len(chosen) >= max_stubs:
            reason = "batch_limit"
        elif chosen and chosen[0]["library"].casefold() != r["library"].casefold():
            reason = "different_library_next_batch"
        if reason:
            rejected.append({"library":r["library"],"nid":r["nid"],"reason":reason})
        else:
            chosen.append(r)
            seen_nids.add(key)
    return chosen, rejected


def apply(checkout: Path, candidates: list[dict], output_dir: Path) -> Path:
    """Build a library-aware patch without altering unrelated upstream macros."""
    if not candidates:
        raise ValueError("No eligible stub candidates; cannot create empty patch")
    lib = candidates[0]["library"]
    planned = plan(checkout, candidates)
    return apply_plan(checkout, planned, output_dir / (lib + "-reviewed-void-stubs.patch"))



def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    cli.add_argument("--anyps5-dir",type=Path,required=True)
    cli.add_argument("--abi-file",type=Path,required=True,
                     help="Human-reviewed public ABI input OUTSIDE the catalogue repository")
    cli.add_argument("--output-dir",type=Path,required=True)
    cli.add_argument("--max-stubs",type=int,default=100)
    cli.add_argument("--apply",action="store_true",help="Write a patch to a clean contribution branch")
    args=cli.parse_args()
    root, checkout = args.root.resolve(), args.anyps5_dir.resolve()
    if args.abi_file.resolve().is_relative_to(root):
        raise ValueError("ABI prototypes must remain outside this data-only repository")
    known,*other=load_inventory(root)
    verified=other[6]
    reviews=read_reviews(args.abi_file)
    occupied=inspect_existing(checkout)
    reserved=set()
    initial_main_sha = None
    if args.apply:
        if git(checkout,"status","--porcelain"):
            raise ValueError("AnyPS5 checkout must be clean before preparation")
        if git(checkout,"branch","--show-current") in ("main","master"):
            raise ValueError("Create a dedicated AnyPS5 contribution branch before --apply")
        # One final upstream snapshot and recheck, never optimistic use of an
        # incomplete progressive PR cache for publication.
        subprocess.run(["git","-C",str(checkout),"fetch","origin","main"],
                       check=True,stdout=subprocess.DEVNULL)
        if git(checkout,"merge-base","HEAD","origin/main") != git(checkout,"rev-parse","origin/main"):
            raise ValueError("Contribution branch is not based on current AnyPS5 main")
        initial_main_sha = git(checkout, "rev-parse", "origin/main")
        occupied = inspect_existing(checkout)
    selected,rejected=choose(reviews,known,verified,occupied,reserved,args.max_stubs)
    print(json.dumps({"candidates":len(reviews),"ready_to_prepare":len(selected),
                      "blocked":rejected,"overlap_checked":bool(args.apply)},indent=2))
    if args.apply and selected:
        # Live audit, not the historical dashboard cache. Every candidate
        # needs positive collision clearance from every current PR head.
        audit = check_candidates(selected, occupied, os.getenv("GITHUB_TOKEN", ""), nid_for)
        save_report(args.output_dir / "CANDIDATE_OVERLAP_AUDIT.json", audit)
        blocked = [r for r in audit["candidates"] if not r["verified_clear"]]
        if blocked:
            raise ValueError(f"Candidate-level overlap not verified: {blocked[:5]}")
        subprocess.run(["git", "-C", str(checkout), "fetch", "origin", "main"],
                       check=True, stdout=subprocess.DEVNULL)
        if git(checkout, "rev-parse", "origin/main") != initial_main_sha:
            raise ValueError("Upstream main advanced during PR audit; rerun on new base")
        if inspect_existing(checkout) != occupied:
            raise ValueError("Current upstream collision inventory changed")
        patch=apply(checkout,selected,args.output_dir)
        try:
            subprocess.run([sys.executable,"tools/check_conventions.py","--base","origin/main"],
                           cwd=checkout,check=True)
            branch=git(checkout,"branch","--show-current")
            subprocess.run([sys.executable,"tools/pr_overlap.py","--branch",branch],
                           cwd=checkout,check=True)
        except BaseException:
            # Restore only our modified files, never reset the contribution branch.
            subprocess.run(["git", "-C", str(checkout), "restore", "--",
                            "core/libs/prx/" + selected[0]["library"]],
                           check=True)
            raise
        branch=git(checkout,"branch","--show-current")
        pr_body = """### What

Prepare {count} reviewed, throwing-only function stubs in {library}.
NID bindings are strictly rehashed and ABI prototypes came from separately reviewed external evidence.
No implementation, ABI correctness or runtime support is claimed.

### Tested

- Python catalogue identity and scope gates: passed
- Current AnyPS5 main and all open PR heads: rechecked
- tools/check_conventions.py --base origin/main: passed
- tools/pr_overlap.py --branch {branch}: passed
- Build and runtime testing: NOT RUN

### Checklist
- [x] Based on current main; no other open PR implements the same functions
- [x] One topic per PR
- [x] No comments in code
- [x] Unimplemented paths throw using NotImplemented_nid_no_patch
- [x] No notes or screenshots added to upstream repository
- [x] No third-party code
- [x] Generic system-library scope only
- [ ] Depends on: none
- [ ] Fixes: none
- [ ] Unblocks: none
- [ ] GPUs tested: n/a
- [x] AI-assisted: yes

Source revision: {sha}
Functions: {count}
Library: {library}
Patch: {patchname}

A maintainer must verify the complete ABI evidence, build and runtime results before changing this draft PR to ready for review.
""".format(count=len(selected),library=selected[0]["library"],
           branch=branch,sha=git(checkout,"rev-parse","origin/main"),
           patchname=patch.name)
        (args.output_dir / "PULL_REQUEST_BODY.md").write_text(pr_body,encoding="utf-8")
        print("Patch:",patch)
        print("Draft PR body:",args.output_dir / "PULL_REQUEST_BODY.md")
        print("Build/runtime testing remains required; do not claim merge readiness.")
    elif args.apply:
        print("No changes written. ABI or identity evidence insufficient.")


if __name__=="__main__":
    main()
