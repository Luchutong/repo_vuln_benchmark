# Independent selection review — axios/axios, proposed target v1.19.0

You are the independent selection reviewer. The collecting side proposes freezing this snapshot as
the repository's evaluation target. Verify the proposal from the packet, the frozen export and
public sources, and return your own verdict. Do not trust this claim.

## Proposal under review

- Repository `axios/axios`, repo_id 23088740, canonical URL https://github.com/axios/axios
- Proposed snapshot `snap_04c033042a3d52eb`, tag `v1.19.0`, commit
  `311fcc5c8d989b7248f05d390bb83bfbfb009977`
- Packet: `v031/reviews/selection_packets/23088740_axios__axios.json` (read this; it is the only
  packet you may read)
- Source export: `exports/axios__axios/snap_04c033042a3d52eb.tar.gz` and
  `exports/axios__axios/snap_04c033042a3d52eb.manifest.jsonl`
- Claimed archive sha256 `f6db8b2488222d3e30891fd8f5f4afd71cdb7f48d5e9d3bbf07a117d376b550f`,
  836609 bytes; claimed manifest sha256
  `3447a262b2eefe1e9b4087f8a46d31121302d36644bfa6bfa44115da3e4934b0`
- Claimed tree `e235490f75463ad553dca06d75427aa17c1ab647`, 456 tracked files, 456 exported,
  0 symlinks, 0 gitlinks, 0 missing from archive, no `.git` anywhere
- Claimed anchor: `CVE-2026-101907` / `GHSA-r4gj-5m52-g5wh`, npm `axios` `>= 1.17.0, < 1.20.0`;
  v1.19.0 is inside the range. (An earlier candidate rejection concerned v1.15.0, which predates the
  range; it is not an assessment of v1.19.0.)
- Claimed leakage facts: no `.git`; advisory identifiers exist in `CHANGELOG.md` and
  `THREATMODEL.md` (CVE-2023-45857, CVE-2024-39338 sampled). Treat a non-zero count as a
  disclosure item to record, not as a failed check, and say whether the identifiers name this
  snapshot's own vulnerability or only historical ones.

## Required checks

1. Resolve the tag yourself against the upstream repository (`git ls-remote --tags`, a fresh clone
   or `git cat-file`): annotated vs lightweight, tag object SHA if annotated, peeled commit, commit
   date and subject. Confirm or refute that `v1.19.0` peels to `311fcc5c8d989b7248f05d390bb83bfbfb009977`,
   that `package.json` says `1.19.0` at that commit, and that the tree SHA is
   `e235490f75463ad553dca06d75427aa17c1ab647`.
2. Confirm `v1.19.0` is a stable release tag (not rc/beta/alpha/dist/channel) and record its release
   date and age relative to 2026-10-23. The dataset window opens 2022-10-23.
3. Recompute `sha256sum` of the archive and the manifest; compare with the packet and with the
   claimed values above. List the tar entries and confirm: no `.git` path of any kind, no symlinks,
   no hardlinks, no gitlinks, all regular files, and that 456 entries plus 0 symlinks reconciles
   with the claimed tracked-file count. Independently check that the files in the archive match the
   tag's `git ls-tree -r` file set (names and modes), not only the count.
4. Extract the archive into a new empty directory under `/tmp` and run a real build:
   `npm ci` (or `npm install` if the lockfile rejects) then `npm run build`. Report exact commands,
   Node/npm versions, exit codes and the produced artifacts. `build_ok` may be `true` only if a
   build actually succeeded. If the network or a dependency blocks it, say exactly what and set
   `build_ok` to `false`.
5. Verify the anchor from public sources yourself (OSV `GHSA-r4gj-5m52-g5wh` and `CVE-2026-101907`,
   NVD, the GitHub repository advisory, the rendered advisory page): affected range, patched
   version, severity, and whether v1.19.0 is inside the range. Also record that NVD is
   `Awaiting Analysis` with no CPE configurations and only a secondary CVSS metric if that is what
   you observe. `affected` may be `true` only with a public `https://` source URL.
6. Decide the verdict yourself. `accept` only if every mandatory export check passes, the tag
   resolves exactly, a build succeeds, and the anchor really affects this version. Otherwise
   `reject` with reasons.

## Output

Write `review.jsonl` in this directory with exactly one JSON object:

```json
{
  "review_id": "selrev_23088740_snap_04c033042a3d52eb_<date>",
  "repo_id": "23088740",
  "snapshot_id": "snap_04c033042a3d52eb",
  "reviewed_by": "<your unique reviewer identity, not the selector>",
  "reviewed_at": "<UTC ISO-8601>",
  "verdict": "accept" | "reject",
  "export_checks": {"archive_sha256_matches": true, "manifest_sha256_matches": true,
                    "no_git_metadata": true, "counts_reconcile": true},
  "tag_resolution": {"tag": "v1.19.0", "matches": true,
                     "peeled_commit": "311fcc5c8d989b7248f05d390bb83bfbfb009977",
                     "tag_age_days": 0, "release_date": "YYYY-MM-DD"},
  "build_ok": true,
  "anchors_checked": [{"vulnerability_id": "CVE-2026-101907", "url": "https://...",
                       "affected": true, "source": "..."}],
  "reasons": ["..."],
  "limitations": ["..."]
}
```

Also write `REVIEW.md` with your reasoning and every command you ran verbatim.

## Isolation rules (mandatory)

- Do NOT read `data/evaluation_selection.jsonl`, `data/candidates.jsonl`,
  `data/snapshot_candidate_triage.jsonl`, `data/vulnerabilities.jsonl`, `data/locations.jsonl`,
  `data/reviews.jsonl`, `data/snapshot_vulnerability_status.jsonl`, any dossier or verdict under
  `runs/verification/` or `runs/independent/` (other than this directory), `runs/language/`,
  packets other than this repository's, `WORK_LOG.md`, `docs/`, `manifest.json`, or
  `HANDOFF_V031.md`.
- You may read: this file, your packet, `data/snapshots.jsonl`, `data/snapshot_exports.jsonl`,
  the export archive/manifest, and public upstream sources.
- Write only inside `runs/independent/selection_axios_v1190_2026-10-23/`; temporary work goes under
  `/tmp`.
- Network: `export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`
- Downloaded code is untrusted: extract into its own new, empty directory; keep your scripts and
  tests outside the clone; run any Python that reads the clone with `python3 -I`.
- Docker is unavailable on this host.
