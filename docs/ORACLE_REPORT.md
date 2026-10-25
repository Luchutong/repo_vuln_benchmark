# 快照真值报告

正式快照 75 个，其中评测目标 22 个：
snap_0ec1c11542393304 (curl-8_3_0), snap_24c4a191fd049fc3 (v5.19.0), snap_25561773eac9d84f (12.0.3), snap_2e50b228f2432623 (v5.0.11), snap_3166f788b2c56baa (4.19.2), snap_39105a8a3ceb9fe4 (v5.4.45), snap_6bc3f36eb61ef280 (v3.20.1), snap_6e1f42aa46ca4df5 (v11.30.0), snap_735b41cb13177d03 (v0.14.2), snap_8ed1cab47a0b7011 (2.3.1), snap_a47bcab3f2c97e92 (v3.7.7), snap_ab695ba3db678939 (3.0.2), snap_b3a6891886ef2160 (v/0.23.4), snap_b57262de7996e8a2 (3.0.2), snap_bb344e672a0544ef (netty-4.1.59.Final), snap_d33251dac37c334c (R_2_4_4), snap_d4899c7054105aea (v1.5.0), snap_d9525608880dc9e1 (v1.7.16), snap_d9b0ffa82cd068d0 (jenkins-2.441), snap_ee79f4175242bbee (v1.6.13), snap_efe695448113758a (7.4.4), snap_f97687a4e0807cb2 (2.2.3)。
状态矩阵 73 行：{'confirmed_affected': 73}。
没有从候选推断任何快照“不受影响”，也没有生成 `unknown` 行来填充分母。

| 漏洞 | 快照 | 状态 | 证明方法 | 证据数 |
|---|---|---|---|---:|
| CVE-2023-50471 | snap_d9525608880dc9e1 | confirmed_affected | version_range_plus_code | 20 |
| CVE-2023-38545 | snap_0ec1c11542393304 | confirmed_affected | version_range_plus_code | 21 |
| CVE-2023-46218 | snap_0ec1c11542393304 | confirmed_affected | version_range_plus_code | 31 |
| CVE-2020-13254 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 26 |
| CVE-2020-13596 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 26 |
| CVE-2020-24583 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 28 |
| CVE-2020-24584 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 28 |
| CVE-2020-7471 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 22 |
| CVE-2020-9402 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 26 |
| CVE-2021-28658 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 29 |
| CVE-2021-3281 | snap_ab695ba3db678939 | confirmed_affected | version_range_plus_code | 31 |
| GHSA-qw6h-vgh9-j6wx | snap_3166f788b2c56baa | confirmed_affected | version_range_plus_code | 14 |
| GHSA-m2qf-hxjv-5gpq | snap_8ed1cab47a0b7011 | confirmed_affected | version_range_plus_code | 19 |
| GHSA-6vm3-jj99-7229 | snap_d4899c7054105aea | confirmed_affected | version_range_plus_code | 18 |
| GHSA-25mq-v84q-4j7r | snap_efe695448113758a | confirmed_affected | version_range_plus_code | 15 |
| CVE-2022-31091 | snap_efe695448113758a | confirmed_affected | version_range_plus_code | 22 |
| GHSA-6hfq-h8hq-87mf | snap_735b41cb13177d03 | confirmed_affected | version_range_plus_code | 13 |
| CVE-2024-23897 | snap_d9b0ffa82cd068d0 | confirmed_affected | version_range_plus_code | 20 |
| CVE-2024-23898 | snap_d9b0ffa82cd068d0 | confirmed_affected | version_range_plus_code | 19 |
| CVE-2025-27622 | snap_d9b0ffa82cd068d0 | confirmed_affected | version_range_plus_code | 27 |
| CVE-2025-27623 | snap_d9b0ffa82cd068d0 | confirmed_affected | version_range_plus_code | 27 |
| CVE-2025-27624 | snap_d9b0ffa82cd068d0 | confirmed_affected | version_range_plus_code | 26 |
| CVE-2025-27625 | snap_d9b0ffa82cd068d0 | confirmed_affected | version_range_plus_code | 25 |
| CVE-2024-52301 | snap_6e1f42aa46ca4df5 | confirmed_affected | version_range_plus_code | 22 |
| CVE-2025-5915 | snap_a47bcab3f2c97e92 | confirmed_affected | version_range_plus_code | 23 |
| CVE-2022-25235 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 11 |
| CVE-2022-25236 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 27 |
| CVE-2022-25313 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 27 |
| CVE-2022-25314 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 27 |
| CVE-2022-25315 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 27 |
| CVE-2022-40674 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 21 |
| CVE-2022-43680 | snap_d33251dac37c334c | confirmed_affected | version_range_plus_code | 21 |
| GHSA-wm47-8v5p-wjpj | snap_bb344e672a0544ef | confirmed_affected | version_range_plus_code | 13 |
| CVE-2021-37136 | snap_bb344e672a0544ef | confirmed_affected | version_range_plus_code | 19 |
| CVE-2021-37137 | snap_bb344e672a0544ef | confirmed_affected | version_range_plus_code | 23 |
| CVE-2021-43797 | snap_bb344e672a0544ef | confirmed_affected | version_range_plus_code | 24 |
| CVE-2023-34462 | snap_bb344e672a0544ef | confirmed_affected | version_range_plus_code | 31 |
| CVE-2024-29025 | snap_bb344e672a0544ef | confirmed_affected | version_range_plus_code | 26 |
| GHSA-5crp-9r3c-p9vr | snap_25561773eac9d84f | confirmed_affected | version_range_plus_code | 15 |
| CVE-2022-42975 | snap_ee79f4175242bbee | confirmed_affected | version_range_plus_code | 16 |
| CVE-2026-56811 | snap_ee79f4175242bbee | confirmed_affected | version_range_plus_code | 21 |
| CVE-2022-1941 | snap_6bc3f36eb61ef280 | confirmed_affected | version_range_plus_code | 17 |
| CVE-2022-3509 | snap_6bc3f36eb61ef280 | confirmed_affected | version_range_plus_code | 23 |
| CVE-2024-7254 | snap_6bc3f36eb61ef280 | confirmed_affected | version_range_plus_code | 26 |
| GHSA-wq4h-7r42-5hrr | snap_f97687a4e0807cb2 | confirmed_affected | version_range_plus_code | 14 |
| CVE-2025-27610 | snap_f97687a4e0807cb2 | confirmed_affected | version_range_plus_code | 22 |
| CVE-2024-32650 | snap_b3a6891886ef2160 | confirmed_affected | version_range_plus_code | 16 |
| CVE-2024-50340 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 19 |
| CVE-2024-50342 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 21 |
| CVE-2024-50345 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 19 |
| CVE-2024-51996 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 27 |
| CVE-2025-64500 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 29 |
| CVE-2026-45063 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 29 |
| CVE-2026-45065 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 33 |
| CVE-2026-45067 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 30 |
| CVE-2026-45068 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 30 |
| CVE-2026-45071 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 30 |
| CVE-2026-45073 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 30 |
| CVE-2026-45077 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 30 |
| CVE-2026-45133 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 26 |
| CVE-2026-45304 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 32 |
| CVE-2026-45305 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 30 |
| CVE-2026-48489 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 32 |
| CVE-2026-48736 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 32 |
| CVE-2026-48784 | snap_39105a8a3ceb9fe4 | confirmed_affected | version_range_plus_code | 25 |
| CVE-2023-23936 | snap_24c4a191fd049fc3 | confirmed_affected | version_range_plus_code | 16 |
| CVE-2023-24807 | snap_24c4a191fd049fc3 | confirmed_affected | version_range_plus_code | 23 |
| CVE-2023-45143 | snap_24c4a191fd049fc3 | confirmed_affected | version_range_plus_code | 24 |
| GHSA-c24v-8rfc-w8vw | snap_2e50b228f2432623 | confirmed_affected | version_range_plus_code | 13 |
| CVE-2024-31207 | snap_2e50b228f2432623 | confirmed_affected | version_range_plus_code | 23 |
| CVE-2024-45811 | snap_2e50b228f2432623 | confirmed_affected | version_range_plus_code | 25 |
| CVE-2024-45812 | snap_2e50b228f2432623 | confirmed_affected | version_range_plus_code | 25 |
| CVE-2024-34069 | snap_b57262de7996e8a2 | confirmed_affected | version_range_plus_code | 16 |

每个评测快照都是对应漏洞的正式脆弱发行 tag/SHA（npm `4.19.2`/`5.0.11`/`5.19.0`、PyPI `2.3.1`/`3.0.2`/`Django 3.0.2`、RubyGems `2.2.3`、
Go module `v1.5.0`、Packagist `7.4.4`/`11.30.0`/`5.4.45`、NuGet `12.0.3`、Maven `4.1.59.Final`、crates.io `0.14.2`/`0.23.4`、
generic C `R_2_4_4`/`v1.7.16`/`v3.7.7`/`curl-8_3_0`、C++ `v3.20.1`、Hex `1.6.13`、
Maven `2.441`），
版本范围、精确 SHA 源码和修复发行版内容三重一致后用 `version_range_plus_code` 判定。
未执行动态红绿测试，因此这是静态真值，不是运行时可利用性证明。
