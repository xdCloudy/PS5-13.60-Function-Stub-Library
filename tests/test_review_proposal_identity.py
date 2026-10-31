"""Deterministic proposal identity and closed-PR suppression regression tests."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from review_proposal_identity import identity_set, fingerprint


class ReviewIdentityTests(unittest.TestCase):
    def example(self):
        return {
            "publication_status": "DRAFT_REVIEW_ONLY",
            "canonical_records_mutated": 0,
            "independent_approval_required": True,
            "reviewable_identity_count": 2,
            "candidates": [
                {"library": "libSceAlpha", "nid": "ABCDEFGHIJK",
                 "proposed_name": "sceAlpha", "source": "boykopovar/AnyPS5",
                 "observed_status": "unnamed_catalog_identity",
                 "canonical_name_approved": False},
                {"library": "libSceBeta", "nid": "LMNOPQRSTUV",
                 "proposed_name": "sceBeta", "source": "DNNDHH/PS5-3.20_Libs",
                 "observed_status": "name_recovery_candidate",
                 "canonical_name_approved": False},
            ],
        }

    def test_source_revision_only_does_not_reopen_closed_identity(self):
        before = self.example()
        after = copy.deepcopy(before)
        after["canonical_manifest_sha256"] = "f" * 64
        after["source_revision_anyps5"] = "a" * 40
        after["candidates"][0]["source_commit"] = "b" * 40
        after["candidates"].reverse()
        self.assertEqual(identity_set(before), identity_set(after))
        self.assertEqual(fingerprint(before), fingerprint(after))

    def test_substantive_new_candidate_has_new_review_identity(self):
        before = self.example()
        after = copy.deepcopy(before)
        after["candidates"][0]["proposed_name"] = "sceAlphaWithEvidence"
        self.assertNotEqual(fingerprint(before), fingerprint(after))

    def test_library_name_casefold_is_only_normalisation(self):
        before = self.example()
        after = copy.deepcopy(before)
        after["candidates"][0]["library"] = "LIBSCEALPHA"
        self.assertEqual(fingerprint(before), fingerprint(after))
        after["candidates"][0]["nid"] = "abcdefghijk"
        self.assertNotEqual(fingerprint(before), fingerprint(after))

    def test_rejects_bad_counts_conflicts_and_approved_candidates(self):
        document = self.example()
        document["reviewable_identity_count"] = 1
        with self.assertRaisesRegex(ValueError, "count"):
            fingerprint(document)
        document = self.example()
        document["candidates"].append(dict(document["candidates"][0],
                                            proposed_name="sceOther"))
        with self.assertRaisesRegex(ValueError, "Conflicting"):
            fingerprint(document)
        document = self.example()
        document["candidates"][0]["canonical_name_approved"] = True
        with self.assertRaisesRegex(ValueError, "Already-approved"):
            fingerprint(document)

    def test_rejects_empty_or_non_review_proposals(self):
        document = self.example()
        document["candidates"] = []
        with self.assertRaisesRegex(ValueError, "at least one"):
            fingerprint(document)
        document = self.example()
        document["publication_status"] = "APPROVED"
        with self.assertRaisesRegex(ValueError, "metadata-only"):
            fingerprint(document)


if __name__ == "__main__":
    unittest.main()
