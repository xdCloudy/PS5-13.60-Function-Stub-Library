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
    cli.add_argument("--defer-live-api-audit",action="store_true",
                     help="Workflow preparation only; publisher MUST do full API audit")
    args=cli.parse_args()
    root, checkout = args.root.resolve(), args.anyps5_dir.resolve()
    if args.abi_file.resolve().is_relative_to(root):
        raise ValueError("ABI prototypes must remain outside this data-only repository")
    output = args.output_dir.resolve()
    if output.is_relative_to(root) or output.is_relative_to(checkout):
        raise ValueError("Audit reports and patches must remain outside both source repositories")
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
    print(json.dumps({"candidates":len(reviews),"identity_eligible":len(selected),
                      "blocked":rejected, "live_overlap_checked": False,
                      "mode": "apply" if args.apply else "read_only_preview"},indent=2))
    if args.apply and selected:
        # Live audit, not the historical dashboard cache. Every candidate
        # needs positive collision clearance from every current PR head.
        try:
            audit = ({"scan_complete": False, "deferred_to_publisher": True, "candidates": []}
                     if args.defer_live_api_audit else
                     check_candidates(selected, occupied, os.getenv("GITHUB_TOKEN", ""), nid_for))
        except Exception as exc:
            audit = {"schema_version": 1, "scan_complete": False,
                     "error_type": type(exc).__name__,
                     "error": str(exc)[:300],
                     "candidates": [{"library": row["library"], "nid": row["nid"],
                                     "verified_clear": False,
                                     "reasons": ["live_api_or_scan_failure"]}
                                    for row in selected]}
            save_report(output / "CANDIDATE_OVERLAP_AUDIT.json", audit)
            raise ValueError("Live overlap verification failed; no patch applied") from exc
        save_report(output / "CANDIDATE_OVERLAP_AUDIT.json", audit)
        blocked = [r for r in audit["candidates"] if not r["verified_clear"]]
        if blocked:
            raise ValueError(f"Candidate-level overlap not verified: {blocked[:5]}")
        subprocess.run(["git", "-C", str(checkout), "fetch", "origin", "main"],
                       check=True, stdout=subprocess.DEVNULL)
        if git(checkout, "rev-parse", "origin/main") != initial_main_sha:
            raise ValueError("Upstream main advanced during PR audit; rerun on new base")
        if inspect_existing(checkout) != occupied:
            raise ValueError("Current upstream collision inventory changed")
        # The upstream overlap tool reads committed Git trees, not the
        # working directory. Commit the generated patch to this clean,
        # single-purpose branch BEFORE running either upstream checker.
        original_head = git(checkout, "rev-parse", "HEAD")
        patch = apply(checkout, selected, output)
        changed_paths = sorted(str(p.relative_to(checkout)) for p in
                               (checkout / "core/libs/prx" / selected[0]["library"]).rglob("*")
                               if p.is_file() and p.suffix.lower() in (".cpp", ".cc", ".cxx", ".h", ".hpp"))
        try:
            subprocess.run(["git", "-C", str(checkout), "add", "--", *changed_paths], check=True)
            subprocess.run(["git", "-C", str(checkout), "-c",
                            "user.name=xdCloudy", "-c",
                            "user.email=52116030+xdCloudy@users.noreply.github.com",
                            "commit", "-m",
                            f"feat({selected[0]['library']}): add {len(selected)} reviewed throwing exports"],
                           check=True)
            subprocess.run([sys.executable, "tools/check_conventions.py",
                            "--base", "origin/main"], cwd=checkout, check=True)
            branch = git(checkout, "branch", "--show-current")
            # AnyPS5's checker returns 0 even when it PRINTS an overlap
            # report; require the exact no-overlap result, not merely rc=0.
            overlap = subprocess.run(
                [sys.executable, "tools/pr_overlap.py", "--branch", branch,
                 "--repo", "boykopovar/AnyPS5"],
                cwd=checkout, check=True, capture_output=True, text=True)
            if overlap.stdout.strip() != "No overlap with open pull requests.":
                raise ValueError("AnyPS5 overlap checker rejected the batch: " +
                                 overlap.stdout[:1500])
            if git(checkout, "status", "--porcelain"):
                raise ValueError("Unexpected uncommitted source changes after validation")
        except BaseException:
            patch.unlink(missing_ok=True)
            subprocess.run(["git", "-C", str(checkout), "reset", "--hard",
                            original_head], check=True)
            raise
        branch=git(checkout,"branch","--show-current")
        pr_body = """### What

Prepare {count} reviewed, throwing-only function stubs in {library}.
NID bindings are strictly rehashed and ABI prototypes came from separately reviewed external evidence.
No implementation, ABI correctness or runtime support is claimed.

### Tested

- Python catalogue identity and scope gates: passed
- AnyPS5 main and upstream Git-based open-PR checker: rechecked
- Final REST API candidate audit: performed again in isolated publisher
- tools/check_conventions.py --base origin/main: passed
- tools/pr_overlap.py --branch {branch}: passed (exact no-overlap verdict)
- Build and runtime testing: NOT RUN

### Checklist
- [x] Based on current main; no other open PR implements the same functions
- [x] One topic per PR
- [x] No comments in code
- [x] Unimplemented paths throw using NotImplemented_nid_no_patch
- [x] No notes or screenshots added to upstream repository
- [x] No third-party code
- [x] Generic system-library scope only
- [x] Depends on: none
- [x] Fixes: none
- [x] Unblocks: none
- [x] GPUs tested: n/a
- [x] AI-assisted: yes

Source revision: {sha}
Functions: {count}
Library: {library}
Patch: {patchname}

ABI evidence must be independently reviewed. This remains a draft until maintainers accept source evidence and downstream build/runtime results.
""".format(count=len(selected),library=selected[0]["library"],
           branch=branch,sha=git(checkout,"rev-parse","origin/main"),
           patchname=patch.name)
        (output / "PULL_REQUEST_BODY.md").write_text(pr_body,encoding="utf-8")
        # Preserve exactly what was committed so a final post-build gate can
        # recheck precisely this batch before sending anything upstream.
        (output / "SELECTED_CANDIDATES.json").write_text(
            json.dumps({"base_sha": initial_main_sha,
                        "patch_commit": git(checkout, "rev-parse", "HEAD"),
                        "candidates": selected}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        print("Patch:",patch)
        print("Draft PR body:",output / "PULL_REQUEST_BODY.md")
        print("Build/runtime testing remains required; do not claim merge readiness.")
    elif args.apply:
        print("No changes written. ABI or identity evidence insufficient.")


if __name__=="__main__":
    main()
