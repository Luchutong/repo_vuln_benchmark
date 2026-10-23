# SELECTION_REPORT — RepoVuln-50 v0.3 评测目标选择

生成时间：2026-10-22T01:55:00Z；数据根目录：`/home/luchitong/work/repo-vuln-50-v03`。
依据：`v03/WORKFLOW.md` §5–§6、`v03/docs/MIGRATION_GUIDE.md` 步骤 2/4。

本报告只记录迁移后的**现状与依据**。迁移脚本把 22 个 v0.2 评测快照原样保留为 v0.3 `proposed` 目标，
没有把任何一条自动升级为 `frozen`，也没有为 28 个无目标仓库编造评测 SHA。

## 1. 统计口径

| 项目 | 数值 |
|---|---:|
| 准入仓库 | 50 |
| 已存 snapshots | 75（每仓至少一条 HEAD 全量扫描快照） |
| v0.2 `evaluation_target=true` | 22 |
| 这些目标实际覆盖的仓库数 | 22（按 repo_id 统计，不是假设） |
| 旧目标数为 0 的仓库 | 28 |
| 旧目标数为 2 及以上的仓库（AMBIGUOUS） | 0 |
| `evaluation_selection` 行 | 22，全部 `decision_status=proposed` |
| `decision_status=frozen` | 0 |
| 仓库 `evaluation_snapshot_id` 非空 | 22 |
| 仓库 `evaluation_snapshot_id` 为空 | 28 |

结论：不存在“一个仓库多个旧评测目标”的歧义，因此本次迁移不需要人工 `--selections` 覆盖。
但 28 个仓库没有任何可验证目标，v0.3 要求的“每仓恰好一个正式评测 Snapshot”只完成了 22/50。

## 2. 已保留的 22 个 proposed 评测目标

| repo_id | 仓库 | 主语言 | 评测 snapshot | commit SHA | 稳定 tag | positives | 语言数 | 决策 |
|---|---|---|---|---|---|---:|---:|---|
| 569041 | curl/curl | C | `snap_0ec1c11542393304` | `6fa1d817e5b1a00d7d0c8168091877476b499317` | curl-8_3_0 | 2 | 63 | proposed |
| 54280778 | DaveGamble/cJSON | C | `snap_d9525608880dc9e1` | `cb8693b058ba302f4829ec6d03f609ac6f848546` | v1.7.16 | 1 | 36 | proposed |
| 4164482 | django/django | Python | `snap_ab695ba3db678939` | `a36974395ebc03a41928db1743074575b143330d` | 3.0.2 | 8 | 65 | proposed |
| 237159 | expressjs/express | JavaScript | `snap_3166f788b2c56baa` | `b28db2c12c3bd9cd763316824446f79bf81e0686` | 4.19.2 | 1 | 28 | proposed |
| 20904437 | gin-gonic/gin | Go | `snap_d4899c7054105aea` | `15ced05c5316609bce5b43389f8e3f06102a8b18` | v1.5.0 | 1 | 20 | proposed |
| 1420053 | guzzle/guzzle | PHP | `snap_efe695448113758a` | `e3ff079b22820c2029d4c2a87796b6a0b8716ad8` | 7.4.4 | 2 | 27 | proposed |
| 23500865 | hyperium/hyper | Rust | `snap_735b41cb13177d03` | `8861f9a7867216c81ea14ac6224c11a1303e7761` | v0.14.2 | 1 | 12 | proposed |
| 3476845 | JamesNK/Newtonsoft.Json | C# | `snap_25561773eac9d84f` | `7c3d7f8da7e35dde8fa74188b0decff70f8f10e3` | 12.0.3 | 1 | 20 | proposed |
| 1103607 | jenkinsci/jenkins | Java | `snap_d9b0ffa82cd068d0` | `3b0de10df3bedba515e13032104d4d84f83045be` | jenkins-2.441 | 6 | 80 | proposed |
| 7548986 | laravel/framework | PHP | `snap_6e1f42aa46ca4df5` | `dff716442d9c229d716be82ccc9a7de52eb97193` | v11.30.0 | 1 | 35 | proposed |
| 3219804 | libarchive/libarchive | C | `snap_a47bcab3f2c97e92` | `b439d586f53911c84be5e380445a8a259e19114c` | v3.7.7 | 1 | 34 | proposed |
| 80314213 | libexpat/libexpat | C | `snap_d33251dac37c334c` | `81b89678e200820271b72cacdd45fb5868855765` | R_2_4_4 | 7 | 40 | proposed |
| 1064563 | netty/netty | Java | `snap_bb344e672a0544ef` | `97d044812dc84288ea2c44c0862c5b1c26cb5b2d` | netty-4.1.59.Final | 6 | 47 | proposed |
| 133092972 | nodejs/undici | JavaScript | `snap_24c4a191fd049fc3` | `f5c89e5c87c7d702996b152c4ad86302b60c4181` | v5.19.0 | 3 | 30 | proposed |
| 596892 | pallets/flask | Python | `snap_8ed1cab47a0b7011` | `721abdc3810057269503a72d2db80fb826f3c85c` | 2.3.1 | 1 | 46 | proposed |
| 997338 | pallets/werkzeug | Python | `snap_b57262de7996e8a2` | `d70dcea305bf842c5a3b55265b5ffac2db012e23` | 3.0.2 | 1 | 34 | proposed |
| 16072585 | phoenixframework/phoenix | Elixir | `snap_ee79f4175242bbee` | `6234b576b94476f285a3397c0a9c5a610d1cdb67` | v1.6.13 | 2 | 41 | proposed |
| 23357588 | protocolbuffers/protobuf | C++ | `snap_6bc3f36eb61ef280` | `21027a27c4c2ec1000859ccbcfff46d83b16e1ed` | v3.20.1 | 3 | 110 | proposed |
| 96071 | rack/rack | Ruby | `snap_f97687a4e0807cb2` | `1741c580d71cfca8e541e96cc372305c8892ee74` | 2.2.3 | 2 | 19 | proposed |
| 57920736 | rustls/rustls | Rust | `snap_b3a6891886ef2160` | `1dee8b13134d877ade94dda7b68c7bf072e18d62` | v/0.23.4 | 1 | 23 | proposed |
| 458058 | symfony/symfony | PHP | `snap_39105a8a3ceb9fe4` | `2b66d7d7d8129531229708ef708860844db91944` | v5.4.45 | 18 | 54 | proposed |
| 257485422 | vitejs/vite | TypeScript | `snap_2e50b228f2432623` | `b44c49302ffbf0c82f984f6219ed6376d1e4552a` | v5.0.11 | 4 | 87 | proposed |

逐项依据（由实际数据计算，见 `runs/verification/` 与 `data/`）：

- **稳定 tag**：22 个目标全部带官方 tag/release（表中 `稳定 tag` 列），commit SHA 沿用 v0.2 的 tag peel 记录；
  本轮迁移没有重新访问 GitHub 复核 tag 指向。
- **同 SHA 正样本**：每个目标至少有 1 条 `confirmed_affected`，且 `known_positives_with_same_sha_location`
  与正样本数完全相等（22/22 仓库；合计 73 条）。
  即位置记录全部指向本 snapshot，不存在把别的 commit 的行号搬过来的情况。
- **复核等级**：73 条均为 grade B（静态归档 + 独立复核，未做动态 PoC）。
- **语言扫描**：22 个目标 `full_scan=true`；`language_tool` 记录为
  `github-linguist + explicit container extraction + versioned scope rules`，
  版本字段含 `github-linguist 9.7.0` 与 `inventory_snapshot.py` 的 sha256，
  语言条目 12–110 条/仓（见第 4 节）。
- **选择策略**：迁移脚本统一写 `selection_policy=documented_exception`，原因是这些目标继承自 v0.2，
  尚未经过 v0.3 的独立选版审查；不把它们包装成“预先登记的稳定发布版本”决策。

## 3. 28 个未选仓库（needs_selection）

| repo_id | 仓库 | 主语言 | 已存 snapshots（`sha` @ tag/HEAD，语言数） | 目录漏洞 | 候选 | 未解决 | 决策 |
|---|---|---|---|---:|---:|---:|---|
| 6181245 | aaubry/YamlDotNet | C# | `snap_4d89919118140399` = `4f7e6e346649…` @ HEAD（30 语言） | 0 | 1 | 1 | needs_selection |
| 105379569 | actix/actix-web | Rust | `snap_0c276eb0aa870861` = `2db7119a9905…` @ HEAD（26 语言） | 0 | 9 | 9 | needs_selection |
| 24195339 | angular/angular | TypeScript | `snap_55025ac2aa21eca5` = `d0b33ad25f96…` @ HEAD（115 语言） | 0 | 40 | 40 | needs_selection |
| 2493904 | apache/tomcat | Java | `snap_465320befa43dd91` = `ed8d6339035f…` @ HEAD（61 语言） | 0 | 41 | 41 | needs_selection |
| 23088740 | axios/axios | JavaScript | `snap_a64c7ddbbb7030b7` = `772a4e54ecc4…` @ v1.15.0（42 语言）<br>`snap_fe7a5e0c75c9adb3` = `fceeb10997ea…` @ HEAD（46 语言） | 0 | 67 | 67 | needs_selection |
| 29207621 | caddyserver/caddy | Go | `snap_5f7d6c5c600a7a23` = `f355b8687d55…` @ HEAD（32 语言） | 0 | 37 | 37 | needs_selection |
| 17620347 | dotnet/aspnetcore | C# | `snap_80fefe20d65e43c8` = `2d105dd1fd11…` @ HEAD（142 语言） | 0 | 68 | 68 | needs_selection |
| 10649374 | elixir-ecto/ecto | Elixir | `snap_b710ed5084cfdd8b` = `c0c99f51ef1d…` @ HEAD（17 语言） | 0 | 4 | 4 | needs_selection |
| 14421569 | elixir-plug/plug | Elixir | `snap_026a9d6d2a05c227` = `05bde7066c37…` @ HEAD（16 语言） | 0 | 11 | 11 | needs_selection |
| 153667429 | elixir-plug/plug_cowboy | Elixir | `snap_8dbd807d0794116d` = `87740b572913…` @ HEAD（7 语言） | 0 | 2 | 2 | needs_selection |
| 72495579 | go-gitea/gitea | Go | `snap_ea22360d9979a561` = `a8e1057f5e75…` @ HEAD（79 语言） | 0 | 293 | 293 | needs_selection |
| 27729880 | grpc/grpc | C++ | `snap_253685caf4acf508` = `8b32af3bf498…` @ HEAD（188 语言） | 0 | 8 | 8 | needs_selection |
| 33100064 | jbeder/yaml-cpp | C++ | `snap_1687bd0bf1463a00` = `c5e65360373d…` @ HEAD（46 语言） | 0 | 7 | 7 | needs_selection |
| 31504491 | labstack/echo | Go | `snap_402e978e7e168b5b` = `8fd0e184dd39…` @ HEAD（30 语言） | 0 | 16 | 16 | needs_selection |
| 3542607 | leethomason/tinyxml2 | C++ | `snap_e44b1fc3e39243d8` = `8224e427b655…` @ HEAD（26 语言） | 0 | 3 | 3 | needs_selection |
| 3955647 | lodash/lodash | JavaScript | `snap_b11ce93a0056bf2e` = `2b5e6f7399a7…` @ HEAD（33 语言） | 0 | 10 | 10 | needs_selection |
| 80945428 | nestjs/nest | TypeScript | `snap_ed2c874b73247465` = `62647d3ec95e…` @ HEAD（46 语言） | 0 | 12 | 12 | needs_selection |
| 11171548 | nlohmann/json | C++ | `snap_34320676e349f7c8` = `5e13f834c16d…` @ HEAD（70 语言） | 0 | 3 | 3 | needs_selection |
| 7634677 | openssl/openssl | C | `snap_10d458b485bb6210` = `b4e83ed7cd99…` @ openssl-3.0.1（54 语言）<br>`snap_e4cbee233ee774b4` = `63bd920445f5…` @ HEAD（85 语言） | 0 | 10 | 10 | needs_selection |
| 2253830 | PHPMailer/PHPMailer | PHP | `snap_d2e05d198fd4c8b3` = `c0b5268a626d…` @ HEAD（26 语言） | 0 | 18 | 18 | needs_selection |
| 11939484 | pyca/cryptography | Python | `snap_adf275f7449012d1` = `f7295d634f83…` @ HEAD（40 语言） | 0 | 43 | 43 | needs_selection |
| 8514 | rails/rails | Ruby | `snap_4e01b34117977bd4` = `0f19d01ab94a…` @ HEAD（88 语言） | 0 | 148 | 148 | needs_selection |
| 135525225 | ruby/rexml | Ruby | `snap_46e51fa7881b678a` = `0fee9c5bfab3…` @ HEAD（15 语言） | 0 | 9 | 9 | needs_selection |
| 106995 | sinatra/sinatra | Ruby | `snap_7787b0b03f0e0a7a` = `cb22afd7902b…` @ HEAD（32 语言）<br>`snap_916afbf76073e831` = `cafaab99db5b…` @ v3.0.3（29 语言） | 0 | 6 | 6 | needs_selection |
| 72174164 | SixLabors/ImageSharp | C# | `snap_0c6ea8e26fa18e71` = `a73c43da5a82…` @ HEAD（30 语言） | 0 | 16 | 16 | needs_selection |
| 1148753 | spring-projects/spring-framework | Java | `snap_40eb10dbcf0e3602` = `42c0a9bcc675…` @ HEAD（69 语言） | 0 | 84 | 84 | needs_selection |
| 67836789 | tokio-rs/tokio | Rust | `snap_f24ebe150d320916` = `cffdc7601134…` @ HEAD（20 语言） | 0 | 6 | 6 | needs_selection |
| 70107786 | vercel/next.js | JavaScript | `snap_c1ec8929758d53a4` = `a89c0afe5702…` @ HEAD（159 语言） | 0 | 86 | 86 | needs_selection |

未选原因：

1. 这些仓库的 Catalog 已验证漏洞数为 **0**，没有任何 `confirmed_affected` 可以支撑“该 SHA 至少一条 B/A 正样本”的选择规则。
   其中 25 个仓库只有默认分支 HEAD 快照（`tag_or_release=null`）；axios（v1.15.0）、OpenSSL（openssl-3.0.1）、
   sinatra（v3.0.3）另有带 tag 的历史快照，但同样没有已确认漏洞。
2. HEAD 不是稳定发布版本，也没有针对它的根因定位；带 tag 的 3 个历史快照也没有任何提升过的漏洞。
3. 它们确实有候选（合计 1058 条，全部未解决），
   但候选未通过提升门槛；按 v0.3 规则不能“先选版本再补证据”，也不能用候选数量反推版本。
4. 用户已明确本轮迁移后不再继续收集，因此这些仓库保持 `needs_selection`，不冻结、不伪造。

## 4. 正式快照语言覆盖（22 个 target）

| 仓库 | 全语言数 | first-party 编程/脚本语言 |
|---|---:|---|
| curl/curl | 63 | Batchfile, C, DIGITAL Command Language, Emacs Lisp, M4Sugar, Perl, Shell |
| DaveGamble/cJSON | 36 | C, Shell |
| django/django | 65 | JavaScript, Python |
| expressjs/express | 28 | Diff, JavaScript, Shell |
| gin-gonic/gin | 20 | Go |
| guzzle/guzzle | 27 | PHP |
| hyperium/hyper | 12 | Rust |
| JamesNK/Newtonsoft.Json | 20 | Batchfile, C#, JavaScript, PowerShell |
| jenkinsci/jenkins | 80 | ANTLR, C, Groovy, Java, JavaScript, Perl, Python, Ruby, Shell |
| laravel/framework | 35 | JavaScript, PHP, Shell |
| libarchive/libarchive | 34 | C, C++, M4Sugar, Shell |
| libexpat/libexpat | 40 | Batchfile, C, C++, Inno Setup, M4Sugar, Python, Ruby, Shell |
| netty/netty | 47 | C, Java, JavaScript, Shell |
| nodejs/undici | 30 | JavaScript, Shell |
| pallets/flask | 46 | Python |
| pallets/werkzeug | 34 | JavaScript, Python |
| phoenixframework/phoenix | 41 | Diff, Earthly, Elixir, Euphoria, HTML+EEX, JavaScript, Shell, ShellSession, Text |
| protocolbuffers/protobuf | 110 | Awk, Batchfile, C, C#, C++, Emacs Lisp, Java, JavaScript, Kotlin, M4, M4Sugar, NASL, Objective-C, PHP, Pawn, PowerShell, Python, Ruby, Shell, Starlark, Vim script |
| rack/rack | 19 | Ruby |
| rustls/rustls | 23 | Python, Rust, Shell |
| symfony/symfony | 54 | JavaScript, PHP, Shell, Twig |
| vitejs/vite | 87 | AppleScript, JavaScript, TSX, TypeScript |

说明：语言数来自 `snapshots.languages`，包含 first_party / test / tooling / vendored / generated / docs 等
全部作用域；表中 `first-party 编程/脚本语言` 只是其中一部分。完整明细在 `data/snapshots.jsonl`。

## 5. 距冻结还缺什么

| 冻结条件（`evaluation_selection` schema + validator） | 当前状态 |
|---|---|
| `decision_status=frozen` | 0/22 |
| `reviewed_by` 且与 `selected_by` 不同 | 未填 |
| `selection_reviewed_at` | 未填 |
| `approval_evidence_urls` | 未填 |
| `frozen_at` | null |
| `leakage_controls.worktree_without_git_history` | false |
| `leakage_controls.ground_truth_isolated` | false |
| `leakage_controls.network_policy` | `uncontrolled` |
| 构建可行性 / 工作树导出验证 | 未做 |
| 28 个仓库的评测 SHA | 未选（0 条已确认漏洞，无法按规则选） |

因此 `manifest.status` 保持 `draft`，`source_cutoff_date` 保持 null（迁移指南要求从 `discovery_coverage`
和采集日志复核后再填，不能用迁移当天日期顶替）。
