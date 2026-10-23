# HANDOFF_V031 — 下一对话交接文档

> 面向全新对话（无本会话记忆）。读完本文件即可接续。数据集根目录：`/home/luchitong/work/repo-vuln-50-v031`。

## 0. 一句话现状

RepoVuln-50 是 50 个上游开源仓库的漏洞审计评测基准，目标「一库一冻结 commit」。当前是 **v0.3.1 draft**：
已完成「无损迁移 + 低成本相关性筛选 + 独立选版审查 + 证据先行选版」，**26/50 仓库有评测目标，其中 23 个已 frozen、
1 个待独立选版审查（echo v4.15.2 于 2026-10-23 通过独立漏洞复核 grade A 并 promote；axios v1.19.0 已达
独立选版 accept 并 frozen）、2 个仍为 rejected（hyper、Newtonsoft.Json 的 legacy `documented_exception` 目标）**；protobuf v3.25.4 与
sinatra v4.0.1 已 frozen。**55 条评测目标上的已确认正样本（44 B + 11 A）**，另有 29 条历史快照样本（全 B）
保留为证据；2626 条候选已产出 1666 条相关性 triage。**未完成 24 库选版、未完成深验证、未达发布门槛**。
本会话没有伪造真值，也没有把成功率和完成度标到实际未达成的水平。

### 0.1 两个证据先行升级的当前状态（2026-10-23）

两个目标都已完成「独立验证 → promote → 迁移快照 → 导出 → 审计导出 → 选版审查包 → 独立选版 accept → frozen」。

- **netty**：旧目标 `snap_bb344e672a0544ef`（4.1.59.Final）超出 4 年规则，升级到
  `netty-4.1.137.Final` = `5471f0a6ffa4ab39db22c468c6c851af4ecae709`（2026-08-06，注释 tag），
  新快照 `snap_5c3900a03253c043`（3479 文件，tree `146e08ab…`）。正样本 CVE-2026-93494 /
  GHSA-ghg5-c4jg-8q5j（StompSubframeDecoder 的 `lastContent` 在 replay 信号下不可达
  `catch (Exception)`，且无 `handlerRemoved0`，pooled ByteBuf 泄漏；4.1.138 修复 commit
  `cb84b06388`）。独立 verdict：`confirmed_affected`，**B**，reviewer
  `independent-reviewer-netty-CVE-2026-93494-r1`（`runs/independent/netty_CVE-2026-93494_v41137_round1/`）。
  已 promote（1 vuln / 1 location / 1 review / 22 evidence / 1 status）；旧目标 6 个正样本经
  `git merge-base --is-ancestor` 判定修复已在快照内，全部改判 `confirmed_not_affected`，旧行归档到
  `data/legacy_*_snap_bb344e672a0544ef.jsonl`（vulnerabilities/locations/reviews/evidence 保持 live，
  与 django/rack/libexpat/phoenix 先例一致）。导出 archive sha256 `089a09be…`，审计导出剩余 advisory 0、
  redacted 1。选版审查包 `v031/reviews/selection_packets/1064563_netty__netty.json`；本机已补齐用户态
  JDK 17 + Maven 3.9.16 并在全新解包目录跑通 `mvn -B -DskipTests … package`（47/47 SUCCESS，约 4 分钟，
  含 epoll/unix-common 原生模块），独立选版审查 `independent-selection-reviewer-netty-2026-10-23`
  返回 **accept**（tag 对象 `5c403d0b` peel 到 `5471f0a6`、3479 个 tar 成员逐个 sha256/size 与 manifest
  对齐且与 `git ls-tree -r` 路径/模式一致、无 `.git`、审计仅 redact `HttpUtil.java` 的 GHSA 记号、
  全新目录 47/47 BUILD SUCCESS 且原生 .so 真实产出），`apply_selection_review.py --apply` 已 **frozen**
  （2026-10-23）。
- **guzzle**：旧目标 `snap_efe695448113758a`（7.4.4，2022-05）超出 4 年规则，升级到 `7.14.1` =
  `6b1d2429a2c312474c523aa9017fba0c07b5f4a0`（2026-07-13），新快照 `snap_1ce353bfdb334948`（119 文件）。
  正样本 CVE-2026-67339 / GHSA-94pj-82f3-465w（`applyProxyAuthorizationHeaderHandling` 只在预测到
  HTTP(S) 代理时才迁移头部，direct / no_proxy / SOCKS 路由下 `applyHeaders` 1910-1929 仍把
  `Proxy-Authorization` 写进 `CURLOPT_HTTPHEADER`，libcurl 默认 `CURLHEADER_UNIFIED` 会发给源站；
  7.14.2 在 1985-1987 跳过该头并经 `applyManagedProxyAuthorization` 1580-1598 走 `CURLOPT_PROXYHEADER`）。
  独立 verdict：`confirmed_affected`，**A**（含 `harness/` 红/绿复现：7.14.1 三条泄漏路由，7.14.2 全部干净），
  reviewer `independent-reviewer-guzzle-CVE-2026-67339-r1`。已 promote（1 vuln / 1 location / 1 review /
  21 evidence / 1 status）；旧目标两个正样本（GHSA-25mq-v84q-4j7r / CVE-2022-31091）修复 commit
  `1dd98b05`（7.4.5）经 ancestry 判定已在 7.14.1 内，改判 `confirmed_not_affected`。导出 archive sha256
  `3a53ce38…`，审计导出剩余 advisory 0、excluded 1（CHANGELOG.md）、redacted 3。选版审查包
  `v031/reviews/selection_packets/1420053_guzzle__guzzle.json`；独立选版审查
  `independent-selection-reviewer-guzzle-2026-10-23` 返回 **accept**（tag peel 一致、archive/manifest
  sha256 与路径逐条核对 119/119、无 `.git`、审计导出 remaining 0 且 source_export_id 对齐、
  在全新目录用用户态 PHP/composer 真实构建并通过 1396 tests），`apply_selection_review.py --apply`
  已 **frozen**（2026-10-23）。
- **本机用户态构建链**（无 sudo）：`~/.local/toolchain/` 下 JDK 17.0.20.1、Maven 3.9.16、
  static PHP 8.4.23（含 curl）、composer 2.10.3。guzzle 在 7.14.1 树上 `composer install` +
  `phpunit`（排除需要 127.0.0.1:10000 的 `HttplugIntegrationTest`）实测 1396 tests / 1 failure
  （`CurlFactoryTest::testFirstProxyTunnelOwnerReusesPooledHandleWithoutPurging` 的对象同一性断言）。
- **方法教训（版本区间判定）**：netty 的 advisory 同时列 4.1 与 4.2 两条分支区间；把
  `(4,1,137)` 与 `(4,2,15)` 直接做元组比较会把任何 4.1.x 误判为「≤4.2.15」，导致 37 条误命中。
  正确做法是先按 major.minor 分支过滤，只对同分支边界求值；按此重算为 23 条命中 / 91 条排除 / 3 条格式
  无法解析（`GHSA-p9jm-q85p-7mcp`、`GHSA-4g8c-wm8x-jfhw`、`GHSA-hh82-3pmq-7frp`）。

## 1. 目录与角色（谁是权威）

| 路径 | 角色 |
|---|---|
| `v031/WORKFLOW.md` | **唯一 SOP**：P0–P8 阶段与发布门槛。任何判断以它为准。 |
| `manifest.json` | `dataset_version=0.3.1`、`status=draft`、`evaluation_policy=one_frozen_snapshot_snapshot_only_oracle` |
| `data/` | 数据。九张主表 + `evaluation_selection.jsonl` + `snapshot_candidate_triage.jsonl` + `snapshot_exports.jsonl` + `snapshot_audit_exports.jsonl` + `snapshot_proposals.jsonl` + `legacy_discovery_coverage_v03.jsonl` |
| `v031/schemas/` | 16 份 schema（新增 `snapshot_exports`/`snapshot_proposals`/`snapshot_audit_exports`；`discovery_coverage`/`manifest` 已 v0.3.1 化） |
| `v031/scripts/` | 迁移 / 导出 / 提案 / 审查 / 校验 / 排对 / 费用脚本（见 §5） |
| `v031/reports/` | `VALIDATION_DRAFT.json` / `VALIDATION_RELEASE.json` / `EXPORT_AND_PROPOSAL_STATUS.md` / `SELECTION_FREEZE_2026-10-22.md` / `queue_P3.json` / `COST_REPORT.json` / `SELECTION_TABLE.md` |
| 根目录 `*.md/_V031.md` | README / LIMITATIONS / SELECTION / CANDIDATE_FUNNEL / MIGRATION_AND_VALIDATION，本版说明 |
| `docs/RESUME_V031.md` | 上一版续跑要点（与本文一致，本文更完整） |
| `v03/`、`migration_backup_v02/`、根 `schemas/`、`runs/`、`scratch/` | **只读保留**：旧版本工具与中间产物 |
| 源 v0.3 目录 | `/home/luchitong/work/repo-vuln-50-v03`，**只读未写**（供对照，勿再写）。 | 

**硬约束（必须遵守）**：不得伪造验证结果、不得擅自改审核等级、不得删除未解决候选、不得提前声明数据集完成、
不得机械依赖 semver 判不存在、不得编造 commit 或直接冻结；`unknown/possible_affected` 未核验前不得声称快照已知
漏洞已穷尽。独立 reviewer 必须在隔离上下文工作，不能读采集方卷宗。

## 2. 真实数据基线（逐行复算，非沿用上报值）

- 九张主表（2026-10-23 复算）：**50 repositories / 88 snapshots / 84 vulnerabilities / 84 locations /
  2533 evidence / 84 reviews / 2626 candidates / 50 discovery_coverage / 55 snapshot_vulnerability_status**。
  另：`evaluation_selection` 26、`snapshot_exports` 26、`snapshot_audit_exports` 26、`snapshot_proposals` 24。
  88 个快照中 26 个是 `evaluation_target=true`，另含 django 旧目标 3.0.2、rack 旧目标 2.2.3、libexpat
  旧目标 R_2_4_4、phoenix 旧目标 v1.6.13、netty 旧目标 4.1.59.Final、guzzle 旧目标 7.4.4 等历史快照。
- 注意：漏洞表 84 行 = 55 行在评测目标快照上（live `snapshot_vulnerability_status` 55 行，全为
  `confirmed_affected`）+ 29 行位于历史快照（django 3.0.2 的 8 条、rack 2.2.3 的 2 条、libexpat R_2_4_4
  的 7 条、phoenix v1.6.13 的 2 条、netty 4.1.59.Final 的 6 条、guzzle 7.4.4 的 2 条等），后者保留作
  历史证据但不在主 oracle 中。**不要把表行数当正样本数。**
- 评测目标：**26 个目标 / 24 frozen / 2 rejected**。24 个 frozen 均通过独立选版审查；2 个 legacy
  `documented_exception`（hyper、Newtonsoft.Json）仍为 rejected（gin、protobuf 已分别由取证目标闭环）。
  django tag 4.2.13（CVE-2024-39330）、rack tag v3.1.13（CVE-2025-46727）、libexpat tag R_2_6_2
  （CVE-2024-45490）、phoenix tag v1.8.8（CVE-2026-56811、CVE-2026-56812）、netty 4.1.137.Final
  （CVE-2026-93494）、guzzle 7.14.1（CVE-2026-67339）、echo v4.15.2（CVE-2026-55677）与 axios v1.19.0
  （CVE-2026-101907）都是证据先行的新目标——已导出全树并做 P6 审计导出，并分别通过独立选版审查后冻结
  （django 第一轮因审计泄漏 reject，修复后第二轮 accept；rack/libexpat 首轮 accept；
  phoenix 首轮因环境无 Elixir 工具链 `build_ok=false`，补齐后由同一审查者独立重建并改判 `accept`；
  netty 首轮因无 JDK/Maven 无法满足 `build_ok`，补齐用户态 JDK 17 + Maven 3.9.16 后重新送审；
  echo/axios 于 2026-10-23 由独立审查者实测 go build / npm ci+build 后 accept）。
  剩余 24 仓库 `needs_selection`（`evaluation_snapshot_id=null`）。
- 已知正样本：`data/vulnerabilities.jsonl` 共 **84 行，reviews 84 行（A 11 / B 73）**；其中 55 行在评测目标
  快照上（44 B + 11 A）。A 级为 rexml CVE-2025-58767、django CVE-2024-39330、rack CVE-2025-46727、
  libexpat CVE-2024-45490、phoenix CVE-2026-56812、guzzle CVE-2026-67339、echo CVE-2026-55677 与
  axios CVE-2026-101907 等，均由独立 reviewer 做动态或实测 red/green（verdict 分别在
  `runs/independent/{rexml_CVE-2025-58767_round1,django_CVE-2024-39330_round1,rack_CVE-2025-46727_round1,libexpat_CVE-2024-45490_round1,phoenix_CVE-2026-56812_v188_round1,guzzle_CVE-2026-67339_v7141_round1,echo_CVE-2026-55677_v4152_round1,axios_CVE-2026-101907_v1190_round1}/`）。
- 候选状态：`verified 95` / `rejected 429` / `pending_location 746` / `in_validation 498` / `pending_version 858`。
- 26 库 triage（`snapshot_candidate_triage.jsonl`，1666 行）：`confirmed_affected 64` /
  `confirmed_not_affected 775` / `possible_affected 20` / `duplicate 12` / `unknown 795`；
  24 个未选仓库的 960 条候选无 triage 行。django 旧快照的
  163 条、rack 旧快照的 50 条、libexpat 旧快照的 143 条、phoenix 旧快照的 8 条、netty 旧快照的 130 条与
  guzzle 旧快照的 17 条 triage 行已分别归档；
  django/rack/libexpat 三个新快照上未复核候选一律保留 unknown（162 条、49 条、135 条）；rexml 的 8 条、
  libexpat 的 7 条与 phoenix 的 8 条已在各自快照上按代码/修复区间 + 祖先关系判定
  （`runs/verification/rexml_snapshot_not_applicable/NOT_APPLICABLE.md`、
  `runs/verification/libexpat_R_2_6_2_fixed_previous/NOT_APPLICABLE.md`；phoenix 的排除性结论分别依据
  `validate_local_url/1` 加固、`compare_host?/2` 点边界与 `long_poll.ex` 的惰性 splitter，见 triage 行 basis）。

## 3. 已做 / 未做（诚实分界）

**已做（本会话交付）**
1. 无损升级 0.3→0.3.1：`UPGRADE_REPORT.json`记录了 9753 源文件 SHA256；六个核心表与 v0.3 源字节级一致；
   源 v0.3 未写入（已用其自记校验和核对）。
2. v0.3.1 工具包安装到 `v031/`；discovery_coverage 归档为 legacy 且 50 条重置 `NEEDS_REVIEW`（不继承旧 PASS）。
3. 初始 P3 相关性 triage 由 `v031/scripts/build_initial_triage.py` 用既有证据生成（零 LLM、零编造）。
4. plan_snapshot_queue 生成队列（当前 triage 对应：P0_SELECT 1049 / DONE 71 / ARCHIVE 303 /
   P1_REVIEW 1203，合计 2626；phoenix 冻结后已重跑刷新）。
5. 校验与测试：draft 0 err；release 仍有门槛阻塞（结构未损坏）；v0.3.1 单测 Ran 35 tests OK。
6. 费用台账：本版零 LLM，0 记账/¥0；`cost_policy.json` 为阈值非网关。
7. 23 个当前目标的确定性全树导出 + P6 审计导出：archive/manifest 可复现、无 `.git`、
   `missing_from_archive_count=0`；审计导出逐目标排除 advisory 文档，剩余 advisory ID 0。
   2026-10-23 修复审计扫描器（Sphinx `:cve:` 角色形式与 1 MiB 截断），django 审计导出重建后排除
   114 个文件、替换 1 个文件、剩余 0。
8. 独立选版审查：23 个隔离 packet，审查者与选择者不同；17 个 accept 已 frozen（48 条 anchor）。
   django 第一轮因审计导出泄漏 Sphinx CVE 角色被 reject，修复后第二轮 accept（2026-10-23 冻结）；
   rack 新目标首轮 accept（2026-10-23 冻结）；phoenix 首轮因环境无 Elixir 工具链 `build_ok=false`，
   补齐用户级 Erlang/Elixir 后由同一审查者独立重建（`mix deps.get`、`mix compile` exit 0）改判 accept。
9. ruby/rexml v3.4.1「先证据、后选版」闭环（本版新增）：CVE-2025-58767 dossier（14 条证据）
   → 独立漏洞复核 **A 级**（red/green 复现，verdict 与脚本存 `runs/independent/rexml_CVE-2025-58767_round1/`）
   → `promote_verified_rows.py` 合并写入 1 漏洞/1 location/1 review/30 evidence/1 status
   → 候选 `disc2_de98c5ab937e69a43862e5b4` 置 `verified` 并补 1 条 `confirmed_affected` triage 行
   → snapshot `snap_23dff8507560a593`（evaluation_target）+ 全树导出 196 文件 + P6 审计导出（排除 NEWS.md，剩余 ID 0）
   → 独立选版审查 accept（4 项导出检查全过、tag peel 一致、anchor 三源确认）→ **frozen**。
10. django tag 4.2.13 目标（本版新增）：CVE-2024-39330 dossier（13 条证据）→ 独立漏洞复核 **A 级**
    （red/green，`runs/independent/django_CVE-2024-39330_round1/`）→ 写入 1 漏洞/1 location/1 review/
    26 evidence/1 status → 候选 `disc2_911c6ce3cba60cce0edccd71` 置 verified、补 triage → 全树导出 6,729 文件
    + P6 审计导出 → 旧 3.0.2 目标降级、其 status/triage/export/audit 行归档 → 选版审查（第一轮 reject：
    `docs/releases/security.txt` 的 Sphinx `:cve:` 角色未过滤；修复后第二轮 **accept 并 frozen**）。
11. rack v3.1.13 目标（本版新增）：CVE-2025-46727 dossier（11 条证据）→ 独立漏洞复核 **A 级**
    （Ruby 3.2.3 red/green：3.1.13 接受 5000 参数/4,194,307 字节，3.1.14 抛 QueryLimitError，
    `runs/independent/rack_CVE-2025-46727_round1/`）→ 写入 1 漏洞/1 location/1 review/21 evidence/1 status
    → 候选 `disc2_7f2500f73d3836ead0e09463` 置 verified、补 triage → 全树导出 180 文件 + 审计导出
    → 旧 2.2.3 目标降级、其 status/triage/export/audit 行归档 → 选版审查 **accept 并 frozen**
    （2026-10-23）。
12. libexpat R_2_6_2 目标（本版新增）：CVE-2024-45490 dossier（10 条证据：OSV/NVD 原始记录、tag peel、
    fix commit 祖先关系、行号 grep、6 行 guard diff）→ 独立漏洞复核 **A 级**（两步 harness：负长度
    `XML_ParseBuffer` 后再 `XML_GetBuffer` 触发 ASan heap-buffer-overflow，R_2_6_3 修复版无崩溃，
    `runs/independent/libexpat_CVE-2024-45490_round1/`）→ 写入 1 漏洞/1 location/1 review/18 evidence/1 status
    → 候选 `disc2_35a922eb511ed468630f4a2d` 置 verified、补 triage → 旧 R_2_4_4 目标降级、其 143 条
    triage、7 条 status、export/audit 行归档 → 全树导出 199 文件 + P6 审计导出 → 选版审查 **accept 并 frozen**
    （2026-10-23）。同轮把 R_2_4_4 时代的 7 个旧 CVE 以修复区间 + 祖先关系判为 `confirmed_not_affected`。
13. phoenix v1.8.8 目标（本版新增）：旧 v1.6.13 仅因超过 4 年被拒，本次先在 v1.8.8 取得两个独立正样本
    —— CVE-2026-56811（8 条证据，独立静态复核 grade B，`16e295d2` 修复于 1.8.9）与 CVE-2026-56812
    （8 条证据，独立复核 grade A：Node red/green 在同一 tag blob 上 20/20 抛错、1.8.9 为 0/20，
    `runs/independent/phoenix_CVE-2026-56812_v188_round1/repro/`）→ `promote_verified_rows.py` 两次合并
    （各 1 漏洞/1 location/1 review/19 evidence/1 status）→ 候选 4 条置 verified、2 条置 rejected
    → 8 条 triage（2 个 CVE 各两条 discovery 路径 confirmed_affected；CVE-2022-42975、CVE-2017-1000163、
    CVE-2026-32689×2 confirmed_not_affected，均附代码级证据）→ 旧 v1.6.13 目标降级，其
    8 triage、2 status、export/audit、21 evidence、location、review 与 selection 行归档
    → 全树导出 478 文件 + P6 审计导出（排除 2 文件，剩余 0）→ 选版审查 **accept 并 frozen**（2026-10-23）。
14. netty 旧目标 4.1.59.Final 超 4 年 → 证据先行升级到 netty-4.1.137.Final（`5471f0a6`，2026-08-06）：
    独立复核 CVE-2026-93494 **B 级**（静态：`StompSubframeDecoder.decode` 在 155 行暂存 `lastContent`，
    `ReplayingDecoderByteBuf` 的 REPLAY 是 `Signal extends Error`，191-195 的 `catch (Exception)` 接不住，
    且无 `handlerRemoved0`，pooled ByteBuf 泄漏；8132 是 `maxChunkSize` 上限而非固定泄漏量）→ promote
    （1 vuln/1 location/1 review/22 evidence/1 status，`grade B` 因无 `reproduction_reference`）→
    旧 6 个正样本按修复 commit ancestor 判 `confirmed_not_affected`，旧 selection/export/audit/status/triage
    归档（vulnerabilities/locations/reviews/evidence 保持 live）→ 全树导出 3479 文件（sha256 `089a09be…`）
    + 审计导出（剩余 0、redacted 1）→ 审查包 `v031/reviews/selection_packets/1064563_netty__netty.json`
    → 独立选版审查 2026-10-23 发起（用户态 JDK 17 + Maven 3.9.16 全量 `mvn package` 已在本机 **BUILD SUCCESS**
    47 模块，审查者需从全新解包目录自行重建）。
15. guzzle 旧目标 7.4.4（2022-05）超 4 年 → 升级到 7.14.1（`6b1d2429`，2026-07-13）：独立复核
    CVE-2026-67339 **A 级**（`harness/` 红/绿：7.14.1 下 direct / no_proxy / SOCKS 三条路由都把
    `Proxy-Authorization` 发给源站，7.14.2 全部干净）→ promote（1 vuln/1 location/1 review/21 evidence/
    1 status）→ 旧两个正样本（GHSA-25mq-v84q-4j7r、CVE-2022-31091）按 `1dd98b05`（7.4.5）ancestor 判
    `confirmed_not_affected`，旧行归档 → 全树导出 119 文件（sha256 `3a53ce38…`）+ 审计导出
    （排除 CHANGELOG.md、redacted 3、剩余 0）→ 独立选版审查 **accept 并 frozen**（2026-10-23，
    审查者在全新目录用用户态 PHP 8.4.23 + composer 2.10.3 真实构建，1396 tests / 1 环境相关 failure）。

**未做（留给后续，别视为已完成）**
- 仍未达 50 库冻结：20 frozen + 3 rejected（protobuf / hyper / Newtonsoft.Json 的 legacy 目标）
  + 27 未选版。
- 6 个 legacy `documented_exception` 目标里，netty/guzzle 已升级；protobuf 已定新目标
  **v28.1（4.28.1，2024-09-10，CVE-2024-7254，区间 4.0.0-RC1→4.28.2）**，独立复核 A 级通过、
  已 promote 并完成导出/审计，独立选版审查进行中；gin 已定 **v1.9.0（2023-02-21，CVE-2023-29401）**，独立复核**已返回
  `confirmed_affected` / grade A**（审查者用 go1.27.3 做红/绿复现，线上头 v1.9.0
  `attachment; filename="setup.bat";x=.txt"` vs v1.9.1 转义版），已迁移旧目标并归档、promote
  （1 vuln/1 location/1 review/24 evidence/1 status）、导出 124 文件 + 审计导出
  （排除 CHANGELOG.md，剩余 0）；独立选版审查 **accept**（go build/vet/test 全 exit 0，
  124/124 文件 manifest 全量比对一致），已 frozen（2026-10-23，第 20 个 frozen）。
  审查者指出两处 collector 表述错误
  （CNA 为 CWE-20 而非 CWE-494；GHSA 实有 CVSS 3.1 4.3 向量），已在 dossier 记录。
  hyper / Newtonsoft.Json 经 OSV 逐版本查询确认**不存在窗口内可用的受影响版本**
  （hyper 最新受影响版 0.14.11 = 2021-07-21；Newtonsoft.Json 最新受影响版 13.0.0，13.0.1 已于
  2021-03-22 发布），故保留 `documented_exception`；证据见
  `runs/verification/documented_exception_evidence_2026-10-23/EVIDENCE.md`（「无已知 advisory」不等于安全）。
- 27 仓库未选版（Catalog 已验证漏洞为 0；不得编造 tag/commit；先补正样本再选版）。
- 1200 unknown 中可能与 SHA 相关的候选未定向核验；27 库候选未 triage。
- `PASS_KNOWN_SWEEP=0/50`（需对固定 SHA 两轮独立检索均无新增「相关」候选，不只是无新增提升）。
- 8 条 grade A（rexml/django/rack/libexpat/phoenix 56812/guzzle 67339/gin 29401/protobuf 7254），其余 live 正样本为 B 级静态验证。
  无 Agent 评测运行；运行时网络隔离尚未由 harness 实施（`network_policy=off` 只是声明）。
  `manifest.source_cutoff_date=null` 未复核。
- 审计导出是字符串级控制：不含 advisory ID 的修复说明/外链仍可能存在。另：collector 的泄漏扫描只匹配
  `CVE-`/`GHSA-`，不匹配 `GO-`/`RUSTSEC-`/`EEF-` 等 ID（gin 的 CHANGELOG.md 含 4 个 `GO-` 条目而未被计数，
  该文件整体被审计导出排除，故剩余 ID 仍为 0；后续仓库需注意同类漏检）。

## 4. 下一步优先级

1. **netty/guzzle 已完成证据先行升级并 frozen（2026-10-23）**；继续处理剩余 4 个 legacy
   `documented_exception` 目标：gin v1.9.0（CVE-2023-29401）已完成漏洞 A 级复核 → promote →
   导出/审计 → 独立选版 **accept → frozen**，全流程闭环；protobuf v28.1（CVE-2024-7254）
   dossier 已完成，独立复核已返回 `confirmed_affected` / A 级（4.28.1 实测 SOE，4.28.2 转 IPBE），
   14 条 discrepancy 已回落进 dossier（CWE-20/RubyGems 包/a037f28f 主分支修复/75-83 行号），
   旧目标已迁移归档、promote（1 vuln/1 location/1 review/77 evidence/1 status）、
   导出 2941 文件 + 审计导出（无排除、剩余 0）；独立选版审查对 checks 1-5 判 **accept**，但
   **`build_ok=false`**（`java/{core,lite,util,kotlin-lite}` 只发 `pom_template.xml`、树内无 protoc
   与生成源码；`third_party/abseil-cpp` 等 3 个 gitlink 被导出策略跳过），`apply_selection_review.py`
   据此标 `build_not_feasible`，v28.1 保持 rejected；已改用 v3.25.4（窗口内、`<3.25.5` 受影响、
   该 tag 仍带真实 `java/core/pom.xml`）作为可构建的替代目标：独立漏洞复核 A 级、迁移/promote/导出/审计完成，
   独立选版审查实测 `mvn -B install -Dmaven.test.skip=true` exit 0（JDK 17 + Maven 3.9.16 + protoc 25.4，
   7/7 模块成功，`build_ok=true`），`apply_selection_review.py --apply` 已 **frozen**（2026-10-23）；
   hyper / Newtonsoft.Json 已用 OSV 逐版本查询证明窗口内无可利用版本（见
   `runs/verification/documented_exception_evidence_2026-10-23/`），保留 documented_exception，
   不再尝试「改成最新版」。禁止直接把 tag 改成最新版。同时复核 `source_cutoff_date`。
   phoenix 可作为「旧 tag 被 4 年规则拒绝 → 在更新稳定 tag 上重新取证」的完整模板。
2. **为 26 未选仓库补已验证正样本**（对候选 SHA 至少一条 B/A confirmed_affected），再按规则选版冻结；
   禁止先选版本后补证据。rexml 已按此流程完成，可作为模板（`runs/verification/rexml_CVE-2025-58767/`）。
   已完成：echo CVE-2026-55677 / v4.15.2（`snap_e0836fa1c53e240d`）与 axios CVE-2026-101907 / v1.19.0
   （`snap_04c033042a3d52eb`）均经独立复核 grade A、promote、导出/审计，选版审查已派发；
   进行中：caddy v2.11.4 侦察（CVE-2026-55458 / GHSA-6365 候选，修复在 v2.11.5）。
   `data/snapshot_proposals.jsonl` 现有 27 个仓库的候选 tag（120 个），仍需源码级确认；
   openssl/openssl 与 nlohmann/json 当前无有界候选。axios(v1.15.0)/OpenSSL(openssl-3.0.1)/sinatra(v3.0.3)
   有带 tag 历史快照但无 confirmed_affected，是首批候选。
   **sinatra 第一轮已判负**：v4.1.1 + CVE-2025-61921 的独立复核用 MRI 2.5.9–3.2.0 与真实 gem 实测
   `split(/\s*,\s*/)` 为线性（正对照 `/^(a|a)*$/` 能测出指数），判 `not_affected`，未写任何数据行
   （`runs/verification/sinatra_CVE-2025-61921_v411/ROUND.md`）。改用 v4.0.1（`7dc5940e…`，2025-05-24，
   该树无 `host_authorization`）上的 CVE-2024-21510（X-Forwarded-Host 开放重定向，4.1.0 修复）。
3. **处理 unknown（现 795 行）**：范围/分支半程已完成并落地——`triage_range_scope.py` v1.1 对 1201 条
   unknown 生成提案（`runs/triage_range_scope_2026-10-23/proposals_v1_1.jsonl`），经独立审计
   （`runs/triage_range_scope_2026-10-23/audit/AUDIT.md`，568 条可执行提案 0 分歧、47 条抽样复核）后
   仅应用 `not_affected_range`：406 行 → `confirmed_not_affected`（版本区间判定，不声称祖先关系；
   见 `DISPOSITION.md`）。**未应用的 42 条 `out_of_scope_product` 全部保留 unknown**（审计判其归属规则不成立，
   CVE-2022-40281 是疑似假阴性）。剩余 795 = 465 条无缓存记录可判 + 330 条范围不可判/冲突；这些需要
   源码/差异级定向核验，相关但未过 B/A 门槛的保留 `unknown`（不能判无效）。所有决策写回
   `snapshot_candidate_triage.jsonl`。
4. **两轮独立快照限定检索**（GHSA/OSV/NVD/官方 advisory + fix diff），两轮零新增**相关**候选且公开库/上游均
   成功，才可声明 `PASS_KNOWN_SWEEP`。
5. 有预算才接 LLM：任何调用记入 `v031/ledger/model_calls.jsonl`（stage/model/input/output/cached tokens/
   cost_cny），再用 `cost_report.py` 复核预算（budget=500，warn 0.8，halt 1.0）。优先 rules-first → cheap model
   → escalate；单候选单阶段≤2 次 LLM，超转人工排队，绝不自动 rejected。

## 5. 常用命令（venv 已就绪，jsonschema 4.26.0）

```bash
cd /home/luchitong/work/repo-vuln-50-v031

# 校验（draft / release 门槛）
.venv/bin/python v031/scripts/validate_dataset.py . --draft --json-out v031/reports/VALIDATION_DRAFT.json
.venv/bin/python v031/scripts/validate_dataset.py . --json-out v031/reports/VALIDATION_RELEASE.json

# 源码导出 / 提案 / 审计导出 / 审查应用
.venv/bin/python v031/scripts/freeze_snapshots.py . --jobs 3
.venv/bin/python v031/scripts/propose_missing_snapshots.py . --jobs 4
.venv/bin/python v031/scripts/build_selection_review_packets.py .
.venv/bin/python v031/scripts/build_audit_exports.py .
.venv/bin/python v031/scripts/apply_selection_review.py . \
  --reviews v031/reviews/selection_review_2026-10-23.jsonl  # 默认 dry-run

# 单条 dossier 合并提升（需独立 verdict；默认 dry-run）
.venv/bin/python v031/scripts/promote_verified_rows.py . \
  --dossier runs/verification/rexml_CVE-2025-58767/dossier.json \
  --verdict runs/independent/rexml_CVE-2025-58767_round1/verdict.json

# 排对 / 漏斗（依据当前 triage）
.venv/bin/python v031/scripts/plan_snapshot_queue.py . --out v031/reports/queue.json

# 用既有证据重建初始 triage（改数据/候选后刷新）
.venv/bin/python v031/scripts/build_initial_triage.py . --checked-at 2026-10-22T00:00:00Z

# 费用
.venv/bin/python v031/scripts/cost_report.py v031/ledger/model_calls.jsonl --budget-cny 500 --out v031/reports/COST_REPORT.json

# 单测
.venv/bin/python -I -m unittest discover -s v031/tests -v
```

## 6. 关键坑（必须知道）

- **GHSA 小写正则**：`v031/schemas/vulnerabilities.schema.json` 的 `vulnerability_id` pattern 必须是
  `^(GHSA-[0-9A-Za-z-]+|CVE-[0-9]{4}-[0-9]+)$`（小写 GHSA ID 真实存在）。初始补丁后 SHA256=
  `efa419ad698472bb4d97cad17966215fd0daf79644b681be5016271c12ac4265`。若此 schema 被覆盖成大写版，9 条真实
  ID 会校验失败，需重打补丁。
- **`validate_v02_reference.py`（v0.3 参考验证器）对 9 条小写 GHSA 误报**，与本版数据无关，别当数据错误。
- **校验器只做结构/引用/声明检查**，不验证漏洞真实性、修复版本或检索完整性。schema 通过 ≠ 漏洞实存。
- **legacy_discovery_coverage_v03.jsonl** 是 v0.3 旧全历史覆盖的档案副本（哈希 `6f8cda79…`）；当前
  `discovery_coverage.jsonl` 应全为 `NEEDS_REVIEW`，你需要重写为 `selected_snapshot_only` 模式才能过 release。
- **queue 的 DONE 是「可作为 recall 正样本」**，不是审毕；ARCHIVE 是「有证据归档」，P1_REVIEW 是 unknown。
- 费用工具不拦截调用；未接入网关时预算靠自觉记录，别声称「已强制封顶」。

## 7. 发布门槛速查（自 `v031/WORKFLOW.md` §P8）

- 50 库各一冻结 SHA、语言覆盖 ≥10 类、每目标正样本可定位+B/A 审核。
- 该 SHA 所有候选均有 triage；`possible_affected/unknown` 必须深核或明确保持 draft。
- `PASS_KNOWN_SWEEP` 指固定快照两轮零新增相关候选（非零新增提升）。
- 不再要求每条历史 CVE 有 snapshot_vulnerability_status 行；未解决历史候选保留但不自动阻塞。

## 8. 交付物清单（本版已完成，勿重建）

`README_V031.md`、`LIMITATIONS_V031.md`、`SELECTION_REPORT_V031.md`、`CANDIDATE_FUNNEL_V031.md`、
`MIGRATION_AND_VALIDATION_V031.md`、`docs/RESUME_V031.md`、`UPGRADE_REPORT.json`、`cost_policy.json`、
`v031/reports/{VALIDATION_DRAFT,VALIDATION_RELEASE,queue_P3,COST_REPORT}.json`、`v031/reports/SELECTION_TABLE.md`。