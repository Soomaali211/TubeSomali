"""Token validation interface (G23 skeleton). No pairing and no real token store in Phase 1."""

from __future__ import annotations

from typing import Protocol


class TokenValidator(Protocol):
    """Returns True only for a currently valid device token. Must be constant-time."""

    #: True only for an implementation backed by real, tested pairing/token storage.
    production_ready: bool

    def validate(self, token: str) -> bool: ...


class DenyAllValidator:
    """Default: every token is rejected (default-deny). Not 'ready' for LAN mode."""

    production_ready = False

    def validate(self, token: str) -> bool:
        return False
