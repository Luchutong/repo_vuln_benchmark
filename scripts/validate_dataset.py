#!/usr/bin/env python3
"""RepoVuln-50 v0.3.1 snapshot-focused validator (NOT exploit proof).

Draft: preserve partial progress, forbid conflicting evaluation targets.
Release: 50 repos, 1 frozen target per repo, catalog/source coverage,
snapshot-specific candidate triage and reviewed known positives (no full historical deep verification).
Never interprets unmatched findings as false positives.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

DATA_NAMES = ('repositories','snapshots','vulnerabilities','locations','evidence','reviews',
              'candidates','discovery_coverage','snapshot_vulnerability_status','evaluation_selection','snapshot_candidate_triage')

def read_jsonl(path, schema, errors, warnings, draft):
    if not path.exists():
        (warnings if draft else errors).append(f'missing: {path.name}')
        return []
    rows=[]
    v=Draft202012Validator(schema, format_checker=FormatChecker())
    with path.open(encoding='utf-8') as f:
        for n,line in enumerate(f,1):
            if not line.strip():continue
            try: obj=json.loads(line)
            except ValueError as e: errors.append(f'{path.name}:{n}: JSON {e}');continue
            if not isinstance(obj,dict):errors.append(f'{path.name}:{n}: expected JSON object');continue
            for err in v.iter_errors(obj):
                errors.append(f'{path.name}:{n}:{"/".join(map(str,err.absolute_path))}: {err.message}')
            rows.append(obj)
    return rows

def unique(rows,key,table,errors):
    d={}
    for row in rows:
        val=row.get(key)
        if val is None:
            errors.append(f'{table}: missing {key}');continue
        if val in d:errors.append(f'{table}: duplicate {key}={val}')
        d[val]=row
    return d

def validate(root:Path,draft=True):
    E,W=[],[]
    sr=Path(__file__).resolve().parents[1]/'schemas'
    schemas={}
    for name in DATA_NAMES+('manifest',):
        try:
            schema=json.loads((sr/f'{name}.schema.json').read_text(encoding='utf-8'))
            Draft202012Validator.check_schema(schema)
            schemas[name]=schema
        except Exception as e:E.append(f'invalid schema {name}: {e}')
    if E:return {'errors':E,'warnings':W},False
    mf=root/'manifest.json'
    if mf.exists():
        try:
            manifest=json.loads(mf.read_text(encoding='utf-8'))
            for err in Draft202012Validator(schemas['manifest'],format_checker=FormatChecker()).iter_errors(manifest):
                E.append(f'manifest:{"/".join(map(str,err.absolute_path))}: {err.message}')
        except Exception as e:E.append(f'manifest cannot read: {e}')
    else:
        (W if draft else E).append('manifest.json missing')
        manifest={}
    data={name:read_jsonl(root/'data'/f'{name}.jsonl',schemas[name],E,W,draft) for name in DATA_NAMES}
    R=unique(data['repositories'],'repo_id','repositories',E)
    S=unique(data['snapshots'],'snapshot_id','snapshots',E)
    V=unique(data['vulnerabilities'],'vulnerability_id','vulnerabilities',E)
    L=unique(data['locations'],'location_id','locations',E)
    Ev=unique(data['evidence'],'evidence_id','evidence',E)
    RV=unique(data['reviews'],'vulnerability_id','reviews',E)
    unique(data['reviews'],'review_id','reviews',E)
    unique(data['candidates'],'candidate_id','candidates',E)
    COV=unique(data['discovery_coverage'],'repo_id','discovery_coverage',E)
    cand=unique(data['candidates'],'candidate_id','candidates',E)
    SEL=unique(data['evaluation_selection'],'repo_id','evaluation_selection',E)
    unique(data['repositories'],'canonical_url','repositories',E)
    unique(data['repositories'],'github_repo_id','repositories',E)
    selected=collections.defaultdict(list)
    triage_index={}
    triage_by_repo=collections.defaultdict(list)
    catalog=collections.defaultdict(set)
    location_pairs=set()
    for sid,s in S.items():
        rid=s.get('repo_id');repo=R.get(rid)
        if not repo:E.append(f'snapshot {sid}: unknown repository {rid}');continue
        sha=s.get('vulnerable_commit')
        if s.get('commit_sha') and s.get('commit_sha')!=sha:E.append(f'snapshot {sid}: commit_sha and vulnerable_commit differ')
        if isinstance(sha,str):
            exp='snap_'+hashlib.sha256((repo['canonical_url']+'@'+sha).encode()).hexdigest()[:16]
            if sid!=exp:E.append(f'snapshot {sid}: expected id {exp}')
        if s.get('evaluation_target',False):
            selected[rid].append(sid)
            if not s.get('full_scan') or not s.get('languages') or not s.get('language_tool') or not s.get('language_tool_version') or not s.get('tracked_files_scanned'):
                E.append(f'evaluation snapshot {sid}: complete language inventory required')
            if not any(x.get('scope')=='first_party' and x.get('role') in ('programming','scripting') for x in s.get('languages',[])):
                E.append(f'evaluation snapshot {sid}: first party programming language missing')
        lang_keys=[(l.get('name'),l.get('scope'),l.get('role'),l.get('embedded_nonadditive',False)) for l in s.get('languages',[])]
        if len(lang_keys)!=len(set(lang_keys)):
            E.append(f'snapshot {sid}: duplicate language grouping')
    for rid,sids in selected.items():
        if len(sids)>1:E.append(f'repo {rid}: {len(sids)} evaluation targets; v0.3 allows ONE')
    if len(data['repositories'])>50:E.append('more than 50 selected repositories')
    alias_owners={}
    for vid,v in V.items():
        rid=v.get('repo_id')
        catalog[rid].add(vid)
        if rid not in R:E.append(f'vulnerability {vid}: repo {rid} unknown')
        sid=v.get('snapshot_id')
        if sid:
            snap=S.get(sid)
            if not snap or snap.get('repo_id')!=rid or snap.get('vulnerable_commit')!=v.get('vulnerable_commit'):
                E.append(f'vulnerability {vid}: optional historical snapshot mismatch')
        aliases={str(x).upper() for x in v.get('aliases',[])}
        if str(vid).upper() not in aliases:E.append(f'vulnerability {vid}: ID not present among aliases')
        for a in aliases:
            if a in alias_owners and alias_owners[a]!=vid:E.append(f'alias {a}: maps to both {vid} and {alias_owners[a]}')
            alias_owners[a]=vid
        ap={(x.get('package'),x.get('ecosystem')) for x in v.get('affected_packages',[])}
        for fr in v.get('fixed_releases',[]):
            if (fr.get('package'),fr.get('ecosystem')) not in ap:E.append(f'vulnerability {vid}: fixed release package not affected')
    count_loc=collections.Counter()
    for lid,l in L.items():
        vid=l.get('vulnerability_id');sid=l.get('snapshot_id');csha=l.get('commit_sha')
        if vid not in V:E.append(f'location {lid}: vulnerability {vid} missing');continue
        count_loc[vid]+=1
        if sid:
            snap=S.get(sid)
            if not snap or snap.get('repo_id')!=V[vid].get('repo_id'):
                E.append(f'location {lid}: snapshot invalid or wrong repository')
            elif csha and csha!=snap.get('vulnerable_commit'):
                E.append(f'location {lid}: commit_sha conflicts with snapshot')
            location_pairs.add((sid,vid))
        elif not csha:E.append(f'location {lid}: needs snapshot_id OR commit_sha')
    for vid in V:
        if not count_loc[vid]:E.append(f'vulnerability {vid}: no root-cause location')
    for vid,rev in RV.items():
        if vid not in V:E.append(f'review {vid}: vulnerability absent')
        if rev.get('reviewer')==rev.get('independent_reviewer'):
            E.append(f'review {vid}: reviewers must be independent')
    for vid in V:
        if vid not in RV:E.append(f'vulnerability {vid}: no approved A/B review')
    target_keys={'repository':R,'snapshot':S,'vulnerability':V,'location':L,
                 'review':{x.get('review_id'):x for x in data['reviews']}}
    passed=collections.defaultdict(set)
    for eid,e in Ev.items():
        ty,tid=e.get('target_type'),e.get('target_id')
        if tid not in target_keys.get(ty,{}):E.append(f'evidence {eid}: target {ty}/{tid} absent')
        if e.get('result')=='PASS':passed[(ty,tid)].add(e.get('field_path',''))
    for vid in V:
        for f in ('severity','vulnerable_commit','fix_commits','fixed_releases'):
            if not any(x==f or x.startswith(f+'.') for x in passed[('vulnerability',vid)]):
                E.append(f'vulnerability {vid}: no PASS evidence for {f}')
    for sid in {x for sids in selected.values() for x in sids}:
        if not any(x=='languages' or x.startswith('languages.') for x in passed[('snapshot',sid)]):
            E.append(f'evaluation snapshot {sid}: no PASS language evidence')
    for lid in L:
        if not any(x=='critical_operation' or x.startswith('critical_operation.') for x in passed[('location',lid)]):
            E.append(f'location {lid}: no PASS root cause evidence')
    for rid,repo in R.items():
        if repo.get('canonical_url','').lower().rstrip('/')=='https://github.com/openclaw/openclaw':
            E.append('excluded repository OpenClaw included')
        refs=repo.get('representative_snapshot_id')
        if refs and (refs not in S or S[refs].get('repo_id')!=rid):E.append(f'repo {rid}: representative snapshot invalid')
        selid=repo.get('evaluation_snapshot_id')
        if selid and (selid not in S or S[selid].get('repo_id')!=rid or selid not in selected[rid]):
            E.append(f'repo {rid}: evaluation_snapshot_id does not refer to selected target')
        if len(selected[rid])==1 and selid!=selected[rid][0]:
            (W if draft else E).append(f'repo {rid}: set evaluation_snapshot_id={selected[rid][0]}')
        if not draft and len(selected[rid])!=1:E.append(f'repo {rid}: release requires EXACTLY one evaluation snapshot')
        if not draft and not catalog[rid]:E.append(f'repo {rid}: no catalog vulnerabilities')
    for rid,sel in SEL.items():
        sid=sel.get('snapshot_id')
        if rid not in R:E.append(f'selection {rid}: unknown repository')
        if sid not in selected.get(rid,[]):E.append(f'selection {rid}: snapshot not marked evaluation_target')
        if sel.get('decision_status')=='frozen':
            controls=sel.get('leakage_controls',{})
            if not controls.get('worktree_without_git_history') or not controls.get('ground_truth_isolated') or controls.get('network_policy')=='uncontrolled':
                E.append(f'selection {rid}: frozen but leakage controls insufficient')
            if not sel.get('frozen_at'):E.append(f'selection {rid}: frozen_at missing')
            if not sel.get('reviewed_by') or sel.get('reviewed_by')==sel.get('selected_by'):
                E.append(f'selection {rid}: second independent reviewer required')
        if not draft and sel.get('decision_status')!='frozen':E.append(f'selection {rid}: not frozen')
    for rid in R:
        if len(selected[rid])==1 and rid not in SEL:
            (W if draft else E).append(f'repo {rid}: evaluation_selection row missing')
    status_rows={}
    positives=collections.Counter()
    statuses=collections.Counter()
    for s in data['snapshot_vulnerability_status']:
        sid,vid,rid,st=(s.get(k) for k in ('snapshot_id','vulnerability_id','repo_id','status'))
        key=(sid,vid)
        if key in status_rows:E.append(f'matrix: duplicated {sid}/{vid}')
        status_rows[key]=s
        snap,vuln=S.get(sid),V.get(vid)
        if not snap or not snap.get('evaluation_target'):E.append(f'matrix {sid}/{vid}: only official evaluation snapshots in main oracle')
        if not vuln or not snap or vuln.get('repo_id')!=rid or snap.get('repo_id')!=rid:
            E.append(f'matrix {sid}/{vid}: repository/vulnerability mismatch')
        statuses[st]+=1
        if st in ('confirmed_affected','confirmed_not_affected'):
            eids=s.get('evidence_ids',[])
            if not eids or any(eid not in Ev or Ev[eid].get('result')!='PASS' for eid in eids):
                E.append(f'matrix {sid}/{vid}: confirmed status without PASS evidence')
            if not s.get('proof_summary'):E.append(f'matrix {sid}/{vid}: confirmed status without proof_summary')
        if st=='confirmed_affected':
            positives[sid]+=1
            if (sid,vid) not in location_pairs:E.append(f'matrix {sid}/{vid}: known positive not located at THIS snapshot')
    # v0.3.1: DO NOT require status rows for every historical Catalog CVE.
    # The oracle is intentionally limited to vulnerabilities verified at the selected SHA.
    for rid in R:
        for sid in selected[rid]:
            if not draft and positives[sid]<1:
                E.append(f'oracle {sid}: no confirmed_affected; not eligible for recall benchmark')
    for t in data['snapshot_candidate_triage']:
        cid,rid,sid,decision=(t.get(k) for k in ('candidate_id','repo_id','snapshot_id','decision'))
        if cid not in cand: E.append(f'triage {cid}: candidate missing')
        elif cand[cid].get('repo_id')!=rid: E.append(f'triage {cid}: repo mismatch')
        if sid not in selected.get(rid,[]): E.append(f'triage {cid}: snapshot is not selected evaluation target')
        k=(sid,cid)
        if k in triage_index: E.append(f'triage duplicate row {sid}/{cid}')
        triage_index[k]=t
        triage_by_repo[rid].append(t)
        if decision=='confirmed_affected':
            vid=t.get('vulnerability_id')
            if not vid or (sid,vid) not in status_rows or status_rows[(sid,vid)]['status']!='confirmed_affected':
                E.append(f'triage {cid}: confirmed_affected without matching selected-SHA oracle')
        if decision in ('confirmed_not_affected','out_of_scope'):
            if t.get('review_method') in ('unresolved','alias_cluster'):
                E.append(f'triage {cid}: negative decision without version/code/scope evidence method')
            if not t.get('evidence_urls'): E.append(f'triage {cid}: negative decision needs source proof')
        if decision=='duplicate':
            target=t.get('canonical_candidate_id')
            if not target or target==cid or target not in cand:
                E.append(f'triage {cid}: invalid canonical candidate for alias/duplicate')
    if not draft:
        for rid in R:
            for sid in selected[rid]:
                missing=[cid for cid,c in cand.items() if c.get('repo_id')==rid and (sid,cid) not in triage_index]
                if missing:
                    E.append(f'snapshot triage {sid}: {len(missing)} catalog candidates not pre-filtered (example {missing[:2]})')
                open_items=[t for t in triage_by_repo[rid] if t.get('decision') in ('possible_affected','unknown')]
                if open_items:
                    E.append(f'snapshot triage {sid}: {len(open_items)} possibly relevant/unknown candidates unresolved, cannot assert benchmark known-positive completeness')

    for cov in data['discovery_coverage']:
        rid=cov.get('repo_id')
        if rid not in R:E.append(f'coverage {rid}: repository unknown')
        if not draft:
            if cov.get('coverage_mode')!='selected_snapshot_only' or cov.get('scope',{}).get('mode')!='selected_snapshot_only':
                E.append(f'coverage {rid}: sweep must be scoped to selected snapshot')
            if cov.get('scope',{}).get('evaluation_snapshot_id') not in selected.get(rid,[]):
                E.append(f'coverage {rid}: missing/mismatched selected snapshot ID')
            if cov.get('relevance_unresolved_count',0)>0:
                E.append(f'coverage {rid}: relevant unknown candidates block full-pass declaration')
        if cov.get('outcome')!='PASS_KNOWN_SWEEP':
            if not draft:E.append(f'coverage {rid}: NOT PASS_KNOWN_SWEEP')
        else:
            passes=cov.get('passes',[])
            if len(passes)<2 or any(p.get('new_relevant_candidate_count',-1)!=0 for p in passes[-2:]):
                E.append(f'coverage {rid}: must have 2 consecutive zero-NEW-RELEVANT-CANDIDATE sweeps')
            stypes={x.get('source_type') for x in cov.get('source_checks',[]) if x.get('result')=='PASS'}
            if not stypes.intersection({'advisory','vulnerability_db'}):E.append(f'coverage {rid}: missing public database successful search')
            if not stypes.intersection({'upstream','code_history'}):E.append(f'coverage {rid}: missing upstream/history successful search')
        if cov.get('unresolved_candidates',0)>0:W.append(f'coverage {rid}: {cov["unresolved_candidates"]} unresolved candidates (disclose limitations)')
    for c in data['candidates']:
        if c.get('status')=='verified' and c.get('vulnerability_id') not in V:
            (W if draft else E).append(f'candidate {c.get("candidate_id")}: verified without catalog link (possible alias; do not drop)')
    if not draft:
        if manifest.get('status')!='release':E.append('manifest: status must be release')
        if not manifest.get('freeze_timestamp'):E.append('manifest: missing freeze_timestamp')
        if not manifest.get('source_cutoff_date'):E.append('manifest: source_cutoff_date unconfirmed')
        if len(R)!=50:E.append(f'repositories {len(R)} != 50')
        if len(SEL)!=50:E.append(f'evaluation_selection {len(SEL)} != 50')
        if len(COV)!=50:E.append(f'discovery_coverage {len(COV)} != 50')
        language_counts=collections.Counter(r.get('primary_language') for r in R.values())
        if len(language_counts)<10:E.append(f'main language diversity {len(language_counts)} < 10')
        if language_counts and language_counts.most_common(1)[0][1]>10:E.append('one dominant main language exceeds 10 repositories')
    elif manifest.get('status')=='release':W.append('manifest marked release while using --draft; execute strict mode')
    grade_counts=collections.Counter(r.get('grade') for r in data['reviews'])
    if V and grade_counts.get('A',0)/len(V)<.6:W.append('grade A <60% aspirational target; report transparent grade-B limitation')
    counts={k:len(v) for k,v in data.items()}
    summary={'version':'0.3.1','mode':'draft' if draft else 'release', 'counts':counts,
            'evaluation_snapshot_count':sum(len(x) for x in selected.values()),
            'repos_with_one_target':sum(len(selected[rid])==1 for rid in R),
            'known_positives':sum(positives.values()),'truth_statuses':dict(statuses),
            'triaged_candidates':len(triage_index),'pending_relevant_triage':sum(t.get('decision') in ('possible_affected','unknown') for t in triage_index.values()),
            'grade_counts':dict(grade_counts),'errors':E[:300],'warnings':W[:150],
            'more_errors':max(0,len(E)-300),'more_warnings':max(0,len(W)-150)}
    return summary,not bool(E)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('root',type=Path);p.add_argument('--draft',action='store_true')
    p.add_argument('--json-out',type=Path)
    a=p.parse_args()
    report,ok=validate(a.root,a.draft)
    output=json.dumps(report,ensure_ascii=False,indent=2)
    print(output)
    if a.json_out:a.json_out.write_text(output+'\n',encoding='utf8')
    print('STRUCTURE CHECK ONLY; not a proof of true vulnerabilities or full coverage')
    sys.exit(0 if ok else 1)

if __name__=='__main__':main()
