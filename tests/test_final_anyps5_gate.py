"""Final publication gate tests; no network or checkout required."""
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import final_anyps5_gate as gate
from update_progress import nid_for


class FinalGateTests(unittest.TestCase):
    def setUp(self):
        self.name = "sceExampleReviewed"
        self.row = {"library": "libSceExample", "nid": nid_for(self.name),
                    "name": self.name, "return_type": "void", "parameters": "void",
                    "abi_reviewed": True, "evidence": "https://example.org/proof"}
        self.data = {"base_sha": "a" * 40, "patch_commit": "b" * 40,
                     "candidates": [self.row]}

    def fake_git(self, checkout, *args):
        return {("rev-parse", "HEAD"): "b" * 40,
                ("rev-parse", "origin/main"): "a" * 40,
                ("rev-parse", "HEAD^"): "a" * 40,
                ("status", "--porcelain"): ""}[args]

    def test_correct_clean_single_commit_and_abi_is_allowed(self):
        with patch.object(gate, "git", self.fake_git):
            self.assertEqual(gate.verify_batch(self.data, Path("/fake")),
                             [self.row])

    def test_wrong_patch_commit_is_blocked(self):
        with patch.object(gate, "git", self.fake_git):
            doc = {**self.data, "patch_commit": "c" * 40}
            with self.assertRaisesRegex(ValueError, "submitted commit"):
                gate.verify_batch(doc, Path("/fake"))

    def test_unreviewed_or_wrong_abi_is_blocked(self):
        with patch.object(gate, "git", self.fake_git):
            for key, value in (("abi_reviewed", False),
                               ("return_type", "int"),
                               ("nid", "01234567890")):
                doc = {**self.data, "candidates": [{**self.row, key: value}]}
                with self.subTest(key=key), self.assertRaises(ValueError):
                    gate.verify_batch(doc, Path("/fake"))

    def test_duplicate_and_oversized_batches_blocked(self):
        with patch.object(gate, "git", self.fake_git):
            for candidates in ([self.row, self.row], [self.row] * 101, []):
                with self.subTest(count=len(candidates)), self.assertRaises(ValueError):
                    gate.verify_batch({**self.data, "candidates": candidates},
                                      Path("/fake"))


if __name__ == "__main__":
    unittest.main()
