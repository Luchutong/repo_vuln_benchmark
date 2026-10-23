# Independent selection review — phoenixframework/phoenix v1.8.8

You are the independent selection reviewer. Decide whether `snap_aca73214a7703174`
(phoenix v1.8.8) may be frozen as an evaluation target in RepoVuln-50 v0.3.1.

Do not trust the collector. Verify from the packet, from the exported archive and from
public upstream sources.

## Packet

Read: `v031/reviews/selection_packets/16072585_phoenixframework__phoenix.json`

It contains: the proposed tag/commit, export facts (archive and manifest sha256, counts,
tree sha), leakage facts, build indicators, and the known-positive anchor
(CVE-2026-56811).

## Required checks (each recorded explicitly)

1. **Tag resolution.** Resolve `v1.8.8` yourself (`git ls-remote --tags` plus a clone or
   `git cat-file`). Record tag type (lightweight/annotated), the peeled commit, the commit
   date and subject. Confirm it equals the packet `commit_sha`. Confirm it is a stable
   release, not a dist/channel/pre-release tag.
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
   advisory really affects the exact version. For CVE-2026-56811 record the affected
   range, the fixed release and the fix-commit ancestry relative to the snapshot commit
   (`git merge-base --is-ancestor`). The anchor must not be taken on faith from the packet.
6. **Build feasibility.** Record honestly what you could and could not build. Node is
   available; Elixir/Erlang are not. If you attempt a build, record the exact commands and
   exit codes. Set `build_ok` true only if you can justify the project is buildable as
   exported (an attempted successful build, or a documented structural/feasibility
   determination that you state explicitly). If you cannot justify it, set false.
7. **Release sanity.** State the release date and age relative to 2026-10-23. Flag it if
   the tag is over four years old or clearly obsolete.
8. **Verdict.** `accept` only if checks 1-5 pass and no release-sanity problem exists.
   Otherwise `reject` with reasons.

## Isolation rules (mandatory)

- Do NOT read `data/evaluation_selection.jsonl`, `data/candidates.jsonl`,
  `runs/verification/`, any dossier or verdict under `runs/independent/`, `WORK_LOG.md`,
  `docs/`, `manifest.json`, or any other selection review file.
- You may read: this file, the packet named above, `data/snapshot_exports.jsonl` (the row
  for this snapshot), `data/snapshot_audit_exports.jsonl` (the row for this snapshot),
  the exported archive/manifest under `exports/phoenixframework__phoenix/`, and public
  upstream sources.
- Use the network proxy: `export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`
- Write only inside `runs/selection_review_phoenix_v188/`; temporary work goes under `/tmp`.

## Output

Write `verdict.json` in this directory with at least:

```json
{
  "review_id": "selrev_16072585_snap_aca73214a7703174_2026-10-23",
  "snapshot_id": "snap_aca73214a7703174",
  "repo_id": "16072585",
  "full_name": "phoenixframework/phoenix",
  "reviewed_by": "<your unique reviewer identity>",
  "reviewed_at": "<UTC ISO-8601>",
  "verdict": "accept" | "reject",
  "tag_resolution": {"tag": "v1.8.8", "peeled_commit": "99df...", "matches": true,
                     "tag_type": "...", "commit_date": "...", "method": "..."},
  "export_checks": {"archive_sha256_matches": true, "manifest_sha256_matches": true,
                    "no_git_metadata": true, "counts_reconcile": true,
                    "archive_sha256_recomputed": "..."},
  "build_ok": true,
  "build_notes": "...",
  "audit_checks": {"remaining_advisory_id_count": 0, "excluded_count": 2,
                   "redacted_count": 0},
  "anchors_checked": [{"vulnerability_id": "CVE-2026-56811",
                       "url": "https://...", "affected": true, "basis": "..."}],
  "independent_checks": ["..."],
  "limitations": ["..."],
  "notes": "..."
}
```

Also write `REVIEW.md` with your reasoning and the exact commands you ran.
