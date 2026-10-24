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
- 126 条 live 漏洞行全部有审核记录：75 条 B 级 + 51 条 A 级；其中 97 条属于 48 个评测快照并各有
  `confirmed_affected` 状态行，29 条 catalog 行位于非评测快照/历史 tag。A 级要求独立 reviewer 动态
  red/green（如 grpc CVE-2023-1428 在 v1.52.0 `GPR_ASSERT(x == kTrailers)` SIGABRT、v1.53.0 同字节
  不 abort）；B 级不等于 PoC 已验证。
- 正式 Oracle（`snapshot_vulnerability_status`）的 97 行只覆盖评测快照中的已确认正样本，无
  `confirmed_not_affected/unknown/out_of_scope` 行。「没有 unknown」不等于「该 SHA 无其他漏洞」：
  未收录漏洞受检索与相关性筛选缺口限制。

- `data/reviews.jsonl` 的 `reviewer` 字段是采集方自述，`promote_verified_rows.py` 原样写入
  dossier 的 `prepared_by`，因此 31 行仍写着「independent reviewer not yet assigned」，
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

- 2626 条候选 → 2613 条 triage 行：117 confirmed_affected / 1321 confirmed_not_affected /
  573 possible_affected / 574 unknown / 28 duplicate（决策来自既有证据与独立复核，零 LLM）。
  2613 = 2064（截至范围判定批次）+ 549 条为「已选版仓库内此前从未有 triage 行的候选」补的 unknown 行
  （`runs/triage_untriaged_unknown_2026-10-24/`，逐行核对 snapshot 等于当前 evaluation_target），
  仅为漏斗补全，**不构成核验**。
- 1321 条 confirmed_not_affected 的依据是既有驳回卷宗里的版本/分支区间（如「fix already in <tag>」「introduced
  after <tag>」）、cached OSV 范围与 GIT 修复提交祖先关系，非裸 semver 字符串比较；仍属规则层判断，
  未逐条做独立源码复核。其中 65 条来自 2026-10-24 的低侧证明批次（`runs/triage_low_side_2026-10-24/`
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
  已有范围/代码级决策，区间命中的一律记入 `possible_affected`（django 28、rack 21、libexpat 36），仍需源码复核。
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
- 581 条 `possible_affected` 只是「已发布的机器可读区间包含冻结 tag」，**不是已确认漏洞**：30 条来自早期
  triage，45 条于 2026-10-24 由 OSV-by-alias 区间命中移入（`runs/osv_alias_2026-10-24/`，如 expat
  R_2_6_2 落在 CVE-2024-45490/91/92 的 `fixed 2.6.3` 之下、cJSON v1.7.16 落在 CVE-2025-57052 的
  `[1.5.0, last_affected 1.7.18]`），521 条由当前生成器的 `possible_affected_range` 提案统一落盘
  （`runs/data_fixes/apply_remaining_possible_2026-10-24.py`）。其中一部分来自粗粒度渲染
  （`<= 1.27.2`、`All versions`），命中偏保守，源码复核时应优先看；撤回/驳回的 advisory 不参与
  （express `adv3_087476da78c375b4` 保持 unknown）。其中 5 条 cJSON v1.7.16 候选（CVE-2023-53154 ×3、
  CVE-2023-50472 ×2）已于 2026-10-24 经独立复核升为 `confirmed_affected`，另 3 条是已确认漏洞的重复
  discovery 行（cJSON CVE-2023-50471、libexpat CVE-2024-45490 ×2），已按既有 A/B 记录链接为
  `confirmed_affected`；其余全部待源码级复核。
  按「命中 tag 的那条边界」分类（`runs/possible_review_queue_2026-10-24/`，2026-10-24 按当前表重跑）：双侧区间 404、
  只有上界/`All versions` 83、NVD CPE 23、alias OSV 42、早期 triage 30；队列已按仓库与证据质量排出，
  但**没有任何一条**因入队而被提升或排除。django CVE-2024-42005、CVE-2024-39329、CVE-2024-41991 与 gitea
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

## 7. 2026-10-24 五条 django 4.2.13 正样本的边界

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
- 与这五条无关但必须保留：`runs/verification/django_CVE-2024-41990_4213_probe/` 与
  `django_CVE-2024-45230_4213_probe/` 已证明两条 urlize DoS 的二次方行为是 4.2.14 引入的回归、
  在 4.2.13 上不可复现；对应候选维持 `possible_affected`，不得据此判 `confirmed_not_affected`。
