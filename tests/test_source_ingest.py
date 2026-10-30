"""Regression tests for public 3.20 forwarding-source ingestion.

Fixtures reproduce the registration structure, not upstream C bodies.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from ingest_320 import classify, ingest, parse_forwarders
from update_progress import nid_for


def example(name="sceAjmBatchCancel", nid=None, owner="libSceAjm"):
    nid = nid or nid_for(name)
    return (
        "int sprx_dlsym(unsigned int handle, const char *nid, void *addr);\n"
        f"static __attribute__ ((used)) void* __ptr_{name};\n"
        f'asm(".global {name}\\n");\n'
        f'if(sprx_dlopen("{owner}", &__handle)) return;\n'
        f'if(sprx_dlsym(__handle, "{nid}", &__ptr_{name})) return;\n'
    )


class Source320Tests(unittest.TestCase):
    def test_real_upstream_nid_pairing(self):
        # This binding exists in upstream libSceAjm.c.
        obs, errors = parse_forwarders(example(), "libSceAjm.c")
        self.assertEqual(errors, [])
        self.assertEqual(len(obs), 1)
        self.assertEqual(obs[0]["nid"], "NVDXiUesSbA")
        self.assertEqual(obs[0]["library"], "libSceAjm")

    def test_registration_order_not_position(self):
        other = "sceAjmBatchWait"
        text = example() + (
            f"static void* __ptr_{other};\n"
            f'asm(".global {other}\\n");\n'
            f'if(sprx_dlsym(__handle, "{nid_for(other)}", &__ptr_{other})) return;\n'
        )
        obs, errors = parse_forwarders(text, "libSceAjm.c")
        self.assertFalse(errors)
        self.assertEqual({r["name"] for r in obs}, {"sceAjmBatchWait", "sceAjmBatchCancel"})

    def test_hyphenated_owners_and_dot_versions_are_registered(self):
        for owner in ("gaikai-player", "libmonosgen-2.0", "libmono-profiler-log"):
            with self.subTest(owner=owner):
                obs, errors = parse_forwarders(example(owner=owner), owner + ".c")
                self.assertEqual(errors, [])
                self.assertEqual(len(obs), 1)
                self.assertEqual(obs[0]["library"], owner)

    def test_missing_owner_parses_name_nid_but_does_not_promote(self):
        text = example().replace(
            'if(sprx_dlopen("libSceAjm", &__handle)) return;', '')
        obs, errors = parse_forwarders(text, "libkernel.c")
        self.assertEqual(errors, [])
        self.assertEqual(len(obs), 1)
        self.assertIsNone(obs[0]["library"])
        proposals, summary = classify(obs,{})
        self.assertEqual(proposals[0]["status"], "ownership_review_required")
        self.assertFalse(proposals[0]["firmware_13_60_export_confirmed"])
        self.assertEqual(summary["statuses"]["ownership_review_required"],1)
        self.assertFalse(proposals[0]["canonical_name_approved"])

    def test_wrong_nid_quarantined(self):
        obs, errors = parse_forwarders(example(nid="12345678901"), "test.c")
        self.assertEqual(obs, [])
        self.assertEqual(errors[0]["reason"], "nid_name_hash_mismatch")

    def test_ambiguous_owner_quarantined(self):
        obs, errors = parse_forwarders(example() +
            'if(sprx_dlopen("libOther", &__handle)) return;', "test.c")
        self.assertEqual(obs, [])
        self.assertEqual(errors[0]["reason"], "ambiguous_library")

    def test_name_recovery_does_not_promote(self):
        n = nid_for("sceAjmBatchCancel")
        ob = [{"library":"libSceAjm", "nid":n,"name":"sceAjmBatchCancel",
               "source_file":"libSceAjm.c"}]
        proposals, report = classify(ob, {("libsceajm", n): {"name":None,
             "firmware_13_60_export_confirmed":True,"name_status":"unresolved"}})
        self.assertEqual(proposals[0]["status"], "name_recovery_candidate")
        self.assertTrue(proposals[0]["firmware_13_60_export_confirmed"])
        self.assertFalse(proposals[0]["canonical_name_approved"])
        self.assertEqual(report["total_valid_registrations"],1)

    def test_historical_only_and_cross_library_alias_preserved(self):
        nid = nid_for("sceAjmBatchCancel")
        ob = [{"library":"libSceAjm","nid":nid,"name":"sceAjmBatchCancel",
               "source_file":"libSceAjm.c"}]
        proposals, _ = classify(ob, {("libother",nid): {"name":"sceAjmBatchCancel"}})
        self.assertEqual(proposals[0]["status"], "historical_only_candidate")
        self.assertTrue(proposals[0]["cross_library_nid_alias_review"])

    def test_withheld_name_never_leaks(self):
        nid = nid_for("sceAjmBatchCancel")
        obs=[{"library":"libSceAjm","nid":nid,"name":"sceAjmBatchCancel",
             "source_file":"libSceAjm.c"}]
        known={("libsceajm",nid): {"name_status":"withheld_by_publication_filter",
                "name":None}}
        proposals, _=classify(obs,known)
        self.assertEqual(proposals[0]["status"],"withheld")
        self.assertNotIn("proposed_name",proposals[0])

    def test_conflicting_source_aliases_not_auto_merged(self):
        nid = nid_for("sceAjmBatchCancel")
        obs=[{"library":"libSceAjm", "nid":nid,"name":name,"source_file":"test.c"}
             for name in ("sceAjmBatchCancel","sceAjmBatchWait")]
        proposals, _=classify(obs,{})
        self.assertTrue(all(p["status"]=="conflicting_source_names" for p in proposals))


    def test_managed_library_suffix_alias_is_not_new_identity(self):
        nid = nid_for("rgctx_fetch_trampoline_mrgctx_40")
        obs = [{"library":"mscorlib.dll","nid":nid,
                "name":"rgctx_fetch_trampoline_mrgctx_40",
                "source_file":"mscorlib.dll.c"}]
        known = {("mscorlib",nid): {"library":"mscorlib",
                 "name":"rgctx_fetch_trampoline_mrgctx_40",
                 "name_status":"verified_nid_binding"}}
        proposals, metrics = classify(obs, known)
        self.assertEqual(proposals, [])
        self.assertEqual(metrics["statuses"]["already_indexed_and_named"], 1)

    def test_quarantine_reason_ledger_is_auditable(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); repo=base/"repo"; src=base/"source"
            (repo/"reports").mkdir(parents=True)
            (repo/"data/firmware-13.60").mkdir(parents=True)
            (repo/"data/historical-3.20-only").mkdir(parents=True)
            src.mkdir()
            (repo/"manifest.json").write_text(json.dumps({"counts":{"total_records":0}}))
            (src/"libSceAjm.c").write_text(example(nid="12345678901"))
            subprocess.run(["git","init","-q",str(src)],check=True)
            subprocess.run(["git","-C",str(src),"add","."],check=True)
            subprocess.run(["git","-C",str(src),"-c","user.name=Test",
                            "-c","user.email=test@example.invalid","commit","-qm","fixture"],check=True)
            doc=ingest(repo,src)
            self.assertEqual(doc["quarantine_diagnostic_records"],1)
            self.assertEqual(doc["quarantine_by_reason"],{"nid_name_hash_mismatch":1})
            self.assertEqual(doc["top_quarantine_sources"],
                             [{"source_file":"libSceAjm.c","rejected_registrations":1}])
            self.assertEqual(doc["canonical_rows_modified"],0)

    def test_full_reconciliation_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp); repo=base/"repo"; src=base/"source"
            (repo/"reports").mkdir(parents=True)
            (repo/"data"/"firmware-13.60").mkdir(parents=True)
            (repo/"data"/"historical-3.20-only").mkdir()
            src.mkdir()
            (repo/"manifest.json").write_text(json.dumps({"counts":{"total_records":0}}))
            (src/"libSceAjm.c").write_text(example())
            subprocess.run(["git","init","-q",str(src)],check=True)
            subprocess.run(["git","-C",str(src),"add","."],check=True)
            subprocess.run(["git","-C",str(src),"-c","user.name=Test",
                            "-c","user.email=test@example.invalid","commit","-qm","fixture"],check=True)
            first=ingest(repo,src)
            report=repo/"reports"/"source-320.json"
            queue=repo/"reports"/"source-320-review.jsonl"
            saved=(report.read_bytes(),queue.read_bytes())
            second=ingest(repo,src)
            self.assertEqual(saved,(report.read_bytes(),queue.read_bytes()))
            forced=ingest(repo,src,force=True)
            self.assertEqual(saved,(report.read_bytes(),queue.read_bytes()))
            self.assertEqual(first,forced)
            self.assertEqual(first,second)
            self.assertEqual(first["statuses"]["historical_only_candidate"],1)
            self.assertEqual(first["canonical_rows_modified"],0)


if __name__ == "__main__":
    unittest.main()
