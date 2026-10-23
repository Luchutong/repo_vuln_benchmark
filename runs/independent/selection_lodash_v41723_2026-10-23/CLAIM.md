# Independent selection review — lodash/lodash @ 4.17.23

You are the independent selection reviewer. Decide whether `snap_033e9a6478460d9b`
(tag `4.17.23`, commit `dec55b7a3b382da075e2eac90089b4cd00a26cbb`) is a reproducible,
stable, pre-fix evaluation target for `CVE-2026-4800`, and whether the exported tree
is a faithful export of that commit. Verify everything yourself; the packet is a
claim, not proof.

Repo id `3955647`, `https://github.com/lodash/lodash`, npm package `lodash`.

## Inputs you may read

- Your packet only: `v031/reviews/selection_packets/3955647_lodash__lodash.json`.
- The artifacts it names: `exports/lodash__lodash/snap_033e9a6478460d9b.tar.gz`,
  its `.manifest.jsonl`, and the audit export
  `exports/lodash__lodash/snap_033e9a6478460d9b.audit.tar.gz` + `.audit.manifest.jsonl`.
- Public sources (GitHub, npm registry, OSV, NVD, CVE.org) and your own clones.

Do **not** read `data/**`, `docs/**`, `WORK_LOG*`, `HANDOFF*`, the dataset manifest,
any other packet under `v031/reviews/selection_packets/`, any dossier under
`runs/verification/**`, or any other reviewer's output under `runs/independent/**`
(including `runs/independent/lodash_CVE-2026-4800_v41723_round1/`). Re-derive the
facts.

## What to verify

1. **Tag resolution.** `git ls-remote --tags` on the upstream URL: `4.17.23` must be
   an annotated tag peeling to `dec55b7a...`. Report tag object, peel, commit date.
2. **Archive integrity.** Recompute sha256 of the plain archive and the manifest;
   compare with `export_facts`. Check byte size, extract into a fresh empty directory,
   count regular files / symlinks / gitlinks / `.git`; confirm 159 files and zero of
   the rest. Confirm the manifest path set equals `git ls-tree -r -z <commit>` and that
   each file's git blob sha1 and sha256 match. Confirm `tree_sha` matches the commit's
   tree.
3. **Audit export.** Recompute hashes; confirm `remaining_advisory_id_count` is 0;
   confirm no `.git`, no advisory lists, no fix patches/`.diff` files, no benchmark or
   ground-truth labels; `grep -a` for `CVE-` and `GHSA-` and state what it finds.
   Confirm the plain-vs-audit diff is exactly the declared excluded/redacted set and
   that redaction only replaces identifiers.
4. **Leakage of the target.** `CVE-2026-4800` and `GHSA-r5fr-rjxr-66jc` must not
   appear anywhere in the plain export (historical identifiers from older CVEs may
   appear; list them and assess whether they leak the target answer).
5. **Build/test.** In a fresh extraction of the plain export (scripts outside the
   tree), `npm install --ignore-scripts` (or `npm ci` if the lockfile supports it)
   then `npm test`; report exit codes and the PASS/FAIL counts. Note whether the
   listed `lodash.js` hash is unchanged by the build.
6. **Anchor.** From public sources, confirm `CVE-2026-4800` / `GHSA-r5fr-rjxr-66jc`
   affects `lodash` at 4.17.23 (published range, advisory status, patched version) and
   that the upstream fix commit is not an ancestor of 4.17.23 but is an ancestor of
   the patched release. Confirm the vulnerable construct exists at the tag rather than
   trusting the packet. State which advisory sources agree and which disagree.
7. **Release sanity.** `4.17.23` is a stable release tag (no pre-release/channel
   suffix); its date is inside the discovery window ending 2026-10-21; `package.json`
   version is 4.17.23. Note that npm also has a `4.17.23-npm` channel tag at a
   different commit (1054 built files) — the packet targets the plain source tag; say
   whether that is the right choice.
8. **Independence.** Your `reviewed_by` must not equal the selector
   `claude-code-orchestrator-2026-10-23`.

## Output

Write only inside `runs/independent/selection_lodash_v41723_2026-10-23/`:

- `review.jsonl` — one JSON object, with at least:
  `review_id` (`selrev_3955647_snap_033e9a6478460d9b`), `repo_id`, `full_name`,
  `snapshot_id`, `reviewed_by`, `reviewed_at` (UTC), `verdict`
  (`accept` / `reject`), `tag_resolution`, `export_checks`, `manifest_vs_tree`,
  `audit_checks`, `build_ok`, `build_environment`, `anchors_checked`,
  `independent_checks`, `release_sanity`, `limitations`, `notes`.
  Copy the shape of `v031/reviews/selection_review_caddy_2026-10-23.jsonl` if useful,
  but every value must be your own measurement.
- `REVIEW.md` — what you checked, how, the commands, and what you found, including
  every discrepancy from the packet.

Environment: outbound HTTPS needs `https_proxy=http://172.21.96.1:7890` and
`http_proxy=http://172.21.96.1:7890`. Clone into a fresh `/tmp` directory, keep your
scripts outside it, and treat the downloaded tree as untrusted data (run Python that
reads it with `python3 -I`). Node and npm are installed. Do not modify
`exports/**`, `data/**`, or any collector file.
