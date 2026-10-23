# Jenkins candidates outside snapshot 2.441 — not applicable

Snapshot: jenkinsci/jenkins 2.441, snapshot_id `snap_2210581e6ea448e2` (repository 1103607).
Decision date: 2026-10-22.

Basis: the Maven `org.jenkins-ci.main:jenkins-core` ranges recorded in
`runs/verification/candidate_dossiers.jsonl` (sourced from the OSV responses in
`runs/discovery_v2/`), compared with the exact snapshot version 2.441. No code was executed.

## Rule

A version V is affected by an OSV interval `{introduced: I, fixed: F}` when `I <= V < F`.
The snapshot is affected only if at least one interval contains 2.441. A candidate is not
applicable when every interval has `F <= 2.441` (the fix is already in the snapshot) or
`I > 2.441` (the flaw was introduced after the snapshot). Ranges without Maven
`jenkins-core` intervals were not classified.

## Fixed at or before 2.441 (171)

| Candidate | CVE | jenkins-core intervals | Why not affected |
|---|---|---|---|
| disc2_48781bf9be26a3718c742f12 | CVE-2020-2099 | 0..2.204.2, 2.205..2.214 | The snapshot already contains the fix. |
| disc2_d4823fc3a439456ae7814f0a | CVE-2020-2100 | 0..2.204.2, 2.205..2.219 | The snapshot already contains the fix. |
| disc2_cbc7677c6421e4e2958d353b | CVE-2020-2101 | 0..2.204.2, 2.205..2.219 | The snapshot already contains the fix. |
| disc2_d7880985716b1cf2c337da75 | CVE-2020-2102 | 0..2.204.2, 2.205..2.219 | The snapshot already contains the fix. |
| disc2_e48b644619a5da3a89a3f24c | CVE-2020-2103 | 2.205..2.219, 0..2.204.2 | The snapshot already contains the fix. |
| disc2_8c412909c89e8d189f0d9c43 | CVE-2020-2104 | 0..2.204.2, 2.205..2.219 | The snapshot already contains the fix. |
| disc2_516d743c6f913249f4975f66 | CVE-2020-2105 | 0..2.204.2, 2.205..2.219 | The snapshot already contains the fix. |
| disc2_463507504f63d12fc6507d80 | CVE-2020-2160 | 0..2.204.6, 2.205..2.228 | The snapshot already contains the fix. |
| disc2_17be74183c864fc098211162 | CVE-2020-2162 | 0..2.228, 2.204.6..2.228 | The snapshot already contains the fix. |
| disc2_f073c840c991187c28224416 | CVE-2020-2220 | 0..2.235.2, 2.236..2.245 | The snapshot already contains the fix. |
| disc2_29a09d80806fa82f7ff757a0 | CVE-2020-2221 | 0..2.235.2, 2.236..2.245 | The snapshot already contains the fix. |
| disc2_c3bb52aba27f059cb894e231 | CVE-2020-2222 | 0..2.235.2, 2.236..2.245 | The snapshot already contains the fix. |
| disc2_60d4940883926d66a54ccf49 | CVE-2020-2223 | 0..2.235.2, 2.236..2.245 | The snapshot already contains the fix. |
| disc2_34b826c5fbd54e6858427911 | CVE-2020-2229 | 0..2.235.4, 2.236..2.252 | The snapshot already contains the fix. |
| disc2_bbc95e49b352540415cacb42 | CVE-2020-2230 | 0..2.235.4, 2.236..2.252 | The snapshot already contains the fix. |
| disc2_bee170d258c61f8b988c8575 | CVE-2020-2231 | 0..2.235.4, 2.237..2.252 | The snapshot already contains the fix. |
| disc2_8f99aaf1024a04d4be19b56c | CVE-2021-21602 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_5c7b1929eaf0e2badfe74239 | CVE-2021-21603 | 0..2.275, 2.263.2..2.275 | The snapshot already contains the fix. |
| disc2_c15ffde29dd84cf8d8b7a406 | CVE-2021-21604 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_16770f02849141cff2e62301 | CVE-2021-21605 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_c1148004a1c49e2d9355e9ea | CVE-2021-21606 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_effebd22a8bee875b4c92273 | CVE-2021-21607 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_b7e227c612b5fddbdb4a01ce | CVE-2021-21608 | 0..2.275, 2.263.2..2.275 | The snapshot already contains the fix. |
| disc2_dad6881768e2f3c8594ec17f | CVE-2021-21609 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_c38ef231e003ae8b236cb751 | CVE-2021-21610 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_cac73c4c055b914c0f8077eb | CVE-2021-21611 | 0..2.263.2, 2.264..2.275 | The snapshot already contains the fix. |
| disc2_49891234647b8253ab9f6cc6 | CVE-2021-21639 | 0..2.277.2, 2.278..2.287 | The snapshot already contains the fix. |
| disc2_fdcec44380b46099a62c42d2 | CVE-2021-21640 | 0..2.277.2, 2.278..2.287 | The snapshot already contains the fix. |
| disc2_629c886d7db161993144149e | CVE-2021-21670 | 0..2.289.2, 2.292..2.300 | The snapshot already contains the fix. |
| disc2_ffab4ff27e07fc112e8fc08d | CVE-2021-21671 | 2.292..2.300, 0..2.289.2 | The snapshot already contains the fix. |
| disc2_f1da156bc0d299c2ead4159c | CVE-2021-21682 | 2.304..2.315, 0..2.303.2 | The snapshot already contains the fix. |
| disc2_7071ef5d39edff6dcc11d04b | CVE-2021-21683 | 0..2.303.2, 2.304..2.315 | The snapshot already contains the fix. |
| disc2_38945c25b52a2fb11213fc3e | CVE-2021-21685 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_52734cfc2b663239ec0bcd85 | CVE-2021-21686 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_ef79fe68969fa4662430e819 | CVE-2021-21688 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_33bcf9b778a9ad5788be786e | CVE-2021-21689 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_99843a134af25ebb50708314 | CVE-2021-21690 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_627c866cdfdbaab87e4cf988 | CVE-2021-21691 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_77e30a0aca1657412b71af9f | CVE-2021-21692 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_cc1bad2cc8b1a6d2e32cc4a3 | CVE-2021-21693 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_83ce1dfde203dcf54752f0ad | CVE-2021-21694 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_104f5884dd4f7efc1abf4a2f | CVE-2021-21695 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_824d6985f99763753604487a | CVE-2021-21696 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_07315c4adc3b45e2c242f5f2 | CVE-2021-21697 | 0..2.303.3, 2.304..2.319 | The snapshot already contains the fix. |
| disc2_45ad9380a0ea1049e402a556 | CVE-2022-0538 | 2.320..2.334, 0..2.319.3 | The snapshot already contains the fix. |
| disc2_7c9beefb3cfb4396170ca734 | CVE-2022-20612 | 2.320..2.330, 0..2.319.2 | The snapshot already contains the fix. |
| disc2_8b5c970a6cdbd509f4bb24ec | CVE-2022-34170 | 2.350..2.356, 2.320..2.332.4, 2.346..2.346.1 | The snapshot already contains the fix. |
| disc2_7be9105f899de0e835d5cbe4 | CVE-2022-34174 | 2.334..2.356, 0..2.332.4 | The snapshot already contains the fix. |
| disc2_9cde54efb128f6c0f080bfba | CVE-2022-34175 | 2.335..2.356 | The snapshot already contains the fix. |
| disc2_eef8c95a2bbae5d9d6498d5d | CVE-2022-41224 | 2.367..2.370 | The snapshot already contains the fix. |
| disc2_d425aa02c9b8243488f968cc | CVE-2023-27898 | 2.376..2.394, 0..2.375.4 | The snapshot already contains the fix. |
| disc2_44b66c5580f7f36f385198fb | CVE-2023-27899 | 2.376..2.387.1, 0..2.375.4, 2.388..2.394 | The snapshot already contains the fix. |
| disc2_0e9fbc4552c704d6ce789236 | CVE-2023-27900 | 2.388..2.394, 0..2.375.4, 2.376..2.387.1 | The snapshot already contains the fix. |
| disc2_b733542a8e065fe91d07dbf5 | CVE-2023-27901 | 2.388..2.394, 0..2.375.4, 2.376..2.387.1 | The snapshot already contains the fix. |
| disc2_ee0239c001964771ca148e9f | CVE-2023-27902 | 2.376..2.387.1, 0..2.375.4, 2.388..2.394 | The snapshot already contains the fix. |
| disc2_4f92e31ccbf80642e960ec43 | CVE-2023-27903 | 2.376..2.387.1, 0..2.375.4, 2.388..2.394 | The snapshot already contains the fix. |
| disc2_6cfac3907cb5ed9c868d7612 | CVE-2023-27904 | 2.376..2.387.1, 0..2.375.4, 2.388..2.394 | The snapshot already contains the fix. |
| disc2_2bd57e3c0794bc19bcbe6cb1 | CVE-2023-39151 | 2.402..2.414.1, 0..2.401.3, 2.415..2.416 | The snapshot already contains the fix. |
| disc2_b7917d948d9a6542c30ca9b0 | CVE-2023-43494 | 2.50..2.414.2, 2.415..2.424 | The snapshot already contains the fix. |
| disc2_0f6d5d587c1a4efaa699e6fc | CVE-2023-43496 | 2.50..2.414.2, 2.415..2.424 | The snapshot already contains the fix. |
| disc2_e8e7756cb48588f8a1f298d0 | CVE-2013-0158 | 1.481..1.498, 0..1.480.2 | The snapshot already contains the fix. |
| disc2_834154f08de71cd06c816354 | CVE-2013-7330 | 1.481..1.502, 0..1.480.3 | The snapshot already contains the fix. |
| disc2_dc390222038b5243df0ce82e | CVE-2014-2058 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_e0a9ff304ecfdd83cc9f9f1a | CVE-2014-2059 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_20fc569505883e7e49b224f6 | CVE-2014-2061 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_1bf953c8f10788f935eb19ac | CVE-2014-2062 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_660a4ebf57a083a4915a7688 | CVE-2014-2063 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_da78c6a3aa1a001917abd1ac | CVE-2014-2064 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_edbedfd640688105cb8911cd | CVE-2014-2065 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_c2288536b013505bbc37f327 | CVE-2014-2066 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_8bbea8d992f563ee75c6fbce | CVE-2014-2067 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_f0df0228cb3f3729382010f7 | CVE-2014-2068 | 1.533..1.551, 0..1.532.2 | The snapshot already contains the fix. |
| disc2_a3ee97b4e3dc86cb1d074df2 | CVE-2014-3666 | 1.566..1.583, 0..1.565.3 | The snapshot already contains the fix. |
| disc2_5182354767b2eff6aa55259f | CVE-2014-3667 | 1.566..1.583, 0..1.565.3 | The snapshot already contains the fix. |
| disc2_135216b43067568bb01247ff | CVE-2014-9634 | 0..1.586 | The snapshot already contains the fix. |
| disc2_6c05db23c0fec51ba61632e3 | CVE-2014-9635 | 0..1.586 | The snapshot already contains the fix. |
| disc2_0453c3695767fcaa288f4e14 | CVE-2015-1812 | 0..1.596.2, 1.600..1.606 | The snapshot already contains the fix. |
| disc2_cc029344ba03637e72bcc6d8 | CVE-2015-1813 | 1.597..1.606, 0..1.596.2 | The snapshot already contains the fix. |
| disc2_18ffbfe3f2e24222a7ae4a8a | CVE-2015-1814 | 1.597..1.606, 0..1.596.2 | The snapshot already contains the fix. |
| disc2_0ad2f4b6e3f385f1b8cd5b8a | CVE-2015-5317 | 0..1.625.2, 1.626..1.638 | The snapshot already contains the fix. |
| disc2_2b2e88991f8cadc43219ddb6 | CVE-2015-5318 | 0..1.625.2, 1.626..1.638 | The snapshot already contains the fix. |
| disc2_ae6b424f83e790588568d211 | CVE-2015-5319 | 1.626..1.638, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_ff6618256bb95dfb8be815a1 | CVE-2015-5321 | 1.626..1.638, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_47cfc5224d66809b520202be | CVE-2015-5322 | 1.626..1.638, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_83b2bd2111e9103d6da1c789 | CVE-2015-5323 | 0..1.625.2, 1.626..1.638 | The snapshot already contains the fix. |
| disc2_a739748b43c57d5785126cbe | CVE-2015-5324 | 1.626..1.638, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_69ab7ecd4d5df2a56bd2b4c0 | CVE-2015-5325 | 0..1.625.2, 1.626..1.638 | The snapshot already contains the fix. |
| disc2_481b6a7f31e7d82623b84222 | CVE-2015-5326 | 0..1.625.2, 1.626..1.638 | The snapshot already contains the fix. |
| disc2_5527ed2d92ced7ea5c4c9804 | CVE-2015-7536 | 1.626..1.640, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_9170f02aa6a4332af47e3318 | CVE-2015-7537 | 1.626..1.640, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_68d62ed2869c4edd34c44b38 | CVE-2015-7538 | 1.626..1.640, 0..1.625.2 | The snapshot already contains the fix. |
| disc2_765503c29d4a19153f92aae0 | CVE-2015-7539 | 0..1.625.2, 1.626..1.640 | The snapshot already contains the fix. |
| disc2_59e4e6dd6429e70817dd6a40 | CVE-2016-0788 | 1.643..1.650, 0..1.642.2 | The snapshot already contains the fix. |
| disc2_1dc7caa322f1e608ff7e51d1 | CVE-2016-0789 | 1.643..1.650, 0..1.642.2 | The snapshot already contains the fix. |
| disc2_3bbaa6502e90d2d56d7eece3 | CVE-2016-0792 | 1.643..1.650, 0..1.642.2 | The snapshot already contains the fix. |
| disc2_8a79e19bd111877ceb5364a6 | CVE-2016-3726 | 1.652..2.3, 0..1.651.2 | The snapshot already contains the fix. |
| disc2_fa1f598afbcda10c2a7f3dae | CVE-2016-3727 | 1.652..2.3, 0..1.651.2 | The snapshot already contains the fix. |
| disc2_6fcc4edf2a1ef93e732930c4 | CVE-2016-9299 | 2.20..2.32, 0..2.19.3 | The snapshot already contains the fix. |
| disc2_edd2a4c003c656830dacc043 | CVE-2017-1000353 | 2.50..2.57, 0..2.46.2 | The snapshot already contains the fix. |
| disc2_c512fe9a169d89657251bfe9 | CVE-2017-1000354 | 2.50..2.57, 0..2.46.2 | The snapshot already contains the fix. |
| disc2_e9a4769d06e635950ba14de0 | CVE-2017-1000355 | 2.50..2.57, 0..2.46.2 | The snapshot already contains the fix. |
| disc2_4d53e48f6e710d3991f70df4 | CVE-2017-1000356 | 2.50..2.57, 0..2.46.2 | The snapshot already contains the fix. |
| disc2_631f0c2c47e22df7c0fe1702 | CVE-2017-1000362 | 1.498..2.32.2, 2.40..2.44 | The snapshot already contains the fix. |
| disc2_3bea57fe417164f087ed3159 | CVE-2017-1000391 | 0..2.73.3, 2.74..2.89 | The snapshot already contains the fix. |
| disc2_cf48d3831c312200c787332f | CVE-2017-1000392 | 0..2.73.3, 2.74..2.89 | The snapshot already contains the fix. |
| disc2_9c3694133a78e1c825e01d5d | CVE-2017-1000393 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_224f7c8666d2d4ee4d74dbad | CVE-2017-1000394 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_bf52206f30bfaa6c16675eed | CVE-2017-1000395 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_61a32ac80704b64ea57e31da | CVE-2017-1000396 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_5b3888e60b31c6507fed343b | CVE-2017-1000398 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_ea9cbbb0515bb2ac16a33ae0 | CVE-2017-1000399 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_d83181db199a82bf03570dff | CVE-2017-1000400 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_e3bcc78543b4182396525e52 | CVE-2017-1000401 | 0..2.73.2, 2.74..2.84 | The snapshot already contains the fix. |
| disc2_4c0914b31e0e73a569471be4 | CVE-2017-1000503 | 2.81..2.89.2, 2.90..2.95 | The snapshot already contains the fix. |
| disc2_7134c837d9313096d7e8fce5 | CVE-2017-1000504 | 2.81..2.89.2, 2.90..2.95 | The snapshot already contains the fix. |
| disc2_8e9097e2dbe7c54cee4a431d | CVE-2017-2598 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_3b7c5a2f06ef47d9b8ef8ae3 | CVE-2017-2599 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_7a731ba9366cb420c9e05a97 | CVE-2017-2600 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_e188b37d5c2f6a3d89ce3a2a | CVE-2017-2601 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_2474c419fc9d5073b2038ba1 | CVE-2017-2602 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_fbb86d0efe06904979069f50 | CVE-2017-2603 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_ff3f4638eefd917214580547 | CVE-2017-2604 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_217ab0c1b62b13917d43cd72 | CVE-2017-2606 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_10b124652162425c1ede37dc | CVE-2017-2608 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_3b47441e58ddfd24dc99fae2 | CVE-2017-2609 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_be909024e68f8cd098a9a449 | CVE-2017-2610 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_fd6d6e3aefe292834762f118 | CVE-2017-2611 | 0..2.44 | The snapshot already contains the fix. |
| disc2_cd73fe747b16488a29b5eb12 | CVE-2017-2612 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_e53f7a417e3c5e7d6fab251d | CVE-2017-2613 | 0..2.32.2, 2.34..2.44 | The snapshot already contains the fix. |
| disc2_617d2994a5ff9a40c585b827 | CVE-2018-1000067 | 0..2.89.4, 2.90..2.107 | The snapshot already contains the fix. |
| disc2_a529a70f7aa239ff679961ac | CVE-2018-1000068 | 0..2.89.4, 2.90..2.107 | The snapshot already contains the fix. |
| disc2_33ec9c21b8498005c561d8be | CVE-2018-1000169 | 0..2.107.2, 2.108..2.116 | The snapshot already contains the fix. |
| disc2_21f537f08c3332d23aab87bb | CVE-2018-1000170 | 2.108..2.116, 0..2.107.2 | The snapshot already contains the fix. |
| disc2_5ca113ce9790c7c31b2558ee | CVE-2018-1000192 | 0..2.107.3, 2.108..2.121 | The snapshot already contains the fix. |
| disc2_f2d72f656b1e8bffe78b5297 | CVE-2018-1000193 | 0..2.107.3, 2.108..2.121 | The snapshot already contains the fix. |
| disc2_5fb8c635a904f04fd696e0b4 | CVE-2018-1000194 | 0..2.107.3, 2.108..2.121 | The snapshot already contains the fix. |
| disc2_038dc1f503b150c434b008c5 | CVE-2018-1000195 | 0..2.107.3, 2.108..2.121 | The snapshot already contains the fix. |
| disc2_174a303b7d3efe5ab8e89dbc | CVE-2018-1000406 | 0..2.138.2, 2.140..2.146 | The snapshot already contains the fix. |
| disc2_4b1cdfc95449dee287315d70 | CVE-2018-1000407 | 0..2.138.2, 2.140..2.146 | The snapshot already contains the fix. |
| disc2_4532ddb25e6bc17a5959f7eb | CVE-2018-1000408 | 0..2.138.2, 2.140..2.146 | The snapshot already contains the fix. |
| disc2_b5df715c6c87e4a6e9f7c94c | CVE-2018-1000409 | 0..2.138.2, 2.140..2.146 | The snapshot already contains the fix. |
| disc2_e045f00a1d627b5e73440d82 | CVE-2018-1000410 | 0..2.138.2, 2.140..2.146 | The snapshot already contains the fix. |
| disc2_cd552baf7e210c0e00574ca2 | CVE-2018-1000861 | 0..2.138.4, 2.140..2.154 | The snapshot already contains the fix. |
| disc2_d9c79c5b9ef35530105c9275 | CVE-2018-1000862 | 0..2.138.4, 2.140..2.154 | The snapshot already contains the fix. |
| disc2_7ef22faf7c563ff16b3b763d | CVE-2018-1000863 | 0..2.138.4, 2.140..2.154 | The snapshot already contains the fix. |
| disc2_7cfa248466c16661f5667444 | CVE-2018-1000864 | 0..2.138.4, 2.140..2.154 | The snapshot already contains the fix. |
| disc2_079bc0d5667eb205568e5993 | CVE-2018-1000997 | 0..2.138.2, 2.140..2.146 | The snapshot already contains the fix. |
| disc2_00a1a94905cf52382dbc2add | CVE-2018-1999001 | 0..2.121.2, 2.122..2.132 | The snapshot already contains the fix. |
| disc2_d6f4bd1f06fe2686b34ccdf7 | CVE-2018-1999002 | 0..2.121.2, 2.122..2.132 | The snapshot already contains the fix. |
| disc2_139cde0c5eba8d086aeb10dc | CVE-2018-1999003 | 0..2.121.2, 2.122..2.133 | The snapshot already contains the fix. |
| disc2_5b0ef7cd3c2942364715d4b6 | CVE-2018-1999004 | 0..2.121.2, 2.122..2.132 | The snapshot already contains the fix. |
| disc2_e456ce4d3328d1b7e0b7c0b3 | CVE-2018-1999005 | 0..2.121.2, 2.122..2.132 | The snapshot already contains the fix. |
| disc2_7904a71efa2a85d6ccc2bf6d | CVE-2018-1999006 | 0..2.121.2, 2.122..2.132 | The snapshot already contains the fix. |
| disc2_3590b931679193a302ca84f1 | CVE-2018-1999042 | 0..2.121.3, 2.122..2.138 | The snapshot already contains the fix. |
| disc2_3600de1b01df6a00024c3428 | CVE-2018-1999044 | 0..2.138 | The snapshot already contains the fix. |
| disc2_d137ef90dd3a80e1d12d4089 | CVE-2018-1999045 | 0..2.121.3, 2.122..2.138 | The snapshot already contains the fix. |
| disc2_510ccb68b18d3acdb1d9a0c0 | CVE-2018-1999046 | 0..2.121.3, 2.122..2.138 | The snapshot already contains the fix. |
| disc2_b0a917335a37415535144ce9 | CVE-2018-6356 | 0..2.89.4, 2.90..2.107 | The snapshot already contains the fix. |
| disc2_2f6ec584db68984b465434f5 | CVE-2019-1003003 | 0..2.150.2, 2.151..2.159 | The snapshot already contains the fix. |
| disc2_51397aeb17bf7203a38964fa | CVE-2019-1003049 | 0..2.164.2, 2.165..2.172 | The snapshot already contains the fix. |
| disc2_0d3852325a992ad6b8252c6f | CVE-2019-1003050 | 0..2.164.2, 2.165..2.172 | The snapshot already contains the fix. |
| disc2_53dad47ecbe3e3832ee5a748 | CVE-2019-10352 | 0..2.176.2, 2.177..2.186 | The snapshot already contains the fix. |
| disc2_4a475b2ecc0079f5e1a0973d | CVE-2019-10353 | 0..2.176.2, 2.177..2.186 | The snapshot already contains the fix. |
| disc2_7b5698f1f3d8529d0ce63599 | CVE-2019-10354 | 0..2.176.2, 2.177..2.186 | The snapshot already contains the fix. |
| disc2_4ce4fc57147487dada7590db | CVE-2019-10383 | 0..2.176.3, 2.177..2.192 | The snapshot already contains the fix. |
| disc2_8017faabcff2c5b25dc74016 | CVE-2019-10384 | 0..2.176.3, 2.177..2.192 | The snapshot already contains the fix. |
| disc2_013d1735dff935c05b9a3286 | CVE-2019-10401 | 0..2.176.4, 2.177..2.197 | The snapshot already contains the fix. |
| disc2_6cd6ce27c55de7bbc2264914 | CVE-2019-10402 | 0..2.176.4, 2.177..2.197 | The snapshot already contains the fix. |
| disc2_d6cbf372ac7a272b81cb2ffc | CVE-2019-10404 | 0..2.176.4, 2.177..2.197 | The snapshot already contains the fix. |
| disc2_19800b5443453a8844fd8e9d | CVE-2019-10405 | 0..2.176.4, 2.177..2.197 | The snapshot already contains the fix. |
| disc2_b7c49913b519ebdccf13ab91 | CVE-2019-10406 | 0..2.176.4, 2.177..2.197 | The snapshot already contains the fix. |

## Introduced after 2.441 (3)

| Candidate | CVE | jenkins-core intervals | Why not affected |
|---|---|---|---|
| disc2_ecd62925f9692bd20873a679 | CVE-2026-27099 | 2.542..2.551, 2.483..2.541.2 | The flaw did not exist in the snapshot version. |
| disc2_6dc05135ee727c716d2c9432 | CVE-2026-33002 | 2.442..2.555 | The flaw did not exist in the snapshot version. |
| disc2_57c4b01baa3406edb78bdd44 | CVE-2026-53441 | 2.483..2.568 | The flaw did not exist in the snapshot version. |

## What this report does not decide

- It does not reject the 18 candidates whose intervals contain 2.441
  (CVE-2024-43044, 43045, 2025-31720/31721, 2025-67635–67639, 2026-27100,
  33001, 53435–53440, 53442). They remain `in_validation`.
- It makes no code-level claim; the exclusion is purely the published Maven range
  versus the exact snapshot version.
- `2.441` is a weekly line; LTS ranges such as `2.426.x` are compared by numeric order
  (`2.426 < 2.441`), which is how Jenkins orders weekly and LTS lines for advisory ranges.

## Applying the decision

For each row above, `triage_status` becomes `rejected` and the blocker records the
intervals and this report. No row is deleted; `data/candidates.jsonl` is rebuilt by
`scripts/build_formal_tables.py --tables candidates`.