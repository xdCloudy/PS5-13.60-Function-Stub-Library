#!/usr/bin/env python3
"""Apply independently approved *existing-identity* names on a review branch.

Approval records are intentionally separate from public source observations.
This never creates new firmware identities, changes firmware scope, assumes ABI
or approves a withheld/conflicting name. It never commits or pushes directly.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re

from update_progress import PUBLIC_SYMBOL, SENSITIVE_SYMBOL, nid_for, write_if_changed
from stage_catalogue_import import collect

SHA = re.compile(r"^[a-f0-9]{64}$")
PR_REVIEW = re.compile(r"^https://github\.com/[^/]+/[^/]+/pull/\d+(?:#pullrequestreview-\d+)?$")
APPROVAL_FILE = "approvals/catalogue-name-approvals.jsonl"


def records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def fingerprint(candidate: dict) -> str:
    fields = (candidate["library"].casefold(), candidate["nid"],
              candidate["proposed_name"], candidate["source"])
    return hashlib.sha256(json.dumps(fields, separators=(",", ":")).encode()).hexdigest()


def allowed(decision: dict, candidate: dict) -> bool:
    if (decision.get("decision") != "approve_name" or
            decision.get("candidate_fingerprint") != fingerprint(candidate) or
            decision.get("library", "").casefold() != candidate["library"].casefold() or
            decision.get("nid") != candidate["nid"] or
            decision.get("name") != candidate["proposed_name"] or
            not decision.get("redistribution_rights_reviewed") is True or
            not decision.get("library_ownership_reviewed") is True or
            not decision.get("firmware_scope_reviewed") is True or
            not isinstance(decision.get("reviewer"), str) or
            not re.fullmatch(r"[A-Za-z0-9-]{1,39}", decision["reviewer"]) or
            not isinstance(decision.get("review_pr_url"), str) or
            not PR_REVIEW.fullmatch(decision["review_pr_url"]) or
            not isinstance(decision.get("independent_evidence"), str) or
            not decision["independent_evidence"].startswith("https://") or
            candidate["source"] in decision["independent_evidence"] or
            candidate["observed_status"] not in
            {"name_recovery_candidate", "unnamed_catalog_identity"}):
        return False
    return True


def update_preview(root: Path, library: str, index_rows: list[dict]) -> None:
    related = [r for r in index_rows if r["library"].casefold() == library.casefold()]
    if not related:
        raise ValueError("Unknown library index for preview")
    shard = Path(related[0]["file"]).name
    target = root / "libraries" / (Path(shard).stem + ".md")
    if not target.exists():
        raise ValueError(f"Missing per-library documentation {target}")
    rows = []
    for item in related:
        rows.extend(records(root/item["file"]))
    named = sorted((r for r in rows if r.get("name")), key=lambda r:r["nid"])
    original = target.read_text(encoding="utf-8")
    count_total = len(rows)
    prev_named = re.search(r"\| Named \| ([\d,]+) \|", original)
    if not prev_named:
        raise ValueError("Unrecognised per-library Markdown format")
    original = re.sub(r"(\| Export identities \| )[\d,]+( \|)", rf"\g<1>{count_total:,}\g<2>", original, count=1)
    original = re.sub(r"(\| Named \| )[\d,]+( \|)", rf"\g<1>{len(named):,}\g<2>", original, count=1)
    original = re.sub(r"(\| Unresolved or withheld \| )[\d,]+( \|)",
                      rf"\g<1>{count_total-len(named):,}\g<2>", original, count=1)
    heading = "## Named export preview"
    if heading not in original:
        raise ValueError("Missing named-preview heading")
    prefix = original.split(heading, 1)[0]
    preview = [heading, "", "A bounded preview; the inventory file contains the complete library.",
               "", "| NID | Symbol |", "|---|---|"]
    preview.extend(f'| {chr(96)}{r["nid"]}{chr(96)} | {chr(96)}{r["name"]}{chr(96)} |'
                   for r in named[:12])
    write_if_changed(target, prefix + "\n".join(preview) + "\n")


def apply(root: Path, approval_file: Path) -> dict:
    """Generate a reviewed canonical change set; call only from a trusted checkout."""
    decisions = records(approval_file)
    staged = collect(root)
    candidates = {(c["library"].casefold(), c["nid"], c["proposed_name"]): c
                  for c in staged["candidates"]}
    rows = []
    index_path = root/"data/library-index.csv"
    with index_path.open(encoding="utf-8", newline="") as fh:
        index = list(csv.DictReader(fh))
    by_lib = {}
    for item in index:
        by_lib.setdefault(item["library"].casefold(), []).append(item)
    map_path = root/"data/verified-name-map.jsonl"
    existing_map = records(map_path)
    map_by_nid = {}
    for row in existing_map:
        old = map_by_nid.setdefault(row["nid"], row["name"])
        if old != row["name"]:
            raise ValueError("Conflicting preexisting verified-name map")
    rejected, approved = [], []
    seen = set()
    planned_shards = {}
    for decision in decisions:
        key = (str(decision.get("library", "")).casefold(), decision.get("nid"),
               decision.get("name"))
        if key in seen:
            rejected.append({"identity": key[:2], "reason": "duplicate_decision"})
            continue
        seen.add(key)
        candidate = candidates.get(key)
        if candidate is None or not allowed(decision, candidate):
            rejected.append({"identity": key[:2], "reason": "missing_staged_or_independent_approval"})
            continue
        name, nid = candidate["proposed_name"], candidate["nid"]
        if (not PUBLIC_SYMBOL.fullmatch(name) or SENSITIVE_SYMBOL.search(name) or
                nid_for(name) != nid or (nid in map_by_nid and map_by_nid[nid] != name)):
            rejected.append({"identity": key[:2], "reason": "name_hash_publication_or_alias_conflict"})
            continue
        occurrences = []
        for item in by_lib.get(key[0], []):
            path = root/item["file"]
            contents = planned_shards.setdefault(path, records(path))
            occurrences.extend((row, path) for row in contents if row["nid"] == nid)
        if len(occurrences) != 1:
            rejected.append({"identity": key[:2], "reason": "unknown_or_ambiguous_canonical_identity"})
            continue
        row, path = occurrences[0]
        if (row.get("name_status") == "withheld_by_publication_filter" or
                row.get("name") not in (None, name) or
                row.get("scope") in (None, "unknown") or
                row.get("firmware_13_60_export_confirmed") not in (True, False)):
            rejected.append({"identity": key[:2], "reason": "name_conflict_withheld_or_unverified_scope"})
            continue
        if row.get("name") == name:
            rejected.append({"identity": key[:2], "reason": "already_named_no_change"})
            continue
        row["name"] = name
        row["name_status"] = "verified_nid_binding"
        row["source_evidence"] = sorted(set(row.get("source_evidence", []) +
                                            ["independently_reviewed_public_symbol"]))
        approved.append({"library": row["library"], "nid": nid, "name": name,
                         "scope": row["scope"], "source": candidate["source"],
                         "review_pr_url": decision["review_pr_url"]})
        map_by_nid[nid] = name
    changed_libraries = {r["library"].casefold() for r in approved}
    if approved:
        for path, content in planned_shards.items():
            if path.name not in {Path(row["file"]).name for lib in changed_libraries
                                 for row in by_lib[lib]}:
                continue
            write_if_changed(path, "".join(json.dumps(x, sort_keys=True,
                                                      separators=(",", ":"), ensure_ascii=False) + "\n"
                                           for x in content))
        verified = [{"name": name, "nid": nid}
                    for nid, name in sorted(map_by_nid.items())]
        write_if_changed(map_path, "".join(json.dumps(x, sort_keys=True,
                                                      separators=(",", ":")) + "\n"
                                           for x in verified))
        for item in index:
            if item["library"].casefold() in changed_libraries:
                item["resolved_names"] = str(sum(bool(x.get("name"))
                        for x in records(root/item["file"])))
        out = io.StringIO()
        writer = csv.DictWriter(out, fieldnames=list(index[0]))
        writer.writeheader()
        writer.writerows(index)
        write_if_changed(index_path, out.getvalue())
        libdoc = root/"LIBRARIES.md"
        summary = libdoc.read_text(encoding="utf-8")
        for lib in changed_libraries:
            for item in by_lib[lib]:
                marker = re.escape("libraries/"+Path(item["file"]).stem+".md")
                matching = [line for line in summary.splitlines() if re.search(marker, line)]
                if len(matching) != 1:
                    raise ValueError("Ambiguous library overview row")
                rowline = matching[0]
                total = sum(int(i["records"]) for i in by_lib[lib])
                named = sum(int(i["resolved_names"]) for i in by_lib[lib])
                fields = rowline.split("|")
                fields[2], fields[3] = f" {total:,} ", f" {named:,} "
                summary = summary.replace(rowline, "|".join(fields))
            update_preview(root, by_lib[lib][0]["library"], index)
        write_if_changed(libdoc, summary)
        readiness_file = root/"readiness.json"
        readiness = json.loads(readiness_file.read_text(encoding="utf-8"))
        named_total = sum(int(r["resolved_names"]) for r in index)
        readiness["named_library_stub_records"] = named_total
        readiness["named_stub_identities"] = len(verified)
        readiness["unresolved_or_withheld_records"] = readiness["total_export_records"] - named_total
        for item in readiness["libraries"]:
            if item["library"].casefold() in changed_libraries:
                item["named"] = sum(int(x["resolved_names"]) for x in by_lib[item["library"].casefold()])
        write_if_changed(readiness_file, json.dumps(readiness, indent=2, ensure_ascii=False)+"\n")
        manifest_path = root/"manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["counts"]["resolved_names"] = named_total
        manifest["counts"]["unresolved_or_withheld_names"] = manifest["counts"]["total_records"] - named_total
        manifest["unique_verified_name_bindings"] = len(verified)
        write_if_changed(manifest_path, json.dumps(manifest, indent=2, ensure_ascii=False)+"\n")
        from refresh_manifest import refresh
        refresh(root)
    return {"approved": approved, "rejected": rejected,
            "total_decisions": len(decisions), "canonical_names_added": len(approved),
            "canonical_identity_count_change": 0,
            "approved_only_from_trusted_manual_decisions": True}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--decisions", type=Path, default=Path(APPROVAL_FILE))
    p.add_argument("--report", type=Path, default=Path("reports/approved-import-ledger.json"))
    args = p.parse_args()
    document = apply(args.root.resolve(), args.decisions.resolve())
    write_if_changed(args.report.resolve(), json.dumps(document, sort_keys=True, indent=2)+"\n")
    print(json.dumps({"approved": len(document["approved"]), "rejected": len(document["rejected"])}))
