#!/usr/bin/env python3
"""Live, fail-closed candidate-specific AnyPS5 PR collision audit.

Same-library unrelated edits are not collisions. Incomplete, ambiguous or moving
PR snapshots fail closed, as do unparsed export registration forms.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from upstream_sync import ROOT_URL, api_json, list_open_prs, DEFINITION, EXPORT_ALIAS

SOURCE = re.compile(r"^core/libs/prx/([^/]+)/")
CODE = re.compile(r"\.(?:cpp|cc|cxx|hpp|h)$")
SHA = re.compile(r"^[0-9a-f]{40}$")
UNKNOWN_REGISTRATION = re.compile(r"\b(?:REGISTER_NID|REGISTER_EXPORT|EXPORT_NID|ASM_FUNCTION)\b")


def head_vector(prs: list[dict]) -> dict[int, str]:
    vector = {}
    for pr in prs:
        number, head = pr.get("number"), pr.get("head", {}).get("sha")
        if (not isinstance(number, int) or number in vector or
                not isinstance(head, str) or not SHA.fullmatch(head)):
            raise ValueError("Incomplete or duplicate open PR head metadata")
        vector[number] = head
    return vector


def check_candidates(candidates: list[dict], main_occupied: set[tuple[str, str]],
                     token: str, nid_for, fetch=api_json) -> dict:
    """Only positively clears identities absent on main and unaffected by ALL PRs.

    A full source-level absence proof for an edited library needs human review:
    arbitrary C++ macros and generated registration files cannot be safely
    interpreted as absent by a regular-expression parser.
    """
    before = head_vector(list_open_prs(token, fetch))
    covered = {key[1] for key in main_occupied}
    result = {(r["library"].casefold(), r["nid"]): set() for r in candidates}
    for key in result:
        if key[1] in covered:
            result[key].add("current_main_cross_library_nid_collision")
    touched = {}
    examined = 0
    failures = []
    for number, head in sorted(before.items()):
        try:
            detail = fetch(f"{ROOT_URL}/pulls/{number}", token)
            if not isinstance(detail, dict) or detail.get("head", {}).get("sha") != head:
                raise ValueError("PR head moved during scan")
            expected = detail.get("changed_files")
            if not isinstance(expected, int) or expected < 0 or expected >= 3000:
                raise ValueError("Unknown or capped changed-file count")
            page, total, libraries, reservations, unknown_global = 1, 0, set(), set(), False
            while True:
                files = fetch(f"{ROOT_URL}/pulls/{number}/files?per_page=100&page={page}", token)
                if not isinstance(files, list):
                    raise ValueError("Invalid files response")
                total += len(files)
                if total > expected or page > 35:
                    raise ValueError("Inconsistent file pagination")
                for file in files:
                    path = file.get("filename", "")
                    match = SOURCE.match(path)
                    if match:
                        libraries.add(match.group(1).casefold())
                    # Inspect actual added C++ exports irrespective of library.
                    # Unrelated changed functions do not reserve a candidate NID.
                    if not CODE.search(path) or path.startswith(("docs/", ".github/")):
                        # Changes to the global NID generator/registration
                        # infrastructure need separate review, not a false
                        # no-collision assertion.
                        if re.search(r"^(?:tools/(?:nid_names|stubgen|pr_overlap)\.py|"
                                     r"core/[^/]*(?:nid|export|registration)[^/]*)$",
                                     path, re.I):
                            unknown_global = True
                        continue
                    patch = file.get("patch")
                    if not isinstance(patch, str):
                        raise ValueError(f"Missing patch for {path}")
                    added = [s[1:] for s in patch.splitlines()
                             if s.startswith("+") and not s.startswith("+++")]
                    if not isinstance(file.get("additions"), int) or len(added) != file["additions"]:
                        raise ValueError(f"Clipped patch for {path}")
                    text = "\n".join(added)
                    names = DEFINITION.findall(text)
                    nids = EXPORT_ALIAS.findall(text)
                    for symbol in names:
                        if symbol.endswith(("_nid_no_patch", "_nid_no_patch_cut")):
                            continue  # Deliberately unexported helper.
                        public_name = re.sub(
                            r"_nid_disambig[0-9]+$", "",
                            symbol.removesuffix("_nid_postfix"))
                        reservations.add(nid_for(public_name))
                    reservations.update(nids)
                    # Any unrecognised export expression might have a literal,
                    # aliased or generated NID. Do not infer non-collision.
                    if (len(re.findall(r"\bAPS5_VABI\b", text)) != len(names) or
                            len(re.findall(r"\bAPS5_EXPORT\b", text)) != len(nids) or
                            UNKNOWN_REGISTRATION.search(text)):
                        unknown_global = True
                if len(files) < 100:
                    break
                page += 1
            if total != expected:
                raise ValueError(f"Truncated file enumeration: {total}/{expected}")
            final_detail = fetch(f"{ROOT_URL}/pulls/{number}", token)
            if not isinstance(final_detail, dict) or final_detail.get("head", {}).get("sha") != head:
                raise ValueError("PR head moved during file enumeration")
            examined += 1
            touched[number] = {"head": head, "libraries": sorted(libraries),
                               "reserved_nids": len(reservations),
                               "global_unknown": unknown_global}
            for key, reasons in result.items():
                if key[1] in reservations:
                    reasons.add(f"pr_{number}_nid_collision")
                if unknown_global:
                    reasons.add(f"pr_{number}_unverified_registration_path")
        except (ValueError, KeyError, TypeError, OSError) as exc:
            failures.append({"pr": number, "reason": str(exc)[:200]})
    after = head_vector(list_open_prs(token, fetch))
    coherent = before == after and examined == len(before) and not failures
    report = {
        "schema_version": 1, "open_pr_total": len(before),
        "open_pr_verified_heads": examined, "head_vector_stable": before == after,
        "scan_complete": coherent, "failures": failures,
        "pr_head_sha": {str(n): sha for n, sha in sorted(before.items())},
        "per_pr_audit": touched,
        "candidates": [{"library": r["library"], "nid": r["nid"],
                        "verified_clear": coherent and not result[(r["library"].casefold(), r["nid"])],
                        "reasons": sorted(result[(r["library"].casefold(), r["nid"])] |
                                          (set() if coherent else {"incomplete_or_moving_pr_snapshot"}))}
                       for r in candidates],
        "method": "Exact head SHA and changed-files pagination; main global NIDs checked. Unrelated modifications in the same library are allowed; incomplete or unknown registration paths block."
    }
    return report


def save_report(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
