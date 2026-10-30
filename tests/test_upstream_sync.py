import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from update_progress import nid_for
from upstream_sync import scan_open_prs_cached

class ProgressiveOverlapTests(unittest.TestCase):
    def test_cache_advances_to_all_open_prs_and_invalidates_changed_heads(self):
        prs = [{"number": number, "head": {"sha": f"head-{number}"},
                "updated_at": f"2026-10-{number:02d}T01:00:00Z"}
               for number in (1,2,3)]
        calls = []
        def mock_fetch(url, token):
            if "/pulls?state=open" in url:
                return list(prs)
            number = int(url.split("/pulls/")[1].split("/")[0])
            calls.append(number)
            return [{"filename":"core/libs/prx/libSample/Export.cpp",
                     "patch":"@@ -0,0 +1 @@\n+int APS5_VABI samplePublicFunction(void) { return 0; }", "additions":1}]
        nid = nid_for("samplePublicFunction")
        known = {("libsample", nid): {"name":"samplePublicFunction"}}
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "open-pr-cache.json"
            counts=[]
            for _ in range(3):
                found, unknown, meta = scan_open_prs_cached(
                    "test-token", known, set(known), nid_for, cache, 1, mock_fetch)
                counts.append(meta["open_pr_scanned"])
            self.assertEqual(counts, [1,2,3])
            self.assertTrue(meta["open_pr_coverage_complete"])
            self.assertEqual(set(found[("libsample",nid)]), {1,2,3})
            self.assertEqual(len(calls), 3)
            # Unchanged PRs should require no extra per-PR file calls.
            _,_,meta = scan_open_prs_cached("test-token",known,set(known),nid_for,cache,1,mock_fetch)
            self.assertEqual(meta["open_pr_cached"],3)
            self.assertEqual(len(calls),3)
            prs[1]["head"]["sha"] = "changed-head-2"
            _,_,meta = scan_open_prs_cached("test-token",known,set(known),nid_for,cache,1,mock_fetch)
            self.assertTrue(meta["open_pr_coverage_complete"])
            self.assertEqual(meta["open_pr_newly_scanned"],1)
            self.assertEqual(calls.count(2),2)
            prs.pop()
            _,_,meta = scan_open_prs_cached("test-token",known,set(known),nid_for,cache,1,mock_fetch)
            self.assertEqual(meta["open_pr_total"],2)
            self.assertEqual(meta["open_pr_scanned"],2)
            self.assertEqual(len(json.loads(cache.read_text())["prs"]),2)

    def test_literal_export_alias_reserves_original_nid(self):
        prs=[{"number":99,"head":{"sha":"aliashead"},
              "updated_at":"2026-10-30T00:00:00Z"}]
        def mock_fetch(url,token):
            if "/pulls?state=open" in url:
                return prs
            return [{"filename":"core/libs/prx/libSceExample/Export.cpp",
                     "patch":'@@ -0,0 +1 @@\n+APS5_EXPORT("H2e8t5ScQGc", helper_nid_no_patch);',
                     "additions":1}]
        with tempfile.TemporaryDirectory() as directory:
            _,unknown,meta=scan_open_prs_cached(
                "t",{},set(),nid_for,Path(directory)/"cache.json",10,mock_fetch)
            self.assertEqual(unknown[("libsceexample","H2e8t5ScQGc")],{99})
            self.assertTrue(meta["open_pr_coverage_complete"])
            self.assertFalse(meta["open_pr_symbol_coverage_complete"])

    def test_partial_nonempty_patch_is_not_accepted(self):
        prs=[{"number":98,"head":{"sha":"truncated"},
              "updated_at":"2026-10-30T00:00:00Z"}]
        def mock_fetch(url,token):
            if "/pulls?state=open" in url:
                return prs
            return [{"filename":"core/libs/prx/libSceExample/Export.cpp",
                     "patch":"@@ -0,0 +1 @@\n+int APS5_VABI partial() {}",
                     "additions":9}]
        with tempfile.TemporaryDirectory() as directory:
            _,_,meta=scan_open_prs_cached(
                "t",{},set(),nid_for,Path(directory)/"cache.json",10,mock_fetch)
            self.assertEqual(meta["open_pr_errors"],1)
            self.assertFalse(meta["open_pr_coverage_complete"])

    def test_missing_patch_is_not_cached_as_safe(self):
        prs = [{"number":8,"head":{"sha":"h8"},"updated_at":"2026-10-30T00:00:00Z"}]
        def mock_fetch(url, token):
            if "/pulls?state=open" in url:
                return prs
            return [{"filename":"core/libs/prx/libSample/Export.cpp"}]
        with tempfile.TemporaryDirectory() as directory:
            cache=Path(directory)/"cache.json"
            _,_,meta=scan_open_prs_cached("t",{},set(),nid_for,cache,10,mock_fetch)
            self.assertFalse(meta["open_pr_coverage_complete"])
            self.assertEqual(meta["open_pr_unscanned"],1)
            self.assertEqual(meta["open_pr_errors"],1)

    def test_unknown_upstream_identity_tracks_exact_pr(self):
        prs = [{"number":42, "head":{"sha":"h42"}, "updated_at":"2026-10-30T01:00:00Z"}]
        def mock_fetch(url, token):
            if "/pulls?state=open" in url:
                return prs
            return [{"filename":"core/libs/prx/libSample/Export.cpp",
                     "patch":"@@ -0,0 +1 @@\n+int APS5_VABI sourceOnly(void) { return 0; }", "additions":1}]
        with tempfile.TemporaryDirectory() as directory:
            _, unknown, meta = scan_open_prs_cached(
                "t", {}, set(), nid_for, Path(directory)/"cache.json", 10, mock_fetch)
            self.assertEqual(unknown[("libsample",nid_for("sourceOnly"))], {42})
            self.assertTrue(meta["open_pr_coverage_complete"])


    def test_moving_head_is_invalidated_before_writing_cache(self):
        original = {"number": 61, "head": {"sha": "a" * 40},
                    "updated_at": "2026-10-30T01:00:00Z"}
        changed = {"number": 61, "head": {"sha": "b" * 40},
                   "updated_at": "2026-10-30T01:01:00Z"}
        calls = {"lists": 0}

        def fetch(url, token):
            if "/pulls?state=open" in url:
                calls["lists"] += 1
                return [original] if calls["lists"] == 1 else [changed]
            return [{"filename": "core/libs/prx/libSample/Export.cpp",
                     "patch": "+int APS5_VABI verifiedTest() {}",
                     "additions": 1}]

        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory) / "cache.json"
            _, _, meta = scan_open_prs_cached(
                "token", {}, set(), nid_for, cache, 10, fetch)
            self.assertFalse(meta["open_pr_coverage_complete"])
            self.assertFalse(meta["open_pr_snapshot_stable"])
            self.assertEqual(meta["open_pr_stale_heads_invalidated"], 1)
            self.assertEqual(meta["open_pr_scanned"], 0)
            self.assertEqual(meta["open_pr_unscanned"], 1)
            self.assertEqual(json.loads(cache.read_text())["prs"], {})

    def test_capped_3000_file_listing_is_not_cached(self):
        pr = {"number": 62, "head": {"sha": "c" * 40},
              "updated_at": "2026-10-30T01:00:00Z"}
        calls = {"pages": 0}

        def fetch(url, token):
            if "/pulls?state=open" in url:
                return [pr]
            calls["pages"] += 1
            return [{"filename": f"docs/note-{i}.md"} for i in range(100)]

        with tempfile.TemporaryDirectory() as directory:
            _, _, meta = scan_open_prs_cached(
                "token", {}, set(), nid_for,
                Path(directory) / "cache.json", 10, fetch)
            self.assertEqual(calls["pages"], 30)
            self.assertFalse(meta["open_pr_coverage_complete"])
            self.assertEqual(meta["open_pr_errors"], 1)

    def test_missing_addition_count_is_not_a_complete_patch(self):
        pr = {"number": 63, "head": {"sha": "d" * 40},
              "updated_at": "2026-10-30T01:00:00Z"}

        def fetch(url, token):
            if "/pulls?state=open" in url:
                return [pr]
            return [{"filename": "core/libs/prx/libSample/Export.cpp",
                     "patch": "+void APS5_VABI unknown() {}"}]

        with tempfile.TemporaryDirectory() as directory:
            _, _, meta = scan_open_prs_cached(
                "token", {}, set(), nid_for,
                Path(directory) / "cache.json", 10, fetch)
            self.assertFalse(meta["open_pr_coverage_complete"])
            self.assertEqual(meta["open_pr_errors"], 1)


if __name__ == "__main__":
    unittest.main()
