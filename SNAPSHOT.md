# 数据表进度快照

- 分支：`snapshot/data-progress-20261026`
- 数据采集完成时间：2026-10-26T07:57:28+08:00（Asia/Shanghai）
- 来源：`/home/luchitong/work/repo-vuln-50-v031`
- 基线：`76bd6d274f038cd7bcd82dba1b2d857da762f132`
- 对比快照：`aa898ac2b36ff1227f0461480fac4b4d0e18ba4d`（2026-10-25）
- 数据状态：`draft`

沿用用户已确认的范围，只发布 `data/` 数据表、`manifest.json` 和进度文档。
本次复制 110 个来源文件，约 29.25 MB。
来源文件清单与 SHA256 见 [`snapshot/metadata.json`](snapshot/metadata.json)。
原始运行证据、源码导出、临时 clone、环境和依赖目录保留本地；表中的证据和导出路径保留原始引用。

## 进度

| 指标 | 本次 | 较 10 月 25 日快照 |
| --- | ---: | ---: |
| 已复核漏洞 | 196 | +29 |
| A 级复核条目 | 119 | +29 |
| 当前评测快照的已确认正样本 | 167 | +29 |
| 证据元数据 | 7998 | +1480 |
| 待确认候选（possible + unknown） | 1065 | -36 |

50 个仓库共有 110 个快照，48 个仓库已有评测选版，其中 46 个已冻结。
196 条漏洞均有 location 和 PASS 复核记录，复核等级为 A 119 / B 77。
候选 triage 共 2613 行：confirmed_affected 191、confirmed_not_affected 1329、
possible_affected 491、unknown 574、duplicate 28。
triage 按候选计，评测正样本按选定快照与漏洞计，计数口径不同。
详细增量见 [`snapshot/PROGRESS.json`](snapshot/PROGRESS.json)。

## 校验与遗留项

- 80 个数据表文件的 JSON/Schema 校验为 0 errors，见 [`snapshot/TABLE_VALIDATION.json`](snapshot/TABLE_VALIDATION.json)。
- 本地 v0.3.1 工具的 126 项测试全部通过，见 [`snapshot/SOURCE_UNITTEST.txt`](snapshot/SOURCE_UNITTEST.txt)。
- 源数据 draft 校验为 0 errors / 48 warnings，见 [`snapshot/SOURCE_VALIDATION_DRAFT.json`](snapshot/SOURCE_VALIDATION_DRAFT.json)。
- 严格 release 校验仍有 199 项未满足要求，见 [`snapshot/SOURCE_VALIDATION_RELEASE.json`](snapshot/SOURCE_VALIDATION_RELEASE.json)。

`nlohmann/json`、`openssl/openssl` 尚未选版；`hyperium/hyper`、`JamesNK/Newtonsoft.Json` 的现有提议被审查拒绝，尚未冻结。
491 条 possible_affected 和 574 条 unknown 仍待核验，50 个仓库的 discovery_coverage 均为 `NEEDS_REVIEW`。
`manifest.status` 保留 `draft`，尚无统一的 source_cutoff_date 或 release freeze_timestamp。
本快照保存当前阶段进度，数据集仍未达到 release 门槛。

源数据校验中的导出文件存在性、哈希检查适用于完整本地目录；本分支发布范围仅为数据表和文档。
既有文档的历史统计按原内容保留；基线工具代码沿用 `main`，上述测试针对当前本地 v0.3.1 工具。

验证本分支文件内容：

```bash
sha256sum --quiet -c SNAPSHOT_CHECKSUMS.sha256
```
