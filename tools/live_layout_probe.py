#!/usr/bin/env python3
"""Read-only placement check using real, pinned AnyPS5 source layouts."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from layout_patch import plan
from update_progress import nid_for

LIBRARIES = ("libSceAudioIn", "libSceVideoOut", "libSceUserService")


def probe(checkout: Path) -> dict:
    report = {}
    for library in LIBRARIES:
        name = "sceAutomationLayoutProbeOnly"
        planned = plan(checkout, [{
            "library": library, "name": name, "nid": nid_for(name),
            "parameters": "void", "return_type": "void"
        }])
        report[library] = {
            "files": sorted(str(path.relative_to(checkout)) for path in planned),
            "declarations_planned": sum(text.count(name) for text in planned.values()),
        }
        if report[library]["declarations_planned"] != 2:
            raise ValueError("Layout planning did not generate one declaration and one definition")
    return report


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--upstream-dir", type=Path, required=True)
    a = p.parse_args()
    print(json.dumps(probe(a.upstream_dir.resolve()), sort_keys=True, indent=2))
