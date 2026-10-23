# LIMITATIONS_V031 — v0.3.1 升级后的真实边界

对应数据根目录：`/home/luchitong/work/repo-vuln-50-v031`。只列已确认缺口，不用「待完善」掩盖，
不把结构校验通过解释成漏洞验证通过。

## 1. 升级无损性

- 升级当时九张主表行数与 v0.3 完全一致（40/75/73/73/1839/73/2626/50/73），且与 v0.2 源字节级一致的部分不变；
  本版后续新增的验证行见 `HANDOFF_V031.md` 的当前计数。
- 升级复制 9753 个源文件、逐一记录 SHA256（`UPGRADE_REPORT.json.source_sha256`），`source_unchanged=true`。
- 本版没有做任何漏洞真值声明：`no_new_triage_or_verification_labels=true`。
- **schema 补丁**：v0.3.1 starter 的 GHSA 正则退回收大写限定（`[0-9A-Z-]`），会拒绝 9 条真实小写 GHSA
  canonical ID；已按 v0.3 的补丁改回 `[0-9A-Za-z-]`（改后 SHA256=efa419ad…，与 v0.3 已补丁版本一致）。
  只改 schema 文件，未改动任何 JSONL 数据。

## 2. 评测目标与真值

- 23/50 仓库有评测目标，其中 17 个已 `frozen`（django tag 4.2.13 第二轮审查 accept、rack tag v3.1.13
  审查 accept、libexpat tag R_2_6_2 审查 accept、phoenix tag v1.8.8 审查 accept，均于 2026-10-23 冻结）；
  其余 6 个 legacy `documented_exception` 目标仍为 `proposed`。
  全部 `leakage_controls` 为
  `worktree_without_git_history=false / ground_truth_isolated=false / network_policy=uncontrolled`（迁移默认，
  非已验证隔离方案）。
- 27 个仓库 `evaluation_snapshot_id=null`：Catalog 已验证漏洞为 0。axios/OpenSSL/sinatra 有历史 tag 快照
  但无 `confirmed_affected`，按 v0.3.1 规则不可自动选，亦不得编造 tag/commit。
- 60 条 live 已知正样本全部 `confirmed_affected`：55 条 B 级 + 5 条 A 级（rexml CVE-2025-58767、
  django CVE-2024-39330、rack CVE-2025-46727、libexpat CVE-2024-45490、phoenix CVE-2026-56812，均有独立
  reviewer 动态 red/green）。旧 django tag 3.0.2 的 8 条、旧 rack 2.2.3 的 2 条、旧 libexpat R_2_4_4 的 7 条
  与旧 phoenix v1.6.13 的 2 条 B 级状态行已归档为历史证据，不计入当前 Oracle；B 级不等于 PoC 已验证。
- 正式 Oracle（`snapshot_vulnerability_status`）只覆盖 23 个已选快照，无 `confirmed_not_affected/unknown/
  out_of_scope` 行。「没有 unknown」不等于「该 SHA 无其他漏洞」：未收录漏洞受检索与相关性筛选缺口限制。
- 27 个未选仓库在 Oracle 中无行，是 `needs_selection`，不是「无漏洞」。

## 3. 候选漏斗完整性

- 2626 条候选 → 23 个已选仓库内 1577 条已 triage：71 confirmed_affected（distinct 漏洞 60）/
  303 confirmed_not_affected / 1203 unknown（决策来自既有证据与独立复核，零 LLM）。
- 303 条 confirmed_not_affected 的依据是既有驳回卷宗里的版本/分支区间（如「fix already in <tag>」「introduced
  after <tag>」），非裸 semver 字符串比较；仍属规则层判断，未逐条做独立源码复核。其中 rexml 的 8 条
  （7 个 distinct CVE + 1 条重复 advisory）与 libexpat 的 7 条（R_2_4_4 时代的 2022 系列 CVE）另加完整
  clone 中修复 tag/fix commit 的祖先关系验证；phoenix 新快照的 4 条排除行另加代码级核对
  （`validate_local_url/1`、`compare_host?/2`、`long_poll.ex` 的惰性 splitter）；但都仍是排除性证据，
  不证明快照无其他漏洞。
- 1203 条 `unknown` 是「未在此零 LLM 阶段确立对冻结 SHA 的相关性」，**不是证明无漏洞**；必须继续核验相关疑点，
  否则保留 draft。其中 django 新快照的 162 条、rack 新快照的 49 条与 libexpat 新快照的 135 条是刻意保留的
  unknown：旧 tag 上的驳回理由不能证明新 tag 不受影响。phoenix 的 8 条候选已全部有新快照上的决策，不再保留 unknown。
- 27 个未选仓库的 1049 条候选无 triage 行（无冻结 SHA，先选版）；已选仓库的候选均已有 triage 行。
- 1 条被撤回 advisory（`adv3_087476da78c375b4`）既有 rejected 状态，标 `unknown`，不自动判无漏洞。

## 4. 检索与覆盖

- 全部仓库 `outcome=NEEDS_REVIEW`；旧全历史覆盖归档于 `legacy_discovery_coverage_v03.jsonl` 供对照。
- 50 条 coverage 的 `passes` 数组是从 v0.3 继承的模板化记录（每行 4 条、文字相同），
  **不是逐仓库真实检索历史**；尤其第 4 条 “static dossier verification … grade B” 对 ruby/rexml 与 django
  不成立（两者实际均为 grade A，见 `runs/independent/rexml_CVE-2025-58767_round1/verdict.json` 与
  `runs/independent/django_CVE-2024-39330_round1/verdict.json`）。
  `unresolved_candidates` 仅按当前 triage 个别更新（rexml 9 → 8，django 155 → 162，rack 48 → 49，
  libexpat 现有 135），其余仓库仍为旧值。
- `PASS_KNOWN_SWEEP=0/50`：没有对固定 SHA 执行两轮独立检索，未声明快照已知漏洞已穷尽。
- 披露截止 2026-10-21；2026-10-22 当日新披露不在数据内。`source_cutoff_date=null` 未复核。

## 5. 费用

- `cost_policy.json` 是阈值配置，不是强制网关（`WARNING` 已记录）。本版迁移与初始 triage 全部为离线规则，
  未产生任何记账的模型调用（`v031/ledger/model_calls.jsonl` 为空，cost_report 输出 0 调用 / ¥0 实测 /
  untracked = DO NOT ASSUME ZERO）。后续任何 LLM 调用必须记账后才可复核预算。

## 6. 评测运行与发布

- 无 `agent_findings.jsonl` / `adjudications.jsonl`：没有审计 Agent 运行，没有已知 recall/TP/FP/novel。
- 数据目录不可直接交给被测 Agent：仅 23/50 目标有去 `.git` 的源码导出，且 17 个已通过独立选版审查并
  frozen；其余 6 个 legacy 目标为 proposed，27 个未选版。
- `manifest.status=draft`；release 门槛（50 冻结目标、snapshot 限定覆盖、相关候选全部核验、cutoff 复核）
  均未达成，本报告如实记录，不做虚假 PASS 声明。