# SELECTION_REPORT_V031 — 每库评测目标选择现状（v0.3.1）

对应数据根目录：`/home/luchitong/work/repo-vuln-50-v031`，生成时间 2026-10-22。
选择一律**不得因测试结果反向换版**；未冻结前不得把数据目录交给被测 Agent。

> **2026-10-23 状态更新（本节优先于下文 10-22 快照）**：评测目标已增至 **23 个**（新增 ruby/rexml v3.4.1、
> django 4.2.13、rack v3.1.13、libexpat R_2_6_2，均先取得 A 级正样本再选版；phoenix 由 v1.6.13
> 升级到 v1.8.8，同样先在新 tag 上取得两个独立正样本 verdict 再选版）；独立选版审查后
> **17 frozen / 6 proposed**（6 个 proposed 均为 legacy `documented_exception`），27 个仓库
> `needs_selection`；已知正样本 **60 条 live（55 B + 5 A）**（旧 django 3.0.2 / rack 2.2.3 /
> libexpat R_2_4_4 / phoenix v1.6.13 状态行已归档，不计入）。
> 当前权威表为 `v031/reports/SELECTION_TABLE.md`，冻结详情见
> `v031/reports/SELECTION_FREEZE_2026-10-22.md`（含 10-23 追加节）。下文为 10-22 的原始快照记录。

## 结论

- 50 个仓库中，**22 个已有 `proposed` 评测目标**（每库一个稳定 tag 的 commit），且该 SHA 均有
  `confirmed_affected` 已确认正样本（`evaluation_selection` 22 行全部 `decision_status=proposed`，0 frozen）。
- **28 个仓库暂无评测目标**（`needs_selection`）：它们 Catalog 已验证漏洞为 0。其中 axios/OpenSSL/sinatra
  各自有一个带 tag 的历史快照（v1.15.0 / openssl-3.0.1 / v3.0.3），但仍无 `confirmed_affected`；
  其余 25 个只有默认分支 HEAD（`tag_or_release=null`）。按 v0.3.1 规则「该 SHA 至少一条 B/A 已确认漏洞」，
  不能自动选择；本轮**没有编造任何 tag 或 commit**。
- 已选 SHA 均为稳定发布 tag（如 netty-4.1.59.Final、jenkins-2.441、django-3.0.2），不是为「更多漏洞」选的
  过旧版本；每个 SHA 至少一个已确认正样本保证可作 recall 基准。

## 已选 22 个仓库（proposed；正样本数 = 该 SHA confirmed_affected 条数）

| 仓库 | 语言 | tag/release | SHA(前10) | 该 SHA 已确认正样本数 |
|---|---|---|---|---|
| netty/netty | Java | netty-4.1.59.Final | snap_bb344 | 6 |
| jenkinsci/jenkins | Java | jenkins-2.441 | snap_d9b0f | 6 |
| nodejs/undici | JavaScript | v5.19.0 | snap_24c4a | 3 |
| guzzle/guzzle | PHP | 7.4.4 | snap_efe69 | 2 |
| phoenixframework/phoenix | Elixir | v1.6.13 | snap_ee79f | 2 |
| gin-gonic/gin | Go | v1.5.0 | snap_d4899 | 1 |
| protocolbuffers/protobuf | C++ | v3.20.1 | snap_6bc3f | 3 |
| hyperium/hyper | Rust | v0.14.2 | snap_735b4 | 1 |
| expressjs/express | JavaScript | 4.19.2 | snap_3166f | 1 |
| vitejs/vite | TypeScript | v5.0.11 | snap_2e50b | 4 |
| libarchive/libarchive | C | v3.7.7 | snap_a47bc | 1 |
| JamesNK/Newtonsoft.Json | C# | 12.0.3 | snap_25561 | 1 |
| django/django | Python | 3.0.2 | snap_ab695 | 8 |
| symfony/symfony | PHP | v5.4.45 | snap_39105 | 18 |
| DaveGamble/cJSON | C | v1.7.16 | snap_d9525 | 1 |
| curl/curl | C | curl-8_3_0 | snap_0ec1c | 2 |
| rustls/rustls | Rust | v0.23.4 | snap_b3a68 | 1 |
| pallets/flask | Python | 2.3.1 | snap_8ed1c | 1 |
| laravel/framework | PHP | v11.30.0 | snap_6e1f4 | 1 |
| libexpat/libexpat | C | R_2_4_4 | snap_d3325 | 7 |
| rack/rack | Ruby | 2.2.3 | snap_f9768 | 2 |
| pallets/werkzeug | Python | 3.0.2 | snap_b5726 | 1 |

> 22 库已确认正样本合计 73 条（与 10-22 当时的 Oracle `confirmed_affected` 总数一致）。
>
> **该表已被取代（2026-10-23）**：django 3.0.2 → 4.2.13、rack 2.2.3 → v3.1.13、
> libexpat R_2_4_4 → R_2_6_2、phoenix v1.6.13（`snap_ee79f`）→ v1.8.8（`snap_aca732`，2 条正样本）；
> 另新增 ruby/rexml v3.4.1。当前快照与正样本数见 `v031/reports/SELECTION_TABLE.md`。

## 未选 28 个仓库（needs_selection；Catalog 已验证漏洞为 0，需先补正样本再选版）

| 仓库 | 语言 | 现有快照情形 |
|---|---|---|
| actix/actix-web | Rust | 仅默认分支 HEAD（tag=null） |
| elixir-ecto/ecto | Elixir | 仅默认分支 HEAD（tag=null） |
| sinatra/sinatra | Ruby | 2 个快照；tag=v3.0.3（无 confirmed_affected） |
| nlohmann/json | C++ | 仅默认分支 HEAD（tag=null） |
| spring-projects/spring-framework | Java | 仅默认分支 HEAD（tag=null） |
| pyca/cryptography | Python | 仅默认分支 HEAD（tag=null） |
| ruby/rexml | Ruby | 仅默认分支 HEAD（tag=null） |
| elixir-plug/plug | Elixir | 仅默认分支 HEAD（tag=null） |
| elixir-plug/plug_cowboy | Elixir | 仅默认分支 HEAD（tag=null） |
| dotnet/aspnetcore | C# | 仅默认分支 HEAD（tag=null） |
| PHPMailer/PHPMailer | PHP | 仅默认分支 HEAD（tag=null） |
| axios/axios | JavaScript | 2 个快照；tag=v1.15.0（无 confirmed_affected） |
| angular/angular | TypeScript | 仅默认分支 HEAD（tag=null） |
| apache/tomcat | Java | 仅默认分支 HEAD（tag=null） |
| grpc/grpc | C++ | 仅默认分支 HEAD（tag=null） |
| caddyserver/caddy | Go | 仅默认分支 HEAD（tag=null） |
| labstack/echo | Go | 仅默认分支 HEAD（tag=null） |
| jbeder/yaml-cpp | C++ | 仅默认分支 HEAD（tag=null） |
| leethomason/tinyxml2 | C++ | 仅默认分支 HEAD（tag=null） |
| lodash/lodash | JavaScript | 仅默认分支 HEAD（tag=null） |
| aaubry/YamlDotNet | C# | 仅默认分支 HEAD（tag=null） |
| tokio-rs/tokio | Rust | 仅默认分支 HEAD（tag=null） |
| vercel/next.js | JavaScript | 仅默认分支 HEAD（tag=null） |
| SixLabors/ImageSharp | C# | 仅默认分支 HEAD（tag=null） |
| go-gitea/gitea | Go | 仅默认分支 HEAD（tag=null） |
| openssl/openssl | C | 2 个快照；tag=openssl-3.0.1（无 confirmed_affected） |
| nestjs/nest | TypeScript | 仅默认分支 HEAD（tag=null） |
| rails/rails | Ruby | 仅默认分支 HEAD（tag=null） |

## 冻结阻塞与后续

- 22 个 proposed 目标要 `frozen` 还需：独立 reviewer（`reviewed_by ≠ selected_by`）、`frozen_at`、
  防泄漏工作树导出（去 `.git`、去未来历史）、构建可行性验证。
- 28 个未选仓库要选版，须先为该版本补充至少一条 B/A 已确认正样本（禁止先选版本后补证据）。
- 语言覆盖：抽查反映主语言多样性 >10 类（C/C++/Java/JS/TS/Python/Go/Rust/Ruby/PHP/Elixir/C#），
  满足 release 主语言 ≥10 的要求；最终以 strict 校验为准。

主要数据表详见 `v031/reports/SELECTION_TABLE.md`（由脚本生成，随状态刷新）。