"""Resource dataclasses. Each `from_dict` tolerates unknown/missing fields."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PaymentIntent:
    id: str = ""
    object: str = "payment_intent"
    amount: int = 0
    currency: str = "MNT"
    status: str = ""
    client_secret: str = ""
    automatic_operator: bool = True
    allowed_operators: List[str] = field(default_factory=list)
    selected_operator: Optional[str] = None
    next_action: Optional[dict] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    livemode: bool = False
    created: int = 0
    expires_at: Optional[int] = None

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PaymentIntent":
        return _build(cls, d)


@dataclass
class Charge:
    id: str = ""
    object: str = "charge"
    payment_intent: str = ""
    operator: str = ""
    operator_charge_id: Optional[str] = None
    status: str = ""
    amount: int = 0
    fee: int = 0
    amount_refunded: int = 0
    failure_code: Optional[str] = None
    failure_message: Optional[str] = None
    livemode: bool = False
    created: int = 0

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Charge":
        return _build(cls, d)


@dataclass
class Event:
    id: str = ""
    object: str = "event"
    type: str = ""
    api_version: str = ""
    data: Optional[dict] = None
    livemode: bool = False
    created: int = 0

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Event":
        return _build(cls, d)


@dataclass
class WebhookEndpoint:
    id: str = ""
    object: str = "webhook_endpoint"
    url: str = ""
    enabled_events: List[str] = field(default_factory=list)
    status: str = ""
    secret: Optional[str] = None
    livemode: bool = False
    created: int = 0

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "WebhookEndpoint":
        return _build(cls, d)


@dataclass
class Deleted:
    id: str = ""
    object: str = ""
    deleted: bool = False

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Deleted":
        return _build(cls, d)


def _build(cls, d: Dict[str, Any]):
    """Construct a dataclass from a dict, ignoring unknown keys."""
    names = {f.name for f in cls.__dataclass_fields__.values()}
    return cls(**{k: v for k, v in (d or {}).items() if k in names})
