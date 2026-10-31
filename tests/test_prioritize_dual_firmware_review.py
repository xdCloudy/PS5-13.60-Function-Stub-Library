"""Ensure prioritisation only ranks unapproved 13.60 candidates."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from prioritize_dual_firmware_review import prioritize, report_md


def entry(name, source, status="no_direct_upstream_source_observation", **kwargs):
    return {
        "library":"libSceExample","name":name,"nid":"A"+name[-1]+"234567890",
        "evidence_class":source,
        "firmware_13_60_export_confirmed":source!="historical_3.20_only",
        "live_main_source_scan":status,
        "signature_verified":False,
        "behaviour_verified":False,
        "approved_for_auto_submit":False,
        **kwargs,
    }


class PriorityTests(unittest.TestCase):
    def test_13_60_only_with_no_main_symbol_is_selected(self):
        rows=[
            entry("sceTestA","dual_3.20_and_13.60"),
            entry("sceTestB","confirmed_13.60_only"),
            entry("sceTestC","historical_3.20_only"),
            entry("sceTestD","dual_3.20_and_13.60",
                  status="upstream_source_symbol_observed"),
        ]
        prioritised,stats=prioritize(rows)
        self.assertEqual([x["name"] for x in prioritised],["sceTestA","sceTestB"])
        self.assertEqual(stats["counts"]["priority_candidates"],2)
        self.assertEqual(stats["counts"]["source_symbol_already_observed"],1)
        self.assertEqual(stats["counts"]["historical_or_unqualified"],1)
        self.assertEqual(stats["automatic_approvals"],0)
        self.assertFalse(prioritised[0]["safe_to_submit_without_further_evidence"])
        self.assertIn("Highest-volume libraries",report_md(prioritised,stats,5))

    def test_approval_and_duplicate_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"approved"):
            prioritize([entry("sceTestA","dual_3.20_and_13.60",
                              approved_for_auto_submit=True)])
        one=entry("sceTestA","dual_3.20_and_13.60")
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            prioritize([one,one])

    def test_cross_provider_symbols_are_excluded_from_submissions(self):
        rows=[
            entry("sceTestA", "dual_3.20_and_13.60",
                  status="upstream_other_library_source_symbol_observed"),
            entry("sceTestB", "confirmed_13.60_only",
                  status="no_direct_upstream_source_observation"),
        ]
        ranked, stats=prioritize(rows)
        self.assertEqual([row["name"] for row in ranked], ["sceTestB"])
        self.assertEqual(stats["counts"]["source_symbol_in_other_provider"], 1)
        self.assertFalse(ranked[0]["approved_for_auto_submit"])
        self.assertIn("provisional", report_md(ranked, stats, 5).lower())

    def test_unknown_source_state_rejected(self):
        with self.assertRaisesRegex(ValueError,"Unknown"):
            prioritize([entry("sceTestA","dual_3.20_and_13.60",
                              status="not_checked")])


if __name__=="__main__":
    unittest.main()
