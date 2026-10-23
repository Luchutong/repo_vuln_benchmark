# CVE-2024-50341 — confirmed not affected at snap_39105a8a3ceb9fe4 (symfony v5.4.45)

Status: **not applicable to this evaluation snapshot**. The candidate
`disc2_35ba5cc08ffab29d21687940` should not be promoted; its triage row is marked
`rejected` with the blocker recorded below.

## Facts verified statically

- Advisory: symfony/security-bundle `>=6.2.0,<6.4.10`, `>=7.0.0,<7.0.10`,
  `>=7.1.0,<7.1.3` (GitHub advisory GHSA-jxgr-3v7q-3w9v, CVE-2024-50341,
  CWE-287, GHSA severity LOW). Issue: `Security::login` (programmatic login)
  does not run the firewall's custom `user_checker`, so a user a checker would
  reject can still be logged in.
- There is no 5.4 range in either the CNA record or the OSV/GHSA record, and the
  advisory's patch is published for branch 6.4 only.
- Fix commit: `22a0789a0085c3ee96f4ef715ecad8255cf0e105` ("use firewall-specific
  user checkers when manually logging in users", 2024-07-17). The patch touches
  `SecurityBundle/Security.php`, `SecurityExtension.php` and the
  `security.user_checker_locator` service.
- Content at the snapshot:
  - Tag peel: `v5.4.45^{}` = `2b66d7d7d8129531229708ef708860844db91944`,
    matching the snapshot's `vulnerable_commit`.
  - `git ls-tree -r v5.4.45 -- src/Symfony/Bundle/SecurityBundle/` contains **no**
    `Security.php` and no `security.user_checker_locator` wiring: the
    programmatic-login helper and the per-firewall checker locator were both
    added in 6.2, after the 5.4 branch diverged.
  - `git merge-base --is-ancestor 22a0789a v5.4.45^{}` reports not-an-ancestor
    (the 5.4 branch never received this change).
- The snapshot is therefore outside the affected range and does not carry the
  vulnerable code path.

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
