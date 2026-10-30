#!/usr/bin/env python3
"""Conservative, transactional patch placement for known AnyPS5 C-ABI layouts."""
from __future__ import annotations

import re
from pathlib import Path
import subprocess

ABI = re.compile(r"\bAPS5_VABI\s+[A-Za-z_]\w*\s*\(")
START = re.compile(r'\bextern\s*"C"\s*\{')
SUFFIXES = {".hpp", ".h", ".cpp", ".cc", ".cxx"}
TOKEN = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|'
                   r"'(?:\\.|[^'\\])*'", re.MULTILINE)


def blocks(source: str) -> list[tuple[int, int]]:
    """Return matching extern-C braces while ignoring comments and strings."""
    masked = TOKEN.sub(lambda match: match.group() if match.group() == '"C"' else re.sub(r"[^\n]", " ", match.group()), source)
    found = []
    for item in START.finditer(masked):
        depth = 0
        for offset in range(item.end() - 1, len(masked)):
            if masked[offset] == "{":
                depth += 1
            elif masked[offset] == "}":
                depth -= 1
                if depth == 0:
                    found.append((item.end() - 1, offset))
                    break
        else:
            raise ValueError("Unclosed extern-C block")
    return found


def pick_file(folder: Path, *, header: bool) -> tuple[Path, str, int]:
    files = sorted(p for p in folder.rglob("*") if p.is_file() and
                   p.suffix.lower() in ({".hpp", ".h"} if header else {".cpp", ".cc", ".cxx"}))
    candidates = []
    for path in files:
        source = path.read_text(encoding="utf-8")
        for left, right in blocks(source):
            if ABI.search(source[left:right]):
                candidates.append((path, source, right))
    if not candidates:
        raise ValueError("No existing extern-C ABI declaration/definition layout; manual placement required")
    libname = folder.name.removeprefix("lib")
    preferred = (["Api.hpp", libname + ".hpp", folder.name + ".hpp"] if header
                 else ["Export.cpp", "Unimplemented.cpp"])
    for basename in preferred:
        found = [row for row in candidates if row[0].name == basename]
        if len(found) == 1:
            return found[0]
    if len(candidates) == 1:
        return candidates[0]
    raise ValueError("Ambiguous declaration/definition layout; manual placement required")


def plan(checkout: Path, records: list[dict]) -> dict[Path, str]:
    if not records or len({r["library"].casefold() for r in records}) != 1:
        raise ValueError("One nonempty library-focused batch required")
    lib = records[0]["library"]
    folder = checkout / "core/libs/prx" / lib
    if not folder.is_dir() or not (folder / "CMakeLists.txt").is_file():
        raise ValueError("Unknown/unregistered upstream library layout")
    cpp, cpp_text, cpp_at = pick_file(folder, header=False)
    hpp, hpp_text, hpp_at = pick_file(folder, header=True)
    all_sources = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                            for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in SUFFIXES)
    definitions, declarations = [], []
    for r in records:
        if r["library"].casefold() != lib.casefold():
            raise ValueError("Mixed library batch")
        name = r["name"]
        if re.search(r"\b" + re.escape(name) + r"\b", all_sources):
            raise ValueError(f"Existing symbol or alias prevents duplicate insertion: {name}")
        signature = "void APS5_VABI " + name + "(" + r["parameters"] + ")"
        declarations.append(signature + ";")
        definitions.append(signature + " {\n    NotImplemented_nid_no_patch(__func__);\n}")
    def insert(source, position, additions):
        prefix = "\n" if position and source[position - 1] != "\n" else ""
        return source[:position] + prefix + "\n\n".join(additions) + "\n" + source[position:]
    return {cpp: insert(cpp_text, cpp_at, definitions),
            hpp: insert(hpp_text, hpp_at, declarations)}


def apply_plan(checkout: Path, planned: dict[Path, str], output: Path) -> Path:
    originals = {path: path.read_bytes() for path in planned}
    try:
        for path, source in planned.items():
            path.write_text(source, encoding="utf-8")
        changed = [str(path.relative_to(checkout)) for path in planned]
        diff = subprocess.check_output(["git", "-C", str(checkout), "diff", "--", *changed],
                                       text=True, stderr=subprocess.PIPE)
        if not diff.strip():
            raise ValueError("No new patch produced")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(diff if diff.endswith("\n") else diff + "\n", encoding="utf-8")
        return output
    except BaseException:
        for path, original in originals.items():
            path.write_bytes(original)
        raise
