# Range-scope triage — disposition of the independent audit (2026-10-23)

The audit in `audit/AUDIT.md` (independent reimplementation, 47-row stratified
sample, 27 adversarial probes) returned **apply after fixes** and split the
proposals by kind. This file records what was changed and what was applied.

## Fixes to `v031/scripts/triage_range_scope.py`

| Defect | Fix |
|---|---|
| D1 — `out_of_scope_product` proposals carried no `evidence_urls` (schema `minItems: 1`, 161/1666 rows invalid on apply) | The out-of-scope branch now emits `https://nvd.nist.gov/vuln/detail/<id>` for every mismatched record. |
| D2 — CPE product mismatch alone was treated as third-party attribution | New veto `mentions_repo()`: if the alias-matched NVD description names this repository's product, the row stays `indeterminate`. `no_matching_package` now carries the description so the veto can see it. |
| D4 — an open `introduced: "0"` range returned `False` (`range_contains`) | A range that ends with any open introduced event now returns `None` (unsupported/indeterminate) instead of "not affected". |
| D5 — `versionEndExcluding: 0.0.0` was used as a real upper bound | `0.0.0` is treated as a "no bound" sentinel after the parse check and dropped. |

## Fixes to `v031/scripts/apply_range_triage.py`

| Defect | Fix |
|---|---|
| D3 — 148 NVD-backed rows rendered an empty range list because only `bounds` was read | `detail_bounds()` falls back to `cpe_matches` and renders the CPE criteria with its version bounds. |
| — | New `--only-proposal` filter so a proposal kind can be withheld from an apply. |
| Overstatement | The basis template no longer claims the fix is "included" by branch ancestry; it says the snapshot is outside the advisory range by version ordering and that ancestry was not verified. |

## Regeneration and delta (proposals v1.1, `proposals_v1_1.jsonl`)

| Proposal | v1.0 | v1.1 |
|---|---|---|
| `not_affected_range` | 407 | 406 |
| `possible_affected_range` | 176 | 177 |
| `out_of_scope_product` | 161 | 42 |
| `indeterminate` | 456 | 576 |
| rows | 1200 | 1201 (axios `adv3_efa9936e479dbcf0` added since v1.0) |

The single lost `not_affected_range` row is `disc2_cbbf645dec334f9187b6897a`
(1.7.16): D5 previously closed it on a `0.0.0` upper bound; it is now
`possible_affected_range`. The 119 rows that became `indeterminate` are D2
vetoes (description names the product) — `CVE-2022-40281`
(`disc2_dd7fbfdb878aeb1d1202444b`) remains `unknown` as the audit required.

## Applied

`apply_range_triage.py . --proposals …/proposals_v1_1.jsonl
--only-proposal not_affected_range --apply` — 406 rows became
`confirmed_not_affected` / `trusted_range_with_branch`, backup
`runs/data_fixes/snapshot_candidate_triage_before_range_scope_2026-10-22T190955Z.jsonl`.

**Not applied:** all `out_of_scope_product` proposals. D1 is fixed for future
regeneration, but the audit found the attribution rule itself unsound (D2) and
the generator changed after v1.0, so no out-of-scope row is written in this
pass. They stay `unknown` and are counted as unresolved.

## Basis-text correction

`runs/data_fixes/correct_range_scope_basis_2026-10-23.py` rewrote "The snapshot
(…) descends from the fixed release(s), so the fix is included." on 449 rows
(406 range-scope rows + 43 axios migration rows) to state that this is a
version-ordering deferral and that fix ancestry was not verified. One echo row
that cites `patched_versions: 4.15.2` for snapshot v4.15.2 keeps its wording:
there the patched release *is* the snapshot, not an ancestry inference.
