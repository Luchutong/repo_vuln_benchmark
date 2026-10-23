# Netty candidates outside snapshot 4.1.59.Final — not applicable

Snapshot: netty/netty tag `netty-4.1.59.Final`, snapshot_id `snap_bb344e672a0544ef`
(repository 1064563). Decision date: 2026-10-22.

Basis: Maven `io.netty*` OSV ranges recorded in
`runs/verification/candidate_dossiers.jsonl`, compared with version 4.1.59.Final.
No code was executed.

## Rule

Affected when `introduced <= V < fixed` for at least one interval. Not applicable when
every interval has `fixed <= V` (fix already shipped) or `introduced > V` (flaw added later).
Versions are compared by numeric release components; the `Final`/`Alpha1` qualifier is
ignored, which does not affect any boundary in this table.

| Candidate | CVE | io.netty intervals | Class | Why not affected |
|---|---|---|---|---|
| disc2_24bc4f8d65059274769c90b9 | CVE-2014-0193 | 3.6.0.Beta1..3.6.9.Final, 3.7.0.Final..3.7.1.Final, 3.8.0.Final..3.8.2.Final, 3.9.0.Final..3.9.1.Final, 4.0.0.Alpha1..4.0.19.Final, 4.0.0.Alpha1..4.0.19.Final | fixed_before_or_at | The snapshot already contains the fix. |
| disc2_003e776a9536099c11273ff6 | CVE-2014-3488 | 0..3.9.2 | fixed_before_or_at | The snapshot already contains the fix. |
| disc2_1f0ecf2310fb1dc4a82cd0e2 | CVE-2015-2156 | 4.0.0..4.0.28.Final, 3.10.0..3.10.3.Final, 0..3.9.8.Final | fixed_before_or_at | The snapshot already contains the fix. |
| disc2_4900e269ce5684f3faf90f64 | CVE-2021-21290 | 4.0.0..4.1.59.Final | fixed_before_or_at | The snapshot already contains the fix. |
| disc2_9760306d1a883d05b1a3c6c6 | CVE-2025-24970 | 4.1.91.Final..4.1.118.Final | introduced_after | The flaw did not exist in the snapshot version. |
| disc2_896edbdd5e561dabbe517174 | CVE-2026-42577 | 4.2.0.Final..4.2.13.Final | introduced_after | The flaw did not exist in the snapshot version. |
| disc2_1bef0d81c331fa7bfbda5cc8 | CVE-2026-48748 | 4.2.0.Final..4.2.15.Final | introduced_after | The flaw did not exist in the snapshot version. |

## What this report does not decide

- The other 25 candidates have at least one interval containing 4.1.59.Final and remain
  `in_validation`.
- No code-level claim is made; the exclusion uses published Maven ranges only.
