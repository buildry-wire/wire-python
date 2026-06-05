import unittest

from wire.errors import WireError, parse_error


class TestParseError(unittest.TestCase):
    def test_parses_envelope(self):
        body = (
            b'{"error":{"type":"invalid_request_error","code":"amount_invalid",'
            b'"message":"amount must be positive","param":"amount","request_id":"req_123"}}'
        )
        err = parse_error(400, body)
        self.assertIsInstance(err, WireError)
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.code, "amount_invalid")
        self.assertEqual(err.param, "amount")
        self.assertEqual(err.request_id, "req_123")
        self.assertIn("amount must be positive", str(err))

    def test_fallback_on_non_json(self):
        err = parse_error(500, b"not json")
        self.assertIsInstance(err, WireError)
        self.assertEqual(err.status_code, 500)


if __name__ == "__main__":
    unittest.main()
