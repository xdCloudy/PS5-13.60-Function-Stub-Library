"""Unattended AnyPS5 submission must require checked-in, pinned review approval."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import anyps5_auto_queue as queue
from update_progress import nid_for


class ApprovedQueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name)
        self.name = "sceExampleReviewed"
        self.lib = "libSceExample"
        self.nid = nid_for(self.name)
        self.row = {"library": self.lib, "name": self.name, "nid": self.nid,
                    "return_type": "void", "parameters": "void", "abi_reviewed": True,
                    "evidence": "https://example.org/independent-abi-review"}
        self.known = {(self.lib.casefold(), self.nid): {
            "name": self.name, "scope": "existing_firmware_system_library",
            "stub_assessment": "throwing_stub_candidate_validation_required",
            "firmware_13_60_export_confirmed": True}}
        self.verified = {(self.lib.casefold(), self.nid)}

    def approve(self, *, stem="example", data=None, changes=None):
        payload = "".join(json.dumps(r) + "\n" for r in (data or [self.row]))
        raw = payload.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        (self.folder / (stem + ".jsonl")).write_bytes(raw)
        approval = {
            "schema_version": 1,
            "approved_for_auto_submit": True,
            "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/33",
            "reviewed_by": "xdCloudy",
            "evidence_sha256": digest,
        }
        approval.update(changes or {})
        (self.folder / (stem + ".approval.json")).write_text(json.dumps(approval))
        return digest

    def select(self, published=None):
        return queue.approved_batches(self.folder, self.known, self.verified,
                                      published or set())

    def test_empty_queue_publishes_nothing(self):
        self.assertEqual(self.select(), [])

    def test_approved_batch_is_selected_with_pinned_digest(self):
        digest = self.approve()
        selected = self.select()
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["sha256"], digest)
        self.assertEqual(selected[0]["count"], 1)
        self.assertEqual(selected[0]["branch"], queue.PREFIX + digest[:16])

    def test_already_published_branch_not_redispatched(self):
        digest = self.approve()
        self.assertEqual(self.select({queue.PREFIX + digest[:16]}), [])

    def test_tampered_evidence_is_rejected(self):
        self.approve()
        (self.folder / "example.jsonl").write_text("modified\n")
        with self.assertRaisesRegex(ValueError, "digest changed"):
            self.select()

    def test_missing_explicit_approval_or_bad_review_is_rejected(self):
        self.approve(changes={"approved_for_auto_submit": False})
        with self.assertRaisesRegex(ValueError, "attestation"):
            self.select()
        self.approve(changes={"review_url": "https://evil.example/pull/22"})
        with self.assertRaisesRegex(ValueError, "attestation"):
            self.select()

    def test_repeated_symbol_or_mixed_library_rejected(self):
        self.approve(data=[self.row, self.row])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.select()
        other = {**self.row, "library": "libAnother"}
        self.approve(data=[self.row, other])
        with self.assertRaisesRegex(ValueError, "mixes libraries"):
            self.select()

    def test_nonqualifying_rows_are_skipped_in_favour_of_other_approvals(self):
        self.approve(stem="aaa")
        first = self.nid
        self.known.pop((self.lib.casefold(), first))
        self.assertEqual(self.select(), [])
        self.known[(self.lib.casefold(), first)] = {
            "name": self.name, "scope": "existing_firmware_system_library",
            "stub_assessment": "throwing_stub_candidate_validation_required",
            "firmware_13_60_export_confirmed": True}
        self.assertEqual(len(self.select()), 1)

    def test_fork_read_failure_aborts_not_assumes_empty(self):
        with patch.object(queue.subprocess, "run",
                          side_effect=subprocess.CalledProcessError(128, ["git"])):
            with self.assertRaises(subprocess.CalledProcessError):
                queue.published_branches()

    def test_fork_branch_parsing(self):
        response = SimpleNamespace(
            stdout=("a" * 40 + "\t" + queue.PREFIX + "f" * 16 + "\n"))
        with patch.object(queue.subprocess, "run", return_value=response):
            self.assertEqual(queue.published_branches(),
                             {queue.PREFIX + "f" * 16})


if __name__ == "__main__":
    unittest.main()
