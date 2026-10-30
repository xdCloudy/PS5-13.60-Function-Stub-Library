"""Integration checks for explicitly approved canonical name recovery."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))
from apply_approved_imports import apply, allowed, fingerprint
from update_progress import nid_for


class ApprovedImportTests(unittest.TestCase):
    def setup_fixture(self, root):
        (root/"reports").mkdir()
        (root/"data/firmware-13.60").mkdir(parents=True)
        (root/"data").mkdir(exist_ok=True)
        (root/"libraries").mkdir()
        (root/"approvals").mkdir()
        library="libSceExample"
        name="sceExampleVerified"
        nid=nid_for(name)
        sha1="a"*40
        sha2="b"*40
        shard="data/firmware-13.60/libsceexample-test.jsonl"
        canonical={"library":library,"nid":nid,"name":None,"name_status":"unresolved",
                   "scope":"existing_firmware_system_library",
                   "firmware_13_60_export_confirmed":True,
                   "firmware_versions":["13.60"],"source_evidence":["firmware_export_table"]}
        (root/shard).write_text(json.dumps(canonical,sort_keys=True,separators=(",",":"))+"\n")
        (root/"data/library-index.csv").write_text(
            "library,scope,records,resolved_names,file\n"+
            f"{library},firmware-13.60,1,0,{shard}\n")
        (root/"data/verified-name-map.jsonl").write_text("")
        (root/"libraries/libsceexample-test.md").write_text(
            f"# {library}\n\n| Export identities | 1 |\n| Named | 0 |\n"
            "| Unresolved or withheld | 1 |\n\n## Named export preview\n\n"
            "A bounded preview; the inventory file contains the complete library.\n\n"
            "| NID | Symbol |\n|---|---|\n")
        (root/"LIBRARIES.md").write_text(
            "| Library | Export records | Named | Qualified candidates |\n|---|---:|---:|---:|\n"
            f"| [{library}](libraries/libsceexample-test.md) | 1 | 0 | 0 |\n")
        readiness={"total_export_records":1,"named_library_stub_records":0,
                   "named_stub_identities":0,"unresolved_or_withheld_records":1,
                   "libraries":[{"library":library,"named":0,"total":1,"qualified":0,"generated":0}]}
        (root/"readiness.json").write_text(json.dumps(readiness))
        manifest={"counts":{"total_records":1,"resolved_names":0,
                            "unresolved_or_withheld_names":1,
                            "firmware-13.60":1,"historical-3.20-only":0},
                  "files":[{"path":shard,"records":1,"bytes":0,"sha256":"0"*64}],
                  "unique_verified_name_bindings":0,
                  "readiness_file":{"path":"readiness.json","sha256":"0"*64}}
        (root/"manifest.json").write_text(json.dumps(manifest))
        manifest_sha=hashlib.sha256((root/"manifest.json").read_bytes()).hexdigest()
        (root/"reports/source-320.json").write_text(json.dumps({
            "inputs":{"source_commit":sha1,"catalogue_manifest_sha256":manifest_sha}}))
        (root/"reports/progress.json").write_text(json.dumps({
            "generated_from":{"anyps5_main_commit":sha2}}))
        proposal={"library":library,"nid":nid,"proposed_name":name,
                  "status":"name_recovery_candidate",
                  "canonical_name_approved":False,"source":"DNNDHH/PS5-3.20_Libs",
                  "source_file":"libSceExample.c","source_commit":sha1}
        (root/"reports/source-320-review.jsonl").write_text(json.dumps(proposal)+"\n")
        (root/"reports/upstream-source-candidates.jsonl").write_text("")
        fingerprint_record={"library":library,"nid":nid,"proposed_name":name,
                            "source":"DNNDHH/PS5-3.20_Libs"}
        approved={"decision":"approve_name","candidate_fingerprint":fingerprint(fingerprint_record),
                  "library":library,"nid":nid,"name":name,
                  "redistribution_rights_reviewed":True,
                  "library_ownership_reviewed":True,
                  "firmware_scope_reviewed":True,
                  "reviewer":"research-maintainer",
                  "review_pr_url":"https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/123",
                  "independent_evidence":"https://example.org/independently-observed-library-export"}
        file=root/"approvals/catalogue-name-approvals.jsonl"
        file.write_text(json.dumps(approved)+"\n")
        return file,shard,nid,name

    def test_approved_recovery_preserves_identity_and_regenerates_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            decision,shard,nid,name=self.setup_fixture(root)
            result=apply(root,decision)
            self.assertEqual(result["canonical_names_added"],1)
            row=json.loads((root/shard).read_text().splitlines()[0])
            self.assertEqual((row["nid"],row["name"]),(nid,name))
            self.assertTrue(row["firmware_13_60_export_confirmed"])
            self.assertEqual(row["scope"],"existing_firmware_system_library")
            self.assertEqual(json.loads((root/"manifest.json").read_text())
                             ["counts"]["resolved_names"],1)
            self.assertEqual(json.loads((root/"readiness.json").read_text())
                             ["named_library_stub_records"],1)
            self.assertIn(name,(root/"libraries/libsceexample-test.md").read_text())
            self.assertIn("| 1 | 1 |",(root/"LIBRARIES.md").read_text())
            self.assertEqual(len((root/"data/verified-name-map.jsonl").read_text().splitlines()),1)

    def test_unapproved_decision_cannot_touch_canonical_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            decision,shard,_,_=self.setup_fixture(root)
            row=json.loads(decision.read_text())
            row["redistribution_rights_reviewed"]=False
            decision.write_text(json.dumps(row)+"\n")
            before=(root/shard).read_bytes()
            result=apply(root,decision)
            self.assertEqual(result["canonical_names_added"],0)
            self.assertEqual(before,(root/shard).read_bytes())
            self.assertEqual(result["rejected"][0]["reason"],
                             "missing_staged_or_independent_approval")

    def test_mismatched_name_hash_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            decision,shard,_,_=self.setup_fixture(root)
            row=json.loads(decision.read_text())
            row["name"]="sceIncorrectName"
            decision.write_text(json.dumps(row)+"\n")
            result=apply(root,decision)
            self.assertEqual(result["canonical_names_added"],0)
            self.assertFalse(json.loads((root/shard).read_text().splitlines()[0])["name"])


if __name__=="__main__":
    unittest.main()
