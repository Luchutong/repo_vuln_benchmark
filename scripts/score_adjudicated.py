#!/usr/bin/env python3
"""RepoVuln v0.3 (v0.2 compatible) offline, frozen-oracle scoring. Does NOT decide whether a finding is real.

Usage: python scripts/score_adjudicated.py DATASET_ROOT --run-id agent-run-001
Requires evaluation/agent_findings.jsonl and evaluation/adjudications.jsonl.
All nonduplicate in-scope agent findings must be adjudicated or unresolved; no
unlabeled finding may be automatically classified as a false positive.
"""
import argparse
import collections
import json
from pathlib import Path


def read_jsonl(path):
    if not path.exists():
        raise SystemExit(f'missing {path}')
    rows=[]
    for n,s in enumerate(path.read_text(encoding='utf8').splitlines(), 1):
        if s.strip():
            try:rows.append(json.loads(s))
            except ValueError as e:raise SystemExit(f'{path}:{n}: {e}') from e
    return rows


def compute(root, run_id):
    data=root/'data';ev=root/'evaluation'
    statuses=read_jsonl(data/'snapshot_vulnerability_status.jsonl')
    snaps=read_jsonl(data/'snapshots.jsonl')
    repos=read_jsonl(data/'repositories.jsonl')
    findings=[x for x in read_jsonl(ev/'agent_findings.jsonl') if x.get('run_id')==run_id]
    judgments=[x for x in read_jsonl(ev/'adjudications.jsonl') if x.get('run_id')==run_id]
    idx={}
    for j in judgments:
        key=(j['run_id'],j['finding_id'])
        if key in idx:raise ValueError(f'duplicate adjudication: {key}')
        if j.get('reviewer')==j.get('independent_reviewer'):
            raise ValueError(f'not independent adjudication: {key}')
        idx[key]=j
    observed=set()
    positives=collections.defaultdict(set)
    for row in statuses:
        if row['status']=='confirmed_affected':
            positives[row['snapshot_id']].add(row['vulnerability_id'])
    evaluated_snaps = {s['snapshot_id']:s['repo_id'] for s in snaps if s.get('evaluation_target')}
    repo_snapshot_counts=collections.Counter(evaluated_snaps.values())
    if any(n != 1 for n in repo_snapshot_counts.values()):
        raise ValueError('v0.3 requires exactly one evaluation snapshot per repository')
    for sid in positives:
        if sid not in evaluated_snaps:raise ValueError(f'positive status for non evaluation snapshot {sid}')
    found_positive=collections.defaultdict(set)
    outcome=collections.Counter()
    for finding in findings:
        key=(finding['run_id'],finding['finding_id'])
        if key in observed:raise ValueError(f'duplicate finding {key}')
        observed.add(key)
        j=idx.get(key)
        if j is None:raise ValueError(f'finding {key} has no adjudication (use unresolved verdict)')
        if j['snapshot_id']!=finding['snapshot_id']:
            raise ValueError(f'finding {key} snapshot differs from adjudication')
        verdict=j['verdict']
        if verdict=='matched_known_tp':
            vid=j.get('canonical_vulnerability_id')
            if vid not in positives.get(finding['snapshot_id'],set()):
                raise ValueError(f'known TP {key} is not confirmed_affected: {vid}')
            found_positive[finding['snapshot_id']].add(vid)
        outcome[verdict]+=1
    extra_keys=set(idx)-observed
    if extra_keys:raise ValueError(f'orphan adjudications: {list(extra_keys)[:3]}')
    known_tp_count=sum(len(v) for v in found_positive.values())
    # Deduplicate repeated known TP claims before computing denominators.
    all_positives=sum(len(v) for v in positives.values())
    per_repo_snap=collections.defaultdict(list)
    for sid,rid in evaluated_snaps.items():
        denom=len(positives.get(sid,set()))
        if denom==0:raise ValueError(f'evaluation snapshot without known positive: {sid}')
        per_repo_snap[rid].append(len(found_positive[sid])/denom)
    if set(per_repo_snap)!= {x['repo_id'] for x in repos}:
        raise ValueError('evaluation snapshot coverage does not include every selected repository')
    per_repo_recall={rid:sum(vals)/len(vals) for rid,vals in per_repo_snap.items()}
    macro_recall=sum(per_repo_recall.values())/len(per_repo_recall) if per_repo_recall else None
    novel=outcome['novel_confirmed_tp']
    tp=known_tp_count+novel
    fp=outcome['confirmed_fp']
    u=outcome['unresolved']
    adjudicated_precision=tp/(tp+fp) if tp+fp else None
    total=tp+fp+u
    # Diagnostic interval, not a confidence interval: unresolved findings
    # could all be invalid or all valid. Present both with U count.
    low=tp/total if total else None
    high=(tp+u)/total if total else None
    return {
      'run_id':run_id,'repo_count':len(repos),'evaluation_snapshot_count':len(evaluated_snaps),
      'known_positive_count':all_positives, 'known_tp_matched_distinct':known_tp_count,
      'known_micro_recall':known_tp_count/all_positives if all_positives else None,
      'known_repo_macro_recall':macro_recall,
      'confirmed_novel_vulnerabilities':novel,
      'adjudicated_precision_conditional':adjudicated_precision,
      'unresolved_count':u,
      'unknown_rate':u/total if total else None,
      'precision_lower_if_all_unresolved_invalid':low,
      'precision_upper_if_all_unresolved_valid':high,
      'confirmed_fp_count':fp,
      'excluded_duplicate_findings':outcome['duplicate'],
      'excluded_out_of_scope_findings':outcome['out_of_scope'],
      'verdict_counts':dict(outcome),
      'warning':'Adjudicated precision is conditional on completed reviews and is not full precision when unresolved > 0.' if u else None
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('root',type=Path)
    ap.add_argument('--run-id',required=True)
    a=ap.parse_args()
    print(json.dumps(compute(a.root,a.run_id),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
