# Independent selection review — protocolbuffers/protobuf v28.1

- Snapshot: `snap_de01ecf37efd6cd5`
- Repo: `23357588` / `protocolbuffers/protobuf`
- Proposed target: tag `v28.1`, commit `10ef3f77683f77fb3c059bf47725c27b3ff41e63`
- Reviewer: `independent-selection-reviewer-protobuf-v28.1-r1`
- Review date: 2026-10-23 (local, UTC+8); clock at review: 2026-10-22T18:06:31Z
- Verdict: **accept** (checks 1-5 pass, release sanity clean); **build_ok = false**

All work used only the allowed inputs: the packet, the `snap_de01ecf37efd6cd5` rows of
`data/snapshot_exports.jsonl` and `data/snapshot_audit_exports.jsonl`, the export files under
`exports/protocolbuffers__protobuf/`, and public upstream sources. Scratch work is under
`/tmp/selrev_pb`; the archive was extracted into a fresh empty directory
`/tmp/selrev_pb/extract` and nothing from it was executed except the CMake/Maven build
commands.

Proxy used for all network access:
`export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`

## 1. Tag resolution — PASS

Commands:

```
git ls-remote --tags https://github.com/protocolbuffers/protobuf.git 'refs/tags/v28*'
git clone --bare --filter=blob:none https://github.com/protocolbuffers/protobuf.git upstream.git
git -C upstream.git cat-file -t refs/tags/v28.1        # -> tag  (annotated)
git -C upstream.git cat-file -p refs/tags/v28.1
git -C upstream.git rev-list -n1 refs/tags/v28.1       # -> 10ef3f77...
git -C upstream.git cat-file -p 10ef3f77...
git -C upstream.git rev-parse 10ef3f77^{tree}
```

`ls-remote` returned:

```
00fd90a1baee0d38e963bdb0c3dd78401298d1cf  refs/tags/v28.1
10ef3f77683f77fb3c059bf47725c27b3ff41e63  refs/tags/v28.1^{}
```

The tag is annotated (tag object `00fd90a1baee0d38e963bdb0c3dd78401298d1cf`), peeling to
`10ef3f77683f77fb3c059bf47725c27b3ff41e63`, exactly the packet `commit_sha`.

- Commit date: `2024-09-10T13:36:10-07:00` (= `2024-09-10T20:36:10Z`)
- Subject: `Updating version.json and repo version numbers to: 28.1`
- Tagger: `Protobuf Team Bot <protobuf-team-bot@google.com> 1726000570 -0700`
- Tree: `f105fc72bff2143fe6db0b2be5ec86a385f858f0` (matches packet `tree_sha`)
- Tag name is exactly `v28.1`: not an rc/dev/dist tag. The repo also has `v28-dev` and
  `v28.0-rc1..3`, none of which is the target.

Maven version declared by the tree: `java/pom.xml` `<version>4.28.1</version>`;
`version.json` `"java": "4.28.1"`, `"protoc_version": "28.1"`.

## 2. Export integrity — PASS (with careful gitlink accounting)

```
sha256sum exports/protocolbuffers__protobuf/snap_de01ecf37efd6cd5.tar.gz
sha256sum exports/protocolbuffers__protobuf/snap_de01ecf37efd6cd5.manifest.jsonl
```

- archive: `214f9f5e8ad3d840cab3f4f8818fc59657dd750bade3268ce7f412c699647c4e` (9,066,843 bytes) — matches packet
- manifest: `2ebd6ab324905a44a60cc5203d2fa718ccb1b29ead61b864d97a771c44c2d347` (576,522 bytes) — matches packet

`tar -tzf ... | grep -E '(^|/)\.git/' | wc -l` -> `0`; no `.git` directory. The only
`.git*` names are tracked files (`.github/`, `.gitignore`, `.gitmodules`, per-directory
`*.gitignore`).

Archive entry shape:

```
tar -tzf ... | wc -l            -> 2941
tar -tzf ... | grep -c '/$'     -> 0        (no directory entries)
tar -tvzf ... | cut -c1 | sort | uniq -c    -> 2941 '-'   (all regular files; 0 symlinks)
```

`git ls-tree -r 10ef3f77`:

```
2856  100644
  85  100755
   3  160000   (third_party/abseil-cpp, third_party/googletest, third_party/jsoncpp)
2944  total
```

Count reconciliation (the point the brief warned about):

- `tree_file_count = 2941` counts **blobs only** (2856 + 85), not the 3 gitlinks.
- `exported_file_count = 2941` = number of regular files in the tar.
- `symlink_count = 0`.
- `gitlink_count = 3`, reported separately; the archive **skips** them entirely — the three
  paths do not exist even as empty entries under the extracted tree.
- Therefore `exported_file_count + symlink_count = tree_file_count` (2941 + 0 = 2941), but
  the naive `exported + symlink + gitlink = tree_file_count` identity does **not** hold
  (2944 != 2941). `missing_from_archive_count = 0` is correct once gitlinks are excluded
  from the comparison.
- Sum of manifest sizes = 88,953,952 = packet `total_bytes`; manifest line count = 2941.

## 3. Manifest vs tree — PASS (verified in full, not just a sample)

Path set comparison and full per-file verification against `git ls-tree -r` at
`10ef3f77` (script `/tmp/selrev_pb/verify.py`, run with `python3 -I`):

- manifest paths vs tree blob paths: 0 missing each way (2941 = 2941)
- extracted files vs manifest: 0 missing each way
- per file: recomputed sha256, size, mode (`100644`->`0644`, `100755`->`0755`) and the
  git blob object id (`sha1("blob <size>\0" + content)`): **0 mismatches of each kind**
- manifest entry types: all `file`; 0 null sha256; 0 mode `120000`.

So the manifest is a faithful, complete description of the exported commit.

## 4. Leakage / audit export — PASS

Row for `snap_de01ecf37efd6cd5` in `data/snapshot_audit_exports.jsonl`:

- `remaining_advisory_id_count = 0`, `remaining_advisory_id_paths = []`
- `excluded_count = 0`, `excluded_paths = []`
- `redacted_count = 0`, `redacted_paths = []`
- audit archive sha `214f9f...` = export archive sha; audit manifest sha `2ebd6a...` =
  export manifest sha; the two manifest files are byte-identical (`cmp` -> SAME).

Independent corroboration: a whole-tree grep over the extracted archive for
`CVE-[0-9]{4}-[0-9]{4,}` and `GHSA-xxxx-xxxx-xxxx` returned no hits.

## 5. Anchor — PASS: CVE-2024-7254 (GHSA-735f-pc8j-v9w8) really affects v28.1

The snapshot declares Java **4.28.1** (and Ruby gem 4.28.1). Sources, as each expresses it:

| Source | Affected expression | Patched |
|---|---|---|
| OSV/GHSA-735f-pc8j-v9w8 | Maven `protobuf-java`, `-javalite`, `-kotlin`, `-kotlin-lite`: `[0,3.25.5)`, `[4.0.0-RC1,4.27.5)`, `[4.28.0-RC1,4.28.2)`; RubyGems `google-protobuf` same three; `4.28.1` listed explicitly in the 4.28 range | 3.25.5, 4.27.5, 4.28.2 |
| CVE CNA record (cveawg.mitre.org, assigner Google) | each Maven package/gem: `version 0, lessThan {3.25.5, 4.27.5, 4.28.2}`; plus Google "Protocol Buffers" `0 .. <28.2`; `defaultStatus unaffected` | 3.25.5, 4.27.5, 4.28.2 |
| NVD API 2.0 (status Analyzed) | CPE: `(<3.25.5)`, `[4.0.0,<4.27.5)`, `[4.28.0,<4.28.2)` for protobuf / -java / -javalite / -kotlin; **protobuf-kotlin-lite uses `versionEndIncluding 4.28.2`**; ruby CPE same three | 3.25.5, 4.27.5, 4.28.2 |
| GHSA page HTML | package cards: "Affected versions <4.28.2; Patched versions 3.25.5, 4.27.5, 4.28.2" | 3.25.5, 4.27.5, 4.28.2 |
| OSV CVE-2024-7254 record | single GIT range: introduced `0`, fixed `9d0ec0f9...`, fixed `cc8b3483...`; extracted events carry CPE fixed 3.25.5 and REFERENCES_COMMIT `cc8b3483` | n/a (no 4.27.5/4.28.2 boundary encoded) |

v28.1 (4.28.1) is inside **every** source's affected set. I also confirmed the code state
rather than trusting the ranges: in the exported v28.1 tree,
`java/core/src/main/java/com/google/protobuf/ArrayDecoders.java` has no recursion-depth
tracking and `UnknownFieldSchema.java` is the pre-fix 3-line form; the v28.2 blob adds
`registers.recursionDepth` / `checkRecursionLimit` in `ArrayDecoders.java` and
`CodedInputStream.java`.

Fix-commit ancestry (`git merge-base --is-ancestor <commit> <target>`):

- `ac9fb5b4` "Add recursion check when parsing unknown fields in Java."
  (2024-09-18, on branch `28.x`): **not** an ancestor of v28.1 (exit 1), **is** an ancestor
  of v28.2 (exit 0); v28.0 also lacks it.
- `9a5f5fe7` (internal, 28.x): ancestor of v28.2, not of v28.1.
- `d6c82fc5` (public PR #18388): on `27.x` (tag v27.5), not an ancestor of v28.1 or v28.2.
- `cc8b3483` (the patch commit cited by CNA/NVD/OSV): on `29.x`/main (tags v29.0+), not an
  ancestor of v28.1 or v28.2.
- `4728531c`, `850fcce9` (3.25.x) and `9d0ec0f9` (v25.5 version bump): not ancestors of
  either v28 tag.

**v28.2 is the first fixed release on the 28.x line**: 28.x tags are v28.0, v28.1, v28.2,
v28.3 (plus rc/dev); v28.2 declares Java 4.28.2 and contains the fix; no v28.1.x patch tag
exists.

### Source disagreements (recorded, not flattened)

1. **Lower bound of the 4.28 range differs**: GHSA/OSV `introduced 4.28.0-RC1`; CNA
   open-ended `version 0, lessThan 4.28.2`; NVD `versionStartIncluding 4.28.0`. All still
   include 4.28.1.
2. **NVD kotlin-lite inclusive upper bound**: `protobuf-kotlin-lite` 4.28 CPE has
   `versionEndIncluding 4.28.2`, which would include the fixed release — inconsistent with
   every other NVD product/range and with OSV/GHSA/CNA. Likely an NVD curation error.
3. **OSV CVE GIT range is malformed-ish**: one range with two `fixed` events and no
   release boundaries for 4.27.5/4.28.2 (only in `database_specific` CPE events).
4. **Cited patch commit is not on the 28.x line**: CNA/NVD/OSV cite `cc8b3483`, which is on
   29.x/main and is not an ancestor of v28.2; the public PR commit `d6c82fc5` is on 27.x.
   The 28.x release was fixed by the separate internal cherry-pick `ac9fb5b4`.
5. **Weakness classification**: CNA CWE-400/CWE-674; NVD primary CWE-787 (secondary
   Google CWE-400/CWE-674).
6. **CNA typo**: product name `protobuf-kotllin-lite`.
7. **Severity**: CVSS 4.0 8.7 HIGH (CNA, NVD secondary, GHSA display) vs CVSS 3.1 7.5 HIGH
   (NVD primary, GHSA). Same level, version difference.

## 6. Build feasibility — FAIL (honest: build_ok = false)

Toolchains present and used: JDK `17.0.20.1+1`, Maven `3.9.16`, CMake `3.28.3`, gcc/g++,
go `1.27.3`. Two real attempts:

**Maven (Java):**

```
export JAVA_HOME=/home/luchitong/.local/toolchain/jdk-17.0.20.1+1
PATH=$JAVA_HOME/bin:/home/luchitong/.local/toolchain/apache-maven-3.9.16/bin:$PATH
mvn -B -f extract/java/pom.xml -Dmaven.repo.local=/tmp/selrev_pb/m2 validate
# exit 1
```

```
[ERROR] Child module .../java/lite/pom.xml ... does not exist
[ERROR] Child module .../java/core/pom.xml ... does not exist
[ERROR] Child module .../java/util/pom.xml ... does not exist
[ERROR] Child module .../java/kotlin-lite/pom.xml ... does not exist
```

The tree ships `pom_template.xml` for `lite`, `core`, `util`, `kotlin`, `kotlin-lite`
(only `java/pom.xml`, `java/bom/pom.xml`, `java/kotlin/pom.xml`, `java/protoc/pom.xml` are
real poms), so the parent reactor cannot even be read. Even with repaired poms,
`java/core/src/main/java` has no generated `DescriptorProtos.java`, `java/lite` has no main
sources, and no `protoc` binary exists anywhere in the tree — the README requires a `protoc`
placed next to the build. So the Java path additionally needs an external protoc + code
generation.

**CMake (C++):**

```
cmake -S /tmp/selrev_pb/extract -B /tmp/selrev_pb/build-cmake \
      -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_BUILD_CONFORMANCE=OFF
# exit 1
```

```
CMake Warning at cmake/abseil-cpp.cmake:28: protobuf_ABSL_PROVIDER is "module" but ABSL_ROOT_DIR is wrong
CMake Error at third_party/utf8_range/CMakeLists.txt:29 (add_subdirectory):
  add_subdirectory given source ".../third_party/abseil-cpp" which is not an existing directory.
```

The three gitlink submodules (`abseil-cpp`, `googletest`, `jsoncpp`) are declared in
`.gitmodules` but their contents are not exported, so configure cannot proceed.

No successful build was achieved and none is claimed. Because the export additionally
omits generated sources and protoc, this is a structural property of the export, not a
missing-toolchain problem. `build_ok = false`.

## 7. Release sanity — PASS

- Release date: 2024-09-10 (tag/commit timestamp `2024-09-10T20:36:10Z`; `version.json` date 2024-09-10).
- Age at 2026-10-23: **772 days** (~2.1 years).
- Dataset window opens 2022-10-23: the release is **after** the window opening, so not
  excluded on age. Not a pre-release/dist tag, not clearly obsolete (v28.1 is the
  affected-version selection; v28.2/v28.3 are the fixed/newer releases).

## 8. Verdict

Checks 1-5 pass and release sanity is clean, so under the instruction's explicit gate
("accept only if checks 1-5 pass and no release-sanity problem exists") the verdict is
**accept**.

The material caveat is the build: the snapshot cannot be built as exported (`build_ok =
false`) because the export omits the gitlink submodule contents, ships Maven
`pom_template.xml` instead of module poms, and contains neither `protoc` nor generated
Java sources. This is recorded as a limitation. The instruction's accept rule names only
checks 1-5 plus release sanity, so this does not by itself flip the verdict; a downstream
pipeline that requires an as-exported build should treat `build_ok=false` as blocking.
