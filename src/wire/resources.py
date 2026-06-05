"""Resource services. Thin wrappers over Client._request."""
from __future__ import annotations

from typing import Dict, List, Optional
from urllib.parse import quote

from .models import Charge, Deleted, Event, PaymentIntent, WebhookEndpoint
from .pagination import ListIterator


class PaymentIntents:
    def __init__(self, client):
        self._c = client

    def create(
        self,
        *,
        amount: int,
        currency: Optional[str] = None,
        automatic_operator: Optional[bool] = None,
        allowed_operators: Optional[List[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        idempotency_key: Optional[str] = None,
    ) -> PaymentIntent:
        body = {"amount": amount}
        if currency is not None:
            body["currency"] = currency
        if automatic_operator is not None:
            body["automatic_operator"] = automatic_operator
        if allowed_operators is not None:
            body["allowed_operators"] = allowed_operators
        if metadata is not None:
            body["metadata"] = metadata
        d = self._c._request("POST", "/v1/payment_intents", body=body, idempotency_key=idempotency_key)
        return PaymentIntent.from_dict(d)

    def retrieve(self, id: str) -> PaymentIntent:
        d = self._c._request("GET", f"/v1/payment_intents/{quote(id)}")
        return PaymentIntent.from_dict(d)

    def confirm(self, id: str, *, return_url: Optional[str] = None, idempotency_key: Optional[str] = None) -> PaymentIntent:
        body = {}
        if return_url is not None:
            body["return_url"] = return_url
        d = self._c._request("POST", f"/v1/payment_intents/{quote(id)}/confirm", body=body, idempotency_key=idempotency_key)
        return PaymentIntent.from_dict(d)

    def cancel(self, id: str) -> PaymentIntent:
        d = self._c._request("POST", f"/v1/payment_intents/{quote(id)}/cancel", body={})
        return PaymentIntent.from_dict(d)

    def list(self, *, limit: int = 0, starting_after: str = "") -> ListIterator:
        def fetch(after, lim):
            d = self._c._request("GET", "/v1/payment_intents", query={"limit": lim, "starting_after": after})
            return [PaymentIntent.from_dict(x) for x in d.get("data", [])], bool(d.get("has_more"))

        it = ListIterator(fetch, lambda p: p.id, limit)
        it._after = starting_after
        return it


class Charges:
    def __init__(self, client):
        self._c = client

    def retrieve(self, id: str) -> Charge:
        d = self._c._request("GET", f"/v1/charges/{quote(id)}")
        return Charge.from_dict(d)

    def list(self, *, limit: int = 0, starting_after: str = "") -> ListIterator:
        def fetch(after, lim):
            d = self._c._request("GET", "/v1/charges", query={"limit": lim, "starting_after": after})
            return [Charge.from_dict(x) for x in d.get("data", [])], bool(d.get("has_more"))

        it = ListIterator(fetch, lambda ch: ch.id, limit)
        it._after = starting_after
        return it


class Events:
    def __init__(self, client):
        self._c = client

    def retrieve(self, id: str) -> Event:
        d = self._c._request("GET", f"/v1/events/{quote(id)}")
        return Event.from_dict(d)

    def list(self, *, limit: int = 0, starting_after: str = "") -> ListIterator:
        def fetch(after, lim):
            d = self._c._request("GET", "/v1/events", query={"limit": lim, "starting_after": after})
            return [Event.from_dict(x) for x in d.get("data", [])], bool(d.get("has_more"))

        it = ListIterator(fetch, lambda e: e.id, limit)
        it._after = starting_after
        return it


class WebhookEndpoints:
    def __init__(self, client):
        self._c = client

    def create(self, *, url: str, enabled_events: Optional[List[str]] = None, idempotency_key: Optional[str] = None) -> WebhookEndpoint:
        body = {"url": url}
        if enabled_events is not None:
            body["enabled_events"] = enabled_events
        d = self._c._request("POST", "/v1/webhook_endpoints", body=body, idempotency_key=idempotency_key)
        return WebhookEndpoint.from_dict(d)

    def retrieve(self, id: str) -> WebhookEndpoint:
        d = self._c._request("GET", f"/v1/webhook_endpoints/{quote(id)}")
        return WebhookEndpoint.from_dict(d)

    def update(self, id: str, *, url: Optional[str] = None, enabled_events: Optional[List[str]] = None,
               status: Optional[str] = None, idempotency_key: Optional[str] = None) -> WebhookEndpoint:
        body = {}
        if url is not None:
            body["url"] = url
        if enabled_events is not None:
            body["enabled_events"] = enabled_events
        if status is not None:
            body["status"] = status
        d = self._c._request("POST", f"/v1/webhook_endpoints/{quote(id)}", body=body, idempotency_key=idempotency_key)
        return WebhookEndpoint.from_dict(d)

    def delete(self, id: str) -> Deleted:
        d = self._c._request("DELETE", f"/v1/webhook_endpoints/{quote(id)}")
        return Deleted.from_dict(d)

    def list(self, *, limit: int = 0, starting_after: str = "") -> ListIterator:
        def fetch(after, lim):
            d = self._c._request("GET", "/v1/webhook_endpoints", query={"limit": lim, "starting_after": after})
            return [WebhookEndpoint.from_dict(x) for x in d.get("data", [])], bool(d.get("has_more"))

        it = ListIterator(fetch, lambda w: w.id, limit)
        it._after = starting_after
        return it
