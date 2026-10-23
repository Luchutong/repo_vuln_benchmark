# Independent selection review — axios/axios, snapshot `snap_04c033042a3d52eb` (tag v1.19.0)

Reviewer: `selrev-independent-deepseek-flash-axios-v1190` (not the selector)
Reviewed at: 2026-10-22T19:05:32Z (2026-10-23 in UTC+8)
Verdict: **accept**

Scope: I read only `CLAIM.md`, the repository's own packet
(`v031/reviews/selection_packets/23088740_axios__axios.json`), `data/snapshots.jsonl`,
`data/snapshot_exports.jsonl`, the frozen export, and public upstream sources. I did not open any
forbidden data file, dossier, other reviewer directory, `WORK_LOG.md`, `docs/`, `manifest.json`, or
`HANDOFF_V031.md`. All writes are confined to this directory; temporary work is under `/tmp`
(`/tmp/axios_review`, `/tmp/axios_v1190_build`, `/tmp/selrev_axios_*`, `/tmp/axios_*` logs).

## Summary of measured values

| Item | Claimed | Measured |
|---|---|---|
| Archive sha256 | `f6db8b2488222d3e30891fd8f5f4afd71cdb7f48d5e9d3bbf07a117d376b550f`, 836609 B | identical, 836609 B |
| Manifest sha256 | `3447a262b2eefe1e9b4087f8a46d31121302d36644bfa6bfa44115da3e4934b0` | identical, 84948 B |
| Tar entries | 456 files, 0 symlinks | 456 regular files (454×0644, 2×0755), 0 symlink/hardlink/dir, 0 `.git` path |
| Tag | `v1.19.0` → `311fcc5c…` | lightweight tag, no tag object, ref points at commit `311fcc5c8d989b7248f05d390bb83bfbfb009977` |
| Tree | `e235490f75463ad553dca06d75427aa17c1ab647` | identical (from commit object of `311fcc5c…`) |
| File set | 456 tracked/exported | 456 = 456 archive blobs; paths, modes and blob sha1 all match `git ls-tree -r` |
| package.json | — | `axios` `1.19.0` at `311fcc5c…` |
| Build | not attempted by collector | `npm ci` exit 0, `npm run build` exit 0 |
| Anchor | `>= 1.17.0, < 1.20.0` | confirmed by OSV/NVD/GitHub; v1.19.0 affected |

## Check 1 — tag resolution (independent)

`git ls-remote` against upstream returned the tag directly at a commit (no `^{}` peel line), and the
clone's `for-each-ref` reports `commit` as the object type, so **v1.19.0 is a lightweight tag**, not
an annotated one. There is no tag object SHA to report. The peeled commit is exactly the claimed
`311fcc5c8d989b7248f05d390bb83bfbfb009977`.

```
$ cd /tmp && export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
$ git ls-remote --tags https://github.com/axios/axios 'v1.19.0*' 'v1.18*' 'v1.20*'
2d06f96e8602c2db13b65a26340ee4a1bbc0b61f	refs/tags/v1.18.0
a209bfb1e5dcbce3cecbf4bd955339d006358887	refs/tags/v1.18.1
311fcc5c8d989b7248f05d390bb83bfbfb009977	refs/tags/v1.19.0
84a9f3b9a4f3244b8c8e818f557d64c7b964fb25	refs/tags/v1.20.0

$ git ls-remote --tags https://github.com/axios/axios | grep -E 'refs/tags/v1\.(19\.0|18\.1|20\.0)(\^\{\})?$'
a209bfb1e5dcbce3cecbf4bd955339d006358887	refs/tags/v1.18.1
311fcc5c8d989b7248f05d390bb83bfbfb009977	refs/tags/v1.19.0
84a9f3b9a4f3244b8c8e818f557d64c7b964fb25	refs/tags/v1.20.0
```

(There is no `refs/tags/v1.19.0^{}` line. The repository does contain 96 peeled lines across 243
tag refs, so the absence here is meaningful and not a tooling artifact.)

```
$ git clone --filter=blob:none --no-checkout --branch v1.19.0 --depth 1 https://github.com/axios/axios /tmp/axios_review
$ cd /tmp/axios_review
$ git log -1 --format='commit=%H%ntree=%T%ncommitter_date=%cI%nauthor_date=%aI%nsubject=%s'
commit=311fcc5c8d989b7248f05d390bb83bfbfb009977
tree=e235490f75463ad553dca06d75427aa17c1ab647
committer_date=2026-07-22T19:26:22+02:00
author_date=2026-07-22T19:26:22+02:00
subject=chore(release): prepare release 1.19.0 (#11095)

$ git for-each-ref refs/tags
311fcc5c8d989b7248f05d390bb83bfbfb009977 commit	refs/tags/v1.19.0

$ git cat-file -t 311fcc5c8d989b7248f05d390bb83bfbfb009977
commit
$ git cat-file -t refs/tags/v1.19.0
commit

$ git show v1.19.0:package.json | python3 -I -c "import json,sys; d=json.load(sys.stdin); print(d['name'], d['version'])"
axios 1.19.0
```

Independent corroboration that this commit is the published release: npm registry metadata for
`axios@1.19.0` carries `gitHead=311fcc5c8d989b7248f05d390bb83bfbfb009977`.

```
$ curl -sS https://registry.npmjs.org/axios/1.19.0   # → 200
name=axios version=1.19.0 gitHead=311fcc5c8d989b7248f05d390bb83bfbfb009977
dist.shasum=ddf864d4c8233c0e6873746ab59361537d05ad39
dist.tarball=https://registry.npmjs.org/axios/-/axios-1.19.0.tgz
```

## Check 2 — stable release and age

- Tag name `v1.19.0` is clean semver; no `rc`, `beta`, `alpha`, `dist`, or channel suffix.
- Commit/tag date: 2026-07-22T19:26:22+02:00 (2026-07-22T17:26:22Z).
- GitHub release page ("Release v1.19.0 · axios/axios") was **released 2026-07-26T14:13:32Z** by
  `jasonsaayman`; the page contains no pre-release marker.
- Age relative to the 2026-10-23 review date: **93 days** from the tag/commit date (92 days from the
  UTC review instant), 89 days from the GitHub release publication. The dataset window opens
  2022-10-23, so the release is comfortably inside it.
- The commit is signed and verified on GitHub (GPG key ID B5690EEEBB952194) per the release page.

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-22T19:04:59Z
$ python3 -I -c "from datetime import date; print((date(2026,10,23)-date(2026,7,22)).days)"
93
$ curl -sSL https://github.com/axios/axios/releases/tag/v1.19.0   # → 200, 236087 bytes
<title>Release v1.19.0 · axios/axios · GitHub</title>
released this <relative-time ... datetime="2026-07-26T14:13:32Z">
grep -c 'Pre-release' /tmp/selrev_axios_rel.html  →  0
```

## Check 3 — export integrity

```
$ sha256sum exports/axios__axios/snap_04c033042a3d52eb.tar.gz exports/axios__axios/snap_04c033042a3d52eb.manifest.jsonl
f6db8b2488222d3e30891fd8f5f4afd71cdb7f48d5e9d3bbf07a117d376b550f  exports/axios__axios/snap_04c033042a3d52eb.tar.gz
3447a262b2eefe1e9b4087f8a46d31121302d36644bfa6bfa44115da3e4934b0  exports/axios__axios/snap_04c033042a3d52eb.manifest.jsonl
$ stat -c '%n %s' …
…tar.gz 836609
…manifest.jsonl 84948

$ tar -tvzf exports/axios__axios/snap_04c033042a3d52eb.tar.gz > /tmp/axios_tarlist.txt
$ wc -l < /tmp/axios_tarlist.txt
456
$ awk '{print substr($1,1,1)}' /tmp/axios_tarlist.txt | sort | uniq -c
    456 -
$ awk '{print $NF}' /tmp/axios_tarlist.txt | grep -cE '(^|/)\.git(/|$)'
0
$ awk '$1!="-rw-r--r--"' /tmp/axios_tarlist.txt
-rwxr-xr-x 0/0              27 2026-07-23 01:26 .husky/commit-msg
-rwxr-xr-x 0/0           50476 2026-07-23 01:26 lib/adapters/http.js
$ awk '{print $NF}' /tmp/axios_tarlist.txt | grep -cE '^/|(^|/)\.\.(/|$)'
0
```

All 456 entries are regular files (the type char is `-` for every line); a hardlink would appear as
type `h` and a symlink as `l`, and neither appears. There are no directory entries. Owned by `0/0`,
deterministic mtime `2026-07-23 01:26`.

Manifest cross-check (Python, `-I`):

```
manifest entries 456
types {'file'}
modes {'0755', '0644'}
targets nonnull 0
dup paths 0
tar members 456 non-regular []
manifest-not-in-tar []
tar-not-in-manifest []
content/mode mismatches: [] total 0
```

So every manifest line's path, declared mode, size and sha256 matches the archive member bytes.

### Independent comparison to the tag's tree (names, modes, blob hashes)

```
$ git ls-tree -r v1.19.0 > /tmp/axios_lstree.txt
$ wc -l < /tmp/axios_lstree.txt
456
$ awk '{print $1}' /tmp/axios_lstree.txt | sort | uniq -c
    454 100644
      2 100755
$ git cat-file -p e235490f75463ad553dca06d75427aa17c1ab647 | wc -l
40
```

Python comparison of `/tmp/axios_lstree.txt` against the archive:

```
ls-tree paths 456
types {'blob'}
tar paths 456
paths only in git: []
paths only in tar: []
git-blob/mode mismatches: [] total 0
```

For each of the 456 files, `sha1("blob <len>\0" + content)` computed from the **archive member**
equals the blob id recorded in `git ls-tree -r v1.19.0`. This is stronger than a count check: names,
modes and content are all identical, with zero symlinks and zero gitlinks in the tree
(`types {'blob'}`, modes only 100644/100755). Reconciliation: 456 tracked = 456 exported,
0 symlinks, 0 gitlinks, 0 missing.

## Check 4 — real build

```
$ rm -rf /tmp/axios_v1190_build && mkdir -p /tmp/axios_v1190_build
$ tar -xzf exports/axios__axios/snap_04c033042a3d52eb.tar.gz -C /tmp/axios_v1190_build \
      --no-same-owner --no-same-permissions     # exit 0
$ find /tmp/axios_v1190_build -type f | wc -l   # 456
$ find /tmp/axios_v1190_build -type l | wc -l   # 0

$ node --version    # v24.16.0
$ npm --version     # 11.13.0

$ export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
$ cd /tmp/axios_v1190_build && npm ci --no-audit --no-fund > /tmp/axios_npm_ci.log 2>&1
npm_ci_exit=0
added 648 packages in 7s

$ cd /tmp/axios_v1190_build && npm run build > /tmp/axios_npm_build.log 2>&1
npm_build_exit=0
> axios@1.19.0 build
> gulp clear && cross-env NODE_ENV=production rollup -c
[GITHUB_TOKEN is not defined]
…
./lib/axios.js → dist/node/axios.cjs
created dist/node/axios.cjs in 606ms
```

`npm ci` forced lockfile fidelity (`package-lock.json` committed in the snapshot) and succeeded
without needing `npm install`. `build_ok` is therefore `true` on a real build, not an inference.

Artifacts produced (sha256 measured):

```
221ab2e4…47714f  dist/axios.min.js.map        (251184 B)
32a0cec8…a47985  dist/axios.min.js            (65099 B)
c97dfeb9…c22eea  dist/axios.js                (195267 B)
1f1dea83…d25cdd  dist/browser/axios.cjs       (150798 B)
4094a73d…f669e2  dist/esm/axios.min.js.map    (240883 B)
eb65b8c2…ea0de7  dist/esm/axios.min.js        (48485 B)
01bea6e0…49ad9d  dist/esm/axios.js            (151770 B)
00abe271…8feb24  dist/node/axios.cjs          (216518 B)
```

The `[GITHUB_TOKEN is not defined]` line is a benign gulp message; the build itself completed.

## Check 5 — anchor verification from public sources

Sources fetched over HTTPS through the proxy:

1. **OSV `GHSA-r4gj-5m52-g5wh`** (`https://api.osv.dev/v1/vulns/GHSA-r4gj-5m52-g5wh`, HTTP 200):
   - aliases `["CVE-2026-101907"]`, summary "Axios: maxRedirects: 0 is not enforced by the fetch
     adapter, allowing redirect-based SSRF"
   - package `npm/axios`; range `SEMVER events [{introduced: 1.17.0}, {fixed: 1.20.0}]`
   - severity `CVSS_V4`: `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N`
     (vector only, no numeric score); `database_specific.severity = HIGH`
   - published 2026-09-30T15:31:58Z; `nvd_published_at` 2026-09-28T18:17:19Z; references the
     GitHub advisory, NVD, PR #11141, fix commit `d19040b…`, and release tag v1.20.0

2. **OSV `CVE-2026-101907`** (`https://api.osv.dev/v1/vulns/CVE-2026-101907`, HTTP 200):
   - GIT range on `https://github.com/axios/axios`: introduced
     `4306df21e84332fc576e98c2de549347c06bfb76`, fixed
     `84a9f3b9a4f3244b8c8e818f557d64c7b964fb25` (v1.20.0 tag) and
     `d19040bda7a8be2f82c3c6e1a5bc03917daee39a`
   - **`versions` explicitly lists `v1.19.0`** (with v1.18.1, v1.18.0, v1.17.0)
   - extracted string range from the CVE affected field: introduced 1.17.0, fixed 1.20.0
   - CNA GitHub_M, CWE-441/CWE-601; published 2026-09-28, modified 2026-10-21

3. **NVD** (`https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-101907`, HTTP 200):
   - `vulnStatus: Awaiting Analysis`, published 2026-09-28T18:17:19, lastModified
     2026-09-30T19:38:27
   - `configurations: null` — **no CPE configurations**
   - `metrics` contains only `cvssMetricV40` with `type: Secondary`,
     `source: security-advisories@github.com`, CVSS 4.0 base 7.0 HIGH, plus an SSVC block. **No
     Primary metric, no CVSS 3.1 score.**
   - description: "From 1.17.0 until 1.20.0, the fetch adapter bypasses the maxRedirects: 0
     redirect policy…"

4. **Rendered GitHub advisory** (`https://github.com/axios/axios/security/advisories/GHSA-r4gj-5m52-g5wh`,
   HTTP 200, 248 KB): "High 7.0", package npm `axios`, **Affected versions `1.17.0`**,
   **Patched versions `>=1.20.0`**, published Sep 16, 2026, references CVE-2026-101907. The
   affected-version cell renders only the lower bound (`1.17.0`); the full range is established by
   the OSV SEMVER events, the CVE's extracted string range, and NVD's "From 1.17.0 until 1.20.0".

Note: the GitHub REST endpoint (`api.github.com/advisories/GHSA-r4gj-5m52-g5wh`) returned HTTP 403
"API rate limit exceeded" from this host, so the rendered page was used instead of REST JSON.

**Version test:** 1.17.0 <= 1.19.0 < 1.20.0, so v1.19.0 is inside the affected range. OSV's version
list names v1.19.0 directly.

### Code-level corroboration inside the frozen tree

```
$ grep -n 'redirect\|Redirect' /tmp/axios_v1190_build/lib/adapters/fetch.js   # (no matches)
$ grep -rn 'maxRedirects' /tmp/axios_v1190_build/lib/adapters/http.js
358:        // (maxRedirects === 0); `options.agents.https` is consumed by
529:      const maxRedirects = own('maxRedirects');
963:        } else if (maxRedirects === 0) {
969:          if (maxRedirects) {
970:            options.maxRedirects = maxRedirects;
```

The Node HTTP adapter enforces `maxRedirects`; the fetch adapter in v1.19.0 never reads it, exactly
as the advisory describes. Comparing the two release trees in the clone:

```
$ git fetch --depth 1 origin refs/tags/v1.20.0:refs/tags/v1.20.0
$ git show v1.20.0:lib/adapters/fetch.js | grep -n 'redirect\|maxRedirects'
22:  redirect: 'follow',
221:      maxRedirects,
478:      if (maxRedirects === 0) {
479:        resolvedOptions.redirect = 'manual';
482:          safeFetchOptions.redirect = 'manual';
$ git show v1.19.0:lib/adapters/fetch.js | grep -n 'redirect\|maxRedirects'   # (no matches)
```

And the cited fix commit postdates the release and introduces exactly that logic:

```
$ git fetch --depth 2 origin d19040bda7a8be2f82c3c6e1a5bc03917daee39a
$ git log -1 --format='commit=%H%ndate=%cI%nsubject=%s' d19040bda7a8be2f82c3c6e1a5bc03917daee39a
commit=d19040bda7a8be2f82c3c6e1a5bc03917daee39a
date=2026-08-12T18:27:45+02:00
subject=fix: harden runtime option handling (#11141)
$ git diff d19040b…^ d19040b… -- lib/adapters/fetch.js | grep -E '^[+-].*(redirect|maxRedirects)'
+  redirect: 'follow',
+      maxRedirects,
+      if (maxRedirects === 0) {
+        resolvedOptions.redirect = 'manual';
+          safeFetchOptions.redirect = 'manual';
```

So the vulnerability is present at this snapshot and fixed only after it: the fix commit is dated
2026-08-12, and the later release v1.20.0 (tag object `84a9f3b9…`, matching the OSV `fixed` event)
carries the redirect handling.

## Leakage assessment

The export contains no `.git` path and no git metadata. Advisory identifiers appear in exactly two
files, and all of them are historical:

- `CHANGELOG.md`: `CVE-2023-45857` (CSRF fix, #6028) and `CVE-2024-39338` (SSRF/protocol-relative
  URL fix, #6539).
- `THREATMODEL.md`: `CVE-2023-45857`, `GHSA-3w6x-2g7m-8v23`, `GHSA-445q-vr5w-6q77`,
  `GHSA-pf86-5x62-jrwf`, `GHSA-vf2m-468p-8v99`, `GHSA-w9j2-pvgh-6h63`, `GHSA-xx6v-rp6x-q39c` —
  all describing already-shipped mitigations for prototype pollution, CRLF/multipart injection,
  XSRF, and decompression limits.

```
$ grep -rIlE 'CVE-[0-9]{4}-[0-9]{4,7}|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}' /tmp/axios_v1190_build --exclude-dir=node_modules
/tmp/axios_v1190_build/CHANGELOG.md
/tmp/axios_v1190_build/THREATMODEL.md
$ grep -rIE 'CVE-2026-101907|GHSA-r4gj-5m52-g5wh' /tmp/axios_v1190_build --exclude-dir=node_modules | wc -l
0
```

None of the identifiers name this snapshot's own vulnerability (`CVE-2026-101907` /
`GHSA-r4gj-5m52-g5wh`), which was published in September 2026, after this July 2026 release. Recorded
as a disclosure item, not a failed check.

## Check 6 — verdict reasoning

Every mandatory check passed and was verified independently, not merely re-read from the packet:

1. Tag resolves exactly (`311fcc5c…`, lightweight), tree `e235490f…`, `package.json` = 1.19.0, and
   npm's published `gitHead` agrees.
2. It is a stable release, dated 2026-07-22 (GitHub release 2026-07-26), 93 days old relative to
   2026-10-23, inside the 2022-10-23 window.
3. Both sha256 values match; the archive contains 456 regular files, 0 symlinks/hardlinks/gitlinks,
   no `.git`, and its path/mode/blob-hash set is identical to `git ls-tree -r v1.19.0`.
4. A real `npm ci` + `npm run build` succeeded (exit 0), producing the expected `dist/` bundles.
5. The anchor is public and real: `CVE-2026-101907` / `GHSA-r4gj-5m52-g5wh`, npm `axios`
   `>= 1.17.0, < 1.20.0`, HIGH 7.0, patched `1.20.0`, and v1.19.0 is inside it — corroborated at
   source level by the missing redirect handling in the snapshot and the fix added post-release.
6. Leakage is limited to historical identifiers and names nothing about this snapshot's own flaw.

**Verdict: accept.**

## Limitations

- GitHub REST advisory API was rate-limited (HTTP 403) from this host; the rendered advisory page
  plus OSV/NVD were used.
- The rendered GitHub page shows the affected range as just `1.17.0`; the full range comes from OSV
  and NVD, both of which state `>= 1.17.0, < 1.20.0` (NVD: "From 1.17.0 until 1.20.0"), and OSV
  lists v1.19.0 explicitly.
- The clone is shallow; ancestor relationships were verified only for the v1.19.0/v1.20.0 trees and
  the fix commit, not by walking full history.
- The snapshot's `CHANGELOG.md` has no v1.19.0 section (newest is v1.18.0, June 13, 2026). This is
  an upstream changelog-lag observation; tag/tree/blob identity and the npm `gitHead` are unaffected.
- The build depended on the npm registry being reachable through the proxy; `npm ci` used the
  committed lockfile.
- `tag_age_days` is computed against the 2026-10-23 review date stated in the claim (UTC+8 local
  date); against the UTC review instant it is 92 days, and against the GitHub release publication
  (2026-07-26) it is 89 days.
