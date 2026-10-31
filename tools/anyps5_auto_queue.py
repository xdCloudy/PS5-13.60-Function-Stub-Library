#!/usr/bin/env python3
"""Choose one explicitly approved AnyPS5 ABI batch for unattended submission.

The trusted main branch contains approvals. Unreviewed catalogue observations,
3.20 name forwarding stubs and inferred prototypes are NEVER submission input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from prepare_anyps5 import choose, read_reviews
from update_progress import load_inventory

SHA256 = re.compile(r"^[0-9a-f]{64}$")
REVIEW = re.compile(
    r"^https://github\.com/xdCloudy/PS5-13\.60-Function-Stub-Library/pull/[1-9][0-9]*$"
)
PREFIX = "refs/heads/feat/automated-reviewed-stubs-"
FORK = "https://github.com/xdCloudy/AnyPS5.git"


def published_branches(fork: str = FORK) -> set[str]:
    """Fail closed if the fork cannot be queried; never assume a missing branch."""
    result = subprocess.run(
        ["git", "ls-remote", "--heads", fork, PREFIX + "*"],
        check=True, text=True, capture_output=True, timeout=120,
    )
    branches = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{40}", parts[0]):
            raise ValueError("Malformed remote branch listing")
        if not parts[1].startswith(PREFIX):
            raise ValueError("Unexpected branch in remote listing")
        branches.add(parts[1])
    return branches


def approved_batches(queue: Path, known: dict, verified: set,
                     published: set[str]) -> list[dict]:
    """Validate every approval and select remaining eligible work in stable order."""
    if not queue.is_dir():
        raise ValueError("Approved ABI queue directory is missing")
    ready = []
    for approval in sorted(queue.glob("*.approval.json")):
        if approval.is_symlink():
            raise ValueError("Symlinked approval files are prohibited")
        stem = approval.name.removesuffix(".approval.json")
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,110}", stem):
            raise ValueError("Unsafe approval filename")
        evidence = queue / (stem + ".jsonl")
        if not evidence.is_file() or evidence.is_symlink():
            raise ValueError(f"Missing or symlinked reviewed evidence for {stem}")
        metadata = json.loads(approval.read_text(encoding="utf-8"))
        if (not isinstance(metadata, dict)
                or metadata.get("schema_version") != 1
                or metadata.get("approved_for_auto_submit") is not True
                or metadata.get("reviewed_by") != "xdCloudy"
                or not isinstance(metadata.get("review_url"), str)
                or not REVIEW.fullmatch(metadata["review_url"])
                or not isinstance(metadata.get("evidence_sha256"), str)
                or not SHA256.fullmatch(metadata["evidence_sha256"])):
            raise ValueError(f"Invalid explicit auto-submission attestation for {stem}")
        raw = evidence.read_bytes()
        if len(raw) > 200_000:
            raise ValueError("Reviewed ABI evidence exceeds 200KB limit")
        digest = hashlib.sha256(raw).hexdigest()
        if digest != metadata["evidence_sha256"]:
            raise ValueError(f"Reviewed ABI digest changed for {stem}")
        # Independently validate even already-published files: an unsafe
        # committed approval must not quietly pass a future scheduled run.
        reviews = read_reviews(evidence)
        if not 1 <= len(reviews) <= 100:
            raise ValueError(f"Approved batch must contain 1-100 rows: {stem}")
        if len({r["library"].casefold() for r in reviews}) != 1:
            raise ValueError(f"Approved batch mixes libraries: {stem}")
        keys = [(r["library"].casefold(), r["nid"]) for r in reviews]
        if len(keys) != len(set(keys)):
            raise ValueError(f"Duplicate reviewed NIDs: {stem}")
        branch = PREFIX + digest[:16]
        if branch in published:
            print(f"Already published; skipping {stem}: {branch}", file=sys.stderr)
            continue
        chosen, rejected = choose(reviews, known, verified, set(), set(), 100)
        if not chosen:
            print(f"No eligible reviewed exports in {stem}; skipping ({len(rejected)} blocked)",
                  file=sys.stderr)
            continue
        # A PR must not silently omit rejected entries in a supposedly
        # reviewed, library-focused batch; re-approve a smaller exact file.
        if len(chosen) != len(reviews):
            print(f"Stale/partial approval {stem}; skipping ({len(rejected)} blocked)",
                  file=sys.stderr)
            continue
        ready.append({"path": "approvals/anyps5/" + evidence.name,
                      "sha256": digest, "count": len(reviews), "branch": branch})
    # Orphaned unapproved evidence must never be picked up.
    return ready


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--github-output", type=Path, required=True)
    p.add_argument("--fork", default=FORK)
    args = p.parse_args()
    root = args.root.resolve()
    known, *other = load_inventory(root)
    verified = other[6]
    ready = approved_batches(root / "approvals/anyps5", known, verified,
                             published_branches(args.fork))
    selected = ready[0] if ready else None
    with args.github_output.open("a", encoding="utf-8") as out:
        out.write("ready=" + ("true" if selected else "false") + "\n")
        if selected:
            out.write("evidence_path=" + selected["path"] + "\n")
            out.write("evidence_sha256=" + selected["sha256"] + "\n")
            out.write("candidate_count=" + str(selected["count"]) + "\n")
    print(json.dumps({"ready": bool(selected), "selected": selected,
                      "remaining_reviewed_batches": len(ready)}))


if __name__ == "__main__":
    main()
