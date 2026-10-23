# Django 3.0.2 — why 13 OSV-listed candidates have no verified affected range

Snapshot: django/django tag 3.0.2, commit
`a36974395ebc03a41928db1743074575b143330d`, snapshot_id
`snap_ab695ba3db678939`. Date: 2026-10-22.

## Method

For every `in_validation` Django candidate, the OSV record in
`runs/discovery_v2/osv_queries/e6dc2df935dc1697766a11af.json` was read in two
parts:

1. the machine-readable `affected[].ranges` and `affected[].versions`;
2. the human-readable `details` text written by the CNA.

The ranges are evaluated against 3.0.2 with the rule `introduced <= V < fixed`,
where a range `{introduced: 0, fixed: X}` literally contains every release below
`X`, including end-of-life 3.0.x. The `details` text is the scoping statement by
the vendor/CNA.

## Finding

The 13 candidates below all have OSV ranges that mechanically include 3.0.2, but
none of their advisory texts name the 3.0 series as affected. The enumerated
`versions` arrays are generated as "every release below `fixed`", so they cannot
be used as evidence that 3.0.2 is vulnerable.

| Candidate | Advisory | Text scope | 3.0.2 in text? |
|---|---|---|---|
| disc2_fe5cd22f5606e09999984889 | CVE-2022-36359 / GHSA-8x94-hmjh-97hq | 3.2 before 3.2.15, 4.0 before 4.0.7 | no |
| disc2_00c12ead68ae4b95c2b982e6 | CVE-2024-45231 / GHSA-rrqc-c2jx-6jgv | fixed in 5.1.1, 5.0.9, 4.2.16 | no |
| disc2_c4d0f4e6aee27f12507cc7c3 | CVE-2025-57833 / GHSA-6w2r-r2m5-xq5w | 4.2 before 4.2.24, 5.1 before 5.1.12, 5.2 before 5.2.6 | no |
| disc2_869ed839e7101f70b458e853 | CVE-2025-64458 / GHSA-qw25-v68c-qjf3 | 5.1 before 5.1.14, 4.2 before 4.2.26, 5.2 before 5.2.8; "earlier, unsupported series ... not evaluated" | not evaluated |
| disc2_d791407a54d5b84b33a8db28 | CVE-2025-64459 / GHSA-frmv-pr5f-9mcr | 5.1 before 5.1.14, 4.2 before 4.2.26, 5.2 before 5.2.8; "earlier, unsupported series ... not evaluated" | not evaluated |
| disc2_964417e6892549137491a482 | CVE-2026-15307 / GHSA-wvqv-fj8w-qmhm | 5.2 before 5.2.17, 6.0 before 6.0.8 | no |
| disc2_956f6f00002b68166b526c02 | CVE-2026-15830 / GHSA-q238-5cxm-5c9h | 5.2 before 5.2.17, 6.0 before 6.0.8 | no |
| disc2_eab6d1a548b2f2a6e24d1666 | CVE-2026-6873 / GHSA-h7pc-vwp9-298g | 5.2 before 5.2.15, 6.0 before 6.0.6 | no |
| disc2_28514ab37f4ffb059c923fdb | CVE-2026-8404 / GHSA-8cjm-8mp7-r2xf | 5.2 before 5.2.15, 6.0 before 6.0.6 | no |
| disc2_d9fa741af9a342d325abcbc7 | CVE-2026-48587 / GHSA-923m-gv2p-w5qp | 5.2 before 5.2.15, 6.0 before 6.0.6 | no |
| disc2_f805f93b227052047bcaf78f | CVE-2026-48588 / GHSA-3h9f-r86x-qvjx | 5.2 before 5.2.16, 6.0 before 6.0.7 | no |
| disc2_129f28a7857053e311c7d94d | CVE-2026-53877 / GHSA-crhf-3pfg-w68w | 5.2 before 5.2.16, 6.0 before 6.0.7 | no |
| disc2_321d50f93bd7f1b2dc581ab7 | CVE-2026-53878 / GHSA-8qcx-xf44-272x | 5.2 before 5.2.16, 6.0 before 6.0.7 | no |

`details` values were read from the OSV records in the query file above; no
network request was needed for this table.

## Consequence

`affected_range` cannot be verified for these candidates against snapshot 3.0.2,
so they cannot reach the promotion gate, which requires all 19
`fields_verified` keys to be true. Their triage status is moved from
`in_validation` to `pending_version` with the blocker text
"advisory text does not assert 3.0.x; enumerated versions are mechanical".
This is a version-applicability deferral, not a rejection: if a later code-level
review or a vendor statement establishes the 3.0 branch, the candidate can be
resumed from its dossier row.

## The fourteenth candidate

`disc2_59949922a1aa40250a8f5123` (CVE-2021-35042) is the only one whose
advisory enumerates 3.0.x. Its range is nevertheless wrong: the fix commit
states the regression appeared in 3.1, and 3.0.2 still validates order_by
arguments. It is rejected with its own evidence in
`../django_cve_2021_35042/NOT_APPLICABLE.md`.

## Methodological note

The earlier count of "18 Django candidates in range" was produced by evaluating
OSV ranges only. That evaluator is correct as a semver calculation but its input
is over-inclusive for EOL series. Range membership in OSV is not by itself
evidence of affectedness; the CNA text and code must agree with it.

## Limitations

- Advisory texts were taken from the saved OSV query response (retrieved
  2026-10-21/22); NVD/CVE descriptions were not re-fetched for all 13.
- No source code at 3.0.2 was inspected for these 13; the deferral rests on the
  absence of a vendor scope statement, not on a code-level disproof. A code check
  could later establish affectedness, but it would still need to reconcile with
  the published range before the dossier's `affected_range` can pass.
