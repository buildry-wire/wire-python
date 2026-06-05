"""Typed Wire API error and envelope parsing."""
from __future__ import annotations

import json
from typing import Optional


class WireError(Exception):
    """A typed error returned by the Wire API."""

    def __init__(
        self,
        message: str,
        *,
        type: str = "api_error",
        code: Optional[str] = None,
        param: Optional[str] = None,
        request_id: Optional[str] = None,
        doc_url: Optional[str] = None,
        operator_decline_code: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.type = type
        self.code = code
        self.param = param
        self.request_id = request_id
        self.doc_url = doc_url
        self.operator_decline_code = operator_decline_code
        self.status_code = status_code

    def __str__(self) -> str:
        return (
            f"{self.message} (type={self.type}, code={self.code}, "
            f"status={self.status_code}, request_id={self.request_id})"
        )


def parse_error(status: int, body: bytes) -> WireError:
    """Decode the Wire error envelope; fall back to a generic error."""
    try:
        env = json.loads(body)
        e = env["error"]
    except (ValueError, KeyError, TypeError):
        return WireError(
            f"unexpected response (status {status})",
            type="api_error",
            status_code=status,
        )
    return WireError(
        e.get("message", "request failed"),
        type=e.get("type", "api_error"),
        code=e.get("code"),
        param=e.get("param"),
        request_id=e.get("request_id"),
        doc_url=e.get("doc_url"),
        operator_decline_code=e.get("operator_decline_code"),
        status_code=status,
    )
