#!/usr/bin/env python3
"""RepoVuln-50 v0.2 offline *structural* validator.

Cannot prove vulnerabilities, completeness, fixes, or false positive labels.
Run `--draft` for partial collection. Release mode checks 50 repos, extensive
source sweeps, snapshot status matrix, cross references, and A/B reviews.
"""
import argparse
import collections
import hashlib
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

NAMES = (
    'repositories', 'snapshots', 'vulnerabilities', 'locations', 'evidence',
    'reviews', 'candidates', 'discovery_coverage', 'snapshot_vulnerability_status',
)

def load(root, name, schema_root, errors, warnings, draft=False):
    filename = root / 'data' / f'{name}.jsonl'
    if not filename.exists():
        (warnings if draft else errors).append(f'{name}: missing {filename}')
        return []
    try:
        schema = json.loads((schema_root / f'{name}.schema.json').read_text(encoding='utf8'))
    except (OSError, ValueError) as e:
        errors.append(f'{name}: invalid schema: {e}')
        return []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    items = []
    for lineno, line in enumerate(filename.read_text(encoding='utf8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f'{name}:{lineno}: invalid JSON: {e}')
            continue
        for e in validator.iter_errors(item):
            errors.append(f'{name}:{lineno}:{"/".join(map(str,e.absolute_path))}: {e.message}')
        if isinstance(item, dict):
            items.append(item)
        else:
            errors.append(f'{name}:{lineno}: row is not an object')
    return items


def by_unique(items, key, name, errors):
    counter = collections.Counter(x.get(key) for x in items)
    for k, n in counter.items():
        if n > 1:
            errors.append(f'{name}: duplicate {key}={k!r} ({n} rows)')
    return {x.get(key): x for x in items}


def run(root:Path, draft:bool):
    errors, warnings = [], []
    schema_root = Path(__file__).resolve().parents[1] / 'schemas'
    data = {n:load(root, n, schema_root, errors, warnings, draft) for n in NAMES}
    repos, snaps, vulns, locs, evid, reviews, cands, covers, statuses = (data[n] for n in NAMES)
    R = by_unique(repos, 'repo_id', 'repositories', errors)
    S = by_unique(snaps, 'snapshot_id', 'snapshots', errors)
    V = by_unique(vulns, 'vulnerability_id', 'vulnerabilities', errors)
    L = by_unique(locs, 'location_id', 'locations', errors)
    E = by_unique(evid, 'evidence_id', 'evidence', errors)
    Reviews = by_unique(reviews, 'vulnerability_id', 'reviews', errors)
    by_unique(reviews, 'review_id', 'reviews', errors)
    by_unique(repos, 'canonical_url', 'repositories', errors)
    by_unique(repos, 'github_repo_id', 'repositories', errors)
    C = by_unique(cands, 'candidate_id', 'candidates', errors)
    Cover = by_unique(covers, 'repo_id', 'discovery_coverage', errors)
    pair_keys = [f'{x.get("snapshot_id")}::{x.get("vulnerability_id")}' for x in statuses]
    if len(pair_keys) != len(set(pair_keys)):
        errors.append('snapshot_vulnerability_status: duplicate (snapshot_id, vulnerability_id)')

    per_repo = collections.Counter()
    snap_by_repo = collections.defaultdict(set)
    eval_by_repo = collections.defaultdict(list)
    for s in snaps:
        rid, sid = s.get('repo_id'), s.get('snapshot_id')
        if rid not in R:
            errors.append(f'snapshot {sid}: unknown repo {rid}')
            continue
        expected = 'snap_' + hashlib.sha256((R[rid]['canonical_url']+'@'+s['vulnerable_commit']).encode()).hexdigest()[:16]
        if sid != expected:
            errors.append(f'snapshot {sid}: expected snapshot_id {expected}')
        snap_by_repo[rid].add(sid)
        if s.get('evaluation_target',False):
            eval_by_repo[rid].append(sid)
        langs = s.get('languages', [])
        if not any(lg.get('scope') == 'first_party' and lg.get('role') in ('programming', 'scripting') for lg in langs):
            errors.append(f'snapshot {sid}: no first-party code language')
        lkeys = [(x.get('name'),x.get('role'),x.get('scope'),x.get('embedded_nonadditive',False)) for x in langs]
        if len(set(lkeys)) != len(lkeys):
            errors.append(f'snapshot {sid}: repeated language/role/scope grouping')
    # Vulnerability identity, relation, release evidence.
    alias_owner = {}
    for v in vulns:
        vid, rid, sid = v.get('vulnerability_id'), v.get('repo_id'), v.get('snapshot_id')
        per_repo[rid] += 1
        if rid not in R:
            errors.append(f'vulnerability {vid}: unknown repo {rid}')
        if sid not in S or S.get(sid,{}).get('repo_id') != rid or S.get(sid,{}).get('vulnerable_commit') != v.get('vulnerable_commit'):
            errors.append(f'vulnerability {vid}: vulnerable snapshot/commit mismatch')
        aliases = {str(x).upper() for x in v.get('aliases',[])}
        if vid not in aliases:
            errors.append(f'vulnerability {vid}: ID missing in alias list')
        for a in aliases:
            if a in alias_owner and alias_owner[a] != vid:
                errors.append(f'vulnerability alias {a}: already owned by {alias_owner[a]}, conflict with {vid}')
            alias_owner[a] = vid
        for fixed in v.get('fixed_releases',[]):
            if not any(fixed.get('package') == affected.get('package') and fixed.get('ecosystem') == affected.get('ecosystem') for affected in v.get('affected_packages',[])):
                errors.append(f'vulnerability {vid}: fixed release package/ecosystem not in affected_packages')

    loc_count = collections.Counter()
    location_pairs = set()
    for l in locs:
        lid, vid = l.get('location_id'), l.get('vulnerability_id')
        loc_count[vid] += 1
        sid = l.get('snapshot_id')
        location_pairs.add((sid,vid))
        if vid not in V:
            errors.append(f'location {lid}: missing vulnerability {vid}')
        elif sid not in S or S[sid].get('repo_id') != V[vid].get('repo_id'):
            errors.append(f'location {lid}: snapshot does not belong to vulnerability repository')
    for vid in V:
        if not loc_count[vid]:
            errors.append(f'vulnerability {vid}: missing verified root-cause location')

    grades = collections.Counter()
    for review in reviews:
        vid = review.get('vulnerability_id')
        grades[review.get('grade')] += 1
        if vid not in V:
            errors.append(f'review: unknown vulnerability {vid}')
        if review.get('reviewer') == review.get('independent_reviewer'):
            errors.append(f'review {vid}: reviewer and independent reviewer identical')
    for vid in V:
        if vid not in Reviews:
            errors.append(f'vulnerability {vid}: missing review')
    targets = {'repository':R, 'snapshot':S, 'vulnerability':V,
               'location':L, 'review':{r.get('review_id'):r for r in reviews}}
    evidence_pass = collections.defaultdict(set)
    for e in evid:
        eid = e.get('evidence_id')
        if e.get('target_id') not in targets.get(e.get('target_type'),{}):
            errors.append(f'evidence {eid}: missing target')
        if e.get('result') == 'PASS':
            evidence_pass[(e.get('target_type'),e.get('target_id'))].add(e.get('field_path',''))
    for vid in V:
        fields = evidence_pass[('vulnerability',vid)]
        for field in ('severity','vulnerable_commit','fix_commits','fixed_releases'):
            if not any(x==field or x.startswith(field+'.') for x in fields):
                errors.append(f'vulnerability {vid}: missing PASS evidence for {field}')
    for sid in S:
        fields=evidence_pass[('snapshot',sid)]
        if not any(x=='languages' or x.startswith('languages.') for x in fields):
            errors.append(f'snapshot {sid}: missing PASS language inventory evidence')
    for lid in L:
        fields=evidence_pass[('location',lid)]
        if not any(x=='critical_operation' or x.startswith('critical_operation.') for x in fields):
            errors.append(f'location {lid}: missing PASS root-cause evidence')
    for c in cands:
        if c.get('repo_id') not in R and not draft:
            warnings.append(f'candidate {c.get("candidate_id")}: repo excluded/not in selected 50; place preselection candidates in runs/')
        if c.get('status')=='verified' and c.get('vulnerability_id') not in V:
            errors.append(f'candidate {c.get("candidate_id")}: marked verified but no catalog vulnerability')

    for r in repos:
        rid = r.get('repo_id')
        if 'github.com/openclaw/openclaw' in str(r.get('canonical_url','')).lower():
            errors.append('blacklist: OpenClaw must be excluded')
        sr = S.get(r.get('representative_snapshot_id'))
        if not sr or sr.get('repo_id') != rid:
            errors.append(f'repo {rid}: invalid representative_snapshot_id')
        if not draft:
            if rid not in Cover:
                errors.append(f'repo {rid}: missing discovery_coverage row')
            if not eval_by_repo.get(rid):
                errors.append(f'repo {rid}: no evaluation_target snapshot')
            if per_repo[rid] == 0:
                errors.append(f'repo {rid}: no verified historical catalog vulnerabilities')
    for coverage in covers:
        rid = coverage.get('repo_id')
        if rid not in R and not draft:
            errors.append(f'discovery_coverage: unknown selected repository {rid}')
        if coverage.get('outcome') == 'PASS_KNOWN_SWEEP':
            passes = coverage.get('passes',[])
            if len(passes) < 2 or any(x.get('new_verified_count',1) != 0 for x in passes[-2:]):
                errors.append(f'coverage {rid}: PASS_KNOWN_SWEEP requires last 2 passes with zero newly verified vulns')
            source_types = {x.get('source_type') for x in coverage.get('source_checks',[]) if x.get('result')=='PASS'}
            if 'advisory' not in source_types and 'vulnerability_db' not in source_types:
                errors.append(f'coverage {rid}: no successful public advisory/database source')
            if 'upstream' not in source_types and 'code_history' not in source_types:
                errors.append(f'coverage {rid}: no successful upstream/history source')
        elif not draft:
            errors.append(f'coverage {rid}: cannot release as PASS_KNOWN_SWEEP')
        if coverage.get('unresolved_candidates',0) > 0:
            warnings.append(f'coverage {rid}: {coverage["unresolved_candidates"]} unresolved candidates; transparent limitation required')

    matrix = {(r.get('snapshot_id'),r.get('vulnerability_id')):r for r in statuses}
    pos_per_snapshot = collections.Counter()
    matrix_counts=collections.Counter()
    for row in statuses:
        sid, vid, rid, status = (row.get(k) for k in ('snapshot_id','vulnerability_id','repo_id','status'))
        matrix_counts[status] += 1
        snap, vuln = S.get(sid), V.get(vid)
        if not snap or not snap.get('evaluation_target'):
            errors.append(f'status {sid}/{vid}: snapshot missing or not an evaluation_target')
        if not vuln:
            errors.append(f'status {sid}/{vid}: unknown catalog vulnerability')
        if snap and (snap.get('repo_id')!=rid or (vuln and vuln.get('repo_id')!=rid)):
            errors.append(f'status {sid}/{vid}: repo mismatch')
        if status in ('confirmed_affected','confirmed_not_affected'):
            ids = row.get('evidence_ids', [])
            if not ids or any(i not in E or E[i].get('result')!='PASS' for i in ids):
                errors.append(f'status {sid}/{vid}: confirmed state without PASS evidence_ids')
            if not row.get('proof_summary'):
                errors.append(f'status {sid}/{vid}: confirmed state without proof_summary')
        if status == 'confirmed_affected':
            pos_per_snapshot[sid] += 1
            if (sid,vid) not in location_pairs:
                errors.append(f'status {sid}/{vid}: confirmed_affected lacks root-cause location for THIS snapshot')
    if not draft:
        for rid, sids in eval_by_repo.items():
            ids = {v['vulnerability_id'] for v in vulns if v.get('repo_id')==rid}
            for sid in sids:
                if pos_per_snapshot[sid] < 1:
                    errors.append(f'evaluation snapshot {sid}: no confirmed_affected vulnerability')
                for vid in ids:
                    if (sid,vid) not in matrix:
                        errors.append(f'evaluation snapshot {sid}: missing status for catalog vuln {vid} (set unknown if unsure)')
        if len(repos) != 50:
            errors.append(f'repository count {len(repos)} != target 50')
        if len(covers) != 50:
            errors.append(f'discovery_coverage count {len(covers)} != 50')
        langs = collections.Counter(x.get('primary_language') for x in repos)
        if len(langs) < 10:
            errors.append(f'primary language categories {len(langs)} < 10')
        if langs and langs.most_common(1)[0][1] > 10:
            errors.append(f'too many repositories of one primary language: {langs.most_common(1)[0]}')
    else:
        for rid in R:
            if rid not in Cover:
                warnings.append(f'coverage for repo {rid} not collected yet')

    if len(vulns) and grades.get('A',0)/len(vulns)<.60:
        warnings.append(f'aspirational grade A rate <60% ({grades.get("A",0)}/{len(vulns)})')
    owners=collections.Counter(str(r.get('owner','')).lower() for r in repos)
    if owners and owners.most_common(1)[0][1]>2:
        warnings.append(f'owner concentration: {owners.most_common(1)[0]}')
    summary = {'mode':'draft' if draft else 'release',
               'counts':{x:len(data[x]) for x in NAMES},
               'verified_catalog_per_repository':dict(per_repo),
               'evaluation_snapshots':sum(len(x) for x in eval_by_repo.values()),
               'snapshot_truth_counts':dict(matrix_counts),
               'verification_grades':dict(grades),
               'errors':errors[:200], 'warnings':warnings[:100], 'truncated_errors':max(len(errors)-200,0)}
    return summary, not bool(errors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root',type=Path)
    parser.add_argument('--draft',action='store_true')
    args=parser.parse_args()
    result,ok=run(args.root,args.draft)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not ok:sys.exit(1)
    print('STRUCTURAL VALIDATION PASSED; NOT a completeness, exploitability, or score validation.')

if __name__=='__main__':main()
