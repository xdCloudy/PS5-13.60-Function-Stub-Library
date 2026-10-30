# Maintainer troubleshooting and release checks

## Before merging a catalogue or automation PR

1. Check for overlap with current main and all open catalogue PRs.
2. Run the unit suite and ensure the canonical manifest still agrees with all
   shard counts and hashes.
3. Confirm source revisions are recorded and public metadata only is emitted.
4. Inspect quarantine records: NID mismatch, conflicting names, missing owner
   or unsafe strings must not be automatically promoted.
5. Confirm a historical-only identity has not become 13.60-confirmed without
   separate firmware evidence.
6. Ensure the Markdown matrices and site/data.json match the same generated JSON.
7. Review the security boundary of the workflow: PR previews read-only,
   main-only jobs with write permission.

## Common failure modes

**3.20 parser reports unparsed registrations:** The upstream generator may
have changed its dlsym syntax. Compare a real file to parse_forwarders(),
extend a regression fixture, and re-run a full scan. Never silently discard
the unmatched registrations.

**Manifest mismatch:** Do not change totals to satisfy the tests. Fix the
underlying inventory, index and manifest together through a separate reviewed
canonical-data change.

**PR scanner incomplete:** Check the number of open heads, missing patches,
head SHA changes, API limits and errors. Incomplete reservations are unknown,
not available stub slots. Re-run the scheduled collector; never override
the final publication gate.

**Source names withheld:** Check the publication filter. Never publish an
unsafe string in an error message or proposal.

**Dashboard stale:** Check the last successful workflow run, data.json
deployment revision and Pages settings. A browser refresh cannot create new
source evidence.

**AnyPS5 patch blocked:** Verify the ABI review file is external, the library
ownership is eligible, the strict name binding is present, the main head
has been updated, and all PR scans completed. The generator is intentionally
restricted to reviewed void signatures and does not fabricate unknown ABIs.

## Outstanding production gates for PR #10

The read-only PR preview can establish source parsing, report consistency,
layout placement and unit-test correctness. It **cannot** verify privileged
workflows or deploy Pages from an unmerged branch.

Before declaring the automation production-ready:

1. Confirm GitHub Pages source is **GitHub Actions** under
   **Settings → Pages → Build and deployment**. Confirm the deployment URL
   from a successful `deploy-pages` job and inspect the published `data.json`.
2. Under **Settings → Actions → General → Workflow permissions**, enable
   **Read and write permissions**, and **Allow GitHub Actions to create and
   approve pull requests**. Restrict human approval-file updates using
   branch protection and CODEOWNERS.
3. Run the trusted-main scheduled/manual `refresh` and verify report
   commits, canonical manifest validation, source SHA consistency and
   no-op rerun idempotence. Run the dependent proposal workflow and
   confirm it updates the existing review branch, not a duplicate PR.
4. A manually approved test identity is required before the canonical-import
   draft workflow can be tested for a real PR; do not invent such an approval.
5. Full upstream open-PR head coverage is not achieved merely by progressive
   patch-cache completion. To publish a stub, obtain external ABI evidence
   and a **successful candidate-level live audit**, including current main
   and every open PR head SHA. A changed target library or uncertain
   global registration must block.
6. Exercise upstream CMake/build/test checks with a real authorised
   contribution checkout. Source layout probes are not ABI, build or
   runtime verification.
7. Check open catalogue naming PRs before merge; their changed library shards
   do not automatically conflict with automation, but shared manifest,
   verified-name map, README, LIBRARIES.md and readiness files do.
8. Keep PR #10 **draft** while privileged workflows/Pages remain unverified;
   do not merge or publish upstream stubs merely to satisfy a coverage target.

When the GitHub REST Pages settings endpoint is unavailable to the connector,
report the setting as **unobserved**, not disabled or already configured.

## Safe release process

Treat import proposals as review material. Approve canonical names only with
applicable independent evidence and then regenerate canonical shards, indexes
and manifest together. Do not auto-merge generated upstream AnyPS5 PRs.

See [AUTOMATION.md](AUTOMATION.md), [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md)
and [DATA_POLICY.md](DATA_POLICY.md).
