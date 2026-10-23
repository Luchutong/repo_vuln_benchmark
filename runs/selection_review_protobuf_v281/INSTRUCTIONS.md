# Independent selection review — protocolbuffers/protobuf v28.1

You are the independent selection reviewer. Decide whether `snap_de01ecf37efd6cd5`
(protobuf v28.1) may be frozen as an evaluation target in RepoVuln-50 v0.3.1.

Do not trust the collector. Verify from the packet, from the exported archive and from
public upstream sources.

## Packet

Read: `v031/reviews/selection_packets/23357588_protocolbuffers__protobuf.json`

It contains: the proposed tag/commit, export facts (archive and manifest sha256, counts,
tree sha), leakage facts, build indicators, and the known-positive anchor
(CVE-2024-7254).

## Required checks (each recorded explicitly)

1. **Tag resolution.** Resolve `v28.1` yourself (`git ls-remote --tags` plus a clone or
   `git cat-file`). Record tag type (lightweight/annotated), the tag object, the peeled
   commit, the commit date and subject. Confirm it equals the packet `commit_sha`. Confirm
   it is a stable release tag, not a pre-release/dist tag, and record the Maven version the
   tree declares.
2. **Export integrity.** Recompute sha256 of the archive and of the manifest named in the
   packet; both must match. Confirm the archive has no `.git/` path. Reconcile the counts
   explicitly: `tree_file_count`, `exported_file_count`, `symlink_count`, `gitlink_count`
   (this repository has gitlinks/submodules; state how they appear in `git ls-tree` and
   whether the archive exports them as entries or skips them), and confirm
   `missing_from_archive_count` is 0.
3. **Manifest vs tree.** Verify the manifest path set and per-file sha256 against
   `git ls-tree -r` / `git cat-file blob` at the resolved commit for at least a sample,
   and report the count reconciliation.
4. **Leakage / audit export.** Read `data/snapshot_audit_exports.jsonl` row for this
   snapshot only. Confirm `remaining_advisory_id_count == 0`, and record
   `excluded_count`, `redacted_count` and the excluded paths.
5. **Anchor.** Verify from public sources (OSV, NVD, the CVE CNA record, GHSA) that the
   anchor advisory really affects the exact version. For CVE-2024-7254 record the affected
   ranges as each source expresses them, the fixed releases, and the fix-commit ancestry
   relative to the snapshot commit (`git merge-base --is-ancestor`). State whether v28.1 is
   inside every source's affected set and whether v28.2 is the first fixed release on the
   28.x line. Do not take the packet's anchor on faith, and report source disagreements
   instead of flattening them.
6. **Build feasibility.** Record honestly what you could and could not build. User-space
   toolchains: JDK 17 at `~/.local/toolchain/jdk-17.0.20.1+1`, Maven 3.9.16 at
   `~/.local/toolchain/apache-maven-3.9.16/bin`, Go 1.27.3 at
   `~/.local/toolchain/go1.27.3/bin`; network through the proxy. Note that `java/core/`
   ships `pom_template.xml` rather than a ready `pom.xml`, and generated sources need
   `protoc`; attempt a real build if you can do it without inventing steps, and record the
   exact commands and exit codes. Set `build_ok` true only if you can justify that the
   project is buildable as exported (an attempted successful build, or a documented
   structural determination you state explicitly). If you cannot justify it, set false and
   say precisely what blocked it.
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
  the exported archive/manifest under `exports/protocolbuffers__protobuf/`, and public
  upstream sources.
- Use the network proxy: `export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`
- Write only inside `runs/selection_review_protobuf_v281/`; temporary work goes under `/tmp`.
- Treat the downloaded archive as untrusted: extract it into a new empty directory and do
  not execute anything from it except the build commands you decide to run.

## Output

Write `verdict.json` in this directory with at least:

```json
{
  "review_id": "selrev_23357588_snap_de01ecf37efd6cd5_2026-10-23",
  "snapshot_id": "snap_de01ecf37efd6cd5",
  "repo_id": "23357588",
  "full_name": "protocolbuffers/protobuf",
  "reviewed_by": "<your unique reviewer identity>",
  "reviewed_at": "<UTC ISO-8601>",
  "verdict": "accept" | "reject",
  "tag_resolution": {"tag": "v28.1", "peeled_commit": "10ef3f77...", "matches": true,
                     "tag_type": "...", "commit_date": "...", "method": "..."},
  "export_checks": {"archive_sha256_matches": true, "manifest_sha256_matches": true,
                    "no_git_metadata": true, "counts_reconcile": true,
                    "archive_sha256_recomputed": "..."},
  "build_ok": true,
  "build_notes": "...",
  "audit_checks": {"remaining_advisory_id_count": 0, "excluded_count": 0,
                   "redacted_count": 0},
  "anchors_checked": [{"vulnerability_id": "CVE-2024-7254",
                       "url": "https://...", "affected": true, "basis": "..."}],
  "release_sanity": {"release_date": "...", "age_days": 0, "over_four_years": false},
  "independent_checks": ["..."],
  "limitations": ["..."],
  "notes": "..."
}
```

Also write `REVIEW.md` with your reasoning and the exact commands you ran.
