# AnyPS5 integration

This repository supplies metadata, not ready-to-merge patches or implemented functions.

- Confirm system-library ownership against current AnyPS5 policy. Managed/AOT,
  title-supplied middleware and shell-only exports may need exclusion or review.
- Recompute every named NID and retain its export evidence.
- Unknown ABI prototypes remain unknown. Use only a representation explicitly
  accepted by the target library's current upstream conventions.
- Unimplemented paths must throw through NotImplemented_nid_no_patch.
- Filter current main, every open upstream PR and locally reserved NIDs.
- Respect the maximum 150 new function stubs per PR, one library per coherent batch,
  complete public declarations and registrations, conventions, overlap and build gates.
- A candidate assessment in this dataset does not mean these gates passed.

AnyPS5 coverage and reservations describe the commit recorded in manifest.json,
not live GitHub state. Refresh them before generating or publishing a PR.

## Automated upstream observation (read-only)

[READINESS.md](READINESS.md) and [reports/progress.json](reports/progress.json) are generated from the full inventory plus a fresh read-only AnyPS5 main checkout. The scanner recomputes candidate NIDs from `APS5_VABI` source definitions and requires an existing verified library/NID/name binding before reporting a match. Definitions are **not** proof of runtime behavior, full registration, ABI validation or a merged contribution. `NotImplemented_nid_no_patch` matches remain throwing stubs, never implemented behavior.

GitHub Actions polls upstream open PRs and interprets added `APS5_VABI` patch lines as *possible* reservations. API failures, missing patches or PR caps mark the reservation scan incomplete; run a fresh comprehensive AnyPS5 overlap audit before submitting new stubs.

Previously unknown upstream definitions become NID-only entries in [the review queue](reports/upstream-review-queue.jsonl). The automation does not insert new names into canonical shards or upgrade classifications without independent NID, provenance, ownership and publication review.
