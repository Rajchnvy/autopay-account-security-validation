# Autopay Account Security Validation

This repository contains **sanitized security validation tests and evidence only**.

> The repository is currently public. The proprietary Autopay source package and any credentials must **not** be uploaded here. The tests are designed to run against a locally mounted copy under `target/` or against an explicitly authorized isolated test environment using synthetic data.

## Scope

- static source-code security proofs
- authentication and authorization abuse cases
- secrets and transport configuration checks
- concurrency and race-condition checks
- failure-injection and resilience test plans
- load, spike and soak test harnesses
- evidence mapping to P0-P4 production-readiness findings

## Safety boundary

Do not point these tests at production, customer data, production credentials, or third-party systems. Run only in an isolated environment with synthetic data and written authorization.

## Current status

The initial source package review has already substantiated multiple production blockers, including unverified email-to-customer binding, plaintext-capable secret storage, shared static service credentials, plaintext internal transport, unauthenticated MongoDB, non-reproducible builds, process-local rate limiting, incomplete auditability, and absent production capacity/recovery evidence.
