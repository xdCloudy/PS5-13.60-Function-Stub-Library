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
blocked if its NID is seen anywhere on current main or an open PR, its library
is touched by any open PR, a central registration path is uncertain, or any
API response or snapshot is incomplete.

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

## Safety model

* Pull request previews have read-only repository credentials.
* Main-branch scheduled work uses the trusted code from main, never executes code
  from an external PR with write credentials, and treats upstream C/C++ as text.
* No source bodies are copied to the catalogue.
* The Pages deployment reads generated static content.
* Checked-in source reports are diffable and provenance-labelled.

See [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md) for the original AnyPS5 scanner design
and [MAINTAINER.md](MAINTAINER.md) for troubleshooting.
