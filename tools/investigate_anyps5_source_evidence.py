#!/usr/bin/env python3
"""Cross-check an unapproved dual-firmware export queue against live AnyPS5 source.

Results are read-only evidence observations. No declaration, return type,
behaviour, ABI correctness or upstream pull request availability is inferred.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess

PATTERN = re.compile(r"\bAPS5_VABI[ \t]+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[ \t]*\(")
EXPORT = re.compile(r'\bAPS5_EXPORT\s*\(\s*"(?P<nid>[-+A-Za-z0-9_/]{11})"')
HEX = re.compile(r"^[0-9a-f]{40}$")
NID = re.compile(r"^[-+A-Za-z0-9_/]{11}$")


def sha(root: Path) -> str:
    result = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if not HEX.fullmatch(result):
        raise ValueError("AnyPS5 source revision is not a Git commit")
    return result


def read_queue(path: Path) -> list[dict]:
    records, seen = [], set()
    with path.open(encoding="utf-8") as source:
        for lineno, line in enumerate(source, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            owner = record.get("library")
            nid = record.get("nid")
            if (not isinstance(owner, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]*", owner)
                    or not isinstance(nid, str) or not NID.fullmatch(nid)
                    or record.get("candidate_only") is True
                    or record.get("approved_for_auto_submit") is not False
                    or record.get("signature_verified") is not False
                    or record.get("behaviour_verified") is not False):
                raise ValueError(f"Unsafe or prematurely approved queue row {lineno}")
            key = (owner.casefold(), nid)
            if key in seen:
                raise ValueError(f"Duplicated library/NID in unapproved queue: {key}")
            seen.add(key)
            records.append(record)
    if not records:
        raise ValueError("No review queue entries")
    return records


def scan(root: Path, required: set[str]) -> dict[str, dict[str, list[dict]]]:
    """Read ALL upstream providers, including .native variants and aliases.

    required remains an API parameter for compatibility but deliberately does
    not filter providers. Cross-library source evidence prevents a second host
    stub from being recommended for a symbol already implemented elsewhere.
    """
    library_root = root / "core/libs/prx"
    if not library_root.is_dir():
        raise ValueError("AnyPS5 core/libs/prx does not exist")
    providers: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for folder in sorted(library_root.iterdir()):
        if not folder.is_dir() or folder.is_symlink():
            continue
        owner = folder.name.casefold()
        for file in sorted(folder.rglob("*")):
            if (not file.is_file() or file.is_symlink() or file.suffix not in
                    (".hpp", ".h", ".cpp", ".cc", ".cxx")):
                continue
            source = file.read_text(encoding="utf-8", errors="replace")
            rel = file.relative_to(root).as_posix()
            # Header declarations or source definitions are hints, never ABI approval.
            for match in PATTERN.finditer(source):
                providers[owner][match.group("name")].append({
                    "source_path": rel, "observation": "APS5_VABI_symbol",
                })
            for match in EXPORT.finditer(source):
                providers[owner][match.group("nid")].append({
                    "source_path": rel, "observation": "APS5_EXPORT_literal_nid",
                })
    return providers


def reconcile(records: list[dict], providers: dict) -> tuple[list[dict], dict]:
    results, counts = [], Counter()
    for row in records:
        owner = row["library"].casefold()
        within = providers.get(owner, {})
        in_owner = within.get(row["name"], []) + within.get(row["nid"], [])
        other = []
        for provider, exported in providers.items():
            if provider == owner:
                continue
            for observation in exported.get(row["name"], []) + exported.get(row["nid"], []):
                other.append({**observation, "provider": provider})
        local_unique = sorted({
            (e["source_path"], e["observation"], owner) for e in in_owner
        })
        cross_unique = sorted({
            (e["source_path"], e["observation"], e["provider"]) for e in other
        })
        # A declaration is not necessarily a linked export. Source matches in
        # another provider may reflect a valid alias or an intended conflict.
        if local_unique:
            state = "upstream_source_symbol_observed"
        elif cross_unique:
            state = "upstream_other_library_source_symbol_observed"
        else:
            state = "no_direct_upstream_source_observation"
        counts[state] += 1
        data = dict(row)
        data["live_main_source_scan"] = state
        data["upstream_source_observations"] = [
            {"path": path, "kind": kind, "provider": provider}
            for path, kind, provider in (local_unique + cross_unique)[:30]
        ]
        data["review_required"] = True
        data["approved_for_auto_submit"] = False
        data["signature_verified"] = False
        data["behaviour_verified"] = False
        # Conservatively flag explicit source symbols, but do not infer
        # absence from no direct observations (macros may expand exports).
        data["safe_to_submit_without_further_evidence"] = False
        results.append(data)
    return results, dict(sorted(counts.items()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    root = args.upstream.resolve()
    head = sha(root)
    records = read_queue(args.queue)
    names = {r["library"].casefold() for r in records}
    providers = scan(root, names)
    reviewed, counts = reconcile(records, providers)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as output:
        for row in reviewed:
            output.write(json.dumps(row, sort_keys=True) + "\n")
    summary = {
        "schema_version": 1,
        "anyps5_main_source_commit": head,
        "total_unapproved_candidates": len(reviewed),
        "direct_source_observations": counts,
        "all_upstream_library_providers_checked": True,
        "cross_library_names_are_not_inferred_safe": True,
        "open_pull_request_scan_performed_here": False,
        "signature_or_behaviour_approvals": 0,
        "upstream_prs_opened": 0,
        "publication_gate": "requires source and cross-library absence, verified identity, no PR overlap, and maintainer-accepted fail-fast convention before publication",
    }
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
