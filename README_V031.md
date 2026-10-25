# RepoVuln-50 v0.3.1（由 v0.3 无损升级）

> 交接 / 续跑，请先读 **`HANDOFF_V031.md`**。
>
> **状态提示（2026-10-24）**：本 README 的「当前状态」段落写于 2026-10-23（当时 23 个已选快照、
> 60 条 live 正样本、1577 条 triage），此后 48/50 目标已选版、46 个 frozen、106 条漏洞行
> （32 A / 45 B，77 条在评测目标上）、triage 2613 行（unknown 1257）。请以 `HANDOFF_V031.md` §2
> 与 `LIMITATIONS_V031.md` §3 为准，不要引用下方旧数字。

本目录是 `/home/luchitong/work/repo-vuln-50-v03` 的 v0.3.1 无损升级产物。
源 v0.3 目录只读保留；升级复制的全部 9753 个源文件按文件逐一记录 SHA256 在 `UPGRADE_REPORT.json`。

## 与 v0.3 的关键变化

- **fixed-SHA 快照优先**：评测目标由「仓库级」收紧为「每库一个冻结 commit」。
- **候选相关性漏斗**新增 `data/snapshot_candidate_triage.jsonl`（零 LLM 规则优先）。
- 旧全历史 `discovery_coverage` 归档为 `data/legacy_discovery_coverage_v03.jsonl`，outcome 全部重置为
  `NEEDS_REVIEW`（不继承旧 PASS 作为快照完整性的保证）。
- `manifest.evaluation_policy = one_frozen_snapshot_snapshot_only_oracle`，`dataset_version=0.3.1`。

## 目录

| 路径 | 内容 |
|---|---|
| `data/` | 九张主表 + `evaluation_selection.jsonl` + `snapshot_candidate_triage.jsonl` + `snapshot_exports.jsonl` + `snapshot_audit_exports.jsonl` + `snapshot_proposals.jsonl` + `legacy_discovery_coverage_v03.jsonl` |
| `exports/` | 23 个已选目标的可复现完整源码导出（无 `.git`；tar.gz 与逐文件 SHA256 清单） |
| `v031/` | v0.3.1 工作流：`WORKFLOW.md`、`AGENT_PROMPT.md`、`docs/`、`schemas/`、`scripts/`、`tests/`、`cost_policy.example.json`、`reports/`、`ledger/` |
| `migration_backup_v02/` + `v03/` | v0.2 / v0.3 原始副本（只读保留） |
| `UPGRADE_REPORT.json` | 0.3.0→0.3.1 升级对账（9753 文件源哈希） |
| `cost_policy.json` | 费用策略配置（阈值，非实时强制） |
| `SELECTION_REPORT_V031.md` / `LIMITATIONS_V031.md` / `docs/RESUME_V031.md` | 本版交付说明 |

## 状态（2026-10-23）

- `manifest.status=draft`，`source_cutoff_date=null`，`freeze_timestamp=null`。
- 九张主表：50 repositories / 80 snapshots / 78 vulnerabilities / 78 locations / 1951 evidence /
  78 reviews / 2626 candidates / 50 discovery_coverage / 60 snapshot_vulnerability_status。
- 评测目标：23 个（每个一库、一个稳定 tag）；独立选版审查后 **17 个 frozen、6 个 proposed**
  （6 个均为 legacy `documented_exception` 目标；django 4.2.13、rack v3.1.13、libexpat R_2_6_2 与
  phoenix v1.8.8 已备正样本（phoenix 为 B + A 各一条）、完成导出与 P6 审计导出，并分别于 2026-10-23
  通过独立选版审查后冻结）；27 个仓库 `needs_selection`。详见 `v031/reports/SELECTION_FREEZE_2026-10-22.md`。
- 已知正样本：60 条 live `confirmed_affected`（55 B + 5 A），覆盖 23 个已选快照；另有 django 3.0.2
  8 条、rack 2.2.3 2 条、libexpat R_2_4_4 7 条与 phoenix v1.6.13 2 条旧快照状态行归档为历史证据，
  不计入 Oracle。
- 候选漏斗：2626 条 → 23 个已选仓库内 1577 条已 triage = 71 confirmed_affected（distinct 漏洞 60）/
  303 confirmed_not_affected / 1203 unknown；1049 条未 triage（全部属于 27 个未选仓库）。
- 动态复现：5 条（rexml CVE-2025-58767、django CVE-2024-39330、rack CVE-2025-46727、
  libexpat CVE-2024-45490、phoenix CVE-2026-56812，均有独立 reviewer red/green）；
  Agent 评测运行、运行时网络隔离仍未发生。
  23/23 已选目标有源码导出；其中 17 个 frozen，6 个仍为 proposed。

## 常用命令

```bash
cd /home/luchitong/work/repo-vuln-50-v031
.venv/bin/python v031/scripts/validate_dataset.py . --draft
.venv/bin/python v031/scripts/plan_snapshot_queue.py . --out v031/reports/queue.json
.venv/bin/python v031/scripts/build_initial_triage.py . --checked-at <ISO>
.venv/bin/python v031/scripts/freeze_snapshots.py . --jobs 3          # 23 个已选目标的确定性源码导出
.venv/bin/python v031/scripts/propose_missing_snapshots.py . --jobs 4 # 27 个未选仓库的 tag 候选
.venv/bin/python v031/scripts/build_selection_review_packets.py .     # 隔离审查包
.venv/bin/python v031/scripts/build_audit_exports.py .                # P6 去 advisory ID 的审计导出
.venv/bin/python v031/scripts/apply_selection_review.py . \
  --reviews v031/reviews/selection_review_2026-10-22.jsonl            # 默认 dry-run；加 --apply 冻结
.venv/bin/python v031/scripts/cost_report.py v031/ledger/model_calls.jsonl --budget-cny 500
.venv/bin/python v031/scripts/validate_dataset.py .        # release 门槛
```

说明：本工具包只做迁移/结构校验/排队/费用汇总，不含在线采集器、自动 PoC 或自动漏洞判定；
schema 通过不代表漏洞实存。