# CVE-2024-43045 — corrections after the round-1 independent review

Independent review: `runs/independent/jenkins_CVE-2024-43045_round1/verdict.json`
(`deepseek-flash (independent review agent)`, 2026-10-21T19:08:08Z). Verdict
`vulnerable_commit`, grade B, 18/19 `fields_verified` true, `cvss: false`.

The raw collected sources under `sources/` are left untouched (their recorded
`sha256_of_observation` values still match). The corrections below were applied
to the dossier's summaries and severity block only.

1. CVSS. `sources/git_object_checks.txt` and the first dossier draft said
   "OSV/GHSA: same CVSS 3.1 vector" as NVD. That is wrong. NVD Primary
   (`nvd@nist.gov`) and NVD Secondary (CISA-ADP, source
   `134c704f-9b21-4f2e-91b3-4a467353bcc0`) publish
   `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L` = 6.3 MEDIUM. GHSA
   `GHSA-8pv9-qh96-9hc6` publishes
   `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` = 5.4 MEDIUM (A:N). The OSV
   record for the CVE itself repeats NVD's 6.3 vector. Levels agree (MEDIUM);
   the vectors do not, and the dossier now lists all three instead of asserting
   equality.
2. Fix commits. `efece77d` is the 2.462.x backport (direct parent of the 2.462.1
   release commit `acc86685`), not the 2.452.x one. The 2.452.x fix is
   `0c13259c` (direct parent of the 2.452.4 release commit `c5a3ba54`). The
   weekly fix `3752f406` and the 2.471 release commit are unchanged.
3. `getACL()`. It is not "never used as an access gate": it backs the
   `checkPermission(View.CREATE)` calls in `doCreateView` (line 190) and
   `doViewExistsCheck` (line 200). It is not consulted when the My Views action
   is read, which is the vulnerability.
4. CWE. GHSA/OSV list CWE-285 in addition to CWE-862; the dossier now records
   both.

The round-1 verdict is not edited. Because the promotion gate requires every
matching `fields_verified` value to be true, this dossier remains
`PENDING_INDEPENDENT_REVIEW` and `promote_verified.py` keeps it pending. A
future independent review of the corrected claim would be a new verdict file,
not a rewrite of this one.
