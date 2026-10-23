# CATALOG_COVERAGE_REPORT — 历史漏洞目录与候选处置

生成时间：2026-10-22T01:55:00Z；范围：截止 2026-10-21 的公开已知漏洞检索（不含 2026-10-22 当日新披露）。

> **2026-10-23 注**：本文件是 2026-10-22 的快照记录，下列计数（73 漏洞 / 1839 证据 / 2626 候选状态等）
> 已被后续验证取代，不再是当前值。当前 live 为 80 snapshots / 78 vulnerabilities / 1951 evidence /
> 60 条 `confirmed_affected`（55 B + 5 A）；候选 triage 为 1577 行 = 71 `confirmed_affected` /
> 303 `confirmed_not_affected` / 1203 `unknown`。phoenix 行（§2）对应已归档的 v1.6.13 快照；
> 当前目标为 v1.8.8（`snap_aca73214a7703174`），该快照 live 正样本 2 条（CVE-2026-56811、
> CVE-2026-56812），§3 的「同一漏洞两条候选」表中 phoenix 另有 CVE-2026-56812 一对
> （`disc2_49ab8b917b7f862af6ea3968`、`adv3_a7fa8aabc9d9faea`）。权威计数见 `HANDOFF_V031.md` §2。

## 1. 汇总

| 指标 | 数值 |
|---|---:|
| 仓库 | 50 |
| Catalog 已提升漏洞 | 73 |
| 根因位置 | 73 |
| 证据行 | 1839（全部 PASS） |
| 复核 | 73（B 级 73，A 级 0） |
| 正式 Oracle 行 | 73（全部 `confirmed_affected`） |
| 候选行 | 2626 |
| `in_validation` | 503 |
| `pending_location` | 750 |
| `pending_version` | 861 |
| `verified` | 83 |
| `rejected` | 429 |
| 未解决（in_validation + pending_location + pending_version） | 2114 |
| `PASS_KNOWN_SWEEP` | 0/50 |
| grade A（动态红绿） | 0 |

迁移没有新增、删除或改写任何候选行：`data/candidates.jsonl` 与 v0.2 源文件字节级一致
（sha256 `396c616de18d3dc8a1d2bca3306a02a3f5312ee36c2d513f01c233c3244bb7be`；见 `MIGRATION_REPORT.json` 的 reconciliation 段）。

## 2. 逐仓库目录与候选

| repo_id | 仓库 | 目录漏洞 | B 级复核 | 候选 | in_validation | pending_location | pending_version | verified | rejected | 未解决 | 覆盖面 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 6181245 | aaubry/YamlDotNet | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | NEEDS_REVIEW |
| 105379569 | actix/actix-web | 0 | 0 | 9 | 1 | 5 | 3 | 0 | 0 | 9 | NEEDS_REVIEW |
| 24195339 | angular/angular | 0 | 0 | 40 | 24 | 13 | 3 | 0 | 0 | 40 | NEEDS_REVIEW |
| 2493904 | apache/tomcat | 0 | 0 | 41 | 35 | 6 | 0 | 0 | 0 | 41 | NEEDS_REVIEW |
| 23088740 | axios/axios | 0 | 0 | 67 | 18 | 19 | 12 | 0 | 18 | 49 | NEEDS_REVIEW |
| 29207621 | caddyserver/caddy | 0 | 0 | 37 | 7 | 12 | 18 | 0 | 0 | 37 | NEEDS_REVIEW |
| 569041 | curl/curl | 2 | 2 | 387 | 0 | 27 | 357 | 2 | 1 | 384 | NEEDS_REVIEW |
| 54280778 | DaveGamble/cJSON | 1 | 1 | 52 | 0 | 13 | 37 | 2 | 0 | 50 | NEEDS_REVIEW |
| 4164482 | django/django | 8 | 8 | 163 | 4 | 23 | 13 | 8 | 115 | 40 | NEEDS_REVIEW |
| 17620347 | dotnet/aspnetcore | 0 | 0 | 68 | 0 | 26 | 42 | 0 | 0 | 68 | NEEDS_REVIEW |
| 10649374 | elixir-ecto/ecto | 0 | 0 | 4 | 1 | 0 | 3 | 0 | 0 | 4 | NEEDS_REVIEW |
| 14421569 | elixir-plug/plug | 0 | 0 | 11 | 5 | 2 | 4 | 0 | 0 | 11 | NEEDS_REVIEW |
| 153667429 | elixir-plug/plug_cowboy | 0 | 0 | 2 | 1 | 0 | 1 | 0 | 0 | 2 | NEEDS_REVIEW |
| 237159 | expressjs/express | 1 | 1 | 6 | 0 | 3 | 0 | 1 | 2 | 3 | NEEDS_REVIEW |
| 20904437 | gin-gonic/gin | 1 | 1 | 5 | 1 | 3 | 0 | 1 | 0 | 4 | NEEDS_REVIEW |
| 72495579 | go-gitea/gitea | 0 | 0 | 293 | 68 | 69 | 156 | 0 | 0 | 293 | NEEDS_REVIEW |
| 27729880 | grpc/grpc | 0 | 0 | 8 | 4 | 3 | 1 | 0 | 0 | 8 | NEEDS_REVIEW |
| 1420053 | guzzle/guzzle | 2 | 2 | 17 | 8 | 2 | 3 | 2 | 2 | 13 | NEEDS_REVIEW |
| 23500865 | hyperium/hyper | 1 | 1 | 11 | 2 | 3 | 3 | 2 | 1 | 8 | NEEDS_REVIEW |
| 3476845 | JamesNK/Newtonsoft.Json | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | NEEDS_REVIEW |
| 33100064 | jbeder/yaml-cpp | 0 | 0 | 7 | 0 | 6 | 1 | 0 | 0 | 7 | NEEDS_REVIEW |
| 1103607 | jenkinsci/jenkins | 6 | 6 | 259 | 18 | 61 | 0 | 6 | 174 | 79 | NEEDS_REVIEW |
| 31504491 | labstack/echo | 0 | 0 | 16 | 4 | 0 | 12 | 0 | 0 | 16 | NEEDS_REVIEW |
| 7548986 | laravel/framework | 1 | 1 | 39 | 4 | 21 | 5 | 2 | 7 | 30 | NEEDS_REVIEW |
| 3542607 | leethomason/tinyxml2 | 0 | 0 | 3 | 0 | 1 | 2 | 0 | 0 | 3 | NEEDS_REVIEW |
| 3219804 | libarchive/libarchive | 1 | 1 | 23 | 0 | 21 | 1 | 1 | 0 | 22 | NEEDS_REVIEW |
| 80314213 | libexpat/libexpat | 7 | 7 | 143 | 0 | 94 | 42 | 7 | 0 | 136 | NEEDS_REVIEW |
| 3955647 | lodash/lodash | 0 | 0 | 10 | 7 | 3 | 0 | 0 | 0 | 10 | NEEDS_REVIEW |
| 80945428 | nestjs/nest | 0 | 0 | 12 | 7 | 4 | 1 | 0 | 0 | 12 | NEEDS_REVIEW |
| 1064563 | netty/netty | 6 | 6 | 130 | 24 | 54 | 37 | 7 | 8 | 115 | NEEDS_REVIEW |
| 11171548 | nlohmann/json | 0 | 0 | 3 | 0 | 3 | 0 | 0 | 0 | 3 | NEEDS_REVIEW |
| 133092972 | nodejs/undici | 3 | 3 | 56 | 11 | 14 | 9 | 4 | 18 | 34 | NEEDS_REVIEW |
| 7634677 | openssl/openssl | 0 | 0 | 10 | 0 | 10 | 0 | 0 | 0 | 10 | NEEDS_REVIEW |
| 596892 | pallets/flask | 1 | 1 | 8 | 1 | 1 | 2 | 2 | 2 | 4 | NEEDS_REVIEW |
| 997338 | pallets/werkzeug | 1 | 1 | 25 | 5 | 3 | 9 | 2 | 6 | 17 | NEEDS_REVIEW |
| 16072585 | phoenixframework/phoenix | 2 | 2 | 8 | 1 | 1 | 2 | 3 | 1 | 4 | NEEDS_REVIEW |
| 2253830 | PHPMailer/PHPMailer | 0 | 0 | 18 | 6 | 8 | 4 | 0 | 0 | 18 | NEEDS_REVIEW |
| 23357588 | protocolbuffers/protobuf | 3 | 3 | 14 | 4 | 4 | 2 | 4 | 0 | 10 | NEEDS_REVIEW |
| 11939484 | pyca/cryptography | 0 | 0 | 43 | 17 | 7 | 19 | 0 | 0 | 43 | NEEDS_REVIEW |
| 96071 | rack/rack | 2 | 2 | 50 | 16 | 22 | 0 | 2 | 10 | 38 | NEEDS_REVIEW |
| 8514 | rails/rails | 0 | 0 | 148 | 71 | 67 | 10 | 0 | 0 | 148 | NEEDS_REVIEW |
| 135525225 | ruby/rexml | 0 | 0 | 9 | 6 | 2 | 1 | 0 | 0 | 9 | NEEDS_REVIEW |
| 57920736 | rustls/rustls | 1 | 1 | 13 | 0 | 5 | 5 | 2 | 1 | 10 | NEEDS_REVIEW |
| 106995 | sinatra/sinatra | 0 | 0 | 6 | 4 | 2 | 0 | 0 | 0 | 6 | NEEDS_REVIEW |
| 72174164 | SixLabors/ImageSharp | 0 | 0 | 16 | 12 | 2 | 2 | 0 | 0 | 16 | NEEDS_REVIEW |
| 1148753 | spring-projects/spring-framework | 0 | 0 | 84 | 56 | 28 | 0 | 0 | 0 | 84 | NEEDS_REVIEW |
| 458058 | symfony/symfony | 18 | 18 | 129 | 2 | 29 | 21 | 18 | 59 | 52 | NEEDS_REVIEW |
| 67836789 | tokio-rs/tokio | 0 | 0 | 6 | 0 | 5 | 1 | 0 | 0 | 6 | NEEDS_REVIEW |
| 70107786 | vercel/next.js | 0 | 0 | 86 | 39 | 34 | 13 | 0 | 0 | 86 | NEEDS_REVIEW |
| 257485422 | vitejs/vite | 4 | 4 | 29 | 9 | 8 | 4 | 4 | 4 | 21 | NEEDS_REVIEW |

（`verified` 列可能大于该仓库 Catalog 漏洞数，原因见第 3 节的别名重复行。）

## 3. 83 条 `verified` 候选与 73 条 Catalog 漏洞的差额

73 条 Catalog 漏洞对应 83 条 `verified` 候选，差额 10 条是**同一漏洞的第二个来源行**，不是 10 个新漏洞，
也没有被计入 Catalog：

| 仓库 | vulnerability_id | 两条候选 |
|---|---|---|
| netty (1064563) | GHSA-wm47-8v5p-wjpj / CVE-2021-21295 | `disc2_c9c0e971dae74f19daaafce3`、`adv3_2e851e608cae94c2` |
| undici (133092972) | CVE-2023-23936 | `disc2_d3b2feffe4781aa8b25d2c09`、`adv3_0a525ae00aaeccc5` |
| phoenix (16072585) | CVE-2026-56811 | `disc2_46723370667ed0c5775db602`、`adv3_935719b31ddff77e` |
| protobuf (23357588) | CVE-2022-1941 | `adv3_cbefb3c10f62d8e1`、`disc2_96245f2879891a26a9e6d07d` |
| hyper (23500865) | GHSA-6hfq-h8hq-87mf / CVE-2021-21299 | `adv3_37d21bbdf941b464`、`disc2_1284bdb1ae69ee453abf460d` |
| cJSON (54280778) | CVE-2023-50471 | `disc2_1c7582219f08a34e1dba3691`、`disc2_b52abaab061df58e572164c9` |
| rustls (57920736) | CVE-2024-32650 | `adv3_941597405a14df2a`、`disc2_3e62dc5c211a988034d1490d` |
| flask (596892) | GHSA-m2qf-hxjv-5gpq / CVE-2023-30861 | `adv3_9f37d56ec6221229`、`disc2_c938598b5b9be9c9763d4ca8` |
| laravel (7548986) | CVE-2024-52301 | `disc2_226d0cf8e0273d5cbb8b8500`、`adv3_03ca478536859402` |
| werkzeug (997338) | CVE-2024-34069 | `adv3_35e2b6ab5b47677a`、`disc2_1a837d8fb2fae06cdbdb009c` |

这些行保持 `status=verified`，以保留来源与审计链；`v0.3/scripts/validate_dataset.py` 对“verified without catalog link”
只给 warning，不要求删除。

## 4. 429 条 `rejected` 的处置类别

以下数字来自既有 `runs/verification/*_snapshot_not_applicable/NOT_APPLICABLE.md` 与 `WORK_LOG.md` 的记录，
本轮迁移**没有重新核验每一条**，只确认候选行仍完整保留：

| 类别 | 条数 |
|---|---:|
| Jenkins 2.441 范围外 | 174 |
| Django 3.0.2 全量区间外 | 114 |
| Symfony 5.4.45 范围外 | 57 |
| axios 1.15.0 范围外 | 18 |
| undici 5.19.0 范围外 | 18 |
| vite 5.0.11 范围外 | 4 |
| netty 4.1.59 范围外 | 7 |
| rack 2.2.3 范围外 | 10 |
| 小型仓库合并范围外（8 仓） | 21 |
| 单条范围/状态判定（CVE-2024-51999、50343、50341、2022-41915、2024-0853、2021-35042） | 6 |
| **合计** | **429** |

这些拒绝都是“不在该仓库评测版本的影响范围内”或公告本身 withdrawn/重复，不等于代码审计结论；
逐条理由保存在 `runs/verification/` 的 NOT_APPLICABLE 文件中，迁移后原样保留。

## 5. 未提升但已有独立 verdict 的 20 条

按 `runs/verification/promotion_report.json`：20 条已有 verdict 但至少一个字段未过门槛
（8 条严重程度来源冲突、15 条独立证据不足、1 条 cvss=false；组间有重叠）。
迁移后它们仍是 pending，没有被提升，也没有被删除。

## 6. 已知检索盲区

- **PASS_KNOWN_SWEEP = 0/50**：全部仓库 `outcome=NEEDS_REVIEW`。`discovery_coverage.passes` 每仓 4 轮，
  末两轮 `new_verified_count` 都是 0，机械上接近停止条件，但仍有大量未解释候选，
  且覆盖面未经独立复核，因此不声明 PASS。
- curl 官方公告 CVE-2023-38546（8.3.0 受影响）没有进入候选表：NVD 关键词结果集与 OSV/仓库公告均无记录。
  已记录在 `WORK_LOG.md`，没有手工补行。
- NVD 只对部分仓库做了关键词检索；50 个 GitHub repository advisory 拉取成功，但 14 个返回空列表。
- OSV 导入 GHSA/NVD/生态记录，端点数量不等于独立来源数量。
- 检索截止 2026-10-21（`discovery_coverage.cutoff_date`），不包含 2026-10-22 当日披露。
