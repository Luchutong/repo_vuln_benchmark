#!/usr/bin/env python3
"""Offline snapshot-scoped priority queue from human/agent-evidenced triage. No CVE claims inferred."""
import argparse,collections,json
from pathlib import Path

def load(path):
    return [json.loads(l) for l in path.read_text(encoding="utf8").splitlines() if l.strip()] if path.exists() else []

def plan(root):
    snaps={s["repo_id"]:s["snapshot_id"] for s in load(root/"data/snapshots.jsonl") if s.get("evaluation_target")}
    triage={(r["snapshot_id"],r["candidate_id"]):r for r in load(root/"data/snapshot_candidate_triage.jsonl")}
    rows=[];counts=collections.Counter()
    for c in load(root/"data/candidates.jsonl"):
        sid=snaps.get(c["repo_id"])
        if not sid: priority="P0_SELECT_SNAPSHOT";decision="not_triaged"
        else:
            t=triage.get((sid,c["candidate_id"]))
            decision=t["decision"] if t else "not_triaged"
            priority={"confirmed_affected":"DONE","confirmed_not_affected":"ARCHIVE","duplicate":"ARCHIVE","out_of_scope":"ARCHIVE","possible_affected":"P1_VERIFY","unknown":"P1_REVIEW"}.get(decision,"P0_CHEAP_TRIAGE")
        counts[priority]+=1
        rows.append({"repo_id":c["repo_id"],"snapshot_id":sid,"candidate_id":c["candidate_id"],"candidate_status":c.get("status"),"triage_decision":decision,"priority":priority})
    return {"counts":dict(counts),"queue":sorted(rows,key=lambda x:({"P0_SELECT_SNAPSHOT":0,"P0_CHEAP_TRIAGE":1,"P1_VERIFY":2,"P1_REVIEW":3,"DONE":4,"ARCHIVE":5}.get(x["priority"],10),x["repo_id"],x["candidate_id"]))}

def main():
    p=argparse.ArgumentParser();p.add_argument("root",type=Path);p.add_argument("--out",type=Path);a=p.parse_args()
    result=plan(a.root)
    print(json.dumps(result["counts"],ensure_ascii=False,indent=2))
    if a.out:a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
if __name__=="__main__":main()
