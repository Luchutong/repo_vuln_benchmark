# 数据质量发现（2026-10-21）

本文件记录在候选核验中发现的**不得直接采用**的源数据问题。每条都指明
受影响的仓库、证据路径和处置。发现问题不等于漏洞结论；未解决的条目仍停留在
`in_validation` / `pending_*`。

## 1. lodash CVE-2026-4800：修复提交与修复版本互相矛盾

- 仓库：`lodash/lodash`，候选 `disc2_29cd55fbcc05a5cf28a87b78`
- OSV/GHSA-r5fr-rjxr-66jc（`runs/raw/osv/a66d1063...json`）声明
  `introduced 4.0.0`、`fixed 4.18.0`，同时给出
  `last_known_affected_version_range <= 4.17.23`。
- CVE List v5 CNA 记录（`runs/verification/express_lodash/sources/CVE-2026-4800_cve.json`，
  assigner `openjs`）声明 `4.0.0 <= v < 4.18.1`，即修复版本是 **4.18.1**。
- OSV 记录引用的修复提交 `3469357cff396a26c363f8c1b5a91dde28ba4b1c` 同时被
  CVE-2021-23337 / GHSA-35jh-r3h4-6jhm（2021 年）引用。该提交是 2021 年
  `_.template` 命令注入的修复，早于 2026 年公告约五年，不能作为 2026 年
  导入键名注入的修复证据。
- 处置：**不提升**。在候选备注中记录冲突；需要上游仓库在 4.18.0/4.18.1
  之间的实际 diff 或新公告引用才能闭合 fix commit 与 fixed release。

## 2. express CVE-2024-51999：官方已 REJECTED

- CVE List v5 记录（`runs/verification/express_lodash/sources/CVE-2024-51999_cve.json`）
  `state = REJECTED`，`dateRejected = 2025-12-02`，CNA 原文：
  "DO NOT USE THIS CANDIDATE NUMBER ... issued in error and is not a valid vulnerability."
- 处置：**永不进入** `data/vulnerabilities.jsonl`。若后续发现同名候选，
  状态必须为 `rejected`，并引用该 CVE 记录。

## 3. express 4.19.2：npm gitHead 与 GitHub tag 指向不同提交（内容相同）

- npm registry `gitHead = b28db2c12c3bd9cd763316824446f79bf81e0686`；
- `refs/tags/4.19.2^{}` = `04bc62787be974874bc1467b23606c36bc9779ba`；
- 两者 `tree` 均为 `f18a74c2f183fd0ab2bd3b411ddd44b792d4481a`，即内容完全相同，
  只是父提交不同（分支历史重写/拣选）。
- 处置：漏洞快照记录 npm 发布提交 `b28db2c`，并在
  `runs/verification/express_cve_2024_43796/git_object_checks.txt` 中留存
  tag 提交与 tree 相等证据。

## 4. express 5.0.0：tag 前缀不一致

- 4.x 使用 `4.20.0`，5.x 稳定版使用 `v5.0.0`（`refs/tags/v5.0.0` =
  `344b022fc7ed95cf07b46e097935e61151fd585f`）。
- 处置：`fixed_releases` 中按真实 tag 记录，不能把 `5.0.0` 当作 tag 名去拼 URL。
  `https://github.com/expressjs/express/releases/tag/5.0.0` 返回 404，
  `.../tag/v5.0.0` 返回 200。

## 5. Flask 修复 tag 为 annotated tag

- `2.3.2` 解引用到 `f3b8f570...`，`2.2.5` 解引用到 `47af817c...`。
- 处置：`fixed_releases.tag` 记录标签名，内容核验使用解引用后的提交；见
  `runs/verification/flask_cve_2023_30861/fixed_content_checks.txt`。

## 6. GHSA 编号大小写与 schema 不符

- `schemas/vulnerabilities.schema.json` 原模式 `^GHSA-[0-9A-Z-]+$` 拒绝真实
  的混合大小写 GHSA 编号（如 `GHSA-qw6h-vgh9-j6wx`）。
- 处置：模式放宽为 `^GHSA-[0-9A-Za-z-]+$`；这是 schema 缺陷修正，不改变任何
  已记录数据。

## 7. 结构校验器的大小写缺陷与 starter 文件偏离

- `scripts/validate_dataset.py` 把别名集合整体转大写后，又用原始大小写的
  `vulnerability_id` 去比较，导致合法的混合大小写 GHSA 记录被判为
  “ID missing in alias list”。已改为大小写不敏感比较。
- 这两个文件原本列在 manifest 的 `frozen_starter_files_sha256` 中。修改后
  `validate_preselection.py` 会报告 SHA-256 不匹配；处置是把新哈希写回，
  并在 `manifest.json` 的 `starter_file_deviations` 中保留原始哈希、当前哈希
  和修改原因，验证器重新通过（266 个摘要一致）。
- 未修改原始 starter zip；偏离仅限上述两个逻辑缺陷。

## 8. gin CVE-2020-36567：公告引用的 PR 并未合并

- GHSA/OSV、CVE List v5 与 GO-2020-0001 都引用
  `https://github.com/gin-gonic/gin/pull/2237` 作为修复链接。
- 独立复核通过 GitHub API 观察到 PR 2237 为 `closed`、`merged: false`；
  实际合入的是 PR 2277，其 `merge_commit_sha` 为
  `a71af9c144f9579f6dbe945341c1df37aaf09c0d`（"removing log injection (#2277)"）。
- 公告给出的 commit SHA 本身正确，只有 PR 链接误导。处置：dossier 的
  `references` 保留原始引用以供审计，根因结论以 commit 内容为准；本条目记录
  该差异，不据此否定漏洞。

## 9. Newtonsoft.Json CVE-2024-21907：修复提交链与溢出阶段描述不一致

- advisory 只引用 `7e77bbe1...`（"default max depth to 128"），但 13.0.1
  实际发货的默认值是 **64**：后续 `b6dc05be...`（"Change MaxDepth default
  to 64 (#2473)"）也在 13.0.1 祖先中，且未被 advisory 引用。
- 13.0.1 源码里的 XML 注释仍写 "The default value is 128"，与代码的 64 不符；
  这是修复发行版内部的文档不一致，不影响修复效果。
- CNA/NVD 称 `JsonConvert.DeserializeObject` 可触发 StackOverflowException；
  OSV 称反序列化主要是 CPU/RAM 消耗、序列化深 JToken 时才栈溢出。独立复核
  读源码后支持后者：reader 使用显式 `List<JsonPosition>` 栈，递归发生在
  JToken/对象图序列化阶段。两者指向同一根因（默认无深度上限）。
- 处置：dossier 的 `fix_commits` 同时记录 `7e77bbe1` 与 `b6dc05be`，
  `fixed_releases.verified_content` 记录实际发货值 64；不删改公告原文。

## 10. Netty CVE-2021-21295：公告指向的类与真实缺陷位置不一致

- advisory 正文把问题归到 `Http2MultiplexHandler`，但该类在 4.1.59.Final
  没有任何 Content-Length 处理逻辑；缺陷实际位于
  `DefaultHttp2ConnectionDecoder` 的 `onHeadersRead` / `onDataRead`。
- 修复提交 `89c241e3...` 的 subject 是 "Merge pull request"，但对象只有一个
  父提交；可达性因此用 `merge-base --is-ancestor` 与 GitHub compare 双重确认。
- 版本写法分歧：NVD 用 `versionEndExcluding: 4.1.60`，CNA/OSV 用
  `4.1.60.Final`；OSV 另有 `io.netty:netty`、`org.jboss.netty:netty`
  两个开放式聚合坐标（introduced 0、无 fixed），比已验证的
  `netty-codec-http2` 范围更宽。
- 处置：dossier 只声明已核验的 `netty-codec-http2` 范围；位置以源码为准；
  `source_crosscheck.notes` 记录聚合坐标差异，不据此扩大受影响声明。

## 11. hyper CVE-2021-21299：CVSS 双评分与 0.12 分支范围缺失

- CNA/GitHub advisory 与 OSV 使用 `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`
  （4.8 MEDIUM）；NVD 主评分与 RUSTSEC 使用
  `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H`（8.1 HIGH）。
  两者描述同一解析缺陷，但影响假设不同。处置：正式 severity 采用 NVD primary
  8.1，并在 dossier 的 `alternate_scores` 保留 4.8；不合并成一个分数。
- CNA/NVD 只声明 `< 0.13.10` 与 `>=0.14.0, <0.14.3`，未给 0.12 分支下界；
  OSV/GitHub/RUSTSEC 另有 `>=0.12.0, <0.12.36`。独立复核还确认
  `v0.12.36` 与 `v0.13.10` 已含修复，而 `v0.12.35`、`v0.13.9` 仍脆弱。
  NVD 的 CPE `>=0.12.0, <0.13.10` 无法表达 0.12.36 已修复，因此仍把
  0.12.36 标为脆弱。处置：dossier 只声明实际读过的 0.14.x 范围；其余分支
  记录在此，不扩大真值矩阵。
- 公告正文只提 0.14.3 与 0.13.10，未提 0.12.36；该 tag 确实含同一修复。
- 各源发布时间不同（CVE 2021-02-11、GHSA 2021-08-25、fix commit 2021-02-05），
  不影响身份判定。

## 12. Vite CVE-2024-23331：平台限定、四分支修复提交与版本边界写法

- CNA 文字说影响“case-insensitive file systems”（典型为 Windows），但 NVD 的
  CPE applicability 用 `AND` 叠加了 Windows OS 条件；Linux 上大小写敏感的文件系统
  不在 NVD 的可适用配置内。处置：dossier 的 `limitations` 明确写出该前提，
  不把漏洞描述成所有平台可用。
- OSV 为四个发行线各列一个 fix commit（`2.9.17`、`3.2.8`、`4.5.2`、`5.0.12`）；
  CNA/NVD 的 references 只列 5.x 的 `91641c4...`。独立复核确认 5.x 的
  `91641c4` 是 `v5.0.12` 的直接父提交；本目录只验证并声明 5.x 范围。
  另外确认 `eeec23b` 是 `v4.5.2` 的祖先、`a26c87d` 是 `v3.2.8` 的祖先，
  但未逐行审查其内容。
- 版本边界写法不同：CNA 用 `<5.0.12`，OSV 用 `fixed: 5.0.12` 事件，
  NVD 用 `versionEndExcluding: 5.0.12`；三者语义一致，不是冲突。
- 2.x 的受影响范围从 `2.7.0` 开始，因此 2.0–2.6 不在任何源的声明内；
  这是范围下界，不是遗漏。
- 处置：dossier 的 `affected_packages` 只声明 `>=5.0.0,<5.0.12`；
  位置以 `index.ts:620` 的 matcher 构造为准，`static.ts:216` 作为消费点。

## 13. protobuf CVE-2022-1941：公告未给修复提交，CNA/NVD 评分不一致

- GHSA-8gq9-2x98-w8hf、CVE List v5 与 NVD 都没有给出修复 commit；仅在 CNA 正文列出
  protobuf-cpp 的修复版本（3.18.3/3.19.5/3.20.2/3.21.6）。
- 在 v3.20.1..v3.20.2 的上游历史中定位到 `b4c395aae`（"Apply patch"），其 diff 为三个 MessageSet
  解析器加入 `enum class State { kNoTag, kHasType, kHasPayload, kDone }` 并跳过重复 payload。
  已用 `merge-base --is-ancestor` 证明它属于 v3.20.2 而不属于 v3.20.1；该提交未被任何公告引用。
- 评分分歧：CNA `metrics.other` 为 5.7 MEDIUM（AV:A/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H）；
  NVD primary 与 OSV 为 7.5 HIGH（AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H）。正式 severity 取 NVD
  primary，CNA 分数作为 alternate score 保留，不合并。
- CWE 分歧：CNA 记录 CWE-1286；NVD 自身的主 weakness 是 `NVD-CWE-Other`，CWE-1286 出现在
  Google 来源的 secondary 条目；CWE-119 只在 GHSA/OSV 的 `database_specific.cwe_ids` 中。
  dossier 将 CWE-1286 作为主 CWE、CWE-119 作为附加映射，并在此保留 NVD-CWE-Other 的归属差异。
- OSV 只有 PyPI 坐标（四个区间），没有 C++ 生态记录；dossier 只声明 CNA/NVD 都能支持的
  protobuf-cpp `>=3.20.0,<3.20.2`，不把 PyPI 区间平移到 C++。
- 处置：只声明已核验的 3.20.x 分支；3.18/3.19/3.21/4.21 的修复未逐行核验，留在 limitations。

## 14. OpenSSL CVE-2022-0778：无候选行，探查材料保留但不提升

- `runs/verification/openssl_cve_2022_0778/` 只有 sources，没有 dossier；`data/candidates.jsonl`
  中也没有 CVE-2022-0778 的候选行。
- 未伪造候选，也未用该 CVE 填充真值矩阵。材料与 3.0.1 快照
  `snap_10d458b485bb6210` 保留为非评测快照，说明见该目录 README。
- 分支差异已记录在 `sources/git_object_checks.txt`：master 的修复提交不在 3.0.2 祖先链上，
  3.0 分支另有 `a466912611aa...`。

## 15. Phoenix CVE-2022-42975：公告引用的修复提交不在修复 tag 的祖先链上

- GHSA-p8f7-22gq-m7j9 / CVE-2022-42975 的公告、NVD references 与 OSV 都只引用
  `6e7185b33a...`（"Fix wildcard check_origin vulnerability."）。
- 该提交位于 mainline，**不是** `v1.6.14` tag（`50b48541...`）的祖先；`git merge-base
  --is-ancestor` 返回 1。1.6.14 是在 1.6 分支上切出的，包含另一个等价提交
  `b2fc631f00...`（同一 subject，同一 hunk），后者才是 1.6.14 的祖先、且不在 1.6.13 中。
- 两处 diff 的受影响 hunk 完全相同：
  `String.ends_with?(request_host, allowed_host)` 改为
  `request_host == allowed_host or String.ends_with?(request_host, "." <> allowed_host)`；
  `b2fc631` 另加回归测试。
- 处置：dossier 的 `fix_commits` 同时列出 `b2fc631`（release-line，canonical）与
  `6e7185b`（advisory-cited mainline），`fixed_releases.verified_content` 以 v1.6.14
  实际内容为准；记录差异，不把公告引用当作 release 祖先。
- CNA 记录仍是最小集（product/version n/a、无 CVSS、无 CWE）；7.5 HIGH 来自 NVD。
  NVD 自身的主 weakness 是 NVD-CWE-Other，CWE-863 出现在 CISA-ADP 的 secondary 条目；
  OSV 元数据同时列 CWE-346 与 CWE-863。dossier 采用 CWE-863/CWE-346，并在此保留
  NVD-CWE-Other 的归属差异。

## 16. Werkzeug CVE-2024-34069：公告修复提交是 merge，NVD 无独立分析

- GHSA-2g68-c3qc-8985 / CVE-2024-34069 引用 `3386395b24c7371db11a5b8eaac0c91da5362692`，
  该提交是 "Merge pull request from GHSA-2g68-c3qc-8985"，真正改动在第二父提交
  `890b6b62...`（其父为 `71b69dfb...`，引入 `trusted_hosts`）。
- 三个提交都不在 3.0.2 中、都是 3.0.3 的祖先；`3386395` 与 3.0.3 release 提交之间只有 1 个提交。
- NVD 记录里没有任何 Analyst 评估：CVSS 7.5 与 CWE-352 都来自 `security-advisories@github.com`
  的 Secondary 条目，NVD references 也只是 GitHub 链接的重复。因此 NVD 在此不是独立佐证，
  dossier 的 `source_crosscheck.notes` 已声明。
- 修复提交没有附带回归测试（改动仅 CHANGES.rst、docs/debug.rst、debug/__init__.py、
  debugger.js、sansio/utils.py、serving.py），所以没有可引用的上游测试作为静态旁证。
- `host_is_trusted` 本身早在 0.9 就存在；修复只是让 debugger 复用它，不是新增机制。

## 17. rustls CVE-2024-32650：同一漏洞三个 release line 各有一个修复提交

- 公告、CVE v5 与 OSV 共列出 5 个提交：`2123576`（回归测试）、`6e938bc`（0.23 线 bail-out）、
  `f45664f`（close_notify 处理）、`5374108`（0.22 线）、`ebcb478`（0.21 线）。
- 只有 `6e938bc`、`2123576`、`f45664f` 被证明是 `v/0.23.5` 的祖先且不在 `v/0.23.4` 中；
  `5374108` 是 `v/0.22.4` 的祖先但不是 0.23.5 的祖先；`ebcb478` 既不在 0.22.4 也不在 0.23.5
  （其所属 0.21 tag 未拉取）。
- 处置：dossier 只声明 `>=0.23.0,<0.23.5`，不把 0.21/0.22 的修复平移到 0.23；其余分支留在 limitations。
- NVD 与 werkzeug 的情况相同：只有 GitHub secondary 指标，没有独立分析。
- 公告自带 Python PoC，按要求未执行；只用上游 Rust 回归测试作为静态旁证（也未运行）。

## 18. undici CVE-2023-23936：同一 CVE 出现三套 CVSS 向量与两套 CWE

- CNA（GitHub_M）与 NVD secondary：`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N` = 6.5 MEDIUM。
- NVD primary（nvd@nist.gov）：`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N` = 5.4 MEDIUM。
- OSV `severity` 另给 `PR:L/UI:R` 变体，没有 base score。
- CWE：CNA 与 NVD secondary 为 CWE-93（CRLF Injection），NVD primary 为 CWE-74（注入）。
- 处置：正式 severity 取 NVD primary 5.4/UI:R，CNA 6.5 作为 alternate 记录；
  `cwe_ids` 同时保留 CWE-93 与 CWE-74，并在 `source_crosscheck` 说明来源，不合并成单一值。
- 修复提交 `a2eff05` 标题是 "Merge pull request..."，但只有一个父提交（v5.19.0 tag commit），
  不存在单独的分支组件提交；公告引用的就是该提交。

## 19. cJSON CVE-2023-50471：修复提交本身先写错，需两个提交才正确

- 公告族：MITRE CNA 无 CVSS、无 CWE、受影响版本写 `n/a`；NVD 给唯一评分
  7.5 HIGH（`AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`）与 CWE-476，CPE 只列 1.7.16；
  Debian OSV 把范围写成 introduced 0、fixed 1.7.17-1，并为 Debian 12 提供
  `1.7.15-1+deb12u1` 回移。
- 上游修复由两个提交组成：`60ff122`（"add NULL checkings (#809)"，同时修
  CVE-2023-50472）先加了 `newitem == NULL` 和一项损坏检查，但检查写成了
  `newitem->prev == NULL`——此时 `newitem->prev` 尚未赋值，等于拒绝合法的非首位插入；
  `f66cbab`（"fix error in null checkings (#810)"）改为 `after_inserted->prev == NULL`。
  两者都在 v1.7.17，v1.7.16 都没有。
- 根因行 2287（`newitem->prev->next = newitem;`）与 issue #802 的描述、版本提交
  `cb8693b`（v1.7.16 tag commit）逐字吻合；但 issue 的机理描述并不准确：2279 行先把
  `after_inserted->prev` 赋给 `newitem->prev`，所以 2287 行的 NULL 来自被破坏数组元素的
  prev，而不是“newitem 没有 prev”；`newitem == NULL` 的更早崩溃点在 2278 行。维护者在
  issue 中表示无法按原报告复现，只有手工把元素的 prev 置 NULL 才可触发。触发状态需要
  一个 prev 为 NULL 的数组元素，公开解析器不会构造该形状，可达性取决于调用方对 API
  的使用，NVD 的 `AV:N` 未体现这一约束。
- 同一修复提交混入 CVE-2023-50472（`cJSON_SetValuestring`）改动；本档案只对
  CVE-2023-50471 建档，未把另一 CVE 当成本条的修复内容。
- 处置：`affected_range` 取上游修复边界 `<1.7.17`，NVD 较窄的 CPE 范围与可达性限制
  保留在 limitations，不静默合并。

## 20. libarchive CVE-2025-5915：OSV 的 fixed commit 是 release 提交，NVD 无 Primary 指标

- OSV 把范围转成 GIT `introduced 0 → fixed 70ff28fc`，`70ff28fc` 是 v3.8.0 的
  release 提交而不是源码修复提交；真正的修复是它的祖先 `a612bf62`
  （"rar: Fix heap-buffer-overflow (#2599)"），已用祖先检查确认在 3.8.0 中、
  不在 v3.7.7 中。
- v3.7.7 与 v3.8.0 都是 annotated tag：tag 对象分别是 `7ce42547`、`2ed9bd7b`，
  peel 后才是 `b439d586`、`70ff28fc`；不 peel 的祖先检查会得到错误结论。
- NVD 的两个 CVSS 条目（Red Hat 与 nvd@nist.gov）都标为 **Secondary**，没有
  Primary 分析；两个向量相同（6.6，`AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:N/A:H`），
  因此这里不是两份独立评分。
- OSV 的 `versions` 列表只到 v3.7.5，漏了 v3.7.6/v3.7.7；实际 tag 与源码检查
  确认 3.7.7 仍含缺陷。处置：`affected_range` 取 CNA/CPE 的 `<3.8.0`，
  `vulnerable_version` 取 3.7.7，并在 limitations 说明版本列表缺口。
- 同一修复提交还改了 `copy_from_lzss_window` 第二个 memcpy 的目的地址
  （`buffer` → `buffer + firstpart`），这是同一行的写侧越界；CVE 描述只讲
  over-read，dossier 按 CVE 措辞但把两处改动都记录下来，未把写侧问题单独
  算成另一个 CVE。

## 21. Laravel CVE-2024-52301：GHSA 的 CVSS_V3 向量自相矛盾，六个分支边界一致但回移提交未逐个追溯

- 公告族在受影响范围上完全一致：CVE v5、NVD CPE、OSV/GHSA 与 FriendsOfPHP 都给出
  六段 `packagist/laravel/framework` 范围（`<6.20.45`、`7.0.0–7.30.7`、
  `8.0.0–8.83.28`、`9.0.0–9.52.17`、`10.0.0–10.48.23`、`11.0.0–11.31.0`），
  修复时间同为 2024-11-12。
- 但 GHSA/OSV 的 `severity` 条目里，CVSS_V3 写作
  `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:N`，三项影响全为 N，数值为 0.0；
  同一条记录的 `database_specific.severity` 却是 HIGH，CNA 的 CVSS 4.0 为 8.7，
  NVD 自己的 Primary CVSS 3.1 为 7.5。这是 GHSA 记录内部的数据缺陷，不是真实评分分歧；
  正式 severity 取 NVD Primary 7.5，0.0 向量只在 `source_crosscheck` 留档。
- 11.x 的源码修复是 `18b326d`（"only use argv on console"），absent from v11.30.0、
  ancestor of v11.31.0，只改 `Application.php`（+3/-1），**没有附带回归测试**。
  6.x–10.x 只验证了各 fixed tag 的内容都含同样的 `runningInConsole()` 守卫，
  没有逐个追溯分支回移提交的 SHA；dossier 的 `fixed_releases.verified_content`
  明确写了这一限制。
- Debian 11 通过 DLA-3997-1 把 6.20.14 回移到 `6.20.14+dfsg-2+deb11u2`；
  该版本号低于上游 6.20.45，不能当作上游修复边界，已单独记录。
- 漏洞机制依赖 `register_argc_argv=On` 且 SAPI 把 query string 暴露为
  `$_SERVER['argv']`；本轮未对具体 PHP SAPI/INI 组合做动态验证，也没有构造
  `?--env=` 请求。评级与可达性限制都保留在 dossier limitations 中。

## 22. curl CVE-2023-38545：OSV 的 GIT 区间端点是 release/补丁提交，MITRE CNA 的版本块描述空区间

- OSV 的 `ranges` 用 `introduced b8d1366852fd...`、`fixed 172e54cda184...`：
  `b8d13668` 是 `curl-7_69_0` 的 tag 提交（release 提交），不是引入提交；
  `172e54cd` 是 "tiny-curl: patch set applied on 8.4.0"，是 8.4.0 tag 之后的
  子提交，也不是源码修复。由该区间生成的 vanir 签名因此指向 `multi.c`、
  `cf-socket.c`、`select.c` 等无关文件。正确端点在 curl.se 公告 JSON 中：
  `4a4b63daaa01ef59b131d91e8e6e6dfe275c0f08`（引入）→
  `fb4415d8aee6c1045be932a34fe6107c2f5ed147`（修复）。
- OSV 还在 `affected.versions` 中列出 `curl-8_4_0`，并有一个
  `introduced 8.4.0 / last_affected 8.4.0` 的 unresolved 区间，与它自己的 GIT
  区间和公告直接矛盾。
- MITRE CNA（HackerOne）的 affected 块为
  `{version 8.4.0, status affected, lessThan 8.4.0}` 与
  `{version 7.69.0, status unaffected, lessThan 7.69.0}`，实际描述空区间，
  无法表达 `>=7.69.0,<8.4.0`；NVD 复制了该块，但其 CPE 配置
  （`haxx:libcurl` 7.69.0 ≤ v < 8.4.0）是正确的。处置：`affected_range`
  取 `>=7.69.0,<8.4.0`，并同时以 CPE 和公告版本列表为准。
- 评分与分类不一致：NVD Primary 为 CVSS 3.1 9.8 CRITICAL（`UI:N`），
  curl 公告、CISA-ADP 与 OSV 为 8.8 HIGH（`UI:R`）；CWE 分别为
  curl 的 CWE-122 与 NVD/CISA-ADP 的 CWE-787。正式 severity 取 NVD 9.8，
  两套 CWE 都保留，分歧写进 dossier 的 `source_crosscheck` 与 limitations。
- 披露时间差：curl.se 公告日期 2023-10-11，MITRE/NVD 发布 2023-10-18；
  属于发布滞后，不是两个漏洞。
- 独立 reviewer 首版 verdict 把 `vulnerable_commit` 填成了引入提交
  `4a4b63da`，与其自身 REVIEW 中的 tag peel 结果（`6fa1d817`）不一致。
  经指出后由 reviewer 自行更正为快照 SHA，采集方未改动 reviewer 产物；
  更正后的 verdict 九项字段仍全为 true。

## 23. Django CVE-2020-7471：NVD 下界低估暴露面、OSV 版本列表越界，且只引用未发布的 master 修复提交

- 代码级核实：`StringAgg` 由 `e4cf8c84`（2015-02-08，1.9 引入）加入，
  同样的 `'%(delimiter)s'` 模板存在于 tag 1.9、1.10.8、2.0、2.1.15。
  NVD 的 CPE 下界只写 `>=1.11` 与 `>=2.2`，因此低估了不受支持分支的暴露面。
  正式 `affected_range` 仍取上游公告/NVD 的支持分支边界
  （`>=1.11,<1.11.28`、`>=2.2,<2.2.10`、`>=3.0,<3.0.3`），代码级更宽的事实
  写入 limitations 与 source_crosscheck，不擅自改写权威范围。
- OSV 的 1.x `affected.versions` 列出 1.0.1–1.8.x，但这些版本还没有 `StringAgg`，
  对本漏洞不成立；`introduced: 0` 是保守超集，逐版本列表则是过宽。
- MITRE 与 NVD 只引用 master 提交 `eb31d845`，它不是任何已发布修复 tag 的祖先；
  真正随发行版发布的是 3.0.x `505826b4`、2.2.x `c67a368`、1.11.x `001b063`，
  只有 OSV 全部列出。dossier 保留四个提交并标注分支角色。
- 时间戳有误导性：修复提交作者日期（2019-12-31，1.11.x 为 2020-01-22）可早于
  3.0.2 tag，但 `505826b4` 不在 3.0.2 中，因为它在 tag 切出后才落到发布分支。
  判定只用 `merge-base --is-ancestor`，不用日期。
- MITRE CNA 记录是占位（vendor/product/version 全 n/a），无 CVSS、无 CWE；
  CWE-89 与 9.8 仅来自 NVD/GHSA。
- 复核期间 GitHub REST API 对共享出口 IP 限流（403 rate limit），改走
  `github.com` 的 `.patch` 端点与自建裸克隆；这是取证通道问题，不是证据冲突。
- 独立 reviewer 首版即与采集档案一致（位置 54-58 与 52-58 重叠，
  vulnerable_commit 同为 `a3697439`），无需更正 reviewer 产物。

## 24. Jenkins CVE-2024-23897：公告描述夸大未授权影响、版本表含 rc/伪版本、双线版本号交错，且公告在修复后修订

`jenkinsci/jenkins` 的 CVE-2024-23897（args4j `@` 文件展开，`CLICommand.getCmdLineParser`
未关闭 atSyntax）在提升过程中发现以下来源缺陷，全部记录而未静默取舍：

- MITRE 与 NVD 的描述称未授权攻击者可“读取任意文件”。Jenkins 官方 advisory 的实际
  边界是：未授权 CLI 命令只能读到文件前几行（当时三行），读完整文件需要 Overall/Read。
  dossier 的 limitation 文本取 advisory 口径，CVSS 仍取 NVD 9.8 并标注差异来源。
- OSV 的 `affected.versions` 混入 release candidate 与伪版本（如 `jenkins-2.426.3-rc`、
  `builds/341` 形态），同时漏掉 2.440.1；不能作为版本范围的来源。
- 周更线与 LTS 线版本号交错：修复的 LTS 2.426.3、2.440.1 数值上都小于受影响的周更
  2.441，而 2.427–2.441 仍受影响。扁平的 Maven 区间无法表达这个析取，两个正式区间
  取公告的线边界（`<2.442`、`<2.426.3`），dossier 明确写出过度近似的方向。
- 修复提交有三个而非两个：周更 `554f0378`、LTS 2.426 `a7486539`、LTS 2.440
  `3e876d4c`。`3e876d4c` 是 `554f0378` 的 cherry-pick，是 `jenkins-2.440.1`
  （`02f2a4cc`）的祖先；首版 dossier 只有前两个，由独立 reviewer 的 verdict 指出后
  补验并加入。
- 公告在 2.440.1 发布后修订：`jenkins-2.440.1` 的发布提交日期为 2024-02-21，
  晚于公告首发 2024-01-24；CNA 的 `dateUpdated` 为 2024-04-15。判定不使用公告页面
  的“首发即全量”假设。
- args4j 2.33 的默认值是 `atSyntax=true`，漏洞成立不依赖项目显式开启；这一点由
  修复方式（显式 `withAtSyntax(ALLOW_AT_SYNTAX)`，默认 false）反证，未执行任何 CLI。
- 独立 reviewer 首版即给出与采集档案相同的 `vulnerable_commit`（`3b0de10d`）和
  重叠位置（309-311），无需更正 reviewer 产物；第三修复提交与 2.440.1 由采集者
  独立复验后写入 dossier 的 evidence 12，reviewer 文件未改动。

## 25. Symfony CVE-2024-50345：NVD 与 CNA/GHSA 的 CVSS 分歧、OSV 版本枚举漏项、CVSS v4.0 只存在于聚合源

`symfony/symfony` 的 CVE-2024-50345（`Request::create` 不按 WHATWG 规则拒绝非法字符，
导致依赖它的跳转校验器可被绕成 open redirect）在提升过程中发现以下来源差异：

- CVSS 3.1 有两条实质不同的向量。NVD Primary 为 6.1 MEDIUM
  `AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`；GitHub_M CNA 记录与 GHSA 页面为
  3.1 LOW `AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N`。差异在 AC、S 与 I 三项。
  NVD 同时把 CNA 向量作为 Secondary 指标保留，所以两条向量都能在 NVD 记录中看到。
  正式 severity 取 NVD Primary 6.1，3.1 LOW 记入 dossier 与 reviewer 的分歧。
- GHSA 页面与 OSV 的 severity 数组还带一条 CVSS v4.0
  `AV:N/AC:L/AT:P/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N`（GHSA 显示 2.3 Low），
  CVE CNA 记录与 NVD 都没有。该向量不参与正式 severity。
- OSV 的三条 ECOSYSTEM 区间事件与公告一致（`0 → 5.4.46`、`6.0.0 → 6.4.14`、
  `7.0.0 → 7.1.7`），但 `affected.versions` 枚举漏掉了区间内已发布的 tag：独立 reviewer
  用 `git ls-remote` 确认 v5.4.41、v5.4.43、v6.4.1、v6.4.5、v6.4.6、v6.4.9、
  v6.4.11、v7.1.2、v7.1.4 都存在且不在列表中。按列表匹配的扫描器会低估受影响版本，
  dossier 只用区间事件，不用该列表。
- NVD 的 CPE 使用 vendor `sensiolabs:symfony`，CNA/GHSA/OSV 使用 Packagist
  `symfony/http-foundation`；本项目映射到 monorepo tag `v5.4.45`。
- 公告署名不一致：symfony.com 只写 Sam Mush，GHSA/OSV 写
  “Sam Mush - IPASSLab && ZGC Lab”。不影响技术字段。
- 修复提交的作者日期为 2024-10-22、committer 日期为 2024-10-29；版本边界只用
  `merge-base --is-ancestor`，不用日期。
- 独立 reviewer 独立选中同一文件同一行段（358-361），`vulnerable_commit` 与采集档案
  相同（`2b66d7d7`），九项 `fields_verified=true`，grade B；reviewer 文件未被改动。

## 26. Symfony CVE-2024-50340：相邻候选的 GHSA 别名张冠李戴、NVD 无 Primary 度量、CVSS v4 与 CWE/下界分歧

`symfony/symfony` 的 CVE-2024-50340（`SymfonyRuntime` 在非 CLI SAPI 上读取由
`register_argc_argv` 从查询串生成的 argv，可改 `APP_ENV`/`APP_DEBUG`）在提升过程中
发现以下来源缺陷：

- **别名张冠李戴**：首版 dossier 把 `GHSA-qq5c-677p-737q` 当成该 CVE 的 GitHub
  公告，实际它属于相邻的 CVE-2024-51736（symfony/process 在 Windows 的 cmd.exe
  劫持）。本 CVE 的真实公告是 `GHSA-x8vp-gf4q-mw5j`，由 CVE List v5 的 references、
  OSV、GitHub HTML 与 advisory-database raw JSON 四方确认。独立 reviewer 发现并
  指出后，dossier 已改正别名、公告页面与证据摘要；错误的旧页面不再作为证据。
- NVD 对 CVE-2024-50340 没有 `nvd@nist.gov` 的 Primary CVSS：唯一的
  `cvssMetricV31` 是 Secondary（source `security-advisories@github.com`），
  weaknesses 也是 Secondary，configurations 为 null，`vulnStatus=Deferred`。
  因此正式 7.3 HIGH 来自 CNA/GHSA，而不是 NVD 自己的分析。
- 严重性表示分歧：CNA/NVD 的 CVSS 3.1 为 7.3 HIGH，GHSA 页面主评级是 CVSS 4.0
  6.9 MODERATE（`AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L`），同页仍保留 3.1 向量。
- CWE 集合分歧：CNA 与 NVD 只有 CWE-74；GHSA/OSV 的 `database_specific.cwe_ids`
  为 `["CWE-20","CWE-74"]`。正式 `cwe_ids` 保留 CWE-74。
- 受影响下界分歧：CNA 字面写 `<5.4.46`，GHSA/OSV/FriendsOfPHP 写 `>=5.3.0`
  （symfony/runtime 自 5.3 引入）。正式 5.4 范围取 `>=5.3,<5.4.46`；6.x/7.x
  仍为 `>=6.0,<6.4.14` 与 `>=7.0,<7.1.7`。
- OSV 的 GIT `fixed` 端点是发行提交 `057d88be`/`d1797e5b`/`50011435`，源修复
  `a77b308c` 只作为末尾追加的 `REFERENCES_COMMIT` fixed 事件；dossier 以源修复
  为 fix commit，不用发行提交。
- CVE 描述有两处笔误：写成 `register_argv_argc`（应为 `register_argc_argv`）与
  “non-SAPI PHP runtimes”（应为 non-CLI SAPIs）。
- 独立 reviewer 独立选中同一文件 98-101 行，`vulnerable_commit` 与采集档案相同
  （`2b66d7d7`），九项 `fields_verified=true`，grade B；reviewer 文件未被改动。
- 修订遗漏：首版改正了 `aliases`、公告 URL 与证据摘要，但 `vulnerability.references`
  仍保留了错误的 `GHSA-qq5c-677p-737q` 链接，并因此被复制进已提升的
  `data/vulnerabilities.jsonl`。本次把 dossier.references 改为
  `GHSA-x8vp-gf4q-mw5j`，随后重跑提升与报表以重建正式表。

## 27. Symfony CVE-2024-50342：公告修订后 CNA/NVD/OSV 仍停在旧修复版本，两段补丁缺一不可

`symfony/symfony` 的 CVE-2024-50342（`NoPrivateNetworkHttpClient` 只检查
`$info['primary_ip']`、不解析主机名，导致解析到私有网段的域名未被拦截，公告称为
内部 IP/端口枚举）在提升过程中发现以下来源与修复信息问题：

- **公告修订与数据库滞后**：Symfony 公告 `article:modified_time` 为
  `2024-11-13T15:04:41+01:00`，正文明确写“Update: Versions 5.4.46, 6.4.14, and 7.1.7
  are still affected and new releases have been published: 5.4.47, 6.4.15, and 7.1.8”，
  受影响区间为 `<5.4.47`、`>=6,<6.4.15`、`>=7,<7.1.8`。GHSA-9c3x-r3wp-mgxm 页面与
  OSV 的 GHSA 记录同步更新为 5.4.47/6.4.15/7.1.8。但 CVE List v5 CNA 记录
  （`dateUpdated 2024-11-07T15:26:33Z`）、NVD 描述（`lastModified 2026-06-17`）与
  OSV 由 cvelistV5 生成的 CVE 记录仍写 `<5.4.46`、`<6.4.14`、`<7.1.7`；本次提升
  采用修订后的公告区间，并以 git 祖先关系确认。
- **两段补丁缺一不可**：第一段 `296d4b34`（父 `706d8628`）由安全合并 `3fc5471c` 进入
  5.4，随 5.4.46/6.4.14/7.1.7 发布；它只把 URL host 交给
  `IpUtils::checkIp($host, ...)`，而 `IpUtils::checkIp` 只比较 IP 字面量
  （5.4 的 `IpUtils.php:37-58` 分派到 `checkIp4/checkIp6`），域名不会被拦截。
  第二段 `b4bf5afd`（父 `2c7c4bac`）由安全合并 `b8f41169` 进入 5.4，通过
  `on_progress` 新增的可选 `$resolve` 闭包或 `dns_get_record(DNS_A/DNS_AAAA)`
  解析主机，并在连接前检查解析出的 IP，随 5.4.47/6.4.15/7.1.8 发布。祖先矩阵：
  `296d4b34` 在 5.4.46/6.4.14/7.1.7 中，`b4bf5afd` 只在 5.4.47/6.4.15/7.1.8 中；
  v5.4.45 的文件 blob `757a9e8a` 等于第一段父提交的 blob，v5.4.46 的
  `c252fce8` 等于第二段父提交的 blob。
- **CNA/NVD 引用不完整**：CNA 与 NVD 的 references 只列第一段补丁 `296d4b34`，
  没有第二段 `b4bf5afd`；只有 GHSA、OSV 的 GHSA 记录、Symfony 公告与
  FriendsOfPHP YAML 同时给出两段补丁。按 CNA/NVD 的单一 fix commit 复现修复会
  得到仍可绕过的版本。
- **严重性双口径**：NVD Primary CVSS 3.1 为
  `AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N` = 4.3 MEDIUM；CNA/GHSA 为
  `AV:N/AC:H/...` = 3.1 LOW。正式 severity 取 NVD Primary 4.3，CNA/GHSA 的
  3.1 记入 dossier limitations。
- **CWE 展示不一致**：CNA `problemTypes`、NVD weaknesses（Secondary）与 OSV
  `database_specific` 均为 CWE-200，但 GitHub GHSA 网页的 Weaknesses 区显示
  “No CWEs”。正式 `cwe_ids` 取数据层的 CWE-200。
- **credits 不一致**：Symfony 公告只感谢 Linus Karlsson；GHSA 正文写
  Linus Karlsson 与 Chris Smith；独立 reviewer 另记录 GHSA 页面列出 reporter
  `zozs`/`cs278` 与 remediation developer `nicolas-grekas`。不影响技术字段。
- **语言统计口径**：独立 reviewer 在“src/ 下、排除 Tests/Intl/Resources/Contracts/
  Translation/Bridge/”的过滤口径下精确复现 3327 个 first-party PHP 文件，
  字节数 11,755,821 与快照的 11,758,368 相差 2,547（0.02%）；25.45% 是快照定义的
  “全部非二进制 tracked 字节”占比，PHP 占全部 tracked 字节的 87.45%。快照口径
  已在 `snapshot_proposal.json` 注明，正式语言字段仍用快照统计。
- **独立复核**：`independent-reviewer-symfony-CVE-2024-50342-deepseek-flash`
  在隔离上下文自行抓取公告、CNA、NVD、OSV、GHSA 与上游 git 历史，确认
  `v5.4.45` 的 82-89 行只检查 `primary_ip`、两段补丁 SHA/父提交/祖先关系无误、
  真实 fixed releases 为 5.4.47/6.4.15/7.1.8，九项 `fields_verified=true`，grade B；
  其 location 取 72-89 行，与 dossier 的 82-85 行重叠。

## 28. Django CVE-2020-9402：四条分支补丁、1.11 修复形态不同与来源引用缺口

`django/django` 的 CVE-2020-9402（Oracle 上 GIS 函数/聚合的 tolerance 参数被格式化
进 SQL 模板，CWE-89）在提升过程中确认以下来源与修复信息问题：

- **发布时间与公告**：Django 公告日期为 2020-03-04，修复发行版为 3.0.4、2.2.11、
  1.11.29；CVE 记录 datePublished 为 2020-03-05T14:49:57Z，NVD 为
  2020-03-05T15:15:12Z，GHSA/OSV 记录到 2020-06-05 才发布。正式 `published_at`
  取 CVE 记录，公告日期早一天记入 dossier limitations。
- **四条分支补丁**：公告列出 master `6695d29b`、3.0 `26a5cf83`、2.2 `fe886a3b`、
  1.11 `02d97f3c`。OSV 只列 master `6695d29b`；NVD 与 CVE v5 的 references 没有
  列任何 fix commit。master 补丁不是 3.0.4/2.2.11/1.11.29 任一发行 tag 的祖先，
  属正常回移；只有 `26a5cf83` 是 3.0.4 的祖先，且在 3.0.2/3.0.3 中不存在。
- **Blob 对应**：3.0.2、3.0.3 与 3.0.x 补丁父提交 `c5cfaad2` 的
  `functions.py` blob 均为 `a79067a4`，`aggregates.py` 均为 `993d9f91`；
  3.0.4 对应修复后 blob `1b0a2a42`、`9d169275`。脆弱提交 `a3697439`
  因此与补丁父提交内容完全一致。
- **1.11 修复形态不同**：2.2.11/3.0.4 将 tolerance 包成 `Value(...)` 作为
  source expression（绑定参数）；1.11.29 的 `functions.py` 仍用
  `"%%(function)s(%%(expressions)s, %s)" % tol`，但先经
  `_handle_param(..., NUMERIC_TYPES)`，非数值类型直接抛 `TypeError`。
  两代修复都阻断字符串注入，机制不同，dossier 分开记录。
- **严重性口径**：NVD Primary CVSS 3.1 为
  `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` = 8.8 HIGH；NVD 遗留 CVSS 2.0
  为 6.5 MEDIUM；GHSA 另有 CVSS 4.0 8.7。正式 severity 取 8.8。
- **CNA 占位**：MITRE CVE v5 的 affected 为 vendor/product/version 全 n/a，
  `problemTypes` 为 n/a，无 CVSS；CWE-89 来自 NVD 与 GHSA。
- **重复 PYSEC 记录**：OSV 同时有 PYSEC-2020-36 与 PYSEC-2020-345，二者区间一致，
  后者把前者列为 alias；正式 aliases 保留 PYSEC-2020-36，dossier 记录重复。
- **release note 笔误**：1.11.29 的 release note 写 “fixes a security issue in
  1.11.29”，按语义应为 1.11.28；不影响修复边界。
- **语言字段复核流程**：独立 reviewer 首轮因本机没有可用的 github-linguist 而把
  `languages` 记为 false。复核任务说明后，reviewer 在允许范围读取
  `runs/language/snap_ab695ba3db678939/`，确认 `full_scan=true`、
  github-linguist 9.7.0、6163 个 tracked files、`NEEDS_REVIEW`（67 个 ambiguous
  文件等），并与自有克隆的 2578 个 `.py` 交叉核对后改为 true。该字段验证的是
  快照盘点状态，不要求 reviewer 本地重跑 Linguist。另：复核提示词写“九项”，
  但把 identity 与 aliases 分列成十个键；正式复核仍按九项字段推导五项布尔值。
- **独立复核**：`independent-reviewer-django-CVE-2020-9402-deepseek-flash`
  在隔离上下文自行抓取公告、CVE v5、NVD、OSV/GHSA、GitHub advisory API 与上游
  git 历史，独立选中 `functions.py` 的 `OracleToleranceMixin.as_oracle`
  113-119 行（次路径 `aggregates.py` 29-32 行），确认四条补丁的祖先关系与
  3.0.4/2.2.11/1.11.29 的修复内容，九项 `fields_verified=true`，grade B。

## 29. Django CVE-2020-13596：NVD 西语描述串到相邻 CVE、GHSA CVSS 4.0 自相矛盾、2.2 修复提交前缀误写 `[2.0.x]`

- **来源一致性**：Django 2020-06-03 公告、NVD 英文描述、MITRE CVE v5、OSV
  GHSA-2m34-jcjv-45xf、GitHub advisory 页与修复提交都指向 admin
  `ForeignKeyRawIdWidget` 查询参数未 URL 编码导致的 XSS（CWE-79）。
  区间为 2.2 <2.2.13、3.0 <3.0.7，修复发行版 3.0.7/2.2.13。
- **NVD 西语描述错误**：`nvd_cve.json` 的 `es` 描述写的是 memcached 键校验/
  键碰撞导致数据泄露，即同批公告里的 CVE-2020-13254；英文描述正确。dossier
  只采用英文描述，并把该翻译错误记入 limitations。
- **GHSA CVSS 4.0 不可用**：OSV 同时给出 CVSS 3.1
  `AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`（6.1）与 CVSS 4.0
  `AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N`；后者
  VC/VI/VA 全为 N，按规范基础分为 0.0，与 6.1 直接冲突。正式 severity 取
  NVD Primary 6.1 MEDIUM，GHSA 的 MODERATE 标签一致。
- **3.1a1 不在区间内但确有漏洞**：NVD、GHSA/OSV 与 PYSEC 的版本枚举都没有
  3.1a1，但该预发布版（2020-05-14）的 widgets.py blob `1ec7c70a` 仍含
  `'&amp;'.join(...)` + `mark_safe`；3.1b1（2020-06-15）blob `59d1004d`
  已修复，说明 3.1 修复 `49d7cc19` 在 b1 前落地，no later 3.1 prerelease
  受影响。公告确实把 3.1 列为受影响分支。
- **introduced 下界只是受支持分支界定**：直接检查 EOL tag 1.11.29、2.0.13、
  2.1.15，均含同一不安全构造且未修复；`>=2.2` / `>=3.0` 不是代码引入点。
  复核期间一次全历史 `git log -S` 把引入定位到 `a19ed8aea39`
  （"Merged the newforms-admin branch into trunk."），但为保持已推广 verdict
  不变，该补充只记录在本条，不回写 `verdict.json`。
- **四条分支补丁与祖先关系**：公告列 master `2dd4d110`、3.1 `49d7cc19`、
  3.0 `1f2dd37f`、2.2 `6d61860b`；分别只在对应分支。`1f2dd37f` 不在
  3.0.2/3.0.6 中、是 3.0.7 的祖先；`6d61860b` 不在 2.2.12 中、是 2.2.13
  的祖先。GHSA/OSV references 只列 3.0 与 2.2 两个提交，漏掉 master 与 3.1。
- **2.2 提交主题误写 `[2.0.x]`**：`6d61860b` 的主题为
  `[2.0.x] Fixed CVE-2020-13596 ...`，但公告把它归到 2.2 分支，且 git
  ancestry 确认它是 2.2.13 的祖先。分支归属以 tag 祖先关系为准，主题原样记录。
- **Blob 对应**：3.0.2、3.0.6 与 3.0.x 补丁父提交 `256d2971` 的 widgets.py
  blob 均为 `7db57f40`；3.0.7 为 `816f848f`。2.2.12 与补丁父 `7e1084ea`
  为 `aa4b6138`，2.2.13 为 `a56baee4`。脆弱快照与补丁父内容完全一致。
- **修复与测试**：改用 `django.utils.http.urlencode(params)` 并移除
  `mark_safe`；新增 `UnsafeLimitChoicesTo(limit_choices_to={'name': '"&><escapeme'})`
  与 `test_render_unsafe_limit_choices_to`，期望
  `name=%22%26%3E%3Cescapeme`。测试只读未执行。
- **NVD HTML 403**：NVD 详情页对非浏览器 UA 返回 403，复核改用官方 CVE
  API 2.0 记录作为主源。
- **独立复核**：`independent-reviewer-django-CVE-2020-13596-deepseek-flash`
  在隔离上下文自行抓取公告、CVE v5、NVD、OSV/GHSA 与上游 git 历史，独立选中
  `widgets.py:151-154`（次路径 `ManyToManyRawIdWidget` 200-215），确认四条
  补丁与 3.0.7/2.2.13 的内容，九项 `fields_verified=true`，grade B。

## 30. Django CVE-2020-13254：CWE-295 语义错配、OSV git ranges 指向无关提交、修复在 3.0.7 仍有绕过路径

- **来源一致性**：Django 2020-06-03 公告、NVD、MITRE CVE v5、OSV
  GHSA-wpjr-j57x-wxfw、GitHub advisory 页与修复提交都指向 memcached 后端
  缺少 cache key 校验，畸形 key 造成键碰撞与潜在数据泄露。区间为
  2.2 <2.2.13、3.0 <3.0.7，修复发行版 3.0.7/2.2.13。
- **CWE 语义错配**：NVD 与 GHSA 都把 CWE-295（Improper Certificate Validation）
  列为 CWE，与 cache-key 校验/键碰撞无关；MITRE CNA 的 problemTypes 为 n/a。
  正式值保留来源给出的 CWE-295，未擅自替换为 CWE-20，dossier 记入 limitations。
- **定性标签与数值矛盾**：GHSA 顶层 severity 为 `high`，但其自身 CVSS 3.1
  为 5.9、NVD Primary 也是 5.9 MEDIUM；`high` 来自 2024 年追加的 CVSS 4.0
  向量 8.2（`CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N`）。
  正式 severity 取 NVD Primary 5.9 MEDIUM
  （`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`），另记 NVD legacy
  CVSS 2.0 4.3。
- **OSV GIT ranges 不可用**：OSV 的 `introduced` 事件指向无关的文档提交
  （`2a62cdcf…`，2022-04-11 把 CVE-2022-28346/28347 加入 security archive；
  `2a04e24d…`，2021-04-06 把 CVE-2021-28658 加入 security archive），
  `fixed` 事件指向 2.2.13/3.0.7 的版本 bump 提交（`8093aaa8…`、`44da7ab…`）
  而非 vendor patch。属 CPE 区间转换缺陷；核验改用公告列出的 changeset
  加 git ancestry。
- **四条分支补丁与祖先关系**：公告列 master `2c824149`、3.1 `580bd64c`、
  3.0 `84b2da55`、2.2 `07e59caa`。`84b2da55` 是 3.0.7 发布提交的父、
  `07e59caa` 是 2.2.13 发布提交的父；`580bd64c` 首见 tag 3.1b1、
  `2c824149` 首见 tag 3.2a1（均非稳定发行版，不计入 fixed_releases）。
- **补丁链**：四个补丁分别以同类 CVE-2020-13596 的四个补丁为父
  （`2dd4d110`、`49d7cc19`、`1f2dd37f`、`6d61860b`）；author date 均为
  2020-05-20，committer date 均为 2020-06-03（发布准备日）。
- **修复内容与自身缺陷**：修复新增 `InvalidCacheKey` 与
  `memcache_key_warnings`，把 base 的 `validate_key` 改为从生成器发警告，
  `BaseMemcachedCache.validate_key` 在首个警告处抛异常；memcached 的
  add/get/set/delete/get_many/incr/decr/set_many 在 `make_key()` 后调用
  `validate_key()`。`delete_many` 仍未校验；`memcache_key_warnings` 在长度
  分支 yield 裸字符串、在字符分支 yield `(message, CacheKeyWarning)` 元组，
  异常仍会抛出但参数不是纯字符串。
- **修复完整性静态观察**：3.0.7 中 `MemcachedCache.get`（178-186）与
  `MemcachedCache.touch`（174-176）覆写仍未调用 `validate_key()`，
  python-memcached 的 get/touch 路径在修复版仍绕过检查。该行为不在
  vendor patch 内，仅静态观察，未据此重开 CVE。
- **位置锚点分歧与协调**：采集 dossier 锚定写路径 `BaseMemcachedCache.set`
  73-77；独立 reviewer 在隔离上下文独立锚定读路径
  `BaseMemcachedCache.get` 69-71，并在 REVIEW.md 中另行列出 set 73-77 为
  同样缺失校验的调用点。两者位于同一连续区间，dossier 据此把
  `critical_operation.line` 协调为 69-77，并新增 `location_revision` 记录
  原始值、reviewer 锚点与协调原因；证据、严重度、版本范围、提交与 reviewer
  值均未改动。这是本数据集第一次出现 reviewer 与采集者选中不同（但相邻且
  同类）调用点，协调规则留待后续固化。
- **3.1a1 边界**：与 13596 不同，本 CVE 的 3.1 修复在 3.1b1 前落地；
  3.1a1 是否含漏洞未在本次核验中单独取 blob，未写入正式区间。
- **独立复核**：`independent-reviewer-django-CVE-2020-13254-deepseek-flash`
  在隔离上下文自行抓取公告、CVE v5、NVD、OSV/GHSA、GitHub advisory API
  与上游 git 历史，九项 `fields_verified=true`，grade B；`docs/releases/`
  的 per-release notes 用于修复内容核验，`security.txt` 在 3.0.7 未含该 CVE 行。
- **语言字段**：GitHub REST 元数据被限流（403），reviewer 依据允许的
  Linguist 快照工件（Python 约 13.47 MB 居首）与本地树确认主语言；
  快照状态维持 `NEEDS_REVIEW`。

## 31. Django CVE-2020-24583：CWE-276 非 CNA 给出、CVSS 三版本不一致、backport 引用的 master 提交不可达

- **来源一致性**：Django 2020-09-01 公告、NVD、OSV/GHSA、GitHub advisory
  与 release notes 都指向 Python 3.7+ 下
  `FileSystemStorage._save` 只用 `os.makedirs(..., mode)` 而不控制 umask，
  导致中间目录按 `0o777 & ~umask` 创建；区间为 2.2 <2.2.16、3.0 <3.0.10、
  3.1 <3.1.1，修复发行版 2.2.16/3.0.10/3.1.1。
- **MITRE CNA 为占位**：vendor/product/version 与 problemType 均为 `n/a`，
  CWE-276 与 CPE 区间都由 NVD 提供，OSV/GHSA 与之一致。
- **CVSS 三版本不一致**：NVD Primary CVSS 3.1 = 7.5 HIGH
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`），NVD legacy CVSS 2.0 = 5.0，
  GitHub advisory 的 CVSS 4.0 overall = 8.7 HIGH。正式 severity 取 NVD
  Primary 3.1，其余作为 legacy/alternate 记录。
- **区间粒度差异**：PYSEC 的 introduced 为 2.2/3.0/3.1，GHSA 用
  2.2a1/3.0a1/3.1a1 并列出预发布版本，NVD CPE 用 2.2/3.0/3.1；区间本身一致。
- **Python 运行时前提未编码**：所有来源都注明“when Python 3.7+ is used”，
  但版本区间只能表达 Django 版本，无法表达 Python 运行时条件；
  本数据集不在 affected_range 中虚构运行时约束，改为在 dossier 记录。
- **master 修复提交引用不一致**：公告列 master changeset `8d727157`，
  但三个分支 backport 的提交消息均写
  “Backport of `ea0febbba531a3ecc8c77b570efbfb68ca7155db` from master”；
  该对象在公开仓库不可达（`not our ref`，完整克隆亦无）。核验以公告列出且
  可达的 `8d727157` 为准，它首见 tag 3.2a1；`ea0febbba` 与 `8d727157`
  的内容等价性无法验证，记为 gap。
- **Blob 对应**：3.0.2 与 3.0.9 的 storage.py 同为 `4c27fce605`，也等于
  3.0.x 修复父 `08892bff` 的 blob；3.0.10 为 `af70b3fa`。2.2.15 为
  `9a7d8793`、2.2.16 为 `1562614e`；3.1 为 `e9166d94`、3.1.1 为
  `16f9d4e2`。修复只改 `old_umask = os.umask(0)` 一行及注释。
- **修复与测试**：新行 `os.umask(0o777 & ~self.directory_permissions_mode)`；
  上传测试改用 `the_directory/subdir/the_file` 并断言父/祖父目录均为 `0o765`；
  staticfiles 测试新增嵌套 css 文件，覆盖 collectstatic 路径。测试只读未执行。
- **未修复路径（reviewer 观察）**：`collectstatic --link` 走
  `link_file` 的直接 `os.makedirs()`，不经过 `FileSystemStorage._save`；
  静态判断本次修复只覆盖 copy 路径，symlink 路径不在 CVE 范围内，未重开。
- **独立复核**：`independent-reviewer-django-CVE-2020-24583-deepseek-flash`
  在隔离上下文自行克隆并抓取公告、CVE v5、NVD、OSV/GHSA、GitHub advisory
  与 release notes，独立选中 `storage.py:239-246`（采集档案 240-246，重叠），
  确认四个 changeset 的分支归属与三个 fixed tag 的 blob，十项
  `fields_verified=true`，grade B。

## 32. Django CVE-2020-24584：与 24583 同批补丁链、CVSS 4.0 与 3.1 损害维度不一致、master 原提交同样不可达

- **来源一致性**：Django 2020-09-01 公告、NVD、OSV/GHSA、GitHub advisory
  与 release notes 都指向 `FileBasedCache._createdir` 未控制 umask，
  Python 3.7+ 下缓存中间目录按系统 umask（通常 `0o755`）创建而非 `0o700`；
  区间为 2.2 <2.2.16、3.0 <3.0.10、3.1 <3.1.1。
- **CWE 与 CNA**：CWE-276 由 NVD/GHSA/OSV 给出，MITRE CNA 仍为占位
  （vendor/product/version 与 problemType 均 n/a）。
- **CVSS 版本差异**：NVD Primary CVSS 3.1 = 7.5 HIGH
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`），NVD legacy v2 = 5.0；
  OSV/GitHub 另给 CVSS 4.0 = 6.9，向量为
  `AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N`。
  v4 把影响归为完整性 Low、机密性 None，与 v3.1 的机密性 High 方向不同。
  正式 severity 取 NVD Primary 3.1，差异只记录不替换。
- **补丁链**：四个 24584 补丁依次以对应分支的 24583 补丁为父——
  master `1853724a` 父 `8d727157`、3.1 `2b099caa` 父 `934430d2`、
  3.0 `cdb367c9` 父 `08892bff`、2.2 `a3aebfdc` 父 `375657a7`；
  author date 均为 2020-08-21，committer date 为 2020-08-25/09-01。
- **master 原提交不可达**：三个 backport 消息引用
  `f56b57976133129b0b351a38bba4ac882badabf0`，与 24583 的 `ea0febbba`
  一样在公开仓库不可达（`not our ref`）；公告列出的可达 master 提交为
  `1853724a`，首见 tag 3.2a1。两者内容等价性无法验证。
- **Blob 对应**：3.0.2 与 3.0.9 的 filebased.py 同为 `48b8df90`，也等于
  3.0.x 修复父 `08892bff` 的 blob；3.0.10 为 `64cc175b`。2.2.15 为
  `ca8b0065`、2.2.16 为 `012b54e8`；3.1 为 `3d76f037`、3.1.1 为
  `10779c55`。
- **修复与测试**：`_createdir` 在 `os.makedirs(self._dir, 0o700,
  exist_ok=True)` 外包 `os.umask(0o077)` / `finally` 还原；回归测试创建
  `dirname/nested/filebasedcache`，断言叶子、父、祖父目录均为 `0o700`，
  并在 win32 跳过（Windows 只部分支持 umask/chmod）。测试只读未执行。
- **独立复核**：`independent-reviewer-django-CVE-2020-24584-deepseek-flash`
  在隔离上下文自行克隆并抓取公告、CVE v5、NVD、OSV/GHSA、GitHub advisory
  与 release notes，独立选中 `filebased.py:115-116`（与采集档案一致），
  确认四条补丁的祖先关系与三个 fixed tag 的内容，十项
  `fields_verified=true`，grade B；语言字段以 Python 约占编程语言字节
  92.27% 佐证。

## 33. Django CVE-2021-3281：archive.extract 双路径穿越、2021 修复本身不完整（2025 年以 CVE-2025-59682 再修）、OSV GIT 区间仍为文档提交

- **来源一致性**：Django 2021-02-01 公告、NVD、OSV/GHSA、GitHub advisory
  与 3.0.12 release notes 都指向 `django.utils.archive.extract`
  （`startapp --template` / `startproject --template`）用绝对路径或含点段
  的成员名穿越；区间为 2.2 <2.2.18、3.0 <3.0.12、3.1 <3.1.6，3.0.2 在区间内。
- **CWE 与 CNA**：NVD/GHSA/OSV 给 CWE-22；MITRE CNA 仍为占位
  （vendor/product/version 与 problemType 均 n/a，无 CVSS）。
- **CVSS 标签不一致**：NVD Primary CVSS 3.1 = 5.3 MEDIUM
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`），NVD legacy v2 = 5.0；
  GitHub 用同一 v3 向量标 Moderate，另给 CVSS 4.0
  `AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N`（维度一致）。
  但 Django 公告与 3.0.12/2.2.18/3.1.6 release notes 均称 severity “low”，
  与 NVD/GHSA 的数值分级不一致，只记录不替换。
- **3.2 预发布分支**：公告把 Django 3.2（alpha）列为受影响并给 3.2 分支
  changeset `f944f79e`；该提交是 tag 3.2 的祖先，3.2 正式版发布时已含
  `target_filename`，因此没有 3.2.x 受影响发行版，fixed_releases 不列 3.2。
- **五个 changeset 与祖先关系**：master `05413afa`（不是 tag 3.2 的祖先）、
  3.2 `f944f79e`（tag 3.2 祖先）、3.1 `02e65928`（3.1.6 祖先，3.1.5 之前
  不存在）、3.0 `52e409ed`（3.0.12 祖先，3.0.11 不含）、2.2 `21e7622d`
  （2.2.18 祖先）。五者 author date 均为 2021-01-22 12:23:18 +0100，
  committer date 为 2021-02-01 09:07–09:14 +0100。
- **OSV GIT 区间**：CVE 与 GHSA 记录的 introduced 事件仍是文档/安全档案提交
  （`2a62cdcf`、`2a04e24d`、`0b8a0296`），fixed 事件是 release 提交
  （`fc0c8cfa`、`81c99e4e`、`3235a7b8`），不是补丁提交；修复核验改用公告
  changeset 与 tag 祖先关系。
- **Blob 对应**：3.0.2/3.0.11/3.1 的 archive.py 同为 `235809f2`；
  3.0.12/3.1.6/3.2 为 `d5a0cf04`；2.2.17 为 `5b9998f8`，2.2.18 为
  `f2f153a1`。3.0.2 的 `TarArchive.extract` 与 `ZipArchive.extract`
  分别在 158、201 行直接 `os.path.join(to_path, name)`，文件内没有
  `target_filename`。
- **修复与测试**：新增 `BaseArchive.target_filename()`，对两侧做
  `os.path.abspath` 后以 `startswith` 判定并在越界时抛
  `SuspiciousOperation`；Tar/Zip 两个 extract 改走该函数。Zip 路径另加
  `if not name: continue`，并把目录判定从 `filename.endswith` 改为
  `name.endswith`。测试新增 `TestArchiveInvalid`：`traversal.tar`（`..`）、
  `traversal_absolute.tar`（`/tmp/evil.py`），win32 额外覆盖盘符 archive。
  测试只读未执行。
- **修复不完整（关键）**：`startswith` 没有路径分隔符边界，目标
  `/tmp/dest` 与兄弟目录 `/tmp/dest_evil` 前缀相同，仍可通过。Django 在
  2025-10-01 以 CVE-2025-59682 再修，提交
  `924a0c092e65fa2d0953fd1855d2dc8786d94de2`（Follow up to `05413afa`）
  改用 `os.path.commonpath`，并新增 `base + "abc"` 的回归测试；
  修复发行版为 4.2.25/5.1.13/5.2.7。该缺陷位于 2021 修复后的代码，
  不在 3.0.2 快照中，因此不改变本条的受影响判定与 grade。
- **位置锚定**：采集档案取 `archive.py:154-158`（Tar extract 循环到
  `os.path.join`，含 Zip 201 行于 trace）；独立 reviewer 独立选中
  `TarArchive.extract` 158 行，并把 `ZipArchive.extract` 201 行列为
  secondary，行号重叠，无需位置修订。
- **独立复核**：`independent-reviewer-django-CVE-2021-3281-deepseek-flash`
  在隔离上下文自行克隆并抓取公告、CVE v5、NVD、OSV/GHSA、GitHub advisory
  与 release notes，确认五个 changeset 的祖先关系、三个 fixed tag 的 blob
  与 2025 年再修提交，十项 `fields_verified=true`，grade B。

## 34. CVE-2021-28658 — Django 上传文件名目录穿越（django 3.0.2）

- **来源一致性**：Django 2021-04-06 安全公告（安全发行 3.0.14 / 2.2.20 / 3.1.8）
  与 GHSA-xgxc-v2qg-chmh、PYSEC-2021-6、OSV CVE 记录、CVE v5 记录一致。
  NVD 主指标 CVSS 3.1 5.3 MEDIUM
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`），CWE-22；另有 CVSS 2.0 5.0。
  GitHub 以 CVSS v4 给 6.9 Moderate，vendor 公告文字仍标 "low"，三者
  指向同一"仅机密性"影响，数值差异只记录不替换。
- **CWE 来源**：MITRE CNA 记录是占位（problemTypes 为 n/a，
  vendor/product/version 全为 n/a，metrics 为 null），CWE-22 来自 NVD
  Primary 与 GitHub advisory 页面，并非 CNA 断言。
- **OSV GIT 区间不可用**：introduced 事件是无关提交——
  `2a04e24d` 为 3.0.x 安全档案补记（在修复之后提交）、`2a62cdcf` 为 2022 年
  2.2.x 安全档案补记、`0b8a0296` 为 2021-12 的 re_path() 文档改动，均非
  3.0.2 祖先；fixed 事件恰好等于 2.2.20 / 3.0.14 / 3.1.8 的 tag peel 提交。
  受影响区间改由 NVD CPE 与 GHSA/PYSEC 生态区间交叉确认，二者一致。
- **五个 changeset 与祖先关系**：master `d4d800ca`、3.2 `2820fd1b`、
  3.1 `cca0d981`（3.1.8 祖先）、3.0 `e7fba622`（3.0.14 祖先）、
  2.2 `4036d62b`（2.2.20 祖先）。master 与 3.2 backport 均不是三个 release
  tag 的祖先（发布分支各自 cherry-pick）。
- **Blob 对应**：3.0.2 与 3.0.13 的 `multipartparser.py` 同为 `fd8fce8b`；
  3.0.14 为 `db1b5ce8`、2.2.20 为 `5a9cca89`、3.1.8 为 `2351055e`，
  均含 `sanitize_file_name`。2.2.19 与 3.1.7 仍为脆弱版本。
- **根因与修复**：3.0.2 的 `IE_sanitize` 只做
  `filename[filename.rfind("\\") + 1:].strip()`，只识别 Windows 反斜杠；
  `parse`（209-212）把 `html.unescape` 后的 `filename*` 值直接传入
  （230 行交给 `handler.new_file`），因此 `/`、`../` 与 HTML 实体编码的
  分隔符都能存活。修复改名 `sanitize_file_name`：反转义、按 `\` 截断后
  再用 `os.path.basename` 去掉 POSIX 路径分量。这是基于路径的清洗，
  不是名称白名单。
- **测试**：3.0.x/2.2.x 测试 diff 覆盖 view 回显 `hax0rd.txt` 与
  `filename*=utf-8''%2Fhax0rd.txt` 两类请求，断言 handler 收到的是
  basename；测试只读未执行。
- **位置锚定**：采集档案取 `multipartparser.py:300-302`
  （`IE_sanitize`），trace 含 `parse` 209-212 与 `new_file` 230；
  独立 reviewer 独立选中同一 `300-302`，并把 209-212 列为 secondary。
- **独立复核**：`independent-reviewer-django-CVE-2021-28658-deepseek-flash`
  在隔离上下文自行克隆仓库、抓取公告/CVE/NVD/OSV/release notes，确认五个
  changeset、三个 fixed tag 的 blob、OSV GIT 边界异常与 CNA 占位，
  十项 `fields_verified=true`，grade B；`BIT-django-2021-28658` 仅由 OSV
  交叉引用佐证，无 Bitnami 一手公告。

## 35. CVE-2022-25236 — libexpat 命名空间 URI 分隔符注入（libexpat R_2_4_4）

- **来源一致性**：NVD 主指标 CVSS 3.1 9.8 CRITICAL
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`），CWE-668；oss-security 2022-02-19
  转载的 2.4.5 `Changes` 条目 #561 明确写了"把畸形的 2-/3 字节 UTF-8 之外的
  命名空间分隔符放进 URI"、可导致"任意破坏（例如代码执行）"并有已知利用。
  MITRE CNA 记录是占位（affected 全 n/a、problemTypes 为 n/a、无 metrics）。
- **OSV 缺陷**：OSV 的 fixed GIT 事件是 `97a48405`（2.4.5 的发布准备合并，
  PR #564），不是代码修复 `a2fe525e`；CWE/CVSS 只在 NVD 与 CISA-ADP 容器中。
- **修复与祖先关系**：代码修复 `a2fe525e660badd64b6c557c2b1ec26ddc07f6e4`
  （"Prevent namespace separator in URIs"），配套回归测试 `2de07742`、
  `Changes` 提交 `e4d7e497`、PR #561 合并 `2cc97e87`。四个提交都用
  `git merge-base --is-ancestor` 确认在 `R_2_4_5` 内、不在 `R_2_4_4` 内；
  `R_2_4_5^{}` 为 `97a48405`，`R_2_4_4^{}` 为 `81b89678`。
- **根因**：`expat/lib/xmlparse.c` 的 `addBinding` 在 3752-3759 只把 URI 与
  内建 XML/xmlns 命名空间比较，不检查 URI 内是否含有
  `m_namespaceSeparator`；随后 3770-3771 为分隔符预留一字节，3825-3828 把
  URI 连同分隔符写入 binding。上游处理器若按分隔符切分展开名，就会看到
  额外/攻击者可控的组件，导致命名空间混淆甚至代码执行。
- **位置锚定**：采集档案 3752-3771，正式表收敛为 3752-3760（代码摘录上限
  500 字符）；独立 reviewer 独立选中 3752-3759 并给出 3825-3828 的写点，
  行号重叠，无需修订。后续 `2ba6c76f`（首见 R_2_4_7）把规则放宽为只拒绝
  非 RFC 3986 字符，属修好后的行为变化，不影响本条判定。
- **独立复核**：`independent-reviewer-libexpat-CVE-2022-25236-deepseek-flash`
  在隔离上下文自行抓取 NVD/CVE/OSV/GHSA/PR/Changes 并核对 tag 与 blob，
  十项 `fields_verified=true`，grade B；GHSA REST 接口被限流，别名只能从
  HTML 页面核对（OSV 本身无 aliases）。

## 36. CVE-2022-25314 — libexpat copyString 整数溢出（libexpat R_2_4_4）

- **来源一致性**：NVD 主指标 CVSS 3.1 7.5 HIGH
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`），CWE-190；oss-security 引用的
  `Changes` 条目 #560 说明该函数只用于解析器创建时调用方传入的编码名、
  通常为硬编码、需要 64 位机器与 GB 级输入，预期影响为拒绝服务。
  MITRE CNA 记录为占位，无 metrics。
- **修复与祖先关系**：修复 `efcb347440ade24b9f1054671e6bd05e60b4cafd`
  只把 `int charsRequired` 改为 `size_t charsRequired`，1 行增 1 行删，
  只动 `expat/lib/xmlparse.c`，未附带回归测试；是 `R_2_4_5` 的祖先、
  不是 `R_2_4_4` 的祖先。2.4.5 中该声明在第 7471 行，2.4.4 在第 7415 行。
- **根因**：`copyString`（7415-7426）用 `int` 逐字符计数且无上界检查，
  再以 `charsRequired * sizeof(XML_Char)` 同时用于 `malloc_fcn` 与
  `memcpy`；计数回绕后分配与拷贝都使用回绕值，可造成越界或崩溃。调用点
  为 `parserInit:1090` 与 `XML_SetEncoding:1241`，输入是库使用者提供的
  编码名，不是文档内容。
- **位置锚定**：采集档案与独立 reviewer 都选中 7415-7426，reviewer 另确认
  7426 行为 `malloc`、7430 行为 `memcpy`，行号一致。
- **独立复核**：`independent-reviewer-libexpat-CVE-2022-25314-deepseek-flash`
  在隔离上下文核对 tag、blob、PR #560 与 2.4.5 源码，十项
  `fields_verified=true`，grade B；并记录 OSV 的 fixed 事件 `97a48405`
  是发布合并而非代码修复，属于 OSV 转换的排序缺陷。

## 37. CVE-2022-25315 — libexpat storeRawNames 整数溢出导致堆越界写（libexpat R_2_4_4）

- **来源一致性**：NVD 主指标 CVSS 3.1 9.8 CRITICAL
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`），CWE-190；`Changes` 条目 #559
  说明 `bufSize` 的整数溢出可导致堆越界写。MITRE CNA 记录为占位；
  GHSA-8w4r-jhg8-8rvj 标 "Moderate" 且 affected/patched 均 Unknown，与
  NVD 的 9.8 冲突，按 NVD 主指标记录并在分歧中保留。
- **修复与祖先关系**：修复 `eb0362808b4f9f1e2345a0cf203b8cc196d776d9`
  在 `bufSize = nameLen + ROUND_UP(...)` 之前加入
  `rawNameLen > (size_t)INT_MAX - nameLen` 检查并改用 `size_t` 中间量；
  是 `R_2_4_5` 的祖先、不在 `R_2_4_4` 中，修复未附带回归测试。
- **根因**：`expat/lib/xmlparse.c` 的 `storeRawNames` 用 `int bufSize` 与
  `int nameLen` 计算扩容尺寸（2.4.4 的 2565-2579），`ROUND_UP` 后的
  `rawNameLength` 可让加法回绕，2578 行的 `bufSize > tag->bufEnd - tag->buf`
  判断因此被绕过，2597 行 `memcpy` 按未回绕长度写入，造成堆越界写。
- **位置锚定**：采集档案与正式表取 2572-2579（含 `bufSize` 计算与
  `REALLOC`）；独立 reviewer 选中 `storeRawNames` 2560-2602、根因行 2577、
  写入行 2597，与 2572-2579 重叠。
- **独立复核**：`independent-reviewer-libexpat-CVE-2022-25315-deepseek-flash`
  在隔离上下文核对 NVD/CVE/OSV/GHSA、PR #559、tag 祖先与 2.4.5 源码，
  十项 `fields_verified=true`，grade B；`XML_UNICODE` 配置下的可利用性
  只依据上游 commit message，未动态验证。

## 38. CVE-2022-25313 — libexpat build_node 递归导致栈耗尽（libexpat R_2_4_4）

- **来源一致性**：NVD 主指标 CVSS 3.1 6.5 MEDIUM
  （`AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`），CWE-674；GHSA 另列 CWE-400。
  上游 `Changes` 条目 #558 写的是"拒绝服务或潜在任意代码执行"，比 NVD
  的 DoS-only 评分更广，按 NVD 记录并在分歧中保留。MITRE CNA 记录为占位。
- **修复与祖先关系**：修复 `9b4ce651b26557f16103c3a366c91934ecd439ab`
  （"Prevent stack exhaustion in build_model"）删除 `build_node`，把
  `build_model` 改为用目标数组作栈的迭代实现；父提交就是漏洞提交，
  经 PR #558 合并 `bbdfcfef` 进入主线，是 `R_2_4_5` 的祖先、不在
  `R_2_4_4` 中。修复未加回归测试（`test_nested_groups` 在 2.4.4 已存在）。
- **根因**：`expat/lib/xmlparse.c` 的 `build_node` 对 DTD 内容模型的每个
  子节点递归调用自身（2.4.4 的 7344-7347），`doProlog:5423` 在解析元素
  声明时经 `build_model` 触发，且 2.4.4 对嵌套深度没有任何上限，深嵌套的
  内容模型可耗尽栈。只有注册了 `XML_SetElementDeclHandler` 的应用可达。
- **位置锚定**：采集档案 7344-7347（递归调用）；独立 reviewer 选中
  `build_node` 7320-7350、递归调用 7346 行、`build_model` 调用点 7386，
  行号重叠。2.4.5 的迭代重写本身有正确性回归，由 2.4.6 的 `b12f34fe`
  （PR #566）修正，不构成本 CVE 的重新出现。
- **独立复核**：`independent-reviewer-libexpat-CVE-2022-25313-deepseek-flash`
  在隔离上下文核对 tag 祖先、2.4.5 源码、PR #558 与上游文本，十项
  `fields_verified=true`，grade B；未动态复现栈耗尽阈值。

## 39. CVE-2023-46218 — curl 混合大小写公共后缀绕过 PSL 检查（curl 8.3.0）

- **来源一致性**：CURL-CVE-2023-46218 的 JSON 记录为 CWE-201、Medium、
  SEMVER 7.46.0→8.5.0、`last_affected 8.4.0`、GIT `e77b5b74`→`2b0994c2`，
  HackerOne 2212193；NVD 主指标 CVSS 3.1 6.5 MEDIUM
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N`），主弱点为 NVD-CWE-noinfo，
  次弱点 CWE-178；两条 CWE 一并记录。
- **来源缺陷**：CVE v5 CNA 的版本编码退化，只表达 8.4.0，未正确表达
  7.46.0–8.4.0，且无 metrics/CWE；OSV 的 GIT 区间用 7.46.0 的发布提交与
  `tiny-curl-8_4` 分支提交作边界，不是代码边界；GHSA-59mm-6rr4-j9p2 是
  Unreviewed 且 `affected` 为空；curl 公告 HTML 里的 commit 链接是缩写
  SHA，完整 SHA 需取其 JSON。
- **根因**：`lib/cookie.c` 的 `Curl_cookie_add` 把未规范化的 `domain` 与
  `co->domain` 直接交给 `psl_is_cookie_domain_acceptable`（8.3.0 的
  1047-1048），而 libpsl 的公共后缀比较区分大小写、`cookie_tailmatch`
  又不区分大小写；因此 `Domain=co.UK` 一类混合大小写公共后缀可绕过 PSL，
  成为跨站 supercookie。修复 `2b0994c2`（"cookie: lowercase the domain
  names before PSL checks"）用 `Curl_strntolower` 把两个域名复制进
  256 字节缓冲区后再比较；不是 8.4.0 的祖先、是 8.5.0 的祖先，
  `curl-8_5_0` 的 `lib/cookie.c` blob `9095cea3` 与修复后内容一致。
- **历史边界**：reviewer 追查发现 7.46.0–7.47.x 使用
  `psl_is_public_suffix`，7.48.0 起（`c140bd78`）改用
  `psl_is_cookie_domain_acceptable`，两个 API 调用前都未规范化大小写，
  因此受影响下界按公告取 7.46.0 是自洽的。
- **测试**：代码修复提交本身不含测试，同系列 `323df4261` 新增
  `tests/data/test1476` 并随 8.5.0 发布；测试只读未执行。
- **位置锚定**：采集档案 1047-1048；独立 reviewer 选中
  `Curl_cookie_add` 1037-1061、关键调用 1048 行，行号重叠。
- **独立复核**：`independent-reviewer-curl-CVE-2023-46218-deepseek-flash`
  在隔离上下文核对快照 tree/blob、tag peel、8.5.0 内容与公告，十项
  `fields_verified=true`，grade B；未动态构造 Cookie 或运行测试。

## 40. CVE-2024-50343 — symfony 5.4.45 已含修复，判定不适用（排除记录）

- **背景**：该候选（`disc2_dd1aa213fa864be8ab94a915`）与同一批 2024-11 公告
  一起出现在 symfony 快照 `snap_39105a8a3ceb9fe4`（v5.4.45）的候选集中，
  但它属于 2024-08 的修复批次，不是 11 月安全发行。
- **否定证据**：GitHub advisory GHSA-g3rh-rrhp-jhh9 的受影响区间是
  `<5.4.43`；修复 `7d1032bbead9a4229b32fa6ebca32681c80cb76f`
  （"[Validator] Add `D` regex modifier in relevant validators"，2024-08-13）
  经 `git merge-base --is-ancestor` 确认是 `v5.4.45` 与 `v5.4.47` 的祖先。
  内容核验：`EmailValidator::PATTERN_HTML5`/`PATTERN_LOOSE` 在 v5.4.42 仍以
  `$/` 结尾，在 v5.4.45 已改为 `$/D`；`v5.4.45^{}` 为
  `2b66d7d7d8129531229708ef708860844db91944`，与快照
  `vulnerable_commit` 一致。因此快照高于修复版本，代码不含该缺陷。
- **处理**：不写 dossier、不派独立 reviewer、不写正式表；在
  `runs/verification/symfony_cve_2024_50343/NOT_APPLICABLE.md` 留存证据链，
  并把 `candidate_dossiers.jsonl` 中该行改为 `rejected` 且写明 blocker。
  正式表的 `snapshot_vulnerability_status` 只接受已晋升的
  `vulnerability_id`，因此否定结论无法写入真值矩阵，只能在本文与
  WORK_LOG 记录。计数随之变化：`in_validation` 978、`rejected` 2、
  未解决 2579。
- **注意**：若重跑 `scripts/build_candidate_dossiers.py`，该行会按上游
  advisory 重新计算回 `in_validation`，届时需要重新应用本排除。

## 41. CVE-2024-51996 — symfony 持久化 remember-me cookie 缺少属主校验（v5.4.45）

- **来源一致性**：CVE v5（GitHub_M CNA）给 CVSS 3.1 7.5 HIGH
  `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`、CWE-287/CWE-289，受影响
  `>=5.3.0,<5.4.47`、`>=6.0.0-BETA1,<6.4.15`、`>=7.0.0-BETA1,<7.1.8`；
  NVD 无 primary 指标，仅转列 GitHub 的 Secondary 7.5，`vulnStatus=Deferred`；
  OSV/GHSA 与 symfony.com 页一致。版本范围上 5.4.45 在受影响区间内。
- **来源缺陷**：GitHub_M CNA 描述与 NVD CISA-ADP 的 CPE 把组件误写成
  "Symphony process"/`symphony_process`，与 GHSA/OSV/symfony.com 的
  authentication bypass 描述不符（疑似从无关公告复制）；CISA-ADP 的受影响
  范围编码畸形（version 0 / lessThanOrEqual 5.3.0）；GHSA 另记 CVSS 4.0 8.7，
  本数据集取 3.1 的 7.5。
- **根因**：`PersistentRememberMeHandler::consumeRememberMeCookie`
  （v5.4.45 的 69-70 行）按 series 取回持久化 token 并校验 token 值，却从不
  比较 `persistentToken->getUserIdentifier()`/`getClass()` 与 cookie 中携带的
  用户标识；父类 `AbstractRememberMeHandler::consumeRememberMeCookie`
  （第 74 行）直接用 `$rememberMeDetails->getUserIdentifier()` 加载用户，因此
  持有任意有效 series/token 的攻击者只要改写 cookie 的 identifier 字段即可
  冒充该账户。
- **修复**：`81354d39`（"[security-http] Check owner of persisted remember-me
  cookie"，2024-11-07）加入属主与 class 比对、用持久化 token 重建
  `RememberMeDetails`、`explode(':', ..., 2)` 及 `unset($rememberMeDetails)`；
  是 `v5.4.47` 的祖先、不是 `v5.4.45`（`2b66d7d7`）的祖先，
  `v5.4.47^{}`=`d869cc18`。reviewer 另用 GitHub compare API
  （v5.4.45...v5.4.47，ahead_by 79）交叉验证浅克隆的祖先判断。
- **独立复核**：`independent-reviewer-symfony-CVE-2024-51996-deepseek-flash`
  在隔离上下文核对身份、别名、CWE、CVSS、范围、修复、位置与语言，十项
  `fields_verified=true`，grade B；行号 69-70 与采集档案重叠；未安装
  Symfony、未构造 cookie 或 PoC。

## 42. CVE-2024-50341 — symfony 5.4.45 不含受影响代码路径（排除记录）

- **背景**：该候选（`disc2_35ba5cc08ffab29d21687940`）出现在 symfony
  快照 `snap_39105a8a3ceb9fe4`（v5.4.45）的候选集中，问题为
  `Security::login` 编程式登录不调用 firewall 自定义 `user_checker`。
- **否定证据**：GHSA-jxgr-3v7q-3w9v / CVE-2024-50341 的范围只有
  `>=6.2.0,<6.4.10`、`>=7.0.0,<7.0.10`、`>=7.1.0,<7.1.3`，没有 5.4 区间；
  修复 `22a0789a0085c3ee96f4ef715ecad8255cf0e105`（2024-07-17，
  "use firewall-specific user checkers when manually logging in users"）
  只针对 6.4 分支发布。`git ls-tree -r v5.4.45 -- src/Symfony/Bundle/SecurityBundle/`
  中不存在 `Security.php`，也没有 `security.user_checker_locator` 的装配，
  这两个能力都是 6.2 引入的；`merge-base --is-ancestor 22a0789a v5.4.45^{}`
  返回非祖先。
- **处理**：不写 dossier、不派独立 reviewer、不写正式表；证据链留在
  `runs/verification/symfony_cve_2024_50341/NOT_APPLICABLE.md`，候选行改为
  `rejected` 并写明 blocker。正式表只接受已晋升 `vulnerability_id` 的
  否定行，因此该结论只能记在本文与 WORK_LOG。
- **计数**：候选表 `rejected` 3 行（含 withdrawn 的 CVE-2024-51999）、
  `verified` 46、未解决 2577。

## 43. CVE-2025-64500 — symfony PATH_INFO 丢失前导斜杠导致有限授权绕过（v5.4.45）

- **来源一致性**：CVE v5（GitHub_M CNA）给 CVSS 3.1 7.3 HIGH
  `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L`、CWE-647，受影响
  `>=2.0.0,<5.4.50`、`>=6.0.0,<6.4.29`、`>=7.0.0,<7.3.7`；NVD 无 primary
  指标，只转列 GitHub 的 Secondary 7.3；OSV/GHSA、symfony.com 页一致。
- **来源缺陷/差异**：CNA 的 affected 只列 symfony/symfony，未单列
  `symfony/http-foundation`（GHSA/OSV 两个包都列）；GHSA 对
  http-foundation 只写 `< 5.4.50`，OSV 归一化为 `introduced 0`。
- **根因**：`Request::preparePathInfo`（v5.4.45 的 1973-1979）在
  `$pathInfo = substr($requestUri, \strlen($baseUrl))` 之后只判断
  `false`/空串，否则原样返回；剩余部分不以 `/` 开头时（如
  `/api/index.phpfoo` 配 baseUrl `/api/index.php`）返回 `foo`。依赖
  `/` 前缀的访问控制规则因此可能被绕过；入口为 `getPathInfo()`（870 行，
  873 行调用）。
- **修复**：`9962b91b`（"[HttpFoundation] Fix parsing pathinfo with no
  leading slash"，2025-11-03）把条件改为
  `false === $pathInfo || '' === $pathInfo || '/' !== $pathInfo[0]` 并返回
  `'/'.$pathInfo`；新增 `/api/index.phpfoo` 的回归用例。是 `v5.4.50`
  （peel `4b031a79`）的祖先、不是 `v5.4.45` 的祖先；
  v5.4.50 的 Request.php blob `393b5472` 与补丁后镜像一致，而 v5.4.45 的
  `561cb887` 与补丁前镜像 `d1103cf8` 不同（其间有其他提交改过该文件），
  因此等价性按代码块而非 blob 判定。
- **独立复核**：`independent-reviewer-symfony-CVE-2025-64500-deepseek-flash`
  在隔离上下文核对身份、别名、CWE、CVSS、范围、提交、修复版本、位置与语言，
  十项 `fields_verified=true`，grade B；另用 GitHub compare API 交叉验证
  祖先关系；未执行请求或 PoC。
