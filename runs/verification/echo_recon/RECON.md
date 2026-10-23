# Recon: labstack/echo (repo_id 31504491)

Date: 2026-10-23. Read-only. No dataset rows written, `data/` and `v031/` untouched.

## Recommendation (single strong pair)

**CVE-2026-55677 / GHSA-vfp3-v2gw-7wfq / GO-2026-6293** — "Encoded slash (%2F) bypasses route-level protection and exposes static files" (CWE-22, CVSS 7.5 HIGH, `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`).

| Item | Value |
|---|---|
| Module | `github.com/labstack/echo/v4` (canonical v4 module) |
| **Vulnerable tag (candidate target)** | `v4.15.2` |
| Vulnerable commit SHA | `25685e6f5f7b0683105d1386db46ae48eb3de028` |
| Vulnerable tree | `d4529971662ff21db287d808d3250058518fff5d` |
| Vulnerable release date | 2026-05-01 (commit `Merge pull request #2963 from aldas/v4_changelog_4_15_2`) |
| **Fixed tag (first fixed)** | `v4.15.3` |
| Fixed commit SHA (deref) | `8800212ad4392d3f5af052f3042aca62cc5911a7` (annotated tag object `b1febadc3ef9d49d0dcd7bdb0f6255344943f1a0`) |
| Fixed tree | `aa3f4a9ddd79eb018ffa56ed698d825269c4a923` |
| **Fix commit (v4)** | `c3fa2a27ff92b2b8db360de614f999ef1da24725` — "fix(static): reject encoded path separators that bypass route-level middleware (#3011)"; v4 backport of GHSA-vfp3-v2gw-7wfq |
| v5 counterpart fix | `8d1ae9d3360a71672418856d58753af25f2c3986` (#3009), fixed in `v5.2.0` |

Affected ranges (GHSA/GO): `github.com/labstack/echo/v4` `< 4.15.3`; `github.com/labstack/echo/v5` `>= 5.0.0, < 5.2.0`; legacy `github.com/labstack/echo` `<= 3.3.10`. Highest vulnerable v4 tag = `v4.15.2`; first fixed v4 tag = `v4.15.3`. v5 equivalent: vulnerable `v5.1.1` → fixed `v5.2.0`.

### Vulnerable code (present at v4.15.2, quoted)

- `echo_fs.go` — `StaticDirectoryHandler` (func starts line 57). Line 61 `tmpPath, err := url.PathUnescape(p)`; line 69 `name := filepath.ToSlash(filepath.Clean(strings.TrimPrefix(p, "/")))`.
- `middleware/static.go` — `StaticWithConfig`, line 173 `p, err = url.PathUnescape(p)`.
- `echo.go` — `GetPath` lines 953-960: `path := r.URL.RawPath; if path == "" { path = r.URL.Path }` (router matches on raw, still-encoded path, so `%2F` is not a segment boundary during routing, then the handler unescapes it into a real separator).

### Fix (present at v4.15.3, absent at v4.15.2)

- `echo_fs.go`: before unescaping, `if pathutil.HasEncodedPathSeparator(p) { return ErrNotFound }`; and `filepath.ToSlash(filepath.Clean(...))` replaced by `path.Clean(...)`.
- `middleware/static.go`: same `pathutil.HasEncodedPathSeparator(p)` guard added.
- New `internal/pathutil/pathutil.go` with `HasEncodedPathSeparator` (%2F/%2f and %5C/%5c).

### Ancestry verification (`git merge-base --is-ancestor`)

- `c3fa2a27` (#3011) ancestor of `v4.15.3` (8800212): **YES**; ancestor of `v4.15.2` (25685e6): **NO**.
- `8d1ae9d` (#3009) ancestor of `v5.2.0` (5786024e): **YES**; ancestor of `v5.1.1`: **NO**.
- `git tag --contains c3fa2a27` → `v4.15.3, v4.15.4, v4.16.0, v4.16.1` (v4 line only). `git tag --contains 8d1ae9d` → `v5.2.0` onward (v5 line only). v4 and v5 are separate branches (`origin/v4`, `origin/v5`/`master`).

### Functional reproduction (strongest evidence)

Ran the fix commit's own regression tests against both trees:

- On **v4.15.3**: `TestStaticDirectoryHandler_EncodedSeparatorDoesNotBypassRoute`, `TestGroupStaticFS_EncodedSeparatorDoesNotBypassRoute`, `TestStatic_EncodedSeparatorDoesNotBypassRoute` all **PASS** (`/admin%2Fsecret.txt` → 404).
- On **v4.15.2** (same test files copied in): all **FAIL** — `GET /admin%2Fsecret.txt` returns **200 with body "TOP-SECRET"**, i.e. the protected `/admin` middleware is bypassed and the file is disclosed. Same for `%2f`, `%5C`, and group-mounted `StaticFS`.

### Buildability

- `go version`: **go1.26.10 linux/amd64** (downloaded from dl.google.com; `go.mod` requires `go 1.25.0`, so toolchain >= 1.25.0 needed — the system has no Go pre-installed, apt candidate is only 1.22).
- `go build ./...` at clean `git archive v4.15.2` extraction: **exit 0**, all modules resolved via `GOPROXY=https://proxy.golang.org,direct` (deps: gommon v0.5.0, fasttemplate v1.2.2, x/net v0.53.0, x/crypto v0.50.0, x/time v0.15.0, etc.). No blocked module.
- `go build ./...` at v4.15.3: **exit 0**.

### Sanity

- Four-year window (from 2022-10-23): `v4.15.2` released 2026-05-01 — **inside**.
- Stable release: `v4.15.2` is a plain semantic tag (no rc/beta/alpha). **Yes**.

## Disagreements between sources (CVE-2026-55677)

1. **Fix commit SHAs differ.** GHSA-vfp3-v2gw-7wfq and GO-2026-6293 reference fix commits `8d1ae9d…` and `c3fa2a27…`. The CVE OSV record's `GIT` range instead lists `fixed: 8800212…` (= `v4.15.3^{}`) and `fixed: 5786024e…` (= `v5.2.0^{}`), which are the *Changelog/release* commits, not the fix PRs. Verified mapping: `c3fa2a27` is the real v4 fix (ancestor of 8800212), `8d1ae9d` is the real v5 fix (ancestor of 5786024e).
2. **Affected product set.** NVD affected versions are `< 4.15.3` and `>= 5.0.0, < 5.2.0` only; it omits the legacy unversioned `github.com/labstack/echo` `<= 3.3.10` range that GHSA lists as `last_affected`.
3. Severity is consistent (HIGH / 7.5 / CWE-22) across GHSA, OSV, GO, NVD. NVD marks the CVE `vulnStatus: Deferred` (GitHub's Secondary CVSS stands as the only scored metric; CISA SSVC = `poc`, `automatable: yes`, `technicalImpact: partial`).

## Second candidate (rejected): CVE-2026-25766 / GHSA-pgvm-wxw2-hrv9 / GO-2026-4502

Windows-only backslash traversal in `middleware.Static` default filesystem. Affects only `github.com/labstack/echo/v5` `5.0.0 – 5.0.2`, fixed in `v5.0.3` (commit `b1d443086ea27cf51345ec72a71e9b7e9d9ce5f1`, merge of PR #2891; it *is* `v5.0.3^{}`). CWE-22, **MODERATE** (CVSS 5.3). Counter-arguments: Windows OS required to trigger, exposure restricted to process working directory and subfolders, lower severity, v5-module-only. CVE-2026-55677 (cross-platform, HIGH, canonical v4 module) is the stronger target.

## "Further 2026 advisories" — repository-scoped, not in the global advisory databases

Ten of `GHSA-23wf-92cp-8pcj`, `GHSA-246p-cpwv-v3jq`, `GHSA-2ffq-g2xg-c22p`, `GHSA-375p-5qhx-8wq4`, `GHSA-3pmx-cf9f-34xr`, `GHSA-xwq5-6cqp-vx96`, `GHSA-v753-g4cw-jm48`, `GHSA-h9g5-28mm-hx3g`, `GHSA-r7w9-592q-9vg4`, `GHSA-99jh-6h7p-pp36`:
- OSV `https://api.osv.dev/v1/vulns/<ID>` → `{"code":5,"message":"Vulnerability not found"}`.
- `github/advisory-database` raw JSON (github-reviewed/2026/09/ and unreviewed/2026/09/) → HTTP **404**.
- No NVD CVE aliases exist for them in any fetched record.

They appear only in the dataset's `discovery_v3` `GitHubRepositoryAdvisory` rows (`adv3_*` candidate_ids), which came from GitHub's own
`/repos/labstack/echo/security-advisories` API response (`runs/discovery_v3/repo_advisories/labstack__echo.json`, retrieved
2026-10-21), where all ten are `state: published` with a GHSA id and an `html_url`.

**Correction (2026-10-23, verified during follow-up):** they are not fabricated. The `html_url` pages are live
repository-scoped advisories, e.g. `https://github.com/labstack/echo/security/advisories/GHSA-3pmx-cf9f-34xr` returns HTTP 200 with
the title "Echo static file middleware route protection bypass via encoded dot-dot traversal", while a control non-existent GHSA on
the same path returns HTTP 404 (9 bytes). `https://github.com/advisories/GHSA-3pmx-cf9f-34xr` returns 404, so these advisories are
published only in the repository's own Security tab and have never entered the global GitHub advisory database or OSV.

Consequence for evaluation-target selection: a repository-scoped GHSA can be cited as an `official_upstream` advisory, but it was not
independently reviewed by GitHub and carries no CVE; better targets are the globally indexed ones (CVE-2026-55677 /
GHSA-vfp3-v2gw-7wfq). Do not discard the repository-scoped rows as invalid — they remain candidates pending source-level review.

## Strongest counter-arguments to the recommendation

1. **Deployment precondition.** The bypass requires a specific (but common) layout: a protected route prefix whose middleware guards a path that is also inside a statically-served root (e.g. `e.Group("/admin", auth)…` + `e.StaticFS("/", …)` with `admin/secret.txt` on disk). It is not an arbitrary file read from any location, nor a full path traversal (`..` is still cleaned by `path.Clean`). Scope = unauthorized read of files already under the static root.
2. **NVD analysis deferred.** Only GitHub's (Secondary) CVSS exists; NVD has not completed independent scoring.
3. **Fresh CVE.** Fixed only ~4.5 months before today; fine for the four-year window, but "newness" means fewer public secondary analyses.
4. **Module/version pinning.** The advisory spans v4 and v5 modules; the eval must pin `github.com/labstack/echo/v4` @ `v4.15.2` vs `v4.15.3` (or v5 @ `v5.1.1` vs `v5.2.0`).
5. **Toolchain floor.** `go.mod` says `go 1.25.0`, so the harness needs a Go toolchain >= 1.25 (verified with 1.26.10).

## Raw sources

Kept under `runs/verification/echo_recon/sources/`:
- `osv/` — OSV records for all 14 advisory IDs + 4 GO IDs + 4 CVE IDs (including the 46-byte "not found" bodies), plus `NOT_FOUND_advisories.txt`.
- `nvd/` — NVD API JSON for CVE-2026-55677, CVE-2026-25766, CVE-2022-40083.
- `ghsa/` — GitHub advisory API attempts (rate-limited bodies; advisory content is mirrored in the OSV GHSA records).
- `git_tags.txt` — `git ls-remote --tags` output.
