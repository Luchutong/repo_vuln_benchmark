# 仓库准入报告（P2 初版）

状态：50/50 依据已采集证据通过 75 分门槛；这是文档/流程门槛，不等于漏洞验证或独立复核完成。

评分口径（每项均由 runs/admission/raw 中的可复查响应计算）：

- 历史与真实性 25：元数据身份匹配、公开非 fork/非归档、浅克隆 PASS、仓库历史 >730 天、观察到 ≥3 条提交。
- 维护 20：pushed_at 180 天内、最新提交 180 天内、365 天内有 release 或 changelog 日期。
- 修复可追踪 20：CVE 提交搜索命中、观察到官方修复 commit/PR diff、安全策略、可用于映射修复的 release/tag。
- 测试 15：CI workflow、workflow 中的测试命令、测试目录/测试配置。
- 发布 15：GitHub Releases 或 tag、365 天内发布、changelog/release notes。
- 元数据 5：description/default_branch/primary_language/owner/created_at 完整。

证据索引与逐仓库分数见 `runs/admission/decisions.jsonl`、`runs/admission/summary.json`；请求日志见 `runs/admission/http_requests.jsonl`。

| 仓库 | 主语言 | 分数 | 默认分支 HEAD SHA |
|---|---|---:|---|
| [DaveGamble/cJSON](https://github.com/DaveGamble/cJSON) | C | 89 | `6d9f2443ab071f86e5d9b43025a40929ec41c46c` |
| [curl/curl](https://github.com/curl/curl) | C | 100 | `82be2bbded0c043b2b225ca97922da1ce874c5f3` |
| [libarchive/libarchive](https://github.com/libarchive/libarchive) | C | 96 | `03b426003adf12c1eb4c34e72bedb4c2bf1ba8d3` |
| [libexpat/libexpat](https://github.com/libexpat/libexpat) | C | 91 | `628f49ba13f789b2f94e678367c8d5da474c12bc` |
| [openssl/openssl](https://github.com/openssl/openssl) | C | 100 | `63bd920445f5339aa0ccaf07475df7abac2c8632` |
| [JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json) | C# | 78 | `52fa3aef1f2cadcd3a3f874251eddc98d3efbbaa` |
| [SixLabors/ImageSharp](https://github.com/SixLabors/ImageSharp) | C# | 94 | `a73c43da5a82f151506dd5288c4897b2b885c325` |
| [aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) | C# | 96 | `4f7e6e346649ec2a402607a3c1ea352c6fb5ecd3` |
| [dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) | C# | 91 | `2d105dd1fd119edff9a797a1b1aeca6d771c6134` |
| [grpc/grpc](https://github.com/grpc/grpc) | C++ | 100 | `8b32af3bf498c2ba9667410eaa8c836e700e97e6` |
| [jbeder/yaml-cpp](https://github.com/jbeder/yaml-cpp) | C++ | 94 | `c5e65360373d1d99d6b6848c991cd4fcee435009` |
| [leethomason/tinyxml2](https://github.com/leethomason/tinyxml2) | C++ | 77 | `8224e427b655b83dae5e2298f1e6919523a78737` |
| [nlohmann/json](https://github.com/nlohmann/json) | C++ | 84 | `5e13f834c16ddcfa12b10495cf48d6087d665343` |
| [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) | C++ | 96 | `0911cfc8a1c15e77db2dd062abdf2af60089bf17` |
| [elixir-ecto/ecto](https://github.com/elixir-ecto/ecto) | Elixir | 83 | `c0c99f51ef1dc71c265162c92623858027122a77` |
| [elixir-plug/plug](https://github.com/elixir-plug/plug) | Elixir | 94 | `05bde7066c373cc47390281d0f698029a725521b` |
| [elixir-plug/plug_cowboy](https://github.com/elixir-plug/plug_cowboy) | Elixir | 83 | `87740b57291398ef63189270806567e7772fce5e` |
| [phoenixframework/phoenix](https://github.com/phoenixframework/phoenix) | Elixir | 100 | `e5880ef7390d6fb4759d6cf9a957a310cefca7c4` |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) | Go | 96 | `f355b8687d5582ea9fcc99f71598109d1e5b6ced` |
| [gin-gonic/gin](https://github.com/gin-gonic/gin) | Go | 100 | `0f09c3a9b4626d9fe9979cf4d0521d6ae32ab646` |
| [go-gitea/gitea](https://github.com/go-gitea/gitea) | Go | 100 | `a8e1057f5e75b0f8cf11191acfde161aa9d88bd2` |
| [labstack/echo](https://github.com/labstack/echo) | Go | 100 | `8fd0e184dd390ffdf082f5eda247c3ab41d5d290` |
| [apache/tomcat](https://github.com/apache/tomcat) | Java | 84 | `ed8d6339035fb93f8628dbff0a1e4ff1df851c2d` |
| [jenkinsci/jenkins](https://github.com/jenkinsci/jenkins) | Java | 100 | `c5f59e8b565d91ba7e9a209337a49e1fbb19f1db` |
| [netty/netty](https://github.com/netty/netty) | Java | 91 | `5776ebc58d19637392d60fe707ee3adcb830c9bf` |
| [spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) | Java | 95 | `42c0a9bcc6755d0938f5b4854308c5e62856bfb9` |
| [axios/axios](https://github.com/axios/axios) | JavaScript | 100 | `fceeb10997ea71778ad8bc9671ad53e9195a707c` |
| [expressjs/express](https://github.com/expressjs/express) | JavaScript | 100 | `0dee2c52c7c873498f8ed7d8ee4ddd0a04d3ada8` |
| [lodash/lodash](https://github.com/lodash/lodash) | JavaScript | 95 | `2b5e6f7399a7b48005140b5d5c6bc6c0e62919a8` |
| [nodejs/undici](https://github.com/nodejs/undici) | JavaScript | 100 | `25543f5bd5744ff673016ed89b4bb09455e4875a` |
| [vercel/next.js](https://github.com/vercel/next.js) | JavaScript | 100 | `a89c0afe5702f604a142f5d185b0b0018b4eefa7` |
| [PHPMailer/PHPMailer](https://github.com/PHPMailer/PHPMailer) | PHP | 100 | `c0b5268a626d6ddbe71333cc1c60c5ae37e44e0d` |
| [guzzle/guzzle](https://github.com/guzzle/guzzle) | PHP | 100 | `b920e5fcaf81d761b8fabe600ca90999beaefdb7` |
| [laravel/framework](https://github.com/laravel/framework) | PHP | 100 | `dd4184fd9306b5b09286689cbad256cf4a8abb6c` |
| [symfony/symfony](https://github.com/symfony/symfony) | PHP | 100 | `ad1bfbb2c5eceddca368790aacc545baaa44bf2d` |
| [django/django](https://github.com/django/django) | Python | 89 | `3d3d943b7442f1f5278ed876331a06047fa96ea8` |
| [pallets/flask](https://github.com/pallets/flask) | Python | 94 | `d086db856be187255b8ec61ef409357393020f32` |
| [pallets/werkzeug](https://github.com/pallets/werkzeug) | Python | 100 | `665e760ca6325a348ce03e5cf780b17e4be01848` |
| [pyca/cryptography](https://github.com/pyca/cryptography) | Python | 100 | `f7295d634f8388edc3625d039513c72e4384431c` |
| [rack/rack](https://github.com/rack/rack) | Ruby | 95 | `412b7e5250612e8b23095eee65ee3268addb4776` |
| [rails/rails](https://github.com/rails/rails) | Ruby | 91 | `0f19d01ab94a6a7d8d5021585aaa9a3a9a39e3f5` |
| [ruby/rexml](https://github.com/ruby/rexml) | Ruby | 89 | `0fee9c5bfab3ae311ed5958ec760db19a2c95eeb` |
| [sinatra/sinatra](https://github.com/sinatra/sinatra) | Ruby | 84 | `cb22afd7902b566b6eaba6c4ea89739494a65d12` |
| [actix/actix-web](https://github.com/actix/actix-web) | Rust | 85 | `2db7119a990511e90e234d8ba118234b51bce68a` |
| [hyperium/hyper](https://github.com/hyperium/hyper) | Rust | 94 | `b07337878fe57b34b2065335ae8cae9ce5a780a0` |
| [rustls/rustls](https://github.com/rustls/rustls) | Rust | 90 | `73650cc7f7d8b280932f554c9032a14a8f9b71f5` |
| [tokio-rs/tokio](https://github.com/tokio-rs/tokio) | Rust | 96 | `cffdc7601134598cebc45d03af0358dedfcb3ff1` |
| [angular/angular](https://github.com/angular/angular) | TypeScript | 90 | `d0b33ad25f9625a6bce303c2b8b29472cceb62b9` |
| [nestjs/nest](https://github.com/nestjs/nest) | TypeScript | 96 | `62647d3ec95e816a4556b3e04106eb4af002b4b8` |
| [vitejs/vite](https://github.com/vitejs/vite) | TypeScript | 94 | `6f2730eacae327cc2ce95c87509b7e7779c615e0` |

## 分布

- C: 5
- C#: 4
- C++: 5
- Elixir: 4
- Go: 4
- Java: 4
- JavaScript: 5
- PHP: 4
- Python: 4
- Ruby: 4
- Rust: 4
- TypeScript: 3

## 限制

- 分数只覆盖已采集的元数据、CI 列表、测试 workflow、release/tag 和单个修复 diff，不构成代码审计。
- GitHub Releases 为空的 6 个仓库使用 tag/changelog 证据，已在 decisions 中标记 `tag_source`；未把 tag 当日发包。
- `head_sha_observed` 是浅克隆看到的分支 HEAD，不等于最终评测快照；评测快照必须绑定已验证漏洞并由 P5 流程选择。
- 仍需独立复核者、全量漏洞核验、快照语言盘点与真值矩阵，才能进入正式发布。

