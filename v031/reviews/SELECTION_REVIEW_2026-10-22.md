# Independent Selection Review — 2026-10-22

Reviewer: `independent-review-agent-2026-10-22`
Scope: evaluation-target selection only (22 packets in `v031/reviews/selection_packets/`).
Verdict rule applied: accept only if checks 1, 3, 4 and 5 pass and checks 2/6 do not trigger a reject reason.

## Summary

| Repo | Tag | Verdict | Reason |
|---|---|---|---|
| netty/netty | `netty-4.1.59.Final` | **reject** | obsolete_release_over_4_years: tag date 2021-02-08 is 5.70 years before 2026-10-22 and 100 newer stable tags exist (newest netty-4.2.19.Final = 4.2.19.Final) |
| jenkinsci/jenkins | `jenkins-2.441` | **accept** | all checks pass; anchors verified; not obsolete |
| nodejs/undici | `v5.19.0` | **accept** | all checks pass; anchors verified; not obsolete |
| guzzle/guzzle | `7.4.4` | **reject** | obsolete_release_over_4_years: tag date 2022-06-09 is 4.37 years before 2026-10-22 and 53 newer stable tags exist (newest 8.3.0 = 8.3.0) |
| phoenixframework/phoenix | `v1.6.13` | **reject** | obsolete_release_over_4_years: tag date 2022-09-29 is 4.06 years before 2026-10-22 and 46 newer stable tags exist (newest v1.8.16 = 1.8.16) |
| gin-gonic/gin | `v1.5.0` | **reject** | obsolete_release_over_4_years: tag date 2019-11-24 is 6.91 years before 2026-10-22 and 20 newer stable tags exist (newest v1.12.0 = 1.12.0) |
| protocolbuffers/protobuf | `v3.20.1` | **reject** | obsolete_release_over_4_years: tag date 2022-04-22 is 4.50 years before 2026-10-22 and 217 newer stable tags exist (newest v36.2 = 36.2) |
| hyperium/hyper | `v0.14.2` | **reject** | obsolete_release_over_4_years: tag date 2020-12-29 is 5.81 years before 2026-10-22 and 51 newer stable tags exist (newest v1.12.0 = 1.12.0) |
| expressjs/express | `4.19.2` | **accept** | all checks pass; anchors verified; not obsolete |
| vitejs/vite | `v5.0.11` | **accept** | all checks pass; anchors verified; not obsolete |
| libarchive/libarchive | `v3.7.7` | **accept** | all checks pass; anchors verified; not obsolete |
| JamesNK/Newtonsoft.Json | `12.0.3` | **reject** | obsolete_release_over_4_years: tag date 2019-11-09 is 6.95 years before 2026-10-22 and 4 newer stable tags exist (newest 13.0.4 = 13.0.4) |
| django/django | `3.0.2` | **reject** | obsolete_release_over_4_years: tag date 2020-01-02 is 6.80 years before 2026-10-22 and 192 newer stable tags exist (newest 6.1.2 = 6.1.2) |
| symfony/symfony | `v5.4.45` | **accept** | all checks pass; anchors verified; not obsolete |
| DaveGamble/cJSON | `v1.7.16` | **accept** | all checks pass; anchors verified; not obsolete |
| curl/curl | `curl-8_3_0` | **accept** | all checks pass; anchors verified; not obsolete |
| rustls/rustls | `v/0.23.4` | **accept** | all checks pass; anchors verified; not obsolete |
| pallets/flask | `2.3.1` | **accept** | all checks pass; anchors verified; not obsolete |
| laravel/framework | `v11.30.0` | **accept** | all checks pass; anchors verified; not obsolete |
| libexpat/libexpat | `R_2_4_4` | **reject** | obsolete_release_over_4_years: tag date 2022-01-30 is 4.73 years before 2026-10-22 and 24 newer stable tags exist (newest R_2_9_0 = 2.9.0) |
| rack/rack | `2.2.3` | **reject** | obsolete_release_over_4_years: tag date 2020-06-15 is 6.35 years before 2026-10-22 and 80 newer stable tags exist (newest v3.2.7 = 3.2.7) |
| pallets/werkzeug | `3.0.2` | **accept** | all checks pass; anchors verified; not obsolete |

**Counts: 12 accept / 10 reject.** All 10 rejects are release-sanity (check 2) only: the proposed tag is more than 4 years old at 2026-10-22 while newer stable tags exist for the same project. Checks 1, 3, 4, 5 and 6 passed for every packet, including all rejects.

## Checks actually run

### 1. Tag integrity
- For every packet: `git ls-remote --tags <canonical_url>.git refs/tags/<tag> refs/tags/<tag>^{}`; compared the peeled commit SHA (or the plain SHA for lightweight tags) against `proposed_target.commit_sha`.
- 21/22 resolved identically (annotated tags compared peeled; lightweight tags: undici v5.19.0, guzzle 7.4.4, gin v1.5.0, protobuf v3.20.1, hyper v0.14.2, Newtonsoft 12.0.3, cJSON v1.7.16, rustls v/0.23.4, laravel v11.30.0, werkzeug 3.0.2).
- `expressjs/express` uses `accepted_via=identical_tree`: tag `4.19.2` peels to `04bc62787be974874bc1467b23606c36bc9779ba`, while the proposed commit is `b28db2c12c3bd9cd763316824446f79bf81e0686`. Both commits were fetched independently (`git init` + `git fetch --depth=1 <sha>`) and `git rev-parse <sha>^{tree}` returned `f18a74c2f183fd0ab2bd3b411ddd44b792d4481a` for both — identical trees, so check 1 passes on the identical-tree path.
- Also verified per packet that `export_facts.tree_sha` equals the proposed commit's tree from `GET /repos/{owner}/{repo}/commits/{sha}` (22/22 match).

### 2. Release sanity
- Commit dates from `GET /repos/{owner}/{repo}/commits/{sha}` (committer date).
- Full tag lists from `git ls-remote --tags`; tags matching `alpha|beta|rcN|dev|preview|snapshot|canary|nightly` were excluded before counting "newer stable tags".
- Applied the stated rule: reject if tag age > 4 years at 2026-10-22 **and** newer stable tags exist. Ten packets triggered it (ages: netty 5.70y, guzzle 4.37y, phoenix 4.06y, gin 6.91y, protobuf 4.50y, hyper 5.81y, Newtonsoft 6.95y, django 6.80y, libexpat 4.73y, rack 6.35y). No proposed tag is a prerelease/dist/channel tag. phoenix v1.6.13 clears the threshold only by ~23 days and is flagged as the marginal case in its `notes`.
- Note: `jenkins-2.441` is a Jenkins weekly release tag; it is a normal stable release in that repo, not a prerelease/channel tag.

### 3. Export integrity
- Recomputed SHA-256 of each `.tar.gz` and each `.manifest.jsonl`; 22/22 matched the packet (and archive byte sizes matched).
- Listed archive members with `tarfile` (no extraction): zero `.git/` paths in all 22; `leakage_facts.git_metadata_present=false` in all 22.
- Counts: `exported_file_count + symlink_count == tree_file_count` and `missing_from_archive_count == 0` for all 22. Manifest type counts agreed with the packet; gitlinks (protobuf: 2) are correctly absent from the manifest.
- Extra content check (beyond the minimum): every archive member's bytes hashed to the manifest `sha256`/`size` (0 mismatches across 49,085 files), and the manifest path set equals `GET /repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1` (0 missing, 0 extra, symlinks included) for all 22.

### 4. Build feasibility
- Every packet's `build_facts.systems` and `build_facts.indicators` contain at least one standard build entry point (CMakeLists.txt, configure.ac/Makefile.am, pom.xml, Cargo.toml, package.json, composer.json, setup.py/pyproject.toml, mix.exs, Gemfile, go.mod, global.json). `build_ok=true` for all 22.
- Missing local toolchains (dotnet for Newtonsoft.Json; php/composer for symfony) were recorded but are not a reject reason per the rules.

### 5. Advisory truth
- Queried `https://api.osv.dev/v1/vulns/<ID>` for all 73 anchors, plus 67 alias records (GHSA-/PYSEC-/RUSTSEC-/GO-).
- For each anchor, evaluated the proposed version against (a) `affected[].versions` (including tag-style spellings such as `curl-8_3_0`, `R_2_4_4`, `v/0.23.4`, `netty-4.1.59.Final`) and (b) every numeric range in `ranges[].events` and `ranges[].database_specific.extracted_events`, across all affected entries and all fix lines (weekly/LTS, 5.x/4.x, etc.).
- 73/73 anchors confirmed affected; every packet has at least one confirmed anchor, so no `no_verified_positive_at_snapshot` reject.
- Range examples recorded in the JSONL: curl 8.3.0 `7.69.0 <= 8.3.0 < 8.4.0` (CVE-2023-38545); express 4.19.2 `0 <= 4.19.2 < 4.20.0` (GHSA-qw6h-vgh9-j6wx = CVE-2024-43796); jenkins 2.441 `0 <= 2.441 < 2.442` (CVE-2024-23897); vite 5.0.11 `5.0.0 <= 5.0.11 < 5.2.14` (CVE-2024-45811); rustls 0.23.4 `0.23.0 <= 0.23.4 < 0.23.5` (CVE-2024-32650); django 3.0.2 `3.0 <= 3.0.2 < 3.0.7` (CVE-2020-13254); werkzeug 3.0.2 `0 <= 3.0.2 < 3.0.3` (CVE-2024-34069).
- `libarchive` CVE-2025-5915 needed extra work: the record's `affected.versions` stops at v3.7.5 and omits v3.7.7, but its AFFECTED_FIELD/CPE ranges read `0 <= 3.7.7 < 3.8.0`. Cross-checked with GitHub: the fix commit `70ff28fcf04ec129a1d064f96e49aa57fcc90e37` is the "Release 3.8.0" commit (2025-05-20) and `compare/v3.7.7...70ff28fcf0` reports `diverged` (behind_by=32), so the fix is not in 3.7.7 — confirmed affected.

### 6. Leakage
- `git_metadata_present=false` for all 22 (also confirmed by tar listing); no ground-truth/oracle rejection could be established.
- Scanned every exported text file (<=2 MB) for the packet's own target advisory IDs: zero occurrences in all 22. The CVE strings the packets report (e.g. curl's older CVE-2000-0973, CVE-2019-3822) are incidental changelog/security-doc text and are not a reject per policy.
- Filename scan for oracle/ground-truth/answer/poc/exploit-style names produced only benign hits (upstream benchmarks, Oracle-DB tests such as `jenkins/core/src/test/resources/jenkins/monitor/os-release-oracle-7` and `django/tests/dbshell/test_oracle.py`).

## Caveats
- "Newer stable tags exist" is evaluated on the repo's own tag namespace with prerelease tokens filtered; it does not attempt to model per-branch support policy, so a packet could in principle be on a still-supported branch (e.g. netty 4.1.x, symfony 5.4.x). The rule as stated is age + newer-stable-tags, and it was applied literally.
- Absence of a deliberately planted oracle file cannot be proven from a source export; no evidence of one was found.

Artifacts: `v031/reviews/selection_review_2026-10-22.jsonl` (22 lines).
