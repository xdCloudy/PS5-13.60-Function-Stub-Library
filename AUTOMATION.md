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
