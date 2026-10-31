# Dual-firmware AnyPS5 review pipeline

The scheduled workflow in .github/workflows/dual-firmware-review.yml
prepares a separate, review-only candidate report from two sources:

- **3.20:** the original public DNNDHH/PS5-3.20_Libs generated forwarding
  sources. This establishes historical name/NID observations only.
- **13.60:** data/firmware-13.60 in this repository. These rows must explicitly
  mark the export as 13.60-confirmed. The historical-3.20-only shard is excluded.

The workflow checks out trusted main, clones the original 3.20 repository,
runs tools/dual_firmware_review.py and its regression tests, uploads an
artifact and opens/updates one draft catalogue PR at
automation/dual-firmware-review. It runs twice daily or by manual dispatch. In addition to the 75-row-per-class
review PR preview, it uploads the complete untruncated JSONL review queue and
runs a separate direct-source scan against the latest AnyPS5 main. It also
checks symbol names against two independent public SDK header collections:
PS5Dev/PS5SDK and ps5-payload-dev/sdk, pinning their source commits and
recording only file/line references (not GPL-licensed header text).

## Classification

- dual_3.20_and_13.60: name/NID pair appears in both sources and a
  confirmed 13.60 catalogue record is an assessed missing throwing-stub
  candidate in an eligible system library.
- confirmed_13.60_only: same 13.60 constraints, but no identical 3.20
  forwarder observation.
- historical_3.20_only: recorded for research, **not** promoted into 13.60.
- Other rows remain excluded from candidate sampling with counts explaining
  covered, reserved, mismatched, unsafe, or unverified source states.

The direct source scan marks candidates with APS5_VABI declarations or literal
APS5_EXPORT aliases in present AnyPS5 main, reporting exact repository paths.
It does not deduce absence from a missing textual match because exports can be
macro-generated. Its output is explicitly **not ABI certification**.

The current AnyPS5 main/open PR comparison is marked as a snapshot, and source
PR coverage may be incomplete. The existing final publisher must perform a
fresh, **complete** overlap scan immediately before publication. Incomplete
scans block publication. The review queue is not a publisher input.

Both public SDKs are works in progress and are not guaranteed to provide the
correct ABI for each PS5 firmware. Even matching header names in both sources
do not automatically approve prototypes or guest behaviour.

## Submission and approval rules

The generated report is NEVER an ABI or behaviour approval. In particular,
names, NIDs, original forwarders, and 13.60 export-table records cannot prove
a C++ prototype, return value, correct no-op semantics, guest ABI or behaviour.

A maintainer must independently establish evidence for exact signatures,
function ownership and behaviour, then approve immutable JSONL records in
the existing approvals/anyps5 (throwing stubs) or
approvals/anyps5-constants (verified constant-return implementations) queues.
Only those existing approval-controlled workflows may build and open an
upstream draft AnyPS5 PR. Automatic merging is prohibited.

The existing ANYPS5_SUBMIT_TOKEN repository secret is used only when
publishing the *catalogue's own draft review PR* in this workflow; downstream
publishers use the same secret at their own final submission gate.
Do not put credentials or proprietary firmware blobs in report artifacts.

The review PR is intentionally not reopened automatically after a maintainer
closes or merges it. Any next review cycle requires deliberate reconciliation.

## Local dry run

From this repository checkout:

    python -m unittest discover -s tests -p 'test_dual_firmware_review.py' -v
    git clone --depth 1 https://github.com/DNNDHH/PS5-3.20_Libs.git ../PS5-3.20_Libs
    python tools/dual_firmware_review.py \
      --source-320 ../PS5-3.20_Libs \
      --out-json /tmp/dual-firmware-triage.json \
      --out-md /tmp/dual-firmware-review.md

Results are metadata-only and produce zero automatic approvals or upstream
PRs. The Markdown and small JSON review summary sample 75 candidates per
source class, but the GitHub Actions artifact includes EVERY candidate in
dual-firmware-all-candidates.jsonl and their direct-source observations in
dual-firmware-reviewed-against-main.jsonl, plus public SDK header evidence
hints in dual-firmware-public-evidence-hints.jsonl.

The authorized submission secret remains required only for the catalogue
review PR and the existing approved upstream submission workflows.

## Priority queue

The workflow also emits dual-firmware-priority-queue.jsonl and the concise
dual-firmware-priority.md report. They rank 13.60-confirmed candidates that
have **no direct** APS5_VABI or literal APS5_EXPORT source observation,
prioritising a matching historical 3.20 source. The source-existence check
is not exhaustive: macros, aliases, open PRs, and generated definitions may
still claim these exports. A candidate is only an investigation target,
not permission to write a stub. Historical 3.20-only records are excluded.

The reviewed report and priority table are updated on the existing review
PR; the complete unapproved ranked queue remains in the run artifact.
