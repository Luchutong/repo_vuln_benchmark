# Independent selection review — `lodash/lodash` @ tag `4.17.23`

- **review_id:** `selrev_3955647_snap_033e9a6478460d9b`
- **snapshot:** `snap_033e9a6478460d9b`
- **repo:** `lodash/lodash` (repo_id `3955647`), npm `lodash`
- **commit:** `dec55b7a3b382da075e2eac90089b4cd00a26cbb`
- **reviewed_by:** `independent-selection-reviewer-lodash-2026-10-23`
- **reviewed_at:** `2026-10-22T19:47:24Z`
- **verdict:** **accept**

All eight required checks pass. The exported tree is a byte-faithful export of the
tagged commit, it is stable and pre-fix for `CVE-2026-4800` / `GHSA-r5fr-rjxr-66jc`,
it builds and its test suite passes, and the plain export contains no reference to
the target advisory. Discrepancies with the packet are listed at the end; none of
them change the verdict.

## Environment and method

Everything was re-derived from public sources and the named artifacts. The plain
and audit archives were extracted into fresh, empty `/tmp` directories
(`/tmp/selrev_lodash/plain`, `/tmp/selrev_lodash/audit`); helper scripts were kept
outside both trees in `/tmp/selrev_lodash/scripts` and executed with
`python3 -I`. Upstream was cloned into `/tmp/selrev_lodash/upstream/lodash`.
Network ran through `https_proxy=http://172.21.96.1:7890`.

## 1. Tag resolution — PASS

```
git ls-remote --tags https://github.com/lodash/lodash
  fd6aaf9433b9bc56452ffc9469e4c6f5793deb2b  refs/tags/4.17.23
  dec55b7a3b382da075e2eac90089b4cd00a26cbb  refs/tags/4.17.23^{}
```

`4.17.23` is an **annotated, PGP-signed** tag:

- tag object `fd6aaf9433b9bc56452ffc9469e4c6f5793deb2b`, type `tag`,
  `object dec55b7a...`, `tag 4.17.23`, tagger `jdalton <john.david.dalton@gmail.com>`
  at `1769016448 -0500` (2026-01-21T17:27:28Z), OpenPGP signature block present.
- peeled commit `dec55b7a3b382da075e2eac90089b4cd00a26cbb`
  ("Bump main to v4.17.23 (#6088)"), author/committer date
  **2026-01-21T12:21:04-05:00 = 2026-01-21T17:21:04Z**, parent `19c9251b3631...`.
- tree `994d2c60471db4e562d9409c8ee3066c7e46b6de`.

The peeled commit equals the packet's `commit_sha`, and the tree equals the packet's
`export_facts.tree_sha` (the packet records `tag_commit_tree_sha: null`; the measured
value is `994d2c60471db4e562d9409c8ee3066c7e46b6de`).

## 2. Archive integrity — PASS

```
sha256(snap_033e9a6478460d9b.tar.gz)           = 73bfcce0d6425f9a75365bf6d67ccda83c5242b102f62e7d33fc8cc96cd22c91  (880722 bytes)
sha256(snap_033e9a6478460d9b.manifest.jsonl)   = b020932c58c38009899004233220b28a5565c288ff7205b15d4e0a6766464551  (29177 bytes)
```

Both match `export_facts` exactly, including the byte size 880722.

Fresh extraction of the plain archive:

- **159 regular files, 0 symlinks, 0 gitlinks, 0 other entries, 0 `.git` directories.**
  The tar contains 159 `isfile()` members only; every entry has uid/gid 0.
- Manifest has 159 unique entries (no duplicate paths), all `type: file`, all mode
  `0644`; the extracted filesystem has exactly the same path set (0 missing, 0 extra),
  and size/sha256/mode match for all 159.
- `git ls-tree -r -z dec55b7a...` from a full clone returns **159 blobs, all mode
  100644**, with a **path set identical** to the manifest's.
- For every one of the 159 files, the recomputed git blob identity
  `sha1("blob <len>\0" + content)` equals the ls-tree blob sha (**0 mismatches**),
  and sha256/size equal the manifest values (**0 mismatches**).
- `tree_file_count 159 = exported_file_count 159 + symlink 0 + gitlink 0`; the tree
  sha of the commit is `994d2c60471db4e562d9409c8ee3066c7e46b6de`, matching
  `export_facts.tree_sha`.

Conclusion: the archive is a faithful, complete export of the tagged commit's tree,
with no `.git` metadata and no symlinks/gitlinks.

## 3. Audit export — PASS (with one scoped limitation)

```
sha256(snap_033e9a6478460d9b.audit.tar.gz)          = 7d499183786306656662d472dc42794632f91980831bb2b472dd766c5ad34126  (878617 bytes)
sha256(snap_033e9a6478460d9b.audit.manifest.jsonl)  = 3497ede2c441d3f5fc00bb3bc33cdbb761537b60397e4a810f6a4d7ea1b3797f  (29009 bytes)
```

The packet does not declare audit hashes; these are my measured values. Extracted
audit tree: **158 regular files, 0 symlinks, 0 gitlinks, 0 `.git`**; its manifest
matches the extracted files exactly (0 missing/extra, all sizes/sha256/modes match).

Plain vs audit diff (computed by comparing the two manifest objects file by file):

- excluded: `threat-model.md` (the only advisory-bearing documentation file);
- redacted: `lodash.js`, `dist/lodash.js`, `test/test.js`.

The content diff is exactly three comment lines in which the historical identifier
`GHSA-xxjr-mmjv-4gpg` is replaced by `ADVISORY-ID-REDACTED`:

```
lodash.js       : // Prevent prototype pollution, see: .../GHSA-xxjr-mmjv-4gpg     -> .../ADVISORY-ID-REDACTED
dist/lodash.js  : same comment                                                      -> same
test/test.js    : 2x "// Prevent regression for .../GHSA-xxjr-mmjv-4gpg"            -> .../ADVISORY-ID-REDACTED
```

Sizes change by +1/+1/+2 bytes (the marker is 1 byte longer than each ID); no
executable statement changes. `node --check` passes on all three redacted files, and
the redacted `lodash.js` still contains the vulnerable `Function(importsKeys, ...)`
sink and still reproduces the PoC (see §6).

Prohibited-content scan of the audit tree:

- no `.diff`/`.patch`/fix files, no advisory list documents, no files named like
  ground-truth/benchmark/label; content grep for `ground[_ -]?truth|oracle|benchmark
  label|expected answer` returns nothing. The `perf/` directory is lodash's own
  upstream performance suite (`perf/perf.js`, `perf/index.html`, `perf/asset/perf-ui.js`),
  not dataset benchmark data.
- `grep -a` for `CVE-[0-9]{4}-[0-9]{4,}` and `GHSA-[0-9a-z]{4}-...` over the
  extracted audit tree and over the audit tar.gz returns **0 identifiers**; an
  independent full-file regex scan of the audit tree finds **0 files with advisory IDs**.

`remaining_advisory_id_count`: the recorded row lives in `data/snapshot_audit_exports.jsonl`,
which this review may not read. Instead I rescanned the produced artifact: **0**. The
allowed aggregate report `v031/reports/AUDIT_EXPORT_REPORT.json` (tool
`build_audit_exports/1.1`) records 28/28 rows exported with an empty `failures` list.

The observed exclusion/redaction set is exactly what the documented build rule
(`v031/scripts/build_audit_exports.py`: exclude advisory-bearing doc paths, redact
IDs in code) derives from an independent scan of the plain tree — 4 advisory-bearing
files, 1 doc (excluded) + 3 code (redacted). I could not read the declared per-path
list itself, only reproduce its derivation.

## 4. Leakage of the target — PASS

Independent substring scan (case-insensitive, all 159 plain files, binary included):
`CVE-2026-4800` and `GHSA-r5fr-rjxr-66jc` occur **nowhere** in the plain export
(0 hits), and nowhere in the audit export.

Historical identifiers that do appear in the plain export:

| Identifier | Location(s) | What it is |
|---|---|---|
| `CVE-2019-10744` | `threat-model.md` | historical prototype pollution example |
| `CVE-2020-28500` | `threat-model.md` | historical ReDoS example |
| `CVE-2021-23337` | `threat-model.md` | historical `_.template` `variable`-option command injection |
| `GHSA-xxjr-mmjv-4gpg` | `lodash.js:4374`, `dist/lodash.js`, `test/test.js` (2x) | **CVE-2025-13465**, prototype pollution in `_.unset`/`_.omit` (verified via OSV) |

Assessment: none of these leaks the target answer. `CVE-2021-23337` is the *prior,
incomplete* fix that the target advisory describes as its root cause, so it is
topical context and could nudge a researcher toward `_.template`, but it does not
name the new CVE, the `options.imports` key vector, the `assignInWith`/inherited-key
aspect, or the fix. `GHSA-xxjr-mmjv-4gpg` is an unrelated 2025 prototype-pollution
CVE near `baseUnset`. The packet's own `leakage_facts` (3 CVEs, 1 GHSA, 4 files) was
reproduced exactly.

## 5. Build / test — PASS

Fresh extraction of the plain export; scripts outside the tree; node `v24.16.0`,
npm `11.13.0`.

- `npm ci --ignore-scripts --no-audit --no-fund` → **exit 0**, 604 packages installed
  from the committed `package-lock.json`.
- `npm test` (whose `pretest` runs `npm run build`) → **exit 0**:
  - `test:main`: **PASS 6800, FAIL 0, TOTAL 6800** (9738 ms)
  - `test:fp`: **PASS 327, FAIL 0, TOTAL 327** (105 ms)

Hash behaviour under the build:

- `lodash.js` is **unchanged**: `2dc5f1b810c466a98386ea2e4b93f023656244bb4bad76a7f696812cc5a2fc7a`
  before and after the build (equals the manifest entry and the git blob content).
- `test/test.js` unchanged: `80444e68...`.
- `dist/lodash.js` and `dist/lodash.min.js` **are regenerated** by `build:main`: the
  committed `dist/lodash.js` (`308d95db...`, 545268 bytes) becomes identical to
  `lodash.js` (`2dc5f1b8...`, 545279 bytes). Upstream committed a dist file whose
  JSDoc line reads `` `0`, `-0', '0n`, `""`, ... falsey `` while the source `lodash.js`
  reads `` `0`, `""`, ... falsy ``; the build rebuilds dist from the source comment.
  This is an upstream property of the commit, not an export defect — the manifest
  faithfully records the committed bytes. Tests are unaffected.

## 6. Anchor — PASS (strong, with one source caveat)

Advisory `GHSA-r5fr-rjxr-66jc` / `CVE-2026-4800`, "lodash vulnerable to Code Injection
via `_.template` imports key names", CWE-94.

| Source | Affected range | Patched | Severity |
|---|---|---|---|
| CVE.org CNA (OpenJS), PUBLISHED 2026-03-31T19:25:55Z, updated 2026-10-15 | `>=4.0.0, <4.18.1` | 4.18.1 | CVSS 3.1 8.1 `AV:N/AC:H/...` HIGH |
| OSV `GHSA-r5fr-rjxr-66jc` (2026-04-01, modified 2026-10-17) | introduced 4.0.0, fixed 4.18.0; `last_known_affected <= 4.17.23` | 4.18.0 | 8.1 AC:H HIGH |
| GitHub Advisory Database JSON (modified 2026-04-01) | introduced 4.0.0, fixed 4.18.0 | 4.18.0 | 8.1 AC:H HIGH |
| NVD (lastModified 2026-10-15) | CPE `>=4.0.0, <4.18.0` | 4.18.0 | NVD 9.8 `AC:L` CRITICAL; CNA 8.1 `AC:H` |

All four sources include **4.17.23** as affected. They **disagree on the patched
version** (CNA 4.18.1 vs OSV/GitHub-DB/NVD 4.18.0) and NVD disagrees with the CNA on
the CVSS metric (`AC:L` 9.8 vs `AC:H` 8.1). Code inspection settles the patched
version for the `lodash` package: the fix lands in 4.18.0.

Upstream fix:

- `879aaa93132d78c2f8d20c60279da9f8b21576d6` "fix: validate imports keys in
  `_.template`" (2026-03-30, Ulises Gascón). It adds
  `arrayEach(importsKeys, ... reForbiddenIdentifierChars.test(key) ...)` and replaces
  `assignInWith` with `assignWith`.
- **Not** an ancestor of `dec55b7a` (4.17.23). **Is** an ancestor of `4.18.0`
  (`59be2de6...`) and `4.18.1` (`cb0b9b92...`); `git tag --contains` → 4.18.0, 4.18.1.

Vulnerable construct actually present at the tag (not taken on trust):

- `lodash.js:180` defines `reForbiddenIdentifierChars = /[()=,{}\[\]\/\s]/`);
- `lodash.js:14952` applies it only to the `variable` option;
- `lodash.js:14889-14891` builds `importsKeys = keys(imports)` via `assignInWith`
  (enumerates inherited keys);
- `lodash.js:14981` passes those keys straight to `Function(importsKeys, ...)` with
  no validation of key names.

Empirical confirmation (harmless marker, default-parameter expression in a key,
`undefined` value so the default evaluates):

```
_.template('hello', { imports: { 'a = globalThis.__pwned = 1': undefined } })
4.17.23 (plain export): compiles, globalThis.__pwned === 1   <-- code execution at compile time
4.18.0 (patched)      : throws "Invalid `imports` option passed into `_.template`"
```

The same probe against the audit (redacted) `lodash.js` still executes, confirming
the audit redaction did not remove the vulnerability.

Caveat about the advisory text: the OSV/GitHub reference list cites
`3469357cff396a26c363f8c1b5a91dde28ba4b1c`, which is the **2021 fix for the
`variable` option** (CVE-2021-23337) and **is** an ancestor of 4.17.23. It is a stale
reference, not the fix for this CVE; the actual fix is `879aaa931`.

## 7. Release sanity — PASS (one wording correction)

- `4.17.23` is a **plain stable release tag**: no `-npm`, `-amd`, `-es`, `-beta`/`-rc`
  or dist/channel suffix. It is an annotated, PGP-signed tag.
- Commit date **2026-01-21T17:21:04Z** is inside the discovery window ending
  2026-10-21, and predates the advisory (published 2026-03-31) and the fix commit
  (2026-03-30), as a pre-fix target must.
- `package.json` at the tag: `"name": "lodash"`, `"version": "4.17.23"`.
- npm registry: version `4.17.23` published 2026-01-21T17:29:52Z; registry
  `dist-tags` currently has only `latest: 4.18.1`.

On the channel variant: upstream git has a sibling annotated tag `4.17.23-npm`
peeling to `835a537f36ee2fd5fb7f524e213ff9ba2d8698f8` ("Bump lodash npm to v4.17.23",
2026-01-21, 5 minutes after the source tag), with **1054 built files** and no
`test/` or `lib/` sources. The npm-published 4.17.23 tarball's `gitHead` is exactly
`835a537f...`, i.e. the npm artifact is built from that sibling commit. The plain
source tag is the **right choice** for a buildable, testable source snapshot: the
`-npm` tree cannot be built or tested from source. The only thing to keep in mind is
that byte-comparison against the npm tarball is not meaningful — this is a source
snapshot, not a repackaging of the npm artifact.

## 8. Independence — PASS

`reviewed_by = independent-selection-reviewer-lodash-2026-10-23`, which differs from
the selector `claude-code-orchestrator-2026-10-23`.

## Discrepancies with the packet

1. **GitHub advisory patched version.** The packet attributes
   `first_patched_version: 4.18.1` to the GitHub repository advisory "updated
   2026-10-15". The public GitHub Advisory Database JSON
   (`advisories/github-reviewed/2026/04/GHSA-r5fr-rjxr-66jc/...json`, modified
   2026-04-01T23:51:12Z) says `fixed: 4.18.0`. I could not fetch the advisory web
   page or REST endpoint to check for a newer revision (HTTP 403, egress rate limit),
   so the 4.18.1 claim is **unverified**; the version that actually contains the fix
   is 4.18.0 (fix commit ancestry + code). The affected range is unaffected either
   way (4.17.23 is below both bounds).
2. **CNA published timestamp.** The packet lists CVE.org `published_at`
   `2026-03-31T19:03:35Z`; the CVE.org record's `datePublished` is
   `2026-03-31T19:25:55.987Z` (`dateUpdated` 2026-10-15T06:39:20Z). Likely an earlier
   revision timestamp; substantive facts match.
3. **"npm also has a `4.17.23-npm` channel tag"** — slightly misleading wording: that
   is an upstream **git** tag, not an npm dist-tag or a registry version. The npm
   registry for `lodash` has only `latest: 4.18.1` and no `4.17.23-npm` entry. The
   observation that it is a different commit with 1054 built files is correct.
4. **`tag_facts.tag_commit_tree_sha` is `null`** in the packet; the measured tree is
   `994d2c60471db4e562d9409c8ee3066c7e46b6de`, and it matches `export_facts.tree_sha`,
   so `tag_tree_matches_commit: true` is nonetheless correct.
5. **`build_facts.build_attempted: false`** — the packet deliberately did not build;
   in this environment the tree builds and tests cleanly (see §5). Not an error, just
   new evidence.
6. **Advisory reference staleness (upstream, not the packet).** OSV/GitHub cite
   `3469357c...` as the fix; that commit is the 2021 `variable`-option fix and is an
   ancestor of 4.17.23. The real fix is `879aaa931...`.
7. Everything else in the packet that I could remeasure — tag/peel, tree sha, file
   count 159, archive/manifest sha256 and byte size, zero symlinks/gitlinks/.git,
   leakage counts, npm vs git tag distinction, severity disagreement (8.1 AC:H vs
   9.8 AC:L), NVD bound `<4.18.0` — matched.

## Limitations

- Per the claim I did not read `data/**`; therefore the recorded
  `remaining_advisory_id_count` / `excluded_paths` / `redacted_paths` fields were not
  inspected directly. I verified the zero-advisory property by rescanning the
  produced artifact and reproduced the exclusion/redaction set from the documented
  build algorithm.
- GitHub's REST API and the advisory web page were not reachable from this egress IP
  (HTTP 403 rate limit); GitHub-side facts were taken from the public
  `github/advisory-database` raw JSON and the OSV mirror. The packet's claimed
  "updated 2026-10-15" GitHub revision could not be checked.
- The packet does not state the start of the discovery window; I only confirmed the
  tag date precedes the stated 2026-10-21 end.
- This is a selection review only: I did not re-verify unrelated CVEs, the full
  dataset row, or exploitability beyond the harmless compile-time PoC marker.
- The `npm test` build regenerates `dist/lodash.js`/`dist/lodash.min.js`; a downstream
  evaluator should hash `lodash.js` (stable) or record the post-build state rather
  than expect committed `dist/` bytes to survive a build.
