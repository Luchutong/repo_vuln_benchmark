# 当前限制

- 数据集仍是 **draft**：50 个仓库全部为 `NEEDS_REVIEW` 覆盖结论，未达到 PASS_KNOWN_SWEEP，不可用于宣称完整真值或跑分。
- 覆盖停止规则要求最近两轮无新增已验证漏洞；最近几轮仍有新增（当前共 73 条已验证漏洞），因此停止条件未满足。
- 只有 73 条漏洞完成 A/B 独立复核，均为 grade B（静态）。没有执行 PoC 或红绿动态测试。
- OSV 聚合记录可能继承 GHSA/NVD/生态库；NVD 仅查询部分仓库；官方 repository advisory 对 50 个仓库拉取成功，但仍有 14 个空列表和若干匿名限流失败。
- 未解决候选 2114 行；主要工作缺口是高披露量仓库的逐条根因/修复闭环，不代表这些仓库更危险。
- 快照语言盘点固定使用 github-linguist 9.7.0，75 个快照全部 `full_scan=true` 且枚举与 `git ls-tree` 一致；仍存在 128 KiB 有界检测和少量 ambiguous 文件。
- 原始来源可能后续修订；截止日只约束首次公开日期，不是历史时点重建。拒绝/撤回记录、复用 fix commit 和冲突修复版本见 `runs/verification/data_quality_findings.md`。
- 未收录不代表无漏洞；Agent 未匹配发现须独立裁决，未决不能自动当 FP。
