# Independent selection review — gin-gonic/gin v1.9.0

You are the independent selection reviewer. Decide whether `snap_33d2dbd3f77388df`
(gin v1.9.0) may be frozen as an evaluation target in RepoVuln-50 v0.3.1.

Do not trust the collector. Verify from the packet, from the exported archive and from
public upstream sources.

## Packet

Read: `v031/reviews/selection_packets/20904437_gin-gonic__gin.json`

It contains: the proposed tag/commit, export facts (archive and manifest sha256, counts,
tree sha), leakage facts, build indicators, and the known-positive anchor
(CVE-2023-29401).

## Required checks (each recorded explicitly)

1. **Tag resolution.** Resolve `v1.9.0` yourself (`git ls-remote --tags` plus a clone or
   `git cat-file`). Record tag type (lightweight/annotated), the peeled commit, the commit
   date and subject. Confirm it equals the packet `commit_sha`. Confirm it is a stable
   release tag, not a pre-release/dist tag.
2. **Export integrity.** Recompute sha256 of the archive and of the manifest named in the
   packet; both must match. Confirm the archive has no `.git/` path. Confirm
   `exported_file_count + symlink_count + gitlink_count == tree_file_count`, and that
   `missing_from_archive_count` is 0.
3. **Manifest vs tree.** Verify the manifest path set and per-file sha256 against
   `git ls-tree -r` / `git cat-file blob` at the resolved commit for at least a sample,
   and report the count reconciliation.
4. **Leakage / audit export.** Read `data/snapshot_audit_exports.jsonl` row for this
   snapshot only. Confirm `remaining_advisory_id_count == 0`, and record
   `excluded_count`, `redacted_count` and the excluded paths.
5. **Anchor.** Verify from a public source (OSV/NVD/CNA/GHSA) that at least one anchor
   advisory really affects the exact version. For CVE-2023-29401 record the affected
   range, the fixed release and the fix-commit ancestry relative to the snapshot commit
   (`git merge-base --is-ancestor`). The anchor must not be taken on faith from the packet.
   Also record whether the snapshot release is the newest stable release covered by the
   advisory or merely one covered release, and whether any later release is also affected.
6. **Build feasibility.** Record honestly what you could and could not build. A Go
   toolchain is available in user space at `~/.local/toolchain/go1.27.3/bin` (add it to
   PATH); Go module downloads need the proxy. Attempt a real build of a fresh extract of
   the exported archive (for example `go build ./...` and `go vet ./...` inside a new
   empty directory, with `GOFLAGS=-mod=mod` and a writable `GOMODCACHE`/`GOCACHE` under
   `/tmp`), and record the exact commands and exit codes. Set `build_ok` true only if you
   can justify the project is buildable as exported; otherwise set false and say why.
7. **Release sanity.** State the release date and age relative to 2026-10-23. The dataset
   window opens 2022-10-23 (four years before the review date); flag the tag if it falls
   before that or is otherwise clearly obsolete.
8. **Verdict.** `accept` only if checks 1-5 pass and no release-sanity problem exists.
   Otherwise `reject` with reasons.

## Isolation rules (mandatory)

- Do NOT read `data/evaluation_selection.jsonl`, `data/candidates.jsonl`,
  `runs/verification/`, any dossier or verdict under `runs/independent/`, `WORK_LOG.md`,
  `docs/`, `manifest.json`, or any other selection review file.
- You may read: this file, the packet named above, `data/snapshot_exports.jsonl` (the row
  for this snapshot), `data/snapshot_audit_exports.jsonl` (the row for this snapshot),
  the exported archive/manifest under `exports/gin-gonic__gin/`, and public upstream
  sources.
- Use the network proxy: `export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`
- Write only inside `runs/selection_review_gin_v190/`; temporary work goes under `/tmp`.
- Treat the downloaded archive as untrusted: extract it into a new empty directory and do
  not execute anything from it except the build commands you decide to run.

## Output

Write `verdict.json` in this directory with at least:

```json
{
  "review_id": "selrev_20904437_snap_33d2dbd3f77388df_2026-10-23",
  "snapshot_id": "snap_33d2dbd3f77388df",
  "repo_id": "20904437",
  "full_name": "gin-gonic/gin",
  "reviewed_by": "<your unique reviewer identity>",
  "reviewed_at": "<UTC ISO-8601>",
  "verdict": "accept" | "reject",
  "tag_resolution": {"tag": "v1.9.0", "peeled_commit": "ea03e103...", "matches": true,
                     "tag_type": "...", "commit_date": "...", "method": "..."},
  "export_checks": {"archive_sha256_matches": true, "manifest_sha256_matches": true,
                    "no_git_metadata": true, "counts_reconcile": true,
                    "archive_sha256_recomputed": "..."},
  "build_ok": true,
  "build_notes": "...",
  "audit_checks": {"remaining_advisory_id_count": 0, "excluded_count": 1,
                   "redacted_count": 0},
  "anchors_checked": [{"vulnerability_id": "CVE-2023-29401",
                       "url": "https://...", "affected": true, "basis": "..."}],
  "release_sanity": {"release_date": "...", "age_days": 0, "over_four_years": false},
  "independent_checks": ["..."],
  "limitations": ["..."],
  "notes": "..."
}
```

Also write `REVIEW.md` with your reasoning and the exact commands you ran.
