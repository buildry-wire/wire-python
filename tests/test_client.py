import unittest

from wire import Client


class TestClient(unittest.TestCase):
    def _client(self, handler, **kw):
        from tests.server import start

        self.srv, url = start(handler)
        self.addCleanup(self.srv.shutdown)
        return Client("sk_test_123", base_url=url, backoff=0.001, **kw)

    def test_auth_and_decode(self):
        seen = {}

        def h(method, path, headers, body):
            seen["auth"] = headers.get("Authorization")
            return 200, {"id": "pi_1", "object": "payment_intent", "amount": 50000}

        c = self._client(h)
        pi = c.payment_intents.retrieve("pi_1")
        self.assertEqual(seen["auth"], "Bearer sk_test_123")
        self.assertEqual(pi.id, "pi_1")
        self.assertEqual(pi.amount, 50000)

    def test_retries_on_503(self):
        calls = {"n": 0}

        def h(method, path, headers, body):
            calls["n"] += 1
            if calls["n"] < 3:
                return 503, {}
            return 200, {"id": "pi_1", "object": "payment_intent"}

        c = self._client(h, max_retries=3)
        c.payment_intents.retrieve("pi_1")
        self.assertEqual(calls["n"], 3)

    def test_no_retry_on_400(self):
        calls = {"n": 0}

        def h(method, path, headers, body):
            calls["n"] += 1
            return 400, {"error": {"type": "invalid_request_error", "message": "bad"}}

        from wire import WireError

        c = self._client(h, max_retries=3)
        with self.assertRaises(WireError):
            c.payment_intents.retrieve("x")
        self.assertEqual(calls["n"], 1)

    def test_idempotency_key_on_post(self):
        seen = {}

        def h(method, path, headers, body):
            seen["key"] = headers.get("Idempotency-Key")
            return 200, {"id": "pi_1", "object": "payment_intent"}

        c = self._client(h)
        c.payment_intents.create(amount=1)
        self.assertTrue(seen["key"])


if __name__ == "__main__":
    unittest.main()
