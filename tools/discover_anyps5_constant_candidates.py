#!/usr/bin/env python3
"""Enumerate existing, simple AnyPS5 throw-only ABI definitions for human review.

This is SOURCE DISCOVERY ONLY. No return behaviour, ABI correctness, firmware
compatibility, or permission to publish is inferred. Do not feed this output
directly to a submission workflow.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess

from prepare_anyps5_constants import (
    INTEGER, POINTER, THROW_ONLY, normalize_type, sha256,
)
from update_progress import nid_for

SUFFIXES = {".cpp", ".cc", ".cxx"}
HEADERS = {".h", ".hpp"}

# Avoid the upstream generator's whitespace-heavy generic regex on entire
# multi-megabyte source files. These bounded, non-overlapping token patterns
# identify only simple source layouts and never infer guest semantics.
TYPE = r"(?:const[ \t]+)?[A-Za-z_][A-Za-z0-9_:]*(?:[ \t]+[A-Za-z_][A-Za-z0-9_:]*){0,2}(?:[ \t]*\*+)?"
NAME = r"[A-Za-z_][A-Za-z0-9_]*"
FRONT = (r"(?P<signature>(?P<rtype>" + TYPE + r")[ \t]+APS5_VABI[ \t]+"
         r"(?P<name>" + NAME + r")[ \t]*\((?P<args>[^(){};]{0,500})\))")
SOURCE_DEFINITION = re.compile(FRONT + r"[ \t\r\n]*\{")
SIMPLE_BODY_DEFINITION = re.compile(FRONT + r"[ \t\r\n]*\{(?P<body>[^{}]{0,512})\}")
HEADER_DECLARATION = re.compile(r"(?P<rtype>" + TYPE + r")[ \t]+APS5_VABI[ \t]+"
                                r"(?P<name>" + NAME + r")[ \t]*\([^(){};]{0,500}\)[ \t\r\n]*;")



def signature_return_class(rtype: str) -> str | None:
    value = normalize_type(rtype)
    if value == "void":
        return "void"
    if value == "bool":
        return "bool"
    if INTEGER.fullmatch(value):
        return "integer"
    if POINTER.fullmatch(value):
        return "pointer"
    return None


def registered_source(folder: Path, source: Path, cmake_text: str) -> bool:
    # An unregistered file might not compile or link into the library.
    name = re.escape(source.name)
    return bool(re.search(r"(?<![A-Za-z0-9_.-])" + name + r"(?![A-Za-z0-9_.-])",
                          cmake_text))


def discover(upstream: Path, revision: str) -> list[dict]:
    """Return only uniquely defined, declared, CMake-listed throw-only bodies."""
    libraries = upstream / "core/libs/prx"
    if not libraries.is_dir():
        raise ValueError("AnyPS5 core/libs/prx directory not found")
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise ValueError("Pin candidate observations to an exact Git SHA")
    rows = []
    for folder in sorted(libraries.iterdir()):
        if not folder.is_dir() or folder.is_symlink():
            continue
        cmakes = sorted(p for p in folder.rglob("CMakeLists.txt")
                        if p.is_file() and not p.is_symlink())
        if not cmakes:
            continue
        cmake_text = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                               for p in cmakes)
        headers = sorted(p for p in folder.rglob("*")
                         if p.is_file() and not p.is_symlink()
                         and p.suffix.lower() in HEADERS)
        sources = sorted(p for p in folder.rglob("*")
                         if p.is_file() and not p.is_symlink()
                         and p.suffix.lower() in SUFFIXES)
        if not headers or not sources:
            continue
        declarations = []
        for p in headers:
            source_text = p.read_text(encoding="utf-8", errors="replace")
            if "APS5_VABI" not in source_text:
                continue
            for match in HEADER_DECLARATION.finditer(source_text):
                declarations.append((p, match))
        # Definitions can appear in several .cpp files: reject all duplicates.
        definitions = []
        name_count = Counter()
        for source in sources:
            content = source.read_text(encoding="utf-8", errors="replace")
            if "APS5_VABI" not in content:
                continue
            # Count every simple C-ABI definition, including nonthrowing
            # bodies, so unrelated extra definitions invalidate eligibility.
            name_count.update(m.group("name") for m in SOURCE_DEFINITION.finditer(content))
            definitions.extend((source, match)
                               for match in SIMPLE_BODY_DEFINITION.finditer(content))
        decl_count = Counter(m.group("name") for _, m in declarations)
        decl_by_name = {m.group("name"): (p, m) for p, m in declarations}
        for source, match in definitions:
            name = match.group("name")
            if (name.endswith(("_nid_no_patch", "_nid_no_patch_cut",
                               "_nid_postfix"))
                    or name_count[name] != 1 or decl_count[name] != 1):
                continue
            rtype = normalize_type(match.group("rtype"))
            category = signature_return_class(rtype)
            header, declaration = decl_by_name[name]
            if (category is None
                    or normalize_type(declaration.group("rtype")) != rtype
                    or not THROW_ONLY.fullmatch(match.group("body"))
                    or not registered_source(folder, source, cmake_text)):
                continue
            # Name->NID is algorithmic metadata, not an assertion that a
            # corresponding PS5 firmware export or guest behaviour exists.
            rows.append({
                "library": folder.name,
                "name": name,
                "nid": nid_for(name),
                "path": source.relative_to(upstream).as_posix(),
                "declaration_path": header.relative_to(upstream).as_posix(),
                "return_type": rtype,
                "return_type_class": category,
                "signature_sha256": sha256(match.group("signature")),
                "body_sha256": sha256(match.group("body")),
                "observed_anyps5_main_sha": revision,
                "behavior": None,
                "behavior_reviewed": False,
                "evidence": None,
                "review_url": None,
                "review_status": "independent_semantic_and_abi_review_required",
            })
    return sorted(rows, key=lambda r: (r["library"].casefold(), r["nid"], r["name"]))


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--upstream-dir", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    args = cli.parse_args()
    upstream = args.upstream_dir.resolve()
    revision = subprocess.check_output(
        ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True).strip()
    rows = discover(upstream, revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as destination:
        for row in rows:
            destination.write(json.dumps(row, sort_keys=True) + "\n")
    libs = {r["library"] for r in rows}
    print(json.dumps({
        "source_commit": revision,
        "candidate_count": len(rows),
        "libraries": len(libs),
        "by_return_type": dict(sorted(Counter(
            r["return_type_class"] for r in rows).items())),
        "behavior_evidence_verified": 0,
        "automatically_approved": 0,
        "output": str(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
