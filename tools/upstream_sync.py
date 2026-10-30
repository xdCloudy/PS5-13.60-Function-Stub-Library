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
    while True:
        files = fetch(f"{ROOT_URL}/pulls/{number}/files?per_page=100&page={page}", token)
        if not isinstance(files, list):
            raise ValueError("Invalid PR file response")
        for entry in files:
            match = SOURCE.match(entry.get("filename", ""))
            if not match:
                continue
            # No patch means GitHub omitted useful evidence; retry in a later run.
            patch = entry.get("patch")
            if patch is None:
                raise ValueError(f"Missing patch for #{number} ({entry['filename']})")
            additions = "\n".join(line[1:] for line in patch.splitlines()
                                  if line.startswith("+") and not line.startswith("+++"))
            for symbol in DEFINITION.findall(additions):
                found.add((match.group(1).casefold(), nid_for(symbol)))
        if len(files) < 100:
            break
        page += 1
    return {"head": pr["head"]["sha"],
            "keys": [list(key) for key in sorted(found)]}


def read_cache(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        if document.get("schema_version") != 1:
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
    current = dict(sorted(current.items(), key=lambda item: int(item[0])))
    cache_text = json.dumps({"schema_version": 1, "prs": current},
                            indent=2, sort_keys=True) + "\n"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if not cache_path.exists() or cache_path.read_text(encoding="utf-8") != cache_text:
        cache_path.write_text(cache_text, encoding="utf-8")
    reservations = {}
    unknown = set()
    for number, entry in current.items():
        for lib, nid in entry["keys"]:
            key = (lib, nid)
            if key in verified and known.get(key, {}).get("name"):
                reservations.setdefault(key, set()).add(int(number))
            else:
                unknown.add(key)
    total = len(prs)
    remaining = total - len(current)
    meta = {
        "open_pr_total": total,
        "open_pr_scanned": len(current),
        "open_pr_cached": hits,
        "open_pr_newly_scanned": scanned,
        "open_pr_unscanned": remaining,
        "open_pr_errors": failures,
        "open_pr_coverage_complete": remaining == 0,
        "open_pr_cache_expired_or_closed": len(old) - hits,
        "method": "All current PR heads progressively indexed by SHA from added APS5_VABI source declarations; this is not an exhaustive symbol/ABI collision audit",
    }
    return reservations, unknown, meta
