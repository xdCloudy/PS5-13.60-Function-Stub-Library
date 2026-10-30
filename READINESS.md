# PS5 13.60 — live readiness

Generated from the checked-in inventory and a read-only AnyPS5 upstream checkout.
No executable stubs or firmware are included here.

## Export inventory and name recovery

| Metric | Count |
|---|---:|
| Export library/NID identities | 314,038 |
| Firmware 13.60 observed exports | 302,338 |
| Historical-only references | 11,700 |
| Logical libraries | 791 |
| Published named records | 47,085 (14.99%) |
| Strict NID/name reverified records | 39,966 |
| Named records requiring status/hash reconciliation | 7,119 |
| Unresolved or withheld records | 266,953 |
| Unique NIDs across all scopes | 300,846 |
| Extra cross-library NID records (not deletions) | 12,302 |
| Repeated library/NID identities across partitions | 890 |

## Stub progress — distinct stages

| Measure | Count | Evidence level |
|---|---:|---|
| Qualified unique NIDs (recomputed) | 10,749 | Named inventory assessment, excluding withheld identities |
| Strictly rehashed qualified unique NIDs | 9,158 | Stronger gate for upstream matching || Generated throwing stubs | 963 | Saved local snapshot |
| Offline statically prepared | 963 | Saved local snapshot |
| Fully validated | 0 | Saved local snapshot |
| Published to AnyPS5 | 0 | Saved historical snapshot; **not live** |
| Qualified NIDs with matching AnyPS5 main source definitions | 0 | Source scan, not export/runtime validation |
| Additional qualified NIDs seen in open-PR additions | 1,105 | Best-effort PR patch scan |
| Qualified NIDs not seen by these scans | 9,644 | Not proof they are missing upstream |
| Additional upstream NID observations needing review | 10,078 | No unverified names published |

**Saved qualified-count discrepancy:** 10,750 published versus 10,749 recomputed (delta +1). This report does not silently modify canonical assessments.

## Upstream observation

- AnyPS5 main revision: `7d4006607aca6f71e80f6352d94e55b314ebaf41`
- Open PRs observed: 1481
- Open PRs scanned: 400
- Open PR audit complete: NO — do not treat reservations as exhaustive

## Source and safety limits

Matching a source definition does not confirm its registration, exported NID, ABI, correct runtime behavior, or merge status. A throwing marker indicates only a source-level NotImplemented call. Multiple libraries sharing a NID are preserved until ownership and equivalence have been independently resolved.

Qualification counts reflect existing catalog assessments with withheld names excluded; strictly rehashed matches are a separate subset, not the full qualification inventory.

The strict rehash gate includes only records with verified_nid_binding status and a matching local SHA1 NID; other named records are withheld from automatic upstream reconciliation until separately audited.

Upstream-only observations are stored as **NID-only review candidates** in [upstream-review-queue.jsonl](reports/upstream-review-queue.jsonl); symbols cannot be promoted to verified names or qualified stubs without independent review.

See [machine-readable progress](reports/progress.json), [library breakdown](reports/library-progress.md), [AnyPS5 integration rules](ANYPS5.md), and [publication policy](DATA_POLICY.md).
