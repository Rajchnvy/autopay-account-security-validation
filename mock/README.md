# Synthetic mock-data subruns

These tests generate deterministic, fictional Autopay-like records (`example.test`, seed 42) and execute isolated proof scenarios. They do not call production, third parties, real customer systems or Vercel.

Each scenario tests a **secure expectation** and records either `passed: true` or `passed: false`. A false secure expectation is evidence that the mocked design condition produces the predicted weakness; it is not a claim that a live production exploit was executed.

The matrix covers identity binding, duplicate identity, consent enforcement, reconciliation, deletion, stale overwrite, monetary precision, audit duplication, replica rate limits, login races, retry amplification, queue backlog, bulk access detection, shared-database blast radius, recovery reconciliation and scoring-input quality.
