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
automation/dual-firmware-review. It runs twice daily or by manual dispatch.

## Classification

- dual_3.20_and_13.60: name/NID pair appears in both sources and a
  confirmed 13.60 catalogue record is an assessed missing throwing-stub
  candidate in an eligible system library.
- confirmed_13.60_only: same 13.60 constraints, but no identical 3.20
  forwarder observation.
- historical_3.20_only: recorded for research, **not** promoted into 13.60.
- Other rows remain excluded from candidate sampling with counts explaining
  covered, reserved, mismatched, unsafe, or unverified source states.

The current AnyPS5 main/open PR comparison is explicitly marked as a
snapshot. The existing final publisher must perform a fresh and complete
overlap scan immediately before publication.

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

Results are metadata-only, capped at 75 sampled candidates per source
class by default, and produce zero automatic approvals or upstream PRs.
