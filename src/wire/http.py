"""Client and the low-level request path (auth, idempotency, retries)."""
from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from .errors import WireError, parse_error

DEFAULT_BASE_URL = "https://api.wire.mn"


class Client:
    """A Wire API client. Pass an API key (sk_live_...)."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 2,
        backoff: float = 0.5,
    ) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._backoff = backoff

        # Resource services (imported here to avoid a circular import).
        from .resources import Charges, Events, PaymentIntents, WebhookEndpoints
        from .webhooks import Webhooks

        self.payment_intents = PaymentIntents(self)
        self.charges = Charges(self)
        self.events = Events(self)
        self.webhook_endpoints = WebhookEndpoints(self)
        self.webhooks = Webhooks()

    def _request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[dict] = None,
        query: Optional[Dict[str, Any]] = None,
        idempotency_key: Optional[str] = None,
    ) -> dict:
        url = self._base_url + path
        if query:
            clean = {k: v for k, v in query.items() if v not in (None, "", 0)}
            if clean:
                url += "?" + urllib.parse.urlencode(clean)

        data = json.dumps(body).encode() if body is not None else None
        headers = {"Authorization": f"Bearer {self._api_key}", "Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        if method == "POST":
            headers["Idempotency-Key"] = idempotency_key or _new_idempotency_key()

        attempt = 0
        while True:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                    raw = resp.read()
                    return json.loads(raw) if raw else {}
            except urllib.error.HTTPError as e:
                status = e.code
                raw = e.read()
                if (status == 429 or status >= 500) and attempt < self._max_retries:
                    time.sleep(_retry_after(e.headers.get("Retry-After")) or self._backoff * (2 ** attempt))
                    attempt += 1
                    continue
                raise parse_error(status, raw)
            except urllib.error.URLError as e:
                if attempt < self._max_retries:
                    time.sleep(self._backoff * (2 ** attempt))
                    attempt += 1
                    continue
                raise WireError(f"request failed: {e.reason}", type="api_error")


def _retry_after(value: Optional[str]) -> float:
    if not value:
        return 0.0
    try:
        return float(int(value))
    except ValueError:
        return 0.0


def _new_idempotency_key() -> str:
    return "idk_" + base64.b32encode(os.urandom(16)).decode().rstrip("=").lower()
