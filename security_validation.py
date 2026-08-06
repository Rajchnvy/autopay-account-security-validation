#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, hashlib
from pathlib import Path

class Finding:
    def __init__(self, id, severity, title, path, lines, evidence, consequence):
        self.id=id; self.severity=severity; self.title=title; self.path=path; self.lines=lines; self.evidence=evidence; self.consequence=consequence
    def asdict(self): return self.__dict__

def read(root, rel):
    return (root/rel).read_text(encoding='utf-8', errors='replace').splitlines()

def locate(lines, pattern):
    rx=re.compile(pattern)
    return [i+1 for i,l in enumerate(lines) if rx.search(l)]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('target', type=Path)
    ap.add_argument('--json', type=Path)
    a=ap.parse_args(); root=a.target
    checks=[]
    def add(id,sev,title,rel,pattern,evidence,consequence):
        hits=locate(read(root,rel),pattern)
        if hits: checks.append(Finding(id,sev,title,rel,hits,evidence,consequence))

    add('P0-ID-001','CRITICAL','Registration issues a customer session without email ownership proof','services/identity/src/service.ts',r'const token = await this\.issueSession\(email, "customer"\)','register() creates the account and immediately issues a session; no activation-token or verified-email step exists in the registration flow.','A person can claim another customer email and obtain a session scoped to that email.')
    add('P0-ID-002','CRITICAL','Email is the account primary key and security binding','services/identity/src/service.ts',r'_id: email','The account document uses normalized email as _id and the issued session stores the same email.','Mutable/shared/recycled email addresses can cause incorrect customer-to-record binding.')
    add('P0-SEC-001','CRITICAL','Production database URI can be stored in a local plaintext file','services/ingestion-worker/src/secretAdapter.ts',r'writeFileSync\(this\.path, JSON\.stringify\(\{ uri \}\)','FileSecretStore writes {uri} as JSON. File mode 0600 reduces local read access but does not encrypt the credential.','Host, backup, support-bundle or process compromise can disclose production credentials.')
    add('P0-SEC-002','CRITICAL','Insecure file secret backend is the default','docker-compose.yml',r'PROD_SECRET_BACKEND=\$\{PROD_SECRET_BACKEND:-file\}','Compose defaults production-secret storage to file unless explicitly overridden.','A production-like deployment can silently inherit plaintext secret storage.')
    add('P0-NET-001','CRITICAL','Internal service traffic is plaintext HTTP','docker-compose.yml',r'=http://','Identity, transactions, scoring, audit and ingestion URLs use http:// inside the service network.','A compromised host/container network can observe tokens, identity headers and customer data.')
    add('P0-DB-001','CRITICAL','MongoDB transport is plaintext and unauthenticated','docker-compose.yml',r'LOCAL_URI=mongodb://mongo:27017','Every Node workload uses mongodb://mongo:27017 without credentials or TLS parameters.','Any process with network reach can read or modify application, session and audit data.')
    add('P1-AUTH-001','HIGH','One shared static token authenticates all internal services','docker-compose.yml',r'INTERNAL_TOKEN=\$\{INTERNAL_TOKEN\}','The same environment variable is injected into gateway, identity, transactions, ingestion, coupons, financing, audit and scoring.','Compromise of one workload permits lateral impersonation across internal APIs.')
    add('P1-RATE-001','HIGH','Rate limiting has process-local default state','services/gateway/src/app.ts',r'rateLimit\(','express-rate-limit is instantiated without evidence of a distributed store.','Limits multiply across replicas and reset on process restart.')
    add('P1-BUILD-001','HIGH','Build falls back from frozen to mutable dependency resolution','Dockerfile.node',r'--frozen-lockfile\s*\|\|\s*pnpm install','The image build continues with a non-frozen install when lock enforcement fails.','The deployed dependency graph can differ from the reviewed lockfile.')
    add('P1-SUPPLY-001','HIGH','Mutable container tags are used','docker-compose.yml',r'image: mongo:7','The Mongo image is referenced by a mutable major tag rather than digest.','Identical source may produce different runtime contents and vulnerability exposure.')
    add('P1-PRIV-001','HIGH','Seeded privileged password may be emitted to logs','services/identity/src/service.ts',r'HASŁO WYGENEROWANE','When no env password is supplied, the generated admin/staff password is embedded in a log message.','Privileged credentials can persist in centralized logs, tickets or exports.')
    add('P1-SESSION-001','HIGH','Session tokens appear stored as bearer-token document IDs','services/identity/src/service.ts',r'const s: Session = \{ _id: token','The raw session token is assigned to Mongo _id; no hashing is shown before storage.','Database disclosure can expose immediately usable live sessions.')

    out={'target':str(root),'target_tree_sha256':hashlib.sha256('\n'.join(sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())).encode()).hexdigest(),'findings':[f.asdict() for f in checks]}
    if a.json: a.json.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out,indent=2))
    return 1 if any(f.severity=='CRITICAL' for f in checks) else 0

if __name__=='__main__':
    raise SystemExit(main())
