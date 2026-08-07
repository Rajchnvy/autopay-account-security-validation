#!/usr/bin/env python3
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

files=sorted(Path("artifacts/subruns").glob("*.json"))
rows=[json.loads(p.read_text(encoding="utf-8")) for p in files]
summary={
  "subruns":len(rows),
  "secure_expectation_passed":sum(1 for r in rows if r["passed"]),
  "weakness_demonstrated":sum(1 for r in rows if not r["passed"]),
  "classifications":dict(Counter(r["classification"] for r in rows)),
  "results":rows,
}
Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/mock_subrun_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
md=["# Mock-data subrun evidence","",f"- Subruns: **{summary['subruns']}**",f"- Secure expectations passed: **{summary['secure_expectation_passed']}**",f"- Weaknesses demonstrated: **{summary['weakness_demonstrated']}**","","| Scenario | Secure expectation | Result |","|---|---|---|"]
for r in rows: md.append(f"| `{r['scenario']}` | {'PASS' if r['passed'] else 'FAIL'} | `{str(r['actual'])[:120]}` |")
Path("artifacts/MOCK_SUBRUN_SUMMARY.md").write_text("\n".join(md)+"\n",encoding="utf-8")
print(json.dumps(summary,indent=2))
