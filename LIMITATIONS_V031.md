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

- 48/50 仓库有评测目标，其中 46 个已 `frozen`（2026-10-23～2026-10-24 逐个通过隔离选版审查 `accept`，
  最新一个是 grpc/grpc v1.52.0：独立复核标签、导出完整性、审计包、正向锚点，并真实构建 `libgrpc.a` +
  消费者链接运行）；其余 2 个 legacy `documented_exception` 目标（hyperium/hyper、JamesNK/Newtonsoft.Json）
  仍为 `proposed`，其独立选版审查结论为 `reject`，如实保留，不冒充已批准目标。
  全部 `leakage_controls` 仍为
  `worktree_without_git_history=false / ground_truth_isolated=false / network_policy=uncontrolled`（迁移默认，
  非已验证隔离方案）。
- 2 个仓库 `evaluation_snapshot_id=null`：nlohmann/json 与 openssl/openssl。两者的漏洞窗口内没有可用稳定
  发布 tag（只有预发布 tag 或窗口内无 tag），按 v0.3.1 规则不可自动选，亦不得编造 tag/commit。
- 187 条漏洞行全部有审核记录：77 条 B 级 + 110 条 A 级（2026-10-26 round76 后按表复算）；其中 158 条属于
  48 个评测快照并各有 `confirmed_affected` 状态行，29 条 catalog 行位于非评测快照/历史 tag。A 级要求独立 reviewer 动态
  red/green（如 grpc CVE-2023-1428 在 v1.52.0 `GPR_ASSERT(x == kTrailers)` SIGABRT、v1.53.0 同字节
  不 abort）；B 级不等于 PoC 已验证。
- 正式 Oracle（`snapshot_vulnerability_status`）的 158 行只覆盖评测快照中的已确认正样本，无
  `confirmed_not_affected/unknown/out_of_scope` 行。「没有 unknown」不等于「该 SHA 无其他漏洞」：
  未收录漏洞受检索与相关性筛选缺口限制。

- `data/reviews.jsonl` 的 `reviewer` 字段是采集方自述，`promote_verified_rows.py` 原样写入
  dossier 的 `prepared_by`，因此 43 行仍写着「independent reviewer not yet assigned」，
  即使同一行的 `independent_reviewer` 与 `independent_verdict_path` 已指向真实隔离裁定。
  判定以 `independent_reviewer` / `independent_verdict_path` / verdict 原件为准；本版未批量
  改写这些叙述字段（改写 review 行需单独守卫与备份），作为已知元数据瑕疵记录在此。
- nlohmann/json 与 openssl/openssl 在 Oracle 中无行，是 `needs_selection`，不是「无漏洞」；
  2026-10-24 已把两者的 13 条 OSS-Fuzz OSV 记录（只有 GIT 提交对）与 44 / 136 个稳定 release tag
  做祖先映射（`runs/unselected_repo_evidence_2026-10-24/`）：**0/13 个窗口内有稳定 tag**，且凡包含
  `introduced` 的稳定 tag 全部已包含 `fixed`——没有稳定版本在漏洞窗口内发布，因此无法提供先于选版的
  正样本；两库维持 `needs_selection`。hyper 与
  Newtonsoft.Json 各有 1 行正样本，但其选版未获独立审查批准，不得作为已验证评测目标引用。

## 3. 候选漏斗完整性

- 2626 条候选 → 2613 条 triage 行：191 confirmed_affected / 1329 confirmed_not_affected /
  491 possible_affected / 574 unknown / 28 duplicate（决策来自既有证据与独立复核，零 LLM）。
  2613 = 2064（截至范围判定批次）+ 549 条为「已选版仓库内此前从未有 triage 行的候选」补的 unknown 行
  （`runs/triage_untriaged_unknown_2026-10-24/`，逐行核对 snapshot 等于当前 evaluation_target），
  仅为漏斗补全，**不构成核验**。
- 1329 条 confirmed_not_affected 的依据是既有驳回卷宗里的版本/分支区间（如「fix already in <tag>」「introduced
  after <tag>」）、cached OSV 范围与 GIT 修复提交祖先关系，非裸 semver 字符串比较；仍属规则层判断，
  未逐条做独立源码复核。其中 1 条（django CVE-2026-53878）是符号缺失级源码复核（4.2 分支不含
  `DomainNameValidator`，24 件钉住产物见 `runs/verification/django_CVE-2026-53878_4213_absent/`），
  不依赖版本序。round70 另有 6 条 undici v5.19.0 候选同属符号缺失级排除（permessage-deflate、
  retry 拦截器、`qsUnescape`、SOCKS 代理在冻结 SHA 上不存在，另一条的 advisory 区间本就不覆盖
  5.19.0；`runs/verification/undici_v5.19.0_not_applicable_round70/`），同样不依赖版本序，且**没有**
  对应的运行时复现。round78 的 1 条 undici v5.19.0 候选（CVE-2026-12151）是源码 + 运行时双重依据的
  机制级排除：advisory 点名的 CONTINUATION 帧在冻结 SHA 上逐帧交付并清空分片表，累积只从 v6.17.0
  （`38c8b55c`）开始，15 次本地探针在 5.19.0 / 6.16.1 上堆增量均为 +0.9 MB、6.17.0 起 0 消息且
  +22.7 MB @200k；同一 harness 的镜像形状（连续 FIN=0 TEXT 帧）在 5.19.0 确实无界增长（+45.0 MB
  @400k），已作为未决事项记录、**不计入**本 CVE（`runs/verification/undici_v5.19.0_CVE-2026-12151/`）。
  round71 由 1 条 undici v5.19.0 候选（CVE-2026-11525，Set-Cookie `SameSite` 子串
  匹配，独立复核 A 级；5.15.0/5.19.0/5.29.0/6.26.0/7.27.0 红，6.27.0/7.28.0/8.5.0 绿）转入
  `confirmed_affected`；复核员同时指出该 CVE 的 NVD 记录自相矛盾（`affectedData` 写 `0 < 6.26.0`、
  描述写 "upgrade to v6.26.0"，而同一记录的 CPE 与 OSV 都是 6.27.0，运行时探针证实 6.26.0 仍红），
  卷宗以 OSV + git 祖先 + 运行时为准，分歧记入
  `runs/independent/undici_v5.19.0_CVE-2026-11525_round71/NOTES.md`。round72 由 1 条 undici v5.19.0 候选
  （CVE-2026-16729，`setCookie()` 对 caller 提供的 `domain`/`unparsed` 不做字符集校验、`;` 可注入额外属性，
  独立复核 A 级；5.19.0/5.29.0/6.27.0/7.28.0/8.8.0 红，6.28.0/7.29.0/8.9.0 绿）转入 `confirmed_affected`；
  复核者另记 4 处分歧（dossier `languages` 只记 JavaScript、未列 `deps/llhttp` 下 C 源；fix commit 时间原标成
  author date 而 committer date 更晚；patch-id 依赖默认算法、`--stable` 值不同；标题 "domain / path / unparsed"
  易被读成 path 也是 `;` 向量，实际 v5.19.0 的 `validateCookiePath` 已拒 `;`，path 只是接受 `>0x7E`）。
  另有 3 条 undici 候选
  （CVE-2026-109383 / CVE-2026-109932 / CVE-2026-87018）的 triage `basis` 引用了一个在 OSV 与
  GitHub 上都不存在的 GHSA id（对应 CVE 记录的 `aliases` 仍指向该 id）；区间数字可由 CVE 记录复现，
  故**不**据字面 id 改判，证据与说明在
  `runs/verification/undici_v5.19.0_alias_ghsa_404_round72/`。round73 由其中 1 条
  （CVE-2026-109932 / 同一 404 GHSA id，WebSocket receiver 对每个 PING 无条件回 PONG、不读
  `writableLength`/`writableNeedDrain`，独立复核 A 级；桩 socket 矩阵 5.15.0/5.19.0/5.29.0/6.29.0/7.30.0/8.12.1
  红、6.29.1/7.30.1/8.12.2 绿、5.14.0 无该模块，真实 `net.Socket` 20 万次 PING 下 v5.19.0 写队列 23.4 MB /
  RSS +181 MB 而修复版 16.5 KB）转入 `confirmed_affected`；复核员另记 4 处分歧（dossier 曾断言 OSV 不提供
  `severity[]`，实际提供且向量即来自该字段，已按复核意见改正并重建卷宗；`languages` 只记 JavaScript；
  严重度 `source_url` 指向 NVD 而权威来源是 CNA；OSV 受影响版本清单漏列 5.29.0），原始分歧保留在
  `runs/independent/undici_v5.19.0_CVE-2026-109932_round73/verdict.json`；该 GHSA id 在
  `api.osv.dev` 与 GitHub 上仍为 404，另有 2 条同现象候选（`adv3_073211b490d13d91`、
  `adv3_b09d54c52de7f879`）保持 `possible_affected`。round76 先由其中 1 条
（`adv3_073211b490d13d91`，CVE-2026-109383：`Agent` 构造函数把 `tls` 选项交给 `util.deepClone`
（`lib/core/util.js:146-148`，`JSON.parse(JSON.stringify(obj))`），函数值静默丢失，
`checkServerIdentity` 永不调用，独立复核 A 级、CWE-295）转入 `confirmed_affected`：复核者自建非 shallow
clone 与九棵 worktree、自有 CA 与叶证书，九版 × 八模式 72 次运行全部 rc=0——带
`tls:{ca,servername,checkServerIdentity}` 时 v5.19.0 / v5.28.5 / v5.29.0 / v6.29.0 / v7.30.0 / v8.12.1
回 HTTP 200 且回调调用 0 次，v6.29.1 / v7.30.1 / v8.12.2 以回调自己的 Error 拒绝且恰好调用 1 次；
`kOptions` 内省显示 RED 版 `kOptions.tls` 丢了函数、GREEN 版在，`default`（无回调）与 `tls_noca` /
`tls_badname` 两条负控证明 RED 的成功是「对端通过 Node 默认链与主机名校验」而非校验被关闭；上游三测试
在 6 个 pre-fix 版本 2 pass / 1 fail、3 个 fixed 版本 3 pass / 0 fail；OSV 的三个 `fixed` 标记就是三个
发版 tag commit，**5.x 线无任何修复**（58 个数字 v5.* tag 无一含修复提交，v5.29.0 实测仍红）；
canonical 取 CNA 7.4 HIGH，NVD 9.1 原样保留。复核者同时收紧影响口径：这是「函数值 tls 选项被静默丢弃、
本应被拒绝的对端被接受」，证据不足以直接称任意 MITM。该 GHSA 在 OSV 与 GitHub 全局仍 404，内容取自
仓库安全公告 API（200）与 CVE 记录；原始分歧保留在
`runs/independent/undici_v5.19.0_CVE-2026-109383_round76/verdict.json`。
round75 再由 1 条 undici v5.19.0 候选
  （CVE-2025-47279，`Pool` 对连接不可恢复失败的 client 永不移除、CWE-401，独立复核 A 级）转入
  `confirmed_affected`：复核者自建七棵 worktree 与自写真实 TLS 探针，并发失败 N=50 / N=200 时
  v5.19.0 / v5.28.5 / v6.21.1 / v7.4.0 的 `pool[kClients].length` 为 51 / 201，v5.29.0 / v6.21.2 /
  v7.5.0 为 1，合成 `connectionError` 后 GREEN 归 0；顺序失败在 RED 也不累积，且复用探针显示首轮建出的
  21 个 client 之后每轮新建 0 个——保留量在首轮并发峰值后饱和、**不随重试次数增长**，N=1000 的
  drop-retained 实验约 1.5 KB/client、RSS 不回落但**无 OOM**，故该行只支持下述影响口径：对象保留
  （CWE-401），不是内存耗尽；上游回归测试在 4 个 RED 版本 1 pass / 1 fail（case 2 `2 !== 0`）、
  3 个 GREEN 版本 2/2 pass。复核者另记三处差异：上述影响表述应收紧、暖池基线 2 个 client 来自
  `PoolBase[kDispatch]` 的同步补位（与缺陷无关）、以及它与采集侧上游记录仅 NVD `timestamp` 与
  OSV key 顺序不同。原始分歧保留在
  `runs/independent/undici_v5.19.0_CVE-2025-47279_round75/verdict.json`。round74 先把 1 条 undici v5.19.0
  候选（CVE-2026-22036，`Content-Encoding` 声明多少层就建多少个解压器、无上限，CWE-770）转入
  `confirmed_affected`：复核者自建九个 worktree 与自写 harness，在 15,017 字节 header（仍低于默认
  16 KiB `maxHeaderSize`）、N=3000 层嵌套 gzip 下，v5.19.0 / v5.29.0 / v6.22.0 / v7.17.0 分别耗时
  180.5 / 192.7 / 203.1 / 201.1 s 且 RSS +229–247 MB，而 v6.23.0 / v7.18.0 / v7.18.1 / v7.18.2 / v8.0.0
  在 13–21 ms 内以「too many content-encodings … maximum allowed is 5」拒绝、N=5 仍正常解压；成本超线性
  （嵌套 gzip 每层重复处理内层，约 O(N²)），非单纯线性放大。复核者另记：7.x 的可选启用 decompress
  interceptor 是第二条路径、直到 7.18.2 才修，故包级区间取 `>=7.0.0,<7.18.2` 正确；`ulimit -v`
  受限实验失败（5.x 的 WASM llhttp 无法分配实例内存）故不作为 OOM 证据；`languages` 未计
  `deps/llhttp` 的 C 源；git 可推导的字段之外 `snapshot_id` 只能采信。原始分歧保留在
  `runs/independent/undici_v5.19.0_CVE-2026-22036_round74/verdict.json`。其中 65 条来自 2026-10-24 的低侧证明批次（`runs/triage_low_side_2026-10-24/`
  56 条 + `runs/triage_low_side_nvd_2026-10-24/` 9 条，独立审计 56/65 与 9/12 可应用，其余 9 条被排除，
  见两目录 README 与 `audit/AUDIT.md`）：证明形式是「快照版本严格低于该 advisory 所拥有区间的每一条
  下界」，与既有的「高于每条上界」对称，同样只是版本序判断而非代码审计。另 275 条来自 2026-10-24 对「无 triage 行候选」的提案批次（独立审计
  280/281 可应用，本批只写入 275 条：剔除 1 条审计认定实际落在受影响区间的 aspnetcore 行，以及
  5 条 actix monorepo 版本基准错误的行，见 WORK_LOG）；另有 47 条来自 GIT 祖先批次
  （`runs/triage_git_ancestry_2026-10-24/`，独立审计判 47/48 可应用，1 条 OSV-2025-657 因
  `introduced` 仅改 CI 文件而保留 unknown）；再 12 条来自 discovery_v3 GitHub repository advisory
  批次（`runs/triage_v3_advisories_2026-10-24/`，7 条改写 + 5 条新增，独立审计 119/119 CONFIRMED、
  verdict APPLY 且不排除任何 claimant）。另 42 条来自 OSV-by-alias 批次
  （`runs/osv_alias_2026-10-24/`，独立审计 42 CONFIRMED / 1 REJECTED / 0 INCONCLUSIVE；被拒的
  cJSON CVE-2023-26819 行保持 unknown）。该批次有 6 条依赖「包名带 registry/owner 前缀但版本线跟随
  仓库 tag」的归属判定（`guzzlehttp/guzzle`、`rails/rails`、`symfony/symfony` 等）：按严格字面口径
  （归一化相等或 Go module path 尾段）会被判无归属，下游若采用严格口径应把这 6 条退回 unknown，
  详见该目录 README 的 ownership 一节。另 6 条来自 8 条 unknown-NA 提案批次
  （`runs/triage_unknown_na_2026-10-24/`，独立审计 6 CONFIRMED / 2 REJECTED / 0 INCONCLUSIVE：
  symfony v5.4.45 1 条、django 4.2.13 2 条、netty-4.1.137.Final 3 条；两条 tomcat 9.0.98 被拒，
  保持 unknown，见下文同源兄弟包一节）。rexml 的 8 条
  （7 个 distinct CVE + 1 条重复 advisory）与 libexpat 的 7 条（R_2_4_4 时代的 2022 系列 CVE）另加完整
  clone 中修复 tag/fix commit 的祖先关系验证；phoenix 新快照的 4 条排除行另加代码级核对
  （`validate_local_url/1`、`compare_host?/2`、`long_poll.ex` 的惰性 splitter）；但都仍是排除性证据，
  不证明快照无其他漏洞。
- 574 条 `unknown` 是「未在此零 LLM 阶段确立对冻结 SHA 的相关性」，**不是证明无漏洞**；必须继续核验相关疑点，
  否则保留 draft。django/django 2 条、libexpat/libexpat 34 条、rack/rack 0 条仍在 unknown；三仓库其余候选
  已有范围/代码级决策，区间命中的一律记入 `possible_affected`（django 27、rack 21、libexpat 36），仍需源码复核。
  phoenix 的 8 条候选已全部有新快照上的决策，不再保留 unknown。
  另有 549 条是 2026-10-24 补入的「此前无 triage 行」候选（`checked_at=2026-10-24T05:30:00Z`），
  与其余 unknown 一样未经核验。
- 当前 574 条 `unknown` 的生成器提案：529 `indeterminate`、42 `out_of_scope_product`、2
  `not_affected_range`、1 `possible_affected_range`。8 条 NA 提案取自 817 行复核的旁路输出
  （`runs/triage_unknown_na_2026-10-24/`），其中 6 条经独立审计 CONFIRMED 后已落盘，2 条 tomcat
  被拒、保持 unknown（见下条）；那 1 条 possible 是已撤回的 express advisory
  （`adv3_087476da78c375b4`），保持 unknown。42 条 alias 排除落盘前（当时 622 条）按提案归因的阻塞
  分布是：包不匹配 170、NVD 归属未定 161、无法细分的 other 155、包不匹配+生态不支持 107、事件不可读
  19、生态不支持 1——落盘的 42 条全部来自这批 indeterminate，`out_of_scope` 42 条未变；没有一行是
  「生成器完全看不到」。
- 同源兄弟包问题：8 条提案中的两条 tomcat `below_lower` 只读取了候选查询的
  `org.apache.tomcat:tomcat-catalina`，而同一 OSV 记录里的 `tomcat-embed-core`（同一源码树、同一
  9.0.98 发布，Maven Central POM 同指 tomcat.apache.org）带有 `9.0.0.M1`/`8.5.83`/`9.0.40` 等下界
  低于快照的分支。独立审计据此判**两条均 REJECTED（as stated）**：排除结论本身为真（CVE-2024-56337
  中 9.0.98 恰为排他性 `fixed`，CVE-2022-45143 中 9.0.98 高于 8.5.84/9.0.69 且低于 10.1.0），但
  正确论证是逐分支的混合证明（部分 above_upper、部分 below_lower 或与 `fixed` 相等），而生成器的
  对称规则只接受「全部 above_upper」或「全部 below_lower」。两条因此保持 unknown；如需落盘，须先让
  生成器支持按分支拆分的混合证明并重新送审，不得按原证明形式改写。反向的例子：strict 模式在
  angular/angular 19.2.15
  （`disc2_22f75256623aa38c50a68574`）上的 possible 命中来自 `@angular/ssr`，npm 元数据指向
  `github.com/angular/angular-cli`（不同仓库），该行**不**升为 possible。兄弟包是否同源必须按包注册表
  元数据判定，不能只看名字。
- 491 条 `possible_affected`（2026-10-26 round86 后复算；每轮独立复核确认即转出，最近 round43 由 542 降至 540、round44 由 540 降至 538、round45 由 538 降至 536、round46 由 536 降至 535、round47 由 535 降至 534、round48 由 534 降至 533、round49 由 533 降至 532、round50 由 532 降至 531、round51 由 531 降至 529、round52 由 529 降至 528、round53 由 528 降至 527、round54 由 527 降至 526、round55 由 526 降至 525、round56 由 525 降至 524、round57 由 524 降至 523、round58 由 523 降至 522、round59 由 522 降至 521、round61 由 521 降至 520、round63 由 520 降至 519、round65 由 519 降至 518、round66 由 518 降至 517、round64 由 517 降至 516、round67 由 516 降至 515、round68 由 515 降至 514、round70 由 514 降至 508 且其中 6 条是源码级功能缺失排除而非独立运行时复核、round69 由 508 降至 507、round71 由 507 降至 506、round72 由 506 降至 505、round73 由 505 降至 504、round75 由 504 降至 503、round74 由 503 降至 502、round76 由 502 降至 501、round78 由 501 降至 500 且该条有源码 + 运行时双重依据、round77 由 500 降至 499 且该条经隔离独立复核员以自建 clone + harness 实测 grade A 后转 confirmed_affected、round80 由 499 降至 498 且该条经隔离独立复核员自建 clone、对拍 rubygems `.gem` 并做运行时红/绿实测（grade A）后转 confirmed_affected、round79 由 498 降至 497 且该条经隔离独立复核员自建 clone 与同 tick harness 实测 v5.19.0 30/30 红、v6.27.0 0/10 与 v7.28.0 0/25 绿（grade A）后转 confirmed_affected，该轮复核启动早于 round80 而入库晚于 round80、round81 由 497 降至 496 且该条经隔离独立复核员自建 clone 与 9 个 per-tag worktree、两种 harness 每版每形态 3 进程红/绿实测（grade A）后转 confirmed_affected、round82 由 496 降至 495 且该条经隔离独立复核员自建 clone 与 9 个 per-tag worktree、自写 harness 每版 5 场景 × 3 进程并逐字重跑上游回归用例（grade A）后转 confirmed_affected、round83 由 495 降至 494 且该条经隔离独立复核员自建 clone 与 9 个 per-tag worktree、自写 harness 三种 crafted 构造（通配 / 捕获组反向引用 / 字符类）每版 3 进程并逐字跑上游回归用例（grade A）后转 confirmed_affected、round84 由 494 降至 493 且该条经隔离独立复核员自建 clone 与 10 个 per-tag worktree、自写 harness 每版 3 进程（六个恶意 host + 五个合法对照）并重放上游 pre/post-fix 两版回归正文（grade A）后转 confirmed_affected、round85 由 493 降至 492 且该条经隔离独立复核员自建 clone 与 9 个 per-tag worktree、自写 fixture 与两种独立 HTML 解析器（Ruby tokenizer + Python html.parser）每版 3 进程、27 份 body 交叉校验并重放上游 pre/post-fix 两形断言（grade A）后转 confirmed_affected、round86 由 492 降至 491 且该条经隔离独立复核员自建 clone 与 9 个 per-tag worktree、自写 harness 160/160 自检、每版 3 进程并做 ObjectSpace 分配计数与 Rack::Files 端到端 206 multipart 对照（grade A）后转 confirmed_affected）只是「已发布的机器可读区间包含冻结 tag」，**不是已确认漏洞**：
  2026-10-24 落盘批次时该表的成分是 30 条来自早期
  triage，45 条于 2026-10-24 由 OSV-by-alias 区间命中移入（`runs/osv_alias_2026-10-24/`，如 expat
  R_2_6_2 落在 CVE-2024-45490/91/92 的 `fixed 2.6.3` 之下、cJSON v1.7.16 落在 CVE-2025-57052 的
  `[1.5.0, last_affected 1.7.18]`），521 条由当前生成器的 `possible_affected_range` 提案统一落盘
  （`runs/data_fixes/apply_remaining_possible_2026-10-24.py`）；此后每有独立复核确认即转入
  `confirmed_affected`，故各成分之和不等于当前行数。其中一部分来自粗粒度渲染
  （`<= 1.27.2`、`All versions`），命中偏保守，源码复核时应优先看；撤回/驳回的 advisory 不参与
  （express `adv3_087476da78c375b4` 保持 unknown）。其中 5 条 cJSON v1.7.16 候选（CVE-2023-53154 ×3、
  CVE-2023-50472 ×2）已于 2026-10-24 经独立复核升为 `confirmed_affected`，另 3 条是已确认漏洞的重复
  discovery 行（cJSON CVE-2023-50471、libexpat CVE-2024-45490 ×2），已按既有 A/B 记录链接为
  `confirmed_affected`；其余全部待源码级复核。
  按「命中 tag 的那条边界」分类（`runs/possible_review_queue_2026-10-25/`，2026-10-26 round86 后按当前 491 行重跑）：双侧区间 325、
  只有上界/`All versions` 80、NVD CPE 21、alias OSV 35、早期 triage 30；队列已按仓库与证据质量排出，
  但**没有任何一条**因入队而被提升或排除。django CVE-2024-42005、CVE-2024-39329、CVE-2024-41991、
  CVE-2025-13372、CVE-2025-59681、CVE-2025-64458、CVE-2026-25673、CVE-2026-15307、CVE-2026-53877、
  CVE-2026-15830 与 gitea
  GHSA-hg5r-vq93-9fv6、GHSA-7wvc-rvp7-w99x（2 条行）分别经独立复核离开 possible；此外
  hg5r 首次改写遗漏的同快照 `adv3_*` 行已用全表扫描（possible 行是否引用同快照已 promote 漏洞）补齐，
  扫描后此类残留为 0（本次 41991 改写后重跑仍为 0）。
- 317 条 unknown 候选在既有缓存中没有任何可排序的版本证据。2026-10-24 按公开 advisory 别名从 OSV
  抓取四轮共 230 条记录（`runs/osv_alias_2026-10-24/`）后，105 条取得本仓库记录：**43 条排除提案经
  独立审计为 42 CONFIRMED / 1 REJECTED / 0 INCONCLUSIVE，42 条已落盘**（`reviewed_by` 指向
  `runs/osv_alias_2026-10-24/audit/AUDIT.md`）、51 条区间命中已移入 possible_affected（其中 2 条 cJSON
  v1.7.16 候选后经独立复核升为 confirmed_affected，见下文 CVE-2023-53154 一节）、9 条仍不可判定；
  其余 212 条**没有可获取的版本证据**（别名 404，或记录只有 GIT/发行版范围），保持 unknown。
  被拒的那条是 cJSON `v1.7.16` / CVE-2023-26819：审计发现公开 CPE 的精确点 1.7.15 低估了范围
  （修复提交 `a328d65a` 首见于 `v1.7.19`，`v1.7.16`/`v1.7.18` 仍含原代码，Debian 首个修复包为
  `1.7.18-3.1+deb13u1`），故该行**保持 unknown**——驳回排除不等于确认受影响，未作正向结论。
  随后的源码级复核（`runs/verification/cjson_CVE-2023-26819_v1716/`）确认：修复提交
  `a328d65a`（"allocate memory for the temporary buffer"，提交信息点名该 CVE）**不是** `v1.7.16`
  的祖先，`parse_number` 的 64 字节栈缓冲（`749fefc`，2017-04-08 引入，故 1.7.15–1.7.18 全系列
  都有）在快照中存在；ASan/UBSan 下用 CVE 给出的 64 位数字载荷实测，v1.7.16 对数组内的长数字
  `parse_error`、v1.7.19 `parsed ok`，边界正是 63 字符拷贝上限。**但没有任何越界/内存安全错误**：
  循环在 `i=63` 停止并写终止符，缺陷表现为「合法 JSON 被拒或被截断」，未复现出 advisory 所称的
  DoS，故不升级为 `confirmed_affected`，也不据公开区间判 `confirmed_not_affected`；该行仍为 unknown。
  该批的排除结论依赖 OSV 自动抽取的 `extracted_events`；
  审计逐行重抓了 28 个别名并比对实时记录，结构一致。
- cJSON CVE-2023-53154 是首个由 `possible_affected` 经完整正向流程升为 `confirmed_affected` 的案例
  （`runs/verification/cjson_CVE-2023-53154_v1716/` 卷宗 + `runs/independent/cjson_CVE-2023-53154_v1716_round1/verdict.json`
  独立裁定，grade A，reviewer 与卷宗 `prepared_by` 不同；三条候选行
  `disc2_42a2b668d6d1d627553d3f5d`/`disc2_84c9f51b7d1891828c9fa21b`/`disc2_43346aec2ac92ab900ce6358`
  同指快照 v1.7.16）。漏洞本体是 `parse_object` 在对象以逗号结束后无边界检查即调用 `parse_string`，
  后者读 `buffer_at_offset(input_buffer)[0]`，在调用方用 `cJSON_ParseWithLength` 且缓冲区恰好无尾字节时
  越界读 1 字节（ASan `heap-buffer-overflow` READ of size 1, cJSON.c:781）；`cJSON_Parse` 传入
  `strlen+1`，不触发。修复 `3ef4e4e` 增加 `cannot_access_at_index(input_buffer, 1)`，首见于 v1.7.18。
  OSV GIT 范围里的 `fixed` 哈希 `acc76239` 是 v1.7.18 tag tip（只改 `CONTRIBUTORS.md`），不是根因修复，
  卷宗与裁定均已区分。该结论**不代表**可利用的信息泄漏；可达性受 API 前提约束，已写入卷宗 limitations。
- cJSON CVE-2023-50472 是第二个由 `possible_affected` 升为 `confirmed_affected` 的同类案例
  （`runs/verification/cjson_CVE-2023-50472_v1716/` 卷宗 + `runs/independent/cjson_CVE-2023-50472_v1716_round1/verdict.json`
  独立裁定，grade A；两条候选行 `disc2_56023e86547f205b18fc6b22`/`disc2_881253322ce67b2c934e3401`
  同指快照 v1.7.16）。漏洞本体是 `cJSON_SetValuestring` 对 `object->valuestring == NULL` 的重置分支
  直接传入 `strlen(NULL)` / `memcpy(newitem, NULL, 0)`，在 `cJSON.c:408` 崩溃
  （v1.7.16 下 UBSan 报 null 指针实参、ASan 报 SEGV；v1.7.17/1.7.18 返回 `NULL` 不崩）。
  修复 `60ff122`（PR #809）首见于 v1.7.17；引入提交 `6b35f1c5`（2020-03-24）首见于 v1.7.13，
  v1.7.13–v1.7.16 该函数字节级相同（sha256 `0bdc48e0…`），故修正后的范围为
  `>=1.7.13,<1.7.17`，而不是 OSV 记录的点范围。v1.7.17 的修复仍存在「第二参数为 NULL 时
  传给 `memcpy`」的残留缺陷（`cJSON_AddItemReferenceToObject` 路径），未另行开案，已写入卷宗 limitations。
  该晋级依据的是独立复现与源码复核，**不是** OSV 区间直接推导。
- cJSON CVE-2025-57052 是第三个同类正向案例（`runs/verification/cjson_CVE-2025-57052_v1716/` 卷宗 +
  `runs/independent/cjson_CVE-2025-57052_v1716_round1/verdict.json` 独立裁定，grade A；四条候选行
  `disc2_3d5c9af0179d9a4e37f348d4`/`disc2_a5fb8eabc9227cb5e7c887cc`/`disc2_c18db19ad5c1923552dcc607`/`disc2_302ad77a98f695fc3045f169`
  同指快照 v1.7.16）。缺陷在 `cJSON_Utils.c:285`：数字循环的条件写死 `pointer[0] <= '9'`，任何
  `>= '0'` 的字节都会被卷进下标（`/1A` → 27），修复 `74e1ff4`（PR #957，2025-09-05）改成
  `pointer[position] <= '9'`，首见于 v1.7.19；引入提交 `d67b008`（2017-04-12）首见于 v1.5.0，
  范围为 `>=1.5.0,<1.7.19`。独立复核明确：库内消费方（`get_array_item`/`insert_item_in_array`/
  `detach_item_from_array`）只遍历链表，ASan+UBSan 在精确堆分配下无报告，实际效果是**解析器差异**
  （CWE-129），advisory 的 CWE-125 / 「out-of-bounds access」与 9.8 分只作为已发布值保留，未获背书；
  记录本身以 `input_validation` 分类并写明差异。同一函数的 `size_t` 溢出（`/18446744073709551617`
  回绕为 1）在 v1.7.19 仍存在，属 open PR #1103，不在本行范围。
- gitea GHSA-hg5r-vq93-9fv6 / CVE-2026-58426 是首个由 `possible_affected` 升为 `confirmed_affected`
  的非 C/C++ 案例（`runs/verification/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5/` 卷宗 +
  `runs/independent/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1/verdict.json` 独立裁定，grade A；候选行
  `disc2_fad8afe3a4f3105bf6b45699`，快照 `snap_bd8b4ed626b39794` = v1.25.5 / `f913d90a`）。根因是
  `routers/api/actions/artifactsv4.go:162-170` 的 `buildSignature` 把 endpoint/expires/artifactName/
  taskID/artifactID 直接拼接后做 HMAC-SHA256，无分隔符或长度前缀；`verifySignature` 信任 URL 里的
  taskID/artifactName、丢弃签过名的 artifactID，且该路由组只用不鉴权的 `ArtifactV4Contexter`。
  修复引入 `actions.BuildSignature`（域名标签 + 8 字节小端长度前缀），`1c2d5e9b` 是 release/v1.26
  的 backport，1.27.x 走主干 `552c29a25`。独立 reviewer 用 Go 原语级红/绿复现了两组 v1.25.5 元组
  生成同一 HMAC、伪造 URL 通过 v1.25.5 验证器（negative control 拒绝），v1.26.2 builder 签名不同；
  **不是**整机集成测试。裁定记录的分歧：advisory 行号是主干行号（本 tag 偏移 2–3 行）、
  字面五字段形式自 v1.22.4 才有（v1.22.0–1.22.3 为四字段等价形式）、AC:L 需目标任务 Running
  （下载还需 artifact 已 UploadConfirmed），评分未改。该 reviewer 的后台收尾在 promote 之后
  才写完：`NOTES.md` 增加 v1.26.2 全量 `hmac.New` 普查说明、`sources/v1262_hmac_sites.txt`
  增加 4 行非 artifact 站点，并更新 verdict 中对应的两个 artifact sha256；已把最终版本复制回
  `runs/independent/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1/`，11 个 artifact 重新校验全部
  一致，结论 / grade / commit 未变。`data/reviews.jsonl` 不存 verdict 摘要，数据行无需改动。
- django CVE-2024-42005 / GHSA-pv4p-cwwg-4rph 经独立复核升为 `confirmed_affected`，**grade B**
  （`runs/verification/django_CVE-2024-42005_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-42005_4213_round1/verdict.json`；候选行
  `disc2_36f78bd1912f0d1afe514278`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `Query.set_values()`（`django/db/models/sql/query.py:2411`）把调用方字段名原样放进 `values_select`，
  从不调用同文件的 `check_alias()`（1123 行）。**可达性被 advisory 措辞夸大**：裸
  `values(field)`/`values_list(field)` 在 4.2.13 不产生别名、不注入；只有再叠加聚合注解
  （`.values(field).annotate(n=Count('id'))`）触发 `set_group_by(allow_aliases=True)` 时才把
  JSONField `KeyTransform` 以原始字段串为 key 移入 annotations，由 `SQLCompiler.as_sql` 拼进 `AS`。
  独立 reviewer 实测 4.2.13 编译出 `AS "data__injected_name" from ...; --"` 并经 DB cursor 执行成功，
  又把修复的 tests-only hunk 打到 4.2.13：回归测试 FAIL（ValueError 未抛），4.2.15 通过——因此
  红/绿验证的是缓解措施而非完整利用链，评 B。评分分歧（NVD Primary 7.3 / Secondary 9.8 /
  GHSA 9.1）按 NVD Primary 记录；reviewer 指出 9.8 的来源实为 CISA-ADP（`134c704f`），
  卷宗沿用了「GitHub CNA」的措辞。该措辞已在新卷宗中改正，promoted 数据行与更早的
  CVE-2024-39330 行也由 `runs/data_fixes/fix_cisa_adp_attribution_2026-10-24.py` 改为
  「CISA-ADP 容器（向量由 GitHub CNA 发布）」；分数与向量未变。
- django CVE-2024-39329 / GHSA-x7q2-wr7g-xqmf 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-39329_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-39329_4213_round1/verdict.json`；候选行
  `disc2_14765a081146e98aa8c1500a`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `ModelBackend.authenticate` 对 `is_active=True` 但密码不可用（`!` 前缀）的用户走
  `check_password`，Django 的 hasher 会为 unusable password 快速返回，跳过常耗时哈希，形成
  计时枚举（CWE-208/CWE-203）。4.2.14 改为对不可用密码也调用
  `make_password(get_random_string(...))`（`fake_runtime`），使失败路径耗时与正常校验一致。
  reviewer 在 4.2.13 / 4.2.14 两树上实测、两次重复运行（`reproduction/timing_*.json`），
  差值约 715×；裁定同时记录根因定位分歧（reviewer 认为根因在 `hashers.check_password` 的
  快速返回，不在 `backends.authenticate`），`location` 取 `django/contrib/auth/hashers.py:46-47`，
  与卷宗 location 同文件同行段。
- gitea GHSA-7wvc-rvp7-w99x / CVE-2026-58423 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/gitea_GHSA-7wvc-rvp7-w99x_v1.25.5/` 卷宗 +
  `runs/independent/gitea_GHSA-7wvc-rvp7-w99x_v1.25.5_round1/verdict.json`；两条候选行
  `adv3_637ca5637354216a`、`disc2_3d2d1a1ee5792687960294ae`，快照 `snap_bd8b4ed626b39794` =
  v1.25.5 / `f913d90a`）。LFS SSH 子命令鉴权绕过：`cmd/serv.go:131` 的 `getAccessMode` 对
  LFS 子命令返回 `AccessModeNone`，而 `routers/private/serv.go:352` 用 `userMode < mode`
  比较，`None`（0）恒小于所需 mode，鉴权被跳过。引入于 1.23.0，修复于 1.26.3
  （backport `8f4b7ebb`，主干 `42513398`）。reviewer 用真实 gitea 服务器做红/绿：
  v1.25.5 下越权读写 LFS 对象成功，修复版被拒；同时保留了对 `internal` 路由模式 0/1 的
  对照记录。
- django CVE-2024-38875 / GHSA-qg2p-9jwr-mmqf 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-38875_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-38875_4213_round1/verdict.json`；候选行
  `disc2_051d93d5bd86570c8437b5dd`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `Urlizer.trim_punctuation` 在 fixpoint 循环里每轮对整词重新 `count()` 开/闭括号、
  每轮只剥一个，N 个括号即 O(N²)；`handle_word` 对任何含 `.`/`@`/`:` 的词都会进入该路径。
  4.2.14 用 `CountsDict` 缓存计数、缓存标点集合、批量 `lstrip`/`rstrip` 替换循环。
  reviewer 在 4.2.13/4.2.14/5.0.6/5.0.7 四棵树上以 `"("*100000 + ":" + ")"*100000`
  实测（约 9.86 s → 0.003 s），并做 N=2000→100000 的缩放确认二次增长；`urlizetrunc`
  与直接调用 `urlize` 两条路径都复现。裁定记录的分歧：OSV GIT 的 `introduced` 事件方向
  反了（真正引入是 2016 年的 `dec334cb66`）、NVD 无 Primary CVSS（7.5 来自 CISA-ADP
  Secondary）、官方公告定为 moderate 而 GHSA/OSV 为 HIGH、且不支持分支 4.1.13 同样受影响
  但不在任何已发布区间内。
- django CVE-2024-41989 / GHSA-jh75-99hh-qvx9 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-41989_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-41989_4213_round1/verdict.json`；候选行
  `disc2_1d98594ee81566538ecb96d2`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `floatformat` 把输入交给 `Decimal(str(text))` 后计算 `int(d) - d`，`int(d)` 会把指数
  展开成天文数字位的整数，`1e10000000000000000` 直接 MemoryError。4.2.15 先看
  `Decimal.as_tuple()`，`len(digits) + abs(exponent) > 200` 时原样返回。reviewer 在
  4.2.13/4.2.15 两版实测：`1e1000000` 26.85 s 后未捕获 ValueError，`1e10000000000000000`
  立即 MemoryError，4.2.15 同一输入微秒级返回；模板过滤器路径同样复现。
- django CVE-2024-39614 / GHSA-f6f8-9mx6-9mx2 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-39614_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-39614_4213_round1/verdict.json`；候选行
  `disc2_97b11946b732970b9a25004c`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `get_supported_language_variant` 对连字符稠密语言码做 rfind 切片，二次方复制；4.2.13
  只有 Accept-Language 头受限（500），LANGUAGE cookie 原样进入。reviewer 自建 venv 实测
  `"en-"*30000`（90,006 字符）2.196 s、cookie 路径 0.802 s，4.2.14 约 0.000075 s / ValueError。
  裁定记录的分歧：OSV 的 GIT 区间 introduced/fixed 哈希均无效（introduced 是 2025/2026 年的
  安全归档提交，fixed 只是版本号 bump），NVD 唯一 CVSS 是 CISA-ADP Secondary 7.5，
  GHSA 用 CVSS 4.0 8.7，Django 自称 moderate。
- django CVE-2024-41991 / GHSA-r836-hh6v-rg5g 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-41991_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-41991_4213_round1/verdict.json`，verdict sha256 `709fce73…`；
  候选行 `disc2_3bb0bba7fbc37c8593e5441b`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `Urlizer.handle_word` 对未截断整词跑 URL 正则后把全部字符交给 `smart_urlquote` →
  `punycode(netloc)`，`is_email_simple` 不限制域名长度；`AdminURLFieldWidget.get_context`
  在验证器判定 `url_valid=False` 后仍对真值调用 `smart_urlquote`。4.2.15 加
  `MAX_URL_LENGTH = 2048`、域名 `len(p2) > 63` 拒绝、widget 改 `if url_valid else ""`。
  reviewer 独立复现：`"한.글."×1,000,000`（约 4 MB）在 4.2.13 的 email/http/www 三条
  `urlize` 路径 10.86 / 10.97 / 11.41 s、widget 11.05 s，RSS 增量约 +200 MB，输出膨胀到
  ~22.0 M 字符；4.2.15 同输入 0.043–0.050 s、RSS 增量 0，widget href 为空；4.2.14 在
  n=100k 仍 1.0603 s，确认首发修复版本是 4.2.15。分歧：OSV 的 GIT 事件哈希无效（版本号 bump /
  2025–2026 年安全归档提交），NVD 7.5 HIGH vs GHSA A:L 约 5.3、Django 自称 moderate；
  CWE-1284 + CWE-130 vs GHSA 另加 CWE-1333，但 reviewer 实测 IDNA 成本随输入线性
  （约 2.6 µs/字符），不支持 ReDoS 归类。未做 HTTP 端到端。
- django CVE-2024-53907 / GHSA-8498-2h75-472j 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-53907_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-53907_4213_round7/verdict.json`；候选行
  `disc2_8b86415747e9508ae2ac2940`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `strip_tags()` 的 `while "<" in value and ">" in value` 循环反复调用 `_strip_once()`，
  没有迭代上限；`"<"*d + "a>"*d` 每轮只剥一层，总代价 O(d·n)。4.2.17 加
  `MAX_STRIP_TAGS_DEPTH = 50` 并在超限时 `raise SuspiciousOperation`。reviewer 自建
  4.2.13/4.2.17 venv 实测 d=1000/2000/4000/8000 为 0.412 / 1.591 / 6.514 / 26.301 s
  （每翻倍约 4×），4.2.17 同 24 KB 0.334 s 抛异常，`striptags` 过滤器 25.603 s vs 0.342 s；
  PyPI 包与 git blob 逐字节一致。分歧：NVD 无 Primary CVSS，只有 CISA-ADP Secondary 7.5
  HIGH（OSV 同向量），OSV `database_specific` 与 Django 均写 moderate；4.2.17 在抛错前
  仍有至多 50 轮全串解析（600 KB 8.27 s，线性），未做 HTTP 端到端或并发 DoS 演示。
- django CVE-2024-53908 / GHSA-m9g8-fxxm-xg86 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-53908_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-53908_4213_round8/verdict.json`；候选行
  `disc2_d997111c20cf6d0610292215`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  Oracle 分支 `HasKeyLookup.as_oracle` 对 `as_sql()` 的结果再做一次 `sql % tuple(params)`，
  把 lhs 绑定值糊进 SQL 文本并返回空参数表；4.2.17 拆成 `_as_sql_parts`/`_combine_sql_parts`
  并保留 `params.extend(lhs_params)`。reviewer 自建 4.2.13/4.2.17 venv 做 compile-level 红/绿：
  lhs `1, '$.foo') OR 1=1 --` 在 4.2.13 得到 `JSON_EXISTS(1, '$.foo') OR 1=1 --, '$."foo"')`
  且 params `[]`，4.2.17 为 `JSON_EXISTS(%s, '$."foo"')` + 绑定参数；公开 ORM 入口同样成立；
  `__` 语法两版逐字节相同。限制：**没有真实 Oracle 实例**（compile-level 明确允许），
  `oracledb` 仅以 `sys.modules` 别名满足 `cx_Oracle` 导入；5.0/5.1 只核对祖先与代码未执行；
  tag 签名因本地无公钥无法校验；带引号 rhs 的 `__has_key` 两版都内联引号，属未改动的 rhs 路径，
  未在真实 Oracle 上验证，未作为新漏洞主张。
- django CVE-2024-45231 / GHSA-rrqc-c2jx-6jgv 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2024-45231_4213/` 卷宗 +
  `runs/independent/django_CVE-2024-45231_4213_round9/verdict.json`；候选行
  `disc2_00c12ead68ae4b95c2b982e6`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `PasswordResetForm.send_mail()` 的 `email_message.send()` 未捕获后端异常：邮件发送持续失败时，
  存在的激活账号触发 500，不存在/未激活/无可用密码的地址不触发，攻击者可据此枚举地址。
  4.2.16 用 try/except + `django.contrib.auth` 的 `logger.exception` 修复。reviewer 用真实
  `PasswordResetView`（test Client、`DEBUG=False`）实测 4.2.13 的 500 vs 302、4.2.16 全 302
  并记录 1 条 ERROR；关闭端口 SMTP 同样复现，locmem 对照两版全 302。限制：只跑了 4.2 分支
  （5.0/5.1 只核对提交与祖先）；test client + 内存 SQLite，不是部署服务器，自定义中间件/500
  处理器可能改变状态码；邮件失败用自定义后端与连接拒绝模拟，不是真实远端故障；
  GitHub 仓库级 advisory 页匿名 404（改用 REST API 与全局页）；NVD 描述把已修复版本写成
  “discovered in”，以 CPE 区间为准；严重度三源分歧（GHSA 3.7 AC:H / NVD 5.3 AC:L /
  Django 自评 low），`severity` 记录 NVD Primary 5.3。
- django CVE-2025-64459 / GHSA-frmv-pr5f-9mcr 经独立复核升为 `confirmed_affected`，**grade A**
  （`runs/verification/django_CVE-2025-64459_4213/` 卷宗 +
  `runs/independent/django_CVE-2025-64459_4213_round10/verdict.json`；候选行
  `disc2_d791407a54d5b84b33a8db28`，快照 `snap_516aa9971dd9509d` = 4.2.13 / `3bf46e2e`）。
  `Q.__init__` 把 `_connector` 原样传给 `tree.Node`，`WhereNode.as_sql` 用
  `" %s " % self.connector` 拼进 SQL，字典展开使 `filter/exclude/get(**dict)` 能到达该命名参数。
  reviewer 实测 4.2.13 `filter(**{"name":"Alice","id":999,"_connector":" OR 1=1 OR "})`
  返回全部 3 行（合法 AND 查询 0 行）、`get()` 抛 `MultipleObjectsReturned`；4.2.26 抛
  `TypeError`/`ValueError` 拒绝。限制：仅 SQLite（注入由后端无关的 ORM 代码生成）；参数仍绑定，
  被改写的是连接符，因此「参数化查询」本身不构成防护；载荷 `" OR 1=1 OR "` 是为保持语法合法而
  选，未尝试注释截断或堆叠语句；通过 `QuerySet` 迭代执行而非 HTTP 应用；未跑全量测试；
  GHSA/OSV 的 4.2 分支写作 introduced 0 而 NVD/PYSEC 从 4.2 起，采用后者；GHSA 漏列实际拦截
  `filter(**dict)` 的配套提交 `279f8b95…`；Django 政策称 "high"（非 CVSS 口径）；GitHub API
  的 `cvss_v4` 为 null，未据此评分。
- 3 条候选行是已确认漏洞的**重复 discovery**（cJSON v1.7.16 / CVE-2023-50471 一条、libexpat
  R_2_6_2 / CVE-2024-45490 两条）。它们此前停在 `possible_affected`，与同快照同名 advisory 的
  已确认行自相矛盾；2026-10-24 用 `runs/data_fixes/link_duplicate_candidates_to_verified_2026-10-24.py`
  在守卫（decision、快照、repo、commit、队列 record 全部匹配）下改为 `confirmed_affected` 并填
  `vulnerability_id` 指向既有记录，**未新做复核、未改任何 review 等级**。仓库与提交层面的重复
  也至此清理：可复核队列不再包含这 3 条。
- 已选版仓库内**没有**候选缺 triage 行（549 条已于 2026-10-24 以 unknown 行补全）；另有 13 条属于
  nlohmann、openssl 两个未选版仓库，未选版仓库没有冻结 SHA，按先选版规则处理，故无 triage 行。
- 范围层排除继承 advisory 自身的完整性。2026-10-24 对**全部 817 条**范围排除行（723 条 `above_upper`
  + 94 条 `below_lower`，含三批新审计落盘的 61 条）做整体复现复核
  （`runs/triage_range_recheck_full_2026-10-24/`，选择器与两模式原始输出均已落盘）：
  **默认模式 817/817 全部重新提出、0 条 divergent**；strict 模式 812/817，差的 5 条是它把同一
  advisory 的其他产品包也当作本仓库包（`openssl-src`、jquery-rails ×2、`DisCatSharp`，另有
  spring-framework v4.1.1 的 GHSA-v596 命中 spring-security），默认模式对这 5 条均给 NA；
  该模式是显式可选项，已知会这样过度阻断。逐条清单见该目录 README，未被静默修改或删除。
  更早的 ad hoc 复核（693 条、后称 807 条）未留脚本，其数字由本次可复现复核取代。
  三批新落盘证据：`runs/triage_unblocked_2026-10-24/`（36 CONFIRMED / 9 REJECTED / 1 INCONCLUSIVE）、
  `runs/triage_fixed_release_2026-10-24/`（17/17）、`runs/triage_git_range_2026-10-24/`
  （10 CONFIRMED / 2 INCONCLUSIVE）；未确认的 12 条保持 unknown。
  其中 vite `adv3_0fee4010849796dd` 与 flask `adv3_6e04d4b614fb9b14` 两行在事后撤回为 unknown
  （`runs/data_fixes/revert_bare_version_exclusions_2026-10-24.py`）：它们依据的「裸版本号=单点」读法
  已被证伪，结论虽大概率仍真，但证明形态不再可复现，故不保留排除。
  粗粒度副本问题的实质：`discovery_v3/repo_advisories` 的 `vulnerable_version_range` 是 GitHub 渲染的
  扁平化区间（多分支被压成 `>= 0.4` / `>= 1.3.0` / `All`），修复版本另存在 `patched_versions`；
  单看区间会得到「包含冻结版本」的假 possible。生成器现在只在同一 advisory 的 OSV 副本给出**完全相同**
  的修复版本集合时把该粗粒度投票视为冗余并丢弃，不据此构造任何边界；集合不符则保留其否决。
  上界包含性：OSV `fixed` 是首个已修复版本、`limit` 是排他上限、NVD `versionEndExcluding` 是排他上界，
  快照恰等于该版本时已在区间外（旧实现要求严格更高，故 `v1.9.0`、`v1.25.5`、`curl-8_3_0` 这类
  「快照即修复版本」的候选一直保留为 unknown）。修后对当时表中的 1257 条 unknown 重跑得 63 条排除提案，
  其中 17 条是本修复新增（gitea 14、curl 1、gin 1、plug 1），已打包送独立审计，
  **未写入数据**（`runs/triage_fixed_release_2026-10-24/`）；获 CONFIRMED 后才会应用。
- GHSA 范围字符串本身有缺陷：已见空合取式（gitea `<= 1.26.4, >1.27.0`）、缺失边界的分支（`< 8.2.0` 无下界）
  和单独一个版本号（vite `6.4.4`、gitea `1.26.2`）。生成器现对不合取 clause 判 indeterminate、把 `;`
  当分支分隔符，并**拒绝把无运算符的裸版本号当作任何边界**（它既可能是单点，也可能是被 GitHub 扁平化后的
  开区间上界，二者不可区分）；这只避免误判，不能修复上游文本错误。审计中据此撤销 8 条 gitea 假排除与
  2 条已落盘的 vite/flask 排除。
- 1 条被撤回 advisory（`adv3_087476da78c375b4`）既有 rejected 状态，标 `unknown`，不自动判无漏洞。

## 4. 检索与覆盖

- 全部仓库 `outcome=NEEDS_REVIEW`；旧全历史覆盖归档于 `legacy_discovery_coverage_v03.jsonl` 供对照。
- 50 条 coverage 的 `passes` 数组是从 v0.3 继承的模板化记录（每行 4 条、文字相同），
  **不是逐仓库真实检索历史**；尤其第 4 条 “static dossier verification … grade B” 对 ruby/rexml 与 django
  不成立（两者实际均为 grade A，见 `runs/independent/rexml_CVE-2025-58767_round1/verdict.json` 与
  `runs/independent/django_CVE-2024-39330_round1/verdict.json`）。
  `unresolved_candidates` 仅按当前 triage 个别更新（rexml 9 → 8，rack 48 → 49，libexpat 现有 135），
  其余仓库仍为旧值。django 行仍写 162，而 2026-10-24 三次 promote 后 live triage 为 30 条
  `possible_affected` + 2 条 `unknown`；`coverage_statement` 里“1 vulnerability … 155 unresolved”
  也停留在首次迁移时点，未随新正样本重写——以 `data/snapshot_candidate_triage.jsonl` 与
  `runs/possible_review_queue_2026-10-24/` 为准。
- `PASS_KNOWN_SWEEP=0/50`：没有对固定 SHA 执行两轮独立检索，未声明快照已知漏洞已穷尽。
- 披露截止：现有候选与缓存 advisory 记录的最新发布时间为 2026-10-21T07:47Z（OSV/NVD）、
  2026-10-21T05:36Z（GitHub advisory），即**没有 2026-10-21 之后发布的披露进入数据**；但采集截止并不统一：
  49/50 条 coverage 写 2026-10-21，rack/rack 写 2026-10-22，另有 rack、django、libexpat、axios、echo
  五个仓库的 pass 4 在 2026-10-22 运行（快照迁移复核，未引入新披露）。因此 `manifest.source_cutoff_date`
  仍为 null，不用单一日期冒充全体截止，也不替发布方决定口径；复核脚本与结论见
  `runs/cutoff_verification_2026-10-24/`。

## 5. 费用

- `cost_policy.json` 是阈值配置，不是强制网关（`WARNING` 已记录）。本版迁移与初始 triage 全部为离线规则，
  未产生任何记账的模型调用（`v031/ledger/model_calls.jsonl` 为空，cost_report 输出 0 调用 / ¥0 实测 /
  untracked = DO NOT ASSUME ZERO）。后续任何 LLM 调用必须记账后才可复核预算。

## 6. 评测运行与发布

- 无 `agent_findings.jsonl` / `adjudications.jsonl`：没有审计 Agent 运行，没有已知 recall/TP/FP/novel。
- 数据目录不可直接交给被测 Agent：48/50 目标有去 `.git` 的源码导出（`data/snapshot_exports.jsonl`
  48 行 `exported`），其中 46 个已通过独立选版审查并 frozen；2 个 legacy 目标仍 proposed（审查 reject），
  2 个仓库未选版；且全部 `leakage_controls` 仍为迁移默认值，没有运行期网络隔离方案。
- `manifest.status=draft`；release 门槛（50 冻结目标、snapshot 限定覆盖、相关候选全部核验、cutoff 复核）
  均未达成（当前 46/50 冻结、574 条 unknown 未决、`source_cutoff_date=null` 因采集截止不统一，见第 4 节），
  本报告如实记录，不做虚假 PASS 声明。

## 7. 2026-10-24/25 django 4.2.13 正样本的边界

- **CVE-2025-32873（strip_tags 二次方 DoS）**：可复现性依赖 CPython `html.parser` 对 EOF 处
  不完整标签的旧行为。上游 CPython 3.12.3 上实测 2,001→128,001 字节为 0.005→7.893 s；本机
  Ubuntu 的 `3.12.3-1ubuntu0.17` 已回移 CPython 3.14 行为（不完整标签直接丢弃），同一载荷打不动，
  且 4.2.21 自带的回归测试在该解释器上会失败。verdict 记录了两者对照；这是环境前提，不是
  漏洞不成立。红/绿只跑 4.2 线（4.2.13 vs 4.2.21）。
- **CVE-2025-57833（FilteredRelation alias 注入）**：红/绿在**内存 SQLite**、进程内 ORM 上完成；
  注入形态与后端相关，未跑 MySQL/PostgreSQL，也未跑 HTTP 端点。演示能力是过滤绕过与对任意子查询的
  布尔条件，未尝试 UNION、时间盲注或枚举其他表。应用必须把调用方可控的 dict 展开进
  `annotate()/alias()`；上游测试字面 alias 在 SQLite 上只报语法错误，可用载荷需保留与 params
  数量一致的占位符。4.2.24 的 `ValueError` 在 Web 框架中如何映射未测；5.1/5.2 修复只核对提交与
  祖先，未执行。
- **CVE-2025-59682（archive 前缀兄弟目录写出）**：只能写到与目标同级、名字以目标路径为前缀的
  兄弟目录，不能写到任意绝对路径，未演示代码执行；演示是进程内 `archive.extract()`，未端到端跑
  `startapp/startproject --template`（其模板目录是随机 `mkdtemp`，前缀不可预测）。只执行 4.2.13 与
  4.2.25；未测 Windows 跨盘 `ValueError` 分支、符号链接/硬链接成员与含反斜杠的 zip 条目。NVD
  Primary 6.5 MEDIUM 与 CNA/OSV 3.1 LOW、发布说明 "low" 不一致，卷宗按 NVD Primary 记录并单列两边。
- **CVE-2025-48432（`log_response()` 日志注入）**：红/绿是进程内 `django.test.Client` 探针
  （4.2.13 / 4.2.22 / 4.2.23 三版；4.2.22 仅 404 已转义、405/410 仍原样），未跑真实 WSGI/ASGI
  服务器，也未经过前置代理——`PATH_INFO` 谁来百分号解码随部署而变，若前置层先做过滤或转义则
  不成立。演示的是日志完整性问题（多一行 / 原始 ANSI ESC），未演示某个具体日志采集器被绕过的
  端到端利用；探针自挂 handler 且 `propagate=False`，未测默认 `LOGGING` 配置与项目自有 formatter。
  4.2.14–4.2.21 只做逐 tag 扫描（仍原样转发参数），未安装执行；5.1/5.2 线只核对祖先与补丁文本。
  完整修复记 4.2.23（NVD 英文描述 / CPE 与 Django 公告口径），GHSA/PYSEC 的 4.2.22 是镜像滞后。
- **CVE-2025-64460（`getInnerText()` 二次方膨胀）**：红/绿走文档化的
  `serializers.deserialize("xml", data)`，但仍是进程内调用，未跑接受 XML 上传/导入的真实端点
  （真实部署还受请求体大小、超时与 worker 限制）。本机规模下绝对耗时不大（4.2.13 在 depth 800 /
  leaf 32k 为 0.155 s），证明的是平方增长曲线与 1 MB 负载 4.63 s vs 0.0097 s 的差距，不是打垮
  真实服务；计时在共享主机上取得，绝对数字不是基准测试。修复同时包含 `getInnerTextList()` 与
  minidom `fast_cache_clearing()` 两项改动，探针未拆分各自贡献（助手本身占 >99% 已说明主因）。
  只执行 4.2.13 与 4.2.27；4.2.14–4.2.26 按公告记为受影响并逐 tag 扫描，未安装执行。
  NVD 无 Primary 指标（唯一 CVSS 3.1 7.5 HIGH 来自 CISA-ADP Secondary），OSV 为 CVSS 4.0 /
  MODERATE，卷宗采用 NVD Secondary 并记录两边。
- **CVE-2025-26699（`wrap()`/`wordwrap` 每行重切剩余串）**：红/绿走文档化的 `wordwrap`
  模板过滤器（模板 `{{ text|wordwrap:10 }}`）与直接 `wrap()`，但仍是进程内调用，未跑真实
  请求/模板渲染端点；触发需要大量换行点的长输入，单个 4.93 MB 不换行 token 两版都线性
  （0.0018 s vs 0.0536 s），不能据此打服务。固定实现的常数因子更高：12,500 words 时比
  4.2.13 慢约 8 倍，交叉点在 400,000–800,000 words，CVE 主张的是渐近复杂度；修复还改变
  行尾空白输出（vulnerable 保留一个尾空格，上游测试只断言子串）。只执行 4.2.13 与 4.2.20；
  4.2.14–4.2.19 按公告记为受影响并逐 tag 扫描，未安装执行；5.0/5.1/main 只核对补丁与祖先。
  NVD Primary 7.5 HIGH 与 CNA/GHSA/OSV 5.0 MEDIUM 不一致，卷宗采用 NVD Primary 并记录两边；
  GitHub languages API 403，语言清单由 reviewer 自行计数。
- **CVE-2025-14550（`ASGIRequest` 每个重复 header 重拼整串）**：红/绿在进程内直接构造
  `ASGIRequest`（与上游回归测试同形），**未跑真实 ASGI 服务器**；真实部署能否收到 200,000 个
  重复头取决于前置服务器的 header 限制（h11 / uvicorn+httptools / hypercorn 各不相同）。效果是
  超线性 CPU 与分配，不是立即崩溃；4.2.13 的逐翻倍比例不均匀（成本由大字符串分配主导）。只执行
  4.2.13 与 4.2.28；4.2.14–4.2.27 按公告与逐 tag 扫描记为受影响，未安装执行；5.2/6.0/main 只核对
  补丁与祖先。固定版在大量**互不相同**的 header 名上常数因子更大（约 3.9×），CVE 主张的是渐近
  复杂度。NVD 无 Primary，CISA-ADP Secondary 7.5 HIGH 被采纳；GHSA 2.7 LOW、Django "moderate"。
- **CVE-2026-1285（`Truncator._truncate_html` 对未匹配结束标签全表扫描）**：独立复核 grade A
  （`runs/independent/django_CVE-2026-1285_4213_round15/verdict.json`，2026-10-24T17:40:45Z promote）。
  红/绿在进程内直接调用 `Truncator(text).chars/wrap()` 与模板过滤器，**未跑真实请求/模板端点**；
  触发需要大量**未匹配**结束标签（`<a>`×m + `</b>`×m），真实部署还受请求体大小与超时限制。
  效果是超线性 CPU，不是崩溃。只安装执行 4.2.13 与 4.2.28；4.2.14–4.2.27 按公告与逐 tag 扫描记为
  受影响。`:1`（默认省略号）因 `truncate_len = 0` 跳过全部标签，需 `:2`、`truncate=""` 或
  `truncatewords_html` 才进循环。4.2.28 的回移不完整：仍保留 `insert(0)` 与成功关闭时的切片，
  良构嵌套在两版都是二次方（n=32,000 约 1.01 s），因此「固定版仍非线性」只作修复形状说明，
  不构成漏洞主张。OSV GIT ranges 的 `fixed` 哈希是发布版本号提交、`introduced` 哈希是 archive
  回填，卷宗只用发布号与四个补丁提交（4.2 `b40cfc60…`、5.2 `9f2ada87…`、6.0 `4b86ba51…`、
  main `a33540b3…`）。CVSS 四方分歧（NVD 无 Primary、CISA-ADP Secondary 7.5 HIGH、CNA CVSS 4.0
  2.7 LOW、Django "moderate"）与发布说明重复段记录在
  `runs/verification/django_CVE-2026-1285_4213/README.md`。
- **CVE-2026-3902（ASGI header 下划线/连字符折叠）**：独立复核 grade A
  （`runs/independent/django_CVE-2026-3902_4213_round16/verdict.json`，2026-10-24T17:50:54Z promote）。
  红/绿在进程内构造 `ASGIRequest` 并调用 `get_asgi_application()`，**未跑真实 uvicorn/daphne、
  没有 TLS 与反向代理**；下划线拼写能否到达 Django 取决于前置 ASGI 服务器与代理（nginx 默认
  `underscores_in_headers off`），所以演示的是「头到达后」的折叠缺陷，不是某个具体部署的端到端
  利用。只安装执行 4.2.13 / 4.2.29 / 4.2.30；4.2.14–4.2.28 按公告与逐 tag 守卫扫描记为受影响，
  未逐版安装；5.2/6.0/main 只核对补丁与祖先。演示的是连字符头被代理剥掉后以下划线拼写重新
  出现（4.2.13/4.2.29 `META` 可见 `6.6.6.6`，4.2.30 无该键），以及双拼写按 scope 顺序合并；
  未演示某个具体应用的鉴权绕过。评分分歧：NVD 无 Primary、CISA-ADP Secondary 7.5 HIGH、
  GHSA HIGH，而 Django 发布说明把本 CVE 标为 "low"。OSV GIT `fixed` 哈希是发布版本号提交、
  `introduced` 哈希是 archive 回填，卷宗只用发布号与四个补丁提交（4.2 `4412731a…`、5.2
  `1cc2a761…`、6.0 `a623c398…`、main `caf90a97…`）。细节见
  `runs/verification/django_CVE-2026-3902_4213/README.md`。
- **CVE-2026-33034（ASGI 缺头/低报 `Content-Length` 绕过 `DATA_UPLOAD_MAX_MEMORY_SIZE`）**：
  独立复核 grade A（`runs/independent/django_CVE-2026-33034_4213_round17/verdict.json`，
  2026-10-24T17:58:38Z promote）。采集方 probe 是进程内构造 `ASGIRequest` 与
  `get_asgi_application()`；复核方另外用真实 **uvicorn 0.54.0 + curl chunked** 做了端到端
  （4.2.13 读满 200,000 B / 200，4.2.30 拒绝 / 400），但真实 HTTP/1.1 下 h11 只交付声明的
  10 字节，所以「低报 CL」只能在 Django ASGI 接口层（合成 scope/body file）复现；无 CL/chunked
  路径可端到端复现。两个拒绝响应的状态码记录不同（采集方 413、复核方 400），语义都是
  `RequestDataTooBig`，不改变裁定。只安装执行 4.2.13 / 4.2.29 / 4.2.30；4.2.14–4.2.28 按公告与
  逐 tag 守卫扫描记为受影响，未逐版安装。评分分歧：NVD 无 Primary、CISA-ADP Secondary 7.5 HIGH、
  GHSA HIGH，而 Django 发布说明把本 CVE 标为 "low"。OSV GIT `fixed` 哈希同样是发布版本号提交，
  卷宗只用发布号与四个补丁提交（4.2 `ed4dfda6…`、5.2 `49e1e2b5…`、6.0 `393dbc53…`、main
  `953c2380…`）。细节见 `runs/verification/django_CVE-2026-33034_4213/README.md`。
- **CVE-2026-33033（base64 multipart 对齐循环二次方复制）**：独立复核 grade A
  （`runs/independent/django_CVE-2026-33033_4213_round18/verdict.json`，2026-10-24T18:01:19Z promote）。
  红/绿与卷宗都是进程内 `MultiPartParser.parse()`，**没有 HTTP 服务器、请求体上限或
  反向代理**；绝对耗时不可移植，结论靠版本对照、对齐对照与 unget 字节增长（128 KiB
  2.15 GB → 2 MiB 66.57 GB）。64 KiB 用例偏快是机制使然（其空白几乎全在 header-leftover
  合并块内被整体消费），不是反例。只安装执行 4.2.13 / 4.2.30（复核另比对 4.2.29 与
  4.2.13 逐字节相同）；4.2.14–4.2.28 按公告范围与逐 tag 守卫扫描记为受影响，5.2/6.0
  只核对补丁与祖先。评分一致（CISA-ADP Secondary 6.5 MEDIUM、GHSA MODERATE、Django
  "moderate"）。OSV GIT 哈希同为发布版本号/回填提交，卷宗只用发布号与四个补丁提交
  （4.2 `f13c20f8…`、5.2 `0b467893…`、6.0 `0910af60…`、main `7e9885f9…`）。细节见
  `runs/verification/django_CVE-2026-33033_4213/README.md`。
- **CVE-2026-4292（`list_editable` 保存循环未校验新建对象）**：独立复核 grade A
  （`runs/independent/django_CVE-2026-4292_4213_round19/verdict.json`，2026-10-24T18:05:34Z promote）。
  红/绿是进程内最小 admin 站点 + Django test client，**没有真实 server 或反向代理**；采集方用
  superuser + `has_add_permission` 覆写，复核方另做了非 superuser staff（仅 view+change、无 add）
  的 perms 模式：4.2.13 两种模式伪造 POST 都 302 并插入行，4.2.30 都 400 且拒绝，正常编辑对照
  两版均 302。只安装执行 4.2.13 / 4.2.30（复核另比对 4.2.29 与 4.2.13 `contenttypes/admin.py`
  逐字节相同）；4.2.14–4.2.28 按公告范围与逐 tag 守卫扫描记为受影响，5.2/6.0 只核对补丁与祖先。
  评分存在内部矛盾：NVD/CVE/PYSEC 采用 CISA-ADP Secondary **9.8 CRITICAL**（PR:N/UI:N，与
  「需 staff 权限」的公告文本不符），GHSA 为 CVSS 4.0 **LOW**，Django 发布说明为 "low"；卷宗为
  与既有 django 行一致采用 NVD 指标并记录全部分歧，数值不可当作真实影响量级。行号比卷宗偏移
  2 行（复核测得 4.2.13 保存循环 2016-2025、4.2.30 guard 2020-2021，location 取重叠区间）。
  细节见 `runs/verification/django_CVE-2026-4292_4213/README.md`。
- **CVE-2026-4277（`GenericInlineModelAdmin.get_formset` 丢失 add 权限包装）**：独立复核 grade A
  （`runs/independent/django_CVE-2026-4277_4213_round20/verdict.json`，2026-10-24T18:16:57Z promote）。
  红/绿是进程内真实 admin change view（`django.test.Client` POST、sqlite `:memory:`、
  Episode + generic Media + `GenericTabularInline`），**没有真实 server、部署或反向代理**；演示的是
  非 superuser staff 用户（仅 view/change、无 `add_media`）伪造 `INITIAL_FORMS=0`、空 inline id 时
  4.2.13 插入一行、4.2.30 不插入，合法编辑对照两版都保存，有 `add_media` 的对照两版都允许新增；
  没有越权读取、数据外带或超出该行本身的持久化影响。只安装执行 4.2.13 / 4.2.30（复核另比对
  4.2.29 与 4.2.13 `contenttypes/admin.py` 逐字节相同）；4.2.14–4.2.28 按公告范围与逐 tag 守卫扫描
  记为受影响，5.2/6.0 只核对补丁与祖先。评分存在内部矛盾：NVD/CVE/PYSEC 采用 CISA-ADP Secondary
  **9.8 CRITICAL**（PR:N/UI:N，与「需 staff 持父模型 change 权限」的公告文本不符），GHSA 为
  CVSS 4.0 **LOW**，Django 发布说明为 "low"；卷宗为与既有 django 行一致采用 NVD 指标并记录全部
  分歧，数值不可当作真实影响量级。provenance 侧：复核方 4.2.13/4.2.30 全量文件 sha256 对比
  0 mismatch，`stable/4.2.x` ref 已消失（4.2 EOL），tag 的 PGP 签名未做密码学验签，改以 PyPI
  全树哈希交叉验证；OSV 4.2 GIT range 倒置（fixed 是 introduced 的祖先），未采用。细节见
- **CVE-2025-13473（mod_wsgi `check_password()` 用户名枚举计时差）**：独立复核 grade A
  （`runs/independent/django_CVE-2025-13473_4213_round21/verdict.json`，2026-10-24T18:26:46Z promote）。
  红/绿是**进程内**调用 handler + 一次性 sqlite，不是真实 mod_wsgi/HTTP Basic 请求；判据是上游同法的
  `mock.patch.object(PBKDF2PasswordHasher, "encode")` 调用计数（不存在/停用用户 0 次 vs 活跃用户 1 次）
  加墙钟（288× 中位、312× 最小，n=30/用例），4.2.28 四个用例都 1 次、比值 0.9-1.0×；返回语义
  `None/False/True` 三版一致，正确口令三版都 True——是枚举面，不是认证绕过。只安装执行 4.2.13 /
  4.2.27 / 4.2.28；4.2.14–4.2.26 依据 OSV/NVD range 与 4.2.27 文件逐字节相同记为受影响。评分采纳
  NVD CISA-ADP Secondary **5.3 MEDIUM**（GHSA CVSS 4.0 **2.7 LOW**、Django 说明 "low"），5.3 高于
  厂商口径，不可当作真实影响量级。provenance：4.2 线 `stable/4.2.x` 分支在 EOL 后已删除（只剩历史
  branch-point tag），CVE OSV 的 GIT range 倒置（4.2 introduced `97aa3b7f` 是 4.2.28 `20c71f6b` 的
  后代、"fixed" 指向发布 bump），复核方改用 ECOSYSTEM range + 自身祖先关系；keyserver 404，签名对
  GitHub 公布公钥验证。细节见 `runs/verification/django_CVE-2025-13473_4213/README.md`。
- **CVE-2026-25674（`FileSystemStorage._save()` / `FileBasedCache._createdir()` 的进程级 umask 竞态）**：
  独立复核 grade A（`runs/independent/django_CVE-2026-25674_4213_round22/verdict.json`，
  2026-10-24T18:37:10Z promote）。红/绿是**进程内**保存 + 4 个合成 canary 线程，不是真实
  web server/上传端点：4.2.13 每个深路径保存都执行 `os.umask(0o077)/os.umask(0o022)`
  （200 次保存 = 400 次调用），同期 canary 建的对象 4,406-4,463 / 4,546-4,607 次落到
  0o700/0o600（应为 0o755/0o644）；4.2.29 同负载 0 次 umask、canary 0 次偏离、改发 5,000 次
  `os.chmod`；零保存负对照 0/148 偏离。三版 Django 自己创建的叶子目录/文件都是 0o700/0o600，
  差别只在全局 umask 窗口。触发需设置 `FILE_UPLOAD_DIRECTORY_PERMISSIONS`
  （默认 None 时 control 三版 0 次 umask），是配置前提而非缓解。只安装执行 4.2.13 / 4.2.28 /
  4.2.29；4.2.14–4.2.27 依据 OSV/NVD range、4.2.13 与 4.2.28 三份文件逐字节相同记为受影响。
  评分采纳唯一的 CISA-ADP Secondary **3.7 LOW**（NVD 无 Primary；GHSA LOW、Bitnami Low、
  Django 说明 "low"），不能当作实测影响量级。provenance：OSV CVE 的 4.2 GIT range 同样倒置
  （introduced `97aa3b7f` 是 4.2.29 的后代、4.2 EOL 分支头），未采用；`stable/4.2.x` 分支已删除。
  细节见 `runs/verification/django_CVE-2026-25674_4213/README.md`。
- django CVE-2026-48588（4.2.13，round23 grade A，见 `runs/verification/django_CVE-2026-48588_4213/`）：
  `UpdateCacheMiddleware.process_response()` 的守卫是
  `if (not request.COOKIES and response.cookies and has_vary_header(response, "Cookie"))`，第 94 行的
  `not request.COOKIES` 让**任意**无关 Cookie（probe 用 `theme=dark`）短路该守卫，于是设了会话 Cookie 且
  `Vary: Cookie` 的响应被写进共享缓存并在第二次同 Cookie 请求时回放给第二个客户端；`cache_page()` 经
  `decorator_from_middleware_with_args(CacheMiddleware)` 走同一段代码。5.2.16 改为无条件
  `if response.cookies and has_vary_header(response, "Cookie"): return response`。
  **4.2 线没有修复版本**：LTS 支持 2026-04-07 结束，修复 2026-06-11 提交、2026-07-07 随 5.2.16 与 6.0.7
  发布；4.2.30 仍带同一份漏洞守卫，4.2.13..4.2.30 之间 `django/middleware/cache.py` 零提交；
  6.1 线另有 `c2a936ab…`（公告未点名 6.1）。范围本身互相矛盾：只有 GHSA 的 `<5.2.16` 覆盖 4.2，
  CNA/NVD/PYSEC/BIT 都只写 5.2 与 6.0，cvelistV5 的 CNA 3.1 指标还把重算为 3.1 的向量写成 4.2 MEDIUM。
  评分采纳 CNA/厂商 CVSS 4.0 **2.3 LOW**，NVD Primary 5.3 记入 `all_published_scores` 但未采用。
  该案同时暴露并修复了一处旧缺陷：25674 的 dossier 未把任何证据映射到 `critical_operation`，validator
  因此报「location ... no PASS root cause evidence」；已在 dossier 补映射并回填 3 条 location 证据
  （`runs/data_fixes/backfill_25674_critical_operation_evidence_2026-10-25.py`）。
- **CVE-2025-13372（PostgreSQL `FilteredRelation` 别名含 `$` 未加引号进入 SQL）**：独立复核 grade A
  （`runs/independent/django_CVE-2025-13372_4213_round30/verdict.json`，2026-10-24T20:10:47Z promote）。
  复现是**编译级**：本机无 postgres/initdb，docker 代理不可用，因此对 4.2.13 / 4.2.26 只展示
  `alias()`/`annotate()` 编译出的 SQL 里别名原样出现（`JOIN "probeapp_author" crafted_alia$`），
  对 4.2.27 展示其在任何连接前抛 `ValueError: Dollar signs are not permitted in column aliases
  on PostgreSQL.`；**没有连库执行，也没有武器化 payload**——卷宗的 `x$f$(SELECT(1))$f$` 经 pglast
  v8.7 解析是语法错误，其余 `$` 别名 PARSE_OK 说明 token 流确实未被过滤。受影响结论依赖公告区间 +
  上游修复提交 + 守卫前后差分。守卫是后端级的（只加在
  `django/db/backends/postgresql/compiler.py`），自定义 backend 覆盖 `compiler_module` 可绕过。
  行号：location 记 `compiler.py:519-536`，实测函数 519–539（537–539 为 `quote_name` 回退），
  精确危险点是 536 行裸返回，重叠故不改判。评分分歧：NVD 仅 CISA-ADP Secondary 4.3 MEDIUM（GHSA
  MODERATE），Django weblog 按厂商政策标 "high"；CVSS 字段保留 4.3 并记录 "high"。
  OSV CVE 的 4.2 与 5.1 introduced 事件都在 fixed 之后（区间倒置），判定改用 ECOSYSTEM/CPE 区间
  + 修复提交祖先。另：4.2.13 的 `add_filtered_relation()` 完全未调用 `check_alias()`，故空白别名
  在 4.2.13 也能进入 SQL——那是 CVE-2025-57833 的机制，不影响本案判定。细节见
  `runs/verification/django_CVE-2025-13372_4213/README.md`。
- **CVE-2025-59681（MySQL/MariaDB 列别名黑名单缺 `#`）**：独立复核 grade A
  （`runs/independent/django_CVE-2025-59681_4213_round31/verdict.json`，2026-10-24T20:20:08Z promote）。
  4.2.13 `Query.check_alias()`（`django/db/models/sql/query.py:1123-1128`，模式在第 51 行）拒绝
  引号、空白、分号与 `--` / `/*` / `*/`，**不含 `#`**；`annotate()`/`alias()`/`aggregate()`/`extra()`
  四条 `**kwargs` 路径都调用它，`ali#as` / `x#` 因而通过校验并参与 SQL 编译，4.2.25 加 `|#|`
  并改写错误文本。**证明限于校验边界**：本机无 MySQL/MariaDB，探针只编译不执行；生成的 SQL 中别名
  是反引号引用的（``AS `ali#as` ``），没有用执行证明未加引号的注释注入上下文；`aggregate()` 未修版
  只观察到「通过 `check_alias` 后连接被拒」。`test_alias_filtered_relation_sql_injection` 属于
  CVE-2025-57833（4.2.13 无、4.2.25 有，修复 patch 中是未改动上下文行），本案只改它的期望消息并
  在 `test_alias_forbidden_chars` 表加 `ali#as`。评分分歧：CNA/GHSA 7.1 HIGH，NVD Primary 9.8
  CRITICAL，卷宗临时采用 7.1 并列出全部口径。OSV CVE 的 GIT `fixed` 事件是发布 tag commit
  （4.2.25/5.1.13/5.2.7），不是 fix 提交；4.2 的 `introduced 97aa3b7f` 是分支头 artifact。
  只执行了 4.2.13/4.2.24/4.2.25，5.1/5.2/6.0 的修复由 patch 与祖先矩阵确认。细节见
  `runs/verification/django_CVE-2025-59681_4213/README.md`。
- **CVE-2025-64458（重定向目标在解析前无长度上限，Windows 上 NFKC 慢归一化 DoS）**：独立复核 grade A
  （`runs/independent/django_CVE-2025-64458_4213_round32/verdict.json`，2026-10-24T20:28:51Z 裁定，
  2026-10-24T20:29:54Z promote）。4.2.13 `HttpResponseRedirectBase.__init__`
  （`django/http/response.py:611-621`）先设 `Location`，再对 `str(redirect_to)` 调
  `urlparse()`（617 行），全程没有长度上限；`urllib.parse.urlsplit()` 对非 ASCII netloc 执行
  `unicodedata.normalize("NFKC", netloc)`，公告称该归一化在 Windows 上异常慢。reviewer 探针实测
  4.2.13/4.2.25 对 20,017 字符目标触发 `urlparse`×1 与 netloc（20,008 字符）NFKC×1；4.2.26 在解析前
  按 >2048 拒绝（0 parse / 0 normalize），4.2.27 把上界放宽到 >16384（ticket 36743），那是上游后续
  bugfix，**不是**本 CVE 的修复。5.1.14 / 5.2.8 是同批修复版本。**影响面仅 Windows**：Linux 上
  NFKC 约 1 ns/字符，未测出可用的 DoS 时延，故记录按「调用边界」而非「实测耗尽」表述；
  没有 HTTP 服务器参与，探针直接构造响应对象。评分：NVD 只有一条 Secondary 7.5 HIGH
  （AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H，CNA 为 DSF），GHSA 记 HIGH 而 Django release note 记
  "moderate"，卷宗按 7.5 记录并列出全部口径。4.2.26 与 4.2.27 的差异只影响拒绝阈值，不影响
  「4.2.13 受影响」这一判定。细节见 `runs/verification/django_CVE-2025-64458_4213/README.md`。
- **CVE-2026-25673（URLField 的 scheme 判定把整串值送进 `urlsplit()`，Windows NFKC DoS）**：独立复核
  grade A（`runs/independent/django_CVE-2026-25673_4213_round33/verdict.json`，
  2026-10-24T20:33:17Z 裁定，2026-10-24T20:35:57Z promote）。4.2.13 `URLField.to_python()`
  （`django/forms/fields.py:759-787`）内部的 `split_url()` 在 766 行执行 `list(urlsplit(url))`，
  无 scheme 时再解析一次（16→23 字符）；`urlsplit()` 对非 ASCII netloc 调
  `unicodedata.normalize("NFKC", netloc)`，公告称该归一化在 Windows 上异常慢。4.2.13 与 4.2.28 的
  `URLField` 类块内容逐字节相同（卷宗 README 记 1,478 字节；reviewer 按含块尾换行口径测得 1,479，
  内容相等已直接验证），4.2.29 不再导入 `urlsplit`/`urlunsplit`，改用
  `scheme, sep, _ = value.partition(":")` 加
  `isascii()`/`isalpha()`/`"/" in scheme` 判定。reviewer 探针在三版安装态各跑两遍：20,017 字符
  Unicode 目标 → `urlsplit`×1（整串）+ NFKC×1（20,008 字符 netloc），纯 ASCII 长串不归一化，
  4.2.29 全 12 例 0/0；把 4.2 fix hunk 应用到 4.2.13 源文件后 URLField 块与 4.2.29 逐字节相同、
  探针 0 调用。**影响面仅 Windows**：Linux 上 20,008 字符归一化约 0.02 ms，未测出 DoS 量级，
  记录按调用边界表述。附带的行为变化：值内部的换行/制表符不再由 `to_python()` 处理
  （`inner_newline` 在 4.2.29 原样返回），默认 `URLValidator` 仍拒绝，自定义 validator 可能不拒。
  评分：NVD 两条 Secondary 7.5 HIGH（无 Primary）、GHSA HIGH、Bitnami High，release note 记
  "moderate"。reviewer 另指出 4.2.29 的 `URLValidator` 对 ≤2048 输入仍走 `urlsplit`（有界残余
  路径），不影响「4.2.13 受影响」的判定。细节见
  `runs/verification/django_CVE-2026-25673_4213/README.md`。
- **CVE-2026-15307（GeoDjango 空间查找把 str/bytes 与 dict 直接交给 GDAL，写文件/SSRF）**：独立复核 grade A
  （`runs/independent/django_CVE-2026-15307_4213_round34/verdict.json`，2026-10-24T20:42:55Z 裁定，
  2026-10-24T20:45:40Z promote）。4.2.13 `BaseSpatialField.get_raster_prep_value()`
  （`django/contrib/gis/db/models/fields.py:172-189`）把任意 str/bytes/`__geo_interface__` 交给 180 行的
  `gdal.GDALRaster(value)`、任意 dict 交给 185 行的同一构造，调用点 `get_prep_value` 在 205 行；
  `GDALRaster.__init__` 对 `/vsi` 前缀跳过 `os.path.exists`（`gdal/raster/source.py:87-97`，可外连），
  dict 分支强制 `_write = 1`（129 行）并在 163 行 `capi.create_ds` 按攻击者 `name` 建文件。reviewer
  在无 root 用户态装出 GDAL 3.13.3 / GEOS 3.14.1 / Python 3.12.15，实测 dict、JSON 字符串与 admin
  changelist 三条路径各写出 694 字节 GTiff（sha256 `c9c452e0…`），`/vsicurl` 取值产生 15 次外连；
  5.2.17 与「4.2.13 + 5.2 fix」均抛 `DisallowedRasterLookup`、零写盘零外连。修复为 main `f1949c1f`、
  backport `115ffd04`（5.2.17）/`208f80cb`（6.0.8），6.1 正式版已含 `39b3e2d0`；4.2 线无修复，4.2.30
  的两个函数与 4.2.13 逐字节相同（采集方复算）。**边界**：GDAL 3.13.3 未必是目标部署版本，驱动集合
  与网络策略会变；**未证 RCE**（只证按攻击者路径写 GDAL 生成文件与 SSRF）；admin 一步跑在非空间
  sqlite 后端，写盘发生在 DB 适配之前；NVD 两条 Secondary CVSS 3.1 8.8 / 4.0 8.7 与 CWE-73+CWE-918
  （GHSA 仅 CWE-73）全部保留，未单取。细节见 `runs/verification/django_CVE-2026-15307_4213/README.md`。
- **CVE-2026-53877（GDALRaster 的 bytes 分支用 `sys.getsizeof` 当缓冲区长度，堆越界读）**：独立复核
  **grade B**（`runs/independent/django_CVE-2026-53877_4213_round35/verdict.json`，
  2026-10-24T20:45:29Z 裁定，2026-10-24T20:47:29Z promote）。4.2.13
  `GDALRaster.__init__` 的 bytes 分支（`gdal/raster/source.py:102-119`）在 106 行
  `size = sys.getsizeof(ds_input)`，把 `PyBytesObject` 头算进缓冲区长度（多约 32 字节；
  `sys.getsizeof(b"") == 33`，`create_string_buffer` 另加 1，合计 32），再交给
  `capi.create_vsi_file_from_mem_buffer`；读 `vsi_buffer`（244-258，`string_at(dat, out_length.value)`）
  时越过缓冲区。5.2.16（`6c66eb8c`）/6.0.7（`38dfbd27`）改为 `len(ds_input)` 并删 `import sys`，
  main 为 `6ca2bbe2ef`，6.1 正式版已含 `a46b417d`；4.2 无 backport。**本卷宗没有执行阶段**：复核机
  同样无 GDAL/GEOS/Django，九字段全部静态核实后按流水线规则停在 B，未做红/绿探针，越界未被实际
  观测。**边界**：`vsi_buffer` 在 4.2.13 库内没有调用者（只有属性与测试），影响需要应用层读取该属性
  后序列化；泄露还是崩溃取决于 allocator；4.2 未被厂商评估，4.2 范围靠 GHSA/PYSEC 的 `0 -> 5.2.16`
  与 4.2.13/5.2.15 整文件逐字节相同（sha256 `366b028d…`）推出；严重性 Django 说 low、GHSA MODERATE、
  NVD 4.8（3.1）/6.3（4.0）MEDIUM 均 Secondary，全部保留。细节见
  `runs/verification/django_CVE-2026-53877_4213/README.md`。
- **CVE-2026-15830（GeoDjango 把深层嵌套 GEOMETRYCOLLECTION 交给 GEOS，栈溢出 SIGSEGV）**：独立复核
  **grade B**（`runs/independent/django_CVE-2026-15830_4213_round36/verdict.json`，
  2026-10-24T20:55:51Z 裁定，2026-10-24T20:58:46Z promote）。4.2.13
  `django/contrib/gis/geos/prototypes/io.py` 的 `_WKTReader.read`（156）与 `_WKBReader.read`（167）
  把 WKT/WKB/HEXEWKB 直接交给 `wkt_reader_read`/`wkb_reader_read(_hex)`，无深度或数量检查；GEOS
  3.15.0 之前每层 `GEOMETRYCOLLECTION` 递归一次且无上限，上游 libgeos `8b8b3da7` 才加入
  `MAX_PARSE_DEPTH = 100`。Django 两阶段修复：5.2.17（`ba80833f`）/6.0.8（`6af5da31`）/6.1
  （`9e4a3f18`，main `d2e59b77`）加 `MAX_GEOM_COLLECTIONS = 198` 前置限流；5.2.18（`1eafa1a8`）/
  6.0.9（`4353dfb5`）/6.1.2（`75d401a1`，main `62ef9d40`）用结构化 `_WKBFrame` 栈式遍历替换字节模式
  扫描，堵住非法字节序 / 递归 MULTIPOINT / 大端 ISO HEXWKB 绕过——因此第一阶段提交在表中记为
  `fix_status=partial`，第二阶段记为 `complete`。**本卷宗没有执行阶段**：本机无 Django、libgeos_c 与
  GDAL，红/绿探针未跑，段错误未被实际观测；证据为 4.2.13/4.2.30 `io.py`/`geometry.py`/`forms/fields.py`
  逐字节相同、逐 tag grep、八个修复提交对 4.2.13/4.2.30 的祖先关系全为 False，以及 GEOS 补丁插入点。
  **边界**：Python 侧 198 只是 GEOS 缺陷的绕行方案，实际暴露还取决于链接的 GEOS 版本（≥3.15.0 已在
  GEOS 内限深 100），而快照不固定 GEOS 版本；也要求应用把用户可控文本送进 `GEOSGeometry`；GeoJSON
  走 GDAL，公告明说不受影响。公开记录矛盾照实保留（GHSA/PYSEC/Bitnami/NVD CPE 说 5.2.17+6.0.8，
  CVE 重写区间与 NVD 描述说 5.2.18+6.0.9；GHSA 的 `6.1a1 → 6.1.1` 偏晚，`9e4a3f18` 已是 6.1 终版
  祖先）。**复核后更正**：复核者指出卷宗 4.2 EOL 日期错一年（实为 2026-04-07 扩展支持结束，4.2.30
  同日发布为末版），另两处小误一并更正，见 `runs/verification/django_CVE-2026-15830_4213/
  POST_REVIEW_CORRECTIONS.md`；verdict 与 grade 未改。细节见同目录 `README.md`。
- 与上述各条无关但必须保留：`runs/verification/django_CVE-2024-41990_4213_probe/` 与
  `django_CVE-2024-45230_4213_probe/` 已证明两条 urlize DoS 的二次方行为是 4.2.14 引入的回归、
  在 4.2.13 上不可复现；对应候选维持 `possible_affected`，不得据此判 `confirmed_not_affected`。

## 8. rack v3.1.13 正样本（CVE-2025-49007）的边界

- **触发条件不是「任意长头行」**：3.1.13 `parser.rb:36` 的未锚定正则以贪婪 `(.*)` 配行尾
  lookahead，二次开销需要同一条 MIME 头行里堆多个字面量起点、且该行 CRLF 之后让 lookahead
  失败（例如折叠续行以空格开头）。单个字面量 + 超长值只呈线性。round37 复核者的纯正则实验
  里就有这个对照（场景 B/C），不要把它简述成「发个长头就能打」。
- **被扫描对象在请求体内**：这里是 multipart body 内部的 MIME 头，不是 HTTP 请求头块，前置
  服务器常见的 8 KB 请求头限制通常不适用；实际边界是 body-size limit（`CONTENT_LENGTH`、反代
  或应用上限）与并发。复核者实测 80 KB 的 part 头被纯 Rack 解析器完整接受并耗尽时间。
- **实测环境是本机 WSL2 + Ruby 3.2.3**：斜率 ≈2.01（3.1.13）与 ≈0.99（3.1.16）来自复核者在真实
  库上的 5 次重复中位数，属于该环境的一次测量，不是跨平台基准；断言的方向（版本修复前后由二次
  降为线性）不依赖绝对值。
- **区间低端只做到部分版本**：3.1.10–3.1.15 的 `parser.rb` 字节相同，3.1.0/3.1.5 整文件不同但
  第 36 行正则逐字节相同；3.1.1–3.1.4、3.1.6–3.1.9 未逐版 diff（区间由三个公开源一致给出）。
- **公开记录口径不一**：NVD CVSS 3.1 5.3 MEDIUM 为 Primary、GHSA/rubysec 4.0 6.6 并列；CWE-1333
  （NVD Primary）与 CWE-770（GitHub/CVE 记录）并列；`CHANGELOG.md` 在 v3.1.16 tag 上仍无
  `[3.1.16]` 小节，发行事实由 tag object、fix 祖先链与 RubyGems 时间共同佐证。

## 9. rack v3.1.13 第二条正样本（CVE-2025-61772）的边界

- **是「缺少上限」，不是放大**：3.1.13 `parser.rb` 的 `handle_mime_head`（306）等 part 头终止空行
  时，406-408 的 `else / :want_read` 没有字节上限，`read_data`（258-262）每次最多追加
  `BUFSIZE = 1_048_576` 字节。内存随客户端实际发送的 body 字节线性增长，上界是部署的 body 限制
  与并发，不是压缩炸弹式的小输入大开销。round38 复核者实测 VmHWM 增量 / body ≈ 1.0×。
- **扫描对象仍是 body 内的 MIME 头**：不是 HTTP 请求头块，前置服务器的请求头限制通常不适用。
- **实测环境是本机 WSL2 + Ruby 3.2.3**：3.1.13/3.1.16 在 1/4/16/64 MiB 下 `@sbuf` 与 VmHWM 的
  数值是单环境测量；方向性结论（3.1.17 在同一构造上 raise）不依赖绝对值。
- **修复阈值不是精确 64 KiB**：`MIME_HEADER_BYTESIZE_LIMIT = 64 * 1024` 比较的是整个 `@sbuf`，
  且检查在每次读之后发生，所以首个触发点是「大于 64 KiB 的第一个 BUFSIZE 整数倍」（默认
  BUFSIZE 1 MiB → 1 MiB 即抛；复核者用 16 KiB bufsize 复测在 `@sbuf = 81,920` 抛错，正是
  16 KiB 的第五个倍数）。写成 `max(64 KiB, BUFSIZE)` 只在 64 KiB 恰为 BUFSIZE 倍数时成立。
- **来源可复现性**：OSV×2 与 NVD 三个 JSON 是「某一时刻的响应」，重抓字节 sha 会变（规范化后只差
  键序与 `timestamp`）；其余上游产物逐字节可复现。详见该卷宗的 `POST_REVIEW_CORRECTIONS.md`。
- **区间低端只做到部分版本**：3.1.13/14/15 字节相同，3.1.16 含 49007 的正则修复但仍无本 CVE 的
  上限，3.1.0 结构相同；3.1.1–3.1.12 未逐版 diff（区间由三个公开源一致给出）。

## 10. rack v3.1.13 第三条正样本（CVE-2025-61770）的边界

- **是「缺少上限」，不是放大**：`handle_fast_forward`（271-292）在等第一个 boundary 时，
  `consume_boundary` 失败的 `else / :want_read`（287-289）没有字节上限，`read_data`（258-262）
  每次最多追加 `BUFSIZE = 1_048_576` 字节；`consume_boundary` 的 `@sbuf.terminate`（438）只移动
  扫描指针、不清空字符串。驻留字节随发送字节线性增长（round39 复核者：64 MiB preamble 时
  `VmRSS` 增量 +65,576 kB ≈ 64 MiB）。
- **峰值 RSS 可超过 payload**：Ruby String 扩容会复制缓冲区，round39 实测 64 MiB 时
  `VmHWM` 141,404 kB 对基线 25,856 kB，约 payload 的 1.6–2 倍；所以「无放大」只对**驻留字节**
  成立，不能读成峰值内存 1:1。
- **触发阈值不是精确 16 KiB**：`BOUNDARY_START_LIMIT = 16 * 1024` 比较的是整个 buffer，且检查在
  每次读之后，首个触发点是「大于 16 KiB 的第一个 BUFSIZE 整数倍」（默认 1 MiB → 1,048,576 B；
  BUFSIZE 8192 → 24,576 B，均为 round39 实测）。
- **实测环境是本机 WSL2 + Ruby 3.2.3 / gem 3.1.13、3.1.17**：绝对数值是单环境测量，方向性结论
  （3.1.17 在同一构造上抛 `multipart boundary not found within limit`）不依赖绝对值。
- **区间低端只做到部分版本**：采集方逐版取了 3.1.0/3.1.13/3.1.14/3.1.15/3.1.16/3.1.17；
  3.1.1–3.1.12 未逐版取文件（round39 复核者用 `git grep` + `git log -S` 覆盖全部 v3.1.x，
  确认 3.1.0–3.1.16 均无该常量、引入者确为 `e08f78c6`）。
- **公开记录的内部口径**：本条 CVE 的 GHSA/OSV/NVD/rubysec 一致指向真实修复提交，未出现
  61771 那种把相邻提交记错的情况；但 `published_at` 取的是 GHSA 时间（2025-10-10 之前上游
  已于 2025-10-07 发 3.1.17）。

## 11. rack v3.1.13 第四条正样本（CVE-2025-61771）的边界

- **是「缺少上限」，不是放大**：没有 `filename` 的 part 用 `BufferPart`（`parser.rb:131-134`），
  其 body 由 `Collector#on_mime_body`（169-171）逐块 `<<` 进一个常驻 String（160 创建）；
  `check_part_limits`（178-195）只限打开文件数与 part 数，从不算字节。round40 复核者实测
  64 MiB 单字段 GC 后 RSS 增量 +67,416 KiB ≈ 1.03× payload（峰值约 1.6× 属分配常数因子）。
- **只影响非文件字段**：带 `filename` 的 part 落 Tempfile，不占这条上限，也不驻留内存
  （round40 对照：64 MiB 带 filename 时 GC 后 RSS 仅 +约 2 MiB）。
- **公开记录把两段改动记混**：GHSA、OSV 的 GIT range 与 rubysec 引用的
  `e08f78c6`/`589127f4`/`d869fed6` 只加 `BOUNDARY_START_LIMIT` 与
  `MIME_HEADER_BYTESIZE_LIMIT`（属 61770 / 61772）；真正的 retained-size 提交是它们的
  **子提交** `f224f93b`/`3beacfcd`/`c370dcd9`。卷宗按代码、tag、祖先关系与逐版字节认定后者，
  并把这个冲突写进 `POST_REVIEW_CORRECTIONS.md`，不做「公告一定对」的推断。
- **公告与实现的数值/变量名不一致**：公告写缓解措施「e.g., 2 MiB」，实际默认
  `BUFFERED_UPLOAD_BYTESIZE_LIMIT = 16 * 1024 * 1024`；commit message 写
  `RACK_MULTIPART_MAX_BUFFERED_UPLOAD_SIZE`，代码与 README 写
  `RACK_MULTIPART_BUFFERED_UPLOAD_BYTESIZE_LIMIT`。以代码为准，两处都照实记录。
- **异常类名易误读**：源码是 `raise Error, "multipart data over retained size limit"`，
  `Error` 是 `Rack::Multipart::BoundaryTooLongError` 的别名，实测 `e.class.name` 为该子类名。
- **实测环境是本机 WSL2 + Ruby 3.2.3 / gem 3.1.13、3.1.16、3.1.17**：单环境测量；3.1.16 仍无
  上限这一点由复核者实测（16 MiB 成功驻留）确认。
- **区间低端只做到部分版本**：采集方逐版取了 3.1.0/3.1.13/3.1.14/3.1.15/3.1.16/3.1.17；
  3.1.1–3.1.12 未逐版 diff。

## 12. rack v3.1.13 第五条正样本（CVE-2025-61919）的边界

- **是「缺少上限」，不是放大**：`Rack::Request#POST`（`lib/rack/request.rb:531`）在 url-encoded
  分支调用 `get_header(RACK_INPUT).read`，即 `IO#read(nil)` 读尽到 EOF，早于任何长度检查。
  round41 复核者实测 1/8/32/64 MiB body 的 VmRSS 增量 +1,024/8,192/32,896/65,536 KiB，
  线性且约 1.0× payload，所以影响取决于部署侧 body cap、并发与单请求大小，而非库内乘数。
- **只覆盖 url-encoded 分支**：同一 32 MiB body 走 `text/plain` 时该分支不进入，读取 0 字节、
  RSS 增量 0 KiB（复核者对照）；multipart 走 `Rack::Multipart`，属 61770/61772 等其它 CVE。
- **「3.1.13 两处无界」只有一处属于本 CVE**：读无界属本 CVE；随后的 `QueryParser` 解析在
  3.1.13 也无界，但那是 **CVE-2025-46727**（3.1.14 引入 `BYTESIZE_LIMIT`/`PARAMS_LIMIT` 修复）。
  本 CVE 的 3.1 修复提交 `cbd541e8` 对 `query_parser.rb` 只加 `attr_reader :bytesize_limit`。
- **3.1.17 是中间态**：parser 已把解析限制在 4 MiB，但读仍先发生——复核者用 8 MiB body 观察到
  `read_calls=[null]`、8,388,610 字节全部读入后才抛 `QueryLimitError`；3.1.18 才把读本身
  限制在 `bytesize_limit + 2 = 4,194,306` 字节。`+2` 与 `|| ''` 都是必要的（否则 limit+1 位为
  NUL 且其后仍有字节时，超限 body 会被静默截断接受；空 body 时 `read` 返回 nil）。
- **`fixed_releases` 只有一条对本快照有操作意义**：3.1.18；3.2.3（`e179614c`）与
  2.2.20（`4e2c9039`）是另两条线的首发，作为元数据并列，不是 3.1.x 的可安装修复。
- **单一 CWE-400**：NVD、GHSA 与 CVE.org 都只给 CWE-400；未把 CWE-770 写进字段。
- **复核后更正**：`entry_point.line` 原写 `503-542`，实为 `503-551`（`def POST` 到 `end`），
  已改 builder/`dossier.json` 并用 `runs/data_fixes/fix_61919_lines_2026-10-25.py` 守卫式改写
  已入库 location 行；3.1.18 `check_query_string` 的检查行实为 222-223（原写 221-223）。
  `critical_operation.line = 531-531` 与 evidence 行未改动。
- **实测环境是本机 WSL2 + Ruby 3.2.3 / 真 gem 3.1.13、3.1.17、3.1.18**：单环境测量；
  gem 取自 RubyGems 官方包并与 tag 文件逐字节比对；另测 `RACK_QUERY_PARSER_BYTESIZE_LIMIT`
  在 3.1.13 上无效、在 3.1.18 上生效（反证）。

## 13. rack v3.1.13 第六条正样本（CVE-2025-61780）的边界

- **是「把请求头当配置」，不是任意文件读**：`variation`（`sendfile.rb:148-152`）在未配置 variation
  时回退到 `env['HTTP_X_SENDFILE_TYPE']`（151），客户端因此能打开 sendfile 并选择回写哪个响应头
  （`headers[type.downcase]`，123/134）；`map_accel_path`（154-165）在应用层无 mappings 时回退到
  `env['HTTP_X_ACCEL_MAPPING']`（157），客户端还能决定内部路径到外部 URL 的替换。可见面是代理映射到
  的内部 URL 与 `x-sendfile` 分支泄露的绝对路径；公告明确说不能任意读文件。
- **两半可分开触发**：启用半只在「未配置 variation 且 `env['sendfile.type']` 未设」时生效；映射半在
  「应用层 mapping 没匹配上」时生效，所以**显式配置了 x-accel-redirect 的部署仍受影响**。
  修复（`7e69f65e`）有意保留后者——`x_accel_mapping` 仅在 `@variation` 匹配 x-accel-redirect 且
  `@mappings` 为空时读头——这是设计取舍，不是修复不彻底。
- **前提由内置组件满足**：`Rack::Files` 的响应体有 `alias :to_path :path`（`files.rb:185`），
  使 `body.respond_to?(:to_path)`（116）为真；但仍需前置代理转发这两个客户端头并执行返回的
  `x-accel-redirect` / `x-sendfile` 头，固定或剥除这两个头的部署不受影响。
- **`^` → `\A` 是修复的一部分**：3.1.13 上含换行的路径可满足 `^` 锚点，round42 复核者实测
  `…safe%0A/pwned/.txt`；3.1.18 的 `\A` 不再匹配。
- **版本覆盖**：`sendfile.rb` 在 v3.1.13 / v3.1.17 / v3.2.2 字节相同（`395efb8b…`），在 v3.1.18 /
  v3.2.3 字节相同（`b0b8a22e…`）；v3.1.0 已含两处回退。复核员另补测 v3.1.14 / v3.1.15 / v3.1.16
  仍为 `395efb8b…`，3.1.1–3.1.12 仍未逐版 diff。
- **`fixed_releases` 三条只有 3.1.18 对本快照有操作意义**：3.2.3（`57277b77`）与 2.2.20
  （`fba2c8bc`）是另两条线的首发。
- **`fix_commits[].commit_date` 用 UTC**：`7e69f65e`/`fba2c8bc` 的 committer date 是
  `2025-10-10T12:57:11+13:00` / `2025-10-10T12:23:52+13:00`，UTC 日期为 2025-10-09；`57277b77`
  为 `2025-10-10T00:34Z`。已按 UTC 记录并在 note 里保留原文。
- **公开记录无归属混淆**：三个提交就是三个分支的真实修复；但发布顺序是 CVE（16:53:57Z）与 NVD
  （17:15:39Z）**早于** GHSA（17:31:31Z），与 CVE-2025-61919 相反。
- **CWE / 评分的取舍**：公开记录给 CWE-200 / 441 / 913 与两个 CVSS 3.1（5.8 Secondary `S:C`、
  5.3 Primary `S:U`）。数据集保留全部已发布值，未按复核员的「CWE-441 为主」建议裁剪 `cwe_ids`。

## 14. vite v5.0.11 上 CVE-2025-46565 的负面测量边界（round60）

- **这是测量，不是判定**：`runs/verification/vite_v5.0.11_CVE-2025-46565/` 记录的是「冻结快照上没跑出来」，
  `finding = not_reproduced_at_snapshot`、`decision = null`。它不把候选升级为 `confirmed_not_affected`，
  `data/snapshot_candidate_triage.jsonl` 里该行仍是 `possible_affected`（`checked_at 2026-10-23T21:54:53Z` 未动）。
- **负面结果的覆盖**：19 条「经 `/.` 取被拒文件」的形状 × 2 种 deny 配置（vite 默认清单；显式
  `['**/.env','**/.env.*','**/*.{crt,pem}','**/src/secret.txt']`）+ 15 条 `?raw`/`?import`/`?url` 组合（仅 5.0.11）。
  未穷尽：自定义 `fs.allow`、`deny` 的其它写法、Windows 路径分隔符与大小写不敏感文件系统、reverse proxy 重写、
  HTTP/2 与 `curl --request-target` 的原样形式都未测。结构性论据只到「5.0.11 的 matcher 带 `matchBase: true`，
  因此 basename 模式对尾斜杠路径同样生效」，不等于全配置证明。
- **区间不匹配是已知缺口**：OSV/公告的 5.x 区间是 `5.0.0 -> 5.4.19`，实测缺陷从 `ba5269cca`（v5.2.6）才出现。
  这不表示 5.0.0–5.2.5 的公告条目错了（它可能覆盖别的形状或别的平台），而是本包的矩阵没有为那段区间提供阳性——
  不能把「快照不透露」写成「区间不透露」。
- **同快照仍存在的相邻泄漏**：5.0.11 上 `/.env?raw` 与 `/.env?raw?import` 直接返回 `.env` 字节（353 / 365 B JS module），
  属 CVE-2025-31125 的族（5.4.16 修，已 `confirmed_affected`）。所以「快照安全」是错的，正确的说法只有
  「`/.` 静态路在该快照不透露」。
- **`/.` 在 raw 族里反而使请求失败**：5.0.11 上所有带 `/.` 的 `?raw` 形状 500 或 shell，连允许文件
  `/allow.bin/.?raw?import` 也 500 —— 说明那条路径在 deny 判定之前就结束，不能当作守卫生效的证据。
- **只在采集侧执行**：5 棵树的 cli sha256 前缀记在 `repro/summary.json`（`3586d12a` / `c7524992` / `a000eda7` /
  `0edabed1` / `b1182f32`），无独立复核；4.5 / 6.x 的修复关系只凭 pin 的补丁与祖先断言，未执行。
- **严重性记录为发布源分歧**：NVD/OSV 唯一向量 CVSS 4.0 6.0 MEDIUM（`UI:P/VC:H/SC:N`），同日 GHSA 页面渲染
  Moderate 但计算器指标对应 `UI:N/VC:L/SC:H`；两者原样保留，未择一平滑。
