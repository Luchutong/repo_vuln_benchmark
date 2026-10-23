# Corrections — CVE-2026-22860 (rack, snapshot 2.2.3)

The round-1 independent review (`runs/independent/rack_CVE-2026-22860_round1/verdict.json`)
found two factual problems with the collector's material. The verdict is **not** rewritten;
the dossier evidence files stay byte-identical (their sha256 values are cited in
`dossier.json`), and the corrections are recorded here.

## 1. Tag 2.2.3 is annotated, not lightweight

`sources/git_object_checks.txt` says "the 2.2.3 tag is unannotated and has no `v`
prefix". The second half is right, the first is wrong:

```
$ git ls-remote --tags https://github.com/rack/rack.git | grep 2.2.3
4d456648c521ad1392afcd8ae35e332c83a09849	refs/tags/2.2.3
$ git rev-parse '2.2.3^{commit}'
1741c580d71cfca8e541e96cc372305c8892ee74
```

`4d456648...` is a tag object, and it peels to the snapshot commit `1741c580...`.
The snapshot identity itself was never in doubt — only the annotation note was wrong.
Verified again with `git cat-file -t 4d456648` → `tag`.

## 2. Branch backport commits

`sources/git_object_checks.txt` and the dossier's `open_questions` say the 2.2.x backport
commit id was not retrieved (GitHub API rate limit). The independent reviewer identified
three branch commits, all reachable upstream and all carrying the same subject and the
same three-file change (CHANGELOG, `lib/rack/directory.rb`, `test/spec_directory.rb`):

| Commit | Subject |
| --- | --- |
| `a5725c031b2717758851f1eadd9b9dfe7555745a` | Prevent directory traversal via root prefix bypass. |
| `48e90303ea09cdcf5091104c1ffc94a2f74e2c5b` | Prevent directory traversal via root prefix bypass. |
| `f9bde3bc2dde2771185ac1a7b7602a4d9fa0a0d8` | Prevent directory traversal via root prefix bypass. |

Checked with `curl https://github.com/rack/rack/commit/<sha>.patch` (HTTP 200 for all
three). The mapping from each sha to a specific maintenance branch (2.2 / 3.1 / 3.2) was
not re-derived here; the release-level proof remains the blob comparison
`be72be0 -> e9e9bb5` between v2.2.21 and v2.2.22.

## 3. Affected-range over-inclusion (reviewer finding, re-verified here)

The reviewer reports that the published `< 2.2.22` range is wider than the vulnerable
code. Re-checked against the tags:

```
2.1.4 = f3cf79d6  lib/rack/directory.rb:97-98
        def check_forbidden(path_info)
          return unless path_info.include? ".."
          body = "Forbidden\n"          # no allow-branch at all
2.2.0 = 0b32090f  lib/rack/directory.rb:113-115
        return unless path_info.include? ".."
        return if ::File.expand_path(::File.join(@root, path_info)).start_with?(@root)
```

So the 2.x line became vulnerable only when tag 2.2.0 introduced the prefix check; at
2.1.4 every path containing `..` is rejected. The snapshot `2.2.3` is inside the truly
affected span either way, so this does not change the entry's validity; it is recorded as
a range-accuracy caveat.

## Effect on promotion

None of the three items changes a verdict field. The round-1 verdict failed only
`evidence_independent`, so the entry stays pending; this file does not move it.
