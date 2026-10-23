#!/usr/bin/env python3
"""Summarize actual model usage ledger. Does not intercept provider calls."""
import argparse,collections,json
from pathlib import Path

def report(path,budget):
    costs=collections.defaultdict(float);tokens=collections.Counter();rows=0;missing=0
    for n,l in enumerate(path.read_text(encoding="utf8").splitlines(),1):
        if not l.strip():continue
        r=json.loads(l);rows+=1
        if "cost_cny" not in r:missing+=1;continue
        c=float(r["cost_cny"])
        if c<0:raise ValueError(f"line {n}: negative cost")
        costs[(r.get("stage","unknown"),r.get("model","unknown"))]+=c
        for k in ("input_tokens","output_tokens","cached_input_tokens"):
            tokens[k]+=int(r.get(k,0))
    spent=round(sum(costs.values()),4)
    return {"calls":rows,"calls_without_cost":missing,"cost_by_stage_and_model":[{"stage":s,"model":m,"cost_cny":round(v,4)} for (s,m),v in sorted(costs.items())],"measured_spend_cny":spent,"untracked_historical_spend_cny": "DO NOT ASSUME ZERO", "total_budget_cny":budget,"tracked_remaining_cny":round(budget-spent,4) if budget is not None else None,"tokens":dict(tokens),"warning":"Cannot claim total or enforce budget until all provider calls are instrumented."}

def main():
    p=argparse.ArgumentParser();p.add_argument("ledger",type=Path);p.add_argument("--budget-cny",type=float);p.add_argument("--out",type=Path);a=p.parse_args()
    result=report(a.ledger,a.budget_cny);out=json.dumps(result,ensure_ascii=False,indent=2);print(out)
    if a.out:a.out.write_text(out+"\n",encoding="utf8")
if __name__=="__main__":main()
