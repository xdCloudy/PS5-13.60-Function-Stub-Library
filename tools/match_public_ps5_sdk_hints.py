#!/usr/bin/env python3
"""Add public SDK header NAME observations to unapproved AnyPS5 review evidence.

Metadata and links only; never copy third-party header text into output or
interpret a header name match as a verified PS5 13.60 signature or behaviour.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess

SHA = re.compile(r"^[a-f0-9]{40}$")
MACRO = re.compile(r"\b_Fn_\s*\(\s*[^,()\n]{1,110},\s*(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*,")
DECL = re.compile(r"(?m)^[ \t]*(?:extern[ \t]+)?(?:[A-Za-z_][A-Za-z0-9_]*[ \t*]+){1,4}(?P<name>[A-Za-z_][A-Za-z0-9_]*)[ \t]*\(")
REPOSITORIES = (
    ("PS5Dev/PS5SDK", "ps5"),
    ("ps5-payload-dev/sdk", "include/ps5"),
)


def get_sha(root: Path) -> str:
    value = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if not SHA.fullmatch(value):
        raise ValueError("Unpinned public SDK checkout")
    return value


def index_headers(root: Path, subfolder: str) -> dict[str, list[dict]]:
    base = root / subfolder
    if not base.is_dir():
        raise ValueError(f"Missing public SDK headers: {base}")
    index = defaultdict(list)
    files = sorted(p for p in base.rglob("*") if p.suffix in (".h", ".hpp")
                   and p.is_file() and not p.is_symlink())
    if not files:
        raise ValueError("No public SDK header files")
    for path in files:
        # Observations only. This is deliberately NOT a C/C++ signature parser.
        source = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(root).as_posix()
        matched = set()
        for expression in (MACRO, DECL):
            for found in expression.finditer(source):
                name = found.group("name")
                line = source.count("\n", 0, found.start()) + 1
                if (name, line) in matched:
                    continue
                matched.add((name, line))
                index[name].append({"path": rel, "line": line})
    return index


def enrich(queue: list[dict], sources: dict[str, dict]) -> tuple[list[dict], dict]:
    results, counts = [], Counter()
    for record in queue:
        name = record.get("name")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            matches = {}
        else:
            matches = {repo: hits.get(name, [])[:12]
                       for repo, hits in sources.items() if name in hits}
        new = dict(record)
        new["public_sdk_header_name_observations"] = matches
        new["signature_verified"] = False
        new["behaviour_verified"] = False
        new["approved_for_auto_submit"] = False
        new["public_sdk_match_is_abi_proof"] = False
        new["review_required"] = True
        counts["matched_at_least_one_sdk"] += bool(matches)
        counts["no_public_sdk_match"] += not bool(matches)
        results.append(new)
    return results, dict(counts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", required=True, type=Path)
    parser.add_argument("--sdk-ps5dev", required=True, type=Path)
    parser.add_argument("--sdk-payload", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--summary", required=True, type=Path)
    args = parser.parse_args()
    source_folders = (args.sdk_ps5dev, args.sdk_payload)
    sources, revisions = {}, {}
    for (name, subfolder), directory in zip(REPOSITORIES, source_folders):
        revisions[name] = get_sha(directory)
        sources[name] = index_headers(directory, subfolder)
    queue = []
    with args.queue.open(encoding="utf-8") as stream:
        for line in stream:
            if line.strip():
                row = json.loads(line)
                if (row.get("approved_for_auto_submit") is not False
                        or row.get("signature_verified") is not False):
                    raise ValueError("Incoming evidence has unauthorized approval flags")
                queue.append(row)
    if not queue:
        raise ValueError("Empty evidence review input")
    enriched, counts = enrich(queue, sources)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as stream:
        for row in enriched:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
    result = {
        "source_revisions": revisions,
        "public_source_repositories": list(sources),
        "licensing_note": "External SDKs are GPL-licensed; only symbol identifiers and GitHub line references are recorded, not source code.",
        "reviewed_candidate_count": len(enriched),
        "header_name_counts": counts,
        "independently_verified_guest_abi": 0,
        "behaviour_approvals": 0,
        "upstream_pr_submissions": 0,
    }
    args.summary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
