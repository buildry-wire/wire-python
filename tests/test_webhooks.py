import json
import pathlib
import unittest

from wire.webhooks import Webhooks

VECTORS = pathlib.Path(__file__).parent / "data" / "webhook-signatures.json"


class TestWebhookVectors(unittest.TestCase):
    def test_vectors(self):
        v = json.loads(VECTORS.read_text())
        w = Webhooks()
        for case in v["cases"]:
            ok = True
            try:
                ev = w.verify_at(
                    case["body"].encode(),
                    case["header"],
                    v["secret"],
                    tolerance=v["tolerance_seconds"],
                    now=v["now"],
                )
            except Exception:
                ok = False
                ev = None
            self.assertEqual(ok, case["valid"], f"case {case['name']}")
            if case["valid"]:
                self.assertTrue(ev and ev.type, f"case {case['name']} should parse event")


if __name__ == "__main__":
    unittest.main()
