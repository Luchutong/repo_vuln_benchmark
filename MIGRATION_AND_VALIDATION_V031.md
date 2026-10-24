# MIGRATION_AND_VALIDATION_V031 — 升级与校验报告（v0.3.1）

对应数据根目录：`/home/luchitong/work/repo-vuln-50-v031`。机器可读者：`UPGRADE_REPORT.json`、
`v031/reports/VALIDATION_DRAFT.json`、`v031/reports/VALIDATION_RELEASE.json`。

> 本文件记录 **升级当时（2026-10-22）** 的基线；§2/§3 的数字是历史值，不随后续工作更新。
> 当前计数以 `HANDOFF_V031.md` §2、`CANDIDATE_FUNNEL_V031.md` 与 `v031/reports/VALIDATION_*.json` 为准。

## 1. 无损升级（0.3.0 → 0.3.1）

- 用 `v031/scripts/upgrade_v03_to_v031.py`（dry-run 后再 `--apply`）从 `/home/luchitong/work/repo-vuln-50-v03`
  复制出本目录；源 v0.3 只读未写。
- 复制 9753 个源文件，逐文件记录 SHA256（`UPGRADE_REPORT.json.source_sha256`），`source_unchanged=true`。
- `no_new_triage_or_verification_labels=true`：升级本身不新增任何漏洞真值标签。
- 变更项：`manifest.dataset_version=0.3.1`、`evaluation_policy=one_frozen_snapshot_snapshot_only_oracle`；
  新增 `data/snapshot_candidate_triage.jsonl`（空→由 P3 规则填充）；旧 `discovery_coverage` 归档为
  `data/legacy_discovery_coverage_v03.jsonl` 且 50 条 outcome 全部重置为 `NEEDS_REVIEW`（不继承旧 PASS）。

## 2. 真实数据基线（复算，非沿用上报值）

- 九张主表：**50 repositories / 75 snapshots / 73 vulnerabilities / 73 locations / 1839 evidence /
  73 reviews / 2626 candidates / 50 discovery_coverage / 73 snapshot_vulnerability_status**。
- 注意实际漏洞为 **73**（用户上报基线为 72）：差异来自逐行复算，v0.3 起即含该条已提升漏洞；
  本版没有改动任何漏洞行。
- 评测目标：22 `proposed`（22 仓库，各一稳定 tag，均有 confirmed_affected），0 frozen；28 仓库
  `needs_selection`。
- 已知正样本：73 条 `confirmed_affected`（全部 B 级），分布在 22 个已选快照。

## 3. P3 候选相关性漏斗（零 LLM）

- `data/snapshot_candidate_triage.jsonl`：1568 行 = 83 confirmed_affected（distinct 漏洞 73）/
  410 confirmed_not_affected / 1075 unknown。另 1058 条在未选仓库，无 triage 行。
- 生成脚本 `v031/scripts/build_initial_triage.py`，决策全部取自既有证据（candidate.status/reason/source_urls/
  Oracle），未调任何模型、未编造。
- 队列 `v031/reports/queue_P3.json`：P0_SELECT_SNAPSHOT 1058 / DONE 83 / ARCHIVE 410 / P1_REVIEW 1075。

## 4. 校验结果

| 模式 | 命令 | errors | warnings | 判定 |
|---|---|---|---|---|
| draft | `validate_dataset.py . --draft` | **0** | 50 | 结构与引用一致，可作 draft 继续 |
| release | `validate_dataset.py .` | **253** | 50 | 未达发布门槛，如实记录 |

- 50 条 warnings 全部为「coverage <repo>: N unresolved candidates (disclose limitations)」与
  grade-A<60% 提示。
- 253 条 release errors 分类：
  - coverage ×150（快照限定覆盖未跑 / 缺所选快照 ID / NOT PASS_KNOWN_SWEEP）
  - repo ×56（28 仓库无评测快照 + 无 catalog 漏洞）
  - selection ×22（目标未 frozen）
  - snapshot triage ×22（各已选快照仍有 unknown/possible 未核验）
  - manifest ×3（非 release / 缺 freeze_timestamp / cutoff 未复核）
  - evaluation_selection ×1（22 ≠ 50）
  - 即全部为发布门槛阻塞，**无结构损坏或引用错误**。

## 5. 测试

- v0.3.1 单测：`python -I -m unittest discover -s v031/tests -v` → **Ran 9 tests, OK**。
- v0.3 回归验证器与历史数据不受影响（见 v0.3 的 `v03/reports`）。

## 6. schema 补丁

- v0.3.1 starter `v031/schemas/vulnerabilities.schema.json` GHSA 正则退回收大写限定，已按 v0.3 补丁改为
  `[0-9A-Za-z-]`（改后 SHA256=efa419ad…）。只改 schema，未动数据。详情见 `LIMITATIONS_V031.md` §1。

## 7. 费用

- `cost_report.py v031/ledger/model_calls.jsonl --budget-cny 500` → 0 记账调用 / ¥0 实测 /
  untracked=DO NOT ASSUME ZERO。本版迁移与漏斗全部离线规则，无模型成本；`cost_policy.json` 为阈值配置，
  非强制网关。见 `v031/reports/COST_REPORT.json`。