# PS5 13.60 — readiness dashboard

**What is this?** An auditable export-name catalogue and AnyPS5 stub research tracker. An export record is **not** a working function, and the inventory is much larger than the eligible system-library stub backlog.

**Last refresh:** 2026-10-30T13:00:07+00:00 · **AnyPS5 main:** [f91137142eaf](https://github.com/boykopovar/AnyPS5/commit/f91137142eafd5df646fca6419a1fc4ef61b89d9)

## At a glance

| Workstream | Progress | Meaning |
|---|---:|---|
| **Recovered names** | **47,085 / 314,038 (15.0%)** | Inventory rows with a published name, not necessarily an ABI signature |
| **AnyPS5 main (live source matches)** | **15,544 library/NID identities** | Matching definitions already present in merged upstream source; not proof of runtime functionality |
| **Qualified throwing-stub candidates** | **10,749 unique NIDs** | Current eligible research backlog, not implemented functions |
| **Locally generated stubs** | **963 / 10,749 (9.0%)** | Historical snapshot of throwing placeholders, not live upstream coverage |

### Name recovery

`███░░░░░░░░░░░░░░░░░░░` **15.0%** — 266,953 unresolved/withheld records.

### Local stub generation (saved snapshot)

`██░░░░░░░░░░░░░░░░░░░░` **9.0%** — placeholders commonly throw rather than implement behaviour.

## How to interpret the pipeline

| Gate | Count | Interpretation |
|---|---:|---|
| Published named export records | 47,085 | Has an associated name, but does not prove correct types/ABI |
| Strictly rehashed named records | 39,966 | Stronger local NID/name/status evidence |
| Qualified unique NIDs | 10,749 | Existing candidate assessments after withholding filter |
| Strictly rehashed qualified NIDs | 9,158 | Conservative subset used for exact source matching |
| Locally generated throwing stubs (saved) | 963 | Not necessarily compiled or merged |
| Statically prepared (saved) | 963 | Historical offline gates |
| Fully validated (saved) | 0 | Historical build/runtime validation only |
| **Present in AnyPS5 main source (live)** | **15,544** | Matched and rehashed library/NID/name in current upstream main; separate from qualified backlog |
| With NotImplemented marker (live) | 12,285 | Source-level placeholder, not working behaviour |
| With nonthrowing C ABI body (live) | 3,259 | No matching NotImplemented marker; **not** necessarily a tested implementation |

**Qualification correction:** the saved report listed 10,750, while the filtered count is 10,749 (difference +1 from saved). Separately, 7,119 named records need strict name/NID/status evidence review. These must not be silently promoted. The old `published to AnyPS5 = 0` is an **archived snapshot** and must not be treated as the current upstream count.

## AnyPS5 upstream — what is already being worked on?

| Evidence | Count | Meaning |
|---|---:|---|
| **Catalogued names present on merged AnyPS5 main** | **15,544 records / 15,537 unique NIDs** | **Live source evidence**, not the saved 0-counter |
| Marked throwing/unimplemented | 12,285 | NotImplemented marker is visible in body |
| Other nonthrowing source definitions | 3,259 | A source body exists; not necessarily correct, wired up or validated |
| Qualified NIDs also in main source | 7,687 | Potential existing coverage |
| Additional qualified NIDs seen in open-PR additions | 1,327 | Possible reservations, not yet merged |
| Qualified NIDs not observed by scans | 1,735 | **Not proof of no overlap** |

### Open PR coverage

`█████████████████████░` **1,388 / 1,450 (95.7%)** current open PR heads indexed.

**Partial:** 62 PR heads remain. Scheduled runs accumulate SHA-keyed observations.
Cache hits: 851 · newly scanned: 537 · failed checks: 13.
**Before submitting a stub PR, still run a final exact overlap review against current main and all open PRs.**

## Automatically imported AnyPS5 source evidence

**10,129** public source-name proposals are available in the [review queue](reports/upstream-source-candidates.jsonl); **3** correspond to unnamed identities already in this firmware catalogue.

The proposed name, NID and source location are searchable, but the name is **not independently verified against firmware**, nor are ABI or behaviour confirmed. Publication-filtered strings are not promoted. [NID-only review queue](reports/upstream-review-queue.jsonl).

## Duplicates are review targets, not deletion instructions

| Identity measure | Count |
|---|---:|
| Indexed export records | 314,038 |
| Distinct NID strings globally, across all scopes | 300,846 |
| Extra cross-library NID records | 12,302 |
| Repeated library/NID across inventory partitions | 890 |

Shared NIDs can be valid exports owned by different libraries. The canonical export inventory preserves their identities. Managed/application and historical-only records are **not automatically AnyPS5 system-library stubs**.

## Which libraries should be reviewed next?

Top 12 libraries sorted by assessed qualified records not seen in current main or scanned PR additions. This is a triage estimate, not a verified patch backlog.

| Library | Qualified pending records | Main matched names (all statuses) | Main pending overlaps | Open PR pending overlaps | Not observed pending |
|---|---:|---:|---:|---:|---:|
| libSceJsc | 2,951 | 84 | 0 | 313 | 2,638 |
| libSceNKWebKit | 8,614 | 7,336 | 7,211 | 0 | 1,403 |
| libSceNpCommon | 782 | 289 | 0 | 669 | 113 |
| libSceVideoOut | 133 | 148 | 100 | 0 | 33 |
| libSceMediaFrameworkInterface | 139 | 0 | 0 | 107 | 32 |
| libSceVnaInternal | 84 | 0 | 0 | 71 | 13 |
| libSceIcu | 72 | 0 | 0 | 60 | 12 |
| libSceVideoStreamingEngine | 58 | 58 | 46 | 0 | 12 |
| libSceCustomMusicSysCallWrapper | 53 | 1 | 0 | 42 | 11 |
| libSceFont | 44 | 201 | 36 | 0 | 8 |
| libSceFontGs | 8 | 0 | 0 | 0 | 8 |
| libSceSaveData | 8 | 0 | 0 | 0 | 8 |

See [all 791 libraries](reports/library-progress.md) or [machine-readable metrics](reports/progress.json) for the full breakdown.

## How it updates

1. This repo's pushes refresh inventory and report files.
2. Scheduled checks inspect AnyPS5 main and progressively scan **all** open PR heads, reusing cached results only when the head SHA remains unchanged.
3. Public source names are staged for audit, without silently rewriting canonical names or qualification.
4. Matching current AnyPS5 main definitions updates the external-source mirror and the live stage counts automatically; no manual movement between snapshot categories is needed.
5. The final build, ABI, ownership and full pre-submission collision check remains a separate gate.

[How synchronization works](UPSTREAM_SYNC.md) · [Integration policy](ANYPS5.md) · [Publication controls](DATA_POLICY.md)
