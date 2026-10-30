#!/usr/bin/env python3
"""Deterministic, data-only reconciliation of public PS5 3.20 forwarding symbols.

A hash-compatible name is a proposal, not firmware or ABI verification. This
module never writes canonical inventory; promotions need a separate reviewed PR.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from update_progress import (
    PUBLIC_SYMBOL, SENSITIVE_SYMBOL, load_inventory, nid_for, write_if_changed,
)

# Match the actual pointer argument in each registration. File order is irrelevant.
DLSYM = re.compile(
    r'\bsprx_dlsym\s*\(\s*[^,()]+\s*,\s*"(?P<nid>[-+A-Za-z0-9_/]{11})"'
    r'\s*,\s*&\s*__ptr_(?P<symbol>[A-Za-z_]\w*)\s*\)',
    re.MULTILINE,
)
DLOPEN = re.compile(r'\bsprx_dlopen\s*\(\s*"(?P<library>[A-Za-z_][\w.]*)"')
SYMBOL = re.compile(r"^[A-Za-z_]\w*$")
SCHEMA = 1
SOURCE_NAME = "DNNDHH/PS5-3.20_Libs"


def parse_forwarders(source: str, source_file: str) -> tuple[list[dict], list[dict]]:
    """Bind exact dlsym NIDs to pointer names; reject ambiguous owners/symbols.

    We require matching pointers and explicit assembly labels to avoid inferring
    C functions from unrelated registrations or from their position in the file.
    """
    owners = set(DLOPEN.findall(source))
    if len(owners) != 1:
        return [], [{"source_file": source_file, "reason": "ambiguous_or_missing_library",
                     "owner_count": len(owners)}]
    library = next(iter(owners))
    declared = set(re.findall(r'\bvoid\s*\*\s*__ptr_([A-Za-z_]\w*)\s*;', source))
    # Generated .global lines are inside string literals; literal text is sufficient.
    exported = set(re.findall(r'\.global\s+([A-Za-z_]\w*)\\n', source))
    observations, rejected = [], []
    for match in DLSYM.finditer(source):
        symbol, nid = match["symbol"], match["nid"]
        common = {"library": library, "nid": nid, "source_file": source_file}
        if symbol not in declared or symbol not in exported:
            rejected.append({**common, "reason": "missing_pointer_or_export_label"})
        elif nid_for(symbol) != nid:
            rejected.append({**common, "reason": "nid_name_hash_mismatch"})
        else:
            observations.append({**common, "name": symbol})
    # Registration not parseable? A nonempty source with dlsym calls but no
    # matches is NOT accepted as an empty source inventory.
    possible = len(re.findall(r'\bsprx_dlsym\s*\(', source))
    if possible > len(observations) + len(rejected):
        rejected.append({"source_file": source_file,
                         "reason": "unparsed_dlsym_registration",
                         "count": possible - len(observations) - len(rejected)})
    return observations, rejected


def classify(observations: list[dict], known: dict) -> tuple[list[dict], dict]:
    """Preserve all library/NID ownership and withhold sensitive names."""
    global_nids = defaultdict(set)
    for (owner, nid) in known:
        global_nids[nid].add(owner)
    grouped = defaultdict(set)
    for o in observations:
        grouped[(o["library"].casefold(), o["nid"])].add(o["name"])
    counts = Counter()
    proposals = []
    per_library = defaultdict(Counter)
    for o in sorted(observations, key=lambda x:
                    (x["library"].casefold(), x["nid"], x["name"], x["source_file"])):
        key = (o["library"].casefold(), o["nid"])
        record = known.get(key)
        status = "already_indexed_and_named"
        existing_name = record.get("name") if record else None
        if len(grouped[key]) > 1:
            status = "conflicting_source_names"
        elif record and record.get("name_status") == "withheld_by_publication_filter":
            status = "withheld"
        elif not PUBLIC_SYMBOL.fullmatch(o["name"]) or SENSITIVE_SYMBOL.search(o["name"]):
            status = "withheld"
        elif not record:
            status = "historical_only_candidate"
        elif existing_name and existing_name != o["name"]:
            status = "conflicting_name_binding"
        elif not existing_name:
            status = "name_recovery_candidate"
        elif record.get("name_status") != "verified_nid_binding":
            status = "existing_name_needs_independent_review"
        counts[status] += 1
        per_library[o["library"]][status] += 1
        if status == "already_indexed_and_named":
            continue
        item = {"library": o["library"], "nid": o["nid"],
                "source_file": o["source_file"], "status": status,
                "firmware_13_60_export_confirmed": bool(
                    record and record.get("firmware_13_60_export_confirmed")),
                "canonical_name_approved": False,
                "abi_verified": False, "runtime_validated": False,
                "source": SOURCE_NAME}
        # Public candidate names are allowed only when publication filter passes.
        if status not in ("withheld",):
            item["proposed_name"] = o["name"]
        if status == "historical_only_candidate" and o["nid"] in global_nids:
            item["cross_library_nid_alias_review"] = True
        proposals.append(item)
    return proposals, {"statuses": dict(sorted(counts.items())),
                        "per_library": {k: dict(sorted(v.items()))
                                        for k, v in sorted(per_library.items())},
                        "total_valid_registrations": len(observations)}


def ingest(root: Path, source_dir: Path, force: bool = False) -> dict:
    root, source_dir = root.resolve(), source_dir.resolve()
    if not (source_dir / ".git").exists():
        raise ValueError("3.20 input must be a git checkout with a recorded revision")
    head = subprocess.check_output(
        ["git", "-C", str(source_dir), "rev-parse", "HEAD"], text=True).strip()
    if not re.fullmatch("[0-9a-f]{40}", head):
        raise ValueError("Invalid source revision")
    manifest = root / "manifest.json"
    manifest_hash = hashlib.sha256(manifest.read_bytes()).hexdigest()
    report_path = root / "reports" / "source-320.json"
    queue_path = root / "reports" / "source-320-review.jsonl"
    files = sorted(p for p in source_dir.rglob("*.c")
                   if ".git" not in p.relative_to(source_dir).parts)
    if not files:
        raise ValueError("No upstream .c sources found")
    # A content digest catches local edits even if HEAD is unchanged.
    hashes = [(p.relative_to(source_dir).as_posix(),
               hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
    source_digest = hashlib.sha256(json.dumps(hashes).encode()).hexdigest()
    inputs = {"source_commit": head, "source_content_sha256": source_digest,
              "catalogue_manifest_sha256": manifest_hash, "parser_schema": SCHEMA}
    if report_path.is_file() and not force:
        previous = json.loads(report_path.read_text(encoding="utf-8"))
        if previous.get("inputs") == inputs and queue_path.exists():
            return previous
    known, *rest = load_inventory(root)
    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    expected = manifest_data["counts"]["total_records"]
    # load_inventory returns rows counted in rest[-2].
    if rest[-2] != expected:
        raise ValueError("Manifest/canonical row counts disagree")
    observations, rejected = [], []
    for p in files:
        rel = p.relative_to(source_dir).as_posix()
        obs, errors = parse_forwarders(p.read_text(encoding="utf-8", errors="replace"), rel)
        observations.extend(obs)
        rejected.extend(errors)
    proposed, summary = classify(observations, known)
    # Never publish raw names from quarantined cases. Public source paths and
    # statuses are the only fields retained in error rows.
    safe_errors = []
    for error in rejected:
        safe_errors.append({k: v for k, v in error.items()
                            if k in {"source_file", "library", "nid", "reason",
                                     "owner_count", "count"}})
    for p in proposed:
        p["source_commit"] = head
    queue = proposed + sorted(safe_errors, key=lambda x:
                              (x.get("source_file", ""), x.get("nid", ""), x["reason"]))
    summary.update({
        "schema_version": SCHEMA,
        "inputs": inputs,
        "source": SOURCE_NAME,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_files_scanned": len(files),
        "source_file_sha256": dict(hashes),
        "quarantined_registrations": len(rejected),
        "review_queue_records": len(queue),
        "canonical_rows_modified": 0,
        "publication_gate": "manual review required before canonical promotion",
        "limitations": [
            "3.20 symbol presence does not confirm a 13.60 firmware export.",
            "Independent hash verification does not verify the C ABI or runtime behavior.",
            "Unresolved owner, conflicting names and unsafe names remain unpromoted.",
            "No C forwarding source, binary content or function body is published."
        ],
    })
    write_if_changed(report_path, json.dumps(summary, sort_keys=True, indent=2) + "\n")
    write_if_changed(queue_path, "".join(json.dumps(x, sort_keys=True) + "\n"
                                        for x in queue))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    report = ingest(args.root, args.source_dir, args.force)
    print(json.dumps({key: report[key] for key in
                      ("source_files_scanned", "total_valid_registrations",
                       "quarantined_registrations", "statuses",
                       "review_queue_records", "canonical_rows_modified")}, indent=2))


if __name__ == "__main__":
    main()
