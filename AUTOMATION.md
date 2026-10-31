# How the automation works

The project keeps two separate kinds of data:

1. **Canonical inventory**: reviewed library/NID records and name evidence under data/.
2. **External observations**: reproducible source matches, review queues and coverage reports under reports/.

A public project adding a symbol never, by itself, changes its firmware version,
ABI verification or runtime classification.

## The refresh cycle

Every three hours, or through a manual workflow run:

1. Check out trusted catalogue main and run its unit tests.
2. Read-only clone current AnyPS5 main and record its exact commit.
3. Refresh the previous manifest's hashes and generate AnyPS5 source observations.
4. Progressively inspect the open PRs, reusing cached results only for the same PR head SHA.
5. Read-only clone DNNDHH/PS5-3.20_Libs and record its exact commit.
6. Pair each sprx_dlsym registration with its named forwarding pointer and recompute the NID.
7. Compare the observed (library, NID) against both canonical firmware partitions.
8. Quarantine mismatches, unsafe names and uncertain owners instead of silently modifying data.
9. Generate the six matrices, Markdown fallback and GitHub Pages JSON.
10. Publish report-only changes using the repository's established main-branch mechanism.

**Polling is not real time.** Refresh times and incomplete PR scans remain visible.
Missing patches and incomplete pagination fail closed.

## Run the pipeline locally

Python 3.12+ and Git are required. No proprietary firmware or local personal
research files are needed.

~~~sh
python -m unittest discover -s tests -v
git clone --depth 1 https://github.com/boykopovar/AnyPS5.git ../AnyPS5
git clone --depth 1 https://github.com/DNNDHH/PS5-3.20_Libs.git ../PS5-3.20_Libs
python tools/refresh_manifest.py
python tools/update_progress.py --upstream-dir ../AnyPS5 --skip-prs
python tools/ingest_320.py --source-dir ../PS5-3.20_Libs
python tools/build_coverage.py
~~~

To include open PR observations, set GITHUB_TOKEN and omit --skip-prs from
update_progress.py. A partial scan is **not** an overlap clearance.

## Reconciliation rules

* Primary identity: case-insensitive logical library plus **exact case-sensitive NID**.
* Cross-library NID repetition: a possible alias; retain all owners for review.
* Name recovery: hash matching is necessary, not sufficient to approve a canonical name.
* Firmware version: a 3.20-only record never becomes 13.60-confirmed automatically.
* Publication filter: withheld names never leak into the source review queue.
* ABI status and implementation quality: cannot be inferred from source presence.
* Import caching: source SHA, content digest, manifest digest and parser version must match
  before skipping a complete re-ingestion.

The importer writes reports/source-320.json and reports/source-320-review.jsonl,
not the original C forwarding code or canonical inventory.

## Draft catalogue-import PR preparation

After a successful refresh on trusted main, the separate
`.github/workflows/catalogue-import-review.yml` workflow rechecks the
catalogue manifest and stages strictly sanitised, hash-compatible name or
historical-reference **proposals**. It opens or updates a single stable-branch draft GitHub
pull request when it finds reviewable identities. A changed source revision
updates an existing open proposal instead of creating another PR. Conflicts and publication-filtered names are excluded.

The draft contains only public metadata in
`reports/catalogue-import-proposal.json`, **not** a rewritten canonical
inventory or an approved name binding. Independent review of provenance,
source licensing and firmware/owner evidence remains necessary.

Automatic PR creation requires `Allow GitHub Actions to create and approve
pull requests` in the repository's **Settings → Actions → General →
Workflow permissions**. Without that permission, the workflow may push a
review branch but cannot open the PR; the failed step is visible in Actions.
The review workflow never runs or executes code from untrusted external PRs.

## Promoting independently approved names into canonical inventory

The staged metadata is not enough to publish. A second, trusted-main workflow,
`.github/workflows/approved-catalogue-import.yml`, reads separately reviewed
decisions from `approvals/catalogue-name-approvals.jsonl` and applies only
previously unresolved **existing library/NID identities**. All source names
are rehashed; the reviewer must attest independent evidence, ownership,
firmware scope, publication rights, and a linked review PR.

The importer keeps old firmware classifications, does not invent additional
identities, rejects withheld names, checks collisions in the canonical name
map, and regenerates affected shards, the index, library pages, verified-name
map, manifest and readiness snapshot. It produces an auditable import ledger.

A successful review decision does not merge automatically: the action opens a
separate **draft** canonical-import PR for maintainers to review. The proposal
workflow keeps one open draft PR and updates its source evidence without
creating new PRs for source-only revisions. If a previous attempt pushed a
branch but failed to create its PR, the workflow recovers the orphaned branch.
A deliberately closed review of the same identities stays closed; genuinely
new identity work uses a fingerprinted review branch. Unreadable past review
evidence blocks publication rather than bypassing review history.

When the stable approved-import PR branch already exists, the current workflow
blocks rather than overwriting unreviewed changes. This requires reconciliation;
it is a deliberate remaining limitation, not successful automatic deduplication.

The approval format and trust requirements are documented in
[approvals/README.md](approvals/README.md). Human rights/evidence attestation
is not replaced with a hash match. No approval decisions have been committed.

## Candidate-specific AnyPS5 collision proof

`tools/candidate_overlap.py` is a **separate live gate** used only when the
stub generator runs with `--apply`. It enumerates current open PRs, retrieves
each exact head SHA and changed-file count, checks every file page and patch
for omissions, and repeats the head enumeration afterwards. A candidate is
blocked if its NID is seen anywhere on current main or an open PR, an actual NID or export overlaps a current PR, a global registration path is uncertain, or any
API response or snapshot is incomplete.

Unrelated source edits in the same library are not function overlaps.

This gate deliberately does **not** change
`open_pr_symbol_coverage_complete = False` in the legacy progress cache.
A complete series of cached *recognised* patches cannot certify that every
possible C++ registration form was parsed. The live audit records a per-PR
head vector and the reason for every candidate-level verdict. Publication is
not allowed on a heuristic absence result.

`tools/layout_patch.py` preserves upstream macros and places throwing void
functions in reviewed ABI regions. CI read-only probes the current
`libSceAudioIn`, `libSceVideoOut` and `libSceUserService` source layouts;
ambiguous layouts fail rather than guessing a filename.

## Draft AnyPS5 contributions

tools/prepare_anyps5.py is explicitly opt-in, operates in a **separate AnyPS5
checkout** and requires a reviewed ABI JSONL file **outside** this repository.
Currently its safe generation envelope is void-returning, reviewed signatures.
Unknown/non-void ABIs are not fabricated.

~~~sh
python tools/prepare_anyps5.py \
  --anyps5-dir ../AnyPS5 \
  --abi-file ../reviewed-abis.jsonl \
  --output-dir ../anyps5-review-patches
~~~

For --apply, use a clean, dedicated AnyPS5 branch based on current main.
The tool rechecks every open PR head and blocks publication on incomplete scans.
It then runs the upstream convention and overlap tools. The generated draft
description explicitly says that build and runtime validation remain outstanding.
The default command is read-only and does not open a PR or write into the catalogue.

## Submitting reviewed AnyPS5 stubs as xdCloudy

The opt-in Actions workflow **Prepare and optionally submit AnyPS5 stub
batch** requires a public GitHub/Gist raw JSONL containing independently
reviewed ABI prototypes, a pinned SHA-256 digest, and a maximum of
100 functions. Draft publication is off by default. No missing signature
is guessed, and a hash match is not proof of ABI correctness.

The preparation job runs without the personal submission token: it selects
one library, commits a throwing-only stub patch, checks exact candidate
NIDs against all current open upstream PRs, runs AnyPS5 conventions and
the official Git-commit-aware overlap checker, and attempts the complete
Linux CMake build and CTest. It records the patch and the audited batch.

When publication is enabled, a separate clean runner reconstructs that
patch, confirms upstream main is unchanged, and repeats a live exact
candidate overlap audit immediately before requesting the submission token.
It verifies the token belongs to xdCloudy, pushes to the personal AnyPS5
fork, and opens a draft PR against the upstream repository. The branch
is never overwritten and is removed if PR creation fails.

The Actions secret must be named ANYPS5_SUBMIT_TOKEN and configured in
the catalogue repository Settings > Secrets and variables > Actions.
A fine-grained token restricted to the fork may be unable to create a
cross-fork PR into an unrelated public upstream repository; if GitHub
refuses it, a classic token with public_repo permission is an option.
Never supply a personal token as workflow inputs or in source code.

ABI evidence must be independently checked before review. Passing a
Linux build does not prove guest ABI or console runtime correctness.

## Scheduled, evidence-gated AnyPS5 PR submission

The new `.github/workflows/anyps5-auto-dispatch.yml` runs every six
hours and can also be triggered manually. It automatically selects the
first eligible, not-already-submitted **explicitly reviewed** ABI batch in
[`approvals/anyps5/`](approvals/anyps5/README.md). With an empty queue it
exits successfully and **opens no PR**.

Each batch is a library-specific JSONL paired with a separate approval file
on trusted `main`, signed off via a linked catalogue PR and pinned to an
exact SHA-256. The scheduler validates the NID hash, 13.60 provenance, ABI
review declaration, current catalogue eligibility, fork-branch state, duplicate
identities and maximum 100 functions. It dispatches the existing submission
workflow with a raw GitHub URL pinned to the **actual committed SHA** and
`publish=true`. The submission workflow independently verifies the source
bytes, rebuilds AnyPS5, audits main/open PR heads and creates a draft upstream
PR as `xdCloudy` only if the final gates pass.

Each contribution branch is addressed by the first 16 hex characters of the
reviewed evidence SHA-256. An existing branch is never overwritten. The
scheduler skips existing contribution branches; a failed/unreachable Git query
fails closed. It dispatches at most one batch per run, avoiding a mass
submission and letting upstream reviews settle.

This does **not** automatically approve newly discovered NIDs or invent ABI
prototypes. In particular, PS5-3.20_Libs contains forwarders, not
behavioural evidence. This workflow generates reviewed *throwing void stubs*,
not zero/null/false/no-op implementations. Constant-return implementations
need their own evidence-specific generator and separate tests. A scheduled
run cannot make independently reviewed ABI or behaviour proof unnecessary.

For unattended submission to work, `ANYPS5_SUBMIT_TOKEN` must exist as a
repository Actions secret, belong to `xdCloudy`, support pushes to the
personal AnyPS5 fork and PR creation against `boykopovar/AnyPS5`. The
scheduled dispatcher uses only the short-lived Actions token with
`actions: write` to start the publisher; it does not receive the personal
submission secret. Without the verified secret and queued approved candidates,
successful PR publication cannot be claimed.

## Scheduled existing-stub constant/null/no-op implementations

The independently gated constant-function stream is **not** the throwing-stub
stream. `.github/workflows/anyps5-constant-auto-dispatch.yml` checks
[`approvals/anyps5-constants/`](approvals/anyps5-constants/README.md) every
six hours and after trusted-main approvals merge. For the first
unpublished, owner-reviewed, digest-pinned one-library batch (1–150
functions), it dispatches `anyps5-constant-submit.yml` with an immutable
source-revision URL and `publish=true`. An empty approval queue is a
successful, safe no-op.

`tools/prepare_anyps5_constants.py` can only modify a pre-existing
`APS5_VABI` source function with a matching declaration, registered CMake
source file, matching canonical name/NID, independently reviewed original
signature+body SHA-256, and a body containing **only**
`NotImplemented_nid_no_patch(__func__);`. The declared return type
must support exactly the reviewed `return 0;`, `return false;`,
`return nullptr;` or an empty `void` body. It cannot infer
semantics from a function name, stub inventory, 3.20 forwarding wrapper
or generic default. It cannot add or change API declarations.

The publisher commits and tests the exact changes, builds the specific
affected library target even when upstream marks it `EXCLUDE_FROM_ALL`,
runs Linux CTest and AnyPS5 conventions, and reconstructs the verified
patch on a fresh runner. The final gate independently rechecks upstream
main and every open Git PR head, including body-only edits to the
specific function that would evade a declaration/export-only scan;
other functions in the same file do not falsely reserve that identity.
Pending generated contributor branches from **both** streams are
checked. Only then does the isolated publisher load the private
`ANYPS5_SUBMIT_TOKEN`, atomically create a unique evidence-digest
branch on `xdCloudy/AnyPS5`, and open a **draft** upstream PR.

A complete Linux build is not console runtime/ABI proof. The
attested behaviour must have independently reviewed evidence *before*
a candidate is committed to the approved queue. No active such
evidence is included by default; absent reviewed data means no
upstream submissions.

## Automatic existing-stub evidence discovery (no speculative implementations)

`tools/discover_anyps5_constant_candidates.py` now runs during trusted-main
readiness refreshes and pull-request previews. It walks the current public
AnyPS5 checkout and selects **only** functions with:

- an exactly single `APS5_VABI` source definition in a registered CMake
  file, and one same-name, matching-return-type public ABI declaration;
- a precisely isolated `NotImplemented_nid_no_patch(__func__);` body;
- a return type supported by the separate constant/no-op publisher
  (integer, boolean, pointer or void).

The reproducible result is written to
`reports/anyps5-constant-candidates.jsonl` in the job and uploaded as
an Actions artifact for inspection (14-day retention). Each row has its
upstream SHA, original source and declaration paths, name/NID,
signature/body SHA-256 and return-type category.

Every row explicitly has `behavior: null`,
`behavior_reviewed: false`, `evidence: null` and
`review_status: independent_semantic_and_abi_review_required`.
**The scanner does not call zero, false, null or a no-op the correct
behaviour just because that value compiles.** The output is never added
to `approvals/anyps5-constants` or dispatched upstream automatically.

Use the artifact as a reproducible **review candidate list**, then
provide independently validated behavioural evidence and explicit
owner approval in the format documented in
[`approvals/anyps5-constants/README.md`](approvals/anyps5-constants/README.md).
Approved batches are subsequently picked up by the unattended draft
PR publisher and its complete live overlap/build/security gates.

## Safety model

* Pull request previews have read-only repository credentials.
* Main-branch scheduled work uses the trusted code from main, never executes code
  from an external PR with write credentials, and treats upstream C/C++ as text.
* No source bodies are copied to the catalogue.
* The Pages deployment reads generated static content.
* Checked-in source reports are diffable and provenance-labelled.

See [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md) for the original AnyPS5 scanner design
and [MAINTAINER.md](MAINTAINER.md) for troubleshooting.
