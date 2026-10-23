#!/usr/bin/env python3
"""Read-only evidence fetcher. Never executes upstream repository instructions or PoCs."""
import concurrent.futures, datetime, hashlib, json, pathlib, urllib.request, urllib.error
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[2]
OUT=BASE/'sources'; OUT.mkdir(parents=True,exist_ok=True)
REPOS={'expressjs/express','lodash/lodash'}
def fetch(item):
    key,url=item
    path=OUT/(key+'.json')
    if path.exists():
        raw=path.read_bytes()
        return dict(key=key,url=url,http_status=200,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest(),retrieved_at=datetime.datetime.fromtimestamp(path.stat().st_mtime,datetime.timezone.utc).isoformat(),cache_hit=True)
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'RepoVuln-50-readonly-verification','Accept':'application/vnd.github+json' if 'api.github.com' in url else '*/*'})
        with urllib.request.urlopen(req,timeout=40) as r:
            raw=r.read(); status=r.status
        path.write_bytes(raw)
        return dict(key=key,url=url,http_status=status,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest(),retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    except Exception as e:
        return dict(key=key,url=url,error=str(e),retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
def main():
    jobs=[]
    for repo in sorted(REPOS):
        name=repo.split('/')[0]
        jobs += [(name+'_official_advisories','https://api.github.com/repos/'+repo+'/security-advisories'),(name+'_releases','https://api.github.com/repos/'+repo+'/releases?per_page=100')]
    seen=set()
    jobs += [
        ('lodash_changelog','https://raw.githubusercontent.com/wiki/lodash/lodash/Changelog.md'),
        ('express_6222_comments','https://api.github.com/repos/expressjs/express/issues/6222/comments?per_page=100'),
        ('express_9266_research','https://www.herodevs.com/vulnerability-directory/cve-2024-9266'),
        ('express_10491_research','https://www.herodevs.com/vulnerability-directory/cve-2024-10491'),
        ('CVE-2014-6393_nvd','https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2014-6393'),
        ('CVE-2018-16487_nvd','https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2018-16487'),
        ('CVE-2024-51999_cve','https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2024/51xxx/CVE-2024-51999.json'),
        ('express_npm_registry','https://registry.npmjs.org/express'),
        ('lodash_npm_registry','https://registry.npmjs.org/lodash'),
    ]
    for sha in ['da4d763ff6ba9df6dbd8f1f0b1d05412dda934d5','aac1d52c4fa1ce19e17bb2b4e06669e8756f6816','7e01531e505c5bd081056aab4f4329d76f1b3fc5','f39139c6fec16c01f30fdf535085a6bab1687e13']:
        jobs.append(('expressjs_commit_'+sha,'https://api.github.com/repos/expressjs/express/commits/'+sha))
    for sha in ['1f8ea07746963a535385a5befc19fa687a627d2b','fe8d32eda854377349a4f922ab7655c8e5df9a0b','879aaa93132d78c2f8d20c60279da9f8b21576d6','bbcb8a03deb54e2cd19f2f53e618e1fe194091bb']:
        jobs.append(('lodash_commit_'+sha,'https://api.github.com/repos/lodash/lodash/commits/'+sha))
    for line in (ROOT/'runs/preselection/vulnerability_candidates.jsonl').read_text().splitlines():
        c=json.loads(line)
        if c['repository_full_name'] not in REPOS: continue
        repo=c['repository_full_name']; ghsa=next(x for x in c['source_record_ids'] if x.startswith('GHSA-'))
        jobs.append((ghsa+'_global','https://api.github.com/advisories/'+ghsa))
        for alias in c['aliases']:
            if alias.startswith('CVE-'):
                year=alias.split('-')[1]; num=alias.split('-')[2]; bucket=num[:-3]+'xxx' if len(num)>3 else '0xxx'
                jobs.append((alias+'_cve','https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/'+year+'/'+bucket+'/'+alias+'.json'))
        for url in c['source_urls']:
            if '/commit/' in url and repo in url:
                sha=url.split('/commit/')[1].split('/')[0]
                if (repo,sha) not in seen:
                    jobs.append((repo.split('/')[0]+'_commit_'+sha,'https://api.github.com/repos/'+repo+'/commits/'+sha)); seen.add((repo,sha))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: results=list(ex.map(fetch,jobs))
    with (BASE/'fetch_log.jsonl').open('a') as log:
        log.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in results))
    print(json.dumps({'requests':len(results),'success':sum('error' not in r for r in results),'errors':[r for r in results if 'error'in r]},indent=2))
if __name__=='__main__': main()
