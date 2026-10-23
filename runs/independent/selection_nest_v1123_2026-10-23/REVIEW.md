# Independent Selection Review — nestjs/nest @ v11.2.3

- **review_id**: `selrev_80945428_snap_af37094ca730365c`
- **repo_id**: 80945428
- **full_name**: nestjs/nest
- **snapshot_id**: `snap_af37094ca730365c`
- **tag_or_release**: v11.2.3
- **commit_sha**: `2b36ee5fea13dedcedfd9815a9c193b2d21130c1`
- **reviewed_by**: `independent-selection-reviewer-nest-2026-10-23`
- **reviewed_at**: 2026-10-23T00:04:29Z
- **VERDICT**: **ACCEPT**

Reviewed only the assigned packet, the export archive/manifest, a fresh public clone, and my own `/tmp` scratch. No other review/verification material was read.

## 1. Tag resolution

Command (with proxy `http://172.21.96.1:7890`):

```
git ls-remote --tags https://github.com/nestjs/nest
```

Relevant refs:

```
56ebf18f91fadf4ef606dacd2ce01c19def1e47   refs/tags/v11.2.3
2b36ee5fea13dedcedfd9815a9c193b2d21130c1   refs/tags/v11.2.3^{}
```

Fresh bare clone at `/tmp/nest_clone/nest.git`:

- `git cat-file -t 56ebf18f...` -> `tag` (**annotated tag**, not lightweight). Tag object content:
  `object 2b36ee5fea13dedcedfd9815a9c193b2d21130c1 / type commit / tag v11.2.3 / tagger Kamil Myśliwiec 1787655522 +0200`.
- Peeled commit `2b36ee5f...` == packet `commit_sha`. **Match.**
- `git rev-parse 2b36ee5f^{tree}` -> `a4bc24860e31c7ace6a133d4acc64c7faeb55659` == packet tree. **Match.**
- Commit date: `2026-08-25 12:58:35 +0200` = `2026-08-25T10:58:35Z`. Message: `chore(release): publish v11.2.3 release`.
- Tag object date: `1787655522 +0200` = `2026-08-25T10:58:42Z`.
- GitHub Releases API (`/repos/nestjs/nest/releases/tags/v11.2.3`): `prerelease=false`, `draft=false`, published `2026-08-25T10:59:41Z`. **Stable release, not a pre-release/dist tag.**

## 2. Archive integrity

| item | expected (packet) | measured | ok |
|---|---|---|---|
| archive sha256 | `b432e7ea89892f28e64e68c9e171e1f86ca4dc5b3d4fa0e612c51dd5dff0d5d8` | same | yes |
| archive bytes | 1155352 | 1155352 | yes |
| manifest sha256 | `3ca2f8780bb1e4240ba025d6748fbd6a2df3da6753348b2692d638c905814573` | same | yes |

- Tar listing: 2141 entries, **all regular files** (2121 `-rw-r--r--`, 20 `-rwxr-xr-x`), **0 symlinks**, **0 directories**, no `.git` directory or gitlink entries.
- Unpacked to `/tmp/nest_snap` (fresh empty dir): 2141 files, 0 symlinks.
- Counts reconcile: `2141 exported + 0 symlink + 0 gitlink = 2141 = tree_file_count`.

## 3. Tree / commit agreement

- `git rev-parse 2b36ee5f^{tree}` = `a4bc24860e31c7ace6a133d4acc64c7faeb55659` (packet `tree_sha`). **Match.**
- `git ls-tree -r 2b36ee5f` -> 2141 entries, all `blob`, modes 2121×`100644` + 20×`100755`.
- **All 2141 manifest entries were cross-checked** (not just a sample) against the git tree and the extracted bytes:
  - path sets identical (no missing / no extra),
  - `mode` (manifest `0644`/`0755`) matches `ls-tree` mode,
  - `size` matches actual file length,
  - `sha256` matches measured sha256 of the extracted bytes,
  - computed git blob sha1 (`sha1("blob <len>\0"+content)`) matches the `ls-tree` blob sha1.
  - **Result: 0 mismatches out of 2141.**
- Note: the manifest schema has no explicit `blob sha1` field; blob sha1 was derived from content and checked against `ls-tree`.

## 4. Known positive at this snapshot

Public sources (all fetched via the proxy):

| source | URL | range containing 11.2.3 | affected |
|---|---|---|---|
| GitHub Advisory API | `https://api.github.com/advisories/GHSA-m8vh-jmq9-5rjg` | `@nestjs/microservices` `< 11.2.4` (first patched 11.2.4) | yes |
| OSV | `https://api.osv.dev/v1/vulns/CVE-2026-102281` (and `.../GHSA-m8vh-jmq9-5rjg`) | `versions` lists `v11.2.3`; introduced 0, fixed 11.2.4 | yes |
| NVD | `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-102281` | CVSS 3.1 7.5 HIGH, matches GHSA | yes |
| CVE.org (CNA GitHub_M) | `https://cveawg.mitre.org/api/cve/CVE-2026-102281` | `nest/nestjs` `< 11.2.4` | yes |

Fix-commit ancestry (fresh clone):

- `d5046225...` (v11.2.4), `ee168a56...` (v12.0.2), `aa97b514...`, `e9dcd4c7...` — **all NOT ancestors** of `2b36ee5f`.
- `2b36ee5f` **IS an ancestor** of v11.2.4 -> snapshot predates the fix.
- v11.2.4 release commit is `2026-09-14 20:13:13 +0200`; fix `e9dcd4c7` is `2026-09-14 16:06:12 +0200` ("fix(microservices): handle unserializable patterns without crashing").

Vulnerable code in the **exported tree**:

- `packages/microservices/server/server-tcp.ts`, lines 95-97:
  ```
  95:    const pattern = !isString(packet.pattern)
  96:      ? JSON.stringify(packet.pattern)
  97:      : packet.pattern;
  ```
  The unguarded `JSON.stringify(packet.pattern)` is **line 96**.
- `packages/microservices/server/server-rmq.ts`, line 302: `: JSON.stringify(packet.pattern);`.
- The fix's `Server#getPatternAsString` guard is **absent** from the tree (`grep -rn getPatternAsString packages/microservices` -> no hits).
- The TCP `'message'` listener at `server-tcp.ts:85` calls `this.handleMessage(...)` without a rejection handler, matching the advisory's unhandled-rejection mechanism.
- `packages/microservices/package.json` version = `11.2.3`.

## 5. Build

- Toolchain: node v24.16.0, npm 11.13.0.
- `npm ci --legacy-peer-deps --ignore-scripts` -> exit **0** (only `npm audit` advisory output).
- `./node_modules/.bin/tsc -b packages` -> exit **0**, no diagnostics.
- `build_ok: true`.

## 6. Sanity of the selection

- `2b36ee5f` is the release commit `chore(release): publish v11.2.3 release` and is the tag target — a coherent single release, not a branch head.
- v11.2.3 (2026-08-25) is older than the fix (2026-09-14) and than v11.2.4, so the tag is **not newer than the fix**.
- v11.2.3 is a stable, non-prerelease, non-draft release.
- Minor, non-blocking observation: monorepo root `package.json` is `@nestjs/core` 11.1.26 while `packages/microservices/package.json` is 11.2.3. This is the repo's per-package Lerna versioning (v11.2.4 likewise carries microservices 11.2.4), so the tag unambiguously denotes the affected package.

## Discrepancies

None. Everything the packet asserted that I could independently check matched.

## Limitations / not verified

- NVD `configurations` (CPE) were empty in the API response; the affected range was taken from the CNA/GHSA metadata and the CVE record text. This does not weaken the anchor because the CVE/GHSA/OSV ranges agree and the vulnerable code is directly present at the commit.
- Did not bisect the lower bound / exact first-affected version (out of scope; the packet itself records the lower bound as "introduced 0").
- The vulnerable behaviour was not executed (a PoC reproduction was not required by this review); the anchor `affected=true` rests on published ranges plus the presence of the exact unguarded code path at the exported commit.
