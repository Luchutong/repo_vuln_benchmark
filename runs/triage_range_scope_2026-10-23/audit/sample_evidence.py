#!/usr/bin/env python3
"""Dump cached evidence for a stratified sample of proposals.

Usage: python3 -I sample_evidence.py [seed]
Prints one block per sampled proposal with the exact advisory ranges/CPE bounds
so the auditor can check the proposal by hand.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROP = ROOT / "runs/triage_range_scope_2026-10-23/proposals.jsonl"


def load_jsonl(p):
    return [json.loads(l) for l in p.open(encoding="utf-8") if l.strip()]


def main(seed=20261023):
    props = load_jsonl(PROP)
    cands = {c["candidate_id"]: c for c in load_jsonl(ROOT / "data/candidates.jsonl")}
    snaps = {s["snapshot_id"]: s for s in load_jsonl(ROOT / "data/snapshots.jsonl")}
    nvd = {}
    for p in (ROOT / "runs/discovery_v2/nvd_queries").glob("*.json"):
        for r in json.loads(p.read_text()).get("records") or []:
            nvd[r.get("id")] = r
    osv = {}
    for p in (ROOT / "runs/discovery_v2/osv_queries").glob("*.json"):
        for r in json.loads(p.read_text()).get("records") or []:
            osv[r.get("id")] = r

    rng = random.Random(seed)
    # stratified quotas: (repo_id, class) -> n
    quota = {
        ("569041", "not_affected_range"): 7, ("569041", "out_of_scope_product"): 7,
        ("4164482", "not_affected_range"): 5,
        ("1103607", "not_affected_range"): 3,
        ("80314213", "not_affected_range"): 3, ("80314213", "out_of_scope_product"): 3,
        ("54280778", "not_affected_range"): 2, ("54280778", "out_of_scope_product"): 2,
        ("458058", "not_affected_range"): 2,
        ("96071", "not_affected_range"): 2,
        ("7548986", "not_affected_range"): 1,
        ("1064563", "not_affected_range"): 1,
        ("237159", "not_affected_range"): 1,
        ("596892", "not_affected_range"): 1,
        ("997338", "not_affected_range"): 1,
        ("20904437", "not_affected_range"): 1,
        ("1420053", "not_affected_range"): 1,
        ("23500865", "not_affected_range"): 1,
        ("23357588", "not_affected_range"): 1,
        ("133092972", "not_affected_range"): 1,
        ("257485422", "not_affected_range"): 1,
    }
    groups = {}
    for p in props:
        k = (p["repo_id"], p["proposal"])
        groups.setdefault(k, []).append(p)
    sample = []
    for k, n in quota.items():
        g = groups.get(k, [])
        rng.shuffle(g)
        sample.extend(g[:n])
    print(f"# sample size {len(sample)} (seed {seed})")

    for p in sample:
        snap = snaps[p["snapshot_id"]]
        cand = cands[p["candidate_id"]]
        print("\n" + "=" * 100)
        print(f"CLASS {p['proposal']} | repo {p['repo_id']} | cand {p['candidate_id']} | "
              f"tag {snap['tag_or_release']} -> {p['snapshot_version']} | status {cand.get('status')}")
        print(f"aliases {cand.get('aliases')}")
        paths = re.findall(r"'(runs/discovery_v2/[^']+)'", cand.get("notes") or "")
        print(f"queries {paths}")
        for d in p.get("records") or []:
            rid = d.get("record")
            print(f"  RECORD {rid}")
            if rid in nvd:
                rec = nvd[rid]
                desc = " ".join((x.get("value") or "") for x in rec.get("descriptions") or [])
                print(f"    desc: {desc[:200]}")
                for cfg in rec.get("configurations") or []:
                    for node in cfg.get("nodes") or []:
                        for c in node.get("cpeMatch") or []:
                            parts = (c.get("criteria") or "").split(":")
                            prod = parts[4] if len(parts) > 4 else "?"
                            if prod not in ("curl", "libcurl", "expat", "libexpat", "cjson"):
                                continue
                            print(f"    CPE {c.get('criteria')} vuln={c.get('vulnerable')} "
                                  f"startIncl={c.get('versionStartIncluding')} startExcl={c.get('versionStartExcluding')} "
                                  f"endIncl={c.get('versionEndIncluding')} endExcl={c.get('versionEndExcluding')}")
            elif rid in osv:
                rec = osv[rid]
                for aff in rec.get("affected") or []:
                    pk = aff.get("package") or {}
                    print(f"    affected pkg={pk.get('name')} eco={pk.get('ecosystem')}")
                    for rg in aff.get("ranges") or []:
                        print(f"      range {rg.get('type')} {rg.get('events')}")
            else:
                print("    (record not found in cache)")
        if p.get("records") and all(d.get("bounds") is not None for d in p["records"]):
            u = []
            for d in p["records"]:
                u += [b.get("highest_upper") for b in d.get("bounds") or [] if b.get("highest_upper")]
            if u:
                print(f"  max upper bound seen by tool: {max(u)}")
        if p.get("evidence_urls") is not None:
            print(f"  evidence_urls: {p.get('evidence_urls')}")
        else:
            print("  evidence_urls: MISSING")


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20261023)
