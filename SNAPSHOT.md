# 数据表进度快照

- 分支：`snapshot/data-progress-20261025`
- 数据采集完成时间：2026-10-25 09:19:07（Asia/Shanghai）
- 来源：`/home/luchitong/work/repo-vuln-50-v031`
- 基线：`76bd6d274f038cd7bcd82dba1b2d857da762f132`
- 对比快照：`2514d91ba5157245ca3397597b4f29029e60db37`（2026-10-24）
- 数据状态：`draft`

沿用已确认的范围，只发布 `data/` 数据表、`manifest.json` 和进度文档。
本次复制 107 个来源文件，约 21.11 MB；清单与来源文件 SHA256 见
[`snapshot/metadata.json`](snapshot/metadata.json)。
工作日志、交接说明、阶段报告、`docs/` 和 `v031/reports/` 下的 Markdown 文件一并保存。
数据表中的证据和导出路径保留原始引用，原始运行证据、导出文件、临时 clone、环境和依赖目录保留本地。

## 与上次快照的进展

| 指标 | 2026-10-24 | 本次 | 变化 |
| --- | ---: | ---: | ---: |
| 漏洞目录条目 | 126 | 167 | +41 |
| A 级复核条目 | 51 | 90 | +39 |
| 当前评测快照的已确认正样本 | 97 | 138 | +41 |
| 证据元数据 | 4298 | 6518 | +2220 |
| 待确认候选（possible + unknown） | 1147 | 1101 | -46 |

50 个仓库共有 110 个快照；48 个仓库已建立评测选版，其中 46 个已冻结，2 个仍为未获批准的提议。
167 条漏洞均有 location 和 PASS 复核记录，复核等级为 A 90 / B 77。
候选 triage 为 2613 行：confirmed_affected 162、confirmed_not_affected 1322、
possible_affected 527、unknown 574、duplicate 28。
triage 行数按候选计，已确认正样本按选定快照与漏洞计，两者口径不同。

## 仍需完成

- `nlohmann/json`、`openssl/openssl` 尚未建立评测选版。
- `hyperium/hyper`、`JamesNK/Newtonsoft.Json` 的现有提议被独立选版审查拒绝，尚未冻结。
- 1101 条候选仍待确认：527 条 possible_affected、574 条 unknown。
- 50 个仓库的 discovery_coverage 均为 `NEEDS_REVIEW`，尚无 `PASS_KNOWN_SWEEP`。

当前仍为 draft，以上计数不表示已穷尽选定快照的全部漏洞。
完整机器可读进度与增量见 [`snapshot/PROGRESS.json`](snapshot/PROGRESS.json)。

## 校验

77 个数据表文件的 JSON/Schema 校验为 0 errors，结果见
[`snapshot/TABLE_VALIDATION.json`](snapshot/TABLE_VALIDATION.json)。
包含本地导出文件的源数据 draft 校验为 **0 errors / 49 warnings**，结果见
[`snapshot/SOURCE_VALIDATION_DRAFT.json`](snapshot/SOURCE_VALIDATION_DRAFT.json)。
源报告的导出文件存在性和哈希检查适用于完整本地数据目录；本分支发布范围仅为数据表和进度文档。
既有文档中的历史统计按原内容保留。

验证本分支文件内容：

```bash
sha256sum --quiet -c SNAPSHOT_CHECKSUMS.sha256
```
