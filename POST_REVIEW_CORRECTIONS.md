# POST_REVIEW_CORRECTIONS — 入库后更正记录

记录「已入库、复核员提出文档级分歧、采集侧独立复算后按实测更正 `data/`」的每一批。
原则：**只更正文叙述与出处字符串，不更判定、等级、候选决策与任何实测数值**；每次
更正都有守卫脚本（dry-run 默认、写前备份、断言被替换字符串等于入库时写入的原值）。

## 2026-10-25 — CVE-2026-32777（libexpat R_2_6_2，round49）

- 复核裁定：`confirmed_affected`，`grade_recommendation = A`，
  `runs/independent/libexpat_R_2_6_2_CVE-2026-32777_round49/verdict.json`，
  `reviewed_at = 2026-10-24T23:58:10Z`。**裁定本身没有被更正，也没有被重新裁定。**
- 复核员记录三条说明性分歧，均属「卷宗文本」而非「红/绿结论」。采集侧没有直接照改，
  先自己复算，再决定改哪一侧。

### 1. 是哪个 token 零推进

- 入库文本：`critical_operation.description` 与 `trace[1].description` 说
  `XmlPrologTok` 对「processing instruction **或** start tag」返回 `XML_TOK_INSTANCE_START`。
- 复核员：PI 不返回该 token。
- 采集侧复算（`/tmp/r49chk/tok.c`，链接 2.6.2 的 `libexpat.a`，直接调 `XmlGetUtf8InternalEncoding()`
  与 `XmlPrologTok`）：

  ```
  input=<?xml version='1.0'?><a   tok=12 advanced=21
  input=<a                       tok=29 advanced=0
  ```

  即 PI 返回 `XML_TOK_XML_DECL`(12) 并**前进** 21 字节；零推进的 `XML_TOK_INSTANCE_START`(29)
  来自其后的 `<a`。复核员正确。
- 落地：`data/locations.jsonl` 的
  `loc_CVE_2026_32777_snap_67132f0363b8bc23.critical_operation.description` 与
  `trace[1].description` 改为只指 start tag，并明确「前面那个 PI 返回 `XML_TOK_XML_DECL` 且会前进」。

### 2. 4550 行属于哪个函数

- 入库文本：`trace[0].function` 写成 `doProlog`。
- 复核员：4550 行不在 `doProlog` 里。
- 采集侧复算：2.6.2 的 `doProlog` 起于 4681，4550 行位于 `entityValueInitProcessor`，正是
  `m_processor = entityValueProcessor` 的交接处。复核员正确。
- 落地：`trace[0].function` 改为 `entityValueInitProcessor`。

### 3. `f31adfd5` 的提交标题

- 入库文本：`fix_commits[f31adfd5…].message` 以 “Prepare release 2.7.5 (2026-03-17)” 开头。
- 复核员：该提交的实际标题是 “Merge pull request #1159 from libexpat/prepare-release”。
- 采集侧复算：`git log -1 --format=%s f31adfd5` 在完整 clone 上确为
  “Merge pull request #1159 from libexpat/prepare-release”。复核员正确。
- 落地：`data/vulnerabilities.jsonl` 的 `CVE-2026-32777.fix_commits[f31adfd5…].message`
  改为 “Merge pull request #1159 from libexpat/prepare-release (2026-03-17); OSV fixed event”。
  该提交在 `fix_commits` 里的角色不变（OSV fixed event 对应的 release 提交）。

### 执行与边界

- 脚本：`runs/data_fixes/apply_post_review_corrections_round49_2026-10-25.py`
  （dry-run 输出 `changes: 4`、`problems: []` 后才 `--apply`）。
- 备份：`runs/data_fixes/vulnerabilities_before_post_review_corrections_round49_20261025T000107Z.jsonl`、
  `runs/data_fixes/locations_before_post_review_corrections_round49_20261025T000107Z.jsonl`。
- 更正后 `python3 -I scripts/validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`；
  九表计数不变（163 / 163 / 6369 / 163 / 134），triage 与两个队列均未重写。
- **没有改**：`reviews.jsonl` 的等级与 `independent_reviewer` / `independent_verdict_path`；
  `snapshot_vulnerability_status` 的 `basis` 与 `checked_at`；`snapshot_candidate_triage.jsonl`
  的任何行；verdict 原件（`runs/independent/**`）；任何 evidence 的实测数值。
- 卷宗侧（`runs/verification/libexpat_R_2_6_2_CVE-2026-32777/`）不回溯改写，其 README
  与 `repro/RESULTS.md` 保留采集时的原始措辞；分歧与裁定以本文件为准。
