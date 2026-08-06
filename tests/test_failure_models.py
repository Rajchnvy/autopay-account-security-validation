import unittest

class FailureModels(unittest.TestCase):
    def test_single_database_failure_impacts_all_workloads(self):
        workloads = {'identity','transactions','ingestion','coupons','financing','audit'}
        mongo_available = False
        availability = {w: mongo_available for w in workloads}
        self.assertTrue(all(v is False for v in availability.values()))

    def test_retry_amplification(self):
        clients=3
        gateway_retries=2
        service_retries=2
        downstream_attempts=clients*gateway_retries*service_retries
        self.assertEqual(downstream_attempts, 12)

    def test_outbox_at_least_once_can_duplicate_without_dedup(self):
        event='evt-1'
        delivered=[]
        delivered.append(event)
        delivered.append(event)
        self.assertEqual(delivered.count(event),2)

if __name__ == '__main__':
    unittest.main()
