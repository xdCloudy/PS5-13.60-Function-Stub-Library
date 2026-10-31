"""Regression tests for read-only live source evidence investigation."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from investigate_anyps5_source_evidence import read_queue, scan, reconcile
from update_progress import nid_for


def row(name="sceTest", library="libSceExample", **overrides):
    return {
        "library": library, "name": name, "nid": nid_for(name),
        "evidence_class": "confirmed_13.60_only",
        "firmware_13_60_export_confirmed": True,
        "signature_verified": False,
        "behaviour_verified": False,
        "approved_for_auto_submit": False,
        "review_status": "needs_independent_abi_and_live_overlap_evidence",
        **overrides,
    }


class EvidenceInvestigatorTests(unittest.TestCase):
    def test_direct_header_observation_is_not_abi_approval(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / "core/libs/prx/libSceExample"
            folder.mkdir(parents=True)
            (folder / "libSceExample.hpp").write_text(
                "int APS5_VABI sceTest(int arg);\n")
            records = [row()]
            observed = scan(root, {"libsceexample"})
            output, counts = reconcile(records, observed)
            self.assertEqual(counts["upstream_source_symbol_observed"], 1)
            self.assertEqual(output[0]["signature_verified"], False)
            self.assertEqual(output[0]["approved_for_auto_submit"], False)
            self.assertEqual(output[0]["safe_to_submit_without_further_evidence"], False)
            self.assertEqual(
                output[0]["upstream_source_observations"][0]["path"],
                "core/libs/prx/libSceExample/libSceExample.hpp")

    def test_literal_nid_alias_observed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            folder=root/"core/libs/prx/libSceExample"
            folder.mkdir(parents=True)
            record=row()
            (folder/"Export.cpp").write_text(
                f'APS5_EXPORT("{record["nid"]}", old_name);')
            state, counts = reconcile([record], scan(root, {"libsceexample"}))
            self.assertEqual(counts["upstream_source_symbol_observed"],1)
            self.assertEqual(state[0]["signature_verified"],False)

    def test_unknown_source_absence_not_proof(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"core/libs/prx/libOther").mkdir(parents=True)
            result,counts=reconcile([row()],scan(root,{"libsceexample"}))
            self.assertEqual(counts["no_direct_upstream_source_observation"],1)
            self.assertFalse(result[0]["safe_to_submit_without_further_evidence"])

    def test_unauthorised_approval_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"candidates.jsonl"
            for change in ({"approved_for_auto_submit":True},
                           {"signature_verified":True},
                           {"behaviour_verified":True},
                           {"candidate_only":True}):
                p.write_text(json.dumps(row(**change))+"\n")
                with self.assertRaises(ValueError):
                    read_queue(p)

    def test_duplicate_and_unsafe_name_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"queue.jsonl"
            p.write_text(json.dumps(row())+"\n"+json.dumps(row())+"\n")
            with self.assertRaisesRegex(ValueError, "Duplicated"):
                read_queue(p)
            p.write_text(json.dumps(row(library="../evil"))+"\n")
            with self.assertRaisesRegex(ValueError,"Unsafe"):
                read_queue(p)


if __name__=="__main__":
    unittest.main()
