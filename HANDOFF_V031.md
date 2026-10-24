# HANDOFF_V031 — 下一对话交接文档

> 面向全新对话（无本会话记忆）。读完本文件即可接续。数据集根目录：`/home/luchitong/work/repo-vuln-50-v031`。

## 0. 一句话现状

RepoVuln-50 是 50 个上游开源仓库的漏洞审计评测基准，目标「一库一冻结 commit」。当前是 **v0.3.1 draft**：
已完成「无损迁移 + 低成本相关性筛选 + 独立选版审查 + 证据先行选版」，**48/50 仓库有评测目标，其中 46 个已
frozen（均通过隔离选版审查 accept，最新为 grpc v1.52.0，2026-10-24 冻结）、2 个 legacy `documented_exception`
目标仍为 rejected（hyper、Newtonsoft.Json）**；nlohmann/json 与 openssl/openssl 无评测目标（漏洞窗口内无可用
稳定 tag）。**97 条评测目标上的已确认正样本（46 B + 51 A）**，另有 29 条历史快照样本（全 B）保留为证据；
2626 条候选已产出 2613 条相关性 triage。**未完成 2 库选版、574 条 unknown 与 573 条 possible 未决、无 Agent 运行、未达发布门槛**。
最新两条正样本（2026-10-24）是 django 4.2.13 上的 CVE-2025-48432、CVE-2025-64460，
均由隔离复核 grade A 后 promote（见 WORK_LOG 同日两卷宗条目）；此前同日三条为
CVE-2025-32873、CVE-2025-57833、CVE-2025-59682。
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

- 九张主表（2026-10-24 复算）：**50 repositories / 110 snapshots / 126 vulnerabilities / 126 locations /
  4298 evidence / 126 reviews / 2626 candidates / 50 discovery_coverage / 97 snapshot_vulnerability_status**。
  另：`evaluation_selection` 48、`snapshot_exports` 48、`snapshot_audit_exports` 48、`snapshot_proposals` 2。
  110 个快照中 48 个是 `evaluation_target=true`，另含 django 旧目标 3.0.2、rack 旧目标 2.2.3、libexpat
  旧目标 R_2_4_4、phoenix 旧目标 v1.6.13、netty 旧目标 4.1.59.Final、guzzle 旧目标 7.4.4 等历史快照。
- 注意：漏洞表 126 行 = 97 行在评测目标快照上（live `snapshot_vulnerability_status` 97 行，全为
  `confirmed_affected`）+ 29 行位于历史快照（django 3.0.2 的 8 条、rack 2.2.3 的 2 条、libexpat R_2_4_4
  的 7 条、phoenix v1.6.13 的 2 条、netty 4.1.59.Final 的 6 条、guzzle 7.4.4 的 2 条等），后者保留作
  历史证据但不在主 oracle 中。**不要把表行数当正样本数。**
- 评测目标：**48 个目标 / 46 frozen / 2 rejected**。46 个 frozen 均通过独立选版审查；2 个 legacy
  `documented_exception`（hyper、Newtonsoft.Json）仍为 rejected（gin、protobuf 已分别由取证目标闭环）。
  django tag 4.2.13（CVE-2024-39330）、rack tag v3.1.13（CVE-2025-46727）、libexpat tag R_2_6_2
  （CVE-2024-45490）、phoenix tag v1.8.8（CVE-2026-56811、CVE-2026-56812）、netty 4.1.137.Final
  （CVE-2026-93494）、guzzle 7.14.1（CVE-2026-67339）、echo v4.15.2（CVE-2026-55677）与 axios v1.19.0
  （CVE-2026-101907）都是证据先行的新目标——已导出全树并做 P6 审计导出，并分别通过独立选版审查后冻结
  （django 第一轮因审计泄漏 reject，修复后第二轮 accept；rack/libexpat 首轮 accept；
  phoenix 首轮因环境无 Elixir 工具链 `build_ok=false`，补齐后由同一审查者独立重建并改判 `accept`；
  netty 首轮因无 JDK/Maven 无法满足 `build_ok`，补齐用户态 JDK 17 + Maven 3.9.16 后重新送审；
  echo/axios 于 2026-10-23 由独立审查者实测 go build / npm ci+build 后 accept；
  grpc v1.52.0 于 2026-10-24 由独立审查者实测 CMake/Ninja 构建 `libgrpc.a` + 消费者链接运行后 accept）。
  剩余 2 仓库 `needs_selection`（`evaluation_snapshot_id=null`）：nlohmann/json、openssl/openssl
  （漏洞窗口内没有可用稳定发布 tag）。
- 已知正样本：`data/vulnerabilities.jsonl` 共 **126 行，reviews 126 行（A 51 / B 75）**；其中 97 行在评测目标
  快照上（46 B + 51 A），29 行位于历史快照（全 B）。A 级为 rexml CVE-2025-58767、django CVE-2024-39330、
  rack CVE-2025-46727、libexpat CVE-2024-45490、phoenix CVE-2026-56812、guzzle CVE-2026-67339、
  echo CVE-2026-55677、axios CVE-2026-101907、grpc CVE-2023-1428、cJSON CVE-2023-53154、cJSON CVE-2023-50472、
  cJSON CVE-2025-57052、gitea GHSA-hg5r-vq93-9fv6（HMAC 无分隔歧义，Go 原语级红/绿）、
  django CVE-2024-39329（不可用密码的计时枚举，实测约 715× 差异）、
  gitea GHSA-7wvc-rvp7-w99x（LFS SSH 子命令鉴权绕过，真实服务器红/绿）与
  django CVE-2024-38875（urlize 括号裁剪二次方复杂度，实测 9.86 s → 0.003 s）、
  django CVE-2024-41989（floatformat 指数内存耗尽）、django CVE-2024-39614
  （语言码二次方切片）、django CVE-2024-41991（urlize/widget IDNA 无上限）与
  django CVE-2024-53907（strip_tags 无深度上限，26.3 s → SuspiciousOperation）与
  django CVE-2024-53908（Oracle `HasKeyLookup.as_oracle` 把 lhs 参数拼进 SQL 文本，compile-level 红/绿）与
  django CVE-2024-45231（密码重置邮件失败时的状态码枚举，真实 view 返回 500 vs 302）与
  django CVE-2025-64459（`_connector` 字典展开注入，filter 返回全部行 vs 4.2.26 拒绝）、
  django CVE-2025-32873（strip_tags 二次方 DoS，7.893 s vs SuspiciousOperation）、
  django CVE-2025-57833（FilteredRelation alias 注入，过滤绕过 vs ValueError）与
  django CVE-2025-59682（archive 前缀兄弟目录写出 vs SuspiciousOperation）、
  django CVE-2025-48432（`log_response()` 未转义参数导致日志注入，4.2.22 部分修复 / 4.2.23 完整）与
  django CVE-2025-64460（XML serializer `getInnerText()` 二次方膨胀，1 MB 载荷 4.63 s vs 0.0097 s）等，均由独立 reviewer 做动态或实测
  red/green（verdict 分别在
  `runs/independent/{rexml_CVE-2025-58767_round1,django_CVE-2024-39330_round1,rack_CVE-2025-46727_round1,libexpat_CVE-2024-45490_round1,phoenix_CVE-2026-56812_v188_round1,guzzle_CVE-2026-67339_v7141_round1,echo_CVE-2026-55677_v4152_round1,axios_CVE-2026-101907_v1190_round1,grpc_CVE-2023-1428_v1.52.0_round1,cjson_CVE-2023-53154_v1716_round1,cjson_CVE-2023-50472_v1716_round1,cjson_CVE-2025-57052_v1716_round1,gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1,django_CVE-2024-39329_4213_round1,gitea_GHSA-7wvc-rvp7-w99x_v1.25.5_round1,django_CVE-2024-38875_4213_round1,django_CVE-2024-53907_4213_round7,django_CVE-2024-53908_4213_round8,django_CVE-2024-45231_4213_round9,django_CVE-2025-64459_4213_round10,django_CVE-2025-32873_4213_round11,django_CVE-2025-57833_4213_round11,django_CVE-2025-59682_4213_round11,django_CVE-2025-48432_4213_round12,django_CVE-2025-64460_4213_round12}/`）。
- 候选状态：`verified 117` / `rejected 429` / `pending_location 738` / `in_validation 485` / `pending_version 857`。
- 全部仓库 triage（`snapshot_candidate_triage.jsonl`，2613 行）：`confirmed_affected 117` /
  `confirmed_not_affected 1321` / `possible_affected 573` / `duplicate 28` / `unknown 574`；
  `pending_relevant_triage` **1147**；
  已选版仓库内候选均有 triage 行（549 条「此前无行」的候选已于 2026-10-24 以 unknown 行补全，
  `runs/triage_untriaged_unknown_2026-10-24/`）；另有 13 条属于两个未选版仓库，按先选版处理。django 旧快照的
  163 条、rack 旧快照的 50 条、libexpat 旧快照的 143 条、phoenix 旧快照的 8 条、netty 旧快照的 130 条与
  guzzle 旧快照的 17 条 triage 行已分别归档；
  django/rack/libexpat 三个新快照上的候选现为 unknown 2 条、0 条、34 条（其余已有范围/代码级决策；
  区间命中一律记入 `possible_affected`：django 28、rack 21、libexpat 36），这些 possible 仍需源码复核；
  rexml 的 8 条、
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
5. 校验与测试：draft 0 err / 49 warning；release 仍有门槛阻塞（结构未损坏）；v0.3.1 单测 35 → 当前 126 tests OK
   （2026-10-24 新增低侧证明、归属、裸版本拒绝与不可读副本不否决的测试）。
6. 费用台账：本版零 LLM，0 记账/¥0；`cost_policy.json` 为阈值非网关。
7. 48 个当前目标的确定性全树导出 + P6 审计导出（`snapshot_exports`/`snapshot_audit_exports` 各 48 行）：archive/manifest 可复现、无 `.git`、
   `missing_from_archive_count=0`；审计导出逐目标排除 advisory 文档，剩余 advisory ID 0。
   2026-10-23 修复审计扫描器（Sphinx `:cve:` 角色形式与 1 MiB 截断），django 审计导出重建后排除
   114 个文件、替换 1 个文件、剩余 0。
8. 独立选版审查：48 个隔离 packet，审查者与选择者不同；46 个 accept 已 frozen（grpc 的 4 条 anchor
   由 `v031/reviews/selection_review_grpc_2026-10-24.jsonl` 记录）。
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
16. 2026-10-24 又 promote 四个独立复核正样本：gitea GHSA-hg5r-vq93-9fv6（A）、django CVE-2024-42005（B，
    `values()`/`values_list()` 经 JSONField key 的 SQL 注入，可达性需额外 aggregate 注解）、django
    CVE-2024-39329（A）与 gitea GHSA-7wvc-rvp7-w99x（A）。每次都是 dossier → 隔离 verdict →
    `promote_verified_rows.py --apply`；随后用带守卫的脚本把对应 triage 行改成 `confirmed_affected`
    （`runs/data_fixes/apply_promoted_candidate_*_2026-10-24.py`，先 dry-run、写备份）并把
    `independent_verdict_path` 从 `/tmp` 指到 `runs/independent/<packet>_round1/`
    （`persist_independent_verdicts_*_2026-10-24.py`，校验保留副本 sha256 与源一致）。
    本轮顺带修掉一处历史遗漏：hg5r 首次改写只改了 `disc2_*` 行，同快照的
    `adv3_d931ecfcc9a09dd2` 仍停在 `possible_affected`；用全表扫描（possible 行是否引用同快照已 promote
    漏洞）找出并一并改写，扫描后此类残留为 0。
17. 纠正一处来源标注错误：NVD source `134c704f-9b21-4f2e-91b3-4a467353bcc0` 是 **CISA-ADP** 容器而非
    GitHub CNA（42005 隔离复核者发现，并用数据集内部既有标注交叉确认）。三个 django dossier 已按此措辞
    重建；`data/vulnerabilities.jsonl` 中 CVE-2024-42005（本轮 promote）与更早的 CVE-2024-39330 仍写
    「GitHub CNA」，已由 `runs/data_fixes/fix_cisa_adp_attribution_2026-10-24.py`（守卫 source_url 与
    唯一子串、写备份）改为「CISA-ADP 容器，向量由 GitHub CNA 发布」。severity 数值与向量未变。
18. django CVE-2024-38875（4.2.13，urlize/urlizetrunc 的 `trim_punctuation` 二次方括号裁剪）
    卷宗 `runs/verification/django_CVE-2024-38875_4213/`（10 条证据）→ 隔离复核 **A 级**：
    reviewer 自建五棵 tag 树实测 N=100000 的 `"("*N + ":" + ")"*N`，4.2.13 9.86 s / 4.2.14
    0.003 s，模板过滤器路径同样复现，并做了 N=2000→100000 的二次缩放；修复提交
    `79f36876` 首见于 4.2.14，5.0.x 为 `72856446`（5.0.7）。verdict
    `runs/independent/django_CVE-2024-38875_4213_round1/verdict.json`。首轮 promote 因
    `fields_verified` 缺 `languages`（reviewer 用 `vulnerability_id` 充当第九项）被工具拒绝，
    请同一 reviewer 自行补核语言清单后重发（sha256 `a70331ce…`），再次 dry-run 通过后
    `--apply`（1 vuln / 1 location / 1 review / 29 evidence / 1 status）。
    triage 行 `disc2_051d93d5bd86570c8437b5dd` 与 review 路径分别由
    `apply_promoted_candidate_round3_*` / `persist_independent_verdicts_round3_*` 改写。
19. gitea GHSA-hg5r-vq93-9fv6 的复核产物在 promote 之后又被 reviewer 的后台收尾更新过一次：
    `NOTES.md` 增加 v1.26.2 全量 `hmac.New` 普查的两段说明，`sources/v1262_hmac_sites.txt`
    增加 4 行非 artifact 站点，verdict 中对应的两个 artifact sha256 随之更新。已把最终版本
    复制回 `runs/independent/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1/`，11 个 artifact
    sha256 全部重新匹配（`repro/main.go` 对应包内 `reproduction/main.go`）；结论未变
    （`confirmed_affected` / A / `f913d90a…`），`data/reviews.jsonl` 不存 verdict sha，无需改数据。
    新 verdict sha256 `529c1170…`。
20. django CVE-2024-39614（4.2.13，`get_supported_language_variant` 对连字符稠密语言码的
    二次方切片）卷宗 `runs/verification/django_CVE-2024-39614_4213/`（12 条证据）→ 隔离复核
    **A 级**：reviewer 在 PyPI 4.2.13/4.2.14 venv 实测 `"en-"*30000` 2.196 s（n=1k/3k/10k/30k
    缩放 0.0015/0.0185/0.2250/2.196 s），90,000 字符 cookie 路径 0.802 s，4.2.14 约
    0.000075 s；verdict sha256 `72a45407…`，24 项 artifact 全匹配。`--apply`
    （2026-10-23T23:33:31Z）追加 1 vuln / 1 location / 1 review / 31 evidence / 1 status。
    保留包 `runs/independent/django_CVE-2024-39614_4213_round1/`（verdict + NOTES + sources +
    scripts + repro，逐项 sha256 复核 0 不匹配）；review 路径与候选行
    `disc2_97b11946b732970b9a25004c` 分别由 `persist_independent_verdicts_round5_*` /
    `apply_promoted_candidate_round5_*` 改写。reviewer 指出 OSV GIT 区间无效（introduced 是
    2025/2026 security-archive 提交、fixed 只是版本号 bump），真实补丁是 `17358fb3` / `8e7a44e4`。
21. django CVE-2024-41989（floatformat 科学计数法指数内存耗尽）隔离复核 **A 级**后 promote
    （2026-10-23T23:32:12Z）：1 vuln / 1 location / 1 review / 29 evidence / 1 status，grade A；
    verdict sha256 `2e8eb95f…`。收尾用 `persist_independent_verdicts_round4_*`（指向
    `runs/independent/django_CVE-2024-41989_4213_round1/verdict.json`）与
    `apply_promoted_candidate_round4_*`（`disc2_1d98594ee81566538ecb96d2` →
    `confirmed_affected`）。两次 promote 后基线 **116 / 87**（A 41 / B 75），possible
    583、unknown 574、NA 1321。
22. django CVE-2024-41991（4.2.13，`urlize`/`urlizetrunc` 与 `AdminURLFieldWidget` 对超大
    Unicode 输入的 DoS）卷宗 `runs/verification/django_CVE-2024-41991_4213/`（12 条证据）→
    隔离复核 **A 级，`confirmed_affected`**：reviewer 实测 4.2.13 的 `"한.글."×1,000,000`
    （约 4 MB）在 email/http/www 三条 `urlize` 路径 10.86 / 10.97 / 11.41 s、widget 11.05 s，
    RSS 增量约 +200 MB，输出膨胀到 ~22.0 M 字符；4.2.15 同输入 0.043–0.050 s、RSS 增量 0，
    widget href 为空；4.2.14 在 n=100k 仍 1.0603 s，确认首发修复版本 4.2.15。verdict
    sha256 `709fce73…`，24 项 artifact 全匹配。`--apply`（2026-10-23T23:42:06Z）追加
    1 vuln / 1 location / 1 review / 31 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-41991_4213_round1/`（verdict + NOTES + feeds +
    scripts + out + 6 个被引用 venv 文件，逐项 sha256 复核 0 不匹配）；review 路径与候选行
    `disc2_3bb0bba7fbc37c8593e5441b` 分别由 `persist_independent_verdicts_round6_*` /
    `apply_promoted_candidate_round6_*` 改写。reviewer 指出 OSV GIT 事件哈希无效、NVD 7.5
    vs GHSA A:L、CWE-1333/ReDoS 归类与线性 IDNA 实测不符。当前基线 **117 / 88**
    （A 42 / B 75），possible 582、unknown 574、NA 1321。
23. django CVE-2024-41990 在 4.2.13 上**不可按已公布形态复现**，已记为探针
    `runs/verification/django_CVE-2024-41990_4213_probe/`（bench.py + 三份日志 + README，
    **不是卷宗、无裁定**）。`".;" * n` 在 4.2.13/4.2.14/4.2.15 的 n=200k 耗时分别为
    0.004674 / 3.271716 / 0.004906 s；4.2.14 每翻倍约 3.4×/4.1×（二次），另六种实体形态
    三版皆线性。机制：4.2.14 的 38875 修复（`79f3687642`，4.2.13 无、4.2.14 有）把
    `rfind("&")` + `unescape(middle[amp:])` 放进通用尾部剥离路径，4.2.15 的 41990 修复
    （`d0a82e26a7`，仅在 4.2.15）复用同一个 `amp`。故候选
    `disc2_0375e0e8d50b5f62dc5c2e03` **维持 `possible_affected`**：无复现不等于快照无其它
    trigger，未 promote、未写 `data/`。
24. django CVE-2024-45230 同样在 4.2.13 上**不可按已公布形态复现**，已记为探针
    `runs/verification/django_CVE-2024-45230_4213_probe/`（bench.py + 四份日志 +
    4.2.16 发布说明摘录 + README，**不是卷宗、无裁定**）。`"&" + ";:"*n` 在
    4.2.13/4.2.14/4.2.15/4.2.16 的 n=200k 耗时 0.005114 / 13.448057 / 13.108951 /
    0.006153 s；`".;"`/`";."`/`":;"`/`";::"` 同型，`"&" + ";"*n` 四版皆毫秒级。
    修复 `d147a8ebbd` 只在 4.2.16；4.2.14 的 38875 修复已引入该二次方，4.2.16
    发布说明亦写 “in 4.2.15”。候选 `disc2_91b14048e4ec3e3a627057a1` **维持
    `possible_affected`**：未 promote、未写 `data/`；4.2.13 的 urlize DoS 已由
    CVE-2024-38875 覆盖，但本条不据此改判 NA。

25. django CVE-2024-53907（4.2.13，`strip_tags()` 剥离循环无深度上限的二次方 DoS）卷宗
    `runs/verification/django_CVE-2024-53907_4213/`（13 条证据）→ 隔离复核 **A 级，
    `confirmed_affected`**：reviewer 自建 4.2.13/4.2.17 venv，`"<"*n + "a>"*n` 在
    n=1000/2000/4000/8000 分别 0.412 / 1.591 / 6.514 / 26.301 s（每翻倍约 4×，二次方），
    4.2.17 同 24 KB 在 50 轮上限处抛 `SuspiciousOperation`（0.334 s）；公共 `striptags`
    过滤器 25.603 s vs 0.342 s。verdict sha256 与保留包逐项复核 0 不匹配，`--apply`
    追加 1 vuln / 1 location / 1 review / 32 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-53907_4213_round7/`（verdict + NOTES + feeds +
    scripts + out + notes + 两个 venv 的 `utils/html.py`、`template/defaultfilters.py`
    与 METADATA，`preserved_sha256.txt` 24 项）；review 路径与候选行
    `disc2_8b86415747e9508ae2ac2940` 分别由 `persist_independent_verdicts_round7_*` /
    `apply_promoted_candidate_round7_*` 改写。reviewer 指出 OSV MODERATE 与 NVD/CISA-ADP
    7.5 HIGH 的标签差异（向量等价），并说明 4.2.17 在抛错前仍有至多 50 轮全串解析。
    基线 **118 / 89**（A 43 / B 75），possible 581、unknown 574、NA 1321。

26. django CVE-2024-53908（4.2.13，Oracle `HasKeyLookup.as_oracle` 把 lhs 参数拼进 SQL 文本）
    卷宗 `runs/verification/django_CVE-2024-53908_4213/`（13 条证据）→ 隔离复核 **A 级，
    `confirmed_affected`**：reviewer 自建 4.2.13/4.2.17 venv，compile-level 复现 payload
    `1, '$.foo') OR 1=1 --`：4.2.13 直接使用得到
    `JSON_EXISTS(1, '$.foo') OR 1=1 --, '$."foo"')`、params `[]`，经公开入口
    `QuerySet.filter(HasKey(Value(payload), 'foo'))` 同样内联；4.2.17 为
    `JSON_EXISTS(%s, '$."foo"')`、params 该 payload。`__` 控制路径（`value__has_key`、
    嵌套 `KeyTransform`、带引号 rhs）两版 SQL/params 逐字节相同。`compare_runs.py` 9/9
    断言通过。verdict sha256 与保留包逐项复核 0 不匹配，`--apply`（2026-10-24T00:10:17Z）
    追加 1 vuln / 1 location / 1 review / 32 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-53908_4213_round8/`（verdict + NOTES + feeds +
    scripts + out + notes + 两个 venv 的 `db/models/fields/json.py` 与 METADATA，
    `preserved_sha256.txt` 25 项）；候选行 `disc2_d997111c20cf6d0610292215` 由
    `apply_promoted_candidate_round8_*` 改写（review 直接指向保留包 verdict，无需 repoint）。
    reviewer 限制：无真实 Oracle 实例（compile-level 明确允许）、`oracledb` 仅以别名满足
    `cx_Oracle` 导入、tag 签名无法本地校验（改用 `git ls-remote`）、5.0/5.1 只查祖先未执行。
    基线 **119 / 90**（A 44 / B 75），possible 580、unknown 574、NA 1321。

27. django CVE-2024-45231（4.2.13，密码重置在邮件后端持续失败时泄漏地址是否存在）
    卷宗 `runs/verification/django_CVE-2024-45231_4213/`（13 条证据）→ 隔离复核 **A 级，
    `confirmed_affected`**：reviewer 自建 4.2.13/4.2.16 venv，用
    `django.test.Client(raise_request_exception=False)`、`DEBUG=False` 走真实
    `PasswordResetView`：失败后端下 4.2.13 对**存在且激活**的地址返回 **HTTP 500**
    （`ValueError: FailingEmailBackend is doomed to fail.`），对不存在/未激活/无可用密码的
    地址返回 302；4.2.16 四类全部 302，且仅存在地址产生 1 条 ERROR
    `Failed to send password reset email to 1`。改用真实 SMTP（127.0.0.1:1 关闭端口）仍
    复现 500 vs 302；locmem 对照两版全 302，证明差异由发信失败触发。位置
    `django/contrib/auth/forms.py` `PasswordResetForm.send_mail` 第 317 行
    `email_message.send()`（方法 295-317），入口 `password_reset` URL →
    `PasswordResetView.form_valid` → `save()` → `get_users()`。verdict sha256 与保留包
    逐项复核 0 不匹配，`--apply`（2026-10-24T00:16:15Z）追加 1 vuln / 1 location /
    1 review / 32 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-45231_4213_round9/`（verdict + NOTES + scripts + out
    + 两个 venv 的 `contrib/auth/forms.py` 与 METADATA，`preserved_sha256.txt` 36 项）；
    候选行 `disc2_00c12ead68ae4b95c2b982e6` 由 `apply_promoted_candidate_round9_*` 改写。
    reviewer 指出 NVD 描述把**已修复版本**写成 “discovered in”、GHSA CVSS 3.1 3.7（AC:H）
    与 NVD 5.3（AC:L）标签差异、Django 自评为 low；GitHub 仓库级 advisory 页匿名 404。
    基线 **120 / 91**（A 45 / B 75），possible 579、unknown 574、NA 1321。

28. django CVE-2025-64459（4.2.13，`Q`/`QuerySet` 的 `_connector` 关键字参数被字典展开
    带进 SQL 连接符）卷宗 `runs/verification/django_CVE-2025-64459_4213/`（14 条证据）→ 隔离复核
    **A 级，`confirmed_affected`**：reviewer 自建 4.2.13/4.2.26 venv，先以 sha256 确认 PyPI
    4.2.13 的 `query_utils.py`/`query.py`/`where.py` 与 tag commit 3bf46e2e 的 blob 逐字节一致，
    再跑红/绿：4.2.13 `filter(**{"name":"Alice","id":999,"_connector":" OR 1=1 OR "})` 生成
    `WHERE ("id" = %s  OR 1=1 OR  "name" = %s)`、params 仅 `[999,"Alice"]`，返回全部 3 行
    （合法 AND 查询 0 行）；`exclude()` 同载荷返回 0 行、`get()` 抛 `MultipleObjectsReturned`
    （匹配 3 行）、`Q(_connector="evil")` 被接受。4.2.26 同调用在构造 SQL 前抛
    `TypeError: The following kwargs are invalid: '_connector'`，`Q(_connector="evil")` 抛
    `ValueError: _connector must be one of 'AND', 'OR', 'XOR', or None.`，合法查询不变。位置
    `django/db/models/query_utils.py` `Q.__init__` 48-53（入口 `query.py`
    `_filter_or_exclude_inplace` 1457-1461，sink `sql/where.py` 171-172），4.2.x 修复
    `59ae82e6…` + 配套 `279f8b95…`（4.2.26，tag `0dfd59e2…`）。verdict
    `runs/independent/django_CVE-2025-64459_4213_round10/verdict.json`，`--apply`
    （2026-10-24T00:23:13Z）追加 1 vuln / 1 location / 1 review / 33 evidence / 1 status。
    保留包 18 件（verdict + NOTES + reproduction 三件 + fetch 五件 + 两个 venv 的三份 ORM
    文件与 METADATA，`preserved_sha256.txt` 全匹配）；候选行
    `disc2_d791407a54d5b84b33a8db28` 由 `apply_promoted_candidate_round10_*` 改写。
    reviewer 指出 GHSA/OSV 的 4.2 分支范围写作 introduced 0（枚举到 1.0.1）而 NVD/PYSEC
    从 4.2 起、Django 政策称 "high"、GHSA 漏列实际拦截 `filter(**dict)` 的配套提交
    `279f8b95…`、GitHub API 的 `cvss_v4` 为 null；限制为仅 SQLite、未跑全量测试。
    基线 **121 / 92**（A 46 / B 75），possible 578、unknown 574、NA 1321。

**未做（留给后续，别视为已完成）**
- 50 库冻结缺口：**46 frozen / 2 rejected（hyper、Newtonsoft.Json 的 legacy 目标）/ 2 未选版**
  （nlohmann/json、openssl/openssl）。
- （以下为历史节点，最终状态见 §4）6 个 legacy `documented_exception` 目标里，netty/guzzle 已升级；protobuf 已定新目标
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
- 2 仓库未选版（Catalog 已验证漏洞为 0；不得编造 tag/commit；先补正样本再选版）。
- 574 unknown 中可能与 SHA 相关的候选未定向核验；两个未选版仓库的 13 条候选按先选版处理。
- `PASS_KNOWN_SWEEP=0/50`（需对固定 SHA 两轮独立检索均无新增「相关」候选，不只是无新增提升）。
- 51 条 grade A（含 rexml/django 39330/django 39329/django 38875/django 41989/django 39614/django 41991/rack/libexpat/phoenix 56812/guzzle 67339/gin 29401/protobuf 7254/grpc 1428/cJSON 53154/cJSON 50472/cJSON 57052/gitea hg5r/gitea 7wvc/django 32873/django 57833/django 59682/django 48432/django 64460 等），其余 live 正样本为 B 级静态验证。
  无 Agent 评测运行；运行时网络隔离尚未由 harness 实施（`network_policy=off` 只是声明）。
  `manifest.source_cutoff_date=null` 未复核。
- 审计导出是字符串级控制：不含 advisory ID 的修复说明/外链仍可能存在。另：collector 的泄漏扫描只匹配
  `CVE-`/`GHSA-`，不匹配 `GO-`/`RUSTSEC-`/`EEF-` 等 ID（gin 的 CHANGELOG.md 含 4 个 `GO-` 条目而未被计数，
  该文件整体被审计导出排除，故剩余 ID 仍为 0；后续仓库需注意同类漏检）。

## 4. 下一步优先级

1. **选版闭环已覆盖 48 个目标：46 frozen / 2 rejected（2026-10-24）**。近期完成闭环的证据先行案例：
   netty 4.1.137.Final、guzzle 7.14.1、echo v4.15.2、axios v1.19.0、gin v1.9.0、protobuf v3.25.4、
   grpc v1.52.0（独立审查者 CMake/Ninja 构建 `libgrpc.a` + 消费者链接运行后 accept）。历史记录：
   gin v1.9.0（CVE-2023-29401）已完成漏洞 A 级复核 → promote →
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
   不再尝试「改成最新版」。禁止直接把 tag 改成最新版。`source_cutoff_date` 已复核：数据内没有
   2026-10-21 之后发布的披露，但 coverage 截止不统一（rack 写 10-22，另 5 仓库 pass 4 在 10-22 运行），
   字段保持 null，见 `runs/cutoff_verification_2026-10-24/`。
   phoenix 可作为「旧 tag 被 4 年规则拒绝 → 在更新稳定 tag 上重新取证」的完整模板。
2. **剩余 2 个未选版仓库**：nlohmann/json 与 openssl/openssl。规则是先补至少一条 B/A
   `confirmed_affected` 再选版，禁止先选版本后补证据。已把两者全部 13 条 OSS-Fuzz OSV 记录
   （json 3 条、openssl 10 条）的 GIT 窗口与稳定 tag 做祖先映射
   （`runs/unselected_repo_evidence_2026-10-24/`，`check_windows.py` 可复现）：**0/13 个窗口内有稳定 tag**；
   凡从 `introduced` 之后可达的稳定 tag 全部已包含 `fixed` 提交——即没有稳定版本是在漏洞窗口内发布的。
   因此既拿不到「证据先行的受影响快照」，这些记录也不能给修复后 tag 提供正样本，维持 `needs_selection`，
   不得编造 tag/commit。解锁路径见该目录 README（ECOSYSTEM 版本区间含稳定 tag 的新 advisory、
   fix 落在两次发布之间的窗口、或有源码级对应的下游受影响版本）。
   rexml 是该流程的模板（`runs/verification/rexml_CVE-2025-58767/`）。
   `data/snapshot_proposals.jsonl` 现仅剩 2 条 `no_proposal` 行。
   **sinatra 第一轮已判负**：v4.1.1 + CVE-2025-61921 的独立复核用 MRI 2.5.9–3.2.0 与真实 gem 实测
   `split(/\s*,\s*/)` 为线性（正对照 `/^(a|a)*$/` 能测出指数），判 `not_affected`，未写任何数据行
   （`runs/verification/sinatra_CVE-2025-61921_v411/ROUND.md`）。改用 v4.0.1（`7dc5940e…`，2025-05-24，
   该树无 `host_authorization`）上的 CVE-2024-21510（X-Forwarded-Host 开放重定向，4.1.0 修复）。
3. **处理 unknown（现 574 行，其中 549 条是 2026-10-24 补入的无证据 unknown）**：范围/分支半程已完成并落地——`triage_range_scope.py` v1.1 对 1201 条
   unknown 生成提案（`runs/triage_range_scope_2026-10-23/proposals_v1_1.jsonl`），经独立审计
   （`runs/triage_range_scope_2026-10-23/audit/AUDIT.md`，568 条可执行提案 0 分歧、47 条抽样复核）后
   仅应用 `not_affected_range`：406 行 → `confirmed_not_affected`（版本区间判定，不声称祖先关系；
   见 `DISPOSITION.md`）。**未应用的 42 条 `out_of_scope_product` 全部保留 unknown**（审计判其归属规则不成立，
   CVE-2022-40281 是疑似假阴性）。当时剩余 1257 条 unknown 需要源码/差异级定向核验，相关但未过 B/A
   门槛的保留 `unknown`（不能判无效）。所有决策写回 `snapshot_candidate_triage.jsonl`。
   2026-10-24 追加：`triage_range_scope.py --include-untriaged` 对从未有 triage 行的候选生成 1662 条
   提案（`runs/triage_untriaged_2026-10-24/proposals.jsonl`），独立审计（`audit/AUDIT.md`）判
   280/281 条 `not_affected_range` 可应用、1 条 aspnetcore 实际落在受影响区间；实际只插入 **275**
   条（再剔除 5 条 actix monorepo 版本基准错误的行），未 triage 候选 887 → **592**，再补 5 条 actix crate 版本修正行 → **587**，aspnetcore 争议行改写为 `possible_affected` → **586**。
   另有 GIT 祖先判定（48 条，`runs/triage_git_ancestry_2026-10-24/`）：独立审计判 47 条可应用、
   1 条（OSV-2025-657）祖先规则不成立但结论另需代码级证据，已落盘 47 条 → unknown **748**。
   该库的 discovery_v3 仓库 advisory 解析已补入生成器：`runs/triage_v3_advisories_2026-10-24/`
   独立审计 119/119 CONFIRMED、verdict APPLY（exclude 为空），12 条 `not_affected_range` 已落地
   （7 条改写 + 5 条新增，unknown → 741）。其中 6 条依赖 registry/owner 前缀包的归属判定，
   严格字面口径下应退回 unknown，已在 LIMITATIONS 与批次 README 中声明。
   2026-10-24 低侧证明批次：`triage_range_scope.py` 加入与「高于每条上界」对称的「低于每条下界」证明
   （GHSA/OSV 65 条、NVD CPE 12 条）。两个独立审计批次判 56/65 与 9/12 可应用，共写入 **65** 行
   （33 改写 + 32 新增，确认 unknown → 708）。apply 后实测：562 条候选无 triage 行，其中 **549** 条属已选版
   仓库、13 条属两个未选版仓库。审计同时暴露并修掉了 4 个
   生成器缺陷（空合取 clause、`;` 分支、裸前导下界版本、exact-CPE 被当作下界）；随后为复核既有排除又修了
   4 个（`=` 等值 clause 双侧有界；不可比记录不得否决；粗粒度副本不得否决精确副本；
   排他上界包含性——OSV `fixed`/`limit`、NVD `versionEndExcluding`，快照恰等于修复版本即排除），
   单测 100 → **117** 项 OK。
   对 693 条既有范围行的复现复核（`runs/triage_strict_recheck_2026-10-24/`，默认 + strict 两种模式）：
   首轮默认 690/693、3 possible；第三个修复（`runs/triage_coarse_dup_2026-10-24/`）后
   **默认 693/693 仍提出同样排除、0 indeterminate、0 possible**；strict 689/693，差的 4 条是跨产品兄弟包
   （`openssl-src`、`jquery-rails` ×2、`DisCatSharp`，默认模式全为 NA）。
   3 条 rack 的根因是 `discovery_v3` 的 `vulnerable_version_range` 是 GitHub 扁平化渲染
   （`>= 0.4` / `>= 1.3.0` / `All`），修复版本在单独的 `patched_versions`；现在仅当同 advisory 的 OSV 副本
   给出完全相同的修复集合时丢弃该冗余投票，不据此构造边界。7 条均未改数据，
   逐条清单见上述两目录 README / `summary.json`。
   上界包含性修后对 1257 条 unknown 重跑得 63 条排除提案（46 条同前一批），新增 **17** 条
   （gitea v1.25.5 14、curl CVE-2023-38039、gin v1.9.0、plug v1.19.2），已打包
   `runs/triage_fixed_release_2026-10-24/proposals.jsonl` 送独立审计，**未应用**。
   随后补全漏斗：为已选版仓库内 549 条从未有 triage 行的候选追加 `unknown` 行
   （`runs/triage_untriaged_unknown_2026-10-24/`，只追加、不覆盖已应用决策），
   triage 2064 → **2613**、unknown 708 → **1257**，draft 校验仍 0 error / 49 warning。
   随后三批独立审计落盘：unblocked 36/46 CONFIRMED、fixed-release 17/17、GIT 10/12，共写 63 行；
   又撤回 vite/flask 2 行（裸版本读法被证伪），NA 1212 → **1273**、unknown 1257 → **1196**。
   全量复现复核（`runs/triage_range_recheck_full_2026-10-24/`）对 817 条范围排除：默认模式 **817/817**、
   strict 812/817（5 条跨产品兄弟包，含 spring-framework 的 spring-security 命中）。
   OSV-by-alias 批次（`runs/osv_alias_2026-10-24/`，四轮抓取 230 条记录）为 105 个无结构化证据的候选取得
   本仓库记录：43 条排除提案经独立审计 42 CONFIRMED / 1 REJECTED / 0 INCONCLUSIVE，42 条已落盘
   （被拒的 cJSON CVE-2023-26819 行保持 unknown，审计据 fix commit `a328d65a` 首次出现于 v1.7.19
   认为该 tag 可能实际受影响，列为正向复核优先项；该优先项已于 2026-10-24 做源码级复核：
   `runs/verification/cjson_CVE-2023-26819_v1716/` 证实修复提交不在 v1.7.16 祖先链、64 字节
   栈缓冲仍在，ASan/UBSan 实测 63 字符边界导致的长数字 `parse_error`，但无越界/DoS，故不升级为
   正样本、该行仍 unknown）、51 条区间命中已移入 `possible_affected`、
   9 条仍不可判定，其余 212 个候选无可获取的版本证据。
   随后把全量复核中 524 条仍 unknown 的 `possible_affected_range` 提案统一落盘
   （`runs/data_fixes/apply_remaining_possible_2026-10-24.py`，从提案证据重走 membership、
   跳过撤回 advisory 1 条、抽查 6 条核对区间）：**523** 条移入 possible。此后 5 条 cJSON v1.7.16
   候选经独立复核升为 `confirmed_affected`（CVE-2023-53154 3 条、CVE-2023-50472 2 条，见下），
   另 3 条重复 discovery 行（CVE-2023-50471 1 条、CVE-2024-45490 2 条）按同快照既有 A/B 记录链接为
   `confirmed_affected`（`runs/data_fixes/link_duplicate_candidates_to_verified_2026-10-24.py`）；
   2026-10-24 又有 4 条 cJSON v1.7.16 候选（CVE-2025-57052）经独立 A 级复核升为 `confirmed_affected`。
   CVE-2016-10749 的 NA 提案经隔离审计判 **REJECTED**（advisory 触发串已死，但快照仍有同一函数的
   另一条越界读，即已确认的 CVE-2023-53154），未落盘，该行保持 `possible_affected`；
   见 `runs/na_proposal_cjson_CVE-2016-10749_2026-10-24/audit_verdict.json`。
   该步骤完成时 unknown **574**、possible_affected **578**、confirmed_affected **112**、pending_relevant_triage **1152**（后续轮次已推进，见 §2 的现算值）。
   另将 817 行复核旁路产生的 8 条 unknown 行 NA 提案打包
   （`runs/triage_unknown_na_2026-10-24/`）送独立审计：**6 CONFIRMED / 2 REJECTED / 0 INCONCLUSIVE**，
   6 条（symfony v5.4.45 1、django 4.2.13 2、netty-4.1.137.Final 3）已落盘，NA 1315 → **1321**；
   两条 tomcat `below_lower` 被拒（证明与同源兄弟包 `tomcat-embed-core` 的下界矛盾），
   排除结论本身成立但需逐分支混合证明，生成器对称规则尚不能表达，两行保持 unknown。
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

# 单测（v031/tests 不是包，discover 必须指定 -t，否则 ImportError；当前 117 tests OK）
.venv/bin/python -I -m unittest discover -s v031/tests -t v031/tests -v
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