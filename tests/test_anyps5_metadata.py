import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from anyps5_metadata import scan_files
from update_progress import nid_for


class AnyPS5SymbolStateTests(unittest.TestCase):
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
