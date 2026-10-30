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
                     "patch":"@@ -0,0 +1 @@\n+int APS5_VABI samplePublicFunction(void) { return 0; }"}]
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

if __name__ == "__main__":
    unittest.main()
