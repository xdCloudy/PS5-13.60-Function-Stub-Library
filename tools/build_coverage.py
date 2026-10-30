#!/usr/bin/env python3
"""Generate all coverage matrices and a static dashboard feed from canonical data.

No guessed ABI/implementation status, no mutation of inventory or source code.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

from update_progress import nid_for, write_if_changed


def build(root: Path) -> dict:
    root = root.resolve()
    progress = json.loads((root / "reports/progress.json").read_text(encoding="utf-8"))
    source_file = root / "reports/source-320.json"
    historical = json.loads(source_file.read_text(encoding="utf-8")) if source_file.exists() else None
    anyps5_states_file = root / "reports/anyps5-symbol-states.json"
    anyps5_states = (json.loads(anyps5_states_file.read_text(encoding="utf-8"))
                    if anyps5_states_file.exists() else None)
    stats = defaultdict(Counter)
    scopes = Counter()
    for part in ("firmware-13.60", "historical-3.20-only"):
        for path in sorted((root / "data" / part).glob("*.jsonl")):
            with path.open(encoding="utf-8") as fd:
                for line in fd:
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    lib = record["library"]
                    row = stats[lib]
                    row["indexed"] += 1
                    row["firmware" if part == "firmware-13.60" else "historical"] += 1
                    if record.get("name"):
                        row["named"] += 1
                    if (record.get("name") and record.get("name_status") == "verified_nid_binding"
                            and nid_for(record["name"]) == record["nid"]):
                        row["strict"] += 1
                    if record.get("name_status") == "withheld_by_publication_filter":
                        row["withheld"] += 1
                    if record.get("name_status") == "conflicting":
                        row["conflicted"] += 1
                    scopes[record["scope"]] += 1
                    row["scope:" + record["scope"]] += 1
    upstream = {r["library"].casefold(): r for r in progress["libraries"]}
    sources = (historical or {}).get("per_library", {})
    sources = {name.casefold(): item for name, item in sources.items()}
    state_by_library = (anyps5_states or {}).get("per_library", {})
    rows = []
    for library, count in sorted(stats.items(), key=lambda entry: (-entry[1]["indexed"], entry[0])):
        up = upstream.get(library.casefold(), {})
        ref = sources.get(library.casefold(), {})
        observed_states = state_by_library.get(library.casefold(), {})
        source_total = sum(ref.values()) if historical else None
        main = up.get("upstream_main_catalogue_source_matches", 0)
        reserved = up.get("open_pr_added_matches", 0)
        qualified = up.get("qualified_records", 0)
        # Priority is a triage ranking, not permission to generate stubs.
        eligible_scope = count.get("scope:existing_firmware_system_library", 0) + count.get(
            "scope:existing_upstream_placeholder_library", 0)
        score = round((min(qualified, count["strict"]) - min(qualified, main + reserved))
                      * (1 if eligible_scope else 0), 2)
        row = {
            "library": library, "indexed": count["indexed"],
            "firmware_13_60": count["firmware"], "historical_only": count["historical"],
            "named": count["named"], "strict_verified": count["strict"],
            "unresolved": count["indexed"] - count["named"],
            "withheld": count["withheld"], "conflicted": count["conflicted"],
            "source_320_references": source_total,
            "anyps5_main_definitions": main, "anyps5_open_pr_matches_partial": reserved,
            "anyps5_declarations_without_definitions": observed_states.get("declaration_without_visible_definition", 0),
            "anyps5_source_nonthrowing_unvalidated": observed_states.get("definition_nonthrowing_unvalidated", 0),
            "anyps5_source_throwing": observed_states.get("definition_throwing", 0),
            "qualified_assessed": qualified,
            "name_recovery_candidates_320": ref.get("name_recovery_candidate", 0),
            "new_historical_candidates_320": ref.get("historical_only_candidate", 0),
            "score_triage_only": max(0, score),
            "ownership_scope_counts": {k[6:]: v for k,v in count.items() if k.startswith("scope:")},
        }
        rows.append(row)
    inv, st = progress["inventory"], progress["stubs"]
    total = inv["records"]
    pr = progress["generated_from"]["anyps5_open_prs"]
    matrix = {
        "schema_version": 1,
        "generated_at_utc": progress["generated_from"]["generated_at_utc"],
        "source_revisions": {
            "anyps5_main": progress["generated_from"].get("anyps5_main_commit"),
            "ps5_320": (historical or {}).get("inputs", {}).get("source_commit"),
        },
        "denominators": {
            "indexed_records": total,
            "verified_name_rate": "strictly rehashed named / all indexed library+NID records",
            "anyps5_main": "matched definitions / indexed library+NID records, not functionality",
            "pr_scan": "current open PR heads successfully scanned / all currently open PRs",
            "library_320": "registered 3.20 forwarder bindings observed in source, not 13.60 exports",
        },
        "discovery": {
            "indexed": total,
            "confirmed_13_60": inv["firmware_13_60"],
            "historical_only": inv["historical_only"],
            "published_named": inv["published_named_records"],
            "strictly_verified_names": inv["strictly_reverified_named_records"],
            "named_pending_strict_check": inv["named_records_not_passed_by_strict_gate"],
            "unnamed_or_withheld": total - inv["published_named_records"],
            "publication_withheld": sum(row["withheld"] for row in rows),
            "conflicted_flagged": sum(row["conflicted"] for row in rows),
        },
        "readiness": {
            "qualified_unique_nids": st["qualified_unique_nids_recomputed"],
            "strict_qualified_unique_nids": st["strictly_rehashed_qualified_unique_nids"],
            "anyps5_main_definition_matches": st["anyps5_main_tracked_source_records_live"],
            "anyps5_throwing_marker": st["anyps5_main_throwing_marker_records_live"],
            "anyps5_nonthrowing_body": st["anyps5_main_nonthrowing_source_records_live"],
            "open_pr_qualified_partial": st["qualified_unique_nids_matched_in_open_pr_additions"],
            "snapshot_locally_prepared_stubs": st["statically_prepared_saved_snapshot"],
            "snapshot_fully_validated_stubs": st["fully_validated_saved_snapshot"],
            "build_verified_live": None, "abi_verified_live": None,
            "runtime_validated_live": None, "fully_implemented_live": None,
        },
        "ownership": dict(sorted(scopes.items())),
        "automation_health": {
            "last_refresh_utc": progress["generated_from"]["generated_at_utc"],
            "pr_scanned": pr["open_pr_scanned"], "pr_total": pr["open_pr_total"],
            "pr_complete": pr["open_pr_coverage_complete"],
            "pr_errors": pr["open_pr_errors"],
            "anyps5_symbol_observations": (anyps5_states or {}).get("observed_library_nid_records"),
            "anyps5_declarations_only": (anyps5_states or {}).get("states", {}).get("declaration_without_visible_definition"),
            "anyps5_export_registration_verified": None,
            "source_320_files": (historical or {}).get("source_files_scanned"),
            "source_320_registrations": (historical or {}).get("total_valid_registrations"),
            "source_320_conflicts_quarantined": (historical or {}).get("quarantined_registrations"),
            "source_320_review_items": (historical or {}).get("review_queue_records"),
            "source_320_canonical_auto_changes": (historical or {}).get("canonical_rows_modified"),
            "source_320_statuses": (historical or {}).get("statuses", {}),
            "anyps5_public_source_proposals": st["auto_imported_public_source_name_proposals"],
            "anyps5_withheld_names": st["source_names_withheld_by_safety_filter"],
            "overlap_publication_safe": False,  # Requires complete, final live scan.
        },
        "libraries": rows,
        "limitations": [
            "An absent PR match is unknown while PR scanning is incomplete.",
            "The 3.20-only source is not evidence of a firmware 13.60 export.",
            "Source definitions are not proof of registration, ABI, build or runtime verification.",
            "Live implementation correctness is not measured; null means unknown.",
            "Priority score indicates triage value, not safe stub-generation eligibility."
        ],
    }
    # Append an actual observed point only when source-backed metrics or PR
    # scan coverage change. Repeated identical refreshes do not create trends.
    history_path = root / "reports/coverage-history.json"
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    entry = {
        "observed_at_utc": matrix["generated_at_utc"],
        "indexed": total,
        "strictly_verified_names": inv["strictly_reverified_named_records"],
        "qualified_unique_nids": st["qualified_unique_nids_recomputed"],
        "anyps5_main_matches": st["anyps5_main_tracked_source_records_live"],
        "open_pr_scanned": pr["open_pr_scanned"],
        "anyps5_commit": matrix["source_revisions"]["anyps5_main"],
        "ps5_320_commit": matrix["source_revisions"]["ps5_320"],
    }
    if not history or {k:v for k,v in history[-1].items() if k != "observed_at_utc"} != {
            k:v for k,v in entry.items() if k != "observed_at_utc"}:
        history.append(entry)
    history = history[-120:]
    matrix["trends"] = history
    write_if_changed(history_path, json.dumps(history, indent=2, sort_keys=True) + "\n")
    report = json.dumps(matrix, indent=2, sort_keys=True) + "\n"
    write_if_changed(root / "reports/coverage-matrices.json", report)
    write_if_changed(root / "site/data.json", report)
    write_if_changed(root / "reports/coverage-matrices.md", render_markdown(matrix))
    return matrix


def number(v):
    return f"{v:,}" if isinstance(v, int) else "unknown" if v is None else str(v)


def render_markdown(doc):
    d, r, h = doc["discovery"], doc["readiness"], doc["automation_health"]
    lines = ["# Coverage matrices", "",
             "All figures come from the canonical inventory and generated source observations. "
             "A known function is not necessarily a working function.", "",
             f"**Last refresh:** {doc['generated_at_utc']} (scheduled polling, not instantaneous).", "",
             "## A. Discovery", "",
             "| Stage | Count | Meaning |", "|---|---:|---|"]
    descriptions = {
        "indexed": "Known logical library/NID records",
        "confirmed_13_60": "Recorded as exports in the extraction labeled firmware 13.60",
        "historical_only": "Known from 3.20 evidence, not established for 13.60",
        "published_named": "Records with a published proposed/recovered name",
        "strictly_verified_names": "Name and status pass a strict NID recomputation check",
        "named_pending_strict_check": "Named records not passing the strict status/hash gate",
        "unnamed_or_withheld": "No published name associated with the record",
        "publication_withheld": "Explicitly withheld by the publication filter",
        "conflicted_flagged": "Explicit conflict status in canonical inventory",
    }
    for key, value in d.items():
        lines.append(f"| {key.replace('_',' ').capitalize()} | {number(value)} | {descriptions.get(key,'')} |")
    lines += ["", "## B. Per-library source comparison", "",
              "3.20 references are registered forwarders, not necessarily 13.60 exports. "
              "Open-PR counts are only observed matches; absence is not clearance.", "",
              "| Library | 13.60 exports | 3.20 references | Named | Strict verified | AnyPS5 main definitions | Open PR matches (partial) | Unnamed |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for row in doc["libraries"]:
        values = [row["library"].replace("|", "/")] + [
            number(row[k]) for k in ("firmware_13_60", "source_320_references",
                                    "named", "strict_verified", "anyps5_main_definitions",
                                    "anyps5_open_pr_matches_partial", "unresolved")]
        lines.append("| " + " | ".join(values) + " |")
    lines += ["", "## C. Readiness stages", "",
              "| Stage | Count | Interpretation |", "|---|---:|---|"]
    for k, v in r.items():
        lines.append(f"| {k.replace('_',' ')} | {number(v)} | "
                     + ("Not measured; never inferred from source bodies"
                        if v is None else "Saved snapshot, not live"
                        if k.startswith("snapshot_") else "Source-backed or canonical classification") + " |")
    lines += ["", "## D. Ownership classifications", "",
              "| Scope | Records |", "|---|---:|"]
    lines.extend(f"| {k} | {number(v)} |" for k,v in doc["ownership"].items())
    lines += ["", "## E. Review priorities", "",
              "Heuristic: remaining assessed qualified records in known system/placeholder scopes, "
              "discounting observed main/PR matches. **Not an eligibility certificate.**", "",
              "| Library | Priority score | Qualified assessed | Unnamed | 3.20 name proposals |",
              "|---|---:|---:|---:|---:|"]
    for row in sorted(doc["libraries"], key=lambda x:(-x["score_triage_only"], x["library"]))[:40]:
        lines.append(f"| {row['library']} | {number(row['score_triage_only'])} | "
                     f"{number(row['qualified_assessed'])} | {number(row['unresolved'])} | "
                     f"{number(row['name_recovery_candidates_320'])} |")
    lines += ["", "## F. Automation health", "",
              "| Signal | Value |", "|---|---|"]
    for key, value in h.items():
        value = json.dumps(value, sort_keys=True) if isinstance(value, dict) else number(value)
        lines.append(f"| {key.replace('_', ' ')} | {value} |")
    lines += ["", "### Actual progress trend", "",
              "| Observed at (UTC) | Indexed | Strictly verified names | AnyPS5 main source matches | Open PR heads scanned |",
              "|---|---:|---:|---:|---:|"]
    for point in doc.get("trends", [])[-20:]:
        lines.append(f"| {point['observed_at_utc']} | {number(point['indexed'])} | "
                     f"{number(point['strictly_verified_names'])} | "
                     f"{number(point['anyps5_main_matches'])} | "
                     f"{number(point['open_pr_scanned'])} |")
    lines += ["", "### Coverage denominators", ""]
    for key, description in doc["denominators"].items():
        lines.append(f"- **{key}:** {description}")
    lines += ["", "### Limitations", ""]
    lines.extend("- " + text for text in doc["limitations"])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    result = build(root)
    print("Matrix libraries:", len(result["libraries"]))
