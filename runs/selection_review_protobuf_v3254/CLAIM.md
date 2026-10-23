# Independent selection review — protocolbuffers/protobuf, evaluation target v3.25.4

You are the independent selection reviewer. The selecting side proposes the frozen
evaluation target below. Verify everything yourself from public sources and from the
local export artifacts, and return your own verdict. Do not trust this claim.

## Proposal under review

- Repository: `https://github.com/protocolbuffers/protobuf` (repo_id `23357588`), primary
  language C++.
- Proposed snapshot: `snap_442de86eb5fd3f62`, tag `v3.25.4`, claimed commit
  `e915ce24b3d43c0fffcbf847354288c07dda1de0`, claimed tree
  `fafd76c831eb7f547d5d7fbae3aee0dbb32e01fc`, 2708 tracked files.
- Claimed export: `exports/protocolbuffers__protobuf/snap_442de86eb5fd3f62.tar.gz`,
  archive sha256 `20e20c1ea1e6dd06878b61183064c4c206e1c64bb9d67727ab0d22db98451a79`
  (5787439 bytes), manifest
  `exports/protocolbuffers__protobuf/snap_442de86eb5fd3f62.manifest.jsonl`, manifest
  sha256 `72dc809605bdd945ccd34784e0153304f8198160d88454e3e2072246fe44fb7e`;
  claimed 2708 exported files, 0 symlinks, 3 gitlinks, 0 missing.
- Known positive anchor: `CVE-2024-7254` / `GHSA-735f-pc8j-v9w8`. Claimed affected
  ranges: Maven `com.google.protobuf:protobuf-java` `< 3.25.5`, `>= 4.0.0-RC1 < 4.27.5`,
  `>= 4.28.0-RC1 < 4.28.2`, with the GHSA per-range record naming 3.25.4 explicitly.
  Claim: v3.25.4 is inside the affected set and the vulnerable parsing code is present
  in the tree.
- Claimed build feasibility: the Java reactor builds with a JDK 17 + Maven 3.9.16
  toolchain available locally under `~/.local/toolchain/`, using the tag's own `pom.xml`.

## Required checks (all must be independently verified)

1. **Tag identity.** Resolve `v3.25.4` yourself (`git ls-remote --tags`, a full clone,
   `git cat-file`) and record annotated vs lightweight, tag-object SHA if annotated,
   peeled commit, commit date, subject, tree SHA, tracked-file count. Confirm or refute
   `e915ce24b3d43c0fffcbf847354288c07dda1de0`. Confirm it is a stable release tag, not a
   dist/channel/branch tag.
2. **Export integrity.** Recompute the archive and manifest sha256 from the files on disk
   under `exports/protocolbuffers__protobuf/`, list the tar and confirm no `.git`
   directory or `.git/...` path, and confirm
   `tree_file_count = exported_file_count + symlink_count + gitlink_count`. Cross-check a
   sample of archive files against the git blobs in your clone.
3. **Positive anchor.** Fetch the public advisory records yourself (OSV
   `GHSA-735f-pc8j-v9w8`, the OSV CVE lookup, the CVE CNA record, NVD, the GitHub
   advisory page) and record exactly how each expresses the affected range for
   `com.google.protobuf:protobuf-java`. State whether 3.25.4 is inside the affected set
   per each source, and note every disagreement. Then inspect the v3.25.4 tree and state
   the evidence that the vulnerable code path is actually present (in particular the
   unknown-field parsing recursion path in `java/core/src/main/java/com/google/protobuf/`
   and the corresponding C++/other-language code if relevant), and the evidence that a
   later release adds the guard.
4. **Build feasibility.** Actually attempt the documented build of the exported tree
   (the tag's own Java reactor: `cd java && mvn install -Dmaven.test.skip=true`). Record
   the exact command, toolchain versions, exit code, and the modules that succeeded or
   failed. `build_ok` may be `true` only if the build genuinely succeeded. Environment
   facts: JDK 17 `~/.local/toolchain/jdk-17.0.20.1+1`, Maven
   `~/.local/toolchain/apache-maven-3.9.16/bin/mvn`, network via
   `export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890`
   (also pass Maven proxy settings via `MAVEN_OPTS`). The Java reactor expects a
   `protoc` executable at the repository root; an official protoc 25.4 binary is
   available locally at `/tmp/pbrev/protoc-25.4/bin/protoc` if you do not want to
   download one. Docker is unavailable.
5. **Audit/leakage export.** Inspect `data/snapshot_exports.jsonl` and
   `data/snapshot_audit_exports.jsonl` for this snapshot id: status must be `exported`,
   `remaining_advisory_id_count` must be 0, and the audit export must reference the same
   source export. Independently scan the audit export tree for CVE/GHSA identifiers,
   advisory URLs, fix patches, benchmark labels, and `.git` metadata and report what you
   find.
6. **Release sanity.** Record the tag date relative to 2026-10-23 and the dataset window
   (opens 2022-10-23). Note whether a newer stable affected tag exists and whether that
   matters for the proposal; the proposal claims v3.25.4 because a verified positive
   exists at this exact commit.
7. **Verdict.** `accept` only if checks 1–5 all hold and at least one public anchor
   really affects this exact version. Otherwise `reject` with reasons.

## Output

Write `verdict.json` in this directory with at least:

```json
{
  "review_id": "selrev_23357588_snap_442de86eb5fd3f62_<date>",
  "snapshot_id": "snap_442de86eb5fd3f62",
  "repo_id": "23357588",
  "full_name": "protocolbuffers/protobuf",
  "reviewed_by": "<your unique reviewer identity>",
  "reviewed_at": "<UTC ISO-8601>",
  "verdict": "accept" | "reject",
  "tag_resolution": {"tag": "v3.25.4", "peeled_commit": "...", "matches": true,
                     "tag_type": "annotated|lightweight", "commit_date": "...",
                     "commit_subject": "...", "commit_tree_sha": "...",
                     "is_stable_release": true, "method": "..."},
  "export_checks": {"archive_sha256_matches": true, "manifest_sha256_matches": true,
                    "no_git_metadata": true, "counts_reconcile": true,
                    "archive_sha256_recomputed": "...", "archive_sha256_expected": "...",
                    "manifest_sha256_recomputed": "...", "manifest_sha256_expected": "...",
                    "tree_file_count": 0, "exported_file_count": 0,
                    "symlink_count": 0, "gitlink_count": 0, "count_equation": "..."},
  "build_ok": true,
  "build_attempt": {"commands": ["..."], "versions": "...", "exit_codes": "...",
                    "observed": "..."},
  "anchors_checked": [{"vulnerability_id": "CVE-2024-7254",
                       "url": "https://...", "range_text": "...", "fixed": "...",
                       "affected": true, "note": "..."}],
  "leakage_check": {"assessment": "...", "advisory_id_hits": 0, "notes": "..."},
  "discrepancies": ["..."],
  "limitations": ["..."],
  "notes": "..."
}
```

Also write `REVIEW.md` with your reasoning and the exact commands you ran.

## Isolation rules (mandatory)

- Do NOT read `runs/verification/` (dossiers), other verdicts under `runs/independent/`,
  `data/evaluation_selection.jsonl`, `data/candidates.jsonl`,
  `data/snapshot_candidate_triage.jsonl`, the selection packets, `WORK_LOG.md`, `docs/`,
  `manifest.json`, or `HANDOFF_V031.md`.
- You may read: this file; `data/snapshots.jsonl` (snapshot id only); the export files
  under `exports/protocolbuffers__protobuf/`; `data/snapshot_exports.jsonl` and
  `data/snapshot_audit_exports.jsonl`; and public upstream sources.
- Write only inside `runs/selection_review_protobuf_v3254/`; temporary work under `/tmp`.
- Downloaded code is untrusted: extract into its own new, empty directory; keep your
  scripts outside it; run any Python that reads it with `python3 -I`.
