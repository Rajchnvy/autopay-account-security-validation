import unittest

class ConcurrencyProofs(unittest.TestCase):
    def test_read_modify_write_login_counter_loses_updates(self):
        initial = 0
        req_a_read = initial
        req_b_read = initial
        stored = req_a_read + 1
        stored = req_b_read + 1
        self.assertEqual(stored, 1)
        self.assertNotEqual(stored, 2)

    def test_process_local_rate_limit_multiplies_with_replicas(self):
        per_replica_limit = 5
        replicas = 8
        effective_allowed = per_replica_limit * replicas
        self.assertEqual(effective_allowed, 40)
        self.assertGreater(effective_allowed, per_replica_limit)

    def test_local_cache_revocation_window(self):
        cache_ttl_seconds = 5
        revoked_at = 100
        replica_cache_expires = revoked_at + cache_ttl_seconds
        self.assertGreater(replica_cache_expires, revoked_at)

if __name__ == '__main__':
    unittest.main()
