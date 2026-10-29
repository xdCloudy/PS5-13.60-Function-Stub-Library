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
