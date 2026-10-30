# Candidate reconciliation — sanitized ps5rs review queue

## Scope

This data-only PR is **stacked on PR #1**, which already verified 152 ICU
names. It publishes a sanitized review index of library/NID identities, not
unapproved candidate names or newly verified function bindings.

- Inventory baseline: **314,038** records (302,338 observed as 13.60;
  11,700 historical-only).
- PR #1 baseline: **46,733 named records** and **36,565 distinct named NIDs**.
- Candidate source: [claimore22/ps5rs](https://github.com/claimore22/ps5rs/tree/5f252a658ff470bcb2b6cd15205fd8ca64ae4477)
  pinned at `5f252a658ff470bcb2b6cd15205fd8ca64ae4477`.
- Catalogue source licence: GPL-2.0 (as declared upstream); the local name
  proposals await publication-rights and per-row evidence review.

## Reconciled candidate classifications

| State | Records | Treatment |
|---|---:|---|
| Already verified in the ICU recovery update | **152** | Exclude from further integration |
| Unresolved, requires independent review | **588** | Retain only library/NID identity and review status |
| Withheld by publication filter | **2** | Do not disclose name or qualify |
| **Total** | **742** | 61 libraries |

The original 740 `recovered` classification was made against the **older**
main-branch snapshot. It becomes misleading after PR #1: its 152 ICU
candidates are now resolved. The remaining 588 pending rows represent
**585 distinct NIDs**. The two withheld entries share one NID; the proposed
name is excluded from all public candidate metadata.

## Current vs. conditional projection

| Measure | Actual after PR #1 | If all 588 remaining candidates later pass review |
|---|---:|---:|
| Export identities | 314,038 | 314,038 |
| Named records | **46,733** | **47,321** (+588) |
| Unique named NIDs | **36,565** | **37,150** (+585) |
| Unresolved or withheld | **267,305** | **266,717** (−588) |
| Saved unique qualified throwing-stub candidates | **10,750** | Unchanged absent separate qualification |

**Merging this PR alone does not change any canonical metrics.** The
projection is not a verification result and is not permission to integrate.
None of the firmware/historical shards, library pages, verified-name map,
manifest or canonical readiness JSON are changed by this PR.

A separate read-only audit found **10,749** distinct qualified NIDs after
excluding one withheld NID counted in two library rows. The published **10,750**
is the original saved metric, not a rounded expression of 10,749. Correcting
that inconsistency needs coordinated source-record and derived-artifact updates.

## Per-library analysis and publication gates

See [recovery-candidate-impact.jsonl](recovery-candidate-impact.jsonl) for
all 61 library-level counts. Major remaining pending-review groups include
libSceFollyShared (126), libSceLibcInternal (86) and
libReactNative.Modules.Vsh.WebAppLauncher (72).

Before adding a pending name to the main inventory: independently confirm
exact spelling and NID hash, verify provenance and publication rights,
confirm library ownership and firmware scope, re-check existing named NIDs,
then regenerate all affected shards, name maps, manifests, index pages and
readiness summaries together. Do not promote candidates into ABI-validated
or qualified AnyPS5 stubs merely because of a NID match. Withheld entries
remain withheld under every outcome.

## Reproducibility and limitations

The public queue is intentionally limited to `library`, `nid`,
`classification`, `review_status`, `catalogue` and `revision`.
There are no proposed name strings, candidate source-row copies, private
filesystem paths, scripts, build tools, firmware, ABI signatures or stubs.
This complies with the repository's data-only publication policy.

The unpublished local source ledger reported NID-hash matches, but because
its proposed names are excluded, a full independent *name rehash* cannot be
reproduced from this sanitized queue. Reviewers can check 742 valid JSONL
rows, unique library/NID keys, the 152 ICU overlap, 588 pending cases, two
withheld cases, and the 61-row library impact report. No live AnyPS5
main/open-PR reservation or runtime audit is claimed.
