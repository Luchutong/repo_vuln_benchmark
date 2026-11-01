# RepoVuln v0.4.0 数据快照：34 库收尾批次

- 分支：`snapshot/v040-34repos-20261101`
- 采集时间：2026-11-01T13:47:23+08:00（Asia/Shanghai）
- 工具包：`/home/luchitong/work/repo-vuln-bench-v040`
- 数据来源：`/home/luchitong/work/repo-vuln-bench-v040-dataset`
- 基线：`76bd6d274f038cd7bcd82dba1b2d857da762f132`

本次沿用已确认的发布范围，保存数据表、进度文档及结构化审查/覆盖报告。
当前数据表作为完整工作检查点保留；已收尾的 34 库与剩余未完成部分分别列明，未改写来源数据。
未上传源码 clone、原始运行载荷、缓存、备份、位置建议草稿或环境依赖。

## 本批次

**34 个仓库已为 PASS_KNOWN_SWEEP，全部有唯一 frozen SHA，共 434 条静态正样本。**
批内候选按实际 triage 表检查，全部已有已解决决策。
完整版本/SHA 清单见 [`snapshot/COMPLETED_REPOSITORIES.md`](snapshot/COMPLETED_REPOSITORIES.md)，
机器可读索引见 [`snapshot/completed_repositories.jsonl`](snapshot/completed_repositories.jsonl)。

## 当前工作集

| 指标 | 数量 |
| --- | ---: |
| 仓库元数据 | 50 |
| frozen 评测 SHA | 47 |
| PASS_KNOWN_SWEEP | 34 |
| NEEDS_REVIEW | 13 |
| 静态 Ground Truth 正样本 / 源码位置 | 721 / 721 |
| 公报准入等级 | T1 569 / T2 152 |
| 证据记录 | 7245 |
| 候选表保留记录 | 1405 |
| 实际未决候选 | 6 |
| QA 复核记录 | 43，全部 pass |

6 条未决候选分布于 next.js（4）、spring-framework（1）、libexpat（1）。
hyper、Newtonsoft.Json、nlohmann/json 三库已记录排除决定，保留元数据和选择队列。
候选表保留已处理记录，1405 条不等于 1405 条未决候选。
T1/T2 和 S1/S2 是 v0.4 公报可信度与静态证据分级，与 v0.3.1 的 A/B 动态复核统计口径不同。

## 检查结果

- 13 个数据表文件 JSON/Schema 检查通过；34 库批次索引、SHA 选择关系和候选闭环检查通过。
- v0.4 draft 校验：**0 errors / 0 warnings**。
- 当前本地 v0.4 工具包：**62 tests passed**。
- 整体 release 检查：**18 项未满足要求**；还需处理 13 库覆盖、6 条未决候选、50 库冻结目标要求及 QA 抽样数量。
- T1 569 条按当前 release 校验至少需要 57 条 QA 复核，现有 43 条；本快照保留该缺口。

本工作集仍为 `draft`。PASS_KNOWN_SWEEP 仅针对指定公报来源及所选 SHA，不等于穷尽所有真实漏洞。
来源 README 和各历史报告按原内容保存，其中历史统计和说明对应其生成时点；当前校验结果以 `snapshot/VALIDATION_*.json` 为准。

## 文件与复核

- `data/`：v0.4 当前工作数据表；`reports/`：选择、迁移、抽样、提升与覆盖报告。
- `v040/`：当前工作流说明和数据契约文档。
- `snapshot/schemas/`：本次使用的 v0.4 Schema 副本。
- `snapshot/metadata.json`：源文件清单、SHA256、批次与校验元数据。
- `snapshot/VALIDATION_DRAFT.json`、`snapshot/VALIDATION_RELEASE.json`：本次重新执行的校验结果。
- `snapshot/TOOLKIT_UNITTEST.txt`：当前本地工具包测试日志。

本分支的可执行基线代码仍来自 `main` 的 v0.3.1 starter。
v0.4 数据应使用 `snapshot/schemas/` 的契约及当前本地 v0.4 工具校验，工具包执行代码不在本次数据发布范围内。

验证本分支所有文件的内容：

```bash
sha256sum --quiet -c SNAPSHOT_CHECKSUMS.sha256
```
