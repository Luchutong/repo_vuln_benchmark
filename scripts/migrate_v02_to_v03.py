#!/usr/bin/env python3
"""Lossless v0.2 -> v0.3.1 draft migration; default dry-run.

Copies source to a NEW folder only on --apply; never edits source.
Ambiguous legacy evaluation snapshots require explicit repo_id -> snapshot_id choice.
No new confirmed_affected, verified, A/B grade, or PASS_KNOWN_SWEEP labels generated.
"""
from __future__ import annotations
import argparse,collections,datetime,hashlib,json,shutil,sys
from pathlib import Path

def load(p):
    if not p.exists():return []
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]

def dump(p, rows):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows),encoding='utf-8')

def file_sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def analyze(source, manual):
    d=source/'data'
    repos=load(d/'repositories.jsonl');snaps=load(d/'snapshots.jsonl')
    status=load(d/'snapshot_vulnerability_status.jsonl')
    R={r['repo_id']:r for r in repos};S={s['snapshot_id']:s for s in snaps}
    by_repo=collections.defaultdict(list)
    for s in snaps:by_repo[s['repo_id']].append(s)
    selection={};issues=[]
    for rid,repo in R.items():
        current=[s['snapshot_id'] for s in by_repo[rid] if s.get('evaluation_target')]
        chosen=manual.get(rid)
        if chosen is not None:
            if chosen not in S or S[chosen]['repo_id']!=rid:
                issues.append(f'INVALID manual selection {rid} -> {chosen}');continue
        elif len(current)==1:chosen=current[0]
        else:
            chosen=None
            if len(current)>1:issues.append(f'AMBIGUOUS {rid}: {len(current)} current targets; must choose manually')
            else:issues.append(f'UNSELECTED {rid}: no previous target; assess candidates, do NOT auto-pick')
        if chosen:selection[rid]=chosen
    for rid in manual:
        if rid not in R:issues.append(f'INVALID manual selection: unknown repo {rid}')
    active={sid for sid in selection.values()}
    relocated=[s for s in status if s.get('snapshot_id') not in active]
    old_targets=[s['snapshot_id'] for s in snaps if s.get('evaluation_target')]
    file_hashes={str(p.relative_to(source)):file_sha(p) for p in sorted((source/'data').glob('*.jsonl'))}
    stats={'source_repositories':len(repos),'source_snapshots':len(snaps),
           'source_evaluation_snapshots':len(old_targets),'selected_targets':len(selection),
           'source_status_rows':len(status),'active_status_rows':len(status)-len(relocated),
           'historical_status_rows':len(relocated),'issues':issues,
           'source_file_sha256':file_hashes,'selected':selection}
    if any(x.startswith('INVALID') for x in issues):raise ValueError('; '.join(issues))
    return stats,repos,snaps,status,relocated,by_repo

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,type=Path,help='existing v0.2 dataset root (read-only)')
    p.add_argument('--out',type=Path,help='new v0.3 output dataset path, MUST NOT exist')
    p.add_argument('--selections',type=Path,help='JSON object {repo_id: selected_snapshot_id}, manual approvals')
    p.add_argument('--apply',action='store_true',help='write into NEW --out; default is dry-run')
    p.add_argument('--report',type=Path,help='optional dry-run report path')
    a=p.parse_args()
    if not (a.source/'data'/'repositories.jsonl').exists():p.error('source is not a v0.2 dataset root')
    if a.apply and not a.out:p.error('--apply requires --out')
    manual=json.loads(a.selections.read_text(encoding='utf-8')) if a.selections else {}
    if not isinstance(manual,dict):p.error('--selections must contain a JSON object')
    stats,repos,snaps,status,relocated,by_repo=analyze(a.source,manual)
    if a.report:a.report.write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))
    if not a.apply:
        print('DRY RUN only. Use --apply --out NEW_DIR after reviewing selection conflicts.');return
    if a.out.exists():p.error(f'refusing to overwrite existing output: {a.out}')
    if a.out.resolve()==a.source.resolve() or a.source.resolve() in a.out.resolve().parents:
        p.error('refusing in-place or nested migration output')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(a.source,a.out,symlinks=False)
    dest=a.out/'data'
    archive=a.out/'migration_backup_v02'
    (archive/'data').mkdir(parents=True,exist_ok=True)
    for source_file in (a.source/'data').glob('*.jsonl'):
        shutil.copy2(source_file,archive/'data'/source_file.name)
    active=set(stats['selected'].values())
    now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    for r in repos:
        r['evaluation_snapshot_id']=stats['selected'].get(r['repo_id'])
    dump(dest/'repositories.jsonl',repos)
    for s in snaps:
        s['evaluation_target']=s['snapshot_id'] in active
        s['purpose']='evaluation' if s['evaluation_target'] else 'historical_evidence'
    dump(dest/'snapshots.jsonl',snaps)
    dump(dest/'snapshot_vulnerability_status.jsonl',[x for x in status if x['snapshot_id'] in active])
    dump(dest/'historical_snapshot_status.jsonl',relocated)
    dump(dest/'snapshot_candidate_triage.jsonl',[])  # no fabricated relevance verdicts
    sel=[]
    for rid,sid in stats['selected'].items():
        sr=next(r for r in repos if r['repo_id']==rid)
        sel.append({
            'repo_id':rid,'snapshot_id':sid,'decision_status':'proposed',
            'selection_policy':'documented_exception',
            'selection_reason':'Legacy v0.2 evaluation snapshot retained provisionally; independent v0.3 selection approval pending.',
            'selected_by':'v03_migration_script','selected_at':now,'frozen_at':None,
            'candidate_count':max(1,len(by_repo[rid])),
            'candidate_snapshot_ids':[x['snapshot_id'] for x in by_repo[rid]],
            'evidence_urls':[sr['canonical_url']],
            'leakage_controls':{'worktree_without_git_history':False,
                               'ground_truth_isolated':False,'network_policy':'uncontrolled'},
            'notes':'Unfrozen migration proposal, not an approved/validated benchmark selection.'
        })
    dump(dest/'evaluation_selection.jsonl',sel)
    # Old global history sweeps do not justify selected-commit PASS; preserve detail, reset outcome.
    cpath=dest/'discovery_coverage.jsonl'
    oldcover=load(cpath)
    if oldcover:
        dump(dest/'legacy_discovery_coverage.jsonl',oldcover)
        for cov in oldcover:
            cov['outcome']='NEEDS_REVIEW'
            cov.setdefault('limitations',[]).append('Legacy global coverage not yet revalidated at selected commit')
        dump(cpath,oldcover)
    manifest={'dataset_version':'0.3.1','status':'draft','target_repository_count':50,
              'evaluation_policy':'one_frozen_snapshot_snapshot_only_oracle',
              'source_cutoff_date':None,'source_dataset_version':'0.2',
              'freeze_timestamp':None,'source_file_sha256':stats['source_file_sha256'],
              'known_limitations':['Migrated draft; selection rows are proposed not frozen',
                'No new vulnerability verification was performed by migration',
                'Coverage sweep and language audit still require independent assessment']}
    (a.out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (a.out/'MIGRATION_REPORT.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'NEW DATASET CREATED: {a.out}\nSource untouched; originals backed up under migration_backup_v02/.')
if __name__=='__main__':main()
