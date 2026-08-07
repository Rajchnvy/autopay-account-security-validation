# Expected subrun outcomes

The following are expected to fail the secure expectation and thereby demonstrate the modeled weakness: identity binding, duplicate identity, consent enforcement, data reconciliation, deletion propagation, stale overwrite, money precision, audit deduplication, rate-limit replicas, login counter race, retry amplification, backlog growth, shared DB blast radius and recovery reconciliation.

The following should pass because the detection/validation control is intentionally modeled as active: bulk-access detection. `model_input_quality` is expected to fail until invalid feature vectors are rejected.

Unexpected changes to these outcomes require review because they may indicate either a control improvement or a broken proof harness.
