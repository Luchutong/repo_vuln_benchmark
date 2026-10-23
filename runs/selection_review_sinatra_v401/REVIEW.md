# Selection Review — sinatra/sinatra (repo_id 106995), snapshot snap_5ab17df9ee6e4957

- Review id: `selrev_106995_snap_5ab17df9ee6e4957_2026-10-23`
- Verdict: **accept**
- build_ok: **true** (personally observed `gem build sinatra.gemspec` succeed)
- Key discrepancy: none blocking. Two notes recorded (chronology of v4.0.1 vs v4.1.x; CNA/NVD not expressing a fixed version).

## 1. Tag resolution

Commands (proxy exported per isolation rules):

```
git ls-remote --tags https://github.com/sinatra/sinatra.git | grep -E 'refs/tags/v4\.(0\.1|1\.0|1\.1)(\^\{\})?$'
```

Output:

```
45c5d28952657c20ec7c85993a52a568a38ee9ba	refs/tags/v4.0.1
7dc5940e44cfa6d176b267f2165aa8116032669d	refs/tags/v4.0.1^{}
6e6f10010d9e446790d72fac88f5d282def82594	refs/tags/v4.1.0
73f3291d114b5b211e067263eeb9c0e197fe8500	refs/tags/v4.1.0^{}
a49be0975319aa8752e67636d67bc8b7e8320910	refs/tags/v4.1.1
7b50a1bbb5324838908dfaa00ec53ad322673a29	refs/tags/v4.1.1^{}
```

`git cat-file -t 45c5d28952657c20ec7c85993a52a568a38ee9ba` → `tag` (annotated).
Tag object points at `object 7dc5940e44cfa6d176b267f2165aa8116032669d`, `type commit`, tagger `zzak <zzak@hey.com>`, PGP-signed, message `4.0.1 release`.

Commit `7dc5940e44cfa6d176b267f2165aa8116032669d`:

```
tree b65107d8754b6a399d23ffd1330542e4d5c14e68
parent 0121b8cc4ea5b692d6e87b30b7def0707b90259b
author zzak <zzak@hey.com> 1748037697 +0900   (2025-05-24T07:01:37+09:00)
committer zzak <zzak@hey.com> 1748038533 +0900 (2025-05-24T07:15:33+09:00)
4.0.1 release
```

- Tag SHA (annotated object) = `45c5d28952657c20ec7c85993a52a568a38ee9ba`
- Peeled commit = `7dc5940e44cfa6d176b267f2165aa8116032669d` → **matches packet commit_sha**
- Commit tree = `b65107d8754b6a399d23ffd1330542e4d5c14e68` → **matches packet tree_sha**
- Stable release (plain `v4.0.1`, not rc/dist/beta). Confirmed via `git tag -l 'v4*'` → v4.0.0, v4.0.1, v4.1.0, v4.1.1, v4.2.0, v4.2.1.
- Context: v4.1.0 → `73f3291d114b5b211e067263eeb9c0e197fe8500` (2024-11-18), v4.1.1 → `7b50a1bbb5324838908dfaa00ec53ad322673a29` (2024-11-20). v4.0.1 was tagged later (2025-05-24) on a 4.0.x maintenance branch, so it is not a descendant of v4.1.0.
- `git merge-base --is-ancestor 7dc5940e 73f3291d` → not ancestor (divergent branches).

## 2. Export integrity

Recomputed checksums in `exports/sinatra__sinatra/`:

```
sha256sum snap_5ab17df9ee6e4957.tar.gz            -> 639f863f...983a63   (matches packet)
sha256sum snap_5ab17df9ee6e4957.manifest.jsonl    -> 52791abe...831289a  (matches packet)
sha256sum snap_5ab17df9ee6e4957.audit.tar.gz      -> 1380c8b87b...286cb
sha256sum snap_5ab17df9ee6e4957.audit.manifest.jsonl -> 01769ab7...214d
```

- `.git` metadata: `tar -tzf ... | grep -cE '(^|/)\.git(/|$|\.)'` → 0. The only `.git*` entries are real tracked files (`.github/workflows/*`, `.gitignore`, `rack-protection/.gitignore`, `sinatra-contrib/.gitignore`). No `.git` directory in the archive or extracted tree.
- Count reconciliation: manifest has 289 entries, all `type=file`; 0 symlinks, 0 gitlinks. `git ls-tree -r 7dc5940e` returns 289 blobs (0 symlink, 0 commit). Equation: **289 = 289 + 0 + 0** → reconciles.
- Path comparison: manifest paths == ls-tree paths exactly (no missing, no extra).
- Byte-for-byte: for all 289 files, sha256(extracted file) == manifest sha256 AND sha256(git cat-file blob `<commit>:<path>`) == manifest sha256. `checked=289 extract_mismatches=0 git_mismatches=0` → ALL_OK.

## 3. Positive anchor (version applicability)

CVE-2024-21510 / GHSA-hxx2-7vcw-mqr3. GitHub REST API was rate-limited; used OSV API and raw.githubusercontent.com copies instead.

- OSV `https://api.osv.dev/v1/vulns/GHSA-hxx2-7vcw-mqr3`: alias CVE-2024-21510; affected pkg:gem/sinatra; range `introduced 0, fixed 4.1.0` (ECOSYSTEM); affected `versions` array explicitly contains `4.0.1` (and `4.0.0`).
- GitHub advisory-database raw JSON (`raw.githubusercontent.com/github/advisory-database/main/advisories/github-reviewed/2024/11/GHSA-hxx2-7vcw-mqr3/GHSA-hxx2-7vcw-mqr3.json`): same range, severity MODERATE, CWE-807, CVSS 3.1 5.4.
- ruby-advisory-db (`raw.githubusercontent.com/rubysec/ruby-advisory-db/master/gems/sinatra/CVE-2024-21510.yml`): `patched_versions: [">= 4.1.0"]`; description "Versions of the package sinatra from 0.0.0 are vulnerable ... via the X-Forwarded-Host (XFH) header"; cvss_v3 5.4.
- CVE CNA (Snyk) `https://cveawg.mitre.org/api/cve/CVE-2024-21510`: "from 0.0.0", CWE-807, CVSS 3.1 5.4 MEDIUM, no explicit fixed version.

All three advisory databases that express a fix agree on **fixed 4.1.0 / patched >= 4.1.0**, and 4.0.1 is inside the affected range. The CNA/NVD record is open-ended (no upper bound) — recorded as a non-substantive discrepancy.

Independent supporting evidence (tree-level):

```
git grep -n host_authorization 7dc5940e -> (absent)
git grep -n host_authorization 73f3291d -> present (lib/sinatra/base.rb, README.md, CHANGELOG.md)
git merge-base --is-ancestor cd3e00de20ddaff34ea30f7a74a7b9dad189d1d8 73f3291d -> yes
git merge-base --is-ancestor cd3e00de20ddaff34ea30f7a74a7b9dad189d1d8 7dc5940e -> no
```

The v4.0.1 tree has no `host_authorization` (the fix) and still contains `@env.include? 'HTTP_X_FORWARDED_HOST'` at `lib/sinatra/base.rb:66`. The fix (PR #2053, commit cd3e00de) is an ancestor of v4.1.0 but not of v4.0.1.

## 4. Build feasibility

```
ruby --version  -> ruby 3.2.3 (2024-01-18 revision 52bb2ac0a6) [x86_64-linux-gnu]
gem --version   -> 3.4.20
bundle --version -> command not found (not required)
cd /tmp/sinatra_extract && gem build sinatra.gemspec
```

Output:

```
WARNING:  open-ended dependency on logger (>= 1.6.0) is not recommended
...
  Successfully built RubyGem
  Name: sinatra
  Version: 4.0.1
  File: sinatra-4.0.1.gem
```

Exit code `0`. Produced `sinatra-4.0.1.gem` (135168 bytes). build_ok = true (observed, not inferred).

## 5. Leakage (P6 audit export)

Extracted `snap_5ab17df9ee6e4957.audit.tar.gz` to `/tmp/sinatra_audit`:

- 288 files (vs 289 in full export). Diff of manifests: exactly `CHANGELOG.md` removed; the 288 remaining files have identical sha256 to the full export.
- Searched extracted audit tree:
  - `CVE-[0-9]{4}-[0-9]+` → 0 hits
  - `GHSA-...` → 0 hits
  - `advisory|open redirect|CVE-2024-21510|host_authorization` (case-insensitive) → 0 hits
  - `benchmark|dataset|RepoVuln|evaluation_target|vulnerable_commit` → 0 hits
  - `.git` directory / `.gitmodules` → none
- Full-export CHANGELOG.md (removed from audit) contained exactly 2 CVE ids — both old and unrelated (`CVE-2018-11627`, `CVE-2018-7212`) — and 0 GHSA ids, matching packet `leakage_facts` (cve_id_count=2, files_with_advisory_ids_count=1 = CHANGELOG.md, ghsa_id_count=0, git_metadata_present=false). CHANGELOG.md had no reference to CVE-2024-21510 / host_authorization / X-Forwarded-Host.
- Conclusion: the P6 audit export contains no advisory identifiers, no fix patches, no `.git` metadata, and no benchmark labels. Packet `leakage_facts` correctly describe the pre-redaction source tree, and the audit redaction removed the single leaky file.

## Verdict

accept. Every mandatory check passed with values matching the packet. No blocking discrepancy found.
