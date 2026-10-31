#!/usr/bin/env python3
"""Stage original PS5 3.20 and independently catalogued 13.60 exports for review.

Outputs are metadata only. No ABI, behaviour, permission or upstream PR approval
is inferred. Never use these reports directly as publisher input.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess

from ingest_320 import parse_forwarders
from update_progress import PUBLIC_SYMBOL, SENSITIVE_SYMBOL, nid_for

NID = re.compile(r"^[-+A-Za-z0-9_/]{11}$")
SHA = re.compile(r"^[a-f0-9]{40}$")
OWNERS = {"existing_firmware_system_library", "existing_upstream_placeholder_library"}
MISSING = "throwing_stub_candidate_validation_required"
DONE = {"covered_in_saved_upstream_snapshot", "reserved_in_saved_open_pr_snapshot"}
GROUPS = ("dual_3.20_and_13.60", "confirmed_13.60_only", "historical_3.20_only")


def commit(directory: Path) -> str:
    sha = subprocess.check_output(
        ["git", "-C", str(directory), "rev-parse", "HEAD"], text=True).strip()
    if not SHA.fullmatch(sha):
        raise ValueError("Invalid Git source commit: " + str(directory))
    return sha


def identity(library: str, nid: str) -> tuple[str, str]:
    return library.casefold(), nid


def safe_name(name: object, nid: str) -> bool:
    return (isinstance(name, str) and PUBLIC_SYMBOL.fullmatch(name) is not None
            and SENSITIVE_SYMBOL.search(name) is None and nid_for(name) == nid)


def load_320(directory: Path) -> tuple[dict, dict]:
    files = sorted(directory.glob("*.c"))
    if not files:
        raise ValueError("Original 3.20 sources are missing")
    results, stats = {}, Counter()
    for file in files:
        if file.is_symlink():
            raise ValueError("Symlinked source is not permitted")
        observations, rejected = parse_forwarders(
            file.read_text(encoding="utf-8"), file.name)
        stats["source_rejections"] += sum(int(x.get("count", 1)) for x in rejected)
        for row in observations:
            stats["valid_observations"] += 1
            lib, nid, name = row["library"], row["nid"], row["name"]
            if not lib or not NID.fullmatch(nid) or not safe_name(name, nid):
                stats["unknown_owner_or_unverified_name"] += 1
                continue
            k = identity(lib, nid)
            if k in results and results[k]["name"] != name:
                raise ValueError("Conflicting 3.20 name for " + str(k))
            results[k] = {"library": lib, "nid": nid, "name": name,
                          "source_file": file.name}
    stats["files"] = len(files)
    stats["indexed"] = len(results)
    return results, dict(stats)


def load_1360(root: Path) -> tuple[dict, dict]:
    files = sorted((root / "data/firmware-13.60").glob("*.jsonl"))
    if not files:
        raise ValueError("13.60 catalogue shards are missing")
    results, stats = {}, Counter()
    for file in files:
        if file.is_symlink():
            raise ValueError("Symlinked catalogue source is not permitted")
        with file.open(encoding="utf-8") as stream:
            for line in stream:
                if not line.strip():
                    continue
                row = json.loads(line)
                stats["rows_read"] += 1
                if row.get("firmware_13_60_export_confirmed") is not True:
                    continue
                if row.get("kind") != "defined_function_export":
                    continue
                lib, nid = row.get("library"), row.get("nid")
                if (not isinstance(lib, str) or not lib or
                        not isinstance(nid, str) or not NID.fullmatch(nid)):
                    raise ValueError("Malformed 13.60 catalogue identity")
                k = identity(lib, nid)
                if k in results:
                    raise ValueError("Duplicate confirmed 13.60 identity " + str(k))
                results[k] = row
                stats["confirmed_exports"] += 1
    stats["files"] = len(files)
    return results, dict(stats)


def classify(older: dict, current: dict) -> tuple[list[dict], dict]:
    rows, stats = [], Counter()
    for k, record in sorted(current.items()):
        if record.get("stub_assessment") in DONE:
            stats["already_covered_or_reserved_snapshot"] += 1
            continue
        if record.get("stub_assessment") != MISSING:
            stats["not_an_assessed_missing_stub"] += 1
            continue
        name = record.get("name")
        if (record.get("name_status") != "verified_nid_binding"
                or not safe_name(name, k[1])):
            stats["unverified_13.60_name"] += 1
            continue
        if record.get("scope") not in OWNERS:
            stats["unverified_library_ownership"] += 1
            continue
        old = older.get(k)
        if old and old["name"] != name:
            stats["cross_version_name_conflict"] += 1
            continue
        group = GROUPS[0] if old else GROUPS[1]
        stats[group] += 1
        rows.append({
            "library": record["library"], "nid": k[1], "name": name,
            "evidence_class": group, "source_3_20_file": old["source_file"] if old else None,
            "firmware_13_60_export_confirmed": True,
            "signature_verified": False, "behaviour_verified": False,
            "approved_for_auto_submit": False,
            "review_status": "needs_independent_abi_and_live_overlap_evidence"
        })
    for k, record in sorted(older.items()):
        if k in current:
            continue
        stats[GROUPS[2]] += 1
        rows.append({
            "library": record["library"], "nid": k[1], "name": record["name"],
            "evidence_class": GROUPS[2],
            "source_3_20_file": record["source_file"],
            "firmware_13_60_export_confirmed": False,
            "signature_verified": False, "behaviour_verified": False,
            "approved_for_auto_submit": False,
            "review_status": "historical_only_not_13.60_eligible"
        })
    priorities = {group: index for index, group in enumerate(GROUPS)}
    rows.sort(key=lambda row: (priorities[row["evidence_class"]],
                               row["library"].casefold(), row["nid"]))
    return rows, dict(sorted(stats.items()))


def generate(root: Path, original: Path, limit: int) -> tuple[dict, str]:
    if not 1 <= limit <= 200:
        raise ValueError("limit must be 1..200 per source class")
    original_sha, catalogue_sha = commit(original), commit(root)
    old, stats320 = load_320(original)
    current, stats1360 = load_1360(root)
    entries, counts = classify(old, current)
    progress = json.loads((root / "reports/progress.json").read_text())
    src = progress.get("generated_from", {})
    upstream_sha = src.get("anyps5_main_commit")
    if not isinstance(upstream_sha, str) or not SHA.fullmatch(upstream_sha):
        raise ValueError("Unpinned AnyPS5 comparison snapshot")
    scan = src.get("anyps5_open_prs", {})
    overlap_complete = (scan.get("open_pr_coverage_complete") is True and
                        scan.get("open_pr_symbol_coverage_complete") is True)
    sample = []
    selected = Counter()
    for row in entries:
        cls = row["evidence_class"]
        if selected[cls] < limit:
            sample.append(row)
            selected[cls] += 1
    report = {
        "schema_version": 1,
        "review_only": True,
        "automatically_approved": 0,
        "automatically_submitted": 0,
        "sources": {
            "3.20": {"repository": "DNNDHH/PS5-3.20_Libs",
                     "commit": original_sha, "counts": stats320},
            "13.60": {"repository": "xdCloudy/PS5-13.60-Function-Stub-Library",
                      "commit": catalogue_sha, "counts": stats1360},
            "upstream_snapshot_commit": upstream_sha,
            "upstream_open_pr_scan_complete": overlap_complete,
        },
        "classification_counts": counts,
        "sample_per_group": limit,
        "candidates_for_manual_review": sample,
    }
    md = [
        "# Dual-firmware AnyPS5 review candidates", "",
        "Read-only identity/evidence triage. This is NOT approval to generate,",
        "implement, submit, or merge AnyPS5 stubs.", "",
        "Original 3.20 source: DNNDHH/PS5-3.20_Libs @ " + original_sha,
        "13.60 catalogue: xdCloudy/PS5-13.60-Function-Stub-Library @ " + catalogue_sha,
        "AnyPS5 comparison snapshot: " + upstream_sha,
        "Complete upstream open PR snapshot: " + str(overlap_complete), "",
        "## Classification counts", "",
        "| Class | Count |", "|---|---:|",
    ]
    for name, count in sorted(counts.items()):
        md.append("| " + name + " | " + str(count) + " |")
    md += ["", "## Sampled review queues", "",
           "Cross-firmware name matches are NOT ABI, return type or behaviour proof.",
           "3.20-only records must never be silently promoted to 13.60.",
           "All open-PR and main export overlaps must be verified afresh before submission.",
           "Only reviewed records and approval files on trusted main may reach",
           "the pre-existing AnyPS5 draft-PR publisher.", ""]
    for cls in GROUPS:
        group = [row for row in sample if row["evidence_class"] == cls]
        md += ["### " + cls, "",
               "| Library | Symbol | NID | Review requirement |",
               "|---|---|---|---|"]
        for row in group:
            md.append("| {library} | {name} | {nid} | {review_status} |".format(**row))
        md.append("")
    return report, "\n".join(md) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-320", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    parser.add_argument("--limit", type=int, default=75)
    args = parser.parse_args()
    report, md = generate(args.root.resolve(), args.source_320.resolve(), args.limit)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    args.out_md.write_text(md)
    print(json.dumps({"counts": report["classification_counts"],
                      "sample_size": len(report["candidates_for_manual_review"]),
                      "auto_approved": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
