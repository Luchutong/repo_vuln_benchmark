#!/usr/bin/env python3
"""List existing per-repo snapshot options; NEVER make an automatic selection."""
import argparse,collections,json
from pathlib import Path

def rows(p):
    return [json.loads(s) for s in p.read_text(encoding='utf8').splitlines() if s.strip()] if p.exists() else []

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    a=ap.parse_args()
    d=a.source/'data'
    repos=rows(d/'repositories.jsonl');snaps=rows(d/'snapshots.jsonl')
    statuses=rows(d/'snapshot_vulnerability_status.jsonl');locs=rows(d/'locations.jsonl')
    grade={x.get('vulnerability_id'):x.get('grade') for x in rows(d/'reviews.jsonl')}
    by_repo=collections.defaultdict(list);positives=collections.defaultdict(set)
    for s in snaps:by_repo[s['repo_id']].append(s)
    for st in statuses:
        if st.get('status')=='confirmed_affected':positives[st['snapshot_id']].add(st['vulnerability_id'])
    located={(l.get('snapshot_id'),l.get('vulnerability_id')) for l in locs}
    output=[]
    for r in repos:
        candidates=[]
        for s in by_repo.get(r['repo_id'],[]):
            sid=s['snapshot_id'];ids=positives[sid]
            candidates.append({
                'snapshot_id':sid,'commit_sha':s.get('vulnerable_commit'),
                'previous_evaluation_target':bool(s.get('evaluation_target')),
                'tag_or_release':s.get('tag_or_release'),
                'full_language_scan':bool(s.get('full_scan') and s.get('languages')),
                'known_positive_rows':len(ids),
                'known_positives_with_same_sha_location':sum((sid,vid) in located for vid in ids),
                'grade_A_count':sum(grade.get(vid)=='A' for vid in ids),
                'grade_B_count':sum(grade.get(vid)=='B' for vid in ids),
                'warning':'Counts are exploratory; candidate is NOT verified suitable for final evaluation.'
            })
        output.append({'repo_id':r['repo_id'],'canonical_url':r['canonical_url'],
                       'current_target_count':sum(s.get('evaluation_target',False) for s in by_repo.get(r['repo_id'],[])),
                       'candidates':candidates,
                       'decision':'MANUAL_REVIEW_REQUIRED'})
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'{len(output)} repositories, {sum(len(x["candidates"]) for x in output)} stored snapshots; wrote {a.out}')

if __name__=='__main__':main()
