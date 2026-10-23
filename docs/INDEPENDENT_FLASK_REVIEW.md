# Flask 独立盲审（截至 2026-10-21）

审核者：`/root/independent_flask_review`。审核开始时仅阅读本项目 `WORKFLOW.md`、`schemas/reviews.schema.json`、`schemas/vulnerabilities.schema.json`；未阅读采集者的 Flask 结论、pilot 作业、构建脚本或已采集响应。以下原始资料由本审核者重新向上游/CVE 原始记录获取，原样响应保存在 `runs/independent/flask_CVE-2023-30861/`。没有执行 Flask、官方测试或 PoC。

## CVE-2023-30861 / GHSA-m2qf-hxjv-5gpq

**技术证据达到 B 级；本文件不是正式 reviews PASS。** 上游回归测试、修复 diff、脆弱源码、CNA 元数据、正式发行和分支可达性相互吻合。全快照固定版本 Linguist 语言盘点以及两位审查者的正式关联尚未在本次独立审核中完成，故没有写入正式表，也没有虚填 `languages_verified=true`。

| 字段 | 独立核验结果 |
| --- | --- |
| 上游与包 | pallets/flask；PyPI Flask |
| 脆弱正式 tag | 2.3.1 = `721abdc3810057269503a72d2db80fb826f3c85c` |
| 另一脆弱发行分支 | 2.2.4 = `74e03298200e33951ca350a35aa3a8c0b4ff8177` |
| 2.3 代码补丁 / 合并 | `8705dd39c4fa563ea0fe0bf84c85da8fcc98b88d` / `70f906c51ce49c485f1d355703e9cc3386b1cc2b` |
| 2.2 回移补丁 / 合并 | `8646edca6f47e2cd57464081b3911218d4734f8d` / `afd63b16170b7c047f5758eb910c416511e9c965` |
| 首次修复正式发行 | 2.3.x 线：2.3.2，tag SHA `f3b8f570545200c87465d18386f3fc9f2258307a`；2.2.x 线：2.2.5，tag SHA `47af817c8fe01045c641b97f8fb784c7ad864eee` |
| 严重程度 | CNA：CVSS 3.1，7.5 high，`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| CWE | CNA：CWE-539；上游 GHSA 页面没有 CWE，不应把空值覆盖 CNA |
| 受影响范围 | CNA：`<2.2.5 || >=2.3.0,<2.3.2`；具体确认 2.3.1 和 2.2.4 |

主要根因在脆弱快照 [sessions.py 第 347 行起](https://github.com/pallets/flask/blob/721abdc3810057269503a72d2db80fb826f3c85c/src/flask/sessions.py#L347)：写 Vary 的判断先检查 accessed，而后才调用 [should_set_cookie 第 245 行](https://github.com/pallets/flask/blob/721abdc3810057269503a72d2db80fb826f3c85c/src/flask/sessions.py#L245)。永久会话在应用未读取或修改会话时仍可因默认刷新配置进入 [set_cookie 第 356 行](https://github.com/pallets/flask/blob/721abdc3810057269503a72d2db80fb826f3c85c/src/flask/sessions.py#L356)。访问 permanent 时可能通过 get 将 accessed 置真，但此时已经越过 Vary 判断。响应因此刷新会话 Cookie 而缺少相应缓存区分。修复在写/删 Cookie 时明确添加 Vary，并将访问检查移到空会话提前返回之前；这覆盖了刷新及清空等路径。

[官方修复与回归](https://github.com/pallets/flask/commit/70f906c51ce49c485f1d355703e9cc3386b1cc2b)新增 `tests/test_basic.py::test_session_refresh_vary`：[第 547 行](https://github.com/pallets/flask/blob/70f906c51ce49c485f1d355703e9cc3386b1cc2b/tests/test_basic.py#L547)先建立永久会话，再请求完全不访问会话的路由，断言两次响应均带 Cookie 的 Vary。这是与公告触发条件直接对应的官方回归；本审核只阅读它，**没有运行红绿测试**。潜在跨客户泄漏还取决于缓存代理处理 Cookie 的方式，以及应用未将响应标私有/不可缓存等部署条件，不能把所有 Flask 应用都标为可实际利用。

分支闭环由 [2.3 修复至发行比较](https://github.com/pallets/flask/compare/70f906c51ce49c485f1d355703e9cc3386b1cc2b...2.3.2)和 [2.2 回移至发行比较](https://github.com/pallets/flask/compare/afd63b16170b7c047f5758eb910c416511e9c965...2.2.5)证实：各比较的 merge-base 等于对应修复合并 SHA，behind_by 为 0，发行代码未回滚 sessions.py。两个正式 release 都非 draft、非 prerelease，并明确对应 [2.3.2](https://github.com/pallets/flask/releases/tag/2.3.2)与 [2.2.5](https://github.com/pallets/flask/releases/tag/2.2.5)安全修复线。

**来源冲突必须保留。** 获取时[上游 GHSA](https://github.com/pallets/flask/security/advisories/GHSA-m2qf-hxjv-5gpq) affected 文本为 `<2.3.1`，这与其修复版本 2.3.2、自身正文及 [CVE CNA 原始记录](https://github.com/CVEProject/cvelistV5/blob/main/cves/2023/30xxx/CVE-2023-30861.json)不一致。[2.3.1→2.3.2 官方 diff](https://github.com/pallets/flask/compare/2.3.1...2.3.2)和独立读取的 2.3.1 源码证明 2.3.1 包含根因；应使用明确分支范围，不能复制错误上界。2.3.2 当时 CHANGES.rst 还把发行年写成 2022；正式 release published_at 为 2023-05-01，当前上游 changelog 已改正。本审核以正式 release/CNA 时间为准。

## 其他公开历史候选的独立初审

这些条目由本次独立读取官方安全页、全历史 CHANGES 和 CVE 原始记录发现，并非从采集者清单挑选。官方安全页当前列出三条仓库公告，但仅此页面不覆盖更早历史。

| 候选 | 独立证据和判断 | 未闭合事项 |
| --- | --- | --- |
| [CVE-2025-47278 / GHSA-4grg-w6v8-c28g](https://github.com/pallets/flask/security/advisories/GHSA-4grg-w6v8-c28g) | 技术 B。仅 3.1.0；脆弱 SHA `ab8149664182b662453a563161aa89013c806dc9`，sessions.py 321–327 先放主密钥再扩展 fallback，导致最后 fallback 被签名使用。修复 `73d6504063bfa00666a92b07a28aaf906c532f09` 将主密钥追加至末尾；官方 `test_session_secret_key_fallbacks` 修改能揭示旧行为。正式 3.1.1 SHA `7fff56f5172c48b6f3aedf17ee14ef5c2533dfd1` 包含修复。CNA CVSS 4.0 1.8 low；CWE-683。 | 未执行测试；语言盘点和第二审核者正式绑定待补。 |
| [CVE-2026-27205 / GHSA-68rp-wp8r-4726](https://github.com/pallets/flask/security/advisories/GHSA-68rp-wp8r-4726) | 上游/CNA、根因、修复、正式发行已证实。3.1.2 脆弱 SHA `2c1b30d0503cfb064f1cb252e6614a06915a362a`：sessions.py 68–94 仅部分值读取方法跟踪 accessed，ctx.py 327 是普通 session 属性；in/len 仅查看键时漏标。修复 `089cb86dd22bff589a4eafb7ab8e42dc357623b4` 在上下文 session 属性访问时跟踪，3.1.3 SHA `22d924701a6ae2e4cd01e9a15bbaf3946094af65` 可达。CNA CVSS 4.0 2.3 low；CWE-524。 | 官方补丁更新 test_session_accessed，但完整测试文件未见 in/len 直接回归断言；不能把新私有属性导致旧版测试报错称为有效触发红绿。本审核暂不授完整 B，待补可信触发回归。 |
| [CVE-2018-1000656 / GHSA-562c-5r94-xh97](https://github.com/advisories/GHSA-562c-5r94-xh97) | [0.12.3 官方安全发行](https://github.com/pallets/flask/releases/tag/0.12.3)和 [PR2691](https://github.com/pallets/flask/pull/2691)明确收紧请求 JSON 编码，避免 Python 非文本编码造成异常内存使用。脆弱 0.12.2 SHA `571334df8e26333f34873a3dcb84441946e6c64c` 的 wrappers.py 151–157 将客户端 charset 传给 json.loads，json.py 145 使用它 decode。主线修复合并 `465b48ed4e4af52493df1febe4687f53032a5e0a`；0.12 回移合并 `b178e89e4456e777b1a7ac6d7199052d0dfdbbbe`，0.12.3 SHA `1a9e58e8c97c47c969736d46410f724f4e834f54` 包含它。GHSA 当前 CVSS 4.0 8.7 high、CWE-20。 | 官方新增编码测试主要测试支持的 UTF；尚缺直接拒绝恶意 charset 的回归验证，不授完整 B。CNA 自身没有结构化 CVSS。 |
| [CVE-2019-1010083 / GHSA-5wv5-4vpf-pj6m](https://github.com/advisories/GHSA-5wv5-4vpf-pj6m) | CNA 引用 [1.0 官方公告](https://www.palletsprojects.com/blog/flask-1-0-released/)，描述与 2018 项相同；1.0/0.12.3 的正式发行正文描述同一 JSON 修复。两个 CNA 均明确提示可能重叠。 | 保留原候选与别名，不独立加计第二个已核实根因；需正式去重裁决，不能将 `<1.0` 错套到已修复的 0.12.3/0.12.4。 |
| Windows 文件越界读取，0.6.1 安全修复，无已核实编号 | [官方 CHANGES](https://github.com/pallets/flask/blob/main/CHANGES.rst)明确称 0.6.1 修复 Windows 下反斜杠逃逸目录导致任意文件下载；[官方比较](https://github.com/pallets/flask/compare/0.6...0.6.1)给出脆弱 0.6 SHA `5cadd9d34da46b909f91a5379d41b90f258d5998`、修复 `aeed530e3221c1b445c13269dcd2fb67548bcefc` 及 Windows 路径测试。 | pending_severity：未核实 CVE/CVSS；GitHub release 对象查询返回404。已定位脆弱 helpers.py 388–394；官方 tag/changelog 可用，发行来源仍需补强。应进入候选，不能丢弃或编造编号。 |
| 0.12.2 safe_join Windows 修复 | 官方 CHANGES 仅称 bug fix；独立查看 issue2033/PR2059 及0.12.1→0.12.2 diff，问题是Windows路径分隔符输出格式不符预期；补丁保留边界检查，改用posixpath连接。 | 未证实为安全漏洞；保留发现与不纳入正样本理由，不能仅按函数名标漏洞。 |

2023 永久会话刷新和 2026 仅访问键的缺陷共享缓存表现，但触发条件、根因与修复集不同，不应仅凭标题相近合并。

## 语言审核的独立准备与限制

独立 GitHub recursive tree 在 2.3.1 SHA 返回 `truncated=false`、249 个 blob；原始记录为 `ind_flask_round5_3.json`。按扩展名初查：Python 80、HTML 20、SQL 2、CSS 2、Shell 1、Batch 1、Makefile 1，另有 RST、YAML、TOML、JSON、配置、二进制图片等。**这不是固定 Linguist 的完整语言结论**，也没有将扩展名误当作嵌入语言识别。

正式语言审核须核对：完整 tracked tree 与每文件清单一一对应；SHA 和 blob 大小正确；固定 Linguist 9.7.0 及覆盖/忽略配置留档；Python/模板/SQL/Shell/Batch/Makefile 等低占比项均保留；HTML/RST 中嵌入 JavaScript/SQL/Shell 的方法与 `embedded_nonadditive` 字节口径明确；first_party/test/tooling/docs/generated/vendored/submodule 分类覆盖所有项，二进制保留且不伪计代码；汇总字节、文件数和分母可重算。仅通过扩展名盘点不足以填 `languages_verified=true`。

## 证据与失败留痕

目录中的原始 JSON 保留 connector 返回内容和错误。第一次读取 Flask 仓库 SECURITY.md、.github/SECURITY.md 均为 404；随后从组织共享仓库 pallets/.github 成功读取安全政策。2692 为 issue，误按 PR 获取返回 404，已保留，并使用成功读取的 issue 及实际回移 PR2695 对照，不把失败当成功。Web CVE 页面只提供 JavaScript 壳，因此使用 CVEProject/cvelistV5 原始 CNA 记录。GitHub Web 的 0.6 比较抓取失败，REST 比较随后成功。0.6.1 GitHub release 对象请求404，保留该失败而不否认已存在的官方tag/changelog。

本次形成独立初审，不宣称全量已知漏洞搜索完成；尚有历史去重、无编号安全修复和触发回归待决，覆盖状态为 NEEDS_REVIEW。没有访问任何外部目标实施利用，没有运行远端仓库指令，没有改正式表。

