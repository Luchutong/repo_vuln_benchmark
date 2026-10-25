# CANDIDATE_FUNNEL_V031 — 候选筛选漏斗（v0.3.1）

> **状态（2026-10-25 复核）**：本文件正文记录的是 **2026-10-23** 的漏斗状态（当时 23 个已选快照、
> 1577 行 triage），此后证据先行选版补到 48 个目标、范围/祖先/低侧批次陆续落盘，正文数字已过时。
> 当前权威计数见 `LIMITATIONS_V031.md` §3 与 `HANDOFF_V031.md` §2；2026-10-26 round86 后实测：
> 2626 条候选、48 个仓库有 `evaluation_target`；**2613** 条 triage 行，恰好覆盖全部 2613 条
> 已选版仓库候选（每候选一行），13 条属未选版仓库（nlohmann/json、openssl/openssl）故无行；
> 决策分布 `confirmed_affected 191` / `confirmed_not_affected 1329` / `possible_affected 491` /
> `duplicate 28` / `unknown 574`（其中 549 条为 2026-10-24 补入的「此前无 triage 行」候选，
> 见 `runs/triage_untriaged_unknown_2026-10-24/`）。round70 由 6 条 undici v5.19.0 候选经源码级
> 功能缺失排除转入 `confirmed_not_affected`（`runs/verification/undici_v5.19.0_not_applicable_round70/`），
> 该 6 条**没有**运行时复现；round78 由 1 条 undici v5.19.0 候选（CVE-2026-12151，源码排除 +
> 15 次本地运行时探针：continuation 帧在 5.19.0 上逐帧交付、堆平坦，累积只在 v6.17.0 之后）转入
> `confirmed_not_affected`（`runs/verification/undici_v5.19.0_CVE-2026-12151/`）；round77 由 1 条 undici v5.19.0 候选（CVE-2026-87018，
> TLS 1.2 重协商换同名 CA 异主机证书后 `lib/client.js:926` 断言杀进程，隔离复核员自建 clone + harness、
> 54 个进程的红/绿矩阵判 grade A）转入 `confirmed_affected`
> （`runs/independent/undici_v5.19.0_CVE-2026-87018_round77/`）；round86 由 1 条 rack v3.1.13 候选（CVE-2026-34826，`lib/rack/utils.rb:419` 的 `$1.split(/,\s*/).each` 无计数上限、CVE-2024-26141 只在建好整组 Range 后校验总字节数；隔离复核员自建 clone 与 9 个 worktree、自写 harness 160/160 自检、每版 3 进程：101 / 10,000 / 200,000 个 `0-0` spec 在 v3.1.13 / v3.1.19 / v3.1.20 / v3.2.5 / v2.2.22 返回同数量 Range（200k 约 250-306 ms），在 v3.1.21 / v3.1.22 / v3.2.6 / v2.2.23 返回 nil；100 个仍接受、101 个被拒；`Rack::Files` 端到端由 409 字节 header 产出 206 multipart/byteranges 203 分块 / 7286 字节）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-34826_round86/`）；round85 由 1 条 rack v3.1.13 候选（CVE-2026-25500，`lib/rack/directory.rb:20` 的 `DIR_FILE` 无 `./` 前缀、`escape_path` 保留 `:` 且 `escape_html` 不中和 scheme；隔离复核员自建 clone 与 9 个 worktree、自写 fixture 与 Ruby/Python 双解析器每版 3 进程：`javascript:alert(1)` 在 v3.1.13 / v3.1.19 / v3.2.4 / v2.2.21 渲染为 scheme-bearing href，v3.1.20 / v3.1.21 / v3.2.5 / v3.2.6 / v2.2.22 全部 `./` 相对）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-25500_round85/`）；round84 由 1 条 rack v3.1.13 候选（CVE-2026-34835，`lib/rack/request.rb:729` 的 AUTHORITY 字符类允许 `/ ? # @ \` 进 `address`，`#host` 原样返回、朴素白名单被翻转；隔离复核员自建 clone 与 10 个 worktree、自写 harness 每版 3 进程：六个恶意 host 在 v3.1.13 / v3.1.19 / v3.1.20 / v3.2.5 全部原样，v3.1.21 / v3.1.22 / v3.2.6 / v3.2.7 全部 nil）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-34835_round84/`）；round83 由 1 条 rack v3.1.13 候选（CVE-2026-34830，`lib/rack/sendfile.rb:160` 的 `path.sub(/^#{internal}/i, external)` 把客户端 `X-Accel-Mapping` 插进正则且不转义；隔离复核员自建 clone 与 9 个 worktree、自写 harness 每版 3 进程：三种 crafted mapping 在 v3.1.13 / v3.1.19 / v3.1.20 / v3.2.5 / v2.2.22 上完全控制 `x-accel-redirect`，v3.1.21 / v3.1.22 / v3.2.6 / v2.2.23 保持字面）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-34830_round83/`）；round82 由 1 条 rack v3.1.13 候选（CVE-2026-34786，`lib/rack/static.rb:167-185` 的 `applicable_rules` 用未解码 `PATH_INFO` 匹配 `:fonts`/Array/Regexp 规则，而真正送文件的是解码后的路径；隔离复核员自建 clone 与 9 个 worktree、自写 harness 每版 5 场景 × 3 进程：`/fonts/test%2Ewoff` 在 v3.1.13 / v3.1.19 / v3.1.20 / v3.2.5 / v2.2.22 只带 1 条头，v3.1.21 / v3.1.22 / v3.2.6 / v2.2.23 带全 4 条）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-34786_round82/`）；round81 由 1 条 rack v3.1.13 候选（CVE-2026-34785，`lib/rack/static.rb:118` 的 `path.index(url) == 0` 只比字符串前缀、无路径分隔符边界，隔离复核员自建 clone 与 9 个 worktree、两种 harness 每版每形态 3 进程：`/root_test/<secret>.txt` 在 v3.1.13 / v3.1.19 / v3.1.20 / v3.2.5 / v2.2.22 3/3 泄露，v3.1.21 / v3.1.22 / v3.2.6 / v2.2.23 3/3 拦截）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-34785_round81/`）；round79 由 1 条 undici v5.19.0 候选（CVE-2026-6733，`lib/client.js:680-706` 把空闲 keep-alive socket 上的非请求响应绑给下一条排队请求，隔离复核员自建 clone 与同 tick harness：v5.19.0 30/30 红、v6.27.0 0/10 与 v7.28.0 0/25 绿、v8.5.0 仍偶发 2/25）转入 `confirmed_affected`
> （`runs/independent/undici_v5.19.0_CVE-2026-6733_round79/`）；round80 由 1 条 rack v3.1.13 候选（CVE-2026-22860，`Rack::Directory#check_forbidden` 的前缀比较缺路径分隔符边界，隔离复核员自建 clone 对拍 rubygems `.gem`、`/../public_backup/` 在 v3.1.13 / v3.1.19 / v3.2.4 回 200 且列表含 root 外文件、v3.1.20 / v3.2.5 回 403）转入 `confirmed_affected`
> （`runs/independent/rack_v3.1.13_CVE-2026-22860_round80/`）；round69 由 1 条 undici v5.19.0 候选（CVE-2026-1525，独立复核 A 级）转入
> `confirmed_affected`；round72 同样由 1 条 undici v5.19.0 候选（CVE-2026-16729，`setCookie()` 的 `domain`/`unparsed`
  未做字符集校验、`;` 注入额外属性，独立复核 A 级）转入 `confirmed_affected`；round71 同样由 1 条 undici v5.19.0 候选（CVE-2026-11525，Set-Cookie
> SameSite 子串匹配，独立复核 A 级）转入 `confirmed_affected`；round73 同样由 1 条 undici v5.19.0 候选
> （CVE-2026-109932，WebSocket receiver 对每个 PING 无条件回 PONG、不看 socket 背压，独立复核 A 级）转入
> `confirmed_affected`，该 CVE 的 GHSA 别名在 OSV 与 GitHub 上均 404，证据见
> `runs/verification/undici_v5.19.0_CVE-2026-109932/`；round75 同样由 1 条 undici v5.19.0 候选
> （CVE-2025-47279，`Pool` 永久保留连接失败 client，独立复核 A 级）转入 `confirmed_affected`；
> 复核者实测保留量在首轮并发峰值后饱和、不随重试次数增长，故只支持对象保留（CWE-401）口径。
> round74 同样由 1 条 undici v5.19.0 候选（CVE-2026-22036，`Content-Encoding` 层数无上限地建解压器，
> 独立复核 A 级）转入 `confirmed_affected`；复核者自写 harness 在 N=3000 层嵌套 gzip 下测得
> 180–203 s / +229–247 MB，修复版 13–21 ms 内以 5 层上限拒绝。round76 同样由 1 条 undici v5.19.0 候选
> （CVE-2026-109383，`Agent` 构造函数经 `util.deepClone` 丢掉函数值形式的 `tls.checkServerIdentity`，
> 独立复核 A 级、CWE-295）转入 `confirmed_affected`；六个 pre-fix 版回 200 且回调 0 次、三个 fixed 版
> 以回调 Error 拒绝且恰好 1 次，58 个数字 v5.* tag 仍无修复。
> 正文的「总览」块保留为历史记录，不再是当前状态。

对应数据：`data/snapshot_candidate_triage.jsonl`（每候选+冻结快照一条）、
`v031/reports/queue_P3.json`（plan_snapshot_queue 落盘）。初始生成 2026-10-22，
2026-10-23 随 django 评测目标从 tag 3.0.2 切到 tag 4.2.13、rack 从 2.2.3 切到 v3.1.13、
libexpat 从 R_2_4_4 切到 R_2_6_2、phoenix 从 v1.6.13 切到 v1.8.8 重新 triage 后更新为下列计数
（旧快照的 django 163 条、rack 50 条、libexpat 143 条与 phoenix 8 条 triage 行分别归档在
`data/legacy_snapshot_candidate_triage_snap_ab695ba3db678939.jsonl`、
`data/legacy_snapshot_candidate_triage_snap_f97687a4e0807cb2.jsonl`、
`data/legacy_snapshot_candidate_triage_snap_d33251dac37c334c.jsonl` 与
`data/legacy_snapshot_candidate_triage_snap_ee79f4175242bbee.jsonl`）。

## 总览

```
原始候选（data/candidates.jsonl）                   2626
│
├─ 位于 23 个已选仓库（有冻结 SHA 可判定）      1577  → 已 triage
│     ├─ confirmed_affected      71   （distinct 漏洞 60，对应 Oracle 正样本）
│     ├─ confirmed_not_affected 303   （版本/分支区间证据 + phoenix 4 条代码级排除）
│     └─ unknown               1203   （未在零 LLM 阶段确立相关性，≠无漏洞）
│
└─ 未 triage                                     1049
      └─ 27 个未选仓库（无冻结 SHA）             1049  → P0_SELECT_SNAPSHOT
```

- 已 triage 覆盖 23 个快照；`review_method`：`source_code_review` 75（71 affected + 4 phoenix 排除行）/
  `trusted_range_with_branch` 299 / `unresolved` 1203。
- 初始 1568 条决策来自既有证据（candidate.status / reason / source_urls / Oracle confirmed_affected），
  未引入任何 LLM 或编造；此后 5 条独立复核提升（rexml CVE-2025-58767、django CVE-2024-39330、
  rack CVE-2025-46727、libexpat CVE-2024-45490、phoenix CVE-2026-56812）各补 affected 行
  （phoenix 的 56811/56812 各有两条 discovery 路径），rexml 的 8 条、libexpat 的 7 条与 phoenix 的
  4 条以修复区间 / 代码级核对 + 完整 clone 祖先关系补 not_affected 行（见下），同时归档了四个旧快照的
  163/50/143/8 条行（其中 19 affected / 127 not_affected / 216 unknown），净得当前 1577 行。
  django 新快照上其余 162 条、rack 新快照上其余 49 条、libexpat 新快照上其余 135 条候选一律保留
  `unknown`——旧快照的驳回理由不能直接证明其在新 tag 上不适用。

## 逐阶段说明

1. **confirmed_affected（71 = 60 distinct vuln）**：`status=verified` 且其 `vulnerability_id` 在该库已选快照的
   Oracle 为 `confirmed_affected`。证据 URL 沿用候选 `source_urls`；判定复用既有代码级复核（source_code_review）。
   「2 候选→1 漏洞」的别名在同快照下计为一个已知正样本，不重复加分。
   其中手工提升的包括：`disc2_de98c5ab937e69a43862e5b4`（CVE-2025-58767，ruby/rexml，
   A 级 red/green）、`disc2_911c6ce3cba60cce0edccd71`（CVE-2024-39330，django tag 4.2.13，A 级
   red/green）、`disc2_7f2500f73d3836ead0e09463`（CVE-2025-46727，rack v3.1.13，A 级 red/green）、
   `disc2_35a922eb511ed468630f4a2d`（CVE-2024-45490，libexpat R_2_6_2，A 级 red/green），以及
   phoenix v1.8.8 上的 `disc2_46723370667ed0c5775db602` / `adv3_935719b31ddff77e`（CVE-2026-56811，B 级）
   与 `disc2_49ab8b917b7f862af6ea3968` / `adv3_a7fa8aabc9d9faea`（CVE-2026-56812，A 级 red/green）；
   其余由规则阶段从既有 Oracle 状态生成。

2. **confirmed_not_affected（303 = 299 trusted_range + 4 phoenix source_code_review）**：`status=rejected` 且 reason 含快照相关性排除子句（`Not applicable to
   snapshot` / `does not apply`），如「fix already in <tag>」「introduced after <tag>」「advisory 区间在
   <tag> 之后」等，属版本/分支区间规则（trusted_range_with_branch），非裸 semver 字符串比较；均有
   runs/verification 下的 NOT_APPLICABLE.md 卷宗佐证与 https 证据 URL。这些候选被归档、不再深度审计。
   其中 rexml 的 8 条（7 个 distinct CVE + 1 条重复 advisory 行）与 libexpat 的 7 条（旧 R_2_4_4
   目标下的 2022 系列 CVE）是 2026-10-23 新增：OSV 修复区间加上完整 clone 中修复 tag/fix commit
   对目标 commit 的祖先关系（`runs/verification/rexml_snapshot_not_applicable/NOT_APPLICABLE.md`、
   `runs/verification/libexpat_R_2_6_2_fixed_previous/NOT_APPLICABLE.md`），只证修复已存在，
   不证快照无其他漏洞。phoenix v1.8.8 上的 4 条（CVE-2017-1000163、CVE-2022-42975 各 1 条，
   CVE-2026-32689 2 条）是 `source_code_review`：除 advisory 区间外还核对了快照内代码
   （`validate_local_url/1` 的 `//` 与反斜杠拒绝、`compare_host?/2` 的点边界、
   `long_poll.ex` 的 `String.splitter` + `Enum.find`）及修复 commit 祖先关系。

3. **unknown（1203）**：位于已选仓库、但此零 LLM 阶段未确立对冻结 SHA 的相关性（`status ∈ {pending_location,
   pending_in_validation, pending_version}`，或 1 条被撤回 advisory 的 rejected）。**unknown ≠ 无漏洞**；
   其中可能与 SHA 相关的须进入 P4 定向核验，否则保留 draft。1 条 `adv3_087476da78c375b4`（advisory
   withdrawn/REJECTED）标 unknown，不自动判无漏洞。django 新快照上 162 条、rack 新快照上 49 条、libexpat 新快照上 135 条候选
   全部保留 unknown：它们在旧 tag 上的驳回理由不构成对新 tag 的适用性证据。phoenix 新快照的 8 条
   候选已全部有决策，不再保留 unknown。

4. **未 triage（1049）**：全部是 27 个未选仓库的候选，无冻结 SHA，须先选版冻结。已冻结的
   rexml 快照上不再有未 triage 候选（8 条已完成判定）。

## 队列（plan_snapshot_queue，`v031/reports/queue_P3.json`）

| 优先级 | 计数 | 含义 |
|---|---|---|
| P0_SELECT_SNAPSHOT | 1049 | 27 未选仓库候选，先选版 |
| DONE | 71 | confirmed_affected（可作 recall 正样本，distinct 漏洞 60） |
| ARCHIVE | 303 | confirmed_not_affected（归档） |
| P1_REVIEW | 1203 | unknown，需低成本定向核验 |

## 约束与诚实边界

- 不因本次筛选删除任何候选；原 `candidates.jsonl` 完整保留。
- 结构校验通过 ≠ 漏洞真实存在；`unknown`/`possible_affected` 未核验前不得声明快照已知漏洞已穷尽。
- 后续新增候选或修正决策时，用 `build_initial_triage.py --checked-at <ISO>` 与 plan_snapshot_queue 刷新。