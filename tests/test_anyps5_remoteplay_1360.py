"""No ABI guessing, duplicate registration, or silent return for Remoteplay."""
import tempfile
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from prepare_anyps5_remoteplay_1360 import NAME,NID,LIBRARY,check,append
from update_progress import nid_for


def fixtures(root):
    directory=root/"core/libs/prx/libSceRemoteplay"
    (directory/"include").mkdir(parents=True)
    (directory/"Export.cpp").write_text(
        '#include "prx/libSceRemoteplay/include/InventoryExports.hpp"\n'
        '#include "prx/libc/include/General.hpp"\nextern "C" {\n'
        "int APS5_VABI sceRemoteplayApprove(){return 0;}\n}\n")
    (directory/"include/InventoryExports.hpp").write_text(
        '#pragma once\nextern "C" {\nint APS5_VABI sceRemoteplayApprove();\n}\n')
    (directory/"libSceRemoteplay.hpp").write_text(
        '#include "prx/libSceRemoteplay/include/InventoryExports.hpp"\n')
    debt=root/"docs/dev/debt"
    debt.mkdir(parents=True)
    (debt/"libSceRemoteplay.md").write_text("# Remoteplay debt\n")
    return directory


def record():
    return {(LIBRARY.casefold(),NID):{
        "library":LIBRARY,"name":NAME,"nid":NID,
        "name_status":"verified_nid_binding",
        "firmware_13_60_export_confirmed":True,
        "scope":"existing_firmware_system_library",
        "kind":"defined_function_export",
        "stub_assessment":"throwing_stub_candidate_validation_required",
    }}


class Nids:
    @staticmethod
    def compute_nid(name):
        return nid_for(name)

    @staticmethod
    def source_locations(nids):
        return []


class RemoteplayTests(unittest.TestCase):
    def test_preserve_existing_and_append_throwing_export(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            folder=fixtures(root)
            entry=check(record(),root,Nids())
            self.assertEqual(entry["nid"],NID)
            self.assertFalse(entry["guest_abi_verified"])
            result=append(root,True)
            self.assertEqual(len(result),3)
            source=(folder/"Export.cpp").read_text()
            self.assertIn("sceRemoteplayApprove(){return 0;}",source)
            self.assertIn(NAME+"() {",source)
            self.assertIn("NotImplemented_nid_no_patch(__func__)",source)
            self.assertNotIn(NAME+"(){ return 0; }",source)
            self.assertIn(NAME+"();",(folder/"include/InventoryExports.hpp").read_text())
            self.assertIn(NID,(root/"docs/dev/debt/libSceRemoteplay.md").read_text())
            with self.assertRaisesRegex(ValueError,"already known"):
                append(root,True)

    def test_wrong_name_nid_and_ownership_are_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            fixtures(root)
            wrong=record()
            wrong[LIBRARY.casefold(),NID]["name"]="sceRemoteplayOther"
            with self.assertRaises(ValueError):
                check(wrong,root,Nids())
            wrong=record()
            wrong[LIBRARY.casefold(),NID]["scope"]="ownership_pending"
            with self.assertRaises(ValueError):
                check(wrong,root,Nids())

    def test_existing_export_or_other_provider_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            fixtures(root)
            class Exported(Nids):
                @staticmethod
                def source_locations(nids):
                    return [{"nid":NID,"path":"other/Export.cpp"}]
            with self.assertRaisesRegex(ValueError,"already registered"):
                check(record(),root,Exported())
            other=root/"core/libs/prx/libOther"
            other.mkdir(parents=True)
            (other/"Export.cpp").write_text(
                "int APS5_VABI "+NAME+"(){return 0;}\n")
            with self.assertRaisesRegex(ValueError,"Existing source symbol"):
                check(record(),root,Nids())


if __name__=="__main__":
    unittest.main()
