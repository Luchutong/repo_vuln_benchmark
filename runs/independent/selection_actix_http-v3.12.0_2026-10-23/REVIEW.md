# Independent selection review — actix/actix-web @ http-v3.12.0

- review_id: `selrev_105379569_snap_ca4042bda2431632`
- snapshot_id: `snap_ca4042bda2431632`
- repo_id: 105379569
- reviewer: `deepseek-flash-independent-selection-reviewer-2026-10-23-02`
- reviewed_at: 2026-10-23T00:31:11Z
- **verdict: accept**

## 1. Tag resolution (executed)

```
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
git ls-remote --tags https://github.com/actix/actix-web.git
```

Result (554 refs, 9 peeled `^{}` refs total, none for this tag):

```
a7a26f1ee0adfeabb5ee85a6eb2a62cff601a70b  refs/tags/http-v3.12.0
0fb89457eda4a78a4cb7ccb3fdebe49a143ce2d5  refs/tags/http-v3.12.1
```

Then, in a fresh repo:

```
git init; git remote add origin https://github.com/actix/actix-web.git
git fetch --depth=1 origin refs/tags/http-v3.12.0:refs/tags/http-v3.12.0
git cat-file -t http-v3.12.0            -> commit
git rev-parse http-v3.12.0^{commit}     -> a7a26f1ee0adfeabb5ee85a6eb2a62cff601a70b
git rev-parse http-v3.12.0^{tree}       -> 329cd0a915a1b4bdb06db1ca981f85205b65fe20
git log -1 --format=%cI http-v3.12.0    -> 2026-02-18T19:10:18+09:00
```

- Object type: **commit**; tag is **lightweight** (no tag object, no `^{}` dereference line).
- Commit UTC: **2026-02-18T10:10:18Z**.
- Subject: `chore(http): release v3.12.0 (#3939)`.
- Stable release, not a dist/moving tag: `http-v3.12.0` is one of the sequential `http-v3.x.y` release tags (v3.10.0, v3.11.0–2, v3.12.0, v3.12.1, v3.13.x, …). crates.io `actix-http` 3.12.0 was published 2026-02-18T10:10:56Z (38 s after the commit timestamp), i.e. the tag and the crates.io release are the same event. `matches = true`.

## 2. Export integrity (executed)

```
sha256sum snap_ca4042bda2431632.tar.gz          aad2fee23b8531ba8bcc7eef312e7bbd98e0fae6d9388ad2158cfbbc1baad9b3
sha256sum snap_ca4042bda2431632.manifest.jsonl  aff848294117d771ed787ba1024dfd3141d984ee1ce4385fe0ac7b077130b508
stat -c %s                                      615451 bytes (archive), 81517 bytes (manifest)
wc -l manifest                                  442
```

Both match the packet (`archive_sha256`, `manifest_sha256`, `archive_bytes` 615451).

Archive extracted into fresh `/tmp/selrev_actix/snap`:

- tar contains 442 entries; on disk: 418 regular files, 24 symlinks, 71 directories.
- `tree_file_count 442 = exported_file_count 418 + symlink_count 24 + gitlink_count 0 + absent 0`. 0 gitlinks confirmed by `git ls-tree -r` (all 442 entries are blobs; 418 mode 100644/100755, 24 mode 120000).
- No `.git` directory/entries anywhere (`tar -tzf | grep -E '(^|/)\.git(/|$)'` -> none; `find . -name .git` -> none). `.gitignore` and `.github/` are ordinary tracked files.
- Manifest verification (script `/tmp/selrev_actix/scripts/verify_manifest.py`, run with `python3 -I`): 442/442 unique paths present, 0 missing, 0 sha256/size/mode mismatches, 0 type mismatches, 0 extra files on disk.
- Upstream fidelity cross-check (`git_blob_crosscheck.py`): for all 442 paths, `git cat-file blob` of the tag tree sha256 equals the manifest sha256; symlink targets equal the 120000 blob contents; no extra git entries. Export is exactly the tracked tree of commit a7a26f1.
- Symlinks are all benign relative links (LICENSE links `../LICENSE-*`, `README.md -> actix-web/README.md`, `actix-files/tests/symlink-test.png -> test.png`); none escapes the tree.

## 3. Audit export (P6) (executed)

Extracted `snap_ca4042bda2431632.audit.tar.gz` into fresh `/tmp/selrev_actix/audit`:

- Audit archive sha256 is **identical** to the evaluation archive (`aad2fee2…`), 615451 bytes, 442 entries; audit manifest sha256 identical (`aff84829…`), so source basis matches this export and the audit copy represents the same tracked tree. `diff -rq snap audit` -> identical.
- No `.git` metadata; no advisory-named paths.
- Scanned every file in the extracted audit tree for `CVE-`, `GHSA-`, `RUSTSEC-`, `GO-NNNN-NNN`, `EEF-`, and exact `CVE-2026-73051` / `GHSA-xhj4-vrgc-hr34`:
  - **Target advisory IDs: 0 hits.** Neither `CVE-2026-73051` nor `GHSA-xhj4-vrgc-hr34` appears anywhere (grep exit 1).
  - Unrelated historical identifiers found (pre-existing upstream content, not the evaluated advisory): `RUSTSEC-2020-0071` (cookie, in actix-web/awc CHANGES), `RUSTSEC-2021-0081` (HTTP request smuggling, actix-http CHANGES), and `deny.toml` dependency-ignore list `RUSTSEC-2024-0336`, `RUSTSEC-2025-0009`, `RUSTSEC-2025-0010`.
  - The packet's `leakage_facts.assessment` ("no_advisory_identifiers_detected_in_scanned_files") is therefore **worded too strongly** — identifiers do exist — but none of them discloses the evaluated advisory, so the anti-leak goal holds.

## 4. Build feasibility (executed)

Toolchain: `cargo 1.98.1 (797e8a9bc 2026-08-05)`, `rustc 1.98.1 (48a229cea 2026-09-01)`.
Workspace `rust-version = "1.88"`, so toolchain is compatible.

```
cargo metadata --no-deps --format-version 1    exit 0; 11 packages; actix-http 3.12.0; actix-web 4.12.1
cargo check -p actix-http                      exit 0
```

Build log tail: `Checking actix-http v3.12.0 (/tmp/selrev_actix/snap/actix-http)` … `Finished dev profile [unoptimized] target(s) in 10.34s`. Dependencies fetched through the proxy. `build_ok = true`.

Workspace sanity: Cargo.lock present, no vendored directory, largest tracked file 96,055 bytes (uncompressed tree 3.04 MB), `LICENSE-APACHE` + `LICENSE-MIT` present, `actix-http/Cargo.toml` `version = "3.12.0"`, license `MIT OR Apache-2.0`.

## 5. Anchors (executed)

Live sources queried 2026-10-23 through the proxy:

- OSV `GHSA-xhj4-vrgc-hr34`: package `actix-http` (crates.io), range `introduced 0 / fixed 3.12.1`, published 2026-04-22.
- GitHub advisory DB record: severity MODERATE, same ECOSYSTEM range `0 – 3.12.1`.
- OSV `CVE-2026-73051`: **GIT range `introduced 0 / fixed a7a26f1ee0adfeabb5ee85a6eb2a62cff601a70b`** (the 3.12.0 release commit), and its version list omits all `http-v3.12.x` tags.
- CVE.org CNA record (VulnCheck, PUBLISHED 2026-08-14, updated 2026-10-21): affected `{version 0, lessThan 3.12.0}` plus explicit `{version 3.12.0, status unaffected}`.
- NVD API record: `Awaiting Analysis`, description "actix-http versions before 3.12.1".
- crates.io: 3.12.0 published 2026-02-18T10:10:56Z; **3.12.1 published 2026-04-18T02:42:16Z**.
- Repository evidence: `git diff http-v3.12.0 http-v3.12.1 -- actix-http` shows `src/h1/decoder.rs` gaining exactly the missing guard:

  ```
  if msg.head().headers.contains_key(header::TRANSFER_ENCODING) {
      ... if !chunked => Err(ParseError::Header);
      if ... CONTENT_LENGTH ... => "both Content-Length and Transfer-Encoding are set" => Err
  }
  ```

  and new tests `hrs_cl_and_chunked_te_http11` / `hrs_identity_te_http11`. `actix-http/CHANGES.md` at 3.12.1 says: "**SECURITY:** Reject HTTP/1 requests with ambiguous request framing from `Content-Length` and `Transfer-Encoding` headers to prevent request smuggling." The 3.12.1 release commit is `0fb89457…` (2026-04-18), four days before the GHSA publication (2026-04-22).

In the snapshot tree itself the guard is **absent** (`grep "both Content-Length and Transfer-Encoding are set" actix-http/src` -> no match), and only the old permissive test `hrs_cl_and_te_http10` exists.

**Contradiction resolution:** GHSA/OSV and the actual code are right — actix-http **3.12.0 is affected**, fixed in **3.12.1**. The CVE.org CNA `affected` field (which says 3.12.0 is unaffected and fixed at 3.12.0) is erroneous; the OSV CVE record's GIT `fixed: a7a26f1` event is a mechanical conversion of that bad CNA range onto the `http-v3.12.0` tag and is likewise wrong. The CVE title/description ("before 3.12.1") contradicts the CVE.org affected field itself. Anchor counts: affected = true.

Anchor URLs (all returned HTTP 200 unless noted):
- https://github.com/advisories/GHSA-xhj4-vrgc-hr34
- https://github.com/actix/actix-web/security/advisories/GHSA-xhj4-vrgc-hr34
- https://api.osv.dev/v1/vulns/GHSA-xhj4-vrgc-hr34
- https://api.osv.dev/v1/vulns/CVE-2026-73051
- https://crates.io/api/v1/crates/actix-http
- https://github.com/actix/actix-web/releases/tag/http-v3.12.1
- https://www.vulncheck.com/advisories/actix-http-before-http-request-smuggling-via-cl-te
- https://nvd.nist.gov/vuln/detail/CVE-2026-73051 (HTML page 403 bot-block; NVD **API** `services.nvd.nist.gov/rest/json/cves/2.0` returned 200 and was used instead)

## 6. Selection sanity

The snapshot is the complete tracked tree (442 paths) of tag `http-v3.12.0`, which contains `actix-http/Cargo.toml` at version 3.12.0 — the vulnerable package — inside the actix-web monorepo workspace. Not a dist tag, not a pre-release. Workspace resolves and compiles. No vendored content (max file 96 KB), licenses present, no gitlinks/submodules. Nothing found that makes the target unsuitable.

## Residual risks / notes

1. The release tag is lightweight; a lightweight tag could in principle be repointed upstream. Current sha matches crates.io publish time and the packet; residual risk is normal for GitHub release tags.
2. **Advisory-range contradiction** (documented above): any downstream consumer that trusts the CVE.org CNA `affected` field instead of GHSA/OSV will believe 3.12.0 is unaffected. The code diff and changelog unambiguously show 3.12.0 vulnerable.
3. Packet leakage wording overstates cleanliness: unrelated RUSTSEC IDs exist in `deny.toml` and CHANGES files; the evaluated advisory is not leaked.
4. GitHub REST API returned 403 (shared-IP rate limit); error bodies saved to `/tmp/selrev_actix/scripts/gh_ref.json` / `gh_tagobj.json` and not used as evidence. Tag facts were derived from `git ls-remote` + `git fetch`, anchors from OSV/NVD APIs, crates.io and the repository itself.
5. Build was run in the extracted `/tmp` tree (`target/` created there only); archive contents were not modified.

## Files/commands used

- Packet: `/home/luchitong/work/repo-vuln-50-v031/v031/reviews/selection_packets/105379569_actix__actix-web.json`
- Exports: `/home/luchitong/work/repo-vuln-50-v031/exports/actix__actix-web/`
- Work dirs (fresh): `/tmp/selrev_actix/{snap,audit,repo,scripts}`
- Scripts (own, outside extracted trees): `/tmp/selrev_actix/scripts/verify_manifest.py`, `git_blob_crosscheck.py`
- No forbidden path was read.
