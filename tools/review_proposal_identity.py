#!/usr/bin/env python3
"""Stable identity fingerprint for idempotent catalogue-review PR publication.

Source commit and manifest changes refresh an *open* proposal, but do not
resurrect a deliberately closed proposal without new identity work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


FIELDS = ("library", "nid", "proposed_name", "source", "observed_status")


def identity_set(document: dict) -> tuple[tuple[str, ...], ...]:
    if (document.get("publication_status") != "DRAFT_REVIEW_ONLY"
            or document.get("canonical_records_mutated") != 0
            or document.get("independent_approval_required") is not True):
        raise ValueError("Not an unapproved, metadata-only review proposal")
    candidates = document.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Proposal must contain at least one candidate")
    identities = {}
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("Malformed candidate")
        values = []
        for key in FIELDS:
            value = candidate.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Missing candidate field: " + key)
            values.append(value.casefold() if key == "library" else value)
        if candidate.get("canonical_name_approved") is not False:
            raise ValueError("Already-approved names cannot enter the review queue")
        key = tuple(values[:2])
        identity = tuple(values)
        if key in identities and identities[key][:3] != identity[:3]:
            raise ValueError("Conflicting names for the same library/NID")
        identities.setdefault(key, identity)
    if document.get("reviewable_identity_count") != len(identities):
        raise ValueError("Declared reviewable identity count disagrees with candidates")
    return tuple(sorted(identities.values()))


def fingerprint(document: dict) -> str:
    payload = json.dumps(identity_set(document), separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def read(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("fingerprint", "same"))
    cli.add_argument("proposal")
    cli.add_argument("other", nargs="?")
    args = cli.parse_args()
    if args.action == "fingerprint":
        if args.other:
            cli.error("fingerprint accepts only one input")
        print(fingerprint(read(args.proposal)))
        return 0
    if not args.other:
        cli.error("same requires two proposal inputs")
    return 0 if identity_set(read(args.proposal)) == identity_set(read(args.other)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
