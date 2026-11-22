import pytest

from app.contracts import CaptionProvider, NotImplementedInPhase, TranslationPipeline, TTSAdapter
from app.errors import ADR004_CODES, ErrorCode, envelope
from app.security.redact import safe_headers


def test_adr004_vocabulary_preserved() -> None:
    assert len(ADR004_CODES) == 13 and "RIGHTS_NOT_DECLARED" in ADR004_CODES


def test_envelope_shape() -> None:
    e = envelope(ErrorCode.NOT_FOUND, "m", "rid")
    assert e == {"error": {"code": "NOT_FOUND", "message": "m", "request_id": "rid"}}


@pytest.mark.parametrize("cls", [CaptionProvider, TranslationPipeline, TTSAdapter])
def test_stubs_are_abstract_and_unimplemented(cls: type) -> None:
    with pytest.raises(TypeError):
        cls()  # abstract: cannot be instantiated without an implementation


def test_stub_bodies_raise() -> None:
    class P(CaptionProvider):
        def get_segments(self, source_ref: str):  # type: ignore[no-untyped-def]
            return super().get_segments(source_ref)

    with pytest.raises(NotImplementedInPhase):
        P().get_segments("x")


def test_sensitive_headers_redacted() -> None:
    h = safe_headers([(b"Authorization", b"Bearer x"), (b"Host", b"localhost")])
    assert h["authorization"] == "[redacted]" and h["host"] == "localhost"
