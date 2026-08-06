# Proof Execution Runbook

## Safety boundary

Never point these tests at production, real customer data, production credentials or third-party systems. Use only an isolated environment with synthetic data and written authorization.

## CI proof available now

The repository workflow proves:

- exactly 300 controls are catalogued;
- every control has a priority, current state and assigned proof method;
- all 14 deterministic simulations run and retain machine-readable results;
- source/runtime/governance/independent evidence is not incorrectly represented as the same thing.

## Private authorized source runner

Mount the proprietary package under `target/` without committing it to this public repository:

```bash
python security_validation.py --target target
python generate_ledger.py
python validate_300.py
```

## Runtime evidence packs required

1. Identity substitution integration test with synthetic victim records.
2. Direct internal-service call and forged-header test.
3. MongoDB unauthenticated-access and TLS enforcement test.
4. Packet capture proving or disproving plaintext east-west traffic.
5. Multi-replica rate-limit and revocation-consistency test.
6. Load, spike, stress and soak tests with p50/p95/p99, saturation and error-rate evidence.
7. Latency, timeout and retry-storm injection.
8. Container kill/restart, graceful drain and dependency failure tests.
9. Mongo failover, backup restore, measured RTO/RPO and post-recovery reconciliation.
10. Authenticated and unauthenticated DAST.
11. SAST, SCA, secret, container, IaC, licence and SBOM generation.
12. Independent penetration, business-logic abuse and operational takeover exercises.

## Evidence package per control

- control ID and assertion;
- expected secure behaviour;
- test/review procedure;
- exact environment and version;
- raw logs, report, screenshot, trace, packet capture or signed document;
- pass/fail conclusion;
- responsible owner;
- remediation PR/change;
- independent retest or approval where required.

A simulation is evidence of a design property only. It does not turn a runtime, legal, privacy or operational control green.
