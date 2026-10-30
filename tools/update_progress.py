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
    verified = set()
    invalid_bindings = 0
    withheld_qualified = 0
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
                    if key in by_identity:
                        raise ValueError(f"Duplicate library/NID identity: {lib}/{nid}")
                    by_identity[key] = row
                    all_libraries[lib] += 1
                    all_nids[nid] += 1
                    scopes[row["scope"]] += 1
                    name = row.get("name")
                    valid = bool(name and row.get("name_status") == "verified_nid_binding"
                                 and nid_for(name) == nid)
                    if valid:
                        verified.add(key)
                        library_named[lib] += 1
                    elif name:
                        invalid_bindings += 1
                    if row.get("stub_assessment") == QUALIFIED:
                        if valid:
                            qualified.add(key)
                        else:
                            withheld_qualified += 1
    return by_identity, all_nids, scopes, all_libraries, library_named, qualified, verified, invalid_bindings, withheld_qualified


def scan_upstream(upstream: Path, known: dict, verified: set):
    observations = {}
    new_candidates = set()
    seen_definitions = 0
    for path in sorted((upstream / "core" / "libs" / "prx").rglob("*.cpp")):
        rel = path.relative_to(upstream).as_posix()
        match = SOURCE.match(rel)
        if not match:
            continue
        lib = match.group(1).casefold()
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, kind in scan_source(text):
            seen_definitions += 1
            nid = nid_for(name)
            key = (lib, nid)
            if key in verified and known[key].get("name") == name:
                # A definition with no marker is not automatically a working implementation.
                if observations.get(key) != "source_definition":
                    observations[key] = kind
            else:
                # Capture an identifier only, never an unreviewed symbol name.
                new_candidates.add((lib, nid))
    return observations, new_candidates, seen_definitions


def api_json(url: str, token: str):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ps5-readiness-sync",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def scan_open_prs(token: str, known: dict, verified: set, max_prs: int):
    root = "https://api.github.com/repos/boykopovar/AnyPS5"
    prs = []
    page = 1
    while True:
        chunk = api_json(f"{root}/pulls?state=open&per_page=100&page={page}", token)
        prs.extend(chunk)
        if len(chunk) < 100:
            break
        page += 1
    total = len(prs)
    reservations = defaultdict(set)
    candidate_nids = set()
    incomplete = total > max_prs
    errors = 0
    for pr in prs[:max_prs]:
        number = pr["number"]
        page = 1
        try:
            while True:
                files = api_json(f"{root}/pulls/{number}/files?per_page=100&page={page}", token)
                for item in files:
                    match = SOURCE.match(item["filename"])
                    if not match:
                        continue
                    lib = match.group(1).casefold()
                    patch = item.get("patch")
                    if patch is None:
                        incomplete = True
                        continue
                    added = "\n".join(line[1:] for line in patch.splitlines()
                                      if line.startswith("+") and not line.startswith("+++"))
                    for name in DEF.findall(added):
                        key = (lib, nid_for(name))
                        if key in verified and known[key].get("name") == name:
                            reservations[key].add(number)
                        else:
                            candidate_nids.add(key)
                if len(files) < 100:
                    break
                page += 1
        except (urllib.error.URLError, TimeoutError, ValueError):
            errors += 1
            incomplete = True
    return reservations, candidate_nids, {
        "open_pr_total": total, "open_pr_scanned": min(total, max_prs),
        "open_pr_errors": errors, "open_pr_coverage_complete": not incomplete,
        "method": "added APS5_VABI declarations in GitHub PR patches; best-effort reservations"
    }


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
    cli.add_argument("--max-open-prs", type=int, default=400)
    args = cli.parse_args()
    root = args.root.resolve()
    old = read_json(root / "readiness.json")
    manifest = read_json(root / "manifest.json")
    known, nids, scopes, libraries, named, qualified, verified, invalid, qualified_invalid = load_inventory(root)
    total = len(known)
    names = len(verified)
    if total != manifest["counts"]["total_records"]:
        raise ValueError("Inventory row count does not match canonical manifest")
    if names != manifest["counts"]["resolved_names"]:
        raise ValueError("Verified names do not match manifest; regenerate canonical dataset first")
    qualified_nids = {key[1] for key in qualified}
    all_uniq_nids = len(nids)
    aliases = total - all_uniq_nids
    upstream = args.upstream_dir.resolve() if args.upstream_dir else None
    main_obs = {}
    unmatched = set()
    definition_count = 0
    pr_obs = {}
    pr_candidates = set()
    pr_meta = {"open_pr_total": None, "open_pr_scanned": 0,
               "open_pr_errors": 0, "open_pr_coverage_complete": False,
               "method": "not checked"}
    sha = None
    if upstream:
        main_obs, unmatched, definition_count = scan_upstream(upstream, known, verified)
        sha = git_head(upstream)
        if not args.skip_prs:
            try:
                pr_obs, pr_candidates, pr_meta = scan_open_prs(
                    os.getenv("GITHUB_TOKEN", ""), known, verified, args.max_open_prs
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
        q = sum(k[0] == libkey for k in qualified)
        main_q = sum(k[0] == libkey for k in main_qualified)
        reserved_q = sum(k[0] == libkey for k in pending_qualified)
        per_lib.append({"library": lib, "records": libraries[lib], "verified_names": named[lib],
                        "qualified_records": q, "upstream_main_source_matches": main_q,
                        "open_pr_added_matches": reserved_q})
    summary = {
        "schema_version": 1,
        "generated_from": {"catalog_manifest_counts": manifest["counts"],
                           "anyps5_main_commit": sha,
                           "anyps5_open_prs": pr_meta,
                           "upstream_sync": "source-scanned" if upstream else "unavailable"},
        "inventory": {
            "records": total, "libraries": len(libraries), "firmware_13_60": manifest["counts"]["firmware-13.60"],
            "historical_only": manifest["counts"]["historical-3.20-only"],
            "verified_named_records": names, "unresolved_or_withheld": total - names,
            "unique_nids_all_scopes": all_uniq_nids,
            "cross_library_nid_extra_records_all_scopes": aliases,
            "nid_shared_by_multiple_records": sum(1 for v in nids.values() if v > 1),
            "name_nid_mismatches_or_nonverified_names": invalid,
            "scope_records": dict(sorted(scopes.items()))
        },
        "stubs": {
            "qualified_unique_nids_recomputed": total_qualified,
            "qualified_library_nid_records_recomputed": len(qualified),
            "saved_qualified_unique_nids": qualified_saved,
            "saved_vs_recomputed_delta": discrepancy,
            "qualified_but_unverified_records_excluded": qualified_invalid,
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
            "new_upstream_nid_candidates_for_review": len(candidate_records)
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
    s = summary["stubs"]
    i = summary["inventory"]
    lines = [
        "# PS5 13.60 — live readiness", "",
        "Generated from the checked-in inventory and a read-only AnyPS5 upstream checkout.",
        "No executable stubs or firmware are included here.", "",
        "## Export inventory and name recovery", "",
        "| Metric | Count |", "|---|---:|",
        f"| Export library/NID identities | {total:,} |",
        f"| Firmware 13.60 observed exports | {i['firmware_13_60']:,} |",
        f"| Historical-only references | {i['historical_only']:,} |",
        f"| Logical libraries | {len(libraries):,} |",
        f"| Verified named records | {names:,} ({pct(names, total)}) |",
        f"| Unresolved or withheld records | {total - names:,} |",
        f"| Unique NIDs across all scopes | {all_uniq_nids:,} |",
        f"| Extra cross-library NID records (not deletions) | {aliases:,} |",
        "",
        "## Stub progress — distinct stages", "",
        "| Measure | Count | Evidence level |", "|---|---:|---|",
        f"| Qualified unique NIDs (recomputed) | {total_qualified:,} | Local inventory assessment only |",
        f"| Generated throwing stubs | {s['locally_generated_saved_snapshot']:,} | Saved local snapshot |",
        f"| Offline statically prepared | {s['statically_prepared_saved_snapshot']:,} | Saved local snapshot |",
        f"| Fully validated | {s['fully_validated_saved_snapshot']:,} | Saved local snapshot |",
        f"| Published to AnyPS5 | {s['published_upstream_saved_snapshot']:,} | Saved historical snapshot; **not live** |",
        f"| Qualified NIDs with matching AnyPS5 main source definitions | {len(main_qualified_nids):,} | Source scan, not export/runtime validation |",
        f"| Additional qualified NIDs seen in open-PR additions | {len(pending_qualified_nids):,} | Best-effort PR patch scan |",
        f"| Qualified NIDs not seen by these scans | {len(unaccounted):,} | Not proof they are missing upstream |",
        f"| Additional upstream NID observations needing review | {len(candidate_records):,} | No unverified names published |",
        "",
        f"**Saved qualified-count discrepancy:** {qualified_saved:,} published versus "
        f"{total_qualified:,} recomputed (delta {discrepancy:+,}). "
        "This report does not silently modify canonical assessments.", "",
        "## Upstream observation", "",
        f"- AnyPS5 main revision: {BT + sha + BT if sha else 'unavailable (offline generation)'}",
        f"- Open PRs observed: {pr_meta['open_pr_total'] if pr_meta['open_pr_total'] is not None else 'unavailable'}",
        f"- Open PRs scanned: {pr_meta['open_pr_scanned']}",
        f"- Open PR audit complete: {'yes (patch availability subject to API)' if pr_meta['open_pr_coverage_complete'] else 'NO — do not treat reservations as exhaustive'}",
        "",
        "## Source and safety limits", "",
        "Matching a source definition does not confirm its registration, exported NID, ABI, "
        "correct runtime behavior, or merge status. A throwing marker indicates only a "
        "source-level NotImplemented call. Multiple libraries sharing a NID are preserved "
        "until ownership and equivalence have been independently resolved.", "",
        "Upstream-only observations are stored as **NID-only review candidates** in "
        f"[upstream-review-queue.jsonl](reports/upstream-review-queue.jsonl); symbols "
        "cannot be promoted to verified names or qualified stubs without independent review.", "",
        "See [machine-readable progress](reports/progress.json), "
        "[library breakdown](reports/library-progress.md), "
        "[AnyPS5 integration rules](ANYPS5.md), and [publication policy](DATA_POLICY.md).", ""
    ]
    write_if_changed(root / "READINESS.md", "\n".join(lines))
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
