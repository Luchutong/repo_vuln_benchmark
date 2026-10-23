#!/usr/bin/env python3
"""Independent re-evaluation of range-scope proposals against cached evidence.

Deliberately does NOT import the tool under audit. Semantics are re-implemented
from the OSV/NVD specs with stricter vetoes. Run with: python3 -I this.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
UPSTREAM = {
    "GitHub", "PyPI", "npm", "Go", "Maven", "crates.io", "RubyGems",
    "Packagist", "NuGet", "Hex", "Pub", "SwiftURL",
}
VERSION_RE = re.compile(r"(\d+(?:\.\d+)+)")


def parse_version(value):
    """Strict-ish parse: returns (tuple, prerelease_bool) or None."""
    if value is None:
        return None
    text = str(value).strip().replace("_", ".")
    m = VERSION_RE.search(text)
    if not m:
        return None
    parts = []
    for comp in m.group(1).split("."):
        d = re.match(r"^\d+", comp)
        if not d:
            return None
        parts.append(int(d.group(0)))
    # detect a pre-release suffix AFTER the matched numeric core
    rest = text[m.end():]
    pre = bool(re.match(r"[-.~](rc|beta|alpha|pre|dev|final|[ab])\d*", rest, re.I))
    return (tuple(parts), pre)


def cmpv(a, b):
    n = max(len(a), len(b))
    aa = a + (0,) * (n - len(a))
    bb = b + (0,) * (n - len(b))
    return (aa > bb) - (aa < bb)


def load_jsonl(p):
    if not p.exists():
        return []
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def range_state(events, ver):
    """Return 'contains' | 'above' | 'open' | 'unsupported' | 'none'."""
    intro = None
    saw_any = False
    unclosed = False
    contains = False
    high = None
    for ev in events:
        keys = set(ev)
        if not keys or not keys <= {"introduced", "fixed", "last_affected", "limit"}:
            return "unsupported", None
        if "introduced" in ev and len(keys) == 1:
            raw = ev["introduced"]
            if str(raw) == "0":
                intro = (0,)
            else:
                p = parse_version(raw)
                if p is None:
                    return "unsupported", None
                intro = p[0]
            saw_any = True
        elif keys == {"fixed"}:
            p = parse_version(ev["fixed"])
            if p is None or intro is None:
                return "unsupported", None
            if cmpv(intro, ver) <= 0 and cmpv(ver, p[0]) < 0:
                contains = True
            high = p[0] if high is None or cmpv(p[0], high) > 0 else high
            intro = None
        elif keys == {"last_affected"}:
            p = parse_version(ev["last_affected"])
            if p is None or intro is None:
                return "unsupported", None
            if cmpv(intro, ver) <= 0 and cmpv(ver, p[0]) <= 0:
                contains = True
            high = p[0] if high is None or cmpv(p[0], high) > 0 else high
            intro = None
        elif keys == {"limit"}:
            p = parse_version(ev["limit"])
            if p is None or intro is None:
                return "unsupported", None
            if cmpv(intro, ver) <= 0 and cmpv(ver, p[0]) < 0:
                contains = True
            high = p[0] if high is None or cmpv(p[0], high) > 0 else high
            intro = None
        else:
            return "unsupported", None
    if intro is not None:
        unclosed = True
    if contains:
        return "contains", high
    if unclosed and intro != (0,):
        # introduced X with no closing event: affected from X onward
        if cmpv(ver, intro) >= 0:
            return "contains", high
        return "open", high
    if unclosed and intro == (0,):
        return "open", high  # introduced 0 with no close: all versions
    if high is None:
        return "unsupported", None
    return "above", high


def record_ids(rec):
    ids = {rec.get("id")} if rec.get("id") else set()
    for a in rec.get("aliases") or []:
        ids.add(a)
    return {i.upper() for i in ids if i}


def evaluate_osv(rec, ver, pkg_name):
    entries = []
    skipped_eco = False
    for aff in rec.get("affected") or []:
        pkg = aff.get("package") or {}
        name = (pkg.get("name") or "").lower()
        eco = pkg.get("ecosystem") or ""
        if pkg_name and name and name != pkg_name.lower():
            continue
        if eco not in UPSTREAM:
            skipped_eco = True
            continue
        entries.append(aff.get("ranges") or [])
    if not entries:
        return "unsupported_ecosystem" if skipped_eco else "no_matching_package"
    any_contains = False
    any_open = False
    any_unsupported = False
    uppers = []
    for ranges in entries:
        for rg in ranges:
            state, high = range_state(rg.get("events") or [], ver)
            if rg.get("type") == "GIT":
                any_unsupported = True
                continue
            if state == "contains":
                any_contains = True
            elif state == "open":
                any_open = True
            elif state == "unsupported":
                any_unsupported = True
            elif state == "above":
                uppers.append(high)
    if any_contains:
        return "possible_affected_range"
    if any_open or any_unsupported or not uppers:
        return "indeterminate"
    return "not_affected_range"


def evaluate_nvd(rec, ver, names):
    """Return status for one NVD record. Stricter than the tool:
    - a start-only CPE vetoes not_affected (open-ended)
    - vendor is recorded but not used for product match (same as tool)
    - an exact CPE whose version parses with a pre-release suffix is vetoed
    """
    any_cpe = False
    matched = []
    for cfg in rec.get("configurations") or []:
        for node in cfg.get("nodes") or []:
            for c in node.get("cpeMatch") or []:
                any_cpe = True
                parts = (c.get("criteria") or "").split(":")
                prod = parts[4] if len(parts) > 4 else ""
                if normalize(prod) not in names:
                    continue
                matched.append(c)
    if not any_cpe:
        return "no_configuration"
    if not matched:
        return "no_matching_package"
    contains = False
    uppers = []
    veto = False
    for c in matched:
        if c.get("vulnerable") is False:
            continue
        cv = c.get("version") or (c.get("criteria", "").split(":")[5] if c.get("criteria") else "*")
        start_inc = c.get("versionStartIncluding")
        start_exc = c.get("versionStartExcluding")
        end_inc = c.get("versionEndIncluding")
        end_exc = c.get("versionEndExcluding")
        if cv not in ("*", "-", None, ""):
            p = parse_version(cv)
            if p is None:
                veto = True
                continue
            if p[1]:
                veto = True
            if cmpv(ver, p[0]) == 0:
                contains = True
            uppers.append(p[0])
            continue
        si = parse_version(start_inc) if start_inc else None
        se = parse_version(start_exc) if start_exc else None
        ei = parse_version(end_inc) if end_inc else None
        ee = parse_version(end_exc) if end_exc else None
        if (start_inc and si is None) or (start_exc and se is None) or (end_inc and ei is None) or (end_exc and ee is None):
            veto = True
            continue
        low_ok = True
        if si is not None and cmpv(ver, si[0]) < 0:
            low_ok = False
        if se is not None and cmpv(ver, se[0]) <= 0:
            low_ok = False
        high_ok = True
        if ei is not None and cmpv(ver, ei[0]) > 0:
            high_ok = False
        if ee is not None and cmpv(ver, ee[0]) >= 0:
            high_ok = False
        if low_ok and high_ok:
            contains = True
        if ei is not None:
            uppers.append(ei[0])
        elif ee is not None:
            uppers.append(ee[0])
        else:
            veto = True  # start-only / open-ended
    if contains:
        return "possible_affected_range"
    if veto or not uppers:
        return "indeterminate"
    if all(cmpv(ver, u) > 0 for u in uppers):
        return "not_affected_range"
    return "indeterminate"


def normalize(v):
    return re.sub(r"[^a-z0-9]", "", (v or "").lower())


def main():
    props = [json.loads(l) for l in (ROOT / "runs/triage_range_scope_2026-10-23/proposals.jsonl").open()]
    cands = {c["candidate_id"]: c for c in load_jsonl(ROOT / "data/candidates.jsonl")}
    snaps = {s["snapshot_id"]: s for s in load_jsonl(ROOT / "data/snapshots.jsonl")}
    repos = {str(r.get("repo_id")): r for r in load_jsonl(ROOT / "data/repositories.jsonl")}
    names_by_repo = {}
    for rid, r in repos.items():
        ns = set()
        full = r.get("full_name") or ""
        if "/" in full:
            ns.add(normalize(full.split("/", 1)[1]))
        for k in ("name", "short_name"):
            if r.get(k):
                ns.add(normalize(r[k]))
        for n in list(ns):
            if n.startswith("lib") and len(n) > 4:
                ns.add(n[3:])
        if "curl" in ns:
            ns.add("libcurl")
        names_by_repo[rid] = ns
    qcache = {}
    out = []
    for p in props:
        if p["proposal"] not in ("not_affected_range", "out_of_scope_product"):
            continue
        snap = snaps.get(p["snapshot_id"], {})
        tag = snap.get("tag_or_release")
        pv = parse_version(tag)
        if pv is None:
            out.append(dict(proposal=p, status="tag-unparsable", note=str(tag)))
            continue
        ver, pre = pv
        cand = cands.get(p["candidate_id"], {})
        aliases = {a.upper() for a in cand.get("aliases") or []}
        paths = re.findall(r"'(runs/discovery_v2/[^']+)'", cand.get("notes") or "")
        statuses = []
        matched_records = []
        product_mismatch = []
        pkg_name = None
        for rel in paths:
            path = ROOT / rel
            if not path.exists():
                continue
            if rel not in qcache:
                try:
                    qcache[rel] = json.loads(path.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    continue
            q = qcache[rel]
            pkg = q.get("package") or {}
            pkg_name = pkg.get("name") or pkg_name
            db = q.get("database")
            recs = q.get("records") or []
            for rec in recs:
                if not (record_ids(rec) & aliases):
                    continue
                if db == "OSV":
                    st = evaluate_osv(rec, ver, pkg_name)
                    if st == "no_matching_package":
                        continue
                elif db == "NVD":
                    st = evaluate_nvd(rec, ver, names_by_repo.get(str(p["repo_id"]), set()))
                    if st == "no_matching_package":
                        product_mismatch.append(rec.get("id"))
                        continue
                else:
                    continue
                statuses.append(st)
                matched_records.append(rec.get("id"))
        if not statuses:
            proposal = "out_of_scope_product" if product_mismatch else "indeterminate"
        elif "possible_affected_range" in statuses:
            proposal = "possible_affected_range"
        elif all(s == "not_affected_range" for s in statuses):
            proposal = "not_affected_range"
        else:
            proposal = "indeterminate"
        out.append(dict(proposal=p, status=proposal, matched=matched_records,
                        statuses=statuses, prerelease=pre, ver=list(ver)))
    with (ROOT / "runs/triage_range_scope_2026-10-23/audit/independent_results.jsonl").open("w") as f:
        for row in out:
            p = row["proposal"]
            f.write(json.dumps(dict(
                candidate_id=p["candidate_id"], repo_id=p["repo_id"], snapshot_tag=p["snapshot_tag"],
                tool=p["proposal"], independent=row["status"],
                matched=row.get("matched"), statuses=row.get("statuses"),
                prerelease=row.get("prerelease"),
            )) + "\n")
    diffs = [r for r in out if r["status"] != r["proposal"]["proposal"]]
    print(f"checked {len(out)}; disagreements {len(diffs)}")
    for r in diffs:
        p = r["proposal"]
        print(f"  {p['repo_id']:>9} {p['snapshot_tag']:<22} {p['candidate_id']}  tool={p['proposal']} indep={r['status']} "
              f"matched={r.get('matched')} statuses={r.get('statuses')}")


if __name__ == "__main__":
    main()
