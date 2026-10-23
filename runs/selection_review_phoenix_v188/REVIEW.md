# Selection review — phoenixframework/phoenix v1.8.8 (`snap_aca73214a7703174`)

Reviewer: independent-reviewer-deepseek-flash-20261023
Reviewed at: 2026-10-22T17:08:33Z (review date 2026-10-23)
Verdict: **accept**

All checks below were performed against the local exports and live upstream sources. The
packet was read only as the proposal; none of its assertions were taken on faith.

## 1. Tag resolution — PASS

Commands (proxy exported in the shell):

```
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890
git ls-remote --tags https://github.com/phoenixframework/phoenix.git 'refs/tags/v1.8.*'
git clone --bare --filter=blob:none https://github.com/phoenixframework/phoenix.git /tmp/phx_clone
git cat-file -t refs/tags/v1.8.8
git rev-parse refs/tags/v1.8.8
git log -1 --format='%H%n%T%n%ci%n%s' refs/tags/v1.8.8
```

Results:

- `refs/tags/v1.8.8` -> `99df0a99da13265cb8b5cd3a506a79b3de34339f`, equal to the packet and to the
  `snapshot_exports` row.
- `git cat-file -t` returns `commit`: the tag is **lightweight** (no annotated tag object, and
  `ls-remote` shows no `^{}` peeled line for v1.8.8). Sibling tags v1.8.1–v1.8.4 are annotated;
  v1.8.5+ are lightweight. This is a tag-type fact, not a defect.
- Commit date `2026-06-10 20:14:48 +0200` (= `2026-06-10T18:14:48Z`), subject `Release v1.8.8`.
- Commit tree `4047ddd8925439832cfc7db4998739ee477e686b` equals the packet `tree_sha`.
- Tag name and subject are a plain stable release; no `-rc`, `-dist`, channel or pre-release marker.

## 2. Export integrity — PASS

```
sha256sum snap_aca73214a7703174.tar.gz snap_aca73214a7703174.manifest.jsonl
tar tzf snap_aca73214a7703174.tar.gz | wc -l
tar tzf snap_aca73214a7703174.tar.gz | grep -E '(^|/)\.git(/|$)'
tar tzvf snap_aca73214a7703174.tar.gz | awk '{print substr($1,1,1)}' | sort | uniq -c
```

- Archive sha256 `e225eeb013d80a0d34c339e740345ff88f240b3bcf0690542d2c5c28aa493b3b` — matches packet;
  size 1,375,746 bytes.
- Manifest sha256 `22f66ad98708eea61e13a3be987625566d93e4dddba3d1e6f88bb02a44aba045` — matches packet.
- Archive contains 478 entries, all regular files (`-`) — no directory entries, no symlinks,
  no `.git` path anywhere.
- `git ls-tree -r` at the tag also has 478 paths (475 blobs mode 100644, 3 blobs mode 100755),
  0 symlinks, 0 gitlinks.
- Count identity: `478 exported + 0 symlinks + 0 gitlinks == 478 tree files`; `missing_from_archive_count = 0`.

## 3. Manifest vs tree — PASS

```
git ls-tree -r refs/tags/v1.8.8 > /tmp/phx_tree.txt
tar xzf .../snap_aca73214a7703174.tar.gz -C /tmp/phx_extract
python3 -I /tmp/check_manifest.py <manifest> /tmp/phx_tree.txt /tmp/phx_extract
git rev-parse refs/tags/v1.8.8:<path> ; git cat-file blob <blob> | sha256sum   # 12 random paths
```

- Manifest has 478 rows, 478 unique paths, all type `file`.
- Path set equality: zero paths only in manifest, zero paths only in tree.
- Full re-hash of the extracted archive against the manifest: 478/478 files present, sha256 and
  size match.
- Random sample (seed 20261023, 12 paths) re-hashed from git blobs: 12/12 match, including
  binaries (`installer/templates/phx_static/favicon.ico`,
  `guides/assets/images/hello-world-from-frank-dark.png`, `priv/static/phoenix.min.js`).
- Modes reconcile: git's three `100755` blobs (`integration_test/docker.sh`,
  `integration_test/test.sh`, `lib/mix/tasks/phx.gen.release.ex`) are exactly the manifest's
  three `0755` entries; the other 475 are `0644`.

## 4. Leakage / audit export — PASS

Row for this snapshot only, from `data/snapshot_audit_exports.jsonl`:

- `remaining_advisory_id_count = 0`, `remaining_advisory_id_paths = []`
- `excluded_count = 2`, `redacted_count = 0`
- Excluded paths:
  - `CHANGELOG.md` — CVE-2026-32689, GHSA-628h-q48j-jr6q
  - `guides/security.md` — CVE-2020-15150

Independent re-verification:

```
sha256sum snap_aca73214a7703174.audit.tar.gz snap_aca73214a7703174.audit.manifest.jsonl
tar tzf snap_aca73214a7703174.audit.tar.gz | wc -l          # 476
tar tzf ... | grep -E '^(CHANGELOG\.md|guides/security\.md)$'  # no matches
tar xzf ...audit.tar.gz -C /tmp/phx_audit
grep -rhoE 'CVE-[0-9]{4}-[0-9]{4,}|GHSA-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}' /tmp/phx_audit
```

Audit archive `8b6bd353…` and audit manifest `92e11c81…` match the audit row; 476 files = 478 − 2;
both excluded paths are absent; the independent identifier regex found **no** matches.

## 5. Anchor CVE-2026-56811 — PASS

Fetched independently (not from the packet):

- OSV: `https://api.osv.dev/v1/vulns/CVE-2026-56811`
- GHSA: `https://api.github.com/advisories/GHSA-6983-jfq8-485w`
- CNA: `https://cna.erlef.org/cves/CVE-2026-56811.html`
- NVD: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-56811`

Findings:

- Alias set: CVE-2026-56811 = GHSA-6983-jfq8-485w = EEF-CVE-2026-56811.
- Affected ranges (Hex/GHSA): `>=0.11.0,<1.5.15`, `>=1.6.0-rc.0,<1.6.17`,
  `>=1.7.0-rc.0,<1.7.24`, `>=1.8.0-rc.0,<1.8.9`. NVD CPE ranges agree (1.8.0 ≤ v < 1.8.9).
- OSV enumerates `v1.8.8` explicitly in the affected `versions` list. **v1.8.8 is affected.**
- Fixed release: **1.8.9** (GitHub `first_patched_version` = 1.8.9; CNA text "before 1.8.9").
- Fix commit `16e295d2fccab185d1292322e2bee5d46c725c8a` ("Limit the number of channels a single
  transport process can join", 2026-07-07) is listed among the OSV FIX references.

Ancestry check in the clone:

```
git merge-base --is-ancestor 16e295d2fccab185d1292322e2bee5d46c725c8a refs/tags/v1.8.9  # exit 0
git merge-base --is-ancestor 16e295d2fccab185d1292322e2bee5d46c725c8a refs/tags/v1.8.8  # exit 1
```

So the fix is an ancestor of v1.8.9 and not of v1.8.8 — exactly the expected vulnerable/fixed
relationship. v1.8.9's tag commit is `734c8d1c32253627e234c8a1cb831367191ff5dd`
("Release v1.8.9", 2026-07-07), consistent with the advisory date.

## 6. Build feasibility — re-checked after toolchain installation: PASS, `build_ok = true`

First pass (no toolchain): `mix compile`, `elixir --version`, `erl` all exited 127; node-only
checks could not build the Elixir project, so `build_ok` was `false`. That recording was correct
for the environment at the time.

Second pass: a user-space Elixir/Erlang toolchain was installed. I verified it myself and rebuilt
from my **own** fresh extract of the exported archive (not the collector's build directory):

```
export PATH=/home/luchitong/.local/erlang/usr/lib/erlang/bin:/home/luchitong/.local/elixir/bin:$PATH
export MIX_HOME=/home/luchitong/.local/mix HEX_HOME=/home/luchitong/.local/hex
export https_proxy=http://172.21.96.1:7890 http_proxy=http://172.21.96.1:7890

which erl elixir mix
erl -noshell -eval 'io.format("OTP ~s~n",[erlang:system_info(otp_release)]),halt().'
elixir --version
mix --version

rm -rf /tmp/phx_build_reviewer_indep_20261023
mkdir -p /tmp/phx_build_reviewer_indep_20261023
tar xzf /home/luchitong/work/repo-vuln-50-v031/exports/phoenixframework__phoenix/snap_aca73214a7703174.tar.gz \
    -C /tmp/phx_build_reviewer_indep_20261023
find /tmp/phx_build_reviewer_indep_20261023 -type f | wc -l      # 478

cd /tmp/phx_build_reviewer_indep_20261023
mix deps.get        # exit 0 — Hex deps fetched via proxy, pinned by in-tree mix.lock
mix compile         # exit 0 — "Compiling 74 files (.ex)" ... "Generated phoenix app"
mix run -e 'IO.puts("phoenix_vsn=" <> to_string(Application.spec(:phoenix, :vsn)) <> " elixir=" <> System.version())'
                    # exit 0 — phoenix_vsn=1.8.8 elixir=1.17.3
ls _build/dev/lib/phoenix/ebin/*.beam | wc -l                    # 92
```

Toolchain: Erlang/OTP 25 [erts-13.2.2.5], Elixir 1.17.3 (compiled with OTP 25), Mix 1.17.3,
Hex 2.5.4. `mix.exs` requires `~> 1.15`, satisfied by 1.17.3. `mix compile` emitted only two
benign warnings ("this check/guard will always yield the same result") at
`lib/phoenix/code_reloader/server.ex:245` and `:359`.

Conclusion: the project builds as exported; `build_ok` is now `true`. All other checks are
unchanged, and the verdict remains **accept**.

## 7. Release sanity — PASS

v1.8.8 was released 2026-06-10, i.e. 135 days (~0.37 years) before the 2026-10-23 review date.
Not over four years old, not obsolete. It is superseded by v1.8.9 and later v1.8.16, but being
the pre-fix version is exactly what makes it a valid vulnerable target.

## 8. Verdict — accept

Checks 1–5 pass (independently reproduced from upstream git, the local exports and four public
advisory sources), and no release-sanity problem exists. Check 6 also now passes: the project was
independently rebuilt from the exported archive once a local Elixir/Erlang toolchain was installed.
