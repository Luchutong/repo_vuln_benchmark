# 仓库准入与选择报告

种子 180 个；已取得真实 GitHub 元数据 180 个；迁移/名称修正 9 处；归档/禁用暂缓 3 个。
按 WORKFLOW 六项质量门槛评分后，**50 个仓库 PASS**（分数 77–100，未使用 75 分以下的仓库）。
主语言分布：C: 5, C#: 4, C++: 5, Elixir: 4, Go: 4, Java: 4, JavaScript: 5, PHP: 4, Python: 4, Ruby: 4, Rust: 4, TypeScript: 3，共 12 种；每种 3–5 个仓库，无单一语言超过 10/50。

评分基于记录的 API/克隆/CI/发行/tag/安全修复观察，是准入门槛，不是代码审计，不能证明不存在漏洞。逐仓库六维分数、证据链接和限制见 `runs/admission/decisions.jsonl` 与 `data/repositories.jsonl`。

| 仓库 | 主语言 | GitHub numeric ID | 分数 |
|---|---|---|---:|
| [aaubry/YamlDotNet](https://github.com/aaubry/YamlDotNet) | C# | 6181245 | 96 |
| [actix/actix-web](https://github.com/actix/actix-web) | Rust | 105379569 | 85 |
| [angular/angular](https://github.com/angular/angular) | TypeScript | 24195339 | 90 |
| [apache/tomcat](https://github.com/apache/tomcat) | Java | 2493904 | 84 |
| [axios/axios](https://github.com/axios/axios) | JavaScript | 23088740 | 100 |
| [caddyserver/caddy](https://github.com/caddyserver/caddy) | Go | 29207621 | 96 |
| [curl/curl](https://github.com/curl/curl) | C | 569041 | 100 |
| [DaveGamble/cJSON](https://github.com/DaveGamble/cJSON) | C | 54280778 | 89 |
| [django/django](https://github.com/django/django) | Python | 4164482 | 89 |
| [dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) | C# | 17620347 | 91 |
| [elixir-ecto/ecto](https://github.com/elixir-ecto/ecto) | Elixir | 10649374 | 83 |
| [elixir-plug/plug](https://github.com/elixir-plug/plug) | Elixir | 14421569 | 94 |
| [elixir-plug/plug_cowboy](https://github.com/elixir-plug/plug_cowboy) | Elixir | 153667429 | 83 |
| [expressjs/express](https://github.com/expressjs/express) | JavaScript | 237159 | 100 |
| [gin-gonic/gin](https://github.com/gin-gonic/gin) | Go | 20904437 | 100 |
| [go-gitea/gitea](https://github.com/go-gitea/gitea) | Go | 72495579 | 100 |
| [grpc/grpc](https://github.com/grpc/grpc) | C++ | 27729880 | 100 |
| [guzzle/guzzle](https://github.com/guzzle/guzzle) | PHP | 1420053 | 100 |
| [hyperium/hyper](https://github.com/hyperium/hyper) | Rust | 23500865 | 94 |
| [JamesNK/Newtonsoft.Json](https://github.com/JamesNK/Newtonsoft.Json) | C# | 3476845 | 78 |
| [jbeder/yaml-cpp](https://github.com/jbeder/yaml-cpp) | C++ | 33100064 | 94 |
| [jenkinsci/jenkins](https://github.com/jenkinsci/jenkins) | Java | 1103607 | 100 |
| [labstack/echo](https://github.com/labstack/echo) | Go | 31504491 | 100 |
| [laravel/framework](https://github.com/laravel/framework) | PHP | 7548986 | 100 |
| [leethomason/tinyxml2](https://github.com/leethomason/tinyxml2) | C++ | 3542607 | 77 |
| [libarchive/libarchive](https://github.com/libarchive/libarchive) | C | 3219804 | 96 |
| [libexpat/libexpat](https://github.com/libexpat/libexpat) | C | 80314213 | 91 |
| [lodash/lodash](https://github.com/lodash/lodash) | JavaScript | 3955647 | 95 |
| [nestjs/nest](https://github.com/nestjs/nest) | TypeScript | 80945428 | 96 |
| [netty/netty](https://github.com/netty/netty) | Java | 1064563 | 91 |
| [nlohmann/json](https://github.com/nlohmann/json) | C++ | 11171548 | 84 |
| [nodejs/undici](https://github.com/nodejs/undici) | JavaScript | 133092972 | 100 |
| [openssl/openssl](https://github.com/openssl/openssl) | C | 7634677 | 100 |
| [pallets/flask](https://github.com/pallets/flask) | Python | 596892 | 94 |
| [pallets/werkzeug](https://github.com/pallets/werkzeug) | Python | 997338 | 100 |
| [phoenixframework/phoenix](https://github.com/phoenixframework/phoenix) | Elixir | 16072585 | 100 |
| [PHPMailer/PHPMailer](https://github.com/PHPMailer/PHPMailer) | PHP | 2253830 | 100 |
| [protocolbuffers/protobuf](https://github.com/protocolbuffers/protobuf) | C++ | 23357588 | 96 |
| [pyca/cryptography](https://github.com/pyca/cryptography) | Python | 11939484 | 100 |
| [rack/rack](https://github.com/rack/rack) | Ruby | 96071 | 95 |
| [rails/rails](https://github.com/rails/rails) | Ruby | 8514 | 91 |
| [ruby/rexml](https://github.com/ruby/rexml) | Ruby | 135525225 | 89 |
| [rustls/rustls](https://github.com/rustls/rustls) | Rust | 57920736 | 90 |
| [sinatra/sinatra](https://github.com/sinatra/sinatra) | Ruby | 106995 | 84 |
| [SixLabors/ImageSharp](https://github.com/SixLabors/ImageSharp) | C# | 72174164 | 94 |
| [spring-projects/spring-framework](https://github.com/spring-projects/spring-framework) | Java | 1148753 | 95 |
| [symfony/symfony](https://github.com/symfony/symfony) | PHP | 458058 | 100 |
| [tokio-rs/tokio](https://github.com/tokio-rs/tokio) | Rust | 67836789 | 96 |
| [vercel/next.js](https://github.com/vercel/next.js) | JavaScript | 70107786 | 100 |
| [vitejs/vite](https://github.com/vitejs/vite) | TypeScript | 257485422 | 94 |
