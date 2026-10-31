"""Tests for isolated, ABI-provisional WebCore throwing export batches."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from prepare_anyps5_webcore_pending import select,render,OWNER
from update_progress import nid_for


NAME="_ZN7WebCore10JSLocation7destroyEPN3JSC6JSCellE"


class FakeNids:
    @staticmethod
    def compute_nid(name):
        return nid_for(name)

    @staticmethod
    def source_locations(nids):
        return []


def catalogue(name=NAME):
    nid=nid_for(name)
    return {(OWNER,nid):{
        "name":name,"nid":nid,"library":"libSceNKWebKit",
        "name_status":"verified_nid_binding",
        "firmware_13_60_export_confirmed":True,
        "scope":"existing_firmware_system_library",
        "stub_assessment":"throwing_stub_candidate_validation_required",
    }}


def upstream(root):
    folder=root/"core/libs/prx/libSceNKWebKit"
    (folder/"include").mkdir(parents=True)
    (folder/"Export.cpp").write_text("")
    (folder/"libSceNKWebKit.hpp").write_text(
        '#include "prx/libSceNKWebKit/include/InventoryExports.hpp"\n')
    (folder/"include/InventoryExports.hpp").write_text(
        '#pragma once\n#include "SceTypes.hpp"\nextern "C" {\n'
        "int APS5_VABI existingExport();\n}\n")
    debt=root/"docs/dev/debt"
    debt.mkdir(parents=True)
    (debt/"libSceNKWebKit.md").write_text(
        "# libSceNKWebKit technical debt\n")
    return folder


class WebCorePendingTests(unittest.TestCase):
    def test_valid_1360_generates_throwing_declaration_and_debt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            folder=upstream(root)
            selected,details=select(catalogue(),root,FakeNids(),40)
            self.assertEqual(details["selected"],1)
            files=render(root,selected,True)
            self.assertEqual(len(files),3)
            cpp=(folder/"Export.cpp").read_text()
            header=(folder/"include/InventoryExports.hpp").read_text()
            debt=(root/"docs/dev/debt/libSceNKWebKit.md").read_text()
            self.assertIn("NotImplemented_nid_no_patch(__func__)",cpp)
            self.assertNotIn("return 0;",cpp)
            self.assertIn(NAME+"();",header)
            self.assertIn(nid_for(NAME),debt)
            with self.assertRaisesRegex(ValueError,"already present"):
                render(root,selected,True)

    def test_preserves_existing_export_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            folder=upstream(root)
            old='int APS5_VABI existingExport() { return 7; }\n'
            (folder/"Export.cpp").write_text(old)
            selected,_=select(catalogue(),root,FakeNids(),40)
            render(root,selected,True)
            result=(folder/"Export.cpp").read_text()
            self.assertTrue(result.startswith(old))
            self.assertIn("NotImplemented_nid_no_patch(__func__)",result)

    def test_global_other_provider_prevents_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            upstream(root)
            other=root/"core/libs/prx/libOther"
            other.mkdir(parents=True)
            (other/"Existing.cpp").write_text(
                'int APS5_VABI '+NAME+'() { throw 1; }\n')
            with self.assertRaisesRegex(ValueError,"already have source observations"):
                select(catalogue(),root,FakeNids(),40)

    def test_cross_library_nid_export_prevents_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            upstream(root)
            class Reserved(FakeNids):
                @staticmethod
                def source_locations(nids):
                    return [{"nid":nid_for(NAME),"path":"libOther/Export.cpp"}]
            with self.assertRaisesRegex(ValueError,"already have source observations"):
                select(catalogue(),root,Reserved(),40)

    def test_wrong_name_hash_is_not_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            upstream(root)
            bad=catalogue()
            k=next(iter(bad))
            bad[k]["name"]="_ZN7WebCore1X1YE"
            with self.assertRaisesRegex(ValueError,"No verified"):
                select(bad,root,FakeNids(),40)


if __name__=="__main__":
    unittest.main()
