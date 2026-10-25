# 来源覆盖报告

截止日 2026-10-21。50 个准入仓库全部完成 OSV 包查询、NVD/CVE 子集查询与官方 GitHub repository advisory 拉取；
advisory 接口 50/50 成功，50 个仓库响应共 846 条公告记录，
其中 36 个仓库至少一条、14 个仓库为空列表（空列表是检索结果，不是“无漏洞”结论）。

候选 2626 行：{'in_validation': 503, 'pending_location': 750, 'pending_version': 861, 'rejected': 429, 'verified': 83}。其中 83 行已随漏洞正式目录提升为 `verified`；
未解决 2114 行。来源族、查询记录和限制见 `data/discovery_coverage.jsonl`；覆盖结论 {'NEEDS_REVIEW': 50}，
因此 **PASS_KNOWN_SWEEP 为 0**，不得把本轮称为完整已知漏洞穷尽。

OSV 聚合记录可能继承 GHSA/NVD/生态库；官方 repository advisory 是独立拉取的源族，但同样不是完整历史漏洞清单。NVD 只查询了部分仓库。
未解决候选集中在高披露量项目（如 Jenkins、Symfony、Next.js），这是工作量而非“漏洞更多”的证明。

| 仓库 | 候选行 | 已验证 | 未解决 | 覆盖结论 |
|---|---:|---:|---:|---|
| [aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) | 1 | 0 | 1 | NEEDS_REVIEW |
| [actix/actix-web](https://github.com/actix/actix-web) | 9 | 0 | 9 | NEEDS_REVIEW |
| [angular/angular](https://github.com/angular/angular) | 40 | 0 | 40 | NEEDS_REVIEW |
| [apache/tomcat](https://github.com/apache/tomcat) | 41 | 0 | 41 | NEEDS_REVIEW |
| [axios/axios](https://github.com/axios/axios) | 67 | 0 | 67 | NEEDS_REVIEW |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) | 37 | 0 | 37 | NEEDS_REVIEW |
| [curl/curl](https://github.com/curl/curl) | 387 | 2 | 385 | NEEDS_REVIEW |
| [DaveGamble/cJSON](https://github.com/DaveGamble/cJSON) | 52 | 1 | 51 | NEEDS_REVIEW |
| [django/django](https://github.com/django/django) | 163 | 8 | 155 | NEEDS_REVIEW |
| [dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) | 68 | 0 | 68 | NEEDS_REVIEW |
| [elixir-ecto/ecto](https://github.com/elixir-ecto/ecto) | 4 | 0 | 4 | NEEDS_REVIEW |
| [elixir-plug/plug](https://github.com/elixir-plug/plug) | 11 | 0 | 11 | NEEDS_REVIEW |
| [elixir-plug/plug_cowboy](https://github.com/elixir-plug/plug_cowboy) | 2 | 0 | 2 | NEEDS_REVIEW |
| [expressjs/express](https://github.com/expressjs/express) | 6 | 1 | 5 | NEEDS_REVIEW |
| [gin-gonic/gin](https://github.com/gin-gonic/gin) | 5 | 1 | 4 | NEEDS_REVIEW |
| [go-gitea/gitea](https://github.com/go-gitea/gitea) | 293 | 0 | 293 | NEEDS_REVIEW |
| [grpc/grpc](https://github.com/grpc/grpc) | 8 | 0 | 8 | NEEDS_REVIEW |
| [guzzle/guzzle](https://github.com/guzzle/guzzle) | 17 | 2 | 15 | NEEDS_REVIEW |
| [hyperium/hyper](https://github.com/hyperium/hyper) | 11 | 1 | 10 | NEEDS_REVIEW |
| [JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json) | 1 | 1 | 0 | NEEDS_REVIEW |
| [jbeder/yaml-cpp](https://github.com/jbeder/yaml-cpp) | 7 | 0 | 7 | NEEDS_REVIEW |
| [jenkinsci/jenkins](https://github.com/jenkinsci/jenkins) | 259 | 6 | 253 | NEEDS_REVIEW |
| [labstack/echo](https://github.com/labstack/echo) | 16 | 0 | 16 | NEEDS_REVIEW |
| [laravel/framework](https://github.com/laravel/framework) | 39 | 1 | 38 | NEEDS_REVIEW |
| [leethomason/tinyxml2](https://github.com/leethomason/tinyxml2) | 3 | 0 | 3 | NEEDS_REVIEW |
| [libarchive/libarchive](https://github.com/libarchive/libarchive) | 23 | 1 | 22 | NEEDS_REVIEW |
| [libexpat/libexpat](https://github.com/libexpat/libexpat) | 143 | 7 | 136 | NEEDS_REVIEW |
| [lodash/lodash](https://github.com/lodash/lodash) | 10 | 0 | 10 | NEEDS_REVIEW |
| [nestjs/nest](https://github.com/nestjs/nest) | 12 | 0 | 12 | NEEDS_REVIEW |
| [netty/netty](https://github.com/netty/netty) | 130 | 6 | 124 | NEEDS_REVIEW |
| [nlohmann/json](https://github.com/nlohmann/json) | 3 | 0 | 3 | NEEDS_REVIEW |
| [nodejs/undici](https://github.com/nodejs/undici) | 56 | 3 | 53 | NEEDS_REVIEW |
| [openssl/openssl](https://github.com/openssl/openssl) | 10 | 0 | 10 | NEEDS_REVIEW |
| [pallets/flask](https://github.com/pallets/flask) | 8 | 1 | 7 | NEEDS_REVIEW |
| [pallets/werkzeug](https://github.com/pallets/werkzeug) | 25 | 1 | 24 | NEEDS_REVIEW |
| [phoenixframework/phoenix](https://github.com/phoenixframework/phoenix) | 8 | 2 | 6 | NEEDS_REVIEW |
| [PHPMailer/PHPMailer](https://github.com/PHPMailer/PHPMailer) | 18 | 0 | 18 | NEEDS_REVIEW |
| [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) | 14 | 3 | 11 | NEEDS_REVIEW |
| [pyca/cryptography](https://github.com/pyca/cryptography) | 43 | 0 | 43 | NEEDS_REVIEW |
| [rack/rack](https://github.com/rack/rack) | 50 | 2 | 48 | NEEDS_REVIEW |
| [rails/rails](https://github.com/rails/rails) | 148 | 0 | 148 | NEEDS_REVIEW |
| [ruby/rexml](https://github.com/ruby/rexml) | 9 | 0 | 9 | NEEDS_REVIEW |
| [rustls/rustls](https://github.com/rustls/rustls) | 13 | 1 | 12 | NEEDS_REVIEW |
| [sinatra/sinatra](https://github.com/sinatra/sinatra) | 6 | 0 | 6 | NEEDS_REVIEW |
| [SixLabors/ImageSharp](https://github.com/SixLabors/ImageSharp) | 16 | 0 | 16 | NEEDS_REVIEW |
| [spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) | 84 | 0 | 84 | NEEDS_REVIEW |
| [symfony/symfony](https://github.com/symfony/symfony) | 129 | 18 | 111 | NEEDS_REVIEW |
| [tokio-rs/tokio](https://github.com/tokio-rs/tokio) | 6 | 0 | 6 | NEEDS_REVIEW |
| [vercel/next.js](https://github.com/vercel/next.js) | 86 | 0 | 86 | NEEDS_REVIEW |
| [vitejs/vite](https://github.com/vitejs/vite) | 29 | 4 | 25 | NEEDS_REVIEW |

数据质量问题（拒绝的 CVE、复用 fix commit、修复版本冲突、tag 拼写）逐条记录在 `runs/verification/data_quality_findings.md`，未被静默丢弃。
