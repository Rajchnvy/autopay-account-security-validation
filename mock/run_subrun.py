#!/usr/bin/env python3
"""Execute one isolated synthetic-data proof scenario and emit machine-readable evidence."""
from __future__ import annotations
import argparse, json, math, random
from collections import Counter
from pathlib import Path

SCENARIOS={
 "identity_binding","duplicate_identity","consent_enforcement","data_reconciliation",
 "deletion_propagation","stale_overwrite","money_precision","audit_deduplication",
 "rate_limit_replicas","login_counter_race","retry_amplification","backlog_growth",
 "bulk_access_detection","shared_db_blast_radius","recovery_reconciliation","model_input_quality"
}

def load(path:str)->dict: return json.loads(Path(path).read_text(encoding="utf-8"))
def result(name:str,passed:bool,expected,actual,evidence:list[str],classification="simulation-proven")->dict:
    return {"scenario":name,"passed":passed,"expected":expected,"actual":actual,"classification":classification,"evidence":evidence}

def run(name:str,d:dict)->dict:
    users=d["users"]; tx=d["transactions"]; cons=d["consents"]; audits=d["audit_events"]
    if name=="identity_binding":
        victim=users[0]; session_issued=not victim["verified"]
        return result(name, not session_issued, "no session before verified immutable identity", {"verified":victim["verified"],"session_modelled_as_issued":session_issued}, ["first synthetic account is deliberately unverified"])
    if name=="duplicate_identity":
        c=Counter(u["email"] for u in users); dup={k:v for k,v in c.items() if v>1}
        return result(name, not dup, "one immutable customer identity per contact address", dup,["generator deliberately creates duplicate email ownership"])
    if name=="consent_enforcement":
        withdrawn={c["customer_id"] for c in cons if not c["granted"] or c["withdrawn_at"]}; exposed=sum(1 for t in tx if t["customer_id"] in withdrawn)
        return result(name, exposed==0,"zero processing records after withdrawal",exposed,[f"withdrawn customer IDs: {len(withdrawn)}"])
    if name=="data_reconciliation":
        ids=[t["transaction_id"] for t in tx]; dup=sum(v-1 for v in Counter(ids).values() if v>1)
        return result(name,dup==0,"no duplicate business records",dup,[f"rows={len(ids)} unique={len(set(ids))}"])
    if name=="deletion_propagation":
        visible=[t for t in tx if t.get("deleted")]
        return result(name,len(visible)==0,"deleted source records absent from projection",len(visible),["synthetic source includes a tombstoned record"])
    if name=="stale_overwrite":
        current=5; incoming=0; accepted=incoming<current
        return result(name,not accepted,"older source version rejected",{"current":current,"incoming":incoming,"accepted":accepted},["models missing monotonic-version guard"])
    if name=="money_precision":
        actual=0.1+0.2
        return result(name,actual==0.3,"exact decimal 0.3",repr(actual),["binary float demonstration"])
    if name=="audit_deduplication":
        delivered=[audits[0]["event_id"],audits[0]["event_id"]]; unique=len(set(delivered))
        return result(name,len(delivered)==unique,"one immutable audit event per event_id",{"deliveries":len(delivered),"unique":unique},["at-least-once delivery without receiver dedup"])
    if name=="rate_limit_replicas":
        local_limit=5; replicas=8; accepted=local_limit*replicas
        return result(name,accepted==local_limit,"global allowance remains configured limit",accepted,[f"{local_limit} x {replicas} process-local counters"])
    if name=="login_counter_race":
        start=0; a=start+1; b=start+1; persisted=b
        return result(name,persisted==2,"two concurrent failures persist as 2",persisted,["read-modify-write lost update"])
    if name=="retry_amplification":
        calls=3*2*2
        return result(name,calls<=3,"bounded end-to-end retry budget <=3",calls,["client x gateway x service retries"])
    if name=="backlog_growth":
        arrival=100; service=60; seconds=30; backlog=(arrival-service)*seconds
        return result(name,backlog==0,"stable queue with no unbounded growth",backlog,["arrival exceeds service rate"])
    if name=="bulk_access_detection":
        actor="staff@example.test"; accesses=[{"actor":actor,"customer_id":u["customer_id"]} for u in users[:120]]; threshold=50; detected=len(accesses)>threshold
        return result(name,detected,"bulk customer access detected and flagged",{"accesses":len(accesses),"threshold":threshold,"detected":detected},["synthetic staff scans 120 customers"])
    if name=="shared_db_blast_radius":
        services=["identity","transactions","ingestion","coupons","financing","audit"]
        return result(name,len(services)==1,"single DB failure affects one bounded workload",len(services),[",".join(services)])
    if name=="recovery_reconciliation":
        before={t["transaction_id"] for t in tx}; restored=set(list(before)[:-3]); missing=before-restored
        return result(name,not missing,"restore reconciles all business records",len(missing),["synthetic restore intentionally omits three records"])
    if name=="model_input_quality":
        sample={"amount":None,"currency":"XXX","days_since_last":-4}; valid=sample["amount"] is not None and sample["currency"] in {"PLN","EUR","USD"} and sample["days_since_last"]>=0
        return result(name,valid,"invalid or missing features rejected",sample,["malformed scoring feature vector"])
    raise ValueError(name)

def main()->None:
    p=argparse.ArgumentParser(); p.add_argument("scenario",choices=sorted(SCENARIOS)); p.add_argument("--data",default="artifacts/mock_data.json"); p.add_argument("--out-dir",default="artifacts/subruns")
    a=p.parse_args(); r=run(a.scenario,load(a.data)); out=Path(a.out_dir); out.mkdir(parents=True,exist_ok=True); (out/f"{a.scenario}.json").write_text(json.dumps(r,indent=2),encoding="utf-8"); print(json.dumps(r,indent=2))
    # A failed secure expectation is evidence of a weakness, so the runner exits zero and records passed=false.
if __name__=="__main__": main()
