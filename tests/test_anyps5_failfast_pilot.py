"""Fail-fast proposal tests: verified identity, never a guessed implementation."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from prepare_anyps5_failfast_pilot import select, prepare, LIBRARY
from update_progress import nid_for


class Nids:
    @staticmethod
    def compute_nid(name):
        return nid_for(name)

    @staticmethod
    def source_locations(values):
        return []


def proposal(name="JSScriptEvaluate"):
    return {"schema_version":1,"library":LIBRARY,
            "require_original_320":True,"max_functions":3,
            "candidates":[{"name":name,"nid":nid_for(name)}]}


class FailFastPilotTests(unittest.TestCase):
    def repo(self, root):
        library = root / "core/libs/prx/libSceJsc"
        (library / "include").mkdir(parents=True)
        (library / "libSceJsc.hpp").write_text(
            '#include "prx/libSceJsc/include/Api.hpp"\n')
        (library / "CMakeLists.txt").write_text(
            'add_library(libSceJsc SHARED EXCLUDE_FROM_ALL Export.cpp)\n')
        (root / "docs/dev/debt").mkdir(parents=True)
        (root / "docs/dev/debt/libSceJsc.md").write_text("# libSceJsc technical debt\n")
        return library

    def valid(self, name="JSScriptEvaluate"):
        nid = nid_for(name)
        past = {("libscejsc", nid): {"library":LIBRARY, "nid":nid,
                                   "name":name, "source_file":"libSceJsc.c"}}
        new = {("libscejsc", nid): {
            "library":LIBRARY, "nid":nid, "name":name,
            "name_status":"verified_nid_binding", "kind":"defined_function_export",
            "firmware_13_60_export_confirmed":True,
            "scope":"existing_firmware_system_library",
            "stub_assessment":"throwing_stub_candidate_validation_required",
        }}
        return past, new

    def test_source_verified_placeholder_never_returns_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            folder=self.repo(root)
            past,new=self.valid()
            selected=select(proposal(),past,new,Nids(),root)
            files=prepare(root,selected,True)
            impl=(folder/"FailFastExports.cpp").read_text()
            header=(folder/"include/FailFastExports.hpp").read_text()
            self.assertIn("int APS5_VABI JSScriptEvaluate()",impl)
            self.assertIn("NotImplemented_nid_no_patch(__func__)",impl)
            self.assertNotIn("return 0;",impl)
            self.assertIn("int APS5_VABI JSScriptEvaluate();",header)
            self.assertEqual(len(files),5)
            self.assertIn("JSScriptEvaluate", (root/"docs/dev/debt/libSceJsc.md").read_text())
            self.assertIn("FailFastExports.cpp",
                (folder/"CMakeLists.txt").read_text())
            with self.assertRaisesRegex(ValueError,"already exists"):
                prepare(root,selected,True)

    def test_13_60_unconfirmed_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.repo(root)
            past,new=self.valid()
            new[("libscejsc",nid_for("JSScriptEvaluate"))][
                "firmware_13_60_export_confirmed"]=False
            with self.assertRaisesRegex(ValueError,"Unqualified"):
                select(proposal(),past,new,Nids(),root)

    def test_missing_3_20_precedent_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.repo(root)
            _,new=self.valid()
            with self.assertRaisesRegex(ValueError,"Unqualified"):
                select(proposal(),{},new,Nids(),root)

    def test_wrong_nid_and_duplicate_candidates_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.repo(root)
            past,new=self.valid()
            wrong=proposal()
            wrong["candidates"][0]["nid"]="00000000000"
            with self.assertRaisesRegex(ValueError,"mismatch"):
                select(wrong,past,new,Nids(),root)
            duplicate=proposal()
            duplicate["candidates"]*=2
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                select(duplicate,past,new,Nids(),root)

    def test_colliding_export_in_anyps5_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            self.repo(root)
            past,new=self.valid()
            class Taken(Nids):
                @staticmethod
                def source_locations(nids):
                    return [{"path":"Export.cpp","nid":list(nids)[0]}]
            with self.assertRaisesRegex(ValueError,"already has an upstream export"):
                select(proposal(),past,new,Taken(),root)


if __name__=="__main__":
    unittest.main()
