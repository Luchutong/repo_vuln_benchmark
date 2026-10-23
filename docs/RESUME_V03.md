# v0.3 续跑与交接

工作主记录：`../WORK_LOG.md`；迁移对账：`../MIGRATION_REPORT.json`；
结构校验：`../VALIDATION_REPORT.json`；v0.3 规范：`../v03/WORKFLOW.md`。

## 当前状态（2026-10-22）

- 数据集根目录：`/home/luchitong/work/repo-vuln-50-v03`；源 v0.2 目录
  `/home/luchitong/work/repo-vuln-50-v02` 未被写入。
- `manifest.status=draft`，`source_cutoff_date=null`，`freeze_timestamp=null`。
- 九张主表：50 repositories / 75 snapshots / 73 vulnerabilities / 73 locations /
  1839 evidence / 73 reviews（全 B）/ 2626 candidates / 50 discovery_coverage /
  73 snapshot_vulnerability_status。
- 评测目标：22 个 `evaluation_target=true`（覆盖 22 个仓库），全部 `proposed`；
  28 个仓库 `evaluation_snapshot_id=null`（`needs_selection`）。
- 候选：503 in_validation / 750 pending_location / 861 pending_version / 83 verified
  （其中 10 条是别名重复行）/ 429 rejected；未解决 2114。
- 覆盖：50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；grade A 0 条。
- 动态复现、Agent 评测运行、工作树导出均未发生。

## 入口

- `v03/WORKFLOW.md`：v0.3 全部 SOP 与发布门槛。
- `v03/schemas/`：13 份 schema（含 `evaluation_selection`、`manifest`）。
- `v03/scripts/migrate_v02_to_v03.py`：只读 dry-run，`--apply --out` 写新目录。
- `v03/scripts/validate_dataset.py`：`--draft` 结构校验；不带 `--draft` 为发布门槛。
- `v03/scripts/plan_selections.py`：列出每仓已存 snapshot 与正样本计数，不做自动选择。
- `migration_backup_v02/`：`data/`（原始 JSONL 字节副本）、`scripts_v02/`、`schemas_v02/`。
- 根目录 `schemas/` 仍是 v0.2 原样，供 `validate_v02_reference.py` 对照。

## 重新生成 / 校验

```bash
cd /home/luchitong/work/repo-vuln-50-v03
.venv/bin/python -I v03/scripts/validate_dataset.py . --draft \
  --json-out /tmp/v03-draft.json
.venv/bin/python -I v03/scripts/validate_dataset.py .            # release 门槛
.venv/bin/python -I -m unittest discover -s v03/tests -v
.venv/bin/python -I scripts/validate_dataset.py . --draft       # v0.2 回归
```

## 发布阻塞

1. 28 个仓库没有评测目标（Catalog 已验证漏洞为 0，不能按规则自动选）。
2. 22 个目标全部 proposed，缺 `reviewed_by`/`selection_reviewed_at`/`approval_evidence_urls`/
   `frozen_at`，`leakage_controls` 全为 false/uncontrolled。
3. `PASS_KNOWN_SWEEP=0/50`，2114 条候选未解决。
4. manifest 不是 release，`source_cutoff_date` 未复核填写。
5. `evaluation_selection` 22 != 50。

## 下一步（按优先级）

1. 若要继续：先为 28 个仓库补已验证正样本，再按 v0.3 规则选版；禁止先选版本后补证据。
2. 为 22 个 proposed 目标补构建可行性、去 `.git` 工作树导出和独立选版审查，之后才能 `frozen`。
3. 继续处理 2114 条未解决候选；任何新提升仍需独立 reviewer 与 `promote_verified.py` 门槛。
4. 只有两轮零新增已验证、公开库与上游/历史检索成功且候选已解释，才可声明 `PASS_KNOWN_SWEEP`。
5. 动态红绿测试未安排；没有它 grade A 不成立。

## 已知工具缺陷

- `v03/scripts/validate_v02_reference.py:108` 用原始 `vulnerability_id` 与已大写别名集合比较，
  对小写 GHSA 误报 9 条；`v03/scripts/validate_dataset.py` 无此问题。
- starter `vulnerabilities.schema.json` 的 GHSA 正则已补小写字符，原因与哈希记录在
  `MIGRATION_REPORT.json.schema_compatibility_patch`。
