# Axios candidates outside snapshot v1.15.0 — not applicable

Snapshot: axios/axios v1.15.0, commit `772a4e54ecc4cc2421e2b746daff0aca10f359d7`,
snapshot_id `snap_a64c7ddbbb7030b7`.
Decision date: 2026-10-22.
Basis: OSV SEMVER `affected` ranges (npm axios) in
`runs/discovery_v2/osv_queries/43acebec61c5b7f04ddfda47.json`, compared with the
exact snapshot version 1.15.0. No code was executed.

## Semver rule used

For an OSV range `{introduced: I, fixed: F}` a version V is affected when
`I <= V < F` (npm semver ordering). The snapshot is affected only if at least one
1.x range contains 1.15.0. A candidate is not applicable to this snapshot when
every relevant range has `F <= 1.15.0` (the fix is already in the snapshot) or
`I > 1.15.0` (the flaw was introduced after the snapshot).

## Candidates to reject

### Fixed at or before 1.15.0 (fix already present)

| Candidate | CVE / GHSA | 1.x range | Fixed | Why not affected |
|---|---|---|---|---|
| disc2_3b58f77ee34a25cdb112a127 | CVE-2019-10742 / GHSA-42xw-2xvc-qx8m | 0.x only | 0.18.1 | no 1.x range; 1.15.0 is above the fixed 0.x release |
| disc2_8ccffc5e63c4c29493fb7db4 | CVE-2020-28168 / GHSA-4w2v-q235-vp99 | 0.x only | 0.21.1 | no 1.x range; 1.15.0 is above the fixed 0.x release |
| disc2_68fa58cebf588a2b53f9973d | CVE-2021-3749 / GHSA-cph5-m8f7-6c5x | 0.x only | 0.21.2 | no 1.x range; 1.15.0 is above the fixed 0.x release |
| disc2_6e97f558a3408b140748789f | CVE-2023-45857 / GHSA-wf5p-g6vw-rhxx | 1.0.0 – 1.6.0 | 1.6.0 | 1.15.0 >= 1.6.0 |
| disc2_d04b6ec3023d6347a2a60aff | CVE-2024-39338 / GHSA-8hc4-vh64-cxmj | 1.3.2 – 1.7.4 | 1.7.4 | 1.15.0 >= 1.7.4 |
| disc2_ec9d334413a375fd9dc63f3c | CVE-2025-27152 / GHSA-jr5f-v2jv-69x6 | 1.0.0 – 1.8.2 | 1.8.2 | 1.15.0 >= 1.8.2 |
| disc2_dafa1b836e80eb31a075a7da | CVE-2025-58754 / GHSA-4hjh-wcwx-xvwj | 1.0.0 – 1.12.0 | 1.12.0 | 1.15.0 >= 1.12.0 |
| disc2_0ff2e528d1ea2973d4ecfce0 | CVE-2026-25639 / GHSA-43fc-jf86-j433 | 1.0.0 – 1.13.5 | 1.13.5 | 1.15.0 >= 1.13.5 |
| disc2_082db01284f93662691de3b4 | CVE-2026-39865 / GHSA-qj83-cq47-w5f8 | 1.13.0 – 1.13.2 | 1.13.2 | 1.15.0 >= 1.13.2 |
| disc2_63561be0b60698a83c2b2e7b | CVE-2025-62718 / GHSA-3p68-rc4w-qgx5 | 1.0.0 – 1.15.0 | 1.15.0 | 1.15.0 is the first fixed release |
| disc2_6c7f2bfbe8787f642dd3956d | CVE-2026-40175 / GHSA-fvcv-3m26-pcqx | 1.0.0 – 1.15.0 | 1.15.0 | 1.15.0 is the first fixed release |

### Introduced after 1.15.0

| Candidate | CVE / GHSA | 1.x range | Introduced | Why not affected |
|---|---|---|---|---|
| disc2_aa4f47c4c377e6f33b3b02ab | CVE-2026-67314 / GHSA-xj6q-8x83-jv6g | 1.15.2 – 1.18.0 | 1.15.2 | 1.15.0 < 1.15.2 |
| disc2_b1d5178f6325dfd9dd466adb | CVE-2026-67320 / GHSA-gcfj-64vw-6mp9 | 1.15.2 – 1.18.0 | 1.15.2 | 1.15.0 < 1.15.2 |
| disc2_a882cec13e7ff8f88a8aa689 | CVE-2026-67321 / GHSA-hcpx-6fm6-wx23 | 1.15.1 – 1.18.0 | 1.15.1 | 1.15.0 < 1.15.1 |
| disc2_d63fd9203ce22a009a2824b4 | CVE-2026-101909 / GHSA-x97p-jq2g-jp4f | 1.15.1 – 1.20.0 | 1.15.1 | 1.15.0 < 1.15.1 |
| disc2_4e286cfc1b4b6ae7d8b8b6ed | CVE-2026-101903 / GHSA-c29m-xwm3-cm6r | 1.16.1 – 1.20.0 | 1.16.1 | 1.15.0 < 1.16.1 |
| disc2_d1fb544edeb4d965f4efbdd9 | CVE-2026-101907 / GHSA-r4gj-5m52-g5wh | 1.17.0 – 1.20.0 | 1.17.0 | 1.15.0 < 1.17.0 |
| disc2_7962c9f9f8ed5d71999a8782 | CVE-2026-101905 / GHSA-m8m8-qj5v-23w3 | 1.15.2 – 1.20.0 | 1.15.2 | 1.15.0 < 1.15.2 |
| adv3_19d3fe4ddda13814 | CVE-2026-68943 / GHSA-xj6q-8x83-jv6g | 1.15.2 – 1.18.0 | 1.15.2 | same advisory as CVE-2026-67314; 1.15.0 < 1.15.2 |
| adv3_729c2617e5ff257a | CVE-2026-69124 / GHSA-gcfj-64vw-6mp9 | 1.15.2 – 1.18.0 | 1.15.2 | same advisory as CVE-2026-67320; 1.15.0 < 1.15.2 |
| adv3_468866e1d6a6671b | CVE-2026-69125 / GHSA-hcpx-6fm6-wx23 | 1.15.1 – 1.18.0 | 1.15.1 | same advisory as CVE-2026-67321; 1.15.0 < 1.15.1 |

## What this report does not decide

- It does not reject any advisory whose range contains 1.15.0, including
  CVE-2026-42033 through 42044, 44486–44496, 67312/67313/67315–67319,
  101898/101900–101902/101904/101906/101908, and the 68941–69123 family.
- It makes no code-level claim about any of the rejected candidates; the exclusion
  is purely the published semver range versus the exact snapshot version. A code
  check could only narrow an affected range, never widen it beyond the advisory.
- It does not touch the duplicate-advisory decisions (CVE-2026-44487 and the
  `adv3_*`/`disc2_*` pairs) beyond the three rows listed above.

## Applying the decision

The status is carried by `runs/verification/candidate_dossiers.jsonl`, from which
`scripts/build_formal_tables.py` restores candidate triage state. For each row
above the `triage_status` becomes `rejected` and the blocker text records the
range and this report. No row is deleted. `data/candidates.jsonl` must not be
edited by hand.
