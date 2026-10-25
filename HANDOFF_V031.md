# HANDOFF_V031 — 下一对话交接文档

> 面向全新对话（无本会话记忆）。读完本文件即可接续。数据集根目录：`/home/luchitong/work/repo-vuln-50-v031`。

## 0. 一句话现状

RepoVuln-50 是 50 个上游开源仓库的漏洞审计评测基准，目标「一库一冻结 commit」。当前是 **v0.3.1 draft**：
已完成「无损迁移 + 低成本相关性筛选 + 独立选版审查 + 证据先行选版」，**48/50 仓库有评测目标，其中 46 个已
frozen（均通过隔离选版审查 accept，最新为 grpc v1.52.0，2026-10-24 冻结）、2 个 legacy `documented_exception`
目标仍为 rejected（hyper、Newtonsoft.Json）**；nlohmann/json 与 openssl/openssl 无评测目标（漏洞窗口内无可用
稳定 tag）。**138 条评测目标上的已确认正样本（48 B + 90 A，按 `data/reviews.jsonl` 与 status 表实测）**，
另有 29 条历史快照样本（全 B）保留为证据；2626 条候选已产出 2613 条相关性 triage。
**未完成 2 库选版、574 条 unknown 与 527 条 possible 未决、无 Agent 运行、未达发布门槛**。
最新正样本是 nodejs/undici `v5.19.0` 上的 CVE-2024-24758（round53，grade A，复核者全新 clone、自写 harness 在 v5.19.0/v5.28.2/v5.28.3 三版上执行 12 个用例红/绿：`httpRedirectFetch` 的跨 origin 分支只删 `authorization`，`proxy-authorization` 被原样送到重定向目标（v5.19.0/v5.28.2 红，目标收到 `Basic UFJPWFktU0VDUkVULXJvdW5kNTM=`），v5.28.3 起三头全空；同快照 v5 线修复提交 `d3aa574b`、6.x 线 `b9da3e40`），随后为
nodejs/undici `v5.19.0` 上的 CVE-2024-30260（round52，grade A，复核者全新 clone、自写 harness 在 v5.19.0/v5.28.3/v5.28.4 三版上执行红/绿：`shouldRemoveHeader` 不剥 `proxy-authorization`，跨 origin 重定向把该 header 送到目标，v5.28.4 起不再送；v5 线实际修复提交是 `64e3402d`，公告只点名的 `68057466` 只修 main），随后为 libexpat `R_2_6_2` 上的 CVE-2024-50602（round51，grade A，复核者全新 clone 与独立构建，自写 harness 在 2.6.2/2.6.3/2.6.4 三版上重跑红/绿：`XML_StopParser` 收下未启动 parser 后 `XML_ResumeParser` 在 `normal_updatePosition` 读 NULL，fill=0 时 2.6.2/2.6.3 分别 exit 134/139，2.6.4 全部 exit 0），随后为同一快照上的 CVE-2026-32778（round50，grade A，复核者全新 clone 与独立构建，自写 harness 在 2.6.2/2.7.4/2.7.5 三版上重跑红/绿：2.6.2 与 2.7.4 在 budget 3 上 `keyeq` 读 NULL 崩溃 exit 1/139，2.7.5 全部 exit 0），随后为同一快照上的 CVE-2026-32777（round49，grade A，复核者自建 clone 与六棵构建树、自写 harness 在 2.6.2/2.7.4/2.7.5 三版上重跑红/绿：红是纯 CPU 自旋挂死 exit 142，绿是立即返回 XML_ERROR_SYNTAX → XML_ERROR_EXTERNAL_ENTITY_HANDLING），随后为同一快照上的 CVE-2026-32776（round48，grade A，复核者自写 harness 在 2.6.2/2.7.4/2.7.5 三版上重跑红/绿，并用 gdb 确认未初始化函数指针），随后为同一快照上的 CVE-2026-24515（round47，grade A，复核者自写 harness 在 2.6.2/2.7.3/2.7.4 三版上重跑红/绿），随后为同一快照上的 CVE-2024-8176（round46，grade A，复核者自写 harness 重跑三种实体形态红/绿 + 非嵌套对照），随后为 PHPMailer 6.1.5 上的 CVE-2021-3603（round45，grade A，复核者自写 `harness.php` 执行红/绿 + 负控制），随后为 werkzeug 3.0.2 上的 CVE-2024-49767（round44，grade A，复核者执行红/绿 + 逐块 `receive_data` 插桩），随后为 flask 2.3.1 上的 CVE-2026-27205（round43，grade A，复核者执行红/绿 + nginx `proxy_cache` 串号演示）、rack 3.1.13 上的 CVE-2025-61780（round42，grade A，复核者执行红/绿并测响应头）、同一快照上的 CVE-2025-61919（round41，grade A，复核者执行红/绿并测内存）、CVE-2025-61771（round40，grade A，复核者执行红/绿并测内存）、CVE-2025-61770（round39，grade A，复核者执行红/绿并测内存）、CVE-2025-61772（round38，grade A，复核者执行红/绿并测内存），再后为同一快照上的 CVE-2025-49007（round37，grade A，复核者执行红/绿），再后十三条为 django 4.2.13 上的 CVE-2026-15830、CVE-2026-53877、CVE-2026-15307、CVE-2026-25673、CVE-2025-64458、CVE-2025-59681、CVE-2025-13372、CVE-2026-1207、CVE-2026-1287、CVE-2026-1312、CVE-2026-48588、CVE-2026-25674、CVE-2025-13473，
均经隔离复核后 promote（其中 CVE-2026-15830 与 CVE-2026-53877 为无执行环境的静态 grade B，其余为 grade A；见 WORK_LOG 同日各卷宗条目）；
更早同日为 CVE-2026-33033、CVE-2026-33034、CVE-2026-3902、CVE-2026-1285、CVE-2025-14550、CVE-2025-48432、CVE-2025-64460、CVE-2025-26699、CVE-2025-32873、CVE-2025-57833、CVE-2025-59682（由新到旧）。
CVE-2024-24758 卷宗（`runs/verification/undici_v5.19.0_CVE-2024-24758/`，25 件 sha256 钉住来源 /
300,348 B、`dossier.json` 25 条证据 / 9 个字段映射 + 1 条快照语言证据）2026-10-25T00:50:25Z 收到
round53 的 **grade A** `confirmed_affected`（nodejs/undici `v5.19.0` lightweight tag →
`f5c89e5c87c7d702996b152c4ad86302b60c4181`，`lib/fetch/index.js` 的 `httpRedirectFetch`
**1204-1207** 行跨 origin 分支只 `delete('authorization')`（1206），没有 `proxy-authorization`，
1231-1239 行把同一 request 的 header list 重新 dispatch 到重定向目标；`headers.js` 的
`HeadersList.delete` 在 v5 线上只收一个参数，所以 v5.28.3 插入的
`delete('proxy-authorization', true)` 多写的 `true` 被忽略、删除照常生效）。v5 线修复提交
`d3aa574b1259c1d8d329a0f0f495ee82882b1458`（父提交即 v5.28.2 的 `9a14e5f3…`，只进 v5.28.3），
6.x 线同款提交 `b9da3e40f1f096a06b4caedbb27c2568730434ef`（只进 v6.6.1）；两者都是
`lib/fetch/index.js` +3/−0、回归测试 +4/−2（stats 9 / +7 / −2），v5 与 main 的 hunk 行号不同
（`@@ -1203,6 +1203,9 @@` vs `@@ -1326,6 +1326,9 @@`）。CWE-200（GHSA / NVD Secondary / OSV；
NVD Primary 是 `NVD-CWE-noinfo`），CVSS 3.1 4.5 MEDIUM
`AV:N/AC:L/PR:H/UI:R/S:U/C:H/I:N/A:N`（NVD Primary；GHSA 与 NVD Secondary 为 3.9 LOW / AC:H）。
2026-10-25T00:51:59Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 51 evidence / 1 status），
候选 `disc2_7bebf1081c3f0249b6759951` 于 00:52:30Z 改写为 `confirmed_affected`（backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round53_20261025T005203Z.jsonl`）。
复核者 `round53-independent-reviewer-luchitong` 全新 clone（HEAD `046bb4c6…`）自建三棵 tag 树、
自写 12 行用例（`undici.fetch` + 两个 loopback `node:http`）：v5.19.0 与 v5.28.2 的跨 origin 目标收到
`Proxy-Authorization: Basic UFJPWFktU0VDUkVULXJvdW5kNTM=`，`Authorization` 已被剥；v5.28.3 三个
敏感头全空；same-origin 三版都保留，负控制（调用方不传）三版都无头，`redirect:'manual'`
目标请求数为 0。v5.19.0 上 `Cookie` 同样泄漏，但那是邻居公告 GHSA-wqq4-5wpv-mx2g 的范围，
卷宗明确排除、复核者确认「范围主张诚实」。五处记为可接受：CWE 出处、4.5 vs 3.9、
`vulnerable_commit_basis` 的「no release at or after v5.28.3」措辞应读作 v5 线（版本列表本身含
v6.6.0）、cookie/host 邻居范围、行号全部逐行吻合。gate 34 个 preserved 文件 0 problems /
0 warnings / `ok: true`。
CVE-2024-30260 卷宗（`runs/verification/undici_v5.19.0_CVE-2024-30260/`，28 件 sha256 钉住来源、
`dossier.json` 23 条证据 / 9 个字段映射 + 1 条快照语言证据）2026-10-25T00:34:51Z 收到 round52 的
**grade A** `confirmed_affected`（nodejs/undici `v5.19.0` lightweight tag →
`f5c89e5c87c7d702996b152c4ad86302b60c4181`，`lib/handler/RedirectHandler.js:186-193` 的
`shouldRemoveHeader` 只在未知 origin 上剥 `authorization`（长度 13）与 `cookie`（长度 6），没有
长度 19 的 `proxy-authorization` 分支；`onHeaders` 108 行传入 `this.opts.origin !== origin` 后，
109-110 行改写 `opts.path` / `opts.origin`，`onComplete` 160 行用同一份 opts 重新 dispatch，
代理凭据随请求到达重定向目标。`v5.28.4` 用 `64e3402d`（v5.x 分支，4 文件 +191/−6，新增
`lib/core/constants.js` 与 `headerNameToString`）补上长度 19 分支与回归测试；公告只点名的
`68057466` 是 main 分支同款修改，只进 `v6.11.1`）。CWE-863（NVD Primary；GHSA API 只列 CWE-200，
OSV 列 CWE-200/285/863），CVSS 3.1 4.3 MEDIUM `AV:N/AC:L/PR:H/UI:R/S:U/C:L/I:L/A:L`（NVD Primary；
GitHub 与 NVD Secondary 都是 3.9 LOW / AC:H）。2026-10-25T00:36:51Z 写入 `data/`（1 漏洞 /
1 location / 1 review / 41 evidence / 1 status），候选 `disc2_e609b9ad4151019e790a2bea` 已改写为
`confirmed_affected`（`checked_at 2026-10-25T00:36:51Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round52_20261025T003654Z.jsonl`）。
复核者 `round52-independent-reviewer-luchitong` 全新 clone（HEAD `046bb4c6…`）自建三棵 tag 树与
自写 harness（只用 `undici.request` + 两个 loopback `node:http` 服务器）跑 15 行用例：
v5.19.0 / v5.28.3 的跨 origin 目标只收到 `proxy-authorization`（对象与扁平数组两种 header 形态都泄漏），
v5.28.4 收到 `{}`；same-origin、direct、`maxRedirections: 0` 三个对照在三个 tag 上表现一致。
复核员独立判定 GHSA `vulnerable_version_range "< 5.28.3"` 与自己的 `patched_versions ">= 5.28.4"`、
OSV/NVD 机器范围及 v5.28.3 实测矛盾，属公告 off-by-one 文本错误（不影响 v5.19.0 的包含关系），
并确认 `64e3402d` 是 `v5.28.3..v5.28.4` 之间唯一改 `RedirectHandler.js` 的提交。gate 27 个
preserved 文件 0 problems / 0 warnings / `ok: true`。复核员另指出三处保真问题（CRLF 测试文件被
文本模式归一化、`retrieved_at` 把本地时间误标为 UTC、CWE 出处不全），采集侧已重采二进制来源
（该文件现与上游 blob `8313e00c…` 逐字节一致）、改用 NVD 响应时间戳并把 CWE-200/285 记入证据，
复核员随后按更正后的来源重测并追加 Addendum：`NOTES.md` 现 20,058 B（sha256 `6178018b…`）、
`verdict.json` 现 15,388 B（`8dfe63b3…`，只改三条 caveat 文案与三条 discrepancy 状态，
`verdict` / `grade_recommendation` / `fields_verified` / `location` / `reviewed_at` 均未变）、
`preserved_sha256.txt` 重算 27 条；重跑 gate 仍 `problems: []` / `warnings: []` / `ok: true`。
CVE-2024-50602 卷宗（`runs/verification/libexpat_R_2_6_2_CVE-2024-50602/`，26 件 sha256 钉住来源、
`dossier.json` 26 条证据 / 9 个字段映射）2026-10-25T00:19:37Z 收到 round51 的
**grade A** `confirmed_affected`（libexpat `R_2_6_2` `expat/lib/xmlparse.c`：2.6.4 之前的
`XML_StopParser`（2226）只有 `XML_SUSPENDED`/`XML_FINISHED` 两个 case，未启动的 parser 落进 2240 行
`default:` 被当作暂停接受并返回 `XML_STATUS_OK`；随后的 `XML_ResumeParser`（2256）因此放行、2265 行
改回 `XML_PARSING`，`callProcessor` 成功后无条件在 2289 行调
`XmlUpdatePosition(parser->m_encoding, parser->m_positionPtr, …)`，而 `m_positionPtr` 自
`XML_GetBuffer` 的 2220 行起就是 NULL，`initUpdatePosition`（`xmltok.c:1031`）→
`normal_updatePosition` 在 `xmltok_impl.c:1781` 用 `BYTE_TYPE(enc, ptr)` 读零页；CWE-754，
NVD **只有 Secondary** 5.9 MEDIUM `AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`
（`134c704f-…`，CISA-ADP），OSV 同向量，上游 Changes 另写 `CWE-476 CWE-754`）。修复为 `51c70190`
（新增 `case XML_INITIALIZED:` → `XML_ERROR_NOT_STARTED` 与错误串，9 增 1 删）+ `5fb89e7b`
（`default:` 收窄成 `case XML_PARSING:`，其余 `assert(0)`，4 增 1 删）+ `b3836ff5`（24 行回归测试
`test_misc_resumeparser_not_crashing` / `test_misc_stopparser_rejects_unstarted_parser`）+
`ef485e96`（merge PR #915），首个 release `R_2_6_4`（tag object `2d994d11…` → `2691aff4…`，2024-11-07），
`R_2_6_3`（`88b3ed55…`）仍在受影响范围内。2026-10-25T00:20:28Z 写入 `data/`（1 漏洞 / 1 location /
1 review / 29 evidence / 1 status），两条候选 `disc2_c7e893eeab17d88e1fe6f972` 与
`disc2_c31db55b4823ecb00d28068d` 均已改写为 `confirmed_affected`（`checked_at
2026-10-25T00:19:37Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round51_20261025T002031Z.jsonl`）。
复核者 `round51-independent-reviewer-luchitong` 全新 clone（HEAD `b8fedbbf…`）与独立构建，
自写 harness 只用公开 API：2.6.2/2.6.3 在 `fill=0` 下 ASan 134、`-O2` 139，栈
`normal_updatePosition:1781 ← initUpdatePosition:1031 ← XML_ResumeParser`（2.6.2:2289 / 2.6.3:2296），
`fill=0xbe` 与对照（正常解析、只 stop、只 resume）全 exit 0，2.6.4 全 exit 0 且
`stop_error=44`（NOT_STARTED）/ `resume_error=34`（NOT_SUSPENDED）；gate 78 个 preserved 文件
0 problems / 0 warnings / `ok: true`。复核员与采集侧都写明同一条限定：崩溃受从未初始化的
`m_parsingStatus.finalBuffer` 门控（为 0 才返回 `XML_ERROR_NONE` 并走到 2289 行，非 0 则返回
`XML_ERROR_NO_ELEMENTS` 不崩），因此不主张「每次必崩」；2.6.4 修的是「未启动 parser 不能被暂停」，
没有初始化该字段。复核员另记两条非实质备注（PR 标题含反引号；NVD source 只按 UUID 记录、未独立
解析机构名），无实质分歧，未触发 `POST_REVIEW_CORRECTIONS` 条目。
CVE-2026-32778 卷宗（`runs/verification/libexpat_R_2_6_2_CVE-2026-32778/`，19 件 sha256 钉住来源、
`dossier.json` 19 条证据 / 9 个字段映射）2026-10-25T00:03:27Z 收到 round50 的
**grade A** `confirmed_affected`（libexpat `R_2_6_2` `expat/lib/xmlparse.c`：`setContext` 在 6789 行
先用 `lookup()` 把 PREFIX 挂进 `dtd->prefixes`（`table->v[i]->name = name` 在 7255），6794 行
`prefix->name = poolCopyString(&dtd->pool, prefix->name);` 在 OOM 时把 NULL 写进已入表的条目并
6796 返回 `XML_FALSE`，parser 停在 `XML_INITIALIZED`；应用清掉分配失败后重试同一 parser，
`startParsing`(1050) → `setContext` → `lookup`(7195) 调 `keyeq(name, table->v[i]->name)`（7139-7144
无 NULL 检查）读 NULL；CWE-476，NVD Primary 5.5 MEDIUM `AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`，
NVD Secondary 与 OSV 2.9 LOW `…/AC:H/PR:N/…/A:L`）。修复为 `576b61e4`（35 增 8 删，新增
`poolCopyStringNoFinish`，把名字复制提前到 `lookup` 之前）+ `d5fa769b`（27 行回归测试
`test_nsalloc_setContext_zombie`）+ `dbd511a2`（Changes）+ `6154446f`（merge PR #1163），首个
release `R_2_7_5`（`f31adfd5…`），`R_2_7_4`（`f5c2890d…`）仍是修复前最后一个 release。
2026-10-25T00:04:26Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 28 evidence / 1 status），
候选 `disc2_ba665e8bf908752125013d03` 已改写为 `confirmed_affected`（`checked_at
2026-10-25T00:04:40Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round50_20261025T000430Z.jsonl`）。
复核者 `round50-independent-reviewer-luchitong` 全新 clone（HEAD `b8fedbbf…`）与独立构建，
自写 harness 全部用例通过：2.6.2 ASan budget 3 `SEGV on unknown address 0x0`
（`keyeq:7140 ← lookup:7195 ← setContext:6789 ← startParsing:1050 ← XML_Parse:1938`）、`-O2` exit 139
（gdb 帧 `lookup(... name="xml" ...) at xmlparse.c:7195`），2.7.4 同样崩，2.7.5 在 budget 0..40 全
exit 0 且 budget 3 的 OOM 落在 `poolCopyStringNoFinish`；对照（不注入失败）两版两构建全 exit 0。
gate 23 个 preserved 文件 0 problems / 0 warnings / `ok: true`。复核员记 3 条说明性备注（NVD
`vulnStatus` 为 "Modified"、不在九字段内；测试行号差 2 行；OSV 的 PR #1159 未单独取证），
无实质分歧，未触发 `POST_REVIEW_CORRECTIONS` 条目。
CVE-2026-32777 卷宗（`runs/verification/libexpat_R_2_6_2_CVE-2026-32777/`，20 件 sha256 钉住来源、
`dossier.json` 20 条证据 / 9 个字段映射）2026-10-24T23:58:10Z 收到 round49 的
**grade A** `confirmed_affected`（libexpat `R_2_6_2` `expat/lib/xmlparse.c`：`entityValueProcessor`
只靠 `XmlPrologTok` 返回非正 token 退出，唯一推进语句是 4664 行 `start = next;`；外部实体内容里的
start tag 返回 `XML_TOK_INSTANCE_START` 且 `next == start`，于是零推进死循环；CWE-835，NVD Primary 5.5
MEDIUM `AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`，NVD Secondary 与 OSV 4.0 `…/PR:N/…/A:L`）。修复为
`55cda8c7`（10 行 guard）+ `a7805c1a`（30 行回归测试）+ `dbd511a2`（Changes）+ `6a814cae`（merge PR
#1162），首个 release `R_2_7_5`（tag object `ef8dd281…` → `f31adfd5…`），`R_2_7_4` 仍是修复前最后一个
release。2026-10-25T00:00:05Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 27 evidence / 1 status），
候选 `disc2_05ab8b8704bfc3d3ff934592` 已改写为 `confirmed_affected`（`checked_at
2026-10-25T00:00:20Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round49_20261025T000010Z.jsonl`）。
复核者自建 clone 与六个构建树，自写 harness 28 个用例全过：2.6.2 与 2.7.4 的 mode 1 以自身 `alarm(8)`
挂死 exit 142（纯 CPU 自旋，`user=3.13 sys=0.00`），2.7.5 立即返回（子解析 `XML_ERROR_SYNTAX` 2、
外层 `XML_ERROR_EXTERNAL_ENTITY_HANDLING` 21）；gate 53 个 preserved 文件 0 problems / 0 warnings。
复核员的 3 条文档级分歧已按实测裁定并落地（见 `POST_REVIEW_CORRECTIONS.md` 与
`runs/data_fixes/apply_post_review_corrections_round49_2026-10-25.py`）：PI 本身返回
`XML_TOK_XML_DECL`(12) 并前进 21 字节，零推进的 `XML_TOK_INSTANCE_START`(29) 来自其后的 `<a`；
4550 行属于 `entityValueInitProcessor` 而非 `doProlog`；`f31adfd5` 的提交标题是
“Merge pull request #1159 from libexpat/prepare-release”。
CVE-2026-32776 卷宗（`runs/verification/libexpat_R_2_6_2_CVE-2026-32776/`，25 件 sha256 钉住来源、
`dossier.json` 18 条证据 / 9 个字段映射）2026-10-24T23:48:50Z 收到 round48 的
**grade A** `confirmed_affected`（libexpat `R_2_6_2` `expat/lib/xmlparse.c`：0 字节外部参数实体在
实体声明值里被引用时，子解析器在编码探测前就调用 `storeEntityValue`，`XmlEntityValueTok` 经
`literalScanners[XML_ENTITY_VALUE_LITERAL]` 调用未初始化函数指针；CWE-476，NVD Primary 5.5 MEDIUM
`AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`，NVD Secondary 与 OSV 4.0 `…/PR:N/…/A:L`）。修复为
`5be25657`（9 行 + 19 行回归测试）+ `dbd511a2`（Changes）+ `635db9e1`（merge PR #1158），首个 release
`R_2_7_5`（tag object `ef8dd281…` → `f31adfd5…`），`R_2_7_4` 仍是修复前最后一个 release。
2026-10-24T23:48:50Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 30 evidence / 1 status），
候选 `disc2_53b5afd3497a71e30facfcaf` 已改写为 `confirmed_affected`（`checked_at
2026-10-24T23:49:00Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round48_20261024T234855Z.jsonl`）。
复核者自行 clone 与构建，自写 harness 只用公开 API：2.6.2 与 2.7.4 的 mode 1 在 ASan 下 134、
`-O2` 下 139（崩溃栈 `storeEntityValue` 6209 / 6796），2.7.5 为 0；mode 2/3/4 对照三版均符合预期；
24/24 用例 PASS，与采集侧一致；它另用 gdb 在 plain 构建看到 `0x0`、在 ASan 看到 `0xbe` 填充，
确认是非确定值的未初始化函数指针。preserved 45 项，gate `problems: []`、`warnings: []`。
CVE-2026-24515 卷宗（`runs/verification/libexpat_R_2_6_2_CVE-2026-24515/`，25 件 sha256 钉住来源、
`dossier.json` 14 条证据 / 9 个字段映射）2026-10-24T23:37:44Z 收到 round47 的
**grade A** `confirmed_affected`（libexpat `R_2_6_2` `expat/lib/xmlparse.c`：
`XML_ExternalEntityParserCreate` 复制了 unknown-encoding handler 却没有复制
`m_unknownEncodingHandlerData`，子解析器解析外部实体、遇到声明未知编码的文本声明时，
`handleUnknownEncoding`（4446）用这个 NULL 调用应用 handler；CWE-476，NVD Primary 2.5 LOW
`AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L`，NVD Secondary 与 OSV 2.9 `…/PR:N/…`）。修复为
`86fc914a`（3 行）+ `3de54af0`（Changes）+ `f14b0845`（merge PR #1131），首个 release
`R_2_7_4`（tag object `ff7046b0…` → `f5c2890d…`），`R_2_7_3` 仍是修复前最后一个 release。
2026-10-24T23:37:44Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 26 evidence / 1 status），
候选 `disc2_e08b1422a5df9ab74c159a7a` 已改写为 `confirmed_affected`（`checked_at
2026-10-24T23:38:00Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round47_20261024T233748Z.jsonl`）。
复核者自行 clone 与构建，自写 harness 只用公开 API：2.6.2/2.7.3 的 mode 1 handler 收到 NULL，
ASan SEGV（`abort_on_error=1` 时 134）、`-O2` 139；2.7.4 handler 收到非 NULL、不崩，子解析以
`XML_ERROR_UNKNOWN_ENCODING`（18）失败；mode 2/3/4 对照三版均符合预期。preserved 27 项、
`check_verdict_packet.py` 0 problems / 0 warnings。复核后更正见卷宗内
`POST_REVIEW_CORRECTIONS.md`（README 行号 1145/1146 → 1144/1145，dossier 的 1145 正确）。
CVE-2024-8176 卷宗（`runs/verification/libexpat_R_2_6_2_CVE-2024-8176/`，24 件 sha256 钉住来源、
`dossier.json` 21 条证据 / 9 个字段映射 / 6 条 limitations）2026-10-24T23:24:46Z 收到 round46 的
**grade A** `confirmed_affected`（libexpat `R_2_6_2` `expat/lib/xmlparse.c`：实体展开没有嵌套计数，
`processInternalEntity`（5817-5874）调用 `doContent`（2952）展开替换文本，替换文本里再出现实体引用
又回到 `processInternalEntity`；属性值走 `appendAttributeValue`（6150）自递归、参数实体定义走
`storeEntityValue`（6271）自递归，N 条线性链接的实体即占用 O(N) 个 C 栈帧直至栈溢出；CWE-674，
NVD 只有 secalert@redhat.com 的 Secondary 3.1 7.5）。修复为 PR #973 合并 `99529768`（六条代码提交 +
Changes + merge），2.7.0 新增 `processEntity`（5972）并改造本已存在的 `internalEntityProcessor`
（2.6.2 的 470/5865/5881 → 2.7.0 6034），三路径改为 `for (;;)` 迭代（6206/6413）；`R_2_6_4` 不含修复、
`R_2_7_0` 含。2026-10-24T23:27:57Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 30 evidence / 1 status），
候选 `disc2_c3dc65c90ed8e1207d042404` 已改写为 `confirmed_affected`
（`checked_at 2026-10-24T23:28:00Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round46_20261024T232800Z.jsonl`）。
复核者自行全量 clone 并按 tag 建两棵源码树，自写公开 API harness 跑三种 issue #893 载荷形态（字符数据
n=20000、属性值 n=100000、参数实体 n=100000）与一个**字节数相同但不嵌套**的对照：2.6.2 ASan 三例分别
在 `processInternalEntity:5858` ↔ `doContent:2952`、`appendAttributeValue:6150`、
`storeEntityValue:6271` 栈溢出，2.7.0 三例全过；2.6.2 `-O2` 三例 SIGSEGV；对照 n=20000 两版均过，
ASan 下 8000 通过 / 9000 崩溃，证明触发因素是嵌套深度而非实体数量。preserved 671 项、
`check_verdict_packet.py` 0 problems / 0 warnings。复核后更正见 `POST_REVIEW_CORRECTIONS.md`
（`internalEntityProcessor` 措辞；卷宗 `field_evidence` 补 `severity` 键并在
`runs/data_fixes/add_severity_evidence_round46_2026-10-25.py` 守卫下补 2 条证据行，6284→6286）。
CVE-2026-27205 卷宗（`runs/verification/flask_2.3.1_CVE-2026-27205/`，25 件来源其中 24 件 sha256 钉住、
`dossier.json` 24 条证据 / 18 个字段映射 / 9 条 limitations）2026-10-24T22:11:30Z 收到 round43 的
**grade A** `confirmed_affected`（flask 2.3.1 `src/flask/sessions.py`：`Vary: Cookie` 由
`SessionInterface.save_session` 写出，门控变量 `SecureCookieSession.accessed` 只在
`__getitem__`（71-73）、`get`（77）、`setdefault` 与 `on_update`（82-87）四处置位；`key in session`、
`len(session)`、迭代与 `.keys()/.values()/.items()` 继承自 `CallbackDict` 且未覆写，读 session 不置位；
2.3.1 上 `flask.session` 与模板 `session` 解析到同一对象，模板里的 `in` 同样盲。`save_session`
（322-350）在 `accessed` 为假时跳过 347-349 的 `Vary` 门，未忽略 `Set-Cookie` 的共享缓存即可把
一个用户的响应发给另一个用户。另一个快照特有表现：334 行 `if not session: return True` 早于
347-349 的门，故空 session 上即使 `.get()` 也无 `Vary`——2.3.3 / 3.1.2 已把门放在 return 之前，
复核者判定这是**同一缺失 `Vary` 结果**而非 CVE 定义根因，修复 diff 也不改这个顺序，verdict 不依赖它。
修复 `089cb86d` 是 merge commit（父 `27be9338` + `c17f3793`，merge tree 等于 fork 分支树，
`commit/<sha>.patch` 返回 `From c17f3793`），只出现在 tag 3.1.3 祖先链上，2.3.1/2.3.3/3.1.2 均无），
2026-10-24T22:16:52Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 58 evidence / 1 status），
两条候选 `disc2_e6455792530ef4ded286ccbd` 与 `adv3_620d1669d829c92b` 均已改写为 `confirmed_affected`
（backup 见 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round43_20261024T221722Z.jsonl`）。
复核者自建四个 venv（PyPI 真包 2.3.1/2.3.3/3.1.2/3.1.3）跑了 64 行红/绿矩阵（8 条访问路径 × 4 版本 ×
2 模式，0 处不符），并用 nginx 1.24.0 `proxy_cache` 演示串号：2.3.1 上「登录后 → 匿名请求」为
MISS→HIT，匿名者拿到 `result=yes` / `session_len=1` 且两次响应都无 `Vary`；3.1.3 同序列为
MISS→MISS 且带 `Vary: Cookie`。preserved 2925 项、`check_verdict_packet.py` 0 problems / 0 warnings。
复核后更正见 `POST_REVIEW_CORRECTIONS.md`（OSV CVE 的 ECOSYSTEM 版本上界由误写的 2.2.5 改为 2.2.0；
GHSA/PYSEC 的「逐版枚举到 3.1.2」不再压缩成三个版本）。
CVE-2024-49767 卷宗（`runs/verification/werkzeug_3.0.2_CVE-2024-49767/`，25 件 sha256 钉住产物其中
20 件网络、5 件本地 blobless 克隆派生、`dossier.json` 25 条证据 / 18 个字段映射 / 10 条 limitations）
2026-10-24T22:29:59Z 收到 round44 的 **grade A** `confirmed_affected`（werkzeug 3.0.2
`src/werkzeug/formparser.py`：`MultiPartParser.parse` 在 353-392 的 multipart 循环里按 `buffer_size`
（默认 64 KiB）分块读入，`MultipartDecoder.receive_data`（`sansio/multipart.py:136-145`）只比较
`len(buffer) + len(data)` 与 `max_form_memory_size`，即**单块**；解析器每块都抽干 decoder，buffer 恒为 0，
非文件字段的每个 `Data` 事件在 381-382 直接 append 进 list、到 384-386 才整段 join+decode，
于是「字段远大于限制、但每块小于限制」的请求逐块放行、内存无界。修复 `50cfeebc` 是 merge commit
（第二父 `8760275a`「apply max_form_memory_size another level up in the parser」，merge tree 等于第二父树、
`commit/<sha>.patch` 返回 `From 8760275a`），在 355/374/379/383-391 增加 `field_size` 按字段累计并抛
`RequestEntityTooLarge`；只在 3.0.6 祖先链上，3.0.2 与 3.0.5 均无，`sansio/multipart.py` 在 3.0.2 与 3.0.5
是同一 blob。引入点是 GHSA 引用的 `cbb446fd`（sans-io 重构），它是 OSV CVE 所写 `introduced 22bfb446`
（「Release 2.0.0rc1」）的祖先、无 0.x/1.x tag 包含，下界因此坐实）。2026-10-24T22:31:22Z 写入 `data/`
（1 漏洞 / 1 location / 1 review / 59 evidence / 1 status），两条候选 `disc2_072f55e1dd1d4707db4e1fce`
与 `adv3_5b31cc3f2c071fe8` 均已改写为 `confirmed_affected`（backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round44_20261024T223140Z.jsonl`）。
复核者自建两个 venv（PyPI 真包 3.0.2 / 3.0.6，装后 `formparser.py` / `sansio/multipart.py` 的 sha256
与 pin 一致）：3 MiB 非文件字段 + 1 MiB 限制 + 默认 64 KiB 分块下，3.0.2 成功返回 3145728 字节、
峰值 RSS 41416 KiB（解析前 34760），3.0.6 在 `formparser.py:389` 抛错；插桩显示 3.0.2 的 49 次非空
`receive_data` 中 buffer 从未累积、`buffer+chunk` 最大 65536 字节，1 MiB 限制从未触发。负控制
（`buffer_size` 2 MiB > 限制；流无视 `read(n)` 一次返回 3 MiB）两版都在 `receive_data` 抛错，
`max_form_memory_size=None` 两版都成功。preserved 70 项、`check_verdict_packet.py` 0 problems / 0 warnings。
复核还发现**上游 3.0.6 新增的回归测试不具判别力**：`max_form_memory_size=10, buffer_size=5` 在 3.0.2 上
也抛错（`sansio/multipart.py:143`），3.0.6 也停在旧 `receive_data:145` 而没走到新检查——已在卷宗
evidence / limitations / open questions / README 更正并记入 `POST_REVIEW_CORRECTIONS.md`（另有 OSV/NVD
重取字节差异两条，语义相等、仅键序与 `/timestamp` 不同，不采纳）。
CVE-2021-3603 卷宗（`runs/verification/phpmailer_6.1.5_CVE-2021-3603/`，32 个来源文件其中 31 件 sha256
钉住 = 26 网络 + 5 本地 blobless 克隆派生，`dossier.json` 47,221 字节 / 30 条证据 / 18 个字段映射 /
14 条 limitations / 5 个 open questions）2026-10-24T22:55:55Z 收到 round45 的 **grade A**
`confirmed_affected`（PHPMailer 6.1.5 `src/PHPMailer.php`：`validateAddress($address,
$patternselect = null)`（1304）在 selector 为 null 时取 `static::$validator`（1306-1307），6.1.5 的默认值
是 `'php'`（576），随后 1309-1311 `if (is_callable($patternselect)) { return
$patternselect($address); }` 直接调用同名全局函数并把返回值当校验结论；内建 switch 的
`case 'php': default: filter_var(...)`（1358-1360）只有在 callable 判定失败时才到达。可达路径：addAddress
999 → addOrEnqueueAnAddress 1063 → addAnAddress 1118 → 1134、setFrom 1235 → 1243、parseAddresses 1178 →
1185/1202/1211、preSend 1453 → 1500、mailSend 1762 → 1781/1784。分支由 `77c0bc8d`（2016-05-09）引入，
首个带分支的发行版是 v5.2.15（`class.phpmailer.php:1056-1061`）与 v6.0.0rc2（1033-1038），但两者的
`$validator` 默认值仍是 `'auto'`，**默认配置劫持**要到 v6.0.0rc3（492 行默认 `'php'`、1136 行分支）才成立，
即代码级 6.0.0rc3 .. 6.4.1；更早版本需要应用自己把 `$validator` 设成 `'php'`。修复 `45f3c18d`（2021-06-15
「Deny string-based callables altogether」，父 `6334bab2` 已带未发布的折中守卫，只拒 `php/pcre/pcre8/html5`）
在 6.5.0 的 1341 行加 `&& !is_string($patternselect)`、1342 改用 `call_user_func`；v6.4.1 无此修复，
5.2 线（到 v5.2.28）也无。2026-10-24T23:01:01Z 写入 `data/`（1 漏洞 / 1 location / 1 review /
66 evidence / 1 status，review `rev_CVE_2021_3603_r1`），两条候选 `disc2_fda17748360754567b087fc3` 与
`adv3_219fba69f30a5c11` 均已改写为 `confirmed_affected`（`checked_at 2026-10-25T07:10:00Z`，backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round45_20261024T230138Z.jsonl`）。
复核者自写 `harness.php`（不用采集方的 probe），对 v6.1.5（`9e8ad5d8…`）与 v6.5.0（`ce454285…`）的
自取文件跑 injected/plain 两种模式：6.1.5 上 `validateAddress('not-an-address')` 返回 true 并调用注入的
`php()`，`addAddress('bad@domain')` 收下 `bad@domain`，`setFrom('bad@domain')` 把 From 设为
`bad@domain`；6.5.0 三项全为 false 且注入调用为 0；marker 在 6.1.5 记到 6 次调用、6.5.0 不存在；
闭包在两版都仍被调用；plain 负控制（不定义任何全局同名函数）两版九项探针结果一致、零调用；
`compare_runs.py` 18/18 断言通过（PHP 8.4.23 CLI、stderr 为空）。packet checker 0 problems / 0 warnings、
preserved 46 项。复核后更正（`POST_REVIEW_CORRECTIONS.md`，3 条全部采纳）：(a) README 原说 merge
`86d2b069`「两个父都不含该分支」不准确——第二父 `444a355b` 的 `class.phpmailer.php` 确有该分支，只有
`src/PHPMailer.php` 这个路径在 master 侧不存在；已改为采集脚本对两个父逐文件实测并写入
`git_introduced.txt`；(b) 补钉 v6.0.0rc3 并把默认值边界写进 `affected_range` 注记、range_expression 与
limitation 5；(c) OSV CVE / NVD / GHSA 渲染页字节漂移记为 limitation 14（字段值经复核者逐项重核均未变）。
九个 canonical 字段的值与 location（1309-1311）一个未改，grade A 仍归因于复核者自己的执行。
CVE-2025-49007 卷宗（`runs/verification/rack_v3.1.13_CVE-2025-49007/`，40 件 sha256 钉住产物、
`dossier.json` 33 条证据 / 18 个字段映射 / 10 条 limitations）2026-10-24T21:16:00Z 收到 round37 的
**grade A** `confirmed_affected`（3.1.13 `Rack::Multipart::Parser#handle_mime_head` 在
`lib/rack/multipart/parser.rb:310` 把整段 MIME 头块交给 36 行那条**未锚定**的
`/Content-Disposition:(.*)(?=#{EOL}(\S|\z))/ni`；`CONTENT_DISPOSITION_MAX_BYTES = 1536` 的检查在
311 行、即匹配之后，头块本身只以空行为界（`@head_regex` 214 行），`read_data` 258-262 每次
最多追加 `BUFSIZE = 1_048_576` 字节；入口 `Rack::Request#POST` 503 → `form_data?` 470/474 →
`parse_multipart` 527 → `Rack::Multipart.parse_multipart`（`multipart.rb:48/62`）。触发条件要准：
**单个**字面量 + 超长值只呈线性，二次开销需要在一条头行里堆许多字面量起点、并让行尾 lookahead
失败，例如折叠续行以空格开头），2026-10-24T21:18:16Z 写入 `data/`（1 漏洞 / 1 location / 1 review /
67 evidence / 1 status），候选 `disc2_dbd720d0f16c279b811322c4` 已改写为 `confirmed_affected`
（backup 见 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round37_20261024T211831Z.jsonl`）。
复核者自行重抓上游（blobless clone + gem + tarball，587 个 preserved 文件）并在真实 rack 3.1.13/3.1.16
上跑了红/绿：同一批 body，3.1.13 中位解析时间 1.336 ms（2.5 KB）→ 1439 ms（80 KB），log-log 斜率
≈2.01；3.1.16 在 80 KB 为 1.305 ms（斜率 ≈0.99），另有 `Rack::Request#POST` 入口探针与普通 multipart
功能对照。修复为 3.1 线 `aed514df`（首个发行 3.1.16）与 3.2 线 `4795831a`（首个发行 3.2.0，不存在
受影响的 3.2.x），两者都改成 `^` 锚定 + `FWS`/`HEADER_VALUE`，且都不是 v3.1.13/14/15 的祖先。
**复核后更正**：复核者指出卷宗机制表述过宽（原写「任意超长头行即超线性」）、`affected_ranges`
第二条把 3.2 线误写成受影响区间、limitation 3 把 body 内 MIME 头与 HTTP 请求头混为一谈，另澄清
`published_at` 是 GHSA 时间（OSV CVE 2025-06-04T22:42:52Z、NVD 2025-06-04T23:15:21Z）并修正
`form_data?` 行号；采集方已在 `dossier.json` 重建时全部更正并写 `POST_REVIEW_CORRECTIONS.md`，
verdict / grade / 九字段 / location 未改动。公开记录差异照实保留：NVD CVSS 3.1 5.3 MEDIUM 为
Primary、GHSA/rubysec 4.0 6.6 为 Secondary，CWE-1333（NVD Primary）与 CWE-770（GitHub）并列；
`CHANGELOG.md` 在 v3.1.16 tag 上仍无 `[3.1.16]` 小节。
CVE-2025-61772 卷宗（`runs/verification/rack_v3.1.13_CVE-2025-61772/`，23 件 sha256 钉住产物、
`dossier.json` 23 条证据 / 18 个字段映射 / 6 条 limitations）2026-10-24T21:29:10Z 收到 round38 的
**grade A** `confirmed_affected`（3.1.13 `Rack::Multipart::Parser#handle_mime_head` 在
`lib/rack/multipart/parser.rb:306` 用 `@sbuf.scan_until(@head_regex)`（307；`@head_regex` 在 214）
等 part 头终止空行；终止符没到时 406-408 的 `else / :want_read` **没有字节上限**，`read_data`
（258-262，`BUFSIZE = 1_048_576`，40 行）持续 `@sbuf.concat`，于是头块永不终止的 part 会把整个
请求体驻留内存。**没有放大**：内存随客户端实际发送字节线性增长，边界是 body 上限与并发；入口
`Rack::Request#POST` 503 → `form_data?` 470/474 → `multipart.rb` 的
`Rack::Multipart.parse_multipart` 48 → `Parser.parse` 62 → `parser.rb` 217。
修复为 3.1 线 `e08f78c6`（首个发行 3.1.17）加 `BOUNDARY_START_LIMIT = 16 KiB` 与
`MIME_HEADER_BYTESIZE_LIMIT = 64 KiB` 并 raise `multipart mime part header too large`；比较对象是
整个 `@sbuf`，实际阈值 `max(64 KiB, BUFSIZE)`。`BUFFERED_UPLOAD_BYTESIZE_LIMIT`（CVE-2025-61771）
来自后续提交 `f224f93b`，未记到本 CVE 名下。2026-10-24T21:30:48Z 写入 `data/`（1 漏洞 / 1 location /
1 review / 40 evidence / 1 status），候选 `disc2_d52e1cedda7ae490c33181a7` 已改写为
`confirmed_affected`（backup `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round38_20261024T213051Z.jsonl`）。
复核者用官方 gem 的 rack 3.1.13/3.1.16/3.1.17、Ruby 3.2.3、30 次独立进程实验测 RSS/VmHWM：
1/4/16/64 MiB body 时 3.1.13 的 `@sbuf.string.bytesize` 为 1,048,630 / 4,194,358 / 16,777,270 /
67,108,918，64 MiB 时 VmHWM 增量 66,560–66,688 kB；3.1.17 在 `@sbuf = 1,048,576` 即 raise，16 KiB
bufsize 复测在 81,920 抛错。**复核后更正**（`POST_REVIEW_CORRECTIONS.md`）：OSV×2 与 NVD 三个 JSON
重抓后字节日志不同（规范化后只差键序与 `timestamp`），其余 10 件逐字节一致；卷宗 trace 把
`request.rb:527` 误称 `parse_multipart`（实为 `Rack::Request#POST` 内的调用）、把 `multipart.rb:62`
误称 `Parser#parse`（实为类方法 `Parser.parse`，实例方法在 `parser.rb:217`）；NVD 另有 `ssvcV203`
对象（非 CVSS）。verdict / grade / 九字段 / location 未改动；另因校验脚本要求，复核者已在 verdict
顶层补 `vulnerable_commit` 并重算 preserved_sha256（284 文件）。
CVE-2025-61770 卷宗（`runs/verification/rack_v3.1.13_CVE-2025-61770/`，23 件 sha256 钉住产物、
`dossier.json` 23 条证据 / 18 个字段映射 / 7 条 limitations）2026-10-24T21:36:32Z 收到 round39 的
**grade A** `confirmed_affected`（3.1.13 `Rack::Multipart::Parser#handle_fast_forward`
`lib/rack/multipart/parser.rb:271-292` 在等第一个 boundary 时，`consume_boundary` 失败分支
287-289 只 `return :want_read`，`read_data`（258-262，`BUFSIZE = 1_048_576`）持续
`@sbuf.concat`，而 `consume_boundary` 的 `@sbuf.terminate`（438）只移动扫描指针不清空字符串，
于是 boundary 之前的全部字节常驻内存；入口 `Rack::Request#POST` 503 → `form_data?` 470/474 →
`Rack::Multipart.parse_multipart` 48 → `Parser.parse` 62 → `parser.rb` 217）。
修复为 3.1 线 `e08f78c6`（首个发行 3.1.17）加 `BOUNDARY_START_LIMIT = 16 KiB` 并 raise
`multipart boundary not found within limit`；3.2 线为 `589127f4`（v3.2.2）、2.2 线为
`d869fed6`（v2.2.19）。2026-10-24T21:39:56Z 写入 `data/`（1 漏洞 / 1 location / 1 review /
40 evidence / 1 status），候选 `disc2_ef186d6243339e8a6f811575` 已改写为 `confirmed_affected`
（backup `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round39_20261024T214000Z.jsonl`）。
复核者用官方 gem 的 rack 3.1.13/3.1.17、Ruby 3.2.3 实测（安装后 parser.rb 内容 sha256 与上游
tag 文件一致）：3.1.13 上 64 MiB preamble 后 `VmRSS` 91,432 kB、对照（4 KiB）25,856 kB，
即 +65,576 kB ≈ 64 MiB 原样驻留，`VmHWM` 141,404 kB，8/16/32 MiB 线性且都能正常解析；
3.1.17 上 1/8/32/64 MiB 均在第 1 次读（1,048,576 B）后抛
`Rack::Multipart::BoundaryTooLongError`，`VmHWM` 27.4–27.8 MB。自定义 `BUFSIZE=8192` 时
3.1.17 在累计 24,576 B（第 3 次读）才抛、8 KiB preamble 正常解析，3.1.13 同样缓冲完整 65,611 B。
**复核后更正**（`POST_REVIEW_CORRECTIONS.md`，已重建 `dossier.json` 并同步 README）：
`40e1e6cc…` 是**文件内容 sha256** 而非 git blob id（三个 tag 的 blob 为 `3960b371…`，
3.1.16 为 `c78f0e39…`，3.1.17 为 `81c91ad6…`）；阈值不是 `max(16 KiB, BUFSIZE)`，而是
「大于 16 KiB 的第一个 BUFSIZE 整数倍」；「无放大」需限定为**驻留字节**无放大，实测峰值
`VmHWM` 可达 payload 约 1.6–2 倍。复核员另用 `git grep` + `git log -S` 覆盖全部 v3.1.x，
确认 3.1.0–3.1.16 均无 `BOUNDARY_START_LIMIT`、引入者确为 `e08f78c6`，补上了采集方
3.1.1–3.1.12 的空档。verdict / grade / 九字段 / location 未改动；因校验脚本要求，
复核者把 `fields_verified` 改为九个布尔 `true`、实际值移入顶层 `field_values`，
并重算 `preserved_sha256.txt`（32 文件，`sha256sum -c` 全绿）。
CVE-2025-61771 卷宗（`runs/verification/rack_v3.1.13_CVE-2025-61771/`，23 件 sha256 钉住产物、
`dossier.json` 23 条证据 / 18 个字段映射 / 8 条 limitations）2026-10-24T21:41:12Z 收到 round40 的
**grade A** `confirmed_affected`（3.1.13 `Rack::Multipart::Parser` 对**没有 filename** 的 part 用
`BufferPart`（`lib/rack/multipart/parser.rb:131-134`，`file?; false`），`Collector#on_mime_head`
（153）为它分配 `body = String.new`（160），`Collector#on_mime_body`（169-171）用
`@mime_parts[mime_index].body << content`（170）把每个块追加进去；`check_part_limits`
（178-195）只限打开文件数（182-187）与 part 数（189-194），**从不算字节**，所以任意多个非文件
字段都常驻内存；入口 `Rack::Request#POST` 503 → `Rack::Multipart.parse_multipart`
（`multipart.rb` 48/62）→ `Parser#parse` → 217 → handle_mime_head / handle_mime_body）。
修复为 3.1 线 `f224f93b`（首发 3.1.17）加 `BUFFERED_UPLOAD_BYTESIZE_LIMIT`（16 MiB，
`RACK_MULTIPART_BUFFERED_UPLOAD_BYTESIZE_LIMIT` 可覆盖）、`@retained_size` / `@body_retained`
与 `update_retained_size`（475-480），超限 raise `Error, "multipart data over retained size limit"`
（`Error` 是 `BoundaryTooLongError` 的别名，实测类名为 `Rack::Multipart::BoundaryTooLongError`）；
3.2 线 `3beacfcd`（3.2.2）、2.2 线 `c370dcd9`（2.2.19）。2026-10-24T21:41:44Z 写入 `data/`
（1 漏洞 / 1 location / 1 review / 40 evidence / 1 status），候选
`disc2_1910309112115463c3ca0169` 已改写为 `confirmed_affected`（backup
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round40_20261024T214207Z.jsonl`）。
复核者用 gem 3.1.13/3.1.16/3.1.17 + Ruby 3.2.3，每个数据点独立进程：3.1.13 上 1/4/16/64 MiB
单字段全部解析成功，`params` 值 `bytesize` = 1,048,576 / 4,194,304 / 16,777,216 / 67,108,864，
64 MiB 时 GC 后 RSS 增量 **+67,416 KiB ≈ 1.03× payload**；3.1.17 上 16/64 MiB 均抛错，
`RACK_MULTIPART_BUFFERED_UPLOAD_BYTESIZE_LIMIT=4096` 与 `=2097152` 都触发（同一变量在 3.1.13
上无效，作反证）；带 `filename` 的 64 MiB 对照落 Tempfile、GC 后 RSS 仅 +约 2 MiB；经
`Rack::Request#POST` 复现同一结果；3.1.16 仍无上限。复核员独立裁定 `f224f93b` 的 parent 恰为
`e08f78c6`，公开记录（GHSA/OSV/NVD/rubysec）引用的 `e08f78c6`/`589127f4`/`d869fed6` 是三个
retained-size 提交的 parent，属**公开记录把两段改动记混**，`fix_commit` 记 `f224f93b` 成立。
**复核后更正**（`POST_REVIEW_CORRECTIONS.md`）：`handle_mime_body` 交给 collector 的行号是
**414/422**（原写 413/421 是 0-based 下标），已改 `build_dossier_61771.py` 与 5 条已入库
evidence 行（`runs/data_fixes/fix_61771_line_offbyone_2026-10-25.py`，backup
`runs/data_fixes/evidence_before_61771_line_offbyone_20261024T214244Z.jsonl`）；异常类名与
`location`/`critical_operation` 行号差异、3.1.16 正则归属 CVE-2025-49007（引用 49007 卷宗，
未独立归因）、「与 round39 15 件逐字节相同」在隔离下不可复核（复核员改为自抓比对 sha256）
均已记录。verdict / grade / 九字段 / location 未改动。
**已入库**：同一快照的第五条卷宗 CVE-2025-61919（round41，
`runs/verification/rack_v3.1.13_CVE-2025-61919/`，19 件产物 / 19 evidence / 18 字段 /
7 limitations）2026-10-24T21:50:49Z 收到 `round41-independent-reviewer` 的 **grade A**
`confirmed_affected`（`reproduction_reference` = `reproduction/logs/matrix_summary.jsonl`，
全部数据由复核者在本机独立执行产生）。主张是 `Rack::Request#POST` 531 行对 url-encoded body
无参 `read`（`IO#read(nil)` 读尽），且 v3.1.13 的 `QueryParser` 连 `BYTESIZE_LIMIT` /
`PARAMS_LIMIT` 都没有；修复为 `cbd541e8`（3.1.18）把读改成
`read(query_parser.bytesize_limit + 2) || ''`（默认 4 MiB），3.2 线 `e179614c`（3.2.3）、
2.2 线 `4e2c9039`（2.2.20）。复核者用真 gem 3.1.13/3.1.17/3.1.18 实测：3.1.13 的
1/8/32/64 MiB body 全部读入（`read_calls=[null]`），VmRSS 增量
+1024/8192/32896/65536 KiB（线性、无放大）；3.1.18 在 4,194,306 字节处截断并抛
`Rack::QueryParser::QueryLimitError`；3.1.17 是中间态（8 MiB 全读入后才触发 parser 限额）；
同 32 MiB 走 `text/plain` 增长 0 KiB、裸 `IO#read(nil)` 增长 32,768 KiB（对照成立）。
2026-10-24T21:53:22Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 41 evidence / 1 status），
候选 `disc2_e4a6cf530641b47a3b064d73` 已改写为 `confirmed_affected`（backup
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round41_20261024T215412Z.jsonl`）。
**复核后更正**（`POST_REVIEW_CORRECTIONS.md`）：`entry_point.line` 原写 `503-542`，实为
**`503-551`**（`def POST` 到 `end`），已改 builder + `dossier.json` 并守卫式改写已入库 location 行
（`runs/data_fixes/fix_61919_lines_2026-10-25.py`，backup
`runs/data_fixes/locations_before_61919_line_fix_20261024T215358Z.jsonl`）；3.1.18
`check_query_string` 的检查实为 **222-223**（原写 221-223，221 是 0-based 下标），该数字只在
dossier 文本里，已随之更正。复核者另裁定：3.1.13 上第二处无界（`QueryParser` 解析本身）属
**CVE-2025-46727**（3.1.14 修），不并入本 CVE；`fixed_releases` 中只有 3.1.18 对本快照有操作意义；
单一 CWE-400 正确。verdict / grade / 九字段 / `critical_operation.line`（531-531）未改动。

**已入库**：同一快照的第六条卷宗 CVE-2025-61780（round42，
`runs/verification/rack_v3.1.13_CVE-2025-61780/`，23 件产物 / 23 evidence / 18 字段 /
7 limitations / 5 open questions）2026-10-24T21:55:41Z 收到 `round42-independent-reviewer` 的
**grade A** `confirmed_affected`（`reproduction_reference` 含脚本、命令、断言与结果文件）。主张是
`Rack::Sendfile` 把客户端请求头当代理配置：`variation`（148-152）在未配置 variation 时回退到
`env['HTTP_X_SENDFILE_TYPE']`（151），`map_accel_path`（154-165）在应用层无 mappings 时回退到
`env['HTTP_X_ACCEL_MAPPING']`（157），出口是 123/134 两处 `headers[type.downcase] = ...`；
`Rack::Files` 的响应体有 `alias :to_path :path`（files.rb:185），前提由内置组件满足。修复为 3.1 线
`7e69f65e`（首发 3.1.18）：`variation` 只保留 `@variation || env['sendfile.type']`，新增
`x_accel_mapping`（仅在显式配置 x-accel-redirect 且无 app mappings 时读头），并把两处映射正则
`^` 改成 `\A`；3.2 线 `57277b77`（3.2.3）、2.2 线 `fba2c8bc`（2.2.20）。代码覆盖：`sendfile.rb` 在
3.1.13 / 3.1.17 / 3.2.2 三者字节相同（`395efb8b…`），3.1.18 / 3.2.3 字节相同（`b0b8a22e…`），
v3.1.0 已有两处回退；复核员另补测 3.1.14/3.1.15/3.1.16 仍为 `395efb8b…`。公开记录**没有**归属
混淆（三个提交即三个分支的真实修复），但时间顺序与 61919 相反：CVE（16:53:57Z）与 NVD
（17:15:39Z）都早于 GHSA（17:31:31Z）。复核员用真 gem 3.1.13/3.1.18 + `Rack::MockRequest` 驱动
`Rack::Sendfile` 包 `Rack::Files`，23/23 断言：3.1.13 裸中间件 + 客户端 `x-sendfile-type:
x-accel-redirect` 与 `x-accel-mapping: <dir>/=/attacker/path/` 产出
`x-accel-redirect: /attacker/path/secret.txt`（CL 0、空 body），`x-sendfile` 分支回显绝对路径，
换行路径被 `^` 锚点匹配；3.1.18 对同样请求不发任何 sendfile 头，显式配置 x-accel-redirect 时仍按
客户端 mapping 映射（修复的有意保留）。2026-10-24T21:56:56Z 写入 `data/`（1 漏洞 / 1 location /
1 review / 42 evidence / 1 status），候选 `disc2_913c1074780d784476386002` 已改写为
`confirmed_affected`（backup
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round42_20261024T215742Z.jsonl`）。
**复核后更正**（`POST_REVIEW_CORRECTIONS.md`）：README 改动行数 50/70 → **67（+47/−20）/ 47（+37/−10）**；
`fix_commits[].commit_date` 原用 +13:00 本地日期，改 **UTC**（`7e69f65e`/`fba2c8bc` → `2025-10-09`，
`57277b77` 保持 `2025-10-10`），builder + dossier 重建 + `data/vulnerabilities.jsonl` 行守卫式改写
（`runs/data_fixes/fix_61780_commit_dates_2026-10-25.py`，backup
`runs/data_fixes/vulnerabilities_before_61780_commit_dates_20261024T215725Z.jsonl`）；README 的
`sources/` 表述改为「24 个文件，其中 23 件钉住」。verdict / grade / 九字段 / 行号未改动。

CVE-2026-15830 卷宗（`runs/verification/django_CVE-2026-15830_4213/`，51 件 sha256 钉住产物、
`dossier.json` 51 条证据 / 18 个字段映射 / 11 条 limitations）2026-10-24T20:55:51Z 收到 round36 的
**grade B** `confirmed_affected`（4.2.13 `django/contrib/gis/geos/prototypes/io.py` 的
`_WKTReader.read`（156）与 `_WKBReader.read`（167）把 WKT/WKB/HEXEWKB 原样交给 GEOS，无任何深度或
数量检查；GEOS 3.15.0 之前每层 `GEOMETRYCOLLECTION` 递归一次且不设上限，深层嵌套耗尽栈后进程
SIGSEGV。上游 libgeos `8b8b3da7` 加入 `MAX_PARSE_DEPTH = 100`；Django 侧两阶段修复：
5.2.17/6.0.8/6.1（`ba80833f`/`6af5da31`/`9e4a3f18`，main `d2e59b77`）加
`MAX_GEOM_COLLECTIONS = 198` 的前置限流，5.2.18/6.0.9/6.1.2（`1eafa1a8`/`4353dfb5`/`75d401a1`，
main `62ef9d40`）改为结构化 `_WKBFrame` 栈式遍历以堵住「非法字节序 / 递归 MULTIPOINT / 大端 ISO
HEXWKB」绕过；4.2 线无任何 backport，4.2.13 与 4.2.30 的 `io.py`/`geometry.py`/`forms/fields.py`
逐字节相同），2026-10-24T20:58:46Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 84 evidence /
1 status），候选 `disc2_956f6f00002b68166b526c02` 已改写为 `confirmed_affected`（backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round36_20261024T205934Z.jsonl`）。
本轮**没有执行阶段**：本机无 Django / libgeos_c / GDAL，红/绿探针未跑，九字段全部静态核实后按流水线
规则停在 B；证据是 4.2.13/4.2.30 整文件字节相同、逐 tag grep（只有 5.2.17 起才有
`MAX_GEOM_COLLECTIONS`）、八个修复提交对 4.2.13/4.2.30 的祖先关系全为 False，以及 GEOS 上游补丁的
`MAX_PARSE_DEPTH` 插入点。复核者另发现 6.1 线公告写的 `6.1a1 → 6.1.1` 偏晚（`9e4a3f18` 已是 6.1
终版 tag 的祖先）。公开记录自相矛盾照实保留：GHSA/PYSEC/Bitnami/NVD CPE 说 5.2.17+6.0.8，CVE 记录
重写区间与 NVD 新描述说 5.2.18+6.0.9；严重性 Django "moderate"、GHSA MODERATE、Bitnami Medium、
NVD 5.3（3.1）/6.9（4.0）均 Secondary。**复核后更正**：复核者指出卷宗把 4.2 EOL 写成 2025-04 是错的
（应为 2026-04-07 扩展支持结束，4.2.30 同日发布为末版），另有两处小误（证据注记 0-based 行号、
`affected_range` 起点）；采集方已在 `dossier.json` 重建时更正并写 `POST_REVIEW_CORRECTIONS.md`，
同时把第一阶段四个提交的 `fix_commits[].fix_status` 由 `complete` 改为 `partial`（后备脚本
`runs/data_fixes/fix_15830_fix_status_2026-10-25.py`，backup
`runs/data_fixes/vulnerabilities_before_15830_fix_status_20261024T205924Z.jsonl`）。
CVE-2026-53877 卷宗（`runs/verification/django_CVE-2026-53877_4213/`，27 件 sha256 钉住产物、
`dossier.json` 27 条证据 / 18 个字段映射 / 10 条 limitations）2026-10-24T20:45:29Z 收到 round35 的
**grade B** `confirmed_affected`（4.2.13 `GDALRaster.__init__` 的 bytes 分支在 `raster/source.py:106`
把 `sys.getsizeof(ds_input)` 当作 vsimem 缓冲区长度传给 `create_vsi_file_from_mem_buffer`，多算
`PyBytesObject` 头的约 32 字节，读 `vsi_buffer`（244-258，`string_at(dat, out_length.value)`）时越过
缓冲区；5.2.16/6.0.7 改为 `len(ds_input)` 并删掉 `import sys`），2026-10-24T20:47:29Z 写入 `data/`
（1 漏洞 / 1 location / 1 review / 69 evidence / 1 status），候选 `disc2_129f28a7857053e311c7d94d`
已改写为 `confirmed_affected`（backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round35_20261024T204741Z.jsonl`）。
本轮**没有执行阶段**：reviewer 机器同样无 GDAL/GEOS/Django，九字段全部静态核实后按流水线规则停在 B；
其独立证据是 4.2.13 与 5.2.15 `source.py` 整文件逐字节相同（sha256 `366b028d…`，并用 PyPI sdist 复核）、
四个修复补丁与祖先关系，以及本地 CPython 测得的 `getsizeof(bytes)` 多 33 字节、
`create_string_buffer` 多 1 字节（合计越界 32 字节，与 release notes 一致）。修复为 main `6ca2bbe2ef`、
backport `6c66eb8c`（5.2.16）/`38dfbd27`（6.0.7），6.1 正式版已含 `a46b417d`；4.2 无 backport。
保留口径：越界仅在应用层读取 `vsi_buffer` 时发生（4.2.13 库内无调用者），泄露还是崩溃取决于 allocator，
均未复现；严重性 Django 说 low、GHSA MODERATE、NVD 4.8/6.3 MEDIUM（均 Secondary）。
CVE-2026-15307 卷宗（`runs/verification/django_CVE-2026-15307_4213/`，32 件 sha256 钉住产物、
`dossier.json` 32 条证据 / 18 个字段映射 / 10 条 limitations）2026-10-24T20:42:55Z 收到 round34 的
grade A `confirmed_affected`（4.2.13 `BaseSpatialField.get_raster_prep_value`（`db/models/fields.py:172-189`）
把任意 str/bytes 交给 180 行的 `gdal.GDALRaster(value)`、任意 dict 交给 185 行的同一构造，调用点
`get_prep_value` 在 205 行；`GDALRaster.__init__` 对 `/vsi` 前缀跳过 `os.path.exists`（`raster/source.py:87-97`），
dict 分支强制 `_write = 1`（129 行）并在 163 行 `capi.create_ds` 按攻击者给出的 `name` 建文件），
2026-10-24T20:45:40Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 72 evidence / 1 status），
候选 `disc2_964417e6892549137491a482` 已改写为 `confirmed_affected`（backup 见
`runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round34_20261024T204602Z.jsonl`）。
reviewer 在无 root 用户态装出 GDAL 3.13.3 / GEOS 3.14.1 / Python 3.12.15 后实测：dict、JSON 字符串与
admin changelist 三条路径各写出 694 字节 GTiff（sha256 `c9c452e0…`），`/vsicurl` 取值产生 15 次外连，
5.2.17 与「4.2.13 + 5.2 fix」均抛 `DisallowedRasterLookup`、零写盘零外连。修复为 main `f1949c1f`、
backport `115ffd04`（5.2.17）/`208f80cb`（6.0.8），6.1 正式版已含 `39b3e2d0`；4.2 线从未修复，
4.2.30 的 `get_raster_prep_value`/`get_prep_value` 与 4.2.13 逐字节相同（采集方另行复算）。保留口径：
GDAL 3.13.3 未必是目标部署版本、未证 RCE（只证攻击者命名文件的生成与 SSRF）、admin 一步跑在非空间 sqlite
后端；NVD 两条 Secondary CVSS 3.1 8.8 / 4.0 8.7 与 CWE-73+CWE-918 一并保留。
CVE-2026-25673 卷宗（`runs/verification/django_CVE-2026-25673_4213/`，31 件 sha256 钉住产物、
`dossier.json` 31 条证据 / 18 个字段映射 / 12 条 limitations）2026-10-24T20:33:17Z 收到 round33 的
grade A `confirmed_affected`（4.2.13 `URLField.to_python()` 的 `split_url()` 在 766 行执行
`list(urlsplit(url))`，`urlsplit()` 对非 ASCII netloc 做 NFKC，Windows 上异常慢；4.2.13 与 4.2.28
的 `URLField` 类块逐字节相同，4.2.29 改用 `value.partition(":")` 并删除 `urllib.parse` 导入），
2026-10-24T20:35:57Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 70 evidence / 1 status），
候选 `disc2_909a78a0d54a444a667c9f27` 已改写为 `confirmed_affected`。reviewer 用自写探针在
4.2.13/4.2.28/4.2.29 三版安装态各跑两遍（20,017 字符 Unicode 目标 → `urlsplit`×1 +
20,008 字符 netloc 的 NFKC×1；4.2.29 全 12 例 0/0），并把 4.2 fix hunk 应用回 4.2.13 源码验证
产物与 4.2.29 逐字节相同。**影响面同样仅 Windows**；Linux 上 20,008 字符归一化约 0.02 ms，
未测出 DoS 量级，记录按调用边界表述；评分 NVD 两条 Secondary 7.5 HIGH 与 release note
"moderate" 的分歧一并保留。
CVE-2025-64458 卷宗（`runs/verification/django_CVE-2025-64458_4213/`，43 件 sha256 钉住产物、
`dossier.json` 43 条证据 / 18 个字段映射 / 12 条 limitations）2026-10-24T20:28:51Z 收到 round32 的
grade A `confirmed_affected`（4.2.13 `HttpResponseRedirectBase.__init__` 在 617 行
`parsed = urlparse(str(redirect_to))` 前没有长度上限；reviewer 复现 4.2.13/4.2.25 接受 20,017 字符
跳转目标、`urlparse`×1 与 20,008 字符 netloc 的 NFKC×1，4.2.26 对 >2048 在解析前抛
`DisallowedRedirect`（0 parse / 0 normalize），4.2.27 上限 16384；含 200 个仅 query 不同的长 URL
绕过 `urlsplit` 缓存对照），2026-10-24T20:29:54Z 写入 `data/`（1 漏洞 / 1 location / 1 review /
72 evidence / 1 status），候选 `disc2_869ed839e7101f70b458e853` 已改写为 `confirmed_affected`。
**影响面仅 Windows**；reviewer 明确保留「Linux 上 NFKC 约 1ns/字符、无法复现实际 DoS」的边界，
卷宗与 triage 行按调用边界（而非已执行 DoS）表述。固定版本记 4.2.26 / 5.1.14 / 5.2.8
（均 2025-11-05），4.2.27 的 16384 上限是 ticket 36743 的回归修复，不记为 CVE fix。
CVE-2025-59681 卷宗（`runs/verification/django_CVE-2025-59681_4213/`，39 件 sha256 钉住产物）2026-10-24T20:18:06Z
收到 round31 的 grade A `confirmed_affected`（4.2.13 `Query.check_alias()` 的
`FORBIDDEN_ALIAS_PATTERN` 不含 `#`，`annotate()`/`alias()`/`aggregate()`/`extra()` 四条路径的
`**kwargs` 键因此通过校验；reviewer 在安装态 4.2.13/4.2.24/4.2.25 上复现 `ali#as`/`x#`
红/绿差分），2026-10-24T20:20:08Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 72 evidence /
1 status），候选 `disc2_edc9a736a4b87db89ace87ae` 已改写为 `confirmed_affected`。
CVE-2025-13372 卷宗（`runs/verification/django_CVE-2025-13372_4213/`）2026-10-24T20:09:36Z 收到 round30 的
grade A `confirmed_affected`（`QuerySet.alias()`/`annotate()` 经 `**kwargs` 展开把 `FilteredRelation`
别名送进 `Query.add_filtered_relation()` 并成为 join alias；`SQLCompiler.quote_name_unless_alias()`
对 `query.alias_map` 中的名字直接返回而不调用 `connection.ops.quote_name()`，4.2.13 的 PostgreSQL
后端无 override，含 `$` 的别名原样进入 SQL token 流；4.2.27 新增 PostgreSQL compiler 拒绝 `$`），
2026-10-24T20:10:47Z 写入 `data/`（1 漏洞 / 1 location / 1 review / 73 evidence / 1 status），候选
`disc2_949b8ff18e401c0a4c7e4b42` 已改写为 `confirmed_affected`。CVE-2026-25674 卷宗（`runs/verification/django_CVE-2026-25674_4213/`）2026-10-24T18:35:49Z 收到 round22 的
grade A `confirmed_affected`（`FileSystemStorage._save()` / `FileBasedCache._createdir()` 用进程级
`os.umask()` 包住 `os.makedirs()`，并发线程 4,406-4,463 / 4,546-4,607 次偏离；4.2.29 的 `safe_makedirs()`
零 umask 调用），2026-10-24T18:37:10Z 写入 `data/`，候选 `disc2_f08644f4f856311a218b8f05`
已改写为 `confirmed_affected`。CVE-2026-48588 卷宗（`runs/verification/django_CVE-2026-48588_4213/`，39 件 sha256 钉住产物、
`dossier.json` 40 条证据 / 19 个字段映射 / 10 条 limitations）2026-10-24T18:50:25Z 收到 round23 的
grade A `confirmed_affected`（`UpdateCacheMiddleware.process_response()` 的 `not request.COOKIES` 前置条件
让带任意无关 Cookie 的请求把受害者的 `Set-Cookie` 写进共享缓存；4.2.13/5.2.15/6.0.6 红、5.2.16/6.0.7 绿，
含真实 WSGI handler 与三类对照），2026-10-24T18:53:18Z 写入 `data/`，候选 `disc2_f805f93b227052047bcaf78f`
已改写为 `confirmed_affected`。**该案 4.2 线没有修复版本**（LTS 支持 2026-04 结束，修复 2026-07 随 5.2.16 /
6.0.7 发布，另 6.1 线有 `c2a936ab…`，公告未点名），卷宗只记 5.2.16 与 6.0.7；评分采用 CNA/厂商 CVSS 4.0
2.3 LOW，NVD Primary 5.3 记入 `all_published_scores` 但不采用。CVE-2025-13473 卷宗（`runs/verification/django_CVE-2025-13473_4213/`）2026-10-24T18:24:19Z 收到 round21 的
grade A `confirmed_affected`（mod_wsgi `check_password()` 对不存在/停用用户在哈希前返回，实测 0 vs 1 次
PBKDF2 调用、288× 中位耗时），2026-10-24T18:26:46Z 写入 `data/`，候选 `disc2_0ae99f3b69a48b480295ab89`
已改写为 `confirmed_affected`。CVE-2026-4277 卷宗
（`runs/verification/django_CVE-2026-4277_4213/`）2026-10-24T18:15:24Z 收到 round20 的
grade A `confirmed_affected`（`GenericInlineModelAdmin.get_formset` 重写后丢失基类的
can_change/can_add 包装，伪造 inline 新增绕过 `has_add_permission`），2026-10-24T18:16:57Z 写入 `data/`，
候选 `disc2_f75eaf5e610a2b495529ddce` 已改写为 `confirmed_affected`。CVE-2026-4292 卷宗
（`runs/verification/django_CVE-2026-4292_4213/`）2026-10-24T18:04:37Z 收到 round19 的
grade A `confirmed_affected`（`ModelAdmin.changelist_view` 的 `list_editable` 保存循环
未校验 `obj._state.adding`，伪造 POST 绕过 `has_add_permission` 插入行），2026-10-24T18:05:34Z 写入 `data/`，
候选 `disc2_518dea83eab5c641d5f2c9ff` 已改写为 `confirmed_affected`。CVE-2026-33033 卷宗
（`runs/verification/django_CVE-2026-33033_4213/`）2026-10-24T18:00:24Z 收到 round18 的
grade A `confirmed_affected`（`MultiPartParser` base64 对齐循环每轮只读 1-3 字节，`LazyStream`
unget 逐字节重拷 64 KiB 分块），2026-10-24T18:01:19Z 写入 `data/`，候选
`disc2_f7b7100a8e247c57aae034fb` 已改写为 `confirmed_affected`。CVE-2026-33034 卷宗
（`runs/verification/django_CVE-2026-33034_4213/`）2026-10-24T17:58:00Z 收到 round17 的
grade A `confirmed_affected`（`HttpRequest.body` 只按声明的 `Content-Length` 检查上限，ASGI
缺头/低报时无界读取 spool 的 body），2026-10-24T17:58:38Z 写入 `data/`，候选
`disc2_0e9bed26286b9becdb4e8091` 已改写为 `confirmed_affected`。CVE-2026-3902 卷宗
（`runs/verification/django_CVE-2026-3902_4213/`）2026-10-24T17:49:58Z 收到 round16 的
grade A `confirmed_affected`（ASGIRequest 把下划线拼写折叠进连字符头的同名 META 键），
2026-10-24T17:50:54Z 写入 `data/`，候选 `disc2_931984b6d2edccd8cf80d5a8` 已改写为
`confirmed_affected`。CVE-2026-1285 卷宗
（`runs/verification/django_CVE-2026-1285_4213/`）2026-10-24T17:38:10Z 收到 round15 的
grade A `confirmed_affected`（`Truncator._truncate_html` 未匹配结束标签二次方），
2026-10-24T17:40:45Z 写入 `data/`，候选 `disc2_0f82375353c52e59aee290ad` 已改写为
`confirmed_affected`。
本会话没有伪造真值，也没有把成功率和完成度标到实际未达成的水平。

### 0.1 两个证据先行升级的当前状态（2026-10-23）

两个目标都已完成「独立验证 → promote → 迁移快照 → 导出 → 审计导出 → 选版审查包 → 独立选版 accept → frozen」。

- **netty**：旧目标 `snap_bb344e672a0544ef`（4.1.59.Final）超出 4 年规则，升级到
  `netty-4.1.137.Final` = `5471f0a6ffa4ab39db22c468c6c851af4ecae709`（2026-08-06，注释 tag），
  新快照 `snap_5c3900a03253c043`（3479 文件，tree `146e08ab…`）。正样本 CVE-2026-93494 /
  GHSA-ghg5-c4jg-8q5j（StompSubframeDecoder 的 `lastContent` 在 replay 信号下不可达
  `catch (Exception)`，且无 `handlerRemoved0`，pooled ByteBuf 泄漏；4.1.138 修复 commit
  `cb84b06388`）。独立 verdict：`confirmed_affected`，**B**，reviewer
  `independent-reviewer-netty-CVE-2026-93494-r1`（`runs/independent/netty_CVE-2026-93494_v41137_round1/`）。
  已 promote（1 vuln / 1 location / 1 review / 22 evidence / 1 status）；旧目标 6 个正样本经
  `git merge-base --is-ancestor` 判定修复已在快照内，全部改判 `confirmed_not_affected`，旧行归档到
  `data/legacy_*_snap_bb344e672a0544ef.jsonl`（vulnerabilities/locations/reviews/evidence 保持 live，
  与 django/rack/libexpat/phoenix 先例一致）。导出 archive sha256 `089a09be…`，审计导出剩余 advisory 0、
  redacted 1。选版审查包 `v031/reviews/selection_packets/1064563_netty__netty.json`；本机已补齐用户态
  JDK 17 + Maven 3.9.16 并在全新解包目录跑通 `mvn -B -DskipTests … package`（47/47 SUCCESS，约 4 分钟，
  含 epoll/unix-common 原生模块），独立选版审查 `independent-selection-reviewer-netty-2026-10-23`
  返回 **accept**（tag 对象 `5c403d0b` peel 到 `5471f0a6`、3479 个 tar 成员逐个 sha256/size 与 manifest
  对齐且与 `git ls-tree -r` 路径/模式一致、无 `.git`、审计仅 redact `HttpUtil.java` 的 GHSA 记号、
  全新目录 47/47 BUILD SUCCESS 且原生 .so 真实产出），`apply_selection_review.py --apply` 已 **frozen**
  （2026-10-23）。
- **guzzle**：旧目标 `snap_efe695448113758a`（7.4.4，2022-05）超出 4 年规则，升级到 `7.14.1` =
  `6b1d2429a2c312474c523aa9017fba0c07b5f4a0`（2026-07-13），新快照 `snap_1ce353bfdb334948`（119 文件）。
  正样本 CVE-2026-67339 / GHSA-94pj-82f3-465w（`applyProxyAuthorizationHeaderHandling` 只在预测到
  HTTP(S) 代理时才迁移头部，direct / no_proxy / SOCKS 路由下 `applyHeaders` 1910-1929 仍把
  `Proxy-Authorization` 写进 `CURLOPT_HTTPHEADER`，libcurl 默认 `CURLHEADER_UNIFIED` 会发给源站；
  7.14.2 在 1985-1987 跳过该头并经 `applyManagedProxyAuthorization` 1580-1598 走 `CURLOPT_PROXYHEADER`）。
  独立 verdict：`confirmed_affected`，**A**（含 `harness/` 红/绿复现：7.14.1 三条泄漏路由，7.14.2 全部干净），
  reviewer `independent-reviewer-guzzle-CVE-2026-67339-r1`。已 promote（1 vuln / 1 location / 1 review /
  21 evidence / 1 status）；旧目标两个正样本（GHSA-25mq-v84q-4j7r / CVE-2022-31091）修复 commit
  `1dd98b05`（7.4.5）经 ancestry 判定已在 7.14.1 内，改判 `confirmed_not_affected`。导出 archive sha256
  `3a53ce38…`，审计导出剩余 advisory 0、excluded 1（CHANGELOG.md）、redacted 3。选版审查包
  `v031/reviews/selection_packets/1420053_guzzle__guzzle.json`；独立选版审查
  `independent-selection-reviewer-guzzle-2026-10-23` 返回 **accept**（tag peel 一致、archive/manifest
  sha256 与路径逐条核对 119/119、无 `.git`、审计导出 remaining 0 且 source_export_id 对齐、
  在全新目录用用户态 PHP/composer 真实构建并通过 1396 tests），`apply_selection_review.py --apply`
  已 **frozen**（2026-10-23）。
- **本机用户态构建链**（无 sudo）：`~/.local/toolchain/` 下 JDK 17.0.20.1、Maven 3.9.16、
  static PHP 8.4.23（含 curl）、composer 2.10.3。guzzle 在 7.14.1 树上 `composer install` +
  `phpunit`（排除需要 127.0.0.1:10000 的 `HttplugIntegrationTest`）实测 1396 tests / 1 failure
  （`CurlFactoryTest::testFirstProxyTunnelOwnerReusesPooledHandleWithoutPurging` 的对象同一性断言）。
- **方法教训（版本区间判定）**：netty 的 advisory 同时列 4.1 与 4.2 两条分支区间；把
  `(4,1,137)` 与 `(4,2,15)` 直接做元组比较会把任何 4.1.x 误判为「≤4.2.15」，导致 37 条误命中。
  正确做法是先按 major.minor 分支过滤，只对同分支边界求值；按此重算为 23 条命中 / 91 条排除 / 3 条格式
  无法解析（`GHSA-p9jm-q85p-7mcp`、`GHSA-4g8c-wm8x-jfhw`、`GHSA-hh82-3pmq-7frp`）。

## 1. 目录与角色（谁是权威）

| 路径 | 角色 |
|---|---|
| `v031/WORKFLOW.md` | **唯一 SOP**：P0–P8 阶段与发布门槛。任何判断以它为准。 |
| `manifest.json` | `dataset_version=0.3.1`、`status=draft`、`evaluation_policy=one_frozen_snapshot_snapshot_only_oracle` |
| `data/` | 数据。九张主表 + `evaluation_selection.jsonl` + `snapshot_candidate_triage.jsonl` + `snapshot_exports.jsonl` + `snapshot_audit_exports.jsonl` + `snapshot_proposals.jsonl` + `legacy_discovery_coverage_v03.jsonl` |
| `v031/schemas/` | 16 份 schema（新增 `snapshot_exports`/`snapshot_proposals`/`snapshot_audit_exports`；`discovery_coverage`/`manifest` 已 v0.3.1 化） |
| `v031/scripts/` | 迁移 / 导出 / 提案 / 审查 / 校验 / 排对 / 费用脚本（见 §5） |
| `v031/reports/` | `VALIDATION_DRAFT.json` / `VALIDATION_RELEASE.json` / `EXPORT_AND_PROPOSAL_STATUS.md` / `SELECTION_FREEZE_2026-10-22.md` / `queue_P3.json` / `COST_REPORT.json` / `SELECTION_TABLE.md` |
| 根目录 `*.md/_V031.md` | README / LIMITATIONS / SELECTION / CANDIDATE_FUNNEL / MIGRATION_AND_VALIDATION，本版说明 |
| `docs/RESUME_V031.md` | 上一版续跑要点（与本文一致，本文更完整） |
| `v03/`、`migration_backup_v02/`、根 `schemas/`、`runs/`、`scratch/` | **只读保留**：旧版本工具与中间产物 |
| 源 v0.3 目录 | `/home/luchitong/work/repo-vuln-50-v03`，**只读未写**（供对照，勿再写）。 | 

**硬约束（必须遵守）**：不得伪造验证结果、不得擅自改审核等级、不得删除未解决候选、不得提前声明数据集完成、
不得机械依赖 semver 判不存在、不得编造 commit 或直接冻结；`unknown/possible_affected` 未核验前不得声称快照已知
漏洞已穷尽。独立 reviewer 必须在隔离上下文工作，不能读采集方卷宗。

## 2. 真实数据基线（逐行复算，非沿用上报值）

- 九张主表（2026-10-25 复算）：**50 repositories / 110 snapshots / 167 vulnerabilities / 167 locations /
  6518 evidence / 167 reviews / 2626 candidates / 50 discovery_coverage / 138 snapshot_vulnerability_status**。
  另：`evaluation_selection` 48、`snapshot_exports` 48、`snapshot_audit_exports` 48、`snapshot_proposals` 2。
  110 个快照中 48 个是 `evaluation_target=true`，另含 django 旧目标 3.0.2、rack 旧目标 2.2.3、libexpat
  旧目标 R_2_4_4、phoenix 旧目标 v1.6.13、netty 旧目标 4.1.59.Final、guzzle 旧目标 7.4.4 等历史快照。
- 注意：漏洞表 167 行 = 138 行在评测目标快照上（live `snapshot_vulnerability_status` 138 行，全为
  `confirmed_affected`）+ 29 行位于历史快照（django 3.0.2 的 8 条、rack 2.2.3 的 2 条、libexpat R_2_4_4
  的 7 条、phoenix v1.6.13 的 2 条、netty 4.1.59.Final 的 6 条、guzzle 7.4.4 的 2 条等），后者保留作
  历史证据但不在主 oracle 中。**不要把表行数当正样本数。**（evidence 6518 行。）
- 评测目标：**48 个目标 / 46 frozen / 2 rejected**。46 个 frozen 均通过独立选版审查；2 个 legacy
  `documented_exception`（hyper、Newtonsoft.Json）仍为 rejected（gin、protobuf 已分别由取证目标闭环）。
  django tag 4.2.13（CVE-2024-39330）、rack tag v3.1.13（CVE-2025-46727）、libexpat tag R_2_6_2
  （CVE-2024-45490）、phoenix tag v1.8.8（CVE-2026-56811、CVE-2026-56812）、netty 4.1.137.Final
  （CVE-2026-93494）、guzzle 7.14.1（CVE-2026-67339）、echo v4.15.2（CVE-2026-55677）与 axios v1.19.0
  （CVE-2026-101907）都是证据先行的新目标——已导出全树并做 P6 审计导出，并分别通过独立选版审查后冻结
  （django 第一轮因审计泄漏 reject，修复后第二轮 accept；rack/libexpat 首轮 accept；
  phoenix 首轮因环境无 Elixir 工具链 `build_ok=false`，补齐后由同一审查者独立重建并改判 `accept`；
  netty 首轮因无 JDK/Maven 无法满足 `build_ok`，补齐用户态 JDK 17 + Maven 3.9.16 后重新送审；
  echo/axios 于 2026-10-23 由独立审查者实测 go build / npm ci+build 后 accept；
  grpc v1.52.0 于 2026-10-24 由独立审查者实测 CMake/Ninja 构建 `libgrpc.a` + 消费者链接运行后 accept）。
  剩余 2 仓库 `needs_selection`（`evaluation_snapshot_id=null`）：nlohmann/json、openssl/openssl
  （漏洞窗口内没有可用稳定发布 tag）。
- 已知正样本：`data/vulnerabilities.jsonl` 共 **167 行，reviews 167 行（A 90 / B 77）**；其中 138 行在评测目标
  快照上（48 B + 90 A），29 行位于历史快照（全 B）。A 级为 rexml CVE-2025-58767、django CVE-2024-39330、
  rack CVE-2025-46727、libexpat CVE-2024-45490、libexpat CVE-2024-8176、libexpat CVE-2024-50602、libexpat CVE-2026-32778、libexpat CVE-2026-32777、libexpat CVE-2026-32776、libexpat CVE-2026-24515、undici CVE-2024-24758、undici CVE-2024-30260、phoenix CVE-2026-56812、guzzle CVE-2026-67339、
  echo CVE-2026-55677、axios CVE-2026-101907、grpc CVE-2023-1428、cJSON CVE-2023-53154、cJSON CVE-2023-50472、
  cJSON CVE-2025-57052、gitea GHSA-hg5r-vq93-9fv6（HMAC 无分隔歧义，Go 原语级红/绿）、
  rack CVE-2025-61919（url-encoded body 无参 `IO#read` 读尽，1/8/32/64 MiB 线性驻留且无放大，
  3.1.18 在 4,194,306 字节截断并抛 `QueryLimitError`）、
  django CVE-2024-39329（不可用密码的计时枚举，实测约 715× 差异）、
  django CVE-2026-6873（`get_signed_cookie` 以 `key + salt` 拼接派生 salt，`("a","bc")` 与 `("ab","c")` 共享签名命名空间；4.2.13/4.2.30/5.2.14/6.0.5 红、5.2.15/6.0.6 对新 cookie 绿，21 次执行含阴性对照，另跑上游 12 个 signed-cookie 测试全过；4.2 线无修复版）与
  django CVE-2026-1207（PostGIS raster `band_lhs/band_rhs` 未做整数校验即拼入 `ST_Band` SQL；字符串 band index 在 4.2.13/4.2.27 红、4.2.28 `TypeError` 绿）与
  django CVE-2026-1287（列别名控制字符未过滤进入 `AS` 片段；4.2.13 红、修复版拒绝）与
  django CVE-2026-1312（`SQLCompiler._order_by_pairs()` 的 `if "." in field:` 把含点 `FilteredRelation` 别名直接拆成 `table` + 未校验 `col` 写入 `ORDER BY`；4.2.13/4.2.27 红、4.2.28 `ValueError` 绿，含 `randomblob` 注入与三条对照）与
  django CVE-2026-48587（Vary 头未 strip，`Vary: " Cookie"` 绕过 cookie 守卫把带 `Set-Cookie` 的响应写入共享缓存；4.2.13/4.2.30 红、5.2.15/6.0.6/6.1 绿）与
  django CVE-2026-48588（`UpdateCacheMiddleware` 的 `not request.COOKIES` 前置条件，带无关 Cookie 时把受害者 `Set-Cookie` 写进共享缓存并回放；4.2.13/5.2.15/6.0.6 红、5.2.16/6.0.7 绿，含真实 WSGI handler 与三类对照）与
  django CVE-2026-25674（进程级 `os.umask()` 包住 `os.makedirs()`，并发 canary 4,406-4,463/4,546-4,607 次偏离；4.2.29 `safe_makedirs()` 零 umask、5,000 次 chmod）与
  django CVE-2025-13473（mod_wsgi `check_password()` 对不存在/停用用户不哈希，0 vs 1 次 PBKDF2、288× 中位耗时；4.2.28 拉平）、
  gitea GHSA-7wvc-rvp7-w99x（LFS SSH 子命令鉴权绕过，真实服务器红/绿）与
  django CVE-2024-38875（urlize 括号裁剪二次方复杂度，实测 9.86 s → 0.003 s）、
  django CVE-2024-41989（floatformat 指数内存耗尽）、django CVE-2024-39614
  （语言码二次方切片）、django CVE-2024-41991（urlize/widget IDNA 无上限）与
  django CVE-2024-53907（strip_tags 无深度上限，26.3 s → SuspiciousOperation）与
  django CVE-2024-53908（Oracle `HasKeyLookup.as_oracle` 把 lhs 参数拼进 SQL 文本，compile-level 红/绿）与
  django CVE-2024-45231（密码重置邮件失败时的状态码枚举，真实 view 返回 500 vs 302）与
  django CVE-2025-64459（`_connector` 字典展开注入，filter 返回全部行 vs 4.2.26 拒绝）、
  django CVE-2025-32873（strip_tags 二次方 DoS，7.893 s vs SuspiciousOperation）、
  django CVE-2025-57833（FilteredRelation alias 注入，过滤绕过 vs ValueError）与
  django CVE-2025-59682（archive 前缀兄弟目录写出 vs SuspiciousOperation）、
  django CVE-2025-59681（`Query.check_alias()` 黑名单缺 `#`，MySQL/MariaDB 注释起始符经 `**kwargs` 别名通过校验，4.2.13/4.2.24 红、4.2.25 `ValueError` 绿）与
  django CVE-2025-64458（`HttpResponseRedirectBase.__init__` 在 parse 前无长度上限，20,017 字符 Unicode 目标触发 `urlparse`×1 与 netloc NFKC×1，4.2.26 在 >2048 时解析前拒绝；影响面仅 Windows）与
  django CVE-2026-25673（`URLField.to_python()` 的 `split_url()` 在 766 行 `list(urlsplit(url))`，非 ASCII netloc 走 NFKC；4.2.13/4.2.28 `URLField` 块逐字节相同，4.2.29 改 `value.partition(":")`；影响面仅 Windows）与
  django CVE-2026-15307（`get_raster_prep_value()` 把 str/bytes 与 dict 直接交给 `GDALRaster`，dict 强制写模式并按攻击者 `name` 建 694 字节 GTiff，`/vsicurl` 取值 15 次外连；5.2.17/6.0.8 用 `DisallowedRasterLookup` 拦截，4.2 线无修复）与
  django CVE-2025-48432（`log_response()` 未转义参数导致日志注入，4.2.22 部分修复 / 4.2.23 完整）与
  django CVE-2025-64460（XML serializer `getInnerText()` 二次方膨胀，1 MB 载荷 4.63 s vs 0.0097 s）与
  django CVE-2025-26699（`wrap()`/`wordwrap` 每行重切剩余串，4.93 MB 载荷 42.54 s vs 0.54 s）与
  django CVE-2025-14550（ASGIRequest 每个重复 header 重拼整串，200,000 头 27.70 s vs 0.0504 s）与
  django CVE-2026-1285（`Truncator._truncate_html` 对未匹配结束标签全表扫描，128k 载荷 189.45 s vs 2.51 s）与
  django CVE-2026-3902（ASGIRequest 把 `x_forwarded_host` 下划线拼写折叠进 `HTTP_X_FORWARDED_HOST`，4.2.13/4.2.29 可见 vs 4.2.30 忽略）与
  django CVE-2026-33034（`HttpRequest.body` 只按声明的 `Content-Length` 检查上限，ASGI 缺头/低报时无界读取；200,000 B 200 vs 400）与
  django CVE-2026-33033（base64 对齐循环逐字节 replay 64 KiB 分块，1 MiB 2.15 s vs 0.00068 s）与
  django CVE-2026-4292（`ModelAdmin.changelist_view` 的 `list_editable` 保存循环未校验新建，伪造 POST 4.2.13/4.2.29 插入 vs 4.2.30 400 拒绝）与
  django CVE-2026-4277（`GenericInlineModelAdmin.get_formset` 丢失 add 权限包装，伪造 inline 新增 4.2.13/4.2.29 插入 vs 4.2.30 忽略）与
  django CVE-2025-13372（`FilteredRelation` 别名经 `**kwargs` 成为 join alias，`quote_name_unless_alias()`
  对 `alias_map` 名字不调用 `ops.quote_name()`，4.2.13/4.2.26 含 `$` 别名原样进 SQL（pglast 解析确认未加引号）、
  4.2.27 新 PostgreSQL compiler 抛 `ValueError`）与
  rack CVE-2025-49007（3.1.13 未锚定 `Content-Disposition` 正则的二次方开销，2.5 KB 1.336 ms →
  80 KB 1439 ms，3.1.16 同载荷 1.305 ms）与
  rack CVE-2025-61772（multipart part 头缺少字节上限，64 MiB body 时 VmHWM 增量约 66 MB，
  3.1.17 在同构造上 raise）、
  rack CVE-2025-61770（multipart preamble 在首个 boundary 前无上限，64 MiB 时 VmRSS +65,576 kB，
  3.1.17 在第 1 次读 1,048,576 B 后即抛错）与
  rack CVE-2025-61771（无 filename 的非文件字段整段驻留内存，64 MiB 时 GC 后 RSS +67,416 KiB，
  3.1.17 在 16/64 MiB 上都抛 "multipart data over retained size limit"）与
  rack CVE-2025-61919（`Rack::Request#POST` 531 行无参 `read` 读尽 url-encoded body，
  1/8/32/64 MiB 的 VmRSS 增量 +1024/8192/32896/65536 KiB，3.1.18 在 4,194,306 字节截断并抛
  `Rack::QueryParser::QueryLimitError`，3.1.17 为「先读后限」中间态）与
  rack CVE-2025-61780（`Rack::Sendfile` 信任客户端 `x-sendfile-type` / `x-accel-mapping`，
  3.1.13 产出 `x-accel-redirect: /attacker/path/secret.txt`，3.1.18 不发该头）与
  undici CVE-2024-30260（`RedirectHandler.shouldRemoveHeader` 对未知 origin 只剥
  `authorization`/`cookie`，跨 origin 重定向把 `proxy-authorization` 送到目标；v5.19.0/v5.28.3 红、
  v5.28.4 绿，对象与扁平数组两种 header 形态都测）等，均由独立 reviewer 做动态或实测
  red/green（verdict 分别在
  `runs/independent/{rexml_CVE-2025-58767_round1,django_CVE-2024-39330_round1,rack_CVE-2025-46727_round1,libexpat_CVE-2024-45490_round1,phoenix_CVE-2026-56812_v188_round1,guzzle_CVE-2026-67339_v7141_round1,echo_CVE-2026-55677_v4152_round1,axios_CVE-2026-101907_v1190_round1,grpc_CVE-2023-1428_v1.52.0_round1,cjson_CVE-2023-53154_v1716_round1,cjson_CVE-2023-50472_v1716_round1,cjson_CVE-2025-57052_v1716_round1,gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1,django_CVE-2024-39329_4213_round1,gitea_GHSA-7wvc-rvp7-w99x_v1.25.5_round1,django_CVE-2024-38875_4213_round1,django_CVE-2024-53907_4213_round7,django_CVE-2024-53908_4213_round8,django_CVE-2024-45231_4213_round9,django_CVE-2025-64459_4213_round10,django_CVE-2025-32873_4213_round11,django_CVE-2025-57833_4213_round11,django_CVE-2025-59682_4213_round11,django_CVE-2025-48432_4213_round12,django_CVE-2025-64460_4213_round12,django_CVE-2025-26699_4213_round13,django_CVE-2025-14550_4213_round14,django_CVE-2026-1285_4213_round15,django_CVE-2026-3902_4213_round16,django_CVE-2026-33034_4213_round17,django_CVE-2026-33033_4213_round18,django_CVE-2026-4292_4213_round19,django_CVE-2026-4277_4213_round20,django_CVE-2025-13473_4213_round21,django_CVE-2026-25674_4213_round22,django_CVE-2026-48588_4213_round23,django_CVE-2026-8404_4213_round24,django_CVE-2026-48587_4213_round25,django_CVE-2026-6873_4213_round26,django_CVE-2026-1312_4213_round27,django_CVE-2026-1287_4213_round28,django_CVE-2026-1207_4213_round29,django_CVE-2025-13372_4213_round30,django_CVE-2025-59681_4213_round31,django_CVE-2025-64458_4213_round32,django_CVE-2026-25673_4213_round33,django_CVE-2026-15307_4213_round34,django_CVE-2026-53877_4213_round35,django_CVE-2026-15830_4213_round36,rack_CVE-2025-49007_round37,rack_CVE-2025-61772_round38,rack_CVE-2025-61770_round39,rack_CVE-2025-61771_round40,rack_CVE-2025-61919_round41,rack_CVE-2025-61780_round42,flask_2.3.1_CVE-2026-27205_round43,werkzeug_3.0.2_CVE-2024-49767_round44,phpmailer_6.1.5_CVE-2021-3603_round45,libexpat_R_2_6_2_CVE-2024-8176_round46,libexpat_R_2_6_2_CVE-2026-24515_round47,libexpat_R_2_6_2_CVE-2026-32776_round48,libexpat_R_2_6_2_CVE-2026-32777_round49,libexpat_R_2_6_2_CVE-2026-32778_round50,libexpat_R_2_6_2_CVE-2024-50602_round51,undici_v5.19.0_CVE-2024-30260_round52,undici_v5.19.0_CVE-2024-24758_round53}/`）。
- 候选状态：`verified 117` / `rejected 429` / `pending_location 738` / `in_validation 485` / `pending_version 857`。
- 全部仓库 triage（`snapshot_candidate_triage.jsonl`，2613 行）：`confirmed_affected 162` /
  `confirmed_not_affected 1322` / `possible_affected 527` / `duplicate 28` / `unknown 574`；
  `pending_relevant_triage` **1101**（= 574 unknown + 527 possible）；
  已选版仓库内候选均有 triage 行（549 条「此前无行」的候选已于 2026-10-24 以 unknown 行补全，
  `runs/triage_untriaged_unknown_2026-10-24/`）；另有 13 条属于两个未选版仓库，按先选版处理。django 旧快照的
  163 条、rack 旧快照的 50 条、libexpat 旧快照的 143 条、phoenix 旧快照的 8 条、netty 旧快照的 130 条与
  guzzle 旧快照的 17 条 triage 行已分别归档；
  django/rack/libexpat 三个新快照上的候选现为 unknown 2 条、0 条、34 条（其余已有范围/代码级决策；
  区间命中一律记入 `possible_affected`：django 9、rack 21、libexpat 35），这些 possible 仍需源码复核；
  rexml 的 8 条、
  libexpat 的 7 条与 phoenix 的 8 条已在各自快照上按代码/修复区间 + 祖先关系判定
  （`runs/verification/rexml_snapshot_not_applicable/NOT_APPLICABLE.md`、
  `runs/verification/libexpat_R_2_6_2_fixed_previous/NOT_APPLICABLE.md`；phoenix 的排除性结论分别依据
  `validate_local_url/1` 加固、`compare_host?/2` 点边界与 `long_poll.ex` 的惰性 splitter，见 triage 行 basis）。
- django 4.2.13 的 CVE-2026-1287 与 CVE-2026-1207 分别于 round28 / round29 完成隔离复核（grade A）并 promote，
  对应候选 `disc2_c3e2d500c2ab4d8d7d3b514a` / `disc2_d7e6c2d74bb34b3fe360cc4d` 已转 `confirmed_affected`。
  CVE-2025-13372 于 round30 完成隔离复核（grade A）并 promote，候选
  `disc2_949b8ff18e401c0a4c7e4b42` 已转 `confirmed_affected`；reviewer NOTES 指出真实危险区间是
  `compiler.py:519-539`（`quote_name_unless_alias()` 在 536 行直接 `return name`），而 location 记的是
  519-536 的首行片段，二者重叠故通过 promoter 的行号校验；结论仍以验证到的 519-539 为准。
  CVE-2025-59681 于 round31 完成隔离复核（grade A）并 promote，候选
  `disc2_edc9a736a4b87db89ace87ae` 已转 `confirmed_affected`；reviewer 在 NOTES 中保留
  "反引号引用下未实测注释注入" 的意见，卷宗与 triage 行均按校验边界（而非武器化注入）表述。
  CVE-2025-64458 于 round32 完成隔离复核（grade A）并 promote，候选
  `disc2_869ed839e7101f70b458e853` 已转 `confirmed_affected`；reviewer 用探针复现了
  4.2.13/4.2.25 对 20,017 字符目标的 `urlparse`×1 与 netloc NFKC×1，4.2.26 在解析前按
  >2048 拒绝（0/0），4.2.27 改为 >16384 的上游后续 bugfix（ticket 36743，非 CVE 修复）；
  NOTES 与 triage 行均记录影响面仅 Windows、Linux 上未测出 DoS 时延，按调用边界而非实测耗尽表述。
  CVE-2026-25673 于 round33 完成隔离复核（grade A）并 promote，候选
  `disc2_909a78a0d54a444a667c9f27` 已转 `confirmed_affected`；reviewer 在三版安装态各跑两遍
  探针（20,017 字符 Unicode 目标 → `urlsplit`×1 + 20,008 字符 netloc 的 NFKC×1，无 scheme 时
  2 次；4.2.29 全 0/0 且不再导入 `urlsplit`），并验证 fix hunk 应用到 4.2.13 后 URLField 块与
  4.2.29 逐字节相同。NOTES 同样保留「仅 Windows、Linux 归一化约 0.02 ms、非实测 DoS」的边界；
  另指出 4.2.29 的 `URLValidator` 对 ≤2048 输入仍会走 `urlsplit`（有界残余路径，不影响 4.2.13 判定）。
  CVE-2026-15830 于 round36 完成隔离复核（grade B，静态）并 promote，候选
  `disc2_956f6f00002b68166b526c02` 已转 `confirmed_affected`；reviewer 同样无法执行 Django/GEOS，
  九字段全部静态核实后停在 B，并独立复算了 4.2.13/4.2.30 的整文件同一性、八个 fix 提交的祖先矩阵、
  逐 tag grep 与 GEOS `MAX_PARSE_DEPTH` 插入点；其 `disagreements` 指出卷宗 4.2 EOL 日期错一年
  （见 §0 与 `runs/verification/django_CVE-2026-15830_4213/POST_REVIEW_CORRECTIONS.md`）。
  CVE-2026-53877 于 round35 完成隔离复核（grade B，静态）并 promote，候选
  `disc2_129f28a7857053e311c7d94d` 已转 `confirmed_affected`；reviewer 无法执行 GDAL，
  九字段全部静态核实后按规则停在 B，并用 4.2.13/5.2.15 整文件同一性、四个 fix 补丁与祖先关系、
  本地 `getsizeof` 差值（33+1 → 越界 32 字节）三方互证。
  CVE-2026-15307 于 round34 完成隔离复核（grade A）并 promote，候选
  `disc2_964417e6892549137491a482` 已转 `confirmed_affected`；reviewer 自建 GDAL 3.13.3 / GEOS 3.14.1
  用户态环境，dict、JSON 字符串与 admin changelist 三条路径各写出 694 字节 GTiff，`/vsicurl` 取值
  产生 15 次外连；5.2.17 与「4.2.13 + 5.2 fix」均抛 `DisallowedRasterLookup`。NOTES 保留
  「未证 RCE、GDAL 版本未必同目标部署、admin 一步用 sqlite 非空间后端」三条边界。
- CVE-2026-53878 以**负证据**结案：`DomainNameValidator` 在 4.2 分支不存在（4.2.13 / 4.2.30 的 `git grep`
  均无匹配，类首见于 5.1；5.2 / 6.0.6 用 `r"$"`，5.2.16 / 6.0.7 改为 `r"\Z"`），公告 OSV/NVD 区间也只覆盖
  5.2 / 6.0。24 件 sha256 钉住产物见 `runs/verification/django_CVE-2026-53878_4213_absent/`，
  候选 `disc2_321d50f93bd7f1b2dc581ab7` 已改写 `confirmed_not_affected`；该否定仅针对本公告，不构成
  `PASS_KNOWN_SWEEP`，也不声明 4.2.13 无其他漏洞。

## 3. 已做 / 未做（诚实分界）

**已做（本会话交付）**
1. 无损升级 0.3→0.3.1：`UPGRADE_REPORT.json`记录了 9753 源文件 SHA256；六个核心表与 v0.3 源字节级一致；
   源 v0.3 未写入（已用其自记校验和核对）。
2. v0.3.1 工具包安装到 `v031/`；discovery_coverage 归档为 legacy 且 50 条重置 `NEEDS_REVIEW`（不继承旧 PASS）。
3. 初始 P3 相关性 triage 由 `v031/scripts/build_initial_triage.py` 用既有证据生成（零 LLM、零编造）。
4. plan_snapshot_queue 生成队列（2026-10-25 重跑，`v031/reports/queue_P3.json`：P0_SELECT_SNAPSHOT 13 /
   DONE 160 / P1_VERIFY 529 / P1_REVIEW 574 / ARCHIVE 1350，合计 2626；此前落盘文件停在 2026-10-23，
   已随 round20–round52 各次提升刷新）。
5. 校验与测试：draft 0 err / 49 warning；release 仍有门槛阻塞（结构未损坏）；v0.3.1 单测 35 → 当前 126 tests OK
   （2026-10-24 新增低侧证明、归属、裸版本拒绝与不可读副本不否决的测试）。
6. 费用台账：本版零 LLM，0 记账/¥0；`cost_policy.json` 为阈值非网关。
7. 48 个当前目标的确定性全树导出 + P6 审计导出（`snapshot_exports`/`snapshot_audit_exports` 各 48 行）：archive/manifest 可复现、无 `.git`、
   `missing_from_archive_count=0`；审计导出逐目标排除 advisory 文档，剩余 advisory ID 0。
   2026-10-23 修复审计扫描器（Sphinx `:cve:` 角色形式与 1 MiB 截断），django 审计导出重建后排除
   114 个文件、替换 1 个文件、剩余 0。
8. 独立选版审查：48 个隔离 packet，审查者与选择者不同；46 个 accept 已 frozen（grpc 的 4 条 anchor
   由 `v031/reviews/selection_review_grpc_2026-10-24.jsonl` 记录）。
   django 第一轮因审计导出泄漏 Sphinx CVE 角色被 reject，修复后第二轮 accept（2026-10-23 冻结）；
   rack 新目标首轮 accept（2026-10-23 冻结）；phoenix 首轮因环境无 Elixir 工具链 `build_ok=false`，
   补齐用户级 Erlang/Elixir 后由同一审查者独立重建（`mix deps.get`、`mix compile` exit 0）改判 accept。
9. ruby/rexml v3.4.1「先证据、后选版」闭环（本版新增）：CVE-2025-58767 dossier（14 条证据）
   → 独立漏洞复核 **A 级**（red/green 复现，verdict 与脚本存 `runs/independent/rexml_CVE-2025-58767_round1/`）
   → `promote_verified_rows.py` 合并写入 1 漏洞/1 location/1 review/30 evidence/1 status
   → 候选 `disc2_de98c5ab937e69a43862e5b4` 置 `verified` 并补 1 条 `confirmed_affected` triage 行
   → snapshot `snap_23dff8507560a593`（evaluation_target）+ 全树导出 196 文件 + P6 审计导出（排除 NEWS.md，剩余 ID 0）
   → 独立选版审查 accept（4 项导出检查全过、tag peel 一致、anchor 三源确认）→ **frozen**。
10. django tag 4.2.13 目标（本版新增）：CVE-2024-39330 dossier（13 条证据）→ 独立漏洞复核 **A 级**
    （red/green，`runs/independent/django_CVE-2024-39330_round1/`）→ 写入 1 漏洞/1 location/1 review/
    26 evidence/1 status → 候选 `disc2_911c6ce3cba60cce0edccd71` 置 verified、补 triage → 全树导出 6,729 文件
    + P6 审计导出 → 旧 3.0.2 目标降级、其 status/triage/export/audit 行归档 → 选版审查（第一轮 reject：
    `docs/releases/security.txt` 的 Sphinx `:cve:` 角色未过滤；修复后第二轮 **accept 并 frozen**）。
11. rack v3.1.13 目标（本版新增）：CVE-2025-46727 dossier（11 条证据）→ 独立漏洞复核 **A 级**
    （Ruby 3.2.3 red/green：3.1.13 接受 5000 参数/4,194,307 字节，3.1.14 抛 QueryLimitError，
    `runs/independent/rack_CVE-2025-46727_round1/`）→ 写入 1 漏洞/1 location/1 review/21 evidence/1 status
    → 候选 `disc2_7f2500f73d3836ead0e09463` 置 verified、补 triage → 全树导出 180 文件 + 审计导出
    → 旧 2.2.3 目标降级、其 status/triage/export/audit 行归档 → 选版审查 **accept 并 frozen**
    （2026-10-23）。
12. libexpat R_2_6_2 目标（本版新增）：CVE-2024-45490 dossier（10 条证据：OSV/NVD 原始记录、tag peel、
    fix commit 祖先关系、行号 grep、6 行 guard diff）→ 独立漏洞复核 **A 级**（两步 harness：负长度
    `XML_ParseBuffer` 后再 `XML_GetBuffer` 触发 ASan heap-buffer-overflow，R_2_6_3 修复版无崩溃，
    `runs/independent/libexpat_CVE-2024-45490_round1/`）→ 写入 1 漏洞/1 location/1 review/18 evidence/1 status
    → 候选 `disc2_35a922eb511ed468630f4a2d` 置 verified、补 triage → 旧 R_2_4_4 目标降级、其 143 条
    triage、7 条 status、export/audit 行归档 → 全树导出 199 文件 + P6 审计导出 → 选版审查 **accept 并 frozen**
    （2026-10-23）。同轮把 R_2_4_4 时代的 7 个旧 CVE 以修复区间 + 祖先关系判为 `confirmed_not_affected`。
13. phoenix v1.8.8 目标（本版新增）：旧 v1.6.13 仅因超过 4 年被拒，本次先在 v1.8.8 取得两个独立正样本
    —— CVE-2026-56811（8 条证据，独立静态复核 grade B，`16e295d2` 修复于 1.8.9）与 CVE-2026-56812
    （8 条证据，独立复核 grade A：Node red/green 在同一 tag blob 上 20/20 抛错、1.8.9 为 0/20，
    `runs/independent/phoenix_CVE-2026-56812_v188_round1/repro/`）→ `promote_verified_rows.py` 两次合并
    （各 1 漏洞/1 location/1 review/19 evidence/1 status）→ 候选 4 条置 verified、2 条置 rejected
    → 8 条 triage（2 个 CVE 各两条 discovery 路径 confirmed_affected；CVE-2022-42975、CVE-2017-1000163、
    CVE-2026-32689×2 confirmed_not_affected，均附代码级证据）→ 旧 v1.6.13 目标降级，其
    8 triage、2 status、export/audit、21 evidence、location、review 与 selection 行归档
    → 全树导出 478 文件 + P6 审计导出（排除 2 文件，剩余 0）→ 选版审查 **accept 并 frozen**（2026-10-23）。
14. netty 旧目标 4.1.59.Final 超 4 年 → 证据先行升级到 netty-4.1.137.Final（`5471f0a6`，2026-08-06）：
    独立复核 CVE-2026-93494 **B 级**（静态：`StompSubframeDecoder.decode` 在 155 行暂存 `lastContent`，
    `ReplayingDecoderByteBuf` 的 REPLAY 是 `Signal extends Error`，191-195 的 `catch (Exception)` 接不住，
    且无 `handlerRemoved0`，pooled ByteBuf 泄漏；8132 是 `maxChunkSize` 上限而非固定泄漏量）→ promote
    （1 vuln/1 location/1 review/22 evidence/1 status，`grade B` 因无 `reproduction_reference`）→
    旧 6 个正样本按修复 commit ancestor 判 `confirmed_not_affected`，旧 selection/export/audit/status/triage
    归档（vulnerabilities/locations/reviews/evidence 保持 live）→ 全树导出 3479 文件（sha256 `089a09be…`）
    + 审计导出（剩余 0、redacted 1）→ 审查包 `v031/reviews/selection_packets/1064563_netty__netty.json`
    → 独立选版审查 2026-10-23 发起（用户态 JDK 17 + Maven 3.9.16 全量 `mvn package` 已在本机 **BUILD SUCCESS**
    47 模块，审查者需从全新解包目录自行重建）。
15. guzzle 旧目标 7.4.4（2022-05）超 4 年 → 升级到 7.14.1（`6b1d2429`，2026-07-13）：独立复核
    CVE-2026-67339 **A 级**（`harness/` 红/绿：7.14.1 下 direct / no_proxy / SOCKS 三条路由都把
    `Proxy-Authorization` 发给源站，7.14.2 全部干净）→ promote（1 vuln/1 location/1 review/21 evidence/
    1 status）→ 旧两个正样本（GHSA-25mq-v84q-4j7r、CVE-2022-31091）按 `1dd98b05`（7.4.5）ancestor 判
    `confirmed_not_affected`，旧行归档 → 全树导出 119 文件（sha256 `3a53ce38…`）+ 审计导出
    （排除 CHANGELOG.md、redacted 3、剩余 0）→ 独立选版审查 **accept 并 frozen**（2026-10-23，
    审查者在全新目录用用户态 PHP 8.4.23 + composer 2.10.3 真实构建，1396 tests / 1 环境相关 failure）。
16. 2026-10-24 又 promote 四个独立复核正样本：gitea GHSA-hg5r-vq93-9fv6（A）、django CVE-2024-42005（B，
    `values()`/`values_list()` 经 JSONField key 的 SQL 注入，可达性需额外 aggregate 注解）、django
    CVE-2024-39329（A）与 gitea GHSA-7wvc-rvp7-w99x（A）。每次都是 dossier → 隔离 verdict →
    `promote_verified_rows.py --apply`；随后用带守卫的脚本把对应 triage 行改成 `confirmed_affected`
    （`runs/data_fixes/apply_promoted_candidate_*_2026-10-24.py`，先 dry-run、写备份）并把
    `independent_verdict_path` 从 `/tmp` 指到 `runs/independent/<packet>_round1/`
    （`persist_independent_verdicts_*_2026-10-24.py`，校验保留副本 sha256 与源一致）。
    本轮顺带修掉一处历史遗漏：hg5r 首次改写只改了 `disc2_*` 行，同快照的
    `adv3_d931ecfcc9a09dd2` 仍停在 `possible_affected`；用全表扫描（possible 行是否引用同快照已 promote
    漏洞）找出并一并改写，扫描后此类残留为 0。
17. 纠正一处来源标注错误：NVD source `134c704f-9b21-4f2e-91b3-4a467353bcc0` 是 **CISA-ADP** 容器而非
    GitHub CNA（42005 隔离复核者发现，并用数据集内部既有标注交叉确认）。三个 django dossier 已按此措辞
    重建；`data/vulnerabilities.jsonl` 中 CVE-2024-42005（本轮 promote）与更早的 CVE-2024-39330 仍写
    「GitHub CNA」，已由 `runs/data_fixes/fix_cisa_adp_attribution_2026-10-24.py`（守卫 source_url 与
    唯一子串、写备份）改为「CISA-ADP 容器，向量由 GitHub CNA 发布」。severity 数值与向量未变。
18. django CVE-2024-38875（4.2.13，urlize/urlizetrunc 的 `trim_punctuation` 二次方括号裁剪）
    卷宗 `runs/verification/django_CVE-2024-38875_4213/`（10 条证据）→ 隔离复核 **A 级**：
    reviewer 自建五棵 tag 树实测 N=100000 的 `"("*N + ":" + ")"*N`，4.2.13 9.86 s / 4.2.14
    0.003 s，模板过滤器路径同样复现，并做了 N=2000→100000 的二次缩放；修复提交
    `79f36876` 首见于 4.2.14，5.0.x 为 `72856446`（5.0.7）。verdict
    `runs/independent/django_CVE-2024-38875_4213_round1/verdict.json`。首轮 promote 因
    `fields_verified` 缺 `languages`（reviewer 用 `vulnerability_id` 充当第九项）被工具拒绝，
    请同一 reviewer 自行补核语言清单后重发（sha256 `a70331ce…`），再次 dry-run 通过后
    `--apply`（1 vuln / 1 location / 1 review / 29 evidence / 1 status）。
    triage 行 `disc2_051d93d5bd86570c8437b5dd` 与 review 路径分别由
    `apply_promoted_candidate_round3_*` / `persist_independent_verdicts_round3_*` 改写。
19. gitea GHSA-hg5r-vq93-9fv6 的复核产物在 promote 之后又被 reviewer 的后台收尾更新过一次：
    `NOTES.md` 增加 v1.26.2 全量 `hmac.New` 普查的两段说明，`sources/v1262_hmac_sites.txt`
    增加 4 行非 artifact 站点，verdict 中对应的两个 artifact sha256 随之更新。已把最终版本
    复制回 `runs/independent/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1/`，11 个 artifact
    sha256 全部重新匹配（`repro/main.go` 对应包内 `reproduction/main.go`）；结论未变
    （`confirmed_affected` / A / `f913d90a…`），`data/reviews.jsonl` 不存 verdict sha，无需改数据。
    新 verdict sha256 `529c1170…`。
20. django CVE-2024-39614（4.2.13，`get_supported_language_variant` 对连字符稠密语言码的
    二次方切片）卷宗 `runs/verification/django_CVE-2024-39614_4213/`（12 条证据）→ 隔离复核
    **A 级**：reviewer 在 PyPI 4.2.13/4.2.14 venv 实测 `"en-"*30000` 2.196 s（n=1k/3k/10k/30k
    缩放 0.0015/0.0185/0.2250/2.196 s），90,000 字符 cookie 路径 0.802 s，4.2.14 约
    0.000075 s；verdict sha256 `72a45407…`，24 项 artifact 全匹配。`--apply`
    （2026-10-23T23:33:31Z）追加 1 vuln / 1 location / 1 review / 31 evidence / 1 status。
    保留包 `runs/independent/django_CVE-2024-39614_4213_round1/`（verdict + NOTES + sources +
    scripts + repro，逐项 sha256 复核 0 不匹配）；review 路径与候选行
    `disc2_97b11946b732970b9a25004c` 分别由 `persist_independent_verdicts_round5_*` /
    `apply_promoted_candidate_round5_*` 改写。reviewer 指出 OSV GIT 区间无效（introduced 是
    2025/2026 security-archive 提交、fixed 只是版本号 bump），真实补丁是 `17358fb3` / `8e7a44e4`。
21. django CVE-2024-41989（floatformat 科学计数法指数内存耗尽）隔离复核 **A 级**后 promote
    （2026-10-23T23:32:12Z）：1 vuln / 1 location / 1 review / 29 evidence / 1 status，grade A；
    verdict sha256 `2e8eb95f…`。收尾用 `persist_independent_verdicts_round4_*`（指向
    `runs/independent/django_CVE-2024-41989_4213_round1/verdict.json`）与
    `apply_promoted_candidate_round4_*`（`disc2_1d98594ee81566538ecb96d2` →
    `confirmed_affected`）。两次 promote 后基线 **116 / 87**（A 41 / B 75），possible
    583、unknown 574、NA 1321。
22. django CVE-2024-41991（4.2.13，`urlize`/`urlizetrunc` 与 `AdminURLFieldWidget` 对超大
    Unicode 输入的 DoS）卷宗 `runs/verification/django_CVE-2024-41991_4213/`（12 条证据）→
    隔离复核 **A 级，`confirmed_affected`**：reviewer 实测 4.2.13 的 `"한.글."×1,000,000`
    （约 4 MB）在 email/http/www 三条 `urlize` 路径 10.86 / 10.97 / 11.41 s、widget 11.05 s，
    RSS 增量约 +200 MB，输出膨胀到 ~22.0 M 字符；4.2.15 同输入 0.043–0.050 s、RSS 增量 0，
    widget href 为空；4.2.14 在 n=100k 仍 1.0603 s，确认首发修复版本 4.2.15。verdict
    sha256 `709fce73…`，24 项 artifact 全匹配。`--apply`（2026-10-23T23:42:06Z）追加
    1 vuln / 1 location / 1 review / 31 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-41991_4213_round1/`（verdict + NOTES + feeds +
    scripts + out + 6 个被引用 venv 文件，逐项 sha256 复核 0 不匹配）；review 路径与候选行
    `disc2_3bb0bba7fbc37c8593e5441b` 分别由 `persist_independent_verdicts_round6_*` /
    `apply_promoted_candidate_round6_*` 改写。reviewer 指出 OSV GIT 事件哈希无效、NVD 7.5
    vs GHSA A:L、CWE-1333/ReDoS 归类与线性 IDNA 实测不符。当前基线 **117 / 88**
    （A 42 / B 75），possible 582、unknown 574、NA 1321。
23. django CVE-2024-41990 在 4.2.13 上**不可按已公布形态复现**，已记为探针
    `runs/verification/django_CVE-2024-41990_4213_probe/`（bench.py + 三份日志 + README，
    **不是卷宗、无裁定**）。`".;" * n` 在 4.2.13/4.2.14/4.2.15 的 n=200k 耗时分别为
    0.004674 / 3.271716 / 0.004906 s；4.2.14 每翻倍约 3.4×/4.1×（二次），另六种实体形态
    三版皆线性。机制：4.2.14 的 38875 修复（`79f3687642`，4.2.13 无、4.2.14 有）把
    `rfind("&")` + `unescape(middle[amp:])` 放进通用尾部剥离路径，4.2.15 的 41990 修复
    （`d0a82e26a7`，仅在 4.2.15）复用同一个 `amp`。故候选
    `disc2_0375e0e8d50b5f62dc5c2e03` **维持 `possible_affected`**：无复现不等于快照无其它
    trigger，未 promote、未写 `data/`。
24. django CVE-2024-45230 同样在 4.2.13 上**不可按已公布形态复现**，已记为探针
    `runs/verification/django_CVE-2024-45230_4213_probe/`（bench.py + 四份日志 +
    4.2.16 发布说明摘录 + README，**不是卷宗、无裁定**）。`"&" + ";:"*n` 在
    4.2.13/4.2.14/4.2.15/4.2.16 的 n=200k 耗时 0.005114 / 13.448057 / 13.108951 /
    0.006153 s；`".;"`/`";."`/`":;"`/`";::"` 同型，`"&" + ";"*n` 四版皆毫秒级。
    修复 `d147a8ebbd` 只在 4.2.16；4.2.14 的 38875 修复已引入该二次方，4.2.16
    发布说明亦写 “in 4.2.15”。候选 `disc2_91b14048e4ec3e3a627057a1` **维持
    `possible_affected`**：未 promote、未写 `data/`；4.2.13 的 urlize DoS 已由
    CVE-2024-38875 覆盖，但本条不据此改判 NA。

25. django CVE-2024-53907（4.2.13，`strip_tags()` 剥离循环无深度上限的二次方 DoS）卷宗
    `runs/verification/django_CVE-2024-53907_4213/`（13 条证据）→ 隔离复核 **A 级，
    `confirmed_affected`**：reviewer 自建 4.2.13/4.2.17 venv，`"<"*n + "a>"*n` 在
    n=1000/2000/4000/8000 分别 0.412 / 1.591 / 6.514 / 26.301 s（每翻倍约 4×，二次方），
    4.2.17 同 24 KB 在 50 轮上限处抛 `SuspiciousOperation`（0.334 s）；公共 `striptags`
    过滤器 25.603 s vs 0.342 s。verdict sha256 与保留包逐项复核 0 不匹配，`--apply`
    追加 1 vuln / 1 location / 1 review / 32 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-53907_4213_round7/`（verdict + NOTES + feeds +
    scripts + out + notes + 两个 venv 的 `utils/html.py`、`template/defaultfilters.py`
    与 METADATA，`preserved_sha256.txt` 24 项）；review 路径与候选行
    `disc2_8b86415747e9508ae2ac2940` 分别由 `persist_independent_verdicts_round7_*` /
    `apply_promoted_candidate_round7_*` 改写。reviewer 指出 OSV MODERATE 与 NVD/CISA-ADP
    7.5 HIGH 的标签差异（向量等价），并说明 4.2.17 在抛错前仍有至多 50 轮全串解析。
    基线 **118 / 89**（A 43 / B 75），possible 581、unknown 574、NA 1321。

26. django CVE-2024-53908（4.2.13，Oracle `HasKeyLookup.as_oracle` 把 lhs 参数拼进 SQL 文本）
    卷宗 `runs/verification/django_CVE-2024-53908_4213/`（13 条证据）→ 隔离复核 **A 级，
    `confirmed_affected`**：reviewer 自建 4.2.13/4.2.17 venv，compile-level 复现 payload
    `1, '$.foo') OR 1=1 --`：4.2.13 直接使用得到
    `JSON_EXISTS(1, '$.foo') OR 1=1 --, '$."foo"')`、params `[]`，经公开入口
    `QuerySet.filter(HasKey(Value(payload), 'foo'))` 同样内联；4.2.17 为
    `JSON_EXISTS(%s, '$."foo"')`、params 该 payload。`__` 控制路径（`value__has_key`、
    嵌套 `KeyTransform`、带引号 rhs）两版 SQL/params 逐字节相同。`compare_runs.py` 9/9
    断言通过。verdict sha256 与保留包逐项复核 0 不匹配，`--apply`（2026-10-24T00:10:17Z）
    追加 1 vuln / 1 location / 1 review / 32 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-53908_4213_round8/`（verdict + NOTES + feeds +
    scripts + out + notes + 两个 venv 的 `db/models/fields/json.py` 与 METADATA，
    `preserved_sha256.txt` 25 项）；候选行 `disc2_d997111c20cf6d0610292215` 由
    `apply_promoted_candidate_round8_*` 改写（review 直接指向保留包 verdict，无需 repoint）。
    reviewer 限制：无真实 Oracle 实例（compile-level 明确允许）、`oracledb` 仅以别名满足
    `cx_Oracle` 导入、tag 签名无法本地校验（改用 `git ls-remote`）、5.0/5.1 只查祖先未执行。
    基线 **119 / 90**（A 44 / B 75），possible 580、unknown 574、NA 1321。

27. django CVE-2024-45231（4.2.13，密码重置在邮件后端持续失败时泄漏地址是否存在）
    卷宗 `runs/verification/django_CVE-2024-45231_4213/`（13 条证据）→ 隔离复核 **A 级，
    `confirmed_affected`**：reviewer 自建 4.2.13/4.2.16 venv，用
    `django.test.Client(raise_request_exception=False)`、`DEBUG=False` 走真实
    `PasswordResetView`：失败后端下 4.2.13 对**存在且激活**的地址返回 **HTTP 500**
    （`ValueError: FailingEmailBackend is doomed to fail.`），对不存在/未激活/无可用密码的
    地址返回 302；4.2.16 四类全部 302，且仅存在地址产生 1 条 ERROR
    `Failed to send password reset email to 1`。改用真实 SMTP（127.0.0.1:1 关闭端口）仍
    复现 500 vs 302；locmem 对照两版全 302，证明差异由发信失败触发。位置
    `django/contrib/auth/forms.py` `PasswordResetForm.send_mail` 第 317 行
    `email_message.send()`（方法 295-317），入口 `password_reset` URL →
    `PasswordResetView.form_valid` → `save()` → `get_users()`。verdict sha256 与保留包
    逐项复核 0 不匹配，`--apply`（2026-10-24T00:16:15Z）追加 1 vuln / 1 location /
    1 review / 32 evidence / 1 status。保留包
    `runs/independent/django_CVE-2024-45231_4213_round9/`（verdict + NOTES + scripts + out
    + 两个 venv 的 `contrib/auth/forms.py` 与 METADATA，`preserved_sha256.txt` 36 项）；
    候选行 `disc2_00c12ead68ae4b95c2b982e6` 由 `apply_promoted_candidate_round9_*` 改写。
    reviewer 指出 NVD 描述把**已修复版本**写成 “discovered in”、GHSA CVSS 3.1 3.7（AC:H）
    与 NVD 5.3（AC:L）标签差异、Django 自评为 low；GitHub 仓库级 advisory 页匿名 404。
    基线 **120 / 91**（A 45 / B 75），possible 579、unknown 574、NA 1321。

28. django CVE-2025-64459（4.2.13，`Q`/`QuerySet` 的 `_connector` 关键字参数被字典展开
    带进 SQL 连接符）卷宗 `runs/verification/django_CVE-2025-64459_4213/`（14 条证据）→ 隔离复核
    **A 级，`confirmed_affected`**：reviewer 自建 4.2.13/4.2.26 venv，先以 sha256 确认 PyPI
    4.2.13 的 `query_utils.py`/`query.py`/`where.py` 与 tag commit 3bf46e2e 的 blob 逐字节一致，
    再跑红/绿：4.2.13 `filter(**{"name":"Alice","id":999,"_connector":" OR 1=1 OR "})` 生成
    `WHERE ("id" = %s  OR 1=1 OR  "name" = %s)`、params 仅 `[999,"Alice"]`，返回全部 3 行
    （合法 AND 查询 0 行）；`exclude()` 同载荷返回 0 行、`get()` 抛 `MultipleObjectsReturned`
    （匹配 3 行）、`Q(_connector="evil")` 被接受。4.2.26 同调用在构造 SQL 前抛
    `TypeError: The following kwargs are invalid: '_connector'`，`Q(_connector="evil")` 抛
    `ValueError: _connector must be one of 'AND', 'OR', 'XOR', or None.`，合法查询不变。位置
    `django/db/models/query_utils.py` `Q.__init__` 48-53（入口 `query.py`
    `_filter_or_exclude_inplace` 1457-1461，sink `sql/where.py` 171-172），4.2.x 修复
    `59ae82e6…` + 配套 `279f8b95…`（4.2.26，tag `0dfd59e2…`）。verdict
    `runs/independent/django_CVE-2025-64459_4213_round10/verdict.json`，`--apply`
    （2026-10-24T00:23:13Z）追加 1 vuln / 1 location / 1 review / 33 evidence / 1 status。
    保留包 18 件（verdict + NOTES + reproduction 三件 + fetch 五件 + 两个 venv 的三份 ORM
    文件与 METADATA，`preserved_sha256.txt` 全匹配）；候选行
    `disc2_d791407a54d5b84b33a8db28` 由 `apply_promoted_candidate_round10_*` 改写。
    reviewer 指出 GHSA/OSV 的 4.2 分支范围写作 introduced 0（枚举到 1.0.1）而 NVD/PYSEC
    从 4.2 起、Django 政策称 "high"、GHSA 漏列实际拦截 `filter(**dict)` 的配套提交
    `279f8b95…`、GitHub API 的 `cvss_v4` 为 null；限制为仅 SQLite、未跑全量测试。
    基线 **121 / 92**（A 46 / B 75），possible 578、unknown 574、NA 1321。

**未做（留给后续，别视为已完成）**
- 50 库冻结缺口：**46 frozen / 2 rejected（hyper、Newtonsoft.Json 的 legacy 目标）/ 2 未选版**
  （nlohmann/json、openssl/openssl）。
- （以下为历史节点，最终状态见 §4）6 个 legacy `documented_exception` 目标里，netty/guzzle 已升级；protobuf 已定新目标
  **v28.1（4.28.1，2024-09-10，CVE-2024-7254，区间 4.0.0-RC1→4.28.2）**，独立复核 A 级通过、
  已 promote 并完成导出/审计，独立选版审查进行中；gin 已定 **v1.9.0（2023-02-21，CVE-2023-29401）**，独立复核**已返回
  `confirmed_affected` / grade A**（审查者用 go1.27.3 做红/绿复现，线上头 v1.9.0
  `attachment; filename="setup.bat";x=.txt"` vs v1.9.1 转义版），已迁移旧目标并归档、promote
  （1 vuln/1 location/1 review/24 evidence/1 status）、导出 124 文件 + 审计导出
  （排除 CHANGELOG.md，剩余 0）；独立选版审查 **accept**（go build/vet/test 全 exit 0，
  124/124 文件 manifest 全量比对一致），已 frozen（2026-10-23，第 20 个 frozen）。
  审查者指出两处 collector 表述错误
  （CNA 为 CWE-20 而非 CWE-494；GHSA 实有 CVSS 3.1 4.3 向量），已在 dossier 记录。
  hyper / Newtonsoft.Json 经 OSV 逐版本查询确认**不存在窗口内可用的受影响版本**
  （hyper 最新受影响版 0.14.11 = 2021-07-21；Newtonsoft.Json 最新受影响版 13.0.0，13.0.1 已于
  2021-03-22 发布），故保留 `documented_exception`；证据见
  `runs/verification/documented_exception_evidence_2026-10-23/EVIDENCE.md`（「无已知 advisory」不等于安全）。
- 2 仓库未选版（Catalog 已验证漏洞为 0；不得编造 tag/commit；先补正样本再选版）。
- 574 unknown 中可能与 SHA 相关的候选未定向核验；两个未选版仓库的 13 条候选按先选版处理。
- `PASS_KNOWN_SWEEP=0/50`（需对固定 SHA 两轮独立检索均无新增「相关」候选，不只是无新增提升）。
- 90 条 grade A（按 `data/reviews.jsonl` 实测，全部在评测目标快照上；含 rexml/django 39330/django 39329/django 38875/django 41989/django 39614/django 41991/rack/libexpat/phoenix 56812/guzzle 67339/gin 29401/protobuf 7254/grpc 1428/cJSON 53154/cJSON 50472/cJSON 57052/gitea hg5r/gitea 7wvc/django 32873/django 57833/django 59682/django 48432/django 64460/django 26699/django 14550/django 2026-1285/django 2026-3902/django 2026-33034/django 2026-33033/django 2026-4292/django 48587/django 6873/django 2026-1312/django 2026-1287/django 2026-1207/django 2026-25674/django 2025-13372/django 2025-59681/django 2025-64458/django 2026-25673/rack 2025-49007/rack 2025-61772/rack 2025-61919/rack 2025-61780/werkzeug 49767/PHPMailer 3603/undici 24758/undici 30260/libexpat 32778/libexpat 32777/libexpat 32776/libexpat 24515 等，2026-10-25 复算），其余 live 正样本为 B 级静态验证（CVE-2026-15830 与 CVE-2026-53877 均为无执行环境的 B）。
  无 Agent 评测运行；运行时网络隔离尚未由 harness 实施（`network_policy=off` 只是声明）。
  `manifest.source_cutoff_date=null` 未复核。
- 审计导出是字符串级控制：不含 advisory ID 的修复说明/外链仍可能存在。另：collector 的泄漏扫描只匹配
  `CVE-`/`GHSA-`，不匹配 `GO-`/`RUSTSEC-`/`EEF-` 等 ID（gin 的 CHANGELOG.md 含 4 个 `GO-` 条目而未被计数，
  该文件整体被审计导出排除，故剩余 ID 仍为 0；后续仓库需注意同类漏检）。

## 4. 下一步优先级

1. **选版闭环已覆盖 48 个目标：46 frozen / 2 rejected（2026-10-24）**。近期完成闭环的证据先行案例：
   netty 4.1.137.Final、guzzle 7.14.1、echo v4.15.2、axios v1.19.0、gin v1.9.0、protobuf v3.25.4、
   grpc v1.52.0（独立审查者 CMake/Ninja 构建 `libgrpc.a` + 消费者链接运行后 accept）。历史记录：
   gin v1.9.0（CVE-2023-29401）已完成漏洞 A 级复核 → promote →
   导出/审计 → 独立选版 **accept → frozen**，全流程闭环；protobuf v28.1（CVE-2024-7254）
   dossier 已完成，独立复核已返回 `confirmed_affected` / A 级（4.28.1 实测 SOE，4.28.2 转 IPBE），
   14 条 discrepancy 已回落进 dossier（CWE-20/RubyGems 包/a037f28f 主分支修复/75-83 行号），
   旧目标已迁移归档、promote（1 vuln/1 location/1 review/77 evidence/1 status）、
   导出 2941 文件 + 审计导出（无排除、剩余 0）；独立选版审查对 checks 1-5 判 **accept**，但
   **`build_ok=false`**（`java/{core,lite,util,kotlin-lite}` 只发 `pom_template.xml`、树内无 protoc
   与生成源码；`third_party/abseil-cpp` 等 3 个 gitlink 被导出策略跳过），`apply_selection_review.py`
   据此标 `build_not_feasible`，v28.1 保持 rejected；已改用 v3.25.4（窗口内、`<3.25.5` 受影响、
   该 tag 仍带真实 `java/core/pom.xml`）作为可构建的替代目标：独立漏洞复核 A 级、迁移/promote/导出/审计完成，
   独立选版审查实测 `mvn -B install -Dmaven.test.skip=true` exit 0（JDK 17 + Maven 3.9.16 + protoc 25.4，
   7/7 模块成功，`build_ok=true`），`apply_selection_review.py --apply` 已 **frozen**（2026-10-23）；
   hyper / Newtonsoft.Json 已用 OSV 逐版本查询证明窗口内无可利用版本（见
   `runs/verification/documented_exception_evidence_2026-10-23/`），保留 documented_exception，
   不再尝试「改成最新版」。禁止直接把 tag 改成最新版。`source_cutoff_date` 已复核：数据内没有
   2026-10-21 之后发布的披露，但 coverage 截止不统一（rack 写 10-22，另 5 仓库 pass 4 在 10-22 运行），
   字段保持 null，见 `runs/cutoff_verification_2026-10-24/`。
   phoenix 可作为「旧 tag 被 4 年规则拒绝 → 在更新稳定 tag 上重新取证」的完整模板。
2. **剩余 2 个未选版仓库**：nlohmann/json 与 openssl/openssl。规则是先补至少一条 B/A
   `confirmed_affected` 再选版，禁止先选版本后补证据。已把两者全部 13 条 OSS-Fuzz OSV 记录
   （json 3 条、openssl 10 条）的 GIT 窗口与稳定 tag 做祖先映射
   （`runs/unselected_repo_evidence_2026-10-24/`，`check_windows.py` 可复现）：**0/13 个窗口内有稳定 tag**；
   凡从 `introduced` 之后可达的稳定 tag 全部已包含 `fixed` 提交——即没有稳定版本是在漏洞窗口内发布的。
   因此既拿不到「证据先行的受影响快照」，这些记录也不能给修复后 tag 提供正样本，维持 `needs_selection`，
   不得编造 tag/commit。解锁路径见该目录 README（ECOSYSTEM 版本区间含稳定 tag 的新 advisory、
   fix 落在两次发布之间的窗口、或有源码级对应的下游受影响版本）。
   rexml 是该流程的模板（`runs/verification/rexml_CVE-2025-58767/`）。
   `data/snapshot_proposals.jsonl` 现仅剩 2 条 `no_proposal` 行。
   **sinatra 第一轮已判负**：v4.1.1 + CVE-2025-61921 的独立复核用 MRI 2.5.9–3.2.0 与真实 gem 实测
   `split(/\s*,\s*/)` 为线性（正对照 `/^(a|a)*$/` 能测出指数），判 `not_affected`，未写任何数据行
   （`runs/verification/sinatra_CVE-2025-61921_v411/ROUND.md`）。改用 v4.0.1（`7dc5940e…`，2025-05-24，
   该树无 `host_authorization`）上的 CVE-2024-21510（X-Forwarded-Host 开放重定向，4.1.0 修复）。
3. **处理 unknown（现 574 行，其中 549 条是 2026-10-24 补入的无证据 unknown）**：范围/分支半程已完成并落地——`triage_range_scope.py` v1.1 对 1201 条
   unknown 生成提案（`runs/triage_range_scope_2026-10-23/proposals_v1_1.jsonl`），经独立审计
   （`runs/triage_range_scope_2026-10-23/audit/AUDIT.md`，568 条可执行提案 0 分歧、47 条抽样复核）后
   仅应用 `not_affected_range`：406 行 → `confirmed_not_affected`（版本区间判定，不声称祖先关系；
   见 `DISPOSITION.md`）。**未应用的 42 条 `out_of_scope_product` 全部保留 unknown**（审计判其归属规则不成立，
   CVE-2022-40281 是疑似假阴性）。当时剩余 1257 条 unknown 需要源码/差异级定向核验，相关但未过 B/A
   门槛的保留 `unknown`（不能判无效）。所有决策写回 `snapshot_candidate_triage.jsonl`。
   2026-10-24 追加：`triage_range_scope.py --include-untriaged` 对从未有 triage 行的候选生成 1662 条
   提案（`runs/triage_untriaged_2026-10-24/proposals.jsonl`），独立审计（`audit/AUDIT.md`）判
   280/281 条 `not_affected_range` 可应用、1 条 aspnetcore 实际落在受影响区间；实际只插入 **275**
   条（再剔除 5 条 actix monorepo 版本基准错误的行），未 triage 候选 887 → **592**，再补 5 条 actix crate 版本修正行 → **587**，aspnetcore 争议行改写为 `possible_affected` → **586**。
   另有 GIT 祖先判定（48 条，`runs/triage_git_ancestry_2026-10-24/`）：独立审计判 47 条可应用、
   1 条（OSV-2025-657）祖先规则不成立但结论另需代码级证据，已落盘 47 条 → unknown **748**。
   该库的 discovery_v3 仓库 advisory 解析已补入生成器：`runs/triage_v3_advisories_2026-10-24/`
   独立审计 119/119 CONFIRMED、verdict APPLY（exclude 为空），12 条 `not_affected_range` 已落地
   （7 条改写 + 5 条新增，unknown → 741）。其中 6 条依赖 registry/owner 前缀包的归属判定，
   严格字面口径下应退回 unknown，已在 LIMITATIONS 与批次 README 中声明。
   2026-10-24 低侧证明批次：`triage_range_scope.py` 加入与「高于每条上界」对称的「低于每条下界」证明
   （GHSA/OSV 65 条、NVD CPE 12 条）。两个独立审计批次判 56/65 与 9/12 可应用，共写入 **65** 行
   （33 改写 + 32 新增，确认 unknown → 708）。apply 后实测：562 条候选无 triage 行，其中 **549** 条属已选版
   仓库、13 条属两个未选版仓库。审计同时暴露并修掉了 4 个
   生成器缺陷（空合取 clause、`;` 分支、裸前导下界版本、exact-CPE 被当作下界）；随后为复核既有排除又修了
   4 个（`=` 等值 clause 双侧有界；不可比记录不得否决；粗粒度副本不得否决精确副本；
   排他上界包含性——OSV `fixed`/`limit`、NVD `versionEndExcluding`，快照恰等于修复版本即排除），
   单测 100 → **117** 项 OK。
   对 693 条既有范围行的复现复核（`runs/triage_strict_recheck_2026-10-24/`，默认 + strict 两种模式）：
   首轮默认 690/693、3 possible；第三个修复（`runs/triage_coarse_dup_2026-10-24/`）后
   **默认 693/693 仍提出同样排除、0 indeterminate、0 possible**；strict 689/693，差的 4 条是跨产品兄弟包
   （`openssl-src`、`jquery-rails` ×2、`DisCatSharp`，默认模式全为 NA）。
   3 条 rack 的根因是 `discovery_v3` 的 `vulnerable_version_range` 是 GitHub 扁平化渲染
   （`>= 0.4` / `>= 1.3.0` / `All`），修复版本在单独的 `patched_versions`；现在仅当同 advisory 的 OSV 副本
   给出完全相同的修复集合时丢弃该冗余投票，不据此构造边界。7 条均未改数据，
   逐条清单见上述两目录 README / `summary.json`。
   上界包含性修后对 1257 条 unknown 重跑得 63 条排除提案（46 条同前一批），新增 **17** 条
   （gitea v1.25.5 14、curl CVE-2023-38039、gin v1.9.0、plug v1.19.2），已打包
   `runs/triage_fixed_release_2026-10-24/proposals.jsonl` 送独立审计，**未应用**。
   随后补全漏斗：为已选版仓库内 549 条从未有 triage 行的候选追加 `unknown` 行
   （`runs/triage_untriaged_unknown_2026-10-24/`，只追加、不覆盖已应用决策），
   triage 2064 → **2613**、unknown 708 → **1257**，draft 校验仍 0 error / 49 warning。
   随后三批独立审计落盘：unblocked 36/46 CONFIRMED、fixed-release 17/17、GIT 10/12，共写 63 行；
   又撤回 vite/flask 2 行（裸版本读法被证伪），NA 1212 → **1273**、unknown 1257 → **1196**。
   全量复现复核（`runs/triage_range_recheck_full_2026-10-24/`）对 817 条范围排除：默认模式 **817/817**、
   strict 812/817（5 条跨产品兄弟包，含 spring-framework 的 spring-security 命中）。
   OSV-by-alias 批次（`runs/osv_alias_2026-10-24/`，四轮抓取 230 条记录）为 105 个无结构化证据的候选取得
   本仓库记录：43 条排除提案经独立审计 42 CONFIRMED / 1 REJECTED / 0 INCONCLUSIVE，42 条已落盘
   （被拒的 cJSON CVE-2023-26819 行保持 unknown，审计据 fix commit `a328d65a` 首次出现于 v1.7.19
   认为该 tag 可能实际受影响，列为正向复核优先项；该优先项已于 2026-10-24 做源码级复核：
   `runs/verification/cjson_CVE-2023-26819_v1716/` 证实修复提交不在 v1.7.16 祖先链、64 字节
   栈缓冲仍在，ASan/UBSan 实测 63 字符边界导致的长数字 `parse_error`，但无越界/DoS，故不升级为
   正样本、该行仍 unknown）、51 条区间命中已移入 `possible_affected`、
   9 条仍不可判定，其余 212 个候选无可获取的版本证据。
   随后把全量复核中 524 条仍 unknown 的 `possible_affected_range` 提案统一落盘
   （`runs/data_fixes/apply_remaining_possible_2026-10-24.py`，从提案证据重走 membership、
   跳过撤回 advisory 1 条、抽查 6 条核对区间）：**523** 条移入 possible。此后 5 条 cJSON v1.7.16
   候选经独立复核升为 `confirmed_affected`（CVE-2023-53154 3 条、CVE-2023-50472 2 条，见下），
   另 3 条重复 discovery 行（CVE-2023-50471 1 条、CVE-2024-45490 2 条）按同快照既有 A/B 记录链接为
   `confirmed_affected`（`runs/data_fixes/link_duplicate_candidates_to_verified_2026-10-24.py`）；
   2026-10-24 又有 4 条 cJSON v1.7.16 候选（CVE-2025-57052）经独立 A 级复核升为 `confirmed_affected`。
   CVE-2016-10749 的 NA 提案经隔离审计判 **REJECTED**（advisory 触发串已死，但快照仍有同一函数的
   另一条越界读，即已确认的 CVE-2023-53154），未落盘，该行保持 `possible_affected`；
   见 `runs/na_proposal_cjson_CVE-2016-10749_2026-10-24/audit_verdict.json`。
   该步骤完成时 unknown **574**、possible_affected **578**、confirmed_affected **112**、pending_relevant_triage **1152**（后续轮次已推进，见 §2 的现算值）。
   另将 817 行复核旁路产生的 8 条 unknown 行 NA 提案打包
   （`runs/triage_unknown_na_2026-10-24/`）送独立审计：**6 CONFIRMED / 2 REJECTED / 0 INCONCLUSIVE**，
   6 条（symfony v5.4.45 1、django 4.2.13 2、netty-4.1.137.Final 3）已落盘，NA 1315 → **1321**；
   两条 tomcat `below_lower` 被拒（证明与同源兄弟包 `tomcat-embed-core` 的下界矛盾），
   排除结论本身成立但需逐分支混合证明，生成器对称规则尚不能表达，两行保持 unknown。
4. **两轮独立快照限定检索**（GHSA/OSV/NVD/官方 advisory + fix diff），两轮零新增**相关**候选且公开库/上游均
   成功，才可声明 `PASS_KNOWN_SWEEP`。
5. 有预算才接 LLM：任何调用记入 `v031/ledger/model_calls.jsonl`（stage/model/input/output/cached tokens/
   cost_cny），再用 `cost_report.py` 复核预算（budget=500，warn 0.8，halt 1.0）。优先 rules-first → cheap model
   → escalate；单候选单阶段≤2 次 LLM，超转人工排队，绝不自动 rejected。

## 5. 常用命令（venv 已就绪，jsonschema 4.26.0）

```bash
cd /home/luchitong/work/repo-vuln-50-v031

# 校验（draft / release 门槛）
.venv/bin/python v031/scripts/validate_dataset.py . --draft --json-out v031/reports/VALIDATION_DRAFT.json
.venv/bin/python v031/scripts/validate_dataset.py . --json-out v031/reports/VALIDATION_RELEASE.json

# 源码导出 / 提案 / 审计导出 / 审查应用
.venv/bin/python v031/scripts/freeze_snapshots.py . --jobs 3
.venv/bin/python v031/scripts/propose_missing_snapshots.py . --jobs 4
.venv/bin/python v031/scripts/build_selection_review_packets.py .
.venv/bin/python v031/scripts/build_audit_exports.py .
.venv/bin/python v031/scripts/apply_selection_review.py . \
  --reviews v031/reviews/selection_review_2026-10-23.jsonl  # 默认 dry-run

# 单条 dossier 合并提升（需独立 verdict；默认 dry-run）
.venv/bin/python v031/scripts/promote_verified_rows.py . \
  --dossier runs/verification/rexml_CVE-2025-58767/dossier.json \
  --verdict runs/independent/rexml_CVE-2025-58767_round1/verdict.json

# 排对 / 漏斗（依据当前 triage）
.venv/bin/python v031/scripts/plan_snapshot_queue.py . --out v031/reports/queue.json

# 用既有证据重建初始 triage（改数据/候选后刷新）
.venv/bin/python v031/scripts/build_initial_triage.py . --checked-at 2026-10-22T00:00:00Z

# 费用
.venv/bin/python v031/scripts/cost_report.py v031/ledger/model_calls.jsonl --budget-cny 500 --out v031/reports/COST_REPORT.json

# 单测（v031/tests 不是包，discover 必须指定 -t，否则 ImportError；当前 117 tests OK）
.venv/bin/python -I -m unittest discover -s v031/tests -t v031/tests -v
```

## 6. 关键坑（必须知道）

- **GHSA 小写正则**：`v031/schemas/vulnerabilities.schema.json` 的 `vulnerability_id` pattern 必须是
  `^(GHSA-[0-9A-Za-z-]+|CVE-[0-9]{4}-[0-9]+)$`（小写 GHSA ID 真实存在）。初始补丁后 SHA256=
  `efa419ad698472bb4d97cad17966215fd0daf79644b681be5016271c12ac4265`。若此 schema 被覆盖成大写版，9 条真实
  ID 会校验失败，需重打补丁。
- **`validate_v02_reference.py`（v0.3 参考验证器）对 9 条小写 GHSA 误报**，与本版数据无关，别当数据错误。
- **校验器只做结构/引用/声明检查**，不验证漏洞真实性、修复版本或检索完整性。schema 通过 ≠ 漏洞实存。
- **legacy_discovery_coverage_v03.jsonl** 是 v0.3 旧全历史覆盖的档案副本（哈希 `6f8cda79…`）；当前
  `discovery_coverage.jsonl` 应全为 `NEEDS_REVIEW`，你需要重写为 `selected_snapshot_only` 模式才能过 release。
- **queue 的 DONE 是「可作为 recall 正样本」**，不是审毕；ARCHIVE 是「有证据归档」，P1_REVIEW 是 unknown。
- 费用工具不拦截调用；未接入网关时预算靠自觉记录，别声称「已强制封顶」。

## 7. 发布门槛速查（自 `v031/WORKFLOW.md` §P8）

- 50 库各一冻结 SHA、语言覆盖 ≥10 类、每目标正样本可定位+B/A 审核。
- 该 SHA 所有候选均有 triage；`possible_affected/unknown` 必须深核或明确保持 draft。
- `PASS_KNOWN_SWEEP` 指固定快照两轮零新增相关候选（非零新增提升）。
- 不再要求每条历史 CVE 有 snapshot_vulnerability_status 行；未解决历史候选保留但不自动阻塞。

## 8. 交付物清单（本版已完成，勿重建）

`README_V031.md`、`LIMITATIONS_V031.md`、`SELECTION_REPORT_V031.md`、`CANDIDATE_FUNNEL_V031.md`、
`MIGRATION_AND_VALIDATION_V031.md`、`docs/RESUME_V031.md`、`UPGRADE_REPORT.json`、`cost_policy.json`、
`v031/reports/{VALIDATION_DRAFT,VALIDATION_RELEASE,queue_P3,COST_REPORT}.json`、`v031/reports/SELECTION_TABLE.md`。