# 续跑与交接

工作主记录：`../WORK_LOG.md`；机器进度：`../runs/progress.json`；结构校验：`../runs/validation_draft.txt`。

## 当前状态（2026-10-22）

- 准入：50/50 PASS（分数 77–100，12 种主语言），见 `runs/admission/decisions.jsonl`。
- 快照：75 个，全部固定 github-linguist 9.7.0、`full_scan=true`、枚举与 `git ls-tree` 一致。
  其中 50 个是各仓库 HEAD 的精确 SHA，22 个是评测目标（覆盖 73 条漏洞；libexpat 的七条共用 R_2_4_4 快照，vite 的四条共用 v5.0.11 快照，symfony 的十八条共用 v5.4.45 快照，django 的八条共用 3.0.2 快照，netty 六条共用 4.1.59.Final 快照、jenkins 五条共用 2.441 快照）（express 4.19.2、flask 2.3.1、
  werkzeug 3.0.2、rack 2.2.3、gin v1.5.0、guzzle 7.4.4、Newtonsoft.Json 12.0.3、
  netty 4.1.59.Final、hyper v0.14.2、rustls 0.23.4、vite v5.0.11、libexpat R_2_4_4、
  protobuf v3.20.1、phoenix v1.6.13、undici 5.19.0、cJSON v1.7.16、libarchive v3.7.7、
  laravel v11.30.0、curl 8.3.0、django 3.0.2、jenkins 2.441、symfony 5.4.45）。另外 2 个是非评测快照：
  OpenSSL 3.0.1（CVE-2022-0778 无候选行，探查材料保留但不提升，见该目录 README）和
  sinatra v3.0.3（`snap_916afbf76073e831`；CVE-2022-45442 仍为 pending，因此 `evaluation_target=false`）。
- 正式目录：73 条漏洞、73 条位置、73 条复核（grade B）、1839 条证据、73 行真值矩阵（全部 `confirmed_affected`）。
  语言覆盖 JS/Python/Ruby/Go/PHP/C#/Java/Rust/TypeScript/C/C++/Elixir。
- 候选：2626 行（in_validation 503 / pending_location 750 / pending_version 861 / verified 83 /
  rejected 429）。未解决 2114 行。`verified` 比漏洞数多 10，全部是别名簇重复行——cJSON、hyper、
  laravel、netty、undici、flask、werkzeug、phoenix、protobuf、rustls 各比本仓库漏洞数多一行，
  均指向已提升漏洞；可按 `data/candidates.jsonl` 的 `status=verified` 逐行复算。
  `rejected` 429 行：withdrawn 的 CVE-2024-51999、已含修复的 CVE-2024-50343、不在受影响范围的 CVE-2024-50341、
  引入版本晚于快照的 netty CVE-2022-41915（4.1.83 引入，快照 4.1.59）、同样晚于快照的
  curl CVE-2024-0853（8.5.0 引入，快照 8.3.0）、18 条 OSV 已发布范围不含 axios v1.15.0 的候选
  （11 条修复已在 1.15.0 及之前，7 条 1.15.1 之后才引入）、django CVE-2021-35042
  （回归在 3.1 引入，3.0.2 仍做 order_by 严格校验）、174 条 Jenkins 范围候选
  （171 条修复已在 2.441 及之前，3 条 2.442 之后才引入），以及按同样区间规则排除的
  netty 7、symfony 57、undici 18、vite 4、rack 10，express/guzzle/hyper/laravel/
  flask/werkzeug/phoenix/rustls 共 21 条，以及 django 114 条（PyPI `django` 的全部
  已发布区间都在 3.0.2 之前修复或之后才引入）。除 35042 有代码证据外，其余按已发布
  范围排除，不含代码层结论；逐条理由见 `runs/verification/*_snapshot_not_applicable/NOT_APPLICABLE.md`
  （axios、Jenkins、netty、symfony、undici、vite、rack、django 各自一份；八个小型仓库合并为
  `small_repos_snapshot_not_applicable/NOT_APPLICABLE.md`）。
  CVE-2026-44487 与 44486 是同一修复的重复公告，不另立条目，候选保持 `pending_location`，
  见 `runs/verification/axios_cve_2026_44487/NOT_APPLICABLE.md`。
- django 3.0.2 版本适用性：13 条候选的 OSV 区间机械包含 3.0.2（`introduced: 0` / “版本列表含 3.0.x”），
  但公告正文只声明 4.2/5.x/6.x，或明说旧分支“未评估、可能受影响”。已将它们的 triage 状态
  从 `in_validation` 降为 `pending_version` 并写入 blocker；没有以 OSV 机械枚举当作受影响证据。
  逐条范围对照见 `runs/verification/django_3.0.2_range_scoping/SCOPING.md`。
- django 3.0.2 全量区间核查：对 118 条 `in_validation` 候选只取 PyPI `django` 的已发布区间，
  114 条的所有区间都在 3.0.2 及之前修复、或在 3.0.2 之后才引入，已拒收；4 条区间包含
  3.0.2（CVE-2021-31542、33203、33571、44420），均已有独立 verdict，保持 pending。
  逐条区间见 `runs/verification/django_snapshot_not_applicable/NOT_APPLICABLE.md`。
  这是范围适用性判定，不是代码层否定；不涉及 3.0.x 的公告文本不作为受影响证据，
  也不把“未评估旧分支”反推成已受影响。
- Jenkins 2.441 版本适用性：对 192 条 `in_validation` 候选按 Maven
  `org.jenkins-ci.main:jenkins-core` 区间逐条计算，171 条修复已在 2.441 及之前、3 条在 2.442
  之后才引入，均已拒收；18 条区间包含 2.441，保持 `in_validation`（其中 8 条已有 verdict）。
  依据与逐条区间见 `runs/verification/jenkins_snapshot_not_applicable/NOT_APPLICABLE.md`。
- netty / symfony 版本适用性：netty 4.1.59.Final 上 32 条候选中 7 条拒收（4 条修复已在快照内，
  3 条 4.1.91+ / 4.2.0 才引入），24 条保留；其中 CVE-2021-21409 判定为已提升
  CVE-2021-21295 在 4.1.59 上的重复公告（公告自称 followup、"miss to fix this one case"；
  其修复 b0fa4d5 改的是 21295 修复在 4.1.60 引入的 `if (!stream.isHeadersReceived())` 门控，
  4.1.59 根本没有 content-length 校验），降为 `pending_location`，不另立条目，
  见 `runs/verification/netty_cve_2021_21409/NOT_APPLICABLE.md`（该范围 `<4.1.61.Final`
  确实包含 4.1.59，因此不是范围拒收）。
  symfony 5.4.45 上 59 条候选按“每个区间都
  `fixed <= 5.4.45` 或 `introduced > 5.4.45`”判定，57 条拒收，2 条保留
  （CVE-2024-51736 `0..5.4.46`、CVE-2026-24739 `0..5.4.51`）。
  报告见 `runs/verification/{netty,symfony}_snapshot_not_applicable/NOT_APPLICABLE.md`。
- undici 5.19.0 / vite 5.0.11 / rack 2.2.3：分别拒收 18 / 4 / 10 条，保留 11 / 9 / 16 条。
  报告见 `runs/verification/{undici,vite,rack}_snapshot_not_applicable/NOT_APPLICABLE.md`。
- 小型仓库：express 4.19.2、guzzle 7.4.4、hyper 0.14.2、laravel 11.30.0、flask 2.3.1、
  werkzeug 3.0.2、phoenix 1.6.13、rustls 0.23.4 共 21 条候选按同一区间规则拒收；
  合并报告见 `runs/verification/small_repos_snapshot_not_applicable/NOT_APPLICABLE.md`。
- 覆盖：50 个仓库全部 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`。累计已提升 73 条漏洞，停止规则未满足。
  已知覆盖边界之一：curl 官方公告 CVE-2023-38546（8.3.0 受影响）未进入候选表——NVD 关键词结果集
  与 OSV/仓库公告都没有这条记录；已记入 `../WORK_LOG.md`，未手工补候选。
- 未提升但已有独立 verdict（20 条，均保持 pending，不强行提升）：
  - `severity_consistent=false`（8 条）：CVE-2021-31542（django，NVD 7.5 HIGH vs Django 公告
    low，另与已提升的 CVE-2021-28658 经 reviewer 判定为不同缺陷）、CVE-2021-33203（django
    admindocs 路径穿越；NVD/GHSA/SUSE/Ubuntu 为 MEDIUM 4.9，Django 公告称 low）、
    CVE-2021-44420（django URL resolver 尾随换行；NVD 7.3 HIGH / GHSA MODERATE / Django 与
    Red Hat low，且 OSV 范围含 3.0.2 而 CNA/NVD 从 3.1 起）、
    CVE-2024-51736（symfony，CNA 0.0 / GHSA 8.4 / NVD 9.8）、CVE-2026-56812（phoenix，
    NVD 7.5 HIGH vs CNA/OSV/GHSA 6.3 MEDIUM）、CVE-2025-31720、CVE-2025-31721（jenkins）、
    CVE-2022-45442（sinatra Content-Disposition；NVD/CNA/GHSA/rubysec 均 HIGH 8.8，但 Ubuntu
    优先级 Medium、Red Hat threat_severity Moderate、SUSE important 且自算 7.0）。
  - `evidence_independent=false`（15 条）：CVE-2021-33571（django `ipv4_re` 前导零，HIGH）、
    CVE-2024-49766（werkzeug `safe_join`，MEDIUM）、CVE-2025-67635、67636、67637、67638、
    67639（jenkins，均为 MEDIUM）、CVE-2021-44420、CVE-2022-45442（sinatra；仅厂商/报告者
    材料与发行版 triage，Debian 的 0007 补丁是上游补丁副本）、CVE-2026-22860（rack
    `Rack::Directory` 根前缀穿越；Debian 的 backport 仍是 vendor commit 的副本）、
    CVE-2025-31720、31721（jenkins）与 CVE-2026-67339（guzzle，全部来源同源于 GitHub advisory）、
    CVE-2026-44486（axios 重定向后陈旧 `Proxy-Authorization` 外带，所有技术材料同源于厂商公告）、
    CVE-2026-42037（axios `formDataToStream.js:27` 未过滤 `.type` 中的 CR/LF，可注入分段头；
    仅厂商/报告者材料，且另有 `affected_range=false`）。
  - `cvss=false`（1 条）：CVE-2024-43045（jenkins My Views 权限缺失）。档案已更正 GHSA 5.4 /
    NVD 6.3 的事实性错误并记录 `CORRECTIONS.md`，但 round-1 verdict 不改写，门槛仍拦下。
  - 另有 CVE-2021-44420 的 `affected_range=false` 与 `cwe=false`（NVD-CWE-Other / CWE-287 /
    CWE-290 三方不一，范围元数据不含 3.0.x），同样按规则不拉平。
  - CVE-2026-42037 的 `affected_range=false`：公告下界 `>=1.0.0` 过宽——`lib/helpers/formDataToStream.js`
    在 npm 1.0.0–1.2.0 中不存在，1.3.0 起才出现且已带缺陷；reviewer 判有效区间 1.3.0–1.15.0，
    修复边界 1.15.1 准确。按规则如实记录，不改写 verdict，也不缩窄档案去凑门槛。
  `promotion_report.json` 因此为 73 promoted / 20 pending：上述 20 条均已有独立 verdict，
  但至少一个字段未过门槛；不通过改写 verdict 或拉平来源来提升。
- `validate_dataset.py --draft`：0 error / 50 warning。仍是 draft，不可发布为完整真值。

## 目录与入口

- `data/`：九张正式表 + `excluded_candidates.jsonl`。
- `runs/admission/`：准入原始观察和 50 条 PASS 决策。
- `runs/language/`：每个快照的全语言盘点；`runs/language/superseded/` 是修复精确 SHA 前生成的
  9 个错误快照，已移出正式扫描，仅保留审计。
- `runs/discovery_v2/`：OSV/NVD 第一、二轮检索与原始响应。
- `runs/discovery_v3/`：官方 GitHub repository advisory 拉取（50/50 成功，846 条记录）、请求日志与归一化候选。
- `runs/verification/`：七十三个已提升漏洞的逐字段核验档案（express、flask、werkzeug、rack、gin、
  guzzle、Newtonsoft、netty、hyper、rustls、vite、libexpat、protobuf、phoenix、undici、cJSON、libarchive、
  laravel、curl、django、jenkins、symfony），以及未提升候选的档案与材料：django CVE-2021-33203、
  CVE-2021-44420、CVE-2021-33571，werkzeug CVE-2024-49766，jenkins CVE-2025-31720、31721、
  67635–67639，CVE-2024-51736，OpenSSL 探查材料，sinatra CVE-2022-45442、rack CVE-2026-22860
  与 guzzle CVE-2026-67339 的完整档案（三者均已有 verdict，但字段未过门槛），
  netty CVE-2022-41915、netty CVE-2021-21409（重复公告判定）与 curl CVE-2024-0853 的
  NOT_APPLICABLE 记录，
  jenkins CVE-2024-43045 的 CORRECTIONS 记录；axios 侧另有 CVE-2026-44486、
  CVE-2026-42037 的完整档案（均已有一轮 verdict、字段未过门槛），CVE-2026-44487 的重复公告判定
  （`axios_cve_2026_44487/NOT_APPLICABLE.md`），以及 18 条范围不适用候选的批量说明
  （`axios_snapshot_not_applicable/NOT_APPLICABLE.md`）；django 侧有 CVE-2021-35042 的
  NOT_APPLICABLE 记录与 13 条候选的范围对照（`django_3.0.2_range_scoping/SCOPING.md`）；
  Jenkins 侧有 174 条范围不适用候选的批量说明（`jenkins_snapshot_not_applicable/NOT_APPLICABLE.md`）；
  django 侧另有 114 条全量区间拒收表（`django_snapshot_not_applicable/NOT_APPLICABLE.md`）；
  netty 7 条、symfony 57 条、undici 18 条、vite 4 条、rack 10 条各有独立批量说明，
  八个小型评测仓库的 21 条合并记录在 `small_repos_snapshot_not_applicable/NOT_APPLICABLE.md`。
- `runs/independent/`：九十三个漏洞的独立 reviewer `REVIEW.md` 与 `verdict.json`（73 已提升 + 20 pending；隔离上下文、只读，
  未读取采集档案与 `data/`）；
  `runs/independent/superseded/` 保留 phoenix 与 protobuf 的 round1
  失败 verdict（入口点/符号与行号笔误，已由 round2 从零复核，未改字段）。
- `runs/verification/promotion_report.json`：推广门槛结果（73 promoted，20 pending：8 条 severity 等级冲突、
  15 条缺独立证据（与等级组有 4 条重叠）、1 条 `cvss=false`；44420 另有 affected_range/cwe 不一致，
  42037 另有 affected_range 不一致）。

## 重新生成

```bash
cd /home/luchitong/work/repo-vuln-50-v02
.venv/bin/python scripts/build_formal_tables.py
.venv/bin/python scripts/validate_dataset.py . --draft > runs/validation_draft.txt
.venv/bin/python scripts/refresh_reports.py
```

注意：

- `build_formal_tables.py` 从 `runs/verification/candidate_dossiers.jsonl` 恢复 triage 状态，
  并从 `data/vulnerabilities.jsonl` 读取已提升漏洞；不要手工编辑 `data/candidates.jsonl`。
- 新增漏洞必须先写 `runs/verification/<name>/dossier.json`（含 `field_evidence`），
  由独立 reviewer 产出 `runs/independent/<name>/verdict.json`，再运行
  `scripts/promote_verified.py`（先 dry-run，确认后再 `--apply`）。
- `promote_verified.py` 强制：verdict 的 `fields_verified` 全为 true、grade A/B、
  vulnerable commit 相同、位置文件相同且行号重叠、reviewer 身份与时间存在。
  grade A 无 `reproduction_reference` 时自动降 B。
- 新增评测快照后需重建 `data/snapshots.jsonl` 和 `data/snapshot_vulnerability_status.jsonl`；
  `evaluation_target` 由已提升漏洞的 snapshot_id 自动推导。

## 下一步

1. 逐仓库把 `in_validation` 候选推进到根因/修复发行版闭环；优先处理候选量大的仓库
   （curl、django、jenkins、symfony、next.js），但不得按数量截断。
2. 每个新提升漏洞都需要新的独立 reviewer；不得复用采集者身份。
3. 若要对某仓库声明 `PASS_KNOWN_SWEEP`，需最近两轮无新增已验证漏洞、官方源与历史补丁源成功、
   且候选已解释。当前不满足。
4. 动态红绿测试尚未安排；没有它，grade A 不能成立。

验证命令：

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_collection.py' -v
.venv/bin/python scripts/validate_preselection.py
.venv/bin/python scripts/validate_dataset.py . --draft
```

draft 通过只表示结构与外键一致；发布验收还需要覆盖停止条件、A/B 复核和人工抽查。
