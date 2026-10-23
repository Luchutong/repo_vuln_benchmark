# Independent audit — range/scope triage pass (2026-10-23)

Auditor: independent check of `runs/triage_range_scope_2026-10-23/`, asked to
decide whether the two proposed conversions are sound to apply.

Artifacts audited (md5):

| file | md5 |
|---|---|
| `runs/triage_range_scope_2026-10-23/proposals.jsonl` | `f2203a9611bced0afa2fe97f93530d60` |
| `v031/scripts/triage_range_scope.py` | `9aa40c191c3d2b28b477d73b0ac759ef` |
| `v031/scripts/apply_range_triage.py` | `468375799cf45e82da3d0b088d9c6b82` |
| `data/snapshot_candidate_triage.jsonl` | `eacf1aa8f1a6f964bd1c425567fdfd59` |
| `runs/triage_range_scope_2026-10-23/METHOD.md` | `9f1b862b2752a2f3cc8f6d18a78b4bb8` |

The audit is read-only against `data/` and `v031/`. Scripts used are in this
directory: `independent_check.py`, `sample_evidence.py`,
`adversarial_probe.py`, plus `independent_results.jsonl`. `python3 -I`
throughout.

Note: `data/snapshot_candidate_triage.jsonl` was rewritten at 03:03, eight
minutes after `proposals.jsonl` was generated (02:55). The current catalog has
1666 rows (`unknown` 1201, `confirmed_not_affected` 369, `confirmed_affected`
64, `possible_affected` 20, `duplicate` 12). All 1200 proposal keys are still
`unknown`; one unknown row added in that update (`adv3_efa9936e479dbcf0`, repo
23088740) has no proposal and is untouched by this pass.

---

## Verdict

**Apply after fixes — split by class.**

| conversion | rows | verdict |
|---|---|---|
| `not_affected_range` → `confirmed_not_affected` (`trusted_range_with_branch`) | 407 | **Sound on the current frozen snapshots. Apply**, after fixing the two latent parser defects below (they do not change any current row) and preferably after fixing the evidence text. |
| `out_of_scope_product` → `out_of_scope` (`upstream_advisory`) | 161 | **Do not apply.** Every row violates the schema (`evidence_urls` empty), and the rule as written classifies advisories whose subject is the repository's own product as third-party. Fix the producer and add a description-subject veto, then re-audit. |

No wrong `not_affected` decision was found: an independent re-implementation
of the OSV/NVD range semantics, written separately from the tool, agrees with
all 568 actionable proposals, and a 47-row stratified sample (35
`not_affected`, 12 `out_of_scope`, 20 repos) was checked by hand against raw
records. The defects below are either (a) an active schema violation and
provenance error confined to `out_of_scope` — including one probable current
false negative, CVE-2022-40281, whose code is present in `curl-8_3_0` — (b) a
latent false-negative that does not fire on the current data, or (c) a correct
decision reached from a badly-worded basis.

---

## Defects

### D1 (blocker, `out_of_scope` only) — every applied `out_of_scope` row is schema-invalid

- Producer: `v031/scripts/triage_range_scope.py:493-501`. The
  `out_of_scope_product` proposal dict is `{**base, proposal, records, reason}`
  and has no `evidence_urls` key (the successful branch at `514-521` adds it).
- Consumer: `v031/scripts/apply_range_triage.py:89`
  (`proposal.get("evidence_urls") or []`) therefore always produces `[]`.
- Schema: `v031/schemas/snapshot_candidate_triage.schema.json:81-102`
  (`allOf[0]`): `out_of_scope` requires `evidence_urls` `minItems: 1`.
- Failing input: any of the 161 proposals, e.g.
  `disc2_a851d46d8833f6f263388579` / `snap_d9525608880dc9e1` (CVE-2009-4924).
- Expected: `["https://nvd.nist.gov/vuln/detail/CVE-2009-4924"]`.
- Actual: `[]`.
- Measured impact: after a simulated `--apply` on a copy of the current
  catalog, **161 of 1666 rows are invalid, all of them `out_of_scope`, all with
  the same error `[] is too short`**. No other row is invalid; no duplicate
  `(snapshot_id, candidate_id)` keys.

### D2 (blocker, `out_of_scope` only) — the rule misattributes advisories whose subject is this repository's product

- Code: `triage_range_scope.py:294` matches only the CPE *product*; the
  description is never consulted. `476-479` turns any alias-matched NVD record
  with no product match into `product_mismatch`, and `491-502` turns a
  non-empty `product_mismatch` with no other status into `out_of_scope_product`.
- Because NVD frequently assigns a component bug to the *embedder*, the
  recorded basis ("the keyword query surfaced a third-party product that merely
  mentions this component") is false for these rows:

| record | row | advisory subject | CPE(s) | status of the decision |
|---|---|---|---|---|
| CVE-2014-1263 | `disc2_42ad80ee991de10d1ab75879` | "curl and libcurl 7.27.0 through 7.35.0 … as used in Apple OS X" | `apple:mac_os_x` | outcome right for 8.3.0, basis false; **would be wrong at any snapshot in 7.27.0–7.35.0** |
| CVE-2016-4303 | `disc2_f6f844593ca0a8c193769c93` | "parse_string … in cjson.c in the cJSON library" | `es:iperf3`, `novell:suse_package_hub…`, `opensuse:*`, `debian_linux` | outcome right (fixed before 1.7.16), basis false |
| CVE-2022-40281 | `disc2_dd7fbfdb878aeb1d1202444b` | "cyassl_connect_step2 in curl/vtls/cyassl.c" | `samsung:tizenrt` | **probable current false negative**: the renamed `wolfssl_connect_step2` in `lib/vtls/wolfssl.c` at `curl-8_3_0` calls `wolfSSL_get_peer_certificate` and the file has no `X509_free`/`FreeX509` at all; curl master now frees it (`wolfSSL_FreeX509` at the `end:` label). The code the advisory describes is in this snapshot. |
| CVE-2004-1378 | `disc2_546a535891e004094d0add05` | "The expat XML parser code, as used in … jabberd" | `jabberstudio:jabberd`, `jadc2s` | outcome right (2004 fix), basis false |

  CVE-2014-1263, CVE-2016-4303 and CVE-2004-1378 are not current false
  negatives because every frozen snapshot is above the upstream fixed release
  (CVE-2014-1263 fixed in 7.36.0; the CVE-2016-4303 `parse_string` overflow was
  fixed in the 2016 cJSON series, long before 1.7.16 — the cached record itself
  only links iperf's fix; the 2004 bug is long fixed). CVE-2022-40281 is
  different: the missing certificate free is present in the snapshot's own
  tree, so that row must at least stay `unknown`, not `out_of_scope`. More
  generally, the rule would close an affected snapshot, and the applied row
  records a false reason.
- Counter-check (ruled out): CVE-2026-4224 (`disc2_ba7d9ce97b900678c9d0da89`,
  CPE `python:python`, description names the Expat parser) is **not** a
  misattribution. The fix is in CPython, `Modules/pyexpat.c`
  (`conv_content_model`, GH-145986/145987, commit `196edfb`), not in libexpat;
  upstream expat 2.6.2 is not implicated. The `out_of_scope` decision is
  correct, only the generic reason text is imprecise.

### D3 (quality, `not_affected` only) — 148 rows carry an evidence sentence that names no record

- Code: `apply_range_triage.py:50-62` builds the basis only from
  `detail["bounds"]`. NVD details expose `cpe_matches`, not `bounds`, so every
  NVD-only row renders an empty list.
- Failing input: `disc2_cbbf645dec334f9187b6897a` (CVE-2016-10749).
- Actual basis: "Snapshot v1.7.16 (parsed 1.7.16) lies after every upper bound
  of the advisory range that names this package: . The snapshot branch descends
  from the fixed release…"
- Expected: the CPE bound (`versionEndExcluding 0.0.0` for this record) or, if
  the bound is unusable, no such claim.
- Measured impact: **148 of the 407** `not_affected` rows (exactly the
  NVD-only rows; the other 259 are OSV-only). `evidence_urls` is still present,
  so the schema passes; only the written basis is empty.

### D4 (latent false-negative) — an open-ended `{introduced: "0"}` range is treated as "does not contain"

- Code: `triage_range_scope.py:124-127`. The comment says an open introduced
  with no closing event is unsupported, but the guard excludes `(0,)` and falls
  through to `return False`.
- Failing input: `range_contains([{"introduced": "0"}], (5, 0))` returns
  `False`; expected `None`. Consequence in `evaluate_osv` (`229-268`): a single
  record whose affected entry has *both* an open `introduced: 0` range and a
  bounded range (`1.0 → 2.0`), evaluated at 5.0, returns
  `not_affected_range`; expected `indeterminate` (the open range asserts every
  version is affected). Reproduced in `adversarial_probe.py`.
- Measured impact: 0 occurrences in the 1125 ranges behind the 407 rows, so no
  current row is wrong. Must be fixed before the tool is run again.

### D5 (latent false-negative) — a nonsensical `versionEndExcluding: 0.0.0` is trusted as an upper bound

- Code: `triage_range_scope.py:331-338` accepts any parseable end value;
  `365-376` then concludes `not_affected_range` because any release is > 0.0.0.
- Failing input: CVE-2016-10749 (`cpe:2.3:a:davegamble:cjson:*…`, only bound
  `versionEndExcluding: 0.0.0`) evaluated at cJSON 1.4.6 returns
  `not_affected_range`; expected `indeterminate`. The description says
  "cJSON before 2016-10-02", so 1.4.6 is affected.
- Measured impact: one current row, `disc2_cbbf645dec334f9187b6897a` at
  v1.7.16 — correct only because 1.7.16 postdates the 2016 fix. The applied
  basis cites the meaningless 0.0.0 bound (see D3). Fix: treat a bound that
  makes an empty range (and any `0`/`0.0.0` placeholder) as unsupported.

### D6 (latent false-negative) — exact-CPE lists are treated as exhaustive

- Code: `triage_range_scope.py:341-348` appends each exact CPE version as an
  upper bound; `376` then clears the snapshot if it is above all of them.
- Measured impact: **36 of 407** rows are decided only by exact CPEs. In 5 of
  them the description states a *higher* upper bound than the largest exact
  CPE (CVE-2012-0036 "before 7.24.0" vs 7.23.1; CVE-2014-0138/0139 "before
  7.36.0" vs 7.35.0; CVE-2016-3739 "before 7.49.0" vs 7.48.0; CVE-2017-8818
  "before 7.57.0" vs 7.56.1). The snapshot (curl 8.3.0) is above both in every
  case, so no current error; a snapshot between the two bounds would be wrongly
  cleared.
- Related evidence-quality issue: `detail["cpe_matches"]` is truncated to 8
  entries (`371`), so the stored per-row CPE evidence is incomplete (CVE-2015-3143
  alone has 143 matched CPE entries).

### D7 (latent) — version parsing collapses pre-releases and letters to the numeric core

- Code: `triage_range_scope.py:55-74`.
- `4.0.0-rc1` and `4.0.0` both parse to `(4,)`; `1.0-beta`, `1.0b2`, `1.0` all
  parse to `(1,)`. The one current instance (GHSA-jj78-5fmv-mv28,
  `fixed: 4.0.0-rc1`, express 4.19.2) is decided correctly because 4.19.2 > 4.
  The collapse is conservative in the current direction (equality blocks
  `not_affected`), but a pre-release *snapshot* tag would be compared as the
  final release. All 20 current snapshot tags parse correctly
  (`curl-8_3_0`→8.3, `netty-4.1.137.Final`→4.1.137, `jenkins-2.441`→2.441,
  `v/0.23.4`→0.23.4, `R_2_6_2`→2.6.2, `4.2.13`, `v1.7.16`).

### D8 (latent) — CPE matching ignores the vendor and mis-parses non-2.3 criteria

- Code: `triage_range_scope.py:289-295`.
- Vendor is read but never compared; all currently matched vendors are
  legitimate for the repo (`cjson_project`/`davegamble`; `curl`/`haxx`/
  `daniel_stenberg`/`libcurl`; `libexpat_project`), so no active issue.
- A CPE 2.2 URI (`cpe:/a:curl:curl:7.30.0`) shifts the fields so `parts[4]` is
  the version; the record becomes `no_matching_package` and, at the proposal
  level, `out_of_scope_product`. Reproduced in `adversarial_probe.py`.
  All cached criteria are CPE 2.3, so 0 current occurrences.

### D9 (ruled out on current data) — OSV package-name filter drops sibling entries

- Code: `triage_range_scope.py:216-217` keeps only the affected entry whose
  package name equals the query package. 2520 of 7296 cached affected entries
  are skipped (monorepo sub-packages and sibling artifacts).
- Checked: no alias-matched OSV record was dropped entirely (0), and no skipped
  sibling entry names the repo's product and contains the snapshot. The only
  sibling that contains the snapshot is `jquery-rails 0→4.3.4` in
  GHSA-6c3j-c64m-qhgq, a different product from the queried Django entry —
  correctly ignored.

---

## Sample audit

Seed 20261023, stratified by (repo, class). 47 rows: 35 `not_affected`, 12
`out_of_scope`, 20 repositories. The "decisive evidence" column was recomputed
from the raw cached OSV/NVD records, not from the proposal.

| # | candidate | repo | tag | class | record(s) | decisive evidence, independently recomputed | verdict |
|---|---|---|---|---|---|---|---|
| 1 | `disc2_474f6db1447cc3bf9ba9e355` | 569041 | `curl-8_3_0` | not_affected | CVE-2014-3620 | max 7.37.1 (versionEndIncluding); 16 bound(s) in matched CPEs/ranges | OK: 7.37.1 < 8.3 |
| 2 | `disc2_3cfe93a823a36726eb30472c` | 569041 | `curl-8_3_0` | not_affected | CVE-2015-3143 | max 7.41.0 (exact); 143 bound(s) in matched CPEs/ranges | OK: 7.41.0 < 8.3 |
| 3 | `disc2_492c9a303f885ec808e65ce5` | 569041 | `curl-8_3_0` | not_affected | CVE-2015-3153 | max 7.42.0 (versionEndIncluding); 2 bound(s) in matched CPEs/ranges | OK: 7.42.0 < 8.3 |
| 4 | `disc2_ebbdf7f86dcb294dbec730f0` | 569041 | `curl-8_3_0` | not_affected | CVE-2022-32207 | max 7.84.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 7.84.0 < 8.3 |
| 5 | `disc2_62300bf3f53794cd0e01aac2` | 569041 | `curl-8_3_0` | not_affected | CVE-2020-8286 | max 7.74.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 7.74.0 < 8.3 |
| 6 | `disc2_01970e0e6edf4b467795e673` | 569041 | `curl-8_3_0` | not_affected | CVE-2016-8621 | max 7.51.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 7.51.0 < 8.3 |
| 7 | `disc2_74a9b27c6ec317c053518174` | 569041 | `curl-8_3_0` | not_affected | CVE-2016-8617 | max 7.51.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 7.51.0 < 8.3 |
| 8 | `disc2_33095b25ab379ebf6e1930f4` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2023-33270 | CPE product(s): monitoring | OK: no CPE names this product |
| 9 | `disc2_e6aa1a09a5842a9770eba210` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2021-33525 | CPE product(s): eyesofnetwork | OK: no CPE names this product |
| 10 | `disc2_6e396c1cd863a8ea1bdde44b` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2020-7646 | CPE product(s): curlrequest | OK: no CPE names this product |
| 11 | `disc2_c468afc36d94af34882bc531` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2024-7330 | CPE product(s): youdiancms | OK: no CPE names this product |
| 12 | `disc2_ef3565a88be2598c13a8a186` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2018-3744 | CPE product(s): html-pages | OK: no CPE names this product |
| 13 | `disc2_eb95428dfa3d3f6ad22705bc` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2017-1000139 | CPE product(s): mahara | OK: no CPE names this product |
| 14 | `disc2_0c35d69e3785ce9af82e9d70` | 569041 | `curl-8_3_0` | out_of_scope | CVE-2002-2444 | CPE product(s): snoopy | OK: no CPE names this product |
| 15 | `disc2_59949922a1aa40250a8f5123` | 4164482 | `4.2.13` | not_affected | GHSA-xpfp-f569-q3p2, PYSEC-2021-109 | max 3.2.5 (fixed); 4 bound(s) in matched CPEs/ranges | OK: 3.2.5 < 4.2.13 |
| 16 | `disc2_fd717fd5ea2aa7d4d0b18bd6` | 4164482 | `4.2.13` | not_affected | GHSA-2m34-jcjv-45xf, PYSEC-2020-32 | max 3.0.7 (fixed); 4 bound(s) in matched CPEs/ranges | OK: 3.0.7 < 4.2.13 |
| 17 | `disc2_85973a855439fbeafad5b056` | 4164482 | `4.2.13` | not_affected | GHSA-7qfw-j7hp-v45g, PYSEC-2015-4 | max 1.7.3 (fixed); 6 bound(s) in matched CPEs/ranges | OK: 1.7.3 < 4.2.13 |
| 18 | `disc2_32e8ea5fc74e6b7635c926ce` | 4164482 | `4.2.13` | not_affected | GHSA-4c42-4rxm-x6qf, PYSEC-2013-18 | max 1.5.4 (fixed); 4 bound(s) in matched CPEs/ranges | OK: 1.5.4 < 4.2.13 |
| 19 | `disc2_b66f36728400e9eed5fe6c5e` | 4164482 | `4.2.13` | not_affected | GHSA-wh4h-v3f2-r2pp, PYSEC-2019-18 | max 2.1.7 (fixed); 6 bound(s) in matched CPEs/ranges | OK: 2.1.7 < 4.2.13 |
| 20 | `disc2_9baf176c59fe1883855799c8` | 1103607 | `jenkins-2.441` | not_affected | GHSA-wr6p-j63r-xqhv | max 1.482 (fixed); 2 bound(s) in matched CPEs/ranges | OK: 1.482 < 2.441 |
| 21 | `disc2_c9eac1912abe2328efc558ac` | 1103607 | `jenkins-2.441` | not_affected | GHSA-6g4r-q7qg-6qx6 | max 2.356 (fixed); 1 bound(s) in matched CPEs/ranges | OK: 2.356 < 2.441 |
| 22 | `disc2_febfe526e6043cbed54a53b2` | 1103607 | `jenkins-2.441` | not_affected | GHSA-5j46-5hwq-gwh7 | max 2.424 (fixed); 2 bound(s) in matched CPEs/ranges | OK: 2.424 < 2.441 |
| 23 | `disc2_c9e4feff0c403330f6174871` | 80314213 | `R_2_6_2` | not_affected | CVE-2022-22823 | max 2.4.3 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 2.4.3 < 2.6.2 |
| 24 | `disc2_eacb4a83aad2bd71fa00ad07` | 80314213 | `R_2_6_2` | not_affected | CVE-2013-0340 | max 2.4.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 2.4.0 < 2.6.2 |
| 25 | `disc2_097dd1bdcf3bd194eac2ac91` | 80314213 | `R_2_6_2` | not_affected | CVE-2016-5300 | max 2.2.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | OK: 2.2.0 < 2.6.2 |
| 26 | `disc2_0c9cbf5bb34d2a9423adad2f` | 80314213 | `R_2_6_2` | out_of_scope | CVE-2009-2473 | CPE product(s): neon | OK: no CPE names this product |
| 27 | `disc2_68415eefb919c3574a4d55d7` | 80314213 | `R_2_6_2` | out_of_scope | CVE-2009-1955 | CPE product(s): apr-util, debian_linux, fedora, http_server, … | OK: no CPE names this product |
| 28 | `disc2_ba7d9ce97b900678c9d0da89` | 80314213 | `R_2_6_2` | out_of_scope | CVE-2026-4224 | CPE product(s): python | OK: no CPE names this product |
| 29 | `disc2_cbbf645dec334f9187b6897a` | 54280778 | `v1.7.16` | not_affected | CVE-2016-10749 | max 0.0.0 (versionEndExcluding); 1 bound(s) in matched CPEs/ranges | Right outcome, placeholder bound — see D5 |
| 30 | `disc2_582c760796f4e1c272b11ee1` | 54280778 | `v1.7.16` | not_affected | CVE-2019-1010239 | max 1.7.8 (exact); 1 bound(s) in matched CPEs/ranges | OK: 1.7.8 < 1.7.16 |
| 31 | `disc2_f72830f9f3614b646d93161c` | 54280778 | `v1.7.16` | out_of_scope | CVE-2015-7392 | CPE product(s): freeswitch | OK: no CPE names this product |
| 32 | `disc2_ea8d49696c0fb4ece964930b` | 54280778 | `v1.7.16` | out_of_scope | CVE-2023-28096 | CPE product(s): opensips | OK: no CPE names this product |
| 33 | `disc2_3506e25e593cc87594a444c3` | 458058 | `v5.4.45` | not_affected | GHSA-j5jh-hpr4-h332 ×3 | max 2.7.7 (fixed); 8 bound(s) | OK: 2.7.7 < 5.4.45 |
| 34 | `disc2_d0ab57e56963e49bcc23fba5` | 458058 | `v5.4.45` | not_affected | GHSA-q8j7-fjh7-25v5 ×2 | max 2.3.3 (fixed); 8 bound(s) | OK: 2.3.3 < 5.4.45 |
| 35 | `disc2_70116dc07dabb8e04192ff5c` | 96071 | `v3.1.13` | not_affected | GHSA-hrqr-hxpp-chr3 | max 2.0.8 (fixed); 2 bound(s) | OK: 2.0.8 < 3.1.13 |
| 36 | `disc2_7813f5d8fb65be7261c2664e` | 96071 | `v3.1.13` | not_affected | GHSA-5f9h-9pjv-v6j7 | max 2.1.3 (fixed); 1 bound(s) | OK: 2.1.3 < 3.1.13 |
| 37 | `disc2_37219051bd3301cae27c59eb` | 7548986 | `v11.30.0` | not_affected | GHSA-jwvj-pwww-3mj5 | max 8.24.0 (fixed); 3 bound(s) | OK: 8.24.0 < 11.30 |
| 38 | `disc2_47160b3df0ad86d2e593605d` | 1064563 | `netty-4.1.137.Final` | not_affected | GHSA-p979-4mfw-53vg ×3 | max 4.1.42 (fixed); 3 bound(s) | OK: 4.1.42 < 4.1.137 |
| 39 | `disc2_40e042b50ddb6f409540b178` | 237159 | `4.19.2` | not_affected | GHSA-jj78-5fmv-mv28 | max 4.0.0 (fixed, tag `4.0.0-rc1`); 1 bound | OK: 4.0.0 < 4.19.2 |
| 40 | `disc2_c8a23ffa0b192708b7c282c6` | 596892 | `2.3.1` | not_affected | GHSA-5wv5-4vpf-pj6m, PYSEC-2019-179 | max 1.0 (fixed); 2 bound(s) | OK: 1.0 < 2.3.1 |
| 41 | `disc2_7e836f9100c76a344150ad20` | 997338 | `3.0.2` | not_affected | GHSA-j544-7q9p-6xp8, PYSEC-2026-1065 | max 0.15.5 (fixed); 2 bound(s) | OK: 0.15.5 < 3.0.2 |
| 42 | `disc2_c394521987ef9072719433a3` | 20904437 | `v1.9.0` | not_affected | GHSA-869c-j7wc-8jqv | max 1.6.0 (fixed); 1 bound(s) | OK: 1.6.0 < 1.9 |
| 43 | `disc2_0f18af849d5c6c77b17d83bf` | 1420053 | `7.14.1` | not_affected | GHSA-cwxw-98qj-8qjx | max 7.12.1 (fixed); 1 bound(s) | OK: 7.12.1 < 7.14.1 |
| 44 | `disc2_efa0137a12dee25417276903` | 23500865 | `v0.14.2` | not_affected | GHSA-q89x-f52w-6hj2, RUSTSEC-2017-0002 | max 0.10.2 (fixed); 4 bound(s) | OK: 0.10.2 < 0.14.2 |
| 45 | `disc2_bc94d866bea54f1c5242ce7d` | 23357588 | `v3.25.4` | not_affected | GHSA-jwvw-v7c5-m82h ×3 | max 3.4.0 (fixed); 5 bound(s) | OK: 3.4.0 < 3.25.4 |
| 46 | `disc2_ca8e28f70b64f69d7252e789` | 133092972 | `v5.19.0` | not_affected | GHSA-pgw7-wx7w-2w33 | max 5.5.1 (fixed); 1 bound(s) | OK: 5.5.1 < 5.19 |
| 47 | `disc2_8b189e980efd021d9c64e2ef` | 257485422 | `v5.0.11` | not_affected | GHSA-92r3-m2mg-pj97 | max 5.0.5 (fixed); 3 bound(s) | OK: 5.0.5 < 5.0.11 |

All 35 `not_affected` samples are correct on the raw evidence. All 12
`out_of_scope` samples are correct decisions at these snapshots; #23–#25 and
#27–#28 depend on NVD attributing the advisory to an embedder, which is the
D2 provenance weakness (for #28 the attribution is in fact correct — the bug is
in CPython, not libexpat). The D2 table separately found one `out_of_scope`
row outside this sample, CVE-2022-40281, that is a probable current false
negative.

Cross-check beyond the sample: a separate re-implementation
(`independent_check.py`) evaluates all 568 actionable proposals from the raw
records and reports **0 disagreements** with the tool.

## Adversarial probes

`adversarial_probe.py` feeds synthetic records to the tool's own functions.

| probe | expected | actual |
|---|---|---|
| tag parsing: `curl-8_3_0`, `netty-4.1.137.Final`, `jenkins-2.441`, `v/0.23.4`, `R_2_6_2`, `4.2.13`, `v1.7.16` | correct tuples | all correct |
| open `{introduced:"0"}`, no closing event | unsupported (`None`) | `False` — **D4** |
| open `{introduced:"0"}` + bounded `1.0→2.0`, snapshot 5.0 | indeterminate | `not_affected_range` — **D4** |
| `last_affected: 2.0` at 2.0 (inclusive) | contains | contains |
| `limit: 3.0` at 2.0 (exclusive) | contains | contains |
| Debian affected entry, upstream query | unsupported ecosystem | unsupported ecosystem |
| GIT commit range | indeterminate | indeterminate |
| `versionEndExcluding 0.0.0` at 1.4.6 | indeterminate | `not_affected_range` — **D5** |
| CPE 2.2 `cpe:/a:curl:curl:7.30.0` | indeterminate | `no_matching_package` → `out_of_scope` — **D8** |
| exact CPE 7.30.0 at 7.30.0 / at 8.3.0 | possible / not affected | possible / not affected |
| start-only CPE at 8.3.0 | possible (open-ended) | possible |
| all matching CPEs `vulnerable=false` | indeterminate | indeterminate |
| record with no configurations | `no_configuration` → indeterminate | `no_configuration` |
| vendor `apple:curl` product `curl` | matches (vendor ignored) — **D8** | matches |
| two records: one fixed < snapshot, one range above the snapshot | indeterminate | indeterminate |
| mac_os_x CPE, "curl and libcurl" description | `no_matching_package` | `no_matching_package` — **D2** |

## Classes of row to exclude / actions

1. **Exclude all 161 `out_of_scope_product` proposals from this apply.** They
   cannot be applied as produced (D1) and the producer rule is unsound for
   advisories about the repository's own product (D2).
2. Before any re-run, fix D4 (`range_contains` open-`introduced:0`) and D5
   (placeholder end bounds). Both are small, local changes. After fixing,
   regenerate and confirm the 407 `not_affected` proposals are unchanged; the
   current run has zero rows in either defective shape.
3. Fix D3 (`apply_range_triage.not_affected_row`) to render NVD bounds
   (`cpe_matches`: criteria + versionEnd*/versionStart*) instead of an empty
   list; otherwise 148 applied rows will assert an evidence range without
   naming it.
4. For `out_of_scope`, emit `evidence_urls` from the record id (the URL builder
   already exists at `triage_range_scope.py:486-490`), and add a veto: if the
   NVD description names the repository product (e.g., "curl and libcurl",
   "cJSON library", "Expat parser"), return `indeterminate`, not
   `out_of_scope`. Re-run the audit on the regenerated set.
5. Rows in `possible_affected_range` (176) and `indeterminate` (456) remain
   `unknown`; nothing in this pass promotes them, which is correct.

## Limitations of this audit

- I did not re-fetch every advisory; cached raw records were the primary
  evidence (as the brief allows). I made four live checks where the cached
  record was ambiguous: CVE-2026-4224 (OSV + CPython fix commit, confirms the
  Python-only scope), CVE-2014-1263 (curl's own security page), CVE-2022-40281
  (`lib/vtls/cyassl.c` was renamed to `lib/vtls/wolfssl.c`; the snapshot still
  has `wolfssl_connect_step2` calling `wolfSSL_get_peer_certificate` with no
  `X509_free`/`FreeX509`, so this one is a probable current false negative),
  and the express/flask fixed tags.
- Branch topology is not modelled (as METHOD.md says). Several `not_affected`
  rows compare a snapshot on one major line (Jenkins 2.441, Netty 4.1.137,
  Symfony 5.4.45, Laravel 11.30) against a fix on another (1.482, 4.0.0,
  2.7.7, 8.24.0). All are far enough below the snapshot that the conclusion is
  safe, but "the snapshot branch descends from the fixed release" is an
  assumption, not something the range data proves.
- The sample is 47 of 568; the full-coverage claim rests on the independent
  re-implementation, which shares the product-name matching and package-name
  filter assumptions with the tool. Those two assumptions were checked
  separately (D8, D9) and produce no active error on this data.
