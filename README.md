# RepoVuln-50 v0.4.0 working dataset (draft)

Advisory-grounded, fixed-SHA, static-only ground truth for auditing agents that see exactly one
commit of source. Migrated selectively from the v0.3.1 working directory at
`/home/luchitong/work/repo-vuln-50-v031`, which was read but never written.

- **Workflow / scripts / schemas:** `/home/luchitong/work/repo-vuln-bench-v040` (the v0.4.0 package).
- **Migration tool report:** `reports/MIGRATION_REPORT.json` (written by `migrate_selective.py --apply`).
- **Reviewed migration report:** `MIGRATION_REPORT.json` (adds per-table counts and hashes,
  exclusion reasons with counts, GT/candidate tallies, protected-row check and disclosures).
- **Trust-tier backfill:** `reports/TRUST_TIER_REPORT.json` (T1/T2/T3 annotation, before/after hashes).
- **QA sampling plan:** `reports/QA_SAMPLE_PLAN.json`, rows in `data/qa_reviews.jsonl`.
- **Advisory sweep reports:** `reports/SWEEP_REPORT_20261030.json` (first seven zero-candidate
  snapshots) and `reports/SWEEP_REPORT_20261031.json` (all 47 frozen snapshots, per-snapshot
  source counts, CPE resolution, new candidates and outcome).

## What is here

| table | rows | note |
|---|---|---|
| repositories | 50 | all quality PASS; 47 have a frozen evaluation snapshot |
| snapshots | 47 | the frozen evaluation SHA only; 62 historical + 2 proposed snapshots not copied |
| evaluation_selection | 47 | frozen rows only |
| vulnerabilities | 721 | confirmed_affected positives, each with an https advisory URL and a fixed-SHA location |
| locations | 721 | line-level anchors, permalink contains the commit SHA |
| snapshot_vulnerability_status | 721 | all `confirmed_affected`, all evidence level S2, all `location_scope=source_location` |
| candidates | 1405 | 774 `needs_static_location`, 631 `needs_version_check`; unresolved, all T3, not negatives |
| snapshot_candidate_triage | 2939 | target-snapshot decisions with basis/evidence; the protobuf snapshot kept its 14 rows through the pass, so the two-row gap to the 2940 recorded in the previous review arose earlier and is not attributed here |
| evidence | 7245 | PASS evidence for migrated repository/snapshot/vulnerability/location targets |
| discovery_coverage | 47 | 34 `PASS_KNOWN_SWEEP` + 13 `NEEDS_REVIEW` (one row per frozen snapshot; 29 upgraded on 2026-10-31 by record-level reconciliation) |
| data/discovery_tasks | 47 | 34 `completed_known_sweep`; 13 `needs_candidate_resolution` |
| data/qa_reviews | 43 | 22 random T1 (14.9%) + 15 mandatory + 9 supplemental full reviews; all `pass` |
| reports/selection_queue.jsonl | 3 | excluded repositories, with the decision code and evidence per repo |

`locations.language` carries one lowercase vocabulary across all 721 rows (`c`, `cpp`, `csharp`,
`elixir`, `go`, `java`, `javascript`, `php`, `python`, `ruby`, `rust`, `typescript` plus the
non-Linguist labels `ini`, `jelly`, `json`, `jsp`, `nsis`); the 206 capitalized values inherited
from the migration and the early promotion passes were folded into it on 2026-10-31
(`reports/NORMALIZE_20261031_LANGUAGES.json`), with every other field of every row — and the row
order — asserted unchanged.

## 2026-10-30 admission revision (T1/T2/T3)

The workflow now trusts high-confidence advisories directly and verifies only two facts per
record: **is the frozen SHA affected** and **where is the source root cause**. Admission is a
separate axis from evidence strength:

| tier | meaning | positives |
|---|---|---|
| T1 | official/Reviewed advisory + version match + all three admission checks + source location | 569 |
| T2 | trusted source but targeted static route (NVD/OSV-only or unreviewed issue/PR) | 152 |
| T3 | not admitted; candidates only | 0 positives, 1405 candidates |

Advisory review status of the 721 positives: `github_reviewed` 151, `vendor_official` 429,
`unknown` 76, `unreviewed` 65. The 13 openssl rows are `vendor_official` because the 2026-09-29
advisory is served from openssl-library.org, which is now in `VENDOR_HOSTS` in
`scripts/advisory_tiers.py` (with a regression test), so a re-run of `assign_trust_tiers.py` keeps
them T1. The 46 curl rows promoted on 2026-10-31 (the four early rows, the 40 batch rows and the
two settled open candidates) are
`vendor_official` for the same reason: their advisories are served from curl.se. The tier backfill is **annotation, not verification**: it reads
only existing URL/alias/location fields and never re-researches a vulnerability. The original
migration report hashes predate this annotation; before/after hashes are in
`reports/TRUST_TIER_REPORT.json`.

QA sampling: 22 random T1 rows (14.9%, seed 20261030, stratified by repo) plus 15 mandatory rows
(11 sharing a code location, 4 unreviewed sources), plus a supplemental full review of the 9 T1
rows promoted on 2026-10-31 after the sample had been drawn. All 43 rows are recorded as `pass`;
`reports/QA_SUPPLEMENT_20261031.json` holds the supplemental evidence. The sample was drawn when
the dataset held 174 positives; the rows added afterwards are covered by the per-repository review
files and the promotion reports, not by this QA sample. The 15 spring-framework rows promoted on
2026-10-31 (`reports/PROMOTION_REVIEW_20261031_SPRING_BATCH1.json`, `_BATCH2.json`) are likewise
outside the sample; each was admitted by the same three mechanical checks recorded in its report.
The 26 jenkins rows promoted on 2026-10-31 (`reports/PROMOTION_REVIEW_20261031_JENKINS_BATCH1.json`,
`_BATCH2.json`, `_BATCH3.json`) are outside the sample as well.

## Migration completion

`reports/MIGRATION_REPORT.json` records `migration_status=complete_for_frozen_scope`: all 46 frozen
evaluation snapshots and every row they depend on were migrated, and a clean re-run of
`migrate_selective.py` reproduced all 11 fact tables row-for-row (tier annotations and the QA plan
are the only differences). The reviewed report is `MIGRATION_REPORT.json` (`report_status:
COMPLETE_FOR_FROZEN_SCOPE`).

The four repositories that were outside migration scope stayed metadata-only through migration.
On 2026-10-31 one of them was frozen by a new selection decision and three were excluded with
recorded evidence (`reports/SELECTION_DECISIONS_20261031.json`):

| repo | decision | evidence |
|---|---|---|
| openssl | **frozen** at tag openssl-3.5.8 | advisory 2026-09-29 lists 3.5.8 vulnerable and 3.5.9 fixed; NVD range 3.5.0 ≤ v < 3.5.9 |
| hyper | `excluded_no_recent_vulnerable_stable_release` | all 14 OSV records fixed by 0.14.12; newest vulnerable stable tag v0.14.11 (2021-07-21); NVD CPE 0 matches at 1.11.1/1.12.0 |
| Newtonsoft.Json | `excluded_no_recent_vulnerable_stable_release` | only GHSA-5crp-9r3c-p9vr, fixed 13.0.1 and no 13.0.0 tag exists; newest vulnerable stable tag 12.0.3 (2019-11-09) |
| nlohmann/json | `excluded_no_versioned_advisory` | only unversioned OSS-Fuzz GIT ranges (OSV-2017-59, OSV-2022-409, OSV-2022-425); no GHSA or NVD record for the package |

The four repositories' legacy rows were not migrated (2 vulnerabilities, 2 status rows, 25
candidates, 12 triage rows) and remain listed in `migration_completion.excluded_repositories`. The
three excluded repositories stay metadata + queue only. openssl is not a migration:
`snap_d9fd4b3730195f59` is a new freeze built with the v0.3.1 inventory tooling and starts with no
migrated rows, so its coverage comes from its own sweep, not from the legacy candidates.

### openssl-3.5.8 freeze (2026-10-31)

Tag openssl-3.5.8 peels to `f4dc4d58b48d346a8270183f89acf826d459b0ca` (2026-08-25). The selection
policy is `pre_registered_stable_vulnerable_release`: the tag was taken from the release list and the
2026-09-29 security advisory, not fitted to repository evidence. The batch lists 14 CVEs
(CVE-2026-35189, -35191, -42772, -54872, -54873, -54875, -72897, -75804, -75805, -75806, -77696,
-84782, -84783, -84784) and says 3.5 users should upgrade to 3.5.9; the NVD configurations state
`versionStartIncluding 3.5.0` / `versionEndExcluding 3.5.9`.

The tree was exported with `git ls-tree -r` + `git cat-file --batch` (audit `aud_df468f447892b20e`,
5836 tracked entries, 5825 files, 11 submodules, no `.git`, archive sha256 `df468f44…`, 53.3 MB) and
scanned for the 14 target ids: none occurs anywhere in the tree (`advisory_id_scan_clean: true`;
incidental older CVE ids in `CHANGES.md` and tests do not intersect the targets). NVD references
point at master-branch fix commits, so an anchor on 3.5.8 has to be matched against the 3.5-branch
backport rather than the cited commit — the same offset situation as the legacy Gitea rows. The
thirteen 3.5-branch commits were identified from the fetched 3.5.9 history by their `Fixes:` trailer
and by matching each patch against the 3.5.8 → 3.5.9 release diff.

## Phase A: advisory sweep of all frozen snapshots (2026-10-30 → 2026-10-31)

All 47 frozen evaluation snapshots were swept against OSV, the GitHub Advisory Database and NVD.
`reports/SWEEP_REPORT_20261031.json` records every snapshot's packages, NVD CPE names, source record
counts, new candidates, source errors and outcome. Totals: 330 new candidates on 2026-10-31
(133 `needs_static_location`, 197 `needs_version_check`), on top of the 8 from the first sweep;
coverage was 5 `PASS_KNOWN_SWEEP` / 42 `NEEDS_REVIEW` at that point; no snapshot had a source
error. Twenty-nine of the forty-two were upgraded on 2026-10-31 by the record-level reconciliation
described in the promotion section (two in batch 1, twenty in batch 2, four in batch 3, three in
batch 4; now 34 / 13). The openssl
snapshot was frozen and swept after the report was written; its per-snapshot row and the recomputed
totals were appended to the same file (`amendments`).

The first sweep (2026-10-30) covered the seven snapshots that carried zero unresolved candidates:

| snapshot | OSV / GH / NVD records | NVD version-applicable | outcome | new candidates |
|---|---|---|---|---|
| YamlDotNet 4.3.2 | 2 / 2 / 1 | 1 | PASS_KNOWN_SWEEP | 0 |
| plug_cowboy 2.8.0 | 3 / 2 / 1 | 1 | PASS_KNOWN_SWEEP | 0 |
| gin v1.9.0 | 3 / 2 / 70 | 0 | PASS_KNOWN_SWEEP | 0 |
| phoenix 1.8.8 | 6 / 4 / 172 | 2 | PASS_KNOWN_SWEEP | 0 |
| rexml 3.4.1 | 2 / 2 / 17 | 1 | PASS_KNOWN_SWEEP | 0 |
| sinatra 4.0.1 | 4 / 4 / 15 | 1 | NEEDS_REVIEW → `PASS_KNOWN_SWEEP` | 1 (`GHSA-mr3q-g2mv-mr4q`) |
| undici 5.19.0 | 50 / 48 / 60 | 22 | NEEDS_REVIEW → `PASS_KNOWN_SWEEP` | 7 |

The tooling decisions that govern admission:

- **Product identity.** The NVD pass resolves `vendor:product` through the CPE dictionary and then
  queries by `virtualMatchString`. A CPE product must equal the package/repository token after
  normalization (language prefixes such as `golang_` are stripped). Sister products are excluded:
  `angular_cli`, `angular.js`, `angular-test-reporter`, `tomcat_native`, `apache_tomcat`.
  Keyword search is a fallback only when no CPE product resolves (dotnet/aspnetcore and
  spring-framework remain on it, and stay `NEEDS_REVIEW`).
- **Alias clustering.** Records merge when their id sets intersect; CVEs embedded in distro ids are
  extracted. Distro rollup ids never enter a cluster: single-CVE distro advisories are reduced to
  the CVE, and rollups that bundle several CVEs without naming an upstream CVE are ignored.
- **Version semantics.** Distro advisory ranges are not treated as proof that the frozen upstream
  release is affected. A CVE corroborated by an upstream OSV record, a GitHub advisory or an NVD CPE
  range becomes `needs_static_location`; a CVE seen only in a distro advisory becomes
  `needs_version_check`.

The 2026-10-31 candidates are concentrated in repositories whose migrated candidate set predated
recent advisories: curl (77), libarchive (24), grpc (22), libexpat (20), Jenkins (15), plus smaller
sets for yaml-cpp, echo, guzzle, django, symfony, tinyxml2, ecto, plug and tokio. 29 of the new
candidates are on Tomcat 9.0.98 from the NVD CPE pass (CVE-2025-31650 and later 9.0.x fixes).

PASS here means the three advisory sources yielded no uncovered version-applicable identifier; it
is not proof that the snapshot has no other vulnerability, and no dynamic reproduction was done.

## 2026-10-31 candidate resolution and location proposals

**Version resolution.** The `needs_version_check` queue was resolved against OSV
`versions`/SEMVER/ECOSYSTEM ranges and NVD 2.0 CPE configurations in two passes. Pass 1
(2026-10-30) covered the 41 repositories then in scope, 558 candidates: `unknown` 234,
`confirmed_not_affected` 199, `out_of_scope` 125, with no candidate meeting the evidence bar for
`possible_affected` (the static queue stayed at 728). Pass 2 (2026-10-31) covered the 105 openssl
candidates added by the openssl sweep: `confirmed_not_affected` 97, `unknown` 7, `out_of_scope` 1,
no status change. The NVD per-CVE API fallback was not used in either pass. Report:
`reports/RESOLUTION_REPORT_20261031.json` (`passes` and `corrections`).

The first openssl result — `unknown` for all 105 — was a tooling artifact and is withdrawn:
`version_tuple()` stripped only a hardcoded list of repository prefixes, so `openssl-3.5.8` yielded
no version tuple and `nvd_evaluate()` answered `unknown` without comparing a single CPE range.
Prefix stripping is now generic
(`^(?:R_|[A-Za-z][A-Za-z0-9]*(?:[-_][A-Za-z][A-Za-z0-9]*)*[-_]v?)(?=\d)`), covered by two
regression tests; replaying the old prefix list over all 47 frozen tags changes the tuple of
`openssl-3.5.8` only.

**Candidate state** now follows the triage decision: 1405 candidates = 1399 resolved (428
`confirmed_not_affected`, 567 `confirmed_affected`, 267 `out_of_scope`, 137 `duplicate`) + 6 open
(6 `possible_affected`). Candidate rows are never
deleted; a decision is an added triage row. The openssl sweep added 118 (13
`needs_static_location`, 105 `needs_version_check`); the 13 static candidates are the 2026-09-29
batch rows promoted below.

**Location proposals.** `propose_locations.py` processed the 698 open `needs_static_location`
candidates: 256 `located`, 32 `located_weak`, 279 `no_removed_line_match`, 131 `no_fix_commit`
(`reports/location_proposals.jsonl`). The matcher now requires the whole hunk pre-image (context +
removed lines) to occur as one contiguous block in the frozen tree, so a removed line is not
matched to an unrelated identical line elsewhere in the file. The function label is the function
whose brace/indent scope actually contains the hit, not the nearest preceding declaration.

**Promotion dry run.** `reports/PROMOTION_DRYRUN_20261031.json` (no `--apply`): 56 plan items →
48 promotable groups (45 T1 + 3 T2), 7 duplicates, 1 already present, 200 rejected — 60
`location_not_named_by_advisory`, 63 `no_promotable_code_location`, 57
`no_citing_advisory_with_version_hit`, 10 `ambiguous_shared_fix_commit`, 8
`no_advisory_cites_fix_commit`, 2 `ambiguous_hunk_match`. Promotion was held for review; 32 of the
48 groups rely on a fix commit whose advisory record does not name the file, which is the main
remaining selection risk.

**Row review (`reports/PROMOTION_REVIEW_20261031.json`).** All 48 groups were checked one by one
against the advisory text, the OSV/GHSA affected ranges and the actual fix-diff hunk. Verdicts:
**35 admit, 12 drop, 1 hold**. The admit groups were applied (`reports/PROMOTION_APPLY_20261031.json`);
the holds and relocated anchors are listed below.

- Wrong version (v4.1.1 only enters through the OSV `introduced:0` range artifact; the advisory
  prose starts at 5.3): CVE-2024-38820, CVE-2026-41846, CVE-2024-22259, CVE-2026-41851.
- Dropped and not re-anchored: CVE-2015-3192 (the hit is a JSON exception string, not the XML DTD
  fix) and CVE-2024-38808 (the hit is a comment in `OpInc`).
- Wrong location as proposed, later relocated and admitted one row at a time (see
  `relocated_rows` in the per-repo review files): CVE-2026-43514 (`DigestCredentialHandlerBase.equals`
  is only deprecated; the vulnerable comparison is `AjpProcessor.java:837`), CVE-2026-60004
  (error-message tweak in a refactor commit; the diffpatching hook install is `patch.go:130`),
  GHSA-2ffq (`secure.go:109` is the unused `req :=` removal; the HSTS change is at 121),
  GHSA-h9g5 (`context.go` Scheme fix belongs to 2ffq; the JSONP fix is `jsonPBlob`),
  GHSA-9c5c (the fix deletes the whole vendored `fastify-middie.ts`; the bypass is decided where
  `run()` copies the raw request target into `holder.url`).
- Withdrawn advisory: CVE-2024-51999 / GHSA-pj86 (withdrawn 2025-12-02 as a correctness bug).
- Hold: CVE-2025-46701 (CGI case-sensitivity; same commit and file, but the anchor is the caller
  branch in `setCGIEnvironment` — relocated to `findCGI` and admitted).

## 2026-10-31 promotion (repository by repository)

After the row review, promotion ran per repository. The dataset now holds **721 positives**: 165
carried from the v0.3.1 migration and 556 added on 2026-10-31, in fifty-nine groups:

- **35 batch-applied** from the reviewed 48-group dry run (`reports/PROMOTION_APPLY_20261031.json`;
  Tomcat 10, Gitea 5, Jenkins 4, Angular 3, Spring 2, Laravel 2, ImageSharp 2, Echo 2, plus one
  each for axios, vite, protobuf, plug and nest).
- **59 applied per repository** with a row-level review file: `reports/PROMOTION_REVIEW_20261031_<REPO>.json`
  (20 files, 34 admits and 25 further relocated anchors; held rows were relocated and applied with
  `promote_candidate.py` rather than the batch gate).
- **1 recorded in the aggregate review** (`reports/PROMOTION_REVIEW_20261031.json`, relocated
  CVE-2025-46701).
- **15 spring-framework rows** promoted 2026-10-31 from the 46 open `possible_affected` candidates
  at v4.1.1.RELEASE (`reports/PROMOTION_REVIEW_20261031_SPRING_BATCH1.json`, 12 rows;
  `reports/PROMOTION_REVIEW_20261031_SPRING_BATCH2.json`, 3 rows): CVE-2015-0201, 2015-3192,
  2018-1271, 2018-1272, 2022-22950, 2022-22965, 2024-22243, 2024-22259, 2024-22262, 2024-38808,
  2025-22233, 2026-41845, 41846, 41848 and 47884. Every anchor is a line the cited fix removes,
  present verbatim at the frozen tag, with the marker absent from the frozen Java scope and
  present among the patch's added lines. Two rows need the class body as the enclosing scope for a
  static field (SockJsUrlInfo's id generator, UriComponentsBuilder's URL split patterns);
  CVE-2018-1272's fix edits `MimeTypeUtils.RND`, so `patch_file` is not the anchor file — at
  4.1.1 the same boundary defect is `FormHttpMessageConverter.java:104`
  `private final Random random = new Random();`, and the boundary generator only moved to
  MimeTypeUtils in 4.3. The other 31 open rows are decided in
  `reports/TRIAGE_REVIEW_20261031_SPRING_OPEN.json`: 14 `confirmed_not_affected` — 13 on
  component absence (STOMP selector registry, ETag parsing, functional routers / Kotlin DSL,
  WebFlux web sessions and multipart, EncodedResourceResolver, SimpleEvaluationContext, the
  WebSocket session id generator, and the Locale-dependent `toLowerCase` precondition of
  CVE-2024-38820) plus CVE-2016-5007 by fix-version equality (the vendor fix version for the 4.1
  line is 4.1.1.RELEASE itself, and the snapshot is that tag with the `trimTokens` API present).
  17 stay `possible_affected` because the vulnerable construct exists but no verbatim pre-image
  can be anchored (additive fixes, a local rename, or an advisory that cites no commit).
- **14 spring-framework rows** settled 2026-10-31 at `4.1.1.RELEASE`
  (`reports/SWEEP_20261031_SPRING.json`), on top of the 18 rows already in GT at this snapshot:
  every one of the 17 candidates that TRIAGE_REVIEW_20261031_SPRING_OPEN had left open was
  re-reviewed against the vendor page, the OSV record and the published fix hunk, and 14 are
  promoted. The anchors are the pre-images of those hunks in the frozen tree: the HTTP invoker
  `ObjectInputStream` (`HttpInvokerServiceExporter.readRemoteInvocation:112-121`), the unfiltered
  property-descriptor cache (`CachedIntrospectionResults:289-303`), the unguarded STOMP CONNECT
  branch (`SimpleBrokerMessageHandler:156-166`), the per-evaluation `Pattern.compile`
  (`OperatorMatches:67`), the unbounded expression tokenizer (`InternalSpelExpressionParser:118`),
  the stateless STOMP client handler (`StompSubProtocolHandler:184-231`), `isReadable()` without
  `exists()` (`FileSystemResource:105-107`), the path-only static-resource cache key
  (`CachingResourceResolver:64`), `StringUtils.delete` version removal
  (`AbstractVersionStrategy:114-116`), the version-stripped path resolved without
  `shouldIgnoreInputPath` (`VersionResourceResolver:151-156`), the default view name without a
  `redirect:`/`forward:` rejection (`DefaultRequestToViewNameTranslator:175-178`), the uncounted
  operator dispatch (`ExpressionState.operate:189-200`), the non-quote-aware parameter split
  (`MimeTypeUtils.parseMimeType:205-241`) and the attacker-controlled JMS type id
  (`MappingJackson2MessageConverter.getJavaTypeForMessage:362-377`); the first of these is
  `source_review` because 6.0.0 removes the exporter rather than patching the sink. Two are
  closed `confirmed_not_affected`: CVE-2020-5421's `jsessionid` bypass needs the CVE-2015-5211
  RFD check that 4.1.1 does not have and `UrlPathHelper` already strips `;` in both
  `removeSemicolonContent` branches, and CVE-2026-41851's unbounded cache is the SpEL pattern
  cache introduced in 5.2.23, absent at 4.1.1. CVE-2026-41849 stays open: its vendor range
  (`5.3.48 and earlier`) covers the snapshot but the only fix is 5.3.49 Enterprise, so the
  CWE-190 overflow site has no public hunk to anchor.
- **26 apache/tomcat rows** promoted 2026-10-31 at the frozen 9.0.98 tag
  (`reports/PROMOTION_REVIEW_20261031_TOMCAT.json`, 23 rows;
  `reports/PROMOTION_REVIEW_20261031_TOMCAT_BATCH2.json`, 3 rows). The candidate set came from the
  9.0.x fix commits named on the vendor security-9 page for every CVE whose "Affects" range
  contains 9.0.98: CVE-2025-31650, 2025-48989, 2025-49124, 2025-52434, 2025-53506, 2025-61795,
  2026-24880, 2026-25854, 2026-29146, 2026-34483, 2026-34487, 2026-41293, 2026-43512, 2026-50229,
  2026-53404, 2026-53434, 2026-55276, 2026-55955, 2026-55956, 2026-65183, 2026-65905, 2026-65927,
  2026-66422, 2026-68569, 2026-68763 and 2026-73180. Every anchor is a line the cited 9.0.x fix
  removes, present verbatim at 9.0.98, with the marker absent from the frozen Java scope and
  present in the patch. Three rows need a scope the shared resolver misses: the two package-private
  methods (`HpackDecoder.decode`, `Http2UpgradeHandler.reserveWindowSize`) and the
  `Http2UpgradeHandler` constructor are found by a stricter declaration matcher, because the
  package-private methods have no access modifier and the constructor is where the initial HTTP/2
  settings are installed. Two rows are functionless: the Windows installer script
  (`res/install-win/tomcat.nsi`, unqualified `icacls.exe`) and the number guess JSP example
  (`webapps/examples/jsp/num/numguess.jsp`, wildcard `jsp:setProperty` binding). CVE-2026-65905 is a
  pure statement reorder, so its marker spans the hunk's post-image (a context `count++;` followed
  by the re-added slot clear); CVE-2026-34487 drops the `headers` argument from a wrapped log call,
  so its marker is the two-line post-image that no longer contains `headers,`. The other 12 open
  rows were first left open by `reports/TRIAGE_REVIEW_20261031_TOMCAT_OPEN.json` (all 12 inside the
  vendor range and none able to pass the fix-diff gate) and are settled by the follow-up sweep
  below.
- **9 apache/tomcat rows, 2 closures, 1 open** settled 2026-10-31 at 9.0.98
  (`reports/SWEEP_20261031_TOMCAT_OPEN.json`, 9 promotions + 3 triage rows). The 12 candidates the
  triage pass had left open were re-read against the frozen tag, and nine are promoted with
  `evidence_type=fix_diff_comparison` on the line the fix inserts beside or the block it rewrites:
  the HTTP/0.9 branch that sets `keepAlive=false` without a method check
  (`Http11Processor.prepareRequestProtocol:609-612`, CVE-2026-24733), the Host header parsed
  without any SNI comparison (`Http11Processor.prepareRequest:788-789`, CVE-2025-66614), the
  case-sensitive lock-out key (`LockOutRealm.isLocked:207-210`, CVE-2026-43513), the unbounded
  WebDAV body read (`WebdavServlet.doPropfind:835-839`, CVE-2026-41284), the GSSAPI-authenticated
  `bindAsUser` credential check (`JNDIRealm.bindAsUser:1839-1848`, CVE-2026-55957), the unbounded
  chat-example backlog (`ChatAnnotation.sendMessage:96-101`, CVE-2026-66299), and three OCSP
  defects in the FFM/panama engine that share `OpenSSLEngine.processOCSPRequest`: an accepted
  OCSP single response with no nonce, signature or freshness check (:1352-1362, CVE-2026-24734), a
  TRY_LATER response that returns UNKNOWN without setting the store-context error (:1352-1380,
  CVE-2026-29145) and OCSP request failures that do the same (:1306-1341, CVE-2026-34500). For the
  seven additive fixes the anchor is the pre-existing line the inserted guard, lowercasing or
  limit protects; 24734 and 41284 anchor on the block the fix rewrites. CVE-2026-59083 is
  `confirmed_not_affected` — the `URLDecoder` call it fixes exists only since the 9.0.103 rewrite
  refactor, and the 9.0.98 valve never decodes the rewritten path. CVE-2026-59084 is `out_of_scope`
  — a documentation-only change, with the code weakness tracked as CVE-2026-29146 (already GT).
  CVE-2025-55752 is `confirmed_not_affected` on the same reading
  (`reports/TRIAGE_20261031_TOMCAT_VITE.json`): the fix b5042622 reverses decode-before-normalize
  in the encode-space rewrite that ee3ab548 introduced in 9.0.103, while 9.0.98 (and 9.0.102)
  rewrite in decoded space, normalize the decoded string at `RewriteValve.java:495` and never call
  `URLDecoder`. The vendor's `Affects: 9.0.0.M11 to 9.0.108` is broader than its own statement
  that "the fix for bug 60013 introduced a regression".
- **openssl/openssl: the 7 remaining `unknown` rows closed** 2026-10-31 at openssl-3.5.8
  (`reports/TRIAGE_REVIEW_20261031_OPENSSL_OPEN.json`, 3 `confirmed_not_affected` + 4
  `out_of_scope`; openssl now has no open candidate). They had stayed `unknown` because their
  advisories carry no range the resolver can map onto `openssl/openssl`. CVE-2025-9230 (CMS RFC
  3211 KEK unwrap) is fixed in 3.5.4 per the 20250930 vendor advisory, so 3.5.8 is past it;
  CVE-2025-27587 (Minerva) covers "OpenSSL 3.0.0 through 3.3.2 on the PowerPC architecture";
  CVE-2024-2408 is PHP's Marvin exposure, and the advisory's own condition — an OpenSSL with
  `rsa_pkcs1_implicit_rejection` from PR #13817, "part of OpenSSL 3.2" — holds at 3.5.8, where
  `RSA_PKEY_CTX.implicit_rejection` defaults to 1 (`crypto/rsa/rsa_pmeth.c:77`) and
  `ossl_rsa_padding_check_PKCS1_type_2` returns a deterministic random message instead of an
  error (`crypto/rsa/rsa_pk1.c:376-388`). The four `out_of_scope` rows name another product and no
  OpenSSL component: CVE-2015-7575 (Mozilla NSS; the frozen tree's only MD5 sigalg is the legacy
  `rsa_pkcs1_md5_sha1` fallback with 67 security bits, below the default level's 80, so
  `tls12_sigalg_allowed` rejects it), CVE-2022-40735 (the Diffie-Hellman protocol project),
  CVE-2025-66109 (WooCommerce Cart Weight plugin) and CVE-2026-22799 (emlog).
- **2 laravel/framework rows, 2 closures** settled 2026-10-31 at v11.30.0
  (`reports/SWEEP_20261031_LARAVEL_OPEN.json`, 2 promotions + 2 triage rows). The four open
  candidates all sat inside a published range that nominally contains v11.30.0. CVE-2024-13918 and
  CVE-2024-13919 are the same 11.36.0 fix 45287fb2 (`Escape data`, PR #53869) applied to the two
  raw Blade echoes of the debug exceptions page: the request-body echo at
  `src/Illuminate/Foundation/resources/exceptions/renderer/components/context.blade.php:54`
  (`{!! $exception->requestBody() !!}`; the producer JSON-encodes `Request::all()` after stripping
  every backslash, `Exception::requestBody` at `Renderer/Exception.php:155-164`) and the
  route-parameter echo at the same file's line 108 (`{!! $routeParametersContext !!}`; producer
  `applicationRouteParametersContext` at `Exception.php:189-197`). Both only render with
  `APP_DEBUG=true` (`Handler::renderExceptionContent` at `Handler.php:841`). The other two are
  `confirmed_not_affected` on frozen-source evidence: CVE-2026-102279's fix b495ca2 splits
  `allowHTML` out of the renderer's `tippy()` call and renames `formatted-source.blade.php` to
  `data-tippy-html-content`, but v11.30.0 has no such component, no `allowHTML` option and ships
  `allowHTML:!1` in `dist/scripts.js`, its only tippy targets being Blade-escaped header and route
  names; CVE-2026-114508's 12.x range starts at 12.45.0, predating the JSON:API resources —
  v11.30.0 has no `src/Illuminate/Http/Resources/JsonApi` directory at all.
- **elixir-ecto/ecto: 4 open candidates closed** 2026-10-31 at v2.2.0
  (`reports/TRIAGE_REVIEW_20261031_ECTO_OPEN.json`, 1 `duplicate` + 3 `out_of_scope`; no
  promotion). GHSA-4r2f-6fm9-2qgh is a GitHub-withdrawn duplicate of GHSA-2xxx-fhc8-9qvq /
  CVE-2017-20166, which is already a Ground Truth row on this snapshot
  (`lib/ecto/repo/queryable.ex:351-352`). The other three advisories were filed under the ecto
  repository but name package `postgrex`: CVE-2026-32687 (`Postgrex.Notifications.listen/3`),
  CVE-2026-58225 (reconnect `DO` dollar-quote) and CVE-2026-66838 (`Postgrex.stream/4 :comment`).
  The frozen ecto tree has no `Notifications` code and only forwards to `Postgrex.stream`
  without ever setting `:comment` (`lib/ecto/adapters/postgres/connection.ex:112-113`), and its
  optional postgrex requirement is `~> 0.13.0` (`mix.exs:47`), below every affected range
  (>= 0.16.0 or >= 0.19.3).
- **1 elixir-plug/plug row, 2 duplicates, 1 closure** settled 2026-10-31 at v1.19.2
  (`reports/SWEEP_20261031_PLUG_OPEN.json`, 1 promotion + 3 triage rows). CVE-2026-56814 is
  promoted at `lib/plug/parsers/multipart.ex:189-219` (`parse_multipart_headers`, function
  granularity): the cumulative `:length` budget is charged for part bodies only, the parsed part
  headers are never deducted (no `headers_size/2`) and the `:skip` branch at :217-218 returns
  without reading the skipped body, so a request of many header-only file parts costs nothing
  against the limit while each part opens a temp file and retains a `Plug.Upload`; fix
  0ee8afcc/56edca2c adds the header charge and `parse_multipart_skip`. The GHSA-95qv copy of that
  advisory and the GHSA-wpmj copy of CVE-2026-56813 (already GT at
  `lib/plug/conn/cookies.ex:72-80`) are `duplicate`. CVE-2018-1000883 is `confirmed_not_affected`:
  all published ranges end at plug 1.1.9/1.2.5/1.3.5 and the frozen tree already validates every
  `Set-Cookie` value in `verify_cookie!` -> `validate_header_key_value!`
  (`lib/plug/conn.ex:1946-1948`).
- **1 django/django row, 3 closures** settled 2026-10-31 at the frozen 4.2.13 tag
  (`reports/SWEEP_20261031_DJANGO_OPEN.json`, 1 promotion + 3 triage rows). CVE-2026-15337 is
  promoted at `django/utils/translation/trans_real.py:462-479` (`check_for_language`, function
  granularity): the function itself carries `@functools.lru_cache(maxsize=1000)` and its only
  pre-filter is `language_code_re`, which accepts arbitrarily long hyphenated codes;
  `set_language()` (`django/views/i18n.py:47-48`) passes the raw POST value straight in, so many
  distinct oversized codes are retained as cache keys, and no `LANGUAGE_CODE_MAX_LENGTH` guard
  exists anywhere in the 4.2.13 tree; fix c72a5dbb/27137e65 moves the cache behind a 500-character
  gate (T2, NVD CVSS 3.1 5.3; NVD also publishes CVSS 4.0 6.9). The two 2024 urlize candidates are
  `confirmed_not_affected` on frozen-source evidence: both fixes edit the `CountsDict`/amp/semicolon
  `trim_punctuation` that shipped in 4.2.14 (`d0a82e26` released in 4.2.15, `d147a8eb` in 4.2.16),
  while 4.2.13 still has the earlier per-pass `html.unescape` implementation
  (`django/utils/html.py:333-367`), so the patched code is absent at this tag; the urlize DoS
  actually present at 4.2.13 is CVE-2024-38875, already GT. CVE-2026-53878 is
  `confirmed_not_affected` because the whole `DomainNameValidator` class is missing from the
  4.2.13 tree and NVD's range starts at 5.2.
- **2 symfony/symfony rows, 2 closures** settled 2026-10-31 at the frozen v5.4.45 tag
  (`reports/SWEEP_20261031_SYMFONY_OPEN.json`, 2 promotions + 2 triage rows). CVE-2026-24739 is
  promoted at `src/Symfony/Component/Process/Process.php:1630-1647` (`Process::escapeArgument`,
  function granularity): the Windows branch returns an argument unquoted when it does not match
  `/[\/()%!^"<>&|\s]/`, whose class omits `=` and the other MSYS2-special characters, so under
  Git Bash the MSYS2 conversion rewrites the value before a native child receives it; the fix
  ec154f6f/35203939050 adds those characters (5.4.51, T1, GHSA CVSS 3.1 6.3). CVE-2026-45070 is
  promoted at `src/Symfony/Component/Mime/Header/ParameterizedHeader.php:57-60` (`setParameters`):
  parameter names are stored and emitted verbatim while only values are checked against
  `TOKEN_REGEX`, so a caller-supplied name can inject headers; 8cc149f5/1503ceb900 adds the
  per-name token check (T1, NVD CVSS 3.1 6.5). The GHSA's fixed version 5.4.52 is stale:
  v5.4.52's file is byte-identical to v5.4.45, and the check first ships in 5.4.55 (as
  FriendsOfPHP `symfony/mime/CVE-2026-45070.yaml` records). CVE-2024-36611 is
  `confirmed_not_affected`: GHSA-7q22 is withdrawn, NVD records that the supplier concluded it is
  a false report and publishes no CPE at all, and the frozen `FormLoginAuthenticator` passes empty
  credentials to the user provider/password check rather than bypassing authentication.
  CVE-2025-68129 is `out_of_scope`: it names Auth0-PHP and Auth0/symfony (CPE `auth0:symfony`
  5.0.0 to <5.6.0), and the frozen monorepo has no auth0 dependency or code.
- **1 dotnet/aspnetcore row, 2 closures** settled 2026-10-31 at the frozen v8.0.13 snapshot
  (`reports/SWEEP_20261031_ASPNETCORE_OPEN.json`, 1 promotion + 2 triage rows). CVE-2026-42899 is
  promoted at `src/Components/Endpoints/src/FormMapping/FormDataReader.cs:124-165`
  (`ProcessFormKeys`, function granularity): `endIndex` is computed as `IndexOf(']') + startIndex`
  and only then tested for the `-1` sentinel, so a key such as `customer[0` (the `[` is not at
  index 0 and nothing closes it) yields `endIndex == startIndex - 1`, slices an empty segment and
  resumes at `endIndex + 1 == startIndex`, where the `[` search finds the same bracket again —
  `startIndex` never advances and the `while` loop spins on the request thread with no allocation
  (CWE-835, unauthenticated form POST → remote DoS). The 8.0.27 fix ab7d766648 (public backport
  #66674, merge b48ed8d3) deletes `ProcessFormKeys` and rewrites `GetKeys()` to skip a key with no
  closing `]`; the same patch touches `RequestDelegateFactory` and `HttpContextFormValueMapper`,
  which shows the form-binding paths that reach it. T1/`vendor_official`, GHSA CVSS 3.1 7.5. The
  earlier aspnetcore pass had left this candidate open on the reading that the 8.0.27 range
  contained no attacker-controlled loop; the servicing compare `v8.0.26...v8.0.27` shows the
  opposite, and the row supersedes that note. CVE-2026-45591 and CVE-2026-92707 are `out_of_scope`:
  both fixes in this repository are MessagePack dependency updates (2.5.187 → 2.5.301 in 8.0.28 via
  `dc6799d732`, with the fix applied as a patch to the MessagePack-CSharp submodule; 2.5.303 in
  8.0.32 via `21f2be26fd`), and the vulnerable deserializer (nested-array recursion, and
  `PrimitiveObjectFormatter` array allocation) lives in `aspnet/MessagePack-CSharp`, whose
  submodule directory is empty in the frozen checkout.
- **2 protocolbuffers/protobuf rows, 1 closure** settled 2026-10-31 at the frozen v3.25.4 snapshot
  (`reports/SWEEP_20261031_PROTOBUF_OPEN.json`, 2 promotions + 1 triage row). The tag peels to
  e915ce24, which is also tagged v4.25.4, and `version.json` records protobuf-python 4.25.4, so
  both pip ranges below contain the frozen python. CVE-2025-4565 is promoted at
  `python/google/protobuf/internal/decoder.py:661-708` (`MessageDecoder`, function granularity):
  the closures `DecodeRepeatedField` (:671) and `DecodeField` (:693) call
  `value._InternalParse(buffer, pos, new_pos)` with no depth argument (:682, :703), and
  `InternalParse` (`python_message.py:1139`) calls every field decoder without one (:1164, :1198),
  so nested messages, recursive groups and SGROUP chains in the unknown-field path
  (`_DecodeUnknownFieldSet`/`_DecodeUnknownField`, :945/:962 via `InternalParse:1182`) recurse
  until CPython raises `RecursionError` — a remote DoS for any parser running the pure-Python
  backend (CWE-674). The 25.x backport d31100c9 ("Manually backport recursion limit enforcement to
  25.x", shipped as 4.25.8, three commits before the v4.25.8 tag) adds
  `DEFAULT_RECURSION_LIMIT = 100`, `SetRecursionLimit`, and `current_depth` threading through
  `InternalParse` and the decoder closures (main fix 17838b, "Add recursion depth limits to pure
  python"); its tests add `self_recursive.proto` and `TestRecursiveGroup` (100 levels parse, 300
  raise "too many levels of nesting") plus `test_decode_unknown_group_field_too_many_levels`.
  CVE-2026-0994 is promoted at `python/google/protobuf/json_format.py:626-656`
  (`_ConvertAnyMessage`): `ConvertMessage` (:463) is the only place that increments
  `self.recursion_depth` and enforces `max_recursion_depth` (:474-477, `ParseDict` default 100 at
  :396), but an Any payload whose `@type` is a well-known type goes through
  `methodcaller(_WKTJSONMETHODS[full_name][1], ...)(self)` (:646-649) instead, so that level is
  never counted and nested Any messages bypass the guard and exhaust the stack. The fix d2b00162
  (PR #25239, issue #25070) routes the branch through `self.ConvertMessage(...)`; the 5.x backport
  is 5ebddcb1, patched in 5.29.6 (range `< 5.29.6` and 6.30.0rc1–6.33.4, fixed 6.33.5). Both rows
  are T1/`vendor_official`; severity is the NVD CVSS 3.1 score (5.3 MEDIUM for 4565, 7.5 HIGH for
  0994 — the Google CNA CVSS 4.0 score of 8.2 is recorded as a note only). GHSA-7gcm-g887-7qv7 has
  no repository advisory endpoint (404); the global GHSA page is cited instead. The third open
  candidate `disc2_c3eea2547f050f3cd7fe6da4` is a `duplicate` of the 4565 row — same advisory, same
  fix commit, same package; its Java `GHSA-735f` alias is CVE-2024-7254, already GT on this
  snapshot.
- **2 netty/netty closures, 0 promotions** settled 2026-10-31 at the frozen 4.1.137.Final release
  commit (`reports/SWEEP_20261031_NETTY_OPEN.json`, 2 triage rows). Both advisories were published
  2026-08-07, list `<= 4.1.136.Final` as vulnerable and 4.1.137.Final as patched, and the frozen
  snapshot is exactly that release, so both candidates are `confirmed_not_affected` with the fix
  read in place. GHSA-cc6x-ffm5-83wf (SOCKS4/5 encoder null bytes, CWE-626): `Socks4ClientEncoder`
  now passes `userId`/`dstAddr` through `sanitize` (:50-57, :61-70), which throws `EncoderException`
  when `AsciiString.c2b(c) == 0`, and `Socks5ClientEncoder` routes every field length through
  `writeFieldLength`/`checkFieldLength` 0..255 (:114, :120-129) instead of a `ByteBuf.writeByte`
  that truncated longer fields. The advisory's SOCKS5 "null byte / CRLF" part concerns
  length-prefixed RFC 1928/1929 fields and is not patched in 4.1.139 or 4.2.17 either, which
  matches a fix aimed at the SOCKS4 terminator and the SOCKS5 length bounds. GHSA-p85m-gvr3-788c
  (missing hostname verification on the OpenSSL client path when trust-manager wrapping is
  unavailable, CWE-297): `ReferenceCountedOpenSslClientContext` now fails closed — if
  `endpointIdentificationAlgorithm` is set and the chosen manager is not an
  `X509ExtendedTrustManager` (the no-`Unsafe` Java 25+ case, where
  `OpenSslX509TrustManagerWrapper` keeps its pass-through `DEFAULT`), context creation throws
  `UnsupportedOperationException` (:181-187); `useExtendedTrustManager` is the
  `javaVersion() >= 7 && instanceof X509ExtendedTrustManager` test at
  `ReferenceCountedOpenSslContext.java:791-793`. Both hunks come from 9e05192391 ("Merge changes
  from forks (#17213) (#17217)") and are absent from netty-4.1.136.Final. The guard is evaluated at
  context creation; a later `engine.setSSLParameters` reaches `configureEndpointVerification`
  (`ReferenceCountedOpenSslEngine.java:2250-2266`), which only sets `SSL_CVERIFY_REQUIRED`.
- **1 PHPMailer/PHPMailer row, 1 closure** settled 2026-10-31 at the frozen v6.1.5 snapshot
  (`reports/SWEEP_20261031_PHPMAILER_OPEN.json`, 1 promotion + 1 duplicate). CVE-2021-34551 is
  promoted at `src/PHPMailer.php:2078-2143` (`setLanguage`, function granularity): `$lang_file` is
  assembled from the caller-supplied `$lang_path` (:2128) and executed with
  `$foundlang = include $lang_file;` (:2137), while the only guard is
  `isPermittedPath` (:1745-1748) = `!preg_match('#^[a-z]+://#i', $path)`. A Windows UNC path
  (`\\attacker\share\`) carries no URI scheme, so it passes; `file_exists()` (:2132) issues the SMB
  request and the remote `phpmailer.lang-xx.php` is then included as PHP — RCE on Windows when the
  application passes untrusted data as `$lang_path`, plus NTLM credential disclosure to that
  share. `$langcode` is itself restricted by `/^[a-z]{2}(?:_[a-zA-Z]{2})?$/` (:2124), so only the
  directory component is attacker-defined. The 6.5.0 fix `acd264bf` ("Merge branch
  'CVE-2021-34551'", 2021-06-16) adds "Do not set this from user input!" to the docblock and
  replaces the include with `file()` plus a per-line regex that copies only
  `$PHPMAILER_LANG['key'] = "…";` assignments for keys already in the built-in table, so language
  files are parsed as text; the commit is an ancestor of tag v6.5.0 (compare: ahead_by 4). Severity
  is the NVD Primary CVSS 3.1 8.1 HIGH (CWE-434) with the same vector as the GitHub global
  advisory; the maintainers' repository advisory scored the same GHSA 5.5 MEDIUM (PR:H) on the
  assumption that the attacker already controls an application setting, recorded as a note.
  `disc2_73fd935199dc7d92bafd4ded` (FriendsOfPHP yaml, aliases BIT-phpmailer-2021-34551 /
  CVE-2021-34551 / GHSA-7q44-r25x-wm4q) is a `duplicate` of that row.
- **1 leethomason/tinyxml2 row, 1 closure** settled 2026-10-31 at the frozen 10.0.0 snapshot
  (`reports/SWEEP_20261031_TINYXML2_OPEN.json`, 1 promotion + 1 duplicate). CVE-2024-50614 is
  promoted at `tinyxml2.cpp:475-568` (`GetCharacterRef`, function granularity):
  `XMLUtil::GetCharacterRef` parses numeric character references with no digit-count limit —
  `ucs += mult * digit; mult *= 16;` (:521-525 hex, :551-559 decimal) — and relies on the debug
  assertions `mult <= UINT_MAX / digit` (:520), `ucs <= ULONG_MAX - digitScaled` (:522) and
  `mult <= UINT_MAX / 16` (:524) with decimal mirrors at (:550, :552, :558). `TIXMLASSERT` expands
  to `assert` only under `TINYXML2_DEBUG` (`tinyxml2.h:79-93`; `meson.build:40-42` for debug
  builds, `CMakeLists.txt:31` for the Debug config) and to a no-op otherwise, so an
  assertion-enabled build aborts once `mult` passes UINT_MAX/16 = 268435455 — after eight hex
  digits (`&#xffffffff;`) or ten decimal digits. The path is reachable from any attribute or text
  through `StrPair::GetStr` (:322-344), which calls `GetCharacterRef` for every `&#` entity when
  entity processing is on (the default). The 10.1.0 fix `494735de` ("fix the potential overflow in
  char refs", 2024-12-05; merge `4cbb2515`, PR #1009) switches to `uint32_t`, defines
  `MAX_CODE_POINT = 0x10FFFF`, returns 0 as soon as `ucs > MAX_CODE_POINT`, deletes the overflow
  assertions and adds the trigger inputs to `xmltest.cpp`; the maintainer confirmed "Should be
  fixed" on issue #996 on 2026-05-24. In release builds the unsigned wrap is defined and
  `ConvertUTF32ToUTF8` returns length 0 for input >= 0x200000 (:440-443), recorded as a static fact
  rather than a second impact; severity is the only published CVSS (Secondary CNA 6.5 MEDIUM,
  `AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`, matching GHSA-xpm9-95h9-q996), tier T2 / review status
  `unknown`. `sweep_f978923aeaa98920` is the second candidate for the same CVE and is a
  `duplicate`.
- **26 jenkinsci/jenkins rows** promoted 2026-10-31 at the frozen 2.441 tag
  (`reports/PROMOTION_REVIEW_20261031_JENKINS_BATCH1.json`, 18 rows; `_BATCH2.json`, 1 row;
  `_BATCH3.json`, 7 rows). The candidate set is the 33 CVEs whose vendor range contains 2.441.
  OSV's GIT ranges for Jenkins cite `[maven-release-plugin] prepare release` commits, which are
  not the fixes, and the advisory page only links `jenkinsci-cert/SECURITY-xxxx` issues, so the
  real fix commits were located with the GitHub commit search API
  (`q=SECURITY-xxxx+repo:jenkinsci/jenkins`); 32 of 33 CVEs resolved to a SECURITY commit,
  CVE-2025-67636 reusing SECURITY-783. Each row passes the same three checks: the pre-image
  line exists verbatim at 2.441, the fix marker is absent from the frozen scope, and the marker
  is present in the fetched fix patch. Nine anchors are statements the fix rewrites (for example
  the `BuildAuthorizationToken.token` field becoming a `Secret`, the `Item` class declaration
  gaining `StaplerProxy`, the ISO-8859-1 URI normalization in `Util.isSafeToRedirectTo`), the
  rest are the frozen statement an inserted guard now protects (agent copy, queue cancellation,
  time-zone dropdown, node replacement, log-record escaping, session fixation, and so on). Two
  scopes needed local handling: class-level fields/annotations use the type declaration as the
  enclosing scope (`BuildAuthorizationToken`, `User`), and `Nodes.replaceNode` performs its write
  inside an anonymous `Runnable`, so the row names the outer method. The remaining 7 CVE rows are
  decided in `reports/TRIAGE_REVIEW_20261031_JENKINS_OPEN.json`: six stay `possible_affected`
  because the fix is purely additive or outside this repository (CVE-2024-43044's `fetchJar` is
  in Remoting, CVE-2025-59476 is a Winstone/support-log-formatter bump, CVE-2026-84655 is a
  test-only core commit, CVE-2026-70427 edits code that postdates 2.441, CVE-2025-59475's
  `jumplist.jelly` does not exist at the tag, CVE-2025-67639's CSRF check is a new method), and
  CVE-2026-33002 is `confirmed_not_affected` because the vendor range starts at 2.442 and 2.441
  has no WebSocket Origin handling at all.
- **6 vercel/next.js rows** promoted 2026-10-31 at the frozen v14.2.24 tag
  (`reports/PROMOTION_REVIEW_20261031_NEXTJS_BATCH1.json`, 4 rows; `_BATCH2.json`, 2 rows). The
  OSV GIT ranges again name release commits (`v14.2.31` 55f7662, `v14.2.32` f30d815, `v15.5.16`
  ad6fd4e), whose patches only bump package versions, so each row cites a code-level commit found
  in or beside the same range: 6b12c60 (CVE-2025-55173 and -57752, the `headers: _req.headers,`
  line in `fetchInternalImage`; the marker is the two-line post-image `method`/`socket` that
  becomes adjacent once the header is deleted), 9c9aaed5 (CVE-2025-57822,
  `resHeaders['location'] = rel` in `getResolveRoutes`, marker `allowedStatusCodes`), 3a15b4ac
  (GHSA-2xp9, `VALID_BLUR_EXT` no longer listing `avif`; a module-level constant, promoted
  functionless with the whole file as scope), 73b94872 (CVE-2026-64648, the
  `isRequestInput && init` merge in `createPatchedFetcher`) and e3e5666c (CVE-2026-64649, the
  `createForwardedActionResponse` origin built from `host.value`). TypeScript scopes needed a
  local resolver: `propose_locations` returns no function for multi-line
  `export async function` signatures and mistakes the destructured parameter brace for the end of
  the declarator, so the helper finds the body brace at paren depth zero and steps outward to the
  named function. The remaining Next.js candidates were settled by the follow-up sweep
  (`reports/SWEEP_20261031_NEXTJS.json`): the rows that sweep touched carry NVD CVSS 3.1 scores
  and `github_reviewed` review status (14 rows added, the 8 earlier rows rewritten; the two
  pre-sweep migration rows CVE-2025-29927 and GHSA-2xp9-vwfh-vxw4 keep `vendor_official`), and the
  rest were closed or left open as described in the next bullets. The snapshot now holds 25
  positives.
- **14 new vercel/next.js rows, 18 closures, 5 open** settled 2026-10-31 at v14.2.24
  (`reports/SWEEP_20261031_NEXTJS.json`, 22 promotions + 23 triage rows). The new anchors are the
  i18n data-route middleware bypass (CVE-2026-44573), the INTERNAL_HEADERS omissions (44572), the
  script-tag JSON escaping (44580), the CSP nonce quote (44581), the WebSocket upgrade SSRF
  (44578), the two image-response buffer limits (44577, 59471), rewrite hostname validation
  (64645), the edge action body limit (64646), the file-system cache path join (75604), the dev
  origin check (48068), the vendored flight-decoder pin (55184), the truncated cache-busting hash
  (44582), the loose RSC header check (44576), the image header pass-through (55173/57752), the
  non-3xx Location SSRF (57822), the unbounded image disk cache (27980), the unvalidated server
  reference lookup (64643), the lossy TextDecoder cache key (64647), the Request-as-RequestInit
  key (64648) and the Host-derived action origin (64649). Six candidates are duplicates that
  reduce to the same vendored flight-decoder row (CVE-2025-67779 with its GHSA twin, plus the
  mwv6/h25m/8h8q/q4gf aliases); two are out of scope (CVE-2026-96889 sharp/libvips, CVE-2026-29057
  http-proxy 1.18.1); one maps to the existing GHSA-2xp9 row; nine are not affected per the OSV
  ranges (fixed before v14.2.24 or introduced after it); and four stay `possible_affected`
  (CVE-2026-23869/23870 with the same decoder question, CVE-2026-64641 and CVE-2026-94482).
  CVE-2026-23864 was promoted after the decoder review described in the next bullet.
- **CVE-2026-23864 promoted at next.js v14.2.24** after the decoder-level review that the sweep
  deferred (`reports/PROMOTION_20261031_NEXTJS_23864.json`). The anchor is
  `packages/next/src/compiled/react-server-dom-webpack/cjs/react-server-dom-webpack-server.node.development.js:3620-3656`
  (`decodeAction`), `evidence_type=source_review`, T1/`github_reviewed`, CWE-770, CVSS 3.1 7.5 as
  published. `action-handler.ts:574` hands the attacker-controlled multipart `FormData` to the
  vendored 18.3.0-canary-178c267a4e-20241218 decoder (pin at
  `compiled/react-server-dom-webpack/package.json:50-51`); `decodeAction` re-runs
  `decodeBoundActionMetaData` (`:3603-3618`) for every duplicate `$ACTION_REF_` field with no
  recorded set, and `parseModelString` case `'K'` (`:3412-3429`) walks the whole backing
  `FormData` per reference, so N duplicated fields cost O(N^2) work. The 19.0.4 hardening
  (`seenActions`, `MAX_BOUND_ARGS`, array limits) is absent from both the development and the
  production bundle; the 15.0.8 fix is the pin sync `99b4501` to react
  `19.0.0-rc-4cd8f914-20260126`, i.e. React commit `de58cca00cf0`. The advisory lists no 14.x
  patch, so the row is `source_review` rather than a 14.x fix-diff comparison. CVE-2026-23869 and
  CVE-2026-23870 stay `possible_affected`: their 19.0.5/19.0.6 fixes harden constructs that the
  18.3 decoder does not contain, so the fix does not map onto this tree.
- **GHSA-xhj4-vrgc-hr34 promoted at actix/actix-web http-v3.12.0**
  (`reports/PROMOTION_20261031_ACTIX_GHSA-XHJ4.json`), the seventh and last legacy `unknown`
  triage row. The advisory covers `actix-http` < 3.12.1 (first patched 3.12.1, CVSS v4.0 6.3
  medium, CWE-444); the frozen tag `http-v3.12.0` (commit `a7a26f1e`) ships `actix-http` 3.12.0,
  so it is inside the range. Anchor `actix-http/src/h1/decoder.rs:231-315` (`Request::decode`,
  fix-diff comparison): `set_headers` (`:75-213`) records `Content-Length` (`:106-127`) and
  `Transfer-Encoding: chunked` (`:135-150`) independently and resolves the payload length by
  testing `chunked` first (`:198-202`) before `content_length` (`:205-209`), so a request carrying
  both is accepted and framed as chunked instead of being rejected (RFC 9112 §6.3); the frozen
  tree's own `hrs_cl_and_te_http10` test (`:1118-1134`) asserts that acceptance with the comment
  "in HTTP/1.0 transfer encoding is simply ignored so it's fine to have both". Fix `3c056bd361`
  ("Merge commit from fork", released in `http-v3.12.1`; compare `http-v3.12.0...http-v3.12.1`
  = ahead 57 / behind 0) inserts the missing cross-check right after the `set_headers` call at
  `:276` and adds the CL+TE, HTTP/1.0 TE and non-chunked-TE rejections. The candidate row
  `adv3_61724d22cf10bab7` had been dropped from `candidates.jsonl` by the migration, so it was
  restored first (schema-validated, inserted after the snapshot's block, dossier from
  `repo_vuln_benchmark-data-only-snapshot-20261026`) — the candidate table is now 1405 rows.
- **Coverage reconciliation: 29 snapshots upgraded to `PASS_KNOWN_SWEEP`** in four batches
  (`reports/COVERAGE_RECON_20261031_SINATRA_UNDICI.json`, sinatra 4.0.1 and undici 5.19.0;
  `reports/COVERAGE_RECON_20261031_BATCH2.json`, twenty; `reports/COVERAGE_RECON_20261031_BATCH3.json`,
  cryptography 41.0.5, plug 1.19.2, PHPMailer 6.1.5 and actix/actix-web http-v3.12.0;
  `reports/COVERAGE_RECON_20261031_BATCH4.json`, the multi-package snapshots gitea v1.25.5,
  protobuf v3.25.4 and symfony v5.4.45). The Phase A outcome `NEEDS_REVIEW`
  recorded only the number of candidates unresolved at sweep time (`unresolved_relevant_candidates`
  equalled the snapshot's whole candidate count in all 42 rows), so it went stale once every
  candidate carried a decision. The upgrade is earned record by record: OSV (`package` + `version`)
  and the GitHub Advisory Database (`affects=pkg@version`) were re-queried on 2026-10-31, and every
  returned record's GHSA/CVE identifiers had to match a triage row at that snapshot — live candidate
  aliases or the basis/notes of an earlier resolved row. sinatra returns 2 OSV / 2 GH records and
  undici 24 / 24, all matched, with 0 undecided live candidates and 0 gaps; NVD was not re-queried
  (the sweep's CPE-filtered counts stand and the limitation is recorded inline). The rows carry a
  `reconciliation` object with both query URLs, the matched/unmatched counts and the triage-row
  counts, and `discovery_tasks` was recomputed (`sync_discovery_tasks.py --apply`). Note that the
  candidate table is not append-only: 56 of undici's 63 triage rows are earlier resolved rows whose
  `candidate_id` no longer exists in `candidates.jsonl`, so a record can only be matched against the
  triage table, never against the live candidates alone. Batch 2 applied the same rule to the 23
  other single-package snapshots: twenty reconciled with 0 gaps over 1–82 OSV and 1–29 GitHub
  records each (caddy, lodash, express, axios, vite, nest, angular, flask, werkzeug, django, rack,
  rails, guzzle, laravel, ecto, rustls, tokio, ImageSharp, jenkins, echo). Four were kept.
  cryptography 41.0.5, plug 1.19.2 and PHPMailer 6.1.5 each carry one legacy `unknown` triage row
  whose candidate no longer exists (a zero-LLM placeholder: "Existing pending_version status gives
  no established relevance to the frozen SHA") — the source records all match, but a snapshot with
  an undecided row is not swept clean, so the upgrade waited. Those three rows were closed on
  2026-10-31 (`reports/ORPHAN_TRIAGE_20261031.json`): the pre-migration dossiers were recovered
  from `repo_vuln_benchmark-data-only-snapshot-20261026`, and each turned out to be a **second
  candidate row for an advisory the snapshot already carries as a promoted row** (CVE-2023-49083
  at cryptography, CVE-2026-54892 at plug, CVE-2020-13625 at PHPMailer, plus CVE-2026-32688 at
  plug_cowboy and CVE-2025-24070 at aspnetcore), so they are closed as `duplicate` of the promoted
  candidate, naming its anchor. The seventh orphan was a NVD *keyword* hit for the guzzle advisory
  CVE-2026-67339 on the curl snapshot (`mapping_statuses=[keyword_results_require_upstream_attribution]`)
  and is `out_of_scope`: the advisory names no curl component and the guzzle snapshot already
  carries the promoted row. Batch 3 then re-ran the three unblocked snapshots (16/8, 4/1 and 3/3
  records, 0 gaps) together with actix/actix-web, whose own last orphan was promoted the same day.
  tomcat 9.0.98 returned 0 OSV and 0 GitHub records for `tomcat-catalina`, so it has no
  record-level evidence at all and its NVD-only sweep stands unchanged; the same is true for
  aspnetcore v8.0.13 (`Microsoft.AspNetCore.App.Runtime` and `Microsoft.AspNetCore.Identity`: 0/0)
  and netty `io.netty:netty-codec-stomp` 4.1.137.Final (0/0). Batch 4 covered the multi-package
  snapshots by querying every package the sweep recorded: gitea (94 OSV / 62 GitHub records), the
  five protobuf packages (5/5) and the twelve symfony packages (42/43), all matched with 0 gaps.
  The remaining 13 snapshots stay `NEEDS_REVIEW` until the same reconciliation runs for them.
- **22 netty/netty rows** promoted 2026-10-31 at the frozen `netty-4.1.137.Final` tag, commit
  5471f0a6, from the 32 open candidates on that snapshot (`reports/SWEEP_20261031_NETTY.json`).
  All 32 GitHub security-advisory records were fetched with `gh api`; every one carries an empty
  `fix_commits` array and the OSV cache has no record for 29 of them, so the rows use
  `evidence_type=source_review` (published advisory text + the frozen source) instead of a
  fix-diff comparison: each anchor is the line the advisory describes, read verbatim at the tag,
  and the vendor range in the advisory covers 4.1.137.Final in all 22. Anchors by construct:
  HTTP/1 request smuggling and chunk parsing in `HttpObjectDecoder` (split
  Transfer-Encoding fields at :859, the suffix-only `chunked` test at :865, the skipped
  chunk-extension validation at :743, the whitespace-terminated chunk size at :1041), the
  unbounded method queue in `HttpServerCodec` (:178) and the extension queue in
  `WebSocketServerExtensionHandler` (:157), HTTP/2 request-authority handling in
  `HttpConversionUtil` (CONNECT authority-form at :445, absolute-form Host mismatch at :449,
  Extended CONNECT downgrade at :273), the unbounded `HpackEncoder` table size (:242) and the
  opt-in value validation in `DefaultHttp2Headers` (:168), protocol-decoder resource limits
  (`SmtpResponseDecoder` continuation list :87, `MqttDecoder` properties length :824,
  `RedisArrayAggregator` nested preallocation :133, `SpdySessionHandler` concurrent streams
  :719, `HAProxyMessage` nested-TLV release :340), the integer/validation defects
  (`StompSubframeDecoder` long-to-int cast :149, `BinaryMemcacheResponseDecoder` signed lengths
  :42, `SmtpCommand` unvalidated command name :69, `RtspMethods` trailing control byte :126), and
  the two OCSP checks (`OcspClient.validateSignature` without the OCSPSigning EKU :314,
  `OcspServerCertificateValidator` skipping validation when `nextUpdate` is absent :175). The
  other 10 candidates are decided in the same report's triage phase: eight `confirmed_not_affected`
  — six because the module does not exist in the 4.1 line (codec-http3 and
  codec-classes-quic are 4.2-only, so GHSA-495p, hfr2, jgph, q9pg, mj35 and CVE-2026-56816 have no
  pre-image), GHSA-2g6j because the frozen `isContentAlwaysEmpty` already excludes 1xx from the
  method queue, and CVE-2026-42583 because `Lz4FrameDecoder` at the tag bounds the decompressed
  length before allocating — and two stay `possible_affected` even though the advisory range ends
  at 4.1.136: the SOCKS5 encoder half of GHSA-cc6x still writes usernames, passwords and domain
  names without the NUL/CRLF `sanitize()` that only `Socks4ClientEncoder` gained, and
  `OpenSslX509TrustManagerWrapper` still returns a plain `X509TrustManager` unwrapped, which is
  the endpoint-identification loss GHSA-p85m describes. With no published 4.1 fix commit, the
  range endpoint and the frozen source disagree, so those two are left open rather than recorded
  as not affected.
- **17 dotnet/aspnetcore rows** promoted 2026-10-31 at the frozen v8.0.13 snapshot, commit
  009e1cca, from the 24 open candidates on that snapshot (`reports/SWEEP_20261031_ASPNETCORE.json`).
  The GitHub advisory records carry no fix commits, so each fix was located by comparing the
  frozen file with the same file in the release named as the first patched version, using the
  `compare/{base}...{head}` release API and the resulting patches: 8.0.21 for CVE-2025-55315,
  8.0.25 for -26130, 8.0.26 for -56170, 8.0.29 for -47300/-47303, 8.0.31 for -69304 and 8.0.32
  for the remaining ten. Every anchor is the frozen line that guard replaces or bounds, and all
  seventeen rows are T1/`vendor_official` with `evidence_type=fix_diff_comparison`. Anchors:
  Kestrel chunk-extension termination (`Http1ChunkedEncodingMessageBody.ParseExtension` :379),
  HTTP/2 trailer and dynamic-table newline checks (`Http2Connection.OnHeaderCore` :1526) and the
  HTTP/1 keep-alive state on abort (`HttpProtocol.CancelRequestAbortedToken` :498), the HTTP/3
  abort lock-order deadlock (`Http3Stream.AbortCore` :176), SignalR stateful-reconnect writes and
  backpressure (`HubConnectionContext.WriteCore` :272, `MessageBuffer.WriteAsyncCore` :138,
  `MessageBuffer.ResendAsync` :279), web utilities (`FormPipeReader.ParseFormValuesFast` :167,
  `FileBufferingReadStream` ctor :82), stale asynchronous authorization
  (`AuthorizeViewCore.OnParametersSetAsync` :90), the localization fallback cache
  (`RequestLocalizationMiddleware` :170), out-of-process IIS body-size clearing
  (`IISMiddleware.Invoke` :135), Negotiate LDAP lookups (`LdapAdapter` filter :44, group filter
  :105, unchecked first entry :62), the Identity reset mail recipient
  (`ForgotPassword.OnPostAsync` :83) and the Blazor debug page's unencoded exception
  (`TargetPickerUi.Display` :296). The other seven candidates are decided in the same report's
  triage phase: two `confirmed_not_affected` by range — CVE-2023-36038 lists only the
  8.0.0-rc.2.23480.2 build and CVE-2021-43877 only 2021-era ANCM module versions, with no 8.0
  servicing range — two `duplicate` (the discovery candidates for CVE-2025-55315 and
  CVE-2026-69304 alias the promoted advisory rows), and three left `possible_affected` in that pass:
  CVE-2026-42899 (the advisory named no component and the 8.0.27 range was read as containing no
  attacker-controlled loop), and CVE-2026-45591 and CVE-2026-92707 (they consume the
  MessagePack-CSharp parser, an empty submodule directory in the frozen checkout). The follow-up
  pass below settled all three: 42899 is promoted at `FormDataReader.ProcessFormKeys`, and the two
  MessagePack rows are `out_of_scope`.
- **5 DaveGamble/cJSON rows** promoted 2026-10-31 at the frozen v1.7.16 snapshot, commit
  cb8693b0, from the 22 open candidates on that snapshot (`reports/SWEEP_20261031_CJSON.json`).
  These advisories have no fixed release to diff against — v1.7.19 and master were fetched and
  compared function by function, and the same construct is still present in both — so all five
  are `evidence_type=source_review`, T2/`unknown` on the NVD CVE record, S2. Anchors: the JSON
  Pointer escape decoder writes the `~1` replacement to the wrong byte
  (`decode_pointer_inplace` `cJSON_Utils.c:377`), JSON Patch add/copy can amplify document depth
  past the unbounded recursion of `cJSON_Duplicate` (`cJSON.c:2753`, whose v1.7.19
  `CJSON_CIRCULAR_LIMIT` guard does not exist at v1.7.16) and `cJSON_Delete` (`cJSON.c:261`),
  `cJSON_Compare` recurses into every object subtree in both directions (`cJSON.c:3097`,
  CWE-407), `apply_patch` detaches and deletes the REPLACE/MOVE target before the operation is
  validated (`cJSON_Utils.c:890`, with the source subtree deleted in cleanup), and
  `parse_number` truncates number literals longer than 63 bytes into its 64-byte stack buffer
  (`cJSON.c:309`, CVE-2023-26819). The other seventeen candidates are decided in the same
  report's triage phase: four `confirmed_not_affected` because the 2016-10-02 backslash guard
  (94df772), the 1.7.9 `get_object_item` NULL checks (be749d7e) and the 1.7.11 `cJSON_Minify`
  rewrite (93688cbe) are all present in the frozen tree; six `out_of_scope` for advisories owned
  by other projects (python-cjson 2009-4924/2010-1666, FreeSWITCH's vendored `esl_json.c`
  2015-7392, OpenHarmony 2022-36423, SKRoot-linuxKernelRoot 2026-24813 and Apache Kvrocks' Lua
  cjson 2026-46752); and seven `duplicate` — CVE-2024-31755 is the same
  `cJSON_SetValuestring` NULL dereference already anchored by CVE-2023-50472 at `cJSON.c:408`,
  and the five Debian OSV aliases of the promoted 2026 rows and of CVE-2026-87933 add no
  distinct vulnerability.
- **3 pyca/cryptography rows** promoted 2026-10-31 at the frozen 41.0.5 snapshot, commit
  5012beda, from the 20 open candidates on that snapshot (`reports/SWEEP_20261031_CRYPTOGRAPHY.json`).
  Anchors: `serialize_key_and_certificates_to_pkcs12` passes the result of `PKCS12_create` to
  `PKCS12_set_mac`, but the NULL check for a certificate/private-key mismatch sits after the call
  (`backend.py:1829`, CVE-2024-26130, fixed in 42.0.4 by commit 97d23167, T1/`vendor_official`);
  `_enc_dec_rsa_pkey_ctx` turns every non-positive `EVP_PKEY_decrypt` return into
  `ValueError("Encryption/decryption failed.")`, the PKCS#1 v1.5 padding oracle that 42.0.0 closed
  by moving the path to Rust and shipping wheels built with OpenSSL 3.2.0 (`rsa.py:163`,
  CVE-2023-50782, T2/`unknown`); and `_ec_key_set_public_key_affine_coordinates` installs affine
  coordinates after only `EC_POINT_set_affine_coordinates`, so on a cofactor > 1 curve a
  small-order point passes without a prime-order subgroup test (`backend.py:1248`,
  CVE-2026-26007, 46.0.5 adds `check_key_infinity` plus `EC_KEY_check_key` when the cofactor is
  not 1, T1/`vendor_official`). The other seventeen candidates are decided in the same report's
  triage phase: ten `confirmed_not_affected` — four outside the advisory range (CVE-2022-3602
  covers 37.0.0-38.0.3, CVE-2023-0286 and CVE-2023-23931 are fixed in 39.0.1, CVE-2023-2650 in
  41.0.0; the 41.0.5 `Cipher.update_into` already uses
  `from_buffer(..., require_writable=True)` at `ciphers.py:159`) and six whose X.509 verifier does
  not exist at 41.0.5 (`src/rust/src/x509/` has no `verify.rs` and `src/cryptography/x509/` has no
  `verification.py`; the 42.0.0 changelog adds the path-validation APIs, CVE-2026-69248 and
  CVE-2026-69249 are introduced in 45.0.0 and 42.0.0 while their PYSEC rows claim
  `introduced:0`); five `out_of_scope` for the wheel-bundled OpenSSL advisories, whose own text
  says sdist users upgrade their own OpenSSL and whose pyca reference commit is "bump openssl in
  CI"; and two `duplicate` PYSEC aliases of the promoted CVE-2024-26130 and CVE-2026-26007 rows.
- **10 angular/angular rows** promoted 2026-10-31 at the frozen 19.2.15 snapshot, commit
  fbe9b9f9, from the 20 open candidates on that snapshot (`reports/SWEEP_20261031_ANGULAR.json`).
  Anchors: `parseUrl` resolves the untrusted `INITIAL_CONFIG.url` against the synthetic
  `resolve://` base, so a protocol-relative request URL replaces `PlatformLocation.hostname`
  (`location.ts:31-34`, CVE-2026-41423, the 19.x fix f3a5bfb rewrites the function and its
  regression test asserts an empty hostname; the `/\host` spelling alone does not cross origins
  under a non-special base); the same function returns a dot-segment-normalized pathname without
  collapsing leading slashes, so `/.//evil.test` is stored as `//evil.test` (`location.ts:36-43`,
  CVE-2026-111754, vendor fix d187e8ae adds `LEADING_SLASHES_REGEX`); the sanitizer switch lists
  only `Property`/`Attribute`/`HostProperty`, leaving `OpKind.TwoWayProperty` unsanitized
  (`resolve_sanitizers.ts:59-61`, CVE-2026-54265, fix 3c70270c); `visitElement` accepts
  `i18n-on*` because the i18n branch checks only `isTrustedTypesSink` (`meta.ts:147`,
  CVE-2026-69151, fix 6c41f5ca); `formatDate` runs an unbounded format string through the
  `DATE_FORMATS_SPLIT` loop (`format_date.ts:92-93`, CVE-2026-54268, fix eeb03f4e caps it at
  256); `formatNumberToLocaleString` passes unbounded `digitsInfo` fraction digits to
  `roundNumber` (`format_number.ts:71-72`, CVE-2026-50171, fix dfdfbe34 caps at 100);
  `transferCacheInterceptorFn` never inspects `withCredentials` (`transfer_cache.ts:139`,
  CVE-2026-50170, fix 34090cb1) and `generateHash` is the 32-bit DJB2 accumulator
  (`transfer_cache.ts:297`, CVE-2026-54266, fix 5f36274d moves the key to SHA-256); and
  `newRequestWithMetadata` rebuilds service-worker requests with headers only, dropping
  credentials and cache mode (`assets.ts:515`, CVE-2026-50184) and the redirect policy
  (`assets.ts:514-515`, CVE-2026-50169, fix 58bf5ecd whose pre-image is exactly this line). The
  other ten candidates are `confirmed_not_affected`: six DOM-parser advisories whose affected
  ranges start at 20.0.0 and whose domino implementation is only an npm dependency from this tree
  (CVE-2026-101895, -50555, -50556, -69149, -88058, -88060); the Angular DevTools row, whose
  affected extension band starts at 1.20.0 while the frozen manifest is 1.0.32 (CVE-2026-101897);
  two VS Code language-service extension rows whose `client/` and `server/` sources are in a
  separate repository (CVE-2026-49241, -50178); and the Unicode-whitespace SSR row, whose named
  prerequisite `String.prototype.trim()` does not exist in `packages/platform-server/src` at this
  SHA (CVE-2026-88056).
- **29 applied by earlier 2026-10-31 batch runs**, subsequently covered row by row in
  `reports/PROMOTION_REVIEW_20261031_LEGACY_BATCH.json` (26 Gitea, 3 libexpat). All 29 were
  admitted: the frozen line at each anchor is one of the lines its cited fix hunk removes. One
  anchor was relocated before admission, CVE-2026-73273, from the tag-path assembly to the
  unbounded `ctx.Req.Body` read at `routers/api/packages/maven/maven.go:263`. Line offsets between
  the anchors and the hunk headers are expected because the fix commits are authored on newer
  branches than the frozen v1.25.5 / R_2_6_2 snapshots.
- **20 Gitea rows promoted 2026-10-31 from the FIX pull requests of the advisories that the batch
  gate had rejected as `ambiguous_shared_fix_commit`** (`reports/PROMOTION_REVIEW_20261031_GITEA_PR.json`):
  18 anchored by source review on the fix hunk's code path, CVE-2026-58420 by comparing the removed
  line of a fix commit the advisory does not cite (identified by content), and CVE-2026-20896 on the
  Docker `app.ini` template line the fix deletes (`function=null` with an explicit functionless
  reason). Ten sibling catalog rows of these CVEs were rewritten as `duplicate`. CVE-2026-58416 was
  triaged `confirmed_not_affected` (the guarded function does not exist at v1.25.5); CVE-2026-58428
  and CVE-2026-58440 stay unresolved because the cited PRs contain no matching hunk.
- **15 Gitea rows** promoted 2026-10-31 from the 1.27.0 security batch (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH2.json`): the vulnerable code of CVE-2026-42931, 50105, 54481, 55982, 55984, 55986, 57897, 58434, 58443, 58444, 58445, 58507, 58508, 58510 and 58511 exists verbatim at the frozen v1.25.5 tree. Five anchors are lines the fix removes, eight are the hunk context line an inserted guard protects (the fix only adds lines), and two are frozen spans read by hand because the fix parent drifted (`routers/api/v1/repo/issue_label.go:181-188`, `services/webhook/general.go:407-419`). Every row was checked for the fix marker being absent from the frozen function and present in the fetched v1.27.0 release tag. Two of the fifteen (CVE-2026-55986, CVE-2026-58508) have no published GHSA page and are T2/`unknown` on their CVE/OSV records; the other thirteen are T1/`vendor_official`. The release-wide OSV GIT ranges cite the unrelated shared commit 73e0e442 for every CVE in the batch, so the rows cite the per-file fix hunks in the 93-file security commit f69e15afe7 (CVE-2026-58434: 362539b78e plus backport 500a09e044) instead. Thirteen sibling catalog rows were rewritten as `duplicate`. CVE-2026-58416 (code first present in v1.26.4) and CVE-2026-55987 (the flawed gate, not the pre-#38009 unconditional block already anchored by CVE-2026-58422) were not promotable at this snapshot; the reasons are recorded in the report's `skipped` section.
- **9 Gitea rows** promoted 2026-10-31, the remainder of the same 1.27.0 advisory set
  (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH3.json`): CVE-2026-57894, 58427, 58431, 58433,
  58435, 58437, 58438, 58441 and 58442. These nine were not covered by batch 2 because their
  fixes are not hunks of the 93-file commit f69e15afe7 but the preceding per-topic security
  commits: 122ebcf0 (#38213, private org member listing), f452c369 (#38323, public-only token
  scope and push options), aab3242f (#38324, team-repo linking, issue dependencies, restore
  SSRF, migration allow-list) and 66a3723c (#38322, LFS proof of possession), with 9e84deb9
  (#38108) plus 97078b96 (#38320) for the clone/mirror redirect SSRF. Two anchors are lines the
  fix removes (`services/lfs/server.go:267-284`, `services/migrations/migrate.go:89-106`), four
  are the frozen line an inserted guard is attached to, and three are frozen lines read by hand
  because the fix parent drifted from v1.25.5. Every row was checked for the marker being absent
  from the frozen function and present in the fetched v1.27.0 tag. CVE-2026-58433 has no GHSA
  page (HTTP 404) and is T2/`unknown` on its CVE/OSV record; the other eight are
  T1/`vendor_official`. Eight sibling catalog rows were rewritten as `duplicate`.
  CVE-2026-55987 stays unresolved: its flawed gate does not exist at v1.25.5 (the frozen
  `routers/web/auth/oauth.go:351-354` block is the pre-#38009 code already anchored by
  CVE-2026-58422), so the skip is recorded in the report.
- **10 Gitea rows** promoted 2026-10-31 from the 2026 advisory set whose OSV ranges cover
  v1.25.5 (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH4.json`): CVE-2026-101023, 101027,
  103059, 103667, 104633, 105267, 105268, 20706, 24791 and 25714. These are the first ten of
  the 87 open `needs_static_location` candidates whose cited release-range commit is a
  **bundle**: 89363035105 (#39501) lands four unrelated handler fixes, f2a1271f (#37118) two,
  and the OSV GIT ranges for the 28.x batch all point at release commits, so a hunk's
  pre-image does not by itself say which CVE it fixes. Each row was therefore attributed by
  matching the advisory text to one modified handler, and checked by the marker being absent
  from the frozen enclosing function and present in that commit's patch added lines (the fix
  releases v1.26.2 / v28.0.0 / v28.1.0 all postdate the v1.27.0 tag, so the v1.27.0 check used
  in batches 2-3 does not apply here). Six anchors are lines the fix removes (including the
  whole 41-line `switch` of `checkTokenPublicOnly`, replaced by a category loop), two are the
  frozen line an inserted guard protects, and two are frozen lines read by hand
  (`container.go:708`, `migrate.go:101`) because the fix parent drifted. All ten are
  T1/`vendor_official`. Three sibling catalog rows were rewritten as `duplicate`; three
  candidates (CVE-2026-28740, 58422, 60004) duplicate an already-promoted CVE and became
  `duplicate`; CVE-2026-24451 is `confirmed_not_affected` for both of its candidates because
  OSV gives the range as introduced 1.26.2. CVE-2026-101029 shares the
  `checkByAllowBlockList` anchor of CVE-2026-58442, CVE-2026-104636's
  `modules/git/redirection.go` does not exist at v1.25.5, and CVE-2026-55987 remains skipped;
  the three reasons are in the report's `skipped` section.
- **8 Gitea rows** promoted 2026-10-31 from per-topic 2026 advisories
  (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH5.json`): CVE-2026-62925, 67577, 70400,
  73130, 73278, 79960, 95112 and 96589. Here the cited fix commit is small and the advisory
  text maps to one hunk, so no bundle attribution was needed: #39026 bounds Alpine .PKGINFO
  entries, #39396 bounds the issue-keyword scan window, #39027 adds the `MaxSize(1024)` tag on
  the gitignores field, #39007 adds `rejectPublicOnly()` to the migration route, #39004 routes
  the per-user visibility check through `IsUserVisibleToViewer`, #38805 requires a WebAuthn
  challenge per request (including OAuth/OIDC link-account sign-in), #37306 resolves the pusher
  through `GetPossibleUserByID` so deploy keys stop acting as the owner, and #39042 revokes the
  transfer recipient's temporary collaboration when the transfer is rejected or cancelled.
  Seven anchors are lines the fix removes; the Alpine one is the append statement an inserted
  bound governs. The gitignores anchor is the struct field itself and carries a
  `functionless_reason` because a field has no enclosing function. All eight are
  T1/`vendor_official`; no sibling catalog row existed for them.
- **6 Gitea rows** promoted 2026-10-31 from advisories whose fixes sit inside shared commits
  (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH6.json`): CVE-2026-27761, 68957, 71184, 86684,
  97208 and 97626. Each advisory names one handler, and the row anchors that handler's guard:
  #38108 adds `checkRepoFeedTokenScope` to the repository feeds (27761), #39004 switches issue
  search to `PublicRepoUnderPublicOwnerCond` (68957), #39501 passes the caller instead of the
  owner to `IsMigrateURLAllowed` in the push-mirror API (86684), honours `DISABLE_NEW_PUSH` in
  `AddPushMirror` (97208) and adds the owner-visibility check to `showUserFeed` (97626), and
  #38808 attaches the pull request to review notifications so the fork approval gate sees them
  (71184). Three anchors are lines the fix removes and three are the frozen line an inserted
  guard protects. Four further advisories in these same commits are **not promotable** at
  v1.25.5 and stay open: 63792 (the collaborative-owner reusable-workflow check does not exist
  in `models/perm/access/repo_permission.go`), 66874 (filtered-workflow skipped status),
  66877 (`checkJobsOfCurrentRunAttempt` absent) and 96594 (the media API LFS-pointer branch is
  newer). One sibling catalog row (`disc2_b338ed123b84038d80886eac`, 27761) was rewritten as
  `duplicate`.
- **6 Gitea rows** promoted 2026-10-31 from per-topic fix commits
  (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH7.json`): CVE-2026-26231, 27780, 28699, 58421,
  70406 and 73126. #38949 keeps the OAuth2 token scope the Basic authenticator was discarding,
  #36963 makes a scanner error in the pre-receive hook fail closed, #38751 adds
  `CheckRepoScopedToken` to the workflow badge, #39006 rejects a compare whose head repository
  the token cannot access (plus backport 320b44df), #37479 requires the PR poster to have write
  access on the head repository before `AllowMaintainerEdit` applies (plus backport 74e51562),
  and #38947 bounds CODEOWNERS regexp matching with a per-rule `MatchTimeout` and a 2 s aggregate
  budget. Two anchors are lines the fix removes; four are the frozen line an inserted guard is
  attached to. CVE-2026-27780 has no GHSA page (HTTP 404) and is T2/`unknown` on its CVE/OSV
  record; the other five are T1/`vendor_official`. Three sibling catalog rows
  (`disc2_789764d31d9c13f7941c61b4`, `disc2_721b9a14b04bd3e8c74e4d26`,
  `disc2_2e0e0bcaa0cecb7c9f998e42`) were rewritten as `duplicate`, and CVE-2026-25779 is
  `confirmed_not_affected` because its OSV GIT range fixes it at f913d90ab664, the frozen
  v1.25.5 commit itself.
- **11 Gitea rows** promoted 2026-10-31 from the 1.27.2 advisory set
  (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH8.json`): CVE-2026-59766, 60010, 63021, 66853,
  70396, 70402, 70407, 71301, 73535, 94205 and 95106. #39047 lowers organization visibility for
  restricted viewers, #39041 moves the organization token scope to the front of
  `/api/v1/orgs`, #39046 requires an organization owner for team links, #39045 applies the PR
  unit permission to same-repository icon/title rendering, #39025 bounds Swift manifest count and
  total size, #39007 adds the repository token scope to organization repo creation, #39008 drops
  hook modes from 0777 to 0755, #39472 enables `transfer.fsckObjects`, #38324 filters starred
  repos and tracked times by current permission, #39399 decides fork-run approval on the PR
  author as well as the trigger, and #38805 gates OpenID linking behind the second factor. Seven
  anchors are lines the fix removes and four are the frozen line an inserted guard is attached
  to. CVE-2026-59766 is T1/`github_reviewed` (its GHSA page resolves and states `< 1.27.0`); the
  other ten have no GHSA page (HTTP 404) and are T2/`unknown` on their CVE/OSV records. One
  sibling catalog row (`disc2_e14d51a6854010ebdb28ff2b`, 59766) was rewritten as `duplicate`.
  Three siblings of 94205 are not promotable at this snapshot (the approval/concurrency/rerun
  code does not exist at v1.25.5), and the 1.27.2 SSRF cluster (96400, 70357, 101029, 89430,
  104636) is deferred to a dedicated review because its fix is the internal git-proxy
  architecture rather than a per-handler hunk; both reasons are in the report.
- **7 Gitea rows** promoted 2026-10-31 from per-topic fix commits
  (`reports/PROMOTION_REVIEW_20261031_GITEA_BATCH9.json`): CVE-2026-58418, 58419, 68964, 78231,
  96399, 96404 and 55987. #38108 disables redirect following in the clone helper (58418, a
  second CVE for the same defect already anchored by CVE-2026-57894 at
  `modules/git/repo.go:141`) and returns early when the notification repository is no longer
  readable (58419); #38406 requires the auto-sync signature before reactivating a
  deactivated OAuth2 user (55987) and routes OpenID verification through an allow-list
  transport (78231); #39004 replaces the inline visibility switch with
  `IsUserVisibleToViewer` (68964); #39354 scans the regexp group pairs instead of indexing
  group 2 (96399); #39400 rejects an installer admin name when post-installation users exist
  (96404). Two anchors are lines the fix removes, one is the line an inserted guard is
  attached to, and four are frozen lines read by hand because the fix parent drifted or the
  fix only replaces behaviour. 58418 and 58419 are T1/`github_reviewed`; the other five have
  no GHSA page (HTTP 404) and are T2/`unknown` on their CVE/OSV records. Three sibling catalog
  rows (`disc2_75cef4ed62ec120f1f711c23`, `disc2_375cd7e26e1e2a07f26b59e5`,
  `disc2_c4e8c5fab859f5bbe0c7e9cf`) were rewritten as `duplicate`. The four advisories left
  open by batch 6 are now resolved as `confirmed_not_affected` at the frozen tag: 63792
  (scoped reusable workflows), 66874 (filtered-workflow statuses) and 66877 (job concurrency)
  describe features that do not exist at v1.25.5, and 96594's media API already serves
  blobs through `ServeContentByReader`, which sets a sniffed `text/plain` content type
  instead of the later raw-write path. CVE-2026-103670 and CVE-2026-104626 are
  `confirmed_not_affected` for the same reason applied to 66877: both need Actions
  concurrency groups, which v1.25.5 does not support. Candidates 58428, 58440, 96580, 73504,
  GHSA-m984-2424-x6vw and GHSA-qg66-h68v-5x2h, CVE-2026-28737, CVE-2026-104632 (fixed through
  the v28 `plan` restructuring of `services/actions/rerun.go`, whose pre-image is absent) and
  the deferred SSRF cluster stay unresolved for the reasons in the report's
  `not_promotable` and `left_open` sections. Follow-up decisions:
  `reports/PROMOTION_REVIEW_20261031_GITEA_BATCH9_FOLLOWUP.json`.
- **15 libexpat rows** promoted 2026-10-31 against the frozen R_2_6_2 tree, in three batches.
  Batch 1 (`reports/PROMOTION_REVIEW_20261031_LIBEXPAT_BATCH1.json`) covers the 2.8.2
  overflow set from PRs 1232/1249/1251/1255/1262/1259/1252/1263/1272: CVE-2026-56403, 56404,
  56405, 56406, 56407, 56408, 56409, 56410, 56411 and 56132. Batch 2
  (`reports/PROMOTION_REVIEW_20261031_LIBEXPAT_BATCH2.json`) adds CVE-2024-45491 (dtdCopy,
  32-bit only), CVE-2024-45492 (nextScaffoldPart, 32-bit only), CVE-2026-25210 (doContent tag
  buffer shift), CVE-2026-93990 (UTF-16 high surrogate accepted; the
  `xmltok_impl.c` fallback plus the `xmltok.c:825` NULL isInvalid4 vtable, the one
  functionless row)
  and CVE-2026-41080 (4-to-8-byte SipHash salt, PR #1183). Batch 3
  (`reports/PROMOTION_REVIEW_20261031_LIBEXPAT_BATCH3.json`) adds CVE-2026-72522 (low
  surrogates misclassified in `*_toUtf16`, PR #1296) and CVE-2026-77214 (XML_ParseBuffer
  trusts len beyond the buffer capacity, PR #1393). Every row anchors the frozen C statement
  its fix hunk protects and passes the two-check model: the fix marker is absent from the
  frozen enclosing function (or file) and present among the patch's added lines. All 15 are
  T2/`unknown` on their CVE/OSV records (no GHSA page), and 16 sibling catalog rows were
  rewritten as `duplicate`. Exclusions, with evidence, are
  `reports/TRIAGE_20261031_LIBEXPAT_OLD_CVES.json` (eight pre-2.0 identifiers that name
  third-party consumers of expat or already-fixed upstream bugs: CVE-2004-1378, 2009-1955,
  2009-2473, 2011-1753, 2016-9063, 2018-14647, 2021-40439, 2023-32206),
  `reports/TRIAGE_20261031_LIBEXPAT_DEBIAN.json` (twelve DSA/DLA rows resolved through the
  Debian security tracker: nine fixed at or before 2.2.10, three duplicates of CVEs already
  in the Ground Truth) and CVE-2026-76641, whose struct-size mismatch needs the 2.8.1
  `defaultAttForName` table that R_2_6_2 does not have. Five candidate rows remain open on the
  advisory range alone: CVE-2025-59375 (two catalog rows; PR #1034 installs a whole
  allocation-tracking mechanism, no pre-image statement), CVE-2025-66382 (no fix commit) and
  CVE-2026-66046 (two catalog rows). Five further Debian-alias rows (CVE-2026-45186, 2026-50219,
  2026-56131, 2026-56412, 2026-76957) were rewritten as `duplicate` because those CVEs are
  already in Ground Truth for this tree.
- **13 openssl rows** promoted 2026-10-31 from the 2026-09-29 advisory batch, one per CVE that
  applies to 3.5.8 (`reports/PROMOTION_REVIEW_20261031_OPENSSL.json`): 8 anchors are lines the
  3.5-branch fix hunk deletes, 4 are additive fixes anchored on the statement the inserted guard
  governs, and 1 is a structural shift (CVE-2026-54873, whose fix targets the reassembly
  implementation introduced by the CVE-2026-42772 fix). CVE-2026-84783 is not applicable to
  3.5.8 (4.0.0 - 4.0.3 only).
- **4 curl rows** promoted 2026-10-31 from source anchors that `propose_locations.py` produced for
  the frozen 8.3.0 tree and that were verified against the curl advisory JSON, the NVD 2.0 CPE
  match and the release that ships the fix
  (`reports/PROMOTION_REVIEW_20261031_CURL_EARLY.json`, rebuilt from the Ground Truth rows and
  their locations after the 18-row batch-2 run reused that report path): CVE-2023-46219
  (`lib/fopen.c:71`), CVE-2024-2004 (`lib/setopt.c:2693-2698`), CVE-2024-8096
  (`lib/vtls/gtls.c:928`) and CVE-2024-2398 (`lib/http2.c:1458`). All four frozen anchors are
  lines their fix commits delete.
- **40 curl rows** promoted 2026-10-31 in three batches against the frozen curl-8_3_0 tree, one
  row per advisory, each passing the three-check model (the frozen statement the fix hunk
  touches exists at 8.3.0, the fix marker is absent from the frozen enclosing C function, and
  the marker is among the patch's added lines). Batch 1
  (`reports/PROMOTION_REVIEW_20261031_CURL_BATCH1.json`, 21 rows) covers CVE-2024-9681,
  CVE-2025-14524, CVE-2025-15224, CVE-2024-7264, CVE-2025-14819, CVE-2026-1965, 2026-3783,
  2026-3784, 2026-4873, 2026-6253, 2026-8924, 2026-10536, 2026-107928, 2026-11856, 2026-12064,
  2026-13608, 2026-18924, 2026-87863, 2026-87864, 2026-87866 and 2026-92390; batch 2
  (`reports/PROMOTION_REVIEW_20261031_CURL_BATCH2.json`, 18 rows) covers CVE-2025-15079,
  CVE-2026-5545, 2026-6276, 2026-6429, 2026-7168, 2026-8286, 2026-8458, 2026-8927, 2026-86409,
  2026-86414, 2026-87865, 2026-82209, 2026-80230, 2026-80231, 2026-92388, 2026-92389, 2026-92391
  and 2026-94266; batch 3 (`reports/PROMOTION_REVIEW_20261031_CURL_BATCH3.json`, 1 row) covers
  CVE-2026-86410, whose fix moved to `src/config2setopts.c` after the frozen tag and whose
  frozen guard is `src/tool_operate.c:1797` in `single_transfer` (see the `patch_file` field).
  Batch 2 excludes CVE-2026-9547: its whole fix body is a `keymatch = CURLKHMATCH_MISMATCH;`
  pair that already occurs in the frozen function, so no marker can satisfy the absence check.
  The other 99 open curl candidates from the zero-LLM resolver were triaged the same day
  (`reports/TRIAGE_REVIEW_20261031_CURL_OPEN.json`): 95 are `out_of_scope` (each basis quotes
  that other product's NVD description — PHP's ext/curl, Firefox's "Copy as cURL", WordPress
  plugins, routers, Zabbix, Couchbase, libexpat, the Ruby/Node curl wrappers), 3 are
  `confirmed_not_affected` (two wcurl rows: `scripts/wcurl` does not exist at 8.3.0; OSV-2025-657:
  the introducing commit 49a1cfae is behind the freeze and `ftp_pp_statemachine` is absent from
  `lib/`), and 1 stays `unknown` (`disc2_3dab3b7574adba0643f369ea` has no advisory id, alias or
  source URL). A follow-up (`reports/TRIAGE_REVIEW_20261031_CURL_FOLLOWUP.json`) reclassified
  CVE-2013-2617 (Ruby Curl Gem) and CVE-2024-32928 (Nest devices disabling
  `CURLOPT_SSL_VERIFYPEER`) from `possible_affected` to `out_of_scope`, and recorded
  CVE-2026-9547 and CVE-2026-5773 as `possible_affected` on the vendor range alone, because
  their fixes add no marker that distinguishes the frozen tree (9547's added lines already
  occur in `myssh_is_known`; 5773 introduces `PROTOPT_CONN_REUSE`, which 8.3.0 does not have).
  Four baseline curl rows (CVE-2023-38545, CVE-2023-46218, CVE-2024-11053, CVE-2025-0167) were
  already tiered from frozen-SHA fields and carry no promotion report; curl/curl now holds 56
  Ground Truth rows.

  Severity is the NVD CVSS 3.1 score (2023-46219 5.3 medium, 2024-2004 3.5 low, 2024-8096 6.5
  medium, 2024-2398 8.6 high); the curl advisory's own rating (Low, Low, Medium, Medium) is recorded
  in `severity.source`, because curl supplies no CVSS vector.
- **2 curl rows, 2 closures** settled 2026-10-31 at the frozen curl-8_3_0 snapshot
  (`reports/SWEEP_20261031_CURL_OPEN.json`): the two candidates the follow-up triage had kept
  `possible_affected` on the vendor range alone, now anchored and promoted.
  CVE-2026-5773 ("Wrong reuse of SMB connection", advisory `CURL-CVE-2026-5773`, affected 7.40.0
  through 8.19.0, backports 8.16.1 / 8.14.2) is promoted at `lib/url.c:1055-1491`
  (`ConnectionExists`, function granularity) with evidence type `source_review`: reuse is decided
  on the conncache key built by `hashkey` (`lib/conncache.c:125-148`, `scope_id/port/hostname`) and
  on TLS/proxy/connect-to/bind/credential properties (`lib/url.c:1190-1298`), never on the URL path;
  SMB keeps its connection alive (`connkeep`, `lib/smb.c:461`), its share is per-URL
  (`smbc->share` from `smb_parse_url_path`, `lib/smb.c:1176`, used by `smb_send_tree_connect`,
  `:686-698`), and `reuse_conn` (`lib/url.c:3286-3355`) discards the smbc parsed for the new URL by
  freeing the temporary connection (`:3354`), so the second transfer tree-connects to the first
  share — a read of the wrong file or a write into the wrong share for
  `smb://host/shareA/…` then `smb://host/shareB/…` with the same credentials (CWE-488). The
  8.20.0 fix `74a169575d` ("protocol: disable connection reuse for SMB(S)", ancestor of tag
  curl-8_20_0, compare ahead_by 184) removes `PROTOPT_CONN_REUSE` from the scheme table in
  `lib/protocol.c`; neither the flag nor that file exists at 8.3.0 (both handlers carry
  `PROTOPT_NONE`, `lib/smb.c:275` and `:303`), so the fix has no pre-image and the row is
  `source_review` rather than `fix_diff_comparison`.
  CVE-2026-9547 ("libssh: known_hosts key type mismatch reported as missing", affected 7.69.0
  through 8.20.0, fixed 8.21.0 / 8.20.1, libssh backend only) is promoted at
  `lib/vssh/libssh.c:334-561` (`myssh_is_known`, function granularity) with evidence type
  `fix_diff_comparison`: at 8.3.0 `case SSH_KNOWN_HOSTS_OTHER:` (`:446`) falls through to
  `keymatch = CURLKHMATCH_MISSING;` (`:453`) and only the `default:` arm assigns
  `CURLKHMATCH_MISMATCH` (`:456`), so a `CURLOPT_SSH_KEYFUNCTION` callback (`:513-517`) that accepts
  an unknown host (`:519-535`) accepts a key of the wrong type; the 8.21.0 fix `0b8dbbc63`
  (ancestor of tag curl-8_21_0, compare ahead_by 337) adds `keymatch = CURLKHMATCH_MISMATCH;` plus
  `break;` to that case, which the frozen file lacks (CWE-297). Both rows are T1 / `vendor_official`
  with severity level `low` and no score or vector, because the curl.se advisories rate both issues
  Low and publish no CVSS, matching the other curl Low rows.
- **1 caddyserver/caddy row, 1 closure** settled 2026-10-31 at the frozen v2.11.4 snapshot
  (`reports/SWEEP_20261031_CADDY_LODASH_EXPRESS_RAILS_GITEA.json`, 2 promotions + 3 triage
  decisions across five repositories). GHSA-6365-7ppr-5r92 ("Connection created for the wrong
  upstream for forward_auth + reverse_proxy", repository advisory, severity medium, no CVSS) is
  promoted at `modules/caddyhttp/reverseproxy/reverseproxy.go:663-666` (`proxyLoopIteration`,
  line granularity, T1 / `vendor_official`, category `race_condition`): reverse_proxy publishes
  the selected upstream through the request's mutable variable map
  (`caddyhttp.SetVar(r.Context(), dialInfoVarKey, dialInfo)` at :666, key
  `"reverse_proxy.dial_info"`, `hosts.go:332-334`) and the transport dial closure reads it back
  through `GetDialInfo` (`hosts.go:299-302`, `caddyhttp.GetVar(ctx, dialInfoVarKey)`) before
  `dialer.DialContext` (`httptransport.go:275-293`), so in a `forward_auth` + `reverse_proxy`
  chain the auth handler's write can land between RoundTrip and the lazy dial: the proxy
  transport dials the auth upstream and the resulting pooled connection serves proxy requests
  (spurious 404s, and a `forward_auth` check can pass against an endpoint that returns 200). The
  2.11.5 fix `1830809afe8c` (#7859) deletes exactly that block and attaches the `DialInfo` to a
  private immutable context key before the roundtrip (`context.WithValue(req.Context(),
  dialInfoCtxKey, di)`, `reverseproxy.go:1032-1042`); it is an ancestor of tag v2.11.5
  (`0a137e2f`; compare ahead_by 0, behind_by 89) and 30 commits after v2.11.4, so the pre-image
  is present. The advisory publishes no CWE; `CWE-362` is recorded as an analyst mapping in the
  checks note, and severity is the advisory's qualitative `medium` with no score/vector.
- **1 lodash/lodash row, 1 closure** settled 2026-10-31 at the frozen 4.17.23 snapshot (same
  report). CVE-2026-2950 ("Prototype Pollution via array path bypass in `_.unset` and `_.omit`",
  repository advisory, CVSS 3.1 6.5 MEDIUM `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L`, CWE-1321) is
  promoted at `lodash.js:4371-4414` (`baseUnset`, function granularity, T1 / `vendor_official`,
  category `integrity`): the CVE-2025-13465 guard skips every non-string segment
  (`if (typeof key !== 'string') { continue; }`, :4385-4390), `castPath` returns an array path
  unchanged (:4556-4561), and `parent()` -> `baseGet` stringifies each segment with `toKey`
  (:6678-6680, :3070-3080, :6856-6862), so
  `_.unset({}, [['constructor'], ['prototype'], 'toString'])` skips the `constructor`/`prototype`
  pair check (:4398-4409) and deletes a built-in prototype member
  (`Object`/`Number`/`String.prototype`); properties are deleted, behaviour is not overwritten,
  matching the advisory. The 4.18.1 fix `fe8d32ed` normalizes every segment with
  `var key = toKey(path[index]);` and rejects `constructor`/`prototype` as non-terminal keys
  unconditionally; it is an ancestor of tag 4.18.1 (`cb0b9b92`; ahead_by 0, behind_by 7) and 6
  commits after the frozen 4.17.23 tag commit `dec55b7a` (annotated tag object `fd6aaf94`).
- **3 candidates closed without promotion** in the same report, each on a full static read of the
  frozen tree. express CVE-2024-51999 is `confirmed_not_affected`: GHSA-pj86-cfqh-vqx6 was
  withdrawn on 2025-12-02 as "a correctness bug, not a vulnerability with real security impact",
  and the described behavior at 4.19.2 (`parseExtendedQueryString` calls
  `qs.parse(str, { allowPrototypes: true })`, `lib/utils.js:288-292`) only shadows keys on the
  requester's own `req.query`; the 4.x security patch `2f64f68c` was reverted on master by
  `697547cd` the same day. rails CVE-2024-26143 is `confirmed_not_affected`: the published rows
  are `>= 7.0.0, < 7.0.8.1` and `>= 7.1.0, < 7.1.3.1` (the earlier `>= 7.0.0` hit was a truncated
  range read), the frozen `RAILS_VERSION` is 8.0.4, and the fix `857f2e4a6a6c` is an ancestor of
  v8.0.4 whose hunk is present (`ERB::Util.html_escape(value)` for string defaults,
  `actionpack/lib/abstract_controller/translation.rb:26-30`). gitea CVE-2026-96580 is
  `out_of_scope`: the unbounded `strategy.matrix` expansion happens inside the pinned
  `gitea.com/gitea/act` module (`go.mod:301` replace of `nektos/act`, no `vendor/`, no
  `MaxJobNumPerRun` in the tree) and every in-tree site only forwards to `jobparser.Parse`
  (`services/actions/notifier_helper.go:362`), the same dependency-only shape as the next.js
  http-proxy row.
- **3 grpc/grpc rows** promoted 2026-10-31 from the 15 open candidates at v1.52.0
  (`reports/SWEEP_20261031_GRPC.json`): CVE-2023-33953 (`hpack_parser.cc:1049-1055`, `EmitHeader`
  — the metadata-size budget is compared per frame, because `BeginFrame` zeroes `frame_length_`
  for every CONTINUATION frame while the batch survives, and only after the field value has been
  buffered), CVE-2023-4785 (`tcp_server_posix.cc:206-221`, `on_read` — every accept4 errno other
  than EAGAIN/ECONNABORTED/EWOULDBLOCK, EMFILE included, jumps to `error:` and returns without
  re-arming the read closure), and CVE-2023-44487 (`frame_rst_stream.cc:105-127`,
  `grpc_chttp2_rst_stream_parser_parse` — a received RST_STREAM closes the stream without
  charging the peer anything). Markers are the three fix hunks: 6bb17232 (1.53.2 HPACK backport,
  `RandomEarlyDetection`), 2788b568 (PR #33656, `kRetryAcceptWaitTime`) and 6358f61d (PR #34637,
  `ping_on_rst_stream_percent`); none of those identifiers exists in the frozen tree. The other
  twelve candidates are resolved: CVE-2023-32732 and CVE-2024-7246 as `confirmed_not_affected`
  (every advisory range starts at 1.53.0, and the v1.52.0 `HPackTable::Memento` has no
  `parse_status` for the 2024-7246 poisoning), and ten as `out_of_scope` (CVE-2019-9515 whose
  upstream implementation list excludes gRPC; four c-ares CVEs, the `third_party/cares/cares`
  submodule being an empty directory at this SHA; four grpc/grpc-go CVEs; and CVE-2026-3381, a
  Perl Compress::Raw::Zlib row matched only through a distro package name).

- **12 libarchive/libarchive rows** promoted 2026-10-31 from the 14 open candidates at v3.7.7
  (`reports/SWEEP_20261031_LIBARCHIVE.json`). One row is T1/`vendor_official` from the repository's
  own GHSA: CVE-2026-45308 (`archive_write_set_format_zip.c:817-823`,
  `archive_write_zip_header` — the central-directory pathname length is stored in a 16-bit field,
  `cd_alloc()` only ever hands out a 64 KiB segment, and `copy_path()` memcpys the whole pathname,
  so a pathname over 64 KiB overflows the segment). The other eleven are T2/`unknown` on their NVD
  records: CVE-2025-1632 (`unzip/bsdunzip.c:879-901`, `list` — NULL pathname into `printf %s`),
  CVE-2025-25724 (`tar/util.c:744-752`, `list_item_verbose` — unchecked `strftime` into
  `char tmp[100]`), CVE-2026-4111 (`rar5.c:2963-2970`, `parse_filter` — the filter block length is
  never compared with the window), CVE-2026-16517 (`archive_write_set_format_zip.c:717-733`,
  `archive_write_zip_header` — encrypted-size additions overflow `int64_t`), CVE-2026-15028
  (`archive_read_support_format_tar.c:3324-3333`, `tar_atol_base_n` — `*++p` reads one byte past
  the field), CVE-2026-4424 (`archive_read_support_format_rar.c:2506-2511`, `parse_codes` — the
  LZSS window is not re-sized after a PPMd dictionary change), CVE-2026-17591
  (`archive_entry.c:1561-1570`, `archive_entry_copy_mac_metadata` — free before an aliased copy),
  CVE-2026-4426 (`iso9660.c:2758-2763`, `parse_rockridge_ZF1` — `pz_log2_bs` used in shift
  expressions without the 15..17 check), CVE-2026-5121 (`iso9660.c:1527-1538`, `zisofs_read_data`
  — `(ceil + 1) * 4` wraps on 32-bit; anchored at the allocation sink the advisory names, because
  the fix is the same `pz_log2_bs` validation as CVE-2026-4426), CVE-2026-5745
  (`archive_acl.c:1719-1727`, `archive_acl_from_text_nl` — `st = field[n].start + 1` before the
  empty-field check) and CVE-2025-60753 (`tar/subst.c:291-296`, `apply_substitution` — a
  zero-length global match never advances `name` while the replacement is appended). Every row was
  also checked the other way: the fix marker is absent from the frozen tree and first appears in
  the release named in the row (3.7.8, 3.8.2, 3.8.4/3.8.5, 3.8.6, 3.8.7, 3.8.8 or 3.8.9, verified
  by grepping the tagged trees). CVE-2025-60753's advisory claims `< 3.8.1` while the actual
  zero-length-match guard (df996732, PR #2787) landed after 3.8.3; the row records both. The two
  remaining candidates are `confirmed_not_affected`: CVE-2024-20696, whose fix eac15e25 (PR #2172)
  is already an ancestor of the frozen v3.7.7 commit, and CVE-2026-14164, whose dangling
  `filtered_buf` double free needs the calloc-failure early returns added by 620bdafa on master
  after 3.8.7 — the frozen `init_unpack()` reassigns both pointers unconditionally.
- **10 Gitea rows** promoted 2026-10-31 from the open-candidate sweep at v1.25.5
  (`reports/SWEEP_20261031_GITEA.json`), all T1/`vendor_official`, each anchored on the frozen
  statement the cited fix changes: CVE-2026-58428 (`services/release/release.go:321-329` — the web
  release-edit loop writes rename targets with `UpdateAttachmentByUUID(..., "name")` and never
  calls `upload.Verify` against `Repository.Release.AllowedTypes`, which the API path does;
  e4ef995f, PR #38314, 1.27.0), CVE-2026-58440 (`services/repository/collaboration.go:68-99` — the
  revocation cleanup drops watches and issue assignments but not user-created webhooks, and
  `services/webhook/deliver.go` only tests `IsActive`; no fix commit exists, the advisory's 1.27.0
  patch claim does not match any commit on main either), CVE-2026-73504
  (`routers/api/v1/repo/action.go:1635-1654` — the global artifact row is fetched before the signed
  URL is checked, so 401-vs-404 is an unauthenticated artifact-to-repository oracle;
  5fc3cec8/6e2cf106, PRs #39049/#39053, 1.27.3), CVE-2026-104636 (`modules/git/repo.go:204-233` —
  `git push` follows HTTP redirects with no policy recheck and no `followRedirects=false`, and the
  tree has no such setting; 1b127448, PR #39426, 28.0.0), CVE-2026-89430
  (`services/mirror/mirror_push.go:133-166` — push-mirror sync forces `git push --mirror` to the
  stored remote without revalidating it, while the LFS branch in the same function does enforce
  the migration list; same fix), CVE-2026-70357 (`services/migrations/dump.go:146-159` — the
  validated hostname is resolved again by the git subprocess at the clone sink; same fix),
  CVE-2026-104632 (`routers/web/repo/actions/view.go:477-505` — cancel leaves `NeedApproval` set
  and the rerun path moves the jobs back to `StatusWaiting`, which `CreateTaskForRunner` claims;
  patched in 28.0.0, no public commit), CVE-2026-101029 (`services/migrations/migrate.go:88-106` —
  the allow decision ORs over every resolved address, so one public answer hides an internal one;
  same 1b127448 fix; a distinct CVE record next to the CVE-2026-58442 row on the same block),
  CVE-2026-96400 (`modules/hostmatcher/hostmatcher.go:111-114` — `MatchBuiltinPrivate` tests only
  `ip.IsPrivate()`, so the reserved and link-local ranges that `migrations.Init` puts on the block
  list are never matched; 920b3f8c, PR #38039, the same fix commit as the CVE-2026-58314 row,
  which anchors the external-matcher branch at 108-110) and CVE-2026-28737
  (`web_src/js/render/plugins/3d-viewer.ts:48-56` — the pinned `online-3d-viewer@0.16.0` is embedded
  directly in the page document, so DOM the library writes from a crafted `.gltf` lives on the
  Gitea origin; d5831b9385eb, PR #37233, 1.26.0 moves the renderer into the sandboxed iframe).
  This decides all thirteen advisories that batch 8 and batch 9 deferred or left open, with three
  exceptions: GHSA-m984-2424-x6vw and GHSA-qg66-h68v-5x2h are `duplicate` of CVE-2026-58432 and
  CVE-2026-58420 (same file and line, same defect, the second advisory naming the other half of
  the patch), and CVE-2026-96580 stays `possible_affected` because the unbounded static matrix
  expansion it fixes lives in the pinned `gitea.com/gitea/act` jobparser, not in this tree. The
  sibling catalog rows for 58428, 58440 and 28737 were rewritten as `duplicate`.

Branch and PR resolution used while relocating anchors:

- Gitea CVE-2026-104627: the v1.25.5 backport `f270534e8396` (the proposals file only cited the
  main-branch `829b49c1ae96`).
- Echo: the v4 backport `b838391e2ead` (the v5 fix is `fc410094b2f3`); both rows share the commit.
- Tomcat: `933dcdb` is the 9.0.x fix (hunk old line 844 matches 9.0.117); `a102a2a` and `d35d9d2`
  are the 10.1.54 and 11.0.21 siblings.
- Django: `ad866a1c` is the 4.2.x fix and its `ipv6.py` pre-image blob matches the frozen 4.2.13
  tree; `4806731e` is the 5.1.x sibling.
- Vite: `c22c43de` is the main-branch fix; the frozen 5.0.11 file still carries the removed line
  verbatim and the advisory lists no 5.0-branch commit (5.0 is EOL, fixed in 5.4.19).
- cJSON CVE-2026-87933: the advisory cites PR #1065, merged as `6d9f2443ab07`; the proposals file
  records `no_fix_commit` for PR-only references, so the batch skipped it and it was applied
  directly after checking the PR merge.

### openssl 3.5.8 batch promotion (2026-10-31)

The 2026-09-29 advisory lists 14 CVEs and 13 of them cover `3.5.0 <= v < 3.5.9`. Each row is
anchored on the frozen 3.5.8 statement the 3.5-branch fix changes; the fix commit is the branch
commit whose message carries the `Fixes: CVE-...` trailer (NVD cites one commit per branch, so the
3.5-branch commit was picked by diffing against the 3.5.8 → 3.5.9 release):

| CVE | 3.5-branch fix | frozen anchor | anchor class |
|---|---|---|---|
| CVE-2026-35189 | `3842516cc15e` | `crypto/x509/v3_purp.c:387` | removed_line |
| CVE-2026-35191 | `0fe4442d4f8e` | `ssl/quic/quic_rx_depack.c:1501` | removed_line |
| CVE-2026-42772 | `ca8402e273af` | `ssl/quic/quic_sf_list.c:117` | removed_line |
| CVE-2026-54872 | `3f7e1363dcce` | `crypto/ec/ec_mult.c:216` | adjacent_insertion |
| CVE-2026-54873 | `279e7ee1392a` | `ssl/quic/quic_sf_list.c:42` | structural_shift |
| CVE-2026-54875 | `469f3e42629f` | `crypto/ec/ecp_sm2p256.c:283` | removed_line |
| CVE-2026-72897 | `4135f553c9d3` | `ssl/ssl_lib.c:5526` | adjacent_insertion |
| CVE-2026-75804 | `4533ee8a5686` | `ssl/quic/quic_fc.c:396` | removed_line |
| CVE-2026-75805 | `9eb2a8a9b861` | `crypto/cmp/cmp_client.c:1002` | removed_line |
| CVE-2026-75806 | `3a4589d015a9` | `ssl/record/methods/tls1_meth.c:259` | adjacent_insertion |
| CVE-2026-77696 | `6b90445a56b9` | `crypto/sm2/sm2_sign.c:289` | removed_line |
| CVE-2026-84782 | `906cf0ef1c85` | `ssl/statem/statem_dtls.c:1218` | adjacent_insertion |
| CVE-2026-84784 | `dba3c48d653c` | `ssl/quic/quic_channel.c:3384` | removed_line |

`removed_line` means the frozen statement is one of the lines the fix deletes. `adjacent_insertion`
means the fix is additive (constant-time top pinning for CVE-2026-54872, the `valid_flags` resize for
CVE-2026-72897, the record-length guard for CVE-2026-75806, the `init_off` reset for CVE-2026-84782)
and the anchor is the statement the inserted guard governs. `structural_shift` is the one honest
weak spot: the CVE-2026-54873 fix introduces `QUIC_RSTREAM_QPARAM` in
`ssl/quic/quic_strm_reas.c`, a file that entered the 3.5 branch with the CVE-2026-42772 reassembly
rewrite, so the hunk does not apply textually to the 3.5.8 `quic_sf_list.c`; the frozen line is the
equivalent packet-buffer retention site. Every row is T1/S2 with `advisory_review_status =
vendor_official`, the NVD severity/CWE/range, and the branch commit permalink in `references`.

The 105 openssl version candidates were resolved after that fix: 97 `confirmed_not_affected`, 7
`unknown`, 1 `out_of_scope`, none flipped to `possible_affected`. The 7 `unknown` are records that
name no evaluable range for the frozen tree rather than evidence of exposure: four carry CPE
configurations for the embedding product only (`php`, `emlog`, Mozilla NSS/`firefox`, and a
`diffie-hellman_key_exchange` project record), CVE-2025-9230 has a GIT range plus an affected-release
list but no version range (the resolver does not infer absence from a `versions` enumeration),
CVE-2025-27587 carries its only version range in `database_specific.extracted_events` with
`source=DESCRIPTION`, which the resolver deliberately ignores as a prose heuristic, and
CVE-2025-66109 has no OSV record. The `out_of_scope` record (CVE-2025-68169) affects the Linux
kernel only. All 8 stay open in the triage queue with their basis text.

### curl 8.3.0 batch promotion (2026-10-31)

`propose_locations.py` processed the 48 open curl candidates: 4 anchored in source code, 3 only in
test fixtures or `docs/` (weak evidence), 26 matched no removed line and 15 name no fix commit.
The four source anchors were verified by hand and admitted:

| CVE | advisory range | frozen anchor | fix (release) | anchor class |
|---|---|---|---|---|
| CVE-2023-46219 | 7.84.0 <= v < 8.5.0 | `lib/fopen.c:71` | `73b65e94` (8.5.0) | removed_line |
| CVE-2024-2004 | 7.85.0 <= v < 8.7.0 | `lib/setopt.c:2693-2698` | `17d302e5` (8.7.0) | removed_line |
| CVE-2024-8096 | 7.41.0 <= v < 8.10.0 | `lib/vtls/gtls.c:928` | `aeb1a281` (8.10.0) | removed_line |
| CVE-2024-2398 | 7.44.0 <= v < 8.7.0 | `lib/http2.c:1458` | `deca8039` (8.7.0) | removed_line |

For every row the frozen 8.3.0 statement is the pre-image of the fix hunk, the curl advisory JSON
and the NVD CPE match give the same start/end, and the release tag named above ships the fixed code
(`dirslash()` temp names, the destination-mask parse, the unconditional OCSP status check,
`free_push_headers()`) while the frozen tree does not. Three of the four anchors are the exact line
the fix deletes; CVE-2024-2004 is anchored on the caller block whose local mask the fix removes.
- **5 yaml-cpp rows** promoted 2026-10-31 from the 13 candidates at `yaml-cpp-0.6.2`
  (`reports/SWEEP_20261031_YAMLCPP.json`), all T2/`unknown` on their NVD/OSV records. Four are the
  stack-exhaustion family that the 0.7.0 `DepthGuard` closes: CVE-2017-5950
  (`src/singledocparser.cpp:48-60`, `HandleNode` — entry point of the unbounded recursion; issue
  #459), CVE-2018-20573 (`src/scanner.cpp:48-60`, `EnsureTokensInQueue` — the deepest frame of the
  same recursion; issue #655), CVE-2018-20574 (`src/singledocparser.cpp:275-303`, `HandleFlowMap` —
  key and value both re-enter `HandleNode`; issue #654) and CVE-2019-6292
  (`src/singledocparser.cpp:324-340`, `HandleCompactMap` — the first frame named in issue #657).
  All four cite 4edff1fa (PR #807), whose `DepthGuard<2000>` becomes 500 in the 0.7.0 release. The
  fifth is CVE-2017-11692 (`src/singledocparser.cpp:73-77`): `ParseProperties` consumes the only
  token of `!2`, the stream is already ended, and the following `m_scanner.peek()` asserts on the
  empty queue; fix c9460110e0 (issue #519, 0.7.0), while the PR #806 attempt was closed unmerged.
  None of these fixes is present in the frozen tag or in vanilla 0.6.3; Debian's 0.6.3-1 is a
  backport of PR #807, so the rows keep Debian's introduced-0/fixed-0.6.3-1 range while naming
  0.7.0 as the first upstream fixed release. The two resolver-cleared rows for 2017-11692 and
  2017-5950 (`confirmed_not_affected` from NVD's <= 0.5.3 CPE alone) are withdrawn and rewritten as
  `duplicate` of the promoted rows. CVE-2026-75432 and its catalog sibling are
  `confirmed_not_affected`: the 0.9.0 indent-deque underflow needs the sentinel-free storage added
  after 0.6.2, while `StartStream` here pushes a `NONE` marker that `PopIndentToHere` and
  `PopAllIndents` stop at and never pop. CVE-2018-20710 is a duplicate of CVE-2019-6285 — NVD
  rejected it as a typo of that id.
- **11 axios rows** settled 2026-10-31 at `v1.19.0` (ten new, one re-anchored;
  `reports/SWEEP_20261031_AXIOS.json`), all T1/`vendor_official`, closing the snapshot's
  remaining candidates: CVE-2026-101898 (the HTTP/2
  transport builds its session from `http2Options` alone, so `config.lookup` and proxy routing
  never reach `http2.connect`, `lib/adapters/http.js:457-468`), 101899 (CIDR `NO_PROXY` entries
  such as `10.0.0.0/8` are matched as literal host strings, `lib/helpers/shouldBypassProxy.js:296-328`),
  101900 (the fetch path merges headers from an inherited FormData `getHeaders`,
  `lib/helpers/resolveConfig.js:65-75`), 101901 (no `error` listener on the
  `ClientHttp2Session`, `lib/helpers/Http2Sessions.js:103-107`), 101902 (an inherited
  `Object.prototype.method` replaces the default GET, `lib/core/Axios.js:146-147`), 101903
  (quadratic backtracking in the `fromDataURI` media-type regex,
  `lib/helpers/fromDataURI.js:7-9`), 101904 (the post-interceptor `config.headers` read reopens
  the header gadget, `lib/core/dispatchRequest.js:34-37`), 101905 (inherited
  `createConnection`; the row is re-anchored to `lib/adapters/http.js:883-894` from 551-565,
  which pointed at the lookup wrapper the same commit moved into `normalizeLookup`), 101906
  (quadratic trailing-dot normalization reachable through a redirect `Location`,
  `lib/helpers/shouldBypassProxy.js:253-272`), 101908 (the raw `fetchOptions` object is passed as
  the fetch init, `lib/adapters/fetch.js:435-437`) and 101909 (`toFormData` reads `dots`,
  `indexes`, `metaTokens`, `maxDepth`, `visitor` and `Blob` off a flattened plain object that
  inherits `Object.prototype`, `lib/helpers/toFormData.js:102-123`). All eleven share one fix,
  `d19040bda7a8` (`fix: harden runtime option handling`, PR #11141, 2026-08-12, released in
  v1.20.0): it is 27 commits ahead of the frozen SHA and an ancestor of the v1.20.0 tag commit
  `84a9f3b9`, and the hunks it makes in each of the nine `lib/` files apply cleanly to the frozen
  tree (`git apply --check --include=<file>`). Severity is the GitHub CNA CVSS 4.0 score (7.0-8.3
  high, 6.9 medium); the batch carries no CVSS 3.1 metric. Three candidates (101903, 101905,
  101909) carry a stale legacy `source_candidate_status=rejected` that contradicts their own
  `reason` field (the npm range contains v1.19.0), NVD's `Awaiting Analysis` status and OSV's
  `github_reviewed: true`; the flag is not adopted. CVE-2026-101907, the redirect-based SSRF
  already promoted from the earlier dossier, stays as it was.
- **10 echo rows** settled 2026-10-31 at `v4.15.2` (nine new positives and one
  `confirmed_not_affected`; `reports/SWEEP_20261031_ECHO.json`), all from repo-owned
  advisories classified T1/`vendor_official`, closing the snapshot's remaining candidates:
  CVE-2026-118653 (default `RealIP()` trusts `X-Forwarded-For`, so the default rate limiter's
  identifier is attacker-chosen, `context.go:313-330`), 118651 (the proxy forwards a
  client-supplied `X-Real-IP` whenever `IPExtractor` is unset,
  `middleware/proxy.go:349-351`), 118655 (the static middleware unescapes an already decoded
  `URL.Path`, so double-encoded separators reach a guarded route,
  `middleware/static.go:169-173`), 118654 (`path.Clean` collapses encoded dot-dot after
  routing, serving files behind route middleware, `middleware/static.go:183`), 118656
  (`sanitizeURI` only inspects offsets 0 and 1, so a leading TAB hides the double slash,
  `middleware/slash.go:122-129`), 118260 (BodyDump captures whole request and response bodies
  with no cap, `middleware/body_dump.go:69-81`), 118264 (the proxy picks the raw tunnel from
  `IsWebSocket()` before the upstream accepts the upgrade, bypassing route middleware,
  `middleware/proxy.go:386-391`), 118262 (the raw tunnel waits for both copy directions
  without closing the peer, retaining handlers and connections,
  `middleware/proxy.go:170-181`) and 118261 (the decompressed body is exposed without a size
  cap, `middleware/decompress.go:90-93`). The nine share four v4 fix commits:
  `c3fa2a27ff92` (v4.15.3, PR #3011) for 118655; `b838391e2ead` (v4.16.0) for 118654 and
  118656; `3fb0ba7e1764` (v4.16.1) for 118260, 118264, 118262 and 118261; `ebbb855f5827`
  (v4.16.3, PR #3197) for 118651 and 118653. Each fix was checked hunk by hunk with
  `git apply --check` against the frozen checkout: twelve of the sixteen hunks that carry a
  fix apply cleanly; for the two proxy/static files whose hunks trail into later refactors the
  exact removed lines were matched verbatim instead (the reasons are in each row's
  `checks_note`). CVE-2026-118658 (Scheme injection through the redirect middlewares) is
  `confirmed_not_affected`: the frozen snapshot *is* the v4.15.2 tag commit, that release's
  CHANGELOG records the `isValidProto` fix (#2962), and `context.go:288-310` validates every
  forwarded scheme header. Severity is the advisory record: CVSS 3.1 5.3-6.1 for six rows and
  CVSS 4.0 9.1 for 118264; the three advisories without a CVSS metric (118260, 118262, 118261)
  carry the advisory level with score null. The four pre-existing adv3 echo rows were
  re-stamped from `github_reviewed` to `vendor_official` because their `advisory_url` is the
  same repo-owned advisory endpoint, so the repository is stable under
  `assign_trust_tiers.py`.
- **10 werkzeug rows** settled 2026-10-31 at `3.0.2` (five new positives, five
  `duplicate`; `reports/SWEEP_20261031_WERKZEUG.json`), all from repo-owned
  `pallets/werkzeug` advisories classified T1/`vendor_official`, closing the snapshot's remaining
  candidates. All five are the `safe_join()` guard in `src/werkzeug/security.py`: CVE-2024-49766
  (a UNC path `//server/share` is not absolute to `ntpath.isabs` on Python < 3.11, so the
  pathname escapes the trusted directory, :147-152, fixed by `87cc78a25f78`, 3.0.6),
  CVE-2025-66221 (no Windows device-name filtering, so `CON`/`NUL`/`AUX` are joined and the read
  hangs, :143-153, `9bdec46fe495`, 3.1.4), CVE-2026-21860 (the 3.1.4 filter used
  `os.path.splitext`, so `CON.txt.html` and `CON ` bypassed it, :147-152, `37797aba2600`, 3.1.5),
  CVE-2026-27199 (`normpath` validates the whole pathname once, so a trailing segment such as
  `example/NUL` passes, :143-145, `f54fe9802625`, 3.1.6) and CVE-2026-102598 (the 3.1.5 check does
  not strip an empty ADS marker, so `NUL:` passes, :147-152, `b2a2c0973008`, 3.1.9). Each fix
  commit is `behind_by` 0 of the release that shipped it; only the 2024 hunk applies to the 3.0.2
  tree with `git apply --check` (offset -4), because the three device-name follow-ups assume code
  added in 3.1.4-3.1.6 — at 3.0.2 `_windows_device_files`, `splitext`, `.partition('.')` and
  `.partition(':')` are all absent, so the vulnerable state is established by verbatim line checks
  and the absence of any device-name filtering. The five OSV/PYSEC disc2 siblings are
  `duplicate` aliases of the same CVEs and fix commits. Severity is the advisory CVSS 4.0 record
  (6.3 medium for all five: `VA:L` for the device-name hangs, `AC:H`/`VC:L` for the UNC row).
- **9 guzzle rows** settled 2026-10-31 at `7.14.1` (five new positives, four `duplicate`;
  `reports/SWEEP_20261031_GUZZLE.json`), all from repo-owned `guzzle/guzzle` advisories,
  T1/`vendor_official`: CVE-2026-67353 (the cookie jar accepts unlimited `Set-Cookie` fields and
  assembles them into one uncapped `Cookie` header, `src/Cookie/CookieJar.php:291-301`, fix
  `7b68220d6543`, 7.15.1), CVE-2026-67354 (the referer redirect option keeps the URI fragment in
  the generated `Referer`, `src/RedirectMiddleware.php:205-209`, same fix), CVE-2026-67355 (a
  `Set-Cookie` without `Domain` is stored with the request host and re-matched as a normal domain,
  so host-only cookies leak to subdomains, `CookieJar.php:239-244`, same fix), CVE-2026-69245
  (`isIpAddressOrNumericHost` only accepts `FILTER_VALIDATE_IP` or an all-numeric last label, so
  `0x7f000001` and percent-escaped cookie domains keep subdomain scope,
  `src/Cookie/SetCookie.php:480-501`, fix `744101956d78`, 7.15.2) and CVE-2026-69246
  (`CurlFactory::getDefaultConf` hands libcurl the URI text in `CURLOPT_URL` while sending `Host`
  separately, so a percent-encoded authority reaches a host the application excluded,
  `src/Handler/CurlFactory.php:1744-1747`, same fix). The 7.15.1 commit is 38 commits after the
  frozen SHA and its `CookieJar`/`SetCookie`/`RedirectMiddleware` patches apply cleanly; the
  7.15.2 commit is 40 after and its `Client`/`CurlHandler`/`StreamHandler`/`HostValidator` patches
  apply cleanly, while the `SetCookie` and `CurlMultiHandler` hunks trail into 7.15.1 context and
  their pre-images were matched verbatim (no percent-escape guard, no inet_aton numeric check, no
  `HostValidator.php` at 7.14.1). The four sweep hits (GHSA-32rq-jhr7-m3hh, -3fvr-2jw6-crq4,
  -mqq9-gxg5-m58g, -mjrx-74jh-7xgw) are GitHub-withdrawn duplicates that redirect to
  GHSA-94pj-82f3-465w (CVE-2026-67339, already in GT) and to the three 7.15.1 advisories above, so
  they are triaged `duplicate`. Severity is the advisory CVSS 3.1 record: 5.3/5.9/5.9/6.5 medium
  and 7.2 high (`S:C` for 69246).
- **12 vite rows** settled 2026-10-31 at `v5.0.11` (two new positives, two re-promoted, six
  `out_of_scope`, one `confirmed_not_affected`, one left open; `reports/SWEEP_20261031_VITE.json`),
  from repo-owned `vitejs/vite` advisories, T1/`vendor_official`: CVE-2026-112946
  (`importAnalysisPlugin` records `fsPathFromUrl(stripBase(url, base))` — a URL-derived path —
  into `safeModulePaths` instead of the resolved id, so an in-root import whose URL is
  `/etc/hostname` authorizes the host file for a later `/@fs/etc/hostname` request,
  `packages/vite/src/node/plugins/importAnalysis.ts:531-538`, fix `e570d8d01609`, 6.4.4),
  CVE-2026-53571 (on Windows, NTFS ADS suffixes and 8.3 short names bypass the fs.deny glob
  because `isFileServingAllowed` rejects neither `:` nor `~`, `static.ts:212-216`, fix
  `96b0c10162`, 6.4.3, CVSS4 8.2), CVE-2026-112945 (`getHtmlFilename` joins the uncleaned
  request URL into `path.join(root, …)` and the attacker-supplied `htmlPath` becomes
  `proxyModuleUrl`, `indexHtml.ts:100-104`, fix `7dafd8e56f15`) and CVE-2025-46565 (the fs.deny
  decision is made on the pre-normalization URL in `serveStaticMiddleware`, so `/.env/.` passes
  the check and sirv still serves `root/.env`, `static.ts:151`, fix `c22c43de6`). 112945 and 46565
  had been promoted earlier with an `affected_range` copied from the first advisory row
  (`>=8.3.0,<8.3.3` and `>=6.3.0,<6.3.4`), which does not contain v5.0.11; both were re-promoted
  with `--replace` and the covering ranges (`<=6.4.3` and `>=5.0.0,<=5.4.18`). All four fix hunks
  target 6.x refactors and fail `git apply --check` at v5.0.11, so the pre-images were matched
  verbatim and every guard the fix adds is absent from the frozen file. Six candidates are
  dependency-only and `out_of_scope`: five launch-editor CVEs (112942, 112943, 112944, 53632,
  2024-52011 — the code is in `vitejs/launch-editor`, vite only declares
  `launch-editor-middleware ^2.6.1`) and CVE-2025-58751 (sirv's `join`/`startsWith` containment;
  vite's fix only updates `patches/sirv@2.0.4.patch`, and the frozen `sirv@2.0.3.patch` carries
  none of the affected sirv source). GHSA-8g5g-mxqh-grgj / CVE-2026-118662 is
  `confirmed_not_affected`: it lists 6.4.4 only, the regression introduced by that release's
  incomplete backport. CVE-2025-62522 is `confirmed_not_affected`
  (`reports/TRIAGE_20261031_TOMCAT_VITE.json`): v5.0.11 compiles `server.fs.deny` with picomatch
  `matchBase: true` (`server/index.ts:620`), and picomatch 2.3.1's `matchBase` tests
  `path.basename(input)`, so a request target ending in `\` becomes a trailing `/` but the
  basename is still `.env` and the deny check at `static.ts:216` refuses it. The bypass needs the
  5.2.6+ matcher (patterns expanded to `**/<pattern>`, `matchBase: false`, `index.ts:688-698`),
  which is exactly where the vendor's 5.x row starts; 5.2.5 still uses `matchBase: true`.
- **8 rack rows** settled 2026-10-31 at `v3.1.13`
  (`reports/SWEEP_20261031_RACK.json`), all T1/`vendor_official` from repo-owned `rack/rack`
  advisories, on top of the 14 rows already in GT at this snapshot. The OSV GIT "fixed" events
  name only the 3.1.21/3.1.22 release bumps, so the code changes were recovered from the
  `v3.1.20...v3.1.21` and `v3.1.21...v3.1.22` compares: CVE-2026-26961 (the greedy
  `MULTIPART` regex resolves several `boundary=` parameters to the last one, so a proxy/WAF that
  honours the first parses a different body structure, `lib/rack/multipart/parser.rb:80-84`,
  fix `10626530f3`), CVE-2026-34827 (the quoted-value loop at `parser.rb:337-358` re-searches
  and `slice!`s the remaining disposition once per escape, super-linear on escape-heavy names,
  fix `17ce7836be`), CVE-2026-34763 (`path.sub(/^#{root}/, '')` interpolates the configured root
  unescaped, so a metacharacter in the root defeats the prefix strip and the listing renders the
  absolute path, `lib/rack/directory.rb:53-55`, fix `29b17c58e5`), CVE-2026-34829 (`BoundedIO`
  is applied only when Content-Length is present and `read_data` at `parser.rb:258-261` keeps no
  total, so chunked uploads are unbounded, fix `367a2a0ec6`), CVE-2026-34230 (wildcard expansion
  re-runs `accept_encoding.map(&:first)` inside the loop, `lib/rack/utils.rb:197-207`, fix
  `55db26e7f4`), CVE-2026-32762 (`forwarded_values` splits on `;` before honouring quoted
  strings, `utils.rb:149-160`, fix `9df5d34d4f`), CVE-2026-26962 (obs-fold CRLF survives
  unfolding into `filename`/`name`, `parser.rb:306-311`, 3-1-stable backport `ae320b4661`) and
  CVE-2026-34831 (`Content-Length` from `body.size` understates a multibyte error body,
  `lib/rack/files.rb:190-200`, fix `c3645d377f`). Every advisory carries per-branch rows
  `<2.2.x`, `>=3.0,<3.1.21` (26962: `<3.1.22`) and `>=3.2,<3.2.6`; the 3.1 row contains the
  frozen tag. Five patches apply with `git apply --check`; the three parser.rb fixes fail only
  on hunks whose context uses identifiers from later 3.1.x releases (FWS/HEADER_VALUE from
  3.1.16, BUFFERED_UPLOAD_BYTESIZE_LIMIT from 3.1.17, PARSER_BYTESIZE_LIMIT from 3.1.21), and
  their substantive hunks were replayed individually (26961 hunk 2 at line 81, 34827 hunk 3 at
  347, 34829 hunks 2/4/5 at 90/215/258).
- **1 undici row, 6 not affected** settled 2026-10-31 at `v5.19.0`
  (`reports/SWEEP_20261031_UNDICI.json`). The seven candidates were discovered from OSV records
  whose ranges are GitHub first-branch rows (`< 6.27.0`, `< 6.28.0`, `< 6.28.1`, rendered as
  `introduced 0`), so the collapsed ranges mathematically cover the frozen tag; static review of
  the frozen tree decides each one. CVE-2026-1528 is promoted: `ByteParser.run` reads the 64-bit
  extended payload length as `(upper << 8) + lower` after rejecting only `upper > 2^31 - 1`
  (`lib/websocket/receiver.js:194-216`), so any upper word above 2^23 - 1 makes the shift produce
  a negative or truncated length and the parser consumes the wrong byte count and throws an
  uncaught `TypeError`. The 6.24.0 fix `5a97f089` (recovered from the `v6.23.0...v6.24.0`
  compare; the advisory carries no commit refs) rejects `upper !== 0 || lower > 2^31 - 1` and
  assigns `lower`; the 6.23.0 pre-image is identical in the changed lines. The record extends the
  vendor row `>=6.0.0,<6.24.0` to `>=0.0.0,<6.24.0` because 5.x ships the same code and has no
  fix, matching the CVE-2026-1527 row already in GT. The other six are `confirmed_not_affected`
  because the vulnerable API or feature does not exist at v5.19.0: no retry interceptor
  (CVE-2026-16728, 18540 — the fixes touch `lib/handler/retry-handler.js`, and `lib/handler/`
  holds only `DecoratorHandler.js` and `RedirectHandler.js`), no cookie percent-decoding
  (CVE-2026-9679 — `lib/cookies/parse.js` trims the value and never calls
  `decodeURIComponent`/`qsUnescape`, and the advisory says the decoding was introduced in
  undici 7), no permessage-deflate negotiation (CVE-2026-2229, 1526 — `connection.js:83` leaves
  `permessageDeflate = ''` with a TODO and `:159-161` fails a server that answers with the
  extension, so there is no `PerMessageDeflate` and no `permessage-deflate.js`), and no
  `maxPayloadSize` (CVE-2026-12151 — the vendor says affected releases start at 6.17.0 and the
  6.27.0 backport `b7f252e7` modifies `maxPayloadSize` bookkeeping, which appears nowhere under
  `lib/` in the frozen tree; the uncapped `#fragments` accumulation is a different, unassigned
  weakness).

- **5 tokio rows, 1 duplicate** settled 2026-10-31 at `tokio-1.8.0`
  (`reports/SWEEP_20261031_TOKIO.json`), on top of the one row already in GT at this snapshot
  (CVE-2021-38191). All six candidates sit inside their vendor version rows at 1.8.0. The OSV GIT
  `fixed` events in these records are not code fixes (`2273eb1a` "chore: fix CI on master",
  `2a3c803d`/`9241c3ed`/`1a997ffb`/`ba81945f` release prep), so each fix was recovered from the
  release compare or the fixing PR and then checked against the frozen tree:
  CVE-2021-45710 (`State::set_complete` is a bare `fetch_or(VALUE_SENT, AcqRel)`, so a send racing
  receiver close publishes the bit on a closed channel and both sides touch the value
  `UnsafeCell`, `tokio/src/sync/oneshot.rs:854-860`, fix `e0cf906ae1` from the
  `tokio-1.8.3...tokio-1.8.4` compare), CVE-2023-22466 (`pipe_mode` overwrites the whole
  `dwPipeMode` DWORD and clears the default `PIPE_REJECT_REMOTE_CLIENTS`, so `reject_remote_clients`
  is silently undone, `tokio/src/net/windows/named_pipe.rs:1449-1456`, fix `9ca156c0b8`, PR #5336;
  the module is `cfg(windows)` and not compiled on the Linux checkout), RUSTSEC-2023-0005
  (`ReadHalf::unsplit` moves `T` out of `Inner<UnsafeCell<T>>` without a `T: Unpin` bound,
  `tokio/src/io/split.rs:77-89`, fix `d6ea7a742b`), RUSTSEC-2025-0023 (slots are `RwLock`-guarded
  and `RecvGuard::clone_value` calls `T::clone` through shared read guards while the channel only
  requires `T: Send`, so a `!Sync` value is cloned in parallel, `tokio/src/sync/broadcast.rs:1060-1065`,
  fix `4b174ce2c9` replaces the lock with a `Mutex`) and RUSTSEC-2026-0386 (`AsyncFd::new` and
  `with_interest` are safe functions over any `T: AsRawFd` and register a descriptor the caller need
  not own, `tokio/src/io/async_fd.rs:175-196`, fix `fb57e675b0`/PR #8587 makes registration an
  `unsafe fn`). Three patches apply with `git apply --check` (oneshot, named pipe, split); the
  broadcast and async_fd patches are from 1.38.x/1.51.x branches and do not apply wholesale, so
  their pre-image lines were verified by direct read (of the broadcast patch only the three
  hunks touching the slot lock and the `Recv` projection apply individually). RUSTSEC-2026-0386 has no CVE/GHSA alias or CVSS, so it is the
  only T2/`unknown` row here; the other four are T1. The sixth candidate
  (`adv3_261c1f2dd536e5cd`) is the vendored-range duplicate of the promoted CVE-2023-22466
  candidate and is closed as `duplicate`.

- **2 libexpat rows, 3 duplicates, 1 left open** settled 2026-10-31 at `R_2_6_2`
  (`reports/SWEEP_20261031_LIBEXPAT.json`), on top of the 29 rows already in GT at this snapshot.
  CVE-2026-66046 is anchored by fix-diff comparison: `storeAtts` rescans
  `elementType->defaultAtts` linearly for every non-normalized attribute value, so one element
  with many attributes costs O(N²) (`expat/lib/xmlparse.c:3453-3461`, fix `f8f7c4ff` in PR #1321,
  contained in `R_2_8_4`). The loop matches the fix pre-image line for line except `int j` vs
  `size_t j`, and the hash-table half of the fix (`defaultAttForName`) does not exist at 2.6.2,
  so `git apply --check` fails and the pre-image was verified by direct read. CVE-2025-59375 is
  the one `source_review` row: every opening tag not served from the free-tag list allocates a
  `TAG` plus a 32-byte buffer and stays live on the tag stack until its end tag
  (`expat/lib/xmlparse.c:2981-2989`), which upstream issue #1018 measured at 120 bytes per
  3-byte tag and 70.77× amplification; the shipped fix (PR #1034, merge `ac7a27e1`, contained in
  `R_2_7_2`) is a parser-wide `MALLOC`/`FREE` tracker that aborts past 64 MiB and 100× direct
  input, with no hunk at the allocation, so no fix-diff anchor exists at this site. Both rows are
  T2/`unknown` (NVD/OSV records only, no reviewed GHSA); OSV's `fixed` event for 59375,
  `7643f96b`, is the release-prep merge #1038 and is not used as the fix commit.
  CVE-2025-66382 stays `possible_affected`: issue #1076 is still open, the details are NDA-bound,
  there is no fix commit and no public root cause to anchor at this SHA; its NVD-only sweep
  candidate is closed as a duplicate, as are the Debian alias rows for 59375 and 66046.

- **2 rustls rows, 2 duplicates, 1 not affected** settled 2026-10-31 at `v/0.23.4`
  (`reports/SWEEP_20261031_RUSTLS.json`), on top of the row already in GT at this snapshot
  (CVE-2024-32650). GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) is anchored on the
  `#[derive(Debug)]` of `Tls13ClientSessionValue` (`rustls/src/msgs/persist.rs:71-72`):
  both public session types derive `Debug`, and so does the `ClientSessionCommon` they embed
  (`:204-210`) with `secret: Zeroizing<PayloadU8>` (`:207`); `PayloadU8`'s manual `Debug`
  hex-dumps its bytes (`rustls/src/msgs/base.rs:189-193`) and `zeroize 1.7.0` derives `Debug`
  for `Zeroizing`, so `{:?}` on a session value prints the TLS 1.3 resumption PSK or TLS 1.2
  master secret, and both types are re-exported from `rustls::client` (`lib.rs:560`). The
  0.23 fix `dcdb9464` removes the derives and hand-writes `Debug` impls that skip `secret`;
  its regression test asserts the 0xa5 secret bytes are absent from the output.
  GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) is anchored on the early `set_kx_hint` in
  `handle_server_hello` (`rustls/src/client/tls13.rs:150-154`): the client stores the server's
  chosen group before certificate/Finished verification, and `initial_key_share` reads the hint
  back at `:207` to start exactly one key exchange, so a forged ServerHello that fails later
  still pins the group offered by later ClientHellos for that name. The 0.23 fix `f04804fa`
  moves the write to `ExpectFinished` and threads `kx_group` through the handler states. Both
  fixes are contained in `v/0.23.46` (`compare v/0.23.46...<sha>` reports `ahead_by 0` or
  `identical`); the parallel 0.24-dev commits `f5f7bf50` and `8fa0dc5d` are not release-branch
  fixes, and `git apply --check` fails for both patches because v/0.23.4 predates the branch's
  ECH and session-type changes, so the pre-image lines were verified by direct read. At 0.23.4
  the configured providers have no hybrid/PQ group, so for w44r only the pre-authentication
  hint poisoning is present. Both rows are T1/`vendor_official`; the advisory records carry no
  CVE and no CWE, so `cwe_ids` is empty. GHSA-h2v8-394m-p7vv is `confirmed_not_affected`:
  Brotli certificate decompression does not exist at the SHA (`rustls/src/compress.rs` absent,
  no brotli dependency, no `CompressedCertificate` handling) and RUSTSEC-2026-0348 puts its
  introduction at 0.23.9. The two RUSTSEC sibling candidates are closed as duplicates; the
  other two candidates at this snapshot had already been closed by the range pass
  (CVE-2024-11738 introduced 0.23.13, GHSA-vp88 introduced 0.23.44).

- **5 ImageSharp rows** settled 2026-10-31 at `v3.1.6`
  (`reports/SWEEP_20261031_IMAGESHARP.json`), on top of the four rows already in GT at this
  snapshot (CVE-2025-27598 plus CVE-2026-106114, 106117 and 106118). All five are T1/
  `vendor_official`, S2, `fix_diff_comparison`, and the frozen SHA is the `v3.1.6` tag commit
  (`compare v3.1.6...313a7e8d` is `identical`). CVE-2025-54575 (GHSA-rxmq-m78w-7wmc) is anchored
  on `GifDecoderCore.ReadComments` (`src/ImageSharp/Formats/Gif/GifDecoderCore.cs:381-411`): the
  loop condition `while ((length = stream.ReadByte()) != 0)` lets the EOF byte `-1` through the
  max-length guard, and with `SkipMetadata` set the body's `stream.Seek(length, ...)` rewinds one
  byte, so an unterminated comment block never terminates; the v3.1.11 backport `f4a26847` adds
  the `length == -1` throw and is the tag commit (`833f3cee` carries the same lines but is
  diverged). CVE-2026-106110 and CVE-2026-106115 are the two CCITT encoders, anchored on
  `T4BitCompressor.CompressStrip` (`.../T4BitCompressor.cs:39-127`) and
  `T6BitCompressor.CompressStrip` (`.../T6BitCompressor.cs:53-132`):
  `TiffCcittCompressor.Initialize` (`:529-531`) allocates `Width * rowsPerStrip` bytes, but T4
  needs up to 13 bits per pixel plus EOL/EOL-padding codes and T6 up to 16 bits per pixel plus the
  EOFB, while `WriteCode` (`:466`) writes through `BitWriterUtils.WriteBit`
  (`BitWriterUtils.cs:52-55`) and an unchecked `Unsafe.Add`; the v3.2.0 fix `baa37cd1` gives each
  subclass a `GetMaximumEncodedBits` bound, sizes the buffer from it and makes `WriteCode` throw
  when the remaining bits are insufficient. CVE-2026-106113 is anchored on
  `ColorNumerics.GetBT709Luminance` (`src/ImageSharp/Common/Helpers/ColorNumerics.cs:29-30`): the
  float dot product is neither NaN-checked nor clamped, and `GrayscaleLevelsRowOperation{TPixel}`
  (`:60-61`), `GlobalHistogramEqualizationProcessor{TPixel}` (`:133`) and
  `AutoLevelProcessor{TPixel}` (`:152`) use the result as the offset of an `Unsafe.Add` into the
  histogram, so an out-of-range or NaN luminance indexes outside it. CVE-2026-106116 is anchored
  on `ExifReader.ReadValues64` (`src/ImageSharp/Metadata/Profiles/Exif/ExifReader.cs:199-211`):
  the entry count comes from the file, and `ReadValue64` (`:418-423`) returns without advancing
  when fewer than 20 bytes remain, so a BigTIFF count larger than the remaining directory bytes
  keeps the loop running for the full declared count; the same `baa37cd1` bounds it by
  `(remaining - 8) / 20`. `baa37cd1` is the `v3.2.0` tag commit (`compare v3.2.0...baa37cd1`
  identical); the 4.x equivalents `a9498c6d`, `c4c4bf29` and `92b12d72` are in `v4.1.2` and are
  not this branch. The hunk pre-images match the frozen files verbatim but at different offsets,
  because the fix commits also insert unrelated methods on the maintained branch, so every
  pre-image was verified by direct read rather than `git apply --check`. The GIF advisory API
  reports no CWE; its CVE/OSV record lists CWE-400 and CWE-770, which the row uses. Ranges:
  `>=3.0.0,<3.1.11` (GIF), `>=2.0.0,<3.2.0` (106110, 106113, 106116) and `>=2.1.0,<3.2.0` (106115).

- **1 Jenkins row** settled 2026-10-31 at `jenkins-2.441`
  (`reports/SWEEP_20261031_JENKINS.json`), on top of the 36 rows already in GT at this snapshot:
  CVE-2025-67639 (SECURITY-1166, GHSA-6837-qgrc-x5p6) is T1/`vendor_official`, S2,
  `fix_diff_comparison`, anchored on `AuthenticationProcessingFilter2`
  (`core/src/main/java/hudson/security/AuthenticationProcessingFilter2.java:55-63`, function
  granularity, range `>=0,<2.528.3`): the filter registered for `j_spring_security_check`
  (`SecurityRealm.java:223-228`, instantiated at `:599`) overrides only
  `successfulAuthentication` (`:66`) and `unsuccessfulAuthentication` (`:93`) and never
  `attemptAuthentication`, so the credential POST is authenticated without a Jenkins crumb, while
  `login.jelly:77-78` and the setup-wizard token form post no crumb field — a cross-site form
  submits the attacker's credentials in the victim's browser and logs the victim into that
  account. Fix `31598feb` (2.541 / 2.528.3) adds the `attemptAuthentication` crumb check and the
  hidden `${h.getCrumb...}` inputs; its hunk pre-image does not apply verbatim because the fix
  branch already uses `PathPatternRequestMatcher` while 2.441 constructs
  `new AntPathRequestMatcher(...)` at `:59`, so the pre-image was verified by direct read. Five
  other open candidates on this snapshot were closed the same day: CVE-2025-59475 as
  `confirmed_not_affected` (the fixed `jenkins/model/navigation/UserAction/jumplist.jelly` and the
  whole `jenkins.model.navigation` package were introduced on 2025-04-18 by the header redesign
  `c42ab43c`, after this snapshot, and the 2.441 header renders only a profile link and logout);
  CVE-2025-59476, CVE-2024-43044 and CVE-2026-84655 as `out_of_scope` (the vulnerable code is
  `io.jenkins.lib:support-log-formatter` 1.2 copied at `war/pom.xml:564-576`, `fetchJar` in
  remoting `3206.vb_15dcf73f6a_9` pinned at `pom.xml:89`, and Stapler/json-lib behind
  `Api.doJson`/`Api.doPython` calling `serveExposedBean(...Flavor.JSON/JSONP/PYTHON)`, whose core
  fix `56fe87ef` is test-only); and CVE-2026-70427 as `duplicate` of the CVE-2026-33001 row at
  `FilePath.readFromTar:3082` (its advisory calls it an incomplete fix of SECURITY-3657, and the
  3657 guard its hunk patches does not exist at 2.441, where the whole tar extraction path is
  still unvalidated).

## Status

Draft. No vulnerability was dynamically reproduced. S2 labels are carried from the prior workflow
where each had an advisory URL plus a fixed-SHA static root-cause location; the added rows were
checked statically against their advisories and fix diffs. Thirty-four frozen SHAs have
`PASS_KNOWN_SWEEP` and 13 still need review; 6 relevant candidates remain open, all
`possible_affected` (next.js 4 — CVE-2026-23869/23870/64641/94482 —, spring-framework 1 —
CVE-2026-41849, libexpat 1 — CVE-2025-66382), and 7 legacy `unknown` triage rows have no
candidate row behind them any more (they block the coverage upgrade of their snapshots until
resolved). The 43-row QA sample is reviewed and all `pass`. The dataset validates with `--draft`
(721 positives, 1405 candidates, 0 errors, 0 warnings); release-mode validation still fails by
design, on the 13 `NEEDS_REVIEW` snapshots and the three repositories that are not frozen yet
(metadata + queue only; openssl is frozen and swept).

## Re-run checks

```bash
cd /home/luchitong/work/repo-vuln-bench-v040
python3 scripts/validate_dataset.py /home/luchitong/work/repo-vuln-bench-v040-dataset --draft
python3 -m unittest discover -s tests -v
# annotation / sampling (dry-run by default)
python3 scripts/assign_trust_tiers.py /home/luchitong/work/repo-vuln-bench-v040-dataset
python3 scripts/qa_sample.py /home/luchitong/work/repo-vuln-bench-v040-dataset --rate 0.15
# candidate resolution and location proposals (dry-run by default)
python3 scripts/resolve_version_candidates.py /home/luchitong/work/repo-vuln-bench-v040-dataset
python3 scripts/propose_locations.py /home/luchitong/work/repo-vuln-bench-v040-dataset
python3 scripts/promote_from_proposals.py /home/luchitong/work/repo-vuln-bench-v040-dataset
```
