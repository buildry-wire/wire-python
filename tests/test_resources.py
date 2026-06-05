import unittest

from wire import Client
from tests.server import start


class TestResources(unittest.TestCase):
    def _client(self, handler):
        self.srv, url = start(handler)
        self.addCleanup(self.srv.shutdown)
        return Client("sk_test_123", base_url=url, backoff=0.001)

    def test_create_payment_intent(self):
        def h(method, path, headers, body):
            assert method == "POST" and path == "/v1/payment_intents", (method, path)
            return 200, {"id": "pi_1", "object": "payment_intent", "amount": 50000, "status": "requires_payment_method"}

        c = self._client(h)
        pi = c.payment_intents.create(amount=50000, currency="MNT")
        self.assertEqual(pi.id, "pi_1")
        self.assertEqual(pi.status, "requires_payment_method")

    def test_list_auto_paginates(self):
        def h(method, path, headers, body):
            if "starting_after" not in path:
                return 200, {"object": "list", "has_more": True, "data": [{"id": "ch_1", "object": "charge"}]}
            return 200, {"object": "list", "has_more": False, "data": [{"id": "ch_2", "object": "charge"}]}

        c = self._client(h)
        ids = [ch.id for ch in c.charges.list(limit=1)]
        self.assertEqual(ids, ["ch_1", "ch_2"])

    def test_delete_webhook_endpoint(self):
        def h(method, path, headers, body):
            return 200, {"id": "we_1", "object": "webhook_endpoint", "deleted": True}

        c = self._client(h)
        d = c.webhook_endpoints.delete("we_1")
        self.assertTrue(d.deleted)


if __name__ == "__main__":
    unittest.main()
