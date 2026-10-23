# v0.3.1 数据契约 — Source-only Snapshot Audit

## 单位与分离

- **Repository**：50 个 `repo_id`；一库一正式评测 SHA（`snapshots.evaluation_target=true`）。
- **Ground truth**：`snapshot_vulnerability_status` 中 `confirmed_affected` 且关联同一 SHA 的 `locations`、A/B 级 `reviews`。它不是全部真漏洞的封闭全集。
- **Historical**：原有 `vulnerabilities`、`candidates`、历史 commits 和证据无损保留；不要求每个旧 Catalog 行在目标 SHA 写矩阵，也不强制新收无关历史 CVE 的深度字段。
- **Triage**：`snapshot_candidate_triage.jsonl` 一行对应一个候选和该库的正式 SHA。`confirmed_not_affected` 是对*该候选在该 SHA*的不适用判定，不能暗示快照其余部分安全。

## 与 v0.3 不同的 Schema

- `manifest.dataset_version=0.3.1`，`evaluation_policy=one_frozen_snapshot_snapshot_only_oracle`。
- 新 `snapshot_candidate_triage` 强制 `candidate_id`, `repo_id`, `snapshot_id`, `decision`, `basis`, `evidence_urls`, `review_method`, `checked_at`。
- `discovery_coverage.scope.mode=selected_snapshot_only`, `scope.evaluation_snapshot_id`, `coverage_mode=selected_snapshot_only`；两轮 `passes[-2:]` 应有 `new_relevant_candidate_count=0`，旧 `new_verified_count=0` 不再足以 PASS。
- 允许旧历史 `vulnerabilities` 存在但未在所选 SHA 有 `snapshot_vulnerability_status` 行；正样本行必须有版本级代码定位与独立 PASS 证据。

## Triage 有效决策

- `confirmed_affected`：必须关联正式 Catalog `vulnerability_id` 且对应 SHA 真值为 `confirmed_affected`。
- `confirmed_not_affected`：有源文件或可信受影响/修复范围及分支关系，且证据足以排除所选 SHA。
- `duplicate`：指向真实存在的其他候选 `canonical_candidate_id`，不重复深验。
- `out_of_scope`：因预先冻结的评测范围不包含该组件，附范围依据。不能把“难于分析”称为范围外。
- `possible_affected` / `unknown`：继续查证；不把缺少数据当成已排除。

## 费用与数据泄漏

`cost_policy.example.json` 是示例预算，不是已实现模型网关。`scripts/cost_report.py` 仅汇总实际日志。不提供历史 commit、fix diff、漏洞公告或裁决标签给受测 Agent；原始源码中非漏洞性文档是否包含未来信息须保持可审计清洗或说明。
