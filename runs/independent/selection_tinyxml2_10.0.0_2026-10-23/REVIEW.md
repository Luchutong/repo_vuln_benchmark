# Selection review: leethomason/tinyxml2 @ 10.0.0 (snap_5b58f4c33f6103b5)

Reviewer: `deepseek-flash-independent-selection-reviewer-2026-10-23`
Reviewed at: 2026-10-23T00:17:57Z
Packet: `/home/luchitong/work/repo-vuln-50-v031/v031/reviews/selection_packets/3542607_leethomason__tinyxml2.json`

## Verdict: APPROVED (accept)

All four mandatory checks pass: tag resolution, export integrity, build, and positive anchor.

## 1. Tag resolution

```
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
git ls-remote --tags https://github.com/leethomason/tinyxml2
```

Observed (relevant line):

```
321ea883b7190d4e85cae5512a12e5eaa8f8731f	refs/tags/10.0.0
```

There is no `refs/tags/10.0.0^{}` line, which means the tag is lightweight and there is no tag object to peel.

Corroborated via GitHub REST API:

- `GET https://api.github.com/repos/leethomason/tinyxml2/git/ref/tags/10.0.0` -> `object.type = "commit"`, `object.sha = 321ea883b7190d4e85cae5512a12e5eaa8f8731f` (annotated tags return `type = "tag"` here).
- `GET .../git/commits/321ea883...` -> author/committer date `2023-12-31T02:08:30Z` (local `2023-12-30T18:08:30-08:00`, epoch 1703988510), tree `d0705dfde7203c93642a251bbec61025c20f3967`, message `Merge pull request #965 from leethomason/v10.0.0`.
- `GET .../releases/tags/10.0.0` -> `tag_name=10.0.0`, `name=v10.0.0`, `draft=false`, `prerelease=false`, `published_at=2023-12-31T02:10:24Z`. Stable release, not a dist/channel tag.

| field | measured | expected | match |
|---|---|---|---|
| resolved_tag_sha | 321ea883b7190d4e85cae5512a12e5eaa8f8731f | same | yes |
| object_type | commit (lightweight) | n/a | n/a |
| commit_date_utc | 2023-12-31T02:08:30Z | n/a | n/a |
| commit_tree | d0705dfde7203c93642a251bbec61025c20f3967 | d0705df... | yes |

## 2. Export checks

Artifacts under `/home/luchitong/work/repo-vuln-50-v031/exports/leethomason__tinyxml2/`:

```
sha256sum snap_5b58f4c33f6103b5.tar.gz snap_5b58f4c33f6103b5.manifest.jsonl
8ee4dbb6ebb5eeca2d45a5a9b54641cabb01a97372def419297315d4167d7dd4  snap_5b58f4c33f6103b5.tar.gz
ca607417f407481c0138d88cbf461790e3b285c762cff54ae1833297ef02a4ce  snap_5b58f4c33f6103b5.manifest.jsonl
```

- `archive_sha256_matches`: true (measured == packet == `8ee4dbb6...7dd4`)
- `manifest_sha256_matches`: true (measured == packet == `ca607417...a4ce`)
- `archive_bytes`: 632032, matches packet.
- Both `.audit.tar.gz` and `.audit.manifest.jsonl` are byte-identical (`cmp`) to the named artifacts.

Extraction:

```
D=$(mktemp -d /tmp/tinyxml2_selrev.XXXXXX)   # -> /tmp/tinyxml2_selrev.hiXwBj
tar -xzf snap_5b58f4c33f6103b5.tar.gz -C "$D"
find "$D" -type f | wc -l   # 273
find "$D" -type l | wc -l   # 0
find "$D" -name .git        # (no output)
tar -tzf ... | wc -l        # 273, all regular-file entries, 0 paths containing "/.git/"
```

Manifest comparison (`/tmp/selrev_scripts/verify_manifest.py`, run with `python3 -I`):

```
{"entries": 273, "disks_files": 273, "mismatches": [], "extra_on_disk": [], "entries_not_on_disk": []}
```

Git tree comparison against a fresh full clone (`git clone https://github.com/leethomason/tinyxml2 /tmp/tinyxml2_clone`):

```
git -C /tmp/tinyxml2_clone rev-parse 321ea883...^{tree}   # d0705dfde7203c93642a251bbec61025c20f3967
git -C /tmp/tinyxml2_clone ls-tree -r 321ea883... | wc -l # 273
mode histogram: 266 x 100644, 7 x 100755   (no 120000 symlink, no 160000 gitlink)
```

`/tmp/selrev_scripts/verify_gittree.py` recomputed sha256 of every git blob via `git cat-file blob` and compared to the manifest:

```
{"git_entries": 273, "manifest_entries": 273, "sha_or_mode_mismatches": [], "in_git_not_manifest": [], "in_manifest_not_git": []}
```

| check | result |
|---|---|
| archive_sha256_matches | true |
| manifest_sha256_matches | true |
| no_git_metadata | true |
| counts_reconcile | true (273 exported + 0 symlink + 0 gitlink = 273 tree files) |
| tree_sha | d0705dfde7203c93642a251bbec61025c20f3967 == packet |
| manifest_entries_checked / mismatches | 273 / 0 |

## 3. Build

```
cmake --version   # cmake version 3.28.3
g++ --version     # g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
make --version    # GNU Make 4.3

cmake -S /tmp/tinyxml2_selrev.hiXwBj -B /tmp/tinyxml2_build -DCMAKE_BUILD_TYPE=Debug
# exit 0
cmake --build /tmp/tinyxml2_build -j
# [100%] Built target xmltest, exit 0
```

Consumer run (`xmltest` needs `resources/dream.xml`, so cwd = extracted source root):

```
cd /tmp/tinyxml2_selrev.hiXwBj && /tmp/tinyxml2_build/xmltest
# Pass 508, Fail 0 ; exit 0
```

`build_ok = true`. Test success is not treated as a selection criterion, but it confirms the export is a coherent, buildable tree.

## 4. Positive anchor

Anchor: CVE-2024-50615 (aliases GHSA-884x-p7qm-gq3f, DEBIAN-CVE-2024-50615).

- OSV: `https://api.osv.dev/v1/vulns/CVE-2024-50615` -> `affected: true`. The record lists `versions` including `10.0.0` and a GIT range `{introduced: "0"}, {last_affected: "321ea883b7190d4e85cae5512a12e5eaa8f8731f"}` — the last affected commit is exactly the 10.0.0 release commit. No `first_patched` in the GIT range.
- GHSA: `https://github.com/advisories/GHSA-884x-p7qm-gq3f` -> `cve_id=CVE-2024-50615`, severity medium, `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H` = 6.5, summary "TinyXML2 through 10.0.0 has a reachable assertion for UINT_MAX/digit...", published 2024-10-28T00:30:48Z. Note: its machine-readable `vulnerabilities` array is empty because tinyxml2 is not registered in a GitHub-supported package ecosystem; affectedness is from the text, corroborated by OSV/NVD.
- NVD 2.0: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2024-50615` -> status "Analyzed", CPE `cpe:2.3:a:tinyxml2_project:tinyxml2:*:*:*:*:*:*:*:*`, `vulnerable: true`, `versionEndIncluding: 10.0.0`.

The packet's severity description (secondary CISA-ADP metric at 6.5, no NVD Primary, no CVSS in CVE.org; GHSA carries the identical vector) is consistent with what the APIs return.

## Concerns / observations

- None disqualifying.
- `tag_facts.tag_commit_tree_sha` is `null` in the packet even though the tree exists (`d0705df...`); the packet only uses it for a boolean `tag_tree_matches_commit`, which is true.
- The GHSA advisory's `vulnerabilities` array is empty; anchor affectedness rests on OSV's version list/GIT range, the GHSA prose, and the NVD CPE.
- The extracted tree includes `docs/` and `dox` (a generated HTML/API doc blob) because the export is the full tracked tree, including export-ignored paths; this matches the packet's `source_completeness` note.

## Reproduction assets

- Extraction dir: `/tmp/tinyxml2_selrev.hiXwBj`
- Build dir: `/tmp/tinyxml2_build`
- Fresh clone: `/tmp/tinyxml2_clone`
- Helper scripts (outside the untrusted tree, run with `python3 -I`): `/tmp/selrev_scripts/verify_manifest.py`, `/tmp/selrev_scripts/verify_gittree.py`, `/tmp/selrev_scripts/git_tree.txt`
