# vitejs/vite candidates outside snapshot v5.0.11 — not applicable

Snapshot: vitejs/vite v5.0.11, snapshot_id `snap_2e50b228f2432623`. Decision date: 2026-10-22.

Basis: npm `vite` OSV ranges recorded in `runs/verification/candidate_dossiers.jsonl`,
compared with 5.0.11. No code was executed.

## Rule

Affected when some interval has `introduced <= V < fixed` for V = 5.0.11.
Not applicable when every interval is either fixed at or before the snapshot
(`fixed <= V`) or lies entirely on a later branch (`introduced > V`).

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_c83c62c152e969822400e100 | CVE-2022-35204 | 0..2.9.13, 3.0.0-alpha.0..3.0.0-beta.4 | fix already in the snapshot |
| disc2_96ec3cb8afc0f3a77847a9f2 | CVE-2023-34092 | 0..2.9.16, 3.0.2..3.2.7, 4.0.0..4.0.5, 4.1.0..4.1.5, 4.2.0..4.2.3, 4.3.0..4.3.9 | fix already in the snapshot |
| disc2_1d710ecff5165e645e27f9cc | CVE-2026-39363 | 8.0.0..8.0.5, 7.0.0..7.3.2, 6.0.0..6.4.2 | fix already in the snapshot |
| disc2_d6145cf146a21ce11cf2d59b | CVE-2026-39364 | 8.0.0..8.0.5, 7.1.0..7.3.2 | fix already in the snapshot |

## What this report does not decide

- The other 9 candidates have an interval containing 5.0.11 and remain `in_validation`.
- No code-level claim is made; the exclusion uses published ranges only.
