# libexpat catalog CVEs confirmed fixed before R_2_6_2

Snapshot: `snap_67132f0363b8bc23` = tag `R_2_6_2` = `fa75b96546c069d17b8f80d91e0f4ef0cde3790d` (2024-03-13).
Checked: 2026-10-23. Source: full bare clone `scratch/libexpat_full_2026-10-23/libexpat.git`,
`git merge-base --is-ancestor <fix> R_2_6_2`.

These are the seven vulnerabilities previously catalogued at the old R_2_4_4 snapshot. Each fix
commit is an ancestor of R_2_6_2, and the fixed release tag predates it, so they are excluded from
the new snapshot. This is exclusion evidence for triage only; it is not a sweep and does not prove
the absence of other vulnerabilities.

| CVE | fixed release | fix commit | ancestor of R_2_6_2 |
|---|---|---|---|
| CVE-2022-25235 | 2.4.5 | 3f0a0cb644438d4d8e3294cd0b1245d0edb0c6c6 | yes |
| CVE-2022-25236 | 2.4.5 | a2fe525e660badd64b6c557c2b1ec26ddc07f6e4 | yes |
| CVE-2022-25313 | 2.4.5 | 9b4ce651b26557f16103c3a366c91934ecd439ab | yes |
| CVE-2022-25314 | 2.4.5 | efcb347440ade24b9f1054671e6bd05e60b4cafd | yes |
| CVE-2022-25315 | 2.4.5 | eb0362808b4f9f1e2345a0cf203b8cc196d776d9 | yes |
| CVE-2022-40674 | 2.4.9 | 4a32da87e931ba54393d465bb77c40b5c33d343b | yes |
| CVE-2022-43680 | 2.5.0 | 5290462a7ea1278a8d5c0d5b2860d4e244f997e4 | yes |

Release tag commits for reference (resolved in the same clone):

- R_2_4_5 = 97a4840578693a346e79302909b67d97492e1880
- R_2_4_9 = d77291a4824d78e697c5dc2b8024fd65ab31e209
- R_2_5_0 = 654d2de0da85662fcc7644a7acd7c2dd2cfb21f0
