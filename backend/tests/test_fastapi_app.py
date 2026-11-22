"""Requires FastAPI + httpx. Locally absent => reported as SKIPPED, never PASS.
In CI set REQUIRE_FASTAPI=1 so a missing dependency FAILS instead of skipping."""

import os

import pytest

try:
    from fastapi.testclient import TestClient

    HAVE = True
except ImportError:
    HAVE = False

if not HAVE:
    if os.environ.get("REQUIRE_FASTAPI") == "1":
        pytest.fail("REQUIRE_FASTAPI=1 but fastapi/httpx not importable", pytrace=False)
    pytest.skip("fastapi/httpx not installed in this environment", allow_module_level=True)

from app.config import ConfigError, Settings
from app.main import create_app
from app.security.middleware import PUBLIC_PATHS


def client() -> TestClient:
    return TestClient(create_app(Settings()), base_url="http://localhost:8000")


def test_health() -> None:
    r = client().get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok", "phase": "1"}


def test_route_enumeration_default_deny() -> None:  # AT-NET-03 (loopback, automated)
    app = create_app(Settings())
    c = TestClient(app, base_url="http://localhost:8000")
    paths = {getattr(r, "path", "") for r in app.routes}
    assert paths, "no routes found"
    for p in paths:
        if p in PUBLIC_PATHS or not p.startswith("/"):
            continue
        assert c.get(p).status_code == 401, f"{p} reachable without token"
    assert c.get("/definitely-unknown").status_code == 401  # unknown routes also default-deny


def test_pairing_not_implemented() -> None:
    r = client().post("/pairing")
    assert r.status_code == 501 and r.json()["error"]["code"] == "NOT_IMPLEMENTED"


def test_docs_and_openapi_disabled() -> None:
    c = client()
    for p in ("/docs", "/redoc", "/openapi.json"):
        assert c.get(p).status_code == 401


def test_no_research_route_registered() -> None:  # AT-YT-09 skeleton
    app = create_app(Settings())
    assert not [r for r in app.routes if "research" in getattr(r, "path", "")]


def test_lan_mode_refuses_create_app() -> None:  # AT-NET-02
    with pytest.raises(ConfigError):
        create_app(Settings(host="0.0.0.0", lan_mode=True))


def test_foreign_host_rejected_at_app_level() -> None:  # AT-NET-10
    c = TestClient(create_app(Settings()), base_url="http://evil.example")
    assert c.get("/health").status_code == 400
