"""Webhook signature verification (HMAC-SHA256 over '<t>.<body>')."""
from __future__ import annotations

import hashlib
import hmac
import time
from typing import Optional

from .models import Event

SIGNATURE_HEADER = "WirePayment-Signature"
DEFAULT_TOLERANCE = 300


class SignatureVerificationError(Exception):
    """Raised when a webhook signature does not verify."""


class Webhooks:
    """Verifies inbound webhook signatures."""

    def verify(self, payload: bytes, header: str, secret: str, tolerance: int = DEFAULT_TOLERANCE) -> Event:
        """Verify a webhook and return the parsed Event. `payload` is the raw body bytes."""
        return self.verify_at(payload, header, secret, tolerance=tolerance, now=int(time.time()))

    def verify_at(self, payload: bytes, header: str, secret: str, *, tolerance: int, now: int) -> Event:
        ts, v1 = _parse(header)
        if ts is None or not v1:
            raise SignatureVerificationError("malformed signature header")
        if abs(now - ts) > tolerance:
            raise SignatureVerificationError("timestamp outside tolerance")
        expected = hmac.new(secret.encode(), f"{ts}.".encode() + payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, v1):
            raise SignatureVerificationError("signature mismatch")
        import json

        return Event.from_dict(json.loads(payload))


def _parse(header: str):
    ts: Optional[int] = None
    v1: Optional[str] = None
    for part in header.split(","):
        k, _, val = part.strip().partition("=")
        if k == "t":
            try:
                ts = int(val)
            except ValueError:
                return None, None
        elif k == "v1":
            v1 = val
    return ts, v1
