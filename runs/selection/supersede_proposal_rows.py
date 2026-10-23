#!/usr/bin/env python3
"""Move snapshot_proposals rows that a selected evaluation target supersedes.

`data/snapshot_proposals.jsonl` holds advisory-range proposals produced by
`propose_missing_snapshots.py`. The draft validator (`validate_dataset.py:275`)
refuses a proposal row for a repository that already has an evaluation target.
When a repository's target is chosen from such a proposal, the proposal row is
archived verbatim in `runs/selection/superseded_snapshot_proposals.jsonl` and
removed from the main table (same procedure as the ruby/rexml row).

Dry-run by default; `--apply` writes both files. The archive only grows.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROPOSALS = ROOT / "data/snapshot_proposals.jsonl"
SNAPSHOTS = ROOT / "data/snapshots.jsonl"
ARCHIVE = ROOT / "runs/selection/superseded_snapshot_proposals.jsonl"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def dump(path: Path, rows: list[dict]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tmp.replace(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    proposals = load(PROPOSALS)
    archived = load(ARCHIVE)
    archived_ids = {row["repo_id"] for row in archived}
    targets = {
        row["repo_id"]: row
        for row in load(SNAPSHOTS)
        if row.get("evaluation_target")
    }

    superseded, kept = [], []
    for row in proposals:
        target = targets.get(row["repo_id"])
        if target is None:
            kept.append(row)
            continue
        if row["repo_id"] in archived_ids:
            raise SystemExit(f"ABORT: proposal {row['repo_id']} already archived")
        row = dict(row)
        row["superseded_by_snapshot_id"] = target["snapshot_id"]
        row["superseded_by_tag"] = target.get("tag_or_release")
        row["superseded_by_selection_at"] = target.get("frozen_at") or target.get("selected_at")
        row["supersede_note"] = (
            "Repository now has a frozen/proposed evaluation target; the proposal row survives "
            "only as historical evidence and is kept out of the main table."
        )
        superseded.append(row)

    print(json.dumps({
        "proposals_before": len(proposals),
        "proposals_after": len(kept),
        "superseded": [
            {"repo_id": r["repo_id"], "full_name": r.get("full_name"),
             "target": r["superseded_by_snapshot_id"], "tag": r["superseded_by_tag"]}
            for r in superseded
        ],
    }, ensure_ascii=False, indent=2))
    if not args.apply:
        print("dry-run; pass --apply to write")
        return 0
    if not superseded:
        print("nothing to do")
        return 0
    dump(ARCHIVE, archived + superseded)
    dump(PROPOSALS, kept)
    print("applied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
