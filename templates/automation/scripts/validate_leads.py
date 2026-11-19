#!/usr/bin/env python3
"""Validate leads.csv (run from the automation folder or anywhere).

Checks the header, market codes, statuses, segments (if restricted), that
every row has a source_url, that emails look like emails, and that no
name+org pair appears twice within a market. Exit code 1 on failure.
"""
import csv
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # the automation folder

HEADER = [
    "date_added", "market", "org", "segment", "name", "role",
    "linkedin_url", "email", "phone", "source_url",
    "evidence_confidence", "rationale", "status", "grade_reason", "graded_date",
]

# Add every market code you use (setup and new-market runs add them here).
VALID_MARKETS = set()
# Leave empty to allow any segment value.
VALID_SEGMENTS = set()
VALID_STATUSES = {"pending", "keep", "reject", "legacy"}
VALID_CONFIDENCE = {"high", "medium", "low", ""}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate(path):
    errors = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != HEADER:
            return [f"header is {reader.fieldnames}, expected {HEADER}"], {}
        rows = list(reader)

    seen = {}
    per_market = {}
    for i, r in enumerate(rows, start=2):
        m = r["market"]
        if VALID_MARKETS and m not in VALID_MARKETS:
            errors.append(f"row {i}: unknown market {m!r} (add it to VALID_MARKETS)")
        if r["status"] not in VALID_STATUSES:
            errors.append(f"row {i}: bad status {r['status']!r}")
        if VALID_SEGMENTS and r["segment"] and r["segment"] not in VALID_SEGMENTS:
            errors.append(f"row {i}: unknown segment {r['segment']!r}")
        if r["evidence_confidence"].lower() not in VALID_CONFIDENCE:
            errors.append(f"row {i}: bad evidence_confidence {r['evidence_confidence']!r}")
        if r["status"] != "legacy" and not r["source_url"].startswith("http"):
            errors.append(f"row {i}: missing or invalid source_url")
        if r["email"] and not EMAIL_RE.match(r["email"]):
            errors.append(f"row {i}: email looks wrong: {r['email']!r}")
        if not r["name"].strip() or not r["org"].strip():
            errors.append(f"row {i}: name and org are required")
        key = (r["name"].strip().lower(), r["org"].strip().lower())
        if key in seen.setdefault(m, set()):
            errors.append(f"row {i}: duplicate name+org in market {m!r}: {r['name']} / {r['org']}")
        seen[m].add(key)
        per_market[m] = per_market.get(m, 0) + 1
    return errors, per_market


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "leads.csv"
    errors, per_market = validate(path)
    if errors:
        print("FAIL")
        for e in errors[:50]:
            print("  " + e)
        sys.exit(1)
    total = sum(per_market.values())
    print(f"PASS: {total} rows, per market {per_market}")


if __name__ == "__main__":
    main()
