"""Fail-closed tests for review proposals and AnyPS5 stub eligibility."""
import hashlib
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from stage_catalogue_import import collect, safe, write
from prepare_anyps5 import choose, read_reviews, apply
from update_progress import nid_for


SHA_A="a"*40
SHA_B="b"*40


def sample(name="sceExample", library="libSceExample"):
    return {"library":library, "nid":nid_for(name), "name":name}


class CatalogueProposalTests(unittest.TestCase):
    def test_reject_mismatched_nid_unsafe_source_and_unapproved_status(self):
        item={"library":"libSceExample","nid":nid_for("sceExample"),
              "proposed_name":"sceExample","source": "boykopovar/AnyPS5",
              "source_file":"core/libs/prx/libSceExample/Export.cpp",
              "source_commit":SHA_B,"canonical_name_approved":False,
              "match_status":"unnamed_catalog_identity"}
        self.assertIsNotNone(safe(item,kind="AnyPS5",source_sha=SHA_B))
        for altered in (dict(item,nid="12345678901"),
                        dict(item,source_file="../secret.cpp"),
                        dict(item,source_commit=SHA_A),
                        dict(item,canonical_name_approved=True),
                        dict(item,match_status="not_in_firmware_catalog")):
            self.assertIsNone(safe(altered,kind="AnyPS5",source_sha=SHA_B))

    def test_duplicate_source_evidence_is_not_two_new_identites(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"reports").mkdir()
            (root/"manifest.json").write_text('{"counts":{"total_records":0}}')
            digest=hashlib.sha256((root/"manifest.json").read_bytes()).hexdigest()
            (root/"reports/source-320.json").write_text(json.dumps(
                {"inputs":{"source_commit":SHA_A,"catalogue_manifest_sha256":digest}}))
            (root/"reports/progress.json").write_text(json.dumps(
                {"generated_from":{"anyps5_main_commit":SHA_B}}))
            item={"library":"libSceExample","nid":nid_for("sceExample"),
                  "proposed_name":"sceExample","status":"name_recovery_candidate",
                  "source": "DNNDHH/PS5-3.20_Libs","source_file":"libSceExample.c",
                  "source_commit":SHA_A,"canonical_name_approved":False}
            queue=root/"reports/source-320-review.jsonl"
            queue.write_text(json.dumps(item)+"\n"+json.dumps(item)+"\n")
            (root/"reports/upstream-source-candidates.jsonl").write_text("")
            document=collect(root)
            self.assertEqual(document["reviewable_identity_count"],1)
            self.assertEqual(document["evidence_observations"],1)
            self.assertFalse(document["candidates"][0]["canonical_name_approved"])
            self.assertEqual(document["canonical_records_mutated"],0)
            out=root/"candidate.json"
            first=write(root,out)
            contents=out.read_bytes()
            second=write(root,out)
            self.assertEqual(contents,out.read_bytes())
            self.assertEqual(first,second)
            queue.write_text("")
            none=write(root,out)
            self.assertEqual(none["reviewable_identity_count"],0)
            self.assertFalse(out.exists())

    def test_manifest_drift_blocks_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/"reports").mkdir()
            (root/"manifest.json").write_text("{}")
            (root/"reports/source-320.json").write_text(json.dumps({"inputs":{
                "source_commit":SHA_A,"catalogue_manifest_sha256":"not-current"}}))
            (root/"reports/progress.json").write_text(json.dumps({
                "generated_from":{"anyps5_main_commit":SHA_B}}))
            with self.assertRaisesRegex(ValueError,"Stale importer"):
                collect(root)


class StubPreparationTests(unittest.TestCase):
    def test_no_abi_file_no_stub_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                read_reviews(Path(tmp)/"missing.jsonl")

    def test_only_strict_verified_system_library_and_no_global_duplicate(self):
        x=sample()
        review={**x,"return_type":"void","parameters":"void",
                "abi_reviewed":True,"evidence":"https://example.org/prototype"}
        key=(x["library"].casefold(),x["nid"])
        row={"name":x["name"],"scope":"existing_firmware_system_library",
             "firmware_13_60_export_confirmed":True,
             "stub_assessment":"throwing_stub_candidate_validation_required"}
        accepted,rejected=choose([review],{key:row},{key},set(),set(),150)
        self.assertEqual(len(accepted),1)
        self.assertEqual(rejected,[])
        accepted,rejected=choose([review],{key:row},{key},set(),{("otherlibrary",x["nid"])},150)
        self.assertFalse(accepted)
        self.assertEqual(rejected[0]["reason"],"already_covered_or_reserved")
        row["scope"]="managed_or_application_native_image"
        accepted,rejected=choose([review],{key:row},{key},set(),set(),150)
        self.assertFalse(accepted)
        self.assertEqual(rejected[0]["reason"],"unsafe_ownership_scope")

    def test_external_checkout_patch_has_exactly_one_throwing_declaration(self):
        with tempfile.TemporaryDirectory() as temp:
            checkout=Path(temp)/"AnyPS5"
            lib=checkout/"core/libs/prx/libSceExample"
            (lib/"include").mkdir(parents=True)
            (lib/"CMakeLists.txt").write_text("add_sce_library(libSceExample)")
            export=lib/"Export.cpp"
            header=lib/"include/Api.hpp"
            export.write_text('#include "prx/libSceExample/include/Api.hpp"\n'
                              'extern "C" {\nvoid APS5_VABI existing() {}\nAPS5_DUMMY_FUN\n}\n')
            header.write_text('#pragma once\nextern "C" {\nvoid APS5_VABI existing();\n}\n')
            subprocess.run(["git","init","-q",str(checkout)],check=True)
            subprocess.run(["git","-C",str(checkout),"add","."],check=True)
            subprocess.run(["git","-C",str(checkout),"-c","user.name=Test",
                            "-c","user.email=test@example.invalid","commit","-qm","fixture"],check=True)
            patch=apply(checkout,[{"library":"libSceExample",
                                   "name":"sceExample", "parameters":"void"}],
                        Path(temp)/"patches")
            body=export.read_text()
            self.assertEqual(body.count("sceExample(void)"),1)
            self.assertEqual(header.read_text().count("sceExample(void)"),1)
            self.assertEqual(body.count("NotImplemented_nid_no_patch(__func__)"),1)
            self.assertNotIn("return 0;",body)
            self.assertIn("APS5_DUMMY_FUN",body)
            self.assertIn("sceExample(void)",patch.read_text())

    def test_stub_batch_limit(self):
        with self.assertRaisesRegex(ValueError,"1 to 150"):
            choose([],{},set(),set(),set(),151)


if __name__=="__main__":
    unittest.main()
