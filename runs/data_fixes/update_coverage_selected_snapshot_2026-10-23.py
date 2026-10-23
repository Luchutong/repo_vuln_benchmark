#!/usr/bin/env python3
"""Record the selected-snapshot triage pass in discovery_coverage for axios/echo.

Both repositories gained an evaluation target on 2026-10-23. Their coverage rows
still said "no independently verified vulnerability" and counted every candidate
unresolved. This script appends a correction, records the pass that produced the
verified positive, and leaves the genuinely open rows (possible_affected and
unknown) counted as unresolved. `PASS_KNOWN_SWEEP` is still not claimed.

Dry-run by default. Writes only data/discovery_coverage.jsonl.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data/discovery_coverage.jsonl"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
WHO = "claude-code-orchestrator-2026-10-23"

UPDATES = {
    "23088740": {
        "snapshot_id": "snap_04c033042a3d52eb",
        "tag": "v1.19.0",
        "vulnerability_id": "CVE-2026-101907",
        "unresolved": 12,
        "counts": {"confirmed_affected": 1, "confirmed_not_affected": 44,
                   "duplicate": 10, "possible_affected": 11, "unknown": 1},
        "total": 67,
        "supersedes": "runs/verification/axios_CVE-2026-101907_v1190/migrate_snapshot_04c033042a3d52eb.py",
    },
    "31504491": {
        "snapshot_id": "snap_e0836fa1c53e240d",
        "tag": "v4.15.2",
        "vulnerability_id": "CVE-2026-55677",
        "unresolved": 9,
        "counts": {"confirmed_affected": 1, "confirmed_not_affected": 4,
                   "duplicate": 2, "possible_affected": 9, "unknown": 0},
        "total": 16,
        "supersedes": "runs/verification/echo_CVE-2026-55677_v4152/migrate_snapshot_e0836fa1c53e240d.py",
    },
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    rows = [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = []
    for row in rows:
        spec = UPDATES.get(str(row.get("repo_id")))
        if not spec:
            continue
        counts = spec["counts"]
        row["corrections"] = list(row.get("corrections") or []) + [{
            "corrected_at": NOW,
            "corrected_by": WHO,
            "summary": (
                f"{spec['total']} candidates were triaged against {spec['snapshot_id']} "
                f"({spec['tag']}): confirmed_affected {counts['confirmed_affected']}, "
                f"confirmed_not_affected {counts['confirmed_not_affected']}, "
                f"duplicate {counts['duplicate']}, possible_affected {counts['possible_affected']}, "
                f"unknown {counts['unknown']}. The verified positive is {spec['vulnerability_id']} "
                "after independent review; possible/unknown rows stay open."
            ),
            "supersedes": spec["supersedes"],
        }]
        row["coverage_statement"] = (
            f"Known-source collection is in progress. One catalog-verified positive "
            f"({spec['vulnerability_id']}) was established at {spec['tag']} "
            f"({spec['snapshot_id']}) after the recorded passes. All {spec['total']} candidates "
            f"were triaged at that snapshot "
            f"(confirmed_affected {counts['confirmed_affected']}, "
            f"confirmed_not_affected {counts['confirmed_not_affected']}, "
            f"duplicate {counts['duplicate']}, possible_affected {counts['possible_affected']}, "
            f"unknown {counts['unknown']}); {spec['unresolved']} stay unresolved and are not "
            "excluded. This is not a snapshot-scoped sweep and PASS_KNOWN_SWEEP is not claimed."
        )
        row["passes"] = list(row.get("passes") or []) + [{
            "ended_at": NOW,
            "new_candidate_count": 0,
            "new_verified_count": 1,
            "notes": (
                "Selected-snapshot triage: independent vulnerability review (grade A), promotion, "
                "freeze and audit export for the evaluation target; remaining candidates triaged "
                "from cached records and git ancestry."
            ),
        }]
        row["unresolved_candidates"] = spec["unresolved"]
        changed.append(row["repo_id"])
    print(json.dumps({"changed": changed, "applied": a.apply}, indent=1))
    if not a.apply:
        print("dry-run; pass --apply to write")
        return 0
    tmp = PATH.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tmp.replace(PATH)
    print("applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
