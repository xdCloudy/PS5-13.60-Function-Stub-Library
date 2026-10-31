"""Precision checks for independently reviewed constant/no-op implementations."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import prepare_anyps5_constants as constants
from update_progress import nid_for


class ConstantStubTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.lib = "libSceExample"
        self.folder = self.root / "core/libs/prx" / self.lib
        self.folder.mkdir(parents=True)
        (self.folder / "CMakeLists.txt").write_text("add_library(example Export.cpp)\n")
        self.cpp = self.folder / "Export.cpp"
        self.hpp = self.folder / "Example.hpp"
        self.name = "sceExampleNoState"

    def fixture(self, rtype="int", body="\n NotImplemented_nid_no_patch(__func__);\n",
                behavior="zero"):
        signature = f"{rtype} APS5_VABI {self.name}(int mode)"
        self.cpp.write_text('#include "Example.hpp"\nextern "C" {\n'
                            + signature + " {" + body + "}\n}\n")
        self.hpp.write_text('extern "C" {\n'
                            + signature + ";\n}\n")
        self.row = {"library": self.lib, "nid": nid_for(self.name),
                    "name": self.name,
                    "path": f"core/libs/prx/{self.lib}/Export.cpp",
                    "behavior": behavior, "behavior_reviewed": True,
                    "signature_sha256": constants.sha256(signature),
                    "body_sha256": constants.sha256(body),
                    "evidence": "https://example.org/independent-behaviour-study",
                    "review_url": "https://github.com/xdCloudy/PS5-13.60-Function-Stub-Library/pull/34"}
        return self.row

    def test_reviewed_integer_return_zero(self):
        self.fixture()
        plan = constants.render(self.root, [self.row])
        self.assertIn("return 0;", plan[self.cpp])
        self.assertNotIn("NotImplemented_nid_no_patch", plan[self.cpp])

    def test_reviewed_false_pointer_and_noop(self):
        for rtype, behavior, expected in [
            ("bool", "false", "return false;"),
            ("void*", "null", "return nullptr;"),
            ("void", "noop", "{\n}"),
        ]:
            with self.subTest(rtype=rtype):
                self.fixture(rtype=rtype, behavior=behavior)
                new = constants.render(self.root, [self.row])[self.cpp]
                self.assertIn(expected, new)

    def test_type_mismatch_rejected(self):
        self.fixture(rtype="int", behavior="null")
        with self.assertRaisesRegex(ValueError, "type-compatible"):
            constants.render(self.root, [self.row])

    def test_abi_change_requires_new_review(self):
        self.fixture()
        self.cpp.write_text(self.cpp.read_text().replace("(int mode)", "(int changed)"))
        with self.assertRaisesRegex(ValueError, "signature differs"):
            constants.render(self.root, [self.row])

    def test_unreviewed_or_changed_body_cannot_be_implemented(self):
        self.fixture()
        self.cpp.write_text(self.cpp.read_text().replace(
            "NotImplemented_nid_no_patch(__func__);",
            "sideEffect(); NotImplemented_nid_no_patch(__func__);"))
        with self.assertRaisesRegex(ValueError, "body"):
            constants.render(self.root, [self.row])
        self.fixture()
        self.row["behavior_reviewed"] = False
        with self.assertRaisesRegex(ValueError, "evidence"):
            constants.render(self.root, [self.row])

    def test_missing_declaration_rejected(self):
        self.fixture()
        self.hpp.write_text("")
        with self.assertRaisesRegex(ValueError, "declaration"):
            constants.render(self.root, [self.row])

    def test_path_escape_and_wrong_nid_rejected(self):
        self.fixture()
        self.row["path"] = f"core/libs/prx/{self.lib}/../libOther/Export.cpp"
        with self.assertRaisesRegex(ValueError, "path"):
            constants.render(self.root, [self.row])
        self.fixture()
        self.row["nid"] = "AAAAAAAAAAA"
        with self.assertRaisesRegex(ValueError, "NID"):
            constants.render(self.root, [self.row])

    def test_duplicate_review_rejected(self):
        self.fixture()
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            constants.render(self.root, [self.row, self.row])

    def test_original_only_one_throw_call_permitted(self):
        self.fixture(body="\n    NotImplemented_nid_no_patch(__func__);\n return 0;\n")
        with self.assertRaisesRegex(ValueError, "standalone throwing"):
            constants.render(self.root, [self.row])

    def test_two_definitions_are_not_edited(self):
        self.fixture()
        second = self.folder / "Other.cpp"
        second.write_text(self.cpp.read_text())
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            constants.render(self.root, [self.row])


if __name__ == "__main__":
    unittest.main()
