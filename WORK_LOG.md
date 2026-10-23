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
