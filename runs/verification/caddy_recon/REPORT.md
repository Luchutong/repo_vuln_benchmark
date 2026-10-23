# Caddy v2.11.4 已知正例复核报告

日期：2026-10-23。范围：只读侦察、源码核对与本地复现；`data/` 与 `v031/` 未被修改。
原始证据 37 个文件在 `sources/`。

## 1. 结论摘要

选定漏洞：**GHSA-8qx7-j2v2-x6q5 / CVE-2026-55458**（Hop-by-hop headers that leak through，CWE-444）。

- 受影响标签 `v2.11.4`：annotated tag 对象 `8ec11a4b7e39a5fd00da2fc5cb9b543e31fd7926`，peeled commit
  `e2eee6a7fce366321294c9c2a79f3146891dcbdf`，tree `89190a02601c918d8de199c16a9d7d778ba204fa`。
- 修复标签 `v2.11.5`：peeled commit `0a137e2fafc3c3fffcd2f27c8ef0a78913165902`。
- 修复提交 `25b3eab6dbd8d2d2670711f26b774e0fd43e1179`：`git merge-base --is-ancestor` 在 v2.11.4 中
  exit=1（不在），在 v2.11.5 中 exit=0（在），v2.11.6/v2.11.7 亦为 0。
- 本地复现：v2.11.4 的 101 响应泄漏 `Alt-Svc`、`Keep-Alive`、`Proxy-Authenticate` 及 Connection 点名头；
  v2.11.5 全部剥离并保留合法 upgrade 头。上游回归测试红/绿均完成。

**最重要的数据发现**：`data/snapshots.jsonl` 中唯一的 caddy 快照不在 v2.11.4，而是固定在 2026-10-21 的
main HEAD `f355b868…`，且已包含修复，因此不能作为本 advisory 的已知正例。

## 2. 数据快照核对

只读取了 `data/snapshots.jsonl`、`data/snapshot_exports.jsonl`、`data/snapshot_audit_exports.jsonl`：

- `snapshots.jsonl` 共 88 条，仅 1 条与 caddy 相关（第 31 行）。
- `snapshot_exports.jsonl`（26 条）与 `snapshot_audit_exports.jsonl`（26 条）无 caddy 记录。

关键字段（`sources/snapshot_record_caddy.json`）：

| 字段 | 值 |
|---|---|
| `snapshot_id` | `snap_5f7d6c5c600a7a23` |
| `repo_id` | `29207621` |
| `tag_or_release` | `None` |
| `vulnerable_commit` | `f355b8687d5582ea9fcc99f71598109d1e5b6ced` |
| `scan_details.git_tree_oid` | `2c52c53dec668480d0ca49f48919827aa67b6235` |
| `evaluation_target` | `False` |
| `purpose` | `historical_evidence` |
| `collected_at` | `2026-10-21T13:14:59.511648Z` |

核对结果（`sources/snapshot_comparison.txt`）：

- `repo_id 29207621` 经 `https://github.com/caddyserver/caddy` 的 meta
  `octolytics-dimension-repository_id` 确认为 `caddyserver/caddy`。
- 该记录 commit/tree 等于本次 clone 的 main HEAD（`f355b868` / `2c52c53d`），**不等于** v2.11.4 的
  `e2eee6a…` / `89190a02…`。
- `git merge-base --is-ancestor 25b3eab6 f355b868` → **exit 0**，修复已存在。

结论：现有快照是 main HEAD 的历史证据快照，对本漏洞而言是已修复状态。若需已知正例，必须新建钉住
`v2.11.4`（`e2eee6a…`，tree `89190a02…`）的快照。

## 3. 标签与提交事实

Clone：`https://github.com/caddyserver/caddy.git`（full clone，`.git` 约 23 MB），HEAD
`f355b8687d5582ea9fcc99f71598109d1e5b6ced`（2026-10-21）。

| tag | 类型 | tag 对象 | peeled commit | tree | go.mod `go` | tagger UTC |
|---|---|---|---|---|---|---|
| v2.11.4 | annotated | `8ec11a4b7e39a5fd00da2fc5cb9b543e31fd7926` | `e2eee6a7fce366321294c9c2a79f3146891dcbdf` | `89190a02601c918d8de199c16a9d7d778ba204fa` | 1.25.1 | 2026-06-03T03:54:40 |
| v2.11.5 | annotated | `91eb0e28cca1a765a7c066bcfca7c87c5168c836` | `0a137e2fafc3c3fffcd2f27c8ef0a78913165902` | `9f3557d4902c2aad65658b31a0b977b4dafc7942` | 1.26.0 | 2026-09-30T21:27:05 |
| v2.11.6 | annotated | `14571dec859484962a2c63c9820c297424d8c184` | `ac834b5dc70a17dca296f47c78c64587d6631cbb` | `1290d76367286ca5eafed88f549f3f186ada24d5` | 1.26.0 | 2026-09-30T22:22:43 |
| v2.11.7 | annotated | `87c43dc4f54861ec7e54302cfb2ad3e34508b6dc` | `72dd0fb067f6d7826c7f79907670ba4a713bfe37` | `733d77ae935d64209fac7398d4aeeb9a6fea840e` | — | 2026-10-03T05:25:14 |

- v2.11.4 commit date `2026-06-01 13:35:02 -0600`，subject
  `templates: Patch for GHSA-vcc4-2c75-vc9v (#7785)`；tag 类型确为 `tag`（annotated）。
- `go.mod`：`module github.com/caddyserver/caddy/v2`。
- v2.11.4→v2.11.5 共 119 个 commit；`git merge-base --is-ancestor v2.11.4 v2.11.5` → exit 0。
- `v2.11.*` 标签：`v2.11.0 v2.11.0-beta.1 v2.11.0-beta.2 v2.11.1 v2.11.2 v2.11.3 v2.11.4 v2.11.5
  v2.11.6 v2.11.7`，无 v2.11.4.x，v2.11.5 是 v2.11.4 后第一个稳定版。

## 4. Advisory 多源对照

### 4.1 GHSA-8qx7-j2v2-x6q5 / CVE-2026-55458（选定）

仓库级缓存（`github_rest_readonly`，`2026-10-21T13:24:00Z`）：

- summary `RFC 7230 §6.1 compliance issue / Hop-by-hop headers that leak through`；severity `low`；
  CWE `CWE-444`；CVSS `None`。
- published `2026-10-13T16:27:12Z`，updated `2026-10-13T16:27:13Z`，state `published`。
- identifiers `GHSA-8qx7-j2v2-x6q5`、`CVE-2026-55458`。
- vulnerable `<=v2.11.4`，patched `v2.11.5`，package `github.com/caddyserver/caddy/v2`。
- `references`：无（None）。

| 来源 | 结果 | 一致性 |
|---|---|---|
| GitHub 仓库 advisory HTML | 200；Affected `<=v2.11.4`；Patched `v2.11.5`；CWE-444；Low；CVE-2026-55458；无 References | 一致 |
| GitHub 全局 advisory | **404** | 未进入全局库 |
| OSV `GHSA-8qx7-j2v2-x6q5` | **404** `Vulnerability not found` | 未收录 |
| OSV `CVE-2026-55458` | **404** `Vulnerability not found` | 未收录 |
| NVD `CVE-2026-55458` | 200，`totalResults=0` | 无记录 |
| CVE.org `CVE-2026-55458` | **404** `CVE_RECORD_DNE` | 无记录 |
| GitHub REST API（未认证） | 403，`x-ratelimit-remaining: 0`，reset `1792698724` | 无法重拉，用缓存+HTML 交叉验证 |

要点：**CVE-2026-55458 仅存在于该仓库级 advisory**，NVD/CVE.org/OSV/GitHub 全局库均查不到；
advisory 无任何 references。

### 4.2 GHSA-6365-7ppr-5r92（未选）

- summary `Connection created for the wrong upstream for forward_auth + reverse_proxy`；severity `medium`；
  无 CWE/CVSS/CVE（页面 `No known CVE`）。
- published `2026-07-10T17:08:10Z`；Affected `< v2.11.5`；Patched `v.2.11.5`（原文带点，笔误）。
- 公开来源：仓库 HTML 200 且字段一致；全局 advisory 404；OSV 404；无 NVD/CVE.org 记录。
- 引入提交 `8aca108d2c9d9e9ff3a39ff00684ea58df1338f6`：在 v2.11.0/v2.11.1/v2.11.2/v2.11.3/v2.11.4
  中为祖先（exit 0），在 **v2.10.2 中不是**（exit 1）。因此 `< v2.11.5` 对 `<= 2.10.2` **过宽**，
  与报告人“降级 2.10.2 不受影响”一致。

### 4.3 选择理由

1. GHSA-8qx7 有确定性、无竞态的本地复现（raw-socket upstream + curl，一次请求即触发）。
2. 修复逻辑与回归测试可在源码级精确指认。
3. GHSA-6365 是竞态类问题，官方 PoC 需加 `time.Sleep(2ms)` 并跑 300 并发 30 秒，不适合确定性评估快照。

GHSA-6365 修复提交也已定位：`1830809afe8c95c6c554740f8719e023415f85cb`
（`reverseproxy: save dial info in a context key...` #7859，WeidiDeng，2026-07-10）；
在 v2.11.4 中 exit=1，v2.11.5 中 exit=0。

## 5. 修复提交与祖先关系

`25b3eab6dbd8d2d2670711f26b774e0fd43e1179`

- subject `Merge commit from fork`；author `Dionis Ramadani <d.ramadani@me.com>`（advisory 报告人，
  文中写明 "I'll add my fix to the branch"）。
- author date `2026-06-12 20:39:01 +0200`；commit date `2026-06-12 12:39:01 -0600`；
  parents `fcba554d…`（单父，安全修复自私有 fork 合入）。
- 提交正文：`fix(reverseproxy): hop-by-hop header fix`、
  `test(headers): Added unit tests for hop-by-hop header behavior`。
- 变更：`reverseproxy.go` +22 −6；新增 `hopheaders_test.go` 191 行。

祖先矩阵（0=是祖先）：

```
25b3eab6 in v2.11.3 -> 1
25b3eab6 in v2.11.4 -> 1
25b3eab6 in v2.11.5 -> 0
25b3eab6 in v2.11.6 -> 0
25b3eab6 in v2.11.7 -> 0
```

`git log -S'upgradeVal := res.Header.Get("Upgrade")' v2.11.4..v2.11.5` 与
`git log -- hopheaders_test.go` 都只命中 `25b3eab6`。

修复内容：v2.11.4 先判 101 并提前 return，再剥离：

```go
// v2.11.4 reverseproxy.go:1218-1230
if res.StatusCode == http.StatusSwitchingProtocols {
    var wg sync.WaitGroup
    h.handleUpgradeResponse(logger, &wg, rw, req, res)
    wg.Wait()
    return nil            // 在剥离之前返回
}
removeConnectionHeaders(res.Header)
for _, h := range hopHeaders {
    res.Header.Del(h)
}
```

v2.11.5 改为先剥离再判 101，并保存/恢复 upgrade 语义：

```go
upgradeVal := res.Header.Get("Upgrade")
removeConnectionHeaders(res.Header)
for _, h := range hopHeaders {
    res.Header.Del(h)
}
if res.StatusCode == http.StatusSwitchingProtocols && upgradeVal != "" {
    res.Header.Set("Upgrade", upgradeVal)
    res.Header.Set("Connection", "Upgrade")
}
```

## 6. 漏洞代码位置

受影响版本 `v2.11.4`：

1. `modules/caddyhttp/reverseproxy/reverseproxy.go`，`func (h *Handler) finalizeResponse(...) error`：
   - 1218–1224：101 提前 return，位于剥离之前。
   - 1226–1230：`removeConnectionHeaders(res.Header)` 与 `hopHeaders` 删除循环只对非 101 生效。
   - 1713–1724：`hopHeaders` 十项 `Alt-Svc, Connection, Proxy-Connection, Keep-Alive,
     Proxy-Authenticate, Proxy-Authorization, Te, Trailer, Transfer-Encoding, Upgrade`。
2. `modules/caddyhttp/reverseproxy/streaming.go`，`func (h *Handler) handleUpgradeResponse(...)`：
   - 90：`copyHeader(rw.Header(), res.Header)` 全量复制上游响应头。
   - 91：`normalizeWebsocketHeaders` 仅重映射 `Sec-Websocket-*`，不删除 hop-by-hop 头。

101 路径同时绕过 `removeConnectionHeaders` 与 `hopHeaders` 循环，是反向代理中唯一绕过剥离的响应路径。

修复版 v2.11.5：剥离前移到 1230–1244，101 时恢复 `Upgrade`/`Connection`。

## 7. 本地复现

### 7.1 环境

- WSL2，Linux `6.6.87.2-microsoft-standard-WSL2`，x86_64。
- Go `go1.26.10 linux/amd64`，sha256
  `ccfe7ae822d2c2f41f4fe7c956199967a4dac22d0ee0d2b2bfdb440aab3b20c5`（与官方 JSON 一致）；
  `GOTOOLCHAIN=local`、`CGO_ENABLED=0`。
- curl 8.5.0；Docker 不可用；全部 127.0.0.1 回环。

### 7.2 构建

两个标签以 `git archive` 展开到独立空目录：

```bash
cd /tmp/recon_build/v2.11.4
go build -trimpath -buildvcs=false -o /tmp/recon_build/caddy_v2114 ./cmd/caddy
cd /tmp/recon_build/v2.11.5
go build -trimpath -buildvcs=false -o /tmp/recon_build/caddy_v2115 ./cmd/caddy
```

两次 exit=0；sha256 见 `sources/build_env.txt`。因 `-trimpath -buildvcs=false`，`caddy version`
为 `unknown`，二进制 provenance 由 tag commit/tree/sha256 界定。

### 7.3 拓扑

- 上游 raw TCP server（`sources/harness/upstream.py`）回 `101 Switching Protocols`，带 `Upgrade`、
  `Connection: Upgrade`、`Sec-WebSocket-Accept` 及 `Alt-Svc`、`Keep-Alive`、`Proxy-Authenticate`、
  `Set-Cookie`；另有 `101conn` 变体（`Connection: Upgrade, X-Custom-ID` + `X-Custom-ID`）和 `200`
  对照变体。
- Caddyfile：

```
{
    auto_https off
    admin off
    log default { level ERROR }
}
:<proxy-port> {
    reverse_proxy 127.0.0.1:<upstream-port>
}
```

  `caddy adapt` exit=0（264 bytes），再 `caddy run --config ... --adapter caddyfile`。
- 客户端：advisory 原始 `curl -sv` PoC 与 raw-socket Python 客户端，结果一致。

### 7.4 红灯：v2.11.4

```bash
curl -sv -H "Upgrade: websocket" -H "Connection: Upgrade" \
  -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  -H "Sec-WebSocket-Version: 13" \
  http://localhost:18174/ws
```

```
< HTTP/1.1 101 Switching Protocols
< Alt-Svc: h2="attacker.example.com:443"; ma=86400
< Connection: Upgrade
< Keep-Alive: timeout=999
< Proxy-Authenticate: Basic realm="phish"
< Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
< Server: Caddy
< Set-Cookie: injected=malicious; Path=/
< Upgrade: websocket
< Date: Thu, 22 Oct 2026 19:10:44 GMT
```

三个 hop-by-hop 头泄漏；raw-socket 响应头总长 333 bytes。`101conn` 变体在 v2.11.4 下泄漏
`X-Custom-Id: should-be-stripped`，`Connection: Upgrade, X-Custom-ID` 未规范化（273 bytes）。

日志：`sources/repro_v2114_curl.txt`、`repro_v2114_ws.txt`、`repro_v2114_conn.txt`。

### 7.5 绿灯：v2.11.5

```
< HTTP/1.1 101 Switching Protocols
< Connection: Upgrade
< Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
< Server: Caddy
< Set-Cookie: injected=malicious; Path=/
< Upgrade: websocket
< Date: Thu, 22 Oct 2026 19:10:46 GMT
```

`Alt-Svc`、`Keep-Alive`、`Proxy-Authenticate` 全部消失，`Upgrade` 与 `Connection: Upgrade` 保留；
`101conn` 中 `X-Custom-Id` 被剥离、`Connection` 规范化为 `Upgrade`（177 bytes）。

日志：`sources/repro_v2115_curl.txt`、`repro_v2115_ws.txt`、`repro_v2115_conn.txt`。

### 7.6 对照：正常 200 响应

两版都剥离 `Alt-Svc`、`Keep-Alive`、`Proxy-Authenticate`；`Set-Cookie` 两版都会转发。
说明泄漏是 101 路径特有。日志：`sources/repro_v2114_plain.txt`、`repro_v2115_plain.txt`。

### 7.7 上游回归测试（红绿）

v2.11.5 自带 `hopheaders_test.go`（4 用例）：

```bash
go test ./modules/caddyhttp/reverseproxy/ -run 'TestFinalizeResponse' -v -count=1
```

4 个 PASS，`ok ... 0.018s`，exit 0（`sources/gotest_v2115.txt`）。

把同一测试文件回植到 v2.11.4 构建树后：

```
--- FAIL: TestFinalizeResponse_101_StripsHopByHopHeaders
    hopheaders_test.go:61: Alt-Svc = "h2=\"evil.com:443\"; ma=86400", want empty (should be stripped)
    hopheaders_test.go:61: Keep-Alive = "timeout=999", want empty (should be stripped)
    hopheaders_test.go:61: Proxy-Authenticate = "Basic realm=\"phish\"", want empty (should be stripped)
--- FAIL: TestFinalizeResponse_101_StripsConnectionNamedHeaders
    hopheaders_test.go:105: X-Custom-Id = "should-be-stripped", want empty
    hopheaders_test.go:108: Connection = "Upgrade, X-Custom-ID", want "Upgrade"
FAIL ... exit 1
```

`TestFinalizeResponse_200_StillStripsHopByHop` 与 `TestFinalizeResponse_101_NoUpgradeRequest`
在 v2.11.4 下也 PASS，与端到端对照一致。日志：`sources/gotest_v2114_backported.txt`。

## 8. 已知正例要素核对表

| 要素 | 结果 |
|---|---|
| 精确标签存在且 annotated | 是 |
| tree | `89190a02601c918d8de199c16a9d7d778ba204fa` |
| 模块路径 / Go 版本 | `github.com/caddyserver/caddy/v2` / 1.25.1 |
| 受影响代码在 v2.11.4 | 是 |
| 修复在后续稳定标签 | 是（v2.11.5/6/7） |
| 修复不在受影响标签 | 是（exit=1） |
| advisory 范围与代码一致 | 是 |
| 本地可复现 | 是（红/绿） |
| 完整修复 | 是，含上游回归测试 |

## 9. 限制与未验证项

1. **CVE 身份未获独立来源确认**：`CVE-2026-55458` 只见于仓库级 advisory；NVD `totalResults=0`、
   CVE.org `CVE_RECORD_DNE`、OSV 404、GitHub 全局 404。
2. **GitHub REST API 未能重拉**：未认证 403（rate limit）；仓库 JSON 用 2026-10-21 缓存，并与
   2026-10-22 公开 HTML 交叉一致。
3. **advisory 无 references**：修复为单父 "Merge commit from fork"，原始 fork 提交不可见。
   advisory→修复提交的关联是推断，依据是作者身份、提交内容/测试与描述逐条吻合、`git log -S` 唯一命中。
4. **只验证 HTTP/1.1 101 路径**：HTTP/2/HTTP/3 extended CONNECT（101→200）场景未实测，需 TLS/h2c；
   相关代码同处 `handleUpgradeResponse`，理论上同样受影响但未验证。
5. **`Set-Cookie` 不是本漏洞差异项**：它不是 hop-by-hop，v2.11.4/v2.11.5、101/200 都转发。
   advisory 把它列为 “cookie injection” 影响属于叙述夸大，评估时应剔除或改写。
6. **`Transfer-Encoding`/`Trailer`/`Te` 未单独实测**：Go transport 特殊处理导致注入不稳定；
   代码层面它们确在 `hopHeaders` 中且 101 路径未剥离。
7. **构建可复现性边界**：`-trimpath -buildvcs=false`，`caddy version` 为 `unknown`；依赖来自公网模块代理。
8. **现有数据快照不可直接用**：见第 2 节，`snap_5f7d6c5c600a7a23` 已含修复，是阻塞项。
9. **未读取**任务禁止的文件与目录（`candidates.jsonl`、`snapshot_candidate_triage.jsonl`、
   `evaluation_selection.jsonl`、`vulnerabilities.jsonl`、`runs/language/`、其他 `runs/verification/`、
   `WORK_LOG`/`HANDOFF`/`docs`），因此无法判断数据集中是否另有 caddy 记录。

## 10. 证据清单

`sources/` 下 37 个文件：

- `advisory_cache_meta.json`、`advisory_cache_GHSA-8qx7-j2v2-x6q5.json`、
  `advisory_cache_GHSA-6365-7ppr-5r92.json`
- `public_sources_notes.json`、`osv_*.json`、`nvd_CVE-2026-55458.json`、
  `cveorg_CVE-2026-55458.json`、`ghhtml_*.html`、`ghglobal_*.html`、`github_api_ratelimit_403.json`、
  `ghrepo_caddy.html`
- `tags_and_refs.txt`、`ancestry.txt`
- `fix_25b3eab6.diff`、`fix_1830809a.diff`、`vulnerable_and_fixed_code.txt`、`go_mod_at_tags.txt`
- `build_env.txt`、`gotest_v2115.txt`、`gotest_v2114_backported.txt`
- `repro_v2114_*.txt`、`repro_v2115_*.txt`
- `snapshot_record_caddy.json`、`snapshot_comparison.txt`
- `harness/upstream.py`、`harness/client_ws.py`、`harness/run_case.sh`

未创建 `dossier.json`；未修改 `data/`、`v031/`；所有下载/克隆位于 `/tmp`，脚本位于
`/tmp/recon_scripts`（另复制到 `sources/harness/`）。
