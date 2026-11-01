# v0.4.0 数据契约

## 正式漏洞

`vulnerabilities.jsonl` 保存漏洞身份、公报来源、官方字段和可选元数据。`fix_commits`、`fixed_releases`、CVSS 向量、PoC、回归测试都不是必填项。缺失值必须保留为 null/unknown，不得由模型猜测。

`locations.jsonl` 保存固定 SHA 上的静态根因锚点：文件、函数/行范围、语言、SHA permalink、危险操作/缺失检查说明和定位粒度。

`snapshot_vulnerability_status.jsonl` 中只有 `status=confirmed_affected` 的 S1/S2 行进入已知漏洞评分分母。必须关联同一 `snapshot_id`、同一 repo 和同一 SHA 的漏洞/位置记录；`location_scope=version_only` 的行可以没有 location，且不进入源码定位评分。

## 准入等级（T1/T2/T3）

| 字段 | 取值 | 说明 |
|---|---|---|
| `advisory_trust_tier` | `T1` | 官方维护者/厂商公告或 GitHub Reviewed Advisory；版本关系明确；三项自动检查通过 |
| | `T2` | 公报可信但存在分支/定位歧义，或来源为 NVD/OSV/第三方；已完成定向静态核查 |
| | `T3` | 未经审核的第三方记录、版本冲突，或来源不可信且无法定位；只作候选，不进正式 GT |
| `advisory_review_status` | `github_reviewed` | GitHub 明确标记 Reviewed 的 Advisory |
| | `vendor_official` | 项目维护者/厂商官方公告（含仓库自有 security advisory） |
| | `unreviewed` | 未审核的 GHSA、issue、PR 或第三方记录 |
| | `unknown` | 仅有 NVD/OSV 聚合记录，无法确认审核状态 |
| `admission_checks` | object | T1 三项检查：`sha_release_match`、`component_present`、`no_counter_evidence`，均为布尔；可附 `checked_at`、`notes` |

**规则**

- T1 必须同时满足：`advisory_review_status ∈ {github_reviewed, vendor_official}`，三项 `admission_checks` 全为 true，且有 `location_scope=source_location` 的定位。
- T2 必须已完成定向静态核查；可以没有全部三项 T1 检查，但必须有版本关系依据和源码定位（或明确 `version_only`）。
- 来源为 `github_reviewed`/`vendor_official` 且版本关系明确、但确实没有可靠源码位置时，记为 **T2 + `location_scope=version_only`**，只进入存在性/版本级统计；不要把这种情况误降为 T3。T3 仅用于来源不可信或版本范围本身冲突导致无法定位的记录。
- T3 不得出现在 `confirmed_affected` 的 S1/S2 分母中。
- `advisory_withdrawn_at` 非空、或 severity `status=conflict`、或存在回溯修复证据时，不得标 T1。

## 证据等级（S1/S2/S3）

- S1：T1/T2 准入 + 明确版本关系 + 固定 SHA 根因定位 + 额外静态佐证（如相关修复 Diff/官方测试/安全检查对照）。
- S2：T1 三项检查通过，或 T2 定向静态核查完成；版本关系与根因代码明确。公报可提供触发条件和利用路径；不要求本地 PoC。
- S3：公告可信但版本关系或根因位置尚未确定，只作为候选，不计入主分母。

## 定位口径

| `location_scope` | 含义 | 评分 |
|---|---|---|
| `source_location` | 有固定 SHA 的文件/函数/行锚点，根因可核对 | 进入存在性 Recall 与源码定位 Recall |
| `version_only` | 公报只声明项目/版本受影响，无可信源码位置 | 只进入存在性和版本级 Recall，不进入源码定位评分 |

## 状态语义

`confirmed_affected` 不代表动态利用已成功，只表示公开已知漏洞的版本范围与固定 SHA 源码证据一致。`confirmed_not_affected` 需要可靠排除证据；`possible_affected`/`unknown` 不得计作阴性。

## 候选解决状态

候选行保留在 `candidates.jsonl`，解决状态以 `snapshot_candidate_triage.jsonl` 的决策为准：

| 决策 | 是否未决 | 含义 |
|---|---|---|
| `confirmed_affected` | 已解决 | 版本关系成立；须提升为正式正样本后才计入召回 |
| `confirmed_not_affected` | 已解决 | 明确的上游版本/分支区间或 CPE 配置排除目标 SHA |
| `duplicate` | 已解决 | 同一漏洞的别名行，实质决策在 canonical 行 |
| `out_of_scope` | 已解决 | 公报属于其他项目，或 OSV/NVD 只命中非本仓库的包/CPE |
| `possible_affected` | 未决 | 版本范围命中，但固定 SHA 的源码根因尚未定位 |
| `unknown` | 未决 | 无可评估的上游范围、GIT-only 记录或归属不明 |

未决候选数 = `candidates` 中无 triage 行、或 triage 决策为 `possible_affected`/`unknown` 的行数。发布前该数必须为 0；用删除候选来“解决”候选不算证据。

## 抽样复核（`qa_reviews.jsonl`）

| 字段 | 说明 |
|---|---|
| `qa_id` | 抽样记录 ID |
| `vulnerability_id` / `snapshot_id` / `repo_id` | 被抽中的正样本 |
| `sampled_at` / `stratum` / `sample_reason` | 抽样时间、分层键、随机或强制原因 |
| `status` | `pending` / `pass` / `fail` |
| `reviewer` / `reviewed_at` | 复核人/时间 |
| `findings` / `action` | 结论与处置（`none`/`downgrade`/`correct`/`escalate`） |

默认抽样 10%–20% 的 T1（初始 15%）；版本冲突、同位置多 CVE、公报与源码不一致、`version_only` 条目强制全查。详见 `REVIEW_SAMPLING.md`。

## 评分

存在性 Recall 的分母是该 SHA 上已确认的 S1/S2 known-positive；源码定位 Recall 的分母是同口径中 `location_scope=source_location` 的条目。不应声称是全部真实漏洞，也不应把 `version_only` 条目算进源码定位分数。函数级标注不能用作精确行级 ground truth。严重程度缺失/冲突时，存在性仍可评分，但 severity 维度应标记不可评估。
