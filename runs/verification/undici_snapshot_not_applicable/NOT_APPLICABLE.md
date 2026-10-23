# nodejs/undici candidates outside snapshot v5.19.0 — not applicable

Snapshot: nodejs/undici v5.19.0, snapshot_id `snap_24c4a191fd049fc3`. Decision date: 2026-10-22.

Basis: npm `undici` OSV ranges recorded in `runs/verification/candidate_dossiers.jsonl`,
compared with 5.19.0. No code was executed.

## Rule

Affected when some interval has `introduced <= V < fixed` for V = 5.19.0.
Not applicable when every interval is either fixed at or before the snapshot
(`fixed <= V`) or lies entirely on a later branch (`introduced > V`).

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_3bfe40713c72b2f9f5ebe049 | CVE-2022-31150 | 0..5.8.0 | fix already in the snapshot |
| disc2_07276f4ca58b5f5f12e4a80c | CVE-2022-31151 | 0..5.8.0 | fix already in the snapshot |
| disc2_b806f6442919e5381d68f4d2 | CVE-2022-35948 | 0..5.8.2 | fix already in the snapshot |
| disc2_44a7f8b48144615fc17b9c7b | CVE-2022-35949 | 0..5.8.2 | fix already in the snapshot |
| disc2_9afafe55fab649e7a300964c | CVE-2024-24750 | 6.0.0..6.6.1 | fix already in the snapshot |
| disc2_1eac6a1b69ae5ca4a915a455 | CVE-2024-38372 | 6.14.0..6.19.2 | fix already in the snapshot |
| disc2_5cf88929380250a232de2b11 | CVE-2026-13697 | 7.0.0..7.29.0, 8.0.0..8.9.0 | fix already in the snapshot |
| disc2_f3f8d3ff4b05dc4bcd17c56c | CVE-2026-14643 | 7.0.0..7.29.0, 8.0.0..8.9.0 | fix already in the snapshot |
| disc2_9ae0f2c3e49d4dc476928400 | CVE-2026-18149 | 7.11.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_ff1f9aced92e5e1ecbb23a60 | CVE-2026-19534 | 6.7.0..6.28.1, 7.0.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_0e00f0abd0973af3614448ca | CVE-2026-84890 | 7.15.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_723ce3ec73dbc0256cd90e74 | CVE-2026-84933 | 7.0.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_855a62dfad007f9e82c63e3c | CVE-2026-84947 | 7.1.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_88c3bdbb3a6dc291387db776 | CVE-2026-84961 | 7.24.1..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_5ba4be75d1ddc59372cde150 | CVE-2026-85008 | 7.0.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_886b8569262bca6edad500b2 | CVE-2026-85014 | 7.0.0..7.29.1, 8.0.0..8.10.2 | fix already in the snapshot |
| disc2_ee9ed841df3b70fc821b920b | CVE-2026-85024 | 6.25.0..6.28.1, 7.28.0..7.29.1, 8.1.0..8.10.2 | fix already in the snapshot |
| disc2_d0f90ab0dd69d5ad036d7ed2 | CVE-2026-85152 | 8.10.0..8.10.2 | fix already in the snapshot |

## What this report does not decide

- The other 11 candidates have an interval containing 5.19.0 and remain `in_validation`.
- No code-level claim is made; the exclusion uses published ranges only.
