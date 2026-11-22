from app.security.middleware import PUBLIC_PATHS, SecurityMiddleware
from app.security.tokens import DenyAllValidator
from tests.asgi_harness import Recorder, request

H = {"host": "localhost:8000"}


class AcceptsTestToken:  # test double, defined in tests only (never in app/)
    production_ready = False

    def validate(self, token: str) -> bool:
        return token == "unit-test-token-not-a-secret"


def make(validator=None, hosts=(), origins=()):  # type: ignore[no-untyped-def]
    rec = Recorder()
    return rec, SecurityMiddleware(rec.app, validator or DenyAllValidator(), hosts, origins)


def test_only_health_and_pairing_public() -> None:
    assert PUBLIC_PATHS == {"/health", "/pairing"}


def test_health_open_without_token() -> None:
    rec, mw = make()
    status, hdr, _ = request(mw, "/health", headers=H)
    assert status == 200 and rec.called and "x-request-id" in hdr


def test_data_route_denied_without_token() -> None:  # AT-NET-03 (middleware level)
    rec, mw = make()
    status, _, body = request(mw, "/segments", headers=H)
    assert status == 401 and not rec.called
    assert body["error"]["code"] == "AUTH_REQUIRED" and body["error"]["request_id"]


def test_default_deny_rejects_any_token() -> None:
    rec, mw = make()
    status, _, _ = request(mw, "/segments", headers={**H, "authorization": "Bearer anything"})
    assert status == 401 and not rec.called


def test_valid_token_via_test_double_passes() -> None:
    rec, mw = make(AcceptsTestToken())
    status, _, _ = request(
        mw, "/segments", headers={**H, "authorization": "Bearer unit-test-token-not-a-secret"}
    )
    assert status == 200 and rec.called


def test_non_bearer_scheme_denied() -> None:
    rec, mw = make(AcceptsTestToken())
    status, _, _ = request(
        mw, "/segments", headers={**H, "authorization": "Basic unit-test-token-not-a-secret"}
    )
    assert status == 401 and not rec.called


def test_unexpected_host_rejected() -> None:  # AT-NET-10 (middleware level)
    rec, mw = make()
    for host in ("evil.example", "192.168.1.9:8000", ""):
        status, _, body = request(mw, "/health", headers={"host": host})
        assert status == 400 and body["error"]["code"] == "HOST_NOT_ALLOWED"
    status, _, _ = request(mw, "/health")  # no Host header at all
    assert status == 400 and not rec.called


def test_extra_allowed_host_accepted() -> None:
    _, mw = make(hosts=("my-pc.local",))
    status, _, _ = request(mw, "/health", headers={"host": "my-pc.local:8000"})
    assert status == 200


def test_foreign_origin_rejected_even_on_public_route() -> None:  # AT-NET-10 (middleware level)
    rec, mw = make()
    status, _, body = request(mw, "/health", headers={**H, "origin": "https://evil.example"})
    assert status == 403 and body["error"]["code"] == "ORIGIN_NOT_ALLOWED" and not rec.called


def test_allowed_origin_echoed_exactly_never_wildcard() -> None:
    _, mw = make(origins=("http://localhost:5173",))
    status, hdr, _ = request(mw, "/health", headers={**H, "origin": "http://localhost:5173"})
    assert status == 200 and hdr["access-control-allow-origin"] == "http://localhost:5173"
    assert hdr["access-control-allow-origin"] != "*"


def test_no_cors_headers_without_origin() -> None:
    _, mw = make()
    _, hdr, _ = request(mw, "/health", headers=H)
    assert "access-control-allow-origin" not in hdr


def test_preflight_foreign_origin_denied() -> None:
    _, mw = make()
    status, _, _ = request(mw, "/segments", "OPTIONS", {**H, "origin": "https://evil.example"})
    assert status == 403
