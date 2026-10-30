#!/usr/bin/env python3
"""Stage deduplicated, review-only catalogue import proposals from source evidence.

This is NOT a canonical-data promotion tool. Only separately reviewed changes
may update immutable firmware shards, the verified-name map and manifest.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

from update_progress import PUBLIC_SYMBOL, SENSITIVE_SYMBOL, nid_for, write_if_changed

SOURCE_320 = "DNNDHH/PS5-3.20_Libs"
SOURCE_ANY = "boykopovar/AnyPS5"
SHA = re.compile(r"^[0-9a-f]{40}$")
NID = re.compile(r"^[A-Za-z0-9_+\-/]{11}$")
ALLOWED_320 = {"historical_only_candidate", "name_recovery_candidate"}
ALLOWED_ANY = {"unnamed_catalog_identity"}
SCHEMA_VERSION = 1


def safe(value: dict, *, kind: str, source_sha: str) -> dict | None:
    if value.get("canonical_name_approved") is not False:
        return None
    if kind == "3.20":
        if value.get("status") not in ALLOWED_320 or value.get("source") != SOURCE_320:
            return None
        name = value.get("proposed_name")
        library = value.get("library")
        origin = value.get("source_file")
        nid = value.get("nid")
        if value.get("source_commit") != source_sha:
            return None
    else:
        if value.get("match_status") not in ALLOWED_ANY or value.get("source") != SOURCE_ANY:
            return None
        name = value.get("proposed_name")
        library = value.get("library")
        origin = value.get("source_file")
        nid = value.get("nid")
        if value.get("source_commit") != source_sha:
            return None
    if (not isinstance(name, str) or not PUBLIC_SYMBOL.fullmatch(name) or
        SENSITIVE_SYMBOL.search(name) or not isinstance(library, str) or
        not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]{0,120}", library) or
        not isinstance(nid, str) or not NID.fullmatch(nid) or nid_for(name) != nid or
        not isinstance(origin, str) or not re.fullmatch(r"[A-Za-z0-9_./-]{1,220}", origin) or
        ".." in Path(origin).parts):
        return None
    if kind == "3.20" and not origin.endswith(".c"):
        return None
    if kind != "3.20" and not origin.startswith("core/libs/prx/"):
        return None
    return {"library": library, "nid": nid, "proposed_name": name,
            "source": SOURCE_320 if kind == "3.20" else SOURCE_ANY,
            "source_file": origin, "source_commit": source_sha,
            "observed_status": value["status" if kind == "3.20" else "match_status"],
            "canonical_name_approved": False,
            "firmware_13_60_export_confirmed_by_this_source": False,
            "signature_verified": False, "runtime_validated": False}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def collect(root: Path) -> dict:
    src_file = root / "reports/source-320.json"
    progress_file = root / "reports/progress.json"
    if not src_file.is_file() or not progress_file.is_file():
        raise ValueError("Missing source input; run upstream reconciliation first")
    src = json.loads(src_file.read_text(encoding="utf-8"))
    progress = json.loads(progress_file.read_text(encoding="utf-8"))
    source_sha = src.get("inputs", {}).get("source_commit")
    any_sha = progress.get("generated_from", {}).get("anyps5_main_commit")
    if not isinstance(source_sha, str) or not SHA.fullmatch(source_sha):
        raise ValueError("Missing trusted 3.20 SHA")
    if not isinstance(any_sha, str) or not SHA.fullmatch(any_sha):
        raise ValueError("Missing trusted AnyPS5 SHA")
    expected_manifest = src.get("inputs", {}).get("catalogue_manifest_sha256")
    actual_manifest = hashlib.sha256((root / "manifest.json").read_bytes()).hexdigest()
    if expected_manifest != actual_manifest:
        raise ValueError("Stale importer snapshot: catalogue manifest differs")
    proposals = []
    for item in load_jsonl(root / "reports/source-320-review.jsonl"):
        x = safe(item, kind="3.20", source_sha=source_sha)
        if x:
            proposals.append(x)
    for item in load_jsonl(root / "reports/upstream-source-candidates.jsonl"):
        x = safe(item, kind="AnyPS5", source_sha=any_sha)
        if x:
            proposals.append(x)
    grouped = defaultdict(set)
    for item in proposals:
        grouped[(item["library"].casefold(), item["nid"])].add(item["proposed_name"])
    conflicts = sorted([{"library": key[0], "nid": key[1], "reason": "source_name_conflict"}
                        for key, names in grouped.items() if len(names) > 1],
                       key=lambda x:(x["library"],x["nid"]))
    accepted = sorted((item for item in proposals
                       if len(grouped[(item["library"].casefold(),item["nid"])]) == 1),
                      key=lambda x:(x["library"].casefold(),x["nid"],x["source"]))
    # Exact duplicates (same source and same library/NID) are not new candidates.
    unique = list({(x["source"], x["library"].casefold(), x["nid"]):x for x in accepted}.values())
    unique.sort(key=lambda x:(x["library"].casefold(),x["nid"],x["source"]))
    identities = {(x["library"].casefold(),x["nid"]) for x in unique}
    return {
        "schema_version": SCHEMA_VERSION,
        "source_revision_320": source_sha,
        "source_revision_anyps5": any_sha,
        "canonical_manifest_sha256": actual_manifest,
        "reviewable_identity_count": len(identities),
        "evidence_observations": len(unique),
        "conflicts": conflicts,
        "candidates": unique,
        "publication_status": "DRAFT_REVIEW_ONLY",
        "independent_approval_required": True,
        "canonical_records_mutated": 0,
        "note": "These records are name or historical-reference proposals only; no ABI, runtime, source licence or 13.60 confirmation is inferred."
    }


def write(root: Path, output: Path) -> dict:
    proposal = collect(root)
    # Do not publish a branch/PR with no proposed canonical work.
    if proposal["reviewable_identity_count"] == 0:
        if output.exists():
            output.unlink()
        return proposal
    write_if_changed(output, json.dumps(proposal,indent=2,sort_keys=True) + "\n")
    return proposal


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output",type=Path,default=Path("catalogue-import-proposal.json"))
    args=parser.parse_args()
    proposal=write(args.root.resolve(),args.output.resolve())
    print(json.dumps({k:proposal[k] for k in ("reviewable_identity_count",
                                               "evidence_observations",
                                               "canonical_records_mutated")}))
