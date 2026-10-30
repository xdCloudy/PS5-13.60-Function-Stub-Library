"""Incremental, auditable enumeration of all open AnyPS5 pull requests.

GitHub Actions' installation token is rate-limited. Rather than auditing an
arbitrary first 400 PRs forever, keep a SHA-keyed cache and scan every open
PR over successive scheduled runs. Updated PR heads automatically invalidate
their previous reservation evidence.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.request

SOURCE = re.compile(r"^core/libs/prx/([^/]+)/.*\.(?:cpp|cc|cxx|h|hpp)$")
DEFINITION = re.compile(r"\bAPS5_VABI\s+([A-Za-z_]\w*)\s*\(")
# Explicit NID aliases must reserve the literal export NID even when the
# helper symbol is named *_nid_no_patch or intentionally hashes differently.
EXPORT_ALIAS = re.compile(r'\bAPS5_EXPORT\s*\(\s*"([A-Za-z0-9+\/\-]{11})"\s*,\s*[A-Za-z_]\w*\s*\)')
ROOT_URL = "https://api.github.com/repos/boykopovar/AnyPS5"


def api_json(url: str, token: str):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "ps5-function-stub-readiness",
               "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers),
                                        timeout=40) as response:
                return json.load(response)
        except (TimeoutError, urllib.error.URLError, ValueError) as exc:
            last = exc
            # One request backing off is better than dropping an entire daily scan.
            if attempt < 2:
                time.sleep(1 + attempt * 2)
    raise last


def list_open_prs(token: str, fetch=api_json):
    records = []
    page = 1
    while True:
        chunk = fetch(f"{ROOT_URL}/pulls?state=open&per_page=100&page={page}", token)
        if not isinstance(chunk, list):
            raise ValueError("Invalid GitHub open PR response")
        records.extend(chunk)
        if len(chunk) < 100:
            return records
        page += 1


def inspect_pr(pr: dict, token: str, nid_for, fetch=api_json):
    """Return a compact NID reservation index for a single PR head."""
    number = int(pr["number"])
    found = set()
    page = 1
    files_seen = 0
    while True:
        files = fetch(f"{ROOT_URL}/pulls/{number}/files?per_page=100&page={page}", token)
        if not isinstance(files, list):
            raise ValueError("Invalid PR file response")
        files_seen += len(files)
        for entry in files:
            match = SOURCE.match(entry.get("filename", ""))
            if not match:
                continue
            # No patch means GitHub omitted useful evidence; retry in a later run.
            patch = entry.get("patch")
            if patch is None:
                raise ValueError(f"Missing patch for #{number} ({entry['filename']})")
            added_lines = [line[1:] for line in patch.splitlines()
                           if line.startswith("+") and not line.startswith("+++")]
            # GitHub can return a nonempty but clipped patch. It is not safe
            # to infer an absent NID from an incomplete hunk.
            if not isinstance(entry.get("additions"), int) or entry["additions"] < 0:
                raise ValueError(f"Missing additions metadata for #{number} ({entry['filename']})")
            if len(added_lines) != entry["additions"]:
                raise ValueError(f"Truncated patch for #{number} ({entry['filename']})")
            additions = "\n".join(added_lines)
            for symbol in DEFINITION.findall(additions):
                found.add((match.group(1).casefold(), nid_for(symbol)))
            for nid in EXPORT_ALIAS.findall(additions):
                found.add((match.group(1).casefold(), nid))
        if len(files) < 100:
            break
        if page >= 30:
            # GitHub's files endpoint returns at most 3,000 entries even if
            # more were changed; the 30th full page is not an absence proof.
            raise ValueError(f"GitHub 3000-file pagination cap for #{number}")
        page += 1
    # GitHub patch lists are capped. A truncated listing cannot certify absence.
    if pr.get("changed_files") is not None and files_seen != int(pr["changed_files"]):
        raise ValueError(f"Unexpected file list for #{number}: {files_seen}/{pr['changed_files']}")
    return {"head": pr["head"]["sha"],
            "keys": [list(key) for key in sorted(found)]}


def read_cache(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("schema_version") != 4:
            return {}
        return document.get("prs", {})
    except (OSError, ValueError, TypeError):
        return {}


def scan_open_prs_cached(token: str, known: dict, verified: set, nid_for,
                         cache_path: Path, max_new: int = 550,
                         fetch=api_json):
    """Preserve completed observations by exact head SHA, audit all PRs over time.

    Cached entries never count when the PR head has moved. Only current open
    PR numbers appear in the new cache; merged/closed PRs expire automatically.
    """
    if max_new < 0:
        raise ValueError("max_new must be nonnegative")
    prs = list_open_prs(token, fetch)
    old = read_cache(cache_path)
    current = {}
    uncached = []
    hits = 0
    for pr in prs:
        number = str(pr["number"])
        cached = old.get(number)
        if isinstance(cached, dict) and cached.get("head") == pr["head"]["sha"] and isinstance(cached.get("keys"), list):
            current[number] = cached
            hits += 1
        else:
            uncached.append(pr)
    # Prioritize recently updated upstream contributions.
    uncached.sort(key=lambda pr: pr.get("updated_at", ""), reverse=True)
    failures = 0
    scanned = 0
    # Parallelism is intentionally bounded to avoid GitHub's secondary limits.
    work = uncached[:max_new]
    if work:
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(inspect_pr, pr, token, nid_for, fetch): pr for pr in work}
            for future in as_completed(futures):
                pr = futures[future]
                try:
                    record = future.result()
                    current[str(pr["number"])] = record
                    scanned += 1
                except (TimeoutError, urllib.error.URLError, ValueError, KeyError, TypeError):
                    failures += 1
    # A PR may merge, close or move to another head while parallel inspection
    # runs. Re-enumerate once, and never persist evidence for a stale head.
    final_prs = list_open_prs(token, fetch)
    before_heads = {str(pr["number"]): pr["head"]["sha"] for pr in prs}
    final_heads = {str(pr["number"]): pr["head"]["sha"] for pr in final_prs}
    if len(before_heads) != len(prs) or len(final_heads) != len(final_prs):
        raise ValueError("Duplicate PR numbers in open-head snapshots")
    stable_snapshot = before_heads == final_heads
    invalidated = [number for number, entry in current.items()
                   if final_heads.get(number) != entry["head"]]
    for number in invalidated:
        del current[number]
    hits = sum(1 for number, entry in current.items()
               if number in old and old[number].get("head") == entry["head"])
    current = dict(sorted(current.items(), key=lambda item: int(item[0])))
    cache_text = json.dumps({"schema_version": 4, "prs": current},
                            indent=2, sort_keys=True) + "\n"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if not cache_path.exists() or cache_path.read_text(encoding="utf-8") != cache_text:
        cache_path.write_text(cache_text, encoding="utf-8")
    reservations = {}
    unknown = {}
    for number, entry in current.items():
        for lib, nid in entry["keys"]:
            key = (lib, nid)
            if key in verified and known.get(key, {}).get("name"):
                reservations.setdefault(key, set()).add(int(number))
            else:
                unknown.setdefault(key, set()).add(int(number))
    total = len(final_prs)
    remaining = total - len(current)
    meta = {
        "open_pr_total": total,
        "open_pr_scanned": len(current),
        "open_pr_cached": hits,
        "open_pr_newly_scanned": scanned,
        "open_pr_unscanned": remaining,
        "open_pr_errors": failures,
        "open_pr_coverage_complete": remaining == 0 and failures == 0 and stable_snapshot,
        "open_pr_snapshot_stable": stable_snapshot,
        "open_pr_stale_heads_invalidated": len(invalidated),
        # Full coverage of parsed PR HEADS is not exhaustive symbol coverage:
        # macros and semantic registration conventions may escape this parser.
        "open_pr_symbol_coverage_complete": False,
        "open_pr_cache_expired_or_closed": len(old) - hits,
        "method": "Current PR heads cached by SHA with post-scan re-enumeration; missing/truncated patches, missing additions counts and GitHub's 3000-file cap fail closed. APS5_VABI and literal APS5_EXPORT identities are provisional reservations, not exhaustive symbol absence.",
    }
    return reservations, unknown, meta
