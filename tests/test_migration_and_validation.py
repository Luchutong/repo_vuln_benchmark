"""Synthetic regression tests. They prove workflow mechanics, NOT vulnerability truth."""
import hashlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_dataset import validate

def writej(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')

def snap(repo,sha,eval_):
    return {'snapshot_id':'snap_'+hashlib.sha256((repo['canonical_url']+'@'+sha).encode()).hexdigest()[:16],
            'repo_id':repo['repo_id'],'vulnerable_commit':sha,'evaluation_target':eval_,
            'language_tool':'Linguist','language_tool_version':'1.0','full_scan':True,
            'tracked_files_scanned':1,'collected_at':'2026-10-22T01:00:00Z',
            'languages':[{'name':'Python','role':'programming','scope':'first_party','file_count':1,
             'code_bytes':100,'share_pct':100.0,'detection_method':'Linguist','confidence':'high'}]}

class TestMigration(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.base=Path(self.t.name)
        self.source=self.base/'v02'
        self.data=self.source/'data'
        self.data.mkdir(parents=True)
        self.ra={'repo_id':'repo_a','canonical_url':'https://github.com/example/a','github_repo_id':1,
                 'owner':'example','full_name':'example/a','project_kind':'library','primary_language':'Python',
                 'quality':{'score':85,'status':'PASS','source_evidence_urls':['https://github.com/example/a'],'summary':'Reviewed'}}
        self.rb={'repo_id':'repo_b','canonical_url':'https://github.com/example/b','github_repo_id':2,
                 'owner':'example','full_name':'example/b','project_kind':'library','primary_language':'Python',
                 'quality':{'score':85,'status':'PASS','source_evidence_urls':['https://github.com/example/b'],'summary':'Reviewed'}}
        self.s1=snap(self.ra,'a'*40,True);self.s2=snap(self.ra,'b'*40,True);self.s3=snap(self.rb,'c'*40,True)
        self.ra['representative_snapshot_id']=self.s1['snapshot_id']
        self.rb['representative_snapshot_id']=self.s3['snapshot_id']
        writej(self.data/'repositories.jsonl',[self.ra,self.rb])
        writej(self.data/'snapshots.jsonl',[self.s1,self.s2,self.s3])
        self.statuses=[{'snapshot_id':x['snapshot_id'],'repo_id':x['repo_id'],
                        'vulnerability_id':f'v{i}','status':'unknown','basis':'not checked',
                        'checked_at':'2026-10-22T01:00:00Z'} for i,x in enumerate((self.s1,self.s2,self.s3))]
        writej(self.data/'snapshot_vulnerability_status.jsonl',self.statuses)
        for n in ('vulnerabilities','locations','evidence','reviews','candidates','discovery_coverage'):
            writej(self.data/f'{n}.jsonl',[])
        self.orig=(self.data/'snapshot_vulnerability_status.jsonl').read_bytes()

    def cmd(self,*args,expect=0):
        p=subprocess.run([sys.executable,str(ROOT/'scripts'/'migrate_v02_to_v03.py'),
                          '--source',str(self.source),*map(str,args)],capture_output=True,text=True)
        self.assertEqual(p.returncode,expect,p.stderr+p.stdout)
        return p

    def test_dry_run_never_writes(self):
        p=self.cmd()
        self.assertIn('DRY RUN only',p.stdout)
        self.assertEqual(sorted(self.base.iterdir()),[self.source])
        self.assertEqual((self.data/'snapshot_vulnerability_status.jsonl').read_bytes(),self.orig)

    def test_conflicting_snapshots_require_explicit_resolution(self):
        p=self.cmd()
        self.assertIn('AMBIGUOUS repo_a',p.stdout)
        dest=self.base/'v03'
        self.cmd('--out',dest,'--apply')
        snaps=[json.loads(x) for x in (dest/'data'/'snapshots.jsonl').read_text().splitlines()]
        self.assertEqual(sum(s['evaluation_target'] for s in snaps),1)  # only repo_b selected
        hist=[json.loads(x) for x in (dest/'data'/'historical_snapshot_status.jsonl').read_text().splitlines()]
        self.assertEqual(len(hist),2)
        self.assertEqual((dest/'migration_backup_v02/data/snapshot_vulnerability_status.jsonl').read_bytes(),self.orig)
        self.assertEqual((self.data/'snapshot_vulnerability_status.jsonl').read_bytes(),self.orig)
        report,ok=validate(dest,True)
        self.assertFalse(any('allows ONE' in e for e in report['errors']), report['errors'])
        self.assertEqual(report['repos_with_one_target'],1)

    def test_manual_choice_preserves_selected_oracle(self):
        selection=self.base/'choose.json'
        selection.write_text(json.dumps({'repo_a':self.s2['snapshot_id']}))
        dest=self.base/'v03'
        self.cmd('--selections',selection,'--out',dest,'--apply')
        active=[json.loads(x) for x in (dest/'data'/'snapshot_vulnerability_status.jsonl').read_text().splitlines()]
        self.assertEqual(len(active),2)  # s2 and s3
        self.assertEqual(len((dest/'data'/'historical_snapshot_status.jsonl').read_text().splitlines()),1)
        original=sorted(x['vulnerability_id'] for x in self.statuses)
        reconstructed=sorted(x['vulnerability_id'] for x in active)+sorted(json.loads(x)['vulnerability_id'] for x in (dest/'data'/'historical_snapshot_status.jsonl').read_text().splitlines())
        self.assertEqual(sorted(reconstructed),original)
        entries=[json.loads(x) for x in (dest/'data'/'evaluation_selection.jsonl').read_text().splitlines()]
        self.assertEqual(len(entries),2)
        self.assertTrue(all(e['decision_status']=='proposed' for e in entries))
        self.assertTrue(all(not e['leakage_controls']['ground_truth_isolated'] for e in entries))

    def test_multiple_targets_rejected_by_validator(self):
        self.ra['evaluation_snapshot_id']=self.s1['snapshot_id']
        writej(self.data/'repositories.jsonl',[self.ra,self.rb])
        writej(self.data/'evaluation_selection.jsonl',[])
        report,ok=validate(self.source,True)
        self.assertFalse(ok)
        self.assertTrue(any('allows ONE' in x for x in report['errors']))

    def test_release_must_have_50_and_frozen_target(self):
        dest=self.base/'v03'
        self.cmd('--out',dest,'--apply')
        report,ok=validate(dest,False)
        self.assertFalse(ok)
        self.assertTrue(any('!= 50' in x or 'not frozen' in x for x in report['errors']))

if __name__=='__main__':unittest.main()
