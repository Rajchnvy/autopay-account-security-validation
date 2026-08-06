# 300-Control Proof Ledger

This repository does **not** claim 300 exploitable vulnerabilities. It records 300 production-readiness controls and assigns the proof required for each.

## Current evidence state

| State | Count |
|---|---:|
| Fixed in source; deployed/retest evidence required | 11 |
| Partial evidence | 75 |
| Missing or unsubstantiated | 214 |
| **Total** | **300** |

## Proof-method allocation

| Proof method | Count | Meaning |
|---|---:|---|
| Source/static review | 80 | Exact code/configuration path, assertion and review |
| Deterministic simulation | 21 | Concurrency/correctness property without a live target |
| Runtime integration | 45 | Isolated deployed services and controlled requests/network evidence |
| Performance/chaos | 54 | Production-like staging, load/failure injection and retained metrics |
| Governance/documentary | 96 | Signed policy, ownership, legal/privacy or operational evidence |
| Independent assurance | 4 | Independent reviewer or exercise |
| **Total** | **300** | |

## What CI proves

The workflow regenerates the complete catalogue and verifies that controls 1 through 300 exist exactly once and each has a priority, status, proof class and evidence state. It then executes 14 safe deterministic simulations and publishes both the generated ledger and machine-readable results as a GitHub Actions artefact.

## What CI cannot prove without the relevant environment

It cannot manufacture WAF, TLS/mTLS, real network isolation, production-like capacity, backup/restore, RTO/RPO, disaster recovery, legal/privacy approval, operational ownership or an independent penetration test. Those controls remain red until their assigned evidence is attached and reviewed.

## Acceptance rule

A control becomes green only with implementation/configuration, an executed procedure, retained result, accountable owner and approval or independent retest where required.
