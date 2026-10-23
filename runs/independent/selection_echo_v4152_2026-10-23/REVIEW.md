# Independent selection review — labstack/echo snapshot `snap_e0836fa1c53e240d` (v4.15.2)

**Verdict: ACCEPT**

Reviewer: `independent-reviewer-deepseek-flash-2026-10-23`
Reviewed at: `2026-10-22T19:07:28Z` (local review date 2026-10-23, UTC+8)
Packet: `v031/reviews/selection_packets/31504491_labstack__echo.json`
Output: `review.jsonl` (one JSON object) in this directory.

Every value below was measured independently; nothing was taken from `CLAIM.md` or the packet without recomputation.
All temporary work was under `/tmp`; no forbidden path was opened.

---

## 0. Measured values at a glance

| Item | Measured | Packet | Match |
|---|---|---|---|
| Archive sha256 | `2e30bb475273dcf3c6f561d64bd5198e0b49dd6e7c71ba78b5d53ec21a53482f` | same | yes |
| Archive bytes | `427496` | `427496` | yes |
| Manifest sha256 | `22f7892221b9372af122db5d3aeef11375cf742b06c485395bfb8e03fca560f3` | same | yes |
| Tar entries / regular files | `110` / `110` | `110` | yes |
| Manifest lines | `110` | — | — |
| Symlinks / hardlinks / gitlinks | `0` / `0` / `0` | `0` / `0` | yes |
| Tree (git) file count | `110` | `110` | yes |
| Tag object type | lightweight (`commit`) | tag_commit | yes |
| Tag commit | `25685e6f5f7b0683105d1386db46ae48eb3de028` | same | yes |
| Commit tree SHA | `d4529971662ff21db287d808d3250058518fff5d` | same | yes |
| `go.mod` module | `github.com/labstack/echo/v4` | — | yes |
| Commit date / release date | `2026-05-01 20:59:02 +0300` / `2026-05-01` | — | — |
| Tag age on 2026-10-23 | `175` days | — | — |
| Go toolchain | `go1.26.10 linux/amd64` (sha256 verified) | — | — |
| `go build ./...` | exit `0` | — | — |
| `go vet ./...` | exit `0` | — | — |
| Anchor affects v4.15.2 | yes, in all 9 sources checked | — | — |

---

## 1. Environment and network

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
```

Everything below ran in `/home/luchitong/work/repo-vuln-50-v031` unless a `cd` is shown explicitly.
Downloaded code was extracted into the fresh, empty `/tmp/echo_extract`; helper scripts lived in
`/tmp/review_scripts`; Python that read the downloaded tree ran with `-I` (or as a stdin heredoc,
which is equivalent for import-path isolation). The git clone lived in `/tmp/echo_git/repo`.

---

## 2. Export integrity (required check 3)

### 2.1 Recompute archive and manifest hashes

```bash
cd /home/luchitong/work/repo-vuln-50-v031 && sha256sum exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz exports/labstack__echo/snap_e0836fa1c53e240d.manifest.jsonl && echo "--- sizes ---" && stat -c '%n %s' exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz exports/labstack__echo/snap_e0836fa1c53e240d.manifest.jsonl && echo "--- manifest line count ---" && wc -l exports/labstack__echo/snap_e0836fa1c53e240d.manifest.jsonl
```

Result: both hashes match the packet exactly; archive is 427496 bytes; manifest has 110 lines.

### 2.2 List tar entries and entry types

```bash
cd /home/luchitong/work/repo-vuln-50-v031 && echo "--- tar entries (verbose) ---" && tar -tzvf exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz && echo "--- count ---" && tar -tzf exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz | wc -l
```

```bash
cd /home/luchitong/work/repo-vuln-50-v031 && mkdir -p /tmp/echo_review && tar -tvzf exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz | awk '{print $1}' | sort | uniq -c && echo "--- any non-regular? ---" && tar -tvzf exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz | grep -E '^[^d-]' || true
```

Result: 110 lines, all `-rw-r--r--` (`100644`-equivalent `0644`), no non-regular entry. No directory
entries, no symlink, no hardlink. The tarfile-level check in §2.3 additionally reports every member
type as `b'0'` (regular).

Explicit `.git` / traversal / absolute-path check:

```bash
cd /tmp/echo_extract
find . -name '.git' -o -name '.git*' | head
tar -tzf /home/luchitong/work/repo-vuln-50-v031/exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz | grep -E '(^|/)\.git(/|$)|(^|/)\.\.(/|$)|^/' || echo "no .git/traversal/absolute entries"
```

Result: `find` matched only `.github`, `.gitignore`, `.gitattributes` (not git metadata); the tar grep
printed `no .git/traversal/absolute entries`.

### 2.3 Manifest ↔ archive ↔ git tree equivalence and content hashes

Extraction into a new empty directory:

```bash
rm -rf /tmp/echo_extract && mkdir -p /tmp/echo_extract && cd /tmp/echo_extract && tar -xzf /home/luchitong/work/repo-vuln-50-v031/exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz && echo "extract exit=$?" && find . -type f | wc -l && find . -type l | wc -l && find . -type d | wc -l && echo "--- go.mod ---" && cat go.mod | head -5
```

Result: exit 0; 110 files, 0 symlinks, 9 directories; `go.mod` says `module github.com/labstack/echo/v4`.

Comparison script (kept outside the extracted tree) and invocation:

```bash
mkdir -p /tmp/review_scripts && cat > /tmp/review_scripts/compare.py <<'PYEOF'
import sys, tarfile, hashlib, json, subprocess, os

arch = sys.argv[1]
manifest = sys.argv[2]
extract_dir = sys.argv[3]
lstree = sys.argv[4]

# archive
with tarfile.open(arch, 'r:gz') as tf:
    members = tf.getmembers()
arch_set = {}
types = {}
for m in members:
    types[m.type] = types.get(m.type,0)+1
    arch_set[m.name] = oct(m.mode & 0o7777)
print("tar member types:", types)
print("tar count:", len(members))

# manifest
man = {}
for line in open(manifest):
    line=line.strip()
    if not line: continue
    o=json.loads(line)
    man[o['path']]=o
print("manifest count:", len(man))

# git ls-tree
gtree = {}
for line in open(lstree):
    line=line.rstrip('\n')
    if not line: continue
    meta, path = line.split('\t',1)
    mode, typ, sha = meta.split()
    gtree[path]=(mode, typ, sha)
print("git tree count:", len(gtree))

def norm_git_mode(m):
    # 100644 -> 0644 ; 100755 -> 0755
    return oct(int(m,8) & 0o7777)

print("\n== archive vs git tree ==")
print("only in archive:", sorted(set(arch_set)-set(gtree)))
print("only in git:", sorted(set(gtree)-set(arch_set)))
mode_mismatch=[]
for p in sorted(set(arch_set)&set(gtree)):
    gm = norm_git_mode(gtree[p][0])
    if arch_set[p] != gm:
        mode_mismatch.append((p, arch_set[p], gm, gtree[p][0]))
print("mode mismatches:", mode_mismatch)
print("non-blob git types:", [(p,t) for p,(m,t,s) in gtree.items() if t!='blob'])
print("git modes:", sorted(set(m for m,_,_ in gtree.values())))

print("\n== manifest vs archive ==")
print("only in manifest:", sorted(set(man)-set(arch_set)))
print("only in archive:", sorted(set(arch_set)-set(man)))
print("manifest types:", sorted(set(o['type'] for o in man.values())))
print("manifest targets non-null:", [(p,o['target']) for p,o in man.items() if o['target'] is not None])

# verify actual content hashes and sizes against manifest
bad_sha=[]; bad_size=[]; missing=[]
for p,o in man.items():
    fp=os.path.join(extract_dir,p)
    if not os.path.isfile(fp):
        missing.append(p); continue
    h=hashlib.sha256(open(fp,'rb').read()).hexdigest()
    if h!=o['sha256']: bad_sha.append((p,h,o['sha256']))
    if os.path.getsize(fp)!=o['size']: bad_size.append((p,os.path.getsize(fp),o['size']))
print("missing files:", missing)
print("sha mismatches:", bad_sha)
print("size mismatches:", bad_size)

# git blob sha verification: compute git blob hash from content
def git_blob_sha(fp):
    data=open(fp,'rb').read()
    h=hashlib.sha1()
    h.update(b'blob %d\x00'%len(data))
    h.update(data)
    return h.hexdigest()
blob_bad=[]
for p,(mode,typ,gsha) in gtree.items():
    fp=os.path.join(extract_dir,p)
    if not os.path.isfile(fp):
        blob_bad.append((p,'MISSING')); continue
    if git_blob_sha(fp)!=gsha:
        blob_bad.append((p,git_blob_sha(fp),gsha))
print("git blob sha mismatches:", blob_bad)
print("\nRESULT:",
      "OK" if not (set(arch_set)^set(gtree)) and not mode_mismatch and not bad_sha and not bad_size and not missing and not blob_bad and not man['CHANGELOG.md']['target'] else "PROBLEM")
PYEOF
python3 -I /tmp/review_scripts/compare.py /home/luchitong/work/repo-vuln-50-v031/exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz /home/luchitong/work/repo-vuln-50-v031/exports/labstack__echo/snap_e0836fa1c53e240d.manifest.jsonl /tmp/echo_extract /tmp/echo_git/lstree.txt
```

Result:

```
tar member types: {b'0': 110}
tar count: 110
manifest count: 110
git tree count: 110

== archive vs git tree ==
only in archive: []
only in git: []
mode mismatches: []
non-blob git types: []
git modes: ['100644']

== manifest vs archive ==
only in manifest: []
only in archive: []
manifest types: ['file']
manifest targets non-null: []
missing files: []
sha mismatches: []
size mismatches: []
git blob sha mismatches: []

RESULT: OK
```

This is the independent name/mode/content check required by the claim: the archive's 110 paths are
exactly the tag's `git ls-tree -r` paths, every mode is `100644`→`0644`, and every extracted file's
recomputed **git blob SHA-1** equals the object SHA stored in commit `25685e6f`'s tree. The manifest's
own per-file `sha256`/`size` also matched all 110 files.

Reconciliation: `exported_file_count 110 + symlink_count 0 = tree_file_count 110`; 0 gitlinks,
0 hardlinks, 0 missing. **Counts reconcile.**

---

## 3. Tag resolution (required checks 1 and 2)

### 3.1 Resolve upstream

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
cd /tmp && git ls-remote --tags https://github.com/labstack/echo v4.15.2 'v4.15.2^{}' 2>&1; echo "exit=$?"
```

```bash
cd /tmp && git ls-remote --tags https://github.com/labstack/echo 2>/dev/null | grep 'v4.15.2' ; echo "---all v4.15 tags---"; git ls-remote --tags https://github.com/labstack/echo 'refs/tags/v4.15*' 2>/dev/null
```

Result: `v4.15.2` appears only as `25685e6f5f7b0683105d1386db46ae48eb3de028 refs/tags/v4.15.2`, with
**no `v4.15.2^{}` peel line**, whereas `v4.15.3` shows both `b1febadc... refs/tags/v4.15.3` and
`8800212a... refs/tags/v4.15.3^{}`. So v4.15.2 is a lightweight tag and v4.15.3 is annotated.

Fresh fetch and object inspection:

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
mkdir -p /tmp/echo_git && cd /tmp/echo_git && rm -rf repo && git init -q repo && cd repo && git remote add origin https://github.com/labstack/echo && git fetch -q --depth 1 origin refs/tags/v4.15.2:refs/tags/v4.15.2 && echo "fetch exit=$?" && git cat-file -t v4.15.2 && echo "--- cat-file -p tag? ---" && git rev-parse v4.15.2 && git rev-parse 'v4.15.2^{commit}' && git log -1 --format='%H%n%ci%n%ct%n%s' v4.15.2 && echo "--- go.mod ---" && git show v4.15.2:go.mod | head -5 && echo "--- tree ---" && git rev-parse 'v4.15.2^{tree}'
```

Result:

```
fetch exit=0
commit                        <- git cat-file -t v4.15.2  (lightweight)
25685e6f5f7b0683105d1386db46ae48eb3de028
25685e6f5f7b0683105d1386db46ae48eb3de028
2026-05-01 20:59:02 +0300
1777658342
Merge pull request #2963 from aldas/v4_changelog_4_15_2
module github.com/labstack/echo/v4
go 1.25.0
d4529971662ff21db287d808d3250058518fff5d
```

Also fetched the two later tags for context and fix-level corroboration:

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
cd /tmp/echo_git/repo
git fetch -q --depth 1 origin refs/tags/v4.15.3:refs/tags/v4.15.3 refs/tags/v4.15.4:refs/tags/v4.15.4 2>&1; echo "fetch exit=$?"
for t in v4.15.2 v4.15.3 v4.15.4; do printf '%s: ' "$t"; git cat-file -t "$t"; done
git cat-file -p refs/tags/v4.15.3 | head -12
for t in v4.15.2 v4.15.3 v4.15.4; do printf '%s -> ' "$t"; git rev-parse "$t^{commit}"; done
for t in v4.15.2 v4.15.3 v4.15.4; do git log -1 --format="$t %H %ci %s" "$t^{commit}"; done
```

Result: `v4.15.3` is an annotated tag object (`object 8800212ad4392d3f5af052f3042aca62cc5911a7`,
tagger `Vishal Rana <vr@labstack.com> 1781453835 -0700`); `v4.15.4` is lightweight at
`ec79b584025d300acc9cb0a2b127a7209c902fd2` (2026-06-15). The v4.15.3 commit
`8800212a...` is exactly the `fixed` event in OSV's GIT range (see §5).

**Tag check conclusion:** v4.15.2 is lightweight, points directly at
`25685e6f5f7b0683105d1386db46ae48eb3de028`, commit tree
`d4529971662ff21db287d808d3250058518fff5d` matches the packet, and `go.mod` declares
`module github.com/labstack/echo/v4`. All confirm.

### 3.2 Stable release / date / age

```bash
cd /tmp/anchor && python3 -I - <<'PY'
from datetime import date
rel=date(2026,5,1); today=date(2026,10,23); window=date(2022,10,23)
print('release',rel,'review',today,'age_days',(today-rel).days,'in_window',rel>=window)
print('days since window open', (today-window).days)
PY
```

Result: release `2026-05-01`, age `175` days on `2026-10-23`, inside the dataset window that opens
`2022-10-23`.

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
cd /tmp/anchor
fetch() { url="$1"; out="$2"; code=$(curl -sSL --max-time 40 -o "$out" -w '%{http_code}' -H 'User-Agent: Mozilla/5.0 independent-review' "$url"); echo "HTTP $code  $url -> $out ($(stat -c%s "$out" 2>/dev/null) bytes)"; }
fetch 'https://github.com/labstack/echo/releases/tag/v4.15.2' release_v4152.html
fetch 'https://github.com/labstack/echo/tags' tags_page.html
```

Rendered release page says `aldas released this 01 May 18:01 ... v4.15.2 25685e6`; the page is a
normal release titled “v4.15.2 - Context.Scheme() header validation”, not marked pre-release.
`CHANGELOG.md` at the tag opens with `## v4.15.2 - 2026-05-01`. Tag name contains no
`rc/beta/alpha/dist/channel` token. **Stable release: confirmed.**

---

## 4. Real build (required check 4)

### 4.1 Toolchain download and verification

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
cd /tmp && curl -sS --max-time 30 'https://go.dev/dl/?mode=json' -o /tmp/go_dl.json && python3 -I -c "
import json
d=json.load(open('/tmp/go_dl.json'))
for r in d[:5]: print(r['version'], r['stable'])
"
```

Result: latest stable `go1.27.3`; `go1.26.10` also stable. Chose `go1.26.10`.

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
mkdir -p /tmp/godl && cd /tmp/godl && curl -sSL --max-time 300 -o go1.26.10.linux-amd64.tar.gz https://go.dev/dl/go1.26.10.linux-amd64.tar.gz; echo "exit=$?"; ls -l; file go1.26.10.linux-amd64.tar.gz
python3 -I -c "
import json
d=json.load(open('/tmp/go_dl.json'))
for r in d:
    if r['version']=='go1.26.10':
        for f in r['files']:
            if f['filename']=='go1.26.10.linux-amd64.tar.gz':
                print(f['filename'], f['sha256'], f['size'], f.get('kind'))
"
sha256sum /tmp/godl/go1.26.10.linux-amd64.tar.gz; stat -c '%s' /tmp/godl/go1.26.10.linux-amd64.tar.gz
```

(An initial `curl -sS -O` without `-L` saved only the 76-byte redirect stub
`<a href="https://dl.google.com/go/...">Found</a>`; re-ran with `-sSL`.)

Result: 66936659 bytes; actual sha256
`ccfe7ae822d2c2f41f4fe7c956199967a4dac22d0ee0d2b2bfdb440aab3b20c5` equals the published value.

```bash
rm -rf /tmp/gotoolchain && mkdir -p /tmp/gotoolchain && tar -C /tmp/gotoolchain -xzf /tmp/godl/go1.26.10.linux-amd64.tar.gz && /tmp/gotoolchain/go/bin/go version
```

Result: `go version go1.26.10 linux/amd64`.

### 4.2 Build and vet against the extracted snapshot

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
export GOROOT=/tmp/gotoolchain/go
export PATH=$GOROOT/bin:$PATH
export GOTOOLCHAIN=local
cd /tmp/echo_extract
echo "== go version =="; go version
echo "== go env =="; go env GOVERSION GOOS GOARCH GOMOD GOPROXY GOTOOLCHAIN
echo "== go build ./... =="
go build ./... 2>&1; echo "BUILD_EXIT=$?"
echo "== go vet ./... =="
go vet ./... 2>&1; echo "VET_EXIT=$?"
```

Result:

```
go version go1.26.10 linux/amd64
go1.26.10
linux
amd64
/tmp/echo_extract/go.mod
https://proxy.golang.org,direct
local
== go build ./... ==
BUILD_EXIT=0
== go vet ./... ==
VET_EXIT=0
```

Networking was enabled and module downloads really happened:

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
export GOROOT=/tmp/gotoolchain/go GOFLAGS= GOTOOLCHAIN=local
export PATH=$GOROOT/bin:$PATH
cd /tmp/echo_extract
echo "=== go list -m all ==="; go list -m all 2>&1 | head -30; echo "LIST_EXIT=$?"
echo "=== module cache download evidence ==="; du -sh "$(go env GOMODCACHE)" 2>/dev/null; ls "$(go env GOMODCACHE)/github.com/labstack" 2>/dev/null
```

Result: full module graph resolved (`gommon v0.5.0`, `testify v1.11.1`, `x/crypto v0.50.0`,
`x/net v0.53.0`, …), module cache 743M, `github.com/labstack/gommon@v0.5.0` present.

Post-build integrity re-check (proves the build did not mutate the source tree):

```bash
cd /tmp/echo_extract
python3 -I /tmp/review_scripts/compare.py /home/luchitong/work/repo-vuln-50-v031/exports/labstack__echo/snap_e0836fa1c53e240d.tar.gz /home/luchitong/work/repo-vuln-50-v031/exports/labstack__echo/snap_e0836fa1c53e240d.manifest.jsonl /tmp/echo_extract /tmp/echo_git/lstree.txt 2>&1 | tail -4
find . -type f | wc -l
```

Result: still `RESULT: OK`, `sha mismatches: []`, `size mismatches: []`, `git blob sha mismatches: []`,
110 files. **`build_ok = true`.**

---

## 5. Anchor verification from public sources (required check 5)

Base scope claim: `CVE-2026-55677` / `GHSA-vfp3-v2gw-7wfq` / `GO-2026-6293`, package
`github.com/labstack/echo/v4`.

### 5.1 Fetches

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
mkdir -p /tmp/anchor && cd /tmp/anchor
fetch() { url="$1"; out="$2"; code=$(curl -sSL --max-time 40 -o "$out" -w '%{http_code}' -H 'User-Agent: independent-selection-review' "$url"); echo "HTTP $code  $url -> $out ($(stat -c%s "$out" 2>/dev/null) bytes)"; }
fetch 'https://api.osv.dev/v1/vulns/GHSA-vfp3-v2gw-7wfq' osv_ghsa.json
fetch 'https://api.osv.dev/v1/vulns/GO-2026-6293' osv_go.json
fetch 'https://api.osv.dev/v1/vulns/CVE-2026-55677' osv_cve.json
fetch 'https://api.github.com/advisories/GHSA-vfp3-v2gw-7wfq' gh_global.json
fetch 'https://api.github.com/repos/labstack/echo/security-advisories/GHSA-vfp3-v2gw-7wfq' gh_repo.json
fetch 'https://cveawg.mitre.org/api/cve/CVE-2026-55677' cve_cna.json
fetch 'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-55677' nvd.json
```

Results: OSV ×3 `200`; CVE CNA `200`; NVD `200`; both unauthenticated `api.github.com` calls `403`
(`API rate limit exceeded`). Rendered-page and raw-database fallbacks:

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
cd /tmp/anchor
fetch() { url="$1"; out="$2"; code=$(curl -sSL --max-time 40 -o "$out" -w '%{http_code}' -H 'User-Agent: Mozilla/5.0 independent-review' "$url"); echo "HTTP $code  $url -> $out ($(stat -c%s "$out" 2>/dev/null) bytes)"; }
fetch 'https://raw.githubusercontent.com/github/advisory-database/main/advisories/github-reviewed/2026/08/GHSA-vfp3-v2gw-7wfq/GHSA-vfp3-v2gw-7wfq.json' advdb_ghsa.json
fetch 'https://github.com/labstack/echo/security/advisories/GHSA-vfp3-v2gw-7wfq' gh_repo_page.html
fetch 'https://github.com/advisories/GHSA-vfp3-v2gw-7wfq' gh_global_page.html
fetch 'https://github.com/labstack/echo/security/advisories' gh_repo_list.html
fetch 'https://osv.dev/vulnerability/GHSA-vfp3-v2gw-7wfq' osv_page.html
fetch 'https://nvd.nist.gov/vuln/detail/CVE-2026-55677' nvd_page.html
fetch 'https://pkg.go.dev/vuln/GO-2026-6293' pkggodev.html
```

All `200`. Because the anonymous GitHub API was rate-limited, the same public endpoints were also
queried with the locally authenticated CLI:

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
cd /tmp/anchor
gh api repos/labstack/echo/security-advisories/GHSA-vfp3-v2gw-7wfq > gh_repo_api.json 2>gh_repo_api.err; echo "exit=$?"; head -c 300 gh_repo_api.err
gh api advisories/GHSA-vfp3-v2gw-7wfq
```

Both succeeded (exit 0); the full JSON of each is parsed in §5.2. The NVD rendered page, by contrast,
returned only the JavaScript `NVD - Home` shell (2092 bytes, no vulnerability detail), so NVD facts
come from the NVD 2.0 API JSON.

### 5.2 What each source says

Parsing commands used (abbreviated to the relevant assertions):

```bash
cd /tmp/anchor && python3 -I - <<'PY'
import json
def show(name, path):
    d=json.load(open(path))
    print("="*30, name, "="*30)
    print("id:", d.get("id"), "aliases:", d.get("aliases"))
    print("modified:", d.get("modified"), "published:", d.get("published"))
    print("severity:", d.get("severity"), "database_specific:", d.get("database_specific"))
    for a in d.get("affected",[]):
        print("  pkg:", a.get("package",{}).get("name"), "ranges:", json.dumps(a.get("ranges")), "versions:", a.get("versions") is not None)
show("OSV GO-2026-6293","osv_go.json")
show("OSV CVE-2026-55677","osv_cve.json")
PY
```

plus the equivalent `json.tool` dumps of `cve_cna.json` and `nvd.json`, and JSON extraction of
`gh_global.json` / `gh_repo_api.json` / `advdb_ghsa.json`.

| Source (public https URL) | v4 range | First patched | v5 range | Legacy v3 | Severity | v4.15.2 affected? |
|---|---|---|---|---|---|---|
| **OSV** `https://api.osv.dev/v1/vulns/GHSA-vfp3-v2gw-7wfq` (modified 2026-09-10) | introduced 0 → fixed **4.15.3** | 4.15.3 | fixed 5.2.0 | last_affected 3.3.10 | HIGH / 7.5 | **yes** |
| **OSV** `https://api.osv.dev/v1/vulns/GO-2026-6293` (modified 2026-08-26, UNREVIEWED) | introduced 0 → fixed **4.15.3** | 4.15.3 | fixed 5.2.0 | absent | — | **yes** |
| **OSV** `https://api.osv.dev/v1/vulns/CVE-2026-55677` (modified 2026-10-21) | GIT fixed **8800212a…** (= v4.15.3 commit) | — | GIT fixed 5786024e… | versions list spans v3 | CVSS 3.1 7.5 | **yes** (`versions` includes `v4.15.2`) |
| **CVE CNA** `https://cveawg.mitre.org/api/cve/CVE-2026-55677` (updated 2026-06-26) | `< 4.15.3` | — | `>= 5.0.0, < 5.2.0` | absent | 7.5 HIGH | **yes** |
| **NVD 2.0 API** `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-55677` (lastModified 2026-06-26) | `< 4.15.3` | — | `>= 5.0.0, < 5.2.0` | absent | CVSS 3.1 Secondary 7.5 HIGH only; `vulnStatus=Deferred`; **no CPE configurations** | **yes** |
| **GitHub global advisory API** `https://api.github.com/advisories/GHSA-vfp3-v2gw-7wfq` (updated 2026-08-25) | `< 4.15.3` | 4.15.3 | `< 5.2.0` | `<= 3.3.10` | high / 7.5; `cvss_v4` null | **yes** |
| **GitHub Advisory DB raw** `https://raw.githubusercontent.com/github/advisory-database/main/advisories/github-reviewed/2026/08/GHSA-vfp3-v2gw-7wfq/GHSA-vfp3-v2gw-7wfq.json` (modified 2026-08-25) | ECOSYSTEM fixed **4.15.3** | 4.15.3 | fixed 5.2.0 | last_affected 3.3.10 | CVSS_V3 | **yes** |
| **Rendered global page** `https://github.com/advisories/GHSA-vfp3-v2gw-7wfq` | `< 4.15.3` | 4.15.3 | `< 5.2.0` | `<= 3.3.10` | High | **yes** |
| **GitHub repository-scoped API** `https://api.github.com/repos/labstack/echo/security-advisories/GHSA-vfp3-v2gw-7wfq` (published 2026-06-14, updated **2026-09-27T19:16:52Z**) | `< 4.15.4` | 4.15.4 | `< 5.2.1` | **absent** | high / 7.5 | **yes** |
| **Rendered repository advisory page** `https://github.com/labstack/echo/security/advisories/GHSA-vfp3-v2gw-7wfq` | **Affected `< 4.15.4`, Patched `4.15.4`** | 4.15.4 | `< 5.2.1`, patched 5.2.1 | absent | High | **yes** |

The repository page carries the explicit update text:

> **Update (2026-09-27)** The first patched versions, v5.2.0 and v4.15.3, fixed only part of this
> issue: other percent-encoded paths (for example `/%61dmin/secret.txt` or
> `/public/%2E%2E/admin/secret.txt`) could still reach files behind a guarded route through
> `Echo.StaticFS` and `Echo.Static`. The complete fix is in v5.2.1 and v4.15.4. The affected and
> patched versions above have been corrected. Upgrade to v5.2.1 / v4.15.4 or later.

### 5.3 Disagreement, recorded explicitly

- **Direction:** the repository-scoped (vendor) record is **broader** than every mirror: it says
  `github.com/labstack/echo/v4 < 4.15.4`, whereas all mirrors still say `< 4.15.3`.
- **Mirrors that lag** (fixed at 4.15.3): GitHub global advisory API/advisory-database/rendered page,
  OSV GHSA-vfp3-v2gw-7wfq, OSV GO-2026-6293, the OSV CVE-2026-55677 GIT events (fixed at
  8800212a…, the v4.15.3 commit), the CVE CNA and NVD.
- **Cause confirmed in code:** v4.15.3 added `internal/pathutil.HasEncodedPathSeparator` which only
  rejects `%2F`/`%5C`; v4.15.4 removed it in favour of `EnablePathUnescapingStaticFiles` (no
  unescaping by default). The diff `v4.15.2 → v4.15.3` touches `echo_fs.go`, `middleware/static.go`
  and adds `pathutil`; `v4.15.3 → v4.15.4` replaces that approach. So 4.15.3 was genuinely partial,
  exactly as the vendor update says.
- **This does not change the affected verdict:** `4.15.2 < 4.15.3 < 4.15.4`, so v4.15.2 is inside
  **both** the lagged and corrected ranges.

### 5.4 Source-level corroboration that the snapshot is vulnerable

```bash
cd /tmp/echo_extract && grep -n 'func (r \*Router) Find\|path :=\|URL\.Path\|EscapedPath\|RawPath' router.go | head -30
grep -n 'func (c \*context) Path\|SetPath' context.go | head
sed -n '55,75p' echo_fs.go
grep -rn '\.Find(\|GetPath(' *.go | head -20
sed -n '945,965p' echo.go
```

- `echo.go:662/667` call `Find(r.Method, GetPath(r), c)`; `GetPath` returns `r.URL.RawPath` when it is
  non-empty. For `/admin%2Fsecret.txt`, net/http sets `RawPath`, so routing sees the still-encoded
  single segment and the `admin/*` guard route never matches.
- `echo_fs.go:57-65` `StaticDirectoryHandler` unconditionally calls `url.PathUnescape()` on the
  wildcard when `disablePathUnescaping` is false, turning `%2F` back into `/` after routing.
- v4.15.2 has no encoded-separator check (`grep -c useEscapedPathForRouting` = 0; no `pathutil`).

*(Note: the advisory's snippet references `useEscapedPathForRouting`, a symbol that exists in no
v4.15.x tag — it appears to come from a newer v4 branch. The behavior it describes is nevertheless
present in v4.15.2 through `GetPath()` + `StaticDirectoryHandler`.)*

**Anchor conclusion:** `affected = true`, with multiple public `https://` sources, and the mechanism
is present in the exact snapshot.

---

## 6. Leakage scan (disclosure item, not a failure)

```bash
cd /tmp/echo_extract && grep -rnoE 'CVE-[0-9]{4}-[0-9]+|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}|GO-[0-9]{4}-[0-9]+' . | sort | uniq -c
grep -rn 'CVE-2026-55677\|GHSA-vfp3-v2gw-7wfq\|GO-2026-6293' . || echo "(none found)"
grep -n '4\.15\.[0-9]' CHANGELOG.md | head -20
```

Result:

- Historical identifiers in `CHANGELOG.md`: `CVE-2023-39325`, `CVE-2023-44487`, `CVE-2024-51744`
  (the packet's three CVEs) plus `GO-2023-2402`, `GO-2024-2687`, `GO-2024-3321`, `GO-2024-3333`,
  `GO-2025-3487`, `GO-2025-3503`, `GO-2025-3595`.
- **None** of this snapshot's own identifiers (`CVE-2026-55677`, `GHSA-vfp3-v2gw-7wfq`,
  `GO-2026-6293`) occurs anywhere in the tree.
- No `.git` metadata. So this is a pre-existing changelog disclosure of historical advisories, not a
  leak of the evaluation anchor. Recorded, not treated as a failed check.

---

## 7. Verdict and residual limitations

**ACCEPT.** Every mandatory check held:

1. Archive and manifest hashes match the packet; 110 regular files, no `.git`, no symlinks/hardlinks/
   gitlinks; counts reconcile.
2. The archive file set is *exactly* the tag tree set (names, modes, and git blob SHAs), not merely
   the same count.
3. `v4.15.2` resolves (lightweight) to `25685e6f5f7b0683105d1386db46ae48eb3de028`, tree
   `d4529971662ff21db287d808d3250058518fff5d`, `go.mod` module `github.com/labstack/echo/v4`.
4. It is a stable release dated 2026-05-01 (175 days old on 2026-10-23, inside a window opening
   2022-10-23).
5. A real build with a checksum-verified `go1.26.10` succeeds: `go build ./...` exit 0 and
   `go vet ./...` exit 0.
6. The anchor genuinely affects v4.15.2 in every public source consulted, under both the corrected
   `< 4.15.4` vendor range and the lagged `< 4.15.3` mirrors.

Limitations (also in `review.jsonl`):

- NVD's rendered detail page is a JS shell; NVD facts come from the NVD 2.0 API. NVD has no CPE
  configurations and `vulnStatus` is `Deferred`; the only CVSS metric is the Secondary 7.5 from
  `security-advisories@github.com`.
- Unauthenticated GitHub API calls were rate-limited (`403`); the same public endpoints were read with
  the authenticated `gh api` client, and both rendered pages were parsed directly.
- The advisory's code snippet uses symbols absent from v4.15.2; the vulnerable behavior was verified
  from this snapshot's own `GetPath()`/`StaticDirectoryHandler` instead.
- The legacy `github.com/labstack/echo` (v3) `<= 3.3.10` range was not tree-verified; it does not
  affect this v4 snapshot decision.
- The repository advisories listing page did not show this GHSA on its first page (paginated); the
  direct advisory page/API was used.
- No live exploit was run; the affected determination is source + advisory based.
- The repository-scoped API's `first_patched_version` is `null` although its range string is
  `< 4.15.4`; the rendered page explicitly lists patched `4.15.4`, so this is a field-population
  quirk, not a range disagreement.
