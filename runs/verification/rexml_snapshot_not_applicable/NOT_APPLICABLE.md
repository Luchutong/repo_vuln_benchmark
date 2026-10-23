# rexml v3.4.1 — 剩余 8 条候选的快照相关性判定

- 快照：`snap_23dff8507560a593`，tag `v3.4.1`，commit `bfb37e9ca4cb974c9bb2dc2f06e1202719d1bc4d`
  （2025-02-16）。
- 对象：rexml 候选池中尚未 triage 的 8 条（7 个 distinct CVE + 1 条同 CVE 的重复 advisory 行）。
- 判定方法（只用于**排除**，不用于声明快照无漏洞）：
  1. 从 OSV 读取该 advisory 的 affected range（`introduced 0` → `fixed X`）；
  2. 在完整 clone（`scratch/rexml_full_2026-10-23`）中确认修复发布 tag 的 commit 是快照 commit 的祖先；
  3. 对 advisory 给出 fix commit 的条目，逐条确认 fix commit 也是快照 commit 的祖先；
  4. 因此快照包含该 advisory 声明的全部修复代码，落在 affected range 之外。

## 逐条结果

| 候选 | CVE | OSV fixed | 修复 tag（peeled commit） | 修复 commit 祖先 | 判定 |
|---|---|---|---|---|---|
| `disc2_5a65131bd3dd9c4ea948f8e8` | CVE-2021-28965 | 3.2.5 | `v3.2.5` = `a622645e980ea5b91ad7b4d6fec32d113f15df88` | advisory 列的 7 个 commit（`2fe62e2`、`3c137eb`、`6a250d2`、`9b311e5`、`a659c63`、`f7bab89`、`f9d88e4`）全部是祖先 | confirmed_not_affected |
| `disc2_a64b411ffb1b9eed257f20a7` | CVE-2024-35176 | 3.2.7 | `v3.2.7` = `085def07425561862d8329001168d8bc9c75ae8f` | `4325835f92f3f142ebd91a3fdba4e1f1ab7f1cfb`（quoted attributes in chunks） | confirmed_not_affected |
| `disc2_3f62ede0b25591316bf13bd6` | CVE-2024-39908 | 3.3.2 | `v3.3.2` = `2b285ac0804f2918de642f7ed4646dc6d645a7fc` | advisory 未给 commit；该 release 内的 ReDoS 修复 `910e5a2`、`1f1e6e9`、`67efb59`、`0af55fa` 均为祖先 | confirmed_not_affected |
| `disc2_6a93fc1123eaf1281246d40b` | CVE-2024-41123 | 3.3.3 | `v3.3.3` = `e4a067e11235a2ec7a00616d41350485e384ec05` | advisory 未给 commit；该 release 内的 `033d190`、`6cac15d`、`2bca7bd` 等修复均为祖先 | confirmed_not_affected |
| `disc2_d59500836deffa78daecb7d7` | CVE-2024-41946 | 3.3.3 | `v3.3.3` = `e4a067e11235a2ec7a00616d41350485e384ec05` | `033d1909a8f259d5a7c53681bcaf14f13bcf0368`（entity expansion limit） | confirmed_not_affected |
| `disc2_78f9100d542890ddeca2013a` | CVE-2024-43398 | 3.3.6 | `v3.3.6` = `95871f399eda642a022b03550479b7994895c742` | `7cb5eaeb221c322b9912f724183294d8ce96bae3`（namespace conflicted attribute check） | confirmed_not_affected |
| `disc2_860cbeb640c57dcc85a303d1` | CVE-2024-49761 | 3.3.9 | `v3.3.9` = `38eaa86ac7abe0d31cf49d8df57ad239fdeb80e9` | `ce59f2eb1aeb371fe1643414f06618dbe031979f`（`&#0x...;` character reference） | confirmed_not_affected |
| `adv3_28ebc75b9dbc99b4` | CVE-2024-49761（重复行） | 3.3.9 | 同上 | 同上 | confirmed_not_affected |

## 依据与复算

- OSV：`https://api.osv.dev/v1/vulns/<GHSA>`（2026-10-22 读取）；NVD 与 ruby-lang 公告作为交叉来源。
- 复算命令（完整 clone）：
  ```bash
  git rev-list -n1 v3.3.9                       # 38eaa86…
  git merge-base --is-ancestor 38eaa86… bfb37e9 # exit 0
  git merge-base --is-ancestor ce59f2e… bfb37e9 # exit 0
  ```
- 结论仅表示：这 7 个 advisory 声明的修复在 v3.4.1 中已存在，候选不适用于该快照。
  它**不**证明 v3.4.1 无其他漏洞，也不构成 `PASS_KNOWN_SWEEP`；本快照仍只有 1 条已确认正样本
  （CVE-2025-58767）。
