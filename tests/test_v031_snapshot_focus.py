"""v0.3.1 regression: no fabricated states, scoped triage, and cost inputs."""
import hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from plan_snapshot_queue import plan
from cost_report import report
from jsonschema import Draft202012Validator


def emit(p,arr):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in arr),encoding='utf8')

class SnapshotFocusTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_queue_prioritizes_relevant_and_archives_justified_irrelevant(self):
        emit(self.root/'data'/'snapshots.jsonl',[{'repo_id':'r1','snapshot_id':'sha1','evaluation_target':True}])
        emit(self.root/'data'/'candidates.jsonl',[{'candidate_id':i,'repo_id':'r1','status':'pending_version'} for i in ('c1','c2','c3')])
        emit(self.root/'data'/'snapshot_candidate_triage.jsonl',[
            {'candidate_id':'c1','repo_id':'r1','snapshot_id':'sha1','decision':'confirmed_not_affected'},
            {'candidate_id':'c2','repo_id':'r1','snapshot_id':'sha1','decision':'possible_affected'}])
        q=plan(self.root)
        self.assertEqual(q['counts'],{'ARCHIVE':1,'P1_VERIFY':1,'P0_CHEAP_TRIAGE':1})
        self.assertEqual(q['queue'][0]['candidate_id'],'c3')
        self.assertEqual(q['queue'][1]['candidate_id'],'c2')

    def test_negative_triage_requires_evidence(self):
        schema=json.loads((ROOT/'schemas/snapshot_candidate_triage.schema.json').read_text())
        row={'candidate_id':'c1','repo_id':'r1','snapshot_id':'s1','decision':'confirmed_not_affected',
            'basis':'This is a documented detailed reason','evidence_urls':[],
            'review_method':'trusted_range_with_branch','checked_at':'2026-10-22T00:00:00Z'}
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(row)))
        row['evidence_urls']=['https://github.com/example/security-advisory']
        self.assertFalse(list(Draft202012Validator(schema).iter_errors(row)))

    def test_upgrade_preserves_legacy_and_resets_coverage(self):
        src=self.root/'v03';dst=self.root/'v031';d=src/'data';d.mkdir(parents=True)
        (src/'manifest.json').write_text(json.dumps({'dataset_version':'0.3.0','status':'release','evaluation_policy':'one_frozen_snapshot_per_repository'}))
        cov=[{'repo_id':'r1','outcome':'PASS_KNOWN_SWEEP','scope':{'start_date':'2020-01-01'}}]
        emit(d/'discovery_coverage.jsonl',cov)
        emit(d/'candidates.jsonl',[{'candidate_id':'c1','repo_id':'r1'}])
        oldbytes=(d/'candidates.jsonl').read_bytes()
        cmd=[sys.executable,str(ROOT/'scripts/upgrade_v03_to_v031.py'),'--source',str(src),'--out',str(dst),'--apply']
        r=subprocess.run(cmd,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertEqual((d/'candidates.jsonl').read_bytes(),oldbytes)
        self.assertEqual((dst/'data'/'candidates.jsonl').read_bytes(),oldbytes)
        self.assertEqual(json.loads((dst/'manifest.json').read_text())['status'],'draft')
        self.assertEqual(json.loads((dst/'manifest.json').read_text())['dataset_version'],'0.3.1')
        upgraded=[json.loads(x) for x in (dst/'data'/'discovery_coverage.jsonl').read_text().splitlines()]
        self.assertEqual(upgraded[0]['outcome'],'NEEDS_REVIEW')
        archived=[json.loads(x) for x in (dst/'data'/'legacy_discovery_coverage_v03.jsonl').read_text().splitlines()]
        self.assertEqual(archived,cov)
        self.assertEqual((dst/'data'/'snapshot_candidate_triage.jsonl').read_text(),'')
        self.assertFalse(dst.exists() and (src/'data'/'snapshot_candidate_triage.jsonl').exists())

    def test_cost_report_never_assumes_missing_cost_zero_total(self):
        path=self.root/'usage.jsonl'
        emit(path,[{'stage':'version','model':'cheap','cost_cny':.1,'input_tokens':100},
                   {'stage':'code','model':'strong','cost_cny':.4,'output_tokens':50},
                   {'stage':'code','model':'strong','input_tokens':30}])
        res=report(path,100)
        self.assertAlmostEqual(res['measured_spend_cny'],.5)
        self.assertEqual(res['calls_without_cost'],1)
        self.assertIn('DO NOT ASSUME ZERO',res['untracked_historical_spend_cny'])

if __name__=='__main__':unittest.main()
