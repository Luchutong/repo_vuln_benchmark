# Symfony candidates outside snapshot v5.4.45 — not applicable

Snapshot: symfony/symfony v5.4.45, snapshot_id `snap_39105a8a3ceb9fe4` (repository 458058).
Decision date: 2026-10-22.

Basis: Packagist `symfony/*` OSV ranges recorded in
`runs/verification/candidate_dossiers.jsonl`, compared with 5.4.45. No code was executed.

## Rule

Affected when at least one interval has `introduced <= 5.4.45 < fixed`. Not applicable
when every interval is either already fixed at the snapshot (`fixed <= 5.4.45`) or
entirely on a later branch (`introduced > 5.4.45`). This branch-aware rule is needed for
monorepo advisories that list 5.4, 6.x and 7.x intervals in one record: a 6.x interval
above the snapshot does not make the 5.4 line affected.

| Candidate | CVE | symfony/* intervals | Why not affected |
|---|---|---|---|
| disc2_24101e7b233587fa816ca810 | CVE-2020-15094 | 4.3.0..4.4.13, 5.0.0..5.1.5, 4.3.0..4.4.13, 5.0.0..5.1.5 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d19302ad9c4b9f5791be30b0 | CVE-2020-5255 | 4.4.0..4.4.7, 5.0.0..5.0.7, 4.4.0..4.4.7, 5.0.0..5.0.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_fe65fe8c9ba4f5f80f51b1b9 | CVE-2020-5274 | 4.4.0..4.4.4, 5.0.0..5.0.4, 4.4.0..4.4.4, 5.0.0..5.0.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_8229d754c6a7eaeb65c13016 | CVE-2020-5275 | 4.4.0..4.4.7, 5.0.0..5.0.7, 4.4.0..4.4.7, 5.0.0..5.0.7, 4.4.0..4.4.7, 5.0.0..5.0.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d9d4a36ebe8ed94ce56f668e | CVE-2021-21424 | 5.0.0..5.2.8, 2.8.0..3.4.48, 4.0.0..4.4.23, 5.0.0..5.2.8, 2.8.0..3.4.48, 4.0.0..4.4.23, 5.0.0..5.2.8, 1.27.0..1.29.2, 1.30.0..1.31.1, 5.1.0..5.2.8, 2.8.0..3.4.49, 4.0.0..4.4.24, 2.8.0..3.4.49, 4.0.0..4.4.24, 5.0.0..5.2.9 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_e88c3434857064ed96f936cd | CVE-2021-32693 | 5.3.0..5.3.2, 5.3.0..5.3.2 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_18d751d9ffcd34ac8ffef350 | CVE-2021-41267 | 5.2.0..5.3.12, 5.2.0..5.3.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_b60e58461a62a71651cab79d | CVE-2021-41268 | 5.3.0..5.3.12, 5.3.0..5.3.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_c9912a7042279f5f67831ee8 | CVE-2021-41270 | 5.0.0..5.3.12, 4.1.0..4.4.35, 4.1.0..4.4.35, 5.0.0..5.3.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d828e7d327a74dbe8c6bf06a | CVE-2022-23601 | 5.3.14..5.3.15, 5.4.3..5.4.4, 6.0.3..6.0.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_4bc9270508955d8495113b92 | CVE-2022-24894 | 2.0.0..4.4.50, 5.0.0..5.4.20, 6.0.0..6.0.20, 6.1.0..6.1.12, 6.2.0..6.2.6, 2.0.0..4.4.50, 5.0.0..5.4.20, 6.0.0..6.0.20, 6.1.0..6.1.12, 6.2.0..6.2.6 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_f3875d2db90680e4cc102066 | CVE-2022-24895 | 2.0.0..4.4.50, 5.0.0..5.4.20, 6.0.0..6.0.20, 6.1.0..6.1.12, 6.2.0..6.2.6, 2.0.0..4.4.50, 5.0.0..5.4.20, 6.0.0..6.0.20, 6.1.0..6.1.12, 6.2.0..6.2.6 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_95aadb5204c4ae62e6329d49 | CVE-2023-46733 | 5.4.21..5.4.31, 6.2.7..6.3.8, 5.4.21..5.4.31, 6.2.7..6.3.8 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_19a74bacb69bd305f4d79211 | CVE-2023-46734 | 2.0.0..4.4.51, 5.0.0..5.4.31, 6.0.0..6.3.8, 2.0.0..4.4.51, 5.0.0..5.4.31, 6.0.0..6.3.8 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_b6304e4c4482f1c24ad6969f | CVE-2023-46735 | 6.3.0..6.3.8, 6.3.0..6.3.8 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_dd37f1a40df4b1b6d2f54033 | CVE-2012-6431 | 2.0.0..2.0.19, 2.0.0..2.0.19, 2.0.0..2.0.19, 2.0.0..2.0.19 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d6f13d0b16b5fb2968a9b273 | CVE-2013-1348 | 2.0.0..2.0.22, 2.0.0..2.0.22 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_1adfd88b535a3eebb4e51353 | CVE-2013-1397 | 2.2.0-BETA1..2.2.0-BETA2, 2.0.0..2.0.22, 2.1.0..2.1.7, 2.0.0..2.0.22, 2.1.0..2.1.7, 2.2.0-BETA1..2.2.0-BETA2 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_c6ca68d492b3afd30b2bdb39 | CVE-2014-4931 | 2.0.0..2.3.18, 2.4.0..2.4.8, 2.5.0..2.5.2, 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_efc41484ed47dfae43434bf0 | CVE-2014-5244 | 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4, 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_56d54e73af9027fc9fb10481 | CVE-2014-5245 | 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4, 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_3b51871bcc58b338ddb12697 | CVE-2014-6061 | 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4, 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_aed4de6407fca732acf51b76 | CVE-2014-6072 | 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4, 2.0.0..2.3.19, 2.4.0..2.4.9, 2.5.0..2.5.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_890ac8f2b6f9233119600239 | CVE-2015-2309 | 2.0.0..2.3.27, 2.4.0..2.5.11, 2.6.0..2.6.6, 2.0.0..2.3.27, 2.4.0..2.5.11, 2.6.0..2.6.6 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_b7bad16f2b1b38ca4a820f9c | CVE-2017-11365 | 2.7.30..2.7.32, 2.8.23..2.8.25, 3.2.10..3.2.12, 3.3.3..3.3.5, 2.7.30..2.7.32, 2.8.23..2.8.25, 3.2.10..3.2.12, 3.3.3..3.3.5, 2.7.30..2.7.32, 2.8.23..2.8.25, 3.2.10..3.2.12, 3.3.3..3.3.5 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_98ae1dcd3d1b66db82964100 | CVE-2017-16653 | 2.7.0..2.7.38, 2.8.0..2.8.31, 3.0.0..3.2.14, 3.3.0..3.3.13, 2.7.0..2.7.38, 2.8.0..2.8.31, 3.0.0..3.2.14, 3.3.0..3.3.13, 2.7.0..2.7.38, 2.8.0..2.8.31, 3.0.0..3.2.14, 3.3.0..3.3.13 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_11ada33b78267189c824e913 | CVE-2018-11385 | 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11, 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11, 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_21ec16c0864ab9e967e3a2eb | CVE-2018-11406 | 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11, 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11, 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11, 2.7.0..2.7.48, 2.8.0..2.8.41, 3.0.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d6824936a690fc1755428812 | CVE-2018-11407 | 2.8.0..2.8.37, 3.0.0..3.3.17, 3.4.0..3.4.7, 4.0.0..4.0.7, 2.8.0..2.8.37, 3.0.0..3.3.17, 3.4.0..3.4.7, 4.0.0..4.0.7, 2.8.0..2.8.37, 3.0.0..3.3.17, 3.4.0..3.4.7, 4.0.0..4.0.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_2ec16ac1d4845f70acb43d41 | CVE-2018-11408 | 2.7.0..2.7.48, 2.8.0..2.8.41, 3.3.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11, 2.7.0..2.7.48, 2.8.0..2.8.41, 3.3.0..3.3.17, 3.4.0..3.4.11, 4.0.0..4.0.11 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_fb26ad6eaf9763ad07f20c58 | CVE-2018-14773 | 2.7.0..2.7.49, 2.8.0..2.8.44, 3.0.0..3.3.18, 3.4.0..3.4.14, 4.0.0..4.0.14, 4.1.0..4.1.3, 2.7.0..2.7.49, 2.8.0..2.8.44, 3.0.0..3.3.18, 3.4.0..3.4.14, 4.0.0..4.0.14, 4.1.0..4.1.3 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_daa29b38bd8a2b5377037ea8 | CVE-2018-14774 | 2.7.0..2.7.49, 2.8.0..2.8.44, 3.3.0..3.3.18, 3.4.0..3.4.14, 4.0.0..4.0.14, 4.1.0..4.1.3 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_dfc2ae04d7c3cc738098e5c0 | CVE-2018-19789 | 2.7.0..2.7.50, 2.8.0..2.8.49, 3.0.0..3.4.20, 4.0.0..4.0.15, 4.1.0..4.1.9, 4.2.0..4.2.1, 2.7.0..2.7.50, 2.8.0..2.8.49, 3.0.0..3.4.20, 4.0.0..4.0.15, 4.1.0..4.1.9, 4.2.0..4.2.1 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_16853c14bc32a33cbeeed948 | CVE-2018-19790 | 2.7.38..2.7.50, 2.8.0..2.8.49, 3.0.0..3.4.20, 4.0.0..4.0.15, 4.1.0..4.1.9, 4.2.0..4.2.1, 2.7.38..2.7.50, 2.8.0..2.8.49, 3.0.0..3.4.19, 4.0.0..4.0.15, 4.1.0..4.1.9, 4.2.0..4.2.1, 2.7.38..2.7.50, 2.8.0..2.8.49, 3.0.0..3.4.20, 4.0.0..4.0.15, 4.1.0..4.1.9 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_a82b7a06ea365572fc852deb | CVE-2019-10909 | 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_5382f84225ce5ee5a4342063 | CVE-2019-10910 | 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_6565e023a737971b482fa281 | CVE-2019-10911 | 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_706d6c102d099b93ede7d58a | CVE-2019-10912 | 3.1.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_283fbd0a98d596ec56e6afee | CVE-2019-10913 | 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7, 2.7.0..2.7.51, 2.8.0..2.8.50, 3.0.0..3.4.26, 4.0.0..4.1.12, 4.2.0..4.2.7 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_cb17180922bf28f46374771c | CVE-2026-45064 | 6.1.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12, 6.1.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_c1573cf9ae22b1d38e6199bf | CVE-2026-45069 | 6.3.0..6.4.40, 7.4.0..7.4.12, 8.0.0..8.0.12, 6.3.0..6.4.40, 7.4.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_5626236223134bf91a3f2c31 | CVE-2026-45072 | 6.4.24..6.4.40, 7.2.9..7.4.12, 8.0.0..8.0.12, 6.4.24..6.4.40, 7.2.9..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_e837dec6163cf0781ccbcc9f | CVE-2026-45074 | 7.1.0..7.4.12, 8.0.0..8.0.12, 7.1.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_5a1f8acd5a304b62119d8e25 | CVE-2026-45075 | 7.4.0..7.4.12, 8.0.0..8.0.12, 7.4.0..7.4.12, 8.0.0..8.0.12, 7.4.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_52dcd6cfd0a2b39bc080354e | CVE-2026-45753 | 6.1.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12, 6.1.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_9e9d4e4d941e1032eb5f2848 | CVE-2026-45754 | 7.1.0..7.4.12, 8.0.0..8.0.12, 6.4.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12, 6.4.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d5bc6deacb7c15c48caa2f37 | CVE-2026-45755 | 7.2.0..7.4.12, 8.0.0..8.0.12, 7.2.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_b6b4513aea452f9dff015f2e | CVE-2026-45756 | 7.3.0..7.4.12, 8.0.0..8.0.12, 7.3.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_786aa6d5a1231ff2a7cfc220 | CVE-2026-47212 | 6.4.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12, 6.4.0..6.4.40, 7.0.0..7.4.12, 8.0.0..8.0.12 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d843b1072de6eb62486038ca | CVE-2026-48747 | 7.2.0..7.4.13, 8.0.0..8.0.13, 7.2.0..7.4.13, 8.0.0..8.0.13 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_04846b2ac758f1671ec84eac | CVE-2026-48760 | 6.1.0..6.4.41, 7.0.0..7.4.13, 8.0.0..8.0.13, 6.1.0..6.4.41, 7.0.0..7.4.13, 8.0.0..8.0.13 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_c89fd48ed00a71689b5b91ba | CVE-2026-48761 | 6.1.0..6.4.41, 7.0.0..7.4.13, 8.0.0..8.0.13, 6.1.0..6.4.41, 7.0.0..7.4.13, 8.0.0..8.0.13 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_590696e4351b7f3c284d7d75 | GHSA-7mx2-7q8p-pgmw | 2.0.0..2.0.6 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_f82de57d8290fe3aa79042fc | GHSA-g2qj-pmxm-9f8f | 5.1.0..5.2.8, 5.1.0..5.2.8 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_d72ecbda6c1a62913b41ea84 | GHSA-hx53-jchx-cr52 | 2.0.0..2.0.19, 2.1.0..2.1.4 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_9045bb178fdbedbe9cd0eb5a | GHSA-mmcv-fvq8-r9x3 | 2.0.0..2.0.11 | every interval fixed at or before 5.4.45, or introduced after it |
| disc2_61cab1ce1c723da2dc0dba16 | GHSA-vfm6-r2gc-pwww | 2.0.0..2.0.19, 2.1.0..2.1.4, 2.0.0..2.0.19, 2.1.0..2.1.4 | every interval fixed at or before 5.4.45, or introduced after it |

## What this report does not decide

- Two candidates have an interval containing 5.4.45 and stay `in_validation`:
  CVE-2024-51736 (`0..5.4.46`, already has a verdict but fails severity_consistent) and
  CVE-2026-24739 (`0..5.4.51`, no dossier yet).
- No code-level claim is made; the exclusion uses published Packagist ranges only.
