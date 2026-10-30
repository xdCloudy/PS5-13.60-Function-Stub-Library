# Automated AnyPS5 readiness synchronization

## Purpose

- Keep the entire PS5 13.60 / historical-only inventory immutable unless a separately reviewed, coordinated data regeneration changes it.
- Regenerate READINESS.md, reports/progress.json, reports/library-progress.md and reports/upstream-review-queue.jsonl directly in the repository. No PNG.
- Pull current AnyPS5 main through a read-only checkout. Poll every three hours to notice new main commits, independently of this repository's pushes.
- On default-branch pushes: update checked-in reports. On PR updates: create an isolated read-only preview artifact. Branch push reports do not race code commits. The main branch report incorporates inventory PRs once merged.
- Accept optional immediate external repository_dispatch events of type anyps5-updated (requires separately configured dispatch credentials or upstream workflow).

## Trusted data sources

1. Inventory source of truth: data/firmware-13.60 and data/historical-3.20-only JSONL shards, plus manifest counts. Exact (library, NID) keys must be unique.
2. Canonical qualification: previously recorded stub_assessment values, recalculated with verified names and rehashed NIDs. Withheld or unresolved names never qualify automatically.
3. Current AnyPS5 main: C++ APS5_VABI source definitions matched by library + computed NID + exact existing verified catalog name. The scanner reports a nonthrowing source body separately from a NotImplemented throwing marker, **not** as validated implementation.
4. Current AnyPS5 open PRs: newly added APS5_VABI names from patch lines provide provisional reservations. PRs adding symbols through other forms or with missing/truncated patches may be missed.
5. Unknown upstream exports: **NID-only candidate records** are saved for independent review, never source names or automatically qualified stubs.


## Bidirectional reconciliation: AnyPS5 as an external source database

At each refresh, the workflow computes matching NIDs from public AnyPS5 source and joins them to the catalogue by **both** library and NID. The result is stored in `reports/anyps5-evidence.jsonl`, keyed by that identity, retaining the AnyPS5 main commit, source location and source-level status. It also stores NID-only PR observations (and the PR number when the symbol was reliably attributed). `reports/upstream-source-candidates.jsonl` contains sanitised public symbol-name proposals for independent review.

This mirror updates the **derived status in `reports/progress.json` and `READINESS.md`** without requiring a manually-maintained “published” counter. In particular:

- `anyps5_main_tracked_source_records_live` is the number of matching, strictly rehashed named library/NID records that **already have a source definition on current AnyPS5 main**. This includes entries previously labelled covered, not just records still qualified as throwing-stub candidates. It is the correct source-backed alternative to the historical `published_anyps5_stubs: 0` snapshot.
- The live stage separately shows source bodies with `NotImplemented_nid_no_patch` and other definitions. A definition without the marker is **not automatically verified as implemented or ABI-correct**.
- Open PR observations are provisional and expire when PRs close or their head SHA changes. A persistent `reports/open-pr-cache.json` tracks which open PR heads were inspected; capped runs accumulate coverage instead of starting at the first 400 every time.
- Library totals are updated in the live per-library report. Existing firmware metadata and verified-name bindings **are not overwritten** solely because an external project has a similar symbol.
- A matching existing name can be counted as source-covered; previously unknown names are imported only into the separate source-review queue. This permits automatic enrichment while retaining evidence and publication gates.

“Published in upstream source” therefore means a source-level identity match on `main`, **not** independently confirmed registration, ABI correctness, implementation quality or runtime tests. This is metadata synchronisation, not automatic copying of C++ function bodies, and it makes no change to AnyPS5 itself.

The refresh is scheduled every three hours and can also be manually dispatched; it is not instant on an AnyPS5 push unless the external repository dispatch hook is separately installed.

## Numbers and limitations

- 100% indexed does not imply 100% symbol names recovered, 100% unique functions, or 100% upstream code readiness.
- A NID shared across libraries is a potential alias, not automatically a duplicate. Never drop a library/NID record based only on a global match.
- Historical-only identities do not prove an export on firmware 13.60.
- Neither source matching nor a locally generated throwing stub proves registration, ABI, tests, correct runtime behavior, or PR merge.
- Upstream patch scans can be incomplete, and the report flags the completeness. Run a live end-to-end collision audit against main and *all* open PRs before any submission.
- The original readiness.json remains a saved canonical snapshot; this pipeline does not rewrite it or hide its documented discrepancy.
- The NID-only review queue stores no names or executable content. The **separate** public source-candidate queue may carry names copied from publicly available AnyPS5 source only after a symbol safety filter; it never carries function bodies, ABI prototypes, private captures, local paths, credentials or keys.

## Local usage

Use Python 3.12+ (standard library only):

    python -m unittest discover -s tests -v
    git clone --depth 1 https://github.com/boykopovar/AnyPS5.git ../AnyPS5
    python tools/update_progress.py --upstream-dir ../AnyPS5 --skip-prs

Set GITHUB_TOKEN and omit --skip-prs to also scan open PR patches. A fresh upstream clone is necessary for useful live comparisons. Without --upstream-dir, the generator produces an inventory-only report explicitly labeled as lacking upstream evidence.

## Workflow triggers

- Default-branch pushes: regenerate and commit report files to main. Branch pushes run the workflow but do not publish, to prevent stale GitHub Actions pushes racing with source commits.
- Pull request to main: generate read-only preview as a workflow artifact (including fork PRs).
- Scheduled (every three hours): refresh main from AnyPS5; schedule runs are not guaranteed to start at an exact minute.
- Manual workflow_dispatch or externally configured repository_dispatch: refresh on demand.

The workflow needs permission to push reports to the branch. A protected branch may reject automated report commits; the action will fail visibly rather than silently claim the dashboard refreshed. Cross-repository push delivery is not instant unless repository_dispatch is configured; polling is the reliable fallback.

## What stays manual and reviewable

Name verification, publication/licence assessment, canonical shard updates, exact owner/scope decisions, ABI validation, C++ stub implementation and safe deduplication changes. This automation is a discovery/coverage tracking tool, not an approval pipeline.
