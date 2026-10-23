# CVE-2026-44487 / GHSA-p92q-9vqr-4j8v — duplicate advisory of CVE-2026-44486

Candidate: `disc2_1139d5dd6253fa31bc99d00a` (status `pending_location`)
Repository: axios/axios, snapshot `snap_a64c7ddbbb7030b7` (v1.15.0)
Decision date: 2026-10-22

## Finding

CVE-2026-44487 describes the same defect as CVE-2026-44486 (GHSA-j5f8-grm9-p9fc):
a stale `Proxy-Authorization` header survives a redirect that is re-evaluated to a
direct connection and is then sent to the redirect target. The two advisories were
published 14 minutes apart (2026-06-04T14:15:01Z and 2026-06-04T14:19:53Z) and
point at the same fix.

Evidence:

- The OSV record for GHSA-p92q-9vqr-4j8v states that "the `1.x` fix in commit
  `afca61a` changes `setProxy(options, configProxy, location, isRedirect)` so
  redirect re-invocation removes every case variant of `Proxy-Authorization`"
  and that the 0.x release 0.32.0 carries the backport-style
  `removeProxyAuthorization()` guard. This is the fix commit and backport already
  verified for CVE-2026-44486 (`afca61a070728e717203c2bc21e7b589b59b858b`,
  `2af6116a957b1dd1b32056181326da8a5540d3bc`).
- Both records give the same affected ranges: npm axios `>=1.0.0,<1.16.0` and
  `<0.32.0`, with fixed releases 1.16.0 and 0.32.0.
- Both place the flaw in `lib/adapters/http.js` `setProxy()` and the redirect
  re-invocation.
- The only substantive differences are editorial: 44487 is written around the
  HTTP-to-HTTPS origin-leak scenario and is classified CWE-201 (insertion of
  sensitive information into sent data), while 44486 covers the general proxy
  re-evaluation case and is classified CWE-200 (exposure of sensitive
  information). Neither is a separate root cause.

## Decision

Do not create a second vulnerability/location/evidence set for CVE-2026-44487 and
do not promote it separately. The dataset models one row per root-cause location;
duplicating the row would inflate the vulnerability count with a second CVE for
the same code and the same fix. The candidate stays `pending_location` rather
than `rejected`, because the advisory is valid and not withdrawn — it is simply
not a distinct entry under the current schema.

If the dataset later requires one row per CVE identifier, this decision must be
revisited and 44487 promoted against the same location with its own CWE and
description, not treated as an alias of 44486.

## Materials

- `sources/osv_GHSA-p92q-9vqr-4j8v.json` — OSV API response, sha256
  `5ab42f7102b7b44e44f0c81b360e60064700d6397c85336b70e4de4611fb8949`,
  retrieved 2026-10-22.
- CVE-2026-44486 materials live in `runs/verification/axios_cve_2026_44486/`
  (git object checks for afca61a/2af6116, v1.15.0 source, fix and backport
  patches).

## Limitations

- The duplicate judgment rests on the advisory text, fix references and ranges;
  no separate dynamic test was run for either CVE.
- The CVE List v5 record for 44487 was not saved in this directory; only the OSV
  record and the previously saved 44486 primary records were compared.
