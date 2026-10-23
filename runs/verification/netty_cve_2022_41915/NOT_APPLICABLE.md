# CVE-2022-41915 — confirmed not affected at snap_bb344e672a0544ef (netty 4.1.59.Final)

Status: **not applicable to this evaluation snapshot**. The candidate
`disc2_...` (netty/netty, aliases CVE-2022-41915 / GHSA-hh82-3pmq-7frp) should not
be promoted; its triage row is marked `rejected` with the blocker recorded below.
No dossier, reviewer, or formal row is created.

## Facts verified statically

- Advisory: `io.netty:netty-codec-http`, introduced 4.1.83.Final, fixed
  4.1.86.Final (GHSA-hh82-3pmq-7frp, CVE-2022-41915, CWE-113/CWE-436,
  CVSS 3.1 6.5 MEDIUM). Issue: `DefaultHttpHeaders.setObject(name,
  Iterable/array)` skipped header-value validation, so a CRLF value could be
  installed and lead to HTTP response splitting when proxied.
- Fix commit: `fe18adff1c2b333acb135ab779a3b9ba3295a1c4` ("Merge pull request
  from GHSA-hh82-3pmq-7frp", 2022-12-12). The patch adds
  `validateValue(valueValidator, name, converted)` in `DefaultHeaders.setObject`
  paths and introduces the pluggable `ValueValidator` in `DefaultHeaders`.
- Snapshot tag peel: `netty-4.1.59.Final^{commit}` =
  `97d044812dc84288ea2c44c0862c5b1c26cb5b2d`, matching the snapshot's
  `vulnerable_commit`.
- Code at the snapshot:
  - `codec/src/main/java/io/netty/handler/codec/DefaultHeaders.java`
    (blob `f246c032`, 34065 bytes, matches the inventory): `setObject(K,
    Iterable<?>)` and `setObject(K, Object...)` convert each value through
    `valueConverter.convertObject(v)`.
  - `codec-http/src/main/java/io/netty/handler/codec/http/DefaultHttpHeaders.java`
    (blob `b667de40`, 16086 bytes, matches the inventory): the default
    constructor uses `valueConverter(true)`, which returns
    `HeaderValueConverterAndValidator.INSTANCE`; its `convertObject`
    (lines 444-462) runs `validateValueChar` over every character and rejects
    CR/LF-ending values. Because the 4.1.59 `setObject` paths go through that
    converter, the suspicious iterator is validated.
  - The bypass appeared only with the 4.1.83 refactor that moved validation out
    of the converter into a separate `ValueValidator` passed to `DefaultHeaders`,
    while `setObject` was left calling the non-validating `fromObject`.
- `git merge-base --is-ancestor fe18adff netty-4.1.86.Final` returns 0, and the
  fix blob is absent at 4.1.59 (the snapshot predates the refactor by 24
  releases).
- The snapshot is therefore outside the affected range `<4.1.83` introduction
  point and its code path still validates header values.

## Consequence

This is a triage exclusion, not a verified vulnerability. The candidate row is
moved from `in_validation` to `rejected` in
`runs/verification/candidate_dossiers.jsonl`; rerunning
`scripts/build_candidate_dossiers.py` must preserve this exclusion. The negative
result is not written into `data/snapshot_vulnerability_status.jsonl`, which only
accepts promoted vulnerability ids.

Collected: 2026-10-22. Sources under `sources/`: CVE List v5, NVD, OSV/GHSA, fix
patch, and the 4.1.59 / 4.1.86 `DefaultHeaders` and `DefaultHttpHeaders` files.

## Distinction from promoted netty entries

CVE-2021-43797 (promoted) is the CRLF injection through *header name* validation
in the same codec; CVE-2022-41915 is about *value* validation in the `setObject`
iterator overloads introduced by a later refactor. Even if it applied, it would
be a separate root cause; here it does not apply because the vulnerable overload
behaviour does not exist at 4.1.59.
