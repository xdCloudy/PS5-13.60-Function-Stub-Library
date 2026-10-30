"""Live candidate clearance and layout-safe patching regression tests."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from candidate_overlap import check_candidates
from layout_patch import plan, apply_plan, pick_file
from update_progress import nid_for


class CandidateOverlapTests(unittest.TestCase):
    def fixture(self, path, *, touched=True, clipped=False, alias=False, moved=False):
        head = "a" * 40
        new_head = "b" * 40
        calls = {"details": 0}
        prs = [{"number": 7, "head": {"sha": head}}]
        def fetch(url, token):
            if "/pulls?state=open" in url:
                return prs
            if url.endswith("/pulls/7"):
                calls["details"] += 1
                return {"head": {"sha": new_head if moved and calls["details"] > 1 else head},
                        "changed_files": 1}
            if "/pulls/7/files?" in url:
                return [{"filename":path, "additions": 3 if clipped else 1,
                         "patch": '+APS5_EXPORT("H2e8t5ScQGc", exportHelper);' if alias else
                                  "+void APS5_VABI sceAnotherFunction() {}"}]
            raise AssertionError(url)
        return fetch

    def candidate(self):
        return [{"library": "libSceExample", "nid": nid_for("sceUniqueForTest")}]

    def test_unaffected_library_can_pass_exact_head_audit(self):
        report = check_candidates(self.candidate(), set(), "token", nid_for,
                                  self.fixture("core/libs/prx/libOther/Export.cpp"))
        self.assertTrue(report["scan_complete"])
        self.assertTrue(report["candidates"][0]["verified_clear"])
        self.assertEqual(report["open_pr_verified_heads"], 1)

    def test_unrelated_function_in_same_library_is_not_collision(self):
        report = check_candidates(self.candidate(), set(), "token", nid_for,
                                  self.fixture("core/libs/prx/libSceExample/Export.cpp"))
        self.assertTrue(report["candidates"][0]["verified_clear"])

    def test_other_library_same_nid_on_main_blocks(self):
        candidate = self.candidate()
        report = check_candidates(candidate, {("libother", candidate[0]["nid"])},
                                  "token", nid_for,
                                  self.fixture("docs/readme.md"))
        self.assertFalse(report["candidates"][0]["verified_clear"])
        self.assertIn("current_main_cross_library_nid_collision",
                      report["candidates"][0]["reasons"])

    def test_missing_patch_or_moving_head_fails_closed(self):
        for clipped, moved in [(True, False), (False, True)]:
            report = check_candidates(self.candidate(), set(), "token", nid_for,
                                      self.fixture("core/libs/prx/libOther/Export.cpp",
                                                   clipped=clipped, moved=moved))
            self.assertFalse(report["scan_complete"])
            self.assertFalse(report["candidates"][0]["verified_clear"])
            self.assertEqual(len(report["failures"]), 1)

    def test_explicit_cross_library_export_alias_is_reserved(self):
        report = check_candidates([{"library":"libSceExample","nid":"H2e8t5ScQGc"}],
                                  set(), "token", nid_for,
                                  self.fixture("core/libs/prx/libOther/Export.cpp", alias=True))
        self.assertFalse(report["candidates"][0]["verified_clear"])
        self.assertIn("pr_7_nid_collision", report["candidates"][0]["reasons"])

    def test_unrelated_core_change_does_not_block(self):
        report = check_candidates(self.candidate(), set(), "token", nid_for,
                                  self.fixture("core/kernel/nid_registry.cpp"))
        self.assertTrue(report["candidates"][0]["verified_clear"])

    def test_exact_function_nid_on_open_pr_blocks(self):
        candidate = self.candidate()
        def fetch(url, token):
            if "/pulls?state=open" in url:
                return [{"number": 7, "head": {"sha": "a" * 40}}]
            if url.endswith("/pulls/7"):
                return {"head": {"sha": "a" * 40}, "changed_files": 1}
            if "/pulls/7/files?" in url:
                return [{"filename": "core/libs/prx/libSceExample/Export.cpp",
                         "additions": 1,
                         "patch": "+void APS5_VABI sceUniqueForTest() {}"}]
            raise AssertionError(url)
        report = check_candidates(candidate, set(), "token", nid_for, fetch)
        self.assertFalse(report["candidates"][0]["verified_clear"])
        self.assertIn("pr_7_nid_collision", report["candidates"][0]["reasons"])

    def test_ambiguous_export_macro_blocks(self):
        def fetch(url, token):
            if "/pulls?state=open" in url:
                return [{"number": 7, "head": {"sha": "a" * 40}}]
            if url.endswith("/pulls/7"):
                return {"head": {"sha": "a" * 40}, "changed_files": 1}
            if "/pulls/7/files?" in url:
                return [{"filename": "core/libs/prx/libSceExample/Export.cpp",
                         "additions": 1,
                         "patch": "+APS5_EXPORT(dynamicNid(), opaque);"}]
            raise AssertionError(url)
        report = check_candidates(self.candidate(), set(), "token", nid_for, fetch)
        self.assertFalse(report["candidates"][0]["verified_clear"])
        self.assertIn("pr_7_unverified_registration_path", report["candidates"][0]["reasons"])


class LayoutPlanTests(unittest.TestCase):
    def make_repo(self, root, name, *, cpp_name="Export.cpp", header_name="Api.hpp"):
        library = root / "core/libs/prx" / name
        (library/"include").mkdir(parents=True)
        (library/"CMakeLists.txt").write_text("add_library(dummy)\n")
        (library/cpp_name).write_text(
            '#include "Api.hpp"\nextern "C" {\n'
            'void APS5_VABI existing() { NotImplemented_nid_no_patch(__func__); }\n}\n')
        (library/"include"/header_name).write_text(
            '#pragma once\nextern "C" {\nvoid APS5_VABI existing();\n}\n')
        subprocess.run(["git","init","-q",str(root)],check=True)
        subprocess.run(["git","-C",str(root),"add","."],check=True)
        subprocess.run(["git","-C",str(root),"-c","user.name=Test",
                        "-c","user.email=test@example.invalid","commit","-qm","baseline"],check=True)
        return library

    def test_videoout_like_unimplemented_and_named_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/"AnyPS5"
            lib=self.make_repo(base, "libSceVideoOut",
                               cpp_name="Unimplemented.cpp",header_name="VideoOut.hpp")
            rows=plan(base,[{"library":"libSceVideoOut","name":"sceNewTest","parameters":"void"}])
            self.assertEqual(len(rows),2)
            self.assertTrue(any(p.name=="Unimplemented.cpp" for p in rows))
            self.assertTrue(any(p.name=="VideoOut.hpp" for p in rows))
            self.assertEqual((lib/"Unimplemented.cpp").read_text().count("sceNewTest"),0)

    def test_preexisting_symbol_is_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/"AnyPS5"
            self.make_repo(base,"libSceExample")
            with self.assertRaisesRegex(ValueError,"Existing symbol"):
                plan(base,[{"library":"libSceExample","name":"existing","parameters":"void"}])

    def test_plan_commit_dryrun_and_patch_rollback_on_bad_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp)/"AnyPS5"
            self.make_repo(base,"libSceExample")
            records=[{"library":"libSceExample","name":"sceNew","parameters":"void"}]
            planned=plan(base,records)
            self.assertEqual(subprocess.check_output(
                ["git","-C",str(base),"status","--porcelain"],text=True).strip(),"")
            original={path:path.read_bytes() for path in planned}
            # Writing to a directory instead of a file must fail, restoring originals.
            with self.assertRaises(OSError):
                apply_plan(base, planned, Path(tmp))
            self.assertEqual(original,{path:path.read_bytes() for path in planned})


if __name__ == "__main__":
    unittest.main()
