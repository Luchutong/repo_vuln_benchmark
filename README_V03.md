# RepoVuln-50 v0.3（由 v0.2 无损迁移）

本目录是 v0.2 数据集 `/home/luchitong/work/repo-vuln-50-v02` 的 v0.3 迁移产物。
源目录只读保留；迁移前的全部 JSONL 字节级备份在 `migration_backup_v02/data/`。

## 目录

| 路径 | 内容 |
|---|---|
| `data/` | 九张主表 + `evaluation_selection.jsonl` + 空的 `historical_snapshot_status.jsonl` |
| `v03/` | v0.3 工作流：`WORKFLOW.md`、`docs/`、`schemas/`、`scripts/`、`tests/` |
| `migration_backup_v02/` | v0.2 原始 data、scripts、schemas 副本 |
| `MIGRATION_REPORT.json` | 迁移前后行数、哈希、无损对账、schema 补丁 |
| `SELECTION_REPORT.md` | 50 个仓库的评测目标现状与选择依据 |
| `CATALOG_COVERAGE_REPORT.md` | 历史漏洞目录、2626 候选处置、检索盲区 |
| `ORACLE_REPORT.md` | 22 个目标快照上的版本真值 |
| `VALIDATION_REPORT.json` | 实际执行的校验、测试、阻塞 |
| `LIMITATIONS.md` | 完整性、证据、版本歧义与动态复现限制 |
| `WORK_LOG.md` | 全部工作记录（含本次迁移） |

## 状态

`draft`。22/50 个仓库有 `proposed` 评测目标，0 个冻结；`PASS_KNOWN_SWEEP=0/50`；
grade A 0 条；未解决候选 2114 条。详见 `LIMITATIONS.md` 与 `VALIDATION_REPORT.json`。

## 常用命令

```bash
cd /home/luchitong/work/repo-vuln-50-v03
.venv/bin/python -I v03/scripts/validate_dataset.py . --draft
.venv/bin/python -I -m unittest discover -s v03/tests -v
```
