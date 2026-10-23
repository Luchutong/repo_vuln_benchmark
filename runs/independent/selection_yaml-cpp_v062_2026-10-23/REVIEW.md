# Independent selection review — jbeder/yaml-cpp @ yaml-cpp-0.6.2

- Review id: `selrev_33100064_snap_f0ec66ad5ca54002`
- Snapshot: `snap_f0ec66ad5ca54002`
- Tag: `yaml-cpp-0.6.2`
- Commit: `562aefc114938e388457e6a531ed7b54d9dc1b62`
- Reviewer: `independent-selection-reviewer-yamlcpp-2026-10-23` (distinct from `claude-code-orchestrator-2026-10-23`)
- Verdict: **accept**

Everything below was re-derived from public sources, a fresh clone of
`https://github.com/jbeder/yaml-cpp`, and my own build. Working directory was
`/tmp/selrev_yamlcpp` (fresh); scripts were kept in `work/`, outside every extracted tree,
and all Python that read extracted files was run with `python3 -I`.

## 1. Tag resolution

Command (through the 7890 proxy):

```
git ls-remote --tags https://github.com/jbeder/yaml-cpp
```

Output for the tag (no peeled `^{}` companion line was emitted for any tag):

```
562aefc114938e388457e6a531ed7b54d9dc1b62	refs/tags/yaml-cpp-0.6.2
9a3624205e8774953ef18f57067b3426c1c5ada6	refs/tags/yaml-cpp-0.6.3
0579ae3d976091d7d664aa9d2527e0d0cff25763	refs/tags/yaml-cpp-0.7.0
```

In a full clone:

```
git cat-file -t 562aefc1...            -> commit
git for-each-ref --format='%(objecttype)' refs/tags/yaml-cpp-0.6.2 -> commit
git log -1 --format='%H %T %ci %s'
  -> 562aefc114938e388457e6a531ed7b54d9dc1b62 296d72b846796a97e4e5f08e8ef64553d1e51756
     2018-03-05 22:56:23 -0600 Bump CMake version to 0.6.2.
```

The tag is **lightweight** (points directly at a commit, no tag object), resolves to
`562aefc1...`, and its tree `296d72b8...` equals the packet's `export_facts.tree_sha`.
Commit date in UTC: `2018-03-06T04:56:23Z`.

## 2. Archive integrity and manifest

Measured with `sha256sum` / `stat` on the exports (not copied, not modified):

| artifact | measured | packet | match |
|---|---|---|---|
| `snap_f0ec66ad5ca54002.tar.gz` sha256 | `84f3ff489b1e02a4b626435686d74bb42e001c12aa3d8e09e07a7d654f778c03` | same | yes |
| `snap_f0ec66ad5ca54002.tar.gz` bytes | 1,383,022 | 1,383,022 | yes |
| `snap_f0ec66ad5ca54002.manifest.jsonl` sha256 | `55c94d1ba5deb4babd3943ca9a515c40baf0cb2fe962780afc6e2e39be527b9b` | same | yes |

Extraction into a fresh empty directory `ext_plain/`:

- tar members: 446, all of type `REGTYPE` (regular file) → 446 files, **0 symlinks, 0
  gitlinks**, 0 directories stored in the tar, **0 `.git` entries**.
- on-disk walk: 446 regular files, 0 symlinks, 57 directories.
- `git ls-tree -r -z 562aefc1` (parsed with Python from the `-z` stream): 446 entries, all
  `blob`.
- manifest entries: 446, unique paths: 446, path set equal to the `-z` ls-tree set
  (`equal True`), and equal to the tar member set.
- per-file checks (Python, `python3 -I`): recomputed sha256 = manifest sha256 for 446/446;
  recomputed git blob sha1 (`sha1("blob <len>\0" + content)`) = ls-tree sha1 for 446/446;
  byte size 446/446; mode (`100644`/`100755`) 446/446.
- counts reconcile: 446 tracked = 446 exported + 0 symlinks + 0 gitlinks + 0 missing.

## 3. Audit export

- `snap_f0ec66ad5ca54002.audit.tar.gz` sha256 = `84f3ff48...`, bytes = 1,383,022.
- `snap_f0ec66ad5ca54002.audit.manifest.jsonl` sha256 = `55c94d1b...`.
- Both hashes and both file sizes are **identical to the plain export**; `cmp` on the two
  manifests and `diff -rq` on the two extracted trees report no differences.
- Extracted audit tree: 446 regular files, 0 symlinks, no `.git` directory, no `*.patch` /
  `*.diff`, no advisory, benchmark or label files.
- Advisory scan on the **full** extracted plain tree and again on the audit tree
  (case-sensitive `grep -a -r -l -F`):

```
CVE-2019-6285 -> 0    CVE-2018-20573 -> 0   CVE-2018-20574 -> 0
CVE-2019-6292 -> 0    CVE-2017-5950  -> 0   CVE-2017-11692 -> 0
CVE-2026-75432 -> 0   GHSA-          -> 0   CVE-           -> 0
```

`remaining_advisory_id_count` is therefore **0**. The only matches of a `.git`-name search
are three tracked `.gitignore` files (`.gitignore`, `test/gtest-1.8.0/.gitignore`,
`test/gtest-1.8.0/googletest/.gitignore`), not metadata. The plain-vs-audit difference is
empty, which is exactly the declared excluded/redacted set of zero.

## 4. Build

Fresh extraction of the plain export; build directory outside the source tree; no script
from the tree was executed. Toolchain: cmake 3.28.3, g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1)
13.3.0, GNU Make 4.3.

```
cmake -S /tmp/selrev_yamlcpp/ext_plain -B /tmp/selrev_yamlcpp/build_plain \
      -DYAML_CPP_BUILD_TESTS=OFF -DYAML_CPP_BUILD_TOOLS=OFF -DCMAKE_BUILD_TYPE=Release
  -> exit 0
cmake --build /tmp/selrev_yamlcpp/build_plain -j$(nproc)
  -> exit 0, artifact libyaml-cpp.a (948,954 bytes), 0 compiler errors, 1 warning
     (deprecation-style notes only)
```

Build result: **build_ok = true**. The vendored googletest tree and the tools/tests targets
were not built (they were disabled).

## 5. Anchor verification

Fetched (through the proxy) NVD API 2.0, OSV (`CVE-2019-6285` and
`DEBIAN-CVE-2019-6285`), CVE.org CVE Services, GitHub Advisory API, and Debian sources.

- **NVD** (`https://nvd.nist.gov/vuln/detail/CVE-2019-6285`): vulnerable CPE
  `cpe:2.3:a:yaml-cpp_project:yaml-cpp:0.6.2`; CWE-674; CVSS 3.0
  `AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H` 6.5 MEDIUM; published 2019-01-14T22:29Z.
- **OSV** (`https://osv.dev/vulnerability/CVE-2019-6285`): GIT range repo
  `https://github.com/jbeder/yaml-cpp`, events `introduced = 562aefc1...` and
  `last_affected = 562aefc1...`, versions `0.6.2` / `yaml-cpp-0.6.2`, modified 2026-10-20.
- **GHSA** (`https://github.com/advisories/GHSA-hg7f-3vww-rc69`): alias of CVE-2019-6285,
  medium 6.5, CWE-674 Uncontrolled Recursion, description names 0.6.2.
- **CVE.org** (`https://www.cve.org/CVERecord?id=CVE-2019-6285`): PUBLISHED, assigner
  mitre, description names yaml-cpp 0.6.2; CNA affected versions are recorded as `n/a`.
- **Debian** (`https://security-tracker.debian.org/tracker/CVE-2019-6285`): bookworm,
  trixie and forky ranges are `introduced 0`, `fixed 0.6.3-1`. The Debian source patch
  `debian/patches/fix-unbounded-recursion-depth.patch` carries
  `Origin: https://github.com/jbeder/yaml-cpp/pull/807` — a downstream backport of the fix.

Fix-commit ancestry (git in the fresh clone):

```
git merge-base --is-ancestor 4edff1fa5dbfca16fc72d89870841bee89f8ef89 562aefc1...  -> exit 1 (not ancestor)
git merge-base --is-ancestor 4edff1fa5dbfca16fc72d89870841bee89f8ef89 9a36242...  -> exit 1 (not ancestor)
git merge-base --is-ancestor 4edff1fa5dbfca16fc72d89870841bee89f8ef89 yaml-cpp-0.7.0 -> exit 0
git tag --contains 4edff1fa...  -> 0.8.0, yaml-cpp-0.7.0, yaml-cpp-0.9.0
```

So `4edff1fa` ("Fix stack overflow (#807)", 2020-04-09) is **not** an ancestor of the
0.6.2 commit and **not** an ancestor of vanilla tag `yaml-cpp-0.6.3`
(`9a3624205e8774953ef18f57067b3426c1c5ada6`, 2019-09-25); the first upstream release
containing it is `yaml-cpp-0.7.0`. Debian's `fixed_version 0.6.3-1` is therefore a
Debian-patched source package, not evidence that vanilla 0.6.3 is fixed.

Source-level confirmation in the exported/committed tree: `src/singledocparser.cpp` at
`562aefc1` has `HandleFlowSequence` (line 183) looping over nodes and calling
`HandleNode(eventHandler)` for each, i.e. recursive flow-sequence handling, and a
`git grep -i 'depth|recursion|max.*nest'` over `src/` and `include/` finds only
`nodebuilder.cpp`'s `m_mapDepth` bookkeeping counter — **no depth guard**. The fix commit
`4edff1f` adds `include/yaml-cpp/depthguard.h`, `src/depthguard.cpp`, and
`DepthGuard<2000> depthguard(depth, m_scanner.mark(), ErrorMsg::BAD_FILE)` at the top of
`HandleNode`.

All sources agree that yaml-cpp 0.6.2 is affected. The only apparent disagreement —
Debian's `fixed_version 0.6.3-1` versus vanilla 0.6.3 — is explained and not a conflict:
Debian backports PR 807. The tag is a legitimate pre-fix target.

## 6. Release sanity

- `yaml-cpp-0.6.2` is a stable release tag in the canonical `yaml-cpp-0.6.x` line, no
  pre-release suffix.
- Commit date `2018-03-05T22:56:23-06:00` (`2018-03-06T04:56:23Z`) is inside the discovery
  window ending 2026-10-21.
- `CMakeLists.txt` lines 29–32 set `YAML_CPP_VERSION_MAJOR/MINOR/PATCH` to `0/6/2`, i.e.
  the CMake version string reads `0.6.2`.
- Later tags in the line: `yaml-cpp-0.6.3` is also pre-fix upstream but is not the
  published affected version and post-dates the CVE; `yaml-cpp-0.7.0` already contains the
  fix and is therefore not a valid pre-fix target. 0.6.2 is the canonical target, pinned by
  the OSV GIT range and named by NVD/GHSA.

## 7. Independence

`reviewed_by = independent-selection-reviewer-yamlcpp-2026-10-23`, distinct from the
selector `claude-code-orchestrator-2026-10-23`.

## Discrepancies from the packet

1. `tag_facts.tag_commit_tree_sha` is `null` while `tag_tree_matches_commit` is `true`. I
   measured the tag/commit tree as `296d72b846796a97e4e5f08e8ef64553d1e51756`, which equals
   `export_facts.tree_sha`; the null is an omission, not a factual conflict.
2. `build_facts.build_attempted` is `false` and `status` is `toolchain_available`. I ran
   the build; it succeeds (exit 0), so the packet understates what is now verified.
3. The packet's leakage scan is described as `lexical_regex_first_1MiB_text_files`; my
   full-tree `grep -a` scan confirms the same conclusion (zero advisory identifiers), so
   the sampling does not hide anything.
4. The packet's severity block discloses that the CVSS 3.1 vector is a re-expression of
   NVD's 3.0 metrics; NVD publishes only 3.0 (6.5 MEDIUM), which I confirmed. This is a
   disclosed schema normalisation, not a data error.
5. The packet publishes no audit-export hashes. I measured them byte-identical to the plain
   export, which is consistent with the declared zero excluded/redacted set.

No discrepancy changes the selection decision.

## Limitations

- Only the library configuration was built (tests/tools off); googletest and test binaries
  were not compiled.
- Affectedness was established from public advisories and source inspection, not from a
  runtime crash reproduction.
- Debian 0.6.3-1 source is no longer the archived version served by sources.debian.org
  (latest 0.6.3-9); the backport was confirmed from the 0.6.3-9 patch set, whose
  `fix-unbounded-recursion-depth.patch` still names upstream PR 807.
- CVE.org's CNA record lists affected versions as `n/a`, so it corroborates identity and
  publication but not the range.
- Public endpoints can change; measurements reflect responses fetched 2026-10-22 UTC.
