"""Public SDK hint matching cannot become automatic ABI evidence."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from match_public_ps5_sdk_hints import index_headers, enrich


class PublicSdkHintTests(unittest.TestCase):
    def test_macro_and_declaration_name_observations(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            path=root/"ps5"
            path.mkdir()
            (path/"libkernel.h").write_text(
                "_Fn_(int, sceKernelSleep, uint32_t seconds);\n"
                "int sceKernelUsleep(unsigned int microseconds);\n")
            index=index_headers(root,"ps5")
            self.assertEqual(index["sceKernelSleep"][0]["line"],1)
            self.assertEqual(index["sceKernelUsleep"][0]["line"],2)

    def test_no_unverified_promotion_even_with_two_sources(self):
        row={"library":"libkernel", "name":"sceKernelSleep","nid":"12345678901",
             "signature_verified":False,"behaviour_verified":False,
             "approved_for_auto_submit":False}
        refs={"PS5Dev/PS5SDK":{"sceKernelSleep":[{"path":"ps5/kernel.h","line":5}]},
              "ps5-payload-dev/sdk":{"sceKernelSleep":[{"path":"include/ps5/foo.h","line":12}]}}
        out,counts=enrich([row],refs)
        self.assertEqual(counts["matched_at_least_one_sdk"],1)
        self.assertFalse(out[0]["signature_verified"])
        self.assertFalse(out[0]["approved_for_auto_submit"])
        self.assertFalse(out[0]["public_sdk_match_is_abi_proof"])
        self.assertEqual(len(out[0]["public_sdk_header_name_observations"]),2)

    def test_empty_public_refs_remain_blocked(self):
        row={"library":"libSceExample", "name":"sceTest", "nid":"ABCDEFGHIJK",
             "signature_verified":False,"behaviour_verified":False,
             "approved_for_auto_submit":False}
        out,counts=enrich([row],{"PS5Dev/PS5SDK":{}})
        self.assertEqual(counts["no_public_sdk_match"],1)
        self.assertTrue(out[0]["review_required"])
        self.assertEqual(out[0]["public_sdk_header_name_observations"],{})


if __name__=="__main__":
    unittest.main()
