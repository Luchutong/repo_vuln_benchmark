# Range-scoping pass over the 1200 unknown triage rows

Date: 2026-10-23. Read-only against the catalog; `data/` not modified by this
pass. Tool: `v031/scripts/triage_range_scope.py` (v1.0), proposal file
`proposals.jsonl` in this directory, apply tool
`v031/scripts/apply_range_triage.py`.

## Goal and rule

Priority 3 of HANDOFF_V031 asks for low-cost targeted verification of the 1200
`unknown` triage rows: version/branch rules first, source review for the ones
that remain relevant, evidence archived for the ones that are not. This pass
does the version/branch half against the **already-cached** discovery records
(`runs/discovery_v2/osv_queries`, `runs/discovery_v2/nvd_queries` and their raw
bodies); it makes no network request and changes no candidate status.

For each unknown row the tool evaluates the advisory's machine-readable ranges
against the release that the frozen snapshot records in `tag_or_release`:

- `not_affected_range` - every alias-matched record that names the snapshot's
  package has an upper bound (`fixed`, `last_affected` or `versionEnd*`) strictly
  below the parsed snapshot version, and no range contains the snapshot. The
  snapshot therefore descends from the fixed release.
- `possible_affected_range` - at least one range contains the snapshot. This is
  a reason to read the code, never a positive: nothing is promoted from it.
- `out_of_scope_product` - the alias-matched NVD record has CPE configurations,
  but none of them names this repository's product (keyword search hit a
  third-party product that merely mentions the component).
- `indeterminate` - no usable range, unparsable tag, unsupported ecosystem or
  event type, conflicting records, or a record with no CPE configuration at all.

Ecosystem restriction: OSV ranges are evaluated only for upstream ecosystems
(`GitHub`, `PyPI`, `npm`, `Go`, `Maven`, `crates.io`, `RubyGems`, `Packagist`,
`NuGet`, `Hex`, `Pub`). Distribution ranges (Debian, Ubuntu, Alpine, ...) order
by package revision, not by upstream release, so they are never used. `GIT`
ranges with commit hashes are unsupported by this pass and remain
`indeterminate`.

## Outcome

1200 rows evaluated. 568 are actionable, 632 stay open.

| repo | snapshot | not_affected_range | out_of_scope_product | possible_affected_range | indeterminate |
|---|---|---|---|---|---|
| DaveGamble/cJSON | `v1.7.16` | 8 | 9 | 6 | 27 |
| curl/curl | `curl-8_3_0` | 117 | 141 | 17 | 109 |
| django/django | `4.2.13` | 101 | 0 | 43 | 18 |
| expressjs/express | `4.19.2` | 3 | 0 | 0 | 1 |
| gin-gonic/gin | `v1.9.0` | 2 | 0 | 0 | 1 |
| guzzle/guzzle | `7.14.1` | 3 | 0 | 5 | 4 |
| hyperium/hyper | `v0.14.2` | 2 | 0 | 3 | 3 |
| jenkinsci/jenkins | `jenkins-2.441` | 56 | 0 | 23 | 0 |
| laravel/framework | `v11.30.0` | 19 | 0 | 6 | 5 |
| libarchive/libarchive | `v3.7.7` | 0 | 0 | 0 | 22 |
| libexpat/libexpat | `R_2_6_2` | 23 | 11 | 2 | 99 |
| netty/netty | `netty-4.1.137.Final` | 9 | 0 | 2 | 103 |
| nodejs/undici | `v5.19.0` | 1 | 0 | 18 | 15 |
| pallets/flask | `2.3.1` | 1 | 0 | 1 | 2 |
| pallets/werkzeug | `3.0.2` | 2 | 0 | 6 | 9 |
| protocolbuffers/protobuf | `v3.25.4` | 5 | 0 | 3 | 2 |
| rack/rack | `v3.1.13` | 28 | 0 | 20 | 1 |
| rustls/rustls | `v/0.23.4` | 0 | 0 | 2 | 8 |
| symfony/symfony | `v5.4.45` | 26 | 0 | 3 | 23 |
| vitejs/vite | `v5.0.11` | 1 | 0 | 16 | 4 |
| **total** | | **407** | **161** | **176** | **456** |

The 176 `possible_affected_range` rows are kept open (they include the
mechanically-widened `introduced: 0` ranges that the Django 3.0.2 scoping
report already warned about). The 456 `indeterminate` rows remain `unknown`.

## Spot checks performed by hand

| candidate | repo / tag | record and range | proposal | why |
|---|---|---|---|---|
| `disc2_59949922a1aa40250a8f5123` | django 4.2.13 | GHSA-xpfp-f569-q3p2 `introduced 3.2a1 -> fixed 3.2.5`, `3.0a1 -> 3.1.13` | not affected | 4.2.13 is after both fixes; the advisory scopes 3.0/3.2 |
| `disc2_9b9516ee0dc53614cc5e96e4` | django 4.2.13 | GHSA-59w8-4wm2-4xw8 `0 -> 1.3.2`, `1.4 -> 1.4.1` | not affected | fixed in 2012, snapshot descends from both lines |
| `disc2_d92bf96baa1800891b60e927` | symfony 5.4.45 | GHSA-r2rq-3h56-fqm4 2.7.48 / 2.8.41 / 3.3.17 / 3.4.11 | not affected | all upper bounds below 5.4.45 |
| `disc2_779ff4b4ed7478f0be9c9b63` | jenkins 2.441 | GHSA-5c56-g5cq-4gj9 `1.481 -> 1.502`, `0 -> 1.480.3` | not affected | weekly line 2.441 includes the 1.x fix |
| `disc2_4f3cff8fc555f1e7514b3567` | curl 8.3.0 | CVE-2000-0973 exact CPE `curl:6.0..6.5.2` | not affected | snapshot not among the exact affected releases |
| `disc2_9a7023322a2601ef7fed58be` | curl 8.3.0 | CVE-2020-14359, CPE `redhat:louketo_proxy` | out_of_scope | NVD description is Keycloak Gatekeeper; no curl CPE |
| `disc2_55238a94418c3540bd952204` | curl 8.3.0 | CVE-2025-5265, CPE `mozilla:firefox` | out_of_scope | "Copy as cURL" in Firefox, not libcurl |
| `disc2_acce0d1397c896021df6f4b7` | curl 8.3.0 | CVE-2014-5000, CPE `lawn-login_project:lawn-login` | out_of_scope | Ruby gem invoking curl, not curl itself |

The Debian `DSA-1921-1` (expat `1.95.8-3.4+etch1`) case was the reason for the
distribution-ecosystem restriction: its revision numbers must never be compared
with upstream `R_2_6_2`, so those rows now stay `indeterminate`.

## Limitations (captured in every applied row)

1. The pass reads cached records; it does not re-fetch advisories. A record that
   changed after 2026-10-21 is not seen here.
2. `introduced: 0 -> fixed X` ranges are mechanically widened by several
   producers (the Django 3.0.2 scoping report demonstrates this). They are used
   only in the safe direction: a snapshot **above X** is judged not affected; a
   snapshot **below X** becomes `possible_affected`, never a positive.
3. Parallel maintained branches (for example OpenSSL 1.1.1 vs 3.0, Python 2 vs
   3) are not modelled. No current row in this pass falls in that shape, but a
   future run must re-examine the differing-major rows listed in the tool's
   audit output.
4. `out_of_scope` is an attribution finding about the catalog candidate, not a
   statement that the third-party product is safe. The candidate row itself is
   preserved with its evidence.
5. Nothing here is a code-level audit, so no row is promoted and no grade is
   assigned.

## v1.1 (2026-10-23, after independent audit)

The audit in `audit/AUDIT.md` blocked the out-of-scope half and required fixes
before the not-affected half. v1.1 applies D1/D2/D4/D5 and regenerates to
`proposals_v1_1.jsonl`; the not-affected proposals were applied with
`--only-proposal not_affected_range` (406 rows). See `DISPOSITION.md` for the
defect table, the delta, and why no `out_of_scope` row was written.
