#!/usr/bin/env python3
"""Final, post-build gate for existing AnyPS5 constant/no-op implementations."""
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
from prepare_anyps5_constants import render, validate_records
from update_progress import nid_for

SHA = re.compile(r"^[0-9a-f]{40}$")
FORK = "https://github.com/xdCloudy/AnyPS5.git"


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), *args], text=True, stderr=subprocess.PIPE).strip()


def verify_metadata(checkout: Path, payload: dict) -> list[dict]:
    rows = payload.get("candidates")
    if not isinstance(rows, list):
        raise ValueError("Missing independently reviewed candidates")
    validate_records(rows)
    base, head = payload.get("base_sha"), payload.get("patch_commit")
    if any(not isinstance(x, str) or not SHA.fullmatch(x) for x in (base, head)):
        raise ValueError("Missing pinned exact Git revision")
    if (git(checkout, "rev-parse", "HEAD") != head
            or git(checkout, "rev-parse", "origin/main") != base
            or git(checkout, "rev-parse", "HEAD^") != base):
        raise ValueError("Reviewed implementation is not one commit on exact main")
    if git(checkout, "status", "--porcelain"):
        raise ValueError("Dirty source checkout")
    return rows


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkout", type=Path, required=True)
    p.add_argument("--batch", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--skip-upstream-tools", action="store_true")
    args = p.parse_args()
    checkout = args.checkout.resolve()
    payload = json.loads(args.batch.read_text(encoding="utf-8"))
    rows = verify_metadata(checkout, payload)
    if git(checkout, "remote", "get-url", "origin").rstrip("/") not in (
        "https://github.com/boykopovar/AnyPS5",
        "https://github.com/boykopovar/AnyPS5.git",
    ):
        raise ValueError("Contribution origin must be official AnyPS5")
    if git(checkout, "ls-remote", "--heads", "origin", "main").split()[0] != payload["base_sha"]:
        raise ValueError("Main advanced; refresh before constant implementation submission")

    with tempfile.TemporaryDirectory(prefix="anyps5-reviewed-constant-") as directory:
        pristine = Path(directory) / "main"
        subprocess.run(["git", "-C", str(checkout), "worktree", "add", "-q",
                        "--detach", str(pristine), "origin/main"], check=True)
        try:
            exact_plan = render(pristine, rows)
            allowed = {p.relative_to(pristine).as_posix() for p in exact_plan}
            changed = set(git(checkout, "diff", "--name-only", "--no-renames",
                              "origin/main..HEAD").splitlines())
            if allowed != changed:
                raise ValueError("Implementation touched files outside exact reviewed bodies")
            for file, expected in exact_plan.items():
                actual = checkout / file.relative_to(pristine)
                if actual.read_text(encoding="utf-8") != expected:
                    raise ValueError("Committed implementation differs from regenerated review plan")
            occupied = set(scan_files(pristine))
            confirmed = {(r["library"].casefold(), r["nid"]) for r in rows}
            if not confirmed <= {(lib.casefold(), nid) for lib, nid in occupied}:
                raise ValueError("Candidate has no original declared AnyPS5 source definition")
            # These identities are intentionally already present in main.
            # The final scanner must still block every OTHER collision and
            # any open/pending PR modifying the precise original function.
            main_other = {(lib, nid) for lib, nid in occupied
                          if (lib.casefold(), nid) not in confirmed}
        finally:
            subprocess.run(["git", "-C", str(checkout), "worktree", "remove",
                            "--force", str(pristine)], check=True)

    targets = {r["nid"]: {"path": r["path"], "name": r["name"]} for r in rows}
    report = check_candidates_git(
        checkout, rows, main_other, os.getenv("GITHUB_TOKEN", ""), nid_for,
        pending_fork_url=FORK, existing_targets=targets)
    save_report(args.report, report)
    if not report["scan_complete"] or any(
        not x["verified_clear"] for x in report["candidates"]
    ):
        raise ValueError("Current AnyPS5 main/open PR/fork collision scan blocked submission")

    if not args.skip_upstream_tools:
        branch = git(checkout, "branch", "--show-current")
        subprocess.run([sys.executable, "tools/check_conventions.py",
                        "--base", "origin/main"], cwd=checkout, check=True)
        overlap = subprocess.run(
            [sys.executable, "tools/pr_overlap.py", "--branch", branch,
             "--repo", "boykopovar/AnyPS5"], cwd=checkout,
            check=True, text=True, capture_output=True)
        if overlap.stdout.strip() != "No overlap with open pull requests.":
            raise ValueError("Official AnyPS5 PR overlap checker did not clear the batch")

    subprocess.run(["git", "-C", str(checkout), "diff", "--check",
                    "origin/main..HEAD"], check=True)
    if git(checkout, "ls-remote", "--heads", "origin", "main").split()[0] != payload["base_sha"]:
        raise ValueError("Main moved during the final collision scan")
    print(f"PASS: {len(rows)} independently reviewed existing constant/no-op bodies; "
          f"{report['open_pr_verified_heads']} open PRs audited")


if __name__ == "__main__":
    main()
