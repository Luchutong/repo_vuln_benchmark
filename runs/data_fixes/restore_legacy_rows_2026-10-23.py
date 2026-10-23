#!/usr/bin/env python3
"""Restore the archived catalog rows for three promoted vulnerabilities.

When the protobuf and gin evaluation snapshots were retargeted, every row tied to
the retired snapshot was moved to ``data/legacy_*_snap_<sid>.jsonl`` — including the
vulnerability, location, review, evidence and status rows. The candidate rows that
reference those vulnerabilities stayed ``status=verified``, so the draft validator
reports "marked verified but no catalog vulnerability", and the two retired snapshots
lost their snapshot-level PASS ``languages`` evidence.

This script puts the archived rows back for the three vulnerabilities whose ids are
not present in the live catalog (CVE-2024-7254 is deliberately skipped: its live row
now belongs to the retargeted snapshot and a second row would duplicate the id):

- ``CVE-2022-1941`` and ``CVE-2022-3509`` at ``snap_6bc3f36eb61ef280``
- ``GHSA-6vm3-jj99-7229`` at ``snap_d4899c7054105aea``

The per-snapshot status rows stay archived: the validator accepts a status row only
for an ``evaluation_target`` snapshot, and both retired snapshots are not targets.
It restores the matching vulnerability/location/review rows, the evidence rows
that target those ids, and the snapshot-level ``languages`` evidence for both
snapshots. Nothing is deleted or rewritten; rows whose ids already exist are refused.
Dry-run by default.
"""
from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

DATA = Path("data")
TARGETS = {
    "snap_6bc3f36eb61ef280": {"CVE-2022-1941", "CVE-2022-3509"},
    "snap_d4899c7054105aea": {"GHSA-6vm3-jj99-7229"},
}
TABLES = ("vulnerabilities", "locations", "reviews", "evidence")


def load(name: str) -> list[dict]:
    path = DATA / f"{name}.jsonl"
    return [json.loads(line) for line in path.open(encoding="utf-8") if line.strip()]


def row_id(row: dict) -> str:
    for key in ("evidence_id", "location_id", "review_id", "vulnerability_id"):
        if key in row:
            return row[key]
    return f'{row.get("snapshot_id")}::{row.get("vulnerability_id")}'


def plan() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = collections.defaultdict(list)
    for sid, vids in TARGETS.items():
        vulns = [json.loads(l) for l in (DATA / f"legacy_snapshot_vulnerabilities_{sid}.jsonl").open()]
        locs = [json.loads(l) for l in (DATA / f"legacy_snapshot_locations_{sid}.jsonl").open()]
        revs = [json.loads(l) for l in (DATA / f"legacy_snapshot_reviews_{sid}.jsonl").open()]
        stats = [json.loads(l) for l in (DATA / f"legacy_snapshot_vulnerability_status_{sid}.jsonl").open()]
        evid = [json.loads(l) for l in (DATA / f"legacy_snapshot_evidence_{sid}.jsonl").open()]
        keep_loc = [r for r in locs if r["vulnerability_id"] in vids]
        loc_ids = {r["location_id"] for r in keep_loc}
        out["vulnerabilities"] += [r for r in vulns if r["vulnerability_id"] in vids]
        out["locations"] += keep_loc
        out["reviews"] += [r for r in revs if r["vulnerability_id"] in vids]
        out["evidence"] += [
            r for r in evid
            if (r["target_type"] == "vulnerability" and r["target_id"] in vids)
            or (r["target_type"] == "location" and r["target_id"] in loc_ids)
            or (r["target_type"] == "snapshot" and r["target_id"] == sid
                and r["field_path"] == "languages")
        ]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    additions = plan()
    conflicts: dict[str, list[str]] = {}
    live: dict[str, list[dict]] = {}
    for table in TABLES:
        live[table] = load(table)
        existing = {row_id(r) for r in live[table]}
        clashes = sorted({row_id(r) for r in additions[table]} & existing)
        if clashes:
            conflicts[table] = clashes
    if conflicts:
        print(json.dumps({"applied": False, "conflicts": conflicts}, indent=2))
        return 1
    report = {t: len(additions[t]) for t in TABLES}
    print(json.dumps({"applied": bool(a.apply), "rows": report}, indent=2))
    if not a.apply:
        return 0
    for table in TABLES:
        rows = live[table] + additions[table]
        with (DATA / f"{table}.jsonl").open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
