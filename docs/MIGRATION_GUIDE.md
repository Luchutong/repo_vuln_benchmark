# v0.3.1 无损升级补充说明

已在 v0.3：使用 `scripts/upgrade_v03_to_v031.py --source <v03> --out <v031> --apply`，不得原地覆盖。旧 coverage 自动降为 NEEDS_REVIEW，保存于 `data/legacy_discovery_coverage_v03.jsonl`，不产生任何新漏洞结论。

若仍在 v0.2：使用更新版 `scripts/migrate_v02_to_v03.py` 直接产生 v0.3.1 草稿；详见下文的旧版迁移说明。

---

# v0.2 → v0.3 无损迁移实操

## 步骤 1：先点清楚你有什么

运行迁移脚本 **无 `--apply`**：

```bash
python scripts/migrate_v02_to_v03.py --source /ABS/PATH/v02-dataset --report /tmp/v02-preflight.json
python scripts/plan_selections.py --source /ABS/PATH/v02-dataset --out /tmp/snapshot-candidates.json
```

核对用户报告的 50 个仓库、22 个评测快照、72 个正式 B 级、72 位置/复核/状态、1816 证据、2626 候选。**不要假设 22 个评测快照一定属于 22 个不同仓库**。若源目录不包含 `data/repositories.jsonl`，先找到真实目录，不要初始化空目录假装继承成果。

## 步骤 2：快照选择必须有依据

对于 1 个旧 `evaluation_target` 的仓库，可以暂时保留该目标，但仍为 proposed；对于 0 或 2+ 个的仓库不能猜测。比较：稳定 release/tag、构建能力、已知 positive、审计证据、数据年代、语言扫描、偏差风险。填写选择文件：

```json
{
  "repo_id_001": "snap_0123456789abcdef"
}
```

只有实际存在且归属于该 `repo_id` 的 SHA 才能使用。如果新要选的 SHA 不在历史 snapshots 表，需要先采集并验证其 commit/语言/根因并更新源或迁移后 v0.3 数据，不能在映射文件里写不存在的虚构 SHA。

## 步骤 3：新目录迁移

```bash
python scripts/migrate_v02_to_v03.py --source /ABS/PATH/v02-dataset \
 --selections /ABS/PATH/approved-selections.json --out /ABS/PATH/v03-dataset --apply
```

拒绝覆盖已有输出。迁移创建：原始数据备份（`migration_backup_v02`）、文件 SHA 报告、非正式历史状态存档、主状态表（仅正式目标快照）、proposed 选择账本、v0.3 draft manifest。不会创建新 CVE、PoC、复核或 `confirmed_affected`。

## 步骤 4：对账 + 修复真实阻塞

```bash
python scripts/validate_dataset.py /ABS/PATH/v03-dataset --draft
```

按 `MIGRATION_REPORT.json` 审核迁移前后候选/vulnerability/evidence/review/locations 数目不下降；若非官方 Oracle 状态行数量下降，只能是**移动到 `historical_snapshot_status`**，不得无故消失。

挑选各仓库唯一 target，并逐个完成：全语言统计、固定 SHA 的代码定位、修复 release、候选真值矩阵、独立审核、已知漏洞检索两轮停止规则。`confirmed_affected` 不允许拷贝自历史 SHA。完成后由审核人决定 `proposed→frozen` 并记录版本日期/泄漏控制。

## 步骤 5：完成后执行严格检查

```bash
python scripts/validate_dataset.py /ABS/PATH/v03-dataset
```

注意严格验证器只检查结构/引用和声明的证据，不代替代码级/PoC 事实验证。全部 PASS 才能正式发布；否则保持 draft。

## 回滚

原始 v0.2 目录从不修改，v0.3 的 `migration_backup_v02/data` 保存原始 JSONL 完整字节副本。需要回滚时停止 v0.3 采集，指向原 v0.2 目录；不要把 v0.3 中新标注直接覆盖 v0.2。

**截止日期注意**：迁移自动生成的 `manifest.source_cutoff_date=null`，代表尚未核实既有数据的真实来源检索截止日期。正式发布前，必须从 `discovery_coverage` 和采集日志复核后再填写，不能直接使用迁移当天的日期。
