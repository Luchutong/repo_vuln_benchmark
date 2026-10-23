# rack/rack candidates outside snapshot 2.2.3 — not applicable

Snapshot: rack/rack 2.2.3, snapshot_id `snap_f97687a4e0807cb2`. Decision date: 2026-10-22.

Basis: RubyGems `rack` OSV ranges recorded in `runs/verification/candidate_dossiers.jsonl`,
compared with 2.2.3. No code was executed.

## Rule

Affected when some interval has `introduced <= V < fixed` for V = 2.2.3.
Not applicable when every interval is either fixed at or before the snapshot
(`fixed <= V`) or lies entirely on a later branch (`introduced > V`).

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_407e485196eb6ec06eedac78 | CVE-2012-6109 | 0..1.1.4, 1.2.0..1.2.6, 1.3.0..1.3.7, 1.4.0..1.4.2 | fix already in the snapshot |
| disc2_5d27617ae1dd3b31d5df65cd | CVE-2013-0183 | 1.3.0..1.3.8, 1.4.0..1.4.3 | fix already in the snapshot |
| disc2_e298bcca8a272602ac5d30de | CVE-2013-0184 | 1.1.0..1.1.5, 1.2.0..1.2.7, 1.3.0..1.3.9, 1.4.0..1.4.4 | fix already in the snapshot |
| disc2_b45a1bfb5d5764d2ed258628 | CVE-2013-0262 | 1.5.0..1.5.2, 1.4.0..1.4.5 | fix already in the snapshot |
| disc2_748b3a716f08503fae20d0f5 | CVE-2013-0263 | 1.5.0..1.5.2, 1.4.0..1.4.5, 1.3.0..1.3.10, 1.2.0..1.2.8, 1.1.0..1.1.6 | fix already in the snapshot |
| disc2_70116dc07dabb8e04192ff5c | CVE-2019-16782 | 0..1.6.12, 2.0.0..2.0.8 | fix already in the snapshot |
| disc2_7813f5d8fb65be7261c2664e | CVE-2020-8161 | 0..2.1.3 | fix already in the snapshot |
| disc2_8bcb3a485d8e080bdb62725d | CVE-2020-8184 | 0..2.1.4, 2.2.0..2.2.3 | fix already in the snapshot |
| disc2_1590f084424fdd68e0db06f2 | CVE-2024-39316 | 3.1.0..3.1.5 | fix already in the snapshot |
| disc2_dbd720d0f16c279b811322c4 | CVE-2025-49007 | 3.1.0..3.1.16 | fix already in the snapshot |

## What this report does not decide

- The other 16 candidates have an interval containing 2.2.3 and remain `in_validation`.
- No code-level claim is made; the exclusion uses published ranges only.
