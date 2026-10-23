# Small evaluation snapshots — candidates outside the pinned version

Decision date: 2026-10-22. Basis: published OSV ranges recorded in
`runs/verification/candidate_dossiers.jsonl`, compared with the exact snapshot
version. No code was executed.

## Rule

Affected when some interval has `introduced <= V < fixed`. Not applicable when every
interval is fixed at/before the snapshot or introduced after it. Only ECOSYSTEM/SEMVER
ranges are evaluated; ranges whose events are commit SHAs are skipped.

## expressjs/express 4.19.2 (`snap_3166f788b2c56baa`) — 1 not applicable

Package: npm `express`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_1dc6c7b967eb67e1dc99a182 | CVE-2024-29041 | 0..4.19.2, 5.0.0-alpha.1..5.0.0-beta.3 | fixed before/at snapshot, or introduced after it |

## guzzle/guzzle 7.4.4 (`snap_efe695448113758a`) — 2 not applicable

Package: Packagist `guzzlehttp/guzzle`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_3a0aaa371dcf1dc2fa150654 | CVE-2022-29248 | 0..6.5.6, 7.0.0..7.4.3 | fixed before/at snapshot, or introduced after it |
| disc2_274c99eb788c7e30ecbebcc6 | CVE-2022-31042 | 4.0.0..6.5.7, 7.0.0..7.4.4, 4.0.0..6.5.7, 7.0.0..7.4.4 | fixed before/at snapshot, or introduced after it |

## hyperium/hyper 0.14.2 (`snap_735b41cb13177d03`) — 1 not applicable

Package: crates.io `hyper`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_673cb1d821f399d033787991 | CVE-2016-10932 | 0..0.9.4, 0.0.0-0..0.9.4 | fixed before/at snapshot, or introduced after it |

## laravel/framework 11.30.0 (`snap_6e1f42aa46ca4df5`) — 7 not applicable

Package: Packagist `laravel/framework` and `illuminate/*`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_a1955455d1789bedf9309597 | CVE-2020-24941 | 0..6.18.35, 7.0.0..7.24.0 | fixed before/at snapshot, or introduced after it |
| disc2_ffb7a21bd48667f0d6a2a949 | CVE-2017-9303 | 5.4.0..5.4.22, 5.4.0..5.4.22 | fixed before/at snapshot, or introduced after it |
| disc2_8b8cba5df26ab563383abf2f | CVE-2018-15133 | 5.6.0..5.6.30 | fixed before/at snapshot, or introduced after it |
| disc2_8dd70a22ce5a65d2cb3cb324 | CVE-2020-19316 | 0..5.8.17 | fixed before/at snapshot, or introduced after it |
| disc2_afdc3d85a1299c2228b1adb9 | CVE-2021-43808 | 0..6.20.42, 7.0.0..7.30.6, 8.0.0..8.75.0, 0..6.20.42, 7.0.0..7.30.6, 8.0.0..8.75.0 | fixed before/at snapshot, or introduced after it |
| disc2_24bf4fb197538aa01257511a | GHSA-7852-w36x-6mf6 | 0..5.5.40, 5.6.0..5.6.15 | fixed before/at snapshot, or introduced after it |
| disc2_43f5ddd764b1cfe1ef4f9568 | GHSA-rj3w-99gc-8j58 | 4.0.0..4.1.29 | fixed before/at snapshot, or introduced after it |

## pallets/flask 2.3.1 (`snap_8ed1cab47a0b7011`) — 2 not applicable

Package: PyPI `flask`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_805dafd76a71ad8a066ce9b6 | CVE-2018-1000656 | 0..0.12.3, 0..0.12.3 | fixed before/at snapshot, or introduced after it |
| disc2_b09ec4fc5f977ddc4571b2d5 | CVE-2025-47278 | 3.1.0..3.1.1, 3.1.0..3.1.1 | fixed before/at snapshot, or introduced after it |

## pallets/werkzeug 3.0.2 (`snap_b57262de7996e8a2`) — 6 not applicable

Package: PyPI `werkzeug` (ECOSYSTEM ranges; GIT ranges skipped).

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_4c125b6a3ea4f61e99945fb4 | CVE-2016-10516 | 0..0.11.11, 0..0.11.11 | fixed before/at snapshot, or introduced after it |
| disc2_88e80973a08639e4f6952082 | CVE-2019-14806 | 0..0.15.3, 0..0.15.3 | fixed before/at snapshot, or introduced after it |
| disc2_7a58bfd94e1651b680e4e7cc | CVE-2022-29361 | 0..2.1.1 | fixed before/at snapshot, or introduced after it |
| disc2_0e5f9ddecfdcf8e9d2bd29a4 | CVE-2023-23934 | 0..2.2.3, 0..2.2.3 | fixed before/at snapshot, or introduced after it |
| disc2_2d5ea55f11bb6d5c764e395b | CVE-2023-25577 | 0..2.2.3, 0..2.2.3 | fixed before/at snapshot, or introduced after it |
| disc2_729d15ee9ce50e6f20872efb | CVE-2023-46136 | 3.0.0..3.0.1, 2.0.0rc1..2.3.8, 0..2.3.8, 3.0.0..3.0.1 | fixed before/at snapshot, or introduced after it |

## phoenixframework/phoenix 1.6.13 (`snap_ee79f4175242bbee`) — 1 not applicable

Package: Hex `phoenix`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_d0815ac298e1db8eb22e83a3 | CVE-2026-32689 | 1.7.0..1.7.22, 1.8.0..1.8.6, 1.7.0..1.7.22, 1.8.0..1.8.6 | fixed before/at snapshot, or introduced after it |

## rustls/rustls 0.23.4 (`snap_b3a6891886ef2160`) — 1 not applicable

Package: crates.io `rustls`.

| Candidate | CVE | intervals | Why not affected |
|---|---|---|---|
| disc2_5e10dfbed0a5d9cdcf448c09 | GHSA-2mjx-qc3c-rqvc | 0.23.13..0.23.45, 0.23.13..0.23.45 | fixed before/at snapshot, or introduced after it |

## What this report does not decide

- Candidates whose intervals contain the snapshot version remain `in_validation`;
  they are listed in the screening output and are not part of this rejection.
- No code-level claim is made; exclusions use published ranges only.
