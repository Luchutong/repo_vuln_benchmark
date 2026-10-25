# RepoVuln-50 v0.2 数据集构建工作记录

- 工作目录：`/home/luchitong/work/repo-vuln-50-v02`
- 启动包：`/home/luchitong/work/repo_vuln_50_agent_starter_v02.zip`（摘要见 manifest.json）
- 启动日期：2026-10-21，Asia/Shanghai
- 当前阶段：P6 草案（正式 Catalog + Snapshot Oracle 已建立；已知漏洞搜索停止条件未满足）
- 状态：draft；29 条漏洞完成静态独立复核（grade B，覆盖 JS/Python/Ruby/Go/PHP/C#/Java/Rust/TypeScript/C/C++/Elixir），未发布，不能用于宣称完整真值。

## 固定要求

以 WORKFLOW.md 为执行规范。50 个真实官方上游、至少 10 种主语言；不设漏洞数量上限。保留全部候选、失败请求和来源盲区。历史漏洞目录和指定 SHA 真值分开；未知不能作无漏洞或误报。最终数据集不保存完整源码，不自动执行 PoC 或仓库指令。

## 阶段清单

- [x] 检查启动包并保留原始 Schema 与结构校验器。
- [x] 创建九张核心 JSONL 表和可续跑目录。
- [x] 建立 150–250 仓库预选池，取得真实元数据并预览语言分布。
- [x] 选定 50 仓库并完成质量评分及证据（50 PASS，分数 77–100，12 种主语言）。
- [ ] 按仓库全量检索公共库、官方源、历史补丁及第三方披露（OSV/NVD/repository advisory 已完成；
      官方发布与历史补丁已对 29 条提升漏洞闭环，停止规则未满足）。
- [ ] 核验 CVSS/CWE、脆弱 SHA、修复 SHA、首次修复发行版（29/2626 候选完成）。
- [x] 指定 SHA 全语言盘点（73 个快照，Linguist 9.7.0，full_scan，ls-tree 一致）。
- [ ] 漏洞根因定位（29 条完成；其余候选仍为 pending_location/in_validation）。
- [ ] A/B 级独立复核和必要的隔离红绿测试（29 条 grade B 静态复核；无红绿测试）。
- [ ] 评测快照逐漏洞真值矩阵、覆盖报告和发布验收（22 个评测快照 × 29 条漏洞已建矩阵；
      覆盖仍全为 NEEDS_REVIEW，未发布）。

## 执行记录

### 2026-10-21：初始化

已解包流程、Schema、校验与评分脚本；原始文件摘要已写入 manifest.json。正式表先留空，预选数据位于 runs/preselection，避免为凑数量填写虚假质量 PASS、审核者或语言清单。

### 2026-10-21：首轮采集与试核验

- 已联网采集 180 个仓库的真实 GitHub 元数据，保存 189 次观察（含 9 个修正前失败/迁移响应）。修正 Kludex/starlette、composefs/tar-rs、ruby/rubygems 等上游路径；3 个归档项目暂缓。
- 建立 50 个优先核查项，当前默认分支主语言为 12 种，每种最多 5 个。它们不是最终通过质量准入的 50 仓库；指定 SHA 的全语言盘点尚未开始。
- 50 个 OSV 包查询均完整翻页成功，保留 1,270 个来源别名簇；另外保留 5 条 cJSON 补充搜索线索，共 1,275 条未核验记录。不得把它们称作 1,275 个已验证独立漏洞。
- OSS-Fuzz 包入口 cjson、expat、yaml-cpp、tinyxml2 返回零条；这是明确的检索盲区，下一轮需补查官方/NVD/CVE/历史补丁，不能推出项目没有漏洞。
- 为 Flask / CVE-2023-30861 建立首个静态证据档案，核对 CNA CVSS、脆弱 tag 的 SHA、两分支修复提交及 release 比较、源码片段和上游回归测试差异。仍缺独立复核和语言普查，状态 NEEDS_REVIEW；没有运行 PoC。
- 九张正式表保持空；预选未决记录位于 runs/preselection。未填写虚假的质量 PASS、A/B grade、第二 reviewer 或快照真值。最终 Catalog 尚为 0。
- 已增加可续跑脚本、查询缓存、原始响应 SHA-256、依赖锁文件和 5 个采集边界测试。所有失败和盲区在报告中披露。

### 2026-10-21：准入、全语言快照与正式表迁移

- 50/50 仓库通过六项质量准入门槛（最低 77 分，12 种主语言，每类 3–5 个，无单一语言超过 10/50）。
  证据保存在 `runs/admission/`，正式表 `data/repositories.jsonl` 为 50 行。
- 快照构建改为**按记录的 `head_sha_observed` 精确 fetch**（`git init --bare` + `git fetch --depth=1`，
  校验 FETCH_HEAD）。此前按分支 tip 克隆导致 9 个仓库的快照 SHA 与准入观察不一致（axios、gitea、
  laravel、libarchive、netty、rails、rustls、spring-framework、next.js），已全部重建；旧的错误快照
  移入 `runs/language/superseded/`，未删除，供审计。
- 全语言盘点：53 个快照全部 `full_scan=true`，`enumeration_matches_git_ls_tree=true`，共 188,870
  个跟踪文件；Linguist 9.7.0 固定版本；发布物不保留源码。
- 官方 GitHub repository advisory 源族：`api.github.com` 匿名 403 限流后改用 `gh auth token` +
  urllib + Link 分页。50/50 成功，846 条公告记录，36 个仓库非空、14 个空列表；原始响应、分页
  SHA-256 与限流头保存在 `runs/discovery_v3/`。空列表按“检索结果”记录，不推导为无漏洞。
- 发现并记录的数据质量问题（未静默修复）：`CVE-2024-51999` 在 CVE List 中为 REJECTED；
  lodash 多个公告的修复版本冲突；同一 fix commit 被发布时间相隔数年的公告复用（已把后一条降级为
  `pending_location`）；express `5.0.0` release 路径 404、正确 tag 为 `v5.0.0`；GHSA ID 大小写导致
  Schema 误拒。详见 `runs/verification/data_quality_findings.md`。

### 2026-10-21：三条漏洞完成独立复核与提升

- 建立三份逐字段核验档案（JS/Python/Ruby）：express `GHSA-qw6h-vgh9-j6wx` / CVE-2024-43796、
  flask `GHSA-m2qf-hxjv-5gpq` / CVE-2023-30861、rack `GHSA-wq4h-7r42-5hrr` / CVE-2022-30123。
  每份包含：别名交叉源、CNA/NVD CVSS 分歧、受影响范围、精确脆弱 SHA、fix commit 可达性、
  首次修复发行版内容核对、根因文件/函数/行号、限制说明。
- 三个独立 reviewer 在隔离上下文、只读、未读取采集档案的条件下复核，全部九个 `fields_verified`
  为 true，位置文件相同且行号重叠。grade 分别为 B、B、A；rack 的 A 因无动态复现被推广脚本自动降为 B。
  未伪造 reviewer 身份、CVSS、修复版本或行号。
- `scripts/promote_verified.py` 作为硬门槛：无 verdict、任一字段未验证、commit 不一致、文件不一致、
  行号不重叠、缺 reviewer/时间，任一条件即不提升。本次 3 promoted / 0 pending。
- 正式表：`vulnerabilities` 3、`locations` 3、`reviews` 3（grade B×3）、`evidence` 150。
  证据按 `field_evidence` 显式映射到 canonical 字段，不再用自由文本 `supports` 充当字段路径。
- 评测快照：express 4.19.2（npm gitHead `b28db2c…`，与 tag 树相同）、flask 2.3.1、rack 2.2.3，
  均标记 `evaluation_target=true`；真值矩阵 3 行全部 `confirmed_affected`，
  方法 `version_range_plus_code`，绑定版本范围、精确 SHA、根因位置与修复发行版内容。
- 候选表 2626 行（含 846 条官方 advisory 归一化记录），其中 4 行标记 `verified`；其余保留
  `in_validation` / `pending_location` / `pending_version` / `discovered` 与阻断原因。
- 覆盖：50 个仓库仍全部 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`。本轮新增 3 条已验证漏洞，
  最近两轮零新增的条件不成立；因此没有声称已知漏洞穷尽。
- `validate_dataset.py --draft`：0 error / 51 warning（warning 为未解决候选、grade A 比例等
  透明性提示）。draft 通过不等于发布验收。

### 2026-10-21：四条新语言漏洞完成独立复核与提升（Go/PHP/C#/Java）

- **gin-gonic/gin — GHSA-6vm3-jj99-7229 / CVE-2020-36567（Go）**。脆弱发行版 v1.5.0
  （lightweight tag → `15ced05c5316609bce5b43389f8e3f06102a8b18`），修复提交
  `a71af9c1...`（"removing log injection (#2277)"），首次修复 v1.6.0
  （`c4fd2489...`）。根因 `logger.go:144-151`（`defaultLogFormatter`）用 `%s`
  写入 `param.Path`，v1.6.0 改为 `%#v`。快照 `snap_d4899c7054105aea`，
  99 个跟踪文件，Go 第一方 45 个文件 / 153,320 字节 / 27.29%。
  NVD 主 CVSS 3.1 7.5 HIGH；CNA 用 CWE-117，NVD 用 CWE-116，两者都记录。
  独立复核另发现公告引用的 PR #2237 从未合并，实际合入 PR #2277；commit SHA
  本身正确，已记入 `data_quality_findings.md` 第 8 条。
- **guzzle/guzzle — GHSA-25mq-v84q-4j7r / CVE-2022-31090（PHP）**。脆弱发行版 7.4.4
  （`e3ff079b...`），修复 7.4.5（`1dd98b05...`，即 tag 提交）。根因
  `src/RedirectMiddleware.php:91-99`：跨源跳转只用 host 判断是否清除
  `CURLOPT_HTTPAUTH` / `CURLOPT_USERPWD`，同 host 换 scheme 或端口仍携带
  Authorization；修复改用 `Psr7\UriComparator::isCrossOrigin`。快照
  `snap_efe695448113758a`，117 个跟踪文件，PHP 第一方 42 个文件 / 30.10%。
  CNA 与 NVD 均 7.7 HIGH；CWE 分歧为 CNA CWE-200、NVD CWE-212，两者都记录。
  独立复核确认修复由 release commit 引入（其父提交的 blob 与 7.4.4 相同），
  并指出同一提交还修了 CVE-2022-31091，但本条目只取 curl-auth 那段。
- **JamesNK/Newtonsoft.Json — GHSA-5crp-9r3c-p9vr / CVE-2024-21907（C#）**。
  脆弱发行版 12.0.3（`7c3d7f8d...`），首次修复 13.0.1（`ae9fe44e...`）。
  `JsonReader` 构造函数不设默认 `_maxDepth`，`Push` 的深度检查
  （`JsonReader.cs:353`）因 null 短路，默认无上限；修复是默认值变更而非逻辑
  变更：`7e77bbe1` 设为 128，`b6dc05be` 再降为 64，13.0.1 实际发货 64。
  快照 `snap_25561773eac9d84f`，1139 个跟踪文件，C# 916 个 / 80.4%。
  NVD/CISA-ADP 7.5 HIGH，CWE-755。独立复核指出 CNA/NVD 与 OSV 对“反序列化
  还是序列化阶段栈溢出”的描述不一致，源码支持 OSV；已记入
  `data_quality_findings.md` 第 9 条。
- **netty/netty — GHSA-wm47-8v5p-wjpj / CVE-2021-21295（Java）**。脆弱发行版
  netty-4.1.59.Final（annotated tag object `da69023f` → commit `97d04481...`），
  修复提交 `89c241e3...`，首次修复 netty-4.1.60.Final（`eef26e8b...`）。
  根因在 `DefaultHttp2ConnectionDecoder` 的 `onHeadersRead` / `onDataRead`：
  未按 RFC 7540 §8.1.2.6 记录或校验 Content-Length，HTTP/2 转 HTTP/1 时可被
  请求走私；修复新增 `HttpUtil.normalizeAndGetContentLength` 与
  `verifyContentLength`。快照 `snap_bb344e672a0544ef`，3117 个跟踪文件，
  Java 第一方 1779 个文件 / 60.98%。CNA 与 NVD 均 5.9 MEDIUM，CWE-444。
  独立复核指出 advisory 正文误指 `Http2MultiplexHandler`、OSV 另有更宽的
  聚合坐标、NVD 版本写法为 `4.1.60`，已记入 `data_quality_findings.md` 第 10 条。
- 推广门槛：7 promoted / 0 pending，全部九项 `fields_verified=true`，grade B。
  正式表更新为 7 漏洞、7 位置、7 复核、215 证据、7 行真值矩阵；评测快照 7 个
  （express 4.19.2、flask 2.3.1、rack 2.2.3、gin v1.5.0、guzzle 7.4.4、
  Newtonsoft 12.0.3、netty 4.1.59.Final）。候选表 `verified` 行为 9：
  flask 与 netty 各有一个 v2 OSV 簇和一个 v3 advisory 簇，别名集合不同而
  各保留一行，分别指向同一条漏洞；它们不是 9 条漏洞。
- `validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，
  1 条为 grade A 比例）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；
  本轮新增 4 条已验证漏洞，停止规则不满足。

### 2026-10-21：Rust 与 TypeScript 漏洞完成独立复核与提升

- **hyperium/hyper — GHSA-6hfq-h8hq-87mf / CVE-2021-21299（Rust）**。脆弱发行版
  v0.14.2（lightweight tag → `8861f9a7867216c81ea14ac6224c11a1303e7761`），
  修复提交 `8f93123e...`（"fix(http1): fix server misinterpretting multiple
  Transfer-Encoding headers"），首次修复 v0.14.3（`48d45949...`，fix 的直接父提交）。
  根因 `src/proto/h1/role.rs:200-213`：循环处理每个 Transfer-Encoding 头，
  chunked 值置 `is_te_chunked=true` 并切换 CHUNKED，后续非 chunked 值没有
  else 分支清除；行 261 的 `if is_te && !is_te_chunked` 因此不触发，
  `Transfer-Encoding: chunked` + `afterlol` 被当作 chunked 接受。快照
  `snap_735b41cb13177d03`，93 个跟踪文件，Rust 第一方 62 个文件 / 63.77%。
  NVD 主评分 8.1 HIGH，CNA/GHSA 4.8 MEDIUM，两者都记录（findings 第 11 条）。
  独立复核另确认 `v0.12.36`、`v0.13.10` 已含修复，而 `v0.12.35`、`v0.13.9`
  仍脆弱；本目录只声明实际读过的 0.14.x 范围。
- **vitejs/vite — GHSA-c24v-8rfc-w8vw / CVE-2024-23331（TypeScript）**。
  脆弱发行版 v5.0.11（`b44c4930...`），修复提交 `91641c4d...`
  （"fix: fs deny for case insensitive systems (#15653)"），首次修复
  v5.0.12（`ee81e196...`）。根因 `packages/vite/src/node/server/index.ts:620`：
  `_fsDenyGlob` 用 `picomatch(config.server.fs.deny, { matchBase: true })`
  构造，缺少 `nocase: true`；在大小写不敏感文件系统上，改换大小写的路径
  不匹配 deny 规则，却在文件系统解析到同一文件，从而绕过 `server.fs.deny`。
  消费点是 `static.ts:216` 的 `server._fsDenyGlob(file)`，该文件在
  v5.0.11 与 v5.0.12 完全相同。快照 `snap_2e50b228f2432623`，1780 个跟踪文件，
  TypeScript 第一方 173 个文件 / 28.31%。CNA/NVD/OSV 一致为 7.5 HIGH、
  CWE-178/200/284；四分支 fix commit 与 NVD 的 Windows-only CPE 条件
  记入 findings 第 12 条。
- **libexpat/libexpat — CVE-2022-25235（C）**。
  脆弱发行版 R_2_4_4（annotated tag `c637e3b1...` peel 到
  `81b89678...`），修复提交 `3f0a0cb6...`
  （"lib: Add missing validation of encoding (CVE-2022-25235)"），首次修复
  R_2_4_5（`97a48405...`）。根因 `expat/lib/xmltok_impl.c:1141-1155`：
  `prologTok` 的 LEAD_CASE 与 `CHECK_NAME_CASE`/`CHECK_NMSTRT_CASE`
  宏在调用 `IS_NMSTRT_CHAR`/`IS_NAME_CHAR` 前缺少 `IS_INVALID_CHAR`
  校验；修复在三处插入 guard。快照 `snap_d33251dac37c334c`，153 个跟踪文件，
  C 第一方 33 个文件 / 0.68%。NVD 9.8 CRITICAL、CWE-116，CNA 未给
  CVSS/CWE；OSV 的 fixed 事件指向 release commit 而非代码修复提交，
  记入 findings。
- **protocolbuffers/protobuf — CVE-2022-1941（C++）**。
  脆弱发行版 v3.20.1（lightweight tag `21027a27...`），修复提交
  `b4c395aa...`（"Apply patch"），首次修复 v3.20.2（`a20c65f2...`）。
  根因 `src/google/protobuf/wire_format_lite.h:1821-1890`：
  自由模板函数 `google::protobuf::internal::ParseMessageSetItemImpl`
  （不是 `WireFormatLite` 成员，类在第 746 行结束）用 `last_type_id == 0` 与
  `message_data.empty()` 充当状态哨兵，没有显式状态机，重复的
  type-id/message tag 不被拒绝；修复引入
  `enum class State { kNoTag, kHasType, kHasPayload, kDone }` 并在终态
  跳过重复 payload。快照 `snap_6bc3f36eb61ef280`，2451 个跟踪文件，
  C++ 第一方 472 个文件 / 36.84%。公告未引用修复提交，该提交由
  v3.20.1..v3.20.2 历史与祖先关系证明；CNA 5.7 与 NVD 7.5 的评分分歧
  记入 findings 第 13 条。
  round1 reviewer 指出 dossier 误把函数写成 `WireFormatLite` 成员且行号只覆盖
  1827-1877，九项中 `location=false`；dossier 已改为完整符号与 1821-1890，
  由新的 round2 reviewer 复核，九项全 true、grade B。round1 verdict 移到
  `runs/independent/superseded/` 保留审计，未改字段。提升时结构校验先报两处
  schema 违规（`code_excerpt` 1609 字符 > 500、openwall 引用为 http），
  已将摘录压到 470 字符并改写为 https 后重新提升。
- **phoenixframework/phoenix — CVE-2022-42975（Elixir）**。
  脆弱发行版 v1.6.13（annotated tag `f0425c12...` peel 到 `6234b576...`），
  修复发行版 v1.6.14（`50b48541...`）。公告只引用 mainline 提交 `6e7185b3...`，
  该提交不在 v1.6.14 祖先链上；1.6.14 实际包含等价提交 `b2fc631f...`
  （父提交即 v1.6.13 peel 提交，受影响 hunk 与公告提交逐行相同），
  两者都记入 dossier。根因 `lib/phoenix/socket/transport.ex:624-629`：
  `compare_host?/2` 的 wildcard 分支只做
  `String.ends_with?(request_host, allowed_host)`，缺少点边界，
  `org1.prefix-ex.com` 会通过 `*.ex.com`；修复要求精确匹配或
  `"." <> allowed_host` 后缀。快照 `snap_ee79f4175242bbee`，429 个跟踪文件，
  Elixir 第一方 194 个文件 / 53.08%。公告提交与 release 的差异记入
  findings 第 15 条。
  round1 reviewer 指出 dossier 把入口点误写成 `check_origin/2:605`（该函数不存在），
  九项中 `location=false`；dossier 改为 `check_origin/5:342` → `origin_allowed?/4:356`
  → `origin_allowed?/2:608/616` → `compare_host?/2:627` 后，由**新的** round2
  reviewer 从零复核，九项全 true、grade B。round1 verdict 移到
  `runs/independent/superseded/` 保留审计，未改任何字段。
- **pallets/werkzeug — CVE-2024-34069（Python）**。
  脆弱发行版 3.0.2（lightweight tag `d70dcea3...`），修复发行版 3.0.3
  （annotated tag `dea2a1d1...` peel 到 `f9995e96...`）。公告引用的
  `3386395b...` 是 merge（"Merge pull request from GHSA-2g68-c3qc-8985"），
  实际改动在 `71b69dfb...`（引入 `trusted_hosts` 与 `check_host_trust`）和
  `890b6b62...`（把 Host 校验应用到 evalex 端点）；三者都在 3.0.3 祖先链上、
  都不在 3.0.2 中，且 `3386395` 与 3.0.3 release 提交之间只隔 1 个提交。
  根因 `src/werkzeug/debug/__init__.py:500-534`：`DebuggedApplication.__call__`
  只凭 `s` 参数等于 `self.secret` 与 PIN cookie 就把 `cmd` 交给
  `execute_command`（367-380），后者在第 380 行 `frame.eval(command)` 执行任意
  Python；请求 Host/Origin 完全不校验，`pin_auth`、`log_pin_request` 与
  `/console` 的 `display_console` 同样无校验。修复后 `execute_command`、
  `display_console`、`pin_auth`、`log_pin_request` 在 `check_host_trust` 失败时
  返回 `SecurityError`，默认 trusted hosts 为 `['.localhost','127.0.0.1']`。
  快照 `snap_b57262de7996e8a2`，311 个跟踪文件，Python 第一方 61 个文件 / 49.65%。
  NVD 无独立分析（CVSS/CWE 均抄自 GitHub secondary），修复提交无回归测试，
  CWE-352 与 DNS-rebinding 机制的对应偏松，均记入 findings 第 16 条。
  独立 reviewer 选定的根因位置是 dispatch 处 `__call__` 500-534（并注明
  sink `execute_command` 367-380 同样可辩护）；dossier 据此把
  `critical_operation` 从 sink 改标为 dispatch 处，未改动任何事实字段，九项全 true、grade B。
- **rustls/rustls — CVE-2024-32650（Rust）**。
  脆弱发行版 0.23.4（lightweight tag `v/0.23.4` = `1dee8b13...`），修复 0.23.5
  （`v/0.23.5` = `14cb5d2e...`）。同一漏洞在 0.21/0.22/0.23 三个 release line 上各有
  修复提交；本档案只核验 0.23 线：`6e938bc`（loop bail-out）、`2123576`（回归测试）、
  `f45664f`（close_notify 处理），三者都是 0.23.5 的祖先且不在 0.23.4 中；`5374108`
  是 0.22.4 的祖先、`ebcb478` 未能绑定到已拉取的 tag，均不声明。
  根因 `rustls/src/conn.rs:553-609`：`ConnectionCommon::complete_io` 的循环没有
  “无法推进”出口。ClientHello 后紧跟 close_notify 时，`process_new_packets()` 把
  `has_received_close_notify` 置真，`wants_read()`/`wants_write()` 都为 false、
  `eof` 仍为 false、`is_handshaking()` 仍为 true，底部 `match` 没有
  `(false, true, true)` 分支，`(..) => {}` 原地重来，线程 100% CPU 空转。0.23.5 在
  循环顶部加 `if !self.wants_write() && !self.wants_read() { return Ok(...) }`。
  快照 `snap_b3a6891886ef2160`，890 个跟踪文件，Rust 第一方 117 个文件 / 16.08%。
  公告自带的 PoC 未执行，上游回归测试也未运行；NVD 同样只有 GitHub secondary 指标，
  记入 findings 第 17 条。
- **nodejs/undici — CVE-2023-23936（JavaScript）**。
  脆弱发行版 5.19.0（`v5.19.0` = `f5c89e5c...`），修复 5.19.1
  （`v5.19.1` = `984d53ba...`）。公告修复提交 `a2eff054...`
  （"Merge pull request from GHSA-5r9g-qh6m-jxff"）是单父提交，父提交恰为
  v5.19.0 提交，且是 v5.19.1 的祖先——加深浅克隆后确认。
  根因 `lib/core/request.js:295-309` 的 `processHeader`：Host 头在
  `request.host === null` 时被单独取出存入 `request.host` 并 `return`，绕过
  `processHeaderValue` 的 `headerCharRegex` 校验；随后 `lib/client.js` 的
  `write()`（1397-1398 行）把 `request.host` 直接拼成 `host: ${host}\r\n`。
  CRLF 进入 Host 头即触发 CWE-93 头注入。修复对 Host 走与普通头相同的
  校验路径。快照 `snap_24c4a191fd049fc3`，591 个跟踪文件，JS 第一方 74 个 /
  15.70%。三个 CVSS 版本不一致（NVD primary 5.4 `UI:R` vs Github/CNA 6.5
  `UI:N`、OSV 第三方向量 `PR:L/UI:R`），CWE 同时挂 CWE-93 与 CWE-74，
  发布修复无回归测试，均记入 findings 第 18 条。
- **DaveGamble/cJSON — CVE-2023-50471（C）**。
  脆弱发行版 1.7.16（lightweight tag `v1.7.16` = `cb8693b0...`），修复 1.7.17
  （`v1.7.17` = `87d8f096...`）。修复由两个提交组成：`60ff122`（PR #809，
  直接以 v1.7.16 提交为父）加 `newitem == NULL` 检查与回归测试，但损坏检查
  写成 `newitem->prev == NULL`（此时尚未赋值）；`f66cbab`（PR #810）改为
  `after_inserted->prev == NULL`。两者都不在 1.7.16 中、都是 1.7.17 的祖先。
  根因 `cJSON.c:2263-2290` 的 `cJSON_InsertItemInArray`：2278 行 `newitem->next`
  在 `newitem == NULL` 且数组非空时解引用空指针；2287 行 `newitem->prev->next`
  在数组元素 prev 被破坏为 NULL 时解引用空指针。公开解析路径不会构造这两种
  状态，可达性依赖宿主 API 误用或外部破坏数组；维护者在 issue #802 中称无法
  按原报告复现，且报告者的机理描述不准确（2279 行会覆盖 `newitem->prev`）。
  快照 `snap_d9525608880dc9e1`，228 个跟踪文件，C 第一方 8 个文件 / 13.60%。
  NVD 是唯一评分来源（7.5 HIGH、CWE-476、CPE 仅 1.7.16），MITRE CNA 无
  CVSS/CWE；Debian 记录 introduced 0、fixed 1.7.17-1，并为 Debian 12 回移。
  均记入 findings 第 19 条。
- **libarchive/libarchive — CVE-2025-5915（C）**。
  脆弱发行版 3.7.7（annotated tag `v3.7.7`，tag 对象 `7ce42547...` peel 到
  `b439d586...`），修复 3.8.0（tag 对象 `2ed9bd7b...` peel 到 `70ff28fc...`）。
  源码修复提交 `a612bf62`（"rar: Fix heap-buffer-overflow (#2599)"，单亲）
  是 v3.8.0 的祖先、不在 v3.7.7 中；OSV 所指的 fixed commit `70ff28fc`
  其实是 v3.8.0 的 release 提交，`a612bf62` 是它的祖先。
  根因 `libarchive/archive_read_support_format_rar.c:3099-3119` 的
  `copy_from_lzss_window`：`parse_filter`（3264-3267）接受攻击者可控的
  `blocklength` 却不与 `dictionary_size` 比较，`run_filters`（3435）把它
  传给拷贝函数；3114 行第二个 `memcpy` 在 `length > 2*lzss_size-windowoffs`
  时从 `window[0]` 读出超过窗口分配范围的字节（堆越界读）。3.8.0 在
  `parse_filter` 加 `blocklength > rar->dictionary_size` 拒绝，并修正该
  `memcpy` 的目的地址为 `buffer + firstpart`（写侧问题，单独记录）。
  快照 `snap_a47bcab3f2c97e92`，1,240 个跟踪文件，C 第一方 219 个文件 /
  25.63%。NVD 两个 CVSS 条目都是 Secondary（无 Primary）；CNA 指派
  CWE-122，但 ASan 报告是 READ、CVSS `I:N`，技术上更接近 CWE-125，
  按要求保留权威指派并记录分歧。3.7.x 维护线与 3.8.0 分叉，OSV 的线性
  GIT 范围不覆盖 3.7.6-3.7.9；版本范围 `<3.8.0` 覆盖。均记入 findings 第 20 条。
- **laravel/framework — CVE-2024-52301（PHP）**。
  脆弱发行版 11.30.0（tag `v11.30.0` → `dff71644...`，2024-10-30），
  11.x 修复 `18b326d`（"only use argv on console"，单亲 `cdf07b66...`）经
  `6d53774` 合并入 11.x，是 v11.31.0 的祖先、不在 v11.30.0 中。六个分支各有修复：
  6.x `841d842`（即 v6.20.45 tag 提交）、7.x `639b222`、8.x `eded6bd`、9.x `695097c`、
  10.x `8c07b63`、11.x `18b326d`；逐分支用 fixed tag 与紧邻前一版本做了双向祖先检查，
  前五个分支的上一版本（6.20.44/7.30.6/8.83.27/9.52.16/10.48.22）都仍是无条件读 argv。
  根因 `src/Illuminate/Foundation/Application.php:760-765` 的 `detectEnvironment`：
  762 行直接把 `$_SERVER['argv']` 交给 `EnvironmentDetector`；后者 18-19 行把任何
  非空 argv 当控制台输入，61-71 行解析 `--env`/`--env=`。当 `register_argc_argv=On`
  且 web SAPI 把 query string 暴露为 argv 时，未认证请求可用 `?--env=<name>` 覆盖
  `app.env`。快照 `snap_6e1f42aa46ca4df5`，2,717 个跟踪文件，PHP 第一方 1,316 个文件 /
  42.36%。GHSA/OSV 的 CVSS_V3 向量三项影响全 N（0.0），与同记录 HIGH、NVD Primary
  7.5、CNA CVSS 4.0 8.7 矛盾；正式 severity 取 NVD 7.5，矛盾记入 findings 第 21 条。
  修复提交未附带回归测试；Debian 11 回移到 `6.20.14+dfsg-2+deb11u2`，版本号低于上游
  6.20.45，单独记录。
- **curl/curl — CVE-2023-38545（C）**。
  脆弱发行版 8.3.0（tag `curl-8_3_0` → `6fa1d817...`，2023-09-13），修复
  `fb4415d8`（"socks: return error if hostname too long for remote resolve"，单亲
  `09e25b9d...`）是 `curl-8_4_0`（`d755a5f7...`）的祖先、不在 8.3.0 中；引入提交
  `4a4b63da`（"socks: make the connect phase non-blocking"，2020-02-14）是
  `curl-7_69_0` 的祖先。根因 `lib/socks.c:904-908` 的 `do_SOCKS5`：
  `socks5_resolve_local` 是函数局部变量，573-574 行每次状态机重入都重新初始化；
  589-592 行在 hostname > 255 时把它置 TRUE，但初始握手 `socks_state_send/recv`
  遇 `CURLE_AGAIN` 时 624/650 行直接返回，下次重入该变量被重置为 FALSE，
  883 行的远程解析分支于是在 906 行写入被截断的一字节长度、907 行把完整
  `hostname_len` 拷入 `socksreq`（即 `data->state.buffer`，569 行，默认 16 KiB），
  造成堆越界写。8.4.0 改为 `failf` + `CURLPX_LONG_HOSTNAME`，并附带
  `tests/data/test728`（256 字符主机名、期望 `CURLE_PROXY` 97；只读未执行）。
  快照 `snap_0ec1c11542393304`，3,798 个跟踪文件，C 第一方 438 个文件 / 32.20%。
  NVD Primary 为 9.8 CRITICAL（UI:N），curl 公告、CISA-ADP 与 OSV 为 8.8 HIGH
  （UI:R）；CWE 分别为 CWE-122 与 CWE-787。MITRE CNA 的 affected 块用
  `lessThan` 描述出空区间，NVD 复制了该块但 CPE 配置正确；OSV 的 GIT 端点取的是
  7.69.0 release 提交与 8.4.0 之后的 tiny-curl 补丁提交，还把 8.4.0 列入
  affected。正式 severity 取 NVD 9.8，其余矛盾记入 findings 第 22 条。
- **django/django — CVE-2020-7471（Python）**。
  脆弱发行版 3.0.2（tag `3.0.2` → `a3697439...`，2020-02-03），3.0.x 修复
  `505826b4`（"[3.0.x] Fixed CVE-2020-7471 -- Properly escaped
  StringAgg(delimiter) parameter."，单亲 `673444da...`）是 3.0.3（`c459a466...`）
  的祖先、不在 3.0.2 中；另有 master `eb31d84`、2.2.x `c67a368`、1.11.x `001b063`
  三个分支提交，分别只对各自修复 tag 成立，master 提交不属于任何已发布修复 tag。
  根因 `django/contrib/postgres/aggregates/general.py:52-58` 的 `StringAgg`：
  54 行模板把 `'%(delimiter)s'` 直接写进 SQL 文本，57-58 行把 delimiter 作为
  原始 kwarg 传入；`Func.__init__` 存入 `self.extra`（expressions.py:592），
  `Func.as_sql` 在 627 行并入格式字典、638 行 `template % data` 原始插值，
  而 `params` 只收集源表达式，delimiter 从不参数化。3.0.3/2.2.10/1.11.28 改为
  `Value(str(delimiter))`，delimiter 走绑定参数；修复提交附带
  `test_string_agg_delimiter_escaping`（单引号 delimiter，只读未执行）。
  快照 `snap_ab695ba3db678939`，6,163 个跟踪文件，Python 第一方 815 个文件 /
  15.24%。NVD Primary 9.8、GHSA/OSV 同一 CVSS 3.1 向量，CWE-89；
  MITRE CNA 记录为 n/a 占位。NVD 下界低估暴露面（1.9/1.10.8、2.0/2.1.15 同含
  漏洞模板），OSV 又把 1.0.1–1.8.x 列入 affected（StringAgg 1.9 才引入），
  两处源缺陷均记入 findings 第 23 条。
- **jenkinsci/jenkins — CVE-2024-23897（Java）**。
  脆弱发行版 2.441（tag `jenkins-2.441` → `3b0de10d...`），周更线修复 `554f0378`
  （`[SECURITY-3314]`）是 2.442（`10b1b883...`）的祖先，LTS 线 `a7486539` 是
  2.426.3（`9ed5f66f...`）的祖先、`3e876d4c` 是 2.440.1（`02f2a4cc...`）的祖先，
  三个提交都不在 2.441 中。根因 `core/src/main/java/hudson/cli/CLICommand.java:309-311`
  的 `getCmdLineParser` 直接 `new CmdLineParser(this)`，第二处
  `CLIRegisterer.bindMethod:134` 同样 `new CmdLineParser(null)`；args4j 2.33 默认
  `atSyntax=true`，`@` 参数按文件展开，未授权 CLI 命令（如 `help 1`、`who-am-i`）可读
  master 本地文件前几行，持 Overall/Read 时可读完整文件。修复改为
  `ParserProperties.defaults().withAtSyntax(ALLOW_AT_SYNTAX)`（默认 false），并附带
  `Security3314Test`（单测源码只读未执行）。入口 `CLICommand.main:227` → 233 →
  `CLIRegisterer.bindMethod:134` → 310。快照 `snap_d9b0ffa82cd068d0`，12,049 个
  跟踪文件，Java 第一方 1,144 个文件 / 24.89%。NVD Primary 9.8，CWE-22/CWE-27；
  MITRE 与 NVD 描述称未授权可读任意文件，公告只给前几行；OSV 版本表含 rc/伪版本且
  漏 2.440.1，公告在 2.440.1 发布后修订；周更/LTS 版本号交错使扁平 Maven 范围只能
  过度近似。以上源缺陷记入 findings 第 24 条。
- **symfony/symfony — CVE-2024-50345（PHP）**。
  脆弱发行版 5.4.45（annotated tag `v5.4.45` → `2b66d7d7...`），修复
  `5a9b08e5`（`[HttpFoundation] Reject URIs that contain invalid characters`，
  父 `e39f6a96`，作者 2024-10-22）经 5.4 安全合并 `ad0a241e` 进入分支，再
  merge-up 到 6.4/7.1；它不在 5.4.45、6.4.13、7.1.6 中，是 5.4.46
  （`057d88be...`）、6.4.14（`d1797e5b...`）、7.1.7（`50011435...`）的祖先。
  根因 `src/Symfony/Component/HttpFoundation/Request.php:358-361` 的
  `Request::create`：直接 `parse_url($uri)`，不按 WHATWG URL 规则拒绝非法字符。
  反斜杠、CR/LF/TAB、NUL 或首尾控制字符会让 PHP 解析出的 host/path 边界与浏览器
  规范化结果不同，依赖 `Request` 的跳转校验器因此可能放行到另一个域，构成
  CWE-601。修复在 parse_url 之后加四道守卫，非法输入抛 `BadRequestException`；
  回归测试 `testCreateWithBadRequestUri` 覆盖这些字符类（只读未执行）。快照
  `snap_39105a8a3ceb9fe4`，11,040 个跟踪文件，PHP 第一方 3,327 个文件 / 25.45%。
  NVD Primary 6.1 MEDIUM（AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N），CNA/GHSA 为
  3.1 LOW（AC:H、S:U、I:N）；OSV 范围事件正确但 `versions` 漏掉 v5.4.41、
  v6.4.1、v7.1.2 等区间内 tag，且 GHSA/OSV 多出 CVSS v4.0 2.3。源缺陷记入
  findings 第 25 条。
- **symfony/symfony — CVE-2024-50340（PHP，与上一条共用 v5.4.45 快照）**。
  同一脆弱发行版 5.4.45（`2b66d7d7...`），修复 `a77b308c`（"Do not read from argv
  on non-CLI SAPIs"，父 `5ebc4c3c`，作者 2024-10-15）由安全合并 `30810edc`
  进入 5.4，再 merge-up 到 6.4/7.1；不在 5.4.45/6.4.13/7.1.6 中，是
  5.4.46/6.4.14/7.1.7 的祖先。根因
  `src/Symfony/Component/Runtime/SymfonyRuntime.php:98-101`：构造器把
  `isset($_SERVER['argv'])` 当作 CLI 信号，直接 `getInput()`；`getInput` 用
  `new ArgvInput()` 读取 argv，并把 `--env/-e`、`--no-debug` 写进
  `putenv/$_SERVER/$_ENV`，没有 SAPI、`$_GET` 或 `register_argc_argv` 判断。
  Web SAPI 且 `register_argc_argv=On` 时，查询串会被 PHP 拆进 argv，构造 URL 即可
  改 `APP_ENV` 或 `APP_DEBUG`（CWE-74）。修复要求 `empty($_GET)` 才走 argv 分支，
  并在 `getInput` 中对 `$_GET` 非空且 `register_argc_argv=On` 抛异常；新增
  `kernel_register_argc_argv.phpt`（只读未执行）。CNA/GHSA 7.3 HIGH
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L`），GHSA 另显 CVSS v4.0 6.9 MODERATE；
  NVD 只有 Secondary 度量且 `vulnStatus=Deferred`。真实 GHSA 为
  `GHSA-x8vp-gf4q-mw5j`（首版误用相邻候选的 `GHSA-qq5c-677p-737q`，该别名属于
  CVE-2024-51736，由 reviewer 纠正）；CWE 仅 CWE-74（GHSA/OSV 另加 CWE-20）；
  5.4 范围下界取 `>=5.3`（Runtime 5.3 引入），OSV 的 fixed 端点是发行提交。
  均记入 findings 第 26 条。
- **symfony/symfony — CVE-2024-50342（PHP，与上两条共用 v5.4.45 快照）**。
  脆弱发行版仍是 5.4.45（`2b66d7d7...`）。修复分两段：第一段
  `296d4b34`（"Filter private IPs before connecting when Host == IP"，父
  `706d8628`）由安全合并 `3fc5471c` 进入 5.4，只对 URL host 是字面 IP 时有效，
  随 5.4.46/6.4.14/7.1.7 发布；第二段 `b4bf5afd`（"Resolve hostnames in
  NoPrivateNetworkHttpClient"，父 `2c7c4bac`）由安全合并 `b8f41169` 进入 5.4，
  增加 `$resolve` 闭包或 `dns_get_record(DNS_A/DNS_AAAA)` 解析主机并在连接前
  检查解析出的 IP，随 5.4.47/6.4.15/7.1.8 发布。根因
  `src/Symfony/Component/HttpClient/NoPrivateNetworkHttpClient.php:82-89`：
  唯一子网检查在 `on_progress` 回调内，只读 `$info['primary_ip']`，从不解析
  URL 主机名；`IpUtils::checkIp` 只接受 IP 字面量，故解析到私有网段的域名不会被
  `PRIVATE_SUBNETS` 拦截，请求被交给内部 client 去解析/连接（公告：内部 IP/端口
  枚举，CWE-200）。Symfony 公告已于 2024-11-13 修订，明确 5.4.46/6.4.14/7.1.7
  仍受影响；CNA、NVD 描述与 OSV 的 CVE 记录仍停在旧区间，CNA/NVD 的 references
  也只列第一段补丁。NVD Primary 4.3 MEDIUM（`AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`），
  CNA/GHSA 为 3.1 LOW（AC:H）；GHSA 网页 Weaknesses 显示 No CWEs，但 CNA/NVD/OSV
  数据层为 CWE-200。独立 reviewer 独立确认两段补丁缺一不可、真实 fixed releases
  为 5.4.47/6.4.15/7.1.8，九项 `fields_verified=true`，grade B；语言统计可近似
  复现（3327 个 first-party PHP 文件，字节差 0.02%）。均记入 findings 第 27 条。
- **django/django — CVE-2020-9402（Python，与 CVE-2020-7471 共用 3.0.2 快照）**。
  脆弱发行版 3.0.2（`a3697439`）。根因在
  `django/contrib/gis/db/models/functions.py:113-119` 的
  `OracleToleranceMixin.as_oracle`：`tol = self.extra.get('tolerance', ...)` 后
  用 `"%%(function)s(%%(expressions)s, %s)" % tol` 直接格式化 SQL 模板；次路径
  `aggregates.py:29-32` 把 `%(tolerance)s` 放进 SDOAGGRTYPE 模板。`Func.as_sql`
  （`django/db/models/expressions.py:638`）执行 `template % data`，params 只来自
  source expressions，故 tolerance 成为 SQL 文本而非绑定参数（公告称 Oracle 上
  GIS 函数/聚合 tolerance 的 SQL 注入，CWE-89）。修复四条：master `6695d29b`、
  3.0 `26a5cf83`、2.2 `fe886a3b`、1.11 `02d97f3c`；3.0 补丁父 `c5cfaad2` 的两个
  文件 blob 与 3.0.2/3.0.3 完全一致，`26a5cf83` 只在 3.0.4 中。2.2.11/3.0.4 用
  `Value(...)` 绑定参数，1.11.29 改用 `_handle_param(..., NUMERIC_TYPES)` 拒绝
  非数值。NVD Primary 8.8 HIGH（`AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`），
  NVD v2.0 另有 6.5 MEDIUM，GHSA 另有 CVSS 4.0 8.7；CWE-89 来自 NVD/GHSA，
  MITRE CNA 为占位且 problemTypes n/a。OSV/NVD 只引用 master 补丁，公告列四条
  backport；OSV 另有重复 PYSEC-2020-345。独立 reviewer 独立选中同一
  `functions.py:113-119`（次路径 29-32），确认四条补丁祖先关系与三个 fixed
  releases，九项 `fields_verified=true`，grade B；语言字段经快照盘点复核后为 true。
  均记入 findings 第 28 条。
- **django/django — CVE-2020-13596（Python，与 7471/9402 共用 3.0.2 快照）**。
  脆弱发行版 3.0.2（`a3697439`）。根因在
  `django/contrib/admin/widgets.py:151-154` 的
  `ForeignKeyRawIdWidget.get_context`：`url_parameters()` 的值经
  `url_params_from_lookup_dict` 仅做 `str(v)`，第 153 行用
  `'&amp;'.join('%s=%s' % (k, v))` 手工拼接，第 154 行对整串调用 `mark_safe`，
  模板 `foreign_key_raw_id.html` 的 `href="{{ related_url }}"` 因 SafeString
  不再转义，引号可闭合属性导致 XSS；次路径 `ManyToManyRawIdWidget` 继承同一
  `get_context`。修复四条：master `2dd4d110`、3.1 `49d7cc19`、3.0 `1f2dd37f`、
  2.2 `6d61860b`；3.0 补丁父 `256d2971` 的 widgets.py blob `7db57f40` 与
  3.0.2/3.0.6 完全一致，`1f2dd37f` 只在 3.0.7 中。修复改用
  `django.utils.http.urlencode(params)` 并移除 `mark_safe`。NVD Primary 6.1
  MEDIUM（`AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`），CWE-79 来自 NVD/GHSA；
  CNA 为占位。异常：2.2 修复提交主题误写 `[2.0.x]`（ancestry 确属 2.2.13）；
  NVD 西班牙语描述误抄 CVE-2020-13254；GHSA CVSS 4.0 向量按规范为 0.0、
  不可用；3.1a1 含漏洞但三个来源均未列。独立 reviewer 独立选中
  `widgets.py:151-154`（次路径 200-215），九项 `fields_verified=true`，
  grade B；复核期间另以全历史搜索定位到构造引入提交 `a19ed8aea39`
  （newforms-admin 合并），但为保持已推广 verdict 不变，该补充只记入
  findings 第 29 条。
- **django/django — CVE-2020-13254（Python，与 7471/9402/13596 共用 3.0.2 快照）**。
  脆弱发行版 3.0.2（`a3697439`）。根因在
  `django/core/cache/backends/memcached.py` 的 `BaseMemcachedCache.get`（69-71）
  与 `BaseMemcachedCache.set`（73-77）：两者都在 `make_key()` 后把 key 直接交给
  client，从不调用 `validate_key()`；`BaseCache.validate_key` 只发
  `CacheKeyWarning`，memcached 后端也未调用它。memcached ASCII 协议以空白/控制字符
  分隔 key，畸形 key 可与另一逻辑 key 落到同一服务端 key：set 覆盖他人条目、get
  读回他人值，造成数据泄露。修复四条：master `2c824149`、3.1 `580bd64c`、
  3.0 `84b2da55`、2.2 `07e59caa`；`84b2da55` 是 3.0.7 发布提交的父、
  `07e59caa` 是 2.2.13 发布提交的父，均经 `merge-base --is-ancestor` 验证；
  `580bd64c` 首见 3.1b1、`2c824149` 首见 3.2a1（预发布，不计入 fixed_releases）。
  修复新增 `InvalidCacheKey` 与 `BaseMemcachedCache.validate_key`，并在
  add/get/set/delete/get_many/incr/decr/set_many 的 `make_key()` 后调用。
  NVD Primary 5.9 MEDIUM（`AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`），CWE-295 来自
  NVD/GHSA（语义错配，原值保留未替换）；MITRE CNA 为占位。异常：OSV GIT ranges
  的 introduced/fixed 指向文档提交与版本 bump 提交，不可用；GHSA 顶层 `high` 与
  自身 CVSS 3.1 5.9 / NVD 5.9 MEDIUM 矛盾（`high` 来自 2024 年追加的 CVSS 4.0 8.2）；
  3.0.7 中 `MemcachedCache.get`/`touch` 覆写仍未调用 `validate_key()`（静态观察，
  未据此重开 CVE）。独立 reviewer 独立选中 `BaseMemcachedCache.get` 69-71，与
  采集档案的 `set` 73-77 不重叠；两者同为缺失校验的调用点，档案据此把位置范围
  协调为连续 69-77 并在 `location_revision` 记录原因，未改动任何证据、严重度、
  版本范围、提交或 reviewer 值。九项 `fields_verified=true`，grade B；
  记入 findings 第 30 条。
- **django/django — CVE-2020-24583（Python，与 7471/9402/13596/13254 共用 3.0.2 快照）**。
  脆弱发行版 3.0.2（`a3697439`）。根因在
  `django/core/files/storage.py:240-246` 的 `FileSystemStorage._save`：
  配置 `FILE_UPLOAD_DIRECTORY_PERMISSIONS` 时先 `old_umask = os.umask(0)`，
  再 `os.makedirs(directory, mode, exist_ok=True)`。Python 3.7+ 的
  `os.makedirs` 只把 `mode` 用于末级目录，中间目录按 `0o777 & ~umask`
  创建，umask 为 0 时中间目录成为 `0o777`。`StaticFilesStorage` 继承
  `FileSystemStorage`，collectstatic 的 copy 路径共用该 `_save`，因此上传与
  收集静态文件的中间目录都受影响。修复四条：master `8d727157`、3.1
  `934430d2`、3.0 `08892bff`、2.2 `375657a7`；分别首见 3.2a1、是 3.1.1 /
  3.0.10 / 2.2.16 的祖先。修复改为
  `os.umask(0o777 & ~self.directory_permissions_mode)`。NVD Primary 7.5 HIGH
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`），CWE-276 由 NVD/GHSA 给出
  （MITRE CNA 占位）。异常：三个 backport 消息引用的 master 提交
  `ea0febbba` 在公开仓库不可达，公告列出的可达 master 提交是 `8d727157`；
  NVD v2 5.0、GHSA v4 8.7 与 v3.1 7.5 并存；Python 3.7+ 运行时前提无法
  编码进版本区间。独立 reviewer 独立选中 `storage.py:239-246`（与档案
  240-246 重叠），十项 `fields_verified=true`，grade B；另观察到
  `collectstatic --link` 走独立的 `os.makedirs` 不受本次修复覆盖，
  仅作静态观察。记入 findings 第 31 条。
- **django/django — CVE-2020-24584（Python，同一 3.0.2 快照）**。
  根因在 `django/core/cache/backends/filebased.py:115-116` 的
  `FileBasedCache._createdir`：`os.makedirs(self._dir, 0o700, exist_ok=True)`
  没有控制 umask，Python 3.7+ 下中间目录按系统 umask（通常 `0o755`）创建，
  比预期的 `0o700` 缓存目录更宽松，本地攻击者可穿越中间目录读取缓存文件。
  修复四条：master `1853724a`、3.1 `2b099caa`、3.0 `cdb367c9`、2.2
  `a3aebfdc`；分别首见 3.2a1、是 3.1.1 / 3.0.10 / 2.2.16 的祖先，且四个
  24584 补丁依次以对应分支的 24583 补丁为父。修复在 `os.makedirs` 外包
  `os.umask(0o077)` / `finally` 还原。NVD Primary 7.5 HIGH，CWE-276；
  OSV CVSS 4.0（`VC:N/VI:L`）与 v3.1（`C:H/I:N`）处理不同。backport 消息
  引用的 master 原提交 `f56b5797` 同样不可达，公告列出的 `1853724a` 可达。
  独立 reviewer 独立选中 `filebased.py:115-116`，十项
  `fields_verified=true`，grade B。记入 findings 第 32 条。
- **django/django — CVE-2021-3281（Python，同一 3.0.2 快照）**。
  根因在 `django/utils/archive.py:154-158` 的 `TarArchive.extract`：成员名经
  `split_leading_dir` 去掉前导目录后直接 `os.path.join(to_path, name)`，既不做
  目标路径归一化也不做边界检查，tar 成员名可携带 `../` 或绝对路径。修复五条：
  master `05413afa`、3.2 `f944f79e`、3.1 `02e65928`、3.0 `52e409ed`、
  2.2 `21e7622d`；新增 `BaseArchive.target_filename`（`os.path.abspath` 后
  `startswith` 校验），zip 路径同时跳过空名与以 `/`、`\` 结尾的目录项。
  NVD Primary 5.3 MEDIUM（`AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`），CWE-22。
  异常：OSV GIT 区间边界指向无关的文档/版本 bump 提交；MITRE CNA 记录为占位；
  vendor 标 "low" 与 NVD 5.3 并存。独立 reviewer 独立选中
  `TarArchive.extract` 行 158（与档案 154-158 重叠），十项
  `fields_verified=true`，grade B。另核实该修复本身不完整：`startswith` 缺
  分隔符边界，2025-10-01 以 CVE-2025-59682（`924a0c09`）改用
  `os.path.commonpath` 重修，影响 4.2.25/5.1.13/5.2.7 之前的后续版本，不影响
  3.0.2 的判定。记入 findings 第 33 条。
- **django/django — CVE-2021-28658（Python，同一 3.0.2 快照）**。
  根因在 `django/http/multipartparser.py:300-302` 的
  `MultiPartParser.IE_sanitize`：只用 `rfind("\\")` 截断 IE 全路径，不处理
  POSIX `/`，3.0.2 也没有 `os.path.basename`，客户端 multipart `filename`
  可携带 `/`、`../` 穿越。调用链：`parse` 209-212 把 `html.unescape` 后的
  filename 传入 `IE_sanitize`，230 行交给 `handler.new_file`。修复五条：
  master `d4d800ca`、3.2 `2820fd1b`、3.1 `cca0d981`、3.0 `e7fba622`、
  2.2 `4036d62b`；ancestry 逐一验证 3.0.14←`e7fba622`、2.2.20←`4036d62b`、
  3.1.8←`cca0d981`，3.0.13/2.2.19/3.1.7 的 `multipartparser.py` blob 仍是
  脆弱版本。修复改为 `sanitize_file_name`：反转义、按 `\` 截断后追加
  `os.path.basename`。NVD Primary 5.3 MEDIUM
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`），CWE-22。异常：OSV GIT
  introduced 事件为无关的 security-archive/文档提交，fixed 事件等于三个 tag
  的 peel 提交；MITRE CNA 占位；vendor "low"、GHSA 的 CVSS v4 6.9 与 NVD 3.1
  5.3 并存。独立 reviewer 独立选中同一 `multipartparser.py:300-302`，十项
  `fields_verified=true`，grade B。记入 findings 第 34 条。
- **libexpat/libexpat — CVE-2022-25236（C，同一 R_2_4_4 快照）**。
  `addBinding` 在扫描 xmlns URI 时只与内建 XML/xmlns 命名空间比较，不检查
  URI 内是否含 `m_namespaceSeparator`（2.4.4 的 3752-3760）；随后为分隔符
  预留一字节并在 3825-3828 把 URI 连同分隔符写入 binding，下游按分隔符
  切分展开名的处理器会看到额外组件。修复 `a2fe525e` 逐字节拒绝 URI 中
  任意位置的分隔符，配套测试 `2de07742`、`Changes` `e4d7e497`、PR #561
  合并 `2cc97e87`，均在 R_2_4_5 内、不在 R_2_4_4 内。NVD Primary 9.8
  CRITICAL（`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`），CWE-668；MITRE CNA
  占位，OSV fixed 事件指向发布合并 `97a48405`。独立 reviewer 独立选中
  3752-3759 与写点 3825-3828，十项 `fields_verified=true`，grade B。
  记入 findings 第 35 条。
- **libexpat/libexpat — CVE-2022-25314（C，同一 R_2_4_4 快照）**。
  `copyString` 用 `int charsRequired` 逐字符计数后乘以
  `sizeof(XML_Char)` 同时用于 `malloc_fcn` 与 `memcpy`（2.4.4 的
  7415-7426）；调用方传入 GB 级编码名时计数回绕，分配与拷贝使用回绕值。
  修复 `efcb3474` 仅把声明改为 `size_t`（1 行增 1 行删，无测试），是
  R_2_4_5 的祖先、不在 R_2_4_4 中。NVD Primary 7.5 HIGH
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`），CWE-190；上游明确该输入是
  库使用者提供的编码名、通常硬编码，预期影响 DoS。独立 reviewer 确认
  7415-7426 与两个调用点 1090/1241，并指出 OSV fixed 事件是发布合并而非
  代码修复，十项 `fields_verified=true`，grade B。记入 findings 第 36 条。
- **libexpat/libexpat — CVE-2022-25315（C，同一 R_2_4_4 快照）**。
  `storeRawNames` 用 `int bufSize`/`int nameLen` 计算扩容尺寸，
  `ROUND_UP` 后的 raw name 长度使加法回绕，绕过 2578 行的扩容判断，
  2597 行 `memcpy` 按未回绕长度写入，造成堆越界写（正式表锚定
  2572-2579）。修复 `eb036280` 在计算前加入
  `rawNameLen > (size_t)INT_MAX - nameLen` 检查，是 R_2_4_5 的祖先、
  不在 R_2_4_4 中，未附带测试。NVD Primary 9.8 CRITICAL
  （`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`），CWE-190；GHSA 标 Moderate
  且 affected/patched Unknown，与 NVD 冲突，保留分歧。独立 reviewer
  选中 2560-2602、根因 2577、写点 2597，十项 `fields_verified=true`，
  grade B。记入 findings 第 37 条。
- **libexpat/libexpat — CVE-2022-25313（C，同一 R_2_4_4 快照）**。
  `build_node` 对 DTD 内容模型的每个子节点递归调用自身（2.4.4 的
  7344-7347），`doProlog:5423`→`build_model:7386` 触发，2.4.4 无任何
  深度上限，深嵌套内容模型可耗尽栈；只有注册
  `XML_SetElementDeclHandler` 的应用可达。修复 `9b4ce651` 删除
  `build_node`、把 `build_model` 改为迭代实现，父提交即漏洞提交，经
  PR #558 合并 `bbdfcfef`，在 R_2_4_5 内、不在 R_2_4_4 内。NVD Primary
  6.5 MEDIUM（`AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`），CWE-674（GHSA
  另列 CWE-400）；上游 Changes 称 DoS 或潜在 RCE，比 NVD 更广。2.4.5 的
  迭代重写有正确性回归，由 2.4.6 的 `b12f34fe`（PR #566）修正。独立
  reviewer 选中 7320-7350、递归 7346，十项 `fields_verified=true`，
  grade B。记入 findings 第 38 条。
- **curl/curl — CVE-2023-46218（C，curl 8.3.0）**。
  `Curl_cookie_add` 把未规范化的 `domain` 与 `co->domain` 直接交给
  `psl_is_cookie_domain_acceptable`（8.3.0 的 1047-1048）；libpsl 的公共
  后缀比较区分大小写而 `cookie_tailmatch` 不区分，`Domain=co.UK` 一类
  混合大小写公共后缀可绕过 PSL 成为跨站 supercookie。修复 `2b0994c2` 用
  `Curl_strntolower` 复制进 256 字节缓冲区再比较，不是 8.4.0 的祖先、
  是 8.5.0 的祖先；回归测试 `test1476` 由 `323df4261` 单独加入 8.5.0。
  NVD Primary 6.5 MEDIUM（`AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N`），
  CWE-201（curl CNA）与 CWE-178（NVD 次弱点）。来源缺陷：CVE v5 CNA
  只表达 8.4.0、无 metrics/CWE；OSV GIT 边界是发布提交；GHSA 为
  Unreviewed 且 affected 为空。reviewer 另追查 7.48.0 的 `c140bd78`
  才切换到该 API，7.46.0–7.47.x 用的 `psl_is_public_suffix` 同样未规范化，
  受影响下界自洽。独立 reviewer 选中 1037-1061、关键调用 1048，十项
  `fields_verified=true`，grade B。记入 findings 第 39 条。
- **symfony/symfony — CVE-2024-51996（PHP，同一 v5.4.45 快照）**。
  `PersistentRememberMeHandler::consumeRememberMeCookie`（69-70 行）按 series
  取回持久化 token 并校验 token 值，却不比对 token 属主与 cookie 携带的
  identifier/class；父类第 74 行直接用 cookie 的 identifier 加载用户，
  因此改写 cookie identifier 即可冒充他人。修复 `81354d39` 加入属主校验并
  用持久化 token 重建 details，是 `v5.4.47` 的祖先、不在 `v5.4.45` 中。
  NVD 无 primary 指标（Deferred），7.5 HIGH 来自 GitHub_M CNA 的 Secondary
  指标；CWE-287/289。来源缺陷：CNA/NVD 描述与 CPE 误写成 "Symphony
  process"，CISA-ADP 范围编码畸形。独立 reviewer 选中 69-70，十项
  `fields_verified=true`，grade B。记入 findings 第 41 条。
- **symfony/symfony — CVE-2025-64500（PHP，同一 v5.4.45 快照）**。
  `Request::preparePathInfo` 用 `substr($requestUri, strlen($baseUrl))` 去掉
  baseUrl 后把剩余部分原样返回（1973-1979），不保证以 `/` 开头；例如
  `/api/index.phpfoo` 配 baseUrl `/api/index.php` 得到 `foo`。依赖 `/`
  前缀假设的访问控制规则因此可能被绕过。修复 `9962b91b`（"Fix parsing
  pathinfo with no leading slash"，2025-11-03）在剩余部分不以 `/` 开头时
  返回 `'/'.$pathInfo`，是 `v5.4.50` 的祖先、不在 `v5.4.45` 中。NVD 无
  primary 指标，7.3 HIGH 来自 GitHub_M CNA 的 Secondary 指标；CWE-647。
  来源说明：CNA 的 affected 只列 symfony/symfony，GHSA/OSV 另列
  symfony/http-foundation；OSV 把下界归一化为 introduced 0。独立 reviewer
  选中 1973-1979，十项 `fields_verified=true`，grade B。记入 findings 第 43 条。
- 推广门槛：38 promoted，0 pending。已提升条目全部十项 `fields_verified=true`，
  grade B。正式表更新为 38 漏洞、38 位置、38 复核、925 证据、38 行真值矩阵；
  评测快照 22 个
  （express 4.19.2、flask 2.3.1、werkzeug 3.0.2、rack 2.2.3、gin v1.5.0、guzzle 7.4.4、
  Newtonsoft 12.0.3、netty 4.1.59.Final、hyper v0.14.2、rustls 0.23.4、vite v5.0.11、
  libexpat R_2_4_4、protobuf v3.20.1、phoenix v1.6.13、undici 5.19.0、cJSON v1.7.16、
  libarchive v3.7.7、laravel v11.30.0、curl 8.3.0、django 3.0.2、jenkins 2.441、symfony 5.4.45）。快照总数 73
  （另有未提升的 OpenSSL 3.0.1 一个非评测快照）。候选表 `verified` 行 47（flask、
  netty、hyper、protobuf、werkzeug、rustls、undici 各有一条别名簇重复行，cJSON 有
  CVE 与 DEBIAN-CVE 两条，laravel 有 disc2 与 adv3 两条，django 有 CVE-2020-7471、
  CVE-2020-9402、CVE-2020-13596、CVE-2020-13254、CVE-2020-24583、CVE-2020-24584、
  CVE-2021-3281 与 CVE-2021-28658 八条，curl、jenkins 与 symfony
  的候选行随本轮提升为 verified（symfony 有五条漏洞共用 snap_39105a8a3ceb9fe4，
  curl 的 CVE-2023-46218 与 libexpat 的 CVE-2022-25235/25236/25313/25314/25315
  各一条），
  均指向已提升漏洞，不是 47 条漏洞）；
  `pending_location` 751、`pending_version` 850、`in_validation` 975，未解决候选 2576
  （`rejected` 3 行：CVE-2024-51999 已 withdrawn；CVE-2024-50343 见 findings 第 40 条；
  CVE-2024-50341 见 findings 第 42 条）。
- `validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，
  1 条为 grade A 比例）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；
  本轮累计新增 34 条已验证漏洞（四语言批次 + hyper/vite + libexpat ×6 + protobuf +
  werkzeug + rustls + undici + cJSON + libarchive + laravel + curl ×2 + django ×8 + jenkins +
  symfony ×5），
  停止规则不满足。

### 续轮：symfony 2026 公告批次 + netty 4.1.59（2026-10-22）

本轮在既有 `snap_39105a8a3ceb9fe4`（symfony v5.4.45，`2b66d7d7`）上继续推进，新提升
14 条：13 条 symfony 2026 公告与 1 条 netty 请求走私。symfony 批次全部由同一快照
静态核验，修复点分别落在 v5.4.52 / v5.4.53；netty 条目落在既有评测快照
`snap_bb344e672a0544ef`（4.1.59.Final，`97d04481`）。全部 grade B（无复现引用，
grade A 自动封顶），52/52 已提升条目均通过十项 `fields_verified=true` 的非独立复核。

- **symfony/symfony — CVE-2026-45063（PHP）**。`X509Authenticator::extractUsername`
  第 49 行的 `emailAddress` 正则未锚定到 DN 起始或逗号/斜杠边界，攻击者控制的证书
  Subject DN 可让中间备选子串命中，从而冒充其他身份。修复 `59ef4840` 锚定 RDN
  边界，随 v5.4.52 发布。
- **symfony/symfony — CVE-2026-45065（PHP）**。`UrlGenerator::doGenerate` 第 192 行
  对含原样交替分支的 requirement 锚定方式错误，中间分支可只匹配子串，生成
  协议相对（`//host`）的站外 URL。修复 `bcf487c2`，随 v5.4.52 发布。
- **symfony/symfony — CVE-2026-45067（PHP）**。`Mime\Address::__construct` 第 55 行
  接受 quoted-string local part 中的 CRLF，导致邮件头/SMTP 命令注入。修复
  `a1c42cbe`，随 v5.4.52 发布；档案记录 CNA 6.3 Medium 与 GHSA HIGH 标签不一致。
- **symfony/symfony — CVE-2026-45068（PHP）**。`SendmailTransport::doSend` 第 111 行
  把收件人直接拼进 sendmail 命令行，未插入选项终止符，前导 `-` 地址可做参数注入。
  修复 `c4514486`，随 v5.4.52 发布；GitHub 公告页与 OSV 的 CVSS 4.0 向量与 CNA 不同。
- **symfony/symfony — CVE-2026-45071（PHP）**。`DomCrawler::addXmlContent` 第 243 行
  启用 `validateOnParse`，在 `LIBXML_NONET` 下仍重新打开外部实体，造成 XXE 文件
  读取。修复 `eea5fd74`，随 v5.4.52 发布；CNA 8.7 / NVD 3.1 7.5 与 GHSA LOW 标签冲突。
- **symfony/symfony — CVE-2026-45073（PHP）**。`Cache\Adapter\PdoAdapter::doClear`
  第 435 行把调用方传入的 `clear()` 前缀直接插值进 `LIKE` 子句，未做引用，形成
  SQL 注入。修复 `ec50b799`，随 v5.4.52 发布；NVD 另给 3.1 7.3 HIGH。
- **symfony/symfony — CVE-2026-45077（PHP）**。MonologBridge `server:log` 默认绑定
  `0.0.0.0:9911`，且对每帧直接 `unserialize` 而不设 `allowed_classes`，暴露反序列化
  面。修复 `0891b2f2`，随 v5.4.52 发布；OSV 顶层 CVSS_V4 与 CNA 向量不一致。
- **symfony/symfony — CVE-2026-45133（PHP）**。`Yaml\Parser::parseBlock` 第 529 行
  在解析嵌套块/序列/映射时无限递归，无深度上限，可栈耗尽。5.4.45 无 `ParserState`；
  修复 `914f427e` 引入 `enterNestingLevel`/`leaveNestingLevel`（默认 128），随
  v5.4.52 发布。CNA 8.2 / NVD 3.1 7.5 与 GHSA/OSV 的 LOW 标签冲突。
- **symfony/symfony — CVE-2026-45304（PHP）**。`Yaml\Parser::parseValue` 第 737 行
  解析集合别名时无数量上限，小文档即可指数级内存放大。修复 `e77391b2`，随
  v5.4.52 发布；GHSA/OSV 的 LOW 标签与 CNA 8.7 / NVD 7.5 冲突。
- **symfony/symfony — CVE-2026-45305（PHP）**。`Yaml\Parser::cleanup` 第 1010 行
  的前导注释正则存在嵌套量词，可灾难性回溯；档案同时订正了此前把 1024 行
  文档起始注释误认为嵌套量词的说法——1022/1029 的文档标记正则是单量词，公告
  一并加固但本身不构成经典 ReDoS。修复 `9749cd43`（possessive quantifier），
  随 v5.4.52 发布；GHSA/OSV 的 LOW 标签与 CNA 8.7 / NVD 7.5 冲突。
- **symfony/symfony — CVE-2026-48489（PHP）**。`DefaultAuthenticationFailureHandler`
  第 77 行在 `failure_forward` 开启时采信请求提供的 `_failure_path`，未认证用户可
  借子请求绕过防火墙。修复 `c48a4276`，随 v5.4.53 发布；各来源等级一致为 High。
- **symfony/symfony — CVE-2026-48736（PHP）**。`NoPrivateNetworkHttpClient::request`
  第 84 行的 `PRIVATE_SUBNETS`（33 行常量）缺少 `::/96`、`2002::/16`、`2001::/32`、
  `64:ff9b::/96`、`64:ff9b:1::/48` 等 IPv6 过渡前缀，内嵌 IPv4 可绕过私网拦截
  形成 SSRF。修复 `82765368`（组件侧）与 `85b83155`（6.4+ IpUtils 侧），随
  v5.4.53 发布。CNA 6.9 Medium、OSV Moderate 与 NVD 3.1 8.6 High（S:C）冲突；
  NVD CPE 的 5.4.43 下界也与 OSV 不一致。
- **symfony/symfony — CVE-2026-48784（PHP）**。`UrlGenerator::doGenerate` 第 224 行
  的 `strtr` 与尾部修正只处理不重叠的 `../`、`./`，链式点段每隔一个漏编码，
  生成 URL 在 RFC 3986 归一化后塌缩到路由之外。修复 `4b63c3a3` 改为按 `/` 拆分
  逐段编码，随 v5.4.53 发布；OSV 文字称改用 `preg_replace_callback`，与补丁的
  `explode` 实现不符。影响依赖部署（WHATWG 浏览器会解码 `%2E`）。
- **netty/netty — CVE-2021-43797（Java，4.1.59.Final）**。`HttpObjectDecoder.splitHeader`
  第 826 行以 `findNonWhitespace(sb, 0, false)` 跳过 Java 空白（含 0x0B、0x0C、
  0x1C-0x1F）而非拒绝，`DefaultHttpHeaders.validateHeaderNameElement`（约 368/392 行）
  也缺 0x1c-0x1f 分支；上游代理重序列化头时可形成请求走私。修复 `07aa6b59`
  在两处强制校验 OWS 并补齐 0x1c-0x1f，是 4.1.71.Final 的祖先、不在 4.1.59 中。
  CNA/NVD 均 6.5 Medium（CWE-444），另记 NVD v2 4.3；MITRE 受影响版本串
  `<= 4.1.7.0.Final` 畸形，补丁 commit 名为 merge 实为单父提交，均记入 disagreements。

- **jenkinsci/jenkins — CVE-2024-23898（Java，jenkins-2.441，`snap_d9b0ffa82cd068d0`）**。
  `CLIAction::doWs` 第 117 行处理 GET `/cli/ws` 时只检查 WebSocket 是否可用，
  随后直接取环境认证并升级连接，全程不校验 `Origin`；跨站页面可携带受害者
  Jenkins 会话 cookie 打开该 WebSocket 并以受害者身份执行 CLI 命令（CWE-346）。
  修复 `de450967`（SECURITY-3315）改为接收 `StaplerRequest`，默认对缺失/不匹配
  的 Origin 返回 403，并保留 `ALLOW_WEBSOCKET` 逃生口；是 jenkins-2.442 的祖先、
  不在 2.441 中，2.426.3/2.440.1 亦含修复。NVD Primary/Secondary 均 3.1 8.8 High，
  CNA 无 metrics，GHSA/OSV 标 HIGH 且同向量；CWE-346 各源一致。来源缺陷：
  当前 OSV 版本列表仍把已修复的 LTS 2.440.1-2.440.3 列为受影响，与 CNA 边界和
  2.440.1 代码树矛盾，已记入 disagreements/limitations。
- **netty/netty — CVE-2021-37136（Java，4.1.59.Final）**。`Bzip2Decoder::decode`
  第 294 行按块分配输出缓冲，第 305 行把块加入 `out` 后第 313 行只 `break` 出
  `switch` 并继续循环；`ByteToMessageDecoder.callDecode` 要等 `decode()` 返回才
  flush，因此一次输入内解出的所有块同时驻留，堆占用随总解压量而非单块增长，
  小压缩流可致 OOME（CWE-400）。修复 `41d3d61a` 改为每块解完即 `return`，
  是 netty-4.1.68.Final 的祖先、不在 4.1.59 中。NVD 3.1 7.5 High（另有 v2 5.0
  Medium），CNA 无 metrics，GHSA/OSV 标 HIGH 且同向量。独立 reviewer 纠正了
  档案初稿的一处过度陈述：4.1.59 已有的 `streamBlockSize` 检查已把
  `bwtBlockLength` 限制在声明块大小内，修复新增的 `MAX_BLOCK_LENGTH` 只是
  defense-in-depth，不是可达根因；档案已据此改写，未把它当作漏洞路径。

未提升条目：

- **symfony/symfony — CVE-2024-51736（PHP）** 档案与候选 `disc2_30376ce611735bc208895bc0`
  已就绪（Windows `Process::prepareWindowsCommandLine` 第 1595 行的 cmd.exe 二进制
  植入），独立 reviewer 给出 grade A，但 `severity_consistent=false`。来源为
  CNA 3.1 0.0 NONE（AV:L）、GHSA/OSV 8.4 High、NVD 9.8 Critical（AV:N）。reviewer
  在澄清后仍按「来源之间是否一致」的定义保留 false，并明确这是定义分歧而非事实
  分歧；因此本轮不提升，待复核口径明确后再处理。

推广门槛：54 promoted，1 pending（51736）。正式表更新为 54 漏洞、54 位置、54 复核、
1376 证据、54 行真值矩阵；评测快照仍 22 个（netty 为该快照内第 2 条漏洞）。候选表
`verified` 行 63（含别名簇重复行，均指向已提升漏洞）；`pending_location` 751、
`pending_version` 850、`in_validation` 959，未解决候选 2560（`rejected` 3 行）。
`validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，1 条为
grade A 比例 0/54）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；停止规则不满足。

### 续轮：guzzle 7.4.4（2026-10-22）

- **guzzle/guzzle — CVE-2022-31091 / GHSA-q559-8m2m-g699（PHP）** 候选
  `disc2_bb6f682c14ef0633261e94dc`，快照 `snap_efe695448113758a` = 7.4.4
  （`e3ff079b`）。`RedirectMiddleware::modifyRequest` 第 202 行用
  `shouldStripSensitiveHeaders()` 决定是否丢弃 `Authorization`/`Cookie`；该 helper
  在 222 行比 host、226 行比 scheme，从不调用 `getPort()`，因此同 host 同 scheme 换端口
  时敏感头被转发。第 92-99 行的 curl 凭据路径只比 `getHost()`，是同一次修复覆盖的第二个
  弱点。修复 `1dd98b05`（7.4.5）改用 `Psr7\UriComparator::isCrossOrigin`（host+scheme+
  port），并把 psr7 下限提到 `^1.9 || ^2.4`。
- 独立 reviewer 全 19 项 true，grade B。其修正已并入档案：影响范围补 6.x `<6.5.8`
  （本地镜像无该 tag，仅按公告记录）；7.4.4 的 header 路径已处理 https→http 降级，
  scheme 缺口只残留在 curl 路径；NVD primary 的 CWE 是 `NVD-CWE-noinfo` 而非 CWE-200。
  reviewer 另核对了 psr7 1.9.0/2.4.0 才引入 `UriComparator`，1.8.3/2.1.0 没有。
- 与本快照已提升的 guzzle 漏洞（GHSA 系列）不重复：7.4.2 的 `cc80b002` 只改 curl 路径
  host 比较，未触及 header 剥离逻辑。

推广门槛：55 promoted，2 pending（51736、undici 24807 待独立复核）。正式表更新为
55 漏洞、55 位置、55 复核、1398 证据、55 行真值矩阵；评测快照仍 22 个。候选表
`verified` 行 64（含别名簇重复行，均指向已提升漏洞）；`pending_location` 751、
`pending_version` 850、`in_validation` 958，未解决候选 2559（`rejected` 3 行）。
`validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，1 条为
grade A 比例 0/55）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；停止规则不满足。

### 续轮：undici 5.19.0（2026-10-22）

- **nodejs/undici — CVE-2023-24807 / GHSA-r6ch-mqf9-qc9w（JavaScript）** 候选
  `disc2_7d5dfcba49f9545e30e0a939`，快照 `snap_24c4a191fd049fc3` = v5.19.0
  （`f5c89e5c`）。`lib/fetch/headers.js` 的 `headerValueNormalize()` 第 27-30 行用
  `/^[\r\n\t ]+|[\r\n\t ]+$/g` 修剪 header 值；尾部分支没有起点锚定，内部空白串每个
  起点都要回溯到串尾，故为 O(n²)。`Headers.append`（211 行）与 `Headers.set`（348 行）
  在长度/合法性校验之前调用它。修复 `f2324e54`（v5.19.1）改为显式 charAt 反向扫描 +
  仅保留起点锚定的正则。
- 独立 reviewer 全 19 项 true，grade B。其核对加强了两点并已并入档案：undici 自身
  `lib/fetch/index.js` 的 `onHeaders`/`onUpgrade` 会把服务端可控 header 直接送入
  `Headers.append`，攻击面不限于「应用转发不可信输入」；CWE 为跨来源并集，精确分类是
  CWE-1333（NVD primary 与 GHSA），CNA/OSV 只写 CWE-20。
- 与同版本 CVE-2023-23936 不重复；同一 v5.19.1 还修了 GHSA-5r9g-qh6m-jxff
  （`lib/core/request.js` CRLF 注入，`a2eff054`），根因不同。
- blob 三方一致：快照 inventory 的 `lib/fetch/headers.js` git_oid `634b81fc74a`
  与 v5.19.0 文件、修复 patch 的 pre-image index 相同。

推广门槛：56 promoted，1 pending（51736）。正式表更新为 56 漏洞、56 位置、56 复核、
1421 证据、56 行真值矩阵；评测快照仍 22 个（undici 为该快照内第 2 条漏洞）。候选表
`verified` 行 65（含别名簇重复行，均指向已提升漏洞）；`pending_location` 751、
`pending_version` 850、`in_validation` 957，未解决候选 2558（`rejected` 3 行）。
`validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，1 条为
grade A 比例 0/56）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；停止规则不满足。

### 续轮：rack 2.2.3（2026-10-22）

- **rack/rack — CVE-2025-27610 / GHSA-7wqh-767x-r66v（Ruby）** 候选
  `disc2_84d772d7d1826dc62f7a6a43`，快照 `snap_f97687a4e0807cb2` = 2.2.3
  （`1741c580`）。`lib/rack/static.rb` 的 `Rack::Static#call` 第 124 行原样取
  `PATH_INFO`，第 126 行用 `can_serve(path)` 做 `urls:` 白名单判定；`route_file`
  只看字符串前缀（116 行）。`/cgi/../x` 或编码点段能通过前缀检查，而同一原始路径交给
  `Rack::Files` 后会被 unescape 并解析点段，于是返回 `root:` 下、`urls:` 前缀之外的
  文件。2.2 分支修复 `873d39e6` 改为 `can_serve(Utils.clean_path_info(Utils.unescape_path(path)))`，
  并加回归测试。
- 独立 reviewer 全 19 项 true，grade B。其修正已并入档案：影响上限是 `root:`（
  `Rack::Files` 清理路径后 `File.join(@root, ...)`，不能逃出 `root:`）；OSV/公告只引用
  `50caab74`，但它属于 main、首个含它的发行是 v3.2.0，并非 2.2.13/3.0.14/3.1.12 的修复；
  真正的分支回移是 `873d39e6`（2.2）、`61f83f63`（3.0）、`70cb3228`（3.1），均已在
  git 中复核。OSV 还把版本号 bump 提交标为 fixed 事件，并把 `50caab74` 追加到 3.1 range。
- 该快照区间内 `static.rb` 只有这一处改动，未发现与邻近 rack 根因重复，也非误报。

推广门槛：57 promoted，1 pending（51736）。正式表更新为 57 漏洞、57 位置、57 复核、
1443 证据、57 行真值矩阵；评测快照仍 22 个（rack 为该快照内第 2 条漏洞）。候选表
`verified` 行 66（含别名簇重复行，均指向已提升漏洞）；`pending_location` 751、
`pending_version` 850、`in_validation` 956，未解决候选 2557（`rejected` 3 行）。
`validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，1 条为
grade A 比例 0/57）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；停止规则不满足。

### 续轮：phoenix 1.6.13（2026-10-22）

- **phoenixframework/phoenix — CVE-2026-56811 / GHSA-6983-jfq8-485w（Elixir）** 候选
  `disc2_46723370667ed0c5775db602`，快照 `snap_ee79f4175242bbee` = v1.6.13
  （`6234b576`）。`lib/phoenix/socket.ex` 的 `Phoenix.Socket.handle_in/4` 在
  `phx_join` 分支（595-613 行）对每个 join 调 `Phoenix.Channel.Server.join/4`
  （598 行），把返回的 pid 记进 `state.channels`；`user_connect/6`（544 行）初始化的
  state 只有 `channels` 与 `channels_inverse`，没有计数、上限或速率限制。一个未认证的
  transport 可以就多个可接受 topic 连续发 `phx_join`，每条连接上的持久 channel 进程数
  无界，可耗尽节点进程（CWE-770）。1.6 分支修复 `d19ca0a8` 在 state 加
  `max_channels_per_transport`（默认 100），611 行在达到上限时以 `"too many channels joined"`
  拒绝；首个含它的 1.6 发行是 v1.6.17（`d26a1292`）。
- 独立 reviewer 全 19 项 true，grade B，位置 595-598、blob `7b9f15f4` 与快照一致。其修正
  已并入档案：1.6 range 上界是开区间且下界为 `1.6.0-rc.0`（1.7/1.8 同样改为 `-rc.0`）；
  下界存在来源分歧（CNA 0.11.0，NVD/OSV 的 CPE 派生 range 1.2.0），本地复核 v0.11.0 已有
  无上限的 `sockets`/`sockets_inverse` 映射且每次 `phx_join` 都 `start_link`，故采用
  0.11.0 并记录两种说法；影响收窄为「channel 的 `join/3` 接受该 topic 时才留下持久进程」
  （如通配 `room:*`）。OSV 还把引入提交 `14a297e8`（"Initial channel processes conversion"）
  误列为 fixed，属上游元数据缺陷。
- 分支修复与发行版映射经 git 复核：`c498ba8c`→v1.5.15、`d19ca0a8`→v1.6.17、
  `a612100c`→v1.7.24、`16e295d2`→v1.8.9，四者都不在前一个发行 tag 中；早先记成
  「OSV 提交无法映射到 tag」是我方核对时配错了 tag，已在 `git_object_checks.txt` 更正并
  重算证据哈希。1.5.15/1.7.24/1.8.9 的修复树未逐行 diff。

推广门槛：58 promoted，1 pending（51736）。正式表更新为 58 漏洞、58 位置、58 复核、
1464 证据、58 行真值矩阵；评测快照仍 22 个（phoenix 为该快照内第 1 条漏洞）。候选表
`verified` 行 68（含别名簇重复行，均指向已提升漏洞）；`pending_location` 751、
`pending_version` 849、`in_validation` 955，未解决候选 2555（`rejected` 3 行）。
`validate_dataset.py --draft`：0 error / 50 warning（49 条为未解决候选的仓库，1 条为
grade A 比例 0/58）。覆盖仍 50/50 `NEEDS_REVIEW`，`PASS_KNOWN_SWEEP=0`；停止规则不满足。

### 未提升：phoenix Presence CVE-2026-56812（2026-10-22）

- **phoenixframework/phoenix — CVE-2026-56812 / GHSA-63mc-hw7g-86rr（JavaScript）** 候选
  `disc2_49ab8b917b7f862af6ea3968`，快照同 v1.6.13。`assets/js/phoenix/presence.js`
  的 `Presence.syncState`/`syncDiff` 用 `state[key]` 裸查表，键名为 `__proto__`、
  `constructor` 等 `Object.prototype` 成员时查到内建值，随后 `currentPresence.metas.map`
  抛 `TypeError`，异常逸出 channel 回调，客户端持久无法同步 presence。1.6 修复
  `89a1c4be` 改用 `Object.create(null)` 与 `toNullProtoObj/1`，仅含于 v1.6.17；
  其余分支为 `7f7b971c`→1.5.15、`b90b2252`→1.7.24、`beffc4da`→1.8.9。
- 独立 reviewer 18/19 项 true，**`severity_consistent=false`**：NVD 主评分
  CVSS 3.1 7.5 HIGH 与 CNA/OSV/GHSA 的 CVSS 4.0 6.3 MEDIUM 分级冲突。按既定口径
  不强行提升，档案保留 verdict 路径与失败原因，进入 pending；与 CVE-2024-51736 同类，
  等待严重度口径裁定。
- reviewer 另指出：快照内 `priv/static/phoenix.js|cjs.js|mjs` 构建产物同样含漏洞代码；
  GHSA 声称修复加了 `Object.prototype.hasOwnProperty.call` 门控，实际是去原型链；
  公告漏列 main 上的等价修复 `e84b8f6a`；OSV-EEF 的版本枚举缺若干 tag（区间本身正确）；
  影响前提是应用用客户端可控值作 presence key。

本轮不计入正式表：仍为 58 漏洞、58 位置、58 复核、1464 证据、58 行真值矩阵；
`promotion_report.json` 为 58 promoted / 2 pending（51736、56812）；候选状态不变。
`validate_dataset.py --draft` 仍为 0 error / 50 warning。

### 提升：netty SnappyFrameDecoder CVE-2021-37137（2026-10-22）

- **netty/netty — CVE-2021-37137 / GHSA-9vjp-v76f-g363（Java）** 候选
  `disc2_e513b1ed392ea93513c4b7a9`，快照 4.1.59.Final（commit
  `97d044812dc84288ea2c44c0862c5b1c26cb5b2d`，文件 blob `74a12895`，8914 字节）。
  `SnappyFrameDecoder.decode` 有两条放大路径：`RESERVED_SKIPPABLE` 在整块未到齐时
  直接 `return`，字节留在 `ByteToMessageDecoder` 的 cumulation buffer 里；`COMPRESSED_DATA`
  以无上限的 `ctx.alloc().buffer()` 分配输出，并在 177/183 行调用 `snappy.decode()`，
  后者在 `Snappy.java:287` 执行 `ensureWritable(uncompressedLength)`；`readPreamble`
  最多读 4 个 varint 字节，可声明 `0x0FFFFFFF`（约 256 MiB），极小帧即可迫使大分配。
- 独立 reviewer 全 19 项 true，grade B，位置取 `121-192`（覆盖 skippable 保留、
  分配与解压 sink）；reviewer 身份
  `netty-CVE-2021-37137-round1-independent-reviewer-2026-10-22`，verdict 在
  `runs/independent/netty_CVE-2021-37137_round1/`。
- 采纳的修正：① 行范围由 121-171 扩到 121-192，补上 `snappy.decode()` sink；
  ② 受影响下界改为 `>=4.0.0`（OSV/GHSA 的 Maven ECOSYSTEM range；CNA/NVD 未给下界）；
  ③ OSV 有两条别名互链记录——CVE 端点含 GIT range（fixed 事件为发行提交 `7d34282f`），
  GHSA 端点含 ECOSYSTEM range（`4.0.0`→`4.1.68.Final`），两者均已存档为证据；
  ④ 修复中的 `MAX_COMPRESSED_CHUNK_SIZE > 16777215` 对 24 位 chunkLength 恒为 false，
  真正生效的是 `getPreamble()<=65536`、受限 `buffer(uncompressedSize, 65536)` 与流式 skip；
  ⑤ GitHub 仓库级 advisory 仍显示 medium/null，属陈旧元数据，与 NVD/OSV/全局 advisory
  的 7.5 HIGH 冲突。
- 修复提交是代码改动 `6da4956b`（不在 4.1.59/4.1.66/4.1.67，含于 4.1.68）；tag
  `netty-4.1.68.Final` 指向独立的 release 提交 `7d34282f`。CWE-400；CVSS 3.1
  7.5 HIGH（NVD Primary 与 OSV/GHSA 同向量），NVD 另有 legacy CVSS 2.0 5.0。
- 档案含 9 条证据（新增 `osv_ghsa_endpoint.json`、`Snappy_4.1.59.java`），
  `field_evidence` 全部指向实际支撑项。正式表更新为 59 漏洞、59 位置、59 复核、
  1487 证据、59 行真值矩阵；候选 `verified` 69 行（`in_validation` 954、
  `pending_location` 751、`pending_version` 849、`rejected` 3），未解决 2554。
  `promotion_report.json` 为 59 promoted / 2 pending（51736、56812）。

### 提升：vite server.fs.deny 目录 glob 绕过 CVE-2024-31207（2026-10-22）

- 候选 `disc2_542206954364f27257e02cfc`，快照 `snap_2e50b228f2432623`（tag `v5.0.11`，
  commit `b44c4930`），仓库 vitejs/vite。
- 根因位置 `packages/vite/src/node/server/index.ts:620` 的 `_createServer()`：deny 匹配器
  仅以 `{ matchBase: true }` 构造；消费者 `isFileServingAllowed`（`static.ts:216`）只在
  deny glob 命中时拒绝，未命中即按 allow 放行。
- 机理区分：目录模式（如 `**/.git/**`）对 `/.git/config` 失效的直接原因是 picomatch 的
  `matchBase` 只拿 basename 去匹配；缺 `dot: true` 是另一个只影响 dotfile basename 的缺陷。
  默认 deny 列表全为无斜杠模式，因此必须使用含目录模式的自定义 `server.fs.deny`，并且
  dev server 需经 `--host`/`server.host` 暴露到网络。
- 修复提交 `d2db33f7`（5.0 线），不在 v5.0.10/v5.0.11/v5.0.12，首个含于 v5.0.13；
  `static.ts` 在 v5.0.11 与 v5.0.13 之间字节一致，唯一代码变化就是匹配器构造。
- 受影响范围 `>=5.0.0,<5.0.13`（仅 5.0 线；advisory 另有 2.9/3.2/4.5/5.1/5.2 线）。CWE-200、
  CWE-284；CVSS 3.1 5.9 MEDIUM，CNA 与 NVD Secondary 同向量（NVD 记录 Deferred、无独立评分）。
- 独立 reviewer 全 19 项 true，grade B，位置 `620`（verdict 在
  `runs/independent/vite_CVE-2024-31207_round1/`）；采纳的修正包括因果区分、前置条件、
  deny 为 allow 之上的黑名单、NVD 非独立佐证、MODERATE/MEDIUM 用词与 nocase 引入版本。
- 档案含 8 条证据。正式表更新为 60 漏洞、60 位置、60 复核、1510 证据、60 行真值矩阵；
  候选 `verified` 70 行（`in_validation` 953、`pending_location` 751、`pending_version` 849、
  `rejected` 3），未解决 2553。`promotion_report.json` 为 60 promoted / 3 pending
  （51736、56812、45143）。

### 提升：undici Cookie 跨源重定向泄漏 CVE-2023-45143（2026-10-22）

- 候选 `disc2_209b5e94df3647a5dc0f74d1`，快照 `snap_24c4a191fd049fc3`（tag `v5.19.0`，
  commit `f5c89e5c`），仓库 nodejs/undici。
- 根因位置 `lib/fetch/index.js:1204-1207` 的 `httpRedirectFetch()`：跨源分支只删除
  `authorization`，未删除 `cookie`/`host`；`lib/fetch/headers.js` 明确不实现 forbidden
  request-header（注释在 232/275/374 行），因此调用方通过 `RequestInit.headers` 设置的
  Cookie 会随重定向后的 `mainFetch()` 再次发出。
- 前置条件：调用方显式设置 Cookie 且 `redirect: 'follow'`；该版本没有 cookie jar
  （`includeCredentials` 仍是 TODO），浏览器式默认禁止设置 Cookie 的行为不适用。
- 修复提交 `e041de35`（GHSA merge），不在 v5.26.0/v5.26.1，首个含于 v5.26.2；补丁在
  同一分支增加 `delete('cookie')` 与 `delete('host')`，并加入跨源重定向回归测试。
- 受影响范围 `<5.26.2`。CWE-200；CVSS 3.1 3.9 LOW（CNA、GHSA、OSV 与 NVD Secondary 同向量），
  NVD Primary 另给 3.5 LOW（不同向量）；两者等级均为 Low，无等级冲突。
- 独立 reviewer 全 19 项 true，grade B，位置 `1204-1207`（verdict 在
  `runs/independent/undici_CVE-2023-45143_round1/`）；采纳的说明包括 NVD Primary 分数/向量
  差异、NVD-CWE-noinfo、`delete('host')` 在 5.26 线已被 `470ee381` 覆盖、Cookie 泄漏仅限
  显式设置的头。
- 档案含 9 条证据。正式表更新为 61 漏洞、61 位置、61 复核、1534 证据、61 行真值矩阵；
  候选 `verified` 71 行（`in_validation` 952、`pending_location` 751、`pending_version` 849、
  `rejected` 3），未解决 2552。`promotion_report.json` 为 61 promoted / 3 pending
  （51736、56812、40674）。

### 提升：libexpat internalEntityProcessor 缺失 storeRawNames 的 use-after-free CVE-2022-40674（2026-10-22）

- 候选 `disc2_71ed2ea54895f3e7bca3e63c`，快照 `snap_d33251dac37c334c`（tag `R_2_4_4`，
  commit `81b89678`），仓库 libexpat/libexpat。
- 根因位置 `expat/lib/xmlparse.c:5629-5692` 的 `internalEntityProcessor()`：内部实体替换
  挂起后该函数被装为 `m_processor`，恢复时直接 `return doContent(...)`（5688-5691），
  未调用 `storeRawNames()`；未闭合标签的 `rawName` 仍指向解析缓冲区（`storeRawNames`
  注释 2555-2559），应用在两次解析之间用 `XML_GetBuffer` 或更大的 chunk 触发缓冲区
  重分配后，闭合标签的 `memcmp`（3014-3015）即读取 stale 指针。
- 前置条件：宿主应用在 handler 中挂起、恢复，并由应用侧触发缓冲区增长；攻击者控制 XML
  内容但不控制应用行为，与 `AC:H`、SSVC `Automatable: no` 一致。
- 修复提交 `4a32da8`（PR #629 唯一代码提交，merge `dde178b`），在 R_2_4_9 中加入
  `storeRawNames` 并在失败时返回 `XML_ERROR_NO_MEMORY`；不在 R_2_4_4/R_2_4_6/R_2_4_7/R_2_4_8。
  OSV 的 fixed GIT event `d77291a` 是 2.4.9 发布 merge，不是代码修复，已在证据中区分。
- 受影响范围 `<2.4.9`。CWE-416；CVSS 3.1 8.1 HIGH（NVD Primary 与 CISA-ADP Secondary 同向量，
  CNA 无数值分，OSV 同向量），无等级冲突。
- 独立 reviewer 全 19 项 true，grade B，位置 `5629-5693`（verdict 在
  `runs/independent/libexpat_CVE-2022-40674_round1/`）；采纳的说明包括全函数闭括号在 5693、
  CNA 措辞 "in doContent" 与缺陷点 `internalEntityProcessor` 的区分、OSV 事件映射、
  可达性前置条件与 Debian advisory 的 alias 语义。
- 档案含 7 条证据。正式表更新为 62 漏洞、62 位置、62 复核、1555 证据、62 行真值矩阵；
  候选 `verified` 72 行（`in_validation` 952、`pending_location` 750、`pending_version` 849、
  `rejected` 3），未解决 2551。`promotion_report.json` 为 62 promoted / 2 pending
  （51736、56812）。

### 提升：libexpat 共享 DTD 过早销毁的 use-after-free CVE-2022-43680（2026-10-22）

- 候选 `disc2_0d881f3a17671c58603c5691`，快照 `snap_d33251dac37c334c`（tag `R_2_4_4`，
  commit `81b89678`），仓库 libexpat/libexpat。
- 根因位置 `expat/lib/xmlparse.c:1069-1072` 的 `parserCreate()` OOM 分支：
  `XML_ExternalEntityParserCreate` 在 `context == NULL` 时令 `newDtd = oldDtd`（1338），
  `parserCreate` 把共享 DTD 赋给 `m_dtd`（1031）；`parserInit` 的 `copyString`（1090）
  在内存分配失败时使 `m_protocolEncodingName` 为空，于是 1069-1072 直接
  `XML_ParserFree(parser)`。此时 `m_isParamEntity` 仍为 `XML_FALSE`（1409 才置真），
  `XML_ParserFree` 的守卫（1475）失效，`dtdDestroy`（1479）销毁父解析器仍在使用的
  共享 DTD，形成 UAF/double free。
- 前置条件：需启用 `XML_DTD` 编译；攻击者 XML 只能触发 NULL-context 外部实体 handler，
  `encodingName` 非空与分配失败由应用/环境决定。
- 修复提交 `5290462a`（PR #650，merge `56967f83`），在 `XML_ParserFree` 前加
  `if (dtd) { parser->m_dtd = NULL; }`；回归测试 `43992e4a`；首个含于 2.5.0（`R_2_5_0`），
  不在 R_2_4_4/R_2_4_9。OSV 只有 `last_affected d77291a`（2.4.9 发布 merge），无 fixed event，
  2.5.0 由上游 `expat/Changes` 的 `#616 #649 #650 CVE-2022-43680` 条目确认。
- 受影响范围 `<2.5.0`（through 2.4.9）。CWE-416；CVSS 3.1 7.5 HIGH（NVD Primary 与
  CISA-ADP Secondary 同向量，CNA 无 metric，OSV 同向量），无等级冲突。
- 独立 reviewer 全 19 项 true，grade B，位置 `1069-1072`（verdict 在
  `runs/independent/libexpat_CVE-2022-43680_round1/`）；采纳的说明包括 `XML_DTD`
  编译前提、Debian advisory 的 alias 语义、fix hunk 在 master 的旧行号 1068 与快照 1069
  的区别、浅克隆下 `git tag --contains` 的漏报。
- 档案含 7 条证据。正式表更新为 63 漏洞、63 位置、63 复核、1576 证据、63 行真值矩阵；
  候选 `verified` 73 行（`in_validation` 952、`pending_location` 749、`pending_version` 849、
  `rejected` 3），未解决 2550。`promotion_report.json` 为 63 promoted / 3 pending
  （51736、56812、45811；其中 45811 的独立复核尚未返回）。

### 提升：vite ?import&raw 绕过 server.fs 检查 CVE-2024-45811（2026-10-22）

- 候选 `disc2_2a264309337602506e7d6579`，快照 `snap_2e50b228f2432623`（tag `v5.0.11`，
  commit `b44c4930`），仓库 vitejs/vite。
- 根因位置 `packages/vite/src/node/server/middlewares/transform.ts:137-142` 的
  `transformMiddleware()` import/JS 分支：`?import&raw` 命中 `isImportRequest`/`isJSRequest`
  后进入该分支，`removeImportQuery`（144）与 `unwrapId`（147）留下
  `/@fs/<abs>?raw`，`transformRequest`（172）经 asset 插件 `load`（`asset.ts:189-196`，
  `fsp.readFile` 在 194）直接返回文件内容；解析器的 `/@fs` 分支无条件返回绝对路径。
  `transformRequest.ts:212` 的 `isFileServingAllowed` 只守 `loadResult == null` 的回退
  分支，`?raw` 不会走到，因此 `serveRawFsMiddleware` 的
  `ensureServingAccess`（`static.ts:181-191`）被绕过。
- 攻击面比公告更宽：无扩展名目标（如 `/@fs/etc/passwd?raw`）仅用 `?raw` 即可经
  `isJSRequest` 进入同一路径，这也是修复同时检查 `rawRE` 与 `urlRE` 的原因。
- 修复提交 `03f103383`（PR #18112 在 5.1 分支的 cherry-pick，parent 为 v5.1.7，
  main 合并 `9d2413c8`），把 `ensureServingAccess` 导出并在 import 分支前插入
  `rawRE/urlRE` 守卫；首个含于 5.1.8（`v5.1.8`），不在 v5.0.11/v5.1.7。
- 受影响范围 `>=5.0.0,<5.1.8`（GHSA 分支口径；CNA 笼统写作 `<5.2.14`）。CWE-200/CWE-284；
  CNA 与 NVD Secondary 为 4.8 MEDIUM（`AV:A/AC:H/PR:N/UI:R/C:H`），GHSA 自行为 5.3 MEDIUM
  （`AV:N/AC:L/PR:N/UI:N/C:L`），两者等级同为 Medium，无等级冲突；NVD 记录为 Deferred，
  无 Primary 指标与 CPE。
- 独立 reviewer 全 19 项 true，grade B，位置 `137-142`（verdict 在
  `runs/independent/vite_CVE-2024-45811_round1/`）；采纳的更正包括 144/147/172 行号、
  `static.ts` 181-191、`6820bb3b`(5.4) 与 `a6da4508`(3.2) 标注对调、
  `03f103383` 不在公告 reference 列表而是 5.1 分支 cherry-pick、`transformRequest.ts:212`
  回退分支的措辞修正、`asset.ts` 189-196。
- 档案含 10 条证据。正式表更新为 64 漏洞、64 位置、64 复核、1601 证据、64 行真值矩阵；
  候选 `verified` 74 行（`in_validation` 951、`pending_location` 749、`pending_version` 849、
  `rejected` 3），未解决 2549。`promotion_report.json` 为 64 promoted / 2 pending
  （51736、56812）。

### 提升：vite cjs/iife/umd 产物中的 DOM Clobbering gadget CVE-2024-45812（2026-10-22）

- 快照沿用 `snap_2e50b228f2432623`（tag v5.0.11，commit `b44c4930`），
  `packages/vite/src/node/build.ts` blob `9525809419` 与 `file_inventory.json` 一致。
- 位置 `packages/vite/src/node/build.ts:1076-1081`，函数 `getRelativeUrlFromDocument`，
  `location_kind=logic`。该函数生成
  `new URL('rel', document.currentScript && document.currentScript.src || document.baseURI).href`，
  对 `document.currentScript` 不做 `tagName` 校验；`relativeUrlMechanisms` 的
  cjs（1097-1100）、iife（1102）、umd（1105-1108）均走此路径，
  `toOutputFilePathInJS` 在 `base` 为 `''`/`'./'` 且非 SSR 时选择相对运行时（1159-1162）。
- 攻击模型：页面已存在可注入的无脚本 HTML（如 `<img name="currentScript" src="https://attacker/…">`）
  时，`document.currentScript` 为 null 的异步执行场景会被命名属性访问遮蔽，
  相对资源 URL 被解析到攻击者源，动态加载的资源/分块脚本即形成 XSS。
  reviewer 补充的实际 sink 链：`asset.ts` 的 `renderAssetUrlInJS`（68-137）把该运行时内联到
  JS 产物的 `__VITE_ASSET__` URL，`importAnalysisBuild.ts` 的分块/资源依赖走同一路径。
- 修复提交 `5caa08f06`（`fix: avoid DOM Clobbering gadget in getRelativeUrlFromDocument (#18115)`，
  parent 为 v5.1.7 之后的 `03f103383`），首次含于 5.1.8（`v5.1.8`，`fe6323127`），
  不在 v5.0.11/v5.1.7；v5.1.8 的 build.ts 第 1097 行增加
  `document.currentScript.tagName.toUpperCase() === 'SCRIPT'` 判断。受影响范围
  `>=5.0.0,<5.1.8`（GHSA 分支口径；CNA 笼统写作 `<5.2.14` 且修复列表漏掉 5.1.8）。
  CWE-79；CNA、NVD Secondary、GHSA 的 CVSS 3.1 均为 6.4 MEDIUM（同一向量
  `AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N`），GHSA 另列 CVSS 4.0 4.8，等级一致；NVD 为 Deferred。
- 独立 reviewer 全 19 项 true，grade B，位置 `1076-1081`（verdict 在
  `runs/independent/vite_CVE-2024-45812_round1/`）。采纳的更正包括 CNA 范围与 5.1.8 重叠、
  CNA 修复列表漏 5.1.8、4.x 边界 4.5.4/4.5.5 差异、`toOutputFilePathInJS` 相对分支为 1159-1162、
  `5caa08f06` 不在 GHSA reference 列表而是 5.1 分支 cherry-pick，以及 CVE-2024-31207
  的公开描述应为 `server.fs.deny` 目录模式绕过。
- 档案含 10 条证据。正式表更新为 65 漏洞、65 位置、65 复核、1626 证据、65 行真值矩阵；
  候选 `verified` 75 行（`in_validation` 950、`pending_location` 749、`pending_version` 849、
  `rejected` 3），未解决 2548。`promotion_report.json` 为 65 promoted / 2 pending
  （51736、56812）。

### 提升：Netty HttpPostRequestDecoder 未限制字段数与缓冲字节导致 OOM CVE-2024-29025（2026-10-22）

- 快照沿用 `snap_bb344e672a0544ef`（tag netty-4.1.59.Final，commit `97d04481`），
  `HttpPostStandardRequestDecoder.java`、`HttpPostMultipartRequestDecoder.java`、
  `HttpPostRequestDecoder.java` 的 blob OID 与 `file_inventory.json` 一致。
- 位置 `codec-http/src/main/java/io/netty/handler/codec/http/multipart/HttpPostStandardRequestDecoder.java:385-391`，
  函数 `addHttpData`，`location_kind=logic`。该方法把每个解码字段追加进 `bodyMapHttpData`
  与 `bodyListHttpData`（add 在 391），无字段数上限；multipart 的同名方法（433-444，add 在 443）
  同样无上限。两个 `offer()`（standard 281-309，writeBytes 在 302；multipart 319-357，
  writeBytes 在 340）把内容累积进 `undecodedChunk`，无 `maxBufferedBytes` 限制；
  4.1.59 的 `HttpPostRequestDecoder` 只有第 38 行 `DEFAULT_DISCARD_THRESHOLD`。
- 攻击模型：能控制 POST body 的远程客户端以 chunked 方式持续提交大量小字段，
  或让单个字段跨多个 chunk 长期无法解码，解码器把全部字段和未解码字节留在堆上，
  仅在超过 discard 阈值时丢弃已消费字节，对活动表单状态没有上限，最终可耗尽内存（CWE-770）。
- 修复提交 `0d0c6ed7`（`Merge pull request from GHSA-5jpm-x58v-624v`，parent `d4a640d2`，
  2024-03-21），首次发行于 4.1.108.Final：新增 `DEFAULT_MAX_FIELDS=128`（第 40 行）、
  `DEFAULT_MAX_BUFFERED_BYTES=1024`（第 42 行），standard 在 addHttpData 432-433 抛
  `TooManyFormFieldsException`、在 offer 339-340 抛 `TooLongFormFieldException`，
  multipart 对应检查在 482-483 与 385-386。受影响范围 `<4.1.108.Final`；CNA（GitHub_M）、
  NVD 唯一的 Secondary 指标、GHSA 的 CVSS 3.1 均为 5.3 MEDIUM（同一向量
  `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`），CWE-770。
- 独立 reviewer 全 19 项 true，grade B，位置 `381-392`（verdict 在
  `runs/independent/netty_CVE-2024-29025_round1/`）。采纳的更正包括：公开复现 gist
  （`vietj` 的 Vert.x `Reproducer.java`）确实存在但作者即报告者，按严格口径不构成独立复现，
  维持 B；`offer()` 方法边界为 standard 281-309、multipart 319-357；
  `netty-4.1.108.Final` 是 annotated tag object `1363e1bd`，`3a3f9d13` 是解引用后的 commit；
  CVE-2021-37137 是 Snappy frame decoder 而非 Bzip2。
- 档案含 11 条证据。正式表更新为 66 漏洞、66 位置、66 复核、1652 证据、66 行真值矩阵；
  候选 `verified` 76 行（`in_validation` 949、`pending_location` 749、`pending_version` 849、
  `rejected` 3），未解决 2547。`promotion_report.json` 为 66 promoted / 2 pending
  （51736、56812）。

### 提升：protobuf Java 运行时未知字段嵌套 group 递归无上限 CVE-2024-7254（2026-10-22）

- 目标：`protocolbuffers/protobuf`（repo_id 23357588），快照 `snap_6bc3f36eb61ef280`，
  tag v3.20.1，commit `21027a27c4c2ec1000859ccbcfff46d83b16e1ed`（与 inventory 的
  2451 个路径、blob 与 mode 全量一致）。
- 根因：`java/core/src/main/java/com/google/protobuf/UnknownFieldSchema.java` 的
  `mergeOneFieldFrom`（第 82 行）在 `WireFormat.WIRETYPE_START_GROUP` 分支（98-105）于第 101 行
  以 `mergeFrom(subFields, reader)` 递归解析子组，既无 depth 参数也无上限；`mergeFrom`
  （114-121）又回到 `mergeOneFieldFrom`。`MessageSchema.mergeFrom`（3851）→ `mergeFromHelper`
  （3863）→ 3909 行调用该分支，因此解析含深层嵌套未知 group 的消息会按 wire 中的嵌套深度
  消耗 Java 栈，最终 `StackOverflowError`。`skipField` 在基类 `CodedInputStream` 是抽象的，
  实际递归分支位于 `CodedInputStream.ArrayDecoder`（662-666，1378、2146 重复），
  `ArrayDecoders` 也有同类路径；v3.20.1 的这些路径同样不做递归检查。
- 修复：3.25 分支 commit `4728531c`（`Add recursion check when parsing unknown fields in Java.`，
  parent `850fcce9`，committer date 2024-09-18、author date 2024-09-17），首次发行于 3.25.5
  （v3.25.5 解引用 `9d0ec0f9`）：新增 `DEFAULT_RECURSION_LIMIT=100`（第 16 行）与静态
  `recursionLimit`（19），START_GROUP 分支累加 `currentDepth` 并在 84-89 抛
  `InvalidProtocolBufferException.recursionLimitExceeded()`，depth 传入 `mergeFrom`（88）；
  同一提交也为 `ArrayDecoder` 的 skipField/skipMessage 与 `ArrayDecoders` 加上限制。
  主分支 `d6c82fc5`（PR #18388）是单亲 squash commit，不是 merge，且不是 v3.25.5 的祖先，
  故不作为修复提交。受影响范围：3.x `<3.25.5`、`4.0.0-RC1-<4.27.5`、`4.28.0-RC1-<4.28.2`。
- 严重性：CNA CVSS 4.0 8.7 HIGH（CWE-400/674），NVD Primary CVSS 3.1 7.5 HIGH +
  Secondary 4.0 8.7 HIGH（Primary CWE-787），GHSA HIGH（3.1 7.5、4.0 8.7，CWE-20/400/787）；
  所有公开发布的等级均为 HIGH，CWE 映射分歧按原样记录、不强行归一。
- 独立 reviewer 全 19 项 true，grade B，位置 `82-121`（verdict 在
  `runs/independent/protobuf_CVE-2024-7254_round1/`）。采纳的更正包括：662-666 行属于嵌套
  `ArrayDecoder`；`d6c82fc5` 为 squash 而非 merge；NVD 标记为 Patch 的 `cc8b3483` 实为
  空白性 "Internal change"，真正修复是 `4728531c`；CNA 范围以 version 0 表达，RC 下界来自
  GHSA/OSV；日期为 committer date。`evidence_independent` 经字段语义澄清后由 false 改为 true
  （该字段指复核证据独立于档案，而非独立第三方复现），grade 仍为 B。
- 档案含 8 条证据。正式表更新为 67 漏洞、67 位置、67 复核、1678 证据、67 行真值矩阵；
  候选 `verified` 77 行（`in_validation` 948、`pending_location` 749、`pending_version` 849、
  `rejected` 3），未解决 2546。`promotion_report.json` 为 67 promoted / 3 pending
  （CVE-2021-31542 待 reviewer 输出、51736、56812）。

### 待定：Django 上传文件名点段校验缺失 CVE-2021-31542（2026-10-22）

- 目标：`django/django`（repo_id 4164482），快照 `snap_ab695ba3db678939`，tag 3.0.2，
  commit `a36974395ebc03a41928db1743074575b143330d`。档案
  `runs/verification/django_cve_2021_31542/dossier.json`，位置
  `django/core/files/uploadedfile.py::_set_name` 38-50（关键行 42 `os.path.basename(name)`），
  `location_kind=dataflow`。
- 根因与链路：multipart filename 经 `IE_sanitize`（multipartparser.py 300-302）与
  `os.path.basename` 后，末尾 `.`/`..` 段仍会存活（如 `/tmp/..`→`..`、`foo\..`→`..`），
  或经 `get_valid_filename` 归一为 `..`（如 `$.$.$`）；3.0.2 全树无 `validate_file_name`。
  保存时经 `FileField.generate_filename`（files.py 295-307）与 `Storage.generate_filename`
  （storage.py 101-108）拼路径，默认 `FileSystemStorage.safe_join` 仍限制在 `MEDIA_ROOT` 内，
  可逃逸的是 `upload_to` 子目录。修复 `25d84d64`（3.1 分支，2021-04-27，parent `6b0c7e6f`）
  首次发行于 3.1.9（`8284fd67`）：新增 `utils.py::validate_file_name`（6-14），在
  `_set_name`、`FileField.generate_filename`、`Storage` 加入检查，`get_valid_filename` 拒绝
  `''/'.'/'..'`，并改写 `sanitize_file_name`（该函数由 CVE-2021-28658 的修复引入）。
- 独立 reviewer 结论 `vulnerable_commit`、grade B，18/19 项 true，唯一 false 为
  `severity_consistent`：NVD 同时发布 CVSS 3.1 7.5 HIGH 与遗留 CVSS 2.0 5.0 MEDIUM，
  Django 自己的公告按策略写 “low severity”，而现代 CVSS 3.1/4.0 均为 HIGH（7.5/8.7）。
  按“已发布等级必须一致、不得强行归一”的规则，该条保持 pending，不计入已提升数。
- 重复性：初始 claim 漏列 CVE-2021-28658（同一快照、同为上传文件名穿越，parser-only
  修复 `cca0d981`，3.1.8/3.0.14/2.2.20）。reviewer 依据公开记录与代码判定两者为不同缺陷
  （报告人、修复提交、发行版、文件与校验层均不同，OSV alias 不交叉），`no_false_positive`
  保持 true；档案已补记该重叠与判定。另采纳更正：旧条目类别标签、机制表述过宽、
  `sanitize_file_name` 归属、受影响范围源分歧。
- `promotion_report.json` 当时维持 67 promoted / 3 pending（31542、51736、56812）。

### 提升：Netty SniHandler 未校验 ClientHello 长度导致 16MB 分配 CVE-2023-34462（2026-10-22）

- 目标：`netty/netty`（repo_id 1064563），快照 `snap_bb344e672a0544ef`，tag
  `netty-4.1.59.Final`，commit `97d044812dc84288ea2c44c0862c5b1c26cb5b2d`。
  档案 `runs/verification/netty_cve_2023_34462/dossier.json`，位置
  `handler/src/main/java/io/netty/handler/ssl/SslClientHelloHandler.java::decode`
  117-132（关键行 132 `ctx.alloc().buffer(handshakeLength)`），`location_kind=logic`。
- 链路：`SniHandler`（第 37 行）→ `AbstractSniHandler`（第 32 行）→
  `SslClientHelloHandler`，两个子类都不覆写 `decode`。`decode` 在 117-118 以
  `getUnsignedMedium` 读取对端可控的 24 位 handshake length（上限 0xFFFFFF≈16MB）；
  当 ClientHello 跨 TLS record 时，130-132 在数据到达前按该长度直接
  `ctx.alloc().buffer(handshakeLength)`，无上限；141 再拷贝 record 载荷。约 9 字节的
  record 即可让每条连接占用 16MB，配合无 idle timeout 可耗尽堆。
- 修复：commit `535da17e`（`Merge pull request from GHSA-6mjq-h674-j845`，parent
  `1bb825b7`，2023-06-20），4.1.94.Final 发行提交 `da1a448d`（parent 即修复提交）。
  新增 `MAX_CLIENT_HELLO_LENGTH=0xFFFFFF`、`maxClientHelloLength` 与构造器，在 140-147
  以 `TooLongFrameException` 拒绝超限长度，并在 `SniHandler`/`AbstractSniHandler`
  暴露 `maxClientHelloLength`。
- 严重性：CNA（GitHub_M）6.5 MEDIUM、NVD Primary 6.5 MEDIUM、NVD Secondary 6.5 MEDIUM、
  GHSA MODERATE，全部一致；CWE-400（CNA/GHSA）与 CWE-770（NVD Primary/GHSA）按原样记录。
- 独立 reviewer 19/19 true，grade B，位置 `117-132`
  （`runs/independent/netty_CVE-2023-34462_round1/`）。采纳的关键更正：**修复没有降低默认上限**——
  `MAX_CLIENT_HELLO_LENGTH` 仍为 0xFFFFFF（`getUnsignedMedium` 不可能超过它），且
  `AbstractSniHandler()`/`SniHandler(Mapping)` 传 `maxClientHelloLength=0`，而守卫要求
  `!=0`，故默认路径完全不受检查；只有显式传入 `[1, 0xFFFFFF]` 才受保护，升级到 4.1.94
  本身不改变默认行为。档案 description、fixed_releases、证据与 limitations 均已按此更正，
  `fix_present` 仍为 true（补丁与机制真实存在，但属 opt-in）。
- 重复性：与已提升的 CVE-2021-37136（Bzip2）、CVE-2021-37137（Snappy）、
  CVE-2021-43797（header CRLF）、CVE-2021-21295（HTTP/2 smuggling）、
  CVE-2024-29025（表单字段累积）在包、机制与修复提交上均不同。
- 正式表更新为 68 漏洞、68 位置、68 复核、1709 证据、68 行真值矩阵；候选 `verified` 78
  （`in_validation` 946、`pending_location` 749、`pending_version` 849、`rejected` 4），
  未解决 2544。当时 `promotion_report.json` 为 68 promoted / 3 pending（31542、51736、56812）。
  提升后发现证据行 `source_url` 误写本地镜像路径导致校验 3 条 error，已同时修正档案与
  `runs/verification/verified_evidence.jsonl` 为 `https://github.com/netty/netty` 并重建，
  复验 0 error。

### 排除：Netty setObject 头值校验绕过 CVE-2022-41915 不适用于 4.1.59（2026-10-22）

- 公告范围为 4.1.83.Final 引入、4.1.86.Final 修复（CNA/OSV/NVD 一致）；快照 4.1.59
  早于引入点。
- 代码核验：4.1.59 的 `DefaultHeaders.setObject(K, Iterable/Object...)` 仍通过
  `valueConverter.convertObject(v)` 转换，而 `DefaultHttpHeaders` 默认构造使用
  `HeaderValueConverterAndValidator`（DefaultHttpHeaders.java 444-462），逐字符校验 CR/LF；
  4.1.83 将校验移入独立 `ValueValidator` 后 `setObject` 改走非校验的 `fromObject`，
  才产生绕过。快照代码不存在该路径。
- 记录于 `runs/verification/netty_cve_2022_41915/NOT_APPLICABLE.md`，候选
  `disc2_7c5f687e933fce0b2eb2d544` 由 `in_validation` 改为 `rejected`。不建立档案/复核/正式行，
  不写入真值矩阵。

### 独立复核拦下：Jenkins My Views 权限缺失 CVE-2024-43045（2026-10-22）

- 独立 reviewer（隔离上下文，未读 `runs/verification/`、`data/`）复核快照 2.441 后给
  `vulnerable_commit`、grade B：`MyViewsProperty` 实现 `Action` 但非 `StaplerProxy`、无
  `getTarget()`，`getIconFileName` 227-229 无权限判断，经 `User.getDynamic` 对任意 Overall/Read
  用户可达；修复 `3752f406`（SECURITY-3349）加入 ADMINISTER 检查与回归测试，包含于 2.471。
  18/19 字段 true。
- 拦截字段：`cvss=false`。档案原称「NVD Secondary 与 OSV/GHSA 同为 6.3 向量」，实际
  NVD Primary/Secondary（CISA-ADP）为 6.3 MEDIUM、`AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L`，
  GHSA-8pv9-qh96-9hc6 为 5.4 MEDIUM、`.../C:L/I:L/A:N`（A:N）。三方**等级仍一致（medium）**，
  故 `severity_consistent` 保持 true，只 `cvss` 为 false。
- 档案按 reviewer 结论做事实更正（未改 verdict、未把 false 改成 true）：列出三个已发布分数而不
  断言数值相同；`efece77d` 更正为 2.462.x 回溯（2.452.x 为 `0c13259c`）；`getACL()` 说明改为
  它只服务于 `View.CREATE` 检查；补记 GHSA 的 CWE-285。更正明细见
  `runs/verification/jenkins_cve_2024_43045/CORRECTIONS.md`，原始 `sources/` 与 sha256 不动。
- 推广门槛要求「每个匹配 verdict 的所有字段为 true」，故该档案保持
  `PENDING_INDEPENDENT_REVIEW`；`promote_verified.py` dry-run 报
  `independent review did not verify: cvss`。正式表不变：68 漏洞 / 68 位置 / 68 复核 / 1709 证据 /
  68 行真值矩阵；`promotion_report.json` 为 68 promoted / 4 pending（31542、51736、56812、
  43045）。未重新生成正式表，未新增证据行。

### 提升：Jenkins agent config.xml 未脱敏导致密钥密文泄露 CVE-2025-27622（2026-10-22）

- 独立 reviewer（隔离上下文，未读 `runs/verification/`、`data/`）复核快照 2.441 后给
  `confirmed`、grade B，19/19 字段 true，位置 `core/src/main/java/hudson/model/Computer.java:1559`
  （范围 1551-1560）：GET 分支只做 `checkPermission(EXTENDED_READ)`，随后
  `Jenkins.XSTREAM2.toXMLUTF8` 原样输出节点 XML；`GetNodeCommand.run` 53/55 行同形。
  reviewer 自行补出序列化链：`XStream2.AssociatedConverterImpl` 注册 `Secret$ConverterImpl`，
  其 `marshal` 写 `getEncryptedValue()`（Secret.java:279），因此泄露的是密文而非明文。
- 权限前提经 reviewer 独立确认：`Computer.EXTENDED_READ` 在 1837 行声明、1843 行由
  `hudson.security.ExtendedReadPermission` 系统属性门控，默认关闭；已写入 limitations。
- 修复 `923cdbc1`（SECURITY-3495/3496，2025-02-25，parent `4a9a3ecd`）在 Computer、GetNodeCommand、
  View、GetViewCommand 四处加 CONFIGURE 分支与 `ExtendedReadRedaction.applyAll`；2.500 发布提交
  `cb753134` 的唯一 parent 即该修复。`ExtendedReadRedaction` 在 2.441 完全不存在（@since 2.479）。
- GHSA 把 weekly 段编码成 introduced 2.493、LTS 段 0→2.492.2；reviewer 判定并集覆盖 2.441 且厂商
  公告写明 "2.499 and earlier"，故 `affected_range` 为 true，机器编码差异记入 limitations。
- 发布：`promote_verified.py --apply` → 69 漏洞 / 69 位置 / 69 复核 / 1736 证据 / 69 行真值矩阵；
  `validate_dataset.py --draft` 0 error / 50 warning；候选 `verified` 79、`in_validation` 945，
  未解决 2543。`promotion_report.json` 为 69 promoted / 5 pending（31542、51736、56812、43045、
  27625（复核进行中））。manifest 与 RESUME 计数同步为 69。

### 提升：Jenkins 反斜杠目标绕过重定向安全判断 CVE-2025-27625（2026-10-22）

- 独立 reviewer（隔离上下文）复核快照 2.441 后给 `confirmed`、grade B，19/19 字段 true，位置
  `core/src/main/java/hudson/Util.java:1658-1660`：`isSafeToRedirectTo` 仅拒绝绝对 URI 与 `//`
  前缀，`isAbsoluteUri`（1646-1652）只把 `':'` 在 `#`/`?`/`/` 之前视为绝对，故 `\\example.org`
  这类反斜杠前缀值被判为安全。
- 可达调用点经 reviewer 逐一确认：`DirectoryBrowserSupport.serveFile` 205-209（pattern/path 参数
  直接进入 `sendRedirect2`）、`AuthenticationSuccessHandler.determineTargetUrl` 42-56（52 行判定）、
  `ParametersDefinitionProperty` 180。
- 修复 `4a9a3ecd`（SECURITY-3501，2025-02-25，parent `84ef1a4d`）改为
  `!isAbsoluteUri(uri) && !uri.startsWith("\\") && !uri.replace('\\','/').startsWith("//")`，
  并新增 `Security3501Test`（test/src/test/java/jenkins/security/）以 `userContent?path=` 的
  5 种反斜杠编码断言 Location 仍在本站。发布链 `4a9a3ecd -> 923cdbc1 -> cb753134`（2.500）为直接父子。
- reviewer 澄清：SECURITY-3501 的报告方是 XBOW（第三方公司），不是 CloudBees；因无非报告方复现，
  仍为 grade B。GHSA 的 weekly 段同样被编码成 introduced 2.493，按 CNA 文本与 OSV GIT 段判为覆盖
  2.441，并记入 limitations。
- 发布：70 漏洞 / 70 位置 / 70 复核 / 1761 证据 / 70 行真值矩阵；`validate_dataset.py --draft`
  0 error / 50 warning；候选 `verified` 80、`in_validation` 944，未解决 2542。
  `promotion_report.json` 为 70 promoted / 4 pending（31542、51736、56812、43045）。

### 提升：Jenkins toggleCollapse 缺少 @POST 导致 CSRF CVE-2025-27624（2026-10-22）

- 独立 reviewer（隔离上下文）复核快照 2.441 后给 `confirmed`、grade B，19/19 字段 true，位置
  `core/src/main/java/jenkins/model/Jenkins.java:4214-4221`：`doToggleCollapse()` 无
  `@POST`/`@RequirePOST`，4216 行取 `paneId`，4218 行直接交给
  `PaneStatusProperties.forCurrentUser().toggleCollapsed(paneId)`，既无权限检查也无 crumb。
- sink 经确认：`PaneStatusProperties.toggleCollapsed`（26-34）把任意字符串加入/移出
  `PersistedList`，登录用户落到 `users/<id>/config.xml`（`User.allocateDefaultPropertyInstancesAsNeeded`
  会为每个 UserPropertyDescriptor 建实例），匿名用户落到 session 属性
  `jenkins_pane_<paneId>_collapsed`（61-83）。UI 触发点是 `pane.jelly:62` 的纯 GET 链接；
  reviewer 另指认 `executors.jelly:140` 与 `queue.jelly:48` 对应广告中的 Build Executor Status /
  Build Queue 部件。
- 修复 `84ef1a4d`（SECURITY-3498，2025-02-25，parent `68425e2c`）加 `@POST`，并把
  `pane.jelly`/`executors.jelly` 链接改为 `class="collapse post"` + `lib.form.link.link`；
  新增 `JenkinsTest.testPaneToggleCollapse` 断言 GET 返回 404（注释说明 `@RequirePOST` 会 405）。
  发布链 `84ef1a4d -> 4a9a3ecd -> 923cdbc1 -> cb753134`（2.500）。reviewer 用上游 tag 直接确认边界：
  `jenkins-2.499` 无 `@POST`，`jenkins-2.492.2` 与 `jenkins-2.500` 有。
- 严重级别：NVD 唯一指标为 CISA-ADP Secondary 5.4 MEDIUM（`AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:L`），
  GHSA/OSV 同为 5.4、MODERATE，CNA 无指标；全部为 medium，`severity_consistent=true`。CWE-352。
- 发布：71 漏洞 / 71 位置 / 71 复核 / 1787 证据 / 71 行真值矩阵；`validate_dataset.py --draft`
  0 error / 50 warning；候选 `verified` 81、`in_validation` 943，未解决 2541。
  `promotion_report.json` 为 71 promoted / 5 pending（31542、51736、56812、43045、27623 复核进行中）。
  manifest 与 RESUME 计数同步为 71。

### 提升：Jenkins view config.xml 未脱敏导致密钥密文泄露 CVE-2025-27623（2026-10-22）

- 独立 reviewer（隔离上下文）复核快照 2.441 后给 `confirmed`、grade B，19/19 字段 true，位置
  `core/src/main/java/hudson/model/View.java:1198-1208`：REST `@WebMethod(name = "config.xml")`
  的 GET 分支只做 `checkPermission(READ)`（View/Read），随后 `writeXml` 直接
  `XStream2.toXMLUTF8`；CLI 对应 `GetViewCommand.java:50-51` 同样只查 View.READ。
- reviewer 另指出同期 `AbstractItem.writeConfigDotXml`（AbstractItem.java:873-891）对 job 已有
  `>********<` 掩码，view 缺失，属明确的不变量缺口；2.441 树中
  `jenkins.security.ExtendedReadRedaction` 完全不存在（@since 2.479，已用 `git ls-tree` 核实）。
- 修复 `923cdbc1`（SECURITY-3495/3496，2025-02-25，parent `4a9a3ecd`）是 2.500 发布提交
  `cb753134` 的直接父；2.500 的 `View.doConfigDotXmlImpl`（980-1007）在 983 行查 READ、988 行按
  CONFIGURE 分支、995 行对无权者 `ExtendedReadRedaction.applyAll`；`GetViewCommand` 55-64 同形。
  reviewer 用上游 tag 确认 `jenkins-2.492.2` 亦含该分支，LTS 回移成立。
- 严重级别：NVD 唯一指标为 CISA-ADP Secondary 4.3 MEDIUM
  （`AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`），GHSA/OSV 同为 4.3、MODERATE，CNA 无指标；CWE-312。
  reviewer 记录 GHSA summary 一行误用 agent 场景措辞（details/reference 正确指向 #SECURITY-3496），
  判为文案复制错误，不影响等级一致性。
- 与 CVE-2025-27622 共用修复提交但为独立 advisory 条目（SECURITY-3495 vs SECURITY-3496；
  agent 配置 + Agent/Extended Read vs view 配置 + View/Read），reviewer 判定不重复。
- 发布：72 漏洞 / 72 位置 / 72 复核 / 1814 证据 / 72 行真值矩阵；`validate_dataset.py --draft`
  0 error / 50 warning；候选 `verified` 82、`in_validation` 942，未解决 2540。
  `promotion_report.json` 为 72 promoted / 4 pending（31542、51736、56812、43045）。
  manifest 与 RESUME 计数同步为 72。

### 独立复核批次：9 条新 verdict 未达门槛，2 条待首轮复核（2026-10-22）

- werkzeug CVE-2024-49766：reviewer 判 `confirmed`、grade B，位置 `src/werkzeug/security.py:147-153`
  （`safe_join`），MEDIUM / CWE-22；19 项中仅 `evidence_independent=false`
  （缺陷只在 Windows + Python < 3.11 的 UNC 路径下成立，未找到第三方复现），保持 pending。
- jenkins CVE-2025-67635、67636、67637、67638、67639（5 条）：均 `confirmed`、grade B，位置在
  `config.jelly` / 相关视图，MEDIUM；5 条都只有 `evidence_independent=false`。
  67638 的 GHSA 周窗口起始版本（2.529）与 CNA 不一致、CWE-312 的适配性等已写入 reviewer
  的 `disagreements`，不影响等级一致（全部 MEDIUM/MODERATE）。
- jenkins CVE-2025-31720、31721：`confirmed`、grade B，但 `severity_consistent=false` 且
  `evidence_independent=false`，保持 pending。
- django CVE-2021-33571：`confirmed`、grade B，位置 `django/core/validators.py:79`
  （`URLValidator.ipv4_re`），HIGH / CWE-918；仅 `evidence_independent=false`
  （无独立第三方复现）。reviewer 另记录 4 位八位组如 `0177.0.0.1` 不被该正则接受，不影响结论。
- 以上 9 条使 `promotion_report.json` 的 pending 从 4 条增至 13 条；已提升数仍为 72。
- 同一快照（django 3.0.2）另完成两份 dossier，等待首轮独立 verdict：
  - CVE-2021-33203：`django/contrib/admindocs/views.py:331` 的 `Path(directory) / template`
    未脱敏，staff 可探测任意文件存在性（自定义模板时泄露内容）；MEDIUM 4.9 / CWE-22；
    范围 `>=3.0,<3.1.12`，修复 `20c67a06`/`dfaba12c`，发布 3.1.12/3.2.4；3.0.14 仍未修复。
  - CVE-2021-44420：`django/urls/resolvers.py:156` 用 `re.search` 匹配以 `$` 结尾的 endpoint
    正则，尾随换行路径可被解析，绕过上游按路径的访问控制；NVD HIGH 7.3、GHSA MODERATE、
    Django 发布说明称 low，**三方等级冲突**；OSV 范围含 3.0.2（`>=3.0a1,<3.1.14`），而
    CNA/NVD 从 3.1 起且 3.0.x 无修复发布。按规则不得强行拉平，dossier 记录冲突。
- CVE-2021-33203 的首轮独立 verdict 已回：`confirmed`、grade A（附 Debian buster
  的 `0028-CVE-2021-33203.patch` 作为 `reproduction_reference`），位置
  `django/contrib/admindocs/views.py:331-334`，19 项中仅 `severity_consistent=false`
  ——reviewer 同时记录了 NVD/GHSA/SUSE/Ubuntu 的 MEDIUM 4.9 与 Django 公告的 “low”。
  按门槛保持 pending；grade A 只在提升时才会计入，未提升不改变现有 B 级分布。
  该条使 pending 的 severity 分组从 5 条增至 6 条，独立 verdict 目录 85→86。
- CVE-2021-44420 的首轮独立 verdict 也回了：`confirmed`、grade B，位置
  `django/urls/resolvers.py:155-156`（`RegexPattern.match`）。置 false 的字段是
  `affected_range`、`severity_consistent`、`evidence_independent`、`cwe`：
  - 等级：NVD 7.3 HIGH，GHSA MODERATE，Django 与 Red Hat 均 low（Red Hat 另给 5.3）；
  - CWE：NVD-CWE-Other / GHSA CWE-287 / Red Hat CWE-290；
  - 范围：NVD/OSV/PYSEC 只列 2.2/3.1/3.2，GHSA 写作 `introduced 3.0a1, fixed 3.1.14`；
  - 独立证据：只有 Django commit/回归测试、官方公告、发行版 tracker 与聚合站，无第三方复现。
  reviewer 同时确认 wsgiref 的 `unquote` 会把 `%0A` 变成 `PATH_INFO` 中的真实 LF，
  且 3.0.2 的 `resolvers.py` blob `19d0d989` 不含 `fullmatch`/`\Z`。
  按门槛保持 pending；15 条 pending 的字段分布见 `docs/RESUME.md`。
- 至此快照 3.0.2 在已公开范围内的 CVE 全部建档：31542、33203、33571、44420；
  CVE-2021-32052 因公告范围从 3.1 起被排除。

### 候选排除：curl CVE-2024-0853 不在快照 8.3.0 范围内（2026-10-22）

- 该候选来自 NVD 关键词命中（`disc2_dfcab5985b2d1ec353cc4edc`），原始记录没有范围、CWE、
  severity 或引用，triage 状态为 `pending_version`（空 affected/fixed_versions）。
- 用上游 CURL-CVE-2024-0853 补足范围：仅 **8.5.0** 受影响（introduced 8.5.0 / fixed 8.6.0；
  GIT 引入 `395365ad2d9a6c3f1a35d5e268a6af2824129832`，修复
  `c28e9478cb2548848eca9b765d0d409bfb18668c`），等级 Low，CWE-299。NVD 为 5.3 MEDIUM，
  但版本判定已足以排除，等级差异不影响。
- 引入提交把 `servercert()` 的 OCSP stapling 检查改为在复用会话时跳过
  （`conn_config->verifystatus && !connssl->reused_session`）。在快照
  curl-8_3_0（`6fa1d817e5b1a00d7d0c8168091877476b499317`）上：
  `git merge-base --is-ancestor 395365ad 6fa1d817` 退出码 1，`vtls_int.h`/`openssl.c`
  中都没有 `reused_session`，`verifystatus` 仍在 `openssl.c:3747`/`4233` 无条件执行。
  漏洞路径不存在。
- 处理：`runs/verification/curl_cve_2024_0853/NOT_APPLICABLE.md` + `sources/`（CURL-CVE JSON、
  NVD JSON、git 对象核查）；`candidate_dossiers.jsonl` 与 `data/candidates.jsonl` 的该行标记
  `rejected`。没有 dossier、没有 reviewer、不写正式表。
- 复算：`pending_version` 849→848、`rejected` 4→5，未解决候选 2540→2539；正式表计数不变。
- 同次核查发现的覆盖边界（不是本轮新增漏洞）：curl 官方 advisory 索引里的
  CVE-2023-38546（cookie injection with none file，7.9.1–8.3.0 受影响，8.4.0 修复，
  Low / CWE-73）没有出现在 `data/candidates.jsonl`。原因可定位：`discovery_v2` 里 curl 的
  NVD 关键词结果集（360 条）与本仓库 OSV/仓库公告结果都不含这条记录（不是被 triage 排除）。
  按“未知 ≠ 无漏洞”的规则，只把它记为覆盖限制，不手工捏造候选，也不据此提升；
  curl 快照的覆盖仍为 `NEEDS_REVIEW`、`PASS_KNOWN_SWEEP=0`。

### sinatra CVE-2022-45442 独立复审判定：等级分歧，保持 pending（2026-10-22）

- 为这个此前零漏洞的仓库新建评测快照 `snap_916afbf76073e831`（tag v3.0.3，
  `cafaab99db5b644e5fbe2a19bdba168e671ff1f2`，repo_id 106995，280 个受控文件，
  Ruby first_party 60 文件 / 235,904 字节 / 27.44%），用
  `scripts/build_snapshot_at.py` 生成，正式表重建后 74 快照 / 1815 证据。
- 漏洞：`lib/sinatra/base.rb:405`（`attachment`）把 `File.basename(filename)` 直接插进
  `Content-Disposition` 的 `filename="%s"`，只剥离目录，不转义 `"`/CR/LF。修复提交
  `ea8fc9495a350f7551b39e3025bfcd06f49f363b`（3.0 线，父 `c90f203f`）与
  `1808bcdf3424eab0c659ef2d0e85579aab977a1a`（2.2 线，父 `ee12b185`）加入
  `MULTIPART_FORM_DATA_REPLACEMENT_TABLE`（`%22/%0D/%0A`）并 `gsub`。blob 身份：
  v3.0.3 `d7e2d65` → v3.0.4 `cbb3f2f`、v2.2.2 `986fe45` → v2.2.3 `fb6945c`，与两个
  补丁的 `index` 行完全对应；回归测试在 v3.0.4 `test/helpers_test.rb:784`（断言
  `filename="test.xml%22;%0D%0Aext=.txt"`），v3.0.3 无。
- 独立 reviewer 结论：`confirmed` / grade **B**，位置 `lib/sinatra/base.rb:405-406`，
  `severity_level=high`。置 false 的两个字段：
  - `severity_consistent`：NVD 主/次、CNA、GHSA/OSV、GitHub 公告页与 rubysec 均为 HIGH 8.8，
    但 Ubuntu 优先级 Medium、Red Hat `threat_severity` Moderate（自算 CVSS 仍 8.8）、
    SUSE 评级 important 并自算 7.0；
  - `evidence_independent`：只有厂商/报告者材料与发行版 triage，Debian 的 0007 补丁是上游
    补丁与测试的副本，按规则算弱；CISA SSVC 标 Exploitation "poc" 但未给引用。
- 无 reproduction reference，grade A 本来也不可得。按门槛保持 pending，不改写 verdict、
  不拉平等级；`candidates.jsonl` 的 triage 状态与其它 pending 一致处理。
- 计数：pending 15→16，`promotion_report.json` 仍为 72 promoted / 16 pending；该候选保持
  `in_validation`，因此未解决候选仍是 2539 行（942 in_validation + 749 pending_location +
  848 pending_version），正式表计数不变。
- 口径提醒：档案的 `source_crosscheck` 只覆盖 CNA/NVD/GHSA，reviewer 额外查了发行版优先级，
  因此“三方一致”不等于“所有已发布等级一致”。后续档案应把发行版评级视为独立来源族。

### rack CVE-2026-22860 独立复审判定：仅缺独立证据，保持 pending（2026-10-22）

- 复用既有评测快照 `snap_f97687a4e0807cb2`（tag 2.2.3，
  `1741c580d71cfca8e541e96cc372305c8892ee74`，repo_id 96071，202 个受控文件，
  Ruby first_party 69 文件 / 315,182 字节 / 36.79%），未新建快照。
- 漏洞：`lib/rack/directory.rb:115`（`check_forbidden`）用裸
  `File.expand_path(File.join(@root, path_info)).start_with?(@root)`，`@root` 不带尾部分隔符，
  因此 `/../root_test/` 这类解析到同级同名前缀目录的路径会被判为“在 root 内”；`get()` 随后用
  未规范化路径 `File.join(@root, path_info)` 进 `list_path`，对目录返回 200 列表。
- 版本证据：v2.2.21 的 `directory.rb` blob 仍是 `be72be0`（与 2.2.3 相同），
  `git diff v2.2.21 v2.2.22 -- lib/rack/directory.rb` 打印 `index be72be0..e9e9bb5`，修复加入
  `@root_with_separator` 与分隔符感知比较；main 分支提交
  `75c5745c286637a8f049a33790c71237762069e7`（父 `f2f225f2`）为同一修复，diff index
  `a0c9c93..ca3c015`。回归测试 `not allow directory traversal via root prefix bypass`
  在 v2.2.22 `test/spec_directory.rb:131`、v3.1.20/v3.2.5 第 152 行，2.2.3 缺失。
- 独立 reviewer 结论：`confirmed` / grade **B**，位置 `lib/rack/directory.rb:115-115`，
  `severity_level=high`。唯一置 false 的字段是 `evidence_independent`：GHSA/OSV/NVD/MITRE/
  rubysec 同源于 GitHub advisory，Debian/Ubuntu/Red Hat 均为转述，Debian 对 `a5725c03` 的
  backport 仍是 vendor 提交副本。
- reviewer 的两处事实更正已单独记录在
  `runs/verification/rack_cve_2026_22860/CORRECTIONS.md`：2.2.3 实为 annotated tag
  （tag object `4d456648`，非轻量标签）；2.2.x 实际自 tag 2.2.0 起受影响（2.1.4 的
  `check_forbidden` 直接拒绝所有含 `..` 的路径，已复验）。三处分支 backport 提交
  `a5725c03`/`48e90303`/`f9bde3bc` 经 `.patch` 端点确认存在。证据文件与其 sha256 未改动，
  verdict 不改写。
- 计数：pending 16→17，`promotion_report.json` 为 72 promoted / 18 pending（另 1 条 guzzle
  CVE-2026-67339 仍等 verdict）；未解决候选仍为 2539。

## 当前交接与验证

[仓库准入报告](docs/SELECTION_REPORT.md)、[来源覆盖报告](docs/COVERAGE_REPORT.md)、[质量报告](docs/QUALITY_REPORT.md)、[快照真值报告](docs/ORACLE_REPORT.md)、[继续工作步骤](docs/RESUME.md)。机器进度见 runs/progress.json；结构校验和预选数据完整性结果分别见 runs/validation_draft.txt、runs/preselection_validation.json。

```bash
cd /home/luchitong/work/repo-vuln-50-v02
bash scripts/start.sh
```

默认回放成功查询缓存；需要获取新的 OSV 观察时加 `--refresh`。这只是数据采集续跑入口，不会自动完成独立审核或把候选提升为真值。

下一阶段：把剩余 2539 个未解决候选逐条推进到根因/修复发行版闭环；每个新提升漏洞配新的独立 reviewer；
在最近两轮零新增已验证漏洞后，才可逐仓库考虑 `PASS_KNOWN_SWEEP`。动态红绿测试尚未安排，grade A 仍不可得。
当前 `promotion_report.json` 为 72 promoted / 18 pending（其中 1 条仅缺 verdict：guzzle CVE-2026-67339）：
31542、33203、31720、31721、51736、56812、
2022-45442 因 `severity_consistent=false`（31720/31721、2022-45442 同时缺独立证据）；33571、
67635–67639、49766、44420、2026-22860 因 `evidence_independent=false`；43045 因 `cvss=false`；
44420 同时因 affected_range/cwe 不一致。
十七者均不计入已提升数，也不改写既有 verdict。
发布前必须满足 WORKFLOW.md 的全部门槛。

最终检查：本轮 `validate_dataset.py --draft` 为 0 error / 50 warning；正式表 50 仓库、74 快照、
72 漏洞、72 位置、72 复核、1815 证据、2626 候选、72 行真值矩阵。采集边界测试与预选完整性检查的旧记录仍有效。
以上均不代表正式数据集发布验收通过。

### guzzle CVE-2026-67339 独立复审判定：仅缺独立证据，保持 pending（2026-10-22）

- 档案：`runs/verification/guzzle_cve_2026_67339/dossier.json`；verdict：
  `runs/independent/guzzle_CVE-2026-67339_round1/verdict.json`（`confirmed`、grade B）。
- 快照 7.4.4（`e3ff079b...`，blob 与 `file_inventory.json` 一致）：`CurlFactory::applyHeaders()`
  把包括 `Proxy-Authorization` 在内的所有请求头写入 `CURLOPT_HTTPHEADER`，没有
  `CURLOPT_PROXYHEADER` / `CURLOPT_HEADEROPT`；`StreamHandler::getDefaultContext()` 同样把
  全部头拼进 stream context。修复提交 `9e4580d4...` 在重定向时移除代理凭据头。
- 唯一置 false 的字段是 `evidence_independent`：OSV/GHSA/NVD/PKSA 与发行版材料同源，
  没有独立复现或第三方分析。按门槛保持 pending，不计入已提升数。
- 计数：promotion_report 仍为 72 promoted / 18 pending；未解决候选不变（2539）。

### 中断与恢复：axios CVE-2026-44486（2026-10-22）

- 04:15 在完成 guzzle verdict 与 promotion dry-run 后，启动 axios v1.15.0 评测快照构建
  （`--sha 772a4e54ecc4cc2421e2b746daff0aca10f359d7 --tag v1.15.0`）。该 `git fetch` 运行到
  07:50 被 SIGKILL（exit 137），只留下空的 `scratch/snapshots/axios__axios__772a4e54ecc4.git`
  （`FETCH_HEAD` 0 字节、无提交）；随后 07:53–08:00 连续 422，旧会话终止。
- 已保留的产物：`runs/verification/axios_cve_2026_44486/sources/` 下 9 个来源文件
  （OSV GHSA-j5f8-grm9-p9fc、NVD、CVE v5、v1 修复补丁、0.x backport 补丁、两版 http.js、
  两个 package.json）。尚未写 dossier，也没有 reviewer。
- 已确认目标 SHA 正确：`git ls-remote` 显示 v1.15.0 = `772a4e54ecc4cc2421e2b746daff0aca10f359d7`。
  注意下载的 npm 版 `http.js` blob 为 `b9981159...`，与修复补丁旧 blob `cf3d164f14...` 不同，
  dossier 行号必须从 `772a4e54` 的仓库树重新计算。
- 本次恢复会话将用 tag ref + 有界超时重试快照构建，然后补 dossier、独立 verdict 与 promotion。

### axios CVE-2026-44486 独立复审判定：仅缺独立证据（2026-10-22）

- 档案：`runs/verification/axios_cve_2026_44486/dossier.json`；verdict：
  `runs/independent/axios_CVE-2026-44486_round1/verdict.json`（`confirmed`、grade B）。
- reviewer 独立核对了 v1.15.0 = `772a4e54`、`lib/adapters/http.js` blob `b9981159`、
  `setProxy` 三参数版本与 `beforeRedirects.proxy` 钩子；并用 follow-redirects 1.15.11
  源码确认只有当重定向改变协议且目标不是 https、或改变主机且目标不是子域时才会剥离
  confidential headers，因此同主机 http→https 重定向会把陈旧 `Proxy-Authorization`
  带到直连目标。修复 `afca61a` 的祖先关系用 GitHub compare 验证（merge_base 即 afca61a，
  距 v1.16.0 ahead 35），v1.16.0 与 v0.32.0 blob 均含修复。
- 19 项 `fields_verified` 中唯一为 false 的是 `evidence_independent`：GHSA、MITRE CVE、
  NVD、Red Hat VEX、CISA SSVC 全部源自项目自身公告；ZeroPath 的 write-up 自述
  “completely AI-generated” 且复用公告 PoC；Debian/Ubuntu/SUSE 只是版本 triage。
  按门槛保持 pending，不计入已提升数。
- reviewer 记录的分歧：0.x 下界 `<0.32.0` 只有公告依据，代码检查显示 per-redirect
  re-resolution 从 0.28.0 才出现；0.x backport 比 1.x 窄（“不同代理且无凭据”的重定向仍保留
  旧头）；NVD 无主 CVSS；CWE-200 与 Red Hat 的 CWE-201 并存。
- promotion dry-run：72 promoted / 20 pending（原 18 条 + 44486 + 42037[待 verdict]）。

### axios 候选快照适用性清理：18 条拒收（2026-10-22）

- 依据：OSV npm SEMVER 区间与快照精确版本 1.15.0 比较。`fixed <= 1.15.0`（修复已包含）
  或 `introduced > 1.15.0`（缺陷晚于快照）者不适用于本快照。
- 拒收 18 条 `disc2_*`：2019-10742、2020-28168、2021-3749、2023-45857、2024-39338、
  2025-27152、2025-58754、2026-25639、2026-39865、2025-62718、2026-40175、
  2026-67314、67320、67321、101903、101905、101907、101909。
- 报告：`runs/verification/axios_snapshot_not_applicable/NOT_APPLICABLE.md`。状态写入
  `runs/verification/candidate_dossiers.jsonl`（备份 `/tmp/candidate_dossiers.bak.20261022.jsonl`），
  再由 `build_formal_tables.py --tables candidates` 重建 `data/candidates.jsonl`；未手改 candidates。
- 计数：rejected 5→23，未解决候选 2539→2521（in_validation 942→924）。
  `validate_dataset.py --draft` 仍为 0 error / 50 warning。
- 未处理：`adv3_*` 的 68943/69124/69125 不在 ledger 中，虽区间显示 introduced 1.15.1/1.15.2
  仍保留 pending_version；待后续统一处理 advisory 家族。

### axios CVE-2026-42037 独立复审判定：affected_range 与独立证据均未过（2026-10-22）

- 档案：`runs/verification/axios_cve_2026_42037/dossier.json`；verdict：
  `runs/independent/axios_CVE-2026-42037_round1/verdict.json`（`confirm`、grade B）。
- 缺陷已确认：v1.15.0 `lib/helpers/formDataToStream.js:27` 的 `FormDataPart` 构造函数把
  `value.type` 原样插入每个 part 的 `Content-Type`，而同函数字符串分支（第 25 行）与
  `escapeName`（第 20–21、54–64 行）都会处理 CR/LF。修复 `75873270`
  （`fix: strip crlf correctly (#10758)`，父提交 `f0b98673`）加入
  `.replace(/[\r\n]/g, '')`；父 blob `f191e8cb` 等于 v1.15.0 快照 blob，
  v1.15.1 tag `ac42446b` 的 blob `7612791` 与修复后一致，且 npm 1.15.0/1.15.1 的
  `dist/node/axios.cjs` 分别保留漏洞行/修复行。入口 `lib/adapters/http.js:509-521`
  对任何 `isSpecCompliantForm(data)` 调用该 helper，`utils.js:738` 只要求
  `append`、`Symbol.toStringTag==='FormData'` 与迭代器，鸭子类型对象即可通过。
- `fields_verified` 两项为 false：
  - `affected_range`：公告下界 `>=1.0.0` 过宽。`formDataToStream.js` 在 npm 1.0.0/1.1.0/1.2.0
    中不存在（也没有等价的 `value.type` 原样插值），1.3.0 才出现且已带缺陷；有效区间应为
    1.3.0–1.15.0，修复边界 1.15.1 准确。
  - `evidence_independent`：OSV/NVD 仅引用 GitHub 公告，Snyk/Debian/Ubuntu/VulDB/OpenCVE
    均为同一公告的聚合；无独立分析或复现。
- reviewer 记录的额外事实：公告称 `value.name` “可能有同样问题”不成立，`escapeName` 会
  百分号编码 CR/LF 与引号；原生 Node `Blob/File` 会把 `.type` 中不可打印字符清成空串，
  因此“用户上传原生 File”的叙事不能直接利用，PoC 用的是自定义 blob-like 对象；
  `form-data` npm 包不满足 `isSpecCompliantForm`，不是本路径的向量。
- promotion dry-run 保持 72 promoted / 20 pending（阻塞字段：`affected_range`,
  `evidence_independent`）。未改写 verdict，也未缩窄档案范围。
- 计数：verdict 92 个（72 已提升 + 20 pending）；`docs/RESUME.md` 已同步 75 快照、
  1816 证据、候选 924/749/848/82/23（未解决 2521）。

### django 3.0.2 候选范围核查：1 条拒收、13 条降为 pending_version（2026-10-22）

- 背景：OSV 多区间扫描曾把 14 条 django 候选算作“影响 3.0.2”。复查发现 OSV 的
  `versions` 数组是按 `introduced..fixed` 机械枚举的，EOL 的 3.0.x 会被自动列入，
  不能单独作为受影响证据。
- CVE-2021-35042（`disc2_59949922a1aa40250a8f5123`）**不适用**：修复提交
  `0bd57a879a0d54920bb9038a732645fb917040e9` 的说明写明回归由 `5139487`
  在 3.1 引入（"This regression appeared in 3.1"）；3.0.2 的
  `django/db/models/sql/query.py:1901` 仍用 `ORDER_PATTERN` 严格校验（`queries.name);`
  会抛 `FieldError`），3.1.12:1900 与 3.2.4:1972 则是宽松的 `if '.' in item:`，
  3.1.13:1902 / 3.2.5:1974 恢复校验。证据与哈希在
  `runs/verification/django_cve_2021_35042/`（含 NOT_APPLICABLE.md）。
  另发现该目录原有的 `sources/osv_ghsa.json` 实际是 Ory fosite 的记录，已保留不动，
  另存正确的 `osv_ghsa_xpfp_f569_q3p2.json`。
- 其余 13 条（2022-36359、2024-45231、2025-57833/64458/64459、
  2026-15307/15830/6873/8404/48587/48588/53877/53878）公告正文只声明
  4.2/5.x/6.x，其中 64458/64459 明说旧分支“未评估、可能受影响”；
  `affected_range` 对 3.0.2 无法核实，状态由 `in_validation` 降为 `pending_version`，
  写入 blocker，未拒收。对照表：`runs/verification/django_3.0.2_range_scoping/SCOPING.md`。
- 计数：in_validation 924→910；pending_version 848→861；rejected 23→24；
  未解决候选 2521→2520。promotion 不变（72/20）。
  `validate_dataset.py --draft`：0 error / 50 warning；`progress.json` 已刷新。

### Jenkins 2.441 候选范围核查：174 条拒收（2026-10-22）

- 方法：对 192 条 `in_validation` Jenkins 候选，只取 Maven
  `org.jenkins-ci.main:jenkins-core` 的 OSV 区间，按 `introduced <= 2.441 < fixed`
  逐条计算；区间里没有 `last_affected`，无需额外分支。
- 结果：171 条所有区间 `fixed <= 2.441`（快照已含修复）；3 条所有区间
  `introduced > 2.441`（CVE-2026-27099 2.542 起、33002 2.442 起、53441 2.483 起）。
  共 174 条改为 `rejected`，blocker 写入区间与报告路径。
- 保留：18 条区间包含 2.441，继续保持 `in_validation`：
  2024-43044、43045、2025-31720/31721、2025-67635–67639、2026-27100、
  33001、53435–53440、53442。其中 43045、31720/31721、67635–67639 已有 verdict
  但字段未过门槛。
- 报告：`runs/verification/jenkins_snapshot_not_applicable/NOT_APPLICABLE.md`
  （逐条候选、CVE、区间）。依据仅 OSV 已发布范围，无代码层结论。
- 计数：in_validation 910→736；rejected 24→198；未解决候选 2520→2346。
  promotion 不变（72/20）。`validate_dataset.py --draft`：0 error / 50 warning，
  `progress.json` 已刷新。

### netty / symfony 快照范围核查：7 + 57 条拒收（2026-10-22）

- netty 4.1.59.Final：对 32 条 `in_validation` 候选按 `io.netty` 的 OSV 区间逐条计算，
  4 条修复已在快照内（CVE-2014-0193、2014-3488、2015-2156、2021-21290——最后一条恰在
  4.1.59.Final 修复），3 条在快照之后才引入（2025-24970 起于 4.1.91.Final、
  2026-42577 与 2026-48748 起于 4.2.0.Final），共 7 条改为 `rejected`；25 条区间包含
  4.1.59.Final，保持 `in_validation`。报告：
  `runs/verification/netty_snapshot_not_applicable/NOT_APPLICABLE.md`。
- symfony 5.4.45：59 条候选按 branch-aware 规则判定——要求“每个区间都满足
  `fixed <= 5.4.45` 或 `introduced > 5.4.45`”。第一版分类器要求“所有区间都 fixed 或都
  introduced”，把 5 条多分支公告误判为 `mixed_unclear`；改为逐区间判定后 57 条
  `not_affected`，2 条保留（disc2_30376ce611735bc208895bc0 CVE-2024-51736 区间
  `0..5.4.46`；disc2_51632e0837f1373e7161a3cc CVE-2026-24739 区间 `0..5.4.51`）。
  报告：`runs/verification/symfony_snapshot_not_applicable/NOT_APPLICABLE.md`。
- 依据均为 OSV 已发布区间，无代码层结论；逐条区间见报告表格。

### undici / vite / rack 快照范围核查：18 + 4 + 10 条拒收（2026-10-22）

- undici 5.19.0：29 条候选中 18 条所有区间已修复或晚于快照，拒收；11 条保留。
- vite 5.0.11：13 条中 4 条拒收，9 条保留。
- rack 2.2.3：26 条中 10 条拒收，16 条保留。
- 报告：`runs/verification/{undici,vite,rack}_snapshot_not_applicable/NOT_APPLICABLE.md`。
- 备注：rack 初筛曾误用 repo id 997338（pallets/werkzeug），导致全部 `no_range`；
  已改用 96071（rack/rack）重跑。werkzeug 初筛未过滤 GIT 型区间，把提交 SHA 当版本号
  解析成 `unclear`；过滤非 ECOSYSTEM 区间后 6 条 `not_affected` / 5 条 `affected`。

### 小型评测仓库快照范围核查：8 仓库 21 条拒收（2026-10-22）

- 覆盖 express 4.19.2（1）、guzzle 7.4.4（2）、hyper 0.14.2（1）、laravel 11.30.0（7）、
  flask 2.3.1（2）、werkzeug 3.0.2（6）、phoenix 1.6.13（1）、rustls 0.23.4（1），
  共 21 条候选在所有区间上“已修复或晚于快照”，统一改为 `rejected`。
  合并报告：`runs/verification/small_repos_snapshot_not_applicable/NOT_APPLICABLE.md`
  （逐仓库表格，含候选、CVE、区间）。
- 边界案例：express CVE-2024-29041 与 guzzle CVE-2022-31042 的 `fixed` 恰等于快照版本
  （4.19.2 / 7.4.4），按 `introduced <= V < fixed` 不含快照，属已修复。
- 各仓库保留（区间含快照）的候选数：guzzle 8、hyper 2、laravel 4、flask 1、
  werkzeug 5、phoenix 1；express、rustls 无保留。gin、protobuf 的候选全部落在区间内，
  未做拒收。
- 计数：in_validation 736→619；rejected 198→315；未解决候选 2346→2229。
  `data/candidates.jsonl` 已由 `build_formal_tables.py --tables candidates` 重建；
  `validate_dataset.py --draft` 0 error / 50 warning；`progress.json` 已刷新；
  promotion 不变（72 promoted / 20 pending）。

### django 3.0.2 全量区间核查：114 条拒收（2026-10-22）

- 触发：复核 `data/candidates.jsonl` 时发现 django 仍有 118 条 `in_validation`，
  其中多数 CVE 的修复版本远早于 3.0.2（例如 CVE-2019-19844 修于 3.0.1），此前只处理了
  OSV 机械包含 3.0.2 的那 14 条，说明全量扫描没有跑过。
- 方法：只取 `affected[].package.name == django`（PyPI）的 `ECOSYSTEM`/`SEMVER` 区间，
  按 `introduced <= 3.0.2 < fixed` 判定；GIT/SHA 区间跳过。114 条候选的所有区间都在
  3.0.2 及之前修复、或在 3.0.2 之后才引入，统一改为 `rejected`。
  逐条候选、CVE 与区间见 `runs/verification/django_snapshot_not_applicable/NOT_APPLICABLE.md`。
- 关键修正：第一版评估器没有按包名过滤，把 CVE-2019-11358（多生态 jQuery XSS）算成
  django 受影响；限定 PyPI `django` 后它落在 `<2.2.2`，实际不适用，一并拒收。
- 保留 4 条区间确实包含 3.0.2 的候选：CVE-2021-31542、33203、33571、44420；
  四者均已有独立 verdict，继续 pending，不因本次批量处理而改变。
- 性质：范围适用性拒收，不含代码层结论；公告未列 3.0.x 不等于已证明代码无缺陷，
  但也不把“未评估旧分支”反推为受影响。
- 计数：in_validation 619→505；rejected 315→429；未解决候选 2229→2115。
  `data/candidates.jsonl` 已重建；`validate_dataset.py --draft` 0 error / 50 warning；
  `progress.json` 已刷新；promotion 不变（72/20）。

### netty CVE-2021-21409：重复公告判定，降为 pending_location（2026-10-22）

- 起点：`runs/verification/netty_cve_2021_21409/sources/` 已备好 21295 的对照材料，
  想给快照 4.1.59.Final 再提升一条。核对 `data/vulnerabilities.jsonl` 时发现
  CVE-2021-21295（GHSA-wm47-8v5p-wjpj）**早已提升**在同一快照（commit 97d0448，
  `runs/independent/netty_CVE-2021-21295_round1/`），因此不能重复提升 21295。
- 改查 21409 本身：OSV `GHSA-f256-j965-7f32`、CVE v5（CNA GitHub_M，2021-03-30T15:05:17Z）、
  NVD 2.0 均已拉取并留档；CVSS 3.1 5.9 MEDIUM、CWE-444、区间
  `io.netty:netty-codec-http2` 4.0.0 → 4.1.61.Final。**区间确实包含 4.1.59**，所以不是范围拒收。
- 判定依据（代码 + 公告原文）：
  - 公告明说 “This is a followup of GHSA-wm47-8v5p-wjpj which did miss to fix this one case”，
    只在“单个 HEADERS 且 endStream=true”这一帧序上漏检。
  - 4.1.59 的 `DefaultHttp2ConnectionDecoder.java` 中 `CONTENT_LENGTH`/`contentLength`/
    `normalize` 出现 0 次，根本没有任何 content-length 校验——这正是已提升的 21295。
  - 4.1.60 才引入 `verifyContentLength`，并用 `if (!stream.isHeadersReceived())` 门控头解析
    （396-411）；新建且 endOfStream=true 的流已是 HALF_CLOSED_REMOTE，门控被跳过，这才是 21409。
  - 21409 的修复 `b0fa4d5aab4215f3c22ce6123dd8dd5f38dc0432` 把门控改成 `isTrailers`
    （4.1.61 的 356/362/400 行），diff 上下文在 4.1.59 不存在。
- 结论：同一快照、同一文件、同一 sink、同一根因，按“一个根因位置一行”的 schema 不另立条目；
  候选 `disc2_1e6dabf5089176b69f5406db` 由 `in_validation` 降为 `pending_location`
  并写入 blockers。沿用 axios CVE-2026-44487 的重复公告处理先例。
  记录见 `runs/verification/netty_cve_2021_21409/NOT_APPLICABLE.md`（含 sha256 与 tag peel）。
- 计数：in_validation 505→504；pending_location 749→750；rejected 不变 429；
  未解决候选 2115 不变。`data/candidates.jsonl` 已重建；
  `validate_dataset.py --draft` 0 error / 50 warning；`progress.json` 已刷新；
  promotion 不变（72/20）。

### protobuf CVE-2022-3509：TextFormat 递归子消息 → 已提升（2026-10-22）

- 起点：protobuf 快照 v3.20.1（`snap_6bc3f36eb61ef280`，vulnerable_commit
  `21027a27c4c2ec1000859ccbcfff46d83b16e1ed`）上已有 round-2 verdict 的候选。
- 材料：OSV `GHSA-g5ww-5jh7-63cx`、CVE v5、NVD 2.0；修复补丁 `a3888f5`
  （"Clean up TextFormat parser (#10673)"）与 backport `db7c178`；v3.20.1 / v3.20.3 /
  v3.21.7 三个版本的 `MessageReflection.java`、v3.20.1 的 `TextFormat.java`；
  `git_object_checks.txt` 记录 tag peel、blob SHA 与 `merge-base --is-ancestor` 结果。
- 缺陷：`BuilderAdapter.newMergeTargetForField`（503-517）在字段已存在时总是
  `newBuilderForType()` 建新实例再 `mergeFrom(已有值)`，每次嵌套出现都把整棵子树
  再合并一遍；`TextFormat.Parser.merge` 的自递归（1799、2079-2080）与
  `finish()`/`setField` 回写（545-546、2193）使深度/宽度线性输入变成指数级合并，
  可致 CPU/内存耗尽（CWE-400，CVSS 3.1 7.5 HIGH，CNA 与 NVD Primary 一致）。
- 修复内容：改为复用 `getFieldBuilder`（`hasNestedBuilders` 缓存），
  `finish()` 返回 `builder` 而非 `buildPartial()`，`setField`/`setRepeatedField`/
  `addRepeatedField` 遇到 `MessageLite.Builder` 时统一 `buildPartial()`。
- **backport 事实**：`a3888f5` 不是 `v3.20.3` 的祖先（GitHub 走 backport 分支），
  已用相同 blob `294d8417` 证明 v3.20.3 的 `MessageReflection.java` 内容就是修复后内容；
  reviewer 独立找到 backport commit `24b65038cfe36191268fda355aca0e43d3ecbcbe`。
- 独立复核：`runs/independent/protobuf_CVE-2022-3509_round1/`（隔离只读上下文），
  19 个字段全 true，grade B（无动态复现），位置 503-518 与档案 503-517 重叠。
- 门槛：dry-run 73 promoted / 20 pending，`--apply` 后重建，
  evidence 1839、candidates 2626（in_validation 503 / verified 83）、
  snapshot_vulnerability_status 73；`validate_dataset.py --draft` 0 error / 50 warning；
  `progress.json` 已刷新。protobuf 本仓库漏洞数 2→3。

## 2026-10-22 v0.2 → v0.3 无损迁移

- 输入：`/home/luchitong/work/repo_vuln_50_agent_starter_v03.zip`
  （sha256 `d15dfdb18546a859c957592f0d5623e8f3ee4bf62b0290a40c3603feabd2b9e6`），
  解压到独立目录，工具与 schema 复制到本仓库 `v03/`。
- 实际基线（重新读取落盘数据，不采用用户历史描述）：50 仓库、75 snapshots、22 个旧评测目标
  （覆盖 22 个不同仓库，无一仓多目标）、73 漏洞、73 locations、1839 evidence、73 reviews（全 B）、
  73 行真值、2626 candidates（503 in_validation / 750 pending_location / 861 pending_version /
  83 verified / 429 rejected），未解决 2114。与用户报告的 72/1816/505/749/82/2115 的差异
  来自此前 protobuf CVE-2022-3509 提升与 triage 更新，未删除候选。
- 迁移：`migrate_v02_to_v03.py` 先 dry-run 再 `--apply` 到 `/home/luchitong/work/repo-vuln-50-v03`。
  源目录未写入；`migration_backup_v02/data/` 保存十个 JSONL 的字节级副本（SHA256 与源一致）。
  九张主表行数不变；7 张表字节级一致；repositories 仅新增 `evaluation_snapshot_id`
  （22 非空 / 28 空）；snapshots 仅新增 `purpose`，`evaluation_target` 22 个无翻转。
  `historical_snapshot_status.jsonl` 为空——没有旧目标被降级。
- 选择：22 个旧目标全部保留为 `proposed`，0 frozen；28 个无已验证漏洞的仓库保持
  `needs_selection`（25 个仅 HEAD，axios/OpenSSL/sinatra 另有 tag 快照但无 confirmed_affected）。
  未按漏洞数量或候选数量自动选版。
- Schema 兼容修补：starter 的 `vulnerabilities.schema.json` GHSA 正则只允许大写，
  拒绝 9 条真实小写 GHSA canonical ID；改为 `[0-9A-Za-z-]`，未改数据。
  原文件 sha256 `bffa7469…`，修补后 `efa419ad…`，记录在 MIGRATION_REPORT。
- 校验：`v03/scripts/validate_dataset.py . --draft` 0 error / 50 warning
  （49 条 coverage unresolved + grade A<60%）；严格模式 132 error，全部是发布门槛未达成。
  v0.2 原验证器回归 0 error；v0.3 两个 unittest 各 5 项通过。
  参考验证器 `validate_v02_reference.py:108` 有大小写缺陷，误报 9 条，未改数据。
- 交付：`MIGRATION_REPORT.json`、`SELECTION_REPORT.md`、`CATALOG_COVERAGE_REPORT.md`、
  `ORACLE_REPORT.md`、`VALIDATION_REPORT.json`、`LIMITATIONS.md`，以及 `v03/` 工作流代码与 schema。
- 状态：manifest 仍为 draft，`source_cutoff_date=null`；PASS_KNOWN_SWEEP 0/50，grade A 0。
  按用户指示，本轮迁移完成后不再继续收集；未完成的 28 个评测目标、22 个冻结审查、
  2114 条未决候选原样保留。

---

# v0.3.1 升级与低成本相关性筛选（2026-10-22）

## 做了什么
1. 用 `v031/scripts/upgrade_v03_to_v031.py`（dry-run 后 --apply）从 `/home/luchitong/work/repo-vuln-50-v03`
   无损升级到本目录；源 v0.3 只读未写。复制 9753 文件并逐一记录 SHA256（`UPGRADE_REPORT.json`）。
2. 安装 v0.3.1 kit 到 `v031/`（WORKFLOW/AGENT_PROMPT/docs/schemas/scripts/tests/cost_policy.example）。
3. schema 补丁：v0.3.1 starter 的 GHSA 正则退回收大写，补回 `[0-9A-Za-z-]`（SHA256=efa419ad…，同 v0.3）。
4. 复算真实基线：50/75/73/73/1839/73/2626/50/73；漏洞实为 **73**（非上报 72）；target 22/0 frozen。
5. 新增 `data/snapshot_candidate_triage.jsonl`（P3 零 LLM 规则）：1568 = 83 confirmed_affected（73 distinct
   vuln）/410 confirmed_not_affected/1075 unknown；28 未选仓库 1058 条候选不 triage。
6. 旧 `discovery_coverage` 归档 `legacy_discovery_coverage_v03.jsonl`，50 条 outcome 重置 NEEDS_REVIEW。
7. 校验：draft 0 errors / 50 warnings；release 253 errors（全为门槛阻塞，无结构损坏）。
   v0.3.1 单测 Ran 9 tests OK。
8. 费用台账：本版迁移+漏斗零 LLM，0 记账调用 / ¥0；cost_policy=500 元阈值，非网关。
9. 交付：README_V031.md / docs/RESUME_V031.md / LIMITATIONS_V031.md / SELECTION_REPORT_V031.md /
   CANDIDATE_FUNNEL_V031.md / MIGRATION_AND_VALIDATION_V031.md / v031/reports/*。

## 未做 / 阻塞
- 未冻结任何目标（需独立 reviewer+frozen_at+防泄漏工作树导出）。
- 28 仓库未选版（Catalog 已验证漏洞为 0；未编造 tag/commit）。
- 1075 unknown + 28 仓库 1058 候选未完成相关核验；未声明 PASS_KNOWN_SWEEP。
- 无动态复现（grade A 0 条）；无 Agent 评测运行；无工作树导出。

## 2026-10-22 独立选版审查、冻结与 P6 审计导出

- 隔离审查包：`v031/scripts/build_selection_review_packets.py` 生成 22 个 packet
  （`v031/reviews/selection_packets/`），只含原始事实，不含 collector 理由/候选数/策略。
- 独立审查：`independent-review-agent-2026-10-22` 写 `v031/reviews/selection_review_2026-10-22.jsonl`，
  **12 accept / 10 reject**；10 个 reject 仅第 2 项 release sanity 未过（tag 超过 4 年且存在更新稳定版），
  其余 5 项检查全过（tag 解析、archive/manifest hash、无 `.git`、计数对账）。
- P6 审计导出：`build_audit_exports.py` 生成 `data/snapshot_audit_exports.jsonl` 与
  `exports/*.audit.tar.gz`；排除 50 个含 advisory ID 的文档、替换 10 个代码文件中的 ID，
  归档重扫剩余 advisory ID **0**。
- 冻结：`apply_selection_review.py --apply` → 12 `frozen`（合计 40 条 anchor）、
  10 保持 `proposed` 并写入拒绝理由；冻结行记录 export/audit ID 与 SHA256。
  备份：`/tmp/evaluation_selection.pre_freeze.jsonl`（临时）。
- schema/validator：新增 `snapshot_audit_exports.schema.json`；validator 校验审计行来源、
  哈希、excluded/redacted 计数，并要求 frozen 目标存在匹配且零 advisory ID 的审计导出。
- 校验/单测：`validate_dataset.py --draft` 0 error / 50 warning；unittest **21 tests OK**
  （新增 audit export 回归测试）。release 门槛仍未通过。
- 未做：10 个被拒目标未改选新 tag；26 个提案仓库未做源码级正样本确认；
  1075 unknown 未核验；无动态复现；未声明 `PASS_KNOWN_SWEEP` 或 release。

## 2026-10-22/23 ruby/rexml v3.4.1：先证据、后选版（首个 grade A）

### 做了什么
1. 从 28 个 needs_selection 仓库中选 ruby/rexml（135525225），先在已发布 tag v3.4.1 上做源码级确认，
   再进入选版流程。
2. 漏洞核验 dossier：`runs/verification/rexml_CVE-2025-58767/dossier.json`，14 条证据
   （OSV/GHSA/NVD/ruby-lang 公告、fix patch、tag peel、v3.4.1/v3.4.2 源码、差分探针），
   快照 `snap_23dff8507560a593`（196 个 tracked 文件，Ruby first-party 54 个）。
3. 独立漏洞复核：`runs/independent/rexml_CVE-2025-58767_round1/verdict.json`，reviewer ≠ prepared_by；
   **grade A**，red/green：v3.4.1 对 4 MB 无空白正文读入全部 4,000,014 字节（64 MiB 文件全量读入、
   RSS 增长约 131 MiB），v3.4.2 同一输入仅读 7 字节即抛
   `XML declaration misses spaces before version`；重复声明 v3.4.1 接受、v3.4.2 拒绝
   `XML declaration is duplicated`。复现脚本保留在
   `runs/independent/rexml_CVE-2025-58767_round1/reproduction/`。
4. 数据合并：新增 `v031/scripts/promote_verified_rows.py`（默认 dry-run；schema 校验、冲突拒绝、
   reviewer≠preparer、commit/文件/行范围校验），写入 1 vulnerability + 1 location + 1 review +
   30 evidence + 1 snapshot_vulnerability_status；`snapshots.jsonl` 增加 evaluation_target 快照，
   `repositories.evaluation_snapshot_id` 指向它；被取代的 snapshot proposal 归档到
   `runs/selection/superseded_snapshot_proposals.jsonl` 后移出主表。
5. 导出与 P6：`freeze_snapshots.py --only ruby/rexml` → 196/196 文件、tag/tree 与 commit 一致、
   无 `.git`、`missing_from_archive_count=0`；`build_audit_exports.py --only ruby/rexml`
   → 排除 `NEWS.md`（含历史 CVE-2021-28965），剩余 advisory ID 0。
6. 独立选版审查：`v031/reviews/selection_review_2026-10-23.jsonl`，四项强制导出检查全 true、
   tag peel 一致（annotated `1069a326…` → `bfb37e9…`）、anchor 由 GHSA/OSV/NVD 三源确认；
   `apply_selection_review.py --apply` → frozen，`vulnerability_count_at_selection=1`，
   leakage_controls 完整；既有 22 行未被降级（有回归测试覆盖）。
7. 工具修复：`build_audit_exports --only` 保留其他行并对旧行缺失计数容错；
   `apply_selection_review` 对未覆盖行保留既有结论、冻结备注改用 review 日期；
   `promote_verified_rows` 要求全部复核字段显式 true、grade A 必须有 reproduction_reference、
   red_green_summary 如实反映复现。
8. 校验：draft 0 error / 50 warning；release 240 error（全部为覆盖/门槛阻塞，无结构错误），
   rexml 仅剩 coverage sweep 三项；unittest 35 OK。

### 未做
- 未声明 `PASS_KNOWN_SWEEP`；rexml 的 coverage 仍为 `NEEDS_REVIEW`（仅在 coverage_statement
  注明 1 条已确认正样本）。
- rexml 的候选行尚未写入 `snapshot_candidate_triage.jsonl`（正样本不依赖 triage，但漏斗统计
  仍为旧 22 库口径）。（已于 2026-10-23 补齐，见下节）
- 其余 27 仓库未选版；10 个被拒目标未改选；1075 unknown 未核验。

## 2026-10-23 rexml 收尾：候选提升、triage 行与文档对账

- 候选 `disc2_de98c5ab937e69a43862e5b4`（aliases CVE-2025-58767 / GHSA-c2f4-jgmc-q2r5）由
  `in_validation` 置 `verified`，写入 `vulnerability_id`，清空已解决的 blocker
  （原为 “No root-cause location mapped at a vulnerable SHA”）；reason 改为与其余 83 条
  verified 一致的 “Promoted after independent review …”，notes 追加
  `verified: CVE-2025-58767 sha=bfb37e9…`。未改 `updated_at`（该字段保留原始观察时间，与既有行一致）。
- 新增 1 条 triage：`snap_23dff8507560a593 / disc2_de98c5ab937e69a43862e5b4`，
  decision=`confirmed_affected`，review_method=`source_code_review`，checked_at 取复核时间
  `2026-10-22T16:14:38Z`；basis 记录版本区间、根因位置、fix commit 与 red/green 结果。
  漏斗变为 1569 行：84 confirmed_affected（distinct 74）/ 410 not_affected / 1075 unknown；
  候选状态 84 verified / 429 rejected / 750 pending_location / 502 in_validation / 861 pending_version。
  仍未 triage：1057 条（27 个未选仓库 + rexml 其余 8 条）。
- 修正 `reviews.jsonl` 的 `rev_CVE_2025_58767_r1.reviewer`：原值原样复制 dossier 的准备期状态
  “Codex collecting agent (single reviewer); no independent reviewer assigned”，与同一行的
  `grade=A`、`independent_reviewer` 自相矛盾；改为身份 “Codex collecting agent”。
  dossier 本身保留为复核前历史记录，不回写（其中 `status=awaiting_independent_review` 属当时事实）。
- 对账：draft 0 error / 50 warning；release 240 error（均为覆盖/门槛阻塞）；unittest 35 OK。
  未声明 `PASS_KNOWN_SWEEP`、未发布。

## 2026-10-23 下一目标：django/django 4.2.13（先证据阶段，未写数据行）

- 背景：django 3.0.2 在 10-22 的独立选版审查中因 tag 超过 4 年（`obsolete_release_over_4_years`）被拒。
  按「先证据、后选版」在同一仓库的更新稳定 tag `4.2.13`（commit `3bf46e2e…`，2024-05-07）上取证。
- 锚点：CVE-2024-39330（GHSA-9jmf-237g-qf46，CWE-22，路径穿越）。
  候选行 `disc2_911c6ce3cba60cce0edccd71` 此前只因不适配 3.0.2 被 rejected，其 source_urls 已含 fix commit。
- 已保存证据（`runs/verification/django_CVE-2024-39330/sources/`，13 条）：
  OSV 记录、GitHub advisory 页、NVD 记录、Django 2024-07-09 安全公告、4.2.x 与 5.0.x 两个 fix patch、
  ls-remote tag、git facts、两版 `storage/base.py` 与 `files/utils.py`、4.2.14 release notes。
- 关键事实：`2b00edc` 是 4.2.14 祖先、不是 4.2.13 祖先；patch 前后 blob id（`16ac22f…→03a1b44…`、
  `85342b2…→11e4f07…`）与两 tag 的 `git hash-object` 完全一致；4.2.13 的 `Storage.save` 只在 `_save`
  之后调用 `validate_file_name`，且 `validate_file_name` 未把反斜杠归一化。
- 语言清单：`runs/language/snap_516aa9971dd9509d/`（6733 tracked files，Python 854 首方 + 1894 测试）。
- 严重度分歧已记录：GitHub HIGH（CVSS 4.0，VC:H）vs NVD 4.3 MEDIUM（PR:L/C:L）。
- 独立复核已启动，reviewer 只收到原始事实；**在 verdict 返回前不写任何数据行**（snapshot/selection/vuln 等均未改）。

- 严重度数值更正：dossier 初稿写 `CVSS 4.0 / 8.7 HIGH`，但 8.7 在已保存证据中**无出处**
  （GHSA 页面的分数由 JS 渲染，OSV 只给 vector）。现改为有出处的口径：NVD 记录 CVSS 3.1
  `4.3 MEDIUM`（`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`，metric source GitHub CNA
  `134c704f`），并在 `source` 字段注明 GitHub advisory 另按 CVSS 4.0 评为 HIGH 的分歧。
  `build_dossier.py` 已同步重建（13 条 evidence 不变）。未写任何数据行。

## 2026-10-23 django 目标切换完成、审计导出修复、rack v3.1.13 升级

- django：独立 verdict（grade A、confirmed_affected、red/green）返回后，`promote_verified_rows.py
  --apply` 写入 1 漏洞（CVE-2024-39330）/1 location/1 review/26 evidence/1 status；候选
  `disc2_911c6ce3cba60cce0edccd71` 置 verified；快照 `snap_516aa9971dd9509d`（tag 4.2.13）设为
  evaluation_target，旧目标 `snap_ab695ba3db678939`（3.0.2）降为 historical_evidence。
  旧快照的 163 条 triage、8 条 status、1 条 export、1 条 audit export 全部归档到 `data/legacy_*`，
  未删除；旧漏洞/location/review/evidence 行保留但不再计入 live Oracle。
- django 新快照的 162 条未复核候选全部补为 `unknown`（不是照搬旧快照的驳回结论），只写 1 条
  confirmed_affected triage。release 校验器关于「162 candidates not pre-filtered」的提示随之出现，
  这是诚实缺口而非结构错误。
- 选版审查第一轮 **reject**：审计导出残留 `docs/releases/security.txt` 的 113 个 Sphinx
  `:cve:`2024-NNNN`` 角色（无 `CVE-` 前缀，旧正则漏检）及 `docs/releases/4.2.txt` 的 1 个。
  修复 `build_audit_exports.py`：正则加入 `:cve:` 角色形式、扫描改为全文 bytes（去掉 1 MiB 截断）。
  重建 django 审计导出：排除 114、替换 1、文件 6,615、剩余 advisory ID 0；第二轮独立审查 **accept**
  （复算 tag peel、6,729 文件逐字节、6,615 文件全字节泄漏扫描 0 命中），已 `--apply` 冻结。
- rack：独立漏洞复核返回 **grade A / confirmed_affected**，并给出可由 Ruby 3.2.3 复现的 red/green
  （v3.1.13 接受 5,000 参数与 4,194,307 字节；v3.1.14 均抛 `QueryLimitError`）。reviewer 同时指出
  dossier 的 3 处非载荷错误（2bb5263 分支实为 3-0-stable、CWE-770 仅见于 NVD/GitHub、excerpt 从 46 行起），
  已按复核事实更正 dossier，未改动其结论。
- rack 目标从 2.2.3（`snap_f97687a4e0807cb2`）切到 v3.1.13（`snap_245aee01ea5112b9`）：
  新增快照行、selection 行（proposed）、全树导出 180 文件、P6 审计导出（排除 1、替换 0、剩余 0）；
  旧快照的 50 条 triage、2 条 status、export/audit 行归档；`promote_verified_rows.py --apply` 写入
  CVE-2025-46727 的 1 漏洞/1 location/1 review/21 evidence/1 status；候选 `disc2_7f2500f7…` 置 verified；
  其余 49 条 triage 为 unknown。独立选版审查 **accept**（tag peel、180 文件逐 blob、179 文件全字节泄漏扫描
  0 命中；审查者记录 packet 的 `tag_commit_tree_sha` 为 null，但 tree 已由其独立验证），已 `--apply` 冻结。
- 当前计数：78 snapshots / 76 vulnerabilities / 76 locations / 1916 evidence / 76 reviews /
  66 snapshot_vulnerability_status（63 B + 3 A）/ 1577 triage（76 affected rows，distinct 66 /
  293 not_affected / 1208 unknown）；23 个评测目标，**15 frozen / 8 proposed**（余下均为 legacy）。
  draft 0 error；unittest 35 OK。未声明 `PASS_KNOWN_SWEEP`、未发布。
- rexml 剩余 8 条候选（7 个 distinct CVE + 1 条重复 advisory）在 v3.4.1 快照上完成判定：OSV 的
  `fixed` 版本分别为 3.2.5/3.2.7/3.3.2/3.3.3/3.3.6/3.3.9；完整 clone 中这些修复 tag 的 commit 与
  advisory 给出的 fix commit 均为快照 commit `bfb37e9…` 的祖先，故判 `confirmed_not_affected`
  （`runs/verification/rexml_snapshot_not_applicable/NOT_APPLICABLE.md`）。这是排除性证据，
  不证明快照无其他漏洞；rexml coverage 的 `unresolved_candidates` 由 8 改为 0（仍 `NEEDS_REVIEW`）。
- 校验器只做结构检查；真正剩余的 triage 缺口是 1208 条 unknown 与 27 个未选仓库的 1049 条候选。

## 2026-10-23 libexpat R_2_4_4 → R_2_6_2 升级（先证据、后选版）

- 背景：libexpat 旧目标 R_2_4_4（`snap_d33251dac37c334c`）在 10-22 独立选版审查中因 tag 超过 4 年
  （`obsolete_release_over_4_years`）被拒。按同一规则，先在更新稳定 tag `R_2_6_2`
  （commit `fa75b96546c069d17b8f80d91e0f4ef0cde3790d`）上取证。
- 锚点：CVE-2024-45490（XML_ParseBuffer 接受负长度）。证据（`runs/verification/libexpat_CVE-2024-45490/sources/`，
  10 条）包含 OSV/NVD 原始 JSON、tag 对象与 peel、fix commit `5c1a3164` 与 `88b3ed5` 的祖先关系、
  `xmlparse.c` 行号 grep、fix patch、R_2_6_2/R_2_6_3 两版函数摘录。
- 复现路径：一次性 `XML_ParseBuffer(parser, -1, …)` 只返回错误（`XML_ERROR_NO_ELEMENTS`），不崩溃；
  崩溃需要随后再次 `XML_GetBuffer` —— `m_bufferEnd` 被移到缓冲区之前，下一次调用返回分配区前 1 字节的指针，
  写入即 ASan heap-buffer-overflow。dossier 与 reviewer 的 harness 都保存了两步路径的日志；选版审查者的一步
  测试未触发崩溃，记录后以代码 + 祖先关系为据（规则允许），结论不受影响。
- 独立漏洞复核（reviewer 未读 collector dossier，自建 harness）：**grade A / confirmed_affected**，
  R_2_6_2 两步触发 ASan overflow、R_2_6_3 修复版无崩溃。verdict 在
  `runs/independent/libexpat_CVE-2024-45490_round1/`。reviewer 指出 dossier 5 处表述/来源不精确
  （location 实际到 2097、CWE-611 来自 nvd@nist.gov、CWE-190 与 9.8 secondary 来自 CISA-ADP、
  修复版第二次 `XML_GetBuffer` 返回有效指针），`build_dossier.py` 已全部更正后重建 dossier（evidence 数不变）。
- 数据写入（verdict 返回之后才执行）：`promote_verified_rows.py --apply` 写入 1 漏洞（CVE-2024-45490）/
  1 location/1 review/18 evidence/1 status；候选 `disc2_35a922eb511ed468630f4a2d` 置 verified 并补 1 条
  confirmed_affected triage。快照 `snap_67132f0363b8bc23`（tag R_2_6_2）设为 evaluation_target，
  旧目标 `snap_d33251dac37c334c`（R_2_4_4）降为 historical_evidence。
- 归档（未删除）：旧快照的 143 条 triage、7 条 status、export/audit 行 → `data/legacy_*_snap_d33251dac37c334c.jsonl`；
  旧 selection 行 → `data/legacy_evaluation_selection_80314213.jsonl`。
- 导出与审计：全树导出 199 文件（198 regular + 1 symlink，`missing_from_archive_count=0`）；
  P6 审计导出排除 `expat/Changes`、替换 `expat/tests/basic_tests.c` 的 advisory ID，剩余 0。
  独立选版审查 **accept**（四项导出检查全 true、tag peel 一致、4 条 https anchor），已 `--apply` 冻结。
- 新快照其余候选：R_2_4_4 时代的 7 个旧 CVE 以 OSV 修复区间 + fix commit 祖先关系判
  `confirmed_not_affected`（`runs/verification/libexpat_R_2_6_2_fixed_previous/NOT_APPLICABLE.md`，
  排除性证据）；其余 135 条保留 `unknown`。coverage 已更新并注明未声明 `PASS_KNOWN_SWEEP`。
- 当前计数：79 snapshots / 77 vulnerabilities / 77 locations / 1934 evidence / 77 reviews /
  60 snapshot_vulnerability_status（56 B + 4 A）/ 1577 triage（70 affected rows，distinct 60 /
  300 not_affected / 1207 unknown）；23 个评测目标，**16 frozen / 7 proposed**；
  27 个未选仓库的 1049 条候选仍无 triage。draft 0 error。未声明 `PASS_KNOWN_SWEEP`、未发布。

## 2026-10-23 — phoenixframework/phoenix：旧目标被 4 年规则拒绝 → 在 v1.8.8 重新取证并冻结

- 背景：phoenix 旧目标 v1.6.13（2022-09-29）在选版审查中仅因 `obsolete_release_over_4_years` 被拒；
  该结论不等于「phoenix 无正样本」。按「先证据、后选版」，先在更新稳定 tag `v1.8.8`
  （commit `99df0a99da13265cb8b5cd3a506a79b3de34339f`，2026-06-10）上取证。
- 锚点 1：CVE-2026-56811（transport 不限制每连接 channel join 数，CWE-770；`>=1.8.0-rc.0,<1.8.9`，
  修复 commit `16e295d2`，1.8.9 引入 `max_channels_per_transport`）。dossier 8 条证据
  （`runs/verification/phoenix_CVE-2026-56811_v188/`）。
- 锚点 2：CVE-2026-56812（Presence 键与 `Object.prototype` 成员冲突时 `state[key]` 返回真值但无
  `metas`，`TypeError` 中止该 topic 的 presence 同步；CWE-754；修复 commit `beffc4da`，1.8.9 用
  `Object.create(null)`/`toNullProtoObj`）。dossier 8 条证据
  （`runs/verification/phoenix_CVE-2026-56812_v188/`）。
- 独立漏洞复核（两个 reviewer 均未读 collector dossier）：
  CVE-2026-56811 → `confirmed_affected`，grade B（静态；`runs/independent/phoenix_CVE-2026-56811_v188_round1/`）；
  CVE-2026-56812 → `confirmed_affected`，grade A（Node red/green：同一 tag blob 上 20/20 原型键抛错，
  1.8.9 为 0/20；复现与源码存 `runs/independent/phoenix_CVE-2026-56812_v188_round1/repro/`）。
  reviewer 指出 `syncDiff` 的首个抛错点是 `.filter`（行 119/128）而非 `.map`，dossier 的 location 跨度
  68-137 不受影响。
- 数据写入（verdict 返回之后才执行）：`promote_verified_rows.py --apply` 两次，各写入 1 漏洞 /
  1 location / 1 review / 19 evidence / 1 status（其中累计 19 evidence 每次）。候选状态：
  `disc2_49ab8b917b7f862af6ea3968` 与 `adv3_a7fa8aabc9d9faea` 置 verified；`disc2_bf1a633e2d88c00a930f2763`
  与 `adv3_4f4c48000f44cf53` 置 rejected（v1.8.8 上 `confirmed_not_affected`，附代码级证据）。
- 快照：`snap_aca73214a7703174` 设为 evaluation_target（478 文件，tree `4047ddd8…`）；旧
  `snap_ee79f4175242bbee`（v1.6.13）降为 historical_evidence。旧目标的 8 triage、2 status、export/audit、
  21 evidence、1 location、1 review 与 selection 行归档到 `data/legacy_*_snap_ee79f4175242bbee.jsonl` 与
  `data/legacy_evaluation_selection_16072585.jsonl`（注：迁移中曾误删 CVE-2022-42975 的 location 与 1 条
  evidence，已从归档文件原样恢复）。
- 导出与审计：全树导出 478 文件（0 symlink、0 gitlink，`missing_from_archive_count=0`，sha256
  `e225eeb0…`）；P6 审计导出 `aud_aca73214a7703174` 排除 `CHANGELOG.md` 与 `guides/security.md`、
  替换 0、剩余 advisory ID 0。
- 选版审查：首轮 `build_ok=false`（环境无 Elixir/Erlang）。随后在用户目录安装 Erlang/OTP 25.3.2.8
  （Ubuntu deb 用 `dpkg -x` 解包，无需 root）与 Elixir 1.17.3（官方 precompiled elixir-otp-25），
  采集侧 `mix deps.get`、`mix compile` 均 exit 0；该审查者从导出包自行重新解压、复跑构建（92 beam），
  改判 `build_ok=true`，总判定 **accept**，`--apply` 冻结
  （`v031/reviews/selection_review_phoenix_2026-10-23.jsonl`）。
- 新快照 8 条候选全部 triage：CVE-2026-56811 ×2、CVE-2026-56812 ×2 → `confirmed_affected`；
  CVE-2022-42975（`compare_host?/2` 点边界，fix 1.6.14）、CVE-2017-1000163（`validate_local_url/1` 拒绝
  `//` 与反斜杠，fix 1.2.3）、CVE-2026-32689 ×2（`long_poll.ex` 惰性 `String.splitter` + `Enum.find`，
  fix 1.8.6）→ `confirmed_not_affected`，均为代码级核对 + 修复 commit 祖先关系，不是裸版本号比较。
- 当前计数：80 snapshots / 78 vulnerabilities / 78 locations / 1951 evidence / 78 reviews /
  60 snapshot_vulnerability_status（55 B + 5 A）/ 1577 triage（71 affected rows，distinct 60 /
  303 not_affected / 1203 unknown）；23 个评测目标，**17 frozen / 6 proposed**；
  27 个未选仓库的 1049 条候选仍无 triage。draft 0 error。未声明 `PASS_KNOWN_SWEEP`、未发布。

## 2026-10-23 protobuf v3.25.4 与 sinatra v4.0.1 提升、旧行恢复

- protobuf：v28.1 因 `build_not_feasible` 无法冻结后改靶到 v3.25.4（`e915ce24…`，2024-07-24）。
  独立复核返回 `confirmed_affected` / A（真实 JDK 17 + Maven 3.9.16 + protoc 25.4 构建，`-Xss256k`
  下 Lite `parseFrom(InputStream)`、Lite `parseFrom(byte[])`、`DiscardUnknownFieldsParser` 三条路径
  exit 42 SOE，v3.25.5 同 payload exit 3 IPBE；深度 3 对照 exit 0）。复核同时给出反例：普通 full-runtime
  生成消息 `parseFrom` 在 v3.25.4 不会溢出，先被 `CodedInputStream.readGroup` 既有 100 层限制拦下，
  该负结果已写入 dossier limitations。
- protobuf 迁移 `--apply`：创建 `snap_442de86eb5fd3f62`，旧 v28.1 目标降为 historical_evidence，
  归档 76 evidence / 1 location / 1 review / 1 vuln / 1 status / 14 triage / 1 selection / export+audit；
  脚本改为保留旧快照的 PASS `languages` evidence（快照行仍在，校验器要求）。
  `promote_verified_rows.py --apply` 写入 1 vuln / 1 location / 1 review / 128 evidence / 1 status。
- sinatra：v4.1.1 的 CVE-2025-61921 复核判 `not_affected`（线性、无数据行）后改靶 v4.0.1
  （`7dc5940e…`），CVE-2024-21510 独立复核 `confirmed_affected` / A，真实 gem 动态验证
  （4.0.1 → `Location: http://attacker.example/…`；4.1.0 默认仍重定向；配置 `permitted_hosts` 才 403）。
  迁移 `--apply` 创建快照、proposed selection、6 条 triage；promote 写入 1 vuln / 1 location /
  1 review / 84 evidence / 1 status。
- 两库 freeze + audit 导出完成：sinatra 289 文件，审计排除 `CHANGELOG.md`、剩余 advisory 0；
  protobuf 2708 文件，整树无任何 CVE/GHSA 记号（独立按字节复扫确认），审计与源导出逐字节相同、
  剩余 0。
- 修正历史遗留不一致（未删除任何行）：v0.3.1 迁移时旧 protobuf v3.20.1 与 gin v1.5.0 快照的
  vulnerability/location/review/evidence 行被归档，但候选仍为 `verified`，校验器报 6 个错误。
  以 `runs/data_fixes/restore_legacy_rows_2026-10-23.py` 从归档恢复 CVE-2022-1941、CVE-2022-3509、
  GHSA-6vm3-jj99-7229 及其 location/review/evidence（60 条，含两个快照的 PASS languages 证据）；
  CVE-2024-7254 旧快照行不复原（id 已属新快照）。per-snapshot status 行保持归档——校验器只接受
  evaluation_target 快照的 status 行。draft 校验 0 error。
- 两处工具修正：`promote_verified_rows.py` 的 status 行只引用 PASS evidence；本轮回填快照时保留了
  旧快照的语言证据。`promote_verified_rows` 的 evidence id 合成规则（`ev_<vid>_snapshot_<idx>`）
  会在同一漏洞跨快照时撞名；已改为把 snapshot id 纳入合成（`ev_<vid>_<snap_…>_<field>_<idx>`），
  并按内容签名复用已有 evidence id，使旧 dossier 重跑保持幂等（protobuf、sinatra 两套 dossier
  干跑均 0 append / 0 conflict）。
- 当前：86 快照（24 个评测目标），82 漏洞/82 location/82 review/2205 evidence/53 status；
  24 条 selection（20 frozen、2 proposed-pending、2 proposed-rejected）；26 库未选版。
  未声明 `PASS_KNOWN_SWEEP`，未发布。

## 2026-10-23 echo 侦察与快照建立

- 侦察（只读，`runs/verification/echo_recon/RECON.md`）：labstack/echo 选定
  CVE-2026-55677 / GHSA-vfp3-v2gw-7wfq / GO-2026-6293（`%2F` 编码斜杠绕过路由级中间件、
  暴露静态目录文件，CWE-22，7.5 HIGH）。v4 受影响最高 tag `v4.15.2`
  （`25685e6f5f7b0683105d1386db46ae48eb3de028`，2026-05-01），首个修复 tag `v4.15.3`
  （`8800212ad4…`），v4 修复 commit `c3fa2a27ff92b2b8db360de614f999ef1da24725`（PR #3011）。
  用修复 commit 自带回归测试在 v4.15.2 上实测 `/admin%2Fsecret.txt` → 200 泄漏、v4.15.3 → 404；
  `git merge-base --is-ancestor` 判定修复在 v4.15.3 内、不在 v4.15.2 内；`go build ./...` 在
  两棵树均 exit 0（需 Go ≥ 1.25，系统未预装，侦察侧临时下载 1.26.10）。
- **数据来源更正（重要）**：侦察初稿把 10 个 2026-09-27 的 GHSA 判为「疑似伪造」。复核后
  （本会话直接请求）这些是 GitHub **仓库级**已发布 advisory：仓库 Security 页面
  `https://github.com/labstack/echo/security/advisories/GHSA-3pmx-cf9f-34xr` 返回 200 且标题匹配，
  而同一路径下不存在的 GHSA 返回 404；它们不进 `github.com/advisories`、`github/advisory-database`
  与 OSV。结论改为：真实但仅仓库级、未经 GitHub 全局复核、无 CVE；可作为 `official_upstream` 证据，
  不应作为首选评测靶子。RECON.md 已就地更正。这提示 `discovery_v3` 的
  `GitHubRepositoryAdvisory` 来源可能还包含其它仓库级 advisory，后续 triage 不应以「OSV 查无此条」
  直接判伪造。
- 快照：`scripts/build_snapshot_at.py` 在 `25685e6f…` 建立
  `snap_e0836fa1c53e240d`（tag v4.15.2，tree `d4529971…`，110 文件，Go 主导），
  提案 `runs/language/snap_e0836fa1c53e240d/snapshot_proposal.json`。
- 并行：axios 侦察已派出（2026-09 披露的一批 fetch adapter/NO_PROXY/header injection，
  候选 v1.19.0）；protobuf v3.25.4 独立选版审查进行中。echo dossier 构建代理已启动
  （`runs/verification/echo_CVE-2026-55677_v4152/`），尚未返回。
- protobuf 选版（2026-10-23）：独立选版审查
  `runs/selection_review_protobuf_v3254/verdict.json` 判 **accept**——annotated tag v3.25.4
  （tag 对象 `5493211695…`）peel 到 `e915ce24…`，tree `fafd76c8…`；archive/manifest sha256 与声明一致、
  2708 个 tar 条目逐字节比对 git blob 全部一致、无 `.git`；真实 `mvn -B install -Dmaven.test.skip=true`
  （JDK 17 + Maven 3.9.16 + 官方 protoc 25.4）exit 0、7/7 模块 BUILD SUCCESS；`build_ok=true`；
  OSV/GHSA/NVD/CNA 均判 3.25.4 受影响；审计导出剩余 advisory 0、与源导出同源。
  `apply_selection_review.py --apply` → **frozen**。审查同时指出 CLAIM 里
  `tree_file_count = exported + symlink + gitlink` 的写法不成立（2708 ≠ 2708+0+3，正确是
  2711 = 2708 blobs + 3 gitlinks），数据本身对账。该审查自述在查 `tree_file_count` 定义时一次全局
  grep 误触 selection_packets 与一份旧 review 的少量计数行（未涉及本快照验证内容），已记录。
- 计数：24 个评测目标（22 frozen + 2 rejected）；53 条目标正样本（44 B + 9 A）+ 29 条历史样本（B）；
  draft 校验 0 error。HANDOFF §0/§4 已按此更新。未声明 `PASS_KNOWN_SWEEP`，未发布。

## 2026-10-23 axios v1.19.0 与 echo v4.15.2 建立评测快照

### axios / CVE-2026-101907（grade A）
- 独立复核 `runs/independent/axios_CVE-2026-101907_v1190_round1/verdict.json`：v1.19.0 轻量 tag
  → `311fcc5c…`，tree `e235490f…`，456 文件；修复 `d19040b…`（#11141）是 v1.20.0 祖先、
  不是 v1.17.0/1.18.0/1.18.1/1.19.0 祖先；九项字段全 true。真实复现：fetch 适配器在
  `maxRedirects: 0` 下仍跟随 302 到内部路径并取回 `INTERNAL-SECRET`，v1.20.0 拒绝；
  http 适配器两个版本都拒绝。审查同时确认 v1.20.0 只处理 `=== 0`，`maxRedirects: 1`
  仍可跟进两跳（已作为 limitation 记录）。
- dossier 重建时修正 schema：`code_excerpt` 超 `locations.schema.json` 的 500 字符上限，
  在 `build_dossier.py` 里按整行截断并加 `…` 标记（不改变代码原文语义），重新生成
  `runs/verification/axios_CVE-2026-101907_v1190/dossier.json`。
- `migrate_snapshot_04c033042a3d52eb.py --apply`：新增快照 `snap_04c033042a3d52eb`
  （87→88 行）、selection 提议行、`repositories.evaluation_snapshot_id` 指向新快照、
  67 条 triage：confirmed_affected 1、confirmed_not_affected 44、duplicate 10、
  possible_affected 11、unknown 1（`adv3_efa99…` CVE-2025-54371 无缓存记录）。
  其余 11 条 2026-09 批次 CVE（101898–101909 去掉 101907）保持 possible_affected，不提升。
- `promote_verified_rows --apply` → 1 vulnerability + 1 location + 1 review + 128 evidence；
  `freeze_snapshots --only axios/axios`、`build_audit_exports --only axios/axios`
  （excluded 2、remaining advisory 0）完成。

### echo / CVE-2026-55677（round 2，grade A）
- round-1 复核拒绝沿用旧范围（`affected_ranges=false`/`fixed_release=false`）：2026-09-27
  vendor 将范围更正为 v4 `< 4.15.4`、v5 `< 5.2.1`，v4.15.3 只是部分修复。round-2 独立复核
  `runs/independent/echo_CVE-2026-55677_v4152_round2/verdict.json`：九项全 true，真实复现确认
  `/admin%2F…`、`/admin%2f…`、`/admin%252F…`、`/%61dmin/…`、`/public/%2E%2E/admin/…` 在 v4.15.2
  均 200 泄漏，v4.15.3 只剩后两种泄漏，v4.15.4 全部 404；三个 tag 均 `go build ./...` exit 0。
- **仓库级 advisory 范围更正**：此前认为 10 条 2026-09-27 仓库级 GHSA「没有任何机器可读范围」，
  实际 `api.github.com/repos/.../security-advisories` 的每条 advisory 都有 `vulnerabilities[]`，
  其中 `{package: github.com/labstack/echo/v4, vulnerable_version_range, patched_versions}` 可用；
  顶层 `vulnerable_version_range` 才是 null。迁移因此改为从
  `runs/discovery_v3/repo_advisories/labstack__echo.json` 读取并解析：
  `< 4.16.0` 等 9 条包含 v4.15.2 → possible_affected（仅表示要读代码，不是正样本）；
  GHSA-23wf-92cp-8pcj `< 4.15.2` → confirmed_not_affected（v4.15.2 本身即 patched 版本）。
  缺失范围时脚本直接 abort，不再静默降级为 unknown。
- `migrate_snapshot_e0836fa1c53e240d.py --apply`：新增快照 `snap_e0836fa1c53e240d`、
  selection 提议行、`repositories.evaluation_snapshot_id`、16 条 triage：
  confirmed_affected 1、confirmed_not_affected 4、duplicate 2、possible_affected 9、unknown 0。
  两条历史 CVE 用 `git merge-base --is-ancestor` 判为已修复；CVE-2026-25766 按包身份（v5-only）判否。
- `promote_verified_rows --apply` → 1 vulnerability + 1 location + 1 review + 200 evidence；
  `freeze_snapshots --only labstack/echo`、`build_audit_exports --only labstack/echo`
  （excluded 1、remaining advisory 0）完成。

### 数据整理与校验
- 新脚本 `runs/selection/supersede_proposal_rows.py`：把已有 evaluation target 的仓库的
  `snapshot_proposals` 行原样归档到 `runs/selection/superseded_snapshot_proposals.jsonl`
  并移出主表（沿用 ruby/rexml 先例）。本次归档 axios 23088740、echo 31504491，
  并顺带归档 sinatra 106995（其 v4.0.1 目标早已冻结但 proposal 行未清理，draft 校验此前一直报错）。
- 修正迁移脚本的两处证据 URL 重复（`https()` 去重）和 `repositories.evaluation_snapshot_id`
  漏写；对已写入的 axios 行做了同内容修正。
- draft 校验：0 error / 49 warning；88 快照（26 个评测目标）、84 漏洞/84 location/84 review、
  2333 evidence、55 条目标正样本、A 11 / B 73。
- 已派发 axios、echo 的独立选版审查（`runs/independent/selection_{axios,echo}_…`），
  尚未返回；在返回并 `apply_selection_review --apply` 之前，两条 selection 仍为 proposed。
- 未声明 `PASS_KNOWN_SWEEP`，未发布。

### 独立选版审查结果（2026-10-23）
- **axios v1.19.0 — accept**：审查人 `selrev-independent-deepseek-flash-axios-v1190`，
  审查记录 `runs/independent/selection_axios_v1190_2026-10-23/{review.jsonl,REVIEW.md}`。
  自测事实：archive sha256 `f6db8b2488222d3e30891fd8f5f4afd71cdb7f48d5e9d3bbf07a117d376b550f`
  （836609 B）与 manifest sha256 `3447a262…` 均与 packet 一致；456 个 tar 成员全为普通文件
  （454×0644、2×0755），无符号/硬链接/gitlink/目录、无 `.git`，路径/大小/模式/sha256 逐条对账，
  456 个 blob sha1 与 `git ls-tree -r v1.19.0` 一致；lightweight tag peel 到
  `311fcc5c`，`package.json` 1.19.0，npm registry gitHead 一致；Node v24.16.0 / npm 11.13.0
  全新目录 `npm ci`（648 包）exit 0、`npm run build` exit 0；OSV 范围 `>=1.17.0,<1.20.0`、
  NVD 仍 `Awaiting Analysis` 无 CPE 仅次要 CVSS 4.0；泄漏仅历史 CVE，CVE-2026-101907 出现 0 次。
  `review.jsonl` 已并入 `v031/reviews/selection_review_2026-10-23.jsonl`，
  `apply_selection_review.py --apply` → 该行 `selection_review_status=accepted`、`decision_status=frozen`；
  draft 校验仍 0 error。
- echo v4.15.2 的独立选版审查仍在进行，未提前冻结。

### echo 选版审查与范围 triage 落地（2026-10-23）
- **echo v4.15.2 — accept**：审查人 `independent-reviewer-deepseek-flash-2026-10-23`
  （`runs/independent/selection_echo_v4152_2026-10-23/`）。实测：archive sha256
  `2e30bb47…`（427496 B）与 manifest sha256 `22f78922…` 与 packet 一致；110 个 tar 成员全为普通文件，
  无符号/硬链接/gitlink、无 `.git`，路径集合与 `git ls-tree -r v4.15.2` 完全一致且逐文件 blob sha1 相符；
  lightweight tag 直接指向 `25685e6f`、tree `d4529971…`、`go.mod` 声明 v4 模块；go1.26.10
  `go build ./...` 与 `go vet ./...` 均 exit 0。Anchor 各源范围均覆盖 v4.15.2，并明确记录
  repo-scoped（`< 4.15.4`）领先、全部镜像滞后一版（`< 4.15.3`）的分歧方向。
  `apply_selection_review.py --apply` 后 `snap_e0836fa1c53e240d` **frozen**；draft 校验 0 error / 49 warning。
  至此 26 个评测目标中 24 frozen、2 rejected（hyper、Newtonsoft.Json）。
- **范围 triage 独立审计 → 有条件应用**：审计 `runs/triage_range_scope_2026-10-23/audit/AUDIT.md`
  结论 apply-after-fixes：NA 407 行可应用（先修 D3/D4/D5），OOS 161 行禁止应用（D1 schema 缺
  `evidence_urls`、D2 归属规则不成立）。已修 `triage_range_scope.py` D1/D2/D4/D5 与
  `apply_range_triage.py` D3 + `--only-proposal`；重生成 v1.1（NA 406 / possible 177 / OOS 42 /
  indeterminate 576），唯一丢失的 NA 是 D5 的 `disc2_cbbf645dec334f9187b6897a`（改判 possible）。
  `--only-proposal not_affected_range --apply` → 406 行 `confirmed_not_affected`（backup
  `runs/data_fixes/snapshot_candidate_triage_before_range_scope_2026-10-22T190955Z.jsonl`）；
  OOS 一条未写，CVE-2022-40281 保持 unknown。处置记录 `runs/triage_range_scope_2026-10-23/DISPOSITION.md`。
- **证据措辞更正**：发现 range-scope 与 axios 迁移共 449 行的 basis 写「快照从修复版本 descend，故修复已包含」，
  这是未被核验的祖先关系断言。`runs/data_fixes/correct_range_scope_basis_2026-10-23.py` 改为
  「版本序判定在受影响区间之外，修复提交的祖先关系未单独核验」（备份两次）。
- 当前 triage：1666 行 = unknown 795 / confirmed_not_affected 775 / confirmed_affected 64 /
  possible_affected 20 / duplicate 12；draft 0 error / 49 warning；51 个单测 OK。
- 仍未声明 `PASS_KNOWN_SWEEP`，未发布；OOS 归属规则待重做后再议。

### lodash 4.17.23 评测目标（2026-10-23）
- **独立验证 CVE-2026-4800 — confirmed_affected / grade B**：审查人
  `independent-reviewer-round1`（`runs/independent/lodash_CVE-2026-4800_v41723_round1/`）。
  自建 clone 与 PoC 复现：4.17.23 tag blob（sha256 `2dc5f1b8…`）上 `comma-pad`/`inherited-pad`/
  `undefined-value` 均置位 `__lodash_rce`，npm tarball 内 `lodash.js`（`71b4b7f5…`）同样复现；
  4.18.1（`f5465f55…`）上 own-key 变体抛 `Invalid \`imports\` option`，inherited-pad 因
  `assignWith` 只拷 own 属性而不抛错也不执行。fix `879aaa93` 不是 4.17.23 祖先、是 4.18.0/4.18.1
  祖先；CVSS 8.1 复算一致；`npm install --ignore-scripts` + `npm test` 复跑 6800/0、327/0。
- **首轮 verdict 有一项 false，未直接推广**：`fields_verified.affected_ranges=false`，因为公告下界
  `>=4.0.0` 不完整——3.10.1 同一 payload 复现（10727/10810，3.x 无 `reForbiddenIdentifierChars`）。
  处置：dossier 保留权威范围 `>=4.0.0, <4.18.1`，新增
  `affected_packages[0].range_completeness`（`published_lower_bound_incomplete`、`exhaustive:false`、
  3.10.1 证据、`first_affected_version:null`、不改写权威范围的政策声明），并按
  `data_quality_findings.md` 第 23 条 Django CVE-2020-7471 先例写入 discrepancies/limitations；
  同时并入 4.18.0 被 npm 标 bad release、inherited-pad 在 4.18.1 的行为、4.17.22 仅主包缺失、
  tarball `private` 被剥离、GitHub 页面 4.18.1 与 Advisory DB JSON 4.18.0 的分歧、三来源发布时间差异。
  round-2 delta 审查（`runs/independent/lodash_CVE-2026-4800_v41723_round2/CLAIM.md`）确认改后记录
  如实、置 `affected_ranges=true`；grade/verdict 未变。
- **迁移与推广**：`migrate_snapshot_033e9a6478460d9b.py --apply` 新增快照、selection 提议、
  `repositories.evaluation_snapshot_id`、10 条 triage（confirmed_affected 1、confirmed_not_affected 8、
  possible_affected 1、unknown 0）。8 条否定全部有 OSV 范围 + 修复提交/修复 tag 的祖先检查：
  2018-16487/2018-3721/2019-1010266/2019-10744/2020-28500/2020-8203/2021-23337 均为祖先；
  2025-13465 的修复版本就是 4.17.23，另有代码守卫与公告四个回归 payload 佐证。CVE-2026-2950
  范围覆盖快照且 4.18.0 不是祖先，recon 观察到的 array-wrapped 绕过未独立验证，保持
  possible_affected 不清零。`supersede_proposal_rows.py --apply`（23→22）。
  `promote_verified_rows --apply` → 1 vulnerability + 1 location + 1 review + 70 evidence + 1 status，
  0 warning。
- **冻结与审计**：`freeze_snapshots --only lodash/lodash`，159 文件、archive sha256
  `73bfcce0…`、无 `.git`/软链/gitlink；泄漏扫描只命中三个历史 CVE，目标 `CVE-2026-4800` 与
  `GHSA-r5fr-rjxr-66jc` 均未出现。`build_audit_exports`：158 文件、excluded 1（threat-model.md）、
  redacted 3（历史 GHSA-xxjr 注释）、`remaining_advisory_id_count=0`。
- **独立选版审查 — accept**：`runs/independent/selection_lodash_v41723_2026-10-23/`，审查人
  `independent-selection-reviewer-lodash-2026-10-23`。复核 tag object `fd6aaf94…` → `dec55b7a…`、
  archive/manifest 哈希与字节数、159 文件逐条 blob sha1/sha256/mode、audit diff 恰为声明集合、
  `npm ci --ignore-scripts` 与 `npm test` 全过、fix 祖先关系与 PoC。修正其 review.jsonl 的两处字段
  类型（`counts_reconcile` 布尔、anchor `url`）后 `apply_selection_review --apply` → frozen 1 / rejected 0；
  审查记录另存 `v031/reviews/selection_review_lodash_2026-10-23.jsonl` 并并入当日汇总。
- **当前 draft 校验**：0 error / 49 warning；90 快照、28 个评测目标（全部 frozen）、86 漏洞/86 location/
  86 review、57 条目标正样本、B 74 / A 12、triage 1713 行（仍 817 条 pending relevant）。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；lodash 的 CVE-2026-2950 仍未解决，`affected_ranges`
  的下界不完整性随行记录而非抹平。

## 2026-10-23 — jbeder/yaml-cpp：CVE-2019-6285 @ yaml-cpp-0.6.2 全流程闭环

- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-2/deepseek-flash/yaml-cpp-CVE-2019-6285-round1`
  （`runs/independent/yaml-cpp_CVE-2019-6285_v062_round1/`）。自建 clone 与静态库实测：
  0.6.2 上 `'['*20000/23100`、`'['*50000/200000`、`'{'*50000/200000` 均 SIGSEGV；
  vanilla 0.6.3 在 `'['*15000` 起同样 SIGSEGV；0.7.0 在每个深度均 `bad file`（DeepRecursion）。
  将 Debian `fix-unbounded-recursion-depth.patch` 应用到 vanilla 0.6.3 后重建也得到 `bad file`，
  证实 Debian `0.6.3-1` 是下游回移。9/9 `fields_verified=true`，位置 `src/singledocparser.cpp`
  `48-214`（HandleNode 48-134、HandleFlowSequence 183-214、递归调用 199，全树无 DepthGuard）。
- **复核措辞缺口回落 dossier**：新增 GHSA `GHSA-hg7f-3vww-rc69` 为别名（GitHub Advisory API 取证；
  OSV 对该 GHSA 返回 404，OSV alias 列表为空）；记录 NVD 另有 legacy CVSS 2.0 4.3；
  CVE.org 的 affected 对象存在但 vendor/product/version 均为 `n/a`，ADP 另有 seclists 引用；
  Debian 覆盖 12/13/14 与 sid；递归实为三层帧（HandleNode→HandleSequence→HandleFlowSequence）；
  「无上游 semver 范围」限定为上游。dossier 重建为 18 evidence / 9 discrepancies / 8 limitations，
  `sources/MANIFEST.sha256` 24 个文件（新增 GitHub advisory JSON）。
- **迁移与推广**：`migrate_snapshot_f0ec66ad5ca54002.py --apply` 新增快照、selection 提议、
  `repositories.evaluation_snapshot_id`、7 条 triage（confirmed_affected 1、possible_affected 6：
  2019-6292/2018-20573/2018-20574/2017-5950 共享递归族但无本 CVE 独立复核；2017-11692 与
  2026-75432 为 unresolved，前者公告称 0.5.3 及更早、后者 Debian 无 fixed 事件且未查
  0.6.2 的 PopIndent/PushIndentTo）。`supersede_proposal_rows.py --apply`（22→21）。
  `promote_verified_rows --apply` → 1 vulnerability + 1 location + 1 review + 66 evidence +
  1 snapshot_vulnerability_status，grade A、0 warning。
- **更正一条 triage 事实**：首次迁移为 CVE-2019-6292 写了「修复提交带该 CVE 的回归测试」，
  实际 `fix_4edff1f.diff` 只命名 CVE_2017_5950/2018_20573/2018_20574/2019_6285；
  已用 `repair_triage_6292_basis.py --apply` 仅改该行 basis，并同步修正迁移脚本。
- **冻结与审计**：`freeze_snapshots --only jbeder/yaml-cpp`，446 文件、tree `296d72b8…`、
  archive sha256 `84f3ff48…`、无 `.git`/软链/gitlink；泄漏扫描 CVE/GHSA 命中 0。
  `build_audit_exports`：无排除、无脱敏，audit 与 plain 逐字节相同，`remaining_advisory_id_count=0`。
- **独立选版审查 — accept**：`runs/independent/selection_yaml-cpp_v062_2026-10-23/`，审查人
  `independent-selection-reviewer-yamlcpp-2026-10-23`。复核轻量 tag `562aefc1`、archive/manifest
  哈希与字节数、446/446 逐条 blob sha1/sha256/mode、全树 grep（9 个模式均 0）、
  `cmake -DYAML_CPP_BUILD_TESTS=OFF -DYAML_CPP_BUILD_TOOLS=OFF -DCMAKE_BUILD_TYPE=Release`
  构建 exit 0（`libyaml-cpp.a` 948,954 字节）。release sanity 判 0.6.2 合法：0.6.3 虽 pre-fix
  但非公告受影响版本，0.7.0 已修复，不存在更新的受影响稳定版。归一化 anchors 的重复
  alias id（GHSA、DEBIAN- 前缀改为 `advisory_id`）后 `apply_selection_review --apply` →
  frozen 1 / rejected 0；审查记录 `v031/reviews/selection_review_yaml-cpp_2026-10-23.jsonl`
  并并入当日汇总。
- **当前 draft 校验**：0 error / 49 warning；91 快照、29 个评测目标、87 漏洞/87 location/
  87 review、`evaluation_selection=29`、B 74 / A 13、triage 1720 行（823 条 pending relevant）。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；yaml-cpp 的 6 条 possible_affected 仍未清零。

## 2026-10-23 — nestjs/nest：CVE-2026-102281 @ v11.2.3 全流程闭环

- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261023-01`
  （`runs/independent/nest_CVE-2026-102281_v1123_round1/`）。自行 clone v11.2.3（`2b36ee5f`）与
  v11.2.4（`d5046225`），`npm ci --legacy-peer-deps --ignore-scripts` 与 `tsc -b packages` 均 exit 0。
  RED：benign ping 正常，随后单条 100000 层嵌套 pattern 的文本帧（1,100,034 字节）使进程
  exit 1，stderr 为 `RangeError: Maximum call stack size exceeded` → `at JSON.stringify` →
  `ServerTCP.handleMessage (.../server-tcp.js:58:20)`。GREEN：同一帧返回
  `{"id":"2","status":"error","err":"There is no matching message handler..."}`，进程存活、
  后续 ping 仍返回 pong，SIGTERM 清理（143）。9/9 `fields_verified=true`，位置
  `packages/microservices/server/server-tcp.ts` `93-97`（关键 95-96 未加保护的
  `JSON.stringify(packet.pattern)`；`bindHandler` 84-86 的 async listener 无 rejection handler；
  RMQ 同类缺陷 `server-rmq.ts` 290-302，consumer promise 未 catch）。
- **复核记录的差异**：公告列出的 fix commit `aa97b514` 是 PR #17737 head，不属于任何 tag；
  真正随版本发布的是 11.x 回移 `e9dcd4c7`（首个包含版本 v11.2.4）与 master squash
  `e93c8e12`（首个包含版本 v12.0.2）；v12.0.1 未修复。NVD 仍为 `Awaiting Analysis`，
  CVSS/CWE 来自 GitHub secondary，与 GHSA/CVE.org 一致。
- **schema 归一（仅一处）**：复核人把范围写成 `start_line/end_line`，而
  `promote_verified_rows` 读 `location.line`。用 `normalize_verdict_location.py` 断言
  93/97 与文件一致后补 `location.line="93-97"`，改动记录在
  `runs/verification/nest_CVE-2026-102281_v1123/verdict_location_normalization.json`；
  verdict、grade、fields_verified 未改。
- **迁移与推广**：`migrate_snapshot_af37094ca730365c.py --apply` 新增快照
  `snap_af37094ca730365c`、selection 提议、`repositories.evaluation_snapshot_id`、1 条
  `confirmed_affected` triage（`source_code_review`）；其余 11 个 nest 候选无独立 verdict，
  保持未 triage、未删除。`supersede_proposal_rows.py --apply`（21→20）。
  `promote_verified_rows --apply` → 1 vulnerability + 1 location + 1 review + 84 evidence +
  1 snapshot_vulnerability_status，grade A、0 warning。
- **冻结与审计**：`freeze_snapshots --only nestjs/nest`，2141 文件、tree `a4bc2486…`、
  archive sha256 `b432e7ea…`、1,155,352 字节、无 `.git`/软链/gitlink；泄漏扫描 CVE/GHSA 命中 0。
  `build_audit_exports`：无排除、无脱敏，`source_export_id` 对齐、`remaining_advisory_id_count=0`。
- **独立选版审查 — accept**：审查人 `independent-selection-reviewer-nest-2026-10-23`
  （`runs/independent/selection_nest_v1123_2026-10-23/`，并入
  `v031/reviews/selection_review_nest_2026-10-23.jsonl`）。复核 annotated tag object
  `56ebf18f…` → commit `2b36ee5f`、commit 日期与 stable release、archive/manifest 哈希与字节数、
  **2141/2141** 条 manifest 逐条 mode/size/sha256/blob sha1 对照 `git ls-tree`（0 mismatch）、
  无 `.git`；`npm ci` 与 `tsc -b packages` 均 exit 0（/tmp 空目录解包）。anchor 经 GitHub
  Advisory、OSV、NVD、CVE.org 四源确认 11.2.3 在 `< 11.2.4` 范围内且修复提交均非祖先；
  导出树 `server-tcp.ts:96` 的未保护 stringify 仍在、`getPatternAsString` 不存在。
  `apply_selection_review --apply` → frozen 1 / rejected 0；`vulnerability_count_at_selection=1`。
- **当前 draft 校验**：0 error / 49 warning；92 快照、30 个评测目标、88 漏洞/88 location/88 review、
  59 条目标正样本、30 条 selection（28 frozen；23500865 与 3476845 两条为此前既有的
  rejected 提议，本轮未改动）、triage 1721 行（823 条 pending relevant）、proposals 20 行。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；nest 其余 11 个候选仍未 triage，两个既有
  rejected 目标仍未冻结。

## 2026-10-23 — leethomason/tinyxml2：CVE-2024-50615 @ 10.0.0 全流程闭环

- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261023-01`
  （`runs/independent/tinyxml2_CVE-2024-50615_v1000_round1/`）。自行取 10.0.0（`321ea883`）与
  10.1.0（`57eea48c`），用项目自带 CMake Debug 构建（定义 `TINYXML2_DEBUG` → 启用
  `TIXMLASSERT`）。RED：`<a>&#9999999999;</a>`、`<a>&#4294967295;</a>`、`<a>&#xFFFFFFFF;</a>`
  分别命中 `tinyxml2.cpp:550`（`digit == 0 || mult <= UINT_MAX / digit`）、`:558`
  （`mult <= UINT_MAX / 10`）、`:524`（`mult <= UINT_MAX / 16`），进程 exit 134；
  GREEN：10.1.0 Debug 对同一输入 exit 0。9/9 `fields_verified=true`，位置
  `tinyxml2.cpp` `519-558`（`XMLUtil::GetCharacterRef`），首个修复版本 10.1.0。
- **复核记录的差异**：GHSA 的机器可读 `vulnerabilities` 为空，受影响性依赖 OSV GIT 范围
  （last_affected 恰为 10.0.0 提交）、GHSA 文字 “through 10.0.0” 与 NVD CPE
  `versionEndIncluding 10.0.0`；CVE.org 的 vendor/product/version 与 CWE 均为 n/a，
  6.5/CWE-617 只来自 CISA-ADP；OSV 范围下界 `introduced 0` 过宽；Debian 12 仍无 fixed 事件；
  issue #997 引用的 master 行 545 在 10.0.0 tag 中实为 550。
- **还发现两处须按事实下修的描述**：(1) 第三个修复提交 `1fadaae0` 的
  `if (length == 0)` 比较的是 `int*` 指针而非解码长度，是死代码，有效防护仍是首个修复的
  `MAX_CODE_POINT = 0x10FFFF` 上界；已在 dossier 的 limitation/discrepancy 与 evidence note
  中改正，fix 归属结论不变。(2) Release 构建把 `TIXMLASSERT` 编译掉，同一输入不崩溃，
  只静默丢弃字符引用；因此这是**仅 Debug/断言构建可触发的 DoS**（与 CWE-617 一致），
  已在 limitation 与 triage basis 中写明。
- **schema 修正（不改结论）**：`promote_verified_rows` 的 schema 要求 `location.trace` 为帧数组、
  `critical_operation`/`entry_point` 带 `language`+`permalink`+`description`、证据
  `source_url` 必须是 https、`snapshot_evidence` 带 `sha256_of_observation`。据此在
  `build_dossier.py` 中补全调用链帧（`XMLDocument::Parse` 2475 → `XMLDocument::Parse()`
  2575 → `XMLText::ParseDeep` 1261 → `StrPair::ParseText` 332 → `GetCharacterRef`），把
  本地构建类证据的 `source_url` 指到对应 tag 的发布页（artifact 与验证方法不变），并补上
  snapshot proposal 的 sha256；dossier 重建后 promote 通过。
- **迁移与推广**：`migrate_snapshot_5b58f4c33f6103b5.py --apply` 新增快照
  `snap_5b58f4c33f6103b5`（tag 10.0.0，tree `d0705dfd…`，273 文件）、selection 提议、
  `repositories.evaluation_snapshot_id`、1 条 `confirmed_affected` triage；既有
  `snap_e44b1fc3e39243d8`（`8224e427` 的 historical_evidence）不是评测目标。其余两个候选
  `disc2_c259dbfa630800a8b2a454ac`（CVE-2024-50614）与 `disc2_f115f4f6a0bd547108c7d1e7`
  （CVE-2018-11210）无独立 verdict，保持未 triage、未删除。
  `supersede_proposal_rows.py --apply`（20→19）。`promote_verified_rows --apply` →
  1 vulnerability + 1 location + 1 review + **55 evidence** + 1 snapshot_vulnerability_status，
  grade A、0 warning。
- **冻结与审计**：`freeze_snapshots --only leethomason/tinyxml2`，273 文件、tree
  `d0705dfde7203c93642a251bbec61025c20f3967`、archive sha256 `8ee4dbb6…7dd4`、632,032 字节、
  无 `.git`/软链/gitlink；泄漏扫描 CVE/GHSA 命中 0。`build_audit_exports`：无排除、无脱敏，
  `source_export_id` 对齐、`remaining_advisory_id_count=0`。
- **独立选版审查 — accept**：审查人 `deepseek-flash-independent-selection-reviewer-2026-10-23`
  （`runs/independent/selection_tinyxml2_10.0.0_2026-10-23/`，并入
  `v031/reviews/selection_review_tinyxml2_2026-10-23.jsonl`）。复核发现 10.0.0 是**轻量 tag**
  （无 tag object，`object.type=commit`）、stable release（draft/prerelease 均 false，
  发布 2023-12-31）、commit 日期与 tree 一致；archive/manifest 哈希与字节数一致，
  audit 副本逐字节相同；273/273 条 manifest 逐条 mode/sha256/blob sha1 对照 `git ls-tree`
  （0 mismatch），无 `.git`；`cmake -DCMAKE_BUILD_TYPE=Debug` + build 均 exit 0，
  `xmltest` 508 pass / 0 fail；anchor 由 OSV、GHSA、NVD 三源确认 10.0.0 受影响。
  `apply_selection_review --apply` → frozen 1 / rejected 0；
  `vulnerability_count_at_selection=1`。
- **当前 draft 校验**：0 error / 49 warning；93 快照、31 条 selection（29 frozen；23500865
  与 3476845 两条为此前既有的 rejected 提议，本轮未改动）、89 漏洞/89 location/89 review、
  55 条目标正样本、triage 1722 行（823 条 pending relevant）、proposals 19 行。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；tinyxml2 其余 2 个候选仍未 triage，
  CVE-2024-50615 的触发条件仅限 Debug/断言构建这一点仍需在评测设计中使用时保留披露。

## 2026-10-23 — actix/actix-web：CVE-2026-73051 @ http-v3.12.0 全流程闭环

- **快照**：`snap_ca4042bda2431632`，tag `http-v3.12.0`（轻量 tag）→
  `a7a26f1ee0adfeabb5ee85a6eb2a62cff601a70b`，tree `329cd0a9…`，442 个受跟踪文件
  （418 regular + 24 symlink + 0 gitlink），全量扫描。
- **dossier**：`runs/verification/actix_CVE-2026-73051_http3120/`，12 条 sha256 钉住证据
  （NVD/CVE.org/OSV CVE/OSV GHSA/GHSA API/fix diff/commit 元数据/tag facts/代码摘录/
  PoC transcript/两个构建日志）。**定位更正**：初稿把调用点 `h1/decoder.rs:275-291`
  当作关键操作，独立复核定位到决策点 `197-212`（`MessageType::set_headers` 中
  `if chunked` 无条件选 chunked，CL 分支仅在 chunked=false 到达，两者从不比较），
  两处行区间无重叠会导致 promote 失败；重读 tag 源码后把 dossier 改为 197-212 并在
  `preparation_note` 记录“先写调用点、后改决策点”，没有让复核迁就采集稿。
- **schema 修正**：`field_evidence` 初版键名写成 `fix_commit`（单数），validator 要求
  `fix_commits`（复数），首轮 promote 因此产生 3 条错标 evidence（`…_fix_commit_05/06/07`）
  与旧 status 行；打印确认后仅删除这 3 条本轮错标行与对应 status，改键名后重新 promote，
  恢复 evidence 2951 / status 61。这是本轮唯一的直接数据编辑。
- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261023-02`
  （`runs/independent/actix_CVE-2026-73051_http3120_round1/`）。自行取 3.12.0/3.12.1，
  自建 Rust 探针驱动 `actix_http::h1::Codec`：RED 3.12.0 接受同时带 CL 与
  `TE: chunked` 的请求并把后续 `GET /admin` 解码为第二个请求（exit 10）；GREEN 3.12.1
  返回 `ParseError::Header`（exit 0）。9/9 `fields_verified=true`，location 197-212。
- **迁移与推广**：`migrate_snapshot_ca4042bda2431632.py`（先 dry-run）在 migration 中断言
  `http-v3.12.0` 不在 advisory-range proposal 的候选里（既有 proposal 只列 5 个旧 0.7.x
  候选）——独立正样本先于选版，不是回填；proposal 行归档为 superseded、不改写。
  `supersede_proposal_rows.py --apply`（19→18）；`promote_verified_rows --apply` →
  1 vulnerability/location/review + **55 evidence** + 1 status，grade A、0 warning。
- **冻结与审计**：`freeze_snapshots --only actix/actix-web` → 418 文件、24 symlink、
  archive sha256 `aad2fee2…`；`build_audit_exports` 无排除、无脱敏，
  `remaining_advisory_id_count=0`，`source_export_id` 对齐。审计只做 CVE-/GHSA- 词法匹配，
  CHANGES.md/deny.toml 里的无关 RUSTSEC ID 仍会保留；目标 advisory 未泄漏，但该词法范围
  应记录为工具限制。
- **独立选版审查 — accept**：审查人
  `deepseek-flash-independent-selection-reviewer-2026-10-23-02`
  （`runs/independent/selection_actix_http-v3.12.0_2026-10-23/`，并入
  `v031/reviews/selection_review_actix_2026-10-23.jsonl`）。tag 解析、archive/manifest
  哈希、442 条 manifest、无 `.git`、`cargo check -p actix-http` exit 0、GHSA anchor 全部通过；
  OSV CVE 的 GIT `fixed` 指向 3.12.0 发布提交被判定为错误、未作为 anchor。
  `apply_selection_review --apply` → frozen（`2026-10-23T00:34:40Z`），
  `vulnerability_count_at_selection=1`。
- **冻结后校验**：`validate_dataset.py . --draft` 0 error / 49 warning；50 repos、
  94 snapshots、32 个评测目标（30 frozen + 2 proposed：hyper、Newtonsoft 按
  documented_exception 保留）、90 vulns（61 评测 + 29 historical）、16 A + 74 B。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；actix 其余候选与 50 库的 `NEEDS_REVIEW`
  结论均未改变。

## 2026-10-23 — apache/tomcat：CVE-2025-24813 @ 9.0.98 推广与冻结（选版审查待做）

- **快照**：`snap_1afe89480f20c291`，tag `9.0.98`（轻量 tag）→
  `727a8467a37e17fef91e12a65db4d56862d36171`，tree `270a240f…`，4527 个受跟踪文件
  （0 symlink / 0 gitlink），全量扫描，51 条语言行。
- **dossier**：`runs/verification/tomcat_CVE-2025-24813_9.0.98/`，15 条 sha256 钉住证据。
  根因位置 `java/org/apache/catalina/servlets/DefaultServlet.java` 664-687（关键操作
  669-675）：`executePartialPut` 用 `path.replace('/', '.')` 从请求路径生成临时文件名
  （671），`new File(tempDir, convertedResourcePath)`（672）落在 context TEMPDIR，
  与基于文件的 session store 默认目录相同，且仅由 `deleteOnExit()`（675）清理。
  复现依赖三个配置前提（DefaultServlet `readonly=false`、文件型 session 持久化、
  webapp classpath 上有可序列化 gadget）；harness 使用写 marker 的 gadget 替身，
  只证明反序列化被触发，不证明真实利用链。
- **schema 修正**：首轮 promote 报 `vulnerabilities/CVE-2025-24813: 'ecosystem' is a
  required property`，根因是 dossier `fixed_releases` 缺 `ecosystem` / `release_url`
  （不是 `affected_packages`）；修正后重建 dossier，evidence 仍为 15 条。
- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261023-03`
  （`runs/independent/tomcat_CVE-2025-24813_9.0.98_round1/`）。自建 blobless clone 解析
  两个 tag，`merge-base --is-ancestor` 证明 fix `eb61aade` 不在 9.0.98、在 9.0.99；
  自行下载 archive.apache.org 源码包（校验 SHA-256）并用 Ant 1.10.15 / JDK 21 双版本构建，
  再用自写 harness 复现 partial PUT 临时文件与 FileStore 会话读取的碰撞：RED 9.0.98
  `PUT 201` → 残留 `<id>.session` → 触发 HTTP 500 且 gadget `readObject()` 写 marker；
  GREEN 9.0.99 同一 PUT 但无残留文件、HTTP 200、无 marker，并用 9.0.99 手工植入对照证明
  反序列化链本身仍在。9/9 `fields_verified=true`。
- **复核稿的一处格式归一**：verdict 初版 `location.line` 是散文（含调用点说明），
  promote 只接受 `N` / `N-M`，故请复核人把它归一为 `664-676`、把散文移入
  `critical_operation`；只改格式，未改结论。
- **verdict 记录的 6 处来源矛盾**：OSV 的 tag-commit 与代码 fix commit 不同；
  security-11.html 引用 main 分支 `0a668e0c`；GitHub API 403；NVD 同时有 9.8 与 10.0
  两条 v3.1 指标；邮件列表 URL 无正文；CPE 记法与 CNA 记法不一致。均按原样记录，未抹平。
- **迁移与推广**：`migrate_snapshot_1afe89480f20c291.py` 先 dry-run；断言 9.0.98 不在
  2026-10-22 advisory-range proposal 的候选里（该 proposal 只列 11.0.x），先有独立正样本
  再选版，proposal 行归档为 superseded、不改写。`--apply`（16:01:32Z）→
  `supersede_proposal_rows.py --apply` → `promote_verified_rows --apply`（16:02:00Z）
  新增 1 vulnerability / 1 location / 1 review / 51 evidence / 1 snapshot_vulnerability_status。
- **冻结与审计**：`freeze_snapshots --only apache/tomcat` → 4527 文件，archive sha256
  `4a2c6134…`；`build_audit_exports` 排除 1 个 `webapps/docs/changelog.xml`、
  脱敏 3 个文件（WebdavServlet/CVE-2007-5461、AsyncStateMachine/CVE-2018-8037、
  TesterSupport/CVE-2009-3555），`remaining_advisory_id_count=0`、`source_export_id` 对齐；
  audit archive sha256 `1a23c7e8…`。
- **选版审查包**：`build_selection_review_packets.py .` 重建 33 个包，含
  `2493904_apache__tomcat.json`。
- **独立选版审查 — accept**：审查人
  `deepseek-flash-independent-selection-reviewer-2026-10-24-01`
  （`v031/reviews/selection_review_tomcat_2026-10-24.jsonl`）。轻量 tag 解析一致、
  4527 条 manifest 路径/大小/sha256 与上游 blob 全匹配、无 `.git`、计数对账
  4527=4527+0+0；用 JDK 17 + Ant 1.10.15 真实构建 `BUILD SUCCESSFUL`（35s，
  `output/build/lib/catalina.jar`）；5 条 https anchor 全部 affected:true
  （OSV GHSA/CVE、NVD、security-9.html、fix patch）。audit 树 grep 目标 CVE/GHSA
  0 命中。`apply_selection_review.py --apply`（16:07:23Z）→ frozen 1 / rejected 0，
  `vulnerability_count_at_selection=1`。
- **审查人记录的非阻断 packet 偏差**：`build_facts` 仍写“未构建、工具链缺失”，实际
  环境已具备 JDK17+Ant（Tomcat 9 主构建是 Ant 而非 Maven）；`tag_commit_tree_sha`
  为 null 但可解析为 `270a240f…`；packet 未标注 audit 导出是脱敏派生版本。
- **冻结后校验**：`validate_dataset.py . --draft` 0 error / 49 warning；50 repos、
  95 snapshots、33 个评测目标、91 vulns（62 评测 + 29 historical）、62 条
  snapshot_vulnerability_status、17 A + 74 B、evidence 3003 行。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；tomcat 其余 pending 候选未 triage。

## 2026-10-23 — vercel/next.js：CVE-2025-29927 @ v14.2.24 推广、冻结与审计（选版审查待做）

- **快照**：`snap_ccfc92616d383a5b`，annotated tag `v14.2.24`（tag object
  `ba09179a…`）→ peel `756be15c4cfecb6fae1c69cae7cfaf336423b6cf`，tree
  `ca8277d2…`，16430 个受跟踪条目 = 16425 文件 + 5 symlink + 0 gitlink，全量扫描，
  120 条语言行。
- **dossier**：`runs/verification/nextjs_CVE-2025-29927_v14.2.24/`，14 条 sha256 钉住证据。
  根因位置 `packages/next/src/server/lib/server-ipc/utils.ts` 42-61：`INTERNAL_HEADERS`
  （42-51）不含 `x-middleware-subrequest`，`filterInternalHeaders`（53-61）只删清单内
  头部；sink 在 `sandbox.ts` 84-104（把该头的 token 数当递归证据，深度 ≥5 直接返回
  `x-middleware-next:1`，跳过 middleware）。入口 `router-server.ts` 149-160 的
  `filterInternalHeaders(req.headers)`（155）。
- **schema 修正**：`fixed_releases` 缺 `ecosystem` / `release_url`（与 tomcat 同类），
  首轮 schema 校验即失败；补齐后重建 dossier（`evidence=14 languages=120`），
  `vulnerabilities` / `locations` 两个 schema 均通过。证据仍为 14 条。
- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261024-01`
  （`runs/independent/nextjs_CVE-2025-29927_v14.2.24_round1/`）。自行解析两个 annotated
  tag（tag object `ba09179a…` / `351782b3…`），核对 npm `gitHead` 与 `dist` tarball
  哈希；确认 `52a078da` 只在 15.x、`5fd3ae8f` 是 14.x backport 且 parent 恰为
  `756be15c`，`merge-base --is-ancestor` 证明其不在 v14.2.24、在 v14.2.25。
  动态复现用已发布 npm 包（`next@14.2.24` / `14.2.25`，`gitHead` 与 tag commit 相同）：
  RED 攻击请求 200 且 body sha256 与已授权响应一致，4-token 对照 307；GREEN 攻击请求
  307；`red_exit=0` / `green_exit=1`。9/9 `fields_verified=true`，location
  `utils.ts:56-60`（与 dossier 42-61 重叠，未要求复核迁就）。
- **verdict 记录的 6 处来源矛盾**：11.x 下界（CVE.org/NVD 有 `>=11.1.4`，OSV/GHSA 无
  11.x 区间）；CVE.org 正文 “1.11.4” 与结构化字段 `11.1.4` 不一致；CWE 归属
  （CVE.org 仅 CWE-285、NVD Primary CWE-863、OSV 两者）；NVD 西班牙语描述漏 12/13 分支；
  两个 fix SHA 未标注所属 release line；引用列表不一致（CVE.org 不含 v14.2.25/v15.2.3
  release tag）。均原样记录，未抹平。
- **迁移与推广**：`migrate_snapshot_ccfc92616d383a5b.py` 先 dry-run；断言 v14.2.24 不在
  2026-10-22 advisory-range proposal 的 5 个 v16.3.x 候选里，先有独立正样本再选版；
  proposal 行归档为 superseded、不改写（17→16，archive 11 行）。`--apply`（16:20:38Z）→
  `promote_verified_rows --apply`（16:20:46Z）新增 1 vulnerability / 1 location / 1 review /
  53 evidence / 1 snapshot_vulnerability_status，grade A、0 warning。
- **冻结与审计**：`freeze_snapshots --only vercel/next.js` → 16425 文件 + 5 symlink，
  archive sha256 `86ef2c89…`（44,450,577 B）；`build_audit_exports` 未排除文件、
  脱敏 1 个 `.devcontainer/base.Dockerfile`（无关 CVE-2019-10131），
  `remaining_advisory_id_count=0`、`source_export_id` 对齐，audit archive sha256
  `84c98074…`。
- **选版审查包**：重建 34 个包，含 `70107786_vercel__next.js.json`。
- **独立选版审查 — accept**：审查人
  `deepseek-flash-independent-selection-reviewer-2026-10-24-02`
  （`v031/reviews/selection_review_nextjs_2026-10-24.jsonl`）。annotated tag 解析
  （tag object `ba09179a…` → peel `756be15c…`）、archive/manifest 哈希、
  16430 行 manifest 全量对账、无 `.git`、计数 16425+5+0、5 条 https anchor
  全部 affected:true（GHSA/OSV/NVD/fix commit/registry）、audit 树目标 ID 0 命中
  （唯一脱敏是无关的 CVE-2019-10131）。构建：`pnpm install --frozen-lockfile` 首次
  卡在 playwright-chromium 的 152.8 MiB 浏览器下载（20+ 分钟零 I/O，判定挂死），
  按指示杀掉后以 `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` 重装，再
  `pnpm --filter next build`（taskr release）**exit 0**，产出 6298 个 dist 文件 /
  103 MB；浏览器下载与编译包无关，已在 reviewer_notes 记录。
  `apply_selection_review --apply`（17:04:51Z）→ frozen 1 / rejected 0。
- **审查人记录的非阻断 packet 偏差**：`tag_commit_tree_sha` 为 null 但可解析；
  `build_facts` 的 `build_attempted=false` 与实际构建成功不符（且需要 corepack pnpm
  shim，并先构建 `@next/env`/`@next/font`）；packet 未标注 audit 包对主包报告的
  无关 CVE 做了脱敏。代码层面 `sandbox.ts` 在 14.2.24/14.2.25 相同，修复落在
  `utils.ts`/`router-server.ts`/`context.ts`，anchor 之间无矛盾。
- 未声明完成或 `PASS_KNOWN_SWEEP`，未发布；next.js 其余 85 个候选未 triage。

## 2026-10-23 — PHPMailer/PHPMailer：CVE-2020-13625 @ v6.1.5 推广、冻结与审计

- **快照**：`snap_b840904431f8a856`，annotated tag `v6.1.5`（tag object
  `68813f2825b9143fcc1f3839346db9b5815ffe3b`）→ peel
  `a8bf068f64a580302026e484ee29511f661b2ad3`，tree
  `b29cb78c8142053207dfa05db8ccb67a9e30ec8d`，117 个受跟踪条目 = 117 文件 + 0 symlink
  + 0 gitlink，PHP 一方代码占比 48.7%，全量扫描。
- **dossier**：`runs/verification/phpmailer_CVE-2020-13625_v615/`，16 条 sha256 钉住证据。
  位置 `src/PHPMailer.php` 3062-3108，critical_operation 3064-3108，函数
  `PHPMailer::attachAll`：`Content-Type: %s; name="%s"%s`（3070）与
  `Content-Disposition: %s; filename="%s"%s`（3094）直接把附件名插进引号，
  `secureHeader()` 只去 CR/LF，`encodeHeader()` 默认 `text` 不转义 `"`。修复
  `c2796cb1cb99d7717290b48c4e6f32cb6c60b7b3` 引入 `quotedString()` 做反斜杠转义并改成
  条件引用。
- **复现**：采集侧 `repro_attachment_name.php` 在 6.1.5 输出
  `filename="invoice.pdf"; filename="malware.exe"`（`INJECTION_SEQUENCE_COUNT=2`），
  6.1.6 输出 `invoice.pdf\"; filename=\"malware.exe`（=0）；并转写上游
  `testAttachmentNaming()` 六条断言（red 3 failed / green 0 failed）。另用 Python
  `email` 复算：同一头 `get_filename()` 取第一个、`get_param('filename')` 取最后一个，
  解析器相关。
- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261024-01`
  （`runs/independent/phpmailer_CVE-2020-13625_v615_round1/`）。自行解析 tag、clone
  两个版本、写独立 red/green（`repro_attachment_quote.php`），location 独立给出
  `3064-3100`（与 dossier 3064-3108 重叠），9/9 `fields_verified=true`。verdict 记录
  8 处来源差异：解析器相关的重复 filename 语义、inline/embedded 同样受影响、补丁顺带
  改了无条件引用策略、RFC822 3.4.1 引用不严谨、NVD “file type” 措辞、fix commit 名为
  merge 实为单亲 squash、GitHub REST `cwe_id=null` 与 OSV/NVD 的 CWE-116 不一致、OSV
  把 5.x/6.x 合成一个区间且 5.x 无修复版本。
- **迁移与推广**：`migrate_snapshot_b840904431f8a856.py` 先 dry-run（保留旧快照
  `snap_d2e05d198fd4c8b3`，不删候选）再 `--apply`（17:13:02Z）→ snapshots 96→97、
  selection 34→35；`supersede_proposal_rows --apply` 仅把 PHPMailer 的 proposal 行
  归档为 superseded（16→15，目标 v6.1.5 不在原 proposal 的 v6.1.8+ 候选内，先有独立
  正样本再选版）；`promote_verified_rows --apply`（17:13:08Z）新增 1 vulnerability /
  1 location / 1 review / 55 evidence / 1 snapshot_vulnerability_status，grade A、
  0 warning、0 conflict。
- **冻结与审计**：`freeze_snapshots --only PHPMailer/PHPMailer` → 117 文件，
  archive sha256 `b4570acc…`（225,393 B），manifest `1e77410b…`，
  `probe_build=toolchain_available`（php/composer）。`build_audit_exports` 排除
  `README.md` / `SECURITY.md` / `changelog.md`（历史 CVE 列表），在
  `src/PHPMailer.php` 脱敏 7 处 CVE-2016-10033/10045，剩 114 文件，
  `remaining_advisory_id_count=0`，audit sha256 `aa017bf5…`。
- **独立选版审查 — accept**：审查人
  `deepseek-flash-independent-selection-reviewer-2026-10-24-01`
  （`v031/reviews/selection_review_phpmailer_2026-10-24.jsonl`）。复核 annotated tag
  peel、archive/manifest 哈希、117 行 manifest 全量对账、117 个 blob 与上游树逐一
  一致、无 `.git`、计数 117+0+0；构建因 phpunit dev 依赖被安全公告阻断，改用
  `composer validate` + `dump-autoload` + 71/71 `php -l` + 加载冒烟，并自行复现了
  未转义引号行为；5 条 https anchor（OSV GHSA/CVE、OSV 精确版本 query、NVD、GHSA 页）
  全部 affected:true，6.1.6 的 query 不再返回该公告；audit 树原始字节扫描
  CVE/GHSA 0 命中。`apply_selection_review --apply`（17:26:10Z）→ frozen 1 /
  rejected 0 / skipped 34。
- **审查人记录的非阻断 packet 偏差**：`build_facts` 只记录工具链存在、未实际构建；
  `tag_facts.tag_commit_tree_sha` 为 null（实测 tree 正确）；GitHub advisories REST
  匿名 403，改用公开 GHSA HTML + OSV/NVD。
- **数据状态**：validator draft 0 error，evaluation_snapshots 35，vulnerabilities 93
  （A19/B74），evidence 3111；PHPMailer 仍余 17 个未 triage 候选。未声明完成或
  `PASS_KNOWN_SWEEP`，未发布。

## 2026-10-23 — tokio-rs/tokio：CVE-2021-38191 @ tokio-1.8.0 推广、冻结与审计

- **证据先行选版**：先在 `tokio-1.8.0`（commit `677107d8d9278265798c5efdc75374a25b41a4b8`，
  tree `61e693d2…`，576 文件，lightweight tag）确认正样本，再建快照
  `snap_bb1aca4519b1aae6`（`runs/language/snap_bb1aca4519b1aae6/snapshot_proposal.json`）。
  既有 `data/snapshot_proposals.jsonl` 的 tokio 行只列 1.43/1.44 的
  GHSA-rr8g-9fpq-6wmg 候选，**不含 1.8.0**；1.8.0 是先有独立正样本后才选定的，未从候选反推。
  旧快照 `snap_f24ebe150d320916`（commit `cffdc760…`，无 tag、非评估目标）保留为历史清点。
- **采集 dossier**（`runs/verification/tokio_CVE-2021-38191_v180/dossier.json`）：17 条证据、
  18 行语言；根因 `tokio/src/runtime/task/join.rs` 193-197（`JoinHandle::abort` 调
  `raw.shutdown()`，在调用线程 drop future；LocalSet 的 !Send 状态必须留在宿主线程）。
  入口 `tokio/src/task/local.rs` 386-396（`spawn_local` 返回的 JoinHandle 是 Send）。
  fix commit `e3851089207f6617dfcc0c7a73013eb819a0bfe0`（PR #3934，修 issue #3929，
  1.5.1 线上提交后 forward-port），在 1.8.0 **不是**祖先、在 1.8.1 是祖先；1.8.1 的
  tag commit 是 `e0c527f3…`，不是 fix commit 本身。
- **采集方 red/green**：自写 harness，LocalSet 中排队未 poll 的 future 持有
  Send+!Sync DropGuard，从另一线程 `abort()`；因 tokio 任务 harness 用 `catch_unwind`
  吞掉 Drop panic，改用 panic hook + AtomicBool 观测。1.8.0 → `WRONG_THREAD_DROP`
  （exit 1）；1.8.1 → `OK`（exit 0）。两 tag 各自 `cargo build` 干净通过。
- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-20261024-01`
  （`runs/independent/tokio_CVE-2021-38191_v180_round1/`）。自行解析 tag、path-dep
  检出两 tag、自写 DropGuard 线程归属观测，1.8.0 exit 42/1.8.1 exit 0，各 3/3 一致；
  9/9 `fields_verified=true`，location 独立给出 `193-197`（与 dossier 一致）。
  记录 5 处来源差异：NVD 文字 “before 1.8.1” 与不连续 CPE、NVD 缺 CWE-366、
  fix commit 就是 1.5.1 tag commit、RUSTSEC functions 与版本列表互补、
  GitHub advisory 网页 404（改用 advisory-database 原始 JSON，REST 限流）。
- **迁移与推广**：`migrate_snapshot_bb1aca4519b1aae6.py` 先 dry-run（保留旧快照、不删候选）
  再 `--apply`（17:34:05Z）→ snapshots 97→98、selection 35→36、triage 1726→1727；
  `supersede_proposal_rows --apply` 归档 tokio 的 proposal 行（15→14）；
  `promote_verified_rows --apply`（17:34:16Z）新增 1 vulnerability / 1 location /
  1 review / 56 evidence / 1 snapshot_vulnerability_status，grade A、0 warning、0 conflict。
  其余 5 个 tokio 候选保持 pending，未清除。
- **冻结与审计**：`freeze_snapshots --only tokio-rs/tokio` → 576 文件，
  archive sha256 `f7366f218c7afe7f183830e4411ee050028d04c843f9a235be8a875003891484`
  （652,762 B），manifest `5152472ec0…`，`probe_build=toolchain_available`（rust/cargo）。
  1.8.0 的 CHANGELOG 尚无 CVE/GHSA 标识符，故 `build_audit_exports` 排除 0、脱敏 0，
  audit 树 576 文件、`remaining_advisory_id_count=0`，audit 包与主导出逐字节相同
  （sha256 `f7366f21…`），audit_export_id `aud_bb1aca4519b1aae6`。
- **独立选版审查**：第一轮审查人
  `deepseek-flash-independent-selection-reviewer-2026-10-24-02` 判 **reject**，唯一失败项是
  BUILD：rustc 1.98.1 下 `cargo build -p tokio` 因
  `tokio/src/time/clock.rs:133` 的 `unused_must_use` 被 crate 级 `#![deny]` 升级为错误
  （exit 101）。该 lint 晚于 2021 年的源码。安装 rustc/cargo 1.53.0（2021-06-17）后，
  审查人**自行**从全新解包重跑 `rustup run 1.53.0 cargo build -p tokio`，exit 0，
  产物 `target/debug/libtokio.rlib`，清 target 复跑仍 0；同时透明记录 1.98.1 +
  `--cap-lints=allow` 也可编译。据此改写为 **accept**（build_ok=true），其余检查测量
  值未动：tag/commit/tree 一致，archive/manifest 哈希一致，576 行 manifest 0 mismatch、
  0 extra，576+0+0=576，上游 shallow clone 576/576 blob 一致，锚点 OSV/NVD/RustSec/GHSA
  均确认 1.8.0 受影响、1.8.1 修复，主导出 0 advisory id，audit 残留 0。
  reviewer_notes 建议 harness 固定 Rust 1.53.x 或使用 lint-cap 参数。
- **选版应用**：`apply_selection_review --apply`（17:40:01Z）→ frozen 1 / rejected 0 /
  skipped 35；`snap_bb1aca4519b1aae6` 记 `selection_review_status=accepted`、
  `frozen_at=2026-10-23T17:40:01Z`、`vulnerability_count_at_selection=1`、
  4 条 https approval 锚点、`snapshot_export_id=exp_snap_bb1aca4519b1aae6`、
  `audit_export_id=aud_bb1aca4519b1aae6`。
- **数据状态**：validator draft 0 error；evaluation_target snapshots 36，frozen selections
  34（hyper、Newtonsoft 仍为 documented_exception 的 proposed），vulnerabilities 94
  （A20/B74），evidence 3167；tokio 另有 5 条候选保持 `pending_location`（4）/
  `pending_version`（1），未删除、未判不存在。未声明完成或
  `PASS_KNOWN_SWEEP`，未发布。

## 2026-10-23 — aaubry/YamlDotNet：CVE-2018-1000210 @ v4.3.2 推广、冻结与审计

- **证据先行选版**：先确认 `v4.3.2`（commit `8f20a18bb8a8c026bef7ce5ad66e7d8e198426df`，
  tree `69f3e12bf80bebe64eaf5f70ecfbe3cb49096bf3`，319 条目 = 318 blob + 1 gitlink，
  lightweight tag）为正样本，再建快照 `snap_c9bc21e647038615`；`snapshot_proposals.jsonl`
  的候选列表包含 v4.3.2，迁移脚本显式断言其属于候选，未从「最新版」反推。
  旧快照 `snap_4d89919118140399`（commit `4f7e6e34…`，无 tag、非评估目标）保留。
- **复现**：采集方 red/green 用固定 `netstandard1.3` 构建的 4.3.2 / 5.0.0 DLL 各跑一次，
  文档 `!System.Text.StringBuilder {}`；4.3.2 反序列化为 `System.Text.StringBuilder`
  （RED_EXIT=1），5.0.0 抛 `Encountered an unresolved tag`（GREEN_EXIT=0）。
  踩坑记录：YAML shorthand tag 不允许空格/逗号，早先的 `!ReproEvil.Evil, repro`
  在 tag 层就非法；out500 目录曾复用旧 DLL 造成假绿，改为全新目录并按 sha256 确认引用
  的 `YamlDotNet.dll` 后重跑。
- **独立漏洞复核 — confirmed_affected / grade A**：审查人
  `independent-reviewer-deepseek-flash-ydn-8f20a18-r1`
  （`runs/independent/yamldotnet_CVE-2018-1000210_v432_round1/`）。自行 `git ls-remote`
  解析 tag、构建 4.3.2 / 5.0.0 / `c8df563` / `0ce8ac1` 四棵树，自写 Program 链接各 tag
  的 netstandard1.3 DLL；red exit 42（canary 构造函数被调用、返回
  `YamlTagCanary.DangerousCanary`），green exit 0（解析阶段拒绝），并测出
  **`c8df563` 单独仍是 42，`0ce8ac1` 才是决定性修复**。9/9 `fields_verified=true`，
  location 独立给出 `TypeNameInTagNodeTypeResolver.cs:35-36`（与 dossier 的 31-36 重叠）。
  记录 11 条 discrepancy，主要包括：NVD/OSV 挂 CWE-639（实际机制 CWE-502）、
  5.0.0 仍保留 `Type.GetType` 行只是不再默认注册、NVD 引用的 `f96b7cc` 是 sink
  而非 fix、CVSS v3.0（AV:L/UI:R）与 v2.0（AV:N）自相矛盾、NuGet 元数据
  `listed=false` 无法佐证发布时间。
- **迁移与推广**：`migrate_snapshot_c9bc21e647038615.py` 先 dry-run 再 `--apply`
  （17:42:46Z）→ snapshots 98→99、selection 36→37、triage 1727→1728；
  `supersede_proposal_rows --apply` 归档 proposal 行（14→13）；
  `promote_verified_rows --apply`（17:43:35Z）新增 1 vulnerability / 1 location /
  1 review / 38 evidence / 1 snapshot_vulnerability_status，grade A、0 warning、0 conflict。
  迁移前修正两处 gate/模式问题（见下）。
- **模式适配（未改判定标准）**：① `code_excerpts.txt` 的溯源探针原写
  `git show 0ce8ac1`，与实际段落标题不符，改为校验真实存在的
  `===== fix commit 0ce8ac1: … =====` 两段；② dossier 的 `snapshot_evidence` 缺
  `source_url` / `verification_method`，已在 `build_dossier.py` 补齐并重建，
  与旧 dossier 相比仅新增这两个键；③ CVSS 3.0 不在 schema 允许的 3.1/4.0 内，
  按 yaml-cpp CVE-2019-6285 的既有先例做记号归一化：保留
  `published_version/score/vector`，`source` 明写「同一组 base metrics 的 3.1 重述，
  不是独立发布」。
- **冻结与审计**：`freeze_snapshots --only aaubry/YamlDotNet` → 318 blobs + 1 gitlink，
  archive sha256 `92b967d06966b497e1006a68e4018213ffebf5de2b1b389f08a51dbc9a91754c`
  （168,581 B），manifest `28c9da01832da5e733a92a977c3d52d9ad964249293bd2277c7e8d6a9cb382de`。
  4.3.2 树内无 CVE/GHSA 标识符，audit 包与主导出逐字节相同（sha256 同），
  318 文件、排除 0、脱敏 0、`remaining_advisory_id_count=0`，audit_export_id
  `aud_c9bc21e647038615`。
- **独立选版审查 — accept**：审查人
  `deepseek-flash-independent-selection-reviewer-yamldotnet-2026-10-24-01`
  （隔离运行，只读 packet + exports + 公开源）。独立验证：lightweight tag 解析一致；
  318 行 manifest 全通过、0 mismatch / 0 extra、318+0+1=319 对账；`git hash-object`
  与上游 blob 全等；无 `.git`；OSV/NVD/GitHub advisory 三方确认 4.3.2 受影响、
  5.0.0 修复；主树 317 个文本文件 CVE/GHSA 命中 0；用 .NET SDK 8.0.426
  `-p:TargetFrameworks=netstandard1.3` 全新解包构建 exit 0，产出 `YamlDotNet.dll`。
  审查人记录的非阻断偏差：packet 的 `build_facts` 报 `no_build_system_detected`
  是 freeze 探针只认 `global.json`、不认 `*.csproj` 造成的误报（本次未改探针，
  以免重写既有 36 行冻结元数据）。
- **选版应用**：`apply_selection_review --apply`（17:45:42Z）→ frozen 1 / rejected 0 /
  skipped 36；`snap_c9bc21e647038615` 记 `accepted`、`frozen_at=2026-10-23T17:45:42Z`、
  `vulnerability_count_at_selection=1`、3 条 https approval 锚点、
  `snapshot_export_id=exp_snap_c9bc21e647038615`、`audit_export_id=aud_c9bc21e647038615`。
- **数据状态**：validator draft 0 error；evaluation_target snapshots 37，frozen selections
  35（hyper、Newtonsoft 仍为 documented_exception 的 proposed），vulnerabilities 95
  （A21/B74），evidence 3205；YamlDotNet 另有 1 条候选保持 `pending_location`。
  未声明完成或 `PASS_KNOWN_SWEEP`，未发布。

## 2026-10-23 — SixLabors/ImageSharp：CVE-2025-27598 @ v3.1.6 推广、冻结与审计、选版审查闭环
- **推广**：独立漏洞判定 `confirmed_affected`（grade A，审查人
  `deepseek-flash-independent-verdict-reviewer-imagesharp-2026-10-24-01`），location
  `src/ImageSharp/Formats/Gif/LzwDecoder.cs:207-211`（`DecodePixelRow` 的 `pixelCount`
  循环未按 `width` 截断），`location_kind=memory`；red `313a7e8d`（AccessViolation/
  栈溢出，exit 134）、green `520e597c`（3.1.7，正常解码，exit 0）。
  `promote_verified_rows --apply` → 1 vulnerability / 1 location / 1 review /
  44 evidence / 1 status。
- **冻结与审计**：`freeze_snapshots --only SixLabors/ImageSharp` → 3952 blobs + 1
  未落地 gitlink = 3953 条目，archive sha256 `01d16929…500914d8`（11,068,510 B），
  manifest `abc3fb68…5abbc53f`。audit 包与主导出**逐字节相同**（排除 0、脱敏 0），
  主树 3952 文件 CVE/GHSA 命中 0，`remaining_advisory_id_count=0`，
  audit_export_id `aud_da570194ab16247d`。
- **独立选版审查 — accept**：审查人
  `deepseek-flash-independent-selection-reviewer-imagesharp-2026-10-24-01`
  （隔离运行）。独立验证：`v3.1.6` 是 lightweight tag 解析到同一 commit；浅克隆树
  `59e909da`、3953 条目与 packet 一致；NuGet 3.1.6 存在且 nuspec commit 相符；
  OSV / NVD（CPE 3.0.0–<3.1.7、CVSS 3.1 7.5、CWE-787）/ GitHub advisory 三方锚点；
  用 .NET SDK 8.0.426 全新构建并以 `issue_2859_A/B.gif` 复现（3.1.6 exit 134，
  3.1.7 干净解码）。
- **审查人记录的非阻断偏差**（未改既有行，仅记录）：① packet 的 `build_facts` 写
  `no_build_system_detected` 不对——导出树缺 `shared-infrastructure` 子模块，
  原样构建报 MSB4019；按 pinned commit `353b9afe` 补齐子模块后 exit 0；② audit 导出
  是主导出的逐字节拷贝，manifest 无 excluded/redacted 字段，脱敏路径本次未被执行；
  ③ GHSA/CVE 引用的 PR 2890 实为 `release/2.1.x` 回移，3.x 的修复经 cherry-pick
  "Fix #2859" 进入 3.1.7。
- **选版应用**：`apply_selection_review --apply`（18:06:58Z）→ frozen 1 / rejected 0 /
  skipped 38；`snap_da570194ab16247d` 记 `decision_status=frozen`、
  `selection_review_status=accepted`、`reviewed_by` 如上、`snapshot_export_id` /
  `audit_export_id` 已填。validator draft 结构 PASS、0 error。
- **数据状态**：snapshots 101、evaluation_selection 39、audit exports 39、proposals 11。
  未声明完成或 `PASS_KNOWN_SWEEP`，未发布。

## 2026-10-23 — rails/rails：CVE-2026-33195 @ v8.0.4 正向样本、迁移、推广、冻结、审计与选版（已冻结）
- **正向样本**：tag `v8.0.4` 为 annotated + PGP 签名 tag object `02d550de…`，peel 到
  `624fe3cd…`（tree `5ec68c2f…`，4770 条目）；修复 tag `v8.0.4.1` → `a79efed9…`
  （tree `43450a67…`）；8-0-stable 修复 commit `a290c8a1`
  "Prevent path traversal in ActiveStorage DiskService"，经 `merge-base --is-ancestor`
  确认是 v8.0.4.1 的祖先且是 v8.0.4 的后代。收集方探针（activestorage 8.0.4 gem）在 root
  外读 canary，exit 3；8.0.4.1 抛 `ActiveStorage::InvalidKeyError`，exit 0。
- **快照**：`build_snapshot_at.py` → `snap_2ac31ec18ac30934`，4770 tracked
  entries、85 language rows。
- **独立判定 — confirmed_affected / grade A**：审查人
  `indep-reviewer-rails-CVE-2026-33195-20261024`（隔离运行，未读 dossier/data），
  自写探针（root=basedir/a/b/storage，秘密文件 basedir/target.txt，key
  `../../target.txt`）red exit 0 / green exit 1，两者输出可重复；声明 gem 内
  `disk_service.rb` sha256 与 tag 树文件逐字节相同。记录的 discrepancies：三源
  CVSS 分歧（9.8 / 8.0 / 8.1）、动态复现用 gem 而非完整应用、探针只触发 dot-segment
  检查、v8.0.4.1 另含相邻的 glob 注入修复、PGP 未做密钥环校验、GitHub REST 限流。
- **迁移**：`migrate_snapshot_2ac31ec18ac30934.py --apply`（18:09:56Z）→ 新增
  snapshot 行（evaluation_target=true、channel=release_tags）、1 条 proposed selection
  （selected_by=Claude collecting agent (deepseek-flash)）、候选
  `disc2_bb4262ddf377291d0b2ff08a` 置 verified、1 条 confirmed_affected triage 行、
  repository.evaluation_snapshot_id 指向新快照；旧历史快照 `snap_4e01b34117977bd4`
  （commit `0f19d01a…`，无 tag）保留不动。`supersede_proposal_rows --apply`：proposals
  11 → 10（rails 的 v8.1.3+ 建议行归档）。
- **推广**：`promote_verified_rows --apply`（18:10:20Z）→ 1 vulnerability / 1 location
  （`activestorage/lib/active_storage/service/disk_service.rb:101-103`，
  location_kind=dataflow）/ 1 review / 47 evidence / 1 status。
- **冻结与审计**：4770 blobs、4769 文件 + 1 symlink，archive `ebc86d96…`
  （11,832,177 B），manifest `bca39a9a…`；主树泄漏评估
  `advisory_identifiers_present`（6 个历史 CVE，目标 CVE 不在其中）。audit 导出
  4764 文件、排除 5、脱敏 0，`remaining_advisory_id_count=0`，archive
  `fb611175…`、manifest `dd82eb16…`。
- **数据状态**：snapshots 102、proposals 10、evaluation_selection 40、audit exports 40；
  选版审查已启动（隔离 agent），accept 前不声明完成。
- **选版审查 — accept**：隔离审查人 `indep-reviewer-rails-...`（独立会话，只读
  packet 与导出件）自建 Ruby 3.2.3 / gem 3.4.20 环境，从导出树重建 7 个 framework
  gem 并 `require "active_storage"`、实例化 `DiskService`（加载文件 sha256 与导出
  一致，证明构建用的是快照代码）；4770 条目逐条与 `git ls-tree -r` 比对 path/mode/
  blob 全部一致，并由导出树重建出 root tree `5ec68c2f…`；tar 无 `.git`、无路径穿越；
  audit 导出恰为主导出减去 5 个文件（3 个 CHANGELOG + `4_1_release_notes.md` +
  `security.md`），`remaining_advisory_id_count=0`。审查记录 5 条非阻断
  discrepancies（packet 的 `tag_facts` 记的是 peel 后 commit、历史 CVE 泄漏判定口径、
  `published_at` 为 null、`build_facts.build_attempted=false` 及 `git ls-files` 提醒
  不适用、安全文件清单偏多）。`apply_selection_review.py --apply` → frozen 1 /
  rejected 0 / skipped 39；`validate_dataset.py --draft` STRUCTURAL VALIDATION PASSED。
  未声明完成或 release。

## 2026-10-23 — angular/angular：CVE-2025-66035 @ 19.2.15 正向样本、迁移、推广、冻结与审计（选版审查进行中）
- **目标选择（证据优先）**：先从 npm 已发布产物上取得正向样本，再选 tag。tag
  `19.2.15` 为 lightweight tag，指向 `fbe9b9f9c1b2e27ae9124632e06f68ea4b415072`
  （tree `6b230c1f…`，8963 条目，commit 主题 “release: cut the v19.2.15 release”）。
  仓库既有历史快照 `snap_55025ac2aa21eca5`（commit `d0b33ad2…`，无 tag）仅为
  历史清单，未在该 SHA 证明漏洞，故不作评估目标。
- **npm 溯源**：`@angular/common@19.2.15` 的 gitHead 为 `1d0bf9c8…`（与 tag
  commit 不同对象，但 tree 同为 `6b230c1f…`，内容一致）；19.2.16 的 gitHead
  `68a0f00b…` 的 tree 等于 `6aaf2dc4…`（19.2.16 tag tree）。
- **红/绿复现**：Node 24 + TestBed（server platform）+ HttpTestingController
  桩后端，真实走 `@angular/common/http` 的 xsrf interceptor 链。探针先发同源
  control POST（两版都带 `X-XSRF-TOKEN`），再发 `//evil.example/steal`：
  19.2.15 仍带 token → exit 3 / RESULT=VULNERABLE；19.2.16 不带 token →
  exit 0 / RESULT=BLOCKED。
- **源码事实**：`packages/common/http/src/xsrf.ts:98-99` 只判断
  `lcUrl.startsWith('http://') || lcUrl.startsWith('https://')`；19.2.x 修复
  commit `05fe6686`（“fix(http): prevent XSRF token leakage to protocol-relative
  URLs”）改为 `ABSOLUTE_URL_REGEX = /^(?:https?:)?\/\//i`，且是 19.2.16 的
  祖先、19.2.15 的后代。
- **通报事实**：OSV npm `@angular/common` 区间 0→19.2.16、20.0.0-next.0→20.3.14、
  21.0.0-next.0→21.0.1；CWE-201/CWE-359；CVSS 4.0 7.7 HIGH。NVD 记录**没有**
  CPE configurations、只有 secondary 的 CVSS 4.0（已记入 dossier discrepancies）。
- **状态**：快照 `snap_3e3c1cd4c21a2a27` 已建（117 language rows），dossier 已写
  （10 条证据，location `xsrf.ts:98-99`，location_kind=logic）；独立漏洞判定
  agent 已启动，未在判定返回前迁移或声明任何结论。
- **独立判定 — confirmed_affected / grade A**：审查人
  `independent-reviewer-r1-angular-cve-2025-66035`（隔离会话，自建 npm 安装
  `/tmp/ngred152`、`/tmp/nggreen1616`，未读 dossier/data）。结论依据：19.2.15
  轻量 tag 的 `xsrf.ts:98-99` 只匹配 `http://`/`https://`；19.2.16 的父提交正是
  `05fe6686`。自写探针走真实 `HttpClient → HttpInterceptorHandler →
  xsrfInterceptorFn` 链（仅桩掉 HttpBackend 与 DOCUMENT）：同源 POST、绝对 URL、
  GET 三组控制组在两版都符合预期，`//attacker.example/collect` 在 19.2.15 带
  token、19.2.16 不带，两次运行均 exit 0（0=符合该模式预期且控制通过）。额外
  记录：NVD 仍为 `Deferred` 且混入 Siemens 范围、OSV 把 `eaa68c4` 误当 21.0.1
  修复点（真实 21.0.1 tag 为 `47a7396`）、`/\attacker.example` 在 19.2.16 仍
  带 token 的越界观察（不在 advisory 描述的模式内、未做浏览器验证）。
- **迁移与推广**：`migrate_snapshot_3e3c1cd4c21a2a27.py --apply`（18:18Z）→ 新
  snapshot 行（evaluation_target=true、channel=release_tags）、proposed selection、
  候选 `disc2_2e5dfad8b2617b832e98268e` verified、1 条 confirmed_affected triage、
  repository.evaluation_snapshot_id 指向新快照；旧历史快照 `snap_55025ac2aa21eca5`
  （`d0b33ad2…`，无 tag）保留。`supersede_proposal_rows --apply` 归档 angular 的
  其他版本建议行。`promote_verified_rows --apply`（18:18:45Z）→ 1 vulnerability /
  1 location / 1 review / 40 evidence / 1 status，无 warning。
- **冻结与审计**：`freeze_snapshots --only angular/angular` → 8963 blobs、8963
  文件（无 symlink/gitlink），archive `374734c3…`（51,116,289 B），manifest
  `a1ecc67f…`；泄漏评估 `no_advisory_identifiers_detected_in_scanned_files`。
  audit 导出 8963 文件、排除 0、脱敏 0，`remaining_advisory_id_count=0`，archive
  与主导出同 sha256。选版审查 packet 已重建，隔离审查已启动，accept 前不声明完成。

## 2026-10-23 — dotnet/aspnetcore：CVE-2025-24070 @ v8.0.13（选版审查进行中）
- **目标选择（证据优先）**：先在 Microsoft 官方发布的 ASP.NET Core 8.0.13 / 8.0.14
  共享框架上取得红/绿行为，再选 tag。`v8.0.13` 为 lightweight tag，指向
  `009e1cca…`（tree `df44a73d…`，15521 条目，commit 主题 “Merged PR 46821…”）；
  `v8.0.14` 指向 `25ef4aa3…`（tree `de5f42f2…`）。仓库既有历史快照
  `snap_80fefe20d65e43c8`（`2d105dd1…`，无 tag）仅为历史清单，未在该 SHA 证明漏洞，
  故不作评估目标。
- **修复事实**：真正的代码修复是 `67f3b042`“Merged PR 47275: Prevent
  RefreshSignInAsync if it is called with wrong user”（2025-02-06），经
  `merge-base --is-ancestor` 确认是 `v8.0.14` 的祖先、不是 `v8.0.13` 的祖先。
  OSV 的 GIT 区间把修复边界记成发布提交 `25ef4aa3`（v8.0.14 tag commit），
  与代码修复不是同一个对象（已记入 dossier discrepancies）。
- **红/绿复现**：自建最小 ASP.NET Core 应用（cookie 认证 + Identity core + 内存
  user store），端点 `/login/alice`、`/refresh/bob`、`/whoami`。8.0.13 上以 alice
  登录后调用 `RefreshSignInAsync(bob)`，下一次请求变成
  `AUTHENTICATED id-bob bob`（exit 3 / RESULT=VULNERABLE）；8.0.14 上保持
  `AUTHENTICATED id-alice alice`（exit 0 / RESULT=BLOCKED），应用日志出现新守卫的
  error。两个 runtime 用 `dotnet-install.sh --runtime aspnetcore` 并排安装。
- **源码事实**：`src/Identity/Core/src/SignInManager.cs:162-184`（v8.0.13）在
  `RefreshSignInAsync` 中认证当前 principal、复制 authenticationMethod/amr claim，
  然后直接 `SignInWithClaimsAsync(user, auth?.Properties, claims)`，从不比较
  `user` 与已认证 principal；v8.0.14 增加未认证与 userId 不一致两道守卫。
- **通报事实**：OSV CVE-2025-24070 受影响版本含 `v8.0.13`、GIT 区间 8.x 修复于
  `25ef4aa3`；NVD CPE `8.0.0 <= v < 8.0.14`（另有 9.0.0–9.0.3 与 VS2022 区间）、
  CWE-1390、CVSS 3.1 7.0 HIGH（仅 secondary，来自 secure@microsoft.com）；GHSA
  的 NuGet 包区间 8.0.0→8.0.14、9.0.0→9.0.3、Microsoft.AspNetCore.Identity
  2.3.0→2.3.1。
- **状态**：快照 `snap_6513f827cbeb91ab` 已建（125 language rows），dossier 已写
  （10 条证据，location `SignInManager.cs:162-184`，location_kind=logic）。
- **独立漏洞判定**：隔离 reviewer 返回 `confirmed_affected`，grade A，
  `reviewer != prepared_by`，9 项字段核验全 true，红/绿分别 exit 0 / exit 1
  （红=漏洞复现成功，绿=被守卫阻止）；location 归一为 `162-184` 并保留原始
  annotated 字符串。已记 4 条 discrepancy（OSV 修复边界=发布提交、versions
  数组缺 8.0.6/8.0.9、CWE-1390 与 log-and-return 补丁的语义差、VS2022 区间）。
- **迁移/晋升**：`migrate_snapshot_6513f827cbeb91ab.py --apply` 与
  `supersede_proposal_rows.py --apply` 均成功；`promote_verified_rows.py`
  dry-run 先因 `locations` schema 行号必须是整数或 `N-M`（裸字符串 “183”/“162”
  不合规）报错，改为 `183-183` 与整数 trace 行后 dry-run 通过，`--apply` 写入
  vulnerability/location/review/evidence(47)/status 各 1 行。
- **冻结/审计**：`freeze_snapshots.py . --only dotnet/aspnetcore` 导出
  `exp_snap_6513f827cbeb91ab`（15519 files，archive `f2c1732e…`，26,260,569 B）；
  `build_audit_exports.py . --only dotnet/aspnetcore` 生成
  `aud_6513f827cbeb91ab`（15519 文件，redacted 2，excluded 0，
  `remaining_advisory_id_count=0`，`source_export_id` 与导出一致）。
- **选版审查**：`build_selection_review_packets.py` 重建 packets（42 个）后，隔离
  reviewer 独立解析 tag（lightweight，`009e1cca…`，tree `df44a73d…`）、重算
  archive/manifest sha256、确认 15519 文件与 2 个 gitlink 的计数关系、并用
  `dotnet build src/Identity/Core/src/Microsoft.AspNetCore.Identity.csproj`
  真实构建成功（build_ok=true），四个 mandatory check 全过、audit 导出 0 个
  advisory id，返回 `accept`。`apply_selection_review.py --apply` 冻结 1 行
  （当前 frozen 39 / proposed 3，其中 2 行为早前 rejected、1 行 angular 待审）。
  validator 仍为 STRUCTURAL VALIDATION PASSED（含未解决候选与 A 率告警）。

## 2026-10-24 — go-gitea/gitea：GHSA-rjvx-x5h2-6px5 @ v1.25.5（独立判定进行中）
- **目标选择（证据优先）**：先取红/绿行为再选 tag。`v1.25.5` 是 annotated tag
  （tag 对象 `366d3718…`，peel 到 `f913d90a…`，tree `c2abec67…`，5651 条目，
  2026-03-12）；`v1.26.0` 为 annotated tag（`8b41bef1…` → `9b9d1e31…`，
  tree `1daa1f13…`，2026-04-18）。Gitea 的 release 分支不是 main 的祖先，
  两 tag 的共同祖先只有 `f09bea7a`（2025-09-24），因此不能用「v1.25.5 是
  v1.26.0 祖先」来论证；改用修复提交 `686d10b7` 为 v1.26.0 祖先、且只在
  `origin/main`/`origin/release/v1.26`、不在 `origin/release/v1.25`，并确认
  不存在 `v1.25.6` 标签。
- **证据事实**：OSV GHSA 记录（GitHub reviewed，2026-07-21）描述
  `POST /api/v1/repos/{owner}/{repo}/forks` 对非管理员只查 `IsOrgMember`，
  不查 `CanCreateOrgRepo`；Go 区间 introduced 0 → fixed 1.26.0；CWE-863；
  CVSS v4 `AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N`（页面 5.3
  moderate）。GO-2026-6074 的 `review_status` 仍为 UNREVIEWED（已记为
  discrepancy）。无 CVE/NVD 记录。
- **源码事实**：v1.25.5 `routers/api/v1/repo/fork.go:135-145` 仅做成员校验
  （136 行 `org.IsOrgMember`），随后 `forker = org.AsUser()`；v1.26.0 新增
  `prepareDoerCreateRepoInOrg`（86-112 行），其中 102 行调用 `CanCreateOrgRepo`
  并在不允许时返回 403。
- **构建/红绿**：用 Go 1.27.3 从两个 tag worktree 各自
  `CGO_ENABLED=1 go build -tags 'sqlite sqlite_unlock_notify'` 构建二进制
  （version 1.25.5 / 1.26.0）；本地 SQLite 实例 + API 播种（admin 建公开仓库、
  组织 `target-org`、can_create_org_repo=false 的团队，user4 入队）。对照组
  user4 直接建仓两版都是 403；fork 攻击在 1.25.5 返回 202 且 fork owner 为
  `target-org`（RESULT=VULNERABLE，重复 2 次一致），1.26.0 返回 403
  「User is not allowed to create repositories in this organization.」
  （RESULT=BLOCKED，重复 2 次一致）。
- **快照/dossier**：`build_snapshot_at.py` 生成 `snap_bd8b4ed626b39794`
  （77 language rows）；dossier 已写（9 条证据，location
  `routers/api/v1/repo/fork.go:135-145`，critical_operation 136-143，
  location_kind=logic），review 状态 PENDING_INDEPENDENT_REVIEW。独立漏洞判定
  agent 已启动，未返回结论，未声明完成。

## 2026-10-24 — angular/angular：选版审查接受并冻结（19.2.15 闭环）
- **隔离选版审查**：审查人 `independent_selection_reviewer_angular_24195339`
  （只读 packet 与四个导出的隔离会话），独立 `git ls-remote` 解析
  `refs/tags/19.2.15`（lightweight，单行无 `^{}` peel，`fbe9b9f9…`），确认
  tree `6b230c1f…` 与 8963 blobs；重算 archive `374734c3…`（51,116,289 B）与
  manifest `a1ecc67f…` 全部吻合；tar 恰 8963 个普通文件、0 symlink/gitlink、
  0 路径穿越/绝对路径/.git 元数据，manifest 逐行 sha256 与解包文件一致，并用
  `git write-tree` 重建出同一 tree；audit 与主导出逐字节相同（排除 0、脱敏 0、
  `remaining_advisory_id_count=0`）。构建：用 snapshot 自带 tsconfig/rollup
  真实编译 zone.js 成功（exit 0），并以 Bazel 6.5.0 构建官方目标
  `//packages/common:npm_package` 成功（exit 0，803.9s），产物含未修复的
  XSRF 逻辑。锚点：OSV/GitHub advisory/npm/NVD 均确认 19.2.15 在
  `< 19.2.16` 区间且 19.2.16 为首个修复版。verdict=accept，四个 mandatory
  check 全 true。
- **落地**：`apply_selection_review.py` dry-run
  `{"applied": false, "frozen": 1, "rejected": 0, "skipped": 41}`，`--apply`
  后 `{"applied": true, "frozen": 1, "rejected": 0, "skipped": 41}`；该 selection
  行转为 `decision_status=frozen`，写入 `snapshot_export_id`/`audit_export_id`、
  审批 URL 与 leakage_controls。`validate_dataset.py . --draft` 仍为
  STRUCTURAL VALIDATION PASSED（保留未解决候选与 A 率告警；不代表完整性、
  可利用性或评分验证）。

## 2026-10-24 — go-gitea/gitea：选版审查接受并冻结（v1.25.5 闭环）
- **隔离选版审查**：审查人 `independent_selection_reviewer_gitea_72495579`
  （只读 packet 与四个导出的隔离会话），独立 `git ls-remote` 解析
  `refs/tags/v1.25.5`（annotated，tag object `366d3718…` → commit
  `f913d90a…`，tree `c2abec67…`），与 packet 的 commit/tree 一致；重算 archive
  `16ed18f3…`（6,363,073 B）与 manifest `f7e47570…` 全部吻合；tar 恰 5651 个
  普通文件、0 symlink/gitlink、0 路径穿越/绝对路径/.git 元数据，manifest 逐行
  sha256 与解包文件一致；audit 导出的 `remaining_advisory_id_count=0`。构建：
  go1.27.3 + CGO + sqlite tags 编译 `gitea v1.25.5` 成功（exit 0，
  142,155,912 B）。锚点：OSV GHSA-rjvx-x5h2-6px5 / GO-2026-6074 区间均为
  introduced 0、fixed 1.26.0，v1.25.5 在区间内。审查同时记录：
  上游仓库自建 advisory 页面写「Affected <= 1.23.7 / Patched None」，与
  GitHub Advisory Database / OSV 的规范区间冲突，该 URL 记为 affected=false
  并说明以规范区间与代码/补丁证据为准。verdict=accept，四个 mandatory check 全 true。
- **落地**：`apply_selection_review.py` dry-run `{"applied": false, "frozen": 1,
  "rejected": 0, "skipped": 42}`，`--apply` 后 `{"applied": true, "frozen": 1,
  "rejected": 0, "skipped": 42}`；该 selection 行转为 `decision_status=frozen`，
  写入 `snapshot_export_id=exp_snap_bd8b4ed626b39794`、
  `audit_export_id=aud_bd8b4ed626b39794`、审批 URL 与 leakage_controls。
  `validate_dataset.py . --draft` 仍为 STRUCTURAL VALIDATION PASSED（保留未解决
  候选与 A 率告警；不代表完整性、可利用性或评分验证）。

## 2026-10-24 — elixir-plug/plug：v1.19.2 迁移、晋级与冻结（选版审查进行中）
- **独立漏洞判定**：`runs/independent/plug_GHSA-j43x-5hjq-rgxf_v1.19.2_round1/verdict.json`
  返回 confirmed_affected、grade A：v1.19.2（lightweight tag →
  `33858427…`，tree `f7ab747f…`，105 files）位于 OSV 区间
  introduced 1.19.0 / fixed 1.19.3；修复 `a61124aa…` 是 v1.19.3 祖先、
  非 v1.19.2 祖先；location `lib/plug/conn/query.ex:215-228`
  与 dossier 的 critical_operation 215-231 重叠；自建 red/green：
  v1.19.2 深层括号键 8000/16000/32000 均可解码、耗时约 3.8–3.9 倍/倍增
  （exit 3，RESULT=VULNERABLE），v1.19.3 在深度 32 抛
  `Plug.Conn.InvalidQueryError`（exit 0，RESULT=BLOCKED），两版对照查询一致。
- **迁移**：`migrate_snapshot_69faea6949b7a9bb.py` dry-run 通过后 `--apply`
  （2026-10-23T19:05:48Z）：新增快照 `snap_69faea6949b7a9bb`（evaluation_target
  true）、evaluation_selection 提议行、`confirmed_affected` triage 行，候选
  `disc2_66f8f9c063af47f3f5e8939f` 置 verified；旧快照
  `snap_026a9d6d2a05c227`（commit `05bde706…`，106 files，无 tag）保留为
  historical inventory，不作评估目标。proposal 行经
  `supersede_proposal_rows.py --apply` 归档（7→6）。
- **晋级/冻结**：`promote_verified_rows.py --apply` 追加 vulnerabilities/locations/
  reviews/evidence（41 条）/snapshot_vulnerability_status 各就位；`freeze_snapshots.py
  --only elixir-plug/plug` 导出 105 文件 archive `414e8dd5…`（202,697 B）与
  manifest `a460e26b…`；`build_audit_exports.py --only elixir-plug/plug` 生成
  `aud_69faea6949b7a9bb`（audit 与主导出字节相同，排除 0、脱敏 0、
  remaining_advisory_id_count=0）。selection 行仍为 `proposed`；
  隔离选版审查已启动，未返回结论，未声明完成。
- **选版审查（2026-10-24 返回）**：审查人
  `independent_selection_reviewer_plug_14421569`（只读 packet 与四个导出的隔离
  会话），独立 `git ls-remote` + 新仓库 fetch 解析 `refs/tags/v1.19.2`
  （lightweight → `33858427…`，tree `f7ab747f…`，与 packet 一致）；重算
  archive `414e8dd5…`（202,697 B）与 manifest `a460e26b…` 吻合；105 个 tar
  成员 = 105 manifest 行 = 105 个解包文件，0 symlink/gitlink、0 重复/绝对/
  穿越路径/.git 元数据，逐行 sha256 与大小全部一致，且每个文件可复现上游 git
  blob sha1；audit 导出的 `remaining_advisory_id_count=0`（审查人自行递归扫描
  GHSA/CVE/EEF 字面量）。构建 `mix deps.get` + `MIX_ENV=prod mix compile`
  exit 0（无警告，81 个 .beam）。锚点：OSV GHSA/EEF 的 versions 数组直接列出
  1.19.2，GitHub advisory 与上游 security advisory 页面均给出
  `>= 1.19.0, < 1.19.3`；上游修复 `b4aa8a0`（2026-06-23）不是该 tag 的祖先，
  Hex 1.19.3 亦于 2026-06-23 发布。verdict=accept，四个 mandatory check 全 true。
- **落地**：`apply_selection_review.py` dry-run `{"applied": false, "frozen": 1,
  "rejected": 0, "skipped": 43}`，`--apply` 后 `{"applied": true, "frozen": 1,
  "rejected": 0, "skipped": 43}`；selection 行转入 frozen，写入
  `exp_snap_69faea6949b7a9bb` / `aud_69faea6949b7a9bb` 与 leakage_controls。
  `validate_dataset.py . --draft` 仍为 STRUCTURAL VALIDATION PASSED（保留未解决
  候选与 A 率告警；不代表完整性、可利用性或评分验证）。
  （审查附带发现：packet 的 `tag_facts.tag_commit_tree_sha` 为 null，但
  `export_facts.tree_sha` 已独立核实；audit 与主导出字节相同，故其
  `remaining_advisory_id_count=0` 额外由审查人自查确认。）

## 2026-10-24 — elixir-plug/plug_cowboy：v2.8.0 迁移、晋级、冻结与选版审查（已接受）
- **独立漏洞判定**：`runs/independent/plug_cowboy_CVE-2026-32688_v2.8.0_round1/verdict.json`
  返回 confirmed_affected、grade A（reviewer `independent-reviewer-r1-plug-cowboy-ghsa-q8x4-x7mp-5vg2`，
  reviewed_at 2026-10-23T19:10:00Z）：v2.8.0 是 lightweight tag
  （`5a4771c4…`，tree `d46ce823…`，20 files），位于 OSV 区间
  `>= 2.0.0, < 2.8.1`；修复 `bfb34cb4…` 是快照 commit 的直接子提交，
  对 v2.8.1 为祖先、对 v2.8.0 不是；location `lib/plug/cowboy/conn.ex:29`
  （`String.to_atom(:cowboy_req.scheme(req))`，客户端可控 `:scheme` 造成
  BEAM atom 永久驻留）。审查人自建 red/green：v2.8.0 触发 10/10 原子增长
  （exit 3，RESULT=VULNERABLE），v2.8.1 仅映射 "http"/"https" 并在
  conn.ex:19 抛 CaseClauseError（exit 0，RESULT=BLOCKED）。
- **迁移**：`migrate_snapshot_39f103d0ed9572cb.py` dry-run 通过后 `--apply`
  （2026-10-23T19:13:07Z）：新增快照 `snap_39f103d0ed9572cb`（v2.8.0，
  evaluation_target true，channel release_tags）、evaluation_selection 提议行、
  一条 `confirmed_affected` triage 行；候选 `disc2_b6a9a610f8bcc9ff8e8fe71e`
  置 verified 并写入 `vulnerability_id=GHSA-q8x4-x7mp-5vg2`；旧快照
  `snap_8dbd807d0794116d`（commit `87740b57…`，20 files）保留为 historical
  inventory，不作评估目标。proposal 行经 `supersede_proposal_rows.py --apply`
  归档（5→4；同仓 v2.7.5/v2.7.4/v2.7.3/v2.7.2 候选未选，未清除）。
- **晋级/冻结**：`promote_verified_rows.py --apply` 写入 vulnerabilities /
  locations（`lib/plug/cowboy/conn.ex` `29-29`）/ reviews（grade A）/ evidence
  51 条（50 条 target_type=vulnerability + 1 条 snapshot）/
  snapshot_vulnerability_status，无 warning/冲突；
  `freeze_snapshots.py --only elixir-plug/plug_cowboy` 导出 20 文件，
  archive `dddc22a5…`（24,332 B）、manifest `2ab20dae…`；
  `build_audit_exports.py --only elixir-plug/plug_cowboy` 生成
  `aud_39f103d0ed9572cb`（audit 与主导出字节相同，excluded 0、redacted 0、
  remaining_advisory_id_count=0）。
- **选版审查（2026-10-24 返回）**：隔离审查人只读 packet 与导出，独立
  `git ls-remote` 解析 `refs/tags/v2.8.0` 为轻量 tag（无 `^{}` peel 行，
  对照 v2.7.0/v2.7.3/v2.8.1 均为 annotated），commit/tree 与 packet 及导出
  tree 一致，commit 在 origin/master，Hex 有 2.8.0 与 2.8.1；重算
  archive/manifest sha256 与字节数吻合；20 tar 成员 = 20 manifest 行 =
  20 解包文件 = 20 个 `git ls-tree -r` blob，0 symlink/gitlink、0 重复/
  绝对/穿越路径、无 `.git`，逐行 sha256/大小与上游 blob sha1 全部一致；
  本机 `mix deps.get` + `MIX_ENV=prod mix compile` exit 0（`Compiling 5 files`
  → `Generated plug_cowboy app`，20 条 warning 全部来自依赖 `plug`，
  本仓源码 0 warning），build_ok=true（packet 的
  `toolchain_missing_in_probe_environment` 仅指采集机）；6 个 https 锚点
  （OSV GHSA/CVE/EEF、NVD、GitHub advisory、上游 security advisory）均
  affected=true，SEMVER `introduced 2.0.0 → fixed 2.8.1`，NVD CPE
  `versionStartIncluding 2.0.0 / versionEndExcluding 2.8.1`；audit 导出
  `remaining_advisory_id_count=0` 由审查人自行递归扫描确认。verdict=accept，
  四个 mandatory check 全 true。
- **落地**：`apply_selection_review.py` dry-run `{"applied": false, "frozen": 1,
  "rejected": 0, "skipped": 44}`，`--apply` 后 selection 行转入
  `decision_status=frozen`，写入 `snapshot_export_id=exp_snap_39f103d0ed9572cb`、
  `audit_export_id=aud_39f103d0ed9572cb` 与 leakage_controls。首轮审查
  JSONL 的 6 个锚点未带 `vulnerability_id`，工具按 URL 去重把
  `vulnerability_count_at_selection` 算成 6；请审查人补
  `vulnerability_id=GHSA-q8x4-x7mp-5vg2` 后重新 apply，该值修正为 1
  （frozen_at 2026-10-23T19:16:11Z），其余结论未变。
  `validate_dataset.py . --draft` 仍为 STRUCTURAL VALIDATION PASSED（保留
  未解决候选与 A 率告警；不代表完整性、可利用性或评分验证）。

## 2026-10-24 — elixir-ecto/ecto：v2.2.0 迁移、晋级与冻结（选版审查进行中）
- **独立漏洞判定**：`runs/independent/ecto_CVE-2017-20166_v2.2.0_round1/verdict.json`
  返回 confirmed_affected、grade A（reviewer
  `independent-reviewer-round1 (Claude Code agent, deepseek-flash) - separate from the collecting agent`，
  reviewed_at 2026-10-23T19:15:38Z），九个字段全部 `{"verified": true}`。
  审查人自建 clone/worktree/harness（未用采集方 probe）：v2.2.0 与 v2.2.1
  均为 lightweight tag（无 `^{}` peel 行），前者 `4f84ddfb…`/tree
  `fcc4d035…`/182 entries，后者 `ae93362c…`/tree `25bb6d58…`；修复
  `db55b0cb…` subject 为 Revert 且 body 明确 revert `8e1b378a`（特性提交，
  2017-07-12），是 v2.2.1 祖先、不是 v2.2.0 祖先；location
  `lib/ecto/repo/queryable.ex:349-356`（nil 分支 351-352）与 dossier
  critical_operation `351-352` 重叠。红/绿：v2.2.0 控制组 `{:ok, 1}`、
  `token: nil` 亦返回 `{:ok, 1}`（RESULT=VULNERABLE，exit 3）；v2.2.1 抛
  `ArgumentError: nil given for :token …`（RESULT=BLOCKED，exit 0）。
- **审查记录的不一致**：① dossier 称两 tag 间只有 revert 一个功能性提交不准，
  `f8f3c1fb` 也改了 `lib/ecto/changeset/relation.ex`（与本 CVE 无关）；
  ② CVE 的 OSV GIT 区间由 NVD CPE 派生指向发布提交 4f84ddfb，真正引入
  特性的是 8e1b378a；③ `v2.2.0-rc.0`/`rc.1` 也含该特性但在 SEMVER 下界
  之外，未纳入评级；④ Linguist 把 `mix.lock` 计为 Elixir，补上后 182 entries
  与 10 行语言分布自洽。
- **迁移**：`migrate_snapshot_c7a36628b7853599.py` dry-run 通过后 `--apply`
  （2026-10-23T19:16:57Z）：新增快照 `snap_c7a36628b7853599`（v2.2.0，
  evaluation_target true，channel release_tags）、evaluation_selection 提议行、
  一条 `confirmed_affected` triage 行；候选 `disc2_247e5c090367033357d7b601`
  置 verified 并写 `vulnerability_id=GHSA-2xxx-fhc8-9qvq`；旧快照
  `snap_b710ed5084cfdd8b`（commit `c0c99f51…`，158 files，无 tag）保留为
  historical inventory，不作评估目标。proposal 行经
  `supersede_proposal_rows.py --apply` 归档（5→4）。同仓 3 个 adv3 候选
  （CVE-2026-32687 / CVE-2026-58225 / CVE-2026-66838）保持 pending，未清除。
- **晋级/冻结**：`promote_verified_rows.py --apply`（2026-10-23T19:17:04Z）
  写入 vulnerabilities / locations（`lib/ecto/repo/queryable.ex` `349-356`）/
  reviews（grade A）/ evidence 46 条 / snapshot_vulnerability_status，
  无 warning、无冲突；`freeze_snapshots.py --only elixir-ecto/ecto` 导出
  182 文件，archive `cf06e542…`（348,787 B）、manifest `6dc37544…`；
  `build_audit_exports.py --only elixir-ecto/ecto` 生成
  `aud_c7a36628b7853599`（source `exp_snap_c7a36628b7853599`，excluded 0、
  redacted 0、remaining_advisory_id_count=0）。selection 行仍为 `proposed`，
  隔离选版审查已启动、尚未返回，未声明完成。
  `validate_dataset.py . --draft` 仍为 STRUCTURAL VALIDATION PASSED（保留
  未解决候选与 A 率告警；不代表完整性、可利用性或评分验证）。
- **选版审查（2026-10-24 返回）**：隔离审查人
  `isolated-selection-reviewer::repo-vuln-50-v031::selrev-ecto::deepseek-flash-independent`
  只读 packet 与导出，独立 `git ls-remote` 解析 `refs/tags/v2.2.0` 为 lightweight
  tag（无 `^{}` peel 行，`cat-file -t` = commit，无 tag 对象，故
  tag_object_sha/tagger_date 为 null），commit/date/tree 与 packet 一致；
  重算 archive `cf06e542…`（348,787 B）与 manifest `6dc37544…` 吻合；
  182 tar 成员 = 182 manifest 行 = 182 解包文件 = 182 个 `git ls-tree -r`
  blob，0 symlink/gitlink/重复/绝对/穿越/`.git`，逐文件 sha256+size
  182/182 通过，按 git blob sha1 复算 182/182 命中；本机 Elixir 1.18.3 /
  OTP 27 `mix deps.get` + `mix compile` exit 0（142 个 ecto beam，
  `Generated ecto app`），build_ok=true；4 条 https 锚点全部 affected=true
  且同一 `vulnerability_id=GHSA-2xxx-fhc8-9qvq`（OSV GHSA/CVE、NVD、
  GitHub advisory），OSV SEMVER introduced 2.2.0 / fixed 2.2.1 且
  versions=["2.2.0"]，NVD CPE 精确钉 2.2.0、CVSS 3.1 9.8；修复 `db55b0cb`
  不是快照祖先（exit 1）、是 v2.2.1 祖先（exit 0）；audit 与主导出字节相同
  （cmp 干净、`diff -r` 一致），excluded 0、redacted 0、剩余 advisory id 0。
  verdict=accept，四个 mandatory check 全 true。
  审查记录的 packet 表述问题：`tag_commit_tree_sha` 为 null 但
  `tag_tree_matches_commit=true` 属自证；锚点 `published_at` 为 null 而
  OSV 实为 2022-04-12；packet 低估构建可行性；`affected_range` 是 OSV
  事件的等价改写而非原文。
- **落地**：`apply_selection_review.py` dry-run `{"applied": false, "frozen": 1,
  "rejected": 0, "skipped": 45}`，`--apply` 后 selection 行转入
  `decision_status=frozen`（2026-10-23T19:19:34Z），写入
  `snapshot_export_id=exp_snap_c7a36628b7853599`、
  `audit_export_id=aud_c7a36628b7853599`、`vulnerability_count_at_selection=1`
  与 leakage_controls。`validate_dataset.py . --draft` 仍为
  STRUCTURAL VALIDATION PASSED（保留未解决候选与 A 率告警；不代表完整性、
  可利用性或评分验证）。

## 2026-10-24 — spring-projects/spring-framework：CVE-2014-3625 正样本、迁移、晋级与冻结（选版审查进行中）
- **正样本采集**：`runs/verification/spring_CVE-2014-3625_v4.1.1.RELEASE/`。
  v4.1.1.RELEASE 为 annotated tag（object `3035d728…`），peel 到 commit
  `993dfbfda2dfc0415409975764f2df7a7a8e622e`（tree `06f43ba8…`，7068 个
  tracked entry，release commit 2014-10-01）；修复版本 v4.1.2.RELEASE
  （object `a4d5631c…`，commit `1a7cb3c4…`，tree `4de80f17…`，7088 entries）。
  采集方自建 JDK8 `javac -sourcepath` 构建（Gradle 1.12 wrapper 不可用），
  `repro/TraversalProbe.java` 只调 public `ResourceHttpRequestHandler` API：
  控制页 index.html 两版均 200（26 B）；`////../testsecret/secret.txt` 与
  `//../testsecret/secret.txt` 在 4.1.1 返回静态根外文件（LEAKS=2，
  RESULT=VULNERABLE，exit 3），在 4.1.2 全部 404（LEAKS=0，RESULT=BLOCKED，
  exit 0）。
- **独立漏洞判定**：`runs/independent/spring_CVE-2014-3625_v4.1.1.RELEASE_round1/verdict.json`
  返回 confirmed_affected、grade A（reviewer
  `independent-reviewer-round1 (Claude Code agent, deepseek-flash) - separate from the collecting agent`，
  reviewed_at 2026-10-23T19:31:43Z），九个核心字段及全部扩展字段均为 true。
  审查人自建 blobless clone、自写 HandlerProbe / UrlPipelineProbe /
  CleanPathCheck，只调 public API，并用 v4.1.1 与 v4.1.2 源码各自 javac 编译：
  RED 六个攻击向量（`file:/…`、`/../`、`//abs`、`/%2E%2E/`，及 URL 管道
  `/resources/file:…`、`/resources/%252E%252E/…`）在 4.1.1 全部 200 且返回
  `SECRET_OUTSIDE_CONTENT_1337`；GREEN 同一输入在 4.1.2 全部 404；控制文件
  hello.txt 两版均 200、缺失文件两版均 404。审查人显式排除了一个假阳性：
  单次编码 `%2E%2E` 经 AntPathMatcher 变成 `../`，旧版 cleanPath 检查也会
  拒绝，因此不计入成功向量。修复 `9cef8e30`（SPR-12354）是 v4.1.2 release
  commit 的直接父提交，是 fixed tag 祖先、不是 v4.1.1 祖先；审查人指出
  OSV references 中的 `161d3e30` 是 4.1.3 的 SPR-12432 后续修复，不应当作
  本 CVE 的 4.1.x primary fix。审查人实际 clone 并核实了两个独立公开 PoC
  （`ilmila/springcss-cve-2014-3625` 的 `stealfile.sh` 即
  `curl …/resources/file:/etc/passwd`；`gforresu/SpringPathTraversal` 4.1.0），
  故 `reproduction_reference` 非 null、维持 grade A。
- **字段规范化（只改机器可读表示，不改结论）**：应下游工具要求，由审查人
  自己把 `location.line` 收敛为 `"87-89"`（说明移入
  `critical_operation.line_note`，其 line 仍为 `"88-89"`）、把
  `tag_under_review_facts.kind` 收敛为 `"annotated"` 并新增 `tag_object`、
  在 `reproduction` 补 `red_commit`/`green_commit`/`green_commits`/
  `red_tag`/`green_tag`/`exit_semantics`、把 `fields_verified` 的
  `affected_range` 补为工具要求的复数键 `affected_ranges`。采集方未改写
  审查结论。
- **dossier**：`build_dossier.py` 对 `sources/` 中 OSV GHSA/CVE、NVD、
  GHSA 页面、tag/commit、fix patch、源码片段、red/green 输出逐条断言后
  生成 `dossier.json`：vulnerability `GHSA-hhm4-hwq6-3c6w`
  （alias CVE-2014-3625），category `path_traversal`，CWE-22，
  location `PathResourceResolver.java` `87-90`、critical_operation
  `88-89`，entry point `ResourceHttpRequestHandler.handleRequest:176`，
  9 条外部证据 + 1 条 snapshot 证据（field_evidence 用索引）。
- **CVSS 2.0 模式扩展**：本 CVE 只有 NVD CVSS v2 5.0 MEDIUM
  （`AV:N/AC:L/Au:N/C:P/I:N/A:N`），OSV/CNA 均无 v3.1/v4.0 分数。
  为在不编造分数的前提下保留权威向量，`schemas/vulnerabilities.schema.json`
  与 `v031/schemas/vulnerabilities.schema.json` 的 severity.version 枚举
  加入 `"2.0"`，vector pattern 加入 v2 形式 `AV:[NAL]/`；其余约束不变，
  已在 dossier 的 severity.source 与 limitations 中写明，跨 CVE 的严重
  程度比较需注意混合度量版本。`validate_dataset.py . --draft` 通过
  （105 条已验漏洞，0 schema error）。
- **迁移**：`migrate_snapshot_0cb7894bf83f49db.py` dry-run 通过后 `--apply`
  （2026-10-23T19:33:34Z）：新增快照 `snap_0cb7894bf83f49db`
  （evaluation_target true，channel release_tags）、evaluation_selection
  提议行、一条 `confirmed_affected` triage 行；候选
  `disc2_91abaf3a7cf344d0559c5de2` 置 verified 并写
  `vulnerability_id=GHSA-hhm4-hwq6-3c6w`；旧快照
  `snap_40eb10dbcf0e3602`（commit `42c0a9bc…`，11462 files，无 tag）保留为
  historical inventory。proposal 行经 `supersede_proposal_rows.py --apply`
  归档（4→3）；该 proposal 只列 v7.0.4–v7.0.8（GHSA-9qf2-26p9-2q2q 等
  24 个 advisory），**不含 v4.1.1.RELEASE**，本次选版是证据优先而非
  按 proposal 列表；同仓其余 83 个候选保持 pending，未清除。
- **晋级/冻结**：`promote_verified_rows.py --apply`（19:34:54Z）写入
  vulnerabilities / locations（`PathResourceResolver.java` `87-90`）/
  reviews（grade A）/ evidence 42 条 / snapshot_vulnerability_status，
  无 warning、无冲突；`freeze_snapshots.py --only
  spring-projects/spring-framework` 导出 7068 文件，archive
  `99daf369…`（9,599,133 B）、manifest `52bb3c0b…`；
  `build_audit_exports.py --only spring-projects/spring-framework` 生成
  `aud_0cb7894bf83f49db`（source `exp_snap_0cb7894bf83f49db`，excluded 0、
  redacted 0、remaining_advisory_id_count=0）。
  `build_selection_review_packets.py` 重建 47 个 packet。
- **隔离选版审查 → 冻结**：隔离审查人（
  `isolated-selection-reviewer-spring`，reviewed_at 2026-10-23T19:48:49Z，
  只读 packet/导出/公开网络）返回 accept：tag 解析 `3035d728…`→
  `993dfbfd…`、tree `06f43ba8…` 与 packet 一致；重算 archive sha256
  `99daf369…`（9,599,133 B）与 manifest `52bb3c0b…`，7068 成员=manifest
  7068 行=`git ls-tree -r` 7068 blob，全量 7068 文件按 manifest size/sha256
  与 git blob sha1 逐条复算 0 不一致；无 `.git`/symlink/gitlink；audit 归档
  与主导出字节相同、`diff -r` 为空、7068 文件正则扫 CVE/GHSA/advisory/CWE
  0 命中（remaining_advisory_id_count=0）；三个 https 锚点（OSV API、NVD
  API、GitHub advisory HTML）均 affected=true。Gradle 1.12 可在 JDK8 运行，
  但 2014 年插件仓库（repo.springsource.org 502 / repo.spring.io 401、
  propdeps 不在 Central）使全量 Gradle 构建不可行，改用 jarjar 复刻 cglib
  后 javac 编译 core 338/338、beans 292/292、beans-groovy、expression+aop
  +context+instrument 913/913、web+webmvc 718 个文件并跑通 SpEL 与
  `ResourceHttpRequestHandler` 探针（exit 0）；12 个 oxm/jasperreports
  可选集成类未编译，已如实记录为限制。三条锚点原先把同一 advisory 写成
  `GHSA-…`/`CVE-…`/`GHSA-… (HTML)` 三个 id，会让下游把漏洞数计成 3，已请
  审查人只做表示层归一（三条 `vulnerability_id` 统一为
  `GHSA-hhm4-hwq6-3c6w`，新增 `source_kind` 区分来源），结论与日期未改。
  `apply_selection_review.py --apply`（2026-10-23T19:49:38Z）后该行
  `decision_status=frozen`、`selection_review_status=accepted`、
  `vulnerability_count_at_selection=1`、`snapshot_export_id=
  exp_snap_0cb7894bf83f49db`、`audit_export_id=aud_0cb7894bf83f49db`；
  `validate_dataset.py . --draft` 通过（105 条已验漏洞，grade A 31/105），
  仅保留各仓 unresolved candidates 的 transparent limitation，未声明数据集
  完成或 release。

## 2026-10-24 — nlohmann/json：正样本在 commit 上复现成功，但无任何 release tag 落在受影响窗口，暂不选版
- **候选**：仓内 3 个 discovery 候选全部是 OSS-Fuzz 报告（OSV-2017-59、
  OSV-2022-409、OSV-2022-425），缺少 CVSS/CWE/同仓 fix 引用，triage 停在
  `pending_location`。本次只做证据核查，不改候选状态。
- **OSV-2022-409 复现**：OSV GIT range 为 introduced
  `a8a547d7a212a6a39943bbd5b4220be504a1a33e`（2022-05-10，
  "change bjdata ndarray flag to detect negative size"）、fixed
  `93c9e0c703b98f5082413920a62067ae0b68671e`（2022-05-18，
  "Discard optimized containers with negative counts in UBJSON/BJData"，
  tree `38ec66b9…`）。修复 diff 在 `binary_reader.hpp` 的四个
  `get_ubjson_size_value`/`get_bjdata_size_value` 分支加 `number < 0`
  检查，并在 ndarray 维度循环里对 0 维度短路。
  GitHub issue #3492 公开了 OSS-Fuzz 最小化用例
  `clusterfuzz-testcase-minimized-parse_bjdata_fuzzer-5698044521218048`
  （zip sha256 `ee53e679…`，17 字节：
  `7b 69 ff 5b 7b 23 5b 23 5b 55 20 55 00 5d 5d 55 00`）。
- **采集方自建复现**（只在 /tmp 新目录、脚本与产物分离，header-only 构建）：
  用 `single_include/nlohmann/json.hpp` 在 `a8a547d` 与 fix 父提交
  `6a7392058e69956d610acefa7e3ce1cd60c8f5a6` 上
  `g++ -fsanitize=address,undefined` 编译只调 public `from_bjdata` 的探针；
  同一 17 字节输入在 a8a547d 触发
  `AddressSanitizer: heap-buffer-overflow`（栈在
  `json_sax_dom_parser::key` → `std::string::compare`，与 issue #3492 的
  `std::__tree`/`basic_string` 栈一致，本机 libstdc++ 报 READ size 8、
  OSS-Fuzz libc++ 报 READ size 1，同一根因）；在 fix commit 与
  `v3.11.0` tag 的 header 上同一输入得到
  `[json.exception.parse_error.110] … unexpected end of input`，无 ASan 报告。
  自建 libFuzzer 也复现同一栈（6.4M 次执行另抓到与本题无关的嵌套
  stack-overflow，未计入）。
- **选版结论（未选版）**：`git tag --contains <introduced> --no-contains
  <fixed>` 对三条 OSV range 均为空；OSV-2022-409 的引入与修复都发生在
  develop 上，修复随 v3.11.0（annotated tag `5d5c4075…` → commit
  `499422b3…`，tree `e76a616b…`）首发，也就是说**没有任何 release 版本
  落在受影响区间**。已用 `build_snapshot_at.py` 在 `a8a547d` 建立
  inventory 快照 `snap_c807975205ec4828`（未设 evaluation_target、未迁移、
  未选版），仅作为证据留档。
- **不选版的原因**：现有 selection 流水线要求稳定 tag 解析
  （`tag_resolution.matches`）才能 accept；本仓若要选版只能选 commit 快照，
  属于策略变更，不能由采集方自行放宽或改判，因此保持
  `no_proposal`/未选中，并作为 transparent limitation 记录。openssl 的
  10 个候选同样全是 OSV-* fuzz bug（GIT range），尚未核验是否也全是
  develop-only；grpc 的候选含 CVE-2023-1428 / CVE-2023-32731 / CVE-2023-32732 /
  CVE-2023-33953 / CVE-2023-4785 等
  有发布版本区间的 advisory，是三个未选仓里唯一可能按现有流水线选版的，
  但需要重量级 C++ 构建，尚未开始。

## 2026-10-24 — grpc/grpc 可行性核查（未开始正样本，未选版）
- 8 个 discovery 候选中，4 个（CVE-2023-1428、CVE-2023-32731、
  CVE-2023-32732、CVE-2023-33953、CVE-2023-4785 对应项）在 OSV 里带
  ECOSYSTEM range（PyPI `grpcio`/RubyGems `grpc`/Maven），即确有发布版本
  落在受影响区间，理论上可按现有“稳定 tag + 固定 commit + 导出 + 隔离
  构建”流水线选版；另 `GHSA-hf3w-6hpw-qp67` 在 api.osv.dev 返回 404，
  不能当作可用 advisory 来源。
- 有利证据：CVE-2023-1428（GHSA-6628-q6j9-w8vg，C++ HTTP/2 对
  `te`/`:scheme` 等非法头触发 abort，CVSS 3.1 AV:N/AC:L/PR:N/UI:N/
  C:N/I:N/A:H）给出同仓 fix commit
  `2485fa94bd8a723e5c977d55a3ce10b301b437f8`，且 range 为 1.51.0–1.53.0；
  CVE-2023-32731/32732 给出 `29d8beeeac2555773b2a2dda5601c74a95d6c10`、
  `65a2a895afaf1d2072447b9baf246374b182a946` 与 PR #32309/#33005。
- 风险：`grpc/grpc` 是大型 C++ 仓，官方构建走 Bazel/CMake，依赖
  abseil/protobuf/boringssl/cares 等第三方；本机此前没有该仓构建产物。
  正样本验证需要真实跑起 server 或 chttp2 传输层单测并用构造的 HTTP/2
  HEADERS 触发 abort，构建成本远高于 spring 的 javac 路线。尚未取得
  任何 red/green 结果，因此**不选版、不迁移、不晋级**；下一步应先确认
  固定版本的构建路径（优先复用仓内 chttp2 单测而非全量 server），再按
  证据优先流程推进。

## 2026-10-24 — openssl/openssl 候选抽样（未核验 tag 窗口，未选版）
- 抽 3 个候选对应的 OSV 记录（OSV-2018-109 `ssl_get_prev_session`
  UAF、OSV-2020-223 `CRYPTO_DOWN_REF` UAF、OSV-2024-635 `do_evp_kdf`
  null-dereference），affected 包均为 OSS-Fuzz/`openssl`，range 全是
  GIT 型（introduced/fixed commit），与 nlohmann 同类。是否仍有 release
  tag 落在各窗口内需要完整 tag 历史（本机未 clone 该仓，未核验），因此
  不能像 semver 那样断言“全部 develop-only”，也不能据此选版。
- 续查（同一日，commit-graph clone）：10 条候选的 OSV GIT 窗口逐条用
  `git tag --contains <introduced> --no-contains <fixed>` 核对，9 条窗口内
  **没有任何 tag**；仅 OSV-2018-153（`asn1_ex_i2c` heap-buffer-overflow，
  2017-11-01 → 2018-06-12）窗口内有 `OpenSSL_1_1_1-pre1`…`pre7` 七个
  **预发布** tag，不是稳定发布版。因此 openssl 与 nlohmann 一样，在现有
  “稳定 tag + 固定 commit” 选版策略下没有可用的 release 目标，保持未选版。

## 2026-10-24 — grpc/grpc CVE-2023-1428：v1.52.0 构建与 RED 证据
- 选版目标：`grpc/grpc` v1.52.0（轻量 tag，直接指向 commit
  `a3f10052090539cd3e19aa8e04f3bf8eceae2964`，tree
  `be9042387e1a7d68a25ee247526f910043fb41bb`，9750 个 tracked 条目）。
  修复版本 v1.53.0（轻量 tag → `358bfb581feeda5bf17dd3b96da1074d84a6ef8d`，
  tree `8263df2b7910944a03f60f5539a569cb6216fc6f`）。
- 修复链核实：master `2485fa94…`（#32507）引入 `EncodedSizeOfKey`；
  v1.52 分支回移 `7a1412fa…`（#32510，首个包含它的发布是 v1.52.2）；
  v1.53 回移 `3f93c166…`（#32511，v1.53.0 的祖先）。`git tag --contains`
  确认 v1.52.0 不含任何回移（不是 fixed），v1.53.0 含 v1.53 回移。
- 根因（v1.52.0 源码）：`src/core/lib/transport/metadata_batch.h:85`
  `TeMetadata::Encode` 内 `GPR_ASSERT(x == kTrailers)`，而
  `hpack_parser.cc` 的 `MetadataSizeLimitExceededEncoder` 在超出
  max_metadata_length 时对已解析的非法值调用 `Key::Encode(value)`
  （`AddToSummary(Key::key(), Key::Encode(value).size())`），于是 abort。
- 构建：本机无系统 OpenSSL，改用仓库自带 BoringSSL
  （`-DgRPC_SSL_PROVIDER=module` 等 module provider），CMake/Ninja，
  RelWithDebInfo，third_party 子模块按 v1.52.0 的 gitlink 检出；
  `ninja -j16 grpc` 成功（1331 步），产出 `libgrpc.a`。
- 自写探针 `runs/verification/grpc_CVE-2023-1428_v1.52.0/repro/probe_hpack.cc`：
  只用公开的内部 `HPackParser` 接口（与仓内 fuzz harness 相同调用序列），
  从文件读一帧字节、给定 max_metadata_length，打印解析返回并检测是否 abort。
- RED（v1.52.0）：仓内 fuzz 语料最小化测试用例的 17 字节
  `40 02 74 65 00 40 02 74 65 02 40 00 65 74 00 3b 65`
  （`te` 头两处非法值）在 limit=58 时
  `ASSERTION FAILED: x == kTrailers`、exit 134（SIGABRT）；
  对照：同字节 limit=1024 正常返回（error=none）；`82 87 84` 合法输入
  在 limit=1024/58 都不 abort（limit=58 时返回 parse error）。
- 状态：RED 已取得；GREEN（v1.53.0 同字节不 abort）尚在构建中。
  在 GREEN 之前不写 dossier、不做隔离判定、不迁移/晋级/冻结。
- GREEN（v1.53.0，工作树切到该 tag、子模块按 v1.53.0 的 gitlink 检出后重建）：
  同一 17 字节 fuzz 用例 limit=58 → `PARSE_RETURNED error=set`、
  `PROBE_COMPLETED_NO_ABORT`、exit 0；生产形态的 8 KB 载荷 limit=8192
  同样返回 parse error、不 abort；对照输入正常解析。
- 生产形态 RED 补充：advisory 明确要求“后续 header 使总大小超过 8KB”。
  自造 8216 字节载荷（两个非法 te + 8000 多字节的普通 header），在默认
  limit=8192 下 v1.52.0 同样在 `metadata_batch.h:85`
  `ASSERTION FAILED: x == kTrailers`、exit 134（SIGABRT）；v1.53.0
  返回 parse error 且不 abort。这比只用 fuzz harness 的 limit=58 更贴近
  真实触发条件。
- 快照：`scripts/build_snapshot_at.py --full-name grpc/grpc --sha
  a3f1005… --repo-id 27729880 --tag v1.52.0` → PASS，
  snapshot_id `snap_0319ebb1a71dfd3c`（9750 个 tracked 文件、170 条
  语言行、primary=C++、evaluation_target 仍为 false）。
- 采集脚本：`runs/verification/grpc_CVE-2023-1428_v1.52.0/collect_sources.py`
  重新拉取 OSV/NVD/advisory 页面，复核 tag/commit/tree/条目数、三条修复提交
  的祖先关系、v1.52 线首发版本（`git tag --contains 7a1412fa` 仅 v1.52.2），
  并用探针重新跑 red/green（断言 SIGABRT 与 no-abort）。
  `build_dossier.py` 从 sources/ 重建 `dossier.json`（10 条 evidence、
  两处 code excerpt、两条 discrepancy：CVE GIT range 无 ECOSYSTEM /
  advisory 固定版本 1.53.0 但 1.52 线在 1.52.2 已修 / 包是语言包装器）。
- 状态：已交给隔离 reviewer（只拿到 repo+tag+CVE，不看 dossier/证据目录），
  等其独立 clone/build/repro 的结论。在拿到 verdict 前不迁移、不晋级、
  不冻结。

## 2026-10-24 — grpc/grpc CVE-2023-1428：隔离判定、迁移、晋级、冻结与审计导出
- 隔离判定：`runs/independent/grpc_CVE-2023-1428_v1.52.0_round1/verdict.json`
  → `confirmed_affected`、grade A，reviewer 独立 clone/构建/复现，
  根因位置 `src/core/ext/transport/chttp2/transport/hpack_parser.cc:1201`
  与采集方一致；fix_commit 记为 v1.53 回移 `3f93c166…`
  （`ancestor_of_fixed_release=true`、`ancestor_of_vulnerable_release=false`），
  并单列 advisory 引用的 master `2485fa94…` 对两个 tag 均非祖先。
- 事实校正：判定后复核 `git merge-base --is-ancestor 2485fa94 v1.53.0`
  为否 —— master 修复经 cherry-pick（`3f93c166…`，与 v1.52 回移
  `7a1412fa…` 同一 patch-id `7de18056…`）进入 v1.53.0，首次随稳定版
  v1.54.0 发布；dossier/migrate 中“master 修复是 v1.53.0 祖先”的表述
  已改为上述准确表述并追加为 discrepancy。
- 迁移：`runs/verification/grpc_CVE-2023-1428_v1.52.0/migrate_snapshot_snap_0319ebb1a71dfd3c.py`
  先 dry-run 后 `--apply`（2026-10-23T20:15:56Z）：快照行
  `evaluation_target=true`、channel `release_tags`，写入 proposed selection
  行、triage 行、candidate `disc2_6d178f1d30a41903b9f0f988` → verified、
  repository 指针；随后 `runs/selection/supersede_proposal_rows.py --apply`
  归档旧的 grpc proposal 行（3→2 行）。
- 晋级：`v031/scripts/promote_verified_rows.py` 先 dry-run 报
  `locations/GHSA-6628-q6j9-w8vg: '1287' does not match
  '^[1-9][0-9]*-[1-9][0-9]*$'`——location/trace 的行号必须是区间。
  已把 dossier 的行号改为实际代码区间：关键操作
  `hpack_parser.cc:1199-1202`（模板 `Encode` 调
  `AddToSummary(Key::key(), Key::Encode(value).size())` 于 1201）、
  入口 `hpack_parser.cc:1287-1290`、`ParseInput 1300-1310`、
  `TeMetadata::ParseMemento` `metadata_batch.cc:129-138`、
  size-limit 处理 `1215-1225`、断言 `metadata_batch.h:84-87`。
  重建 dossier 后 `--apply` 成功（2026-10-23T20:16:46Z）：新增
  vulnerabilities 1、locations 1、reviews 1、evidence 38、
  snapshot_vulnerability_status 1，无 warning/conflict。
- 冻结：`freeze_snapshots.py . --only grpc/grpc` →
  `data/snapshot_exports.jsonl` / `v031/reports/FREEZE_REPORT.json`：
  archive sha256 `01be7272…`、导出 9723 个文件（12 symlink、15 gitlink
  单独记录）、leakage 评估 `no_advisory_identifiers_detected_in_scanned_files`、
  build_status `toolchain_available`（冻结只记录构建系统存在，不执行构建）。
- 审计导出：`build_audit_exports.py . --only grpc/grpc` → 48 行导出、
  146 个文件被排除、33 个被脱敏，无 failure。
- 选版复核包：`build_selection_review_packets.py .` → 48 个 packet，
  grpc 为 `v031/reviews/selection_packets/27729880_grpc__grpc.json`
  （已知正样本锚点 GHSA-6628-q6j9-w8vg / CVE-2023-1428，ECOSYSTEM 与
  NVD CPE 均为 `>=1.51.0, <1.53.0`）。
- 状态：已派隔离选版 reviewer（只读自己的 packet、`exports/grpc__grpc/**`
  与公开网络，不看 dossier/verification/data/runs/WORK_LOG），
  在拿到 accept/reject 前不写 `evaluation_selection.jsonl` 的冻结结论。

## 2026-10-24 — grpc/grpc v1.52.0：独立选版 accept、frozen、draft 校验
- 隔离选版复核（`v031/reviews/selection_evidence_grpc_2026-10-24/`，
  `v031/reviews/selection_review_grpc_2026-10-24.jsonl`）：**accept**。
  - 标签：`git ls-remote` + blobless clone + `cat-file` 确认轻量 tag →
    `a3f1005…`，tree `be904238…` 与 packet 一致，commit 2023-02-03T20:10:16Z
    "Bump version to 1.52.0 (on v1.52.x branch) (#32187)"；pre1/pre2 另有指向。
  - 导出：重算 archive `01be7272…`（8,527,837 字节）与 manifest `62b2f9a0…`；
    9735 成员 = 9723 文件 + 12 symlink，15 gitlink 单列，**全量**逐文件 sha256/size 与
    manifest、`git ls-tree -r` 路径三方对齐，0 缺失 0 多余，无 `.git`。
  - 审计包：与主包 `cmp` 逐字节一致；对 9723 文件 48,537,768 字节扫描 CVE/GHSA/CWE 全 0，
    `advisory` 仅 `cpu.h` 一处普通英文。
  - 锚点：OSV GHSA/CVE、NVD CPE（`1.51.0 <= v < 1.53.0`）、GitHub advisory 页四源均 affected=true。
  - 构建：解包导出树 + 按 gitlink 取 abseil/boringssl/protobuf/zlib/cares/re2 六个 pin，
    CMake 3.28.3 + Ninja `ninja -j16 grpc` 1331 步 exit 0 → `libgrpc.a`
    19,752,388 字节 sha256 `67863596…`；消费者静态链接并运行 exit 0，
    输出 `version_string=30.0.0`（该树 `version.cc` 硬编码值）。残余限制：只构建 C++ core，
    未跑 ctest（BUILD_TESTS=OFF），GitHub REST API 403 限流。
- 应用审查：`apply_selection_review.py --apply` → grpc 选版行
  `decision_status=frozen`、`selection_review_status=accepted`（frozen_at 2026-10-23T20:24:02Z），
  approval anchors 4 条。选版统计变为 **46 frozen / 2 rejected（documented_exception）**。
- 校验修正：`validate_dataset.py --draft` 报
  `vulnerability GHSA-6628-q6j9-w8vg: ID missing in alias list`。按本库「canonical ID 必须
  在自己的 aliases 里」的惯例，把 `GHSA-6628-q6j9-w8vg` 加入 dossier 的 aliases
  （`build_dossier.py` 已同步修改并重建 dossier），并同步修正已 promote 的
  `data/vulnerabilities.jsonl` 该行（只改 aliases，不动任何验证字段）。
  修正后 draft 校验 **0 error / 49 warning**（48 条 coverage unresolved + aspirational A 率
  32/106）。
- 文档同步：`LIMITATIONS_V031.md` §2/§3/§6 与 `HANDOFF_V031.md` §0/§2/§3/§4 的过时计数
  改为当前实况（48 目标 / 46 frozen / 2 rejected / 2 未选版；106 条正样本 A32 B74，
  其中评测快照 77 条 = 45B+32A；triage 1739 行 86/802/795/28/28，887 条候选未 triage）。
- 仍未完成（如实保留 draft）：2 个 legacy documented_exception 目标；nlohmann/openssl 未选版；
  795 条 unknown；48 条 coverage 的 unresolved 候选；`source_cutoff_date=null` 未复核；
  无 agent 评测运行；无运行期网络隔离。**未声明完成、未声明 PASS_KNOWN_SWEEP、未 release。**

## 2026-10-24 — grpc 冻结后遗留候选的线索记录（未决策，不开新验证）
- 复核 grpc 冻结快照上的 7 条未 triage 候选时确认：`disc2_a3afc58773feb683298ba558`
  （CVE-2023-33953 / GHSA-496j-2rq6-j6cc，"Excessive Iteration in gRPC"）的 OSV
  范围为 `introduced 0, fixed 1.53.2`（PyPI grpcio / RubyGems grpc），**v1.52.0 落在范围内**；
  对应 `hpack_parser.cc` 的三个向量（字符串先缓冲后限长、varint 前导 0 无界、跨 CONTINUATION
  帧的元数据溢出检查）。本会话只做了线索核实，**没有写 triage 决策、没有声称 confirmed**，
  候选维持原状态，留待源码级/复现级验证。
- 其余 6 条：GHSA-cfgp-2977-2fmm 与 GHSA-9hxf-ppjv-w6rq 的 OSV 范围是
  1.53.0–1.53.0 / 1.54.0–1.54.1（v1.52.0 不在内）；GHSA-p25m-jpj4-qcrr 为
  1.53.0–1.53.1 / 1.54.0–1.54.2 / 1.55.0–1.55.2（v1.52.0 不在内）；
  CVE-2017-8359 的 OSV GIT 范围为 last_affected `c25267fd…`（2017 年）；
  CVE-2020-7768 / GHSA-pp75-xfpw-37g9 的受影响包是 npm `grpc` / `@grpc/grpc-js`（grpc-node 仓）；
  GHSA-hf3w-6hpw-qp67 在 OSV 无记录，仓库 advisory 只覆盖 1.8x 线。
  以上均未落 triage 行，`LIMITATIONS_V031.md` 已声明 grpc 其余候选未清除。

## 2026-10-24 — grpc 遗留候选落 triage；全库未 triage 候选提案；两库选版窗口复测
- grpc 7 条候选已落 `data/snapshot_candidate_triage.jsonl`（`triage_grpc_candidates.py --apply
  --update-coverage`，triage 行 1739→**1746**）：5 条 `confirmed_not_affected`
  （CVE-2017-8359 按 GIT last_affected + fix 祖先；CVE-2020-7768 按 npm 包归属 grpc-node；
  CVE-2023-32731/32732/4785 按 advisory 起始版本 1.53.0；GHSA-hf3w-6hpw-qp67 按其自身
  1.82.2/1.83.1 修复版本），**CVE-2023-33953 维持 `possible_affected`**（v1.52.0 在
  `0..1.53.2` 内，未做复现），加上原有 1 条既有 `confirmed_affected`。
  `discovery_coverage` 中 grpc `unresolved_candidates=1`，`outcome` 仍 `NEEDS_REVIEW`。
- `v031/scripts/triage_range_scope.py` 增加 `--include-untriaged`（对没有 triage 行的候选也提案）。
  `runs/triage_untriaged_2026-10-24/proposals.jsonl` 共 1662 条：
  `indeterminate 925 / possible_affected_range 414 / not_affected_range 281 / out_of_scope_product 42`。
  其中未 triage 候选 867 条（`not_affected_range` 281 全部来自这一组），既有 unknown 行 795 条。
- `v031/scripts/apply_range_triage.py` 增加 `--insert-untriaged`：只对 `not_affected_range`
  且候选==仓库评测快照的提案追加新行，其它提案一律不插入。dry-run 结果：**inserted=281**、
  0 冲突（候选/仓库/快照三方对齐），待独立审计后决定是否 `--apply`。
- 未选版两库独立复测（`runs/verification/needs_selection_windows_2026-10-24/`）：
  nlohmann/json 57 个 tag / 3 个有界 GIT 窗口、openssl/openssl 451 个 tag / 10 个窗口，
  **落在窗口内的稳定 tag 均为 0**（含 2026-10-23 新 tag `openssl-4.1.0`）。
  两库维持 `evaluation_snapshot_id=null`，不编造 tag/commit。
- 未 triage 候选提案落地：独立审计 `runs/triage_untriaged_2026-10-24/audit/AUDIT.md` 复算 281 条
  `not_affected_range`（0 键冲突、0 alias 不符、抽样 40 条/49 record 对 live OSV 全一致），结论
  APPLY_WITH_EXCLUSIONS：`disc2_05ed96dc1c16b758a459c217`（aspnetcore v8.0.13）实际落在
  `Microsoft.AspNetCore.App.Runtime.*` 8.0.0–8.0.21 内，必须排除。另发现 5 条 actix monorepo 行
  用 tag 版本 [3,12] 冒充各 crate 版本（actix-web 实为 4.12.1、actix-files 0.6.10），结论虽成立但
  basis 不成立，本批一并排除。最终以 `proposals_applied.jsonl` **插入 275 条**
  `confirmed_not_affected`（`apply_range_triage.py --insert-untriaged --only-proposal not_affected_range
  --apply`，备份 `runs/data_fixes/snapshot_candidate_triage_before_range_scope_2026-10-23T204256Z.jsonl`）。
  triage 行 1746→**2021**（1083 not_affected / 795 unknown / 86 affected / 29 possible / 28 duplicate），
  未 triage 候选 887→**592**。`validate_dataset.py . --draft`：**0 error / 49 warning**。
- 待办：aspnetcore 争议行应重提案（优先同快照 `adv3_0c015197f7987011`）；actix 5 条需按 crate 实际版本
  重新生成提案；生成器需按 record 取全部 repo-owned 包并去重。
- actix monorepo 5 条按 crate 实际版本重做：`runs/triage_actix_monorepo_2026-10-24/`
  从 tag `http-v3.12.0` 取三个 crate 的 Cargo.toml（actix-web 4.12.1 / actix-http 3.12.0 /
  actix-files 0.6.10，sha256 已断言），重新判定后插入 5 条 `confirmed_not_affected`：
  3 条上界严格低于快照；2 条 actix-files 0.6.10 与 `fixed` 相等，按 OSV `fixed` 开区间
  写明「快照是首个不受影响版本」，不套用「严格低于上界」措辞。
  triage 2021→**2026**（1088 not_affected），未 triage 候选 592→**587**；draft 校验仍 0 error / 49 warning。
- 审计争议行 `disc2_05ed96dc1c16b758a459c217`（aspnetcore v8.0.13 / GHSA-5rrx-jjjq-q2r5）按缓存
  OSV 原始记录复核：`Microsoft.AspNetCore.App.Runtime.*` 8.0.0–8.0.21 含 8.0.13（9.0/10.0-rc 分支另列），
  写成 **`possible_affected`**（`runs/triage_aspnetcore_CVE-2025-55315_2026-10-24/`），不做复现、不称 confirmed。
  triage 2026→**2027**（possible 30），未 triage 候选 587→**586**；draft 校验 0 error / 49 warning。
- `triage_range_scope.py --strict-records` 评估（`runs/triage_strict_records_2026-10-24/README.md`）：
  默认模式只评估缓存 query 里点名的包，strict 模式评估 record 内全部上游包、按 `(type, events)` 去重，
  任一同族包命中即 `possible_affected_range`，且 record 不含被查询包时不得给出排除。
  先前「strict 少了 281 条 not_affected_range」是**不同输入基线**造成的假象：1662 条的文件生成于 275 条
  落盘之前，而 `--include-untriaged` 只补没有 triage 行的候选。今日同基线重跑：默认 1381
  （414 possible / 925 indeterminate / 42 out_of_scope）vs strict 1381（416 / 923 / 42），
  候选集合完全相同，只有 2 条 indeterminate→possible：
  `disc2_150757786799c6fb1a80df4f`（spring-framework 4.1.1 撞上同 record 内 spring-security-core 的
  4.1.0–4.1.5，跨产品误报）与 `disc2_22f75256623aa38c50a68574`（@angular/ssr 19.2.16 分支确实覆盖
  @angular/platform-server 19.2.15，可成立）。结论：strict 仅作非默认安全网，未用于任何落盘数据；
  后续需按产品命名空间（Maven groupId / npm scope / NuGet family）限定同族包后才考虑默认启用。
- 生成器补上 discovery_v3 仓库 advisory 路径（`runs/triage_v3_advisories_2026-10-24/`）：此前 261 条未 triage 候选
  在 notes 里只有 `runs/discovery_v3/repo_advisories/*.json`，而生成器只认 `runs/discovery_v2/*`，于是统一落到
  「no cached advisory record」。新增 `evaluate_ghsa`：按 `||` 拆 OR 子句、逗号 AND、拒绝含预发布标记的版本、
  拒绝带残余运算符的版本串（旧 `parse_version` 会把 `4.4.13 || >= 5.1.0` 静默截成 `4.4.13`），
  `withdrawn_at` 一律不定；并加**包归属闸门**（包名归一化后等于仓库名，或 Go module 路径以其结尾），
  挡住 actix-files 0.6.9 对 tag `http-v3.12.0`、Microsoft.AspNetCore.Identity 2.1.39 对 tag `v8.0.13`
  这类跨产物版本比较。同 1381 候选上：NA 0→**12**，possible 414→**522**，indeterminate 925→805；
  `verify.py` 用独立比较器复算 12 条排除（0 失败）和 107 条纯 v3 possible（0 失败），48 条 OSV+v3 混合跳过。
  12 条中 7 条是既有 unknown 行、5 条是未 triage 候选；**尚未落盘**，已交独立审计（claims.json 119 条）。
- v3 范围语法与回落（同日续）：GitHub advisory 里有 `1.7.0>=`、`=< 5.8.1`、`< =9.0.13`、
  `=> 11.1.4 < 12.3.5`、`6.1.8 - 6.4.0`、`All versions` 等手写写法，`parse_clause` 改为规范化+分词
  解析（连字符区间按两端闭区间，只会多报 possible、不会多报排除；散文式 `<= 1.24 through main`
  仍按不可解析处理）；notes 路径里找不到 alias 记录时用 `build_alias_index` 扫全量 v2 缓存兜底。
  另修正「记录存在但无可比包范围」仍被写成「no cached advisory record」的措辞，改为列出 record。
  同 1381 候选：possible 522→**524**、indeterminate 805→803、NA 仍 **12**；审计基线文件保持
  `proposals.jsonl`，增量在 `proposals_with_recovery.jsonl`。单测 36 条通过。
- GIT 祖先判定 48 条经独立审计（`runs/triage_git_ancestry_2026-10-24/audit/AUDIT.md`，
  逐条在 clone 内用 `GIT_NO_LAZY_FETCH=1` 重跑、48/48 与 live OSV 比对无漂移）：
  结论 APPLY_WITH_EXCLUSIONS，落盘 **47 条**（`--apply --exclude-candidate disc2_1db859a0e22a5b17f65d44ab`），
  triage 仍 2027 行：not_affected 1088→**1135**、unknown 795→**748**；备份
  `runs/data_fixes/snapshot_candidate_triage_before_git_ancestry_20261023T205412Z.jsonl`；
  draft 校验 0 error / 49 warning。被排除行 OSV-2025-657 的结论虽对（curl 8.3.0 无
  `ftp_pp_statemachine`，8.14.0 才有），但其 `introduced` 只是 CI 文件改动、fixed 是 libssh2 SFTP 修复，
  祖先规则对该记录不成立，**保持 unknown**。审计另提 4 项脚本缺陷（多 fixed/introduced 只取首个、
  非 GIT range 只记 note 不阻断、not_introduced 缺代码级证据、未断言 repo 与 clone origin 一致），
  已写入 run README，下一轮祖先判定前修。
- discovery_v3 批次独立审计完成并落盘（2026-10-24）：审计方用自写解析器（`audit/audit_script.py`，不导入生成器）
  逐条重算 119 条 claim（12 NA + 107 pure-v3 possible），全部 CONFIRMED：15 个 repo 的 advisory 文件齐全、
  119 个 `ghsa_id` 全部命中、无 withdrawn、无空 vulnerabilities、无 OSV/GHSA 混形；12 条 NA 的每个 owned
  vulnerability 的每个 clause 都有上界且快照高于所有上界（`7.14.1 > 7.4.2/7.4.3`、`3.0.2 > 2.3.7 且 > 3.0.1`、
  `41.0.5 > 41.0.3`、`8.0.4 > 7.1.0/7.1.3.1`、`1.25.5 > 1.25.4/1.23.7` 均按数值分量复核）；bound 文本与
  原始 advisory 逐字一致。verdict `APPLY`，`exclude: []`。
- 应用该批次：`proposals.jsonl` 过滤出 12 条 `not_affected_range`（`proposals_applied.jsonl`），
  `--only-proposal not_affected_range --insert-untriaged --apply --reviewed-by "independent audit 2026-10-24 …"`：
  7 条既有 unknown 改写 + 5 条新增；triage 2027→**2032** 行，confirmed_not_affected 1135→**1147**、
  unknown 748→**741**，confirmed_affected 86 / possible_affected 30 / duplicate 28 不变；
  备份 `runs/data_fixes/snapshot_candidate_triage_before_range_scope_2026-10-23T205548Z.jsonl`；
  已选版仓库内未 triage 候选 586→**581**（另 13 条属未选版仓库）；draft 校验 0 error / 49 warning。
- 审计提出的口径问题（已记录，未改判）：审计脚本按「归一化相等或 Go module path 尾段」的严格字面读法，
  会把 `guzzlehttp/guzzle`、`rails/rails`、`symfony/symfony` 等 6 条 NA 判为无归属；但按「包版本线跟随
  仓库 tag」的实质判据，这些包正是仓库自身的发行包（前缀只是 registry/owner），审计逐条确认后才给出 APPLY。
  实现实际按仓库 basename 做「相等或以之结尾」匹配（`repo_names` 只放 basename），行为与实质判据一致、
  与旧 docstring 的窄描述不一致：已改写 `package_belongs_to_repo` docstring 说明真实规则，并加 2 条单测
  钉住两侧（`guzzlehttp/guzzle`/`symfony/symfony`/`rails` 归属；`symfony/http-kernel`/`actix-files` 不归属）。
  下游若坚持严格字面口径，应把这 6 条退回 unknown——已写进 LIMITATIONS 与该批次 README。
- 审计另提醒「过包含」方向风险（未落盘，仅登记）：10 条 possible 仅由无上界 clause 支撑（cryptography 6、
  gitea 3、rails GHSA-9822 1），其中 5 条按 `patched_versions` 看已高于补丁；3 条 laravel possible 依赖
  advisory 把大版本线拆成缺上界条目。任何一条在升格为 `confirmed_affected` 前必须人工对 `patched_versions`。
- 单测 76 条通过（新增 2 条归属测试）。
- 新增低侧（below-lower）范围证明（2026-10-24，待审计）：此前 `triage_range_scope.py` 只接受「快照在所有上界之后」
  这一种排除证明。现补上对称证明：快照严格早于每条 owned clause 的下界（漏洞是后来引入的）。规则：
  每条 clause 都须有下界（`<2.0.0` 这种从 -∞ 开始的 clause 阻断证明）；`>=x` 要求快照 `< x`，`>x` 允许 `<= x`；
  先判 contains（命中即 possible）；含预发布串、无法解析的 constraint、withdrawn advisory 一律阻断。
  GHSA 侧上界不是必需（`>=2.0.0` 这种开放式范围仍可排除 1.x）；OSV 侧因开放式 range 属 unsupported，
  保持 indeterminate 而不做低侧排除。`not_affected_row` 的 basis 现在按 proof 区分措辞（above_upper /
  below_lower / 混合），`detail.proof` 随 proposal 落盘。
- 低侧批次（`runs/triage_low_side_2026-10-24/`）：输入为当前 741 条 unknown + 581 条无 triage 行候选
  （共 1322）→ possible 524 / NA **65** / indeterminate 691 / out_of_scope 42。65 条全部为 below_lower：
  spring 23、undici 12、django 6、cryptography 6、rustls 3、next 3、symfony 2、PHPMailer 2、tomcat 2、
  ImageSharp 2、vite 1、netty 1、aspnetcore 1、gitea 1；其中 25 条是既有 unknown 行、40 条无 triage 行。
  试运行（未落盘）确认 25 改 + 40 插、无 snapshot 不匹配；`na_claims.jsonl` 65 条已交独立审计（隔离 reviewer，
  不得读 data/WORK_LOG/HANDOFF/generator），verdict 未回。**尚未写入任何数据行**。
- 祖先判定脚本 v1.1（`runs/triage_git_ancestry_2026-10-24/`）：按审计修 F2/F3/F5——`range_state()` 评估整条事件序列
  （每个 introduced/fixed 开闭一个窗口，证据列出每个 event 的祖先结论）；记录里若含可比的上游生态范围
  （PyPI/npm/Go/Maven/crates.io/RubyGems/Packagist/NuGet/Hex/Pub/SwiftURL）则阻断判定，发行版范围
  （Debian/Alpine/OSS-Fuzz）不阻断；克隆前校验 `remote.origin.url` 与仓库 full_name；notes 说明 fixed 事件常是
  OSS-Fuzz 二分边界而非补丁本身。对当前 741 条 unknown 试跑仅解出 1 条（仍是审计已排除的 OSV-2025-657），
  故不落盘；报告 `report_v1_1_dry.json`。新增 9 条单测，套件 93 条通过。
- 复核披露截止（`runs/cutoff_verification_2026-10-24/`，`verify_cutoff.py` + `REPORT.md` + `summary.json`）：
  49/50 条 coverage 写 `cutoff_date=2026-10-21`，**rack/rack 写 2026-10-22**；rack、django、libexpat、
  axios、echo 的 pass 4 在 2026-10-22 运行（快照迁移复核）。数据内所有候选 `published_at` 最大
  2026-10-21T05:36Z、OSV/NVD 缓存最大 2026-10-21T07:47Z、GitHub advisory 最大 2026-10-21T05:36Z，
  **没有 2026-10-21 之后发布的披露进入数据**。但采集截止不统一，`manifest.source_cutoff_date` 继续
  保持 null，不在没有统一口径时写单一日期；LIMITATIONS 第 4/6 节同步改正（原「2026-10-22 当日新披露
  不在数据内」对 rack 的 coverage 声明不准确）。
- 低侧批次审计返回并落盘（2026-10-24）：独立 reviewer（`runs/triage_low_side_2026-10-24/audit/`，
  自写 `audit_script.py`、`python3 -I`、不导入生成器、不读 data/WORK_LOG/HANDOFF/dossier）对 65 条
  claim 判 **56 CONFIRMED / 3 REJECTED / 6 INCONCLUSIVE**，verdict `APPLY_WITH_EXCLUSIONS`。
  排除 9 条：gitea `adv3_21c8f05a9aa6e0fe`（**真排除错误**：OSV 副本 `[0, 1.27.0)` 含 1.25.5，GitHub 文本
  `<= 1.26.4, >1.27.0` 是空合取）；tomcat 两条（同记录其他 owned 区间把 9.0.98 放在下界之上，结论可能仍真
  但不是 below_lower 证明）；undici `disc2_8a587c1ea6aeab32d1825879`（分支 `< 8.2.0` 无下界）；
  spring 两条（下界为预发布 `7.0.0-M1`）；next.js 两条（预发布 canary 下界）；
  aspnetcore `disc2_d87402cd07b44ec2df9a73d4`（唯一受影响包是 `Microsoft.AspNetCore.*` 兄弟包）。
  审计另指出 `disc2_150757786799c6fb1a80df4f` 的 spring 排除依赖「spring-security-core 属外部产品」这一
  归属判定，该行只能抑制 spring-framework，**不得用于消除 spring-security 命中**；23 条确认行依赖
  owner/module 前缀式归属，AUDIT.md §8 逐条列出供严格口径下游退回。
- 应用低侧 GHSA/OSV 批次：`proposals_applied_audited.jsonl` 只含 56 条确认行，
  `apply_range_triage.py --apply --reviewed-by "independent audit 2026-10-24 (…/AUDIT.md; …NVD…/AUDIT.md)"`。
  与 NVD 批次合并后结果：triage **2064** 行（changed 33 / inserted 32），
  `confirmed_not_affected` **1212**、`unknown` **708**（1212+708+86+30+28=2064），
  备份 `runs/data_fixes/snapshot_candidate_triage.before_low_side_2026-10-24.jsonl`；
  draft 校验 0 error / 49 warning；已选版仓库内无 triage 行候选 581 → **549**（另 13 条属未选版仓库）。
- NVD 低侧批次审计**重做**（`runs/triage_low_side_nvd_2026-10-24/audit/`）：首轮审计在 `osv_queries/` 下找不到
  原始 NVD 记录、误报「缓存无原始数据」；指出正确路径 `runs/discovery_v2/nvd_queries/` 后，审计方按
  `configurations[].nodes[].cpeMatch` 重算，导出 13 个匹配 / 12 条记录（9 Modified / 3 Analyzed，无
  rejected/withdrawn）。判 **9 CONFIRMED / 2 REJECTED / 1 INCONCLUSIVE**。排除 3 条：两个 cJSON 行
  （CPE 只点名 `1.7.17`/`1.7.19`，不是下界；cached `DEBIAN-CVE-2024-31755` 是 `[0, 1.7.18-1)` 含 1.7.16）、
  curl `disc2_3497bcafab1101a70a25ecf0`（同记录还有 Debian 11 的 `debian_linux:11.0` vulnerable 匹配，
  其 curl 7.74.0 在 `>= 8.13.0` 之外，下界不是全部受影响集）。9 条 curl 行均为 `versionStartIncluding`
  显式下界，已落盘。
- 生成器修复（由两批审计驱动，`v031/scripts/triage_range_scope.py`，单测 93 → **100 条 OK**）：
  1. `clause_is_consistent`：合取 clause 的上下界若无交集（gitea `<= 1.26.4, >1.27.0`）则阻断两种排除证明，
     不再取下界；2. `parse_constraints` 把 `;` 当分支分隔符（undici `7.23.0 < 7.28.0; 8.0.0 < 8.5.0`）；
  3. `parse_clause` 把裸前导版本读作该分支闭下界；4. `evaluate_nvd` 不再把 exact CPE 当闭下界
     （CVE-2024-31755 的 `cjson:1.7.17` 只说明该版本受影响，Debian 同 CVE 是 `[0,1.7.18-1)`），
     只有 exact 匹配的记录现在给 `indeterminate`。复核：用修好的生成器对**应用前**表重跑，65 条已落盘 claim
     仍全部被提出（73 NA 中 65 条命中，`missing: []`）；对同一输入 GHSA/OSV 侧现提 63 条（gitea 消失、
     undici GHSA-hm92 变 possible），只落盘审计确认的 56 条。
- 既有排除的复现复核（`runs/triage_strict_recheck_2026-10-24/`）：把**应用前**表中 693 条 basis 为
  「lies after every upper bound」（`proof=above_upper`）的行临时置回 unknown（连同当时 741 条 unknown，
  共 1434 候选），用当前生成器重算，两种模式各跑一遍，未写任何数据。
  **首轮（仅 strict）**：654 仍 NA / 32 indeterminate / 7 possible；strict 与默认都出现的 3 条
  （`disc2_e68c3ebee9050b637417aeb7`、`disc2_cd7c6b92922ddd5287fda28f`、`disc2_50fafffdada5d6d62c89dd1d`）
  阻断项来自 `discovery_v3/repo_advisories` 的粗区间（`>= 0.4` / `>= 1.3.0` / `All`），同记录
  `patched_versions` 为 `3.0.9.1, 2.2.8.1`，与 OSV 证明一致；仅 strict 出现的 4 条是跨产品兄弟包
  （cryptography 41.0.5 vs `openssl-src [0,111.25.0)`；django 4.2.13 ×2 vs `jquery-rails [0,4.3.4)`（GHSA-6c3j）；
  aspnetcore 8.0.13 vs `DisCatSharp [0,9.8.3]`（GHSA-qhqf））。
- 按上条 32 条 indeterminate 逐个定位，查出并修掉两个真实生成器缺陷（`v031/tests/test_triage_range_scope.py`
  57 条 OK）：
  1. **等值 clause 是双侧有界**：v3 把单个受影响版本渲染成 `4.5.0`（vite GHSA-92r3），解析为 `=4.5.0`；
     高位证明只认 `<`/`<=` 因而强制 indeterminate，且 `below_lower_bound` 把 `=` 当「小于等于」
     （会误判精确版本在区间外）。现 `=` 同时算上下界，只有精确版本在区间内。
  2. **不可比记录不得否决**：GitHub 副本只列 monorepo 子模块（npm `next` vs 仓库 `vercel/next.js`、
     `@nestjs/*`、netty 模块、rails 组件）或只有发行版生态时，归属守卫会丢弃该记录，旧逻辑却把它算作
     indeterminate 并拖垮整体判定，即使同一 advisory 的 OSV 副本已证明排除。此类记录现带
     `comparable: false`，由新 `combine_votes` 忽略；任何**可比的** possible 仍然一票否决。
- 修后复跑同一 1434 候选：**默认模式 690/693 仍为 not_affected_range、0 indeterminate、3 possible**
  （即只剩 3 条 rack）；strict 模式 686/693、0 indeterminate、7 possible（多出的 4 条是跨产品）。
  32 条 indeterminate 全部是两个缺陷造成的，**不是数据不成立**，故未降级任何行。
  副作用：默认模式对 1434 候选提出的 NA 总数由 692 升到 **735**（多出的 43 条中 32 条是被复核行，
  其余 11 条是原本 indeterminate 的 unknown 候选）；**这些只是提案，未应用**，将来应用仍需独立审计。
  证据：该目录 `default_recheck.jsonl`、`strict_recheck.jsonl`、`summary.json`、README。
- 仍未解决的 3 条 rack 行：生成器不消费 `patched_versions`，v3 开放式区间与 OSV 修复列表不一致；
  已写进该目录 README 的 follow-up（要么教会 `evaluate_ghsa` 用 `patched_versions`，要么明确
  「v3 开放式区间不可用」的政策）。`comparable` 标记同样用于 `unsupported_ecosystem`；withdrawn
  仍按保守处理（否决）。
- `CHECKSUMS.sha256` 盘点（2026-10-24）：该文件是 **v0.3 基线**（46 行，与 `../repo-vuln-50-v03/CHECKSUMS.sha256`
  逐字一致）加 2 条 v0.3.1 新文件；v0.3 自身仍是 46/46 OK。对当前 v0.3.1 树核验为 **34 OK / 14 FAILED**，
  失败项全是已记录的数据工作产物（11 个 `data/*.jsonl` + `manifest.json` + 2 个报告），
  `data/snapshot_candidate_triage.jsonl` 的哈希自首次追加后未再更新。结论：该文件只能证明「v0.3 源未被动过」，
  **不能**作为 v0.3.1 当前树的完整性校验；本版未重新生成校验和（重新生成会抹掉「哪些文件被改过」的记录），
  下游如需要当前树校验应另生成并保留此基线。
- 漏斗补全（`runs/triage_untriaged_unknown_2026-10-24/`）：`build_initial_triage.py` 的设计是「已选版仓库内的
  每个候选都有一行 triage，无证据者为 unknown/unresolved」，但 2026-10-22 构建时这些仓库还没有冻结快照，
  46 个目标冻结后其候选一直无行（562 条，其中 549 条属已选版仓库）。重跑 builder 到临时文件
  （`--out /tmp/initial_triage_now.jsonl --checked-at 2026-10-24T05:30:00Z`）→ 2613 行；**只追加**
  当前表中不存在的 549 个 candidate_id，全部为 `unknown`/`unresolved`，不回写 rebuild 对既有候选的判定
  （rebuild 与已应用表在 909 条上有分歧，因为它不知道后续范围/祖先/代码级工作）。逐行核对
  `snapshot_id == data/snapshots.jsonl` 的当前 `evaluation_target`，0 不匹配；涉 17 个仓库
  （72495579 239、70107786 65、1148753 51、17620347 44、24195339 38、2493904 31…）。
  备份 `runs/data_fixes/snapshot_candidate_triage.before_untriaged_unknown_2026-10-24.jsonl`（2064 行），
  追加行原文 `added_rows.jsonl`。结果：triage **2613** 行（unknown 708 → **1257**、其余计数不变，
  distinct id 2613）；已选版仓库内无 triage 行候选 549 → **0**，未选版仓库仍 13 条；
  draft 校验 0 error / 49 warning（warning 来自 coverage 的 unresolved 计数，与此无关）。
  这 549 行**不是核验结论**，与既有 unknown 同义，仍须源码/差异级复核。

## 2026-10-24 — 粗粒度 advisory 渲染修复：范围排除现在 693/693 可复现

- 接上一条「仍未解决的 3 条 rack 行」。根因确认：`discovery_v3/repo_advisories` 存的是 GitHub 渲染后的
  **扁平化区间**（多分支 advisory 被压成 `>= 0.4` / `>= 1.3.0` / `All`），修复版本另放在 `patched_versions`
  （`3.0.9.1, 2.2.8.1` 等）。单看该字段区间无上界，故包含冻结版本 3.1.13，GitHub 副本投
  `possible_affected_range`；同一 advisory 的 OSV 副本保留逐分支 `introduced`/`fixed`，证明 `above_upper`。
  `combine_votes` 让粗粒度副本否决了精确副本。
- `v031/scripts/triage_range_scope.py` 的修法（**不消费 `patched_versions` 造边界**，只做「冗余副本」判定）：
  1. `evaluate_ghsa` 在「所有可读 clause 只有下界、没有上界」且无不可读 clause 时，给 detail 打
     `coarse_range: true` 并附 `patched_versions`（有不可读 clause 则不打标，因为可能藏分支）；
  2. `evaluate_osv` detail 增加 `fixed_versions`（该副本 `fixed` 事件的版本集合）；
  3. `combine_votes` 仅在同一 advisory id 存在精确副本、且两侧修复版本集合按版本元组**完全相等**时，
     丢弃这条粗粒度投票；集合不等（多一条分支）、无精确副本、任一侧版本不可解析时保留投票。
     丢弃只会减少投票，不会凭空制造排除。
- 单测 100 → **113 条 OK**，新增 `CoarseRenderingTests` 7 条（等集合丢弃、多分支保留、无精确副本保留、
  精确副本为 possible 时仍胜出、`evaluate_ghsa` 打标、`evaluate_osv` 报 `fixed_versions`）。
- 复跑复核（`runs/triage_coarse_dup_2026-10-24/`，`rebuild.py` 复现方法）：**默认模式 693/693** 仍提出
  同样的排除、0 indeterminate、**0 possible**；strict 模式 689/693（剩下 4 条仍是已知的跨产品兄弟包，
  `openssl-src`、`jquery-rails`×2、`DisCatSharp`，默认模式全为 NA）。3 条 rack 行的每条记录正是
  预期的两票：OSV `proof=above_upper` + `fixed_versions`，v3 `coarse_range=true` + 相同 `patched_versions`。
  1434 候选上的 NA 提案总数 735 → **738**（+3 即 rack），其余不变。
- 未改动任何数据行；`data/snapshot_candidate_triage.jsonl` 未写。46 条未审计提案批次不受影响：3 个 rack
  候选在低侧批次应用前已是 `confirmed_not_affected`，本就不在该批次输入内；用修后生成器重跑同一输入，
  相对现表仍是**同样的 46 条**（无新增、无移除）。

## 2026-10-24 — 上界包含性修复：快照恰好落在修复版本时不再 unknown

- 复核新暴露的生成器缺陷：高位证明「快照高于每条上界」用 `cmp > 0` 处理所有上界，但 OSV 的 `fixed`
  （首个已修复版本）与 `limit`（排他上限）本身**不在**受影响区间内，NVD 的 `versionEndExcluding` 同理。
  于是当冻结 tag 恰好等于修复版本时（`v1.9.0`、`v1.25.5`、`curl-8_3_0` 等），生成器判
  `indeterminate` 而非排除。`last_affected`（含）与 `versionEndIncluding`（含）保持原语义。
- 修法：新增 `above_osv_upper(version, bound, kind)`（`fixed`/`limit` 用 `>=`，`last_affected`
  及未知 kind 用 `>` 保守处理）与 `above_inclusive_upper(version, bound, inclusive)`；
  `evaluate_osv` 现按每条 range 的 `upper_kind` 判定，`evaluate_nvd` 的 `upper` 改为
  `(bound, inclusive)` 二元组，exact CPE 与 `versionEndIncluding` 为含、`versionEndExcluding` 为不含。
  单测 113 → **117 条 OK**（新增 OSV `fixed` 等值、`last_affected` 含/不含、`limit` 等值、
  NVD 两种 end 边界共 4 条）。
- 只放宽、不收紧：已应用的 693 条范围排除仍 **693/693** 复现（默认模式，证据
  `runs/triage_fixed_release_2026-10-24/`，`rebuild.py` 同法），strict 仍 689/693（4 条跨产品兄弟包）。
  同一 1434 候选输入的 NA 提案 738 → 740。
- 对现表 1257 条 unknown 重跑默认模式：63 条 `not_affected_range` 提案（525 possible / 627 indeterminate /
  42 out_of_scope），其中 46 条即已在 `runs/triage_unblocked_2026-10-24/` 送审的批次，
  **新增 17 条**全部为「快照恰在修复版本」形态：gitea v1.25.5 14 条（GHSA/GO-2026-6333…6347 配对）、
  curl `CVE-2023-38039`（`versionEndExcluding 8.3.0`）、gin `GHSA-3vp4`（fixed 1.9.0）、
  plug `GHSA-468c`（五分支末支 `[1.19.0, 1.19.2)`）。已打包为
  `runs/triage_fixed_release_2026-10-24/proposals.jsonl`（含 `repository_full_name`）并送独立隔离审计；
  **未写入任何数据行**。

## 2026-10-24 — 三批审计落盘、裸版本读法撤回、生成器四处修复、OSV-by-alias 补证

- 三批独立隔离审计返回并落盘，只应用 CONFIRMED 行（`apply_range_triage.py --apply --reviewed-by`
  各指向对应 `AUDIT.md`）：
  - `runs/triage_unblocked_2026-10-24/`：46 条 claim → **36 CONFIRMED / 9 REJECTED / 1 INCONCLUSIVE**，
    应用 36 条。REJECTED 里 8 条是 gitea v1.25.5 的「裸版本号读成单点」假排除（实际 `[0, 1.27.0)`
    或 `[0, 1.26.3)` 含 1.25.5），1 条是 withdrawn advisory；INCONCLUSIVE 的 `adv3_7aa7ec319170401e`
    自身 affected/patched 两个字段互相矛盾。这 10 条保持 unknown。
  - `runs/triage_fixed_release_2026-10-24/`：17 条 → **17/17 CONFIRMED**，全部应用（gitea 14、curl、gin、plug）。
  - `runs/triage_git_range_2026-10-24/`：12 条 → **10 CONFIRMED / 2 INCONCLUSIVE**（PYSEC-2013-19、
    PYSEC-2013-21 的上游记录缺证据），应用 10 条。
  - 净变化：`confirmed_not_affected` 1212 → **1273**（+36+17+10−2，见下条撤回），`unknown` 1257 → **1196**；
    12 条未确认 claim 留在 unknown。
- 撤回 2 条已落盘排除（`runs/data_fixes/revert_bare_version_exclusions_2026-10-24.py`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_bare_version_revert_2026-10-23T213854Z.jsonl`）：
  vite `adv3_0fee4010849796dd`（GHSA-8g5g，"6.4.4"）与 flask `adv3_6e04d4b614fb9b14`（GHSA-4grg，"3.1.0"）。
  审计自己的读法仍支持排除，但该读法不再被任何可复现的证明形态支持；脚本守卫要求行仍是 NA、reviewer 是该
  审计、basis 点名 advisory，否则中止。两行 basis 写明「撤回不是声称存在漏洞」。
- 生成器修复（`v031/scripts/triage_range_scope.py`，单测 117 → **126 条 OK**）：
  1. `parse_clause` **拒绝把无运算符的裸版本号当边界**：GitHub 把 `<= 1.26.2` 渲染成 `1.26.2`、
     把修复版本单列在 `patched_versions`，旧逻辑读成 `=1.26.2` 使整段区间塌成一个点（gitea 六行、
     vite 一行）。裸版本既可能是单点也可能是扁平化后的开区间上界，不可区分，故不提供任何边界。
     原 `test_equality_clause_is_bounded_on_both_sides` 因此改写为断言 indeterminate；
     `test_explicit_equality_clause_still_parses` 保留显式 `=` 的双侧语义。
  2. `combine_votes` 的**不可读副本不再否决可读副本**：同一 advisory id 的一条副本完全不可读
     （如 discovery_v3 渲染）而另一条（OSV）可读并证明排除时，旧逻辑让不可读票拖成 indeterminate
     （vite GHSA-92r3 复现 790/792）；现在丢弃「同 id 存在可读副本」的不可读票，若该 id 处处不可读则
     仍保留其否决。新增 3 条 `CombineVotesTests`。
  3. `evaluate_osv` / `evaluate_nvd` 在 detail 里记录 `skipped_packages` / `skipped_products`
     （同记录里因包名不匹配而被跳过的兄弟包，如 tomcat `catalina` vs `embed-core`、snoopy），
     便于审计区分「记录不可读」和「记录读的是别的包」；`unsupported_ecosystem` 的 early-return
     detail 也补上 `record`。新增 2 条单测。
- 全量复现复核（`runs/triage_range_recheck_full_2026-10-24/`，`rebuild_full.py`）：把当前表里**全部**
  带范围证明的 817 行（723 `above_upper` + 94 `below_lower`）在 `/tmp` 副本中置回 unknown，
  跑两模式。**默认模式 817/817 全部重新提出、0 divergent**；strict 812/817，差的 5 条为跨产品兄弟包
  （`openssl-src`、jquery-rails ×2、`DisCatSharp`、spring-framework 的 GHSA-v596 命中 spring-security）。
  此前 ad hoc 的「807 条 / 802」数字不再引用，由本次可复现结果取代。
- OSV-by-alias 补证（`runs/osv_alias_2026-10-24/`）：317 条无结构化证据的 unknown 行，按公开别名从 OSV
  抓取四轮（round1 202 别名/116 记录；round2 82 条由 `DEBIAN-CVE-*` 派生的裸 CVE；round3 33 条
  `DSA-*`/`DLA-*`；round4 由 Debian 记录 `upstream` 字段派生的 38 个 CVE），缓存 230 条原始记录。
  `evaluate.py` 只读 `database_specific.extracted_events`，按 OSV 事件顺序判 membership，并要求记录
  `ranges[].repo` 指向本仓库；单版本抽取（`StandaloneSingleVersion` 或 `introduced==last_affected`）
  不能支撑 `below_lower`。结果 105 个候选取得本仓库记录：51 `possible` / 45 `exclusion` / 9 `unknown`；
  43 条排除提案（含 2 条 cJSON 单版本案例被规则丢弃）已打包 `proposals_exclusion.jsonl` 送独立审计，
  **未应用**；51 条区间命中用 `runs/data_fixes/apply_alias_possible_2026-10-24.py --apply` 移入
  `possible_affected`，脚本在落盘前从缓存重走事件、要求行仍 unknown、tag 未变、事件逐字存在，
  备份 `runs/data_fixes/snapshot_candidate_triage_before_alias_possible_2026-10-23T215127Z.jsonl`。
  其余 212 个候选没有任何可获取的版本证据（别名 404 或只有 GIT/发行版范围），保持 unknown。
  该批抓取脚本首版把 `DSA`/`DLA` 过滤掉并每轮覆盖同一 manifest，已改为 `--worklist/--manifest`；
  round1 的逐条状态因此丢失（缓存与 worklist 仍在，README 如实记录）。
- 未应用生成器 possible 提案统一落盘（`runs/data_fixes/apply_remaining_possible_2026-10-24.py`）：
  全量复核的默认模式对 524 条仍为 unknown 的行提出 `possible_affected_range`（快照落在某条已发布区间内），
  此前只应用 NA、这些正侧提案一直悬置。脚本从提案自己的证据重走 membership（OSV 事件顺序、GHSA clause
  合取、NVD `cpe_matches` 连同 `0.0.0` 无界哨兵），要求行仍 unknown、tag 未变、至少一条记录真的含 tag；
  **撤回/驳回的 advisory 一律跳过**——express 的 `adv3_087476da78c375b4`（GHSA-pj86，"not an actual
  vulnerability"）因此保持 unknown，不被抬成 possible。落盘 523 条，`possible_affected` 81 → **604**、
  `unknown` 1145 → **622**；备份
  `runs/data_fixes/snapshot_candidate_triage_before_remaining_possible_2026-10-23T215453Z.jsonl`。
  抽查 6 条（tokio 1.8.0、django 4.2.13、gitea v1.25.5、vite v5.0.11、cJSON v1.7.16、curl-8_3_0）
  逐条核对区间，均确实包含 tag。这一步只是把「区间命中」如实记成 possible，**不是漏洞确认**；
  其中 coarse 渲染（`<= 1.27.2`、`All versions`）造成的命中偏保守，需源码复核时优先看。
- 当前表：**2613** 行 = confirmed_affected 86 / confirmed_not_affected 1273 / possible_affected 604 /
  unknown 622 / duplicate 28；draft 校验 0 error / 49 warning（warning 为 coverage unresolved 计数），
  `pending_relevant_triage` 1226（= 604 + 622）。`CHECKSUMS.sha256` 仍未重生成（保留 v0.3 基线记录）。
- unknown 行的生成器侧提案与同源兄弟包（`runs/triage_unknown_na_2026-10-24/`）：817 行范围复核的默认模式
  输出里另含对仍为 unknown 的 622 行的提案——571 `indeterminate`、42 `out_of_scope_product`、8
  `not_affected_range`、1 `possible_affected_range`。那 1 条 possible 是已撤回的 express
  `adv3_087476da78c375b4`（GHSA-pj86 的粗粒度 `< 4.22.0` 命中；`apply_remaining_possible` 已按撤回跳过），
  保持 unknown。571 条 indeterminate 的阻塞归因：包不匹配 170、NVD 归属未定 161、other 155、
  包不匹配+生态不支持 107、事件不可读 19、生态不支持 1；**没有**任何一行是生成器完全看不到。
  8 条 NA 提案未被应用，已打包 `runs/triage_unknown_na_2026-10-24/` 送独立审计（`build_packet.py`
  在 scratch 上重跑 default/strict 两模式，拒绝对非 unknown 行打包）。
  - strict 对 8 条只保留 3 条 NA（symfony 1、django 2），5 条转 indeterminate（netty 3、tomcat 2）。
  - tomcat 两条是本批的关键反例：`below_lower` 只读取候选查询的 `tomcat-catalina`，而同一 OSV 记录里的
    `tomcat-embed-core`（同一源码树、同一 9.0.98 发布；Maven Central 两个 POM 的 `<url>` 同指
    tomcat.apache.org）带有 `[9.0.0.M1, fixed 9.0.98)`、`[9.0.40, fixed 9.0.69)` 等下界低于快照的分支。
    结论（9.0.98 等于 `fixed`，排他）大概率仍真，但「低于每一条下界」的证明形式为假，故不应用、不改
    basis，交审计裁定；若审计给出不同形式的证明，须另立证明再落盘。
  - netty 三条的 strict 分歧来自 `org.jboss.netty:netty` 的 `introduced: "0"`（无结束事件、无法解析的
    OSV 哨兵）与 GIT-only 块；候选自身包的 `[0,4.1.44)`、`[4.0.0,4.1.45)`、`[4.0.0,4.1.61.Final)`
    都严格低于 4.1.137。
  - symfony 的兄弟包 `symfony/html-sanitizer` 是同一 monorepo 组件的 subtree split，分支同为
    6.1/7.0/8.0，`v5.4.45` 低于全部下界；django 两条为 2013 年 advisory 的 `above_upper`，两份记录一致。
  - 反向证据：strict 在 angular/angular 19.2.15（`disc2_22f75256623aa38c50a68574`）上给出 possible，
    命中来自 `@angular/ssr`，npm registry 元数据的 repository 是 `github.com/angular/angular-cli`；
    `@nguniversal/common` 指向 angular/universal，均非本仓库，故该行**不**升为 possible，仍 unknown。
    这说明兄弟包必须先查包注册表的 repository 归属，不能按名字猜。
- 文档计数修正：`LIMITATIONS_V031.md` 第 3 节的表头仍是旧值（1212 / 1257 / 30），已改为
  1273 / 604 / 622 / 28；删除了一段遗留的「81 条 possible」重复段落（被 604 段取代）；
  「1257 条 unknown 重跑」改为「当时表中的 1257 条」，release 门槛段的 1257 改为 622。
- OSV-by-alias 排除批次审计与落盘（`runs/osv_alias_2026-10-24/audit/`）：独立审计逐条重抓 28 个别名、
  比对缓存与实时 OSV/NVD 记录（结构一致），对 43 条排除提案给出 **42 CONFIRMED / 1 REJECTED /
  0 INCONCLUSIVE**、总判 `APPLY_WITH_EXCLUSIONS`。`apply_confirmed.py` 只转换 CONFIRMED 条目为
  `apply_range_triage.py` 的 schema（补 snapshot_id、把 entries 展成 bounds），拒绝 REJECTED 与非
  unknown 行；dry-run 42/42 可应用后 `--apply`，`reviewed_by` 记录
  `independent audit 2026-10-24 (runs/osv_alias_2026-10-24/audit/AUDIT.md)`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_range_scope_2026-10-23T220428Z.jsonl`。
  计数：`confirmed_not_affected` 1273 → **1315**、`unknown` 622 → **580**（落盘的 42 条全部来自
  原 indeterminate 提案组，`out_of_scope` 42 条未变）。
  - 被拒的是 `disc2_a3f5e5512dbfb5d1ff940b26`（cJSON `v1.7.16`，CVE-2023-26819）：审计认为 OSV/NVD
    的 exact CPE 点 1.7.15 低估了真实范围——修复提交 `a328d65ad490b64da8c87523cbbfe16050ba5bf6`
    的提交信息点名该 CVE 且首见于 `v1.7.19`，`v1.7.16`/`v1.7.18` 仍含原解析代码，Debian 首个修复包为
    `1.7.18-3.1+deb13u1`。按规则**驳回排除 ≠ 确认受影响**，该行保持 unknown，不改审核等级；
    已列为下一次正向源码复核的优先候选（若确认，应按 positive 流程另立 review，而不是复用本次 verdict）。
  - 审计还确认：唯一 `below_lower`（CVE-2026-76956，`[2.8.2,2.8.4)`）的引入提交就是 `R_2_8_2` tag
    提交且非 `R_2_6_2` 祖先；CVE-2024-28757 的 `fixed: 2.6.2` 为开区间、`R_2_6_2` tag 提交即修复提交；
    26 条 Debian `DEBIAN-CVE-*`（ECOSYSTEM、无 repo）被 repository-match 正确忽略，其中
    `DEBIAN-CVE-2026-76956` 的 `[0, 2.9.0-1~deb13u1)` 若误当上游范围会错含 2.6.2。
- 8 条 unknown-NA 提案批次审计与落盘（`runs/triage_unknown_na_2026-10-24/`）：独立审计逐条重算并
  实查注册表，判 **6 CONFIRMED / 2 REJECTED / 0 INCONCLUSIVE**。`apply_confirmed.py` 只取 CONFIRMED、
  校验行仍为 unknown / repo_id 与 tag 未变、把 packet 丢失的 `snapshot_version` 按生成器同一解析补回、
  丢弃无可排序事件（discovery_v3 散文字段）的副本记录；dry-run 6/6 可应用后 `--apply`，
  `reviewed_by` = `independent audit 2026-10-24 (runs/triage_unknown_na_2026-10-24/audit/AUDIT.md)`，
  备份 `runs/data_fixes/snapshot_candidate_triage_before_range_scope_2026-10-23T221024Z.jsonl`。
  计数：`confirmed_not_affected` 1315 → **1321**、`unknown` 580 → **574**（django unknown 4 → 2）。
  - 确认：symfony `v5.4.45`（6.1/7.0/8.0 三条下界之下）、django `4.2.13` ×2（`fixed 1.5.2`/`1.4.6`
    之上，GHSA 与 PYSEC 两份副本一致）、netty `netty-4.1.137.Final` ×3（高于 4.1.44/4.1.45/4.1.61.Final；
    `org.jboss.netty:netty`、`io.netty:netty` 的 `introduced: "0"` 开区间块实为 GHSA `< 4.0.0` 的转换
    产物——`last_known_affected_version_range`、`versions[]` 与 Maven Central 最大版本均证实无 4.x/4.1.x
    发布——因此对 4.1.x tag 丢弃）。
  - 被拒：两条 tomcat `9.0.98`（CVE-2024-56337、CVE-2022-45143）。审计认定 `below_lower` **as stated**
    为假：同源 `tomcat-embed-core` 带 `[9.0.0.M1, fixed 9.0.98)`、`[8.5.83,8.5.84)`、`[9.0.40,9.0.69)`
    等下界低于 tag；但排除结论本身为真，正确论证是逐分支混合（9.0 分支等于排他性 fixed / 高于 fixed，
    10.1/11.0 分支低于下界）。生成器的对称规则只接受全 above_upper 或全 below_lower，无法表达混合
    证明，故两行保持 unknown、原 basis 不改写；下一步须给生成器加「逐分支混合证明 + 单测」并重新送审。
  - 审计方法记录：GitHub advisories API 因共享代理 IP 触发 403，改用 raw.githubusercontent.com 的
    advisory-database 副本与 OSV 复核（已在 `audit/AUDIT.md` 说明，不影响结论）。
- cJSON CVE-2023-26819 源码级复核（`runs/verification/cjson_CVE-2023-26819_v1716/`）：承接
  OSV-by-alias 审计把该行列为「正向复核优先项」的标记。全量 clone 到隔离 `/tmp`、v1.7.16 与 v1.7.19
  两个 worktree，harness 与脚本放在源码树外，ASan+UBSan 编译（GCC 13.3, glibc 2.39）跑 6 个载荷。
  结论：修复提交 `a328d65a`（提交信息明确 "This fixes CVE-2023-26819"）不是 `v1.7.16` 的祖先；
  `parse_number` 的 64 字节栈缓冲自 `749fefc`（2017-04-08）起存在，覆盖 1.7.15–1.7.18 全系列，
  公开 CPE 的 1.7.15 点确实低估范围。行为差异可复现：数组内 64 位整数的 advisory 载荷在 v1.7.16
  `parse_error`、v1.7.19 `parsed ok`，边界即 63 字符拷贝上限；整文档单数字时 v1.7.16 静默截断后
  `parsed ok`。但两种构建均无 ASan/UBSan 报告——循环在 i=63 停止并写终止符，无越界，advisory 所称
  DoS 未能复现（拒绝合法 JSON ≠ 拒绝服务）。因此**不升级为 confirmed_affected**，也未据公开区间
  判 not_affected；该行保持 unknown，双向理由写入 ROUND.md。
- 两库选版证据核查（`runs/unselected_repo_evidence_2026-10-24/`）：把已缓存的 13 条 OSS-Fuzz OSV
  记录（nlohmann/json 3 条、openssl/openssl 10 条，全部只有 GIT introduced/fixed 提交对）与稳定
  release tag 做祖先映射。`check_windows.py` 用 `git tag --contains` / `--merged` 的交集判定窗口
  （fixed 排他，恰在 fixed 的 tag 单列），稳定 tag 口径为 `v<M>.<m>.<p>`（json 44 个）与
  `openssl-<M>.<m>.<p>` + `OpenSSL_1_1_1x` / `OpenSSL_1_1_0x` / `OpenSSL_1_0_2x`（openssl 136 个，
  预发布不计）。结果：**0/13 个窗口内有稳定 tag**；每一行「包含 introduced 的稳定 tag」集合与
  「包含 fixed 的稳定 tag」集合完全相等（json 31/5/5，openssl 101/101/77/77/77/77/77/30/30/30），
  即没有稳定版本在漏洞窗口内发布。正对照（introduced=openssl-3.0.0^、fixed=openssl-3.0.1）能正确
  找出 openssl-3.0.0，证明方法本身有效。两库因此维持 needs_selection；修复之后的 tag 只是这些记录的
  负样本，不能用来满足「先有正样本再选版」。README 记录了口径、逐条窗口表与三条解锁路径。
- cJSON CVE-2023-53154 正向核验与 promote（`runs/verification/cjson_CVE-2023-53154_v1716/`、
  `runs/independent/cjson_CVE-2023-53154_v1716_round1/`）：这是首个由 `possible_affected`
  （「已发布区间包含冻结 tag」）经完整正向流程升为 `confirmed_affected` 的案例，三条候选行
  `disc2_42a2b668d6d1d627553d3f5d`/`disc2_84c9f51b7d1891828c9fa21b`/`disc2_43346aec2ac92ab900ce6358`
  同指 `DaveGamble/cJSON` 快照 `snap_d9525608880dc9e1`（v1.7.16，`cb8693b0`）。
  - 漏洞本体：`parse_object` 处理对象结尾逗号时先 `offset++` 再无边界检查地调用 `parse_string`，
    后者读 `buffer_at_offset(input_buffer)[0]`（cJSON.c:781）。只有调用方用 `cJSON_ParseWithLength`
    且缓冲区恰好无尾字节时越界读 1 字节（卷宗 harness：`malloc(len)` + `memcpy`，len=7 的
    `{"1":1,`）；`cJSON_Parse` 传 `strlen+1`，不触发。修复 `3ef4e4e730e5` 在 v1.7.18 加入
    `cannot_access_at_index(input_buffer, 1)`，回归测试 `826cd6f8`。
  - 卷宗 `dossier.json` 15 条证据（OSV/NVD/CVE v5/Debian 记录、tag 与祖先检查、fix diff、两版
    `cJSON.c`、issue #800、changelog、回归测试、独立 harness 与日志）。OSV GIT 的 `fixed`
    哈希 `acc76239` 是 v1.7.18 tag tip（只改 `CONTRIBUTORS.md`），不是根因修复；卷宗与 ROUND.md
    区分记录，release 边界 1.7.18 仍成立。NVD primary 5.5 与 CNA 2.9 的分歧按 NVD primary 落库。
  - 隔离独立复核：reviewer `independent-reviewer-cjson-CVE-2023-53154-deepseek-flash` 用自建 clone
    与自写脚本，clang 18.1.3 + gcc 13.3.0 双编译器红/绿（v1.7.16 ASan heap-buffer-overflow READ of
    size 1，v1.7.18/v1.7.19 `parse_error`），location `cJSON.c:1656-1660` 与卷宗重叠，
    `fields_verified` 九项全 true，grade A。裁定记录两处分歧：CVSS 2.9 vs 5.5、crash site 归因
    `parse_string` 而非 `parse_object`；两者均未改变受影响结论。
  - 落盘：`promote_verified_rows.py --apply` appended 1 vulnerability / 1 location / 1 review /
    31 evidence / 1 snapshot_vulnerability_status；三条 triage 行由 `possible_affected` 改为
    `confirmed_affected`（`vulnerability_id=CVE-2023-53154`，`review_method=source_code_review`）。
    备份 `runs/data_fixes/*_before_cjson_53154_2026-10-23T2230Z.jsonl`。
  - 计数：`confirmed_affected` 86 → **89**、`possible_affected` 604 → **601**、
    vulnerabilities/locations/reviews 106 → **107**、evidence 3685 → **3716**、
    status 77 → **78**、grade A 32 → **33**、`pending_relevant_triage` 1178 → **1175**。
    复算：2613 triage = 89 / 1321 / 601 / 574 / 28；draft 校验 0 error / 49 warning。
  - 队列同步：`runs/possible_review_queue_2026-10-24/build_queue.py` 按当前表重跑，604 → **601**
    （`range_precise` 414 / `range_coarse` 83 / `nvd_cpe` 25 / `alias_osv` 49 / `legacy_triage` 30；
    cJSON 21 → 18），README 记录这 3 行已由 promote 移出、其余未决行未被提升或排除。
- cJSON CVE-2023-50472 卷宗补齐但**未 promote**（`runs/verification/cjson_CVE-2023-50472_v1716/`）：
  卷宗、来源与红/绿包已备（v1.7.16 ASan SEGV at cJSON.c:408 `strlen`，UBSan "null pointer passed
  as argument 1"；v1.7.17 / v1.7.18 `result=(null)` 且 exit 0），但只有采集方复现，尚无独立裁定。
  补齐 `vulnerability.vulnerability_id` 后以 schema-probe verdict 做 dry-run，输出
  `promoted: true`（29 evidence、grade B 因无 `reproduction_reference`）且无 schema 错误；该 probe
  在 `/tmp` 使用后即删除，**不是** review，不得据此落盘。CVE-2024-31755（同 `strlen` 行的第二参数
  NULL 解引用、修复 `7e4d5da`）同样只记录、不 promote：advisory 范围只列 v1.7.17，若按现有
  status-row 模板落库会写出对该快照为假的范围陈述。

## 2026-10-24 — cJSON CVE-2023-50472 独立复核、A 级晋级；3 条重复候选链回既有记录

- cJSON CVE-2023-50472 走完「卷宗 → 隔离独立裁定 → promote → 改写 triage」全链
  （`runs/verification/cjson_CVE-2023-50472_v1716/`、
  `runs/independent/cjson_CVE-2023-50472_v1716_round1/verdict.json`）：
  - 漏洞本体：`cJSON_SetValuestring` 只检查 `cJSON_String` / `cJSON_IsReference` 位，随后
    对 `object->valuestring == NULL` 的字符串项调用 `strlen` / `memcpy`，崩溃在 `cJSON.c:408`。
    采集方复现（v1.7.16 UBSan 「null pointer passed as argument 1」+ ASan SEGV；v1.7.17/v1.7.18
    返回 `NULL` 且 exit 0）与独立复核结果一致。
  - 隔离 reviewer `independent-reviewer-cjson-CVE-2023-50472-deepseek-flash`（≠ 卷宗
    `prepared_by`）用自建 clone、自写 harness，clang 18.1.3 与 gcc 13.3.0 双编译器红/绿，
    核对同一 `cb8693b0` 提交与 `cJSON.c:404-412` `cJSON_SetValuestring`（与卷宗 404/408 重叠），
    `fields_verified` 九项全 true、`reproduction_reference` 齐备，`grade_recommendation: A`，
    裁定时间 `2026-10-23T22:33:52Z`。
  - 独立裁定把受影响窗口收窄为 `>=1.7.13,<1.7.17`：引入提交 `6b35f1c5`（2020-03-24）首见于
    v1.7.13，v1.7.13–v1.7.16 该函数字节级相同（sha256 `0bdc48e0f04dd194…`）。卷宗已按此修正
    `affected_packages[0].affected_range`，并记录 OSV 的点范围与实测窗口的区别。
  - 落盘：`promote_verified_rows.py --apply` appended 1 vulnerability / 1 location / 1 review /
    29 evidence / 1 snapshot_vulnerability_status（`applied_at 2026-10-23T22:35:11Z`，grade A）。
    两条 triage 候选 `disc2_56023e86547f205b18fc6b22` / `disc2_881253322ce67b2c934e3401` 由
    `possible_affected` 改为 `confirmed_affected`（`apply_promoted_candidate_2026-10-24.py`，
    备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_2026-10-23T223521Z.jsonl`）。
  - 未采用 CVE-2024-31755：同 `strlen` 行第二参数的 NULL 解引用、修复 `7e4d5da`，advisory 范围只列
    v1.7.17；按现有 status-row 模板落库会写出对该快照为假的范围陈述，故只记录、不晋级。
- 3 条候选行是与同快照已确认漏洞重复的 discovery，此前停在 `possible_affected`，与同名 advisory 的
  已确认行自相矛盾（cJSON v1.7.16 / CVE-2023-50471 1 条；libexpat R_2_6_2 / CVE-2024-45490 2 条）。
  `runs/data_fixes/link_duplicate_candidates_to_verified_2026-10-24.py` 在守卫下（当前 decision 必须是
  `possible_affected`、快照/repo/commit 与漏洞行一致、队列 record 等于该 CVE）改为
  `confirmed_affected` 并填 `vulnerability_id`；未新做复核、未改任何 review 等级，备份
  `runs/data_fixes/snapshot_candidate_triage_before_duplicate_link_2026-10-23T223434Z.jsonl`。
- 另有一个为 CVE-2023-50471 新建的完整卷宗包（dossier/sources/harness/复现日志），在 promote dry-run
  报 conflicts 时发现该 CVE 已有 grade B 的独立复核（`runs/independent/cjson_CVE-2023-50471_round1/`，
  location 2263-2290），为避免覆盖既有记录，**整包删除**而非晋级；该工作不计入本次数据集变更。
- 计数（复算）：vulnerabilities/locations/reviews 107 → **108**（A 33 → **34**，B 74）、
  evidence 3716 → **3745**、status 78 → **79**、评测目标正样本 78 → **79**（45 B + 34 A）；
  triage 2613 = confirmed_affected 89 → **94** / confirmed_not_affected 1321 / possible_affected
  601 → **596** / unknown 574 / duplicate 28；`pending_relevant_triage` 1175 → **1170**。
  队列按当前表重跑（`runs/possible_review_queue_2026-10-24/build_queue.py`）：596 =
  `range_precise` 414 / `range_coarse` 83 / `nvd_cpe` 24 / `alias_osv` 45 / `legacy_triage` 30；
  cJSON 18 → **15**（10 alias / 5 NVD），libexpat 38 → **36**（34 alias）。
- 校验：`validate_dataset.py --draft` **0 error / 49 warning**（`known_positives 79`、
  `triaged_candidates 2613`、`pending_relevant_triage 1170`）；`v031/tests` **126 tests OK**。
  仍未声明 `PASS_KNOWN_SWEEP`、未完成两库选版、未达 release 门槛。

## 2026-10-24 — cJSON CVE-2025-57052 独立复核与 A 级晋级；CVE-2016-10749 排除提案送审

- CVE-2025-57052 @ cJSON v1.7.16 走完「卷宗 → 隔离独立裁定 → promote → 改写 triage」全链
  （`runs/verification/cjson_CVE-2025-57052_v1716/`、
  `runs/independent/cjson_CVE-2025-57052_v1716_round1/verdict.json`）：
  - 缺陷在 `cJSON_Utils.c:285`：`decode_array_index_from_pointer` 的数字循环第二半写死
    `pointer[0] <= '9'`，任何 `>= '0'` 的字节都被折进下标（`/1:` → 20，`/1A` → 27）；
    修复 `74e1ff4`（2025-09-05，PR #957）改为 `pointer[position] <= '9'`，首见于 v1.7.19。
    引入提交 `d67b008`（2017-04-12）首见于 v1.5.0，规范范围 `>=1.5.0,<1.7.19`。
  - 采集方红/绿：harness 建 21 元素数组、指针 `/1:`；v1.7.16 gcc/clang 均
    `result=element[20]`，v1.7.19 均 `result=NULL`，exit 0。
  - 隔离 reviewer `independent-security-reviewer:deepseek-flash:rv57052`（≠ `prepared_by`）
    自建 clone、自写 harness：v1.7.16 把 `/1A` 解析为下标 27（GetPointer 返回 element 27、
    JSON Patch add/remove 作用于 27），v1.7.19 拒绝（NULL，patch status 11/13）；
    逐 tag 扫描确认缺陷存在于 v1.5.0–v1.7.18、修复只在 v1.7.19（tag `c859b25`，CMake
    VERSION 1.7.19），`fields_verified` 九项全 true，`grade_recommendation: A`。
  - 诚实差异（已写入卷宗、ROUND.md 与 LIMITATIONS）：库内消费方
    （`get_array_item`/`insert_item_in_array`/`detach_item_from_array`）只遍历链表，
    ASan+UBSan 在精确堆分配下两版均无报告，实际效果是**解析器差异**（CWE-129）；
    advisory 的 CWE-125 /「out-of-bounds access」与 CISA-ADP 9.8 只记录为已发布值、未获背书。
    博客 PoC `/0A` 在两版都被既有前导零守卫拒绝；同函数的 `size_t` 溢出
    （`/18446744073709551617` 回绕）在 v1.7.19 仍在，属 open PR #1103，不在本行范围。
  - 落盘：`promote_verified_rows.py --apply` appended 1 vulnerability / 1 location / 1 review /
    26 evidence / 1 snapshot_vulnerability_status（`applied_at 2026-10-23T22:51:05Z`，grade A）。
    四条候选 `disc2_3d5c9af0179d9a4e37f348d4` / `disc2_a5fb8eabc9227cb5e7c887cc` /
    `disc2_c18db19ad5c1923552dcc607` / `disc2_302ad77a98f695fc3045f169` 由
    `runs/data_fixes/apply_promoted_candidate_57052_2026-10-24.py` 改为 `confirmed_affected`
    （守卫：当前 decision / 快照 / repo / commit / advisory 引用 / 漏洞行逐项核对；默认 dry-run；
    备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_candidate_57052_2026-10-23T225107Z.jsonl`）。
- CVE-2016-10749 @ cJSON v1.7.16 的 `confirmed_not_affected` 提案已打包
  （`runs/na_proposal_cjson_CVE-2016-10749_2026-10-24/`），隔离审计返回 **REJECTED**，
  **未落盘**，该候选 `disc2_cbbf645dec334f9187b6897a` 仍为 `possible_affected`：
  - 提案两层论证：(1) OSV GIT fixed 事件 `94df7724`（2016-10-02「fix buffer overflow (#30)」）与
    `0d10e279`（2016-11-11）均是 v1.7.16 的祖先，更早的加固 `a167d9e3`（2017-05-10）首见于
    v1.5.2；(2) v1.7.16 代码 `cJSON.c:790` 已改为先判边界再累加、`:795` 拒绝尾随反斜杠、
    `:805` 拒绝缓冲末尾，对应 2016 年两处修复的行为。
  - 审计（隔离在 `/tmp/na10749`，自建 clone）确认：advisory 触发串在 v1.7.16 已不再越界
    （gcc/clang ASan，200k 随机 + 597,871 条穷举输入零报告；对照组能触发，harness 有效）；
    三个提交都在快照祖先链上。但审计预先声明「快照上存在真实 over-read 即否决 NA」，
    并找到同一函数另一条仍在的越界读——`{"1":1,` 经 `cJSON_ParseWithLength` 在 v1.7.16/1.7.17
    触发 `heap-buffer-overflow`（`cJSON.c:781`，即已确认的 CVE-2023-53154，`3ef4e4e` 在 v1.7.18
    修复）。故按规则判 REJECTED。
  - 处理方式：不覆盖审计结论、不做「换问法再送审」；审计原文与全部日志归档进提案包
    （`audit_verdict.json`、`audit_logs/`），README 如实区分「advisory 触发已死」与
    「快照整体仍有越界读」两件事。`apply_audited_na.py` 未执行。
- 计数（复算）：vulnerabilities/locations/reviews 108 → **109**（A 34 → **35**，B 74）、
  evidence 3745 → **3771**、status 79 → **80**、评测目标正样本 79 → **80**（45 B + 35 A）；
  triage 2613 = confirmed_affected 94 → **98** / confirmed_not_affected 1321 / possible_affected
  596 → **592** / unknown 574 / duplicate 28；`pending_relevant_triage` 1170 → **1166**。
  队列按当前表重跑（`runs/possible_review_queue_2026-10-24/build_queue.py`）：592 =
  `range_precise` 414 / `range_coarse` 83 / `nvd_cpe` 23 / `alias_osv` 42 / `legacy_triage` 30；
  cJSON 15 → **11**（7 alias / 4 NVD）。
- 校验：`validate_dataset.py --draft` **0 error / 49 warning**（`known_positives 80`、
  `triaged_candidates 2613`、`pending_relevant_triage 1166`）。
  仍未声明 `PASS_KNOWN_SWEEP`、未完成两库选版、未达 release 门槛。

## 2026-10-24 — gitea GHSA-7wvc-rvp7-w99x 卷宗（LFS 子动词绕过），送隔离复核

- 在 possible 队列里挑出 gitea 集群（80 条 `range_precise`）中下界明确、修复已发布的
  `disc2_3d2d1a1ee5792687960294ae`（`GHSA-7wvc-rvp7-w99x` / `CVE-2026-58423` /
  `GO-2026-6046`，快照 `snap_bd8b4ed626b39794`，tag `v1.25.5`）。
- 卷宗 `runs/verification/gitea_GHSA-7wvc-rvp7-w99x_v1.25.5/`：
  - 漏洞路径：`cmd/serv.go:115-132` `getAccessMode` 对未知 LFS 子动词落到
    `perm.AccessModeNone`（0），生产模式下 `PanicInDevOrTesting` 只记日志不 panic
    （`modules/setting/setting.go:239-243`）；`routers/private/serv.go:319-364` 的
    `userMode < mode` 在 `mode==0` 时恒假，私有仓库放行；`cmd/serv.go:264-286` 以原始
    子动词作 `Op` 铸造 LFS JWT，`services/lfs/server.go:611-615` 只在写操作校验 `Op`，
    下载侧接受该令牌。
  - 范围：OSV GHSA/Go 都是 `introduced 1.23.0, fixed 1.26.3`；逐 tag 扫描证实
    `getAccessMode` 首见于 v1.23.0（v1.22.6 无此函数），裸 `AccessModeNone` 回落到
    v1.26.2 为止，v1.26.3 起改为 `(mode, ok)`。
  - 修复：release 分支 `8f4b7ebb`（#38015）只在 v1.26.3/v1.26.4；main 分支 `42513398`
    首见 v1.27.0；v1.25.5 之后没有 1.25.x tag，无回移。
  - 评分：CVSS 3.1 7.7 HIGH（NVD Secondary，向量与 GitHub advisory 一致），CWE-287。
  - 局限：采集方未做动态复现；范围下界未逐一构建中间 release；Go 记录 UNREVIEWED。
- 生成器 `build_dossier.py` 对 `sources/` 每个产物做 sha256 断言后再写 `dossier.json`
  （9 条证据）；schema-probe dry-run（`/tmp` 用后即删，**不是** review）报
  `promoted: true`、无 schema 错误。
- 已派隔离 reviewer（只看 `/tmp/rv7wvc`、自建 clone、不读本仓库），等裁定；
  在裁定返回前不改 `data/`、不承诺该行会晋级。

## 2026-10-24 — gitea GHSA-hg5r-vq93-9fv6 卷宗（Artifacts V4 HMAC 歧义），送隔离复核

- 同一 gitea 集群里再取一条 `range_precise`：`disc2_fad8afe3a4f3105bf6b45699`
  （`GHSA-hg5r-vq93-9fv6` / `CVE-2026-58426` / `GO-2026-6060`，快照
  `snap_bd8b4ed626b39794`，tag `v1.25.5`，commit `f913d90ab6`）。
- 卷宗 `runs/verification/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5/`：
  - 漏洞路径：`routers/api/actions/artifactsv4.go:162-170` 的 `buildSignature` 把
    `endpoint`/`expires`/`artifactName` 与十进制 `taskID`/`artifactID` 裸拼后做 HMAC，
    无分隔符、无长度前缀，不同元组可拼出同一段字节；`154-157` 的
    `UploadArtifact`/`DownloadArtifact` 只挂 `ArtifactV4Contexter()`，不要求登录；
    `verifySignature`（`222-243` 重算、`249` 按 URL 的 `taskID` 取任务）之后，
    `uploadArtifact`（`347-373`）与 `downloadArtifact`（`576-583`）按 URL 选中的
    run/attempt + `artifactName` 取产物，不按签名里的 `artifactID` 绑定。
  - 范围：OSV GHSA/Go 都是 `introduced 1.22.0, fixed 1.26.2`；逐 tag 验证
    `artifactsv4.go` 在 v1.21.11 不存在、v1.22.0 起存在。
  - 修复：`1c2d5e9b`（PR #37707 的回移 #37795）只在 v1.26.2/v1.26.3/v1.26.4；
    新增 `modules/actions/artifacts.go` 的 `BuildSignature`（tag + 字符串长度前缀 +
    定宽整数），同时改 `routers/api/v1/repo/action.go`，并加回归测试；
    v1.25.5 的 `modules/actions/artifacts.go` 无 `BuildSignature`（已摘录）。
  - 评分：CVSS 3.1 9.6 CRITICAL（NVD Secondary 且 `vulnStatus=Deferred`；GitHub
    advisory 同向量并把 OSV severity 记为 CRITICAL），CWE-347；
    OSV 详情自带动态 PoC，记录 `v1.25.5 f913d90ab6 reproduced dynamically`。
  - 局限：采集方未复现该 PoC；范围下界只验证端点 tag 的文件存在性；Go 记录 UNREVIEWED。
- 生成器 `build_dossier.py` 对本包 `sources/` 每个产物做 sha256 断言后再写
  `dossier.json`（8 条证据，修复 patch 取完整提交的 4 个文件）；schema-probe dry-run
  （`/tmp` 用后即删，**不是** review）报 `promoted: true`、28 条证据、grade B、无 schema 错误。
- 已派第二个隔离 reviewer（只看 `/tmp/rvhg5r`、自建 clone、不读本仓库与第一个 reviewer
  的目录），等裁定；在裁定返回前不改 `data/`、不承诺该行会晋级。

## 2026-10-24 — django CVE-2024-42005 卷宗（values() JSON key SQL 注入），送隔离复核

- possible 队列里 django 集群共 43 条 `range_precise`（快照 4.2.13 /
  `snap_516aa9971dd9509d`）。先做只读普查：43 条全部在 OSV 范围内、31 条带 commit
  引用、没有任何修复 commit 是 4.2.13 的祖先；9 条既有 django 正样本与这 43 条无别名重叠。
- 取 `disc2_36f78bd1912f0d1afe514278`（`GHSA-pv4p-cwwg-4rph` / `CVE-2024-42005` /
  `PYSEC-2024-70`）建卷宗 `runs/verification/django_CVE-2024-42005_4213/`：
  - 漏洞路径：`django/db/models/query.py:1311-1319` 的 `values()`/`values_list()` 把字段名
    原样交给 `_values()`（`1308` → `query.set_values(fields)`）；
    `django/db/models/sql/query.py:2411-2436` 的 `set_values()` 用
    `field_names = list(fields)` 保留字符串，`2460-2461` 交给 `add_fields()` 生成 SELECT
    别名；同一文件 `1123-1128` 有 `check_alias()` 却从未被 `set_values()` 调用。
    带 JSONField 的构造 key 因此把引号/分号带进别名。
  - 范围：OSV PyPI 4.2 线 `introduced 4.2, fixed 4.2.15`（并行 5.0 线 `< 5.0.8`）；
    tag 4.2.13 = `c2845b37` → `3bf46e2e`（tree `31f1034a`），4.2.14 = `98cf264c` 同样缺修复。
  - 修复：`f4af67b9`（`stable/4.2.x`，首见 4.2.15 且只在 4.2.15+）与 `32ebcbf2`
    （`stable/5.0.x`，首见 5.0.8）；修复在 `set_values()` 的 `if fields:` 后加
    `for field in fields: self.check_alias(field)`，并加 JSON 字段回归测试与 4.2.15 发布说明。
  - 评分：NVD Primary 7.3 HIGH（`C:L/I:L/A:L`）；NVD Secondary（GitHub CNA）9.8
    （`C:H/I:H/A:H`）；OSV/GHSA 向量 `C:H/I:H/A:N`——三处分歧，卷宗记 NVD Primary 并写明。CWE-89。
  - 局限：采集方未跑回归测试；利用需要应用把不可信字段名转交 `values()`/`values_list()`。
- 生成器 `build_dossier.py` 对本包 `sources/` 每个产物做 sha256 断言后再写
  `dossier.json`（9 条证据）；schema-probe dry-run（`/tmp` 用后即删，**不是** review）
  报 `promoted: true`、29 条证据、grade B、无 schema 错误。
- 已派第三个隔离 reviewer（只看 `/tmp/rv42005`、自建 clone、不读本仓库），等裁定；
  在裁定返回前不改 `data/`、不承诺该行会晋级。

## 2026-10-24 — django CVE-2024-39329 卷宗（不可用密码计时枚举），送隔离复核

- 同一 4.2.13 快照再取 `disc2_14765a081146e98aa8c1500a`（`GHSA-x7q2-wr7g-xqmf` /
  `CVE-2024-39329` / `PYSEC-2024-57`）建卷宗
  `runs/verification/django_CVE-2024-39329_4213/`：
  - 漏洞路径：`django/contrib/auth/backends.py:40-53` 的 `ModelBackend.authenticate()`
    只为不存在用户补一次默认哈希（#20760），存在用户走 `user.check_password()`；
    `django/contrib/auth/hashers.py:46-47` 的 `check_password()` 对
    `password is None or not is_password_usable(encoded)` 直接 `return False`
    （`49-54` 的未知 hasher 分支同样立即返回），因此「存在但密码不可用」的登录响应
    快于「不存在」账号，可远程枚举。
  - 范围：OSV PyPI 4.2 线 `introduced 4.2, fixed 4.2.14`（并行 5.0 线 `< 5.0.7`）；
    tag 4.2.13 = `3bf46e2e`（tree `31f1034a`），4.2.14 = `bfe7062d` → `98cf264c`
    （tree `eb3c76d8`）。
  - 修复：`156d3186`（`stable/4.2.x`，首见 4.2.14）与 `07cefdee`（`stable/5.0.x`，
    首见 5.0.7）；把早退条件提成 `fake_runtime`，为真时先
    `make_password(get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH))` 再返回，
    并加 `test_check_password_calls_make_password_to_fake_runtime` 与 4.2.14 发布说明。
  - 评分：NVD 只有 Secondary（GitHub CNA `134c704f`）5.3 MEDIUM
    `C:L/I:N/A:N`，无 Primary；OSV 同向量、CVSS 4.0 `VC:L`。CWE-208。
  - 局限：采集方未做计时测量；只声称顺序关系（不可用时更快），不声称毫秒差。
- 生成器 `build_dossier.py` 对本包 `sources/` 每个产物做 sha256 断言后再写
  `dossier.json`（9 条证据）；schema-probe dry-run（`/tmp` 用后即删，**不是** review）
  第一次因 `severity.level="moderate"` 被 schema 拒绝，改为 `"medium"` 后报
  `promoted: true`、29 条证据、grade B。
- 已派第四个隔离 reviewer（只看 `/tmp/rv39329`、自建 clone、不读本仓库），等裁定；
  在裁定返回前不改 `data/`、不承诺该行会晋级。

## 2026-10-24 — gitea GHSA-hg5r-vq93-9fv6 独立复核 A 级，promote 并改写 triage

- 隔离 reviewer `rvhg5r-independent-reviewer-2026-10-23` 返回 `confirmed_affected`，
  grade **A**：`buildSignature`（`routers/api/actions/artifactsv4.go:162-170`）把
  endpoint/expires/artifactName/taskID/artifactID 直接拼接做 HMAC-SHA256；
  `verifySignature`（`:222-266`）信任 URL 里的 taskID/artifactName、丢弃签过名的
  artifactID；该路由组只用不鉴权的 `ArtifactV4Contexter`。reviewer 用 Go 1.24.6
  做了原语级红/绿：v1.25.5 的两组元组生成同一 HMAC 且伪造 URL 通过验证器
  （negative control 失败），v1.26.2 的 `actions.BuildSignature`（域名标签 + 8 字节
  小端长度前缀）签名不同。分歧已随 verdict 保存：advisory 行号是主干行号（本 tag
  偏移 2–3 行）、五字段形式自 v1.22.4 才有、`1c2d5e9b` 是 release/v1.26 backport
  （主干 `552c29a25`）、AC:L 需目标任务 Running。
- `promote_verified_rows.py --apply`：1 vulnerability / 1 location / 1 review /
  28 evidence / 1 status，grade A，warnings 只有 dossier 状态措辞。
- verdict、NOTES、sources 与 repro 已从 `/tmp/rvhg5r` 复制到
  `runs/independent/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1/`，并用
  `runs/data_fixes/persist_independent_verdicts_2026-10-24.py`（守卫：旧路径、sha256
  一致、reproduction 目录存在）把 review 行的 `independent_verdict_path` 改为仓库相对路径。
- triage 行 `disc2_fad8afe3a4f3105bf6b45699` 由
  `runs/data_fixes/apply_promoted_candidate_hg5r_2026-10-24.py`（守卫：decision、
  snapshot、repo、advisory 引用）从 `possible_affected` 改为 `confirmed_affected`，
  备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_2026-10-23T231020Z.jsonl`。

## 2026-10-24 — django CVE-2024-42005 独立复核 B 级，promote 并改写 triage

- 隔离 reviewer `rv42005-independent-reviewer` 返回 `confirmed_affected`，grade **B**。
  除源码复核外做了红/绿：把修复的 tests-only hunk 打到 4.2.13，回归测试
  `test_values_expression_alias_sql_injection_json_field` FAIL（ValueError 未抛），
  4.2.15 通过；另实测 4.2.13 编译出
  `AS "data__injected_name" from "expressions_company"; --"` 并经 DB cursor 执行成功。
  评 B 的理由：裸 `values(field)`/`values_list(field)` 不注入，必须在 values 后再叠加
  聚合注解才会经 `set_group_by(allow_aliases=True)` 把原始字段串带进 annotations；
  回归测试只断言抛 `ValueError`，验证的是缓解措施而非完整利用链。
- 分歧（随 verdict 保存）：可达性被 advisory 夸大；9.8 的来源是 CISA-ADP
  （`134c704f`）而非卷宗写的 GitHub CNA——卷宗措辞待统一，本行按 NVD Primary 7.3 记录；
  MySQL 需反引号 payload，SQLite/PostgreSQL/Oracle 用双引号。
- `promote_verified_rows.py --apply`：1 vulnerability / 1 location / 1 review /
  29 evidence / 1 status，grade B。
- verdict 等已复制到 `runs/independent/django_CVE-2024-42005_4213_round1/` 并由同一
  persist 脚本改指；triage 行 `disc2_36f78bd1912f0d1afe514278` 由
  `runs/data_fixes/apply_promoted_candidate_django_2026-10-24.py` 改为
  `confirmed_affected`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_2026-10-23T231054Z.jsonl`。
- 复算：111 vulnerabilities / 111 locations / 3828 evidence / 111 reviews /
  82 status；reviews A 36 / B 75；triage 2613 = confirmed_affected 100 /
  confirmed_not_affected 1321 / possible_affected 590 / unknown 574 / duplicate 28；
  pending 1164；draft 校验 0 error / 49 warning。possible 队列重跑为 591
  （`range_precise` 413 / `range_coarse` 83 / `nvd_cpe` 23 / `alias_osv` 42 /
  `legacy_triage` 30），README 与 HANDOFF/LIMITATIONS 计数同步。

## 2026-10-24 — django CVE-2024-38875 卷宗（urlize 括号二次方裁剪），送隔离复核

- possible 队列再取 `disc2_051d93d5bd86570c8437b5dd`（`GHSA-qg2p-9jwr-mmqf` /
  `CVE-2024-38875` / `PYSEC-2024-56`）建卷宗
  `runs/verification/django_CVE-2024-38875_4213/`：
  - 漏洞路径：`django/template/defaultfilters.py:370-385` 的 `urlize`/`urlizetrunc`
    → `django/utils/html.py:390-393` → `Urlizer.__call__`（250-273）→ `handle_word`
    （276-291，含 `.`/`@`/`:` 的词）→ `trim_punctuation`（333-367）。后者在 fixpoint
    循环里每轮对整词调用 `middle.count(closing)`/`count(opening)`，每轮只从两端各剥
    一个括号，N 个括号即 O(N²) 时间与分配。
  - 范围：OSV PyPI 4.2 线 `introduced 4.2, fixed 4.2.14`（显式列出 4.2.13；并行 5.0 线
    `< 5.0.7`）；tag 4.2.13 = `c2845b37` → `3bf46e2e`（tree `31f1034a`），4.2.14 =
    `bfe7062d` → `98cf264c`（tree `eb3c76d8`）。
  - 修复：`79f36876`（`stable/4.2.x`，首见 4.2.14）与 `72856446`（`stable/5.0.x`，
    首见 5.0.7）；新增 `CountsDict` 缓存计数、`cached_property` 缓存标点集合、批量
    `lstrip`/`rstrip`，并加 6 条 20 万字符回归输入与 4.2.14 发布说明。
  - 评分：NVD 只有 Secondary（`134c704f`）7.5 HIGH `A:H`，无 Primary；OSV 同向量、
    CVSS 4.0 `VA:H`。CWE：OSV CWE-130/CWE-770，NVD 只有 CWE-130。
  - 局限：未做时间/内存实测；可达性要求应用把攻击者可控文本交给过滤器且输入保持为
    单个词（不含空白/引号）并同时含括号与 `.`/`@`/`:`；candidate 行仍带 3.0.2 旧结论。
- 生成器断言全部通过后写出 `dossier.json`（10 条证据）；schema-probe dry-run
  （`/tmp/probe38875` 用后即删，**不是** review）报 `promoted: true`、29 条证据、
  grade B、无 schema 错误。
- 已派第五个隔离 reviewer（只看 `/tmp/rv38875`、自建 clone、不读本仓库），等裁定；
  在裁定返回前不改 `data/`、不承诺该行会晋级。

## 2026-10-24 — 仍待裁定

- 当前没有已派出、未返回的 reviewer。（`GHSA-7wvc-rvp7-w99x`、`CVE-2024-39329` 与
  `CVE-2024-38875` 均已在后续小节 promote。）

## 2026-10-24 — CVE-2024-39329 与 GHSA-7wvc-rvp7-w99x promote（均 A 级）

- `CVE-2024-39329`（django 4.2.13，不可用密码的计时枚举）：隔离 reviewer
  `rv39329-independent-reviewer` 返回 `confirmed_affected` / **A**，实测 4.2.13 与
  4.2.14 的失败路径耗时差约 715×（两次重复运行，`reproduction/timing_*.json`）。
  裁定记录根因分歧：reviewer 认为根因在 `hashers.check_password` 对 unusable password 的
  快速返回，而非 `backends.authenticate`；`location` 已对齐到
  `django/contrib/auth/hashers.py:46-47`（与卷宗 location 同文件同行段），
  verdict sha256 `373b9dc7…`。
- `GHSA-7wvc-rvp7-w99x`（gitea 1.25.5，LFS SSH 子命令鉴权绕过）：隔离 reviewer 返回
  `confirmed_affected` / **A**，用真实 gitea 服务器红/绿（v1.25.5 越权读写 LFS 对象成功，
  1.26.3 被拒）；根因 `cmd/serv.go:131` 返回 `AccessModeNone` 而
  `routers/private/serv.go:352` 用 `userMode < mode` 比较。verdict 补正 schema 字段后
  sha256 `4997de82…`。
- 两次 `promote_verified_rows.py --apply`：各 1 vulnerability / 1 location / 1 review /
  29 evidence / 1 status，grade A。
- verdict 与复现材料复制到 `runs/independent/django_CVE-2024-39329_4213_round1/`、
  `runs/independent/gitea_GHSA-7wvc-rvp7-w99x_v1.25.5_round1/`；review 行由
  `runs/data_fixes/persist_independent_verdicts_round2_2026-10-24.py` 改指（守卫 old path、
  保留副本 sha256 一致、reproduction 目录存在），备份
  `runs/data_fixes/reviews_before_verdict_paths_round2_2026-10-23T231500Z.jsonl`。
- triage 行由 `runs/data_fixes/apply_promoted_candidate_round2_2026-10-24.py` 改为
  `confirmed_affected`（dry-run 后 apply，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round2_2026-10-23T231509Z.jsonl`）：
  `disc2_14765a081146e98aa8c1500a` → CVE-2024-39329；`adv3_637ca5637354216a` 与
  `disc2_3d2d1a1ee5792687960294ae` → GHSA-7wvc-rvp7-w99x；另发现并修掉 hg5r 首次改写的
  遗漏 `adv3_d931ecfcc9a09dd2`（同快照、同 advisory，仍停在 possible）。全表扫描
  「possible 行是否引用同快照已 promote 漏洞」结果由 4 条降为 0。
- 来源标注纠正：NVD `134c704f` 是 CISA-ADP 容器，不是 GitHub CNA。42005 的数据行与更早的
  CVE-2024-39330 行仍写错，由 `runs/data_fixes/fix_cisa_adp_attribution_2026-10-24.py`
  （守卫 source_url 与唯一子串）改为「CISA-ADP 容器（向量由 GitHub CNA 发布）」，
  备份 `runs/data_fixes/vulnerabilities_before_cisa_adp_fix_2026-10-23T231524Z.jsonl`；
  分数与向量未改，三个 django 卷宗此前已按新措辞重建。
- 复算：113 vulnerabilities / 113 locations / 3886 evidence / 113 reviews / 84 status；
  reviews A 38 / B 75；triage 2613 = confirmed_affected 104 /
  confirmed_not_affected 1321 / possible_affected 586 / unknown 574 / duplicate 28；
  `pending_relevant_triage` 1160；draft 校验 0 error / 49 warning。possible 队列重跑为
  586（`range_precise` 408 / `range_coarse` 83 / `nvd_cpe` 23 / `alias_osv` 42 /
  `legacy_triage` 30；gitea 136 = 76 precise + 60 coarse，django 41），HANDOFF、
  LIMITATIONS、队列 README 与 django 普查 README 计数同步。

## 2026-10-24 — django CVE-2024-38875 独立复核 A 级，promote

- 隔离 reviewer `rv38875-independent-reviewer-2026-10-24` 返回 `confirmed_affected` / **A**。
  它自建 4.2.13 / 4.2.14 / 5.0.6 / 5.0.7 / 4.1.13 五棵 tag 树，以
  `"("*100000 + ":" + ")"*100000` 实测：4.2.13 direct 9.861909 s、模板过滤器 9.844213 s；
  4.2.14 0.002778 s / 0.003399 s；5.0.6 9.711278 s / 8.012470 s；5.0.7 0.002944 s /
  0.004539 s。N=2000→100000 的缩放从 0.006 s 增到 9.862 s（每翻倍约 3.5–4×），
  `urlizetrunc` 路径 7.469 s；不支持的 4.1.13 同样中招（N=20000 时 0.333 s）。
- 分歧（随 verdict 保存）：NVD 无 Primary CVSS（唯一 metric 是 CISA-ADP Secondary）；
  OSV GIT `introduced` 事件方向反了（真正引入是 2016 年 `dec334cb66`）；官方公告 moderate /
  GHSA/OSV HIGH（v4 8.7）；CWE 集合不一致；受影响区间只覆盖受支持分支。
- verdict schema 首轮缺 `languages`（reviewer 用 `vulnerability_id` 充当第九项），
  `promote_verified_rows.py` dry-run 拒绝；请同一 reviewer 自行核验语言清单（Python 2761
  个 `.py` / 455628 行）后重发，sha256 `a70331cedfc2c77b923aeae6edef4af13137b29beb96c6a1673711680d429986`。
- dry-run 通过后 `--apply`：1 vulnerability / 1 location / 1 review / 29 evidence /
  1 status，grade A；verdict 等复制到 `runs/independent/django_CVE-2024-38875_4213_round1/`，
  review 路径由 `persist_independent_verdicts_round3_2026-10-24.py` 改指（备份
  `reviews_before_verdict_paths_round3_2026-10-23T232005Z.jsonl`）；triage 行
  `disc2_051d93d5bd86570c8437b5dd` 由 `apply_promoted_candidate_round3_2026-10-24.py` 改为
  `confirmed_affected`（备份
  `snapshot_candidate_triage_before_promoted_rows_round3_2026-10-23T232006Z.jsonl`）。
- 复算：114 vulnerabilities / 114 locations / 3915 evidence / 114 reviews / 85 status；
  reviews A 39 / B 75；triage 2613 = confirmed_affected 105 / 1321 / possible 585 /
  unknown 574 / duplicate 28；pending 1159；draft 校验 0 error / 49 warning。possible
  队列重跑 585（407 / 83 / 23 / 42 / 30；gitea 136，django 40）。

## 2026-10-24 — django CVE-2024-41989 卷宗（floatformat 大指数内存耗尽）

- 取 possible 行 `disc2_1d98594ee81566538ecb96d2`（`GHSA-jh75-99hh-qvx9` /
  `CVE-2024-41989` / `PYSEC-2024-67`）建卷宗
  `runs/verification/django_CVE-2024-41989_4213/`：
  - 4.2.13 `django/template/defaultfilters.py` 的 `floatformat` 用
    `Decimal(str(text))` 解析（科学计数法只存系数+指数），随后 `int(d) - d`（167 行）
    把指数展开成完整整数，`"1e10000000000000000"` 直接吃内存（CWE-400）。
    `django/utils/numberformat.py:51-55` 虽有 200 位截断，但值要先进过滤器才会到达那里。
  - 修复 `fc76660f`（4.2.x，首见 **4.2.15**）：先读 `as_tuple()`，
    `len(digits)+abs(exponent) > 200` 即原样返回；5.0.x 对应 `27900fe5`（首见 5.0.8）。
    tag 4.2.13 = `c2845b37` → `3bf46e2e`（tree `31f1034a`），4.2.15 = `d982d728` →
    `4d32ebcd`（tree `381a4e3a`）。逐 tag 扫描：4.2.13/4.2.14 无守卫，4.2.15 有；
    5.0.7 无、5.0.8 有。
  - 评分：NVD **Primary** 7.5 HIGH A:H（nvd@nist.gov），CISA-ADP Secondary 同向量；
    GitHub/OSV 的 CVSS 3.1 是 A:L（5.3 MODERATE），OSV 另有 CVSS 4.0 VA:L——分歧写入
    limitations；CWE-400 只以 CISA-ADP Secondary weakness 出现（Primary 为
    NVD-CWE-noinfo）。
  - 局限：采集方未做内存/时间实测；可达性要求攻击者可控的**字符串**输入；发布说明写的
    模块是 `django.utils.numberformat`，但守卫实际在模板过滤器；candidate 行仍带 3.0.2
    旧 triage 结论。
- 生成器断言全部通过后写出 `dossier.json`（10 条证据）；schema-probe dry-run
  （`/tmp/probe41989` 用后即删，**不是** review）报 `promoted: true`、29 条证据、grade B、
  无 schema 错误。已派隔离 reviewer，等裁定；裁定前不改 `data/`。

## 2026-10-24 — 补记：gitea GHSA-hg5r-vq93-9fv6 复核产物的收尾刷新

- 该 reviewer 的后台收尾在 promote 之后才写完：`NOTES.md` 增加了 v1.26.2 全量
  `hmac.New` 普查的两段说明，`sources/v1262_hmac_sites.txt` 增加 4 行非 artifact 的
  `hmac.New` 站点，并据此更新了 verdict 里的两个 `artifacts.sha256`。
- 已把 reviewer 的最终 `verdict.json`、`NOTES.md`、`sources/v1262_hmac_sites.txt` 复制回
  `runs/independent/gitea_GHSA-hg5r-vq93-9fv6_v1.25.5_round1/`；重新逐项核对后
  **11 个 artifact 的 sha256 全部匹配**（`repro/main.go` 对应包内 `reproduction/main.go`）。
  结论未变：`confirmed_affected`、grade A、commit `f913d90a…`；`data/reviews.jsonl`
  不存 verdict 摘要，故数据行无需改动。新 verdict sha256
  `529c1170034e2478bef7b420fb660b2caa237b5b91d42033a56c18aef8d9130b`。

## 2026-10-24 — django CVE-2024-39614 卷宗（翻译语言码二次方 DoS）

- 取 possible 行 `disc2_97b11946b732970b9a25004c`（`GHSA-f6f8-9mx6-9mx2` /
  `CVE-2024-39614` / `PYSEC-2024-59`）建卷宗
  `runs/verification/django_CVE-2024-39614_4213/`：
  - 4.2.13 `django/utils/translation/trans_real.py` 的
    `get_supported_language_variant()`：507 行以整串初始化候选列表，512-514 的
    `while (i := lang_code.rfind("-", 0, i)) > -1:` 每个连字符追加一个
    `lang_code[:i]` 切片（n 字符 → n 个切片、合计 O(n²) 字节），518-519 又对每个候选
    `code.lower()` 查字典再复制一遍；`@lru_cache(maxsize=1000)`（491 行）还会驻留超长键。
  - 4.2.13 只对 **Accept-Language 头**在 `parse_accept_lang_header`（618-645）做了 500
    字符截断；`get_language_from_request`（546-585）从 `request.COOKIES` 取的语言
    cookie 在 561 行取出后于 570 行原样传入，不限长。
  - 修复 `17358fb3`（4.2.x，首见 **4.2.14**）把常量改名 `LANGUAGE_CODE_MAX_LENGTH`
    （注释明确写 header or cookie），在函数入口检查：超过 500 时截到 500 内最后一个
    连字符，否则 `ValueError("'lang_code' exceeds the maximum accepted length")`；
    回归测试含 501 字符边界、strict 用例与 `g("en-" * 30000)` 灾难用例。5.0.x 对应
    `8e7a44e4`（首见 5.0.7）。tag 4.2.13 = `c2845b37` → `3bf46e2e`（tree `31f1034a`），
    4.2.14 = `bfe7062d` → `98cf264c`（tree `eb3c76d8`）；逐 tag 扫描 4.2.13/5.0.6 无守卫，
    4.2.14/5.0.7 有。
  - 实测（`bench.py`，PyPI 安装的 4.2.13 / 4.2.14，CPython 3.12.3，每个用例单起子进程）：
    4.2.13 直接调用 12,000 字符 0.029 s / 24 MB、24,000 字符 0.141 s / 94 MB、
    90,000 字符 1.893 s / **1.29 GiB**；同长度走 LANGUAGE cookie 1.674 s / 1.29 GiB；
    strict=True 也走完全程（1.628 s）。4.2.14 全部 <1 ms、≤256 KB，90,000 字符先截成
    `en` 返回，strict 在 0.16 ms 抛 ValueError。
  - 评分：NVD **没有 Primary** CVSS，唯一指标是 CISA-ADP 容器（`134c704f…`）的
    Secondary 7.5 HIGH A:H；NVD weakness 也只有 CISA-ADP 的 CWE-130，而 GitHub/OSV 记录
    CWE-130 + CWE-770；OSV 另有 CVSS 4.0 VA:H，Django 发布说明称 “moderate”。分歧写入
    dossier limitations 与 severity.source。
  - 局限：实测为直接调用/合成 request，未经真实 WSGI 前端（gunicorn 默认单字段约 8 KiB，
    90 KB cookie 未必可送达；但 >500 字符即二次方，12,000 字符已 29 ms / 24 MB）；
    lru_cache 驻留未测；4.2.14 的 ValueError 不是 LookupError，
    `get_language_from_request` 只捕 LookupError，超长无通用变体 cookie 会变成 500。
- 生成器断言（OSV/PYSEC/NVD/两个补丁/两份发布说明/代码摘录/逐 tag 扫描/bench 日志/
  快照继承）全部通过后写出 `dossier.json`（12 条证据，63659 字节）；schema-probe dry-run
  （`/tmp/probe39614`，**不是** review）报 `promoted: true`、31 条证据、grade B、无
  schema 错误；首轮 probe 报的 3 个非 https `source_url`/permalink 已改为 PyPI 发布页并
  删掉 bench 的本地 permalink trace。已派隔离 reviewer，裁定前不改 `data/`。

## 2026-10-24 — django CVE-2024-41989 隔离复核通过并 promote（A 级）

- 隔离 reviewer（工作区 `/tmp/rv41989`，未读卷宗/数据）返回 `confirmed_affected` / grade A：
  4.2.13 下 `floatformat` 的 `Decimal(str(text))` + `int(d) - d` 在 `1e1000000` 上耗时
  26.85 s 后抛未捕获 ValueError，`1e10000000000000000` 立即 MemoryError；4.2.15 先检查
  `Decimal.as_tuple()`，`len(digits) + abs(exponent) > 200` 时原样返回，同一输入 0.000054 s。
  模板过滤器入口同样复现。verdict sha256 `2e8eb95f…`（首轮 `reviewer_identity` 是对象，
  schema 要求字符串，请同一 reviewer 只改该字段后重发）。
- `promote_verified_rows.py --apply`（2026-10-23T23:32:12Z）追加 1 vuln / 1 location /
  1 review（`rev_CVE_2024_41989_r1`）/ 29 evidence / 1 status，grade A。
- 收尾脚本：
  - `runs/data_fixes/persist_independent_verdicts_round4_2026-10-24.py`：校验 `/tmp` 源与保留副本
    sha256 一致、24 项 artifact 逐个匹配、`reproduction_reference` 含 26.85 s / MemoryError /
    0.000054 s 后，把 `independent_verdict_path` 改指
    `runs/independent/django_CVE-2024-41989_4213_round1/verdict.json`，并在
    `red_green_summary` 追加保留副本位置（备份 `reviews_before_verdict_paths_round4_*`）。
  - `runs/data_fixes/apply_promoted_candidate_round4_2026-10-24.py`：守卫 decision / snapshot /
    repo / alias 引用后，把 `disc2_1d98594ee81566538ecb96d2` 改为 `confirmed_affected`
    （备份 `snapshot_candidate_triage_before_promoted_rows_round4_*`）。
    两者均先 dry-run 再 `--apply`。
- 注意：`data/reviews.jsonl` 的 `reviewer` 字段仍是采集方 `prepared_by`，以
  `independent_reviewer` / `independent_verdict_path` 为准（见 LIMITATIONS）。

## 2026-10-24 — django CVE-2024-39614 隔离复核通过并 promote（A 级）

- reviewer（工作区 `/tmp/rv39614`）自建 4.2.13 / 4.2.14 venv，实测 `get_supported_language_variant`
  的二次方切片：`"en-"*30000`（90,006 字符）冷缓存 2.196 s，n=1k/3k/10k/30k 为
  0.0015/0.0185/0.2250/2.196 s；90,000 字符经 `django_language` cookie 走
  `get_language_from_request` 0.802 s；4.2.14 同输入约 0.000075 s 返回 `"en"`，
  `g("x"*501)` 与 strict 超长抛 ValueError。verdict sha256 `72a45407…`，24 项 artifact
  与 `/tmp/rv39614` 逐个 sha256 匹配。
- 首轮 dry-run 报 `promoted: true`，唯一 warning 是 dossier status 为
  `READY_FOR_INDEPENDENT_REVIEW`（与既有卷宗一致，未改）。`--apply`（2026-10-23T23:33:31Z）
  追加 1 vuln / 1 location / 1 review（`rev_CVE_2024_39614_r1`）/ 31 evidence / 1 status。
- 保留包 `runs/independent/django_CVE-2024-39614_4213_round1/`：verdict、NOTES、sources/、
  scripts/、repro/ 全部复制，24 项 sha256 复核为 0 不匹配。收尾脚本
  `persist_independent_verdicts_round5_2026-10-24.py`（支持 verdict 的
  `artifacts.sha256` 字典格式，校验 2.196 s / 0.802 s / 0.000075 s）把 review 路径改指保留副本；
  `apply_promoted_candidate_round5_2026-10-24.py` 把 `disc2_97b11946b732970b9a25004c` 改为
  `confirmed_affected`。均先 dry-run，各自写备份。
- reviewer 记录的分歧：OSV 的 GIT ranges 无效（introduced 是 2025/2026 年 security-archive
  提交，fixed 只是 4.2.14/5.0.7 的版本号 bump；真实补丁是 `17358fb3` / `8e7a44e4`）；
  NVD 唯一 CVSS 是 CISA-ADP Secondary 7.5，GHSA CVSS 4.0 8.7，Django 自称 moderate；
  NVD 只给 CWE-130，GHSA 给 CWE-130 + CWE-770；公告未点名触发字符，源码显示是 `-`。

## 2026-10-24 — django CVE-2024-41991 卷宗（urlize / AdminURLFieldWidget Unicode DoS）

- 卷宗 `runs/verification/django_CVE-2024-41991_4213/`，证据 12 条，dossier 64561 字节：
  - 4.2.13 `django/utils/html.py` 的 `Urlizer.handle_word`（276-326）在 293-296 用
    `simple_url_re` / `simple_url_2_re` 匹配**未截断整词**，命中后把全部字符交给
    `smart_urlquote`（191-225：urlsplit / punycode(netloc) / unquote+quote path+fragment），
    全链路无长度上限；`is_email_simple`（369-383）不限制域名部分，邮箱分支 297-303 直接
    punycode 任意长度域名。
  - 第二 sink：`AdminURLFieldWidget.get_context`（`django/contrib/admin/widgets.py` 376-389）
    在 `value` 为真时无条件 `smart_urlquote(value)` 生成 href，即使验证器已判
    `url_valid=False`。
  - 修复 `efea1ef7`（4.2.x，首见 **4.2.15**）新增 `MAX_URL_LENGTH = 2048`、给两个正则加
    `len(middle) <= MAX_URL_LENGTH`、域名部分 `len(p2) > 63` 拒绝、widget 改
    `if url_valid else ""`；5.0.x 为 `523da877`（5.0.8）。逐 tag 扫描 4.2.13/4.2.14/5.0.7
    无守卫，4.2.15/5.0.8 全有。tag 4.2.13 = `c2845b37` → `3bf46e2e`（tree `31f1034a`），
    4.2.15 = `d982d728` → `4d32ebcd`（tree `381a4e3a`）。
  - 实测（`bench.py`，PyPI 4.2.13 / 4.2.15，CPython 3.12.3，每个用例单起子进程）：
    `urlize()` 1,000,010 字符 Unicode URL 2.8816 s / 50,812 KB、输出 5,500,035 字符且带链接；
    widget 4,000,010 字符 10.5850 s / 202,020 KB、`url_valid=False` 但仍生成
    18,000,010 字符 href；2,049 字符 URL 4.2.13 仍建链接。4.2.15 对应 0.0104 s（原样返回）、
    0.000555 s（href 为空），2,049 字符不再建链接，2,047 字符与短输入对照行为不变。
  - 评分/CWE 分歧：NVD Primary 7.5 A:H（`nvd@nist.gov`）+ 相同 CISA-ADP Secondary；GHSA/OSV
    MODERATE（CVSS 3.1 A:L 5.3、CVSS 4.0 VA:L）；NVD CWE-1284 Primary + CWE-130 Secondary，
    OSV 另加 CWE-1333——均写入 dossier 与 limitations。
- 生成器断言（OSV/PYSEC/NVD/两个补丁/两份发布说明/代码摘录/逐 tag 守卫/bench/快照继承）全部
  通过；schema-probe dry-run（`/tmp/probe41991`，**不是** review）报 `promoted: true`、
  31 evidence、无 schema 错误。已派隔离 reviewer（工作区 `/tmp/rv41991`），裁定前不改 `data/`。

## 2026-10-24 — django CVE-2024-41991 独立复核 A 级并 promote

- 隔离 reviewer（`/tmp/rv41991`，未读采集方材料）返回 `confirmed_affected` / **A**，verdict
  sha256 `709fce73db2ce1985339b832d1e57fbbe81c6a445b394da35ec7e1a2af7154d9`；
  `fields_verified` 九项齐全、`reviewer_identity` 为字符串、location
  `django/utils/html.py:293-303` 与 dossier 的 `critical_operation` 293-296 重叠。
- reviewer 自测（PyPI 4.2.13 / 4.2.15 独立 venv，CPython 3.12.3，`python -I`，payload
  `"한.글."×1,000,000` ≈4 MB）：4.2.13 email/http/www 三条 `urlize` 10.86 / 10.97 / 11.41 s、
  `AdminURLFieldWidget` 11.05 s，峰值 RSS 增量 +201,608 / +201,976 / +209,656 / +201,976 KiB，
  `urlize` 输出 ~22.0 M 字符；4.2.15 0.043–0.050 s、RSS 增量 0、原样返回、widget href 空。
  4.2.14 n=100k 仍 1.0603 s（4.2.13 1.0606 s）。微基准显示耗时在 `str.encode("idna")`
  （400,003 字符域名 1.0555 s，两个正则匹配 ≤0.0001 s，IDNA 约 2.6 µs/字符线性），
  reviewer 据此不同意 CWE-1333/ReDoS 归类。
- `promote_verified_rows.py` 先 dry-run 再 `--apply`（2026-10-23T23:42:06Z）：追加
  1 vuln / 1 location / 1 review（`rev_CVE_2024_41991_r1`）/ 31 evidence / 1 status，
  grade A；唯一 warning 是 dossier 状态不是 PENDING（沿用既有卷宗状态字段）。
- 保留包 `runs/independent/django_CVE-2024-41991_4213_round1/`：verdict、NOTES、feeds/、
  out/、scripts/ 与 6 个被引用的 venv 文件按原相对路径复制，24 项 sha256 复核 0 不匹配。
- `persist_independent_verdicts_round6_2026-10-24.py` 把 review 的 `independent_verdict_path`
  由 `/tmp/rv41991/verdict.json` 改指保留副本（守卫：源/副本 sha 相等、24 项 artifact、
  feeds/scripts/out/venvs 目录、repro 中的 1,000,000 / AdminURLFieldWidget / 4.2.15）；
  `apply_promoted_candidate_round6_2026-10-24.py` 把 `disc2_3bb0bba7fbc37c8593e5441b`
  改为 `confirmed_affected`。均先 dry-run，各自写备份。
- 全表扫描 possible 行是否引用同快照已 promote 漏洞：0 残留。基线 **117 / 88**
  （A 42 / B 75），possible 582、unknown 574、NA 1321、pending 1156；`validate_dataset --draft`
  errors 0。

## 2026-10-24 — django CVE-2024-41990 探针（4.2.13 上不可复现，记档不提升）

- 目录 `runs/verification/django_CVE-2024-41990_4213_probe/`：`bench.py`（每个 (pattern, n)
  单起子进程、`settings.configure` 后直接 `urlize()`）、`logs/bench_4.2.13.jsonl` /
  `bench_4.2.14.jsonl` / `bench_4.2.15.jsonl`（各 22 行 = 版本行 + 7 pattern × n∈{50k,100k,200k}）、
  README。**不是卷宗，不产出裁定。**
- 关键数据 `".;" * n`：4.2.13 0.001325 / 0.002550 / 0.004674 s（线性）；4.2.14
  0.235239 / 0.800212 / 3.271716 s（每翻倍 3.4×/4.1×，二次）；4.2.15
  0.002346 / 0.002658 / 0.004906 s。`&semi;`、`&#59;`、`&period;`、`&amp;`、`&lt;`、
  `&hellip;` 在三版全部线性（如 `&semi;` n=200k：0.010211 / 0.011293 / 0.009720 s）。
- 祖先关系（`/tmp/django_survey/src` 上 `merge-base --is-ancestor` 核对）：
  `79f3687642`（38875，2024-06-24）不在 4.2.13、在 4.2.14/4.2.15；`d0a82e26a7`
  （41990，2024-07-18）只在 4.2.15。diff 显示 4.2.14 把 `amp = middle.rfind("&")` 与
  `html.unescape(middle[amp:])` 提到通用尾部剥离路径（每次处理都扫整段尾部），4.2.15 复用
  同一个 `amp` 消除重复 `unescape`。即 41990 的该 trigger 是 38875 补丁引入的回归。
- 处置：候选 `disc2_0375e0e8d50b5f62dc5c2e03`（`snap_516aa9971dd9509d`）**保持
  `possible_affected`**，不 promote、不写 `data/`、无 reviewer；无复现只排除了这一条
  trigger（`urlizetrunc`、其它大输入路径未穷举），不能写成“4.2.13 不受影响”。
  基线维持 116 / 87。

## 2026-10-24 — django CVE-2024-45230 探针（4.2.13 上不可复现，记档不提升）

- 目录 `runs/verification/django_CVE-2024-45230_4213_probe/`：`bench.py`、四份日志
  （4.2.13/4.2.14/4.2.15/4.2.16，各 19 行 = 版本行 + 6 pattern × n∈{50k,100k,200k}）、
  `sources/rel_4.2.16.txt`、README。**不是卷宗，不产出裁定。**
- 触发形态按 4.2.16 回归测试：一个 `&` 开头，后接重复的尾部标点单元。关键数据
  `"&" + ";:"*n`：4.2.13 0.001349 / 0.002442 / 0.005114 s（线性）；4.2.14
  0.926732 / 3.846817 / 13.448057 s；4.2.15 0.796886 / 3.242101 / 13.108951 s
  （两者每翻倍约 3.7–4.2×，二次）；4.2.16 0.001599 / 0.003233 / 0.006153 s。
  `".;"`、`";."`、`":;"`、`";::"` 在 4.2.14/4.2.15 的 200k 用例 13–20 s，在
  4.2.13/4.2.16 均 <0.01 s；`"&" + ";"*n` 四版都毫秒级（阴性对照）。
  4.2.13 与 4.2.16 在 n=1,000,000（2,000,001 字符）分别 0.0247 / 0.0305 s。
- 修复 `d147a8ebbd`（2024-08-12）只在 4.2.16；4.2.14 的 38875 补丁
  `79f3687642` 已引入该二次方。发布说明 4.2.16 原文写 “fixes one security issue
  ... in 4.2.15”，与实测（4.2.14/4.2.15 受影响）一致。
- 处置：候选 `disc2_91b14048e4ec3e3a627057a1`（`snap_516aa9971dd9509d`）**保持
  `possible_affected`**，不 promote、不写 `data/`、无 reviewer；4.2.13 的 urlize DoS
  已由已确认的 CVE-2024-38875 覆盖，但本条不据此改判 `confirmed_not_affected`。

## 2026-10-24 — django CVE-2024-53907 独立复核 A 级并 promote（118 / 89）

- 卷宗 `runs/verification/django_CVE-2024-53907_4213/`：`collect_sources.py` 钉住 13 件
  sha256 产物（OSV GHSA/PYSEC、NVD、GHSA 页面、三条分支修复补丁、4.2.13/4.2.17 发布说明、
  按 tag 代码摘录、tag/祖先/守卫扫描、两份 bench 日志），`build_dossier.py` 先断言再写
  `dossier.json`（READY_FOR_INDEPENDENT_REVIEW）。
- 隔离 reviewer（`/tmp/rv53907`，未读任何采集方/数据集材料）自建 PyPI venv：`"<"*n + "a>"*n`
  在 4.2.13 的 n=1000/2000/4000/8000 为 0.412 / 1.591 / 6.514 / 26.301 s，每翻倍约 4×；
  4.2.17 同 24 KB 在 50 轮上限抛 `SuspiciousOperation`（0.334 s）；`striptags` 过滤器
  25.603 s vs 0.342 s；`_strip_once` 逐层剥离 n=5 trace 已记录。verdict
  `runs/independent/django_CVE-2024-53907_4213_round7/verdict.json`，grade **A**，九项
  `fields_verified` 全 true，location `django/utils/html.py` `strip_tags` 171-182
  （关键循环 176-181），修复 commit `790eb058…`（4.2.17，`1f0356ff…`）。
- `promote_verified_rows.py --apply`（2026-10-24T00:02:49Z）追加 1 vuln / 1 location /
  1 review / 32 evidence / 1 status。保留包 24 件（verdict、NOTES、scripts、feeds、out、
  notes、两个 venv 的 `utils/html.py`、`template/defaultfilters.py`、METADATA），
  `preserved_sha256.txt` 全匹配。
- `persist_independent_verdicts_round7_*` 把 review 路径从 `/tmp/rv53907/verdict.json`
  改指保留包并补 red/green 注记；`apply_promoted_candidate_round7_*` 把
  `disc2_8b86415747e9508ae2ac2940` 改写为 `confirmed_affected`，均先 dry-run、写备份。
- `validate_dataset.py --draft`：errors 0；118 vulnerabilities / 118 locations /
  4038 evidence / 118 reviews / 89 status；A 43 / B 75。队列重建 582 → **581**
  （range_precise 404 → 403，django 37 → 36），triage：confirmed_affected 109、
  possible 581、unknown 574、NA 1321、duplicate 28，pending_relevant_triage 1155。
- reviewer 记录的两处口径：OSV `database_specific` 标 MODERATE，NVD 只有 CISA-ADP
  Secondary CVSS 3.1 7.5 HIGH（向量等价）；4.2.17 在抛错前仍会做至多 50 轮全串解析
  （24 KB 0.334 s、600 KB 8.27 s，线性）。

## 2026-10-24 — django CVE-2024-53908 独立复核 A 级并 promote（119 / 90）

- 卷宗 `runs/verification/django_CVE-2024-53908_4213/`：`collect_sources.py` 钉住 13 件
  sha256 产物（OSV GHSA/PYSEC、NVD、GHSA 页面、三条分支修复补丁、4.2.13/4.2.17 发布说明、
  按 tag 代码摘录、tag/祖先/守卫扫描、两份 bench 日志），`build_dossier.py` 先断言再写
  `dossier.json`（READY_FOR_INDEPENDENT_REVIEW）。机制：`HasKeyLookup.as_oracle`
  （`django/db/models/fields/json.py` 212-260，关键行 254-260）把 `as_sql()` 返回的
  lhs 参数经 `sql % tuple(params)` 内联进 SQL 文本，并返回空参数表。
- 隔离 reviewer（`/tmp/rv53908`，未读任何采集方/数据集材料）自建 4.2.13/4.2.17 venv，
  compile-level 红/绿（无真实 Oracle，明确允许）：payload `1, '$.foo') OR 1=1 --`
  在 4.2.13 直接使用得到 `JSON_EXISTS(1, '$.foo') OR 1=1 --, '$."foo"')`、params `[]`；
  经公开入口 `QuerySet.filter(HasKey(Value(payload), 'foo'))` 同样内联；4.2.17 为
  `JSON_EXISTS(%s, '$."foo"')` + 单个绑定参数。`__` 控制路径（`value__has_key`、
  嵌套 `KeyTransform`、带引号 rhs）两版 SQL/params 逐字节相同，`compare_runs.py`
  9/9 断言通过。verdict
  `runs/independent/django_CVE-2024-53908_4213_round8/verdict.json`，grade **A**，
  九项 `fields_verified` 全 true，location `json.py` `HasKeyLookup.as_oracle` 254-260，
  4.2.x 修复 commit `7376bcbf…`（4.2.17，`1f0356ff…`）。
- `promote_verified_rows.py --apply`（2026-10-24T00:10:17Z）追加 1 vuln / 1 location /
  1 review / 32 evidence / 1 status；review 的 `independent_verdict_path` 直接写入保留包
  路径（无需 repoint）。保留包 25 件（verdict、NOTES、scripts、feeds、out、notes、
  两个 venv 的 `db/models/fields/json.py` 与 METADATA），`preserved_sha256.txt` 全匹配。
- `apply_promoted_candidate_round8_*` 把 `disc2_d997111c20cf6d0610292215` 改写为
  `confirmed_affected`（先 dry-run、写备份）。
- `validate_dataset.py --draft`：errors 0；119 vulnerabilities / 119 locations /
  4070 evidence / 119 reviews / 90 status；A 44 / B 75。队列重建 581 → **580**
  （range_precise 403 → 402，django 36 → 35），triage：confirmed_affected 110、
  possible 580、unknown 574、NA 1321、duplicate 28，pending_relevant_triage 1154。
- reviewer 限制：无 Oracle 实例；`oracledb 26.0.1` 仅以 `sys.modules['cx_Oracle']`
  别名满足导入；`git verify-tag` 因本地无公钥未能校验签名（用 `git ls-remote` 证上游一致性）；
  5.0/5.1 只查祖先与代码未执行；带引号 rhs 的 `__has_key` 两版都内联引号，属于未改动的
  rhs 路径，未作为新漏洞主张。

## 2026-10-24 — django CVE-2024-45231 卷宗与独立复核 A 级并 promote（120 / 91）

- 卷宗 `runs/verification/django_CVE-2024-45231_4213/`：`collect_sources.py` 钉住 13 件
  sha256 产物（OSV GHSA/PYSEC、NVD（503 时用同 CVE 缓存并告警）、GHSA 页面、三条分支修复
  补丁、4.2.13/4.2.16 发布说明、代码摘录、tag/祖先/守卫扫描、两份 bench 日志），
  `build_dossier.py` 先断言再写 `dossier.json`（READY_FOR_INDEPENDENT_REVIEW）。机制：
  `PasswordResetForm.send_mail()` 的 `email_message.send()`（`django/contrib/auth/forms.py`
  295-317，关键行 317）未捕获邮件后端异常；`save()` 只在 `get_users()` 返回用户时发送，
  故失败后端下只有存在且激活、有可用密码的地址会抛 500。采集方 bench（in-process）：
  4.2.13 存在地址抛 `ValueError`、其余五类不抛；4.2.16 全部不抛并记 ERROR 日志。
- 隔离 reviewer（`/tmp/rv45231`，未读任何采集方/数据集材料）进一步用真实
  `PasswordResetView`（`django.test.Client(raise_request_exception=False)`、`DEBUG=False`）
  做 HTTP 级红/绿：4.2.13 存在地址 **500**、不存在/未激活/无可用密码 **302**；4.2.16 四类
  全 **302** 且仅存在地址产生 1 条 ERROR `Failed to send password reset email to 1`；
  关闭端口 SMTP（127.0.0.1:1）同样 500 vs 302；locmem 对照两版全 302。另发现
  `setup_test_environment()` 会静默改用 locmem 掩盖缺陷。verdict
  `runs/independent/django_CVE-2024-45231_4213_round9/verdict.json`，grade **A**，九项
  `fields_verified` 全 true，location `forms.py` `PasswordResetForm.send_mail` 317，
  4.2.x 修复 commit `bf4888d3…`（4.2.16，`6f9fea33…`）。
- `promote_verified_rows.py --apply`（2026-10-24T00:16:15Z）追加 1 vuln / 1 location /
  1 review / 32 evidence / 1 status；`independent_verdict_path` 直接指向保留包。保留包
  36 件（verdict、NOTES、scripts、out、两个 venv 的 `contrib/auth/forms.py` 与 METADATA），
  `preserved_sha256.txt` 全匹配。`apply_promoted_candidate_round9_*` 把
  `disc2_00c12ead68ae4b95c2b982e6` 改写为 `confirmed_affected`（先 dry-run、写备份）。
- `validate_dataset.py --draft`：errors 0；120 vulnerabilities / 120 locations /
  4102 evidence / 120 reviews / 91 status；A 45 / B 75。队列重建 580 → **579**
  （range_precise 402 → 401，django 35 → 34），triage：confirmed_affected 111、
  possible 579、unknown 574、NA 1321、duplicate 28，pending_relevant_triage 1153。
- reviewer 记录的口径：NVD 描述把已修复版本写成 “discovered in”（以 CPE 区间为准）；
  GHSA CVSS 3.1 3.7（AC:H）vs NVD 5.3（AC:L），Django 自评 low；仓库级 advisory 页匿名 404；
  只跑 4.2 分支（5.0/5.1 只核对提交与祖先）。

## 2026-10-24 — django CVE-2025-64459 卷宗与独立复核 A 级并 promote（121 / 92）

- 卷宗 `runs/verification/django_CVE-2025-64459_4213/`：`collect_sources.py` 钉住 14 件
  sha256 产物（OSV GHSA/PYSEC、NVD、GHSA 页面、四条修复补丁、4.2.13/4.2.26 发布说明、
  代码摘录、tag/祖先/守卫扫描、两份 bench 日志），`build_dossier.py` 先断言再写
  `dossier.json`（READY_FOR_INDEPENDENT_REVIEW）。机制：`Q.__init__`
  （`django/db/models/query_utils.py` 48-53）把 `_connector` 原样交给 `tree.Node`，
  `WhereNode.as_sql`（`sql/where.py` 171-172）用 `" %s " % self.connector` 拼进 SQL；
  字典展开使 `filter/exclude/get(**data)` 能到达该命名参数（入口 `query.py` 1457-1461）。
  采集方 bench（in-memory SQLite）：4.2.13 载荷 `" OR 1=1 OR "` 生成
  `WHERE (id > %s  OR 1=1 OR  name = %s)`，params 仍为 `[0,"alice"]`，返回 alice+bob；
  exclude 返回空、get 抛 `MultipleObjectsReturned`、`Q(_connector="evil")` 被接受；
  4.2.26 六例分别抛 `ValueError: _connector must be one of 'AND', 'OR', 'XOR', or None.`
  与 `TypeError: The following kwargs are invalid: '_connector'`，对照查询不变。
- 隔离 reviewer（`/tmp/rv64459`，未读任何采集方/数据集材料）自建 4.2.13/4.2.26 venv，
  先用 sha256 确认 PyPI 4.2.13 的 `query_utils.py`/`query.py`/`where.py` 与 tag commit
  3bf46e2e 的 blob 逐字节一致，再做红/绿：4.2.13 `filter(**{"name":"Alice","id":999,
  "_connector":" OR 1=1 OR "})` 返回全部 3 行（合法 AND 查询 0 行），`get()` 抛
  `MultipleObjectsReturned`（匹配 3 行）；4.2.26 同调用被 `TypeError` 拦下，
  `Q(_connector="evil")` 抛 `ValueError`，合法查询 SQL/params/结果不变。verdict
  `runs/independent/django_CVE-2025-64459_4213_round10/verdict.json`，grade **A**，
  九项 `fields_verified` 全 true，location `query_utils.py` `Q.__init__` 48-53，
  4.2.x 修复 commit `59ae82e6…`（4.2.26，`0dfd59e2…`）与配套 `279f8b95…`。
- `promote_verified_rows.py --apply`（2026-10-24T00:23:13Z）追加 1 vuln / 1 location /
  1 review / 33 evidence / 1 status；`independent_verdict_path` 直接指向保留包。保留包
  18 件（verdict、NOTES、reproduction 三件、fetch 五件、两个 venv 的三份 ORM 文件与
  METADATA），`preserved_sha256.txt` 全匹配。`apply_promoted_candidate_round10_*` 把
  `disc2_d791407a54d5b84b33a8db28` 改写为 `confirmed_affected`（先 dry-run、写备份）。
- `validate_dataset.py --draft`：errors 0；121 vulnerabilities / 121 locations /
  4135 evidence / 121 reviews / 92 status；A 46 / B 75。队列重建 579 → **578**
  （range_precise 401 → 400，django 34 → 33），triage：confirmed_affected 112、
  possible 578、unknown 574、NA 1321、duplicate 28，pending_relevant_triage 1152。
- reviewer 记录的口径：GHSA/OSV 的 4.2 分支范围写作 introduced 0（枚举到 1.0.1），
  NVD/PYSEC 从 4.2 起；Django 安全政策把该问题称 "high"（非 CVSS 口径）；GHSA 列出的
  修复提交漏了实际拦截 `filter(**dict)` 的配套提交 `279f8b95…`；GitHub API 的
  `cvss_v4` 为 null/0.0。限制：仅 SQLite、未跑 MySQL/PostgreSQL 与全量测试、
  未尝试布尔绕过以外的取数载荷。

## 2026-10-24 — django 三卷宗（32873 / 57833 / 59682）独立复核 A 级并 promote（124 / 95）

三个卷宗都先由采集方建 `collect_sources.py` + sha256 钉住的 `sources/`，再由
`build_dossier.py` 逐条断言后写 `dossier.json`；三份 `dossier.json` 均为
READY_FOR_INDEPENDENT_REVIEW，未含裁定。

- **CVE-2025-32873**（`runs/verification/django_CVE-2025-32873_4213/`）：`strip_tags`
  把整段输入反复交给 `_strip_once()`（4.2.13 `django/utils/html.py` 170-182），
  以 `">" + "<a"*n` 触发每轮全串 `find(">")`，二次方。采集方 bench：n=200…12800
  时 0.0012→4.1606 s；4.2.21 对同一载荷在解析前抛 `SuspiciousOperation`。
  隔离 reviewer（`runs/independent/django_CVE-2025-32873_4213_round11/verdict.json`，
  grade **A**）自建 CPython 3.12.3 + 4.2.13/4.2.21 venv：4.2.13 在 2,001…128,001
  字节为 0.005→7.893 s（倍增 3.1–4.8×），4.2.21 全部在 0.00014 s 内抛异常；模板
  `|striptags` 同样命中。另确认公告列出的 `9f3419b…` 是 main 提交、不是发布 tag
  祖先，进入 4.2.21 的是回移 `9cd8028f…`；NVD 的 CWE-770 仅为 Secondary。
  **环境前提**：该 DoS 依赖上游 CPython 对 EOF 处不完整标签的旧行为；本机 Ubuntu
  的 `3.12.3-1ubuntu0.17` 已回移 CPython 3.14 行为（不完整标签直接丢弃），在其上
  打不动，且会让 4.2.21 自带的新测试失败。红/绿是在 2024-04-15 发布的上游
  CPython 3.12.3 上做的，`env_probe.log` 记录了两者对照（0.507 s vs 0.00015 s）。
- **CVE-2025-57833**（`runs/verification/django_CVE-2025-57833_4213/`）：
  `Query.add_filtered_relation`（`django/db/models/sql/query.py` 1622-1651）直接
  保存 alias、未调 `check_alias()`，alias 经 `Join.as_sql` 未加引号拼入 SQL。采集方
  bench：`x ON 1=1 AND ? IS NOT NULL AND ? IS NOT NULL --` 让 4.2.13 返回两本书
  （过滤被绕过），对 `author.secret` 的布尔 oracle 返回 2/0 行；4.2.24 四个 crafted
  alias 全抛 `ValueError`，良性 alias 的 SQL 模板与结果不变。隔离 reviewer
  （`..._round11/verdict.json`，grade **A**）自建 partial clone：确认 4.2.13 是
  `31334e69…` 的祖先、`31334e69…` 是 4.2.24 tag commit `5e23d890…` 的祖先；逐字节
  比对 4.2.13/4.2.24 wheel 的 3613 个 `django/**` 文件与 tag blob（0 不一致）；
  用自拟 payload 复现 `['b1','b1','b2','b2']`（正常语义 `[]`）。注：NVD Primary 8.1
  与 CNA/OSV 7.1 不同；NVD 的 CWE-89 仅为 Secondary；GHSA/PYSEC 的 5.0 范围从
  `5.0a1` 起，不影响 4.2.13。
- **CVE-2025-59682**（`runs/verification/django_CVE-2025-59682_4213/`）：
  `BaseArchive.target_filename`（4.2.13 `django/utils/archive.py` 144-149）用
  `filename.startswith(target_path)` 判路径包含。采集方 bench：`pkg/ok.txt` +
  `../target-evil/pwned.txt` 在 4.2.13 返回并写出 `work/target-evil/pwned.txt`，
  4.2.25 抛 `SuspiciousOperation`；纯 `../outside.txt` 两版都拒。隔离 reviewer
  （`..._round11/verdict.json`，grade **A**）自建 4.2.13/4.2.25 venv，用 zip 与
  tar.gz 各复现一次，4.2.25 两种都抛
  `SuspiciousOperation: Archive contains invalid path: '../application/pwned.txt'`；
  location 定在 line 147，入口补到 `django/core/management/templates.py` 的
  `TemplateCommand.extract/handle_template`。另记录：OSV 的 GIT range 事件不可信
  （所列 fixed 是 version-bump），应以 PyPI/ECOSYSTEM 为准；tag `5.0.14` 也含同一
  缺陷但 5.0.x EOL 未列入范围；该 guard 源自 CVE-2021-3281 的 `05413afa…`。
- 提升：三份 verdict 的九项 `fields_verified` 全 true、`reviewed_by` 与采集方不同。
  `promote_verified_rows.py --apply` 依次于 00:40:57Z / 00:40:59Z / 00:40:59Z
  追加 3 vuln / 3 location / 3 review / 96 evidence / 3 status；
  `apply_promoted_candidate_round11_2026-10-24.py`（先 dry-run，备份
  `runs/data_fixes/backup_round11_20261024T004055Z/` 与
  `snapshot_candidate_triage_before_promoted_rows_round11_20261024T004113Z.jsonl`）
  把 `disc2_b6fba8183d54aae8c3543dba`、`disc2_c4d0f4e6aee27f12507cc7c3`、
  `disc2_f1721afcacadb2214d2d6cbf` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**124 vulnerabilities / 124 locations /
  4231 evidence / 124 reviews / 95 status**；A 49 / B 75。队列重建 578 → **575**
  （range_precise 400 → 397，django 33 → 30）；triage：confirmed_affected 115、
  possible 575、unknown 574、NA 1321、duplicate 28。
- 仍未解决：`runs/verification/django_CVE-2024-41990_4213_probe/` 与
  `django_CVE-2024-45230_4213_probe/` 已证明两条 urlize DoS 的二次方行为是 4.2.14
  引入的回归、在 4.2.13 上不可复现，对应候选保持 `possible_affected`，不得据此
  判 not_affected，也不得提升。

## 2026-10-24 — django 两卷宗（48432 / 64460）独立复核 A 级并 promote（126 / 97）

两卷宗同样先由采集方建 sha256 钉住的 `sources/` + `collect_sources.py`，再由
`build_dossier.py` 断言后写 READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`，未含裁定。

- **CVE-2025-48432**（`runs/verification/django_CVE-2025-48432_4213/`）：
  4.2.13 的 `log_response()`（`django/utils/log.py` 241-249）把调用方位置参数原样交给
  logger，`BaseHandler.get_response`（`django/core/handlers/base.py` 142-149）对每个
  4xx/5xx 传 `request.path`；URL 里的 `%0A` / `%1B` 经 WSGI 解码后成为真实换行 / ESC，
  单次请求即可伪造日志行或注入终端控制序列。隔离 reviewer
  （`runs/independent/django_CVE-2025-48432_4213_round12/verdict.json`，reviewed_at
  00:51:54Z，grade **A**）在 4.2.13 / 4.2.22 / 4.2.23 三个 venv 里实测：4.2.13 的
  404/405/410 三条日志路径全部原样输出（`%0A` 变 3 行格式化记录、`%1B` 为原始 0x1B），
  4.2.23 全部转义、良性请求三版逐字节一致。**关键纠偏**：4.2.22 只修了 `log_response()`
  一条路径（404 已转义），405 `http_method_not_allowed` 与 410 `RedirectView.get` 仍
  原样——所以卷宗把完整修复版本记为 **4.2.23**（NVD 英文描述 / CPE 与 Django 公告口径），
  4.2.22 记为该路径的部分修复，GHSA/PYSEC 仍写 4.2.22 属镜像滞后。采集方据此回填
  `range_expressions`（4.2.23 完整 / 4.2.22 仅 log_response）与 5.1.11、5.2.3 follow-up
  证据；location 定在 `log_response` 241-243。
- **CVE-2025-64460**（`runs/verification/django_CVE-2025-64460_4213/`）：
  4.2.13 的 `getInnerText()`（`django/core/serializers/xml_serializer.py` 393-407）对子元素
  执行 `inner_text.extend(getInnerText(child))`，返回值是 `str`，`extend` 按字符展开，
  每层都把叶子文本再复制一遍 → O(depth × leaf)；sink 是 `_handle_object` 第 281 行
  `field.to_python(getInnerText(field_node).strip())`。隔离 reviewer
  （`..._round12/verdict.json`，reviewed_at 00:55:14Z，grade **A**）用文档化入口
  `serializers.deserialize("xml", data)` 在 4.2.13 / 4.2.27 上跑阶梯与 1 MB 压力：
  每联合翻倍耗时 3.176 / 3.678 / 3.779 / 4.011× vs 1.619 / 1.631 / 1.720 / 1.896×；
  1,013,722 字节文档 4.631656 s vs 0.009695 s（477.74×），直接 `getInnerText` 占
  4.2.13 端到端 >99%（4.659800 s vs 0.000278 s）；良性文档两版解析结果一致
  （Widget pk 7 "hello world"）。reviewer 另指出 OSV 的 GIT range introduced 提交是修复后
  的后代提交、不可信；CWE-407、NVD 只有 CISA-ADP Secondary 7.5 HIGH 而 OSV 为
  CVSS 4.0 / MODERATE 的分歧都记入卷宗。location 定在 `getInnerText` 393-407。
- 提升：两份 verdict 九项 `fields_verified` 全 true、`reviewed_by` 与采集方不同。
  `promote_verified_rows.py --apply` 依次追加 **1 vuln / 1 location / 1 review / 35 evidence /
  1 status**（48432）与 **1 / 1 / 1 / 32 / 1**（64460，含各自 location 证据 2 条）。
  随后 `apply_promoted_candidate_round12_2026-10-24.py`（先 dry-run；备份
  `runs/data_fixes/backup_round12_20261024T005501Z/`、
  `backup_round12_20261024T005727Z/` 与
  `snapshot_candidate_triage_before_promoted_rows_round12_20261024T005731Z.jsonl`）在
  00:57:29Z 把 `disc2_69acdbeb36ad1d787b4e65c9`、`disc2_997bfd0592735772098d6792` 改写为
  `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**126 vulnerabilities / 126 locations /
  4298 evidence / 126 reviews / 97 status**；A 51 / B 75。队列重建 575 → **573**
  （range_precise 397 → 395，django 30 → 28）；triage：confirmed_affected 117、
  possible 573、unknown 574、NA 1321、duplicate 28，pending_relevant_triage 1147。
- 仍未解决：`django_CVE-2024-41990_4213_probe/` 与 `django_CVE-2024-45230_4213_probe/`
  证明的不可复现结论不变，对应候选继续维持 `possible_affected`；其余 django 新快照
  possible 28 条仍未逐条源码复核。本轮不声称已知漏洞穷尽，也不声明 release。
- 复核后补记（48432，2026-10-24）：隔离 reviewer 在 promote 之后又对同一 verdict 做了
  增量修订（decision/grade 不变，仍 `confirmed_affected` / A）：补充 `django/middleware/csrf.py`
  214-223（403）、`django/utils/cache.py` 126-134（412）与
  `django/views/decorators/http.py` 32-42（`require_http_methods` 405）三个同样把
  `request.path` 交给 `log_response()` 的调用点，说明它们由 fix 1 覆盖；而类视图
  `View.http_method_not_allowed` 的 405 走直接 `logger.warning`，才需要 4.2.23 的 fix 2。
  修订后的 verdict sha256 为 `8f0cb161270d76f86e8e0ca6d0e8a0ce92bf7f35600ecb459d74260973ea4fb9`，
  `preserved_sha256.txt` 已同步；`data/` 未存 verdict 哈希，promote 行无需改动。

## 2026-10-24 — django CVE-2025-26699 卷宗、独立复核 A 级并 promote（127 / 98）

- **卷宗**（`runs/verification/django_CVE-2025-26699_4213/`）：`collect_sources.py`
  钉住 19 件 sha256 产物（OSV CVE/GHSA/PYSEC、NVD、GHSA 公告 HTML、PyPI 4.2.13 /
  4.2.20 JSON、两条 raw `text.py`、四条修复补丁、4.2.19 / 4.2.20 发布说明、代码摘录、
  两份 bench 日志、tag/祖先/守卫扫描），`build_dossier.py` 逐项断言后写
  READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（20 条证据、16 个 field_evidence 键）。
  `django/utils/text.py` 在 4.2.13 与 4.2.20 上 git blob / raw.githubusercontent.com /
  venv 三方 sha256 全等（`c30d8dca…` / `d0829e2f…`）。
- **机制**：4.2.13 `wrap()`（`django/utils/text.py` 88-117）手写循环每输出一行就
  `line = line[space:]`（112 行）复制整个剩余串，n 字符约 n/width 行 → O(n²/width)；
  文档化入口 `wordwrap` 过滤器（`django/template/defaultfilters.py` 398-400）直接
  `wrap(value, int(arg))`。4.2.20 改为 `textwrap.TextWrapper`（89-109）。OSV 的 GIT
  range `fixed` 哈希是发布版本号提交（`35c58a79…` 等）、`introduced` 哈希落在修复后，
  卷宗只采用发布号与补丁提交。
- **采集方实测**（`sources/bench_4213.jsonl` / `bench_4220.jsonl`）：上游测试形状
  （sentence × 20,000，width 10，1,520,000 字节）4.2.13 2.840059 s vs 4.2.20
  0.150700 s（18.85×）；`wordwrap` 过滤器 2.830695 s vs 0.146404 s（19.33×）；
  4.2.13 从 1,000 起每翻倍 3.18–5.12×（超线性），4.2.20 1.91–2.18×（线性）。
  固定实现常数因子更大：12,500 words 时慢 8.1×，交叉点在 400,000–800,000 words。
- **隔离复核**（`runs/independent/django_CVE-2025-26699_4213_round13/verdict.json`，
  reviewer `independent-reviewer-round13/deepseek-flash`，reviewed_at
  2026-10-24T16:52:16Z）：`confirmed_affected`、grade **A**，九项 `fields_verified`
  全 true，location `django/utils/text.py` `wrap` 88-117（关键循环 100-117，
  112 行 `line = line[space:]`），入口 `defaultfilters.py` 396-400。reviewer 自建
  4.2.13 / 4.2.20 两个 PyPI wheel venv（wheel sha256 `a17fcba2…` / `213381b6…`
  与 PyPI JSON 一致），用 `{{ text|wordwrap:10 }}` 跑 n=1,000…64,000（最大
  4,928,000 字符）：4.2.13 0.010993 → **42.541894 s**，4.2.20 0.007053 →
  0.540858 s（**78.66×**），每翻倍 3.12–5.01× vs 1.77–2.25×；直接 `wrap()` 对照
  37.945832 s vs 0.553276 s。良性串两版输出逐字节一致（sha256 `a4484ba2…`）；
  DoS 载荷的差异仅在行尾空白（`rstrip` 后各档 sha256 相同）；单个 4,928,000 字符
  不换行 token 两版都线性（0.001772 s vs 0.053617 s），说明触发条件是需要大量换行点。
  reviewer 独立用父提交关系确认修复 `e88f7376…` 是 4.2.20 发布提交 `35c58a79…`
  的唯一父提交、4.2.19 及更早 tag 不含它；5.0.13 / 5.1.7 同理。
- **promote 前的 schema 纠偏**：首次 dry-run 被 `v031/schemas/*.json` 拒绝——
  `fix_commits` 每项必须有 https `url`、`fixed_releases` 必须有
  `package` / `ecosystem` / `version` / `release_url`、`location.trace` 必须是对象数组
  （不是单个对象）、证据 `source_url` 必须 `^https://`。据此改 `build_dossier.py`
  （补齐字段、trace 改成 wordwrap → wrap → `_generator` 三步、git/bench 产物的
  source_url 指向对应 tag blob），重建后才通过。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T16:53:44Z）追加
  **1 vuln / 1 location / 1 review / 47 evidence / 1 status**（47 = 46 条字段证据
  + 1 条 snapshot 语言证据），warnings 为空。随后
  `apply_promoted_candidate_round13_2026-10-24.py`（先 dry-run；备份
  `runs/data_fixes/backup_round13_20261024T165259Z/` 与
  `snapshot_candidate_triage_before_promoted_rows_round13_20261024T165346Z.jsonl`）
  在 16:53:46Z 把 `disc2_2edf09d5878747bbb482de5a` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**127 vulnerabilities / 127 locations /
  4345 evidence / 127 reviews / 98 status**；A 52 / B 75。队列重建 573 → **572**
  （range_precise 395 → 394，django 28 → 27）；triage：confirmed_affected 118、
  possible 572、unknown 574、NA 1321、duplicate 28，pending_relevant_triage 1146。
- reviewer 记录的分歧：NVD Primary 7.5 HIGH vs CNA/MITRE、GHSA/OSV 的 5.0 MEDIUM；
  CWE-770 仅 NVD Secondary（MITRE）；Django weblog 把 main 与 5.2 预发布列入修复
  目标，但 CVE/GHSA/PYSEC 范围只编码 4.2 / 5.0 / 5.1；同样的 slice 循环存在于
  3.2 / 4.1（支持窗口产物，非真实引入）；修复同时改变行尾空白输出（上游测试只断言
  子串）；GitHub languages API 403，语言清单由 reviewer 自行计数（6,733 文件，
  2,761 个 `.py`）。
- 仍未解决：其余 django 新快照 possible 27 条未逐条源码复核；41990 / 45230 的
  probe 结论仍是「4.2.13 不可复现」，对应候选保持 `possible_affected`。本轮不声称
  已知漏洞穷尽，也不声明 release。

## 2026-10-25 — django CVE-2024-56374 探针（线性 + 内存放大，记档不提升）

- **目标**：`django/django` tag `4.2.13`（commit `3bf46e2e…`，tree `31f1034a…`），
  公告 CVE-2024-56374 / `GHSA-qcgg-j2x8-h9g8` / `PYSEC-2025-1` /
  `BIT-django-2024-56374`，CWE-770；范围 `4.2 < 4.2.18`、`5.0 < 5.0.11`、
  `5.1 < 5.1.5`（OSV / GHSA / PYSEC / NVD CPE 四源一致）；NVD 有 Primary 与
  Secondary 两条 3.1 指标，同向量 `AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:L`（5.8
  MEDIUM），GHSA `database_specific` 为 MODERATE。
- **修复**：4.2 分支 `ad866a1ca3e7d60da888d25d27e46a8adb2ed36e`（2025-01-06
  author date，随 2025-01-14 的 4.2.18 发布），新增
  `MAX_IPV6_ADDRESS_LENGTH = 39` 与 `_ipv6_address_from_str()`；
  `django/forms/fields.py` 的 `GenericIPAddressField` 补
  `kwargs.setdefault("max_length", …)`；模型字段按发布说明不受影响。
  5.0 `e8d4a200…`、5.1 `4806731e…`、main `ca2be772…`。OSV 的 GIT `fixed`
  哈希（`a7b0e50e…` 等）是发布版本号提交，不是补丁提交。
- **实测**（`probe_time.py` 3 reps 取最小；`probe_ipv6.py` 带 tracemalloc）：
  4.2.13 的耗时**线性**——`":"*n` 从 64 KiB 到 16 MiB 每 ×4 涨
  3.36 → 4.33 → 3.99 → 4.26 倍，16 MiB 时 `clean_ipv6_address` 0.217487 s、
  `is_valid_ipv6_address` 0.213959 s（4.2.18 为 0.015239 / 0.001419 s）。
  内存放大是稳定常数：16 MiB 冒号串峰值 **176,542,836 B（10.52×）**、
  `"0"*n+"::1"` 5.00×、`"::1%"+"%"*n` 3.25×，4.2.18 一律 1.00×。
  语义差异：4.2.13 接受任意长 scope id 的 `fe80::1%<16 MiB>` 并清洗成
  `fe80::1`（`is_valid` 返回 True），4.2.18 对 >39 字符一律拒绝。
- **结论**：4.2.13 确实缺上限（公告的结构性前提成立），但可测代价是线性时间 +
  3.25–10.52× 内存放大，没有超线性；按本数据集「超线性可复现 DoS」口径不派
  复核、不写 `data/`，候选 `disc2_35cca10445711b7f2ca00d76` 维持
  `possible_affected`。材料在 `runs/verification/django_CVE-2024-56374_4213_probe/`
  （3 支脚本、6 份日志、10 件钉住产物）。

## 2026-10-25 — django CVE-2025-14550 卷宗、独立复核 A 级并 promote（128 / 99）

- **卷宗**（`runs/verification/django_CVE-2025-14550_4213/`）：`collect_sources.py`
  钉住 21 件 sha256 产物（OSV CVE/GHSA/PYSEC/BIT、NVD、GHSA 公告 HTML、Django
  weblog、PyPI 4.2.13 / 4.2.28 JSON、两条 raw `asgi.py`、四条修复补丁、4.2.27 /
  4.2.28 发布说明、代码摘录、tag/祖先/守卫扫描、两份 bench 日志、wheel 哈希），
  `build_dossier.py` 逐项断言后写 READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`
  （22 条证据、9 条 limitations）。`django/core/handlers/asgi.py` 在 4.2.13
  （`4a77175d…`）与 4.2.28（`e16ebcaf…`）上 git tag blob、raw.githubusercontent.com
  与安装后的 venv 文件三方 sha256 全等。
- **机制**：4.2.13 `ASGIRequest.__init__`（`django/core/handlers/asgi.py` 83-97）
  对每个重复 header 执行 96 行 `value = self.META[corrected_name] + "," + value`
  再 97 行写回，m 个 v 字节重复头复制约 `(v+1)·m²` 字节、m 次 dict 写，输入只有
  `O(m·v)`；文档化入口 `django.core.asgi.get_asgi_application()` →
  `ASGIHandler.create_request()`（同文件 213-219）→ `ASGIRequest`。4.2.28 改为
  `collections.defaultdict(list)` 逐条 append、98 行一次 `META.update()` 线性合并；
  上游回归测试 `test_meta_not_modified_with_repeat_headers` 用 200,000 个重复头
  并断言 `setitem_count <= 100`。OSV 的 GIT `fixed` 哈希（`20c71f6b…` /
  `4a96a199…` / `ba00558d…`）是发布版本号提交、`introduced` 哈希落在修复之后，
  卷宗只采用发布号与补丁提交（4.2 `f578acc8…`、5.2 `1ba90069…`、6.0 `972dbdd4…`、
  main `eb22e1d6…`）。同一 CVE 另覆盖另一包 asgiref（`WsgiToAsgi`，修到 3.11.1），
  本卷宗不涉及。
- **采集方实测**（`sources/bench_4213.jsonl` / `bench_4228.jsonl`）：3 字节重复头
  阶梯 2,000 → 128,000，4.2.13 每翻倍 2.42–18.71×（32,000 → 128,000 贵 129.5×），
  4.2.28 稳定 1.84–2.19×；上游同规模 n=200,000 27.034773 s vs 0.049667 s（544.3×），
  META 写 200,002 vs 2 次。**固定后的常数因子更大**：20,000 个互不相同的 header 名
  4.2.28 反而慢约 3.9×（0.022177 s vs 0.005750 s）——CVE 主张的是渐近复杂度，
  这一点如实记录。
- **隔离复核**（`runs/independent/django_CVE-2025-14550_4213_round14/verdict.json`，
  reviewer `independent-reviewer-round14/deepseek-flash`，reviewed_at
  2026-10-24T17:20:27Z）：`confirmed_affected`、grade **A**，九项 `fields_verified`
  全 true，location `django/core/handlers/asgi.py` 95-97（关键行 96）。reviewer
  未读任何采集方材料，自建 4.2.13 / 4.2.28 两个 PyPI wheel venv，直接构造
  `ASGIRequest(scope, io.BytesIO(b""))`：n=200,000 **27.696 s vs 0.0504 s
  （549.95×）**，`setitem_count` **200,005 vs 5**（上限 100）；阶梯 2,500 → 200,000
  每翻倍 2.65 / 3.88 / 2.84 / 5.29 / 19.31 / 5.41 / 1.68×、log-log 斜率 **2.33**
  vs **1.02**；良性对照两版 `META` 逐字节一致（sha256 `d973a897…`）；走完整
  `get_asgi_application()` 入口 100,000 头 5.511 s vs 0.0329 s，入口可达性独立确认。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T17:21:51Z）追加
  **1 vuln / 1 location / 1 review / 47 evidence / 1 status**，warnings 为空。随后
  `runs/data_fixes/promote_2025_14550_triage_round14_2026-10-25.py`（先 dry-run，
  提升前因无行返回 rc=1；提升后 dry-run 1 change；`--apply` 备份
  `snapshot_candidate_triage_before_promoted_rows_round14_20261024T172152Z.jsonl`）
  把 `disc2_5a2a3a6523e51a18cc663630` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**128 vulnerabilities / 128 locations /
  4392 evidence / 128 reviews / 99 status**；A 53 / B 75。队列重建 572 → **571**
  （range_precise 394 → 393，django 27 → 26）；triage：confirmed_affected 119、
  possible 571、unknown 574、NA 1321、duplicate 28。
- reviewer 记录的分歧：NVD **没有 Primary 指标**，唯一 CVSS 是 CISA-ADP Secondary
  3.1 7.5 HIGH（卷宗采纳，同 CVE-2025-66035 先例），CNA（GitHub）CVSS 4.0 渲染 2.7
  LOW，Django 发布说明自称 "moderate"；CWE-407 来自 OSV/GHSA 与 NVD 唯一的
  weakness（Secondary）。
- 仍未解决：其余 django 新快照 possible 26 条未逐条源码复核；41990 / 45230 / 56374
  的 probe 结论不变（4.2.13 不可复现超线性），对应候选继续维持 `possible_affected`。
  本轮不声称已知漏洞穷尽，也不声明 release。

## 2026-10-25 — django CVE-2026-1285 卷宗建包（待独立复核，不写 `data/`）

- **目标**：`django/django` tag `4.2.13`（commit `3bf46e2e…`，tree `31f1034a…`），
  快照 `snap_516aa9971dd9509d`，候选 `disc2_0f82375353c52e59aee290ad`；公告
  CVE-2026-1285 / `GHSA-4rrr-2h4v-f3j9` / `PYSEC-2026-45` /
  `BIT-django-2026-1285`，CWE-407；范围 `4.2 < 4.2.28`、`5.2 < 5.2.11`、
  `6.0 < 6.0.2`（OSV / GHSA / PYSEC / NVD CPE 四源一致）。评分同 14550：
  NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 7.5 HIGH；CNA CVSS 4.0
  2.7 LOW、Bitnami High、Django "moderate"，四处记录。
- **修复**：4.2 `b40cfc60…`（祖先关系：4.2.28 / 4.2.29 为真，4.2.27 及更早为假），
  5.2 `9f2ada87…`、6.0 `4b86ba51…`、main `a33540b3…`；OSV GIT `fixed` 哈希
  （`20c71f6b…` / `4a96a199…` / `ba00558d…`）是发布版本号提交、`introduced`
  哈希是 security archive 回填，卷宗只用发布号与四个补丁提交。
- **机制**：4.2.13 `Truncator._truncate_html`（`django/utils/text.py` 273-285）
  对每个结束标签 `open_tags.index(tagname)`（276）全表扫描，未匹配时吞
  `ValueError`；`<a>`×m + `</b>`×m 使每次关闭都扫描 m 项 → O(m²)，输入只增长
  4m 字节。4.2.28 换成 LIFO 检查（`open_tags[0] == tagname`），但 `insert(0)`
  与成功关闭的切片保留。5.2 / 6.0 / main 本来就是 `deque` +
  `self.tags.remove(tag)`（同样是 O(m) 扫描），三处修复改成
  `self.tags[0] == tag` + `popleft()`。
- **实测**（`sources/bench_4213.jsonl` / `bench_4228.jsonl`，3 次取最小）：
  未匹配结束标签阶梯 1,000 → 16,000，4.2.13 0.055183 → **3.132921 s**
  （每翻倍 1.73 / 2.58 / 3.42 / 3.72，log-log 斜率 1.90），4.2.28 0.040392 →
  0.144501 s（1.17 / 1.20 / 1.43 / 1.78，斜率 0.83）；同 n 版本比 4.3× / 10.4× /
  **21.7×**；`truncatewords_html` n=8,000 为 0.842038 vs 0.086117 s。模板过滤器
  （56,000 字符载荷）：`truncatechars_html:2` **0.530144 vs 0.043797 s（12.1×）**、
  `:100` 12.0×、`truncatewords_html:1` 10.1×，而 `:1` 为 1.01×（`truncate_len = 0`
  跳过全部标签）；`chars(1, truncate="")` 0.528740 vs 0.042204 s 证明边界在
  `truncate_len` 而非长度。良构嵌套两版都二次方（n=32,000 1.009801 vs
  1.017046 s），如实记录 4.2.28 回移不完整。语义差异：`<a><b><c></b>XX` 在
  4.2.13 输出 `<a><b><c></b>XX</a>`，4.2.28 输出 `<a><b><c></b>XX</c></b></a>`。
- **建包与纠错**：`collect_sources.py` 钉住 25 件产物，`build_dossier.py` 断言后
  写 READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（26 条证据、11 条 limitations）。
  首版守卫扫描只匹配 4.2 的 `open_tags[0] == tagname`，把 5.2.11 / 6.0.2 误记为
  `lifo=False`；修正为同时匹配 `self.tags[0] == tag` 后重抓 sources（GHSA 页面、
  NVD、OSV CVE/GHSA、Django weblog 的远程字节自首抓后已变化；raw 源码、补丁、
  PyPI JSON、bench/filter 日志不变），`manifest.json` 与 `dossier.json` 已同步重建。
- **状态**：卷宗 `runs/verification/django_CVE-2026-1285_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，已派发隔离复核（round15）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`。等 verdict 返回后再决定 promote。

## 2026-10-25 — django CVE-2026-1285 独立复核通过并提升（grade A）

- **裁定**：`runs/independent/django_CVE-2026-1285_4213_round15/verdict.json`，
  reviewer `independent-reviewer-round15/deepseek-flash`，`reviewed_at`
  2026-10-24T17:38:10Z，结论 `confirmed_affected`、`grade_recommendation` A，
  12 条 findings；`fields_verified` 为九键全真，`location` 为
  `django/utils/text.py` 第 276 行（与卷宗 273-285 / 关键 276-282 重叠），
  `fix_commit` `b40cfc60…`、`fixed_release` `4.2.28`。复核方独立 clone 建
  venv 复现，未读卷宗/dossier。
- **复核方数字**：未匹配结束标签阶梯 8k / 16k / 32k / 128k 上 4.2.13 为
  0.5106 / 2.0273 / 7.7315 / **189.45 s**，4.2.28 为 0.0435 / 0.1001 /
  0.2667 / 2.51 s，最大 **75.5×**；良好嵌套对照 64k 上 3.4610 vs 3.4305 s
  基本相同，超额「错配 − 良构」在 4.2.13 上每次加倍约 4×、在 4.2.28 上为负。
  量级与采集方一致（采集方 16k 21.7×），规模更大。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T17:40:45Z）追加
  **1 vuln / 1 location / 1 review / 51 evidence / 1 status**，warnings 为空。
  提升前唯一阻塞是卷宗 `ev_1285_semantics` 的 `source_url` 为命令描述而非
  https（`bench.py --child semantics under a venv with django==4.2.13 and
  4.2.28`），已把该证据改为指向 4.2.13 关键代码段的 blob 永久链接并在 note
  中注明输出为本地 bench 记录，`build_dossier.py` 重建后 dry-run 通过。
- **triage**：`runs/data_fixes/promote_2026_1285_triage_round15_2026-10-25.py`
  先 dry-run（提升前返回 rc=1「no CVE-2026-1285 row」；提升后 1 change），
  `--apply` 备份 `snapshot_candidate_triage_before_promoted_rows_round15_20261024T174048Z.jsonl`，
  把 `disc2_0f82375353c52e59aee290ad` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**129 vulnerabilities / 129 locations /
  4443 evidence / 129 reviews / 100 status**；A 54 / B 75。队列重建 571 → **570**
  （range_precise 393 → 392，django 26 → 25）；triage：confirmed_affected 120、
  possible 570、unknown 574、NA 1321、duplicate 28。全表精确别名扫描确认没有
  `possible_affected` 行再引用已提升漏洞（`PYSEC-2026-45` 只作为 `PYSEC-2026-4312`
  的子串出现在 werkzeug 候选里）。
- 仍未解决：41990 / 45230 / 56374 的 probe 结论不变（4.2.13 不可复现超线性），
  对应候选继续维持 `possible_affected`；其余 django possible 25 条未逐条源码复核。
  本轮不声称已知漏洞穷尽，也不声明 release。

## 2026-10-25 — django CVE-2026-3902 卷宗建包（待独立复核，不写 `data/`）

- **目标**：`django/django` tag `4.2.13`（commit `3bf46e2e…`，tree `31f1034a…`），
  快照 `snap_516aa9971dd9509d`，候选 `disc2_931984b6d2edccd8cf80d5a8`；公告
  CVE-2026-3902 / `GHSA-mvfq-ggxm-9mc5` / `PYSEC-2026-51` /
  `BIT-django-2026-3902`，CWE-290；范围 `4.2 < 4.2.30`、`5.2 < 5.2.13`、
  `6.0 < 6.0.4`（OSV / GHSA / PYSEC / Bitnami / NVD CPE 五源一致）。评分：
  NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 7.5 HIGH；GHSA 按该向量
  标 HIGH，Django 4.2.30 发布说明把本 CVE 标 severity "low"，两处记录。
- **修复**：4.2 `4412731a…`（祖先关系：4.2.30 为真，4.2.13/4.2.29 为假），
  5.2 `1cc2a761…`、6.0 `a623c398…`、main `caf90a97…`（两条稳定线提交信息均声明
  为 main 的 backport）；OSV GIT `fixed` 哈希（`3396992e…` / `7d831a9e…` /
  `141e791f…`）是发布版本号提交、`introduced` 哈希是 archive 回填，卷宗只用
  发布号与四个补丁提交。
- **机制**：4.2.13 `ASGIRequest.__init__`（`django/core/handlers/asgi.py`
  84-97）把每个 header 名折叠为 `HTTP_%s % name.upper().replace("-", "_")`
  （91），重复键用逗号拼接（95-97），**没有下划线拒绝**；因此
  `X_Forwarded_For` 与 `X-Forwarded-For` 落到同一个 `META` 键，代理按惯例
  剥掉的连字符头可被下划线拼写写回。4.2.29 改为 `defaultdict` 但无守卫；
  4.2.30 在 88-90 插入 `if "_" in name: continue`（同步改测试客户端、新增
  `test_underscores_in_headers_ignored`）；main 同形。
- **实测**（`sources/headers_{4213,4229,4230}.jsonl`，进程内 `ASGIRequest`
  直构 + `get_asgi_application()` 完整路径）：仅 `x_forwarded_for: 6.6.6.6`
  时 4.2.13/4.2.29 `META` 与 `request.headers` 均为 6.6.6.6、应用层 echo
  `forwarded-for=6.6.6.6`，4.2.30 完全不可见；连字符 198.51.100.7 + 下划线
  6.6.6.6 在 4.2.13/4.2.29 合并为 `198.51.100.7,6.6.6.6`（顺序随 scope）、
  4.2.30 只保留 198.51.100.7；`x_forwarded_proto` 同样在 4.2.13/4.2.29 可见；
  连字符正常用例三版逐字节相同。
- **建包**：`collect_sources.py` 钉住 25 件产物（四份 OSV、NVD、GHSA 页、
  weblog、两版发布说明、三份 PyPI、三份 raw asgi.py、四份补丁、代码摘录、
  tag/祖先/守卫扫描、三份探测日志、wheels），`build_dossier.py` 断言后写
  READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（25 条证据、5 条 limitations、
  16 个字段映射）。用临时 verdict 做过一次 promote schema 检查（不写 `data/`，
  临时文件已删），locations 的 `entry_point`/`trace` 形状修正后通过。
- **状态**：卷宗 `runs/verification/django_CVE-2026-3902_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，已派发隔离复核（round16）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`。等 verdict 返回后再决定 promote。

## 2026-10-25 — django CVE-2026-3902 round16 独立复核 grade A，提升入 `data/`

- **裁定**：`runs/independent/django_CVE-2026-3902_4213_round16/verdict.json`
  （reviewed_at `2026-10-24T17:49:58Z`，reviewer `independent-reviewer-round16/deepseek-flash`）
  返回 `confirmed_affected` / grade A，九项 `fields_verified` 全 true；
  `fix_commit` 与卷宗一致 `4412731aa64d62a6dd7edae79e0c15b72666d7ca`，
  `fixed_release` 4.2.30，location 为 4.2.13 `django/core/handlers/asgi.py:91`
  （落在卷宗 84-97 内），`reviewer ≠ prepared_by`。
- **复核独立实测**：自行从 PyPI 装 4.2.13 / 4.2.29 / 4.2.30，跑
  `ASGIRequest` 直构与 `ASGIHandler.__call__` 两路，5 个用例 × 3 版本：
  `x_forwarded_host: attacker.example` 在 4.2.13/4.2.29 的 `META` 为
  `attacker.example`、应用层 `host=attacker.example|for=10.6.6.6`，4.2.30
  两键均 `<absent>`；连字符 + 下划线双拼写在 4.2.13/4.2.29 合并为
  `legit.example,attacker.example`，4.2.30 只剩 `legit.example`；连字符对照
  三版相同。机制与卷宗的 `x_forwarded_for` 结果一致。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T17:50:54Z）追加
  **1 vuln / 1 location / 1 review / 50 evidence / 1 status**，warnings/conflicts 为空。
- **triage**：`runs/data_fixes/promote_2026_3902_triage_round16_2026-10-25.py`
  先 dry-run（提升前返回 `no CVE-2026-3902 row at snap_516aa9971dd9509d`；
  提升后 1 change），`--apply` 备份
  `snapshot_candidate_triage_before_promoted_rows_round16_20261024T175057Z.jsonl`，
  把 `disc2_931984b6d2edccd8cf80d5a8` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**130 vulnerabilities / 130 locations /
  4493 evidence / 130 reviews / 101 status**；A 55 / B 75。队列重建 570 → **569**
  （range_precise 392 → 391，django 25 → 24）；triage：confirmed_affected 121、
  possible 569、unknown 574、NA 1321、duplicate 28。全表精确别名扫描确认没有
  `possible_affected` 行再引用已提升漏洞。
- 仍未解决：41990 / 45230 / 56374 的 probe 结论不变（4.2.13 不可复现超线性），
  对应候选继续维持 `possible_affected`；其余 django possible 24 条未逐条源码复核。
  本轮不声称已知漏洞穷尽，也不声明 release。

## 2026-10-25 — django CVE-2026-33034 卷宗建包（待独立复核，不写 `data/`）

- **目标**：`django/django` tag `4.2.13`（commit `3bf46e2e…`，tree `31f1034a…`），
  快照 `snap_516aa9971dd9509d`，候选 `disc2_0e9bed26286b9becdb4e8091`；公告
  CVE-2026-33034 / `GHSA-933h-hp56-hf7m` / `PYSEC-2026-49` /
  `BIT-django-2026-33034`，CWE-770；范围 `4.2 < 4.2.30`、`5.2 < 5.2.13`、
  `6.0 < 6.0.4`（OSV / GHSA / PYSEC / Bitnami / NVD CPE 五源一致）。评分：
  NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 7.5 HIGH
  `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`；GHSA 按该向量标 HIGH，Django
  4.2.30 发布说明把本 CVE 标 severity "low"，两处记录。
- **修复**：4.2 `ed4dfda6…`（祖先关系：4.2.30 为真，4.2.13/4.2.29 为假），
  5.2 `49e1e2b5…`、6.0 `393dbc53…`、main `953c2380…`（三条稳定线提交信息均声明
  为 main 的 backport）；OSV GIT `fixed` 哈希（`3396992e…` / `7d831a9e…` /
  `141e791f…`）同样只是发布版本号提交，卷宗只用发布号与四个补丁提交。
- **机制**：4.2.13 `HttpRequest.body`（`django/http/request.py` 331-347）只把
  `DATA_UPLOAD_MAX_MEMORY_SIZE` 与 `int(META.get("CONTENT_LENGTH") or 0)` 比较
  （331-339），随后 `self.read()` 读完整流（342）；ASGI 的
  `ASGIHandler.read_body`（`asgi.py` 192-211）把每个分块无上限写入
  `SpooledTemporaryFile`，chunked 请求没有 `content-length`，比较恒为
  `0 > limit`（假），body 被整体缓存。低报 `Content-Length` 同样只要不超过
  上限就通过。4.2.29 的该文件与 4.2.13 **逐字节相同**；4.2.30 新增
  `_check_data_too_big()`、对 seekable 流 `seek(0, SEEK_END)` 量实际大小、
  对非 seekable 流最多读 `limit+1` 再复检，并新增
  `DataUploadMaxMemorySizeASGITests`。
- **实测**（`sources/body_{4213,4229,4230}.jsonl`，`DATA_UPLOAD_MAX_MEMORY_SIZE=1024`，
  body 200,000 B，进程内 `ASGIRequest` 直构 + `get_asgi_application()`）：
  无 `content-length` 的 4 分块 body 与声明 `content-length: 10` 的 200,000 B
  body 在 4.2.13/4.2.29 都被完整读取（`bytes=200000`，应用层 200
  `read:200000`），4.2.30 两例均 `RequestDataTooBig` / 413；声明 5000 B 的
  超限 body 在两版都 413（旧声明检查本身有效）；500 B 小 body 三版都 200。
- **建包**：`collect_sources.py` 钉住 25 件产物（四份 OSV、NVD、GHSA 页、
  weblog、两版发布说明、三份 PyPI、三份 raw request.py、四份补丁、代码摘录、
  tag/祖先/守卫扫描、三份探测日志、wheels），`build_dossier.py` 断言后写
  READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（25 条证据、6 条 limitations、
  16 个字段映射）。用临时 verdict 做过一次 promote schema 检查（不写 `data/`，
  临时文件已删），dry-run 返回 49 evidence / 1 各表，无 warnings。
- **状态**：卷宗 `runs/verification/django_CVE-2026-33034_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，已派发隔离复核（round17）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`；triage 改写脚本
  `runs/data_fixes/promote_2026_33034_triage_round17_2026-10-25.py` 的守卫在
  提升前正确拒绝。等 verdict 返回后再决定 promote。

## 2026-10-25 — django CVE-2026-33034 提升（round17 独立复核 grade A）

- **verdict**：`confirmed_affected`，**grade A**，
  `independent-reviewer-round17/deepseek-flash`（≠ `prepared_by`），
  `reviewed_at 2026-10-24T17:58:00Z`，产出
  `runs/independent/django_CVE-2026-33034_4213_round17/`（`verdict.json`、
  `NOTES.md`、`preserved_sha256.txt`、`reproduction/`，43 个文件
  `sha256sum -c` 全通过）。九项 `fields_verified` 全 true；fix
  `ed4dfda6…`、fixed_release `4.2.30`、location
  `django/http/request.py:331-347`（`HttpRequest.body`）与卷宗一致。
- **复核方实测**：`DATA_UPLOAD_MAX_MEMORY_SIZE=1024`、body 200,000 B 时，
  无 `Content-Length` / `CL=10` / `CL=1024` 三种 scope 在 4.2.13/4.2.29
  直构 `ASGIRequest` 与 `get_asgi_application()` 都读到完整 200,000 字节；
  4.2.30 全部 `RequestDataTooBig`，非 seekable 回退只读 1025 字节。
  真实 **uvicorn 0.54.0 + curl `Transfer-Encoding: chunked`**：4.2.13 → 200
  `len=200000`，4.2.30 → 400；诚实 `CL=5000` 三版拒绝，512 B 小 body 三版
  200。与采集方差异（如实保留）：采集方进程内 probe 记为 413，复核方为
  400（同一拒绝语义的不同映射）；真实 HTTP/1.1 下低报 `Content-Length`
  只能在 Django ASGI 接口层复现。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T17:58:38Z）追加
  **1 vuln / 1 location / 1 review / 49 evidence / 1 status**，
  warnings/conflicts 为空。
- **triage**：`runs/data_fixes/promote_2026_33034_triage_round17_2026-10-25.py`
  先 dry-run（提升前返回 `no CVE-2026-33034 row at snap_516aa9971dd9509d`；
  提升后 1 change），`--apply` 备份
  `snapshot_candidate_triage_before_promoted_rows_round17_20261024T175839Z.jsonl`，
  把 `disc2_0e9bed26286b9becdb4e8091` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**131 vulnerabilities / 131 locations /
  4542 evidence / 131 reviews / 102 status**；A 56 / B 75。队列重建 569 → **568**
  （range_precise 391 → 390，django 24 → 23）；triage：confirmed_affected 122、
  possible 568、unknown 574、NA 1321、duplicate 28、pending 1142。
- 相关文档已同步：卷宗 README 改 PROMOTED 并加复核结果、队列 README、
  HANDOFF、LIMITATIONS。

## 2026-10-25 — django CVE-2026-33033 提升（round18 独立复核 grade A）

- **verdict**：`confirmed_affected`，**grade A**，
  `independent-reviewer-round18/deepseek-flash`（≠ `prepared_by`），
  `reviewed_at 2026-10-24T18:00:24Z`，产出
  `runs/independent/django_CVE-2026-33033_4213_round18/`。九项
  `fields_verified` 全 true；fix `f13c20f8…`、fixed_release `4.2.30`、
  location `django/http/multipartparser.py:305-313` 与卷宗一致；复核方自建
  clone 核对 tag/commit/祖先，并确认 git tag 与 PyPI wheel 的
  `multipartparser.py` sha256 相同、4.2.13 与 4.2.29 逐字节相同。
- **复核方实测**（进程内 `MultiPartParser.parse()`，3 次取中位）：128 KiB
  0.1458 s vs 0.000185 s（788×）、512 KiB 1.0003 s vs 0.000512 s（1954×）、
  1 MiB 2.1529 s vs 0.000683 s（3152×）、2 MiB 4.4371 s vs 0.001273 s
  （3486×）；对齐对照两版约 0.0001-0.0013 s，解码结果均为 `b"ABC"`。unget
  计数插桩显示 4.2.13 replay 字节从 128 KiB 的 2.15 GB 线性涨到 2 MiB 的
  66.57 GB（约每输入字节 31.7 KB），对齐对照恒约 262 KB；与卷宗「64 KiB
  偏快是机制使然」一致。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T18:01:19Z）追加
  **1 vuln / 1 location / 1 review / 49 evidence / 1 status**，
  warnings/conflicts 为空。
- **triage**：`runs/data_fixes/promote_2026_33033_triage_round18_2026-10-25.py`
  先 dry-run，`--apply` 备份
  `snapshot_candidate_triage_before_promoted_rows_round18_20261024T180119Z.jsonl`，
  把 `disc2_f7b7100a8e247c57aae034fb` 改写为 `confirmed_affected`。
- `validate_dataset.py --draft`：errors 0；**132 vulnerabilities / 132 locations /
  4591 evidence / 132 reviews / 103 status**；A 57 / B 75。队列重建 568 → **567**
  （range_precise 390 → 389，django 23 → 22）；triage：confirmed_affected 123、
  possible 567、unknown 574、NA 1321、duplicate 28、pending 1141。

## 2026-10-25 — django CVE-2026-33033 卷宗建包（待独立复核，不写 `data/`）

- **目标**：同一快照 `snap_516aa9971dd9509d`、tag `4.2.13`（commit
  `3bf46e2e…`，tree `31f1034a…`），候选 `disc2_f7b7100a8e247c57aae034fb`；
  公告 CVE-2026-33033 / `GHSA-5mf9-h53q-7mhq` / `PYSEC-2026-48` /
  `BIT-django-2026-33033`，CWE-407；范围 `4.2 < 4.2.30`、`5.2 < 5.2.13`、
  `6.0 < 6.0.4`（OSV / GHSA / PYSEC / Bitnami / NVD CPE 五源一致）。评分：
  NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 6.5 MEDIUM
  `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`；GHSA 标 MODERATE，Django 4.2.30
  发布说明也标 severity "moderate"，**厂商与公告口径一致**（与前四条
  「厂商 low、公告 HIGH」不同）。
- **修复**：4.2 `f13c20f8…`（祖先关系：4.2.30 为真，4.2.13/4.2.29 为假），
  5.2 `0b467893…`、6.0 `0910af60…`、main `7e9885f9…`（三条稳定线提交信息均声明
  为 main 的 backport），首发 4.2.30（commit `3396992e…`，tree `ad50710b…`）。
- **机制**：4.2.13 `MultiPartParser._parse`（`django/http/multipartparser.py`
  305-313）对 base64 分片逐解析器分块做四字节对齐，每轮只
  `field_stream.read(4 - remaining)` 读 1-3 字节并把
  `b"".join(over_chunk.split())` 原地拼到 `stripped_chunk`；`LazyStream.read`
  （441-465）取整个 `_leftover`，经 `unget`（495-506）用
  `bytes + self._leftover` 重建，于是每个空白字节都 replay 一遍当前 64 KiB
  分块。`unget` 的同长度 40 次保护因长度逐次递减 1 而不触发。4.2.29 的该
  文件与 4.2.13 **逐字节相同**；4.2.30 改成每轮读 `self._chunk_size`、
  累积 `stripped_parts` 列表最后 join 一次（305-314），并新增
  `test_multipart_file_upload_base64_whitespace_heavy`。
- **实测**（`sources/parse_{4213,4229,4230}.jsonl`，进程内
  `MultiPartParser.parse()`，负载 `b"QUJ" + 空格*N + b"D"`）：4.2.13 /
  4.2.29 / 4.2.30 分别为 128 KiB 0.135 / 0.143 / 0.00025 s，256 KiB
  0.404 / 0.437 / 0.00037 s，512 KiB 0.975 / 1.016 / 0.00068 s，1 MiB
  2.128 / 2.127 / 0.0010 s；64 KiB 边界对照三版都 <0.001 s（其后只剩几百
  字节才到结束边界）；对齐对照三版约 0.0002 s；六个用例解码结果都是 3 字节。
  1 MiB 时固定版快约 2100 倍。增长是「每个完整 64 KiB 空白分块被逐字节
  replay」的叠加，受影响的 64 KiB 用例刻意保留为边界对照。
- **建包**：`collect_sources.py` 钉住 25 件产物（四份 OSV、NVD、GHSA 页、
  weblog、两版发布说明、三份 PyPI、三份 raw multipartparser.py、四份补丁、
  代码摘录、tag/祖先/守卫扫描、三份探测日志、wheels），`build_dossier.py`
  断言后写 READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（25 条证据、
  6 条 limitations、16 个字段映射）。用临时 verdict 做过一次 promote schema
  检查（不写 `data/`，临时文件已删），dry-run 返回 49 evidence / 1 各表，
  无 warnings。
- **状态**：卷宗 `runs/verification/django_CVE-2026-33033_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，已派发隔离复核（round18）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`；triage 改写脚本
  `runs/data_fixes/promote_2026_33033_triage_round18_2026-10-25.py` 的守卫在
  提升前正确拒绝。（round17 复核随后返回 grade A，见上文提升条目。）

## 2026-10-25 — django CVE-2026-4292 卷宗建包（待独立复核，不写 `data/`）

- **目标**：同一快照 `snap_516aa9971dd9509d`、tag `4.2.13`，候选
  `disc2_518dea83eab5c641d5f2c9ff`；公告 CVE-2026-4292 /
  `GHSA-mmwr-2jhp-mc7j` / `PYSEC-2026-53` / `BIT-django-2026-4292`，
  CWE-862；范围 `4.2 < 4.2.30`、`5.2 < 5.2.13`、`6.0 < 6.0.4`。评分：NVD
  无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 **2.7 LOW**
  `AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:L/A:N`；GHSA LOW、Django 发布说明
  "low"，三方一致。
- **修复**：4.2 `abfe1a1c…`（祖先关系：4.2.30 为真，4.2.13/4.2.29 为假），
  5.2 `397c2204…`、6.0 `428c48f3…`、main `6afe7ce9…`。
- **机制**：4.2.13 `ModelAdmin.changelist_view`（`django/contrib/admin/options.py`
  2003-2022）在 `list_editable` + `_save` 的 POST 上用请求数据构造 formset，
  保存循环对所有已变更表单调用 `save_form(..., change=True)` 并持久化，
  未检查 `obj._state.adding`；伪造 `INITIAL_FORMS=0`、空 id 即创建新行，
  绕过 `has_add_permission`。4.2.29 的该文件与 4.2.13 逐字节相同；4.2.30
  在保存前 `if obj._state.adding: raise BadRequest(...)`（2019-2021），并新增
  `test_forged_post_submission_when_no_add_permission` 与
  `ParentWithUUIDPKAdmin`。
- **实测**（`sources/probe_{4213,4229,4230}.jsonl`，进程内最小 admin 站点 +
  test client，superuser，`has_add_permission` 覆写为 False）：4.2.13 与
  4.2.29 的伪造 POST 返回 **302** 并创建 1 行（title `The News`）；4.2.30
  返回 **400**、创建 0 行。三版 `login=true`、`count_before=0`。
- **建包**：`collect_sources.py` 钉住 25 件产物（四份 OSV、NVD、GHSA 页、
  weblog、两版发布说明、三份 PyPI、三份 raw options.py、四份补丁、代码摘录、
  tag/祖先/守卫扫描、三份探测日志、wheels），`build_dossier.py` 断言后写
  READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（25 条证据、6 条 limitations、
  16 个字段映射）。用临时 verdict 做过 promote schema 检查（不写 `data/`，
  临时文件已删），dry-run 返回 49 evidence / 1 各表，无 warnings。
- **状态**：卷宗 `runs/verification/django_CVE-2026-4292_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，已派发隔离复核（round19）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`；triage 改写脚本
  `runs/data_fixes/promote_2026_4292_triage_round19_2026-10-25.py` 的守卫在
  提升前正确拒绝。（round19 复核随后返回 grade A，见下文提升条目。）

## 2026-10-25 — django CVE-2026-4292 提升（round19 独立复核 grade A）

- **裁定**：`confirmed_affected`，grade A，复核方
  `independent-reviewer-round19/deepseek-flash`（≠ `prepared_by`），
  产出 `runs/independent/django_CVE-2026-4292_4213_round19/`。九项
  `fields_verified` 全 true；`fix_commit abfe1a1c…`、`fixed_release 4.2.30`、
  location `django/contrib/admin/options.py:2016-2025`（与卷宗 2016-2022
  重叠）；`reproduction_reference` 指向其自建脚本与四份输出。
- **复核方实测**：自建最小 admin 站点，除卷宗的 superuser + override 模式外，
  还做了非 superuser staff（仅 view+change、无 add）的 perms 模式。4.2.13 两种
  模式伪造 POST 都返回 302 并插入 `The News`；4.2.30 两种模式都返回 400 且
  不插入。正常编辑对照两版均 302 且标题被改；四次运行 stderr 全空。复核方
  另核对了 tag/commit/祖先、安装源码 sha256 与 tag 一致、4.2.13 与 4.2.29
  `options.py` 逐字节相同、上游回归测试只在 4.2.30 存在。
- **行号**：复核方测得 4.2.13 保存循环 2016-2025、4.2.30 guard 2020-2021，
  与卷宗 2016-2022 / 2019-2021 相差 2 行，无实质差异。
- **提升**：`promote_verified_rows.py` dry-run 与 `--apply` 均返回 1 vuln /
  1 location / 1 review / 49 evidence / 1 status，无 warnings、无 conflicts
  （applied_at `2026-10-24T18:05:34Z`）。
- **triage**：`runs/data_fixes/promote_2026_4292_triage_round19_2026-10-25.py`
  先 dry-run 后 `--apply`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round19_20261024T180536Z.jsonl`，
  把 `disc2_518dea83eab5c641d5f2c9ff` 改写为 `confirmed_affected`
  CVE-2026-4292（`checked_at 2026-10-25T06:05:00Z`）。
- **校验**：`validate_dataset.py . --draft` errors 0、warnings 0（仅 coverage
  披露），counts `133/133/4640/133/104`；reviews 58 A + 75 B。
- **队列**：重建后 567 → 566；`range_precise` 389 → 388，django
  22 → 21。triage 现状：`confirmed_affected 124`、`possible_affected 566`、
  `unknown 574`、`confirmed_not_affected 1321`、`duplicate 28`（pending 1140）。
- **文档**：卷宗 README 标 PROMOTED 并附 round19 结果；队列 README 计数与
  提升段落更新；本日志与 HANDOFF / LIMITATIONS 同步。未生成 CHECKSUMS，
  未声称 PASS_KNOWN_SWEEP 或完成。

## 2026-10-25 — django CVE-2026-4277 卷宗建包（待独立复核，不写 `data/`）

- **目标**：同一快照 `snap_516aa9971dd9509d`、tag `4.2.13`，候选
  `disc2_f75eaf5e610a2b495529ddce`；公告 CVE-2026-4277 /
  `GHSA-pwjp-ccjc-ghwg` / `PYSEC-2026-52` / `BIT-django-2026-4277`，
  CWE-862；范围 `4.2 < 4.2.30`、`5.2 < 5.2.13`、`6.0 < 6.0.4`。
- **评分分歧**：NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1
  **9.8 CRITICAL** `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`（CVE/PYSEC 重复）；
  GHSA 是 CVSS 4.0 `AV:N/AC:L/AT:P/PR:L/UI:N/...` 且
  `database_specific.severity = LOW`；Django 4.2.30 发布说明写 "low"。
  卷宗为与既有 django 行一致采用 NVD 指标，同时把三方分数都写入
  `all_published_scores`，并在 limitations 里明确 9.8 的 `PR:N/UI:N` 与
  「需 staff 持父模型 change 权限」的公告文本矛盾、数值高估。
- **修复**：4.2 `051f3909…`（祖先关系：4.2.30 为真，4.2.13/4.2.29 为假），
  5.2 `60ffa957…`、6.0 `08a752c1…`、main `ef8b25dc…`。
- **机制**：4.2.13 `GenericInlineModelAdmin.get_formset`
  （`django/contrib/contenttypes/admin.py` 98-135）覆盖基类方法时没有复用
  `InlineModelAdmin.get_formset`（options.py 2375-2427）安装的
  `can_change`/`can_add` + `has_changed()` 包装；普通表单校验不拦新建
  实例，伪造 `INITIAL_FORMS=0`、空 inline id 的 POST 经
  `ModelAdmin.save_formset`（options.py 1239-1243）的 `formset.save()`
  插入一行，绕过 `has_add_permission`。4.2.29 的该文件与 4.2.13 逐字节相同；
  4.2.30 补上 `PermissionProtectedModelForm`（130-143），并新增
  `test_add_inline_without_add_permission` /
  `test_add_inline_with_change_permission_only`。
- **实测**（`sources/probe_{4213,4229,4230}.jsonl`，进程内最小 admin 站点 +
  test client，三个用例）：A 无 add 权限的伪造新增——4.2.13/4.2.29 返回 302
  并插入 `["Forged"]`，4.2.30 返回 302 但不插入；B 有 add 权限的对照——
  三版都插入；C 合法编辑 + 伪造新增——4.2.13/4.2.29 得到
  `["Edited","Forged"]`，4.2.30 只得到 `["Edited"]`。
- **建包**：`collect_sources.py` 钉住 25 件产物（四份 OSV、NVD、GHSA 页、
  weblog、两版发布说明、三份 PyPI、三份 raw contenttypes/admin.py、四份补丁、
  代码摘录、tag/祖先/守卫扫描、三份探测日志、wheels），`build_dossier.py`
  断言后写 READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（25 条证据、
  7 条 limitations、16 个字段映射）。用临时 verdict 做过一次 promote schema
  检查（不写 `data/`，临时文件已删），dry-run 返回 49 evidence / 1 各表，
  无 warnings、无 conflicts。
- **状态**：卷宗 `runs/verification/django_CVE-2026-4277_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，已派发隔离复核（round20）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`；triage 改写脚本
  `runs/data_fixes/promote_2026_4277_triage_round20_2026-10-25.py` 的守卫在
  提升前正确拒绝（`no CVE-2026-4277 row at snap_516aa9971dd9509d`）。

## 2026-10-25 — django CVE-2026-4277 提升（round20 独立复核 grade A）

- **裁定**：`confirmed_affected`，grade A，复核方
  `independent-reviewer-round20/deepseek-flash`（≠ `prepared_by`），
  产出 `runs/independent/django_CVE-2026-4277_4213_round20/`。九项
  `fields_verified` 全 true；`fix_commit 051f3909…`、`fixed_release 4.2.30`、
  location `django/contrib/contenttypes/admin.py:98`（`line_range 98-135`，
  与卷宗 98-135 重叠）；`reproduction_reference` 指向其自建脚本与输出。
- **复核方实测**：真实 admin change view（`django.test.Client` 进程内 POST，
  sqlite `:memory:`，Episode + generic Media + `GenericTabularInline`）。非
  superuser 的 staff 用户无 `add_media`：4.2.13 伪造 `INITIAL_FORMS=0` 的 inline
  返回 302 并插入 1 行，4.2.30 返回 302 但插入 0 行；有 `add_media` 的对照两版
  都插入 1 行；「1 条合法编辑 + 1 条伪造新增」4.2.13 得到 2 行、4.2.30 只有被
  编辑的 1 行；空 extra form 两版都不插入。机制层 form MRO 与 `has_changed()`
  对照一致，两次运行 stderr 均 0 字节。
- **provenance**：复核方 4.2.13 / 4.2.30 全量文件 sha256 对比 3613↔3613、
  3614↔3614，0 mismatch；`stable/4.2.x` ref 已消失（4.2 EOL），fix commit 经
  tag 4.2.30 与安全归档链接到达；tag 带 PGP 签名但公钥取不到，未做密码学
  验签，改以 PyPI 全树哈希交叉验证；OSV 4.2 GIT range 倒置，未采用。
- **提升**：`promote_verified_rows.py` dry-run 与 `--apply` 均返回 1 vuln /
  1 location / 1 review / 49 evidence / 1 status，无 warnings、无 conflicts
  （applied_at `2026-10-24T18:16:57Z`）。
- **triage**：`runs/data_fixes/promote_2026_4277_triage_round20_2026-10-25.py`
  先 dry-run 后 `--apply`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round20_20261024T181659Z.jsonl`，
  把 `disc2_f75eaf5e610a2b495529ddce` 改写为 `confirmed_affected`
  CVE-2026-4277（`checked_at 2026-10-25T07:05:00Z`）。
- **校验**：`validate_dataset.py . --draft` errors 0、warnings 0（仅 coverage
  披露），counts `134/134/4689/134/105`；reviews 59 A + 75 B。
- **队列**：重建后 566 → 565；`range_precise` 388 → 387，django
  21 → 20。triage 现状：`confirmed_affected 125`、`possible_affected 565`、
  `unknown 574`、`confirmed_not_affected 1321`、`duplicate 28`（pending 1139）。
- **文档**：卷宗 README 标 PROMOTED 并附 round20 结果；队列 README 计数与
  提升段落更新；本日志与 HANDOFF / LIMITATIONS 同步。未生成 CHECKSUMS，
  未声称 PASS_KNOWN_SWEEP 或完成。

## 2026-10-25 — django CVE-2025-13473 卷宗建包（待独立复核，不写 `data/`）

- **候选**：`disc2_0ae99f3b69a48b480295ab89`（`possible_affected`，basis 仅范围
  命中），快照 `snap_516aa9971dd9509d` / tag 4.2.13（commit
  `3bf46e2e…`）；CVE-2025-13473 / `GHSA-2mcm-79hx-8fxw` / `PYSEC-2026-42` /
  `BIT-django-2025-13473`，CWE-208。
- **评分**：NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 5.3 MEDIUM
  `AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N`（CVE/PYSEC/Bitnami 重复）；GHSA 为
  CVSS 4.0 且 `severity = LOW`，Django 4.2.28 发布说明写 severity "low"。
  卷宗采用 NVD 指标，三方分数入 `all_published_scores`，差异在 README 明确
  记录。
- **修复**：4.2 `6dc23508…`（祖先关系：4.2.28 为真，4.2.13/4.2.27 为假），
  5.2 `184e38ab…`、6.0 `d72cc3be…`、main `3eb814e0…`。
- **机制**：`django/contrib/auth/handlers/modwsgi.py` 的 `check_password()`
  （4.2.13，7-26）对 `DoesNotExist`（19-21）与停用用户（22-23）在**任何哈希
  之前**返回 `None`，只有活跃用户走 `user.check_password()`（24，PBKDF2-SHA256
  600,000 轮）。4.2.27 该文件与 4.2.13 逐字节相同；4.2.28 引入 `_get_user()`
  （7-27）对 None 情形调用 `UserModel().set_password("")`（25）补一次默认哈希，
  `check_password` 改为先取 `_get_user()`（45-47），并新增回归测试
  `test_check_password_fake_runtime`。
- **实测**（`sources/probe_{4213,4227,4228}.jsonl`，进程内 + 一次性 sqlite）：
  用 `mock.patch.object(hasher, "encode")` 计数（与上游测试同法）加 12 次
  中位耗时。4.2.13/4.2.27 上 `inactive` 与 `doesnotexist` 为 0 次哈希、
  0.0003 s 量级，活跃用户 1 次、0.108-0.131 s，比值约 310-350 倍；4.2.28
  三类用户都 1 次哈希、0.108 s，比值 < 2。`unusable` 行因 4.2.27 起
  `hashers.check_password()` 已单独补哈希，标为跨版本混杂项，判别用例是
  `inactive` / `doesnotexist`。
- **建包**：`collect_sources.py` 钉住 25 件产物（四份 OSV、NVD、GHSA 页、
  weblog、两版发布说明、三份 PyPI、三份 raw modwsgi.py、四份补丁、代码摘录、
  tag/祖先/守卫扫描、三份探测日志、wheels），`build_dossier.py` 断言后写
  READY_FOR_INDEPENDENT_REVIEW 的 `dossier.json`（74,315 字节、25 条证据、
  7 条 limitations、16 个字段映射）。
- **状态**：卷宗 `runs/verification/django_CVE-2025-13473_4213/` README 标
  READY_FOR_INDEPENDENT_REVIEW，派发隔离复核（round21）；**未写 `data/`，
  未改 triage 行**，候选维持 `possible_affected`。

## 2026-10-25 — django CVE-2025-13473 独立复核通过并提升（round21）

- **复核**：隔离复核方 `independent-reviewer-round21/deepseek-flash`，裁定
  `confirmed_affected`、grade **A**（2026-10-24T18:24:19Z）。复核方自行 clone
  django、重算 4.2.13/4.2.27/4.2.28 的 tag object / commit / tree、自己从
  `git log 4.2.27..4.2.28` 定位修复提交 `6dc23508…`（`git tag --contains` =
  4.2.28/29/30），自建三份 PyPI venv（wheel sha256 与 PyPI 元数据一致），
  用 `mock.patch.object(PBKDF2PasswordHasher, "encode")` 计数加 15 次 × 2 轮
  墙钟（n=30/用例）跑红/绿。九项 `fields_verified` 全 true；
  `reviewer_identity` ≠ dossier `prepared_by`。
- **复核实测**：4.2.13（modwsgi.py 与 4.2.27 逐字节相同）`existing/correct` 1 次
  哈希、0.109 s，`inactive` 0 次、0.0011 s，`nonexistent` 0 次、0.0004 s，
  中位比值 288×（最小 312×）；4.2.28 全部 1 次、约 0.11-0.12 s，比值 0.9-1.0×；
  返回语义 `None/False/True` 三版一致，正确口令三版都返回 True。索引停用/不存在
  用户 0 vs 1 次 PBKDF2 调用即红/绿判据。
- **location**：`django/contrib/auth/handlers/modwsgi.py` `check_password`
  第 21 行（range 18-24），与卷宗 `17-24` 重叠。
- **提升**：先跑
  `promote_verified_rows.py . --dossier runs/verification/django_CVE-2025-13473_4213/dossier.json --verdict runs/independent/django_CVE-2025-13473_4213_round21/verdict.json`。
  首次 dry-run 被 schema 拒绝：`locations/CVE-2025-13473: '24' does not match
  '^[1-9][0-9]*-[1-9][0-9]*$'` —— 卷宗 `trace[2].line` 写成字符串 `"24"`（schema
  只接受整数或 `a-b` 区间）。改卷宗与 `build_dossier.py` 为整数 `24` 后 dry-run
  `promoted: true`、`warnings: []`，再 `--apply`
  （2026-10-24T18:26:46Z）：vulnerabilities 1 / locations 1 / reviews 1 /
  evidence 50 / snapshot_vulnerability_status 1，无冲突。
- **triage**：`runs/data_fixes/promote_2025_13473_triage_round21_2026-10-25.py`
  先 dry-run（1 行待改、0 problems）再 `--apply`，把
  `disc2_0ae99f3b69a48b480295ab89` 由 `possible_affected` 改成
  `confirmed_affected` / CVE-2025-13473；备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round21_20261024T182647Z.jsonl`。
- **校验**：`validate_dataset.py . --draft` → repositories 50 / snapshots 110 /
  vulnerabilities 135 / locations 135 / evidence 4739 / reviews 135 /
  candidates 2626 / snapshot_vulnerability_status 106 /
  snapshot_candidate_triage 2613；known positives 106（A 60 + B 75）；
  triaged 2613、`pending_relevant_triage` 1138；errors 0、warnings 49。
- **队列**：`runs/possible_review_queue_2026-10-24/build_queue.py` 重建 → 总数
  565→**564**（alias_osv 42 / nvd_cpe 23 / range_coarse 83 / range_precise 386 /
  legacy_triage 30），django 19；`plan_snapshot_queue.py` 重生成
  `v031/reports/queue_P3.json` → ARCHIVE 1349 / DONE 126 / P1_REVIEW 574 /
  P1_VERIFY 564 / P0_SELECT_SNAPSHOT 13（合计 2626）。
- **复核方记录异常（原样保留）**：4.2 线 `stable/4.2.x` 分支在 EOL 后已从
  GitHub 删除（只剩历史 branch-point tag）；CVE OSV 的 GIT range 是倒置/混杂的
  （4.2 的 introduced `97aa3b7f` 是 4.2.28 的 `20c71f6b` 的后代，fixed 事件指向
  发布 bump 提交），复核方改用 ECOSYSTEM range + 自身祖先关系；GHSA API
  `cwe_ids=null` 而 OSV/NVD 均有 CWE-208；评分采纳 NVD CISA-ADP 3.1 5.3 MEDIUM
  （GHSA 4.0 2.7 LOW，Django 说明 low）；keyserver 404，签名对 GitHub 公布公钥验证。
- **状态**：卷宗 README 标 PROMOTED；队列/漏斗/HANDOFF/LIMITATIONS 同步。
  **未声称完成、未重生成 CHECKSUMS、未做 release**；下一条候选为
  CVE-2026-25674（`disc2_f08644f4f856311a218b8f05`，卷宗在建）。

## 2026-10-25 — django CVE-2026-25674 卷宗建包（待独立复核，不写 `data/`）

- **候选**：`disc2_f08644f4f856311a218b8f05`（`possible_affected`，basis 仅范围
  命中），快照 `snap_516aa9971dd9509d` / tag 4.2.13（commit `3bf46e2e…`）；
  CVE-2026-25674 / `GHSA-mjgh-79qc-68w3` / `PYSEC-2026-2449` /
  `BIT-django-2026-25674`，CWE-362。选它之前已把 4.2 线其余 10 条队列行逐条
  处置（`runs/scouting_2026-10-25/README.md`）。
- **评分**：NVD 无 Primary，唯一 CVSS 是 CISA-ADP Secondary 3.1 **3.7 LOW**
  `AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`（CVE/PYSEC 重复）；GHSA
  `database_specific.severity = LOW`（无分数）、Bitnami Low、Django 4.2.29
  发布说明 "low"——四方在等级上一致，但 3.7 仍是次要向量。
- **修复**：4.2 `54b50bf7…`（stable/4.2.x，2026-01-21，自称 main `019e44f6…`
  的 backport）、5.2 `b07ed2a1…`、6.0 `264d5c70…`；首发 4.2.29
  （tag object `64e4e3b9…`、commit `f2ec75ef…`、tree `b52696ee…`，2026-03-03），
  最后受影响 4.2.28（tag object `059b53d3…`、commit `20c71f6b…`）。
- **机制**：4.2.13 `django/core/files/storage/filesystem.py` `_save()`
  在 `directory_permissions_mode` 非空时用进程级
  `os.umask(0o777 & ~mode)` 包住 `os.makedirs()`（76-85，finally 恢复）；
  `filebased.py` `_createdir()` 同法（116-123，`os.umask(0o077)` 包 0o700）。
  4.2.29 引入 `django/utils/_os.py` 的 `makedirs()`/`safe_makedirs()`
  （mkdir 后逐层 chmod，不碰全局 umask），两处调用点改写并新增
  `SafeMakeDirsTests.test_permissions_correct_despite_umask_change` 类回归测试。
- **实测**（`sources/probe_{4213,4228,4229}_run{1,2}.jsonl`，进程内、三版 venv、
  各跑两次）：control（`directory_permissions_mode=None`）三版都 `[]`；
  trigger（0o700/0o600、200 次 24 层深保存）4.2.13 调用 `["0o77","0o22"]`、
  canary 异常对象 4234/4199，4.2.28 为 4291/4295，4.2.29 调用 `[]`、异常 **0**；
  cache 首写 4.2.13/4.2.28 为 `["0o77","0o22"]`、4.2.29 `[]`。三版叶子目录
  0o700、叶子文件 0o600——差异只在并发第三方对象的权限上。
- **建包**：`collect_sources.py` 钉住 34 件产物（四份 OSV、NVD、GHSA 页、
  weblog、4.2.29 与 4.2.28 发布说明、三份 PyPI、9 份 raw 文件、四条线补丁、
  代码摘录、tag/祖先/逐 tag 守卫扫描、6 份探测日志、wheels），`build_dossier.py`
  断言后写 `dossier.json`（39,057 字节、32 条证据、7 条 limitations、
  16 个字段映射）。建包时修正三处断言：发布说明里 "low" 出现两次（同页还有
  25673 的 "moderate"）、守卫扫描行含 sha 后缀、`{tag:7s}` 对 6.0.2 多一个
  空格；另把 7 条本地产物的 `source_url` 改成指向被探测代码的 permalink
  （evidence schema 要求 `^https://`）。
- **状态**：卷宗 README 标 READY_FOR_INDEPENDENT_REVIEW，派发隔离复核
  （round22，`runs/independent/django_CVE-2026-25674_4213_round22/`）；
  **未写 `data/`，未改 triage 行**，候选维持 `possible_affected`。
- **round22 回执（2026-10-24T18:35:49Z）**：`confirmed_affected` / grade
  A，复核方 `independent-reviewer-round22/deepseek-flash`，位置
  `filesystem.py` 76-85（line 79），九项字段全部为真，`fix_commit 54b50bf7…`
  与卷宗一致；`promote_verified_rows.py` 2026-10-24T18:37:10Z 写入
  `data/`（1 vuln / 1 location / 1 review / 42 evidence / 1 svs），
  复核随附的 red/green 记录（`reproduction/probe_umask.py` 与 7 份 JSONL）
  留档。复核指出卷宗 README 引用的 4.2.13 注释文字与实际源码不符（行号
  76-85 本身正确），已在 README 中改为 `sources/raw_filesystem_4213.py`
  的真实文本。候选 `disc2_f08644f4f856311a218b8f05` 已改写为
  `confirmed_affected`（备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round22_20261024T183712Z.jsonl`）；
  队列重算 563 行（django 18），`queue_P3.json` 为 DONE 127 / P1_VERIFY 563。

### CVE-2026-48588 卷宗建包（2026-10-25）

- 目标：`django/django` 快照 `snap_516aa9971dd9509d`（tag 4.2.13，commit
  `3bf46e2e…`），候选 `disc2_f805f93b227052047bcaf78f`（当前
  `possible_affected`，basis 为 `GHSA-3h9f-r86x-qvjx[introduced 0, fixed
  5.2.16]` 范围命中）。路径
  `runs/verification/django_CVE-2026-48588_4213/`。
- **建包**：`collect_sources.py` 钉住 39 件产物（四份 OSV、NVD、GHSA 页、
  2026-07-07 weblog、5.2.16/5.2.15/6.0.7/4.2.30 发布说明、5.2.16 安装 FAQ、
  三份 PyPI、12 份 raw 文件、三条线补丁、代码摘录、tag/祖先/逐 tag 守卫扫描、
  6 份探测日志、wheels、manifest）。`build_dossier.py` 逐条断言后写
  `dossier.json`（48,570 字节、40 条证据、19 个字段映射、9 条 limitations）。
  建包时踩到两处：一次 `pip download` 装三个钉死版本触发
  `ResolutionImpossible`，改为每版单独一次下载；`4.2.0`/`5.2.0` 不是有效 tag
  （`fatal: invalid object name` 被 `2>/dev/null` 吞掉，grep 误报守卫缺失），
  改用真实 tag `4.2` / `5.2` 后确认两者都带漏洞守卫。
- **源码事实**：4.2.13 `django/middleware/cache.py:91-98` 的守卫是
  `if (not request.COOKIES and response.cookies and
  has_vary_header(response, "Cookie"))`，第 94 行的 `not request.COOKIES`
  是关键操作；`cache_page()`（`views/decorators/cache.py:8-26`）经
  `decorator_from_middleware_with_args(CacheMiddleware)` 走同一段
  `process_response`。逐 tag 守卫扫描：4.2/4.2.1/4.2.13/4.2.30 的
  `cache.py` 逐字节相同（sha256 `5807cc01…`）且都带漏洞守卫；5.2/5.2.14/
  5.2.15 同形态；5.2.16 与 6.0.7 为无条件
  `if response.cookies and has_vary_header(response, "Cookie"): return
  response`。
- **4.2 无修复版本**：Django 4.2 LTS 安全支持 2026 年 4 月结束（5.2.16 文档
  原文），修复 2026-06-11 三线提交（`721685aa` 5.2.x、`64f9a2b2` 6.0.x、
  `6e365f8d` main）、2026-07-07 随 5.2.16 / 6.0.7 发布；4.2 最后一个版本
  4.2.30（2026-04-07）仍带漏洞守卫，其发布说明未提本 CVE。卷宗
  `fixed_releases` 只记 5.2.16 与 6.0.7，**未编造 4.2.31**。
- **实测**（`sources/probe_{4213,5215,5216}_run{1,2}.jsonl`，进程内
  LocMemCache + `django.test.Client`，五个用例、两轮一致）：无 Cookie 对照组
  三版都 `keys=0`、视图调用 2 次；`junk=1` 两次请求在 4.2.13/5.2.15 上
  `keys=2`（中间件）/`keys=4`（`cache_page`）、`holds_private_token=True`、
  第二次命中缓存（调用 1 次），5.2.16 全部 `keys=0`、调用 2 次。
  4.2.13 与 5.2.15 的 probe 输出完全相同。
- **评分离散**：NVD Primary 3.1 5.3 MEDIUM，同条 NVD 另有 CNA Secondary
  3.1 3.1 LOW 与 4.0 2.3 LOW；GHSA LOW、Bitnami Medium、Django 发布说明
  "low"。卷宗采用 NVD Primary 5.3 并在 severity 里记录全部六个值，README
  写明厂商自评为 low。
- **状态**：`dossier.json` 标 READY_FOR_INDEPENDENT_REVIEW，派发隔离复核
  （round23，`runs/independent/django_CVE-2026-48588_4213_round23/`）；
  **未写 `data/`，未改 triage 行，未动 CHECKSUMS**，候选维持
  `possible_affected`。
- **round23 回执（2026-10-24T18:50:25Z）**：`confirmed_affected` / grade A，复核方
  `independent-reviewer-round23/deepseek-flash`；位置
  `django/middleware/cache.py:94`（条件 `93-97`），九项字段全部为真，
  `vulnerable_commit` 为快照提交 `3bf46e2e…`（另记
  `introduced_by_commit c083e381…`，2014 年守卫起点），`fix_commit 721685aa…`，
  `fixed_release 5.2.16`（另 6.0.7，4.2.x 无）。复核方自写两套探针（进程内
  `CacheMiddleware` 与真实 WSGI handler），5 个版本 × 2 轮日志 sha256 完全一致、
  stderr 全 0 字节；4.2.13/5.2.15/6.0.6 `leak=True`，5.2.16/6.0.7 `leak=False`，
  负对照（无 Cookie）与正对照（无 `Set-Cookie`）均符合预期；其测到的
  `cache.py` 字节哈希与卷宗逐 tag 扫描逐位一致。`preserved_sha256.txt` 72 项全部
  匹配、10 条 reproduction 路径全部存在（本会话复核）。
- **字段语义对齐**：首版 verdict 把 `vulnerable_commit` 写成 2014 引入提交、
  `aliases` 漏主 CVE id、`last_affected_release` 未分分支，均已请复核方按自己的
  证据重发；`cvss` 新增 `catalog_recommendation`（建议 2.3 LOW）。卷宗据此把
  severity 从 NVD Primary 5.3 改为 CNA/厂商 CVSS 4.0 2.3 LOW（NVD 5.3 仍保留在
  `all_published_scores`），limitations 9 → 10（新增 6.1 线 `c2a936ab…` 未点名
  一条），dossier 重建后 50,240 字节 / 40 条证据 / 19 个字段映射。
- **写库**：`promote_verified_rows.py --apply` 2026-10-24T18:53:18Z 写入
  （1 vuln / 1 location / 1 review / 52 evidence / 1 svs）；triage 行
  `disc2_f805f93b227052047bcaf78f` 改写为 `confirmed_affected`（备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round23_20261024T185325Z.jsonl`）；
  队列重算 562 行（django 17、range_precise 384），`queue_P3.json` 为
  DONE 128 / P1_VERIFY 562 / P1_REVIEW 574 / ARCHIVE 1349 / P0_SELECT 13。
- **顺带修掉 round22 遗留缺陷**：25674 的 dossier `field_evidence` 没有任何
  `critical_operation` 映射，validator 报
  `location loc_25674_snap_516aa9971dd9509d: no PASS root cause evidence`（此前
  用 `head/tail` 截断查看校验输出，误报为「0 error」）。已在 25674 的
  `build_dossier.py` 补映射并重建 dossier（39,121 字节 / 32 证据 / 17 字段映射），
  再用 `runs/data_fixes/backfill_25674_critical_operation_evidence_2026-10-25.py`
  追加 3 条 location 证据并同步 status 行的 `evidence_ids`（备份
  `evidence_before_25674_critical_operation_20261024T185359Z.jsonl` 与
  `snapshot_vulnerability_status_before_25674_critical_operation_20261024T185359Z.jsonl`）。
  现 `validate_dataset.py --draft`：0 error / 49 warning，137 vuln / 137 location /
  4836 evidence / 137 review / 108 svs。

### CVE-2026-8404 卷宗建包（2026-10-25，round24，待独立复核）

- **候选**：`disc2_28514ab37f4ffb059c923fdb`（django/django @ `snap_516aa9971dd9509d` /
  4.2.13，队列 `range_precise`，记录 `GHSA-8cjm-8mp7-r2xf`，范围
  `introduced 0, fixed 5.2.15`）。队列中排在 53877（GDALRaster，需要 GDAL）之后，
  本会话选择先做无重依赖的 8404。
- **证据**：新建 `runs/verification/django_CVE-2026-8404_4213/`，
  `collect_sources.py` 产出 43 个 sha256 钉住的文件（4 个 OSV、NVD、GHSA 页面、
  2026-06-03 weblog、5.2.15 / 6.0.6 / 4.2.30 release notes、FAQ EOL、
  3 份 PyPI JSON、7 个 tag 的 `cache.py` + 2 个 decorator、4 条分支修复补丁、
  `#36560` 补丁、摘录、tag/祖先/守卫扫描、6 版本 × 2 轮探针日志、6 个 wheel
  sha256）。`build_dossier.py` 对每条公告字段、范围、CPE、评分、release notes
  文本、4.2 无补丁事实、祖先矩阵和探针矩阵逐项断言，任何失败即拒绝写
  `dossier.json`。
- **探针**（`bench.py`，自写）：`django.test.Client` + LocMemCache，alice →
  bob → 匿名三客户端；`private` 小写为负对照，`Private` / `pRiVaTe` /
  `Private, max-age=60` / decorator 路径为机制 case，`No-Store` / `no-cache`
  为相邻 #36560 case，`public, max-age=60` 为正对照。4.2.13 / 4.2.30 / 5.2.14 /
  6.0.5 全部缓存并泄漏 alice 响应体；5.2.15 / 6.0.6 全部拒绝；正对照 6 个版本
  均缓存。每版本跑两遍，去掉随机 temp 路径后逐字段一致、stderr 全 0 字节。
- **事实结论**：修复在 5.2.15 / 6.0.6（5.2 线 `366d9ae6…`、6.0 线 `b4330259…`、
  main `d618d7ae…`、6.1 线 `130467c8…`）；4.2 线无修复（EOL 2026-04，最后版本
  4.2.30 于 2026-04-07，`4.2.13..4.2.30` 之间 `cache.py` 零提交、字节相同、
  无 4.2.31）。公告口径不一致：只有 GHSA 的 `introduced 0` 范围覆盖 4.2，
  CNA 原文只把 5.0.x/4.1.x/3.2.x 列为"未评估"，未点名 4.2。同一修复提交还
  顺带 backport 上游 #36560（no-cache/no-store），不属于本案描述。
- **卷宗**：`dossier.json` 99,456 字节 / 38 条证据 / 19 个字段映射 / 11 条限制，
  状态 READY_FOR_INDEPENDENT_REVIEW；`critical_operation` 为
  `django/middleware/cache.py:100-101`，快照提交 `3bf46e2e…`。
- **状态**：派发隔离复核（round24，`runs/independent/django_CVE-2026-8404_4213_round24/`）；
  预写 triage 改写脚本 `runs/data_fixes/promote_2026_8404_triage_round24_2026-10-25.py`
  （dry-run 因缺 vuln 行按预期拒绝）。**未写 `data/`，未改 triage，未动
  CHECKSUMS**。

### CVE-2026-48587 卷宗建包（2026-10-25，round25，待独立复核）

- **候选**：`disc2_d9fa741af9a342d325abcbc7`，`django/django` @ 4.2.13
  （快照 `snap_516aa9971dd9509d`，队列记录 `GHSA-923m-gv2p-w5qp`，
  `introduced 0, fixed 5.2.15`）。与 8404 同一安全发布，共用 6 个 wheel 环境。
- **证据**：新建 `runs/verification/django_CVE-2026-48587_4213/`，
  `collect_sources.py` 产出 49 个 sha256 钉住的文件（4 个 OSV、NVD、GHSA 页面、
  weblog、5.2.15 / 6.0.6 / 4.2.30 release notes、FAQ EOL、3 份 PyPI JSON、
  7 个 tag 的 `utils/cache.py` 与 `middleware/cache.py`、4 条修复补丁、
  2 条 helper 后续提交、摘录、tag/祖先/守卫扫描、6 版本 × 2 轮探针日志、
  6 个 wheel sha256）。`build_dossier.py` 对公告字段、范围、CPE、评分、
  release notes 文本、4.2 无补丁与无通配守卫、祖先矩阵和探针矩阵逐项断言，
  任何失败即拒绝写 `dossier.json`。
- **探针**（`bench.py`，自写）：`django.test.Client` + LocMemCache，覆盖
  `Vary: *` / `" *"` / `"* "`、`Vary: Cookie` / `" Cookie"`（无 Cookie 请求
  收到 `Set-Cookie`）、以及 `public` 正对照。4.2.13 / 4.2.30 没有通配守卫，
  普通 `*` 也缓存（与本 CVE 无关，单独标注）；5.2.14 / 6.0.5 被空格绕过；
  5.2.15 / 6.0.6 拒绝。Cookie 守卫路径在 4.2.13 / 4.2.30 / 5.2.14 / 6.0.5
  上缓存并把 alice 的响应体与 `Set-Cookie` 回放给 bob；5.2.15 / 6.0.6 不回放。
  每版本跑两遍，去掉随机 temp 路径后逐字段一致、stderr 全 0 字节。
- **事实结论**：修复在 5.2.15 / 6.0.6（5.2 线 `9b62b0af…`、6.0 线 `1721035a…`、
  main `42aa0b33…`、6.1 线 `e06958db…`，四条独立 cherry-pick；6.1 另有
  `e30a5c83…` 引入 `split_header_value()`）。4.2 线无修复（EOL，最后版本
  4.2.30，两个 cache 文件与 4.2.13 字节相同，fix 合入晚于 EOL）。GHSA 的
  `introduced 0` 与版本列表覆盖 4.2，CVE/PYSEC/Bitnami/NVD 从 5.2 起，
  CNA 原文不点名 4.2。release notes 只描述 `Vary: *` 路径，而 CVE 描述更宽；
  4.2 上与修复相关的只有 Cookie 守卫，判断留给复核方。
- **已知残余（记录、不作证据）**：5.2.15 / 6.0.6 的 `learn_cache_key()` 仍用
  `cc_delim_re` 且不 strip，带空格的 Vary 头名仍会让缓存 key 忽略该头；探针
  第三个请求在修复版本上仍可看到 bob 响应被匿名请求复用。
- **卷宗**：`dossier.json` 97,942 字节 / 43 条证据 / 19 个字段映射 / 12 条限制，
  状态 READY_FOR_INDEPENDENT_REVIEW；`critical_operation` 为
  `django/utils/cache.py:330-332`，快照提交 `3bf46e2e…`；内存 schema 预校验
  （vulnerability / location / 78 条 evidence）零错误。
- **状态**：派发隔离复核（round25，`runs/independent/django_CVE-2026-48587_4213_round25/`）；
  预写 triage 改写脚本 `runs/data_fixes/promote_2026_48587_triage_round25_2026-10-25.py`
  （dry-run 因缺 vuln 行按预期拒绝）。**未写 `data/`，未改 triage，未动 CHECKSUMS**。

### CVE-2026-8404 复核完成并提升（2026-10-25，round24）

- **独立 verdict**：`runs/independent/django_CVE-2026-8404_4213_round24/`，
  `confirmed_affected` / grade **A**，reviewer_identity 与卷宗 `prepared_by` 不同；
  `vulnerable_commit` 为快照提交 `3bf46e2e…`；九个字段全部 `true`；
  定位 `django/middleware/cache.py:100-101`（重叠卷宗 100-101）；
  `reproduction_reference` 指向自写 `probe_cache_control.py` 与 7 版本 × 2 轮日志。
  `preserved_sha256.txt` 的 56 个文件逐条复算，0 缺失 / 0 不一致。
- **复核要点**：4.2.13 第 101 行大小写敏感的子串测试；4.2.30 与 4.2.13 的
  `cache.py` blob 相同；自建探针在 4.2.13 / 4.2.30 上复现 `Private` 跨用户泄漏，
  5.2.15 / 6.0.6 / 6.1 全绿；4.2 线 EOL 且无修复版本，`fixed_releases` 不记 4.2。
- **提升**：`promote_verified_rows.py --apply` 写入 1 vuln / 1 location / 1 review /
  67 evidence / 1 status（`applied_at` 2026-10-24T19:17:59Z）；
  `runs/data_fixes/promote_2026_8404_triage_round24_2026-10-25.py --apply`
  把 `disc2_28514ab37f4ffb059c923fdb` 改为 `confirmed_affected`（先 dry-run，
  写备份 `snapshot_candidate_triage_before_promoted_rows_round24_20261024T191801Z.jsonl`）。
- **校验与重排**：`validate_dataset.py . --draft` 结构校验通过（0 error）；
  `build_queue.py` 重跑 = alias_osv 42 / nvd_cpe 23 / range_coarse 83 /
  range_precise 383 / legacy_triage 30（合计 561）；
  `plan_snapshot_queue.py` 重跑 = P0 13 / P1_VERIFY 561 / P1_REVIEW 574 /
  DONE 129 / ARCHIVE 1349。
- **计数同步**：triage 129 / 1321 / 561 / 28 / 574，`pending_relevant_triage` 1135；
  HANDOFF、CANDIDATE_FUNNEL、LIMITATIONS_V031 已改成现值。
  **未动 CHECKSUMS，未声明完成 / PASS_KNOWN_SWEEP / release。**

### CVE-2026-6873 卷宗建包（2026-10-25，round26，待独立复核）

- **候选**：`disc2_eab6d1a548b2f2a6e24d1666`（django/django @ 4.2.13，
  快照 `snap_516aa9971dd9509d`，队列记录 `GHSA-h7pc-vwp9-298g`，
  `introduced 0, fixed 5.2.15`）。同一 2026-06-03 安全发布的第三案。
- **证据**：新建 `runs/verification/django_CVE-2026-6873_4213/`，
  `collect_sources.py` 产出 56 个 sha256 钉住的文件（4 个 OSV、NVD、GHSA 页面、
  weblog、5.2.15 / 6.0.6 / 4.2.30 release notes、FAQ EOL、3 份 PyPI JSON、
  7 个 tag 的 `request.py` / `response.py` / `signing.py`、4 条修复补丁、
  2 条 fallback 默认值后续提交、摘录、tag/祖先/代码矩阵、6 版本 × 2 轮探针
  日志、6 个 wheel sha256）。`build_dossier.py` 逐项断言公告字段、范围、CPE、
  评分、notes 文本、helper 格式、祖先矩阵与探针矩阵，失败即拒绝写
  `dossier.json`。
- **探针**（`bench.py`，自写）：视图固定读 `get_signed_cookie("ab", salt="c")`，
  用 `(a, bc)` 与 `(ab, c)` 的拼接碰撞构造跨上下文 cookie。4.2.13 / 4.2.30 /
  5.2.14 / 6.0.5 默认接受碰撞；5.2.15 / 6.0.6 只接受 legacy 回退
  （`SIGNED_COOKIE_LEGACY_SALT_FALLBACK` 默认 True），strict 才拒绝；
  6.1 默认 False（只做文件级检查）。无关盐对在所有版本都拒绝；
  每版本两轮、stderr 全 0 字节。
- **事实结论**：修复在 5.2.15 / 6.0.6 / 6.1（5.2 线 `594360cb…`、6.0 线
  `c807d9c3…`、6.1 线 `42bdfd74…`、main `70d36515…`，author 日期 2026-05-08）；
  helper 为 `f"django.http.cookies.v2:{len(salt)}:{salt}{cookie_name}"`。
  4.2 线无修复（EOL 2026-04，最后版本 4.2.30 于 2026-04-07，修复晚于 EOL，
  无 4.2.31）；4.2.13 与 4.2.30 的 request.py 因 CVE-2026-33034 不同，
  但两版都保留 `key + salt`。GHSA 的 `introduced 0` 与 versions 列表覆盖
  4.2，CVE/PYSEC/Bitnami/NVD 从 5.2 起；GHSA 记录缺全部 6.0.x。
- **卷宗**：`dossier.json` 102,124 字节 / 57 条证据 / 19 个字段映射 /
  12 条限制，READY_FOR_INDEPENDENT_REVIEW；`critical_operation` 为
  `django/http/request.py:191`，快照提交 `3bf46e2e…`；用 promote 脚本的
  helpers 做内存 schema 预校验（vulnerability / location / 76 条 evidence）
  **零错误**（中途修正 advisory_status 与 location 子对象结构）。
- **状态**：派发隔离复核（round26，
  `runs/independent/django_CVE-2026-6873_4213_round26/`）；预写 triage 改写脚本
  `runs/data_fixes/promote_2026_6873_triage_round26_2026-10-25.py`
  （dry-run 因缺 vuln 行按预期拒绝）。**未写 `data/`，未改 triage，
  未动 CHECKSUMS**。

## 2026-10-24 — django CVE-2026-48587 round25 独立复核完成并提升

- **复核**：`runs/independent/django_CVE-2026-48587_4213_round25/`，隔离复核
  身份 `independent-reviewer/deepseek-flash-round25`（自建 clone / venv / 抓取 /
  探针），verdict `confirmed_affected`、grade **A**、`vulnerable_commit`
  `3bf46e2e…`；九字段全部独立判定为 true；位置 `django/utils/cache.py:326-334`
  与卷宗的 `326-332` 在同一 `has_vary_header` 函数内重叠；59 个 preserved
  文件逐个 sha256 校验 0 坏。
- **机制**：4.2.13 / 4.2.30 的 `has_vary_header()` 只做 `.lower()`，不做
  `.strip()`；`cc_delim_re` 只吃逗号两侧空白。`Vary: " Cookie"` 因此不被识别为
  已含 Cookie，缓存响应带上 alice 的 `Set-Cookie: sessionid=…` 并被 bob 命中。
  5.2.15 / 6.0.6 的修复在两处补 `.strip()`（5.2 `9b62b0af71…`、6.0
  `1721035a72…`、6.1 cherry-pick `e06958dbff…`、main `42aa0b3364…`）；
  **4.2 线没有补丁**（4.2.30 为最后一版，早于 CVE）。
- **范围裁定**：CVE/PYSEC/Bitnami/NVD 的范围从 5.2 起、不含 4.2；只有 GHSA 的
  `introduced 0 -> 5.2.15` 与 versions 列表覆盖 4.2，属范围算术 artifact。
  复核方另把 `exact_wildcard` 泄漏归因于 CVE-2026-6907（4.2 从未获得该守卫），
  没有算进本 CVE。
- **提升**：`promote_verified_rows.py --apply` 追加 vulnerabilities / locations /
  reviews / evidence 77 条 / snapshot status 各 1；
  `runs/data_fixes/promote_2026_48587_triage_round25_2026-10-25.py --apply`
  把 `disc2_d9fa741af9a342d325abcbc7` 改为 `confirmed_affected`
  （备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round25_20261024T192729Z.jsonl`）。
  `scripts/validate_dataset.py --draft` **STRUCTURAL VALIDATION PASSED**。
- **计数**：triage 2613 = confirmed_affected **130** / confirmed_not_affected 1321 /
  possible_affected **560** / duplicate 28 / unknown 574；vulns 139、reviews 139
  （grade A **64** / B 75）；django 新快照 possible 15。
- **队列**：`runs/possible_review_queue_2026-10-24/build_queue.py` 与
  `v031/scripts/plan_snapshot_queue.py . --out v031/reports/queue_P3.json` 已按
  当前 560 行重跑（alias_osv 42 / nvd_cpe 23 / range_coarse 83 /
  range_precise 382 / legacy 30；P1_VERIFY 560、P1_REVIEW 574、DONE 130）。
- **仍未完成**：CVE-2026-6873 round26 复核仍在跑；CVE-2026-1312 的下一卷宗
  探针环境已建（4.2.13 / 4.2.27 / 4.2.28），卷宗尚未成文。未声明数据集完成、
  未重生成 CHECKSUMS。

## 2026-10-24 — django CVE-2026-6873 round26 独立复核完成并提升

- **复核**：`runs/independent/django_CVE-2026-6873_4213_round26/`，隔离复核
  身份 `independent security reviewer (deepseek-flash, round26, isolated: no
  collector packet or dataset access)`（自建 clone / venv / 抓取 / 探针，
  未读采集方 packet、`data/` 等）；verdict `confirmed_affected`、grade **A**、
  `vulnerable_commit` `3bf46e2e…`；九字段全部独立判定为 true；位置
  `django/http/request.py:191` 与卷宗一致（另记录写路径
  `django/http/response.py:282`）；109 个 preserved 文件逐个 sha256 校验
  0 坏 / 0 缺。
- **机制**：4.2.13 的 `HttpRequest.get_signed_cookie()` 用
  `signing.get_cookie_signer(salt=key + salt)` 派生 cookie 签名 salt；拼接不是
  单射，`("a","bc")` 与 `("ab","c")` 都变成 `abc`，共享同一签名命名空间，
  一对上下文签发的 cookie 在另一对下被接受。写路径
  `HttpResponse.set_signed_cookie()` 同样拼接。5.2.15 / 6.0.6 引入
  `_cookie_signer_salt` / v2 salt 与 `SIGNED_COOKIE_LEGACY_SALT_FALLBACK`
  （默认 True，仅保护新签发 cookie）；6.1 起默认 False。**4.2 线无修复版**
  （4.2.30 为最后一版，2026-04-07；stable/4.2.x 于 2026-04-24 打 EOL tag）。
- **范围裁定**：GHSA `introduced 0 -> 5.2.15` 覆盖 4.2.13；NVD / PYSEC /
  Bitnami / CVE-OSV 只列 5.2/6.0。复核方在实际执行中确认 4.2.13 受影响
  （红/绿矩阵 7 个 release × 3 种 setting 共 21 次执行，含阴性对照，另跑通
  上游 12 个 signed-cookie 测试）。GHSA `introduced 0` 与 6.0 范围重叠、
  OSV GIT 范围把 release tag 当引入 commit，均作为上游不一致记录。
- **提升**：`promote_verified_rows.py --apply` 追加 vulnerabilities / locations /
  reviews / evidence 75 条 / snapshot status 各 1；
  `runs/data_fixes/promote_2026_6873_triage_round26_2026-10-25.py --apply`
  把 `disc2_eab6d1a548b2f2a6e24d1666` 改为 `confirmed_affected`
  （备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round26_20261024T193114Z.jsonl`）。
  `scripts/validate_dataset.py --draft` **STRUCTURAL VALIDATION PASSED**
  （0 error / 49 warning）。
- **计数**：triage 2613 = confirmed_affected **131** / confirmed_not_affected 1321 /
  possible_affected **559** / duplicate 28 / unknown 574；vulns 140、reviews 140
  （grade A **65** / B 75）；django 新快照 possible 14。
- **队列**：`runs/possible_review_queue_2026-10-24/build_queue.py` 与
  `v031/scripts/plan_snapshot_queue.py . --out v031/reports/queue_P3.json` 已按
  当前 559 行重跑（alias_osv 42 / nvd_cpe 23 / range_coarse 83 /
  range_precise 381 / legacy 30；P1_VERIFY 559、P1_REVIEW 574、DONE 131、
  ARCHIVE 1349、P0_SELECT_SNAPSHOT 13）。
- **仍未完成**：CVE-2026-1312 的卷宗构建中（探针红/绿已取得，收集包 52 件
  已 pin）；未声明数据集完成、未重生成 CHECKSUMS。

## 2026-10-25 — django CVE-2026-1312 采集包完成，派发 round27 隔离复核

- **采集**：`runs/verification/django_CVE-2026-1312_4213/`，`collect_sources.py`
  钉住 **52** 个 artifact（OSV CVE/GHSA/PYSEC/Bitnami、NVD、GHSA 页面、
  2026-02-03 weblog、4.2.28/4.2.27/5.2.11/6.0.2 release notes、FAQ、3 个 PyPI
  版本、8 个 tag 的 `query.py`/`compiler.py`、4.2.27/4.2.28 的 ordering 与
  filtered_relation 测试、8 条 fix patch、编号源码摘录、tag/commit/祖先/代码
  矩阵、6 份探针日志、wheel sha256），manifest 逐件复核字节与 sha256 一致。
- **探针**：venv 4.2.13 / 4.2.27 / 4.2.28（asgiref 3.8.1 + sqlparse 0.5.3），
  每版两遍、两份 JSONL 字节相同、stderr 0 字节。红/绿：4.2.13 与 4.2.27 接受
  带点的 `FilteredRelation` 别名并把 `ORDER BY ("probe_article".pub_date)` 写进
  SQL（行序被改写），跨表别名产生 `probe_author.name` 与
  `OperationalError: no such column`；4.2.28 抛
  `ValueError: FilteredRelation doesn't support aliases with periods`。
  `extra(order_by=...)` 的合法点号在三版都可用（固定路径未误伤）。
- **代码矩阵**：4.2.13/4.2.27 三项守卫全 False；4.2.28/4.2.30 全 True；
  5.2.10/6.0.1 全 False；5.2.11/6.0.2 全 True。4.2.28 与 4.2.30 的
  `query.py`/`compiler.py` sha256 相同。4.2 两条修复只进 4.2.28/4.2.30，
  不是 4.2.13/4.2.27 的祖先。
- **卷宗**：`build_dossier.py` 全断言通过后产出 `dossier.json`（96,290 字节 /
  52 evidence / **18** 字段映射 / 9 限制，READY_FOR_INDEPENDENT_REVIEW）；
  用 promoter 的 `validate_rows` 做内存 schema 预校验 82 条 evidence、0 error。
  `critical_operation` = `django/db/models/sql/compiler.py:405-413`，
  `entry_point` = `query.py:1622-1632`，快照提交 `3bf46e2e…`；中文 `README.md`
  写明隔离规则与待复核方独立裁定的三处冲突（affected_ranges 的 CVE GIT
  `97aa3b7f` 倒置、CVSS 5.4 vs NVD Secondary 8.5 vs Django "high"、
  同批 CVE-2026-1287 控制字符修复是否计入）。
- **状态**：派发隔离复核 round27（`runs/independent/django_CVE-2026-1312_4213_round27/`）；
  预写 triage 改写脚本
  `runs/data_fixes/promote_2026_1312_triage_round27_2026-10-25.py`
  （dry-run 因缺 vuln 行按预期拒绝）。**未写 `data/`，未改 triage，
  未动 CHECKSUMS**。

## 2026-10-25 — django CVE-2026-1287 采集包完成，派发 round28 隔离复核

- **采集**：`runs/verification/django_CVE-2026-1287_4213/`，
  `collect_sources_1287.py` 钉住 **37** 个 artifact（OSV CVE/GHSA/PYSEC/
  Bitnami、NVD、GHSA 页面、2026-02-03 weblog、4.2.28/4.2.27/5.2.11/6.0.2
  release notes、3 个 PyPI 版本、8 个 tag 的 `query.py`、4.2.27/4.2.28 的
  annotations 测试、4 条 fix patch、编号源码摘录、tag/commit/祖先/代码矩阵、
  6 份探针日志、wheel sha256），builder 逐件复核字节与 sha256。
- **探针**：venv 4.2.13 / 4.2.27 / 4.2.28，每版两遍、两份 JSONL 字节相同、
  stderr 0 字节。红/绿：4.2.13 与 4.2.27 接受控制字符别名，
  `annotate` 产出 `AS "name\x01"`、`values` 产出 `AS "name\x9f"`、
  `extra(select=...)` 产出 `AS "name\x01"`、`aggregate` 返回键 `name\x01`；
  4.2.28 对六个入口全部抛
  `ValueError: Column aliases cannot contain whitespace characters, hashes,
  control characters, ...`。NUL 字节在 4.2.13/4.2.27 是 SQLite 执行期
  `ProgrammingError`，4.2.28 是更早的 `ValueError`；`name#x` 只在 4.2.13
  被接受（4.2.27 起有 CVE-2025-59681 的 `#` 守卫），记为 collateral。
- **代码矩阵**：4.2.13 控制字符 False/哈希守卫 False；4.2.27 False/True；
  4.2.28 与 4.2.30 均 True/True 且 `query.py` sha256 相同；5.2.10/5.2.11、
  6.0.1/6.0.2 同样按修复翻转。祖先矩阵：4.2 `f75f8f3597` 只进 4.2.28/
  4.2.30，5.2 `3e68ccdc11` 只进 5.2.11，6.0 `0c0f5c2178` 只进 6.0.2，
  main `e891a84c7e` 不在任何 release tag。
- **卷宗**：`build_dossier_1287.py` 全断言通过后产出 `dossier.json`
  （87,114 字节 / 37 evidence / **18** 字段映射 / 10 限制 /
  READY_FOR_INDEPENDENT_REVIEW）；用 promoter 的 `validate_rows` 做内存
  schema 预校验 **77** 条 evidence、0 error。`critical_operation` =
  `django/db/models/sql/query.py:1123-1128`（`Query.check_alias`），
  `entry_point` = `query.py:1130-1138`（`add_annotation`），快照提交
  `3bf46e2e…`；中文 `README.md` 写明隔离规则与待复核方独立裁定的四处冲突
  （CVE GIT `97aa3b7f` 倒置、CVSS 5.4 vs NVD Secondary 8.3 vs GHSA CVSS 4.0
  HIGH、`alias()`/`FilteredRelation` 只登记不发射的验收口径、CVE-2025-59681
  的 `#` 守卫是否计入）。
- **状态**：派发隔离复核 round28
  （`runs/independent/django_CVE-2026-1287_4213_round28/`）；预写 triage 改写
  脚本 `runs/data_fixes/promote_2026_1287_triage_round28_2026-10-25.py`
  （dry-run 因缺 vuln 行按预期拒绝）。**未写 `data/`，未改 triage，
  未动 CHECKSUMS**。

## 2026-10-25 — CVE-2026-1312 round27 复核通过并提升

- **复核**：`runs/independent/django_CVE-2026-1312_4213_round27/verdict.json`，
  `reviewer_identity=independent-reviewer-round27-deepseek-flash`（≠ prepared_by），
  `reviewed_at=2026-10-24T19:39:58Z`，`confirmed_affected` / grade **A**，
  九字段全 true，`vulnerable_commit=3bf46e2e…`；location
  `django/db/models/sql/compiler.py:405`（`SQLCompiler._order_by_pairs`）与卷宗
  `critical_operation` 405-413 重叠。`preserved_sha256.txt` 51 个文件（sha256 + 字节数）
  逐件重算，0 缺失/0 不符；`reproduction_reference` 含 probe、两遍日志、
  results_matrix、fix_diffs、wheel_provenance、git_facts 与上游测试红/绿。
- **提升**：`promote_verified_rows.py --apply` 追加 vulnerabilities 1、locations 1、
  reviews 1、evidence 82、snapshot_vulnerability_status 1，grade A，无 conflict；
  triage 行 `disc2_347876bad6fbc9f296c7c7b8` 经
  `runs/data_fixes/promote_2026_1312_triage_round27_2026-10-25.py --apply` 改为
  `confirmed_affected`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round27_20261024T194100Z.jsonl`。
- **校验**：`validate_dataset.py . --draft` 0 error / 49 warning；vulnerabilities
  141、reviews 141（A 66 / B 75）、evidence 5137、snapshot_vulnerability_status 112。
- **计数**：triage 2613 = confirmed_affected **132** / confirmed_not_affected 1321 /
  possible_affected **558** / duplicate 28 / unknown 574；队列重跑
  DONE **132** / P1_VERIFY **558** / P1_REVIEW 574 / ARCHIVE 1349 /
  P0_SELECT_SNAPSHOT 13（`v031/reports/queue_P3.json`）。
- **同步**：`HANDOFF_V031.md`（112 条目标正样本 = 46 B + 66 A、141 行、round27 路径、
  A 级清单、队列与 triage 计数）、`CANDIDATE_FUNNEL_V031.md`、`LIMITATIONS_V031.md`
  （558 / 380 双侧区间）。**未重生成 CHECKSUMS，未声明数据集完成或发布**。

## 2026-10-25 — django CVE-2026-1207 采集包完成，派发 round29 隔离复核

- **候选 / 快照**：`disc2_d7e6c2d74bb34b3fe360cc4d`，`snap_516aa9971dd9509d`
  （django/django，repo_id 4164482，commit `3bf46e2e…`，tag 4.2.13）。
  漏洞为 PostGIS raster lookup 的 band index SQL 注入（CWE-89），
  修复版本 4.2.28 / 5.2.11 / 6.0.2。
- **采集**：`collect_sources_1207.py` 钉住 **37** 个 artifact（OSV CVE/GHSA/
  PYSEC/Bitnami、NVD、GHSA 页面、2026-02-03 weblog、4.2.28/4.2.27/5.2.11/
  6.0.2 release notes、3 个 PyPI 版本、8 个 tag 的 `postgis/operations.py`、
  4.2.27/4.2.28 raster 测试、4 条 fix patch、编号源码摘录、tag/commit/祖先/
  守卫矩阵、6 份探针日志、wheel sha256）。
- **探针**：4.2.13 / 4.2.27 / 4.2.28 各两遍，JSONL 成对字节一致、stderr 0。
  4.2.13 与 4.2.27 的 `operations.py` 字节相同（`b31797feb99d4612…`），
  `check_raster()` 接受字符串 band index 并插值：LHS `%s, evil` /
  `%s, 1) UNION SELECT 1 --`，RHS 同理；4.2.28（`67480ae1966f0ddd…`）
  对非整数抛 `TypeError: Band index must be an integer, but got 'str'.`；
  整数与无 band 对照三版不变。
- **代码**：`check_raster` 的 LHS 分支 53-63、RHS 分支 64-74；
  入口 `GISLookup.process_band_indices()`（`lookups.py:37-54`，第 54 行把 rhs
  tuple 元素原样赋给 `band_rhs`）；`PostGISOperator.as_sql` 40-43。
  4.2.13→4.2.27 之间无 commit 改动 `operations.py`；逐 tag 守卫矩阵
  4.2.27 F / 4.2.28 T / 5.2.10 F / 5.2.11 T / 6.0.1 F / 6.0.2 T。
  祖先矩阵：4.2 fix `a14363102d` 只进 4.2.28/4.2.30，5.2 `17a1d64a58`
  只进 5.2.11，6.0 `8f77e73011` 只进 6.0.2，main `81aa529296` 不在任何 tag。
- **卷宗**：`build_dossier_1207.py` 全断言通过后产出 `dossier.json`
  （87,288 字节 / 37 evidence / 18 字段映射 / 10 限制 /
  READY_FOR_INDEPENDENT_REVIEW）；用 promoter 的 `validate_rows` 做内存
  schema 预校验 77 条 evidence、0 error。`critical_operation` =
  `django/contrib/gis/db/backends/postgis/operations.py:64-74`（RHS band
  index），`entry_point` = `lookups.py:37-54`；中文 `README.md` 写明隔离规则
  与五处待裁定冲突（CVSS 5.4 vs NVD Secondary 8.3 vs GHSA CVSS 4.0 HIGH、
  CVE GIT 4.2 introduced `97aa3b7f` 倒挂、LHS 是否算真实攻击面、无 GDAL/
  PostGIS 的探针保真度、与 1287/1312 的归因边界）。
- **状态**：派发隔离复核 round29
  （`runs/independent/django_CVE-2026-1207_4213_round29/`）；预写 triage 改写
  脚本 `runs/data_fixes/promote_2026_1207_triage_round29_2026-10-25.py`
  （dry-run 因缺 vuln 行按预期拒绝）。**未写 `data/`，未改 triage，
  未动 CHECKSUMS**。

## 2026-10-25 — django 4.2.13：CVE-2026-1287 / CVE-2026-1207 提升，CVE-2026-53878 负证据结案

- **CVE-2026-1287（round28）**：隔离 reviewer
  `round28-isolated-independent-reviewer (no collector dossier access)`，
  `confirmed_affected` / grade **A**，九字段全 true，location
  `django/db/models/sql/query.py:1123-1128`。首版 `vulnerable_commit` 是对象、
  `preserved_sha256.txt` 只有两列且漏列文件，退回后改为字符串 + 60 文件三列
  （sha256 / 字节数 / 路径）；`check_verdict_packet.py` 复核 0 problem。
  `promote_verified_rows.py --apply` 追加 vulnerabilities 1 / locations 1 /
  reviews 1 / evidence 76 / status 1，triage 行 `disc2_c3e2d500c2ab4d8d7d3b514a`
  改为 `confirmed_affected`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round28_20261024T195238Z.jsonl`。
- **CVE-2026-1207（round29）**：reviewer `independent-reviewer-r29`，
  `reviewed_at=2026-10-24T19:50:30Z`，`confirmed_affected` / grade **A**，
  location `django/contrib/gis/db/backends/postgis/operations.py:53-74`（与卷宗
  `critical_operation` 64-74 重叠），`vulnerable_commit=3bf46e2e…`。
  首版 verdict 缺 `grade_recommendation`，补齐后按要求重生成
  `preserved_sha256.txt`（15 文件三列，摘要与字节数逐件复核，未列文件 0）；
  检查器 0 problem / 0 warning。dry-run 后
  `promote_verified_rows.py --apply` 追加 vulnerabilities 1 / locations 1 /
  reviews 1 / evidence 76 / status 1；triage 行
  `disc2_d7e6c2d74bb34b3fe360cc4d` 改为 `confirmed_affected`，备份
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round29_20261024T195421Z.jsonl`。
- **CVE-2026-53878（负证据）**：`build_not_applicable_53878.py` 对 24 件
  sha256 钉住产物做 fail-closed 断言后产出 `NOT_APPLICABLE.md` 与
  `decision.json`。结论是**符号缺失**而非版本序：`DomainNameValidator` 在
  4.2.13 / 4.2.30 的 `django/core/validators.py` 与全树 `git grep` 均不存在，
  5.0 也不存在，首见于 5.1；5.2 / 6.0.6 的类块用 `r"$"`，5.2.16 / 6.0.7
  改为 `r"\Z"`；GHSA/PYSEC/BIT/CPE 区间均只覆盖 5.2 与 6.0，fix commit
  不是 4.2 tag 的祖先。triage 行 `disc2_321d50f93bd7f1b2dc581ab7` 经
  `runs/data_fixes/not_applicable_53878_triage_2026-10-25.py --apply` 改为
  `confirmed_not_affected`（`source_code_review`），备份
  `runs/data_fixes/snapshot_candidate_triage_before_53878_negative_20261024T195433Z.jsonl`。
  该否定只针对本公告，不构成 `PASS_KNOWN_SWEEP`，也不声称 4.2.13 无其他漏洞。
- **校验**：`validate_dataset.py . --draft` **0 error / 49 warning**；
  vulnerabilities 143、reviews 143（A **68** / B 75）、evidence **5289**、
  snapshot_vulnerability_status **114**（全部 confirmed_affected）。
- **计数**：triage 2613 = confirmed_affected **134** / confirmed_not_affected
  **1322** / possible_affected **555** / duplicate 28 / unknown 574；
  `pending_relevant_triage` **1129**。队列重跑
  DONE **134** / P1_VERIFY **555** / P1_REVIEW 574 / ARCHIVE 1350 /
  P0_SELECT_SNAPSHOT 13（`v031/reports/queue_P3.json`）；possible 队列按 555
  行重跑（`runs/possible_review_queue_2026-10-24/summary.json`：双侧 377、
  上界/All versions 83、NVD CPE 23、alias OSV 42、早期 triage 30）。
- **同步**：`HANDOFF_V031.md`（114 条目标正样本 = 46 B + 68 A、143 行、A 级
  清单、三案路径、triage/队列计数）、`CANDIDATE_FUNNEL_V031.md`、
  `LIMITATIONS_V031.md`（1322 / 555 / 377）。**未重生成 CHECKSUMS，
  未声明数据集完成或发布。**

## 2026-10-25 — round22 证据清单补正（CVE-2026-25674，已提升后）

- 事后用 `check_verdict_packet.py` 复核 round22 时，`preserved_sha256.txt`
  无法覆盖 round 目录的 40 个文件（大量 `file not covered by
  preserved_sha256.txt`），尽管该轮早已于 2026-10-24T18:37:10Z 写入 `data/`。
- 已请原隔离复核方**只重生成清单**，不读 collector dossier、不改 verdict：
  40 个文件全部覆盖，严格三列 `<sha256>  <bytes>  <relative path>`，
  无重复、无目录项；`verdict.json` 内容未改（sha256 `54dd94cf…`）。
- `check_verdict_packet.py` 重跑：`problems: []`、`warnings: []`、`ok: true`，
  `preserved_files: 40`。
- 本次只是证据清单完整性补正：不重跑提升、不改 `data/`、不改 triage 行；
  25674 的入库记录仍以 2026-10-24T18:37:10Z 那次为准。**未重生成
  CHECKSUMS，未声明数据集完成或发布。**

## 2026-10-25 — round30 提升（CVE-2025-13372，django 4.2.13）

- 隔离 reviewer `independent-reviewer-r30`，`reviewed_at=2026-10-24T20:09:36Z`，
  `confirmed_affected` / grade **A**，九字段全 true，location
  `django/db/models/sql/compiler.py:519-536`（实测函数 519–539，危险点在 536 行裸
  `return name`），`vulnerable_commit=3bf46e2e023904c825728267f3131c42f02ce696`。
  机制：`FilteredRelation` 别名经 `**kwargs` 展开进入 `query.alias_map`，
  `SQLCompiler.quote_name_unless_alias()` 不调用 `connection.ops.quote_name()`，
  4.2.13 的 PostgreSQL 后端无 override，含 `$` 的别名原样进入 SQL；4.2.27 新增后端
  compiler 抛 `ValueError`。
- `check_verdict_packet.py`：13 个 preserved 文件、`problems: []`、`warnings: []`、
  `ok: true`。
- `promote_verified_rows.py --apply` 追加 vulnerabilities 1 / locations 1 /
  reviews 1 / evidence **73** / status 1；triage 行
  `disc2_949b8ff18e401c0a4c7e4b42` 由 `possible_affected` 改为
  `confirmed_affected`（`runs/data_fixes/promote_2025_13372_triage_round30_2026-10-25.py`），
  备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round30_20261024T201047Z.jsonl`。
- **校验**：`validate_dataset.py . --draft` **0 error / 49 warning**；
  vulnerabilities **144**、reviews **144**（A **69** / B 75）、evidence **5362**、
  snapshot_vulnerability_status **115**（全部 confirmed_affected）。
- **计数**：triage 2613 = confirmed_affected **135** / confirmed_not_affected
  **1322** / possible_affected **554** / duplicate 28 / unknown 574；
  `pending_relevant_triage` **1128**。队列重跑 DONE **135** / P1_VERIFY **554** /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13
  （`v031/reports/queue_P3.json`）；possible 队列按 554 行重跑
  （`runs/possible_review_queue_2026-10-24/summary.json`：双侧 376、上界/All
  versions 83、NVD CPE 23、alias OSV 42、早期 triage 30；django 9）。
- **同步**：`HANDOFF_V031.md`（115 条目标正样本 = 46 B + 69 A、144 行、A 级清单、
  round28–30 路径、triage/队列计数）、`CANDIDATE_FUNNEL_V031.md`、
  `LIMITATIONS_V031.md`（554 / 376 与本案的编译级复现限制）。**未重生成
  CHECKSUMS，未声明数据集完成或发布。**

## 2026-10-25 — round31 提升（CVE-2025-59681，django 4.2.13）

- 隔离 reviewer `independent-reviewer-r31`，`reviewed_at=2026-10-24T20:18:06Z`，
  `confirmed_affected` / grade **A**，九字段全 true，location
  `django/db/models/sql/query.py:1123-1128`（与卷宗 `critical_operation` 同文件、行号重叠），
  `vulnerable_commit=3bf46e2e023904c825728267f3131c42f02ce696`。机制：4.2.13
  `Query.check_alias()` 的 `FORBIDDEN_ALIAS_PATTERN` 不含 `#`，`annotate()`/`alias()`/
  `aggregate()`/`extra()` 的 `**kwargs` 键通过校验；MySQL/MariaDB 把 `#` 当行注释起始，
  4.2.25 加 `|#|` 并改写错误文本。reviewer 自行下载 4.2.13/4.2.24/4.2.25 wheel，
  在安装态复现 red/green（`ali#as`/`x#` 前两版通过、4.2.25 `ValueError`），每版两遍一致。
- 卷宗重建后（39 件产物；把 entry_point 行号收敛为单一区间、references 只保留 https）
  `check_verdict_packet.py`：13 个 preserved 文件、`problems: []`、`warnings: []`、
  `ok: true`。
- `promote_verified_rows.py --apply` 追加 vulnerabilities 1 / locations 1 /
  reviews 1 / evidence **72** / status 1；triage 行
  `disc2_edc9a736a4b87db89ace87ae` 由 `possible_affected` 改为
  `confirmed_affected`（`runs/data_fixes/promote_2025_59681_triage_round31_2026-10-25.py`），
  备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round31_20261024T202022Z.jsonl`。
- **校验**：`validate_dataset.py . --draft` **0 error / 49 warning**；
  vulnerabilities **145**、reviews **145**（A **70** / B 75）、evidence **5434**、
  snapshot_vulnerability_status **116**（全部 confirmed_affected）。
- **计数**：triage 2613 = confirmed_affected **136** / confirmed_not_affected
  **1322** / possible_affected **553** / duplicate 28 / unknown 574；
  `pending_relevant_triage` **1127**。队列重跑 DONE **136** / P1_VERIFY **553** /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13
  （`v031/reports/queue_P3.json`）；possible 队列按 553 行重跑
  （`runs/possible_review_queue_2026-10-25/summary.json`：双侧 375、上界/All
  versions 83、NVD CPE 23、alias OSV 42、早期 triage 30；django 8）。
- **保留意见**：探针只编译不执行（无 MySQL/MariaDB），SQL 中别名是反引号引用，
  未用执行证明注释注入；`test_alias_filtered_relation_sql_injection` 属 CVE-2025-57833；
  CVSS 采用 7.1 HIGH 并记录 NVD Primary 9.8。
- **同步**：`HANDOFF_V031.md`（116 条目标正样本 = 46 B + 70 A、145 行、A 级清单、
  round31 路径、triage/队列计数）、`CANDIDATE_FUNNEL_V031.md`、
  `LIMITATIONS_V031.md`（553 / 375 与本案的校验边界限制）。**未重生成
  CHECKSUMS，未声明数据集完成或发布。**

## 2026-10-25 — round32 提升（CVE-2025-64458，django 4.2.13）

- 隔离 reviewer `independent-reviewer-r32`，`reviewed_at=2026-10-24T20:28:51Z`，
  `confirmed_affected` / grade **A**，九字段全 true，location
  `django/http/response.py:611-621`（与卷宗 `critical_operation` 同文件、行号重叠），
  `vulnerable_commit=3bf46e2e023904c825728267f3131c42f02ce696`。机制：4.2.13
  `HttpResponseRedirectBase.__init__` 在设 `Location` 后直接 `urlparse(str(redirect_to))`
  （617 行），没有长度上限；`urlsplit()` 对非 ASCII netloc 调
  `unicodedata.normalize("NFKC", netloc)`，公告称该归一化在 Windows 上异常慢。
  reviewer 探针实测 4.2.13/4.2.25 对 20,017 字符目标触发 `urlparse`×1 与
  netloc（20,008 字符）NFKC×1；4.2.26 在解析前按 >2048 拒绝（0/0），4.2.27 放宽到
  >16384（ticket 36743，上游后续 bugfix，不是本 CVE 修复）。5.1.14 / 5.2.8 同批修复。
  每版两遍输出一致。
- `check_verdict_packet.py`：21 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- `promote_verified_rows.py --apply` 追加 vulnerabilities 1 / locations 1 /
  reviews 1 / evidence **72** / status 1；triage 行
  `disc2_869ed839e7101f70b458e853` 由 `possible_affected` 改为
  `confirmed_affected`（`runs/data_fixes/promote_2025_64458_triage_round32_2026-10-25.py`），
  备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round32_20261024T203006Z.jsonl`。
- **校验**：`validate_dataset.py . --draft` **0 error / 49 warning**；
  vulnerabilities **146**、locations **146**、reviews **146**（A **71** / B 75）、
  evidence **5506**、snapshot_vulnerability_status **117**（全部 confirmed_affected）。
- **计数**：triage 2613 = confirmed_affected **137** / confirmed_not_affected
  **1322** / possible_affected **552** / duplicate 28 / unknown 574；
  `pending_relevant_triage` **1126**。队列重跑 DONE **137** / P1_VERIFY **552** /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13
  （`v031/reports/queue_P3.json`，2026-10-25 04:33 落盘）；possible 队列按 552 行重跑
  （`runs/possible_review_queue_2026-10-25/summary.json`：双侧 374、上界/All
  versions 83、NVD CPE 23、alias OSV 42、早期 triage 30）。
- **保留意见**：影响面仅 Windows，Linux 上 NFKC 约 1 ns/字符，未测出 DoS 时延，
  记录按调用边界而非实测耗尽表述；没有 HTTP 服务器参与；NVD 只有一条 Secondary 7.5
  HIGH（无 Primary），release note 记 "moderate"，卷宗按 7.5 并列出全部口径；
  4.2.27 的阈值放宽不是安全修复。
- **同步**：`HANDOFF_V031.md`（117 条目标正样本 = 46 B + 71 A、146 行、A 级清单、
  round32 路径、triage/队列计数）、`CANDIDATE_FUNNEL_V031.md`、
  `LIMITATIONS_V031.md`（552 / 374 与本案的 Windows-only 限制）、
  `runs/possible_review_queue_2026-10-25/README.md`。**未重生成
  CHECKSUMS，未声明数据集完成或发布。**

## 2026-10-25 — round33 提升（CVE-2026-25673，django 4.2.13）

- 隔离 reviewer `independent-reviewer-r33`，`reviewed_at=2026-10-24T20:33:17Z`，
  `confirmed_affected` / grade **A**，`fields_verified` 九键全 true，location
  `django/forms/fields.py:759-787`（与卷宗 `critical_operation` 同文件、行号重叠），
  `vulnerable_commit=3bf46e2e023904c825728267f3131c42f02ce696`。机制：4.2.13
  `URLField.to_python()` 的 `split_url()` 在 766 行 `list(urlsplit(url))`，无 scheme 时
  再解析一次；`urlsplit()` 对非 ASCII netloc 做 `unicodedata.normalize("NFKC", netloc)`，
  Windows 上异常慢。reviewer 自写探针在 4.2.13/4.2.28/4.2.29 安装态各跑两遍：20,017 字符
  Unicode 目标触发 `urlsplit`×1（整串）+ NFKC×1（20,008 字符 netloc），纯 ASCII 长串不归一化，
  无 scheme 时 2 次；4.2.29 全 12 例 0/0 且不再导入 `urlsplit`。reviewer 另把 4.2 fix
  （`b3e8ec8cc3`）hunk 应用到 4.2.28（产物与 4.2.29 tag 文件逐字节相同）与 4.2.13（URLField
  块与 4.2.29 相同、探针 0 调用）。首次提交的 verdict 用了 `fix_commits`/`fixed_releases`
  且缺 `languages`，checker 报 3 个 problem；由 reviewer 自行改正为 canonical 九键
  （未由采集方代改），`preserved_sha256.txt` 重新生成 40 行。
- `check_verdict_packet.py`：40 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- `promote_verified_rows.py --apply` 追加 vulnerabilities 1 / locations 1 /
  reviews 1 / evidence **70** / status 1；triage 行
  `disc2_909a78a0d54a444a667c9f27` 由 `possible_affected` 改为
  `confirmed_affected`（`runs/data_fixes/promote_2026_25673_triage_round33_2026-10-25.py`），
  备份 `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round33_20261024T203608Z.jsonl`。
- **校验**：`validate_dataset.py . --draft` **0 error / 49 warning**；
  vulnerabilities **147**、locations **147**、reviews **147**（A **72** / B 75）、
  evidence **5576**、snapshot_vulnerability_status **118**（全部 confirmed_affected）。
- **计数**：triage 2613 = confirmed_affected **138** / confirmed_not_affected
  **1322** / possible_affected **551** / duplicate 28 / unknown 574；
  `pending_relevant_triage` **1125**。队列重跑 DONE **138** / P1_VERIFY **551** /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13
  （`v031/reports/queue_P3.json`）；possible 队列按 551 行重跑
  （`runs/possible_review_queue_2026-10-25/summary.json`：双侧 373、上界/All
  versions 83、NVD CPE 23、alias OSV 42、早期 triage 30）。
- **保留意见**：影响面仅 Windows；Linux 上 20,008 字符归一化约 0.02 ms，未测出 DoS 时延，
  记录按调用边界表述；4.2.29 的 `URLValidator` 对 ≤2048 输入仍走 `urlsplit`（有界残余路径，
  不影响 4.2.13 判定）；commit 祖先/tag→commit 映射取自钉住产物，未联网复核 GitHub；
  README 的 1,478 字节与 reviewer 含块尾换行的 1,479 字节口径差异已记录，内容相等已直接验证；
  评分 NVD 两条 Secondary 7.5 HIGH 与 release note "moderate" 的分歧保留。
- **同步**：`HANDOFF_V031.md`（118 条目标正样本 = 46 B + 72 A、147 行、A 级清单、
  round33 路径、triage/队列计数）、`CANDIDATE_FUNNEL_V031.md`、
  `LIMITATIONS_V031.md`（551 / 373 与本案的 Windows-only 限制）、
  `runs/possible_review_queue_2026-10-25/README.md`。**未重生成
  CHECKSUMS，未声明数据集完成或发布。**

## 2026-10-25 — CVE-2026-15307 卷宗构建（django 4.2.13，待复核）

- 采集 `runs/verification/django_CVE-2026-15307_4213/`：`collect_sources_15307.py` 抓取并
  sha256 钉住 **32** 件产物（4 OSV + NVD + 5.2.17/6.0.8 release notes + 四个 fix patch +
  4.2.13/5.2.16/5.2.17 的 `fields.py` 与 `raster/source.py` + 4.2.13 `raster/const.py` 与
  `admin/options.py` + 4.2.13/5.2.17 的 geoapp 与 geoadmin 测试 + weblog/archive +
  grep/tag 事实 + 5 个 PyPI 记录）。
- `build_dossier_15307.py` 为 fail-closed：断言 GHSA/PYSEC/Bitnami 的
  `0->5.2.17`、`6.0a1/6.0.0->6.0.8`，NVD 两条 Secondary（3.1 8.8 / 4.0 8.7）、
  CWE-73+CWE-918，CPE `*->5.2.17` 与 `6.0->6.0.8`，四个 fix 提交与唯一祖先归属，
  **4.2.13 与 5.2.16 的 `get_raster_prep_value`/`get_prep_value` 逐字节相同**，
  4.2.13 两个 `return gdal.GDALRaster(value)`（180/185 行）、`/vsi` 前缀放行
  （`source.py:87-97`）、dict 强制 `self._write = 1`（129 行），5.2.17 新增
  `DisallowedRasterLookup`/`check_raster_lookup_value`，以及 admin `lookup_allowed`
  只校验路径不校验值。产出 `dossier.json`（32 evidence / 18 字段 / 10 limitations /
  38,669 字节，`READY_FOR_INDEPENDENT_REVIEW`）。
- README 明确写出**本卷宗没有执行阶段**：本机无 GDAL/GEOS/Django，无法构造 `GDALRaster`，
  写盘与外连都未实测，受影响判定只建立在静态证据上（预期评级边界为 B）。
- 已派出隔离 reviewer round34（禁止读 dossier/`data/**` 等，允许读 README 与 `sources/`）。
  **尚未收到结论；未写库、未改审核等级、未移动队列。**

## 2026-10-25 — CVE-2026-15307 round34 收口（grade A）与 CVE-2026-53877 round35 收口（grade B 静态）

两轮复核在 2026-10-24T20:42–20:47Z 前后返回，均经 `check_verdict_packet.py` 校验
（round34 `ok=true`、32 个 preserved 文件；round35 首次因 `preserved_sha256.txt` 格式不符被拒，
由 reviewer 自行重生成后 `ok=true`、21 个文件），随后 `promote_verified_rows.py --apply` 写库，
再由 `runs/data_fixes/` 下的两个带守卫脚本改写对应 triage 行（先 dry-run，再 `--apply`，
均先备份 `snapshot_candidate_triage`）。

- **CVE-2026-15307（round34，grade A）**：reviewer 在无 root 用户态用 micromamba 装出
  GDAL 3.13.3 / GEOS 3.14.1 / Python 3.12.15，实测 dict、JSON 字符串、admin changelist
  三条路径各写出 694 字节 GTiff（sha256 `c9c452e0…`），`/vsicurl` 取值产生 15 次外连后
  因写模式抛错；5.2.17 与「4.2.13 + 5.2 fix」均 `DisallowedRasterLookup`、零写盘零外连。
  采集方另行复算 4.2.30 的 `get_raster_prep_value`/`get_prep_value` 与 4.2.13 逐字节相同、
  且不含 `DisallowedRasterLookup`/`check_raster_lookup_value`，确认 4.2 线无修复。
  2026-10-24T20:45:40Z 写入 1 漏洞 / 1 location / 1 review / 72 evidence / 1 status；
  候选 `disc2_964417e6892549137491a482` → `confirmed_affected`
  （backup `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round34_20261024T204602Z.jsonl`）。
- **CVE-2026-53877（round35，grade B）**：reviewer 的机器同样无 GDAL/GEOS/Django，未做红/绿，
  九字段全部静态核实后按规则停在 B。其独立证据：4.2.13 与 5.2.15 `raster/source.py` 整文件
  逐字节相同（sha256 `366b028d…`，并用 PyPI sdist 复核）、四个 fix 补丁与祖先关系
  （5.2.16 / 6.0.7 / 6.1 正式版）、本地 CPython 测得 `getsizeof(bytes)` +33 与
  `create_string_buffer` +1 合计越界 32 字节。reviewer 同时指出卷宗的三处 provenance nit：
  fix 补丁是 `git show` 格式而非 GitHub `.patch` 字节、`grep_facts.txt`/`tag_and_commit.txt`
  的 tree URL 与本地 git 输出不符、dossier 把 CVE 自身也列进 aliases。
  2026-10-24T20:47:29Z 写入 1 漏洞 / 1 location / 1 review / 69 evidence / 1 status；
  候选 `disc2_129f28a7857053e311c7d94d` → `confirmed_affected`
  （backup `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round35_20261024T204741Z.jsonl`）。
- **复算**：draft 校验 0 err / 49 warning；vulnerabilities **149** / locations **149** /
  reviews **149**（A **74** / B 75）/ evidence **5717** / snapshot_vulnerability_status **120**；
  triage 2613 = confirmed_affected **140** / confirmed_not_affected 1322 / possible_affected
  **549** / duplicate 28 / unknown 574，`pending_relevant_triage` **1123**；队列重跑
  DONE **140** / P1_VERIFY **549** / P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13
  （`v031/reports/queue_P3.json`，带 `--out` 落盘）；possible 队列按 549 行重跑
  （双侧 **371**、上界/All versions 83、NVD CPE 23、alias OSV 42、早期 triage 30）。
- **同步**：`HANDOFF_V031.md`（120 条目标正样本 = 46 B + 74 A、149 行、最新清单、
  A 级清单、round34/round35 路径、triage/队列计数）、`CANDIDATE_FUNNEL_V031.md`、
  `LIMITATIONS_V031.md`（§3 计数、549/371、两条本案边界条目）、
  `runs/possible_review_queue_2026-10-25/README.md`。
  **未重生成 CHECKSUMS，未声明数据集完成或发布，也未把 round35 的静态 B 表述成执行验证。**

### 2026-10-24T20:55Z：CVE-2026-15830 round36 独立复核、promote 与复核后更正

- **卷宗**：`runs/verification/django_CVE-2026-15830_4213/`，51 件 sha256 钉住产物（OSV×4、NVD、
  七版 release notes、八个 fix 补丁、GEOS 上游补丁、4.2.13/4.2.30 与 5.2.17/5.2.18 的
  `io.py`/`geometry.py`/`db/models/fields.py`/`forms/fields.py`、两版 `test_geos_limit.py`、
  greps、tag/commit、PyPI×7 等），`dossier.json` 51 evidence / 18 字段映射 / 11 limitations。
  fail-closed 构建器断言了每个 release-note 片段、每行源码、字节同一性、祖先矩阵与 PyPI 日期。
- **机制**：4.2.13 `django/contrib/gis/geos/prototypes/io.py` 的 `_WKTReader.read`（156）与
  `_WKBReader.read`（167）把 WKT/WKB/HEXEWKB 原样交给 GEOS，无深度/数量检查；GEOS 3.15.0 之前
  每层 `GEOMETRYCOLLECTION` 递归一次无上限（上游 `8b8b3da7` 才加 `MAX_PARSE_DEPTH = 100`），
  深层嵌套耗尽栈 → SIGSEGV。两阶段修复：5.2.17/6.0.8/6.1（`ba80833f`/`6af5da31`/`9e4a3f18`，
  main `d2e59b77`）加 `MAX_GEOM_COLLECTIONS = 198`；5.2.18/6.0.9/6.1.2（`1eafa1a8`/`4353dfb5`/
  `75d401a1`，main `62ef9d40`）改为结构化 `_WKBFrame` 栈式遍历，堵住非法字节序 / 递归 MULTIPOINT /
  大端 ISO HEXWKB 绕过。4.2 线无 backport，4.2.13 与 4.2.30 的 `io.py`/`geometry.py`/`forms/fields.py`
  逐字节相同。
- **复核**：2026-10-24T20:55:51Z 收到 round36 `verdict.json`：`confirmed_affected`，
  **grade B**（静态；无 `reproduction_reference`），九字段全 true，`reviewed_by != prepared_by`
  （`independent-reviewer-round36` vs `django-4.2.13-collector-15830`）；`check_verdict_packet.py`
  `ok: true`，15 件 preserved 文件。reviewer 独立复算：tag peel、4.2.13/4.2.30 字节同一性、
  八个 fix 的祖先矩阵、逐 tag grep、GEOS 补丁插入点、GHSA `6.1a1 → 6.1.1` 偏晚。
  **未执行**：本机与 reviewer 机器均无 Django/libgeos_c/GDAL，段错误未被观测。
- **复核指出的更正**（采集方接受）：①4.2 的 EOL 不是 2025-04，而是**扩展支持 2026-04-07 结束**
  （4.2.30 同日发布为末版）；②`raw_geos_geometry_4213` 注记把 0-based 索引 740/753 当行号
  （实为 741/754）；③`affected_packages[0].affected_range` 起点写成 `>= 5.2`，而公告区间
  `0 -> 5.2.17` 也覆盖 4.2.13。三处已在 `dossier.json` 重建时更正（57,073 字节 / 11 limitations），
  并写入 `runs/verification/django_CVE-2026-15830_4213/POST_REVIEW_CORRECTIONS.md`；
  **verdict、grade、fields_verified、location 均未改动**，`prepared_at` 改为真实 UTC
  （2026-10-24T20:52:00Z）。
- **自查更正**：八条 fix_commits 原先全标 `fix_status=complete`；第二阶段发布说明明言第一阶段
  限流可被绕过，故改为第一阶段四条 `partial`、第二阶段四条 `complete`（dossier 已改，
  已 promote 的行由 `runs/data_fixes/fix_15830_fix_status_2026-10-25.py` 带断言更正，
  backup `runs/data_fixes/vulnerabilities_before_15830_fix_status_20261024T205924Z.jsonl`）。
- **写入**：2026-10-24T20:58:46Z `promote_verified_rows.py --apply`（无 warning/conflict）→
  1 漏洞 / 1 location / 1 review / 84 evidence / 1 status；20:59:30Z triage 行
  `disc2_956f6f00002b68166b526c02` → `confirmed_affected`（backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round36_20261024T205934Z.jsonl`）。
- **复算**：draft 校验 0 err（结构通过，仍非完整性/可利用性验证）；vulnerabilities **150** /
  locations **150** / reviews **150**（按表实测 A **73** / B **77**；此前文档写的 A74/B75 与实测
  不符，已按实测更正，其中 121 条评测目标 = 73 A + 48 B，29 条历史快照全 B）/ evidence **5801** /
  snapshot_vulnerability_status **121**；triage 2613 = confirmed_affected **141** /
  confirmed_not_affected 1322 / possible_affected **548** / duplicate 28 / unknown 574，
  `pending_relevant_triage` **1122**；队列 DONE **141** / P1_VERIFY **548** / P1_REVIEW 574 /
  ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13；possible 队列按 548 行重跑（双侧 **370**、上界/All
  versions 83、NVD CPE 23、alias OSV 42、早期 triage 30），README 已记录离队候选。
- **同步**：`HANDOFF_V031.md`（121 条目标正样本、150 行、最新十三条清单与 round36 条目、表格计数）、
  `LIMITATIONS_V031.md`（§3 计数、548/370、§7 新增 15830 条目）、`CANDIDATE_FUNNEL_V031.md`、
  `runs/possible_review_queue_2026-10-25/README.md`。
  **未重生成 CHECKSUMS，未声明数据集完成、未声明 `PASS_KNOWN_SWEEP`，未把 round36 的静态 B
  表述成执行验证；41990/45230/56374 未动。**

## 2026-10-25 — CVE-2025-49007 round37 收口（rack v3.1.13，grade A 执行红/绿）

本卷宗（`runs/verification/rack_v3.1.13_CVE-2025-49007/`，40 件 sha256 钉住产物）在
2026-10-24T21:16:00Z 收到 round37 独立复核，`check_verdict_packet.py` 结果 `ok: true`
（587 个 preserved 文件、0 problems / 0 warnings），判 `confirmed_affected` / grade **A**，
`reviewer_identity` = `round37-independent-reviewer`。

- **机制**：`lib/rack/multipart/parser.rb:310` 的 `handle_mime_head` 把整段 MIME 头块交给
  36 行未锚定的 `/Content-Disposition:(.*)(?=#{EOL}(\S|\z))/ni`；`CONTENT_DISPOSITION_MAX_BYTES
  = 1536` 的检查在 311 行、即匹配之后；头块只以空行为界（`@head_regex` 214），`read_data`
  258-262 每次最多追加 `BUFSIZE = 1_048_576` 字节。触发条件：单字面量 + 长值只呈线性，
  二次开销需要在一条头行堆多个字面量起点且行尾 lookahead 失败（如空格开头的折叠续行）。
  入口 `Rack::Request#POST` 503 → `form_data?` 470/474 → `parse_multipart` 527 →
  `Rack::Multipart.parse_multipart`（`multipart.rb:48/62`）。
- **复核者执行阶段**（非采集方）：自行 blobless clone + gem + tarball 重抓，用 `-I` 加载
  真实 rack 3.1.13/3.1.16，`prepend` 埋点取 `head_b/sbuf_b`，`CLOCK_MONOTONIC` 在被测进程内
  计时；同一批 body 下 3.1.13 中位 1.336 ms（2.5 KB）→ 1439 ms（80 KB），log-log 斜率 ≈2.01；
  3.1.16 在 80 KB 为 1.305 ms（斜率 ≈0.99）；普通 multipart 两版均解出 `{"field1"=>"value"}`；
  另有 `Rack::Request#POST` 入口探针与纯正则补充实验；原始日志在
  `runs/independent/rack_v3.1.13_CVE-2025-49007_round37/reproduction/`。
- **修复**：3.1 线 `aed514df37e33907df3c971ed3ca9a0a20ac2901`（首个发行 v3.1.16）、3.2 线
  `4795831a0a310c2d31102749e551b38faab6401f`（首个发行 v3.2.0；**不存在**受影响的 3.2.x），
  均改为 `^` 锚定 + `FWS`/`HEADER_VALUE`，且都不是 v3.1.13/14/15 的祖先。
- **复核后更正**（见 `POST_REVIEW_CORRECTIONS.md`）：机制表述过宽 → 改为精确触发条件；
  `affected_ranges` 第二条把 3.2 线误当受影响区间 → 改为 `no affected 3.2 release` +
  `first_patched_version 3.2.0`；limitation 3 混淆 body 内 MIME 头与 HTTP 请求头 → 改为
  body-size limit 与并发；`published_at` 补注为 GHSA 时间（OSV CVE 2025-06-04T22:42:52Z、
  NVD 2025-06-04T23:15:21Z）；`form_data?` 行号 474 → def 470 / test 474 / 常量 153-155。
  verdict、grade、九字段、location 均未改动；dossier 重建为 47,964 字节 / 33 evidence /
  10 limitations / 5 open questions。
- **写入**：2026-10-24T21:18:16Z `promote_verified_rows.py --apply`（无 warning / conflict）→
  1 漏洞 / 1 location / 1 review / 67 evidence / 1 status；21:18:31Z triage 行
  `disc2_dbd720d0f16c279b811322c4` → `confirmed_affected`（backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round37_20261024T211831Z.jsonl`）。
  MECHANISM 文本同步更正，并补入复核者的实测数字。
- **复算**：draft 校验 0 err（结构通过，仍非完整性/可利用性验证）；vulnerabilities **151** /
  locations **151** / reviews **151**（A **74** / B **77**；其中 122 条评测目标 = 74 A + 48 B，
  29 条历史快照全 B）/ evidence **5868** / snapshot_vulnerability_status **122**；
  triage 2613 = confirmed_affected **142** / confirmed_not_affected 1322 / possible_affected
  **547** / duplicate 28 / unknown 574，`pending_relevant_triage` **1121**；队列 DONE **142** /
  P1_VERIFY **547** / P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13；possible 队列按
  547 行重跑（双侧 **369**、上界/All versions 83、NVD CPE 23、alias OSV 42、早期 triage 30）。
- **同步**：`HANDOFF_V031.md`（122 条目标正样本、151 行、最新正样本与 round37 条目、表格计数、
  verdict 路径清单）、`LIMITATIONS_V031.md`（§3 计数、547/369）、`CANDIDATE_FUNNEL_V031.md`、
  `runs/possible_review_queue_2026-10-25/README.md`、本 packet 的 `README.md` 与
  `POST_REVIEW_CORRECTIONS.md`。
  **未重生成 CHECKSUMS，未声明数据集完成、未声明 `PASS_KNOWN_SWEEP`、未发布；grade A 表述为
  独立复核者的执行复现，不是采集方的运行；41990/45230/56374 未动。**

## 2026-10-25 — CVE-2025-61772 卷宗构建（rack v3.1.13，待复核）

`runs/verification/rack_v3.1.13_CVE-2025-61772/`：23 件 sha256 钉住产物，`dossier.json`
33,519 字节 / 23 evidence / 18 字段索引 / 6 limitations / 5 open questions，状态
`READY_FOR_INDEPENDENT_REVIEW`。候选 `disc2_d52e1cedda7ae490c33181a7`
（2026-10-24T21:28Z 更正：先前误写为 `disc2_1bccc3f05172e8f4c3d38a09`，那个 id 属于
CVE-2026-22860 / GHSA-mxw3-3hh2-x2mh 的候选；本条的正确候选是 d52e1ced…）。

- **机制**：`parser.rb:306` `handle_mime_head` 等 part 头终止符（CRLFCRLF）时，406-408 的
  `else / :want_read` 分支**没有字节上限**，`read_data`（258-262，`BUFSIZE = 1_048_576`，40 行）
  持续 `@sbuf.concat`；头块永不终止 ⇒ 整个请求体驻留内存。**无放大**：内存随客户端实际发送
  字节线性增长，边界是 body 上限与并发。入口 `Request#POST` 503 → `form_data?` 470/474
  （`multipart/form-data` 在 153-155）→ `parse_multipart` 527 → `Multipart.parse_multipart`
  （`multipart.rb:48/62`）。
- **修复**：3.1 线 `e08f78c6`（首个发行 3.1.17）加 `BOUNDARY_START_LIMIT = 16 KiB` 与
  `MIME_HEADER_BYTESIZE_LIMIT = 64 KiB` 并 raise `multipart mime part header too large`；
  比较对象是整个 `@sbuf`，实际阈值 `max(64 KiB, BUFSIZE)`。3.2 线 `589127f4`（3.2.2）、
  2.2 线 `d869fed6`（2.2.19）。`BUFFERED_UPLOAD_BYTESIZE_LIMIT` 来自后续提交 `f224f93b`
  （CVE-2025-61771），**未**记到本 CVE 名下。
- **取材差异（如实记录）**：构建时 `api.github.com` 配额耗尽（0/60，reset 22:00Z），本卷宗
  **不含任何 API JSON**；tag peeling、祖先关系、作者/提交时间、diffstat 来自本地 blobless
  clone 的 git 命令输出，命令与原始 stdout 逐字钉在 `sources/git_tags.txt`、
  `sources/git_ancestry.txt`。文件/补丁走 raw 与 `.patch` URL。
- **已派**隔离复核者（`round38-independent-reviewer`），要求自行重抓、以**内存（RSS）**
  为主做红/绿对照 3.1.17 的 raise，并输出 verdict/NOTES/preserved_sha256/reproduction/
  refetch_upstream。复核结果尚未返回；**未写 `data/`、未改 triage、未下 verdict**。

## 2026-10-25 — CVE-2025-61770 卷宗构建（rack v3.1.13，待复核）

`runs/verification/rack_v3.1.13_CVE-2025-61770/`：23 件 sha256 钉住产物，`dossier.json`
34,513 字节 / 23 evidence / 18 字段索引 / 7 limitations / 5 open questions，状态
`READY_FOR_INDEPENDENT_REVIEW`。候选 `disc2_ef186d6243339e8a6f811575`
（已对 queue 与 `data/snapshot_candidate_triage.jsonl` 双向核对）。

- **机制**：`parser.rb:271` `handle_fast_forward` 找首个 multipart boundary；`consume_boundary`
  （434-441）扫 `@body_regex`（435，定义在 210），找不到时只 `@sbuf.terminate`（438，仅移指针，
  不释放字符串）；287-289 的 `else / return :want_read` **没有字节上限**，`read_data`
  （258-262，`BUFSIZE = 1_048_576`，40 行）持续 `@sbuf.concat` ⇒ 首个 boundary 之前的
  preamble 按实际收到字节驻留内存。**无放大**。入口同 61772（`Request#POST` 503 →
  `form_data?` 470/474 → `parse_multipart` 527 → `multipart.rb:48/62`）。
- **修复**：3.1 线 `e08f78c6`（3.1.17）加 `BOUNDARY_START_LIMIT = 16 KiB` 并 raise
  `multipart boundary not found within limit`（315 行），比较整个 `@sbuf.string.bytesize`，
  实际阈值 `max(16 KiB, BUFSIZE)`；3.2 线 `589127f4`（3.2.2）、2.2 线 `d869fed6`（2.2.19）。
  同一提交还修 61772；`BUFFERED_UPLOAD_BYTESIZE_LIMIT`（61771）是后续 `f224f93b`，**未**记到本
  CVE 名下。
- **交叉校验**：本卷宗与 round38 卷宗共享的 17 件上游产物 + 2 件 git 派生件重新抓取后
  sha256 全部一致（19 件逐字节相同），4 件本 CVE 独有 advisory 不同。
- **取材限制**：`api.github.com` 仍为 0/60（reset 22:00Z），无 API JSON；tag peeling、祖先
  关系、作者/提交时间、diffstat 来自本地 blobless clone，命令与 stdout 钉在
  `sources/git_tags.txt`、`sources/git_ancestry.txt`。
- **预检**：复用 `promote_verified_rows` 的离线 schema 预检 → `schema_errors: []`、
  evidence **40** 行、id 唯一、`proof_method = version_range_plus_code`。
- **已派**隔离复核者（`round39-independent-reviewer`）到
  `runs/independent/rack_v3.1.13_CVE-2025-61770_round39/`，要求独立重抓、以 RSS/VmHWM 为主
  做红/绿（3.1.13 vs 3.1.17），并核实 `@sbuf.terminate` 是否真的让 preamble 驻留。
- **未写 `data/`、未改 triage、未提升队列、未下 verdict**；`promote_2025_61770_triage_round39.py`
  已就位并 dry-run 过（按预期因缺 vuln 行拒绝执行）。41990/45230/56374 未动。

## 2026-10-25 — CVE-2025-61772 round38 收口（rack v3.1.13，grade A 执行红/绿并测内存）

2026-10-24T21:29:10Z 收到 round38 独立复核（`runs/independent/rack_v3.1.13_CVE-2025-61772_round38/`）：
`confirmed_affected`，grade **A**，`location = lib/rack/multipart/parser.rb:406-408`，
九字段全 true，284 个 preserved 文件（复核者 `sha256sum -c` 全过），`refetch_upstream/` 自建
blobless clone 重剥 tag。初次运行 `check_verdict_packet.py` 仅一项失败：verdict 顶层缺
`vulnerable_commit`（采集方给复核者的输出规格漏写该字段）；请复核者自行补齐并重算
`preserved_sha256.txt`（未代改其 verdict），复跑后 `ok: true`、`problems: []`、`warnings: []`。

- **复核者执行的红/绿（不是采集方的运行）**：官方 gem 的 rack 3.1.13/3.1.16/3.1.17，Ruby 3.2.3，
  body = `--BOUNDARY\r\nContent-Disposition: form-data; name="a"\r\n` + N 字节 `A`（无 CRLFCRLF），
  N = 1/4/16/64 MiB，30 次独立进程，读 `/proc/self/status` 的 VmRSS/VmHWM。
  3.1.13/3.1.16 的 `@sbuf.string.bytesize` = 1,048,630 / 4,194,358 / 16,777,270 / 67,108,918，
  64 MiB 时 VmHWM 增量 66,560–66,688 kB；3.1.17 在 `@sbuf = 1,048,576` 即抛
  `Rack::Multipart::Error: multipart mime part header too large`，16 KiB bufsize 复测在 81,920 抛错
  （验证 `max(64 KiB, BUFSIZE)`）。无放大：≥16 MiB 时 VmHWM 增量 / body ≈ 1.0×。
- **提升**：`promote_verified_rows.py --apply`（2026-10-24T21:30:48Z）写入 1 vulnerability /
  1 location / 1 review / **40 evidence** / 1 snapshot_vulnerability_status；候选
  `disc2_d52e1cedda7ae490c33181a7` 经 `promote_2025_61772_triage_round38.py --checked-at
  2026-10-24T21:31:00Z --apply` 改写为 `confirmed_affected`（backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round38_20261024T213051Z.jsonl`）。
- **复核后更正**（`runs/verification/rack_v3.1.13_CVE-2025-61772/POST_REVIEW_CORRECTIONS.md`，
  **未改 dossier.json、未动 verdict/grade/九字段/location**）：(1) OSV×2 与 NVD 三个 JSON 重抓字节
  sha 不同（规范化后只差键序与 `timestamp`），其余 10 件逐字节一致；(2) trace 两处函数名错位
  （`request.rb:527` 实为 `Rack::Request#POST` 内调用，`multipart.rb:62` 实为类方法 `Parser.parse`，
  实例 `Parser#parse` 在 `parser.rb:217`）；(3) NVD 另有 `ssvcV203` 对象（非 CVSS）；
  (4) candidate_id 更正已披露并被记录；(5) 3.2.2/2.2.19 作为另两分支首个修复版被复核者接受。
- **复算**：draft 校验 0 err / 49 warning（结构通过，仍非完整性/可利用性验证）；vulnerabilities
  **152** / locations **152** / reviews **152**（A **75** / B **77**；其中 123 条评测目标 =
  75 A + 48 B，29 条历史快照全 B）/ evidence **5908** / snapshot_vulnerability_status **123**；
  triage 2613 = confirmed_affected **143** / confirmed_not_affected 1322 / possible_affected
  **546** / duplicate 28 / unknown 574，`pending_relevant_triage` **1120**；队列 DONE **143** /
  P1_VERIFY **546** / P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13；possible 队列按 546 行
  重跑（双侧 **368**、上界/All versions 83、NVD CPE 23、alias OSV 42、早期 triage 30）。
- **同步**：`HANDOFF_V031.md`（123 条目标正样本、152 行、最新正样本与 round38 条目、表格计数、
  verdict 路径清单、§3 的 A 级计数）、`LIMITATIONS_V031.md`（§2/§3 计数、546/368、新增 §9
  rack 61772 边界）、`CANDIDATE_FUNNEL_V031.md`、`runs/possible_review_queue_2026-10-25/README.md`、
  本 packet 的 `README.md` 与 `POST_REVIEW_CORRECTIONS.md`。
  **未重生成 CHECKSUMS，未声明数据集完成、未声明 `PASS_KNOWN_SWEEP`、未发布；grade A 表述为
  独立复核者的执行复现，不是采集方的运行；41990/45230/56374 未动。**

## 2026-10-25 — CVE-2025-61771 卷宗构建（rack v3.1.13，round40，待复核）

与前两份姊妹卷宗同快照（`snap_245aee01ea5112b9`，tag `v3.1.13`，commit `03795378`），
候选 `disc2_1910309112115463c3ca0169`。GitHub REST API 仍是 `0/60`（`reset
2026-10-24T22:00:00Z`），故继续走 raw/patch + 本地 blobless clone（`/tmp/rack_repo`）路线，
命令与原始 stdout 逐字钉进 `sources/git_tags.txt` / `sources/git_ancestry.txt`。

- **机制（采集方读码陈述）**：无 `filename` 的 part 走 `BufferPart`：
  `Collector#on_mime_head` 的 `body = String.new`（parser.rb:160）、
  `Collector#on_mime_body` 的 `@mime_parts[mime_index].body << content`（170）都不计字节；
  `check_part_limits`（178-195）只数打开的文件数与 part 数；`handle_mime_body` 把整段
  （413）或增量尾部（421）交出去。**没有放大**，内存随发送字节线性增长。
- **修复切分（本轮重点）**：本 CVE 的 3.1 线修复是 **`f224f93b`**（"Limit amount of
  retained data when parsing multipart requests"，3.2 = `3beacfcd`，2.2 = `c370dcd9`），
  不是兄弟 `e08f78c6`。`f224f93b` 以 `MIME_HEADER_BYTESIZE_LIMIT = 64 * 1024` 为上下文行，
  不重加 `BOUNDARY_START_LIMIT`/`MIME_HEADER_BYTESIZE_LIMIT`（构建脚本有断言）。
  祖先关系实测：`f224f93b` 只在 v3.1.17、`3beacfcd` 只在 v3.2.2、`c370dcd9` 只在 v2.2.19；
  兄弟 `e08f78c6` 在 v3.1.17 也为 True、对 v3.1.13 为 False。
- **公开记录两处问题（如实入卷宗）**：(1) GHSA-w9pc-fmgc-vxvw 的 `references`、OSV
  `CVE-2025-61771` 的 GIT 区间、rubysec 的 `related.url` **都只引用兄弟提交**
  `e08f78c6`/`589127f4`/`d869fed6`，没有一处引用 `f224f93b`/`3beacfcd`/`c370dcd9`；
  (2) advisory 缓解措辞写 "e.g., 2 MiB"，实际默认值是 16 MiB；且提交信息写的环境变量名
  （`RACK_MULTIPART_MAX_BUFFERED_UPLOAD_SIZE`）与代码/README 的
  `RACK_MULTIPART_BUFFERED_UPLOAD_BYTESIZE_LIMIT` 不一致。
- **产物**：23 件 sha256 固定（OSV×2、NVD、rubysec、3 个 fix 补丁、RubyGems 版本表、
  `parser.rb`×6、`multipart.rb`×2、`request.rb`、`spec_multipart.rb`×2、`CHANGELOG.md`×2、
  2 件 git 派生）。`dossier.json` 37,371 字节 / 23 evidence / 18 字段 / 8 limitations /
  5 open questions，状态 `READY_FOR_INDEPENDENT_REVIEW`。
- **交叉校验**：与 round39 的 23 件同名产物比较，**15 件逐字节相同**
  （`parser.rb`×6、`multipart.rb`×2、`request.rb`、`spec`×2、`changelog`×2、RubyGems 版本表、
  `git_tags.txt`），8 件不同（4 件本 CVE 独有 advisory、3 个 fix 补丁、`git_ancestry.txt`）。
- **离线预检**（未写 `data/`）：`promote_verified_rows.evidence_rows()` 产出 39 条
  evidence 行 + 1 条 snapshot evidence，id 唯一、`source_url` 全 https、
  `critical_operation.line = 169-171` 合法，`problems: []`。
- **复核派发**：round40 隔离复核者（`round40-independent-reviewer`）已派出，任务说明里
  强制要求 verdict 顶层 `vulnerable_commit`（round38 就漏在这）、要求实测内存红/绿并加
  「带 filename 的对照」、要求独立确认 retained-size 提交是 `f224f93b` 而非 `e08f78c6`。
  **未写 `data/`、未改 triage、未提升队列、未动 41990/45230/56374、未重生成 CHECKSUMS、
  未声明完成或 PASS_KNOWN_SWEEP；没有执行 rack 代码、没有测内存。**

## 2026-10-25 — CVE-2025-61770 round39 收口（rack v3.1.13，grade A 执行红/绿并测内存）

- **verdict**：2026-10-24T21:36:32Z，复核者 `round39-independent-reviewer`，`confirmed_affected`，
  grade **A**，`reproduction_reference = reproduction/00_SUMMARY.txt`，preserved 32 文件
  （`runs/independent/rack_v3.1.13_CVE-2025-61770_round39/`）。
- **校验**：第一次 `check_verdict_packet.py` 返回 `ok: false`，原因是复核员把 `fields_verified`
  写成了字段值对象（九个键都在，值不是 `true`）。采集方没有代改复核文件，而是要求复核员
  本人把实际值移入顶层 `field_values`、把 `fields_verified` 改为九个布尔 `true`、重算
  `preserved_sha256.txt`。复核员改完后重跑：`ok: true`，`problems: []`，`warnings: []`。
- **入库**：2026-10-24T21:39:56Z `promote_verified_rows.py --apply`（1 漏洞 / 1 location /
  1 review / 40 evidence / 1 status）；2026-10-24T21:40:30Z 守卫式 triage 改写，候选
  `disc2_ef186d6243339e8a6f811575` → `confirmed_affected`，backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round39_20261024T214000Z.jsonl`
  （脚本 `runs/data_fixes/promote_2025_61770_triage_round39.py`）。
- **复核员的实测**（Ruby 3.2.3，genuine gem 3.1.13/3.1.17，安装后 parser.rb 内容 sha256 与上游
  tag 文件一致）：3.1.13 上 64 MiB preamble 解析后 `VmRSS` 91,432 kB、对照（4 KiB）25,856 kB，
  即 **+65,576 kB ≈ 64 MiB 原样驻留**，`VmHWM` 141,404 kB；8/16/32 MiB 线性且都正常解析。
  3.1.17 上 1/8/32/64 MiB 均在第 1 次读（1,048,576 B）后抛
  `Rack::Multipart::BoundaryTooLongError: multipart boundary not found within limit`，
  `VmHWM` 27.4–27.8 MB。自定义 `BUFSIZE=8192` 时 3.1.17 在累计 24,576 B（第 3 次读）才抛、
  8 KiB preamble 正常解析；3.1.13 同样缓冲完整 65,611 B。`@sbuf.terminate` 专项实测确认只移动
  扫描指针不清空字符串（terminate 后 `bytesize = 1,048,576`、`pos = 1,048,576`、`rest_size = 0`；
  再 `concat` 后涨到 2,097,152，找到 boundary 后 preamble 仍在 `@sbuf`）。
- **复核后更正**（`runs/verification/rack_v3.1.13_CVE-2025-61770/POST_REVIEW_CORRECTIONS.md`）：
  (1) `40e1e6cc…` 是**文件内容 sha256** 而非 git blob id（三 tag 的 blob 为 `3960b371…`、
  3.1.16 `c78f0e39…`、3.1.17 `81c91ad6…`）；(2) 阈值不是 `max(16 KiB, BUFSIZE)`，而是「大于
  16 KiB 的第一个 BUFSIZE 整数倍」；(3)「无放大」限定为**驻留字节**，峰值 `VmHWM` 约 payload
  1.6–2 倍；(4) 复核员用 `git grep` + `git log -S` 覆盖全部 v3.1.x，确认 3.1.0–3.1.16 无
  `BOUNDARY_START_LIMIT`、引入者确为 `e08f78c6`，补上采集方 3.1.1–3.1.12 的空档；
  (5) tag→commit、祖先关系、三分支 fix 与 `f224f93b` 归属均独立复算一致。
  `dossier.json` 已按 (1)(2)(3) 重建（证据 23 / 字段 18 / limitations 7，字节数与重建前同为
  35,147），README 同步；已入库 triage 行的两处错误措辞用守卫脚本
  `runs/data_fixes/fix_61770_threshold_wording_2026-10-25.py` 改写（backup
  `runs/data_fixes/snapshot_candidate_triage_before_61770_wording_20261024T214218Z.jsonl`）；
  已 promote 的 40 条 evidence 行不含被更正句子（逐行 grep 确认），无需改写。
- **当时复算**（round40 promote 之前）：153 vulnerabilities / 153 locations / 5948 evidence /
  153 reviews（A 76 / B 77）/ 124 status；triage `confirmed_affected 144` / `possible_affected 545`
  / `unknown 574`；队列 P1_VERIFY 545、`range_precise 367`；`validate_dataset.py . --draft`
  结构通过。
- **未做的事**：未运行被测代码、未自行给判定（grade A 全部归复核员执行）；未动
  41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声称数据集完成或 `PASS_KNOWNSWEEP`。

## 2026-10-25 — CVE-2025-61771 round40 收口（rack v3.1.13，grade A 执行红/绿并测内存）

- **verdict**：2026-10-24T21:41:12Z，复核者 `round40-independent-reviewer`，`confirmed_affected`，
  grade **A**，`reproduction_reference = reproduction/`，preserved 255 文件
  （`runs/independent/rack_v3.1.13_CVE-2025-61771_round40/`）。
- **校验**：`check_verdict_packet.py` 一次通过（`ok: true`，`problems: []`，`warnings: []`）。
  `preserved_sha256.txt` 不含自身一行（文件无法包含自己的哈希，checker 的 `check_preserved`
  显式排除该文件），复核员在 NOTES §9 说明。
- **入库**：2026-10-24T21:41:44Z `promote_verified_rows.py --apply`（1 漏洞 / 1 location /
  1 review / 40 evidence / 1 status）；2026-10-24T21:42:07Z 守卫式 triage 改写，候选
  `disc2_1910309112115463c3ca0169` → `confirmed_affected`，backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round40_20261024T214207Z.jsonl`
  （脚本 `runs/data_fixes/promote_2025_61771_triage_round40.py`）。
- **复核员的实测**（gem 3.1.13/3.1.16/3.1.17 + Ruby 3.2.3，每个数据点独立进程，
  `/proc/self/status` 取 VmHWM/VmRSS，payload 边写盘边解析）：3.1.13 单字段（无 `filename`）
  1/4/16/64 MiB 全部解析成功，`params` 值 `bytesize` = 1,048,576 / 4,194,304 / 16,777,216 /
  67,108,864，64 MiB 时 GC 后 RSS 增量 **+67,416 KiB ≈ 1.03× payload**；3.1.17 上 16/64 MiB 均抛
  `multipart data over retained size limit`，`RACK_MULTIPART_BUFFERED_UPLOAD_BYTESIZE_LIMIT=4096`
  （16 KiB 输入）与 `=2097152`（4 MiB 输入）都触发，同一变量在 3.1.13 上无效（反证）；
  带 `filename` 的 64 MiB 对照落 Tempfile（盘上 67,108,864 字节）、不触发上限、GC 后 RSS
  仅比基线高约 2 MiB；经真实入口 `Rack::Request#POST` 复现同一结果；3.1.16 仍无上限。
- **复核员对切分的独立裁定**：`f224f93b` 的 parent 恰为 `e08f78c6`，前者才加
  `BUFFERED_UPLOAD_BYTESIZE_LIMIT` / `update_retained_size` / 报错文本 / README / 本 CVE 的
  CHANGELOG 条目；GHSA / OSV / NVD / rubysec 引用的 `e08f78c6`/`589127f4`/`d869fed6` 正是三个
  retained-size 提交的 parent，属**公开记录把两段改动记混**，`fix_commit = f224f93b` 成立。
  另确认「2 MiB（公告）vs 16 MiB（代码）」与 commit message / 代码的环境变量名不一致。
- **复核后更正**（`runs/verification/rack_v3.1.13_CVE-2025-61771/POST_REVIEW_CORRECTIONS.md`）：
  (1) `handle_mime_body` 交给 collector 的行号是 **414/422**，卷宗原写 413/421（0-based 下标），
  已改 `build_dossier_61771.py` 5 处并重建 `dossier.json`（字节数不变 37,371），并同步改写
  已入库 5 条 evidence 行
  （`runs/data_fixes/fix_61771_line_offbyone_2026-10-25.py`，backup
  `runs/data_fixes/evidence_before_61771_line_offbyone_20261024T214244Z.jsonl`）；
  (2) 异常类名为 `Rack::Multipart::BoundaryTooLongError`（`Error` 是别名），已写进 triage
  `notes`；(3) `location.line` 153-171 与 `critical_operation.line` 169-171 并存属有意设计；
  (4) 3.1.16 正则改动归因 CVE-2025-49007 属引用 49007 卷宗、未独立归因，照实记录；
  (5)「与 round39 15 件逐字节相同」在隔离下对复核员不可复核，复核员改为自抓比对
  `sources/manifest.json` 的 sha256（除 OSV×2 与 NVD 的 `timestamp`/键序外全部一致）。
- **复算（当前权威值）**：154 vulnerabilities / 154 locations / **5988 evidence** / 154 reviews
  （**A 77 / B 77**）/ **125** snapshot_vulnerability_status；triage `confirmed_affected 145` /
  `confirmed_not_affected 1322` / `possible_affected 544` / `duplicate 28` / `unknown 574`
  （`pending_relevant_triage 1118`）；`plan_snapshot_queue` → DONE 145 / P1_VERIFY 544 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0 13；`build_queue.py` → `range_precise 366` /
  `range_coarse 83` / `nvd_cpe 23` / `alias_osv 42` / `legacy_triage 30`；
  `validate_dataset.py . --draft` 结构通过（`STRUCTURAL VALIDATION PASSED`，仍**不是**完整性、
  可利用性或分数校验）。
- **未做的事**：未运行被测代码、未自行给判定；未动 41990/45230/56374；未重生成
  `CHECKSUMS.sha256`；未声称数据集完成或 `PASS_KNOWNSWEEP`。

## 2026-10-25 — CVE-2025-61919 卷宗构建（rack v3.1.13，round41，待复核）

- **主张**：v3.1.13 的 `Rack::Request#POST`（`lib/rack/request.rb` 503 起）在 url-encoded 分支
  `elsif form_data? || parseable_data?`（526）走 `form_vars = get_header(RACK_INPUT).read`
  （531）——无长度参数，即 `IO#read(nil)` 读到 EOF，把整个 body 复制进一个 Ruby String；
  之后才 `parse_query(form_vars, '&')`（538）。**该 tag 的 `Rack::QueryParser` 完全没有限长**：
  `initialize(params_class, param_depth_limit)`（36），全文件不含 `BYTESIZE_LIMIT` /
  `PARAMS_LIMIT` / `QueryLimitError`（构建脚本逐 token 断言缺席）。所以在这个快照上，
  url-encoded 路径是**两处独立的无界**（先无界读、再无界解析）。**没有放大**，内存随发送
  字节线性增长。
- **修复**：3.1 线 `cbd541e8`（首发 3.1.18）把该行改成
  `get_header(RACK_INPUT).read(query_parser.bytesize_limit + 2) || ''`（3.1.18 的 534），
  并给 `query_parser.rb` 加 `attr_reader :bytesize_limit`（60）、缩短 `QueryLimitError`
  消息；3.2 线 `e179614c`（3.2.3）、2.2 线 `4e2c9039`（2.2.20，签名差异含 `key_space_limit`）。
  祖先关系实测：三者各自只在自己那条线的 tag 上为 True，对 v3.1.13/v3.1.17 为 False；
  相邻 multipart 修复 `f224f93b` 已在 v3.1.17/18、不在 v3.1.13（说明是不同变更）。
- **为何补钉 3.1.17 的 `query_parser.rb`**：4 MiB 的 `BYTESIZE_LIMIT` 与 4096 的 `PARAMS_LIMIT`
  在 3.1.17 就已存在（54 / 57，`check_query_string` 221/225 已在用），但**没有**
  `attr_reader :bytesize_limit`，所以 `Rack::Request` 读不到上限、仍然无界读。这解释了为什么
  本 CVE 的补丁在 `query_parser.rb` 侧只加了一个 accessor。该文件已作为第 19 件产物钉住，
  构建脚本对三处事实（两常量行号、accessor 缺席）有断言。
- **公开记录**：与 61771 不同，本条 CVE 的 GHSA / OSV / NVD / rubysec 内部一致，都指向三个
  真实修复提交（OSV 的 GIT range 同时含三个 tag commit 与三个 fix commit）；
  CVSS 3.1 7.5 HIGH（NVD 单条 Secondary，无 CVSS 4.0），CWE-400，SSVC automatable **no**；
  发布次序是**先发版后公告**（三个 gem 2025-10-10T00:36–00:41Z，GHSA 17:33:35Z、
  OSV 19:22:42Z、NVD 20:15:37Z），已写进 `published_at_note`。
- **产物**：19 件 sha256 固定（OSV×2、NVD、rubysec、3 个 fix 补丁、RubyGems 版本表、
  `query_parser.rb`×3（3.1.13/3.1.17/3.1.18）、`request.rb`×2、`spec_request.rb`×2、
  `CHANGELOG.md`×2、2 件 git 派生）。`dossier.json` 32,203 字节 / 19 evidence / 18 字段 /
  7 limitations / 5 open questions，状态 `READY_FOR_INDEPENDENT_REVIEW`；
  `critical_operation.line = 531-531`，`location.line = 526-538`。
- **离线预检**（未写 `data/`）：`promote_verified_rows.evidence_rows()` +
  `snapshot_evidence_rows()` 产出 **40 + 1 = 41** 条待入库 evidence 行，逐条对
  `v031/schemas/evidence.schema.json` 校验，`problems: []`；id 唯一、`source_url` 全 https。
- **复核派发**：round41 隔离复核者（`round41-independent-reviewer`）已派出，任务说明里
  明确要求 `fields_verified` 必须是**九个布尔 true**、实际值放 `field_values`（round39 就卡
  在这），要求 gem 3.1.13/3.1.18 实测 1/8/32/64 MiB 的 `params` bytesize 与 VmRSS/VmHWM，
  要求加「GET/其它路径」与「`RACK_QUERY_PARSER_BYTESIZE_LIMIT=8192` 正反」两个对照，
  并要求独立裁定五个开放问题（尤其「无放大的整体驻留是否足以 confirmed_affected」与
  「3.1.13 缺席的 QueryParser 限长算不算本 CVE」）。
- **未做的事**：未写 `data/`、未改 triage、未提升队列、未动 41990/45230/56374、
  未重生成 `CHECKSUMS.sha256`、未声明完成或 `PASS_KNOWNSWEEP`；没有执行 rack 代码、没有测内存。

## 2026-10-25 — CVE-2025-61780 卷宗构建（rack v3.1.13，round42，待复核）

- **主张**：v3.1.13 的 `Rack::Sendfile`（`lib/rack/sendfile.rb`）把**客户端请求头**当代理配置。
  `variation`（148-152）在构造时未给 variation、且 `env['sendfile.type']` 未设时，回退到
  `env['HTTP_X_SENDFILE_TYPE']`（151），于是客户端可以自行打开 sendfile 并决定回写哪个响应头
  （`headers[type.downcase]`，123/134）；`map_accel_path`（154-165）在应用层没有匹配的
  mappings 时回退到 `env['HTTP_X_ACCEL_MAPPING']`（157），于是客户端还能决定文件路径到 URL
  的替换，最终出现在 123 行的 `x-accel-redirect` 响应头里。**两半可分开触发**：启用半要求
  中间件没配 variation，映射半在「显式配置了 x-accel-redirect」的部署上**仍然生效**。
  `Rack::Files` 响应体有 `alias :to_path :path`（files.rb:185），触发前提由内置组件满足。
- **修复**：3.1 线 `7e69f65e`（首发 3.1.18）`variation` 只留 `@variation || env['sendfile.type']`，
  新增 `x_accel_mapping`（`return nil unless @variation =~ /x-accel-redirect/i`、
  `return nil if @mappings.any?`），`map_accel_path` 改调该 helper，两处映射正则 `^` → `\A`；
  3.2 线 `57277b77`（3.2.3）、2.2 线 `fba2c8bc`（2.2.20，2.x 头大小写）。
- **代码覆盖**：`sendfile.rb` 在 v3.1.13 / v3.1.17 / v3.2.2 三者**字节相同**（`395efb8b…`），
  v3.1.18 / v3.2.3 字节相同（`b0b8a22e…`），v3.1.0 已有两处回退（只有「未知 variation」日志行
  不同）。祖先实测：三个修复提交对 v3.1.0/3.1.13/3.1.17/3.2.2/2.2.19 全为 False，各自只在
  自己那条线的发布 tag 上为 True；OSV 的 `introduced 52901caf` 就是 `3.0.0` 标签 commit，
  Sendfile 首次进 core 的 `981f182b` 也是 v3.1.0 的祖先。
- **公开记录**：**没有**归属混淆（三个提交就是三个分支的真实修复），但时间顺序与 61919 相反：
  CVE 16:53:57Z 与 NVD 17:15:39Z 都早于 GHSA 17:31:31Z；三个 gem（2.2.20/3.1.18/3.2.3）
  00:36–00:41Z 最早。NVD 有两个 CVSS 3.1（5.8 Secondary `S:C`、5.3 Primary `S:U`）与三个 CWE
  （200/441/913），SSVC automatable **yes**，无 CVSS 4.0；rubysec cvss_v3 5.8。
- **产物**：23 件 sha256 固定（OSV×2、NVD、rubysec、3 个 fix 补丁、RubyGems 版本表、
  `sendfile.rb`×8（3.1.0/3.1.13/3.1.17/3.1.18/3.2.2/3.2.3/2.2.19/2.2.20）、
  `spec_sendfile.rb`×2、`CHANGELOG.md`×2、`files.rb`、2 件 git 派生）。
  `dossier.json` 37,114 字节 / 23 evidence / 18 字段 / 7 limitations / 5 open questions，
  状态 `READY_FOR_INDEPENDENT_REVIEW`；`critical_operation.line = 117-165`（覆盖 117-123 的分派
  与 148-165 的两个 helper），`location.line = 104-166`。
- **离线预检**（未写 `data/`）：`precheck_rows_61780.py` 用 `evidence_rows()` +
  `snapshot_evidence_rows()` 产出 **41 + 1 = 42** 条待入库 evidence 行，连同 vulnerability /
  location 行逐条对 v0.3.1 schema 校验，`problems: []`，id 无重复。
- **复核派发**：round42 隔离复核者（`round42-independent-reviewer`）已派出，任务说明同样要求
  `fields_verified` 九个布尔 true、值放 `field_values`；要求安装 gem 3.1.13/3.1.18 用
  `Rack::MockRequest` 实测「攻击头」「显式配置 x-accel-redirect」「x-sendfile 路径反射」三组，
  并要求独立复核 tag peel、祖先关系与三个字节相等事实。
- **未做的事**：未写 `data/`、未改 triage、未提升队列、未执行 rack 代码、未起代理；
  未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明完成或 `PASS_KNOWNSWEEP`。

## 2026-10-24/25 — CVE-2025-61919 入库（rack v3.1.13，round41，grade A）

- **复核**：`round41-independent-reviewer`（隔离目录
  `runs/independent/rack_v3.1.13_CVE-2025-61919_round41/`）给出 `confirmed_affected`、grade **A**，
  `reproduction_reference = reproduction/logs/matrix_summary.jsonl`；九字段
  （aliases/cwe/cvss/affected_ranges/vulnerable_commit/fix_commit/fixed_release/location/languages）
  全为 true，实际值在 `field_values`；`sha256sum -c` 142/142 OK。
  `check_verdict_packet.py` → `ok: true`、`problems: []`、`warnings: []`、143 个 preserved 文件。
- **复核员实测**（真 gem 3.1.13 / 3.1.17 / 3.1.18 + Ruby 3.2.3）：3.1.13 上 1/8/32/64 MiB 的
  url-encoded body 全部读入（`read_calls=[null]`），VmRSS 增量 +1,024/8,192/32,896/65,536 KiB
  （线性、1.0×、无放大）；3.1.18 在 4,194,306 字节截断并抛 `QueryLimitError`；3.1.17 全读 8 MiB
  后才抛 parser 限额（「read 先于 limit」的直接证据）；`text/plain` 对照读取 0/ΔRSS 0，裸
  `IO#read(nil)` ΔRSS 32,768 KiB。
- **入库**：2026-10-24T21:53:22Z `promote_verified_rows.py --apply`（1 漏洞 / 1 location /
  1 review / 41 evidence / 1 status）；2026-10-24T21:54:12Z 守卫式 triage 改写，候选
  `disc2_e4a6cf530641b47a3b064d73` → `confirmed_affected`
  （`runs/data_fixes/promote_2025_61919_triage_round41.py`，backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round41_20261024T215412Z.jsonl`）。
- **复核后更正**（`runs/verification/rack_v3.1.13_CVE-2025-61919/POST_REVIEW_CORRECTIONS.md`）：
  `entry_point.line` 503-542 → **503-551**（builder + dossier 重建，已入库 location 行用
  `runs/data_fixes/fix_61919_lines_2026-10-25.py` 守卫式改写，backup
  `runs/data_fixes/locations_before_61919_line_fix_20261024T215358Z.jsonl`）；3.1.18
  `check_query_string` 检查行 221-223 → **222-223**（仅 dossier 文本）。复核员另裁定
  3.1.13 的第二处无界（QueryParser 解析）属 **CVE-2025-46727**，且 `fixed_releases` 只有
  3.1.18 对本快照有效——两点写进 triage `notes` 与 LIMITATIONS §12，未改表字段。
- **计数**：vulnerabilities 155 / locations 155 / evidence 6029 / reviews 155（A 78 / B 77）/
  snapshot_vulnerability_status 126；triage confirmed_affected **146**、possible_affected **543**、
  unknown 574、confirmed_not_affected 1322、duplicate 28；队列 P3：DONE 146 / P1_VERIFY 543 /
  P1_REVIEW 574；possible 复核队列 543 行（`range_precise 365`）。`validate_dataset.py . --draft`
  → `STRUCTURAL VALIDATION PASSED`（0 error）。
- **未做的事**：未改 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明完成或
  `PASS_KNOWN_SWEEP`；rate 提示仍为 78/155（<60%）。

## 2026-10-24/25 — CVE-2025-61780 入库（rack v3.1.13，round42，grade A）

- **复核**：`round42-independent-reviewer`（隔离目录
  `runs/independent/rack_v3.1.13_CVE-2025-61780_round42/`）给出 `confirmed_affected`、grade **A**；
  九字段全 true，`reproduction_reference` 含脚本、命令、断言与结果文件；真 gem 3.1.13 / 3.1.18
  的 `sendfile.rb` sha256（`395efb8b…` / `b0b8a22e…`）与 tag 文件、peel 后 git blob 三者一致。
  `check_verdict_packet.py` → `ok: true`、`problems: []`、43 个 preserved 文件。
- **复核员实测**（`Rack::MockRequest` 驱动 `Rack::Sendfile` 包 `Rack::Files`，23/23 断言）：
  3.1.13 裸中间件 + `x-sendfile-type: x-accel-redirect` + `x-accel-mapping: <dir>/=/attacker/path/`
  → `x-accel-redirect: /attacker/path/secret.txt`、CL 0、空 body；`x-sendfile` 分支回显绝对路径；
  换行路径在 3.1.13 被 `^` 锚点匹配（`…safe%0A/pwned/.txt`），3.1.18 的 `\A` 不匹配；
  3.1.18 对同样请求不发任何 sendfile 头；显式配置 `x-accel-redirect` 时仍按客户端 mapping 映射
  （修复的有意保留）。
- **入库**：2026-10-24T21:56:56Z `promote_verified_rows.py --apply`（1 漏洞 / 1 location /
  1 review / 42 evidence / 1 status）；2026-10-24T21:57:42Z 守卫式 triage 改写，候选
  `disc2_913c1074780d784476386002` → `confirmed_affected`
  （`runs/data_fixes/promote_2025_61780_triage_round42.py`，backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round42_20261024T215742Z.jsonl`）。
- **复核后更正**（`runs/verification/rack_v3.1.13_CVE-2025-61780/POST_REVIEW_CORRECTIONS.md`）：
  README 的两处改动行数 50/70 → **67（+47/−20）/ 47（+37/−10）**；`fix_commits[].commit_date`
  原用 +13:00 本地日期，改为 **UTC**（`7e69f65e` 与 `fba2c8bc` → `2025-10-09`，`57277b77` 保持
  `2025-10-10`），builder + dossier 重建 + 已入库 `data/vulnerabilities.jsonl` 行守卫式改写
  （`runs/data_fixes/fix_61780_commit_dates_2026-10-25.py`，backup
  `runs/data_fixes/vulnerabilities_before_61780_commit_dates_20261024T215725Z.jsonl`）；README 的
  `sources/` 件数改为「24 个文件，其中 23 件钉住」。`location.line = 104-166` 与
  `critical_operation.line = 117-165` 的不相等但重叠未改（有意分层）。复核员另补测
  3.1.14/3.1.15/3.1.16 的 `sendfile.rb`，仍为 `395efb8b…`。
- **计数**：vulnerabilities 156 / locations 156 / evidence 6071 / reviews 156（A 79 / B 77）/
  snapshot_vulnerability_status 127；triage confirmed_affected **147**、possible_affected **542**、
  unknown 574、confirmed_not_affected 1322、duplicate 28；队列 P3：DONE 147 / P1_VERIFY 542 /
  P1_REVIEW 574；possible 复核队列 542 行（`range_precise 364`）。`validate_dataset.py . --draft`
  → `STRUCTURAL VALIDATION PASSED`（0 error）。
- **未做的事**：未改 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明完成或
  `PASS_KNOWN_SWEEP`；未把「CWE-441 为主」的建议写进 `cwe_ids` 字段（保持三值公开记录）。

## 2026-10-24/25 — CVE-2026-27205 卷宗构建（Flask 2.3.1，round43）

- **选题**：`snap_8ed1cab47a0b7011`（rep_id 596892，`tag_or_release = 2.3.1`，
  `vulnerable_commit = 721abdc3810057269503a72d2db80fb826f3c85c`）上的 CVE-2026-27205 /
  GHSA-68rp-wp8r-4726 / PYSEC-2026-2151。两条候选 `disc2_e6455792530ef4ded286ccbd` 与
  `adv3_620d1669d829c92b` 都指向本快照与同一公告，均为 `possible_affected`，尚未复核。
  选它是为了换仓库（上一条 Python 卷宗是 django，之后连续四条 rack）。
- **采集**：`collect_sources_27205.py` 在 `/tmp/flask_repo`（blobless clone）上跑出
  `{"pinned": 24, "expected": 24, "failures": []}`。24 件 = 22 件网络（OSV×3、NVD、
  `commit/<sha>.patch`、PyPI、`sessions.py`×4、`ctx/app/globals/templating`×2、
  `tests/test_basic.py`×2、`CHANGES.rst`×2）+ 2 件 git 派生（`git_tags.txt`、
  `git_ancestry.txt`）。`sources/` 目录共 25 个文件，`manifest.json` 自身不钉住。
- **关键代码事实**（2.3.1，`sessions.py` sha256 `912d178b…`）：`SecureCookieSession.accessed`
  默认 False（68），只在 `on_update`（73）与 `__getitem__`/`get`/`setdefault`（78/82/86）置真；
  文件内无 `__contains__`/`__len__`/`__iter__` 覆写，所以 `in`/`len()`/迭代不置位。
  `save_session`（322）先执行空 session 的早返回（334），再判断 Vary（347-349）——这是
  2.3.1 特有的第二层；2.3.3（333 早于 338）与 3.1.2（363 早于 368）已把 Vary 块提前。
- **修复事实**：`089cb86d` 是 merge commit（`Merge commit from fork`，父 `27be9338` 与
  `c17f3793`，tree 与 `c17f3793` 相同），改动在第二父；`commit/<sha>.patch` 因此是
  `From c17f3793`。3.1.3（tag object `8d05782c` → `22d92470`）的 `ctx.py` 新增
  `RequestContext.session` property（368-375，374 行置位），`sessions.py` 删掉三个逐方法覆写，
  `app.py` 1321-1322 改用 `ctx._session`，`templating.py` 不再替换 session 代理。祖先关系实测：
  修复不在 2.3.1 / 2.3.3 / 3.1.2，在 3.1.3；2.3.3 是 2.3 线最后版本，未获修复。
- **卷宗**：`build_dossier_27205.py`（fail-closed，A–M 组断言）产出 `dossier.json`
  39,279 字节 / 24 evidence / 18 字段 / 9 limitations / 5 open questions，状态
  `READY_FOR_INDEPENDENT_REVIEW`；`critical_operation.line = 347-349`（Vary 门），
  `location.line = 322-350`（save_session），`entry_point` = `app.py` 2004-2005。
  README 写明红/绿预期、两处开放问题（空 session 行为、2.3 线无回移）与隔离要求。
- **离线预检**（未写 `data/`）：`precheck_rows_27205.py` 用 `evidence_rows()` +
  `snapshot_evidence_rows()` 产出 **57 + 1 = 58** 条待入库 evidence 行，连同 vulnerability /
  location 行逐条对 v0.3.1 schema 校验，`problems: []`，id 无重复。
- **复核派发**：round43 隔离复核者（`round43-independent-reviewer`）已派出，要求
  `fields_verified` 九个布尔 true、值放 `field_values`；要求装真 Flask 2.3.1 / 3.1.3 跑
  `in`/`len`/迭代/`.get()`/`[]`/`.setdefault()` 与不碰 session 的对照路由，分「无 cookie」
  与「`/login` 后非空」两轮，并独立复核 tag peel、祖先关系与 merge/第二父事实。
- **未做的事**：未写 `data/`、未改 triage、未提升队列、未执行 Flask、未起缓存代理；
  未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明完成或 `PASS_KNOWN_SWEEP`。

### round43 落地：CVE-2026-27205（flask 2.3.1）复核通过并入库

- **复核**：`runs/independent/flask_2.3.1_CVE-2026-27205_round43/`，`round43-independent-reviewer`，
  `reviewed_at` 2026-10-24T22:11:30Z，`verdict = confirmed_affected`，`grade_recommendation = A`，
  九个 `fields_verified` 全 true，`reproduction_reference = reproduction/logs/matrix_summary.jsonl`。
- **复核者实测**：四个 venv 装 PyPI 真包 2.3.1 / 2.3.3 / 3.1.2 / 3.1.3（`sessions.py` sha256
  `912d178b…` / `ac51f640…` / `76ebd81a…` / `7b2c11aa…`，与 tag 文件一致），8 条访问路径 ×
  4 版本 × 2 模式共 **64 行红/绿，0 处不符**：2.3.1/2.3.3/3.1.2 上 `in`/`len`/迭代无 `Vary`，
  `.get`/`[]`/`.setdefault` 有；仅 3.1.3 每条路径都有。另用 nginx 1.24.0 `proxy_cache`
  （尊重但不忽略 `Set-Cookie`）演示串号：2.3.1 上「先登录后匿名」MISS→HIT，匿名者拿到
  `result=yes` / `session_len=1` 且两次响应均无 `Vary`；反序则登录者拿到 `result=null`。
  3.1.3 同序列 MISS→MISS 且带 `Vary: Cookie`。
- **口径拆分**：复核者把「空 session 早返回（334）先于 Vary 门（347-349）」判为
  **该快照特有的同结果表现，不是本 CVE 的根因、修复 diff 也不改这个顺序**，verdict 不依赖它；
  采集方接受，dossier 与 triage 文案均按此写，不含混算作 CVE 的一部分。
- **packet 校验**：`check_verdict_packet.py` 最终 `ok: true`、2925 个 preserved 项、
  0 problems / 0 warnings。首轮只差 12 个 venv 解释器路径：清单不登记则 `file not covered`，
  登记绝对符号链接则 `path escapes round dir`（checker 的 realpath 要求与 `rglob` 跟随链接
  互相冲突）。复核者把 4 个 `bin/python3` 换成 `/usr/bin/python3.12` 的逐字节副本
  （sha256 `e50d468e…`，8,020,928 B），`python`/`python3.12` 保留为指向 `python3` 的相对链接，
  四个 venv 复跑确认版本正确；改动全在 round dir 内，`verdict.json` 与复现日志未动。
- **复核后更正**（`runs/verification/flask_2.3.1_CVE-2026-27205/POST_REVIEW_CORRECTIONS.md`）：
  OSV CVE 的 ECOSYSTEM 版本上界原误写 `2.2.5`（实际列表 17 项，最大 **2.2.0**）；「0.x/1.x/
  2.0.x/2.1.x/2.2.x」的区间化措辞改为逐版枚举；GHSA/PYSEC 的「枚举 2.3.1/2.3.3/3.1.2」
  改为「逐版枚举到 3.1.2（唯一缺的是修复版 3.1.3）」。`build_dossier_27205.py` 已改并重建
  `dossier.json`（39,279 → 39,515 字节，24 evidence / 18 字段 / 9 limitations 不变），
  `precheck_rows_27205.py` 仍为 `problems: []`，重建后 checker 复跑仍 `ok: true`。
  verdict / grade / fields_verified / location 均未改动。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-24T22:16:52Z 写入
  1 漏洞 / 1 location / 1 review / **58 evidence** / 1 status；review `rev_CVE_2026_27205_r1`，
  `reviewer` = `flask-2.3.1-collector-27205`，`independent_reviewer` = `round43-independent-reviewer`，
  grade A 归因于复核者实际执行的 64 行红/绿与 nginx 串号复现。
- **triage**：`runs/data_fixes/promote_2026_27205_triage_round43.py`（带守卫，dry-run 先跑，
  `problems: []`）把两条候选 `disc2_e6455792530ef4ded286ccbd` 与 `adv3_620d1669d829c92b`
  改写为 `confirmed_affected`，`checked_at = 2026-10-24T22:20:00Z`；
  backup `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round43_20261024T221722Z.jsonl`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`（非完备性/可利用性
  校验）。九张主表现为 157 vulnerabilities / 157 locations / **6129 evidence** / 157 reviews
  （A 80 / B 77）/ **128 snapshot_vulnerability_status**；triage 2613 行 =
  149 confirmed_affected / 1322 confirmed_not_affected / 540 possible_affected / 574 unknown /
  28 duplicate。`plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 149 / P1_VERIFY 540 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 540 行（`range_precise 363` / `range_coarse 82` / `nvd_cpe 23` / `alias_osv 42` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

### round44 落地：CVE-2024-49767（werkzeug 3.0.2）复核通过并入库

- **对象**：`werkzeug` 3.0.2（`snap_b57262de7996e8a2`，`repo_id 997338`，轻量 tag `3.0.2` →
  `d70dcea305bf842c5a3b55265b5ffac2db012e23`），CVE-2024-49767 / GHSA-q34m-jh98-gwm2 /
  PYSEC-2026-3417（werkzeug），另有 PYSEC-2026-1860（quart，独立记录，不计入本仓库）。
- **机制**：`MultiPartParser.parse`（`src/werkzeug/formparser.py:353-392`）用 `_chunk_iter`
  按 `buffer_size`（默认 64 KiB）读 body 并逐块交给 `MultipartDecoder.receive_data`；唯一的
  `max_form_memory_size` 检查在那里，比较的是 `len(self.buffer) + len(data)`——**单块**而非
  **单字段**。`parse` 每轮把解码器排空，因此 buffer 恒为空，非文件 part 的 `Data` 事件在 381-382
  直接 append 到列表，384-386 再整体 join/decode：大于限制但按更小块投递的普通字段全数绕过检查
  并完整驻留内存。修复 merge `50cfeebc`（第二父 `8760275a` "apply max_form_memory_size another
  level up in the parser"，merge tree 等于第二父的 tree，`commit/<sha>.patch` 返回的正是
  `From 8760275a`，两份 patch 逐字节相同）在 355 声明 `field_size`、374 对 Field 归零、
  379 对 File 置 None、386 逐事件累加、388-389 超限抛 `RequestEntityTooLarge`；
  `sansio/multipart.py` 保留原逐块检查、只加注释。修复随 3.0.6 发布
  （annotated tag `a82e04ed` → `5eaefc39`）。3.0.5 仍脆弱：Data 分支在 380 裸 append，
  `sansio/multipart.py` 与 3.0.2 的 blob 逐字节相同（`bbf5cbb3…`）。
- **引入点**：GHSA 引用的 `cbb446fd`（"Refactor the Multipart parsing into a Sans-IO layer",
  2021-01-20）里 Data 分支已是裸 `_write`（456-457）、`receive_data`（116-123）也只有逐块检查；
  OSV CVE 把引入点写成 `22bfb446` = "Release 2.0.0rc1"（2021-02-07）。`cbb446fd` 是
  `22bfb446` 的祖先，被 `2.0.0rc1` / `2.0.0` / `3.0.2` / `3.0.6` 包含，无 0.x/1.x tag 包含，
  与公布区间下界 2.0.0rc1 一致（`affected_range ">= 2.0.0rc1, < 3.0.6"`）。
- **卷宗**：`runs/verification/werkzeug_3.0.2_CVE-2024-49767/`，`build_dossier_49767.py`
  fail-closed 构建，`sources/` **25 个** sha256 pin（20 网络 + 5 派生：`git_tags` /
  `git_ancestry` / `git_introduced` / `raw_formparser_intro.py` / `raw_multipart_intro.py`），
  `dossier.json` 40,507 字节 / **25 evidence** / 18 field_evidence / **10 limitations** /
  5 open_questions，`status READY_FOR_INDEPENDENT_REVIEW`，`prepared_by
  werkzeug-3.0.2-collector-49767`；`precheck_rows_49767.py` 输出
  `{"vulnerabilities":1,"locations":1,"evidence":59}` / 18 字段 / `problems: []`。
- **复核**：`runs/independent/werkzeug_3.0.2_CVE-2024-49767_round44/`，
  `round44-independent-reviewer-werkzeug-3.0.2`，`reviewed_at` 2026-10-24T22:29:59Z，
  `verdict = confirmed_affected`，`grade_recommendation = A`，九个 `fields_verified` 全 true，
  `reproduction_reference = reproduction/raw/redgreen_wz302.stdout.json`，8 limitations / 5 discrepancies。
- **复核者实测**：两个 preserved venv 装 PyPI 真包 3.0.2 / 3.0.6，安装后 `formparser.py` /
  `sansio/multipart.py` sha256 与 tag 文件一致（3.0.2 `5411abb1…` / `bbf5cbb3…`；3.0.6
  `9a4acff2…` / `7cc1a063…`）。`MultiPartParser(max_form_memory_size=1 MiB, buffer_size=64 KiB)`
  + 3 MiB 普通字段：3.0.2 在 0.0077 s 内完整返回 3145728 字节的字段值，峰值 RSS 41416 KiB
  （解析前 34760 KiB）；3.0.6 在 `formparser.py:389` 抛 `RequestEntityTooLarge`，RSS 34900 vs 34772 KiB。
  逐块插桩：3.0.2 共 49 次非空 `receive_data`，`buffer + chunk` 最大 65536 字节、
  非空 buffer 的调用 0 次，1 MiB 限制从未触发。负控制两条（`buffer_size` 2 MiB > 限制、
  无视 `read(n)` 一次返回 3 MiB）两版都在 `receive_data` 抛错；边界
  `max_form_memory_size=None` 两版都成功——即绕过要求限制已设置且分块小于限制。
- **复核后更正**（`POST_REVIEW_CORRECTIONS.md`，5 条）：**采纳 1 条**——上游
  `test_multipart_max_form_memory_size`（`max_form_memory_size=10, buffer_size=5`）在 3.0.2
  也会抛错（帧在 `sansio/multipart.py:143`），3.0.6 停在 `receive_data:145`、
  根本没走到新增的 `formparser.py:389`，**该测试不具判别力**；已改写 evidence 文字、新增 1 条
  limitation、改写 `open_questions[4]`、README 两处补注。**不采纳 2 条**（非事实差异）：
  OSV 记录 `json.load()` 后完全相等、仅键序/空白不同；NVD 记录唯一差异是 `/timestamp`。
  第 4 条 `snapshot_evidence` 涉及 `data/**`、复核期间不得读，由采集方前后各读一次覆盖
  （`repo_id 997338` / `3.0.2` / `d70dcea3…`）。第 5 条其余全部一致。
  verdict / grade / location（`formparser.py:381-382`）/ 九个字段 / 区间 / 严重度均未改动，
  判别依据是复核员自己的 3 MiB 红/绿，不依赖那条上游测试，故不需重新复核。
- **packet 校验**：`check_verdict_packet.py` → `{"decision":"confirmed_affected","grade":"A",
  "preserved_files":70,"problems":[],"warnings":[],"ok":true}`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-24T22:31:22Z 写入
  1 漏洞 / 1 location / 1 review / **59 evidence** / 1 status；review `rev_CVE_2024_49767_r1`，
  `reviewer` = `werkzeug-3.0.2-collector-49767`，`independent_reviewer` =
  `round44-independent-reviewer-werkzeug-3.0.2`，grade A 归因于复核者实际执行的红/绿与插桩。
- **triage**：`runs/data_fixes/promote_2024_49767_triage_round44.py`（带守卫，dry-run 先跑，
  `problems: []`）把两条候选 `disc2_072f55e1dd1d4707db4e1fce` 与 `adv3_5b31cc3f2c071fe8`
  改写为 `confirmed_affected`，`checked_at = 2026-10-24T22:35:00Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round44_20261024T223140Z.jsonl`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`（非完备性/可利用性
  校验）。九张主表现为 158 vulnerabilities / 158 locations / **6188 evidence** / 158 reviews
  （A 81 / B 77）/ **129 snapshot_vulnerability_status**；triage 2613 行 =
  151 confirmed_affected / 1322 confirmed_not_affected / 538 possible_affected / 574 unknown /
  28 duplicate。`plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 151 / P1_VERIFY 538 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 538 行（`range_precise 362` / `range_coarse 81` / `nvd_cpe 23` / `alias_osv 42` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

### round45 落地：CVE-2021-3603（PHPMailer 6.1.5）复核通过并入库

- **对象**：`PHPMailer/PHPMailer` v6.1.5（`snap_b840904431f8a856`，`repo_id 2253830`，annotated tag
  `68813f28` → commit `a8bf068f64a580302026e484ee29511f661b2ad3`），CVE-2021-3603 /
  GHSA-77mr-wc79-m8j3 / BIT-phpmailer-2021-3603。
- **机制**：`PHPMailer::validateAddress($address, $patternselect = null)`
  （`src/PHPMailer.php:1304`）在 selector 为 null 时取 `static::$validator`（1306-1307），6.1.5 的默认值
  是 `'php'`（576），随后 1309-1311 `if (is_callable($patternselect)) { return
  $patternselect($address); }` 直接调用同名全局函数并把返回值当作校验结论；内建 switch 的
  `case 'php': default: filter_var(...)`（1358-1360）只有 callable 判定失败时才到达。可达路径：
  addAddress 999 → addOrEnqueueAnAddress 1063 → addAnAddress 1118 → 1134、setFrom 1235 → 1243、
  parseAddresses 1178 → 1185/1202/1211、preSend 1453 → 1500、mailSend 1762 → 1781/1784。
  公告前提是攻击者已能在宿主全局命名空间定义同名函数：本缺陷提供触发通路，不是独立远程利用。
- **引入点**：`77c0bc8d`（2016-05-09，"Add ability to inject custom validator and set custom default
  validator, fixes #573"）把分支加进 `class.phpmailer.php`；6.0 线经 merge `86d2b069` 带入。合并前
  两个父逐文件实测：`384609cc`（6.0 侧）`src/PHPMailer.php` 存在但分支 0 次、无 `class.phpmailer.php`；
  `444a355b`（master 侧）无 `src/PHPMailer.php`，`class.phpmailer.php` 有 1 次——所以「没有任何一份
  6.0 文件在合并前含该分支」成立，但「两个父都不含该分支」不成立（round45 复核员指出，已更正）。
  首个带分支的发行版是 v5.2.15（`class.phpmailer.php:1056-1061`）与 v6.0.0rc2（1033-1038）；
  两者的 `$validator` 默认值仍是 `'auto'`，**默认配置劫持**自 v6.0.0rc3（492 行默认 `'php'`、
  1136 行分支）起，即代码级 6.0.0rc3 .. 6.4.1；更早版本需应用自己把 `$validator` 设成 `'php'`
  或显式传 `'php'`。下界仍取「分支存在」口径 5.2.15 / 6.0.0rc2，rc3 边界单列为 range_expression。
- **修复与首发**：`45f3c18dc6a2de1cb1bf49b9b249a9ee36a5f7f3`（2021-06-15T17:37:24+02:00，
  "Deny string-based callables altogether"，父 `6334bab2` 已带未发布的折中守卫，只拒
  `php/pcre/pcre8/html5`），在 6.5.0 的 1341 行加 `&& !is_string($patternselect)`、1342 改用
  `call_user_func`。修复是 v6.5.0（轻量 tag `a5b5c43e`）的祖先，v6.4.1 无；5.2 线到 v5.2.28
  （2020-03-19）仍无，故 5.2 线无修复版本。fix 提交自己的文件仍是 VERSION 6.4.1、且早于同发布的
  CVE-2021-34551 `setLanguage()` 重写，因此与 v6.5.0 tag 文件不逐字节相同；`validateAddress`
  1335-1342 两处一致。
- **卷宗**：`runs/verification/phpmailer_6.1.5_CVE-2021-3603/`，`collect_sources_3603.py` 最后一次
  `{"pinned": 31, "expected": 31, "fetched": 5, "reused": 26, "failures": []}`（32 个文件 = 31 pin +
  `manifest.json`；26 网络 + 5 派生，其中 v6.0.0rc3 为复核后补钉）；`build_dossier_3603.py`
  fail-closed 构建，`dossier.json` 47,221 字节 / **30 evidence** / 18 field_evidence /
  **14 limitations** / 5 open_questions，`status READY_FOR_INDEPENDENT_REVIEW`，`prepared_by
  phpmailer-6.1.5-collector-3603`；`precheck_rows_3603.py` 输出
  `{"vulnerabilities":1,"locations":1,"evidence":66,"snapshot_vulnerability_status":1}` /
  九个 canonical 全覆盖 / `problems: []`。
- **复核**：`runs/independent/phpmailer_6.1.5_CVE-2021-3603_round45/`，
  `round45-independent-reviewer`，`reviewed_at` 2026-10-24T22:55:55Z，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九个 `fields_verified` 全 true，location 1309-1311，
  `reproduction_reference = reproduction/harness.php`，6 limitations / 4 discrepancies。
- **复核者实测**：自写 `harness.php`（不用采集方 probe），输入是自己的 refetch（v6.1.5
  `9e8ad5d8…`、v6.5.0 `ce454285…`），PHP 8.4.23 CLI（NTS、WSL2），injected 模式在 `require` 前定义
  全局 `php()`（返回 true、记录调用、写 marker）与 `phpx()`（返回 false），plain 模式不定义任何同名函数。
  6.1.5 vs 6.5.0：`validateAddress('not-an-address')` 默认 selector → true 且调用 `php(...)` vs false
  无调用；`validateAddress('victim@example.com')` → true 调用 vs true 无调用；
  `validateAddress('not-an-address','php')` → true 调用 vs false；`validateAddress('victim@example.com',
  'phpx')` → false 调用 vs true；`addAddress('bad@domain')` → true 收下收件人 vs false 无收件人；
  `setFrom('bad@domain')` → true 且 From 变 `bad@domain` vs false 保持 `root@localhost`。marker 在
  6.1.5 记录 6 次注入调用、6.5.0 不存在；闭包两版都仍被调用（修复只禁字符串）；plain 负控制两版
  九项探针一致、零调用；`compare_runs.py` 18/18 断言通过、stderr 全空。
- **复核后更正**（`POST_REVIEW_CORRECTIONS.md`，3 条全部采纳）：(a) merge 父提交措辞——改为采集脚本
  对两个父逐文件实测并写入 `git_introduced.txt`、builder 断言、dossier 证据与 README；(b) `$validator`
  默认值边界——补钉 v6.0.0rc3、新增 evidence 行、`affected_range` 注记与 range_expression、
  limitation 5；(c) OSV CVE / NVD / GHSA 渲染页活记录漂移——limitation 14，字段值经复核者逐项重核
  均未变。九个 canonical 字段的值与 location 一个未改，grade A 仍归因于复核者自己的执行，
  不依赖任何采集方改动。
- **packet 校验**：`check_verdict_packet.py` → `{"decision":"confirmed_affected","grade":"A",
  "preserved_files":46,"problems":[],"warnings":[],"ok":true}`（复核后再次运行仍 ok）。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-24T23:01:01Z 写入
  1 漏洞 / 1 location / 1 review / **66 evidence** / 1 status；review `rev_CVE_2021_3603_r1`，
  `reviewer` = `phpmailer-6.1.5-collector-3603`，`independent_reviewer` =
  `round45-independent-reviewer`。
- **triage**：`runs/data_fixes/promote_2021_3603_triage_round45.py`（守卫与 round44 同构，另加
  `independent_reviewer != reviewer` 与 verdict 作者一致性检查；dry-run 先跑 `problems: []`）把
  `disc2_fda17748360754567b087fc3` 与 `adv3_219fba69f30a5c11` 改写为 `confirmed_affected`，
  `checked_at = 2026-10-25T07:10:00Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round45_20261024T230138Z.jsonl`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`（非完备性/可利用性
  校验）。九张主表现为 159 vulnerabilities / 159 locations / **6254 evidence** / 159 reviews
  （A 82 / B 77）/ **130 snapshot_vulnerability_status**；triage 2613 行 =
  153 confirmed_affected / 1322 confirmed_not_affected / 536 possible_affected / 574 unknown /
  28 duplicate。`plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 153 / P1_VERIFY 536 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 536 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 42` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2024-8176 入库（libexpat R_2_6_2，round46，grade A）

### round46 落地：CVE-2024-8176（libexpat R_2_6_2）复核通过并入库

- **对象**：`libexpat/libexpat` `R_2_6_2`（`snap_67132f0363b8bc23`，`repo_id 80314213`，annotated tag
  `2628777302c195dd489baaa76fc2a7f048fe0aa7` → commit `fa75b96546c069d17b8f80d91e0f4ef0cde3790d`），
  CVE-2024-8176（CWE-674，NVD 只有 secalert@redhat.com 的 Secondary CVSS 3.1 7.5）。
- **机制**：实体展开没有嵌套计数。`processInternalEntity`（`expat/lib/xmlparse.c:5817-5874`）调用
  `doContent`（2952）展开替换文本，替换文本里再出现实体引用又回到 `processInternalEntity`；
  属性值走 `appendAttributeValue`（6150）自递归，参数实体定义走 `storeEntityValue`（6271）自递归。
  N 条线性链接的实体即占用 O(N) 个 C 栈帧，8 MiB 栈上约 9000 层即溢出。
- **修复与首发**：PR #973 合并 `99529768b4a722f46c69b04b874c1d45b3eb819c`（2025-03-13，六条代码提交 +
  Changes + merge），首发 2.7.0（`R_2_7_0` tag object `98f15369f1cb88b8cf6ae6388bb69dd58b0db433`
  → `6d4ffe856df497ac2cae33537665c3fec7ec8a00`，OSV GIT range 的 fixed 事件）。2.7.0 新增
  `processEntity`（5972），并把本已存在的 `internalEntityProcessor`（2.6.2 的 470 声明 / 5865 赋给
  `m_processor` / 5881 定义，原用于解析暂停续跑）改造成主循环入口（6034）；`appendAttributeValue`
  （6206）与 `storeEntityValue`（6413）改为 `for (;;)` 迭代。`R_2_6_4` 不含修复、`R_2_7_0` 含。
- **卷宗**：`runs/verification/libexpat_R_2_6_2_CVE-2024-8176/`，24 件 sha256 钉住来源
  （OSV / NVD / issue #893 / PR #973 / 六条修复提交 / 两个 tag 的 `xmlparse.c` 与 `Changes`），
  `dossier.json` 21 条证据 / 9 个字段映射 / 6 条 limitations；采集侧 `repro/` 用公开 API 跑三种载荷形态
  与一个非嵌套对照，11 个用例全 PASS（`failures=0`），崩溃栈分别落在 5858↔2952、6150、6271。
- **独立复核**：`runs/independent/libexpat_R_2_6_2_CVE-2024-8176_round46/`，
  `reviewer_identity = round46-independent-reviewer`，`reviewed_at = 2026-10-24T23:24:46Z`，
  `verdict = confirmed_affected`，`grade_recommendation = A`，九项 `fields_verified` 全 true，
  `location` 行区间 `5817-5874` 与卷宗 `critical_operation` 完全重叠。复核者自行全量 clone、自己建两棵
  tag 树、自写 harness 与驱动，未复用采集方 harness：2.6.2 ASan 三种形态 stack-overflow、2.7.0 全过、
  2.6.2 `-O2` 三例 SIGSEGV；非嵌套对照与 mode1 文档字节数完全相同（537,839 B）而两版均过，ASan 下
  8000 过 / 9000 崩，证明触发因素是嵌套深度。唯一分歧是 `internalEntityProcessor` 措辞（已记入
  `POST_REVIEW_CORRECTIONS.md` 并改 README），判定不受影响。
- **门禁与入库**：`check_verdict_packet.py` 首次报三个上游 `README.md` 符号链接未进
  `preserved_sha256.txt`（复核者用 `find -type f` 统计，校验器用 `rglob`/`is_file` 跟随链接）；补齐后
  671 行、0 problems / 0 warnings。`promote_verified_rows.py --apply` 于 2026-10-24T23:27:57Z 写入
  1 漏洞 / 1 location / 1 review / **30 evidence** / 1 status；review 的 `reviewer` =
  `libexpat-8176-collector`，`independent_reviewer` = `round46-independent-reviewer`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round46_2026-10-25.py`（守卫 decision / snapshot /
  repo / 别名引用与 grade A PASS 复核，dry-run 先跑 `problems: []`）把 `disc2_c3dc65c90ed8e1207d042404`
  改写为 `confirmed_affected`，`checked_at = 2026-10-24T23:28:00Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round46_20261024T232800Z.jsonl`。
- **复核后更正**：卷宗 `field_evidence` 原来只有 `cvss` 键，`validate_dataset.py` 要求 `severity` 键，
  导致 `--draft` 报 `CVE-2024-8176: missing PASS evidence for severity`。处理：`build_dossier_8176.py`
  增加 `"severity": [1, 0]`（与 `cvss` 同指向 NVD / OSV 两条钉住记录）并重建，逐键比对确认除
  `severity` 与 `prepared_at` 外无变化（旧件备份
  `runs/data_fixes/dossier_8176_before_severity_key_20261024T233000Z.json`）；再由
  `runs/data_fixes/add_severity_evidence_round46_2026-10-25.py`（用 promoter 自己的 `evidence_rows()`，
  守卫 verdict 的 `cvss` 已验证且 grade A）追加 2 行 `field_path=severity` 证据，
  `data/evidence.jsonl` 6284→6286，备份
  `runs/data_fixes/evidence_before_severity_rows_round46_20261024T233500Z.jsonl`。round47 卷宗已按同一
  规范在送审前同时写 `cvss` 与 `severity`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`（非完备性/可利用性
  校验）。九张主表现为 160 vulnerabilities / 160 locations / **6286 evidence** / 160 reviews
  （A 83 / B 77）/ **131 snapshot_vulnerability_status**；triage 2613 行 =
  154 confirmed_affected / 1322 confirmed_not_affected / 535 possible_affected / 574 unknown /
  28 duplicate。`plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 154 / P1_VERIFY 535 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 535 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 41` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2026-24515 入库（libexpat R_2_6_2，round47，grade A）

### round47 落地：CVE-2026-24515（libexpat R_2_6_2）复核通过并入库

- **卷宗**：`runs/verification/libexpat_R_2_6_2_CVE-2026-24515/`（25 件来源、`dossier.json` 14 条证据 /
  9 个字段映射）。主张：`XML_ExternalEntityParserCreate` 复制了 unknown-encoding handler，却没有复制
  `m_unknownEncodingHandlerData`（`parserInit` 置 NULL，restore 只恢复 handler），子解析器解析外部实体、
  遇到声明未知编码的文本声明时，`handleUnknownEncoding` 用 NULL 调用应用 handler；CWE-476。
- **修复边界**：`86fc914a`（3 行）+ `3de54af0`（Changes）+ `f14b0845`（merge PR #1131），首个 release
  `R_2_7_4`（tag object `ff7046b0…` → `f5c2890d…`，2026-01-31）；`R_2_7_3` 是修复前最后一个 release。
- **采集侧复现**：`repro/harness_24515.c` 只用公开 API，2.6.2/2.7.3 在外部实体声明未知编码时 handler
  收到 NULL（ASan 134 / `-O2` 139），2.7.4 handler 收到非 NULL、子解析以 unknown encoding 失败；
  主文档未知编码等三种对照均符合预期，12 个用例全 PASS（`failures=0`）。
- **独立复核**：`runs/independent/libexpat_R_2_6_2_CVE-2026-24515_round47/`，
  `reviewer_identity = round47-independent-reviewer`，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九项 `fields_verified` 全 true，`location` 行区间与卷宗
  `critical_operation` 1476 重叠。复核者自行全量 clone、按 tag 建源码树、自写 harness 与驱动，
  三个版本（2.6.2 / 2.7.3 / 2.7.4）× 两种构建：红侧 ASan SEGV（`abort_on_error=1` 时 134）、
  `-O2` 139，handler 收到 NULL；绿侧 2.7.4 不崩、handler 非 NULL、子解析报
  `XML_ERROR_UNKNOWN_ENCODING`（18）。
- **门禁**：`check_verdict_packet.py` 首次报三个上游 `README.md` 符号链接未进
  `preserved_sha256.txt`（`find -type f` 与 `rglob` + `is_file()` 的差异），补齐后 27 行、
  0 problems / 0 warnings。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-24T23:37:44Z 写入 1 漏洞 / 1 location /
  1 review / **26 evidence** / 1 status；review 的 `reviewer` = `libexpat-24515-collector`，
  `independent_reviewer` = `round47-independent-reviewer`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round47_2026-10-25.py`（守卫 decision / snapshot /
  repo / 别名引用与 grade A PASS 复核，dry-run 先跑 `problems: []`）把 `disc2_e08b1422a5df9ab74c159a7a`
  改写为 `confirmed_affected`，`checked_at = 2026-10-24T23:38:00Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round47_20261024T233748Z.jsonl`。
- **复核后更正**：卷宗 README 把 `parserInit` 的两句标成 1145/1146，实际是 1144/1145（`dossier.json`
  引用的 1145 指 `m_unknownEncodingHandlerData`，本身正确）。已改 README 注释并记入卷宗内
  `POST_REVIEW_CORRECTIONS.md`；判定、grade、九个字段与 location 均未改动。复核者另记录重抓字节
  差异（OSV 键序、NVD `timestamp`）与本出口 GitHub REST 限流改用 `.patch`/HTML 的事实，均无实质分歧。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  161 vulnerabilities / 161 locations / **6312 evidence** / 161 reviews（A 84 / B 77）/
  **132 snapshot_vulnerability_status**；triage 2613 行 = 155 confirmed_affected /
  1322 confirmed_not_affected / 534 possible_affected / 574 unknown / 28 duplicate。
  `plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 155 / P1_VERIFY 534 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 534 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 40` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2026-32776 入库（libexpat R_2_6_2，round48，grade A）

### round48 落地：CVE-2026-32776（libexpat R_2_6_2）复核通过并入库

- **卷宗**：`runs/verification/libexpat_R_2_6_2_CVE-2026-32776/`（25 件来源、`dossier.json` 18 条证据 /
  9 个字段映射）。主张：0 字节外部参数实体在实体声明值里被引用时，子解析器在编码探测前就进入
  `storeEntityValue`，`enc` 仍是 `XmlInitEncoding()` 设的 probe encoding（只填 `scanners[]`，不填
  `literalScanners[]`），`XmlEntityValueTok` 经未初始化的 `literalScanners[XML_ENTITY_VALUE_LITERAL]`
  调用；CWE-476。触发需要外部 DTD + `XML_ExternalEntityParserCreate` + `XML_SetParamEntityParsing`。
- **修复边界**：`5be25657`（`storeEntityValue` 9 行：`entityTextPtr >= entityTextEnd` 早退 + 19 行回归
  测试）+ `dbd511a2`（Changes）+ `635db9e1`（merge PR #1158），首个 release `R_2_7_5`
  （tag object `ef8dd281…` → `f31adfd5…`，2026-03-17）；`R_2_7_4` 是修复前最后一个 release。
- **采集侧复现**：`repro/harness_32776.c` 只用公开 API，四个 mode（0 字节实体在实体值中、非空对照、
  实体值无引用、0 字节实体在声明之间）；2.6.2 与 2.7.4 的 mode 1 在 ASan 下 134、`-O2` 下 139
  （崩溃栈 `storeEntityValue:6209` / `:6796`），2.7.5 为 0；24 个用例全 PASS（`failures=0`）。
  记录写明：被调用的是**未初始化**函数指针，零页读 NULL、ASan 填 `0xbe`，不是代码写死的 NULL。
- **独立复核**：`runs/independent/libexpat_R_2_6_2_CVE-2026-32776_round48/`，
  `reviewer_identity = round48-independent-reviewer`，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九项 `fields_verified` 全 true，`location` 6209 与卷宗
  `critical_operation` 重叠。复核者自行 clone、按 tag 构建、独立重写 harness，24/24 与采集侧数值一致；
  另用 gdb 在 plain 构建看到 `#0 0x0`、在 ASan 看到高位垃圾地址，独立确认未初始化函数指针。
  它记录 3 条说明性差异（无实质分歧），未触发任何更正。
- **门禁**：`check_verdict_packet.py` → 45 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-24T23:48:50Z 写入 1 漏洞 / 1 location /
  1 review / **30 evidence** / 1 status；review 的 `reviewer` = `libexpat-32776-collector`，
  `independent_reviewer` = `round48-independent-reviewer`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round48_2026-10-25.py`（守卫 decision / snapshot /
  repo / 别名引用与 grade A PASS 复核，dry-run 先跑 `problems: []`）把 `disc2_53b5afd3497a71e30facfcaf`
  改写为 `confirmed_affected`，`checked_at = 2026-10-24T23:49:00Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round48_20261024T234855Z.jsonl`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  162 vulnerabilities / 162 locations / **6342 evidence** / 162 reviews（A 85 / B 77）/
  **133 snapshot_vulnerability_status**；triage 2613 行 = 156 confirmed_affected /
  1322 confirmed_not_affected / 533 possible_affected / 574 unknown / 28 duplicate。
  `plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 156 / P1_VERIFY 533 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 533 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 39` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2026-32777 入库（libexpat R_2_6_2，round49，grade A）

- **候选与快照**：`disc2_05ab8b8704bfc3d3ff934592`（`possible_affected`，
  `review_method = trusted_range_with_branch`）→ 快照 `snap_67132f0363b8bc23` =
  `R_2_6_2`（annotated tag object `2628777302…` peel 到 `fa75b965…`）。
- **问题**：`expat/lib/xmlparse.c` 的 `entityValueProcessor`（2.6.2 起 4633-4666）在实体值里只靠
  `XmlPrologTok` 返回非正 token 退出，唯一的推进语句是 4664 行 `start = next;`。外部实体内容开头的
  start tag 返回 `XML_TOK_INSTANCE_START` 且 `next == start`，于是零推进死循环（CWE-835，NVD Primary
  5.5 MEDIUM；NVD Secondary 与 OSV 4.0 为 `AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`）。
- **修复**：`55cda8c7`（10 行 guard）+ `a7805c1a`（30 行回归测试）+ `dbd511a2`（Changes）+
  `6a814cae`（merge PR #1162），首个 release `R_2_7_5`（tag object `ef8dd281…` → `f31adfd5…`，
  2026-03-17）；`R_2_7_4`（`f5c2890d…`）仍是修复前最后一个 release。
- **卷宗**：`runs/verification/libexpat_R_2_6_2_CVE-2026-32777/`，20 件 sha256 钉住来源、
  `dossier.json` 20 条证据 / 9 个字段映射；`precheck_rows_32777.py` 输出 `problems: []`。
- **采集侧复现**：`repro/harness_32777.c` 只用公开 API，外部实体内容 `<!ENTITY e "<a>">` 一类形态；
  2.6.2 与 2.7.4 在 ASan 与 `-O2` 下均挂死（由外部 `timeout`/`alarm` 收尾），2.7.5 立即返回
  `XML_ERROR_SYNTAX` → 外层 `XML_ERROR_EXTERNAL_ENTITY_HANDLING`。
- **独立复核**：`runs/independent/libexpat_R_2_6_2_CVE-2026-32777_round49/`，
  `reviewer_identity = round49-independent-reviewer`，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九项 `fields_verified` 全 true，`location` 4664 与卷宗
  `critical_operation` 重叠；`reviewed_at = 2026-10-24T23:58:10Z`。复核者自建 clone 与六个构建树
  （2.6.2 / 2.7.4 / 2.7.5 × ASan+UBSan / `-O2`），自写 harness 28 个用例全过：红行以自身 `alarm(8)`
  挂死 exit 142，`user=3.13 sys=0.00` 证明是纯 CPU 自旋而非阻塞；绿行立即返回。
- **门禁**：`check_verdict_packet.py` → 53 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-25T00:00:05Z 写入 1 漏洞 / 1 location /
  1 review / **27 evidence** / 1 status；review 的 `reviewer` = `libexpat-32777-collector`，
  `independent_reviewer` = `round49-independent-reviewer`，`status = PASS`、`grade = A`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round49_2026-10-25.py`（守卫 decision / snapshot /
  repo / 别名引用与 grade A PASS 复核）把 `disc2_05ab8b8704bfc3d3ff934592` 改写为
  `confirmed_affected`，`checked_at = 2026-10-25T00:00:20Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round49_20261025T000010Z.jsonl`。
- **复核后更正**：复核员记录 3 条文档级分歧，采集侧用自己的 tokenizer 探针独立复算后按实测裁定
  （`runs/data_fixes/apply_post_review_corrections_round49_2026-10-25.py`，dry-run 后 `--apply`，
  写前备份）：① `XmlPrologTok` 对 PI 返回 `XML_TOK_XML_DECL`(12) 并前进 21 字节，零推进的
  `XML_TOK_INSTANCE_START`(29) 来自其后的 `<a`；② 4550 行属于 `entityValueInitProcessor`
  （`doProlog` 起于 4681），不是 `doProlog`；③ `f31adfd5` 的提交标题是
  “Merge pull request #1159 from libexpat/prepare-release”。只改
  `critical_operation.description`、`trace[0].function`、`trace[1].description` 与
  `fix_commits[f31adfd5].message`，**不动**判定、等级、候选决策与任何实测数值。记录见
  `POST_REVIEW_CORRECTIONS.md`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  163 vulnerabilities / 163 locations / **6369 evidence** / 163 reviews（A 86 / B 77）/
  **134 snapshot_vulnerability_status**；triage 2613 行 = 157 confirmed_affected /
  1322 confirmed_not_affected / 532 possible_affected / 574 unknown / 28 duplicate。
  `plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 157 / P1_VERIFY 532 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 532 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 38` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2026-32778 入库（libexpat R_2_6_2，round50，grade A）

- **候选与快照**：`disc2_ba665e8bf908752125013d03`（`possible_affected`，
  `review_method = trusted_range_with_branch`）→ 快照 `snap_67132f0363b8bc23` =
  `R_2_6_2`（annotated tag object `2628777302…` peel 到 `fa75b965…`）。
- **问题**：`setContext` 先用 `lookup()` 把 PREFIX 挂进 `dtd->prefixes`（`lookup` 在 7255 行
  `table->v[i]->name = name`），再用 `poolCopyString` 复制名字；2.6.2 的 6794 行
  `prefix->name = poolCopyString(&dtd->pool, prefix->name);` 在 OOM 时把 NULL 写进已入表的条目，
  6796 行返回 `XML_FALSE`，parser 停在 `XML_INITIALIZED`。应用清掉分配失败后在同一 parser 上重试，
  `startParsing`(1050) → `setContext` → `lookup`(7195) 用 `keyeq`(7139-7144) 读那一格的 NULL 名字即崩
  （CWE-476，NVD Primary 5.5 MEDIUM；NVD Secondary 与 OSV 2.9 LOW）。
- **修复**：`576b61e4`（35 增 8 删，新增 `poolCopyStringNoFinish` 并把名字复制提前到 `lookup` 之前）+
  `d5fa769b`（27 行回归测试 `test_nsalloc_setContext_zombie`）+ `dbd511a2`（Changes）+
  `6154446f`（merge PR #1163），首个 release `R_2_7_5`（`f31adfd5…`）；`R_2_7_4`（`f5c2890d…`）
  仍是修复前最后一个 release。
- **卷宗**：`runs/verification/libexpat_R_2_6_2_CVE-2026-32778/`，19 件 sha256 钉住来源、
  `dossier.json` 19 条证据 / 9 个字段映射；`precheck_rows_32778.py` 输出 `problems: []`。
- **采集侧复现**：`repro/harness_32778.c` 只用公开 API（`XML_ParserCreate_MM` + 空格分隔符，
  计数分配器），mode 1 遍历预算 0..29 并在失败后同一 parser 重试，mode 4 只取 i = 3；
  2.6.2 与 2.7.4 的 ASan 构建 134、`-O2` 构建 139，2.7.5 全 0（`ok_at_i=11`）。24 个用例全 PASS
  （`failures=0`），崩溃栈 `keyeq:7140 ← lookup:7195 ← setContext:6789 ← startParsing:1050 ←
  XML_Parse:1938`。
- **独立复核**：`runs/independent/libexpat_R_2_6_2_CVE-2026-32778_round50/`，
  `reviewer_identity = round50-independent-reviewer-luchitong`，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九项 `fields_verified` 全 true，`location` 6794 与卷宗
  `critical_operation` 重叠；`reviewed_at = 2026-10-25T00:03:27Z`。复核者全新 clone
  （HEAD `b8fedbbf…`）并在 `/tmp/indep32778_r50/clone` 之外另建构建树，自写 harness：
  2.6.2 ASan budget 3 `SEGV on unknown address 0x0`（exit 1）、`-O2` exit 139（gdb 帧
  `lookup(... name="xml" ...) at xmlparse.c:7195`），2.7.4 同样崩，2.7.5 在 budget 0..40 全
  exit 0 且 budget 3 的 OOM 落在 `poolCopyStringNoFinish`；对照（不注入失败）两版两构建全 exit 0。
- **门禁**：`check_verdict_packet.py` → 23 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-25T00:04:26Z 写入 1 漏洞 / 1 location /
  1 review / **28 evidence** / 1 status；review 的 `reviewer` = `libexpat-32778-collector`，
  `independent_reviewer` = `round50-independent-reviewer-luchitong`，`status = PASS`、`grade = A`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round50_2026-10-25.py`（守卫 decision / snapshot /
  repo / 别名引用与 grade A PASS 复核，dry-run 先跑 `problems: []`）把 `disc2_ba665e8bf908752125013d03`
  改写为 `confirmed_affected`，`checked_at = 2026-10-25T00:04:40Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round50_20261025T000430Z.jsonl`。
- **复核备注（未触发更正）**：NVD 记录的 `vulnStatus` 是 “Modified” 而非 dossier 的
  `advisory_status: "reviewed"`（不属于九字段，不改）；回归测试行号差 2 行（1510 vs 1512，
  引用口径不同）；OSV 引用的 PR #1159 未单独取证，只作说明。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  164 vulnerabilities / 164 locations / **6397 evidence** / 164 reviews（A 87 / B 77）/
  **135 snapshot_vulnerability_status**；triage 2613 行 = 158 confirmed_affected /
  1322 confirmed_not_affected / 531 possible_affected / 574 unknown / 28 duplicate。
  `plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 158 / P1_VERIFY 531 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13）；`runs/possible_review_queue_2026-10-25/`
  重跑为 531 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 37` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2024-50602 入库（libexpat R_2_6_2，round51，grade A）

- **候选 / 快照**：`disc2_c7e893eeab17d88e1fe6f972`（卷宗署名）与 `disc2_c31db55b4823ecb00d28068d`
  （`related_candidate_ids`），同库同快照同公告，两者都是 `possible_affected`、`trusted_range_with_branch`；
  快照 `snap_67132f0363b8bc23` = libexpat `R_2_6_2`（annotated tag object
  `2628777302c195dd489baaa76fc2a7f048fe0aa7`），commit `fa75b96546c069d17b8f80d91e0f4ef0cde3790d`。
- **机制**：2.6.4 之前的 `XML_StopParser`（2.6.2 的 2226 行）在 `switch` 里只有 `XML_SUSPENDED`
  与 `XML_FINISHED` 两个 case，未启动（`XML_INITIALIZED`）的 parser 落进 2240 行 `default:`，
  2248 行被设为 `XML_SUSPENDED` 并返回 `XML_STATUS_OK`。随后 `XML_ResumeParser`（2256）只检查
  「不是 `XML_SUSPENDED` 就报错」，于是放行、2265 行改回 `XML_PARSING`、2267 行跑 `callProcessor`；
  当它返回 `XML_ERROR_NONE` 时跳过 2270-2273 的失败分支，2289 行
  `XmlUpdatePosition(parser->m_encoding, parser->m_positionPtr, …)` 便以 `m_positionPtr == NULL`
  （`XML_GetBuffer` 新建缓冲分支 2220 行置 NULL，从未推进）调用 → `initUpdatePosition`
  （`xmltok.c:1031`）→ `normal_updatePosition` 在 `xmltok_impl.c:1781` 以 `BYTE_TYPE(enc, ptr)`
  读零页。CWE-754（NVD 唯一弱点条目）；NVD **只有 Secondary** 5.9 MEDIUM
  `AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`（`134c704f-9b21-4f2e-91b3-4a467353bcc0`，CISA-ADP），
  OSV 同向量；上游 Changes 条目另写 `CWE-476 CWE-754`。
- **修复**：`51c70190`（新增 `case XML_INITIALIZED:` → `XML_ERROR_NOT_STARTED` 与错误串
  “parser not started”，9 增 1 删）+ `5fb89e7b`（`default:` 收窄为 `case XML_PARSING:`，其余
  `default: assert(0);`，4 增 1 删）+ `b3836ff5`（24 行回归测试 `test_misc_resumeparser_not_crashing`、
  `test_misc_stopparser_rejects_unstarted_parser`）+ `ef485e96`（merge PR #915，
  `2024-10-28T14:14:02Z`），首个 release `R_2_6_4`（tag object `2d994d11…` → `2691aff4…`，
  2024-11-07）；`R_2_6_3`（`88b3ed55…`）仍在范围内。2.6.4 的 `XML_ResumeParser` 主体没有改。
- **卷宗**：`runs/verification/libexpat_R_2_6_2_CVE-2024-50602/`，26 件 sha256 钉住来源
  （0 mismatch）、`dossier.json` 26 条证据 / 9 个字段映射；`precheck_rows_50602.py` 输出
  `problems: []`，九项 canonical 字段全部有 PASS 证据（合成 30 条证据行）。
- **采集侧复现**：`repro/harness_50602.c` 只用公开 API 复刻上游测试形状
  （`XML_ParserCreate_MM(NULL, &suite, NULL)` → `XML_GetBuffer(parser, 1)` →
  `XML_StopParser(parser, XML_TRUE)` → `XML_ResumeParser(parser)`），私有 memory suite 可把
  新鲜分配填成指定字节。36 个主用例 + 3 个 `malloc_fill_byte=0` 补充运行，`failures=0`：
  2.6.2/2.6.3 在 `fill=0` 下 ASan 134、`-O2` 139，栈
  `normal_updatePosition:1781 ← initUpdatePosition:1031 ← XML_ResumeParser`（2.6.2:2289 /
  2.6.3:2296），`fill=0xbe` 返 `resume_error=3`、2.6.4 打印 `stop_error=44` / `resume_error=34`。
  限定已写进 `repro/RESULTS.md`：崩溃受从未初始化的 `m_parsingStatus.finalBuffer` 门控。
- **独立复核**：`runs/independent/libexpat_R_2_6_2_CVE-2024-50602_round51/`，
  `reviewer_identity = round51-independent-reviewer-luchitong`，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九项 `fields_verified` 全 true，`location` 2226-2252 /
  `line_of_interest = 2240` 与卷宗 `critical_operation` 重叠；`reviewed_at = 2026-10-25T00:19:37Z`。
  复核者全新 clone（HEAD `b8fedbbf…`）并自建 `R_2_6_2`/`R_2_6_3`/`R_2_6_4` 的 ASan+UBSan 与
  `-O2` 六棵构建树，自写 harness：2.6.2/2.6.3 在 fill=0 下 134/139，默认与 fill=0xbe 全 0，
  2.6.4 全 0；三个 tag 的 annotated tag 与五个 fix 提交的祖先矩阵、OSV/NVD/PR #915 重取
  （PR 逐字节相同，OSV 仅键序不同，NVD 仅 `timestamp` 不同）均自行复核。复核员未读未跑采集侧
  `repro/`。其对 `finalBuffer` 的结论与采集侧一致：不主张「每次必崩」，`confirmed_affected` 不变。
- **门禁**：`check_verdict_packet.py` → 78 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-25T00:20:28Z 写入 1 漏洞 / 1 location /
  1 review / **29 evidence** / 1 status；review 的 `reviewer` = `libexpat-50602-collector`，
  `independent_reviewer` = `round51-independent-reviewer-luchitong`，`status = PASS`、`grade = A`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round51_2026-10-25.py`（守卫 decision /
  snapshot / repo / 别名引用与 grade A PASS 复核，dry-run 先跑 `problems: []`）把两条候选都改写为
  `confirmed_affected`，`checked_at = 2026-10-25T00:19:37Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round51_20261025T002031Z.jsonl`。
- **复核备注（未触发更正）**：卷宗引用的 PR #915 标题在实测记录里带反引号
  （``Stop `XML_ResumeParser` from crashing``），卷宗按不带反引号的摘要表述；NVD source
  `134c704f-…` 卷宗写作 “CISA-ADP”，复核员只按 UUID 记录、未独立解析机构名。
  两条都不属于九字段，不改动任何数据行。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  165 vulnerabilities / 165 locations / **6426 evidence** / 165 reviews（A 88 / B 77）/
  **136 snapshot_vulnerability_status**；triage 2613 行 = 160 confirmed_affected /
  1322 confirmed_not_affected / 529 possible_affected / 574 unknown / 28 duplicate。
  `plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 160 / P1_VERIFY 529 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13，共 2626）；`runs/possible_review_queue_2026-10-25/`
  重跑为 529 行（`range_precise 361` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 35` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## 2026-10-25 — CVE-2024-30260 入库（nodejs/undici v5.19.0，round52，grade A）

- **候选 / 快照**：`disc2_e609b9ad4151019e790a2bea`（`possible_affected`、
  `review_method = trusted_range_with_branch`），快照 `snap_24c4a191fd049fc3` = nodejs/undici
  `v5.19.0`（**lightweight tag** → `f5c89e5c87c7d702996b152c4ad86302b60c4181`，
  `Bumped v5.19.0`，2023-02-13）。快照语言构成 JavaScript 69.41% / C 17.12% / Markdown 4.31%，
  591 个 tracked 文件。
- **机制**：`lib/handler/RedirectHandler.js` 的 `shouldRemoveHeader`（186-193）对未知 origin 只剥
  `host`、`content-*`（仅 303）、`authorization`（长度 13）与 `cookie`（长度 6）；
  `proxy-authorization` 长度 19，没有对应分支，`cleanRequestHeaders` 因此保留它。
  `index.js:93` 把 `url.origin` 写进 `opts.origin`；`lib/interceptor/redirectInterceptor.js:14`
  在 `maxRedirections` 非 0 时构造 RedirectHandler；`onHeaders` 108 行以
  `this.opts.origin !== origin` 作为 unknownOrigin，109-110 行把 `opts.path` / `opts.origin`
  改到重定向目标，`onComplete` 160 行用同一份 opts 重新 dispatch，代理凭据随请求到达新 origin。
  CWE-863（NVD Primary；NVD Secondary CWE-285，GHSA API 只列 CWE-200，OSV 列 CWE-200/285/863），
  CVSS 3.1 4.3 MEDIUM `AV:N/AC:L/PR:H/UI:R/S:U/C:L/I:L/A:L`（NVD Primary；GitHub 与 NVD Secondary
  为 3.9 LOW / AC:H）。
- **修复**：`64e3402d`（v5.x 分支，「Merge pull request from GHSA-m4v8-wqvr-p9f7」，4 文件 +191/−6：
  `RedirectHandler.js` +11/−6 增加长度 19 分支、新增 `lib/core/constants.js` +118 与
  `lib/core/util.js` 的 `headerNameToString` +11、回归测试 +51），首个 release `v5.28.4`
  （`fb983069…`，2024-04-02）；`v5.28.3`（`e71cb4c8…`）的 `shouldRemoveHeader` 与 v5.19.0
  逐字节相同，仍在影响范围内。公告只点名的 `68057466` 是 main 分支同款修改
  （`lib/handler/redirect-handler.js` +2/−2），只进 `v6.11.1`（`6df3c738…`）。
- **卷宗**：`runs/verification/undici_v5.19.0_CVE-2024-30260/`，28 件 sha256 钉住来源
  （116,762 B，0 mismatch）、`dossier.json` 23 条证据 / 9 个字段映射 + 1 条快照语言证据；
  `precheck_rows_30260.py` 输出 `problems: []`，九项 canonical 字段全部有 PASS 证据
  （合成 40 条证据行）。
- **采集侧复现**：`repro/harness_30260.js` 只用公开 API（`undici.request`）+ 两个 loopback
  `node:http` 服务器，`run_repro.sh` 在 v5.19.0 / v5.28.3 / v5.28.4 上跑 5 种 mode 共 15 个用例，
  `failures=0`：v5.19.0 与 v5.28.3 的跨 origin 目标只收到 `proxy-authorization`（对象与扁平数组
  两种 header 形态都泄漏），v5.28.4 收到空集；same-origin 保留、direct 三者都到、
  `maxRedirections: 0` 时目标从未被联系，三个对照在三版上一致。环境 Node v24.16.0 / npm 11.13.0。
- **独立复核**：`runs/independent/undici_v5.19.0_CVE-2024-30260_round52/`，
  `reviewer_identity = round52-independent-reviewer-luchitong`，`verdict = confirmed_affected`，
  `grade_recommendation = A`，九项 `fields_verified` 全 true，`location` 186-193 /
  `line_of_interest = 190` 与卷宗 `critical_operation` 重叠；`reviewed_at = 2026-10-25T00:34:51Z`。
  复核者全新 clone（HEAD `046bb4c6…`）自建三棵 tag 树、自写 `probe_redirect_header.js` 与
  `run_matrix.sh` 跑 15 行用例（结果与采集侧一致），独立确认四个 tag 的 tag 类型与 commit、
  两个修复提交的祖先矩阵（`64e3402d` 是 `v5.28.3..v5.28.4` 之间唯一改 `RedirectHandler.js` 的提交），
  并独立判定 GHSA `vulnerable_version_range "< 5.28.3"` 与其 `patched_versions ">= 5.28.4"`、
  OSV/NVD 机器范围及 v5.28.3 实测矛盾，属公告 off-by-one 文本错误（不影响 v5.19.0 的包含关系）。
  复核员未读未跑采集侧 `repro/`。
- **复核后保真更正**（复核员指出、采集侧重算后修正，均不涉及判定字段）：
  1. `collect_sources_30260.py` 原用 `subprocess(text=True)` 再 `.encode()`，把上游本为 CRLF 的
     `test/redirect-cross-origin-header.js` 归一化为 LF；改为二进制读取后该文件 1,273 B、
     51 个 CRLF、sha256 `4358fb46…`，`git hash-object` 等于上游 blob `8313e00c…`；MANIFEST 与
     证据 sha 随之更新，构建脚本增加「不再是 51 个 CRLF 就拒绝」的断言。
  2. `retrieved_at` / `prepared_at` 原写 `2026-10-25T09:10:00Z`（本地 +0800 误标 UTC），改为取
     NVD 响应的 `timestamp`（现为 `2026-10-25T00:36:00Z`）；快照证据用
     `runs/language/snap_24c4a191fd049fc3/snapshot_proposal.json` 的 `collected_at`。
  3. CWE 出处补全：`cwe_ids` 仍为 NVD Primary 的 CWE-863，证据增加 GHSA API 的 CWE-200 与
     OSV 的 CWE-200/285/863，limitations 写明四处出处差异。
  复核员随后按更正后的来源重测并追加 Addendum（`NOTES.md` 20,058 B / sha256 `6178018b…`、
  `verdict.json` 15,388 B / `8dfe63b3…`，只改三条 caveat 文案与三条 discrepancy 状态：
  `verdict` / `grade_recommendation` / `fields_verified` / `location` / `reviewed_at` 未变；
  `preserved_sha256.txt` 重算 27 条）。重跑 `check_verdict_packet.py` 仍
  `problems: []` / `warnings: []` / `ok: true`。
- **门禁**：`check_verdict_packet.py` → 27 个 preserved 文件、`problems: []`、`warnings: []`、
  `ok: true`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-25T00:36:51Z 写入 1 漏洞 / 1 location /
  1 review / **41 evidence** / 1 status；review 的 `reviewer` = `undici-30260-collector`，
  `independent_reviewer` = `round52-independent-reviewer-luchitong`，`status = PASS`、`grade = A`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round52_2026-10-25.py`（守卫 decision /
  snapshot / repo / 别名引用与 grade A PASS 复核，dry-run 先跑 `problems: []`）把
  `disc2_e609b9ad4151019e790a2bea` 改写为 `confirmed_affected`，
  `checked_at = 2026-10-25T00:36:51Z`；backup
  `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round52_20261025T003654Z.jsonl`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  166 vulnerabilities / 166 locations / **6467 evidence** / 166 reviews（A 89 / B 77）/
  **137 snapshot_vulnerability_status**；triage 2613 行 = 161 confirmed_affected /
  1322 confirmed_not_affected / 528 possible_affected / 574 unknown / 28 duplicate。
  `plan_snapshot_queue.py` 落盘 `v031/reports/queue_P3.json`（DONE 161 / P1_VERIFY 528 /
  P1_REVIEW 574 / ARCHIVE 1350 / P0_SELECT_SNAPSHOT 13，共 2626）；`runs/possible_review_queue_2026-10-25/`
  重跑为 528 行（`range_precise 360` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 35` /
  `legacy_triage 30`）。HANDOFF / LIMITATIONS_V031 / CANDIDATE_FUNNEL / 队列 README 已同步。
- **未做的事**：未动 41990/45230/56374；未重生成 `CHECKSUMS.sha256`；未声明数据集完成、
  `PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected` 仍不代表快照漏洞已穷尽。

## Round 53 — nodejs/undici v5.19.0 / CVE-2024-24758（fetch 跨 origin 重定向泄漏 Proxy-Authorization）

- **对象**：仓库 `nodejs/undici`，快照 `snap_24c4a191fd049fc3`（`tag_or_release = v5.19.0`，
  lightweight tag → `f5c89e5c87c7d702996b152c4ad86302b60c4181`），候选
  `disc2_7bebf1081c3f0249b6759951`（`possible_affected`，`trusted_range_with_branch`，
  命中 OSV GHSA-3787-6prv-h9w3 的 `introduced 0 → fixed 5.28.3` / `6.0.0 → 6.6.1`）。
- **采集**：`runs/verification/undici_v5.19.0_CVE-2024-24758/collect_sources_24758.py` 钉住 **25 个文件 /
  300,348 B**（OSV GHSA+CVE、NVD、GHSA API、v5.28.3/v6.6.1 release、两个 fix commit API、三个 tag 的
  `lib/fetch/index.js`、v5.19.0 `headers.js`、v5.28.3/v6.6.1 回归测试、两个 `package.json`、6 段带断言的
  代码切片、2 个补丁、`git_facts.txt`），`mismatches: []`；`git cat-file -t` 确认五个 tag 都是 lightweight。
- **机制**：`lib/fetch/index.js` 的 `httpRedirectFetch` 在 v5.19.0 的 **1204-1207** 行跨 origin 分支只
  `delete('authorization')`（1206），没有 `proxy-authorization`；1092 行走 `await httpRedirectFetch(...)`，
  1231 行 `request.urlList.push(locationURL)`、1239 行 `mainFetch(fetchParams, true)` 用同一份 header list
  重发。v5.28.2（最后一个受影响 release）删了 authorization/cookie/host 但没有 proxy-authorization，
  v5.28.3 在 1206-1207 插入 `delete('proxy-authorization', true)`；v5 的 `HeadersList.delete` 只收一个
  参数，多写的 `true` 被忽略、删除照常生效。
- **修复提交**：v5 线 `d3aa574b1259c1d8d329a0f0f495ee82882b1458`（父提交即 v5.28.2 的 `9a14e5f3…`，
  只进 v5.28.3）、6.x 线 `b9da3e40f1f096a06b4caedbb27c2568730434ef`（只进 v6.6.1）；两者都是
  `lib/fetch/index.js` +3/−0、`test/fetch/redirect-cross-origin-header.js` +4/−2（stats 9 / +7 / −2），
  hunk 行号不同（v5 `@@ -1203,6 +1203,9 @@` / main `@@ -1326,6 +1326,9 @@`）。
- **卷宗**：`dossier.json` 25 条证据 / 9 个字段映射 + 1 条快照语言证据；`precheck_rows_24758.py`
  → `problems: []`，rows = 1 vulnerability / 1 location / 52 evidence / 1 status，九项 canonical 字段
  均有 PASS 证据。
- **采集侧复现**：`repro/run_matrix.sh` 在 v5.19.0 / v5.28.2 / v5.28.3 上跑 7 种 mode、21 个用例
  （`logs/results.tsv`）：v5.19.0 与 v5.28.2 的跨 origin 目标收到
  `{"authorization": null, "proxyAuthorization": "proxy-secret"}`，v5.28.3 收不到；same-origin 三版保留、
  `cross-origin-noheader` 负控制无头、`direct`/`manual` 证明目标从未被联系。`cookie` 模式是邻居公告
  GHSA-wqq4-5wpv-mx2g（`e041de35`）的控制组，v5.19.0 泄漏、v5.28.2 起不泄漏，不计入本 CVE。
- **隔离复核**（`round53-independent-reviewer-luchitong`，reviewed_at `2026-10-25T00:50:25Z`）：
  只读 `dossier.json` 与 `sources/**`，自建 clone 与解压树、自写 12 行用例；**grade A / confirmed_affected**，
  红行实测目标收到 `Proxy-Authorization: Basic UFJPWFktU0VDUkVULXJvdW5kNTM=`，v5.28.3 三头全空；
  五处记为可接受（CWE 出处、4.5 vs 3.9、`vulnerable_commit_basis` 措辞、cookie/host 邻居范围、行号），
  无硬错误。
- **门禁**：`check_verdict_packet.py` → 34 个 preserved 文件、`problems: []`、`warnings: []`、`ok: true`。
- **入库**：`promote_verified_rows.py --apply` 于 2026-10-25T00:51:59Z 写入 1 漏洞 / 1 location / 1 review /
  **51 evidence** / 1 status；`independent_reviewer = round53-independent-reviewer-luchitong`，
  `status = PASS`、`grade = A`。
- **triage**：`runs/data_fixes/apply_promoted_candidate_round53_2026-10-25.py`（同样守卫 decision / snapshot /
  repo / 别名引用与 grade-A PASS 复核，dry-run 先跑 `problems: []`）把
  `disc2_7bebf1081c3f0249b6759951` 改写为 `confirmed_affected`，`checked_at = 2026-10-25T00:52:30Z`；
  backup `runs/data_fixes/snapshot_candidate_triage_before_promoted_rows_round53_20261025T005203Z.jsonl`。
- **校验与计数**：`validate_dataset.py . --draft` → `STRUCTURAL VALIDATION PASSED`。九张主表现为
  **167 vulnerabilities / 167 locations / 6518 evidence / 167 reviews（A 90 / B 77）/
  138 snapshot_vulnerability_status**；triage 2613 行 = 162 confirmed_affected / 1322 confirmed_not_affected /
  527 possible_affected / 574 unknown / 28 duplicate。`plan_snapshot_queue.py` 落盘
  `v031/reports/queue_P3.json`（DONE 162 / P1_VERIFY 527 / P1_REVIEW 574 / ARCHIVE 1350 /
  P0_SELECT_SNAPSHOT 13，共 2626）；`runs/possible_review_queue_2026-10-25/` 重跑为 527 行
  （`range_precise 359` / `range_coarse 80` / `nvd_cpe 23` / `alias_osv 35` / `legacy_triage 30`）。
  HANDOFF / LIMITATIONS_V031 / CANDIDATE_FUNNEL / 队列 README 已同步。
- **本轮另做的失败排查（不作为正样本）**：django 4.2.13 上的 CVE-2024-45230 候选
  （`disc2_91b14048e4ec3e3a627057a1`）经代码与实测判定**不能**在该 SHA 复现：`urlize` 的
  `trim_punctuation` 分号/实体分支（`rstripped = middle.rstrip(";")`）是 4.2.14 由 CVE-2024-38875 的修复
  引入的，4.2.13 里不存在；实测 `"&" + ";:" * n` 在 4.2.13 与 4.2.16 上线性（n=40000→80000：
  0.0011→0.0020 s / 0.0015→0.0025 s），只有 4.2.15 二次（0.4983→2.0096 s）；4.2.13 的二次输入是
  括号嵌套（属已入库的 CVE-2024-38875）。该候选**保留为 `possible_affected`，未改写**，待专门复核；
  不据此宣称 45230 在 4.2.13 不存在。
- **未做的事**：未动 41990/45230/56374 的判定（本轮没有把它们升为 `confirmed_affected`）；未重生成
  `CHECKSUMS.sha256`；未声明数据集完成、`PASS_KNOWN_SWEEP` 或 release；`unknown`/`possible_affected`
  仍不代表快照漏洞已穷尽。
