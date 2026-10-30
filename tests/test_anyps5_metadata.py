import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from anyps5_metadata import scan_files
from update_progress import nid_for


class AnyPS5SymbolStateTests(unittest.TestCase):
    def test_explicit_nid_alias_is_registration_evidence_not_abi(self):
        with tempfile.TemporaryDirectory() as tmp:
            lib=Path(tmp)/"core/libs/prx/libSceExample"
            lib.mkdir(parents=True)
            nid="H2e8t5ScQGc"
            (lib/"Export.cpp").write_text(
                '// APS5_EXPORT("12345678901", fakeComment);\n'
                'APS5_EXPORT("H2e8t5ScQGc", sceExampleUnknown_nid_no_patch);\n')
            rows=scan_files(Path(tmp))
            entry=rows[("libsceexample",nid)]
            self.assertTrue(entry["explicit_alias_seen"])
            self.assertTrue(entry["export_registered"])
            self.assertFalse(entry["definition_seen"])
            self.assertIsNone(entry["abi_verified"])
            self.assertNotIn(("libsceexample","12345678901"),rows)

    def test_declarations_definitions_and_build_presence_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            lib=Path(tmp)/"core/libs/prx/libSceExample"
            (lib/"include").mkdir(parents=True)
            (lib/"CMakeLists.txt").write_text("add_sce_library(libSceExample)")
            (lib/"include/Api.hpp").write_text(
                'extern "C" { void APS5_VABI sceExampleDeclared(); '
                'void APS5_VABI sceExampleThrow(); }\n')
            (lib/"Export.cpp").write_text(
                'void APS5_VABI sceExampleThrow() {\n'
                '  NotImplemented_nid_no_patch(__func__);\n}\n'
                'void APS5_VABI sceExampleBody() { return; }\n')
            results=scan_files(Path(tmp))
            declared=results[("libsceexample",nid_for("sceExampleDeclared"))]
            throwing=results[("libsceexample",nid_for("sceExampleThrow"))]
            body=results[("libsceexample",nid_for("sceExampleBody"))]
            self.assertTrue(declared["declared"])
            self.assertFalse(declared["definition_seen"])
            self.assertTrue(throwing["throwing_marker"])
            self.assertFalse(throwing["nonthrowing_body_seen"])
            self.assertTrue(body["nonthrowing_body_seen"])
            self.assertIsNone(body["runtime_validated"])
            self.assertIsNone(body["export_registered"])
            self.assertTrue(body["build_config_present"])


if __name__=="__main__":
    unittest.main()
