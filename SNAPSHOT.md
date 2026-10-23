# 数据进度快照

- 分支：`snapshot/data-progress-20261023-090849`
- 采集时间：2026-10-23 09:09:46–09:09:56（Asia/Shanghai）
- 来源：`/home/luchitong/work/repo-vuln-50-v031`
- 基线：`76bd6d274f038cd7bcd82dba1b2d857da762f132`
- 数据状态：`draft`

本快照保存 `data/`、`runs/`、`exports/`、`v031/reports/`、`v031/reviews/`、
`v031/ledger/`、`v03/reports/`、`migration_backup_v02/data/`，以及交接文档、工作日志和数据报告。
运行记录中的原始响应、证据、复核材料、缓存和复现结果一并保留。
`scratch/` 中的临时 clone、`.venv/`、`tools/gems/` 和 Python 缓存未纳入本分支。
工作流、通用脚本和 Schema 沿用基线；本次提交保存数据进度。

当前主表包含 50 个仓库、94 个快照、32 条评测选版、90 条漏洞和复核记录、
2951 条证据、1723 条候选 triage。32 个评测目标快照共有 61 条已确认正样本。

Draft 结构校验结果为 **0 errors / 49 warnings**，详细结果见
[`snapshot/VALIDATION_DRAFT.json`](snapshot/VALIDATION_DRAFT.json)。
来源目录中既有报告和工作日志按原内容保留，报告中的历史统计对应各自生成时间。
本快照的采集信息见 [`snapshot/metadata.json`](snapshot/metadata.json)。

疑似凭据扫描的 34 处命中已逐项核查：18 处为与 GitHub 上游公告逐字比对的公开示例，
5 处为上游测试凭据，2 处为环境变量模板，9 处为跨 JSON 字段误报；未发现实际凭据。
核查结果见 [`snapshot/CREDENTIAL_SCAN_REVIEW.json`](snapshot/CREDENTIAL_SCAN_REVIEW.json)，原始数据未改写。

验证本分支所有文件的内容：

```bash
sha256sum --quiet -c SNAPSHOT_CHECKSUMS.sha256
```

`CHECKSUMS.sha256` 是来源目录中的历史文件；本次快照使用 `SNAPSHOT_CHECKSUMS.sha256`。
