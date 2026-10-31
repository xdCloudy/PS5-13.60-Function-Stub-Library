#!/usr/bin/env python3
"""Full Git-object based final NID collision audit for a selected AnyPS5 batch.

Unlike the background REST scanner, this scans exact open PR Git trees and
never assumes a clipped GitHub textual patch proves an export is absent.
The open PR head vector is snapshotted twice and every Git ref is verified.
"""
from __future__ import annotations

import re
from pathlib import Path
import subprocess

from candidate_overlap import head_vector, SOURCE, CODE, UNKNOWN_REGISTRATION
from upstream_sync import list_open_prs, DEFINITION, EXPORT_ALIAS, api_json
from prepare_anyps5_constants import FUNCTION

GLOBAL_CODEGEN = re.compile(
    r"^(?:tools/(?:nid_names|stubgen)\.py|core/.*(?:nid_registry|export_registry).*)$",
    re.I,
)
PUBLIC_NAME_DISAMBIG = re.compile(r"_nid_disambig[0-9]+$")
ASM_EXPORT = re.compile(
    r'\bAPS5_(?:SIGNAL_)?ASM_FUNCTION\s*\(\s*"([A-Za-z_][A-Za-z_0-9]*)"\s*\)'
)
ASM_TOKEN = re.compile(r"\bAPS5_(?:SIGNAL_)?ASM_FUNCTION\b")
BUILD_REGISTRATION = re.compile(
    r"^core/libs/prx/([^/]+)/.*(?:CMakeLists\.txt|\.(?:def|map|exports|inc))$",
    re.I,
)


def git(checkout: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(checkout), *args], capture_output=True,
        text=True, errors="replace", check=True)
    return proc.stdout.strip()


def decode_changed_exports(
    diff: str, nid_for, *, candidate_libraries: set[str] | None = None
) -> tuple[set[str], bool]:
    """Parse full textual Git diff additions; unknown registration syntax blocks."""
    reservations: set[str] = set()
    unknown = False
    path = ""
    additions: list[str] = []

    def flush() -> None:
        nonlocal unknown
        if not additions:
            return
        text = "\n".join(additions)
        if GLOBAL_CODEGEN.fullmatch(path):
            unknown = True
        build = BUILD_REGISTRATION.fullmatch(path)
        if build:
            # Export maps, definition files and included registration snippets
            # can introduce a global NID collision from ANY library. Ordinary
            # library-local CMake changes are only uncertain for that library.
            export_metadata = Path(path).suffix.lower() in (
                ".def", ".map", ".exports", ".inc")
            if (export_metadata or candidate_libraries is None or
                    build.group(1).casefold() in candidate_libraries):
                unknown = True
        if not CODE.search(path) or not path.startswith("core/libs/prx/"):
            return
        names = DEFINITION.findall(text)
        aliases = EXPORT_ALIAS.findall(text)
        assembly = ASM_EXPORT.findall(text)
        for symbol in names:
            if symbol.endswith(("_nid_no_patch", "_nid_no_patch_cut")):
                continue
            canonical = PUBLIC_NAME_DISAMBIG.sub(
                "", symbol.removesuffix("_nid_postfix"))
            reservations.add(nid_for(canonical))
        reservations.update(aliases)
        for symbol in assembly:
            if symbol.endswith(("_nid_no_patch", "_nid_no_patch_cut")):
                continue
            canonical = PUBLIC_NAME_DISAMBIG.sub(
                "", symbol.removesuffix("_nid_postfix"))
            reservations.add(nid_for(canonical))
        if (len(re.findall(r"\bAPS5_VABI\b", text)) != len(names) or
                len(re.findall(r"\bAPS5_EXPORT\b", text)) != len(aliases) or
                len(ASM_TOKEN.findall(text)) != len(assembly) or
                UNKNOWN_REGISTRATION.search(text)):
            unknown = True

    for line in diff.splitlines():
        if line.startswith("diff --git "):
            flush()
            additions = []
            path = ""
        elif line.startswith("+++ b/"):
            path = line[6:]
        elif line.startswith("+") and not line.startswith("+++"):
            additions.append(line[1:])
        elif line.startswith("Binary files ") and CODE.search(path):
            unknown = True
    flush()
    return reservations, unknown


HUNK = re.compile(r"^@@ -([0-9]+)(?:,([0-9]+))? \+[0-9]+(?:,[0-9]+)? @@", re.MULTILINE)


def changed_existing_function(base_source: str, patch: str, name: str) -> bool:
    """Did an exact Git old-line hunk touch this function, even without a name?

    Unknown function layouts fail closed. In particular, body-only PR edits
    must not silently bypass NID scanners looking only at added signatures.
    """
    if not patch.strip():
        return False
    matches = [m for m in FUNCTION.finditer(base_source) if m.group("name") == name]
    if len(matches) != 1:
        return True
    match = matches[0]
    first = base_source.count("\n", 0, match.start()) + 1
    last = base_source.count("\n", 0, match.end()) + 1
    hunks = list(HUNK.finditer(patch))
    if not hunks:
        return True
    for h in hunks:
        old_start = int(h.group(1))
        old_count = int(h.group(2) or 1)
        if old_count:
            if old_start <= last and old_start + old_count - 1 >= first:
                return True
        elif first - 1 <= old_start <= last:
            return True
    return False


GENERATED_FORK_REF = re.compile(r"^refs/heads/feat/automated-reviewed-stubs-([0-9a-f]{16})$")


def generated_heads(checkout: Path, fork: str) -> dict[str, str]:
    """Snapshot only branches produced by this workflow, not historical work."""
    listing = git(checkout, "ls-remote", "--heads", fork,
                  "refs/heads/feat/automated-reviewed-stubs-*")
    heads = {}
    for line in listing.splitlines():
        parts = line.split()
        if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{40}", parts[0]):
            raise ValueError("Malformed generated-fork ref")
        match = GENERATED_FORK_REF.fullmatch(parts[1])
        if not match or match.group(1) in heads:
            raise ValueError("Unexpected generated-fork ref")
        heads[match.group(1)] = parts[0]
    if len(heads) > 300:
        raise ValueError("Too many pending generated fork branches")
    return heads


def check_candidates_git(
    checkout: Path, candidates: list[dict],
    main_occupied: set[tuple[str, str]], token: str, nid_for,
    *, fetch=api_json, per_fetch: int = 80, pending_fork_url: str | None = None,
    existing_targets: dict[str, dict] | None = None,
) -> dict:
    """Clear only exact selected identities absent on main and all open PR heads."""
    if not 1 <= per_fetch <= 100:
        raise ValueError("Invalid Git fetch batch")
    by_path: dict[str, list[tuple[str, str]]] = {}
    if existing_targets:
        expected_nids = {r["nid"] for r in candidates}
        if set(existing_targets) != expected_nids:
            raise ValueError("Every reviewed implementation requires an exact target")
        for row in candidates:
            target = existing_targets[row["nid"]]
            if target.get("path") != row.get("path") or target.get("name") != row.get("name"):
                raise ValueError("Reviewed source targets differ from submitted candidates")
            path = row["path"]
            if not path.startswith("core/libs/prx/" + row["library"] + "/"):
                raise ValueError("Reviewed target escapes candidate library")
            by_path.setdefault(path, []).append((row["nid"], row["name"]))

    def changed_existing(base: str, ref: str) -> set[str]:
        if not by_path:
            return set()
        changed = git(checkout, "diff", "--no-ext-diff", "--no-renames",
                      "--name-only", base, ref, "--", *sorted(by_path)).splitlines()
        if not set(changed) <= set(by_path):
            raise ValueError("Unexpected path from reviewed implementation diff")
        touched: set[str] = set()
        for path in changed:
            base_source = git(checkout, "show", f"{base}:{path}")
            patch = git(checkout, "diff", "--no-ext-diff", "--no-renames",
                        "--unified=0", base, ref, "--", path)
            for nid, name in by_path[path]:
                if changed_existing_function(base_source, patch, name):
                    touched.add(nid)
        return touched

    before = head_vector(list_open_prs(token, fetch))
    candidate_libraries = {r["library"].casefold() for r in candidates}
    all_nids = {nid for _, nid in main_occupied}
    reasons: dict[str, set[str]] = {
        r["nid"]: ({"current_main_nid_collision"} if r["nid"] in all_nids else set())
        for r in candidates
    }
    failures = []
    scanned = 0
    audit_refs = {}
    fork_audit = {}
    fork_stable = pending_fork_url is None
    numbered = sorted(before)
    try:
        for offset in range(0, len(numbered), per_fetch):
            subset = numbered[offset:offset + per_fetch]
            specs = [
                f"+refs/pull/{n}/head:refs/anyps5-final/{n}"
                for n in subset
            ]
            git(checkout, "fetch", "--quiet", "--no-tags", "origin", *specs)
        for n in numbered:
            ref = f"refs/anyps5-final/{n}"
            sha = git(checkout, "rev-parse", ref)
            if sha != before[n]:
                raise ValueError(f"PR #{n} head moved while fetching Git ref")
            base = git(checkout, "merge-base", "origin/main", ref)
            # A complete local Git diff has no REST changed-files or patch cap.
            diff = git(checkout, "diff", "--no-ext-diff", "--no-renames",
                       "--unified=0", base, ref, "--", "core/", "tools/")
            reserved, unknown = decode_changed_exports(
                diff, nid_for, candidate_libraries=candidate_libraries)
            body_modified = changed_existing(base, ref)
            for nid, blocked in reasons.items():
                if nid in body_modified:
                    blocked.add(f"pr_{n}_existing_function_modified")
                if nid in reserved:
                    blocked.add(f"pr_{n}_nid_collision")
                if unknown:
                    blocked.add(f"pr_{n}_unknown_export_registration")
            audit_refs[str(n)] = {"sha": sha, "reserved_nids": len(reserved),
                                  "unknown_registration": unknown}
            scanned += 1
    except (subprocess.CalledProcessError, OSError, ValueError) as exc:
        failures.append({"reason": str(exc)[:300]})
    if pending_fork_url is not None:
        try:
            fork_before = generated_heads(checkout, pending_fork_url)
            for suffix, head in sorted(fork_before.items()):
                ref = f"refs/anyps5-pending/{suffix}"
                git(checkout, "fetch", "--quiet", "--no-tags",
                    pending_fork_url,
                    f"+refs/heads/feat/automated-reviewed-stubs-{suffix}:{ref}")
                sha = git(checkout, "rev-parse", ref)
                if sha != head:
                    raise ValueError("Generated fork branch moved while fetching")
                base = git(checkout, "merge-base", "origin/main", ref)
                diff = git(checkout, "diff", "--no-ext-diff", "--no-renames",
                           "--unified=0", base, ref, "--", "core/", "tools/")
                reserved, unknown = decode_changed_exports(
                    diff, nid_for, candidate_libraries=candidate_libraries)
                body_modified = changed_existing(base, ref)
                for nid, blocked in reasons.items():
                    if nid in body_modified:
                        blocked.add(f"generated_fork_{suffix}_existing_function_modified")
                    if nid in reserved:
                        blocked.add(f"generated_fork_{suffix}_nid_collision")
                    if unknown:
                        blocked.add(f"generated_fork_{suffix}_unknown_registration")
                fork_audit[suffix] = {"sha": sha, "reserved_nids": len(reserved),
                                      "unknown_registration": unknown}
            fork_stable = generated_heads(checkout, pending_fork_url) == fork_before
        except (subprocess.CalledProcessError, OSError, ValueError) as exc:
            fork_stable = False
            failures.append({"reason": "Generated fork branch audit failed: " +
                             str(exc)[:220]})
    try:
        after = head_vector(list_open_prs(token, fetch))
        stable = after == before
    except (ValueError, OSError, TypeError) as exc:
        stable = False
        failures.append({"reason": "Failed to resnapshot PR heads: " + str(exc)[:200]})
    complete = not failures and stable and fork_stable and scanned == len(before)
    return {
        "schema_version": 1, "method": "Exact Git diffs for all open PRs and generated pending fork branches, with before/after head snapshots",
        "scan_complete": complete,
        "head_vector_stable": stable,
        "generated_fork_snapshot_stable": fork_stable,
        "generated_fork_branches_verified": len(fork_audit),
        "per_generated_fork_branch_audit": fork_audit,
        "open_pr_total": len(before),
        "open_pr_verified_heads": scanned,
        "failures": failures,
        "per_pr_audit": audit_refs,
        "candidates": [
            {"library": r["library"], "nid": r["nid"],
             "verified_clear": complete and not reasons[r["nid"]],
             "reasons": sorted(reasons[r["nid"]] | (
                 set() if complete else {"incomplete_or_moving_pr_snapshot"}
             ))}
            for r in candidates
        ],
    }
