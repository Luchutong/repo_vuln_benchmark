# OpenSSL CVE-2022-0778：未提升的探查记录（保留，不进入真值表）

状态：**UNPROMOTED / 不作为验证漏洞**。本目录只保存探查阶段的一手材料，没有 `dossier.json`，
也没有独立复核，因此不会进入 `data/vulnerabilities.jsonl`、`data/reviews.jsonl` 或状态矩阵。

未提升的原因：

1. `data/candidates.jsonl` 中没有 CVE-2022-0778 的候选行。提升流程要求 dossier 来自真实候选，
   不能为了凑数临时造一条候选。
2. 修复提交的映射存在分支差异：master 上的 `3118eb6...` 不是 3.0.2 tag 的祖先；3.0 分支的
   `a466912611aa...` 是 3.0.2 的祖先、不是 3.0.1 的祖先。该差异记录在
   `sources/git_object_checks.txt`，但尚未按候选核验流程逐字段闭环。
3. 没有独立 reviewer verdict。

已保留的证据：

- `sources/cve_v5.json`、`sources/nvd_cve.json`：公告身份与评分来源。
- `sources/bn_sqrt_3.0.1.c`、`sources/bn_sqrt_3.0.2.c`：两个 tag 的 `crypto/bn/bn_sqrt.c` 内容。
- `sources/git_object_checks.txt`：tag/commit 身份、修复提交可达性检查。

关联快照：`runs/language/snap_10d458b485bb6210`（openssl/openssl，tag `openssl-3.0.1`，
commit `b4e83ed7cd99c12d27e0e220c3afa1745a68f921`，24,247 个 tracked files）。该快照是真实的
语言盘点观察，但 `evaluation_target=false`，不被任何已验证漏洞引用；它因此作为非评测快照保留，
不构成真值声明。若后续补齐候选与独立复核，可从这份材料继续。
