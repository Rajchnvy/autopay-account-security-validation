#!/usr/bin/env python3
"""Validate the 300-control evidence ledger and run safe deterministic simulations.

This never targets production. Runtime/live tests require an explicitly authorized isolated target.
"""
from __future__ import annotations
import csv, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "evidence" / "controls_300.csv"
RESULTS = ROOT / "evidence" / "validation_results.json"
ALLOWED_PROOF = {"source_static_review","deterministic_simulation","runtime_integration","runtime_performance_chaos","governance_documentary","independent_assurance"}
ALLOWED_STATES = {"fixed_in_source_retest_required","partial_evidence","missing_or_unsubstantiated"}

def load_controls():
    with LEDGER.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def validate_ledger(rows):
    errors=[]; ids=[]
    required=["id","domain","control","priority","status","proof_type","evidence_state"]
    for n,row in enumerate(rows,1):
        for k in required:
            if not row.get(k,"").strip(): errors.append(f"row {n}: missing {k}")
        ids.append(int(row["id"]))
        if row["proof_type"] not in ALLOWED_PROOF: errors.append(f"control {row['id']}: invalid proof type")
        if row["evidence_state"] not in ALLOWED_STATES: errors.append(f"control {row['id']}: invalid evidence state")
    if ids != list(range(1,301)): errors.append("control IDs are not exactly 1..300")
    return errors

def lost_update(initial=0,writers=2):
    snapshots=[initial for _ in range(writers)]; persisted=initial
    for snap in snapshots: persisted=snap+1
    return persisted

def distributed_limit(local_limit,replicas): return local_limit*replicas

def retry_amplification(*layers):
    out=1
    for x in layers: out*=x
    return out

def stale_cache_accepts(revoked_at,cached_until,request_at): return revoked_at <= request_at < cached_until

def duplicate_delivery(immediate,flush,receiver_dedup):
    deliveries=int(immediate)+int(flush)
    return 1 if receiver_dedup and deliveries else deliveries

def stale_overwrite(current_version,incoming_version,version_check):
    if version_check and incoming_version < current_version: return current_version
    return incoming_version

def queue_growth(arrival_rate,service_rate,seconds): return max(0,(arrival_rate-service_rate)*seconds)

def source_load(workers,polls_per_worker,leader_election):
    active=1 if leader_election and workers else workers
    return active*polls_per_worker

def float_money_error(): return (0.1+0.2) != 0.3

def shared_failure_impact(dependants,isolated): return 1 if isolated and dependants else dependants

class DesignSimulations(unittest.TestCase):
    def test_login_counter_lost_update(self): self.assertEqual(lost_update(0,2),1)
    def test_rate_limit_multiplies_per_replica(self): self.assertEqual(distributed_limit(5,8),40)
    def test_retry_amplification(self): self.assertEqual(retry_amplification(3,2,2),12)
    def test_revocation_cache_window(self): self.assertTrue(stale_cache_accepts(100,105,103))
    def test_outbox_duplicate_without_dedup(self): self.assertEqual(duplicate_delivery(True,True,False),2)
    def test_outbox_dedup_control(self): self.assertEqual(duplicate_delivery(True,True,True),1)
    def test_stale_ingestion_overwrite_without_version_check(self): self.assertEqual(stale_overwrite(10,8,False),8)
    def test_version_check_blocks_stale_overwrite(self): self.assertEqual(stale_overwrite(10,8,True),10)
    def test_backlog_grows_without_backpressure(self): self.assertEqual(queue_growth(100,60,30),1200)
    def test_ingestion_source_load_multiplies(self): self.assertEqual(source_load(4,10,False),40)
    def test_leader_election_limits_source_load(self): self.assertEqual(source_load(4,10,True),10)
    def test_binary_float_is_not_exact_money(self): self.assertTrue(float_money_error())
    def test_shared_database_blast_radius(self): self.assertEqual(shared_failure_impact(6,False),6)
    def test_isolated_data_plane_reduces_blast_radius(self): self.assertEqual(shared_failure_impact(6,True),1)

def main():
    rows=load_controls(); errors=validate_ledger(rows)
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(DesignSimulations))
    payload={"controls_total":len(rows),"ledger_errors":errors,"simulations_run":result.testsRun,"simulation_failures":len(result.failures),"simulation_errors":len(result.errors),"note":"Simulations prove design properties only; runtime, performance, governance and independent controls require their assigned evidence."}
    RESULTS.write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2))
    return 0 if not errors and result.wasSuccessful() else 1

if __name__=="__main__": raise SystemExit(main())
