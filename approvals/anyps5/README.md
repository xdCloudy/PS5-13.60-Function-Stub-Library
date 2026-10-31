# Independently reviewed AnyPS5 submission queue

The six-hourly `.github/workflows/anyps5-auto-dispatch.yml` workflow reads
**only** reviewed pairs of files from this directory on trusted `main`:

- `<batch>.jsonl` contains 1–100 independently validated **void** C ABI
  records for one library. The format is the same as
  `tools/prepare_anyps5.py`: `library`, `nid`, `name`, `return_type`
  (`void`), `parameters`, `abi_reviewed: true`, and an independent
  evidence URL per function.
- `<batch>.approval.json` is a separate explicit publication attestation.
  It must declare exactly `schema_version: 1`,
  `approved_for_auto_submit: true`, `reviewed_by: "xdCloudy"`,
  `review_url` linking to a catalogue repository pull request, and
  `evidence_sha256` of the *exact* JSONL bytes.

Example approval metadata (replace the digest with the real file SHA-256):

```json
{
  "schema_version": 1,
  "approved_for_auto_submit": true,
  "reviewed_by": "xdCloudy",
  "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/33",
  "evidence_sha256": "0000000000000000000000000000000000000000000000000000000000000000"
}
```

**The example is not an approval**, and no live approval data is included in
this directory. An explicit merged review and individually supported ABI is
required; simply putting `abi_reviewed: true` in an auto-generated file
does not establish correctness. Do not commit unverifiable candidates.

The selector checks the exact evidence digest, owner identity, review
attestation, name-to-NID hashes, catalogue qualification and firmware scope.
It rejects mixed-library, oversized, duplicate and partially eligible batches.
Already-published digest-addressed fork branches are skipped. Unknown or
unreachable GitHub state blocks the run, rather than allowing an optimistic
submission.

When an approved batch is available, the scheduler dispatches the existing
publisher with an **immutable commit-pinned public URL** and exact digest,
`publish=true`. The publisher revalidates all source, live upstream PR and
fork-branch conflicts, builds and tests AnyPS5, then uses
`ANYPS5_SUBMIT_TOKEN` only for the last draft-PR submission. No automatic
merges, no overwrites and no guessed signatures or guest behaviour.

**Not supported by this queue:** implementing existing functions using
`nullptr`, zero, false or a no-op. Those require separate *per-function
behavioural evidence*, even where a declaration or 3.20 forwarding name
exists. This queue generates reviewed **throwing** stubs only.

The schedule is intentionally a no-op with an empty queue. One eligible
batch is dispatched per run, avoiding a PR flood. For a retry of a
previously submitted function, first reconcile its upstream PR rather
than altering old approval files.
