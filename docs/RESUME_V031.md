# v0.3.1 续跑与交接

> **新对话请先读 `../HANDOFF_V031.md`**（自包含交接文档，含基线/未做清单/优先级/命令/坑）。

工作主记录：`../WORK_LOG.md`；升级对账：`../UPGRADE_REPORT.json`；
v0.3.1 规范：`../v031/WORKFLOW.md`；候选漏斗：`data/snapshot_candidate_triage.jsonl`。

## 当前状态（2026-10-23，含 rexml / django / rack / libexpat / phoenix 更新）

- 数据集根目录：`/home/luchitong/work/repo-vuln-50-v031`；源 v0.3 目录
  `/home/luchitong/work/repo-vuln-50-v03` 未被写入。
- `manifest.status=draft`，`dataset_version=0.3.1`，`source_cutoff_date=null`，`freeze_timestamp=null`。
- 九张主表行数：50 repositories / 80 snapshots / 78 vulnerabilities / 78 locations /
  1951 evidence / 78 reviews / 2626 candidates / 50 discovery_coverage / 60 snapshot_vulnerability_status。
- 选举：23 个目标覆盖 23 仓库（各一稳定 tag，均有 confirmed_affected）；独立审查后
  **17 frozen / 6 proposed**（6 个 proposed 均为 review reject 的 legacy `documented_exception`）；
  27 仓库 `needs_selection`（`evaluation_snapshot_id=null`）。
  冻结详情见 `v031/reports/SELECTION_FREEZE_2026-10-22.md`、
  `v031/reviews/selection_review_2026-10-23.jsonl`、`selection_review_django_2026-10-23_r2.jsonl`、
  `selection_review_rack_2026-10-23.jsonl`、`selection_review_libexpat_2026-10-23.jsonl` 与
  `selection_review_phoenix_2026-10-23.jsonl`。
- 已知正样本：60 条 live `confirmed_affected`（55 B + 5 A），分布在 23 个已选快照。
  A 级为 ruby/rexml v3.4.1 CVE-2025-58767、django 4.2.13 CVE-2024-39330、rack v3.1.13
  CVE-2025-46727、libexpat R_2_6_2 CVE-2024-45490 与 phoenix v1.8.8 CVE-2026-56812，
  均有独立 reviewer red/green 复现。旧 django 3.0.2 的 8 条、rack 2.2.3 的 2 条、
  libexpat R_2_4_4 的 7 条与 phoenix v1.6.13 的 2 条状态行已归档，不计入。
- 候选漏斗：`snapshot_candidate_triage.jsonl` 1577 行（23 个已选仓库）：
  `confirmed_affected=71` / `confirmed_not_affected=303` / `unknown=1203`。
  rexml/django/rack/libexpat/phoenix 的目标漏洞已置 `verified` 并补 triage 行；rexml 其余 8 条、
  libexpat 旧目标 7 条与 phoenix 新快照 4 条已按 OSV 修复区间 + 代码级核对/祖先关系判为不适用；
  django 新快照其余 162 条、rack 新快照其余 49 条、libexpat 新快照其余 135 条与 27 个未选仓库的
  1049 条候选仍未定向核验。
- 覆盖：`discovery_coverage` 50 条全部 `NEEDS_REVIEW`；旧全历史归档于
  `data/legacy_discovery_coverage_v03.jsonl`。rexml/django/rack/libexpat/phoenix 的 coverage 声明已注明
  各自已确认正样本，未声明 sweep 完成。
- 源码导出：23/23 `exported`，完整 tracked tree、无 `.git`、`missing_from_archive_count=0`；
  P6 审计导出 23/23（`build_audit_exports/1.1`，排除 130、替换 10），剩余 advisory ID 0。
- 仅 5 条动态复现已由独立 reviewer 完成（rexml/django/rack/libexpat/phoenix CVE-2026-56812，
  后者为 Node red/green harness，见 `runs/independent/phoenix_CVE-2026-56812_v188_round1/repro/`）；
  Agent 评测运行、运行时网络隔离均未发生。

## 入口

- `v031/WORKFLOW.md`：v0.3.1 全部 SOP 与发布门槛（P0–P8）。
- `v031/schemas/`：16 份 schema（新增 `snapshot_candidate_triage`/`snapshot_exports`/`snapshot_proposals`/
  `snapshot_audit_exports`）。
- `v031/scripts/upgrade_v03_to_v031.py`：只读 dry-run，`--apply --out` 写新目录。
- `v031/scripts/build_initial_triage.py`：用已有证据生成初始 `snapshot_candidate_triage.jsonl`。
- `v031/scripts/plan_snapshot_queue.py`：根据 triage 输出验证优先级队列。
- `v031/scripts/cost_report.py` + `cost_policy.json` + `v031/ledger/model_calls.jsonl`：费用汇总。
- 源 v0.3 的既有 `v03/`、迁移备份、`runs/`、`scratch/`、根 `schemas/`（v0.2 对照）只读保留。

## 重新生成 / 校验

```bash
cd /home/luchitong/work/repo-vuln-50-v031
.venv/bin/python v031/scripts/validate_dataset.py . --draft \
  --json-out v031/reports/VALIDATION_DRAFT.json
.venv/bin/python v031/scripts/validate_dataset.py .            # release 门槛
.venv/bin/python v031/scripts/plan_snapshot_queue.py . --out v031/reports/queue.json
.venv/bin/python v031/scripts/build_initial_triage.py . --checked-at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
.venv/bin/python -I -m unittest discover -s v031/tests -v
```

## 发布阻塞（v0.3.1 release 尚不成立）

1. 27 个仓库没有冻结 SHA（Catalog 已验证漏洞为 0，按规则不能自动选；不得编造 tag/commit）。
   其中 axios (v1.15.0) / OpenSSL (openssl-3.0.1) / sinatra (v3.0.3) 有历史 tag 快照但无 confirmed_affected。
2. 仅 16/23 已选目标 `frozen`；7 个因 tag 超过 4 年被审查拒绝，仍为 `proposed`（均为 legacy 目标）。
3. 1207 条 `unknown` + 27 未选仓库的 1049 条候选未完成相关性核验；其中相关疑点必须深入核验或保留
   draft，不能声称快照已知漏洞已全。`PASS_KNOWN_SWEEP` 需对固定 SHA 两轮零新增「相关」候选。
4. `manifest.source_cutoff_date=null` 未从采集日志复核。
5. 仅 4 条 grade A（rexml/django/rack/libexpat，独立 reviewer red/green 复现）；其余 56 条为 B 级静态验证。

## 下一步（按优先级）

1. 先处理 7 个审查拒绝目标：在更新稳定 tag 上取得 B/A 正样本后再提交新审查；禁止先改 tag 后补证据。
2. 为 27 仓库按 v0.3.1 规则补已验证正样本并选版冻结；rexml v3.4.1 已完成该闭环，可作模板
   （`runs/verification/` + `runs/independent/` + `promote_verified_rows.py`）；
   `snapshot_proposals.jsonl` 的 27 个仓库候选（120 tag）仍需源码级确认；禁止先选后补证据。
3. 对 1207 条 `unknown` 中可能与冻结 SHA 相关的候选做低成本定向核验（P4），未通过门槛的保留 pending。
4. 两轮独立快照限定检索、zero 新增相关候选 + 公开库与上游检索成功，才可声明 `PASS_KNOWN_SWEEP`。
5. 记录后续每个 LLM 调用的 stage/model/tokens/cost 到 `v031/ledger/model_calls.jsonl` 再跑 cost_report。

## 已知工具缺陷

- v0.3.1 starter `v031/schemas/vulnerabilities.schema.json` 的 GHSA 正则仍为 `[0-9A-Z-]`（大写限定），
  与 v0.3 starter 同源缺陷；已按 v0.3 的补丁改为 `[0-9A-Za-z-]`（改后 SHA256=efa419ad…，
  正则与 v0.3 已补丁版本逐字节一致）。补丁只改 schema，未动数据。
- `v03/scripts/validate_v02_reference.py`（v0.3 参考验证器）遇小写 GHSA 会误报，与 v0.3.1 数据无关。