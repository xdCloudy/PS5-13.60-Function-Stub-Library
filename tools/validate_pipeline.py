#!/usr/bin/env python3
"""Fail closed when JSON, dashboard and Markdown coverage totals diverge.

Run after generators, not before. This does not approve upstream names or ABI.
"""
from __future__ import annotations

import json
from pathlib import Path


def validate(root: Path) -> dict:
    root=root.resolve()
    def j(rel):
        return json.loads((root/rel).read_text(encoding="utf-8"))
    doc=j("reports/coverage-matrices.json")
    preview=j("site/data.json")
    progress=j("reports/progress.json")
    manifest=j("manifest.json")
    source=j("reports/source-320.json")
    symbols=j("reports/anyps5-symbol-states.json")
    if doc != preview:
        raise ValueError("Dashboard and canonical JSON matrix disagree")
    total=doc["discovery"]["indexed"]
    inv=progress["inventory"]
    for name,actual,expected in (
        ("inventory indexed",total,manifest["counts"]["total_records"]),
        ("13.60 source scope",doc["discovery"]["confirmed_13_60"],manifest["counts"]["firmware-13.60"]),
        ("historical source scope",doc["discovery"]["historical_only"],manifest["counts"]["historical-3.20-only"]),
        ("named",doc["discovery"]["published_named"],manifest["counts"]["resolved_names"]),
        ("strict verification",doc["discovery"]["strictly_verified_names"],inv["strictly_reverified_named_records"]),
        ("library rows",len(doc["libraries"]),inv["libraries"]),
        ("source revision",doc["source_revisions"]["ps5_320"],source["inputs"]["source_commit"]),
        ("AnyPS5 revision",doc["source_revisions"]["anyps5_main"],symbols["source_sha"]),
        ("3.20 valid registrations",sum(source["statuses"].values()),source["total_valid_registrations"]),
        ("AnyPS5 scanned symbols",sum(symbols["states"].values()),symbols["observed_library_nid_records"]),
    ):
        if actual != expected:
            raise ValueError(f"{name}: {actual!r} != {expected!r}")
    d=doc["discovery"]
    if not(0 <= d["strictly_verified_names"] <= d["published_named"] <= total):
        raise ValueError("Invalid name recovery progression")
    if d["confirmed_13_60"] + d["historical_only"] != total:
        raise ValueError("Firmware partitions overlap or do not cover inventory")
    if sum(r["indexed"] for r in doc["libraries"]) != total:
        raise ValueError("Per-library identity totals disagree")
    if sum(r["strict_verified"] for r in doc["libraries"]) != d["strictly_verified_names"]:
        raise ValueError("Per-library strictly rehashed names disagree")
    if sum(r["named"] for r in doc["libraries"]) != d["published_named"]:
        raise ValueError("Per-library published names disagree")
    for row in doc["libraries"]:
        if not (0 <= row["strict_verified"] <= row["named"] <= row["indexed"]):
            raise ValueError("Invalid per-library name progression")
        if row["unresolved"] != row["indexed"]-row["named"]:
            raise ValueError("Invalid unresolved count")
        if row["firmware_13_60"]+row["historical_only"] != row["indexed"]:
            raise ValueError("Inconsistent per-library firmware partitions")
        if row["anyps5_main_definitions"]>row["indexed"]:
            raise ValueError("AnyPS5 source matches cannot exceed catalogue records")
    h=doc["automation_health"]
    if h["pr_total"] is not None and (h["pr_scanned"]<0 or h["pr_total"]<h["pr_scanned"]):
        raise ValueError("Invalid PR scan counts")
    if h["pr_complete"] and (h["pr_total"] is None or h["pr_total"]!=h["pr_scanned"] or h["pr_errors"]):
        raise ValueError("Invalid completed PR scan")
    if h["overlap_publication_safe"] is not False:
        raise ValueError("Heuristic symbol scan cannot certify safe publication")
    if source["canonical_rows_modified"] != 0:
        raise ValueError("External source importer unexpectedly mutated canonical records")
    md=(root/"reports/coverage-matrices.md").read_text(encoding="utf-8")
    for required in ("## A. Discovery","## B. Per-library source comparison",
                     "## C. Readiness stages","## D. Ownership classifications",
                     "## E. Review priorities","## F. Automation health",
                     f"{total:,}",f"{d['strictly_verified_names']:,}"):
        if required not in md:
            raise ValueError(f"Markdown matrix missing {required}")
    html=(root/"site/index.html").read_text(encoding="utf-8")
    if 'fetch("./data.json"' not in html:
        raise ValueError("Dashboard is not reading the generated JSON")
    return {"indexed":total,"libraries":len(doc["libraries"]),
            "strict_verified":d["strictly_verified_names"],
            "source_registrations":source["total_valid_registrations"],
            "anyps5_source_symbols":symbols["observed_library_nid_records"],
            "published_canonical_changes":source["canonical_rows_modified"],
            "checked":True}


if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    print(json.dumps(validate(root),indent=2))
