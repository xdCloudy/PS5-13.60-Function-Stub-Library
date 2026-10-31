"""Real local Git integration tests for pre-submission NID collision audit."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from git_candidate_overlap import check_candidates_git, decode_changed_exports, changed_existing_function
from update_progress import nid_for


def git(repo, *args):
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE).strip()


class GitOverlapTests(unittest.TestCase):
    def test_full_diff_recognises_public_nid_postfix(self):
        diff = (
            "diff --git a/core/libs/prx/libSceExample/Export.cpp b/core/libs/prx/libSceExample/Export.cpp\n"
            "+++ b/core/libs/prx/libSceExample/Export.cpp\n"
            "@@ -0,0 +1 @@\n"
            "+void APS5_VABI sceMissing_nid_postfix(void) {}\n"
        )
        reserved, unknown = decode_changed_exports(diff, nid_for)
        self.assertIn(nid_for("sceMissing"), reserved)
        self.assertFalse(unknown)

    def test_assembly_export_nid_postfix_is_reserved(self):
        diff = (
            "diff --git a/core/libs/prx/libSceExample/Clock.cpp b/core/libs/prx/libSceExample/Clock.cpp\n"
            "+++ b/core/libs/prx/libSceExample/Clock.cpp\n"
            "@@ -0,0 +1 @@\n"
            '+APS5_SIGNAL_ASM_FUNCTION("sceClockGuest_nid_postfix")\n'
        )
        reserved, unknown = decode_changed_exports(diff, nid_for)
        self.assertIn(nid_for("sceClockGuest"), reserved)
        self.assertFalse(unknown)

    def test_unrecognised_assembly_macro_is_unknown(self):
        diff = (
            "diff --git a/core/libs/prx/libSceExample/Export.cpp b/core/libs/prx/libSceExample/Export.cpp\n"
            "+++ b/core/libs/prx/libSceExample/Export.cpp\n"
            "+APS5_ASM_FUNCTION(dynamicSymbol)\n"
        )
        reserved, unknown = decode_changed_exports(diff, nid_for)
        self.assertEqual(reserved, set())
        self.assertTrue(unknown)

    def test_relevant_cmake_change_blocks_but_unrelated_library_does_not(self):
        for owner, expected in [("libSceExample",True),("libOther",False)]:
            diff = (
                f"diff --git a/core/libs/prx/{owner}/CMakeLists.txt b/core/libs/prx/{owner}/CMakeLists.txt\n"
                f"+++ b/core/libs/prx/{owner}/CMakeLists.txt\n"
                "+add_library(extra_export_registration)\n"
            )
            _, unknown = decode_changed_exports(
                diff, nid_for, candidate_libraries={"libsceexample"})
            self.assertEqual(unknown, expected, owner)

    def test_unrelated_library_export_map_is_global_unknown(self):
        diff = (
            "diff --git a/core/libs/prx/libOther/Exports.map b/core/libs/prx/libOther/Exports.map\n"
            "+++ b/core/libs/prx/libOther/Exports.map\n"
            "+sceExportFromOtherLib;\n"
        )
        _, unknown = decode_changed_exports(
            diff, nid_for, candidate_libraries={"libsceexample"})
        self.assertTrue(unknown)

    def test_unsupported_dynamic_export_fails_closed(self):
        diff = (
            "diff --git a/core/libs/prx/libSceExample/Export.cpp b/core/libs/prx/libSceExample/Export.cpp\n"
            "+++ b/core/libs/prx/libSceExample/Export.cpp\n"
            "@@ -0,0 +1 @@\n"
            "+APS5_EXPORT(computedNid, helper);\n"
        )
        _, unknown = decode_changed_exports(diff, nid_for)
        self.assertTrue(unknown)

    def test_generated_fork_branch_reserves_unsubmitted_nid(self):
        with tempfile.TemporaryDirectory() as tmp:
            bare=Path(tmp)/"fork.git"
            checkout=Path(tmp)/"checkout"
            subprocess.run(["git","init","--bare","-q",str(bare)],check=True)
            subprocess.run(["git","clone","-q",str(bare),str(checkout)],check=True)
            path=checkout/"core/libs/prx/libSceExample/Export.cpp"
            path.parent.mkdir(parents=True)
            path.write_text("void APS5_VABI sceExisting() {}\n")
            git(checkout,"add",".")
            git(checkout,"-c","user.name=Fixture","-c","user.email=fixture@example.invalid",
                "commit","-qm","base")
            git(checkout,"branch","-M","main")
            git(checkout,"push","-q","-u","origin","main")
            git(checkout,"switch","-q","-c","feat/automated-reviewed-stubs-0123456789abcdef")
            path.write_text(path.read_text()+"void APS5_VABI scePendingFromFork() {}\n")
            git(checkout,"add",".")
            git(checkout,"-c","user.name=Fixture","-c","user.email=fixture@example.invalid",
                "commit","-qm","pending")
            git(checkout,"push","-q","origin","HEAD")
            git(checkout,"switch","-q","main")
            candidate=[{"library":"libSceExample","nid":nid_for("scePendingFromFork")}]
            with patch("git_candidate_overlap.list_open_prs",return_value=[]):
                report=check_candidates_git(
                    checkout,candidate,set(),"mock",nid_for,
                    pending_fork_url=str(bare))
            self.assertTrue(report["scan_complete"])
            self.assertEqual(report["generated_fork_branches_verified"],1)
            self.assertFalse(report["candidates"][0]["verified_clear"])
            self.assertTrue(any(reason.startswith("generated_fork_")
                                for reason in report["candidates"][0]["reasons"]))

    def test_local_git_refs_clear_unrelated_and_block_exact_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            bare = Path(tmp) / "upstream.git"
            checkout = Path(tmp) / "work"
            subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
            subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
            lib = checkout / "core/libs/prx/libSceExample"
            lib.mkdir(parents=True)
            path = lib / "Export.cpp"
            path.write_text("void APS5_VABI sceExisting() {}\n")
            git(checkout, "add", ".")
            git(checkout, "-c", "user.name=Fixture", "-c",
                "user.email=fixture@example.invalid", "commit", "-qm", "base")
            git(checkout, "branch", "-M", "main")
            git(checkout, "push", "-q", "-u", "origin", "main")
            git(checkout, "switch", "-q", "-c", "feature")
            path.write_text(path.read_text() + "void APS5_VABI sceAddedFromPR() {}\n")
            git(checkout, "add", ".")
            git(checkout, "-c", "user.name=Fixture", "-c",
                "user.email=fixture@example.invalid", "commit", "-qm", "add")
            head = git(checkout, "rev-parse", "HEAD")
            git(checkout, "push", "-q", "origin", "HEAD:refs/pull/7/head")
            git(checkout, "switch", "-q", "main")
            snapshot = [{"number": 7, "head": {"sha": head}}]
            candidates = [
                {"library": "libSceExample", "nid": nid_for("sceAddedFromPR")},
                {"library": "libSceExample", "nid": nid_for("sceCompletelyDifferent")},
            ]
            with patch("git_candidate_overlap.list_open_prs", return_value=snapshot):
                result = check_candidates_git(
                    checkout, candidates, set(), "mock", nid_for)
            self.assertTrue(result["scan_complete"])
            self.assertEqual(result["open_pr_verified_heads"], 1)
            self.assertFalse(result["candidates"][0]["verified_clear"])
            self.assertIn("pr_7_nid_collision", result["candidates"][0]["reasons"])
            self.assertTrue(result["candidates"][1]["verified_clear"])

    def test_body_only_pr_collision_detected_without_repeated_abi_line(self):
        source = (
            "int APS5_VABI sceReviewed() {\n"
            " NotImplemented_nid_no_patch(__func__);\n"
            "}\n"
            "int APS5_VABI sceUnrelated() {\n"
            " NotImplemented_nid_no_patch(__func__);\n"
            "}\n"
        )
        inside = ("diff --git a/Export.cpp b/Export.cpp\n"
                  "@@ -2 +2 @@\n"
                  "- NotImplemented_nid_no_patch(__func__);\n"
                  "+ return 0;\n")
        outside = inside.replace("@@ -2 +2 @@", "@@ -5 +5 @@")
        self.assertTrue(changed_existing_function(source, inside, "sceReviewed"))
        self.assertFalse(changed_existing_function(source, outside, "sceReviewed"))
        self.assertTrue(changed_existing_function(source, outside, "sceUnrelated"))
        self.assertTrue(changed_existing_function("bad source", inside, "sceReviewed"))

    def test_existing_function_body_pr_head_blocks_only_changed_function(self):
        with tempfile.TemporaryDirectory() as tmp:
            bare = Path(tmp) / "remote.git"
            checkout = Path(tmp) / "repo"
            subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
            subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
            source = checkout / "core/libs/prx/libSceExample/Export.cpp"
            source.parent.mkdir(parents=True)
            source.write_text(
                "int APS5_VABI sceOne() {\n NotImplemented_nid_no_patch(__func__);\n}\n"
                "int APS5_VABI sceTwo() {\n NotImplemented_nid_no_patch(__func__);\n}\n"
            )
            git(checkout, "add", ".")
            git(checkout, "-c", "user.name=Fixture", "-c",
                "user.email=fixture@example.invalid", "commit", "-qm", "main")
            git(checkout, "branch", "-M", "main")
            git(checkout, "push", "-q", "-u", "origin", "main")
            git(checkout, "switch", "-q", "-c", "other-implementation")
            source.write_text(source.read_text().replace(
                "int APS5_VABI sceTwo() {\n NotImplemented_nid_no_patch(__func__);",
                "int APS5_VABI sceTwo() {\n return 0;"))
            git(checkout, "add", ".")
            git(checkout, "-c", "user.name=Fixture", "-c",
                "user.email=fixture@example.invalid", "commit", "-qm", "change body")
            head = git(checkout, "rev-parse", "HEAD")
            git(checkout, "push", "-q", "origin", "HEAD:refs/pull/9/head")
            git(checkout, "switch", "-q", "main")
            path = "core/libs/prx/libSceExample/Export.cpp"
            candidates = [
                {"library": "libSceExample", "name": name, "nid": nid_for(name),
                 "path": path} for name in ("sceOne", "sceTwo")
            ]
            targets = {r["nid"]: {"name": r["name"], "path": path}
                       for r in candidates}
            with patch("git_candidate_overlap.list_open_prs",
                       return_value=[{"number": 9, "head": {"sha": head}}]):
                outcome = check_candidates_git(
                    checkout, candidates, set(), "mock", nid_for,
                    existing_targets=targets)
            self.assertTrue(outcome["scan_complete"])
            self.assertTrue(outcome["candidates"][0]["verified_clear"])
            self.assertFalse(outcome["candidates"][1]["verified_clear"])
            self.assertIn("pr_9_existing_function_modified",
                          outcome["candidates"][1]["reasons"])


    def test_header_only_parameter_changes_reserve_exact_declaration(self):
        header = (
            "int APS5_VABI sceReviewed(\n"
            "    int original_parameter\n"
            ");\n"
            "int APS5_VABI sceElse(\n"
            "    int other_parameter\n"
            ");\n"
        )
        changed_one = (
            "diff --git a/Example.hpp b/Example.hpp\n"
            "@@ -2 +2 @@\n"
            "-    int original_parameter\n"
            "+    int changed_parameter\n"
        )
        changed_other = changed_one.replace("@@ -2 +2 @@", "@@ -5 +5 @@")
        self.assertTrue(changed_existing_function(
            header, changed_one, "sceReviewed", declaration=True))
        self.assertFalse(changed_existing_function(
            header, changed_other, "sceReviewed", declaration=True))
        self.assertTrue(changed_existing_function(
            header, changed_other, "sceElse", declaration=True))



if __name__ == "__main__":
    unittest.main()
