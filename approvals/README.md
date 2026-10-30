# Reviewed canonical name-import approvals

The generated catalogue-import proposal is **not an approval**. Do not add a
name to canonical inventory solely because its NID rehashes.

Approval decisions live in `approvals/catalogue-name-approvals.jsonl` only
after a separate human-reviewed pull request has merged into trusted
`main`. A reviewed decision permits the workflow to generate another
**draft PR** containing canonical changes; neither workflow merges code.

Each JSONL decision must contain:

| Field | Meaning |
|---|---|
| `decision` | Exactly `approve_name` |
| `candidate_fingerprint` | SHA-256 over compact JSON array `[library.casefold(),nid,proposed_name,source]` |
| `library`, `nid`, `name` | Exact existing catalogue identity and proposed name |
| `reviewer` | Human reviewer's GitHub handle |
| `review_pr_url` | Link to the distinct PR carrying the reviewed approval |
| `independent_evidence` | Public HTTPS evidence separate from the source proposal |
| `redistribution_rights_reviewed` | Reviewer attested source licence/republication rights |
| `library_ownership_reviewed` | Reviewer attested exact library ownership |
| `firmware_scope_reviewed` | Reviewer attested source scope remains accurate |

The importer checks these fields, the current pending proposal, the strict NID
rehash, the global name-map conflicts, existing canonical identities and
publication filters. It can recover a name **only for an existing unresolved
library/NID record**. It cannot add new identities or upgrade 3.20-only evidence
into a 13.60 claim. Names already published are not added again.

Reviewers must verify the source and permissions themselves; the presence of
a HTTPS URL or a boolean in JSON is *not independent verification*. Approval
file changes must be restricted to authorised maintainers using branch
protection/CODEOWNERS rules. A malicious actor with direct write access to
trusted main could forge attestations, so repository protections are essential.

If the original source observation disappears or its identity changes, the
fingerprinted decision remains review history but cannot be applied without a
matching staged candidate. A denied/unknown record remains unmodified.

**Never commit proprietary SDK material, raw firmware, function bodies,
credentials or private research artifacts as approval evidence.**
