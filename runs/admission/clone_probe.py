#!/usr/bin/env python3
"""Read-only HTTPS Git ref reachability probe. Never checks out or executes source."""
import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, time
ROOT = pathlib.Path(__file__).resolve().parents[2]
def probe(repo):
    target = ROOT / 'runs/admission/raw' / (repo['full_name'].replace('/', '__') + '__clone_probe.json')
    cmd = ['git', '-c', 'credential.helper=', 'ls-remote', '--exit-code', repo['canonical_url'] + '.git', 'HEAD']
    start = time.time()
    env = dict(__import__('os').environ, GIT_TERMINAL_PROMPT='0')
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=35, env=env)
        result = {'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr}
    except Exception as e:
        result = {'returncode': None, 'error': str(e)}
    record = {'tool': 'git_ls_remote_read_only', 'query': {'argv': cmd}, 'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': round(time.time()-start, 3), 'response': result}
    target.write_text(json.dumps(record, ensure_ascii=False) + '\n')
    return repo['full_name'], result['returncode']
repos = [json.loads(l) for l in (ROOT/'runs/preselection/priority_shortlist.jsonl').open()]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    for result in pool.map(probe, repos):
        print(*result, flush=True)
