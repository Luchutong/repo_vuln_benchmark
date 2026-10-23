# CVE-2024-0853 — confirmed not affected at snap_0ec1c11542393304 (curl 8.3.0)

Status: **not applicable to this evaluation snapshot**. The candidate
`disc2_dfcab5985b2d1ec353cc4edc` (curl/curl, alias CVE-2024-0853) should not be
promoted; its triage row is marked `rejected` with the blocker recorded below.
No dossier, reviewer, or formal row is created.

## Facts verified statically

- Advisory: CURL-CVE-2024-0853 (also CVE-2024-0853), "OCSP verification bypass
  with TLS session reuse", CWE-299, severity **Low**. The saved record
  (`sources/curl_CVE-2024-0853.json`) lists:
  - SEMVER range introduced `8.5.0`, fixed `8.6.0`;
  - GIT range introduced `395365ad2d9a6c3f1a35d5e268a6af2824129832`, fixed
    `c28e9478cb2548848eca9b765d0d409bfb18668c`;
  - `versions: ["8.5.0"]` and `last_affected: "8.5.0"` — upstream states that
    only 8.5.0 is affected.
- NVD records CVSS 3.1 5.3 MEDIUM (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N), no
  CWE, and no CPE configuration list. The level difference from curl's "Low"
  is noted but is not decisive here: the version check settles the candidate.
- The flaw was introduced by `395365ad` ("openssl: when a session-ID is reused,
  skip OCSP stapling"): it sets `connssl->reused_session` and changes
  `servercert()` to run `verifystatus()` only when
  `conn_config->verifystatus && !connssl->reused_session`. Reusing a cached
  session therefore skips the OCSP stapling check — that skip is the bypass.
- Snapshot 8.3.0 (`curl-8_3_0` = `6fa1d817e5b1a00d7d0c8168091877476b499317`):
  `git merge-base --is-ancestor 395365ad 6fa1d817` exits 1, so the introducing
  commit is not in the snapshot's history. Both `lib/vtls/vtls_int.h` and
  `lib/vtls/openssl.c` at the snapshot have no `reused_session` symbol, and
  `servercert()` still runs `verifystatus()` unconditionally (lines 3747 and
  4233 of `openssl.c`). The vulnerable path does not exist at 8.3.0.

## Consequence

This is a triage exclusion, not a verified vulnerability. The candidate row is
moved from `pending_version` to `rejected` in
`runs/verification/candidate_dossiers.jsonl` and `data/candidates.jsonl`.
Rerunning `scripts/build_candidate_dossiers.py` would regenerate the row and
must not be run without preserving this exclusion. The negative result is not
written into `data/snapshot_vulnerability_status.jsonl`, which only accepts
promoted vulnerability ids.

Collected: 2026-10-22. Sources under `sources/`: CURL-CVE JSON, NVD JSON, and
the git object checks (tags, introducing commit, ancestry, blob greps).

## Note on the candidate's discovery record

The candidate came from an NVD keyword hit and carried no affected ranges, no
CWE, no severity and no references (`triage_status` was `pending_version` with
"no fixed version event" blockers). The exclusion above supplies the missing
range from the upstream CURL-CVE record; it is not an inference from the NVD
text, which does not state versions.
