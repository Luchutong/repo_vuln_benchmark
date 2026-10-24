# 数据表进度快照

- 分支：`snapshot/data-progress-20261024`
- 数据采集完成时间：2026-10-24 09:13:47（Asia/Shanghai）
- 来源：`/home/luchitong/work/repo-vuln-50-v031`
- 基线：`76bd6d274f038cd7bcd82dba1b2d857da762f132`
- 数据状态：`draft`

本分支按用户确认的范围，只发布 `data/` 数据表、`manifest.json` 和进度文档。
进度文档包括工作日志、交接说明、阶段报告、`docs/` 和 `v031/reports/` 下的 Markdown 文件。
本次复制 109 个文件，合计约 18.51 MB；具体文件清单见 [`snapshot/metadata.json`](snapshot/metadata.json)。

当前主表包含 50 个仓库、110 个快照、48 条评测选版、126 条漏洞和复核记录、
4298 条证据元数据、2613 条候选 triage。

表中的证据与导出路径保留原始引用。`runs/` 原始运行证据、`exports/` 导出文件、
临时 clone、环境目录及原始审查材料保留本地，不在本分支上传。
本次提交直接基于 `main` 创建，完整本地快照不属于本分支的提交历史。

数据表的 JSON 和 Schema 校验结果见 [`snapshot/TABLE_VALIDATION.json`](snapshot/TABLE_VALIDATION.json)。
包含本地导出文件的源快照 draft 校验为 **0 errors / 49 warnings**，结果保存在
[`snapshot/SOURCE_VALIDATION_DRAFT.json`](snapshot/SOURCE_VALIDATION_DRAFT.json)。
该源报告的文件存在性和导出哈希检查适用于完整本地快照。
既有文档中的历史统计按原内容保留。

验证本分支文件内容：

```bash
sha256sum --quiet -c SNAPSHOT_CHECKSUMS.sha256
```
