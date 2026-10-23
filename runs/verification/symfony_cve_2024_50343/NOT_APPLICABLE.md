# CVE-2024-50343 — confirmed not affected at snap_39105a8a3ceb9fe4 (symfony v5.4.45)

Status: **not applicable to this evaluation snapshot**. The candidate
`disc2_dd1aa213fa864be8ab94a915` should not be promoted; its triage row is marked
`rejected` with the blocker recorded below.

## Facts verified statically

- Advisory: symfony/validator `<5.4.43`, `<6.4.11`, `<7.1.4` (GitHub advisory
  GHSA-g3rh-rrhp-jhh9, CVE-2024-50343). Issue: a regex using `$` can accept input
  ending in `\n`; the fix adds the PCRE `D` modifier.
- Fix commit: `7d1032bbead9a4229b32fa6ebca32681c80cb76f` ("[Validator] Add `D`
  regex modifier in relevant validators", 2024-08-13).
- Ancestry (`git --git-dir=/tmp/symfony_git merge-base --is-ancestor`):
  - `7d1032bb` **is** an ancestor of `v5.4.45` (exit 0) and of `v5.4.47`.
  - Tag peel: `v5.4.45^{}` = `2b66d7d7d8129531229708ef708860844db91944`,
    matching the snapshot's `vulnerable_commit`.
- Content:
  - At `v5.4.45`, `src/Symfony/Component/Validator/Constraints/EmailValidator.php`
    lines 28-29 already end with `$/D`, and `UrlValidator` uses the patched
    pattern.
  - At `v5.4.42`, the same `EmailValidator::PATTERN_HTML5` ends with `$/`
    without the modifier, showing the change happened before 5.4.45.
- The snapshot is therefore **above** the fixed version for the 5.4 branch and
  does not carry the vulnerable code.

## Consequence

No dossier, reviewer, or formal row is created. This is a triage exclusion, not a
verified vulnerability: `data/snapshot_vulnerability_status.jsonl` only accepts
`vulnerability_id` values that exist in `data/vulnerabilities.jsonl`, so the
negative result is recorded here and in `WORK_LOG.md` / findings rather than in
the truth matrix. The candidate row was moved from `in_validation` to `rejected`
in `runs/verification/candidate_dossiers.jsonl`; rerunning
`scripts/build_candidate_dossiers.py` would recompute that status from the
upstream advisory data and must preserve this exclusion.

Collected: 2026-10-22. Sources kept under `sources/` (NVD, CVE v5, OSV/GHSA,
symfony.com page, fix patch, GHSA HTML).
