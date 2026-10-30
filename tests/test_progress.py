import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from update_progress import nid_for


class ReportTests(unittest.TestCase):
    def test_nid_algorithm_matches_known_public_binding(self):
        self.assertEqual(nid_for("sceNpLwCondInit"), "++eqYdzB8Go")

    def test_duplicate_alias_and_withheld_do_not_inflate_stubs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "catalog"
            shard = root / "data" / "firmware-13.60"
            shard.mkdir(parents=True)
            symbol = "samplePublicFunction"
            nid = nid_for(symbol)
            records = [
                {"library": lib, "nid": nid, "name": symbol,
                 "name_status": "verified_nid_binding",
                 "scope": "existing_firmware_system_library",
                 "stub_assessment": "throwing_stub_candidate_validation_required"}
                for lib in ("libSample", "libAlias")
            ]
            records.append({"library": "libWithheld", "nid": nid_for("secretName"),
                            "name": None, "name_status": "withheld_by_publication_filter",
                            "scope": "ownership_pending",
                            "stub_assessment": "throwing_stub_candidate_validation_required"})
            (shard / "sample.jsonl").write_text(
                "".join(json.dumps(row) + "\n" for row in records), encoding="utf-8")
            (root / "manifest.json").write_text(json.dumps({
                "counts": {"total_records": 3, "resolved_names": 2,
                           "firmware-13.60": 3, "historical-3.20-only": 0}}))
            (root / "readiness.json").write_text(json.dumps({
                "metrics": {"qualified_unique_stub_candidates": 2,
                            "generated_throwing_stubs": 0,
                            "statically_prepared_stubs": 0,
                            "fully_validated_stubs": 0,
                            "published_anyps5_stubs": 0}}))
            upstream = Path(temporary) / "AnyPS5"
            cpp = upstream / "core/libs/prx/libSample/Export.cpp"
            cpp.parent.mkdir(parents=True)
            cpp.write_text("int APS5_VABI samplePublicFunction(void) {\n"
                           " NotImplemented_nid_no_patch(__func__);\n return 0;\n}\n"
                           "int APS5_VABI novelSymbol(void) { return 1; }\n")
            subprocess.run([sys.executable, str(ROOT / "tools" / "update_progress.py"),
                            "--root", str(root), "--upstream-dir", str(upstream),
                            "--skip-prs"], check=True, capture_output=True, text=True)
            report = json.loads((root / "reports/progress.json").read_text())
            self.assertEqual(report["inventory"]["records"], 3)
            self.assertEqual(report["inventory"]["cross_library_nid_extra_records_all_scopes"], 1)
            self.assertEqual(report["stubs"]["qualified_unique_nids_recomputed"], 1)
            self.assertEqual(report["stubs"]["qualified_but_unverified_records_excluded"], 1)
            self.assertEqual(report["stubs"]["qualified_unique_nids_matched_in_main_source"], 1)
            self.assertEqual(report["stubs"]["new_upstream_nid_candidates_for_review"], 1)
            queue = (root / "reports/upstream-review-queue.jsonl").read_text()
            self.assertNotIn("novelSymbol", queue)
            self.assertNotIn("secretName", queue)
            self.assertIn("Saved qualified-count discrepancy", (root / "READINESS.md").read_text())


if __name__ == "__main__":
    unittest.main()
