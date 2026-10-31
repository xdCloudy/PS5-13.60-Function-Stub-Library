# Reviewed existing-function constant/no-op implementation queue

This queue is **separate** from `approvals/anyps5/`, which covers
new, unimplemented throwing void stubs. This queue only implements
**already-declared and already-defined** AnyPS5 functions whose *complete*
semantics have been independently established to be one constant result or a
genuine no-op.

The scheduled workflow `.github/workflows/anyps5-constant-auto-dispatch.yml`
runs every six hours and whenever this queue is changed on trusted `main`.
It selects one reviewed, previously unpublished library-specific batch,
dispatches the checked-in publisher and opens a **draft** upstream PR as
`xdCloudy` after all gates pass.

## Exact evidence format

Each pair consists of `<batch>.jsonl` with 1–150 rows in **one library** and
`<batch>.approval.json` with owner-approved, pinned source bytes.

Example row **shape only** (the fabricated hashes below are not valid
evidence and must not be submitted):

```json
{
  "library": "libSceExample",
  "nid": "HASHFROMNAME",
  "name": "sceExampleFunction",
  "path": "core/libs/prx/libSceExample/Export.cpp",
  "behavior": "zero",
  "behavior_reviewed": true,
  "signature_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "body_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "evidence": "https://example.org/independent-primary-source",
  "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/34"
}
```

The `nid` must be the **actual** matching PS5 NID for the exact name; the two
hashes are of the original `APS5_VABI` C++ signature and *entire original
function body*, respectively, without modification. Record evidence URLs
must support the **behaviour**, not merely the name, NID, ABI or source
forwarder. The accepted `behavior` values are:

- `zero` — integer-returning function, `return 0;`
- `false` — `bool` function, `return false;`
- `null` — pointer-returning function, `return nullptr;`
- `noop` — `void` function with no statements

Original bodies must contain **only** `NotImplemented_nid_no_patch(__func__);`.
There must be exactly one source definition and one matching public
`APS5_VABI` declaration, and exactly the independently reviewed original
bytes. Functions with nontrivial state, out-parameters, alternate error
codes, callbacks, registers, or unknown ABI/semantics are not eligible.

Example approval metadata **shape only**:

```json
{
  "schema_version": 1,
  "approved_for_auto_submit": true,
  "reviewed_by": "xdCloudy",
  "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/34",
  "evidence_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
}
```

These examples are placeholders, not endorsements or approved candidates.
A merged review authorisation is required before adding actual queue files.
No review approvals are currently checked into this directory. The empty
queue correctly creates **zero** upstream PRs.

## Submission safeguards

The generator does not create declarations, exports, dependencies, or
new function entries. It only replaces independently reviewed original
throw-only bodies and verifies return-type compatibility. The publisher
performs the AnyPS5 convention and official overlap checks, Linux full
build and CTest; a separate uncredentialed publisher reconstructs the
expected exact edits and audits every current upstream PR head and pending
fork branch. The extra Git-hunk audit detects PRs modifying the *same
function body* even without repeating its symbol name, while allowing
unrelated edits to other functions in the same file. Unknown or moving
upstream states prevent publication.

Branches are `feat/automated-reviewed-constants-<first-16-sha256>`,
created **without overwrites**, with draft PRs opened as `xdCloudy`
only when the private `ANYPS5_SUBMIT_TOKEN` is valid and authorised.
No automatic upstream merges. A Linux build does not constitute PS5
runtime validation.

**PS5-3.20_Libs generated .c files are forwarding wrappers; they cannot
establish null/zero/no-op semantics.** Do not promote such files into
reviewed behaviour evidence.
