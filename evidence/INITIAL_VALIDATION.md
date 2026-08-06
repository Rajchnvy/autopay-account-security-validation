# Initial practical validation evidence

Validation target: isolated copy of `autopay-account-handover-2026-08-05(2).zip` using synthetic/local analysis only.

Target file-tree fingerprint: `8cbd09a7e93edf7fd4053bd0aa5d6b6cdcf210550403cf19ed1f2d386eb646e8`

## Substantiated directly from source

| ID | Severity | Proven condition | Exact source evidence |
|---|---|---|---|
| P0-ID-001 | Critical | Registration creates a session without proving email ownership | `services/identity/src/service.ts:50-73`; session issued at line 72 immediately after account insertion |
| P0-ID-002 | Critical | Email is the identity/account primary key | `services/identity/src/service.ts:50-73`; `_id: email` at line 60 and session uses email |
| P0-SEC-001 | Critical | Production URI is written as plaintext JSON | `services/ingestion-worker/src/secretAdapter.ts:20-32`; `writeFileSync(... JSON.stringify({ uri }))` |
| P0-SEC-002 | Critical | File secret backend is the deployment default | `docker-compose.yml:56`; `${PROD_SECRET_BACKEND:-file}` |
| P0-NET-001 | Critical | Service-to-service traffic uses plaintext HTTP | `docker-compose.yml:33,44-45,62,85,115-121` |
| P0-DB-001 | Critical | MongoDB uses unauthenticated plaintext connection strings | `docker-compose.yml:22,40,52,69,81,92` |
| P1-AUTH-001 | High | One shared static token is injected into every service | `docker-compose.yml:25,43,55,72,84,95,103,113` |
| P1-BUILD-001 | High | Build can ignore frozen lockfile failure | `Dockerfile.node`; `pnpm install --frozen-lockfile || pnpm install` |
| P1-SUPPLY-001 | High | Mutable Mongo image tag | `docker-compose.yml:5`; `mongo:7` |
| P1-PRIV-001 | High | Generated privileged password can be logged | `services/identity/src/service.ts:154-177` |
| P1-SESSION-001 | High | Raw bearer session token is stored as document `_id` | `services/identity/src/service.ts:43-47` |

## Executed simulation proofs

Six deterministic tests were executed successfully:

1. Read-modify-write login failure counting loses a concurrent increment.
2. Process-local rate limits multiply by replica count.
3. Process-local verification cache creates a revocation window.
4. Single shared Mongo failure affects all dependent workloads.
5. Layered retries amplify downstream attempts.
6. At-least-once outbox delivery can duplicate without receiver deduplication.

Execution result:

```text
Ran 6 tests
OK
```

These simulations do not claim a live exploit of a production environment. They demonstrate that the identified algorithms/topology have the stated failure properties.

## What could not yet be executed

The supplied environment could not download pnpm from the public registry, and Docker is unavailable. Therefore the claimed 248 application tests, browser E2E suite, live DAST, container scans, load tests and process-kill experiments have not yet been independently reproduced. These remain unverified claims until GitHub Actions or an authorized runner executes them and retains artifacts.

## Release conclusion

The direct source proofs are sufficient to keep the current decision at **NO-GO** for public/customer-facing production. The most important condition is the unverified email-to-customer binding; infrastructure hardening alone cannot close it.
