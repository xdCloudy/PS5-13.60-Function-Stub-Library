#!/usr/bin/env python3
"""Generate auditable, source-backed PS5 readiness reporting (stdlib only).

This script does not modify canonical firmware inventory records, qualify names,
infer ABI correctness, or assert that upstream source definitions are exported.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.request
from upstream_sync import scan_open_prs_cached
from render_readiness import render_report

NID_SUFFIX = bytes.fromhex("518d64a635ded8c1e6b039b1c3e55230")
DEF = re.compile(r"\bAPS5_VABI\s+([A-Za-z_]\w*)\s*\(")
SOURCE = re.compile(r"^core/libs/prx/([^/]+)/.*\.cpp$")
QUALIFIED = "throwing_stub_candidate_validation_required"
BT = chr(96)


def nid_for(name: str) -> str:
    digest = hashlib.sha1(name.encode("utf-8") + NID_SUFFIX).digest()
    return base64.b64encode(digest[:8][::-1]).decode("ascii").rstrip("=")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(a: int, b: int) -> str:
    return f"{a / b * 100:.2f}%" if b else "n/a"


def scan_source(content: str):
    """Find concrete C ABI definitions; never mistake declarations for proof."""
    for match in DEF.finditer(content):
        name = match.group(1)
        pos, depth = match.end() - 1, 0
        while pos < len(content):
            if content[pos] == "(":
                depth += 1
            elif content[pos] == ")":
                depth -= 1
                if depth == 0:
                    pos += 1
                    break
            pos += 1
        if depth != 0:
            continue
        # Look only for a body before a ';' or an unrelated declaration.
        tail = content[pos:pos + 300]
        brace = tail.find("{")
        if brace < 0 or (";" in tail[:brace]):
            continue
        start = pos + brace
        end, nesting = start, 0
        while end < len(content):
            if content[end] == "{":
                nesting += 1
            elif content[end] == "}":
                nesting -= 1
                if nesting == 0:
                    break
            end += 1
        body = content[start:end + 1] if nesting == 0 else ""
        yield name, "throwing_marker" if "NotImplemented_nid_no_patch" in body else "source_definition"


def load_inventory(root: Path):
    by_identity = {}
    all_nids = Counter()
    scopes = Counter()
    all_libraries = Counter()
    library_named = Counter()
    qualified = set()
    assessed_qualified = set()
    verified = set()
    invalid_bindings = 0
    withheld_qualified = 0
    total_rows = 0
    verified_rows = 0
    for directory in ("firmware-13.60", "historical-3.20-only"):
        for path in sorted((root / "data" / directory).glob("*.jsonl")):
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    lib = row["library"]
                    nid = row["nid"]
                    key = (lib.casefold(), nid)
                    total_rows += 1
                    # The same library/NID can appear in both firmware and historical
                    # partitions. Retain every row; prefer the 13.60 row for lookup.
                    by_identity.setdefault(key, row)
                    all_libraries[lib] += 1
                    all_nids[nid] += 1
                    scopes[row["scope"]] += 1
                    name = row.get("name")
                    valid = bool(name and row.get("name_status") == "verified_nid_binding"
                                 and nid_for(name) == nid)
                    if valid:
                        verified.add(key)
                        verified_rows += 1
                        library_named[lib] += 1
                    elif name:
                        invalid_bindings += 1
                    if row.get("stub_assessment") == QUALIFIED:
                        if name and row.get("name_status") != "withheld_by_publication_filter":
                            assessed_qualified.add(key)
                        if valid:
                            qualified.add(key)
                        else:
                            withheld_qualified += 1
    return (by_identity, all_nids, scopes, all_libraries, library_named,
            qualified, assessed_qualified, verified, invalid_bindings,
            withheld_qualified, total_rows, verified_rows)


PUBLIC_SYMBOL = re.compile(r"^[A-Za-z_][A-Za-z_0-9]{0,230}$")
SENSITIVE_SYMBOL = re.compile(r"(api.?key|password|credential|secret|bearer|auth.?token|private.?key)", re.I)


def scan_upstream(upstream: Path, known: dict, verified: set):
    observations = {}
    new_candidates = set()
    source_candidates = {}
    matched_sources = {}
    withheld = 0
    seen_definitions = 0
    for path in sorted((upstream / "core" / "libs" / "prx").rglob("*.cpp")):
        rel = path.relative_to(upstream).as_posix()
        match = SOURCE.match(rel)
        if not match:
            continue
        lib = match.group(1).casefold()
        content = path.read_text(encoding="utf-8", errors="replace")
        for name, kind in scan_source(content):
            seen_definitions += 1
            nid = nid_for(name)
            key = (lib, nid)
            record = known.get(key)
            if key in verified and record.get("name") == name:
                if observations.get(key) != "source_definition":
                    observations[key] = kind
                    matched_sources[key] = rel
                continue
            new_candidates.add(key)
            # Only approved, public C symbol-shaped strings may appear in
            # the *separate* review queue. Canonical names are never mutated.
            if record and record.get("name_status") == "withheld_by_publication_filter":
                withheld += 1
                continue
            if not PUBLIC_SYMBOL.fullmatch(name) or SENSITIVE_SYMBOL.search(name):
                withheld += 1
                continue
            if record is None:
                status = "not_in_firmware_catalog"
            elif not record.get("name"):
                status = "unnamed_catalog_identity"
            elif record.get("name") != name:
                status = "conflicts_with_published_name"
            else:
                status = "published_name_requires_evidence_review"
            source_candidates.setdefault(key, {
                "library": lib, "nid": nid, "proposed_name": name,
                "source": "boykopovar/AnyPS5",
                "source_file": rel, "source_kind": kind,
                "match_status": status, "verification": "public_source_nid_hash_only",
                "canonical_name_approved": False, "signature_verified": False,
                "implementation_verified": False,
            })
    return observations, new_candidates, seen_definitions, source_candidates, matched_sources, withheld


def git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"],
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def write_if_changed(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    cli.add_argument("--upstream-dir", type=Path, help="Fresh read-only checkout of AnyPS5 main")
    cli.add_argument("--skip-prs", action="store_true", help="Offline/fixture mode")
    cli.add_argument("--max-open-prs", type=int, default=550,
                     help="Maximum uncached PR heads to inspect per run; prior heads stay cached")
    args = cli.parse_args()
    root = args.root.resolve()
    old = read_json(root / "readiness.json")
    manifest = read_json(root / "manifest.json")
    (known, nids, scopes, libraries, named, qualified, assessed_qualified,
     verified, invalid, qualified_invalid, total, names) = load_inventory(root)
    if total != manifest["counts"]["total_records"]:
        raise ValueError("Inventory row count does not match canonical manifest")
    named_total = names + invalid
    if named_total != manifest["counts"]["resolved_names"]:
        raise ValueError("Named record count differs from manifest; regenerate canonical inventory")
    strict_rehash_shortfall = named_total - names
    qualified_nids = {key[1] for key in assessed_qualified}
    strict_qualified_nids = {key[1] for key in qualified}
    all_uniq_nids = len(nids)
    cross_scope_repeated_identities = total - len(known)
    aliases = len(known) - all_uniq_nids
    upstream = args.upstream_dir.resolve() if args.upstream_dir else None
    main_obs = {}
    unmatched = set()
    source_candidates = {}
    matched_sources = {}
    withheld_source_names = 0
    definition_count = 0
    pr_obs = {}
    pr_candidates = set()
    pr_meta = {"open_pr_total": None, "open_pr_scanned": 0,
               "open_pr_errors": 0, "open_pr_coverage_complete": False,
               "method": "not checked"}
    sha = None
    if upstream:
        (main_obs, unmatched, definition_count,
         source_candidates, matched_sources, withheld_source_names) = scan_upstream(upstream, known, verified)
        sha = git_head(upstream)
        if not args.skip_prs:
            try:
                pr_obs, pr_candidates, pr_meta = scan_open_prs_cached(
                    os.getenv("GITHUB_TOKEN", ""), known, verified,
                    nid_for, root / "reports/open-pr-cache.json", args.max_open_prs
                )
            except (urllib.error.URLError, TimeoutError, ValueError) as e:
                pr_meta["error"] = type(e).__name__
    main_qualified = {k for k in main_obs if k in qualified}
    pending_qualified = {k for k in pr_obs if k in qualified and k not in main_qualified}
    main_qualified_nids = {k[1] for k in main_qualified}
    pending_qualified_nids = {k[1] for k in pending_qualified} - main_qualified_nids
    total_qualified = len(qualified_nids)
    unaccounted = qualified_nids - main_qualified_nids - pending_qualified_nids
    candidate_records = sorted(unmatched | pr_candidates)
    # Keep old generated-stub counts labeled as saved. Do not fabricate fresh build/CI evidence.
    qualified_saved = old["metrics"]["qualified_unique_stub_candidates"]
    discrepancy = qualified_saved - total_qualified
    # GitHub observations only cover named C ABI definitions; other upstream forms may be missed.
    per_lib = []
    for lib in sorted(libraries, key=lambda lib: (-libraries[lib], lib)):
        libkey = lib.casefold()
        q = sum(k[0] == libkey for k in assessed_qualified)
        main_q = sum(k[0] == libkey for k in main_qualified)
        reserved_q = sum(k[0] == libkey for k in pending_qualified)
        per_lib.append({"library": lib, "records": libraries[lib], "verified_names": named[lib],
                        "qualified_records": q, "upstream_main_source_matches": main_q,
                        "open_pr_added_matches": reserved_q})
    summary = {
        "schema_version": 1,
        "generated_from": {"generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                           "catalog_manifest_counts": manifest["counts"],
                           "anyps5_main_commit": sha,
                           "anyps5_open_prs": pr_meta,
                           "upstream_sync": "source-scanned" if upstream else "unavailable"},
        "inventory": {
            "records": total, "libraries": len(libraries), "firmware_13_60": manifest["counts"]["firmware-13.60"],
            "historical_only": manifest["counts"]["historical-3.20-only"],
            "published_named_records": named_total,
            "strictly_reverified_named_records": names,
            "named_records_not_passed_by_strict_gate": strict_rehash_shortfall,
            "verified_named_records": named_total, "unresolved_or_withheld": total - named_total,
            "unique_nids_all_scopes": all_uniq_nids,
            "cross_library_nid_extra_records_all_scopes": aliases,
            "repeated_library_nid_records_across_scopes": cross_scope_repeated_identities,
            "nid_shared_by_multiple_records": sum(1 for v in nids.values() if v > 1),
            "name_nid_mismatches_or_nonverified_names": invalid,
            "scope_records": dict(sorted(scopes.items()))
        },
        "stubs": {
            "qualified_unique_nids_recomputed": total_qualified,
            "qualified_library_nid_records_recomputed": len(assessed_qualified),
            "strictly_rehashed_qualified_unique_nids": len(strict_qualified_nids),
            "saved_qualified_unique_nids": qualified_saved,
            "saved_vs_recomputed_delta": discrepancy,
            "qualified_records_outside_strict_rehash_gate": qualified_invalid,
            "locally_generated_saved_snapshot": old["metrics"]["generated_throwing_stubs"],
            "statically_prepared_saved_snapshot": old["metrics"]["statically_prepared_stubs"],
            "fully_validated_saved_snapshot": old["metrics"]["fully_validated_stubs"],
            "published_upstream_saved_snapshot": old["metrics"]["published_anyps5_stubs"],
            "upstream_source_definitions_seen": definition_count,
            "verified_catalog_identity_main_source_matches": len(main_obs),
            "qualified_unique_nids_matched_in_main_source": len(main_qualified_nids),
            "qualified_unique_nids_matched_in_open_pr_additions": len(pending_qualified_nids),
            "qualified_unique_nids_not_matched_in_main_or_pr_scans": len(unaccounted),
            "main_throwing_marker_record_matches": sum(k in qualified and v == "throwing_marker"
                                                       for k, v in main_obs.items()),
            "main_nonthrowing_definition_record_matches": sum(k in qualified and v == "source_definition"
                                                             for k, v in main_obs.items()),
            "new_upstream_nid_candidates_for_review": len(candidate_records),
            "auto_imported_public_source_name_proposals": len(source_candidates),
            "external_source_evidence_records": len(main_obs) + len(source_candidates) + len(pr_candidates - set(main_obs) - set(source_candidates)),
            "auto_imported_catalog_matching_proposals": sum(x["match_status"] == "unnamed_catalog_identity" for x in source_candidates.values()),
            "source_names_withheld_by_safety_filter": withheld_source_names
        },
        "limitations": [
            "Cross-library NID repetition does not prove semantic equivalence or permit deletion.",
            "A source definition or PR patch does not prove exported, registered, ABI-correct or runtime-tested behavior.",
            "PR reservations are incomplete when pagination, patches or API requests fail.",
            "Auto-discovered upstream NIDs are review inputs only; no new name or qualification is auto-approved.",
            "Local generated/validated/published counts are historical saved snapshots, not live upstream measurements."
        ],
        "libraries": per_lib
    }
    write_if_changed(root / "reports" / "progress.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")
    candidates = "\n".join(json.dumps({"library": lib, "nid": nid,
                                     "status": "upstream_observed_needs_independent_review",
                                     "source_commit": sha}, sort_keys=True)
                           for lib, nid in candidate_records)
    write_if_changed(root / "reports" / "upstream-review-queue.jsonl", candidates + ("\n" if candidates else ""))
    proposals = "\n".join(json.dumps({**record, "source_commit": sha}, sort_keys=True)
                          for key, record in sorted(source_candidates.items()))
    write_if_changed(root / "reports" / "upstream-source-candidates.jsonl",
                     proposals + ("\n" if proposals else ""))
    # External-source mirror: one sanitized identity per (library, NID), with
    # its provenance and current coverage. This is not canonical firmware data.
    evidence = {}
    for key, kind in sorted(main_obs.items()):
        lib, nid = key
        evidence[key] = {"library": lib, "nid": nid, "external_db": "boykopovar/AnyPS5",
                         "upstream_main_commit": sha, "observed_on_main": True,
                         "source_file": matched_sources.get(key),
                         "source_classification": kind, "match_status": "catalogue_reverified",
                         "canonical_name_approved": True,
                         "abi_validated": False, "runtime_validated": False}
    for key, item in sorted(source_candidates.items()):
        lib, nid = key
        evidence[key] = {"library": lib, "nid": nid, "external_db": "boykopovar/AnyPS5",
                         "upstream_main_commit": sha, "observed_on_main": True,
                         "source_file": item["source_file"],
                         "source_classification": item["source_kind"],
                         "match_status": item["match_status"],
                         "proposed_name": item["proposed_name"],
                         "canonical_name_approved": False,
                         "abi_validated": False, "runtime_validated": False}
    for key, numbers in pr_obs.items():
        lib, nid = key
        record = evidence.setdefault(key, {"library": lib, "nid": nid,
                                           "external_db": "boykopovar/AnyPS5",
                                           "upstream_main_commit": sha,
                                           "observed_on_main": False,
                                           "match_status": "pr_only_review",
                                           "canonical_name_approved": False,
                                           "abi_validated": False, "runtime_validated": False})
        record["open_pr_numbers"] = sorted(numbers)
    for lib, nid in sorted(pr_candidates):
        key = (lib, nid)
        evidence.setdefault(key, {"library": lib, "nid": nid,
                                  "external_db": "boykopovar/AnyPS5",
                                  "upstream_main_commit": sha,
                                  "observed_on_main": False,
                                  "match_status": "pr_only_nid_review",
                                  "canonical_name_approved": False,
                                  "abi_validated": False, "runtime_validated": False})
    write_if_changed(root / "reports" / "anyps5-evidence.jsonl",
                     "".join(json.dumps(record, sort_keys=True) + "\n"
                             for key, record in sorted(evidence.items())))
    summary["stubs"]["external_source_evidence_records"] = len(evidence)
    write_if_changed(root / "reports" / "progress.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")
    write_if_changed(root / "READINESS.md", render_report(summary))
    table = ["# Library progress", "",
             "All identities remain represented; source definition matches are **not** validation.", "",
             "| Library | Exports | Named | Qualified | Main matches | Open PR matches |",
             "|---|---:|---:|---:|---:|---:|"]
    for row in per_lib:
        lib = row["library"].replace("|", r"\|")
        table.append(f"| {lib} | {row['records']:,} | {row['verified_names']:,} | "
                     f"{row['qualified_records']:,} | {row['upstream_main_source_matches']:,} | "
                     f"{row['open_pr_added_matches']:,} |")
    write_if_changed(root / "reports" / "library-progress.md", "\n".join(table) + "\n")
    print(f"Inventory {total:,}; verified {names:,}; qualified {total_qualified:,}; "
          f"main NID matches {len(main_qualified_nids):,}; PR NID matches {len(pending_qualified_nids):,}; "
          f"review candidates {len(candidate_records):,}")


if __name__ == "__main__":
    main()
