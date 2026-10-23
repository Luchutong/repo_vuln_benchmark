#!/usr/bin/env python3
"""Read-only source upgrade v0.3 -> v0.3.1. Does NOT create triage verdicts or true vulnerability labels."""
from __future__ import annotations
import argparse,hashlib,json,shutil
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--apply',action='store_true');a=ap.parse_args()
    src=a.source.resolve();dst=a.out.resolve()
    if not (src/'manifest.json').is_file():ap.error('manifest.json absent')
    m=json.loads((src/'manifest.json').read_text(encoding='utf8'))
    if m.get('dataset_version')!='0.3.0':ap.error('expected v0.3.0 source manifest, received '+str(m.get('dataset_version')))
    if dst==src or src in dst.parents:ap.error('cannot write into source or nested source')
    if dst.exists():ap.error('destination already exists')
    source_files={str(p.relative_to(src)):sha(p) for p in sorted(src.rglob('*')) if p.is_file()}
    print(json.dumps({'files_to_copy':len(source_files),'source_version':m['dataset_version'],'source_status':m.get('status'),'source_untouched':True},ensure_ascii=False,indent=2))
    if not a.apply:return
    shutil.copytree(src,dst)
    m['dataset_version']='0.3.1';m['evaluation_policy']='one_frozen_snapshot_snapshot_only_oracle';m['status']='draft';m['freeze_timestamp']=None
    m.setdefault('known_limitations',[]).append('v0.3 full-history coverage does not establish selected-snapshot completeness; repeat scoped sweep')
    (dst/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    d=dst/'data';d.mkdir(parents=True,exist_ok=True)
    # Preserve old coverage in an explicit archive; do not inherit PASS as a benchmark completeness guarantee.
    cover=d/'discovery_coverage.jsonl'
    if cover.exists():
        shutil.copy2(cover,d/'legacy_discovery_coverage_v03.jsonl')
        rows=[json.loads(line) for line in cover.read_text(encoding='utf8').splitlines() if line.strip()]
        for row in rows:
            row['outcome']='NEEDS_REVIEW'
            row.setdefault('limitations',[]).append('Must run v0.3.1 selected-snapshot discovery checks before new PASS')
        cover.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf8')
    triage=d/'snapshot_candidate_triage.jsonl'
    if not triage.exists():triage.write_text('',encoding='utf8')
    (dst/'UPGRADE_REPORT.json').write_text(json.dumps({'from':'0.3.0','to':'0.3.1','source_sha256':source_files,'source_unchanged':True,'no_new_triage_or_verification_labels':True,'coverage_reset_to_needs_review':True},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Created new v0.3.1 draft at',dst,'; source untouched, no vulnerability status fabricated')
if __name__=='__main__':main()
