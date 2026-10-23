# Independent selection review — gin-gonic/gin v1.9.0

- **Snapshot:** `snap_33d2dbd3f77388df`
- **Repo:** gin-gonic/gin (`repo_id` 20904437)
- **Proposed target:** tag `v1.9.0`, commit `ea03e10384502e1baf6f560a2b0ea32c342ede5b`
- **Reviewer:** `independent-selection-reviewer-gin-v1.9.0-r1`
- **Reviewed at (UTC):** 2026-10-22T18:00:50Z (local review date 2026-10-23)
- **Verdict:** **ACCEPT**
- **build_ok:** **true**

Packet read: `v031/reviews/selection_packets/20904437_gin-gonic__gin.json`.
Allowed data rows read: `data/snapshot_exports.jsonl` line 6 and
`data/snapshot_audit_exports.jsonl` line 6 (both for `snap_33d2dbd3f77388df`).
Nothing else in the forbidden set was opened.

Environment used for all network steps:

```bash
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
```

Scratch work: `/tmp/selrev_gin_33d2/` (clone, extracts, build, scripts). The exported
archive and manifests were treated as untrusted: extracted into fresh empty directories;
the only thing executed from the extract was the Go toolchain.

---

## Check 1 — Tag resolution

```bash
git ls-remote --tags https://github.com/gin-gonic/gin.git 'refs/tags/v1.9.0*'
# ea03e10384502e1baf6f560a2b0ea32c342ede5b	refs/tags/v1.9.0
git clone https://github.com/gin-gonic/gin.git /tmp/selrev_gin_33d2/repo/gin
cd /tmp/selrev_gin_33d2/repo/gin
git cat-file -t refs/tags/v1.9.0          # -> commit   (lightweight tag)
git rev-parse refs/tags/v1.9.0            # -> ea03e10384502e1baf6f560a2b0ea32c342ede5b
git show -s --format='%H %T %aI %cI %s' ea03e10384502e1baf6f560a2b0ea32c342ede5b
# ea03e10384502e1baf6f560a2b0ea32c342ede5b 6f69147e1e437ae784e04246b747b6377840f2ae \
#   2023-02-21T17:20:32+08:00 2023-02-21T17:20:32+08:00 docs(readme): release v1.9.0 version (#3474)
```

- `git ls-remote` emitted a single ref line with **no `^{}` peeled companion**, which is
  the signature of a lightweight tag; `git cat-file -t` confirms the ref points directly
  at a `commit` object rather than an annotated `tag` object.
- Tag type: **lightweight**. Peeled commit = `ea03e103…`, which equals the packet
  `commit_sha` and `resolved_tag_sha`. Tree = `6f69147e…`, which equals the packet
  `tree_sha`.
- Commit date **2023-02-21T17:20:32+08:00** (= 2023-02-21T09:20:32Z), subject
  `docs(readme): release v1.9.0 version (#3474)`.
- Stable release: the name has no `-rc/-alpha/-beta/-dev` suffix, the commit is the
  release announcement, and it is followed by the `v1.9.1` release. This is a stable
  release tag, not a pre-release or distribution tag.

**Result: PASS.**

## Check 2 — Export integrity

```bash
sha256sum exports/gin-gonic__gin/snap_33d2dbd3f77388df.tar.gz
# 3727bad543059a481677bb78cacd695c861dfe487fa26c130ad6d38883dbaa75
sha256sum exports/gin-gonic__gin/snap_33d2dbd3f77388df.manifest.jsonl
# af9462c5b84f9b7efe3290ee02016717a374fc37ca963a7b03e37496fbdbec94
stat -c '%s' exports/gin-gonic__gin/snap_33d2dbd3f77388df.tar.gz   # 162798
tar -tzf …/snap_33d2dbd3f77388df.tar.gz | wc -l                    # 124
tar -tzf …/snap_33d2dbd3f77388df.tar.gz | grep -E '(^|/)\.git(/|$)' # none
tar -tzf …/snap_33d2dbd3f77388df.tar.gz | grep -E '(^/|(^|/)\.\.(/|$))' # none
tar -tvzf …/snap_33d2dbd3f77388df.tar.gz | awk '{print substr($1,1,1)}' | sort | uniq -c
# 124 '-'   -> all regular files, zero symlinks
```

| fact | packet | recomputed | match |
|---|---|---|---|
| archive sha256 | `3727bad5…dbaa75` | `3727bad5…dbaa75` | yes |
| manifest sha256 | `af9462c5…dbec94` | `af9462c5…dbec94` | yes |
| archive bytes | 162798 | 162798 | yes |

- No `.git/` path in the archive; no absolute or `..` paths.
- Counts: `exported_file_count 124 + symlink_count 0 + gitlink_count 0 = 124 = tree_file_count`.
- `missing_from_archive_count` 0, confirmed independently by extracting all 124 files.

**Result: PASS.**

## Check 3 — Manifest vs git tree

```bash
git ls-tree -r ea03e10384502e1baf6f560a2b0ea32c342ede5b | wc -l     # 124
git ls-tree -r ea03e10384502e1baf6f560a2b0ea32c342ede5b | awk '{print $1}' | sort | uniq -c
# 124 100644
# per blob:
git cat-file blob <blob> | sha256sum
python3 -I /tmp/selrev_gin_33d2/scratch/compare_tree.py <manifest> /tmp/selrev_gin_33d2/scratch/tree_table.tsv
# tree entries: 124
# manifest entries: 124
# path sets equal: True
# mismatches: 0
# RESULT: OK
```

I verified **all 124** entries (not only a sample): path set, type, mode (`100644` ↔
`0644`) and per-file sha256 against `git ls-tree -r` + `git cat-file blob`.

Additionally, extracting the archive and hashing every file
(`python3 -I …/verify_manifest.py`) gave: 124 manifest entries, 124 extract files,
0 missing, 0 extra, 0 per-file problems.

**Result: PASS.**

## Check 4 — Leakage / audit export

Row read from `data/snapshot_audit_exports.jsonl` (line 6):

- `remaining_advisory_id_count`: **0**
- `excluded_count`: **1**, excluded path **`CHANGELOG.md`** (advisory ids `CVE-2020-28483`)
- `redacted_count`: **0**, `redacted_paths`: `[]`
- `audit_file_count`: 123; `source_completeness`:
  `full_tracked_tree_minus_advisory_docs_with_id_redaction_in_code`

Independent verification:

```bash
sha256sum …/snap_33d2dbd3f77388df.audit.tar.gz        # 3c6bf2b7…b7686  (matches row)
sha256sum …/snap_33d2dbd3f77388df.audit.manifest.jsonl # d5ba6c14…d5be1 (matches row)
tar -xzf …/….audit.tar.gz -C /tmp/selrev_gin_33d2/audit_extract
find audit_extract -type f | wc -l                    # 123
ls audit_extract/CHANGELOG.md                         # absent
grep -rInE 'CVE-[0-9]{4}-[0-9]+|GHSA-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}|GO-[0-9]{4}-[0-9]+' audit_extract
# no matches
```

Audit manifest verified against the audit extract: 123/123 paths, 0 sha mismatch, 0 extras.
Compared to the full manifest: exactly `CHANGELOG.md` removed, nothing added, and the 123
common paths are byte-identical.

**Result: PASS** (remaining advisory ids 0, excluded 1, redacted 0).

### Leakage note (packet imprecision)

The full export (124 files) is not advisory-free: `CHANGELOG.md` contains
`CVE-2020-28483` and also `GO-2022-0969`, `GO-2022-0288`, `GO-2023-1571`, `GO-2022-1144`.
The packet's `leakage_facts` enumerate only CVE/GHSA identifiers (`cve_id_count: 1`,
`ghsa_id_count: 0`) and therefore omit the four GO-* identifiers. Because the audit export
excludes the file entirely, this does not change `remaining_advisory_id_count == 0`.
Acceptance assumes the **audit export** is the evaluation artifact.

## Check 5 — Anchor (CVE-2023-29401)

Public sources independently fetched (not taken from the packet):

```bash
curl -s https://api.osv.dev/v1/vulns/CVE-2023-29401
curl -s -H 'Accept: application/vnd.github+json' \
     https://api.github.com/advisories/GHSA-2c4m-59x9-fr2g
curl -s 'https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2023-29401'
```

| source | affected range | fixed | v1.9.0 affected |
|---|---|---|---|
| OSV (`cna_assigner: Go`) | `>=1.3.1-0.20190301021747-ccb9e902956d, <1.9.1`; versions list includes `v1.9.0`; GIT fixed `4ea0e648…` | v1.9.1 | yes |
| GHSA-2c4m-59x9-fr2g | `>= 1.3.1-0.20190301021747-ccb9e902956d, < 1.9.1` | first patched `1.9.1` | yes |
| NVD | CPE `versionStartIncluding 1.3.1-0.20190301021747-ccb9e902956d`, `versionEndExcluding 1.9.1` | v1.9.1 | yes |

- Severity: NVD primary and CISA-ADP 4.3 MEDIUM, GHSA `medium`, same vector
  `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N` — matches the packet.
- **Fix commit:** `4ea0e648e38a63d6caff14100f5eab5c50912bcd` (the v1.9.1 release commit);
  the actual patch is `2d4bbec941551479b1fdf1e54ece03e6e82a7e72` (PR #3556,
  "fix lack of escaping of filename in Content-Disposition").
- **Ancestry:**
  ```
  git merge-base --is-ancestor ea03e103 4ea0e648   # exit 0  -> snapshot is ancestor of fix
  git merge-base --is-ancestor 4ea0e648 ea03e103   # exit 1  -> fix is NOT ancestor of snapshot
  git merge-base ea03e103 4ea0e648                 # ea03e103…
  git merge-base --is-ancestor ea03e103 2d4bbec    # exit 0  -> patch is a descendant of snapshot
  ```
  So the snapshot predates the fix and cannot contain it.
- **Vulnerable code present at the snapshot:** `context.go:1057-1059` sets
  `Content-Disposition` from the raw filename with no escaping; the v1.9.1 diff adds
  `escapeQuotes()` to exactly that line.
- **Newest stable release covered?** Yes. `v1.9.0` is the highest version in OSV's
  affected list; the range ends at `<1.9.1`.
- **Later releases affected?** No. v1.9.1 (`4ea0e648`, 2023-05-31) and every later tag
  (v1.10.0, v1.10.1, v1.11.0, v1.12.0) are outside the range.

**Result: PASS.**

## Check 6 — Build feasibility

Fresh extract of the exported archive into an empty directory:

```bash
export PATH="$HOME/.local/toolchain/go1.27.3/bin:$PATH"
export GOFLAGS=-mod=mod GOTOOLCHAIN=local
export GOMODCACHE=/tmp/selrev_gin_33d2/gomodcache
export GOCACHE=/tmp/selrev_gin_33d2/gocache
export GOPATH=/tmp/selrev_gin_33d2/gopath
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
rm -rf /tmp/selrev_gin_33d2/build && mkdir -p /tmp/selrev_gin_33d2/build
tar -xzf exports/gin-gonic__gin/snap_33d2dbd3f77388df.tar.gz -C /tmp/selrev_gin_33d2/build
cd /tmp/selrev_gin_33d2/build
go version            # go1.27.3 linux/amd64
go build ./...        # exit 0, real 0m15.3s (deps downloaded through the proxy)
go vet ./...          # exit 0, real 0m3.9s
go test -run='^$' -count=1 ./...   # exit 0, all packages compile
# ok gin, ok binding, ? ginS [no test files], ok internal/bytesconv,
# ? internal/json [no test files], ok render
```

`go.mod`/`go.sum` sha256 after the builds are identical to the manifest entries
(`66eb675c…` / `65c079e4…`); `diff -rq` against the untouched extract shows no changes.
The build is reproducible from the export as-is.

**build_ok = true.**

## Check 7 — Release sanity

- Release date: **2023-02-21** (2023-02-21T09:20:32Z).
- Dataset window opens **2022-10-23**; the tag is **after** the window, so not flagged.
- Age at 2026-10-23: **1340 days** (≈ 3.67 years), **not over four years**.
- It is superseded by v1.9.1 … v1.12.0, but it is the newest release affected by the
  anchor, which is expected for a vulnerable target. Not "clearly obsolete" under the
  stated rule.

**No release-sanity problem.**

## Check 8 — Verdict

Checks 1–5 pass, the build is feasible, and there is no release-sanity problem.
**Verdict: accept.**

---

## Discrepancies between packet and observation

1. **Anchor `published_at`.** Packet: `2023-05-12T20:19:25Z`. That is exactly the GitHub
   Advisory (GHSA-2c4m-59x9-fr2g) publication time; OSV records `2023-06-08T20:27:15Z`
   and NVD `2023-06-08T21:15:16Z`. Source-choice difference only; the affected/fixed facts
   agree across all three sources.
2. **Leakage enumeration.** Packet reports `cve_id_count: 1` (CVE-2020-28483) and
   `ghsa_id_count: 0` but does not count the four `GO-*` identifiers also present in
   `CHANGELOG.md` (GO-2022-0969, GO-2022-0288, GO-2023-1571, GO-2022-1144). The audit
   export removes the whole file, so `remaining_advisory_id_count` is still 0.
3. Nothing else disagreed: tag ref/commit/tree, archive and manifest sha256, byte sizes,
   file counts, and per-file content all matched the packet and the allowed data rows.

## Artifacts written

- `/home/luchitong/work/repo-vuln-50-v031/runs/selection_review_gin_v190/verdict.json`
- `/home/luchitong/work/repo-vuln-50-v031/runs/selection_review_gin_v190/REVIEW.md`
