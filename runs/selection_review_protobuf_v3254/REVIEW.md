# Independent selection review — protocolbuffers/protobuf, target v3.25.4

Reviewer: `selrev-independent-protobuf-v3254-2026-10-23` (this review was performed independently of the selecting side; the CLAIM's assertions were re-derived, not trusted).

Snapshot: `snap_442de86eb5fd3f62` — repo `23357588` / `protocolbuffers/protobuf` — tag `v3.25.4`.

**Verdict: accept.** All of checks 1–5 pass, and the public anchor CVE-2024-7254 / GHSA-735f-pc8j-v9w8 really affects this exact version, both statically and at runtime.

---

## 1. Tag identity — pass

Commands (network via `export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`):

```
git ls-remote --tags https://github.com/protocolbuffers/protobuf.git 'refs/tags/v3.25.4*'
git clone --depth 1 --branch v3.25.4 https://github.com/protocolbuffers/protobuf.git repo
git cat-file -p 54932116954e3a46fa8934f66478a3ca54ce730c
git cat-file -p e915ce24b3d43c0fffcbf847354288c07dda1de0
git ls-tree -r HEAD | wc -l
git ls-tree -r HEAD | awk '{print $1}' | sort | uniq -c
git ls-remote --heads origin | grep v3.25
```

Observed:

- `refs/tags/v3.25.4` -> annotated tag object `54932116954e3a46fa8934f66478a3ca54ce730c` -> peeled commit `e915ce24b3d43c0fffcbf847354288c07dda1de0`. Matches the claim and the export record's `tag_resolution.object`.
- Tag object: `type commit`, `tag v3.25.4`, tagger `Protobuf Release <protobuf-team@google.com> 1721841006 +0000` (2024-07-24T17:10:06Z), message `Tag release v3.25.4`; annotated, not lightweight.
- Commit: tree `fafd76c831eb7f547d5d7fbae3aee0dbb32e01fc`, author/committer date 2024-07-24T15:17:14Z, subject `Updating version.json and repo version numbers to: 25.4`. Tree matches the claim.
- `git ls-tree -r`: 2711 entries = 2708 blobs (2620 mode 100644 + 88 mode 100755) + 3 gitlinks (`third_party/abseil-cpp`, `third_party/googletest`, `third_party/jsoncpp`); 0 symlinks (mode 120000).
- `version.json` in the tree declares `protoc_version 25.4`, `java 3.25.4`, `cpp 4.25.4`, date 2024-07-24. No branch named `v3.25.4` exists; this is a stable release tag.
- GitHub REST API was rate-limited (403), so repository id was confirmed from the github.com repository page HTML meta tag: `repository_id" content="23357588"`.

## 2. Export integrity — pass

Commands:

```
sha256sum exports/protocolbuffers__protobuf/snap_442de86eb5fd3f62.{tar.gz,manifest.jsonl}
tar tzf .../snap_442de86eb5fd3f62.tar.gz | wc -l          # 2708
tar tzf ... | grep -E '(^|/)\.git(/|$)'                   # no hits
tar tvzf ... | awk '{print substr($1,1,1)}' | sort | uniq -c   # 2708 x '-'
cmp snap_442de86eb5fd3f62.tar.gz snap_442de86eb5fd3f62.audit.tar.gz
cmp snap_442de86eb5fd3f62.manifest.jsonl snap_442de86eb5fd3f62.audit.manifest.jsonl
python3 -I /tmp/selrev-pb/tools/check_export.py <extracted export> <manifest> <clone>
```

Results:

- Archive sha256 `20e20c1e...451a79` (5787439 bytes) — matches claim and `data/snapshot_exports.jsonl`.
- Manifest sha256 `72dc8096...44fb7e` (532072 bytes) — matches claim and the export record.
- 2708 tar entries, all regular files, 0 directories, 0 symlinks; no `.git` or other VCS metadata.
- Manifest: 2708 lines, all `type: file`, `target: null`.
- Full byte-level cross-check (not just a sample): for every one of the 2708 paths, `git cat-file --batch` content of the commit's blob hashes to the manifest's `sha256` and has the manifest's `size`; every extracted file hashes to the manifest value. 0 mismatches, 0 manifest-only paths, 0 archive-only paths, 0 git blobs missing from the manifest. Gitlinks are correctly absent from manifest and archive.
- Counts: `tree_file_count=2708` (blobs) = `exported_file_count=2708` + `symlink_count=0`; total tree entries 2711 = 2708 blobs + 3 gitlinks. Note: the CLAIM's literal equation `tree_file_count = exported_file_count + symlink_count + gitlink_count` is wrong as written (2708 != 2711) because the exporter excludes gitlinks from `tree_file_count` (confirmed in `v031/scripts/freeze_snapshots.py`, `tree_files = {r for r in tree_rows if r["type"] != "commit"}`). The data itself reconciles exactly; this is a claim wording error, not an integrity defect.

## 3. Positive anchor — pass

Public records fetched (curl via proxy, all HTTP 200):

| Source | How protobuf-java is expressed | 3.25.4 affected? |
|---|---|---|
| OSV `GHSA-735f-pc8j-v9w8` (api.osv.dev) | Maven ECOSYSTEM ranges `[0, 3.25.5)`, `[4.0.0-RC1, 4.27.5)`, `[4.28.0-RC1, 4.28.2)`; `versions[]` includes `3.25.4` | yes |
| GitHub advisory page | Affected `< 3.25.5`, `>= 4.0.0-RC1, < 4.27.5`, `>= 4.28.0-RC1, < 4.28.2`; patched 3.25.5 / 4.27.5 / 4.28.2 | yes |
| OSV `CVE-2024-7254` | GIT range `0 -> fixed 9d0ec0f9...` / `cc8b3483...`; CPE-derived `protobuf-java [0, 3.25.5)` inside `database_specific`; no Maven ECOSYSTEM range | yes |
| CVE CNA record (`cveawg.mitre.org`) | `protobuf-java` `lessThan 3.25.5` (also 4.27.5, 4.28.2), state PUBLISHED, title “Stack overflow in Protocol Buffers Java Lite” | yes |
| NVD (`services.nvd.nist.gov`) | CPE `google:protobuf-java` `versionEndExcluding 3.25.5` (also 4.27.5, 4.28.2); Analyzed; CVSS 7.5 / 8.7 | yes |
| OSV version query | POST query Maven `com.google.protobuf:protobuf-java` = `3.25.4` returns `GHSA-735f-pc8j-v9w8` | yes |

Representational disagreements (none affects 3.25.4): the GHSA/OSV records give explicit 4.x introduced markers while the CNA restarts each 4.x range at version 0; NVD uses only end-excluding CPEs and has one `versionEndIncluding 4.28.2` quirk on the kotlin-lite CPE; OSV's CVE-only record lists only GIT tags in `versions[]`.

Vulnerable code path present in the exported v3.25.4 tree:

- `CodedInputStream.java` — the four decoder `skipMessage()` implementations loop `skipField(tag)` with no `checkRecursionLimit()`/`recursionDepth`; `skipField(START_GROUP)` calls `skipMessage()`, so nested unknown groups recurse without bound.
- `UnknownFieldSchema.java` — `mergeOneFieldFrom(...)` for `WIRETYPE_START_GROUP` calls `mergeFrom(subFields, reader)` recursively with no depth parameter.
- `ArrayDecoders.java` — `skipField(...)` for `WIRETYPE_START_GROUP` recurses into `skipField(...)` with no depth guard.

Guard present in later release: diffing v3.25.5 (tag peeled commit `9d0ec0f92b5b5fdeeda11f9dcecc1872ff378014`, itself listed as an OSV fixed commit) against v3.25.4 shows `checkRecursionLimit()`/`++recursionDepth` added to `skipMessage`, `DEFAULT_RECURSION_LIMIT = 100` plus depth tracking added to `UnknownFieldSchema` and `ArrayDecoders`, and `InvalidProtocolBufferException.recursionLimitExceeded` used.

Runtime confirmation (using the tree built in check 4, plus the official 3.25.5 jar from Maven Central):

- lite-generated message parsing 100,000 nested unknown START_GROUP tags on protobuf-java **3.25.4** -> `java.lang.StackOverflowError`.
- same input on protobuf-java **3.25.5** -> `InvalidProtocolBufferException: Protocol message had too many levels of nesting... Use setRecursionLimit()`.

## 4. Build feasibility — pass

Prepared a copy of the extracted tree at `/tmp/selrev-pb/build`, placed an official protoc 25.4 binary at the repo root (its sha256 `22a39a40...6ba5da` is byte-identical to the official `protoc-25.4-linux-x86_64.zip` release I downloaded and to `/tmp/pbrev/protoc-25.4/bin/protoc`).

Exact build command (fresh empty local Maven repository, proxy passed through `MAVEN_OPTS`):

```
export JAVA_HOME=/home/luchitong/.local/toolchain/jdk-17.0.20.1+1
export PATH="$JAVA_HOME/bin:$PATH"
export MAVEN_OPTS="-Dhttps.proxyHost=172.21.96.1 -Dhttps.proxyPort=7890 -Dhttp.proxyHost=172.21.96.1 -Dhttp.proxyPort=7890 -Xmx1g"
cd /tmp/selrev-pb/build/java
~/.local/toolchain/apache-maven-3.9.16/bin/mvn -B -Dmaven.repo.local=/tmp/selrev-pb/m2 install -Dmaven.test.skip=true
```

Result: **exit code 0, BUILD SUCCESS, 7/7 modules SUCCESS** (BOM, Parent, Lite, Core, Util, Kotlin-Core, Kotlin-Lite), total time 01:30 min, 0 `[ERROR]` lines. Toolchain: OpenJDK 17.0.20.1 (Temurin), Apache Maven 3.9.16, protoc 25.4. Ant-run invoked `Running protoc ...` for source generation; `protobuf-java-3.25.4.jar` (1,831,626 bytes) was installed and contains `CodedInputStream.class` / `UnknownFieldSchema.class` compiled from this tree.

`data/snapshot_exports.jsonl` still says `build_attempted=false` and `java_maven={java:false,mvn:false}` (PATH probe); that metadata is stale, the build is genuinely feasible with the explicit toolchain paths.

## 5. Audit/leakage export — pass

- `data/snapshot_exports.jsonl` for this snapshot: `status=exported`, commit/tree as above, `missing_from_archive_count=0`, `symlink_count=0`, `gitlink_count=3`.
- `data/snapshot_audit_exports.jsonl`: `status=exported`, `remaining_advisory_id_count=0`, `remaining_advisory_id_paths=[]`, `redacted_count=0`, `excluded_count=0`, `source_export_id=exp_snap_442de86eb5fd3f62`, `source_archive_sha256` equals the source archive sha. The audit archive and manifest are byte-identical to the source archive and manifest (`cmp` clean), i.e. the audit tree is the same 2708 files.
- Independent scan of the extracted tree: **0** CVE ids, **0** GHSA ids, no advisory URLs (only generic securityscorecards / Google security-intake / awakesecurity links), no `.patch`/`.diff` files, no `.git`/`.hg`/`.svn`/CVS metadata, no snapshot id or benchmark/selection labels. The only matches for “vulnerab” are generic prose in `SECURITY.md`, an `ExtensionRegistry.java` comment, and `.github/workflows/test_runner.yml`.

## 6. Release sanity

- Tag date 2024-07-24; dataset window opens 2022-10-23; review date 2026-10-23 — the tag is inside the window and predates the advisory publication (2024-09-19), so no advisory leakage is expected, and none was found.
- Newer stable affected tags do exist elsewhere in the version series (v27.0–v27.4 = C++ 4.27.x affected, fixed by v27.5 = 4.27.5; v28.0–v28.1 affected, fixed by v28.2 = 4.28.2). v3.25.4 is the newest affected tag in the 3.25.x line. This does not invalidate the proposal: the target is a frozen snapshot with a verified positive at this exact commit.

## 7. Verdict

`accept`: checks 1–5 all hold, and at least one public anchor (CVE-2024-7254 / GHSA-735f-pc8j-v9w8) really affects this exact version, confirmed by five public sources, by the code present in the tree, by the v3.25.5 fix diff, and by runtime reproduction.

## Discrepancies / limitations

See `verdict.json` → `discrepancies` and `limitations`. The material ones: the CLAIM's count equation double-counts gitlinks (data still reconciles exactly); the export record's build probe is stale; and GitHub's REST API rate limit prevented API-based repo/release metadata checks (repository id confirmed from page HTML, tag from git).

Isolation disclosure: while locating the exporter's definition of `tree_file_count`, one broad grep also matched a few lines of `v031/reviews/selection_packets/*.json` and `v031/reviews/SELECTION_REVIEW_2026-10-22.md` before those forbidden paths were recognized. The exposed text was limited to per-repository `tree_file_count`/gitlink numbers and one generic count-check sentence; it said nothing about this snapshot's verification, and no finding relies on it — every count here was recomputed independently from the export artifacts and the public git tree. No other forbidden path was read.
