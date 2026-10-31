"""Dual-firmware review must never promote metadata into ABI or PR approval."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from dual_firmware_review import (classify, identity, load_320, load_1360,
                                  safe_name)
from update_progress import nid_for


def row(name="sceAjmBatchCancel", lib="libSceAjm", **extra):
    return {
        "library": lib, "nid": nid_for(name), "name": name,
        "name_status": "verified_nid_binding",
        "firmware_13_60_export_confirmed": True,
        "kind": "defined_function_export",
        "scope": "existing_firmware_system_library",
        "stub_assessment": "throwing_stub_candidate_validation_required",
        **extra,
    }


class DualFirmwareReviewTests(unittest.TestCase):
    def test_both_firmwares_are_metadata_only(self):
        current = row()
        old = {"library": current["library"], "nid": current["nid"],
               "name": current["name"], "source_file": "libSceAjm.c"}
        entries, counts = classify(
            {identity(old["library"], old["nid"]): old},
            {identity(current["library"], current["nid"]): current})
        self.assertEqual(counts["dual_3.20_and_13.60"], 1)
        self.assertFalse(entries[0]["signature_verified"])
        self.assertFalse(entries[0]["approved_for_auto_submit"])
        self.assertTrue(entries[0]["firmware_13_60_export_confirmed"])

    def test_1360_only_is_distinct_from_historical_only(self):
        newer = row()
        oldname = "sceAjmBatchWait"
        previous = {"library": "libSceAjm", "nid": nid_for(oldname),
                    "name": oldname, "source_file": "libSceAjm.c"}
        entries, counts = classify(
            {identity(previous["library"], previous["nid"]): previous},
            {identity(newer["library"], newer["nid"]): newer})
        self.assertEqual(counts["confirmed_13.60_only"], 1)
        self.assertEqual(counts["historical_3.20_only"], 1)
        self.assertFalse(entries[1]["firmware_13_60_export_confirmed"])
        self.assertFalse(entries[1]["approved_for_auto_submit"])

    def test_false_abi_or_covered_source_never_promoted(self):
        candidate = row(scope="ownership_pending")
        entries, counts = classify({}, {identity(candidate["library"],candidate["nid"]):candidate})
        self.assertFalse(entries)
        self.assertEqual(counts["unverified_library_ownership"], 1)
        covered = row(stub_assessment="covered_in_saved_upstream_snapshot")
        entries, counts = classify({}, {identity(covered["library"],covered["nid"]):covered})
        self.assertFalse(entries)
        self.assertEqual(counts["already_covered_or_reserved_snapshot"], 1)

    def test_conflicting_names_are_not_qualified(self):
        candidate = row()
        old = {"name":"sceAjmBatchWait", "source_file":"libSceAjm.c"}
        entries, counts = classify({identity(candidate["library"],candidate["nid"]):old},
                                   {identity(candidate["library"],candidate["nid"]):candidate})
        self.assertFalse(entries)
        self.assertEqual(counts["cross_version_name_conflict"], 1)

    def test_names_must_match_nid(self):
        self.assertFalse(safe_name("sceAjmBatchCancel","00000000000"))
        self.assertTrue(safe_name("sceAjmBatchCancel",nid_for("sceAjmBatchCancel")))

    def test_reads_original_forwarder_and_confirmed_1360_shard(self):
        name = "sceAjmBatchCancel"
        nid = nid_for(name)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old = root / "source"
            old.mkdir()
            (old / "libSceAjm.c").write_text(
                "static void* __ptr_" + name + ";\n"
                'asm(".global ' + name + r'\n");' + "\n"
                'if(sprx_dlopen("libSceAjm", &__handle)) return;\n'
                'if(sprx_dlsym(__handle, "' + nid + '", &__ptr_' + name + ')) return;\n')
            originals, _ = load_320(old)
            self.assertIn(identity("libSceAjm",nid), originals)
            shard = root / "data" / "firmware-13.60"
            shard.mkdir(parents=True)
            current = row()
            (shard / "test.jsonl").write_text(json.dumps(current)+"\n")
            confirmed, stats = load_1360(root)
            self.assertEqual(stats["confirmed_exports"], 1)
            self.assertEqual(classify(originals,confirmed)[1]["dual_3.20_and_13.60"], 1)

    def test_duplicate_confirmed_1360_rows_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            directory=root/"data"/"firmware-13.60"
            directory.mkdir(parents=True)
            (directory/"test.jsonl").write_text(json.dumps(row())+"\n"+json.dumps(row())+"\n")
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                load_1360(root)


if __name__ == "__main__":
    unittest.main()
