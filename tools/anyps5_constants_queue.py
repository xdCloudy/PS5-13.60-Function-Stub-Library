#!/usr/bin/env python3
"""Find the next explicitly approved, unsubmitted constant/no-op AnyPS5 batch."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from prepare_anyps5_constants import read_records

DIR = "approvals/anyps5-constants"
PREFIX = "refs/heads/feat/automated-reviewed-constants-"
FORK = "https://github.com/xdCloudy/AnyPS5.git"
REVIEW = re.compile(
    r"^https://github\.com/xdCloudy/PS5-13\.60-Function-Stub-Library/pull/[1-9][0-9]*$"
)
SHA256 = re.compile(r"^[a-f0-9]{64}$")


def fork_heads(fork: str = FORK) -> set[str]:
    result = subprocess.run(
        ["git", "ls-remote", "--heads", fork, PREFIX + "*"],
        check=True, text=True, capture_output=True, timeout=120)
    heads = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if (len(parts) != 2 or not re.fullmatch(r"[a-f0-9]{40}", parts[0])
                or not re.fullmatch(PREFIX + r"[a-f0-9]{16}", parts[1])):
            raise ValueError("Unknown fork ref; aborting automated submission")
        heads.add(parts[1])
    return heads


def select(queue: Path, existing: set[str]) -> list[dict]:
    if not queue.is_dir():
        raise ValueError("Reviewed constant-implementation queue does not exist")
    options = []
    for approval in sorted(queue.glob("*.approval.json")):
        if approval.is_symlink():
            raise ValueError("Symlinked approval not permitted")
        stem = approval.name.removesuffix(".approval.json")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,110}", stem):
            raise ValueError("Unsafe batch identity")
        file = queue / (stem + ".jsonl")
        if not file.is_file() or file.is_symlink():
            raise ValueError("Approval missing its exact evidence file")
        metadata = json.loads(approval.read_text(encoding="utf-8"))
        if (not isinstance(metadata, dict)
                or metadata.get("schema_version") != 1
                or metadata.get("approved_for_auto_submit") is not True
                or metadata.get("reviewed_by") != "xdCloudy"
                or not isinstance(metadata.get("review_url"), str)
                or not REVIEW.fullmatch(metadata["review_url"])
                or not isinstance(metadata.get("evidence_sha256"), str)
                or not SHA256.fullmatch(metadata["evidence_sha256"])):
            raise ValueError("Unreviewed or malformed constant implementation approval")
        raw = file.read_bytes()
        if len(raw) > 200_000:
            raise ValueError("Reviewed implementation file too large")
        digest = hashlib.sha256(raw).hexdigest()
        if digest != metadata["evidence_sha256"]:
            raise ValueError("Reviewed source bytes changed after approval")
        rows = read_records(file)
        branch = PREFIX + digest[:16]
        if branch in existing:
            print(f"Submitted already: {stem}", file=sys.stderr)
            continue
        options.append({"path": DIR + "/" + file.name, "sha256": digest,
                        "count": len(rows), "branch": branch})
    return options


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--github-output", type=Path, required=True)
    parser.add_argument("--fork", default=FORK)
    args = parser.parse_args()
    options = select(args.root / DIR, fork_heads(args.fork))
    chosen = options[0] if options else None
    with args.github_output.open("a", encoding="utf-8") as output:
        output.write("ready=" + ("true" if chosen else "false") + "\n")
        if chosen:
            output.write(f"evidence_path={chosen['path']}\n")
            output.write(f"evidence_sha256={chosen['sha256']}\n")
            output.write(f"candidate_count={chosen['count']}\n")
    print(json.dumps({"ready": bool(chosen), "selected": chosen,
                      "other_approved_batches": max(0, len(options) - 1)}))


if __name__ == "__main__":
    main()
