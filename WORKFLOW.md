# RepoVuln-50 v0.3.1 — 固定快照、漏洞相关性优先、成本受控

**目标：50 个优质上游仓库 = 50 个冻结评测 commit。** 被测审计 Agent 每次只接触其中一个 commit 的完整一方源码和必要构建文件，不允许读取数据集私有标签、未来修复历史或随意联网搜索答案。评测时根据该 SHA 上**已确认存在的已知漏洞**比较其报告，未匹配项独立裁决，不能自动计误报。

## 0. 与 v0.3 的关键差异

- **不再要求穷尽、深度验证仓库的全部历史 CVE 或所有安全修复 commit**。只要求尽力发现、验证**可能影响所选 SHA**的公开已知漏洞。
- 历史无关漏洞元数据/已有 B 级标注可保留，作为 `legacy` 证据；不因本次优化而删除或降级，但也不再要求为了其补做全量修复定位、复现或评测矩阵状态行。
- 固定 commit **先确定，再做目标相关性筛选**。评测 SHA 与漏洞的关联优先使用离线、确定性的版本与分支规则，遇到来源冲突/不确定时做局部源码检查；**不可机械依赖 semver 判不存在**。
- 对每个可能影响所选 SHA 的漏洞，执行正式类型、CVSS、修复版本、根因位置和 A/B 证据审核。A 级需隔离红绿复现；B 级需要独立修复差异/测试/根因交叉审核。
- 数据集不宣称记录该 SHA 的所有真实漏洞；`KnownPositive` 指采集截止日前**已发现且已证实在该 SHA 存在**的漏洞。对未匹配新发现单独裁决。

## 1. 一次评测任务的逻辑

```
50 个上游仓库
  └─ 各冻结一个 SHA  ←  官方稳定发行/可复现/可审计/至少一个已知正样本
        ├─ 全量语言扫描（所有一方语言；第三方、测试、配置分别标记）
        ├─ 公告+OSV+GHSA+NVD+Security+定向 fix PR 查询（仅做候选发现）
        ├─ 低成本候选相关性判断 → snapshot_candidate_triage.jsonl
        │    ├─ confirmed_not_affected / out_of_scope / duplicate → 保存证据并归档，不再深度审计
        │    ├─ possible_affected / unknown → 定向修复 diff、源码根因、人工复核
        │    └─ confirmed_affected → 要求同一 SHA 的定位、独立证据、A/B审核
        └─ 已确认已知漏洞 Oracle（固定版本） → 待测 Agent 的结果比对+开放世界裁决
```

原始历史候选仍保存在 `candidates.jsonl`；旧 `vulnerabilities.jsonl` 里的已验证历史漏洞仍保留。新增历史无关线索**不需要进入完整 `vulnerabilities.jsonl`，只需候选/出处/排除理由**。Snapshot Oracle 的正样本只来自正式 `snapshot_vulnerability_status.status=confirmed_affected`；不可从历史 CVE 列表机械复制。

## 2. 阶段 SOP（按顺序执行）

### P0 只读接管与冻结

复核原始 50 个仓库、22 个旧评测快照、72 条 B 级（用户提供的上次统计，**必须从真实文件复算**）、候选 2626、已验 1816 项证据及队列情况。源目录只读；复制到新版本目录，记录旧数据文件的 SHA256、数量、旧 verdict、所有未解决候选。不因架构调整将任何 old B 改成 A。迁移期间不采集新的不相关历史漏洞。

### P1 每库选一个正式目标 SHA

候选以发布 tag/完整树、可构建性、范围可控、语言完整、是否有至少一条真实漏洞为优先；不以最大化漏洞数选择过旧版本。记录 `evaluation_selection`，需独立审核、冻结，且**不得因测试结果反向换版**。对于未来分支、Git 日志、带 CVE 的构建注释、隐性修复文件和网络泄漏执行隔离。若部分仓库还没选好，先按 P0 优先冻结其 SHA，而不是大面积挖掘历史 CVE。

### P2 快照限定的“公开已知漏洞”检索

针对具体 `repo_id + SHA + release/tag + 组件`，从 GitHub Advisory、OSV、NVD/CVE、官方 SECURITY/Release/PR、已定位的相关 fix commits 多源检索。记录每个来源及查询时间、完整分页、去重、披露日期、相对所选 SHA 的影响范围。**不枚举仓库所有 Git 历史提交来猜漏洞**。源搜索深度限于与该版本可能相关的安全修复/公告，执行两轮独立检索且记录 *new_relevant_candidate_count*，它不是 new_verified_count。

### P3 零 LLM 优先的候选相关性筛选

建立 `snapshot_candidate_triage.jsonl`：每个当前候选在该库选定 SHA 下给出 `confirmed_affected | confirmed_not_affected | duplicate | out_of_scope | possible_affected | unknown`、依据、原始 URL 与方法。引入版本、回溯补丁、分支回合并、重命名、semver prerelease 不清楚时保留 `unknown`，不以字符串大小比较定性。`confirmed_not_affected` 必须有可信的源码/版本/分支证据。可通过规则完成则不调用 LLM；重复 CVE/OSV/GHSA 别名只验证一次。快照无关的结果归档，不要求其 CVSS+修复定位+动态 PoC 全部完整。

### P4 仅深度验证与评测 SHA 有关的候选

对 `possible_affected`、`unknown` 优先查看修复 PR/diff、根因调用路径；与 SHA 确实相关则正式审核并加入 `vulnerabilities.jsonl`、`locations.jsonl`、`reviews.jsonl` 与版本 Oracle。类型（CWE）、CVSS 原始向量与来源冲突都要留记录；安全级别矛盾可阻塞严重程度评分，却不必抹除已证实的“漏洞确实存在”的证据。对未通过 B/A 门槛的相关候选保留 `pending`，**不能判无效**。不做整库全修复历史重构。

### P5 版本级已知真值冻结

`expected_known_positives = {v | (selected_snapshot,v).status == confirmed_affected AND A/B review AND location.commit == selected SHA}`。每个正样本记录缺陷文件/位置、根因证据、漏洞类型、CVSS/等级及官方修复版本；一条 CVE 多入口只计一个漏洞，不重复加分。对遗留历史 `vulnerabilities` 之外的当前已知候选，同样执行相关性盘点，不要求所有历史 CVE 出现在版本矩阵中。冻结 `oracle_version`、选择 SHA、标注截止日期与哈希。

### P6 暴露给被测审计 Agent 的输入

仅用 `git archive <SHA>`（或等效干净工作树）提供完整指定范围源码，禁止暴露 `.git` 历史、公告、修复 patch、benchmark 标签、已知 CVE 列表。提供一致的构建配置，但若 `.github`、变更日志本身泄漏答案，必须在**不改变漏洞语义**的前提下统一做信息泄漏审查；记录对真实源码的任何裁剪。允许静态审计跨文件和跨语言。下载依赖时应采用离线固定版本并隔离网络。

### P7 开放世界评分

经去重/别名/根因匹配后计算：`known recall@SHA = 匹配已确认的 known positives / 该 SHA known positives 数`。50 库等权 macro recall，允许按 CWE、严重程度、主语言、跨语言缺陷分组。定位精度、严重程度偏差单独算，缺失/冲突 CVSS 时将该维度标未评估，不伪造。未匹配 findings → unresolved → 独立审核；证明新漏洞后 `novel_confirmed_tp`，证明不成立后 `confirmed_fp`；冻结本轮真值不被悄然修改。报告已裁决精确率、未决数和区间，**不自动给未匹配项 FP 或封闭世界 F1**。

### P8 发布门槛与成本停止条件

- 50 库独立质量 PASS、各一个冻结 SHA，全部语言清单完整，主语言覆盖 ≥10 类；已确认的每个目标 positive 同一 SHA 可定位、B/A 审核通过。
- 该 SHA 的候选均有 triage；无法排除的 `possible_affected/unknown` 必须完成深入核验，或明确保持 draft/覆盖不足，不能声称已知漏洞已全。`PASS_KNOWN_SWEEP` 表示针对**固定快照**的两次独立搜索均无新增**相关候选**，不是仅无新增“可提升漏洞”。
- 不再要求每条历史 CVE 在目标 SHA 上有一个 `snapshot_vulnerability_status` 行；校验器只约束已提交的状态和位置真实性。
- 保留未解决历史候选，但旧全历史的 2115 条不能因未补 A/B 自动阻塞：先判断与正式 SHA 是否有关，再决定是否深入。
- 必须记录阶段 token 与人民币费用；预防无止境重试。额外深度审核调用模型前需检查实际预算。**本包附成本汇总工具，但不是模型调用网关；未接入 Agent 时无法自动阻止扣费。**

## 3. 费用策略（可调整初始阈值，不是实测价格）

- Tier0：去重、OSV 区间/分支条件、fix diff 定位、语言计数/版本排除全部离线规则优先。
- Tier1：低成本模型，仅处理条件不清晰的公告和较小的代码 diff。
- Tier2：困难路径升级更强模型/人工，需明确升级理由。
- 单候选单阶段原则上最多 2 次 LLM 尝试，超过则转人工排队并保留此前结果；**绝不自动 rejected**。
- 示例累计预算 500 元，已支出约 40 元是用户估计值，真实价格从服务商账单核对。每阶段记录调用费用，仓库/快照/候选 ID，生成 COST_REPORT。
- 优先级：先补齐 50 个目标 SHA → 处理可能相关的疑点 → 冻结目标真值 → 仅在有明确研究价值时扩展历史库。

## 4. 运行顺序

```bash
python -m pip install -r requirements.txt
# 从已经迁移过的 v0.3 数据无损升级，默认 dry-run
python scripts/upgrade_v03_to_v031.py --source /path/to/v03 --out /path/to/v031
python scripts/upgrade_v03_to_v031.py --source /path/to/v03 --out /path/to/v031 --apply
# v0.2 的项目可继续使用更新后的 v0.2 迁移脚本（输出 v0.3.1 草稿）
python scripts/migrate_v02_to_v03.py --source /path/to/v02 --out /path/to/v031 --apply
# 根据已有 triage 决策排列后续验证任务，不会自动猜真假
python scripts/plan_snapshot_queue.py /path/to/v031 --out /path/to/queue.json
python scripts/validate_dataset.py /path/to/v031 --draft
# 完成全部 50 组目标版本及适用漏洞验证后，再执行严格门禁
python scripts/validate_dataset.py /path/to/v031
```

**工具边界**：本工具包只提供 Schema、排队/迁移/结构校验/离线分数计算及费用汇总，不包含在线采集器、自动真实 PoC、自动漏洞判定或已构建的 50 仓数据。不得将 Schema PASS 视为漏洞确凿存在。
