# Mock subrun to control mapping

| Subrun | Primary control areas |
|---|---|
| identity_binding | 29, 30, 208 |
| duplicate_identity | 30, 208 |
| consent_enforcement | 79, 214, 216, 218 |
| data_reconciliation | 73, 85, 209 |
| deletion_propagation | 75, 211, 219 |
| stale_overwrite | 71, 72, 193, 213 |
| money_precision | 78, 212 |
| audit_deduplication | 144, 194, 201 |
| rate_limit_replicas | 33, 42, 190, 202 |
| login_counter_race | 33, 191 |
| retry_amplification | 43, 46, 124, 125 |
| backlog_growth | 126, 194, 195, 205 |
| bulk_access_detection | 147, 199, 217 |
| shared_db_blast_radius | 5, 68, 69, 103 |
| recovery_reconciliation | 130, 131, 133 |
| model_input_quality | 70, 79, 218, 223, 224 |

A simulation demonstrates a design property under controlled assumptions. Controls remain red until source/runtime evidence confirms the assumptions and an authorized retest passes in the target environment.
