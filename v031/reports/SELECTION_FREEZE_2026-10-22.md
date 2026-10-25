# 选版冻结记录 — 2026-10-22

本记录只说明「哪些目标已冻结、依据是什么」。它**不是**发布声明，
也不是 50 仓库目标选择完成或 `PASS_KNOWN_SWEEP` 的证明。

## 输入

- 选版审查：`v031/reviews/selection_review_2026-10-22.jsonl`
  （审查者 `independent-review-agent-2026-10-22`，与 `selected_by` 不同）
- 隔离审查包：`v031/reviews/selection_packets/`（22 个，只含原始事实）
- 源码导出：`data/snapshot_exports.jsonl`（22/22 `exported`）
- 审计导出：`data/snapshot_audit_exports.jsonl`（22/22 `exported`，剩余 advisory ID 0）
- 应用工具：`v031/scripts/apply_selection_review.py --apply`

## 结果：12 frozen / 10 保持 proposed

| 仓库 | tag | commit date | 冻结时正样本锚点 |
|---|---|---|---|
| jenkinsci/jenkins | `jenkins-2.441` | 2024-01-16 | 6 |
| nodejs/undici | `v5.19.0` | 2023-02-13 | 3 |
| expressjs/express | `4.19.2` | 2024-03-25 | 1 |
| vitejs/vite | `v5.0.11` | 2024-01-05 | 4 |
| libarchive/libarchive | `v3.7.7` | 2024-10-13 | 1 |
| symfony/symfony | `v5.4.45` | 2024-10-27 | 18 |
| DaveGamble/cJSON | `v1.7.16` | 2023-07-05 | 1 |
| curl/curl | `curl-8_3_0` | 2023-09-13 | 2 |
| rustls/rustls | `v/0.23.4` | 2024-03-25 | 1 |
| pallets/flask | `2.3.1` | 2023-04-25 | 1 |
| laravel/framework | `v11.30.0` | 2024-10-30 | 1 |
| pallets/werkzeug | `3.0.2` | 2024-04-01 | 1 |

合计 40 条 anchor（每条都在 OSV/GitHub Advisory 中确认该 tag 受影响且有 https URL）。
冻结行同时记录 `snapshot_export_id`、`snapshot_export_sha256`、`audit_export_id`、
`audit_archive_sha256`、`legacy_selection_reason` 与 `leakage_controls`。

## 10 个未冻结（仍为 proposed，审查拒绝）

| 仓库 | tag | commit date | 拒绝原因 |
|---|---|---|---|
| netty/netty | `netty-4.1.59.Final` | 2021-02-08 | `obsolete_release_over_4_years` |
| guzzle/guzzle | `7.4.4` | 2022-06-09 | 同上 |
| phoenixframework/phoenix | `v1.6.13` | 2022-09-29 | 同上（约超 4 年 23 天） |
| gin-gonic/gin | `v1.5.0` | 2019-11-24 | 同上 |
| protocolbuffers/protobuf | `v3.20.1` | 2022-04-22 | 同上 |
| hyperium/hyper | `v0.14.2` | 2020-12-29 | 同上 |
| JamesNK/Newtonsoft.Json | `12.0.3` | 2019-11-09 | 同上 |
| django/django | `3.0.2` | 2020-01-02 | 同上 |
| libexpat/libexpat | `R_2_4_4` | 2022-01-30 | 同上 |
| rack/rack | `2.2.3` | 2020-06-15 | 同上 |

拒绝仅来自审查第 2 项（release sanity）；tag 解析、哈希、无 `.git`、计数对账均通过。
审查者明确指出 4 年阈值不区分维护分支；本记录不推翻审查结论，也不自动改选新版本。
若要继续，必须先在新 tag 上取得源码级正样本再选版。

## 泄漏控制现状（诚实边界）

- `worktree_without_git_history=true`、`ground_truth_isolated=true`：
  审计归档不含 `.git`，且 advisory ID 已清零。
- `network_policy=off` 是声明的评测策略，`runtime_enforcement=pending_harness`：
  目前没有评测 harness 执行该策略，不能声称运行时已强制断网。
- 审计导出是字符串级控制；不含 advisory ID 的修复说明仍可能存在于树中。

## 追加（2026-10-23，本地日期）：ruby/rexml v3.4.1

- 路线与上表不同：先在该 tag 上取得 **A 级正样本**（CVE-2025-58767，独立 reviewer red/green 复现），
  再导出并提交隔离选版审查。
- 审查文件：`v031/reviews/selection_review_2026-10-23.jsonl`；verdict=accept，
  四项导出检查（archive/manifest 哈希、无 `.git`、计数对账）全 true，tag peel 一致，
  anchor 由 GHSA/OSV/NVD 三源确认。
- 结果：`snap_23dff8507560a593` 冻结，`vulnerability_count_at_selection=1`；
  P6 审计导出排除 `NEWS.md`，剩余 advisory ID 0。评测必须使用 audit 归档。
- 该目标的 coverage 仍为 `NEEDS_REVIEW`，不构成 `PASS_KNOWN_SWEEP` 声明。

## 追加（2026-10-23）：django 4.2.13 与 rack v3.1.13

两者路线相同：先在候选稳定 tag 上取得 **A 级正样本**（独立 reviewer red/green），再导出全树、
做 P6 审计导出、提交隔离选版审查。旧目标 django 3.0.2 与 rack 2.2.3 的 selection 行已归档
（`data/legacy_evaluation_selection_*.jsonl`），对应快照改为 `historical_evidence`。

| 仓库 | tag | commit | 审查文件 | 结果 |
|---|---|---|---|---|
| django/django | `4.2.13` | `3bf46e2e023904c825728267f3131c42f02ce696` | `v031/reviews/selection_review_django_2026-10-23_r2.jsonl` | 第一轮 reject（审计泄漏 Sphinx `:cve:` 角色）→ 修复 → 第二轮 accept，已冻结 |
| rack/rack | `v3.1.13` | `037953789da9cd49c4a3453ade6ede13619276e0` | `v031/reviews/selection_review_rack_2026-10-23.jsonl` | 首轮 accept，已冻结 |

- django 审查复算：6,729 个文件逐字节匹配 tag tree、6,615 文件全字节扫描 0 泄漏、114 个排除路径对账；
- rack 审查复算：180 个 blob 全部匹配 tree、179 文件全字节扫描 0 泄漏（排除 `CHANGELOG.md`）；
  审查者记录 packet 的 `tag_commit_tree_sha` 为 null，但 tree 已独立验证，不影响结论。
- 当前 23 个评测目标：**16 frozen / 7 proposed**（余下 7 个均为 legacy `documented_exception`）。
- 两个目标的 coverage 仍为 `NEEDS_REVIEW`，不构成 `PASS_KNOWN_SWEEP` 声明。

## 追加（2026-10-23）：libexpat R_2_6_2

- 路线同上：先在候选稳定 tag 上取得 **A 级正样本**（CVE-2024-45490，独立 reviewer 用两步 harness
  复现 ASan heap-buffer-overflow，R_2_6_3 修复版无崩溃），再导出全树、做 P6 审计导出、提交隔离选版审查。
- 旧目标 R_2_4_4（`snap_d33251dac37c334c`）的 selection 行归档至
  `data/legacy_evaluation_selection_80314213.jsonl`；快照改为 `historical_evidence`；其 143 条 triage、
  7 条 status 与 export/audit 行分别归档为 `data/legacy_*_snap_d33251dac37c334c.jsonl`。
- 审查文件：`v031/reviews/selection_review_libexpat_2026-10-23.jsonl`；verdict=accept，
  四项导出检查全 true、tag peel 一致（R_2_6_2 → `fa75b96546c069d17b8f80d91e0f4ef0cde3790d`）、
  4 条 https anchor 确认。
- 结果：`snap_67132f0363b8bc23` 冻结，`vulnerability_count_at_selection=4`；P6 审计导出排除
  `expat/Changes`、替换 `expat/tests/basic_tests.c` 中的 advisory ID，剩余 0。
- 同轮把 R_2_4_4 时代的 7 个旧 CVE 在新快照上以修复区间 + fix commit 祖先关系判为
  `confirmed_not_affected`（排除性证据，见 `runs/verification/libexpat_R_2_6_2_fixed_previous/NOT_APPLICABLE.md`）；
  新快照其余 135 条候选保留 `unknown`。coverage 仍为 `NEEDS_REVIEW`，不构成 `PASS_KNOWN_SWEEP` 声明。

## 追加（2026-10-23）：phoenixframework/phoenix v1.8.8

- 路线同上（先证据、后选版）：旧目标 v1.6.13（2022-09-29）仅因超过 4 年被拒；本次先在 v1.8.8
  取得两个独立正样本 verdict —— CVE-2026-56811（静态复核，grade B，`16e295d2` 修复于 1.8.9）
  与 CVE-2026-56812（grade A，Node red/green 对同一 tag blob 20/20 抛错、1.8.9 为 0/20，
  复现见 `runs/independent/phoenix_CVE-2026-56812_v188_round1/repro/`），再注册快照并导出。
- 新快照 `snap_aca73214a7703174`（commit `99df0a99da13265cb8b5cd3a506a79b3de34339f`，478 文件）；
  源码导出 sha256 `e225eeb0…`；P6 审计导出 `aud_aca73214a7703174`（排除 `CHANGELOG.md`、
  `guides/security.md`，替换 0，剩余 advisory ID 0）。旧 v1.6.13 的快照、triage、export/audit、
  status、evidence、location、review 与 selection 行均已归档到 `data/legacy_*_snap_ee79f4175242bbee.jsonl`
  和 `data/legacy_evaluation_selection_16072585.jsonl`。
- 审查文件：`v031/reviews/selection_review_phoenix_2026-10-23.jsonl`，审查者
  `independent-reviewer-deepseek-flash-20261023`。首轮 `build_ok=false`（环境无 Elixir）；
  补齐用户级 Erlang/Elixir 后由该审查者自行从导出包重新解压重建（`mix deps.get`、`mix compile`
  均 exit 0，产出 92 个 beam），改判 `build_ok=true`，总判定 `accept`。
- 结果：`snap_aca73214a7703174` 冻结；`vulnerability_count_at_selection=1`（这是审查者核验的
  锚点数，仅 CVE-2026-56811；同一快照另有 CVE-2026-56812 经另一独立 reviewer 验证，数据集在该
  快照的 live `confirmed_affected` 为 2）。
- 同快照 8 条候选全部 triage：CVE-2026-56811 与 CVE-2026-56812 各两条 discovery 路径记
  `confirmed_affected`；CVE-2022-42975、CVE-2017-1000163 与 CVE-2026-32689 的两条路径记
  `confirmed_not_affected`（均给出代码级排除与修复 commit 祖先关系，而非仅比较版本号）。
- 当前 23 个评测目标：**17 frozen / 6 proposed**（余下 6 个均为 legacy `documented_exception`）。
