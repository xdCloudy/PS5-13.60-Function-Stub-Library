#!/usr/bin/env python3
"""Fail-closed final, post-build AnyPS5 stub submission gate.

This runs on the ACTUAL committed contribution branch after builds, and
checks current upstream main and every open PR immediately before publishing.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from anyps5_metadata import scan_files
from candidate_overlap import save_report
from git_candidate_overlap import check_candidates_git
from layout_patch import plan
from update_progress import nid_for

SHA = re.compile(r"^[0-9a-f]{40}$")


def git(checkout: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(checkout), *args], text=True).strip()


def verify_batch(data: dict, checkout: Path) -> list[dict]:
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or not 1 <= len(candidates) <= 100:
        raise ValueError("Expected a nonempty batch containing at most 100 exports")
    base = data.get("base_sha")
    commit = data.get("patch_commit")
    if any(not isinstance(v, str) or not SHA.fullmatch(v) for v in (base, commit)):
        raise ValueError("Missing exact 40-character commit provenance")
    if git(checkout, "rev-parse", "HEAD") != commit:
        raise ValueError("The submitted commit differs from the approved batch")
    if git(checkout, "rev-parse", "origin/main") != base:
        raise ValueError("Upstream main changed since this batch was selected")
    if git(checkout, "rev-parse", "HEAD^") != base:
        raise ValueError("Submission branch must contain exactly one patch commit")
    if git(checkout, "status", "--porcelain"):
        raise ValueError("Dirty AnyPS5 checkout: review generated changes before submission")
    if len({(r["library"].casefold(), r["nid"]) for r in candidates}) != len(candidates):
        raise ValueError("Duplicate candidate identities")
    for r in candidates:
        if nid_for(r["name"]) != r["nid"]:
            raise ValueError("Batch contains a mismatched NID/name")
        if r.get("abi_reviewed") is not True or r.get("return_type") != "void":
            raise ValueError("Unreviewed or unsupported ABI")
    return candidates


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkout", type=Path, required=True)
    p.add_argument("--batch", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--skip-upstream-tools", action="store_true",
                   help="Tools already validated in preparation job; publisher stays data-only")
    args = p.parse_args()
    checkout = args.checkout.resolve()
    data = json.loads(args.batch.read_text(encoding="utf-8"))
    candidates = verify_batch(data, checkout)
    origin = git(checkout, "remote", "get-url", "origin")
    if origin.rstrip("/") not in (
        "https://github.com/boykopovar/AnyPS5.git",
        "https://github.com/boykopovar/AnyPS5",
    ):
        raise ValueError("origin must be the official AnyPS5 upstream")
    upstream_head = git(checkout, "ls-remote", "--heads", "origin", "main").split()[0]
    if upstream_head != data["base_sha"]:
        raise ValueError("Upstream main advanced during preparation; rebase/reselect")

    with tempfile.TemporaryDirectory(prefix="anyps5-main-check-") as tmp:
        pristine = Path(tmp) / "main"
        subprocess.run(
            ["git", "-C", str(checkout), "worktree", "add", "-q",
             "--detach", str(pristine), "origin/main"], check=True)
        try:
            main_occupied = set(scan_files(pristine))
            # Never trust an artifact just because it was uploaded by another
            # job. Regenerate the expected text from the reviewed batch and
            # prove that the published commit has no unrelated code changes.
            planned = plan(pristine, candidates)
            allowed = {p.relative_to(pristine).as_posix() for p in planned}
            actual_paths = set(git(
                checkout, "diff", "--name-only", "--no-renames",
                "origin/main..HEAD").splitlines())
            if actual_paths != allowed:
                raise ValueError("Proposal changes files outside the approved "
                                 "single-library throwing-stub placement")
            for target, expected_content in planned.items():
                published = checkout / target.relative_to(pristine)
                if published.read_text(encoding="utf-8") != expected_content:
                    raise ValueError(
                        f"Proposal does not match regenerated safe patch: {published}")
        finally:
            subprocess.run(
                ["git", "-C", str(checkout), "worktree", "remove", "--force",
                 str(pristine)], check=True)

    report = check_candidates_git(
        checkout, candidates, main_occupied, os.environ.get("GITHUB_TOKEN", ""),
        nid_for, pending_fork_url="https://github.com/xdCloudy/AnyPS5.git")
    save_report(args.report, report)
    if not report["scan_complete"] or any(
        not r["verified_clear"] for r in report["candidates"]
    ):
        raise ValueError("Final candidate NID/PR clearance failed; see audit report")

    if not args.skip_upstream_tools:
        branch = git(checkout, "branch", "--show-current")
        overlap = subprocess.run(
            [sys.executable, "tools/pr_overlap.py", "--branch", branch,
             "--repo", "boykopovar/AnyPS5"], cwd=checkout,
            text=True, capture_output=True, check=True)
        if overlap.stdout.strip() != "No overlap with open pull requests.":
            raise ValueError("Official AnyPS5 checker found unresolved conflicts: "
                             + overlap.stdout[:2000])
        subprocess.run([sys.executable, "tools/check_conventions.py",
                        "--base", "origin/main"], cwd=checkout, check=True)
    subprocess.run(["git", "-C", str(checkout), "diff", "--check",
                    "origin/main..HEAD"], check=True)
    # Check main once more after the expensive final PR review.
    if git(checkout, "ls-remote", "--heads", "origin", "main").split()[0] != data["base_sha"]:
        raise ValueError("Upstream main moved after final PR collision audit")
    print(f"PASS: {len(candidates)} committed, reviewed void exports; "
          f"{report['open_pr_verified_heads']} open PR heads rechecked; "
          "no candidate collisions; upstream tools were validated in preparation.")


if __name__ == "__main__":
    main()
