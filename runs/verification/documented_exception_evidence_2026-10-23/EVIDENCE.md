# documented_exception evidence — 2026-10-23

Purpose: decide, with evidence rather than version-string intuition, whether the three
remaining legacy `documented_exception` repositories can be moved off their out-of-window
targets. The 4-year rule is applied against the review date 2026-10-23, i.e. the window is
2022-10-23 onward (the same threshold that rejected phoenix v1.6.13 at 2022-09-29).

All API responses were fetched over the proxy on 2026-10-23 and are stored next to this file.

## hyper (crates.io `hyper`)

Current target: `v0.14.2` (2021), rejected as `obsolete_release_over_4_years`.

Boundary queries against `https://api.osv.dev/v1/query` (package `crates.io/hyper`, exact
version):

| version | published | advisories returned |
| --- | --- | --- |
| 0.14.10 | 2021-07-07 | GHSA-f67m-9j94-qv9j, RUSTSEC-2022-0022 |
| 0.14.11 | 2021-07-21 | GHSA-f67m-9j94-qv9j, RUSTSEC-2022-0022 |
| 0.14.12 | 2021-08-24 | none |
| 1.0.0 | 2023-11-15 | none |
| 0.14.32 (latest 0.14) | 2024-12-16 | none |
| 1.12.0 (latest) | 2026-10-06 | none |

`osv_hyper_boundary.log`, `osv_query_hyper_0.14.32.json`, `osv_query_hyper_1.12.0.json`,
`crates_hyper_dates.log`.

Conclusion: the newest release that any published advisory covers is 0.14.11
(2021-07-21), roughly 15 months before the 4-year window opens. Every in-window release
(0.14.12 and later, plus all 1.x) carries no known advisory in OSV/RUSTSEC as of the
discovery cutoff. There is therefore no in-window tag on which a known positive could be
established; moving the target would require discovering a new vulnerability, not re-targeting.
Status: stays `documented_exception`. "No known advisory" is not a claim that hyper is safe.

## Newtonsoft.Json (NuGet `Newtonsoft.Json`)

Current target: `12.0.3` (2019-11-09), rejected as `obsolete_release_over_4_years`.

The only advisory returned for the package is `GHSA-5crp-9r3c-p9vr`
("Improper Handling of Exceptional Conditions in Newtonsoft.Json"), introduced 0, fixed
13.0.1. Exact-version queries:

| version | published | advisories returned |
| --- | --- | --- |
| 12.0.3 | 2019-11-09 | GHSA-5crp-9r3c-p9vr |
| 13.0.0 | not listed on nuget.org (unlisted) | GHSA-5crp-9r3c-p9vr |
| 13.0.1 | 2021-03-22 | none |
| 13.0.3 | 2023-03-08 | none |

`osv_newtonsoft_boundary.log`, `osv_query_newtonsoft_*.json`.

Conclusion: the only affected versions are 12.0.3 and earlier and 13.0.0, and 13.0.1 was
itself published 2021-03-22, so 13.0.0 predates that date and is outside the 4-year window by
more than a year. No in-window release is known to be affected. Status: stays
`documented_exception`.

## gin (Go `github.com/gin-gonic/gin`)

Unlike the two above, gin does have an in-window vulnerable tag, so it is NOT kept as a
documented exception; it is being re-targeted to v1.9.0.

| version | published | advisories returned by exact-version query |
| --- | --- | --- |
| 1.9.0 | 2023-02-21 | GHSA-2c4m-59x9-fr2g, GO-2023-1737 (CVE-2023-29401) |
| 1.10.0 | 2024-05 | none |
| 1.11.0 | 2025 | none |
| 1.12.0 | 2026 | none |

`osv_version_queries.log`.

Conclusion: v1.9.0 is the newest stable tag that any published advisory covers, and it is
inside the window, so it is the correct re-target. The positive (CVE-2023-29401,
`Context.FileAttachment` filename escaping) is under independent review in
`runs/independent/gin_CVE-2023-29401_v190_round1/`.

## What this does not establish

- Absence of advisories is not evidence of absence of vulnerabilities; it only means no
  known positive exists for those tags. hyper and Newtonsoft.Json stay documented exceptions
  and are not claimed safe.
- No network-wide audit of third-party databases beyond OSV (which mirrors GHSA, Go vulndb,
  PyPA, RustSec and CVE) was performed for this note.
