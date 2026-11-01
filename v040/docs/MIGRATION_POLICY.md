# 选择性迁移策略

| 来源表 | 新工作集策略 | 原因 |
|---|---|---|
| repositories | 保留质量状态 PASS 的仓库元数据 | 后续仍需完成目标仓库覆盖 |
| snapshots | 只保留 frozen selection 对应的唯一 SHA | 不把 proposed/draft 版本带入新工作集 |
| evaluation_selection | 只保留 frozen 行 | 不复制尚未审核的选择草稿 |
| vulnerabilities | 只保留目标 SHA 上有确认状态、公报来源和固定 SHA 静态位置的正式正样本 | 其余不属于新流程的正式 GT |
| locations | 只保留上述正样本在目标 SHA 上的定位 | 避免搬运其他历史版本行号 |
| snapshot_vulnerability_status | 只保留可关联正式漏洞/位置的 confirmed_affected | 仅这些记录作为 Known Recall 分母 |
| evidence | 只保留已迁入 repo/snapshot/vulnerability/location 的 PASS 证据 | 排除无关或失败的 draft 证据 |
| candidates | 只保留冻结 SHA 对应的 active/possible/unknown 候选；与 GT 别名重复的去重 | 供后续静态定位，而不是重做全历史 |
| snapshot_candidate_triage | 只保留冻结 SHA 上有依据的 triage | 可复用目标版本的排除/未决结果 |
| reviews | 不复制旧 A/B 审核表 | 新流程不再依赖双审核与动态复现；已有等级仅在报告中统计，不作为准入门槛 |
| discovery_coverage | 不复制旧全历史 coverage | 旧记录不能证明新 SHA 的覆盖闭环 |
| 原始 Token/Prompt 日志 | 不复制原始日志；只可迁移费用汇总 | 降低体积并避免无关上下文泄漏 |
| 其他历史快照/漏洞 | 不复制到新工作集；源目录保持不变，迁移报告仅记数量与排除原因 | 不需要为历史 CVE 重新做深度审核 |

**默认策略只接纳 `decision_status=frozen` 的评测选择。** 若当前项目确实需要某个尚未 frozen 的旧快照，先人工审核并冻结，再执行迁移；不要在迁移脚本里自动把 draft 改成正式版本。

## T1/T2/T3 回溯标注

- 迁移后的正样本按公报来源与既有检查结果标注 `advisory_trust_tier` 与 `advisory_review_status`。
- 这是**标注**，不是重新验证：脚本只读已有 URL/别名/位置字段，不访问网络、不重新判定漏洞真实性。
- T1 要求官方/Reviewed 来源 + 三项 `admission_checks` 全 true + `location_scope=source_location`；不满足但来源可信、已有定向核查的记 T2；候选一律 T3。
- 标注脚本 `assign_trust_tiers.py` 默认 dry-run，`--apply` 前备份到 `reports/backups/`，并写独立报告记录 before/after 哈希；迁移报告的原始计数与哈希不被改写。
