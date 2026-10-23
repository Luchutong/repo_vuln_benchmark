# CVE-2025-61921 — reconnaissance only, no dossier

Candidate: `disc2_557b53e230e242da6d97eaef` (sinatra/sinatra, RubyGems `sinatra`),
snapshot `snap_916afbf76073e831` (tag v3.0.3, `cafaab99db5b644e5fbe2a19bdba168e671ff1f2`).

Range check: OSV GHSA-mr3q-g2mv-mr4q and CNA both state `introduced 0`, `fixed 4.2.0`,
so v3.0.3 is inside the affected range. Fix commits named by the candidate:
`3fe8c38dc405586f7ad8f2ac748aa53e9c3615bd` and
`8ff496bd4877520599e1479d6efead39304edceb`.

Why no dossier was prepared in this round: the published severity LEVELS disagree.

| Source | Score | Level |
| --- | --- | --- |
| CNA GitHub_M (CVE List v5) | CVSS 4.0 2.7 | LOW |
| OSV GHSA-mr3q-g2mv-mr4q (`database_specific.severity`) | CVSS 4.0 2.7 | LOW |
| NVD Primary (`nvd@nist.gov`, CVSS 3.1) | 7.5 | HIGH |
| NVD Secondary (`security-advisories@github.com`, CVSS 4.0) | 2.7 | LOW |

The level conflict would set `severity_consistent=false` and block promotion, so the
cycle was stopped at reconnaissance. The candidate stays `in_validation`; nothing in
`data/` was changed. The three saved advisory records are kept here so a later round
does not have to refetch them.

No reviewer was assigned, no dossier exists, and no formal table row may be derived
from this directory.
