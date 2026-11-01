# RepoVuln-50 v0.4.0 — Advisory-Grounded Static Ground Truth

**核心原则：只为固定评测 SHA 建立静态漏洞真值；不要求本地 PoC、编译、动态复现或穷尽历史 fix commit。**

- `WORKFLOW.md`：新工作流与准入标准。
- `MIGRATION_PROMPT.md`：直接交给当前 Agent 的迁移指令，强调只迁移必要数据、不搬运无关 draft。
- `docs/DATA_CONTRACT.md`：新数据契约与 S1/S2/S3 定义。
- `docs/MIGRATION_POLICY.md`：哪些旧数据保留、筛选、排除。
- `scripts/migrate_selective.py`：从 v0.3.1 数据目录进行选择性迁移；默认 dry-run，不覆盖源目录。
- `scripts/validate_dataset.py`：静态 Ground Truth 结构与证据校验（含 T1/T2/T3、`location_scope` 与抽样规则）。
- `scripts/score_known_gt.py`：已知漏洞召回率计算，分存在性与源码定位两个口径，保留未决发现独立裁决原则。
- `scripts/cost_report.py`：汇总实际 Token/费用日志；不接管模型调用网关。
- `scripts/advisory_tiers.py`：公报可信度分类与三项检查的共享逻辑。
- `scripts/assign_trust_tiers.py`：对既有正样本做 T1/T2/T3 回溯标注；默认 dry-run。
- `scripts/qa_sample.py`：按 10%–20% 分层抽样复核 T1；默认 dry-run。
- `scripts/resolve_version_candidates.py`：逐个仓库解析 `needs_version_check` 候选。按 OSV 记录的
  `versions`/SEMVER/ECOSYSTEM 区间与 NVD 2.0 年度 feed 的 CPE 配置判定冻结 tag 是否受影响；
  写入 triage 决策（`possible_affected` / `confirmed_not_affected` / `out_of_scope` / `unknown`），
  命中时把候选改为 `needs_static_location`。默认 dry-run。
- `scripts/resolution_report.py`：按仓库汇总候选解决状态（已解决 / 未决 / 决策分布）。
- `scripts/fetch_eval_sources.py`：把每个冻结快照的评测 SHA 浅克隆到数据集外的原始缓存
  （`sources/<owner>__<repo>`），逐个校验 `HEAD == commit_sha`；只作为只读静态审查输入。
- `scripts/propose_locations.py`：对已有 fix commit 的候选抓取 commit patch，把补丁里被删除的
  行在冻结源码树中定位，产出文件/行号/函数的位置**建议**（写入 `reports/location_proposals.jsonl`），
  不写数据集。
- `scripts/promote_candidate.py`：把人工确认的候选提升为正式 Ground Truth：复核冻结源码树
  （文件/函数存在性、行号范围、代码摘录），生成 schema 合法的 vulnerabilities / locations /
  snapshot_vulnerability_status / triage 行；默认 dry-run，`--apply` 才写入。
- `scripts/promote_from_proposals.py`：T1 快速通道的批量前端。逐条把 location 建议交给同一套
  复核逻辑，并额外要求：定位文件由公报正文点名（避免 release 合并提交把多个公报的 hunk 混在
  一起）、公报区间包含冻结 tag、同一公报在同快照下只产生一条漏洞行（其余候选记为 `duplicate`）。
  默认 dry-run。
- `scripts/fill_location_excerpts.py`：为缺少 `code_excerpt` 的 locations 行从冻结源码树回填
  代码摘录；文件不存在、行号越界或 HEAD 不符的行只报告、不写入。默认 dry-run。
- `scripts/record_qa_reviews.py`：按 `qa_id` 写入抽样复核结果（status/findings/action/reviewer），
  用 qa_reviews schema 校验；不改动漏洞与位置行本身。

准入规则见 `WORKFLOW.md` 第 2–4 节；抽样细则见 `docs/REVIEW_SAMPLING.md`。

## Quick start

```bash
python -m pip install -r requirements.txt
# 只预览迁移计划，不写文件
python scripts/migrate_selective.py --source /path/to/current_v031 --out /path/to/new_v040
# 检查报告后执行；目标目录必须不存在
python scripts/migrate_selective.py --source /path/to/current_v031 --out /path/to/new_v040 --apply
python scripts/validate_dataset.py /path/to/new_v040 --draft
python -m unittest discover -s tests -v
```

默认只迁移**已经冻结的评测快照**及其必要的正样本/源码位置/证据；没有冻结快照的合格仓库只保留仓库元数据，并进入 `selection_queue.jsonl`。不迁移旧 `reviews`、旧全历史 `discovery_coverage`、其他历史快照、无关历史漏洞、全量 rejected/duplicate 候选或原始调用日志。所有源文件保持只读，迁移报告记录数量、排除原因和哈希。

如确有需要，可先人工冻结某个快照后重跑迁移；不建议把未冻结的 draft 快照直接当作正式评测目标。

**重要边界**：S1/S2 是基于公报、版本关系与固定 SHA 静态代码证据的 Ground Truth 等级，不代表动态利用已成功。Schema 通过不等于漏洞真实性已被自动证明。
