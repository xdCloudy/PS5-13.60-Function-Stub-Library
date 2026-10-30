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

## Production automation status and remaining evidence gates

PR #10 was merged into main on 30 October 2026. The GitHub Pages deployment
and production refresh passed. The catalogue-import workflow subsequently
passed its retry after enabling Actions PR creation permissions.

The catalogue review publisher now updates one existing open draft PR, recovers
a branch left by a failed creation attempt, and suppresses re-publication of
unchanged identities from a deliberately closed review. A new identity revision
uses a separate fingerprinted branch. An unreadable closed proposal fails
closed instead of silently treating review history as disposable.

**Still unverified:** An Actions-created *brand-new* draft PR after the
permission change. The successful retry exercised the existing-PR path.
Approved canonical name import needs a real independently reviewed approval
before its privileged publication path can be exercised.

Full upstream PR coverage does not follow from the progressive symbol cache
alone. AnyPS5 patch generation still needs independent ABI evidence, a complete
current-main/open-PR overlap audit, convention checks, builds and manual review.
The reviewed-void signature generator is deliberately opt-in. Do not assert
firmware scope or implementation correctness solely from matching hashes.

When a privileged workflow fails, inspect its actual job logs and the branch
state before retrying. Never remove a closed-review history marker simply to
force another PR.

## Safe release process

Treat import proposals as review material. Approve canonical names only with
applicable independent evidence and then regenerate canonical shards, indexes
and manifest together. Do not auto-merge generated upstream AnyPS5 PRs.

See [AUTOMATION.md](AUTOMATION.md), [UPSTREAM_SYNC.md](UPSTREAM_SYNC.md)
and [DATA_POLICY.md](DATA_POLICY.md).
