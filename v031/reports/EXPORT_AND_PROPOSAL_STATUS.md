# 源码导出、审计导出与选版提案状态（2026-10-22）

> **2026-10-23 更新（phoenix）**：phoenixframework/phoenix 由 v1.6.13 升级到 v1.8.8
> （`snap_aca73214a7703174`，commit `99df0a99…`，478 文件）。先取得 CVE-2026-56811 与
> CVE-2026-56812 的独立验证，再选版：源码导出（sha256 `e225eeb0…`）与 P6 审计导出
> （`aud_aca73214a7703174`，排除 `CHANGELOG.md`、`guides/security.md` 两个文件，剩余 advisory ID 0）
> 均为 `exported`；独立 selection review 在补齐 Elixir/Erlang 工具链并自行重建（`mix deps.get` /
> `mix compile` 均 exit 0）后判定 `accept`，该行已冻结。旧 v1.6.13 的导出行、审计行与选版行已归档到
> `data/legacy_*_snap_ee79f4175242bbee.jsonl` 与 `data/legacy_evaluation_selection_16072585.jsonl`。
> 当前为 **23 个目标导出、23 个审计导出（共排除 130 个文件、替换 10 个文件、剩余 advisory ID 0）、
> 6 个 legacy proposed、27 个未选仓库提案（120 tag）**。
>
> **2026-10-23 更新**：新增 ruby/rexml v3.4.1（`snap_23dff8507560a593`）、django 4.2.13
> （`snap_516aa9971dd9509d`，取代 3.0.2）、rack v3.1.13（`snap_245aee01ea5112b9`，取代 2.2.3）与
> libexpat R_2_6_2（`snap_67132f0363b8bc23`，取代 R_2_4_4）——四者的源码导出与 P6 审计导出均
> `exported`（rexml 196 文件、django 6,729 文件、rack 180 文件、libexpat 199 文件 / 198 regular +
> 1 symlink；各自剩余 advisory ID 0），并分别通过独立选版审查后冻结。审计扫描器升级为
> `build_audit_exports/1.1`（识别 Sphinx `:cve:` 角色、全文扫描）。
> `snapshot_proposals.jsonl` 已移除被取代的 rexml 行，归档于
> `runs/selection/superseded_snapshot_proposals.jsonl`）。下文为 10-22 原始记录。

本文件记录 P0/P1 阶段的可复现产物。冻结结论见
`v031/reports/SELECTION_FREEZE_2026-10-22.md`；本文件**不是**发布声明，也不是漏洞确认。

## 1. 已选 22 个目标的完整源码导出

- 工具：`v031/scripts/freeze_snapshots.py`（`freeze_snapshots/1.0`）
- 数据表：`data/snapshot_exports.jsonl`（22 行，全部 `status=exported`）
- 产物：`exports/<owner>__<repo>/<snapshot_id>.tar.gz` + `.manifest.jsonl`
- 导出方法：`git ls-tree -r` + `git cat-file --batch` 重建**全部 tracked tree**，
  绕开 `.gitattributes export-ignore`（`source_completeness=full_tracked_tree_including_export_ignored_paths`）。
- 确定性：gzip `mtime=0`、固定成员 mtime=commit 时间、uid/gid=0、路径排序。
- 对账：22/22 仓库 `missing_from_archive_count=0`；`exported_file_count + symlink_count == tree_file_count`
  （django 4 / libexpat 1 / rustls 3 / vite 1 个 symlink；protobuf 2 个 gitlink 不导出）。
- 标签一致性：21 个 `tag_commit`；express `4.19.2` 标签 peel 到 `04bc627`，记录 commit 为
  `b28db2c`（npm `gitHead`），两者 `^{tree}` 相同，按 `accepted_via=identical_tree` 接受。
- 泄漏扫描：无 `.git` 元数据；逐文件记录 CVE/GHSA 字符串命中的文件（上游 CHANGES/SECURITY 文档，
  不是 oracle 文件）。
- 构建可行性：仅检测构建系统指示文件与本地工具链，**未执行构建**。

## 2. 28 个未选仓库的 tag 提案

- 工具：`v031/scripts/propose_missing_snapshots.py`
- 数据表：`data/snapshot_proposals.jsonl`（28 行）
- 结果：26 个仓库有候选（125 个 tag），2 个仓库无候选
  （openssl/openssl、nlohmann/json：缓存中的 OSV 范围只有 commit-hash 边界或开放区间，
  无法在发布 tag 之间作出区分）。
- 提案依据：OSV + GitHub Repository Advisory 的**有界**版本区间；语义化版本比较只用于
  **浮现**候选，不用于证明不存在。
- 已排除的伪候选：
  - 预发布/dist tag（`2.0.0-rc3`、`4.17.4-amd`、`vsix-22.2.0`）；
  - 子 crate 标签（actix-web 的 `http-v3.12.0`、`awc-v3.10.0`）；
  - FIPS/通道标签（`FIPS_TEST_10`）；
  - commit-hash 被误读为版本号的 OSV 区间；
  - 只有下界、没有上界的开放区间（无法区分版本，通常是截断数据）；
  - 显式版本列表中的预发布（如 `OpenSSL_1_1_1-pre1`）不再匹配稳定 release。
- 每个候选都带 blocker：`source_level_confirmation_at_tag_commit_pending`、
  `independent_selection_review_pending`、`known_positive_oracle_review_pending`。
- **尚未选定任何未选仓库的版本**，也未为其创建 oracle 行。

## 3. P6 泄漏收敛的审计导出

- 工具：`v031/scripts/build_audit_exports.py`（`build_audit_exports/1.0`）
- 数据表：`data/snapshot_audit_exports.jsonl`（22 行，全部 `status=exported`）
- 产物：`exports/<owner>__<repo>/<snapshot_id>.audit.tar.gz` + `.audit.manifest.jsonl`
- 规则：含 CVE/GHSA ID 的 changelog/security 文档整文件排除；代码/测试文件只就地替换
  advisory ID 为 `ADVISORY-ID-REDACTED`，保留可执行语义；每次排除/替换均记录路径与原 SHA256。
- 结果：排除 50 个文件、替换 10 个文件、**剩余 advisory ID 0**；归档产出后重新扫描确认。
- 局限：这是**字符串级**泄漏控制，不识别不含 ID 的修复说明或外部 advisory 链接；
  完整树仍保留在 `exports/*.tar.gz` 作为可复现记录，不用于暴露给被评测 agent。

## 4. 独立选版审查结果

- 审查文件：`v031/reviews/selection_review_2026-10-22.jsonl`（22 行）
- 审查者：`independent-review-agent-2026-10-22`，未读取收集器理由字段；审查者 ≠ 选择者。
- 结果：**12 accept / 10 reject**；10 个 reject 仅因「tag 发布超过 4 年且存在更新稳定版」，
  其余 5 项检查（tag 解析、归档哈希、清单哈希、无 `.git`、计数对账）全部通过。
- 已按 `v031/scripts/apply_selection_review.py --apply` 写入：12 行 `decision_status=frozen`
  （合计 40 条已验证正样本锚点），10 行保持 `proposed` 并记录 `selection_review_reasons`。
- 审查者 caveat：4 年规则是字面阈值，不识别分支维护线（例如 netty 4.1.x、symfony 5.4.x）。
  被拒目标没有被重新选版，也未先选后补证据。

## 5. 仍未完成

- 6 个被拒目标（phoenix 已在 v1.8.8 取得正样本并冻结）与 26 个提案仓库的源码级正样本确认
  （先证据、后选版；禁止先选后补）。
- 1203 条 `unknown` 候选与 27 个未选仓库的候选行相关性核验。
- 两轮快照限定检索（`PASS_KNOWN_SWEEP`）。
- 动态复现现有 5 条 grade A（rexml/django/rack/libexpat 的构建级验证，以及 phoenix CVE-2026-56812
  的 Node red/green 复现），其余 live 正样本仍为 B 级静态验证；
  工作树级网络隔离尚待 harness 运行时实施。
