# CVE-2021-35042 / GHSA-xpfp-f569-q3p2 — not applicable to Django 3.0.2

Candidate: `disc2_59949922a1aa40250a8f5123` (status `in_validation`)
Repository: django/django, snapshot `snap_ab695ba3db678939` (tag 3.0.2)
Tag dereference: `refs/tags/3.0.2^{}` = `a36974395ebc03a41928db1743074575b143330d`,
which equals the snapshot `vulnerable_commit`. Decision date: 2026-10-22.

## Finding

The SQL injection in `QuerySet.order_by()` was introduced in Django 3.1 and does
not exist in 3.0.2. The vulnerable path is a regression from the commit that
started deprecating raw SQL column references; 3.0.2 still performs strict
column-name validation.

Evidence:

1. CVE List v5 CNA description: "Django 3.1.x before 3.1.13 and 3.2.x before
   3.2.5 allows QuerySet.order_by SQL injection" — 3.0.x is not listed
   (`sources/cve_v5.json`).
2. Fix commit `0bd57a879a0d54920bb9038a732645fb917040e9`, subject
   "[3.1.x] Fixed CVE-2021-35042 -- Prevented SQL injection in
   QuerySet.order_by()", states in its message: "Regression introduced in
   513948735b799239f3ef8c89397592445e1a0cd5 ... The main branch is not affected
   ..." and the release note it adds says "This regression appeared in 3.1 as a
   side effect of fixing :ticket:`31426`."
   (`sources/fix_0bd57a8_3.1.patch`, sha256
   `2eabb0113a6e3bfe83ee6303ccb4a46ba6943ad08b6930f012b15e2f10c3450b`.)
3. Code, `django/db/models/sql/query.py` `add_ordering()`:
   - 3.0.2 line 1901 rejects any string that does not match `ORDER_PATTERN`
     (`\?|[-+]?[.\w]+$` in `sql_constants_3.0.2.py`):
     `if not hasattr(item, 'resolve_expression') and not ORDER_PATTERN.match(item):`
     A payload such as `queries.name);` contains `;`/`)` and is rejected with
     `FieldError`.
   - 3.1.12 line 1900 (pre-fix) and 3.2.4 line 1972 (pre-fix) accept any string
     containing a dot and `continue` into the raw-alias path:
     `if '.' in item:`.
   - 3.1.13 line 1902 and 3.2.5 line 1974 restore the pattern check:
     `if '.' in item and ORDER_PATTERN.match(item):`.
4. The fix's regression test expects `Article.objects.order_by('queries.name);')`
   to raise `FieldError`, confirming that a dot-containing SQL fragment is the
   attack input.

Therefore the OSV/GHSA range with `introduced: 3.0a1` is over-inclusive for the
3.0 series; the CNA text, the fix commit message, and the code all place the
regression in 3.1. The snapshot 3.0.2 is **not affected**.

## Decision

Reject the candidate for this snapshot. Status is carried by
`runs/verification/candidate_dossiers.jsonl` (`triage_status=rejected`) and
`scripts/build_formal_tables.py --tables candidates`; no table row is deleted.

This is a range-applicability rejection, not a judgment that the advisory is
invalid: 3.1.0–3.1.12 and 3.2.0–3.2.4 are affected.

## Data-quality note

The pre-existing `sources/osv_ghsa.json` in this directory is **not** the record
for GHSA-xpfp-f569-q3p2: its content is GHSA-v3q9-2p3m-7g43 ("Token reuse in Ory
fosite"). It was left untouched for audit. The correct record fetched on
2026-10-22 is `sources/osv_ghsa_xpfp_f569_q3p2.json`
(sha256 `48a9ef8171fdcb61e1dc2fcf825791776086c8e69fce4d120c7c79c851355adc`).

## Limitations

- No Python runtime execution: the code comparison is static, at the exact
  tagged sources fetched from `raw.githubusercontent.com`.
- Line numbers refer to the files saved in `sources/`, not to the published
  release tarballs; blob identities were not compared against npm/PyPI wheels.
