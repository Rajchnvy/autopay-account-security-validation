#!/usr/bin/env python3
"""Generate deterministic synthetic Autopay-like data for isolated security tests."""
from __future__ import annotations
import argparse, json, random
from datetime import datetime, timedelta, timezone
from pathlib import Path

MERCHANTS=["Orange Polska","Allegro","Netflix","Spotify","mBank","PGE","Play","LOT"]
CURRENCIES=["PLN","EUR","USD"]

def build(seed:int, customers:int, tx_per_customer:int)->dict:
    rng=random.Random(seed)
    now=datetime(2026,8,1,tzinfo=timezone.utc)
    users=[]; tx=[]; consents=[]; audits=[]
    for i in range(customers):
        cid=f"CUST-{i+1:05d}"
        email=f"customer{i+1:05d}@example.test"
        users.append({"customer_id":cid,"email":email,"status":"active","verified":False if i==0 else True,"role":"customer"})
        consents.append({"customer_id":cid,"purpose":"account_view","version":"v1","granted":i%7!=0,"withdrawn_at":None if i%7 else (now-timedelta(days=2)).isoformat()})
        for j in range(tx_per_customer):
            amount=round(rng.uniform(1,2500),2)
            if j==0 and i==0: amount=0.1
            tx.append({
                "transaction_id":f"TX-{i+1:05d}-{j+1:04d}","customer_id":cid,"email":email,
                "merchant":rng.choice(MERCHANTS),"amount":amount,"currency":rng.choice(CURRENCIES),
                "booked_at":(now-timedelta(minutes=rng.randint(0,200000))).isoformat(),
                "source_version":rng.randint(1,5),"deleted":False
            })
        audits.append({"event_id":f"AUD-{i+1:05d}","customer_id":cid,"action":"view","actor":email,"timestamp":now.isoformat()})
    # deliberate anomalies for data-quality and abuse proofs
    tx.append(dict(tx[0]))  # duplicate
    stale=dict(tx[1]); stale["source_version"]=0; stale["transaction_id"]="TX-STALE-0001"; tx.append(stale)
    tx[2]["deleted"]=True
    users.append({"customer_id":"CUST-DUP-EMAIL","email":users[0]["email"],"status":"active","verified":False,"role":"customer"})
    return {"meta":{"synthetic":True,"seed":seed,"customers":customers,"tx_per_customer":tx_per_customer},"users":users,"transactions":tx,"consents":consents,"audit_events":audits}

def main()->None:
    p=argparse.ArgumentParser(); p.add_argument("--seed",type=int,default=42); p.add_argument("--customers",type=int,default=250); p.add_argument("--transactions",type=int,default=40); p.add_argument("--out",default="artifacts/mock_data.json")
    a=p.parse_args(); data=build(a.seed,a.customers,a.transactions)
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(data,indent=2),encoding="utf-8")
    print(json.dumps({"generated":True,"path":str(out),"users":len(data["users"]),"transactions":len(data["transactions"]),"synthetic":True},indent=2))
if __name__=="__main__": main()
