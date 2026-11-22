"""Pure-ASGI security middleware: Host allow-list, Origin/CORS allow-list, default-deny auth,
request IDs, error envelope. Does not log headers, bodies or tokens."""

from __future__ import annotations

import json
import uuid
from collections.abc import Awaitable, Callable, MutableMapping
from typing import Any

from app.errors import ErrorCode, envelope
from app.security.tokens import TokenValidator

Scope = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[MutableMapping[str, Any]]]
Send = Callable[[MutableMapping[str, Any]], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]

#: The only routes reachable without a token (ARCHITECTURE §11).
PUBLIC_PATHS = frozenset({"/health", "/pairing"})
LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "[::1]"})


def _hdr(scope: Scope, name: str) -> str | None:
    key = name.lower().encode()
    for k, v in scope.get("headers", []):
        if k == key:
            return str(v.decode("latin-1"))
    return None


def host_without_port(host: str) -> str:
    h = host.strip().lower()
    if h.startswith("["):
        end = h.find("]")
        return h[: end + 1] if end != -1 else h
    return h.split(":", 1)[0]


class SecurityMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        validator: TokenValidator,
        allowed_hosts: tuple[str, ...] = (),
        allowed_origins: tuple[str, ...] = (),
    ) -> None:
        self.app = app
        self.validator = validator
        self.allowed_hosts = LOOPBACK_HOSTS | {h.lower() for h in allowed_hosts}
        self.allowed_origins = frozenset(allowed_origins)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "lifespan":
            await self.app(scope, receive, send)
            return
        if scope["type"] != "http":  # websockets etc. are denied by default
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1008})
            return
        rid = uuid.uuid4().hex
        scope.setdefault("state", {})["request_id"] = rid

        host = _hdr(scope, "host")
        if host is None or host_without_port(host) not in self.allowed_hosts:
            await self._deny(send, 400, ErrorCode.HOST_NOT_ALLOWED, "Host not allowed.", rid)
            return
        origin = _hdr(scope, "origin")
        if origin is not None and origin not in self.allowed_origins:
            await self._deny(send, 403, ErrorCode.ORIGIN_NOT_ALLOWED, "Origin not allowed.", rid)
            return
        if scope["method"] == "OPTIONS" and origin is not None:
            await self._preflight(send, origin, rid)
            return

        if scope["path"] not in PUBLIC_PATHS:
            auth = _hdr(scope, "authorization") or ""
            token = auth[7:].strip() if auth[:7].lower() == "bearer " else ""
            if not token or not self.validator.validate(token):
                await self._deny(
                    send, 401, ErrorCode.AUTH_REQUIRED, "Authentication required.", rid
                )
                return

        async def send_wrapped(message: MutableMapping[str, Any]) -> None:
            if message["type"] == "http.response.start":
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", rid.encode()))
                if origin is not None:  # exact echo of an allow-listed origin; never "*"
                    headers.append((b"access-control-allow-origin", origin.encode()))
                    headers.append((b"vary", b"Origin"))
                message = {**message, "headers": headers}
            await send(message)

        await self.app(scope, receive, send_wrapped)

    async def _deny(self, send: Send, status: int, code: ErrorCode, msg: str, rid: str) -> None:
        body = json.dumps(envelope(code, msg, rid)).encode()
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [
                    (b"content-type", b"application/json"),
                    (b"content-length", str(len(body)).encode()),
                    (b"x-request-id", rid.encode()),
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})

    async def _preflight(self, send: Send, origin: str, rid: str) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": 204,
                "headers": [
                    (b"access-control-allow-origin", origin.encode()),
                    (b"access-control-allow-headers", b"authorization, content-type"),
                    (b"access-control-allow-methods", b"GET, POST, DELETE"),
                    (b"vary", b"Origin"),
                    (b"x-request-id", rid.encode()),
                ],
            }
        )
        await send({"type": "http.response.body", "body": b""})
