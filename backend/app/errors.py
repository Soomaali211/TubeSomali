"""Fixed error vocabulary and JSON envelope (ADR-004). Messages never contain user text or secrets."""

from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    # ADR-004 vocabulary
    NO_CAPTIONS = "NO_CAPTIONS"
    CAPTIONS_UNAVAILABLE = "CAPTIONS_UNAVAILABLE"
    LANGUAGE_NOT_AVAILABLE = "LANGUAGE_NOT_AVAILABLE"
    VIDEO_UNAVAILABLE = "VIDEO_UNAVAILABLE"
    RATE_LIMITED = "RATE_LIMITED"
    PROVIDER_BLOCKED = "PROVIDER_BLOCKED"
    NETWORK_TIMEOUT = "NETWORK_TIMEOUT"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    POLICY_RESTRICTED = "POLICY_RESTRICTED"
    INVALID_URL = "INVALID_URL"
    UNSUPPORTED_FILE = "UNSUPPORTED_FILE"
    RIGHTS_NOT_DECLARED = "RIGHTS_NOT_DECLARED"
    AUDIO_UNAVAILABLE = "AUDIO_UNAVAILABLE"
    # Phase 1 additions (PROPOSED extension of ADR-004; owner has not approved the additions)
    AUTH_REQUIRED = "AUTH_REQUIRED"
    HOST_NOT_ALLOWED = "HOST_NOT_ALLOWED"
    ORIGIN_NOT_ALLOWED = "ORIGIN_NOT_ALLOWED"
    NOT_FOUND = "NOT_FOUND"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    INTERNAL_ERROR = "INTERNAL_ERROR"


ADR004_CODES = frozenset(c.value for c in list(ErrorCode)[:13])


def envelope(code: ErrorCode, message: str, request_id: str) -> dict[str, object]:
    return {"error": {"code": code.value, "message": message, "request_id": request_id}}
