"""Minimal ASGI driver so the security middleware is tested without any web framework."""

from __future__ import annotations

import asyncio
import json
from typing import Any


class Recorder:
    def __init__(self) -> None:
        self.called = False

    async def app(self, scope: Any, receive: Any, send: Any) -> None:
        self.called = True
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"{}"})


def request(
    mw: Any, path: str = "/x", method: str = "GET", headers: dict[str, str] | None = None
) -> tuple[int, dict[str, str], Any]:
    hdrs = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    scope = {"type": "http", "method": method, "path": path, "headers": hdrs}
    sent: list[dict[str, Any]] = []

    async def receive() -> dict[str, Any]:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(m: dict[str, Any]) -> None:
        sent.append(m)

    asyncio.run(mw(scope, receive, send))
    start = next(m for m in sent if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    hdr = {k.decode(): v.decode() for k, v in start["headers"]}
    return start["status"], hdr, json.loads(body) if body else None
