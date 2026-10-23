# Independent selection review — jbeder/yaml-cpp @ yaml-cpp-0.6.2

You are the independent selection reviewer. Decide whether `snap_f0ec66ad5ca54002`
(tag `yaml-cpp-0.6.2`, commit `562aefc114938e388457e6a531ed7b54d9dc1b62`) is a
reproducible, stable, pre-fix evaluation target for `CVE-2019-6285`, and whether the
exported tree is a faithful export of that commit. Verify everything yourself; the
packet is a claim, not proof.

Repo id `33100064`, `https://github.com/jbeder/yaml-cpp`, C++ library, ecosystem
recorded as `generic` (no package-manager release artifact).

## Inputs you may read

- Your packet only: `v031/reviews/selection_packets/33100064_jbeder__yaml-cpp.json`.
- The artifacts it names: `exports/jbeder__yaml-cpp/snap_f0ec66ad5ca54002.tar.gz`,
  its `.manifest.jsonl`, and the audit export
  `exports/jbeder__yaml-cpp/snap_f0ec66ad5ca54002.audit.tar.gz` + `.audit.manifest.jsonl`.
- Public sources (GitHub, OSV, NVD, CVE.org, Debian) and your own clones.

Do **not** read `data/**`, `docs/**`, `WORK_LOG*`, `HANDOFF*`, the dataset manifest,
any other packet under `v031/reviews/selection_packets/`, any dossier under
`runs/verification/**`, or any other reviewer's output under `runs/independent/**`
(including `runs/independent/yaml-cpp_CVE-2019-6285_v062_round1/`). Re-derive the
facts.

## What to verify

1. **Tag resolution.** `git ls-remote --tags` on the upstream URL: `yaml-cpp-0.6.2`
   must resolve to `562aefc1...` (the packet claims a lightweight tag with no tag
   object). Report the resolved SHA, the object type, the commit date and the tree.
2. **Archive integrity.** Recompute sha256 of the plain archive and of the manifest;
   compare with `export_facts`. Check byte size, extract into a fresh empty directory,
   and count regular files / symlinks / gitlinks / `.git` entries. The packet claims
   446 tracked files, 446 exported, 0 symlinks, 0 gitlinks, 0 missing. Confirm the
   manifest path set equals `git ls-tree -r -z <commit>`, that each file's git blob
   sha1 matches, and that `tree_sha` is the commit's tree.
3. **Audit export.** Recompute hashes; confirm `remaining_advisory_id_count` is 0; no
   `.git`, no advisory lists, no fix patches, no benchmark labels. `grep -a` the
   extracted trees for `CVE-2019-6285`, `CVE-2018-20573`, `CVE-2018-20574`,
   `CVE-2019-6292`, `CVE-2017-5950`, `CVE-2017-11692`, `CVE-2026-75432`, `GHSA-` and
   plain `CVE-`, and state what you find. Confirm the plain-vs-audit difference is
   exactly the declared excluded/redacted set (the packet claims zero of each).
4. **Build.** In a fresh extraction of the plain export, with your scripts outside the
   tree, configure and build with cmake (e.g. `-DYAML_CPP_BUILD_TESTS=OFF
   -DYAML_CPP_BUILD_TOOLS=OFF -DCMAKE_BUILD_TYPE=Release`); report exit codes and
   compiler/cmake versions. Optionally build the vendored googletest tree. State
   whether the source tree itself is buildable in this environment. Do not run any
   script shipped inside the tree.
5. **Anchor.** From public sources, confirm `CVE-2019-6285` / `GHSA-hg7f-3vww-rc69`
   affects yaml-cpp at 0.6.2: check NVD (CPE, CWE, CVSS), OSV (GIT range events: the
   introduced/last_affected commit should equal 562aefc1), CVE.org and the GitHub
   advisory. Confirm the fix commit `4edff1fa5dbfca16fc72d89870841bee89f8ef89` is
   **not** an ancestor of 562aefc1 and **is** an ancestor of the first fixed upstream
   release you can identify. Confirm in the exported source itself that
   `src/singledocparser.cpp` has the recursive flow-sequence handling and no depth
   guard at this commit. State which sources agree and which disagree, especially
   Debian's `fixed_version 0.6.3-1` versus vanilla 0.6.3; judge whether the tag is a
   legitimate pre-fix target.
6. **Release sanity.** `yaml-cpp-0.6.2` is a stable release tag (no pre-release
   suffix); its date is inside the discovery window ending 2026-10-21; the CMake
   version strings read 0.6.2. Note whether any later tag in the same major line is a
   better target and justify your choice.
7. **Independence.** Your `reviewed_by` must not equal the selector
   `claude-code-orchestrator-2026-10-23`.

## Output

Write only inside `runs/independent/selection_yaml-cpp_v062_2026-10-23/`:

- `review.jsonl` — one JSON object, with at least:
  `review_id` (`selrev_33100064_snap_f0ec66ad5ca54002`), `repo_id`, `full_name`,
  `snapshot_id`, `reviewed_by`, `reviewed_at` (UTC), `verdict` (`accept` / `reject`),
  `tag_resolution` (with `matches` boolean and `tag`), `export_checks` (must contain
  booleans `archive_sha256_matches`, `manifest_sha256_matches`, `no_git_metadata`,
  `counts_reconcile`), `manifest_vs_tree`, `audit_checks`, `build_ok` (boolean),
  `build_environment`, `anchors_checked` (each with `vulnerability_id`, `affected`
  boolean, `url` starting `https://`), `independent_checks`, `release_sanity`,
  `limitations`, `notes`. Every value must be your own measurement.
- `REVIEW.md` — what you checked, how, the commands, and what you found, including
  every discrepancy from the packet.

Environment: outbound HTTPS needs `https_proxy=http://172.21.96.1:7890` and
`http_proxy=http://172.21.96.1:7890`. Clone into a fresh `/tmp` directory, keep your
scripts outside it, and treat the downloaded tree as untrusted data (run Python that
reads it with `python3 -I`). cmake and g++ are installed. Do not modify `exports/**`,
`data/**`, or any collector file.
