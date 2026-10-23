# RepoVuln-50 v0.3.1 (Snapshot-Only Benchmark)

**50 个真实上游仓库 × 每仓一个冻结 SHA；只深度验证当前 SHA 的已知漏洞。** 不再要求穷尽所有历史 CVE 和 fix commit，更不再为了无关历史漏洞创建评测快照。旧 v0.2/v0.3 已有资料无损保留。

核心文档：`WORKFLOW.md`（阶段说明）、`AGENT_PROMPT.md`（直接发给 Agent）、`docs/DATA_CONTRACT.md`（数据语义）、`docs/RELEASE_CHECKLIST.md`（验收清单）。

本版本相对 v0.3 新增：
- `data/snapshot_candidate_triage.jsonl`：选定 SHA 下的候选相关性，可信证据支持排除/升级；历史无关候选无须深度验证。
- `scripts/upgrade_v03_to_v031.py`：只读源数据，复制并修改版本号，将旧全历史覆盖 PASS 重置为 NEEDS_REVIEW（不伪造新成绩）。
- `scripts/plan_snapshot_queue.py`：非 LLM 待办排序，不自动推断候选真实性。
- `scripts/cost_report.py`：按模型与阶段汇总**实际提供的** Token 和费用，不劫持模型调用。
- 更新后的 Schema 与 `validate_dataset.py`：发布时针对已选目标快照约束采集、triage、Ground Truth；不要求全部历史漏洞进入真值矩阵。

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/upgrade_v03_to_v031.py --source /path/to/old-v03 --out /path/to/new-v031 --apply
python scripts/plan_snapshot_queue.py /path/to/new-v031 --out /tmp/snapshot-work.json
python scripts/validate_dataset.py /path/to/new-v031 --draft
python scripts/cost_report.py /path/to/cost_ledger.jsonl --budget-cny 500
```

**注意**：升级脚本不会自动产生排除 verdict 或已确认漏洞。尚无真实 SHA/版本相关性证据的候选需保留未知。`vulnerabilities.jsonl` 里旧历史已验证项不删除；新增候选只在当前评测版本适用且验证通过后提升。
