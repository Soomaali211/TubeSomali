"""Helpers to keep secrets and text out of logs."""

from __future__ import annotations

SENSITIVE_HEADERS = frozenset({"authorization", "cookie", "set-cookie", "proxy-authorization"})


def safe_headers(headers: list[tuple[bytes, bytes]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in headers:
        name = k.decode("latin-1").lower()
        out[name] = "[redacted]" if name in SENSITIVE_HEADERS else v.decode("latin-1")
    return out
