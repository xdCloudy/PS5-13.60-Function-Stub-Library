#!/usr/bin/env python3
"""Refresh manifest SHA-256s without modifying canonical export or name data."""
from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def refresh(root: Path) -> bool:
    path = root / "manifest.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    for entry in document["files"]:
        target = root / entry["path"]
        if not target.is_file():
            raise ValueError(f"Missing manifest file {entry['path']}")
        data = target.read_bytes()
        entry["sha256"] = hashlib.sha256(data).hexdigest()
        entry["bytes"] = len(data)
    readiness = document.get("readiness_file")
    if isinstance(readiness, dict):
        target = root / readiness["path"]
        readiness["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    with (root / "data/library-index.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    total = sum(int(row["records"]) for row in rows)
    named = sum(int(row["resolved_names"]) for row in rows)
    if total != document["counts"]["total_records"]:
        raise ValueError(f"Inventory count mismatch: {total}")
    if named != document["counts"]["resolved_names"]:
        raise ValueError(f"Published names mismatch: {named} != {document['counts']['resolved_names']}")
    with (root / "data/verified-name-map.jsonl").open(encoding="utf-8") as names:
        unique = sum(bool(line.strip()) for line in names)
    if unique != document["unique_verified_name_bindings"]:
        raise ValueError(f"Verified-name-map count mismatch: {unique}")
    serialised = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    current = path.read_text(encoding="utf-8")
    if serialised != current:
        path.write_text(serialised, encoding="utf-8")
        return True
    return False

if __name__ == "__main__":
    print("Manifest refreshed" if refresh(ROOT) else "Manifest already current")
