## 已选 23 个仓库（17 frozen / 6 proposed，均含 confirmed_affected 正样本）

「该 SHA 已确认正样本数」为该快照 `snapshot_vulnerability_status` 中 live `confirmed_affected` 的
distinct 漏洞数；旧 django 3.0.2、rack 2.2.3、libexpat R_2_4_4 与 phoenix v1.6.13 的状态行已归档，不计入。
phoenix 于 2026-10-23 由 v1.6.13 升到 v1.8.8（先取得 CVE-2026-56811 / CVE-2026-56812 的独立验证，再选版），
新快照 `snap_aca73214a7703174` 已通过独立 selection review 并冻结。

| 仓库 | 语言 | tag/release | SHA(前10) | 该 SHA 已确认正样本数 | 选版状态 |
|---|---|---|---|---|---|
| curl/curl | C | `curl-8_3_0` | `snap_0ec1c1` | 2 | frozen |
| DaveGamble/cJSON | C | `v1.7.16` | `snap_d95256` | 1 | frozen |
| django/django | Python | `4.2.13` | `snap_516aa9` | 1 | frozen |
| expressjs/express | JavaScript | `4.19.2` | `snap_3166f7` | 1 | frozen |
| gin-gonic/gin | Go | `v1.5.0` | `snap_d4899c` | 1 | proposed |
| guzzle/guzzle | PHP | `7.4.4` | `snap_efe695` | 2 | proposed |
| hyperium/hyper | Rust | `v0.14.2` | `snap_735b41` | 1 | proposed |
| JamesNK/Newtonsoft.Json | C# | `12.0.3` | `snap_255617` | 1 | proposed |
| jenkinsci/jenkins | Java | `jenkins-2.441` | `snap_d9b0ff` | 6 | frozen |
| laravel/framework | PHP | `v11.30.0` | `snap_6e1f42` | 1 | frozen |
| libarchive/libarchive | C | `v3.7.7` | `snap_a47bca` | 1 | frozen |
| libexpat/libexpat | C | `R_2_6_2` | `snap_67132f` | 1 | frozen |
| netty/netty | Java | `netty-4.1.59.Final` | `snap_bb344e` | 6 | proposed |
| nodejs/undici | JavaScript | `v5.19.0` | `snap_24c4a1` | 3 | frozen |
| pallets/flask | Python | `2.3.1` | `snap_8ed1ca` | 1 | frozen |
| pallets/werkzeug | Python | `3.0.2` | `snap_b57262` | 1 | frozen |
| phoenixframework/phoenix | Elixir | `v1.8.8` | `snap_aca732` | 2 | frozen |
| protocolbuffers/protobuf | C++ | `v3.20.1` | `snap_6bc3f3` | 3 | proposed |
| rack/rack | Ruby | `v3.1.13` | `snap_245aee` | 1 | frozen |
| ruby/rexml | Ruby | `v3.4.1` | `snap_23dff8` | 1 | frozen |
| rustls/rustls | Rust | `v/0.23.4` | `snap_b3a689` | 1 | frozen |
| symfony/symfony | PHP | `v5.4.45` | `snap_39105a` | 18 | frozen |
| vitejs/vite | TypeScript | `v5.0.11` | `snap_2e50b2` | 4 | frozen |

## 未选 27 个仓库（needs_selection，无冻结 SHA）

「候选数」为 `candidates.jsonl` 中该仓库的候选行数（全部未 triage，队列 P0_SELECT_SNAPSHOT）。
`代表快照 tag=HEAD` 表示 `representative_snapshot_id` 指向默认分支 HEAD；
axios/OpenSSL/sinatra 另有带 tag 的历史快照（v1.15.0 / openssl-3.0.1 / v3.0.3），但同样无 confirmed_affected。

| 仓库 | 语言 | 代表快照 tag | 候选数 |
|---|---|---|---:|
| aaubry/YamlDotNet | C# | HEAD（无 tag） | 1 |
| actix/actix-web | Rust | HEAD（无 tag） | 9 |
| angular/angular | TypeScript | HEAD（无 tag） | 40 |
| apache/tomcat | Java | HEAD（无 tag） | 41 |
| axios/axios | JavaScript | HEAD（无 tag） | 67 |
| caddyserver/caddy | Go | HEAD（无 tag） | 37 |
| dotnet/aspnetcore | C# | HEAD（无 tag） | 68 |
| elixir-ecto/ecto | Elixir | HEAD（无 tag） | 4 |
| elixir-plug/plug | Elixir | HEAD（无 tag） | 11 |
| elixir-plug/plug_cowboy | Elixir | HEAD（无 tag） | 2 |
| go-gitea/gitea | Go | HEAD（无 tag） | 293 |
| grpc/grpc | C++ | HEAD（无 tag） | 8 |
| jbeder/yaml-cpp | C++ | HEAD（无 tag） | 7 |
| labstack/echo | Go | HEAD（无 tag） | 16 |
| leethomason/tinyxml2 | C++ | HEAD（无 tag） | 3 |
| lodash/lodash | JavaScript | HEAD（无 tag） | 10 |
| nestjs/nest | TypeScript | HEAD（无 tag） | 12 |
| nlohmann/json | C++ | HEAD（无 tag） | 3 |
| openssl/openssl | C | HEAD（无 tag） | 10 |
| PHPMailer/PHPMailer | PHP | HEAD（无 tag） | 18 |
| pyca/cryptography | Python | HEAD（无 tag） | 43 |
| rails/rails | Ruby | HEAD（无 tag） | 148 |
| sinatra/sinatra | Ruby | HEAD（无 tag） | 6 |
| SixLabors/ImageSharp | C# | HEAD（无 tag） | 16 |
| spring-projects/spring-framework | Java | HEAD（无 tag） | 84 |
| tokio-rs/tokio | Rust | HEAD（无 tag） | 6 |
| vercel/next.js | JavaScript | HEAD（无 tag） | 86 |
