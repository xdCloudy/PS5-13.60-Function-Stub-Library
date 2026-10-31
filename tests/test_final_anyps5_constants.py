"""Final constant implementation publisher must not trust candidate artifacts."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import final_anyps5_constants as gate
from update_progress import nid_for


class FinalConstantGateTests(unittest.TestCase):
    def setUp(self):
        self.name = "sceReviewedConstant"
        self.row = {
            "library": "libSceExample", "name": self.name,
            "nid": nid_for(self.name), "path": "core/libs/prx/libSceExample/Export.cpp",
            "behavior": "zero", "behavior_reviewed": True,
            "evidence": "https://example.org/independent-semantics",
            "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/34",
            "signature_sha256": "a" * 64, "body_sha256": "b" * 64,
        }
        self.data = {"base_sha": "c" * 40, "patch_commit": "d" * 40,
                     "candidates": [self.row]}

    def fake_git(self, path, *argv):
        return {
            ("rev-parse", "HEAD"): "d" * 40,
            ("rev-parse", "origin/main"): "c" * 40,
            ("rev-parse", "HEAD^"): "c" * 40,
            ("status", "--porcelain"): "",
        }[argv]

    def test_single_clean_commit_and_verified_candidates(self):
        with patch.object(gate, "git", self.fake_git):
            self.assertEqual(gate.verify_metadata(Path("/fake"), self.data),
                             [self.row])

    def test_diff_sha_dirty_state_or_unreviewed_constant_rejected(self):
        with patch.object(gate, "git", self.fake_git):
            for change in (
                {**self.data, "patch_commit": "e" * 40},
                {**self.data, "base_sha": "e" * 40},
                {**self.data, "candidates": [{**self.row, "behavior_reviewed": False}]},
                {**self.data, "candidates": [{**self.row, "nid": "AAAAAAAAAAA"}]},
            ):
                with self.subTest(change=change), self.assertRaises(ValueError):
                    gate.verify_metadata(Path("/fake"), change)

    def test_multiple_identity_or_nonexisting_input_rejected(self):
        with patch.object(gate, "git", self.fake_git):
            for rows in ([], [self.row, self.row]):
                with self.assertRaises(ValueError):
                    gate.verify_metadata(Path("/fake"), {**self.data, "candidates": rows})


if __name__ == "__main__":
    unittest.main()
