# CANDIDATE_FUNNEL_V031 — 候选筛选漏斗（v0.3.1）

对应数据：`data/snapshot_candidate_triage.jsonl`（每候选+冻结快照一条）、
`v031/reports/queue_P3.json`（plan_snapshot_queue 落盘）。初始生成 2026-10-22，
2026-10-23 随 django 评测目标从 tag 3.0.2 切到 tag 4.2.13、rack 从 2.2.3 切到 v3.1.13、
libexpat 从 R_2_4_4 切到 R_2_6_2、phoenix 从 v1.6.13 切到 v1.8.8 重新 triage 后更新为下列计数
（旧快照的 django 163 条、rack 50 条、libexpat 143 条与 phoenix 8 条 triage 行分别归档在
`data/legacy_snapshot_candidate_triage_snap_ab695ba3db678939.jsonl`、
`data/legacy_snapshot_candidate_triage_snap_f97687a4e0807cb2.jsonl`、
`data/legacy_snapshot_candidate_triage_snap_d33251dac37c334c.jsonl` 与
`data/legacy_snapshot_candidate_triage_snap_ee79f4175242bbee.jsonl`）。

## 总览

```
原始候选（data/candidates.jsonl）                   2626
│
├─ 位于 23 个已选仓库（有冻结 SHA 可判定）      1577  → 已 triage
│     ├─ confirmed_affected      71   （distinct 漏洞 60，对应 Oracle 正样本）
│     ├─ confirmed_not_affected 303   （版本/分支区间证据 + phoenix 4 条代码级排除）
│     └─ unknown               1203   （未在零 LLM 阶段确立相关性，≠无漏洞）
│
└─ 未 triage                                     1049
      └─ 27 个未选仓库（无冻结 SHA）             1049  → P0_SELECT_SNAPSHOT
```

- 已 triage 覆盖 23 个快照；`review_method`：`source_code_review` 75（71 affected + 4 phoenix 排除行）/
  `trusted_range_with_branch` 299 / `unresolved` 1203。
- 初始 1568 条决策来自既有证据（candidate.status / reason / source_urls / Oracle confirmed_affected），
  未引入任何 LLM 或编造；此后 5 条独立复核提升（rexml CVE-2025-58767、django CVE-2024-39330、
  rack CVE-2025-46727、libexpat CVE-2024-45490、phoenix CVE-2026-56812）各补 affected 行
  （phoenix 的 56811/56812 各有两条 discovery 路径），rexml 的 8 条、libexpat 的 7 条与 phoenix 的
  4 条以修复区间 / 代码级核对 + 完整 clone 祖先关系补 not_affected 行（见下），同时归档了四个旧快照的
  163/50/143/8 条行（其中 19 affected / 127 not_affected / 216 unknown），净得当前 1577 行。
  django 新快照上其余 162 条、rack 新快照上其余 49 条、libexpat 新快照上其余 135 条候选一律保留
  `unknown`——旧快照的驳回理由不能直接证明其在新 tag 上不适用。

## 逐阶段说明

1. **confirmed_affected（71 = 60 distinct vuln）**：`status=verified` 且其 `vulnerability_id` 在该库已选快照的
   Oracle 为 `confirmed_affected`。证据 URL 沿用候选 `source_urls`；判定复用既有代码级复核（source_code_review）。
   「2 候选→1 漏洞」的别名在同快照下计为一个已知正样本，不重复加分。
   其中手工提升的包括：`disc2_de98c5ab937e69a43862e5b4`（CVE-2025-58767，ruby/rexml，
   A 级 red/green）、`disc2_911c6ce3cba60cce0edccd71`（CVE-2024-39330，django tag 4.2.13，A 级
   red/green）、`disc2_7f2500f73d3836ead0e09463`（CVE-2025-46727，rack v3.1.13，A 级 red/green）、
   `disc2_35a922eb511ed468630f4a2d`（CVE-2024-45490，libexpat R_2_6_2，A 级 red/green），以及
   phoenix v1.8.8 上的 `disc2_46723370667ed0c5775db602` / `adv3_935719b31ddff77e`（CVE-2026-56811，B 级）
   与 `disc2_49ab8b917b7f862af6ea3968` / `adv3_a7fa8aabc9d9faea`（CVE-2026-56812，A 级 red/green）；
   其余由规则阶段从既有 Oracle 状态生成。

2. **confirmed_not_affected（303 = 299 trusted_range + 4 phoenix source_code_review）**：`status=rejected` 且 reason 含快照相关性排除子句（`Not applicable to
   snapshot` / `does not apply`），如「fix already in <tag>」「introduced after <tag>」「advisory 区间在
   <tag> 之后」等，属版本/分支区间规则（trusted_range_with_branch），非裸 semver 字符串比较；均有
   runs/verification 下的 NOT_APPLICABLE.md 卷宗佐证与 https 证据 URL。这些候选被归档、不再深度审计。
   其中 rexml 的 8 条（7 个 distinct CVE + 1 条重复 advisory 行）与 libexpat 的 7 条（旧 R_2_4_4
   目标下的 2022 系列 CVE）是 2026-10-23 新增：OSV 修复区间加上完整 clone 中修复 tag/fix commit
   对目标 commit 的祖先关系（`runs/verification/rexml_snapshot_not_applicable/NOT_APPLICABLE.md`、
   `runs/verification/libexpat_R_2_6_2_fixed_previous/NOT_APPLICABLE.md`），只证修复已存在，
   不证快照无其他漏洞。phoenix v1.8.8 上的 4 条（CVE-2017-1000163、CVE-2022-42975 各 1 条，
   CVE-2026-32689 2 条）是 `source_code_review`：除 advisory 区间外还核对了快照内代码
   （`validate_local_url/1` 的 `//` 与反斜杠拒绝、`compare_host?/2` 的点边界、
   `long_poll.ex` 的 `String.splitter` + `Enum.find`）及修复 commit 祖先关系。

3. **unknown（1203）**：位于已选仓库、但此零 LLM 阶段未确立对冻结 SHA 的相关性（`status ∈ {pending_location,
   pending_in_validation, pending_version}`，或 1 条被撤回 advisory 的 rejected）。**unknown ≠ 无漏洞**；
   其中可能与 SHA 相关的须进入 P4 定向核验，否则保留 draft。1 条 `adv3_087476da78c375b4`（advisory
   withdrawn/REJECTED）标 unknown，不自动判无漏洞。django 新快照上 162 条、rack 新快照上 49 条、libexpat 新快照上 135 条候选
   全部保留 unknown：它们在旧 tag 上的驳回理由不构成对新 tag 的适用性证据。phoenix 新快照的 8 条
   候选已全部有决策，不再保留 unknown。

4. **未 triage（1049）**：全部是 27 个未选仓库的候选，无冻结 SHA，须先选版冻结。已冻结的
   rexml 快照上不再有未 triage 候选（8 条已完成判定）。

## 队列（plan_snapshot_queue，`v031/reports/queue_P3.json`）

| 优先级 | 计数 | 含义 |
|---|---|---|
| P0_SELECT_SNAPSHOT | 1049 | 27 未选仓库候选，先选版 |
| DONE | 71 | confirmed_affected（可作 recall 正样本，distinct 漏洞 60） |
| ARCHIVE | 303 | confirmed_not_affected（归档） |
| P1_REVIEW | 1203 | unknown，需低成本定向核验 |

## 约束与诚实边界

- 不因本次筛选删除任何候选；原 `candidates.jsonl` 完整保留。
- 结构校验通过 ≠ 漏洞真实存在；`unknown`/`possible_affected` 未核验前不得声明快照已知漏洞已穷尽。
- 后续新增候选或修正决策时，用 `build_initial_triage.py --checked-at <ISO>` 与 plan_snapshot_queue 刷新。