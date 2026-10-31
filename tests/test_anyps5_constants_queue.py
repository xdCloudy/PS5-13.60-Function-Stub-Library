"""Approved source-locked constant/no-op queue never publishes unreviewed work."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import anyps5_constants_queue as queue
from update_progress import nid_for


class ConstantQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.name = "sceExampleNoState"
        self.row = {
            "library": "libSceExample", "nid": nid_for(self.name), "name": self.name,
            "path": "core/libs/prx/libSceExample/Export.cpp",
            "behavior": "zero", "behavior_reviewed": True,
            "signature_sha256": "a" * 64, "body_sha256": "b" * 64,
            "evidence": "https://example.org/proof",
            "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/34",
        }

    def approve(self, *, changes=None, rows=None):
        raw = "".join(json.dumps(x) + "\n" for x in (rows or [self.row])).encode()
        digest = hashlib.sha256(raw).hexdigest()
        (self.root / "one.jsonl").write_bytes(raw)
        approval = {
            "schema_version": 1, "approved_for_auto_submit": True,
            "reviewed_by": "xdCloudy",
            "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/34",
            "evidence_sha256": digest,
        }
        approval.update(changes or {})
        (self.root / "one.approval.json").write_text(json.dumps(approval))
        return digest

    def test_empty_is_no_pr(self):
        self.assertEqual(queue.select(self.root, set()), [])

    def test_pinned_approval_is_selected_once(self):
        digest = self.approve()
        chosen = queue.select(self.root, set())
        self.assertEqual(chosen[0]["sha256"], digest)
        self.assertEqual(chosen[0]["count"], 1)
        self.assertEqual(queue.select(self.root, {queue.PREFIX + digest[:16]}), [])

    def test_rejects_tamper_and_fake_review(self):
        self.approve()
        (self.root / "one.jsonl").write_text("tampered")
        with self.assertRaisesRegex(ValueError, "bytes changed"):
            queue.select(self.root, set())
        self.approve(changes={"reviewed_by": "thirdparty"})
        with self.assertRaisesRegex(ValueError, "approval"):
            queue.select(self.root, set())

    def test_requires_correct_library_nid_and_semantics(self):
        self.approve(rows=[{**self.row, "nid": "AAAAAAAAAAA"}])
        with self.assertRaisesRegex(ValueError, "NID"):
            queue.select(self.root, set())
        self.approve(rows=[{**self.row, "behavior_reviewed": False}])
        with self.assertRaisesRegex(ValueError, "evidence"):
            queue.select(self.root, set())

    def test_fork_unreachable_fails_closed(self):
        with patch.object(queue.subprocess, "run",
                          side_effect=subprocess.CalledProcessError(128, ["git"])):
            with self.assertRaises(subprocess.CalledProcessError):
                queue.fork_heads()

    def test_fork_digest_ref_parsed(self):
        ref = queue.PREFIX + "f" * 16
        with patch.object(queue.subprocess, "run", return_value=SimpleNamespace(
            stdout="a" * 40 + "\t" + ref + "\n")):
            self.assertEqual(queue.fork_heads(), {ref})


if __name__ == "__main__":
    unittest.main()
