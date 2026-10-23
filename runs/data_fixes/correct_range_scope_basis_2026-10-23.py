#!/usr/bin/env python3
"""Correct the overstatement in the range-scope triage basis text.

The 2026-10-23 range-scope apply wrote "The snapshot branch descends from the
fixed release, so the fix is included." for 406 rows. Version ordering above the
advisory's upper bound does not prove that the fix commit is an ancestor of the
snapshot, and no ancestry check was run for these rows. Rewrite the sentence to
say exactly what was established, and adjust the notes wording the same way.

Dry-run by default. Writes only data/snapshot_candidate_triage.jsonl.
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / "data/snapshot_candidate_triage.jsonl"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

OLD_SENTENCES = (
    "The snapshot branch descends from the fixed release, so the fix is included.",
    "The snapshot descends from the fixed releases, so the fix is included.",
)
NEW_BASIS = (
    "This is a version-ordering deferral at the frozen tag: the snapshot is outside the "
    "advisory's affected range, but the fix commit was not verified as an ancestor of the "
    "snapshot."
)
OLD_NOTES = "This is a version/branch deferral at the frozen tag, not a code-level audit."
NEW_NOTES = "This is a version-range deferral at the frozen tag, not a code-level audit."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    rows = [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("review_method") != "trusted_range_with_branch":
            continue
        basis = row.get("basis") or ""
        notes = row.get("notes") or ""
        if not any(s in basis for s in OLD_SENTENCES):
            continue
        row["basis"] = basis
        for sentence in OLD_SENTENCES:
            row["basis"] = row["basis"].replace(sentence, NEW_BASIS)
        row["notes"] = notes.replace(OLD_NOTES, NEW_NOTES)
        changed += 1
    print(json.dumps({"changed": changed, "applied": a.apply, "corrected_at": NOW}, indent=1))
    if not a.apply:
        print("dry-run; pass --apply to write")
        return 0
    backup = ROOT / "runs" / "data_fixes" / (
        "snapshot_candidate_triage_before_basis_fix_" + NOW.replace(":", "") + ".jsonl"
    )
    shutil.copy2(PATH, backup)
    tmp = PATH.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tmp.replace(PATH)
    print(json.dumps({"backup": str(backup.relative_to(ROOT))}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
