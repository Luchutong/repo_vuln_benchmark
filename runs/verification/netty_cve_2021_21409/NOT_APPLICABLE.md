# CVE-2021-21409 / GHSA-f256-j965-7f32 — duplicate of promoted CVE-2021-21295 at snapshot 4.1.59.Final

Candidate: `disc2_1e6dabf5089176b69f5406db` (was `in_validation`)
Repository: netty/netty, snapshot `snap_bb344e672a0544ef` (tag `netty-4.1.59.Final`, commit `97d044812dc84288ea2c44c0862c5b1c26cb5b2d`)
Decision date: 2026-10-22
Status after this note: `pending_location` (valid advisory, not a distinct entry at this snapshot)

## Finding

CVE-2021-21409 is not a second defect at 4.1.59.Final. It describes the one frame
ordering that the fix for CVE-2021-21295 (GHSA-wm47-8v5p-wjpj) failed to cover, and
its own advisory says so:

> The content-length header is not correctly validated if the request only use a
> single Http2HeaderFrame with the endStream set to to true. ... This is a followup
> of https://github.com/netty/netty/security/advisories/GHSA-wm47-8v5p-wjpj which
> did miss to fix this one case.

> ### Patches
> This was fixed as part of 4.1.61.Final

The CVE v5 record gives the same framing ("before version 4.1.61.Final ... This is a
followup of GHSA-wm47-8v5p-wjpj/CVE-2021-21295 which did miss to fix this one case"),
CVSS 3.1 5.9 MEDIUM `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:N`, CWE-444, and
`"versions": [{"status": "affected", "version": "< 4.1.61.Final"}]`. NVD repeats the
CNA text, publishes the same 5.9 MEDIUM vector as Primary and Secondary, and records
CWE-444 from both `nvd@nist.gov` and the GitHub secondary source.

CVE-2021-21295 is already promoted for this exact snapshot: `data/vulnerabilities.jsonl`
holds `GHSA-wm47-8v5p-wjpj` at `snap_bb344e672a0544ef`, commit `97d0448…`, location
`codec-http2/.../DefaultHttp2ConnectionDecoder.java` (round-1 verdict in
`runs/independent/netty_CVE-2021-21295_round1/`). Under the "one row per root-cause
location" schema used throughout this dataset, 21409 would duplicate that row: same
file, same sink, same missing check, same HTTP/2-to-HTTP/1.1 proxy precondition.

## Why the 21409-specific defect is not separately present at 4.1.59

The code 21409's fix edits exists only from 4.1.60.Final onward, because 21295's fix
created it:

- 4.1.59.Final decoder: zero occurrences of `CONTENT_LENGTH`, `contentLength` or
  `normalize`; `onHeadersRead` never reads the header, and `onDataRead` delivers DATA
  at line 292 without any length comparison. There is nothing to be "incorrectly
  validated", because nothing is validated at all — that is exactly CVE-2021-21295,
  already promoted.
- 4.1.60.Final decoder: adds `VALIDATE_CONTENT_LENGTH` (55), `contentLengthKey` (67),
  `verifyContentLength()` (234), the DATA-path call (314), the Content-Length
  normalization block gated by `if (!stream.isHeadersReceived())` (396-411), and the
  post-headers `verifyContentLength(stream, 0, endOfStream)` (415). The gate is what
  21409 is about: a new stream created with `endOfStream=true`
  (`connection.remote().createStream(streamId, endOfStream)`) is already in
  HALF_CLOSED_REMOTE state, so `isHeadersReceived()` is true and the normalization
  block is skipped.
- The 21409 fix (`b0fa4d5aab4215f3c22ce6123dd8dd5f38dc0432`, merged for
  4.1.61.Final) captures `isTrailers = stream.isHeadersReceived()` before the stream
  is created and changes the gate to `if (!isTrailers)`. In 4.1.61.Final the decoder
  contains `boolean isTrailers = false;` (356), `isTrailers = stream.isHeadersReceived();`
  (362) and `if (!isTrailers) {` (400). The patch's diff context matches 4.1.60/4.1.61,
  not 4.1.59: at 4.1.59 the line `// extract the content-length header` does not exist.

So at snapshot 4.1.59 the entire content-length validation is absent; 21409's
narrower endStream case is a subset of the already-promoted missing-validation
vulnerability, not a distinct root cause.

## Decision

Do not promote CVE-2021-21409 as a second vulnerability at `snap_bb344e672a0544ef`.
It is not marked `rejected`: the advisory is valid and its published range
(`< 4.1.61.Final`, i.e. 4.0.0 → 4.1.61.Final) does include 4.1.59. It is not
promoted because the dataset models one row per root-cause location, and that row
already exists as CVE-2021-21295. The candidate moves to `pending_location` with
blockers naming the duplicate relation and the code fact above.

If the dataset later requires one row per CVE identifier, 21409 must be promoted
against the same location with its own description and CWE/CVSS, not treated as an
alias of `GHSA-wm47-8v5p-wjpj`.

## Materials

All in `sources/`:

- `osv_GHSA-f256-j965-7f32.json` — OSV API response (aliases CVE-2021-21409,
  published 2021-03-30T15:10:38Z, `github_reviewed: true`, MODERATE, CWE-444;
  Maven `io.netty:netty-codec-http2` ECOSYSTEM interval 4.0.0 → 4.1.61.Final),
  sha256 `b36518b928b4871b3b6e5d2bc65cce7f8e90962f42811ec8555dd177129068b2`.
- `cve_v5_CVE-2021-21409.json` — CVE List v5 record, CNA GitHub_M, published
  2021-03-30T15:05:17Z, sha256
  `1912179d8fc49b698af93cc034fa97b3a9ed7a2f07b7bc0691d585806498d5dd`.
- `nvd_CVE-2021-21409.json` — NVD 2.0 API response, published
  2021-03-30T15:15:14.573, status Modified, sha256
  `7c0ca5c276a1cfe4b46c36318e87e934a67107d4bb16c011d223616da3237416`.
- `fix_commit_b0fa4d5.patch` — upstream commit patch, sha256
  `c6f6255986f459bf970212c8801033357527025173e415cf1e8510125d1bd68a`.
- `DefaultHttp2ConnectionDecoder_4.1.59.java` (739 lines, git blob
  `1bbaf632b50677231c15e62f71e66493bb17b6fc`), `_4.1.60.java` (810 lines) and
  `_4.1.61.java` (git blob `ac24992a10e…`, the patch's new blob) — raw files at
  the three tags.
- Tag refs (`git ls-remote`, run 2026-10-22):
  `netty-4.1.59.Final` da69023f → 97d044812dc84288ea2c44c0862c5b1c26cb5b2d;
  `netty-4.1.60.Final` f026e60f → eef26e8bb571612b76235841a84f605b9ae5d777;
  `netty-4.1.61.Final` 2885a7e0 → ccb3ff388f2eb0d107e746fc8b7222b98dd0339a
  (saved as `tag_refs_21409.txt`).

## Limitations

- The duplicate judgment rests on the advisory's own "followup / missed this one case"
  text plus the three file snapshots; no dynamic HTTP/2 test was run.
- Only `io.netty:netty-codec-http2` was considered. OSV also lists open-ended ranges
  for the `org.jboss.netty:netty` (3.x) and `io.netty:netty` aggregate coordinates;
  neither is the 4.1.59 artifact under audit.
- This is a deduplication decision, not a claim that 21409 is invalid as a CVE.
