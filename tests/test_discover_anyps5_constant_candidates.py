"""Source-only candidate discovery never creates behavioural attestations."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import discover_anyps5_constant_candidates as discovery
from update_progress import nid_for

REVISION = "a" * 40


class CandidateDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.folder = self.root / "core/libs/prx/libSceExample"
        self.folder.mkdir(parents=True)
        self.cpp = self.folder / "Export.cpp"
        self.hpp = self.folder / "Example.hpp"
        (self.folder / "CMakeLists.txt").write_text("add_library(example Export.cpp)\n")
        self.name = "sceExampleReviewed"

    def fixture(self, rtype="int", body="\n NotImplemented_nid_no_patch(__func__);\n"):
        sig = f"{rtype} APS5_VABI {self.name}(int count)"
        self.cpp.write_text('extern "C" {\n' + sig + " {" + body + "}\n}\n")
        self.hpp.write_text('extern "C" {\n' + sig + ";\n}\n")

    def discover(self):
        return discovery.discover(self.root, REVISION)

    def test_exact_single_throw_source_yields_unapproved_hashes(self):
        self.fixture()
        rows = self.discover()
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["nid"], nid_for(self.name))
        self.assertEqual(row["return_type_class"], "integer")
        self.assertEqual(row["path"], "core/libs/prx/libSceExample/Export.cpp")
        self.assertEqual(row["declaration_path"], "core/libs/prx/libSceExample/Example.hpp")
        self.assertEqual(row["signature_sha256"], discovery.sha256(
            f"int APS5_VABI {self.name}(int count)"))
        self.assertIsNone(row["behavior"])
        self.assertIsNone(row["evidence"])
        self.assertFalse(row["behavior_reviewed"])
        self.assertEqual(row["observed_anyps5_main_sha"], REVISION)

    def test_noop_false_pointer_and_integer_type_enumeration(self):
        for rtype, kind in (("void", "void"), ("bool", "bool"),
                            ("void*", "pointer"), ("int", "integer")):
            with self.subTest(rtype=rtype):
                self.fixture(rtype)
                rows = self.discover()
                self.assertEqual([r["return_type_class"] for r in rows], [kind])
                self.assertIsNone(rows[0]["behavior"])

    def test_nonthrowing_body_not_candidate(self):
        self.fixture(body="\n return 0;\n")
        self.assertEqual(self.discover(), [])

    def test_source_not_in_cmake_not_candidate(self):
        self.fixture()
        (self.folder / "CMakeLists.txt").write_text("add_library(example Elsewhere.cpp)\n")
        self.assertEqual(self.discover(), [])

    def test_header_prototype_mismatch_rejected(self):
        self.fixture()
        self.hpp.write_text(self.hpp.read_text().replace("int APS5", "void APS5"))
        self.assertEqual(self.discover(), [])

    def test_duplicate_definition_or_declaration_rejected(self):
        self.fixture()
        (self.folder / "Other.cpp").write_text(self.cpp.read_text())
        self.assertEqual(self.discover(), [])
        (self.folder / "Other.cpp").unlink()
        (self.folder / "Other.hpp").write_text(self.hpp.read_text())
        self.assertEqual(self.discover(), [])

    def test_unknown_type_does_not_infer_behaviour(self):
        self.fixture("SceCustomResult")
        self.assertEqual(self.discover(), [])

    def test_signature_hash_matches_implementation_patch_parser(self):
        self.fixture("unsigned int")
        rows = self.discover()
        from prepare_anyps5_constants import FUNCTION
        original = FUNCTION.search(self.cpp.read_text())
        self.assertIsNotNone(original)
        self.assertEqual(rows[0]["signature_sha256"],
                         discovery.sha256(original.group("signature")))
        self.assertEqual(rows[0]["body_sha256"],
                         discovery.sha256(original.group("body")))

    def test_large_whitespace_only_does_not_match(self):
        self.fixture()
        self.cpp.write_text(
            self.cpp.read_text() + "\\n" +
            "int " + " " * 30000 + " APS5_VABI " + " " * 30000 +
            "invalid_no_signature;\\n")
        rows = self.discover()
        self.assertEqual(len(rows), 1)

    def test_nonthrowing_duplicate_is_still_detected(self):
        self.fixture()
        second = self.folder / "Other.cpp"
        second.write_text(
            f'int APS5_VABI {self.name}(int count) {{\\n'
            '  return 0;\\n}\\n')
        self.assertEqual(self.discover(), [])

    def test_missing_real_upstream_checkout_or_revision_fails(self):
        with self.assertRaises(ValueError):
            discovery.discover(self.root / "missing", REVISION)
        self.fixture()
        with self.assertRaises(ValueError):
            discovery.discover(self.root, "not-a-git-sha")


if __name__ == "__main__":
    unittest.main()
