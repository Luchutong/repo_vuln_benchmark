# Triage of lodash/lodash candidates at tag 4.17.23

Snapshot under triage: `snap_033e9a6478460d9b` = tag `4.17.23` →
commit `dec55b7a3b382da075e2eac90089b4cd00a26cbb` (plain source tag, 159 tracked files).
Collected 2026-10-22/23 by the collecting agent; not an independent review.
Raw artifacts in `sources/`, hashes in `sources/MANIFEST.sha256`.

## Provenance

- `sources/osv_GHSA-*.json` — fetched 2026-10-23 from
  `https://api.osv.dev/v1/vulns/<GHSA>` over HTTPS through the session proxy; HTTP 200,
  9 records, one per non-CVE-2026-4800 candidate. CVE-2026-4800's own OSV record lives with
  the main dossier evidence (`../lodash_CVE-2026-4800_v41723/sources/osv_GHSA-r5fr-rjxr-66jc.json`)
  and is not duplicated here.
- `sources/ancestry_triage.txt` — generated 2026-10-22T19:34:09Z in the upstream clone
  `/tmp/lodash_recon` (clone of `https://github.com/lodash/lodash`, HEAD `2b5e6f73`,
  `4.18.1-11-g2b5e6f739`). Every `ancestor_of_*` value is the exit status of
  `git merge-base --is-ancestor <ref> <rev>` (0 = yes, 1 = no); tags resolved with
  `<tag>^{commit}`.

## OSV ranges as fetched (npm/lodash)

| candidate | CVE | introduced | fixed | GHSA |
|---|---|---|---|---|
| `disc2_068d581ea2777b13d8dae7fe` | CVE-2018-16487 | 0 | 4.17.11 | GHSA-4xc9-xhrj-v574 |
| `disc2_62fb2e6c311a7ce40dacfd81` | CVE-2018-3721 | 0 | 4.17.5 | GHSA-fvqr-27wr-82fm |
| `disc2_ad1e9ee0df8beb08168a074a` | CVE-2019-1010266 | 4.7.0 | 4.17.11 | GHSA-x5rq-j2xg-h7qm |
| `disc2_0f09e7f5cfcdde3e7e94e09f` | CVE-2019-10744 | 0 | 4.17.12 | GHSA-jf85-cpcp-j695 |
| `disc2_ed6ca9c7dbf6191b7f7cd22b` | CVE-2020-28500 | 4.0.0 | 4.17.21 | GHSA-29mw-wpgm-hmr9 |
| `disc2_4b23e60c6196adab2a0bb6bf` | CVE-2020-8203 | 3.7.0 | 4.17.19 | GHSA-p6mc-m468-83gw |
| `disc2_de942b91684f49da0ec58687` | CVE-2021-23337 | 0 | 4.17.21 | GHSA-35jh-r3h4-6jhm |
| `disc2_62672c826f88924a8e6686e9` | CVE-2025-13465 | 4.0.0 | 4.17.23 | GHSA-xxjr-mmjv-4gpg |
| `disc2_e723f5f71a79988ec17c4cfc` | CVE-2026-2950 | 0 | 4.18.0 | GHSA-f23m-r3pf-42rh |
| `disc2_29cd55fbcc05a5cf28a87b78` | CVE-2026-4800 | 4.0.0 | 4.18.0 | GHSA-r5fr-rjxr-66jc |

Note the last row's CNA/GitHub advisory range is `<4.18.1`; OSV encodes `<4.18.0`. That
disagreement is recorded in the dossier and is not resolved by this triage.

## Decisions and basis

- **CVE-2026-4800 — confirmed_affected.** Known positive at this SHA; the independent
  reviewer, not this file, is the authority. Dossier:
  `../lodash_CVE-2026-4800_v41723/dossier.json`.
- **CVE-2025-13465 — confirmed_not_affected.** The advisory's fixed version is 4.17.23, i.e.
  the snapshot is the first fixed release. Corroborated three ways: fix `edadd4521` is an
  ancestor; `lodash.js` at the tag carries the advisory-linked guards in `baseUnset`
  (comments at 4374, `typeof key !== 'string'` at 4388, `__proto__`/`constructor` checks at
  4393-4398); and the advisory's four regression payloads (omit-proto, omit-ctor,
  unset-proto, unset-ctor) all leave both prototypes intact at 4.17.23 while all four delete
  a builtin at 4.17.21 (see `../lodash_CVE-2026-4800_v41723/sources/poc_reproduction.txt`).
  `516085f3` and `daec92cf` are related follow-ups but are ancestors of neither release and
  are not needed for the call.
- **Seven 2018–2021 CVEs — confirmed_not_affected.** For each, the fixed release named by
  OSV is an ancestor of `dec55b7a` (table: 4.17.5, 4.17.11 ×2, 4.17.12/4.17.13,
  4.17.19/4.17.20, 4.17.21 ×2), and where the advisory publishes a fix commit, that commit
  is an ancestor too. CVE-2019-10744 publishes no commit; its fixed release 4.17.12 is an
  ancestor, and `lodash-es`'s 4.17.14 variant is irrelevant at this package. The call rests
  on git ancestry of the fix, not on comparing version strings.
- **CVE-2026-2950 — possible_affected, left unresolved.** OSV range `introduced 0,
  fixed 4.18.0` covers 4.17.23, and 4.18.0 is not an ancestor. Recon observed an
  array-wrapped `baseUnset` bypass reproducing at 4.17.23, but that has not been
  independently verified, so it cannot be promoted as a positive and must not be written
  down as a negative.

## Limitations

- Triage is collector-side; the only independent artifact in this set is the round-1 verdict
  for CVE-2026-4800.
- `review_method: trusted_range_with_branch` means vendor range plus ancestry of the fix, not
  a reproduction at the snapshot.
- The OSV records are a moving target; `checked_at` on each triage row records when they were
  fetched.
- Only the npm `lodash` package is triaged. `lodash-es`, `lodash-amd` and `lodash.template`
  are in several advisory ranges but are separate distributions and are not part of this
  snapshot.
