"""Readable, annotated Markdown from the machine-generated readiness totals."""
from __future__ import annotations

def n(x): return f"{x:,}" if isinstance(x, int) else str(x)
def pct(a,b): return f"{a*100/b:.1f}%" if b else "n/a"
def bar(a,b):
    count = max(0,min(22,round(22*a/b))) if b else 0
    return "█"*count + "░"*(22-count)

def render_report(doc: dict) -> str:
    i, s, meta = doc["inventory"], doc["stubs"], doc["generated_from"]
    pr = meta["anyps5_open_prs"]
    total, named, q = i["records"], i["published_named_records"], s["qualified_unique_nids_recomputed"]
    gen = s["locally_generated_saved_snapshot"]
    bt = chr(96)
    revision = meta.get("anyps5_main_commit")
    link = (f"[{revision[:12]}](https://github.com/boykopovar/AnyPS5/commit/{revision})" if revision else "not scanned")
    lines = [
        "# PS5 13.60 — readiness dashboard", "",
        "**What is this?** An auditable export-name catalogue and AnyPS5 stub research tracker. "
        "An export record is **not** a working function, and the inventory is much larger than the "
        "eligible system-library stub backlog.", "",
        f"**Last refresh:** {meta.get('generated_at_utc', 'unknown')} · **AnyPS5 main:** {link}", "",
        "## At a glance", "",
        "| Workstream | Progress | Meaning |", "|---|---:|---|",
        f"| **Recovered names** | **{n(named)} / {n(total)} ({pct(named,total)})** | Inventory rows with a published name, not necessarily an ABI signature |",
        f"| **AnyPS5 main (live source matches)** | **{n(s['anyps5_main_tracked_source_records_live'])} library/NID identities** | Matching definitions already present in merged upstream source; not proof of runtime functionality |",
        f"| **Qualified throwing-stub candidates** | **{n(q)} unique NIDs** | Current eligible research backlog, not implemented functions |",
        f"| **Locally generated stubs** | **{n(gen)} / {n(q)} ({pct(gen,q)})** | Historical snapshot of throwing placeholders, not live upstream coverage |",
        "",
        "### Name recovery", "",
        f"{bt}{bar(named,total)}{bt} **{pct(named,total)}** — {n(total-named)} unresolved/withheld records.", "",
        "### Local stub generation (saved snapshot)", "",
        f"{bt}{bar(gen,q)}{bt} **{pct(gen,q)}** — placeholders commonly throw rather than implement behaviour.", "",
        "## How to interpret the pipeline", "",
        "| Gate | Count | Interpretation |", "|---|---:|---|",
        f"| Published named export records | {n(named)} | Has an associated name, but does not prove correct types/ABI |",
        f"| Strictly rehashed named records | {n(i['strictly_reverified_named_records'])} | Stronger local NID/name/status evidence |",
        f"| Qualified unique NIDs | {n(q)} | Existing candidate assessments after withholding filter |",
        f"| Strictly rehashed qualified NIDs | {n(s['strictly_rehashed_qualified_unique_nids'])} | Conservative subset used for exact source matching |",
        f"| Locally generated throwing stubs (saved) | {n(gen)} | Not necessarily compiled or merged |",
        f"| Statically prepared (saved) | {n(s['statically_prepared_saved_snapshot'])} | Historical offline gates |",
        f"| Fully validated (saved) | {n(s['fully_validated_saved_snapshot'])} | Historical build/runtime validation only |",
        f"| **Present in AnyPS5 main source (live)** | **{n(s['anyps5_main_tracked_source_records_live'])}** | Matched and rehashed library/NID/name in current upstream main; separate from qualified backlog |",
        f"| With NotImplemented marker (live) | {n(s['anyps5_main_throwing_marker_records_live'])} | Source-level placeholder, not working behaviour |",
        f"| With nonthrowing C ABI body (live) | {n(s['anyps5_main_nonthrowing_source_records_live'])} | No matching NotImplemented marker; **not** necessarily a tested implementation |",
        "",
        f"**Qualification correction:** the saved report listed {n(s['saved_qualified_unique_nids'])}, "
        f"while the filtered count is {n(q)} (difference {s['saved_vs_recomputed_delta']:+,} from saved). "
        f"Separately, {n(i['named_records_not_passed_by_strict_gate'])} named records "
        "need strict name/NID/status evidence review. These must not be silently promoted. "
        f"The old `published to AnyPS5 = {n(s['published_upstream_saved_snapshot'])}` is an **archived snapshot** and "
        "must not be treated as the current upstream count.", "",
        "## AnyPS5 upstream — what is already being worked on?", "",
        "| Evidence | Count | Meaning |", "|---|---:|---|",
        f"| **Catalogued names present on merged AnyPS5 main** | **{n(s['anyps5_main_tracked_source_records_live'])} records / {n(s['anyps5_main_tracked_unique_nids_live'])} unique NIDs** | **Live source evidence**, not the saved 0-counter |",
        f"| Marked throwing/unimplemented | {n(s['anyps5_main_throwing_marker_records_live'])} | NotImplemented marker is visible in body |",
        f"| Other nonthrowing source definitions | {n(s['anyps5_main_nonthrowing_source_records_live'])} | A source body exists; not necessarily correct, wired up or validated |",
        f"| Qualified NIDs also in main source | {n(s['qualified_unique_nids_matched_in_main_source'])} | Potential existing coverage |",
        f"| Additional qualified NIDs seen in open-PR additions | {n(s['qualified_unique_nids_matched_in_open_pr_additions'])} | Possible reservations, not yet merged |",
        f"| Qualified NIDs not observed by scans | {n(s['qualified_unique_nids_not_matched_in_main_or_pr_scans'])} | **Not proof of no overlap** |",
        "",
        "### Open PR coverage", "",
        f"{bt}{bar(pr['open_pr_scanned'],pr['open_pr_total'] or 0)}{bt} "
        f"**{n(pr['open_pr_scanned'])} / {n(pr['open_pr_total'] or 0)} "
        f"({pct(pr['open_pr_scanned'],pr['open_pr_total'] or 0)})** current open PR heads indexed.", "",
        ("**All current heads scanned.** The source parser still cannot guarantee every possible overlap."
         if pr["open_pr_coverage_complete"] else
         f"**Partial:** {n(pr.get('open_pr_unscanned', (pr['open_pr_total'] or 0)-pr['open_pr_scanned']))} "
         "PR heads remain. Scheduled runs accumulate results in an SHA-keyed cache."),
        f"Cache hits: {n(pr.get('open_pr_cached',0))} · newly scanned: {n(pr.get('open_pr_newly_scanned',0))} "
        f"· failed checks: {n(pr.get('open_pr_errors',0))}.",
        "**Before submitting a stub PR, still run a final exact overlap review against current main and all open PRs.**", "",
        "## Automatically imported AnyPS5 source evidence", "",
        f"**{n(s.get('auto_imported_public_source_name_proposals',0))}** public source-name proposals "
        "are available in the [review queue](reports/upstream-source-candidates.jsonl); "
        f"**{n(s.get('auto_imported_catalog_matching_proposals',0))}** correspond to unnamed "
        "identities already in this firmware catalogue.", "",
        "The proposed name, NID and source location are searchable, but the name is "
        "**not independently verified against firmware**, nor are ABI or behaviour confirmed. "
        "Publication-filtered strings are not promoted. "
        "[NID-only review queue](reports/upstream-review-queue.jsonl).", "",
        "## Duplicates are review targets, not deletion instructions", "",
        "| Identity measure | Count |", "|---|---:|",
        f"| Indexed export records | {n(total)} |",
        f"| Distinct NID strings globally, across all scopes | {n(i['unique_nids_all_scopes'])} |",
        f"| Extra cross-library NID records | {n(i['cross_library_nid_extra_records_all_scopes'])} |",
        f"| Repeated library/NID across inventory partitions | {n(i['repeated_library_nid_records_across_scopes'])} |",
        "",
        "Shared NIDs can be valid exports owned by different libraries. The canonical "
        "export inventory preserves their identities. Managed/application and historical-only "
        "records are **not automatically AnyPS5 system-library stubs**.", "",
        "## Which libraries should be reviewed next?", "",
        "Top 12 libraries sorted by assessed qualified records not seen in current "
        "main or scanned PR additions. This is a triage estimate, not a verified patch backlog.", "",
        "| Library | Qualified pending records | Main matched names (all statuses) | Main pending overlaps | Open PR pending overlaps | Not observed pending |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    rows = sorted((row for row in doc["libraries"] if row["qualified_records"]),
                  key=lambda r: (-(r["qualified_records"]-r["upstream_main_source_matches"]-
                                   r["open_pr_added_matches"]), r["library"]))
    for r in rows[:12]:
        ql,m,p=r["qualified_records"],r["upstream_main_source_matches"],r["open_pr_added_matches"]
        lines.append(f"| {r['library'].replace('|','/')} | {n(ql)} | {n(r.get('upstream_main_catalogue_source_matches',0))} | {n(m)} | {n(p)} | {n(max(0,ql-m-p))} |")
    lines += ["",
        f"See [all {n(i['libraries'])} libraries](reports/library-progress.md) or "
        "[machine-readable metrics](reports/progress.json) for the full breakdown.", "",
        "## How it updates", "",
        "1. This repo's pushes refresh inventory and report files.",
        "2. Scheduled checks inspect AnyPS5 main and progressively scan **all** open PR heads, "
        "reusing cached results only when the head SHA remains unchanged.",
        "3. Public source names are staged for audit, without silently rewriting canonical names or qualification.",
        "4. Matching current AnyPS5 main definitions updates the external-source mirror and "
        "the live stage counts automatically; no manual movement between snapshot categories is needed.",
        "5. The final build, ABI, ownership and full pre-submission collision check remains a separate gate.", "",
        "[How synchronization works](UPSTREAM_SYNC.md) · "
        "[Integration policy](ANYPS5.md) · [Publication controls](DATA_POLICY.md)", ""
    ]
    return "\n".join(lines)
