# LIMITATIONS — RepoVuln-50 v0.3 迁移后的真实边界

生成时间：2026-10-22T02:05:00Z；对应数据根目录：`/home/luchitong/work/repo-vuln-50-v03`。

本文件只列已经确认的缺口，不用“待完善”掩盖未完成项，也不把结构校验通过解释成漏洞验证通过。

## 1. 迁移完整性

- 九张主表行数不变：repositories 50、snapshots 75、vulnerabilities 73、locations 73、
  evidence 1839、reviews 73、candidates 2626、discovery_coverage 50、snapshot_vulnerability_status 73。
- `vulnerabilities/locations/evidence/reviews/candidates/discovery_coverage/snapshot_vulnerability_status`
  与 v0.2 源文件**字节级一致**（SHA256 见 `MIGRATION_REPORT.json`）。
- `repositories` 只新增 `evaluation_snapshot_id`（22 非空、28 空）；`snapshots` 只新增 `purpose`
  并改写 `evaluation_target`（22 个，无翻转）。所有原有字段值逐行比对未变。
- 原始 `data/*.jsonl` 已字节级备份在 `migration_backup_v02/data/`，备份 SHA256 与源目录相同。
- **源目录 `/home/luchitong/work/repo-vuln-50-v02` 未被写入**；迁移产物全部在新目录。
- 没有发生历史状态搬迁：`data/historical_snapshot_status.jsonl` 为空，因为 22 个旧评测目标全部保留。

## 2. 评测目标选择

- 50 个仓库中只有 22 个有评测目标，且全部是 v0.2 继承的 `proposed` 记录；**0 个 frozen**。
- 另外 28 个仓库 `evaluation_snapshot_id=null`：它们没有已验证漏洞；25 个只有默认分支 HEAD
  （`tag_or_release=null`），axios / OpenSSL / sinatra 另有带 tag 的历史快照（v1.15.0 / openssl-3.0.1 / v3.0.3），
  但同样没有 `confirmed_affected`。按 v0.3 规则“该 SHA 至少一条 B/A 已确认漏洞”，无法选择；
  按用户指示本轮不继续收集，因此保持 `needs_selection`，没有编造 tag 或 commit。
- 22 个已选目标虽然都有稳定 tag、完整语言扫描和同 SHA 正样本，但还没有完成 v0.3 要求的
  独立选版审查、构建可行性验证、防泄漏工作树导出，因此不能冻结。
- `leakage_controls` 全部为 `worktree_without_git_history=false`、`ground_truth_isolated=false`、
  `network_policy=uncontrolled`；这是迁移默认值，不是已经验证的隔离方案。
- `manifest.source_cutoff_date=null`：迁移指南要求从 `discovery_coverage` 和采集日志复核后填写，
  本轮只确认数据里的 `cutoff_date=2026-10-21`，没有把迁移日期当作披露截止日。

## 3. Catalog 与检索覆盖

- 73 条 Catalog 漏洞全部是 B 级：有修复 diff、根因代码、公告与独立复核，**没有任何 A 级动态红绿复现**。
  B 级不等于 PoC 已验证。
- 候选 2626 条中仍有 2114 条未解决（`in_validation` 503、`pending_location` 750、`pending_version` 861）；
  本次迁移没有推进或清理它们。
- 429 条 `rejected` 主要是“不在该仓库评测版本影响范围内”的范围判定，除 Django CVE-2021-35042 外
  大多没有代码级否证；逐条理由在 `runs/verification/*_snapshot_not_applicable/NOT_APPLICABLE.md`。
- 20 条已有独立 verdict 但未过提升门槛（8 条严重程度来源冲突、15 条独立证据不足、1 条 cvss=false），
  仍为 pending，没有被强行提升。
- `PASS_KNOWN_SWEEP = 0/50`：全部 `NEEDS_REVIEW`。末两轮 `new_verified_count=0` 只是机械计数，
  未解决候选没有解释完，覆盖面也没有独立复核，因此不声明完成检索。
- 已知盲区：curl CVE-2023-38546（8.3.0 受影响）未进入候选；NVD 只对部分仓库检索；
  50 个 repository advisory 拉取中 14 个为空列表；OSV 端点数量不等于独立来源数量。
- 披露截止为 2026-10-21，2026-10-22 当日新披露不在数据内。

## 4. Oracle 与真值

- 正式 Oracle 只覆盖 22 个评测快照，73 行全部 `confirmed_affected`；没有
  `confirmed_not_affected`、`unknown`、`out_of_scope` 行。
- “没有 unknown”不等于“该 SHA 已证明无其他漏洞”：22 个仓库的 Catalog 恰好等于已提升漏洞集合，
  而未收录漏洞受第 3 节检索缺口限制。
- 28 个未选仓库在 Oracle 中没有任何行，它们是 `needs_selection`，不是“无漏洞”。
- 20 条 pending 候选、rack CVE-2025-46727 / CVE-2025-61772 的材料没有进入 Oracle；
  其中 rack 两条已完成档案与代码/版本核验，但独立复核未完成，不能按 B 级收录。

## 5. 工具与 Schema 兼容性

- **starter schema 缺陷**：`v03/schemas/vulnerabilities.schema.json` 的 GHSA 正则使用 `[0-9A-Z-]`，
  拒绝真实 GHSA 编号中的小写字符。已将补齐为 `[0-9A-Za-z-]`，改前/改后 SHA256 与原因记录在
  `MIGRATION_REPORT.json.schema_compatibility_patch`；没有改动任何数据。
- **参考验证器缺陷**：`v03/scripts/validate_v02_reference.py` 第 108 行把原始 `vulnerability_id`
  与已大写的别名集合比较，对 9 条小写 GHSA ID 误报“ID missing in alias list”。
  `v03/scripts/validate_dataset.py` 使用 `str(vid).upper()`，结果 0 errors。未修改该参考脚本。
- 校验器只做结构/引用/证据声明检查，不验证漏洞真实性、修复版本正确性或检索完整性。

## 6. 评测运行

- 数据目录中不存在 `agent_findings.jsonl` / `adjudications.jsonl`，本轮没有任何审计 Agent 运行结果，
  因此没有已知 TP/FP/novel 统计，也没有 Macro Known Recall。
- `evaluation_selection` 未冻结，工作树导出（去 `.git`、去未来历史）尚未生成；
  不能把当前数据目录直接交给被测 Agent。

## 7. 发布状态

- `manifest.status=draft`；严格模式下 132 个结构/门槛错误（28 仓库无目标、22 选择未冻结、
  50 仓库无 PASS_KNOWN_SWEEP、manifest 三项、selection 22≠50）。
- 在 B1–B5 关闭前，本数据集不能发布为 v0.3 release；本报告与 `VALIDATION_REPORT.json`
  如实记录这些阻塞，不做虚假 PASS 声明。
