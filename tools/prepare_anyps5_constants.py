#!/usr/bin/env python3
"""Precisely replace existing, reviewed AnyPS5 throwing bodies with constants.

Never derives return semantics from names, NIDs, 3.20 forwarders or a C++
type. Only a separately reviewed, hash-pinned original function and explicit
semantic evidence can authorize a change.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from update_progress import nid_for

MAX_BATCH = 150
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
NID = re.compile(r"^[A-Za-z0-9+/-]{11}$")
SHA = re.compile(r"^[a-f0-9]{64}$")
FUNCTION = re.compile(
    r"(?P<signature>(?P<rtype>(?:[A-Za-z_][A-Za-z0-9_:]*\s*\*?\s*){1,3})"
    r"\s+APS5_VABI\s+(?P<name>[A-Za-z_][A-Za-z_0-9]*)\s*"
    r"\((?P<args>[^(){};]*)\))\s*\{(?P<body>[^{}]*)\}",
    re.MULTILINE,
)
THROW_ONLY = re.compile(r"\s*NotImplemented_nid_no_patch\s*\(\s*__func__\s*\)\s*;\s*")
DECLARATION = re.compile(
    r"(?P<rtype>(?:[A-Za-z_][A-Za-z0-9_:]*\s*\*?\s*){1,3})"
    r"\s+APS5_VABI\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\([^(){};]*\)\s*;"
)
INTEGER = re.compile(r"^(?:int|long|short|size_t|ssize_t|unsigned(?:\s+(?:int|long|short))?|"
                     r"(?:std::)?u?int(?:8|16|32|64)_t)$")
POINTER = re.compile(r"^(?:const\s+)?[A-Za-z_][A-Za-z0-9_:]*(?:\s+const)?\s*\*+$")
RETURNS = {
    "zero": "return 0;",
    "false": "return false;",
    "null": "return nullptr;",
    "noop": "",
}


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def normalize_type(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).replace(" *", "*")


def validate_records(records: list[dict]) -> None:
    if not 1 <= len(records) <= MAX_BATCH:
        raise ValueError("Reviewed batch must contain 1-150 existing functions")
    lib = records[0].get("library")
    if not isinstance(lib, str) or not NAME.fullmatch(lib):
        raise ValueError("Invalid library")
    identities = set()
    for row in records:
        if not isinstance(row, dict):
            raise ValueError("Invalid reviewed row")
        name, nid = row.get("name"), row.get("nid")
        if (row.get("library") != lib or not isinstance(name, str)
                or not NAME.fullmatch(name) or not isinstance(nid, str)
                or not NID.fullmatch(nid) or nid_for(name) != nid):
            raise ValueError("Invalid or mixed-library NID/name")
        if (row.get("behavior_reviewed") is not True
                or row.get("behavior") not in RETURNS
                or not isinstance(row.get("evidence"), str)
                or not row["evidence"].startswith("https://")
                or not isinstance(row.get("review_url"), str)
                or not row["review_url"].startswith("https://github.com/")
                or not all(isinstance(row.get(k), str) and SHA.fullmatch(row[k])
                           for k in ("signature_sha256", "body_sha256"))):
            raise ValueError("Independent behaviour evidence and exact source hashes required")
        if (lib.casefold(), nid) in identities:
            raise ValueError("Duplicate candidate in reviewed batch")
        identities.add((lib.casefold(), nid))
        path = row.get("path")
        if (not isinstance(path, str) or not re.fullmatch(
            r"core/libs/prx/" + re.escape(lib) + r"/[A-Za-z0-9_./-]+\.cpp", path)
                or any(part in (".", "..") for part in Path(path).parts)):
            raise ValueError("Source path outside the reviewed library")


def read_records(path: Path) -> list[dict]:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
               if line.strip()]
    validate_records(records)
    return records


def render(checkout: Path, rows: list[dict]) -> dict[Path, str]:
    """Only edits an exact single-throw body, with verified declaration and ABI."""
    validate_records(rows)
    lib = rows[0]["library"]
    folder = checkout / "core/libs/prx" / lib
    if not folder.is_dir() or not (folder / "CMakeLists.txt").is_file():
        raise ValueError("No registered AnyPS5 library")
    headers = [p for p in folder.rglob("*") if p.is_file()
               and not p.is_symlink() and p.suffix.lower() in (".hpp", ".h")]
    sources = [p for p in folder.rglob("*") if p.is_file()
               and not p.is_symlink() and p.suffix.lower() in (".cpp", ".cc", ".cxx")]
    if not headers or not sources:
        raise ValueError("Cannot verify upstream ABI declarations and sources")
    header_text = "\n".join(p.read_text(encoding="utf-8") for p in headers)
    declarations = list(DECLARATION.finditer(header_text))
    all_definitions = []
    for p in sources:
        all_definitions += [(p, m.group("name")) for m in
                            FUNCTION.finditer(p.read_text(encoding="utf-8"))]
    planned = {}
    for row in rows:
        path = (checkout / row["path"]).resolve()
        if not path.is_relative_to(folder.resolve()) or not path.is_file():
            raise ValueError("Source escapes registered library or is missing")
        cmake_files = [p for p in folder.rglob("CMakeLists.txt")
                       if p.is_file() and not p.is_symlink()]
        # EXCLUDE_FROM_ALL libraries must still compile the exact edited source.
        # A merely present but unregistered C++ file is not a valid target.
        if not any(re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(path.name) +
                             r"(?![A-Za-z0-9_.-])",
                             p.read_text(encoding="utf-8")) for p in cmake_files):
            raise ValueError("Reviewed source is not explicitly registered in a CMake target")
        original = planned.get(path, path.read_text(encoding="utf-8"))
        matches = [m for m in FUNCTION.finditer(original) if m.group("name") == row["name"]]
        if len(matches) != 1 or sum(name == row["name"] for _, name in all_definitions) != 1:
            raise ValueError("Definition missing or ambiguous; no function edited")
        match = matches[0]
        rtype = normalize_type(match.group("rtype"))
        declared = [m for m in declarations if m.group("name") == row["name"]]
        if len(declared) != 1 or normalize_type(declared[0].group("rtype")) != rtype:
            raise ValueError("Missing or mismatched source ABI declaration")
        if sha256(match.group("signature")) != row["signature_sha256"]:
            raise ValueError("Original ABI signature differs from independently reviewed hash")
        if sha256(match.group("body")) != row["body_sha256"] or not THROW_ONLY.fullmatch(match.group("body")):
            raise ValueError("Function body is not an exact standalone throwing stub")
        compatible = {
            "zero": bool(INTEGER.fullmatch(rtype)),
            "false": rtype == "bool",
            "null": bool(POINTER.fullmatch(rtype)),
            "noop": rtype == "void",
        }
        if not compatible[row["behavior"]]:
            raise ValueError("Reviewed constant is not type-compatible with existing ABI")
        replacement = ("\n    " + RETURNS[row["behavior"]] + "\n"
                       if RETURNS[row["behavior"]] else "\n")
        start, end = match.span("body")
        planned[path] = original[:start] + replacement + original[end:]
    return planned


def apply(checkout: Path, rows: list[dict], patch_file: Path) -> None:
    plan = render(checkout, rows)
    original = {p: p.read_bytes() for p in plan}
    try:
        for path, content in plan.items():
            path.write_text(content, encoding="utf-8")
        paths = [str(p.relative_to(checkout)) for p in sorted(plan)]
        diff = subprocess.check_output(["git", "-C", str(checkout),
                                        "diff", "--no-ext-diff", "--", *paths], text=True)
        if not diff.strip():
            raise ValueError("No changes generated")
        patch_file.parent.mkdir(parents=True, exist_ok=True)
        patch_file.write_text(diff if diff.endswith("\n") else diff + "\n", encoding="utf-8")
    except BaseException:
        for p, data in original.items():
            p.write_bytes(data)
        raise


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkout", type=Path, required=True)
    p.add_argument("--evidence", type=Path, required=True)
    p.add_argument("--patch", type=Path, required=True)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    rows = read_records(args.evidence)
    if args.apply:
        apply(args.checkout, rows, args.patch)
    else:
        planned = render(args.checkout, rows)
        print(json.dumps({"eligible": len(rows),
                          "files": sorted(str(p) for p in planned)}, indent=2))


if __name__ == "__main__":
    main()
