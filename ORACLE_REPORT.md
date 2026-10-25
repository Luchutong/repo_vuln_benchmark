# ORACLE_REPORT — 唯一评测快照的版本真值

> **2026-10-23 注**：本文件是 2026-10-22 的快照记录，下表已过时。当前 live Oracle 为
> 23 个评测快照、60 条 `confirmed_affected`（55 B + 5 A）；django 已由 3.0.2 切到 4.2.13
> （CVE-2024-39330），rack 已由 2.2.3 切到 v3.1.13（CVE-2025-46727），libexpat 已由 R_2_4_4 切到
> R_2_6_2（CVE-2024-45490），phoenix 已由 v1.6.13 切到 v1.8.8（CVE-2026-56811、CVE-2026-56812），
> 旧的 8+2+7+2 条状态行已归档。
> 当前权威计数与说明见 `HANDOFF_V031.md` §2、`LIMITATIONS_V031.md` §2 与
> `v031/reports/SELECTION_TABLE.md`。

生成时间：2026-10-22T01:55:00Z；依据 `v03/WORKFLOW.md` §6、`v03/docs/DATA_CONTRACT.md`。

## 1. 范围

- `data/snapshot_vulnerability_status.jsonl` 只保留 22 个 `evaluation_target=true` 快照上的状态行。
- 状态行 73 条，全部 `confirmed_affected`；`confirmed_not_affected`、`unknown`、`out_of_scope` 均为 0。
- 迁移没有把任何历史状态行移出正式矩阵（`historical_snapshot_status.jsonl` 为空），因为 22 个旧目标全部原样保留。
- 28 个没有评测目标的仓库在 Oracle 中没有行；它们不是“无漏洞”，而是 `needs_selection`。

## 2. 逐仓库真值

| repo_id | 仓库 | 评测 snapshot | commit SHA | confirmed_affected | confirmed_not_affected | unknown | out_of_scope |
|---|---|---|---|---:|---:|---:|---:|
| 569041 | curl/curl | `snap_0ec1c11542393304` | `6fa1d817e5b1a00d7d0c8168091877476b499317` | 2 | 0 | 0 | 0 |
| 54280778 | DaveGamble/cJSON | `snap_d9525608880dc9e1` | `cb8693b058ba302f4829ec6d03f609ac6f848546` | 1 | 0 | 0 | 0 |
| 4164482 | django/django | `snap_ab695ba3db678939` | `a36974395ebc03a41928db1743074575b143330d` | 8 | 0 | 0 | 0 |
| 237159 | expressjs/express | `snap_3166f788b2c56baa` | `b28db2c12c3bd9cd763316824446f79bf81e0686` | 1 | 0 | 0 | 0 |
| 20904437 | gin-gonic/gin | `snap_d4899c7054105aea` | `15ced05c5316609bce5b43389f8e3f06102a8b18` | 1 | 0 | 0 | 0 |
| 1420053 | guzzle/guzzle | `snap_efe695448113758a` | `e3ff079b22820c2029d4c2a87796b6a0b8716ad8` | 2 | 0 | 0 | 0 |
| 23500865 | hyperium/hyper | `snap_735b41cb13177d03` | `8861f9a7867216c81ea14ac6224c11a1303e7761` | 1 | 0 | 0 | 0 |
| 3476845 | JamesNK/Newtonsoft.Json | `snap_25561773eac9d84f` | `7c3d7f8da7e35dde8fa74188b0decff70f8f10e3` | 1 | 0 | 0 | 0 |
| 1103607 | jenkinsci/jenkins | `snap_d9b0ffa82cd068d0` | `3b0de10df3bedba515e13032104d4d84f83045be` | 6 | 0 | 0 | 0 |
| 7548986 | laravel/framework | `snap_6e1f42aa46ca4df5` | `dff716442d9c229d716be82ccc9a7de52eb97193` | 1 | 0 | 0 | 0 |
| 3219804 | libarchive/libarchive | `snap_a47bcab3f2c97e92` | `b439d586f53911c84be5e380445a8a259e19114c` | 1 | 0 | 0 | 0 |
| 80314213 | libexpat/libexpat | `snap_d33251dac37c334c` | `81b89678e200820271b72cacdd45fb5868855765` | 7 | 0 | 0 | 0 |
| 1064563 | netty/netty | `snap_bb344e672a0544ef` | `97d044812dc84288ea2c44c0862c5b1c26cb5b2d` | 6 | 0 | 0 | 0 |
| 133092972 | nodejs/undici | `snap_24c4a191fd049fc3` | `f5c89e5c87c7d702996b152c4ad86302b60c4181` | 3 | 0 | 0 | 0 |
| 596892 | pallets/flask | `snap_8ed1cab47a0b7011` | `721abdc3810057269503a72d2db80fb826f3c85c` | 1 | 0 | 0 | 0 |
| 997338 | pallets/werkzeug | `snap_b57262de7996e8a2` | `d70dcea305bf842c5a3b55265b5ffac2db012e23` | 1 | 0 | 0 | 0 |
| 16072585 | phoenixframework/phoenix | `snap_ee79f4175242bbee` | `6234b576b94476f285a3397c0a9c5a610d1cdb67` | 2 | 0 | 0 | 0 |
| 23357588 | protocolbuffers/protobuf | `snap_6bc3f36eb61ef280` | `21027a27c4c2ec1000859ccbcfff46d83b16e1ed` | 3 | 0 | 0 | 0 |
| 96071 | rack/rack | `snap_f97687a4e0807cb2` | `1741c580d71cfca8e541e96cc372305c8892ee74` | 2 | 0 | 0 | 0 |
| 57920736 | rustls/rustls | `snap_b3a6891886ef2160` | `1dee8b13134d877ade94dda7b68c7bf072e18d62` | 1 | 0 | 0 | 0 |
| 458058 | symfony/symfony | `snap_39105a8a3ceb9fe4` | `2b66d7d7d8129531229708ef708860844db91944` | 18 | 0 | 0 | 0 |
| 257485422 | vitejs/vite | `snap_2e50b228f2432623` | `b44c49302ffbf0c82f984f6219ed6376d1e4552a` | 4 | 0 | 0 | 0 |

## 3. 证据绑定

每条 `confirmed_affected` 在 v0.3 validator 下满足：

- `evidence_ids` 非空，且每条证据 `result=PASS`；
- `proof_summary` 非空；
- `(snapshot_id, vulnerability_id)` 在同 SHA 的 `locations` 中存在。
  22 个目标共 73 条正样本，全部有同 SHA 位置记录。

根因定位与复核材料在 `runs/verification/` 与 `runs/independent/`，迁移时整目录复制，未改写。

## 4. 为什么没有 `unknown` / `out_of_scope`

22 个被选仓库的 Catalog 恰好等于已提升的 73 条漏洞，而这些漏洞在 v0.2 中都已经在该快照上验证为
`confirmed_affected`。没有出现“Catalog 有、当前 SHA 尚未判定”的行，所以不需要填 `unknown`。
这不是“已证明这些版本没有其他漏洞”：Catalog 本身不完整（50/50 `NEEDS_REVIEW`、`PASS_KNOWN_SWEEP=0`），
未收录的漏洞不会被记成 `confirmed_not_affected`。

## 5. 冲突与注意事项

- 20 条已有 verdict 的 pending 候选不在 Oracle 中；它们尚未通过提升门槛。
- `CVE-2026-44487`（axios）与 `CVE-2021-21409`（netty）是重复公告，候选保持 `pending_location`，
  不作为第二条 Oracle 行。
- rack CVE-2025-46727、CVE-2025-61772 的档案与材料已存在，但没有完成独立复核/提升，未进入 Oracle。
- 冻结评测的 `oracle_version` 尚未产生；本轮 Oracle 是 draft 快照，不是发布版本。
