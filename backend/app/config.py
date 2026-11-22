"""Settings from environment variables, validated; fails safely (raises ConfigError).

Phase 1 decisions kept OPEN (not chosen here): transport (HTTPS vs HTTP fallback, Q11), backend
host (Q16), LAN pairing implementation. Therefore LAN mode can never become ready in Phase 1.
"""

from __future__ import annotations

import ipaddress
import os
from collections.abc import Mapping
from dataclasses import dataclass

PREFIX = "TUBESOMALI_"
LOOPBACK_NAMES = frozenset({"localhost", "127.0.0.1", "::1", "[::1]"})


class ConfigError(Exception):
    """Invalid or unsafe configuration. The server must not start."""


def _bool(env: Mapping[str, str], key: str, default: bool) -> bool:
    raw = env.get(PREFIX + key)
    if raw is None or raw == "":
        return default
    v = raw.strip().lower()
    if v in ("1", "true", "yes", "on"):
        return True
    if v in ("0", "false", "no", "off"):
        return False
    raise ConfigError(f"{PREFIX}{key} must be a boolean (true/false)")


def _list(env: Mapping[str, str], key: str) -> tuple[str, ...]:
    raw = env.get(PREFIX + key, "")
    return tuple(p.strip() for p in raw.split(",") if p.strip())


def is_loopback_host(host: str) -> bool:
    h = host.strip().lower()
    if h in LOOPBACK_NAMES:
        return True
    try:
        return ipaddress.ip_address(h.strip("[]")).is_loopback
    except ValueError:
        return False


@dataclass(frozen=True)
class Settings:
    host: str = "127.0.0.1"
    port: int = 8000
    lan_mode: bool = False
    allowed_hosts: tuple[str, ...] = ()
    allowed_origins: tuple[str, ...] = ()
    env: str = "dev"


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    e = os.environ if env is None else env
    host = e.get(PREFIX + "HOST", "127.0.0.1").strip() or "127.0.0.1"
    try:
        port = int(e.get(PREFIX + "PORT", "8000"))
    except ValueError as exc:
        raise ConfigError(f"{PREFIX}PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ConfigError(f"{PREFIX}PORT must be 1-65535")
    mode = e.get(PREFIX + "ENV", "dev").strip().lower() or "dev"
    if mode not in ("dev", "release"):
        raise ConfigError(f"{PREFIX}ENV must be 'dev' or 'release'")
    origins = _list(e, "ALLOWED_ORIGINS")
    if any(o == "*" for o in origins):
        raise ConfigError("wildcard CORS origin is not allowed")
    return Settings(
        host=host,
        port=port,
        lan_mode=_bool(e, "LAN_MODE", False),
        allowed_hosts=_list(e, "ALLOWED_HOSTS"),
        allowed_origins=origins,
        env=mode,
    )


def validate_settings(settings: Settings, *, access_control_ready: bool) -> None:
    """Raise ConfigError for any unsafe combination (AT-NET-01/02 at configuration level)."""
    if settings.lan_mode and not access_control_ready:
        raise ConfigError(
            "LAN mode requires working access control; none is available in this build. "
            "Refusing to start."
        )
    if not is_loopback_host(settings.host) and not settings.lan_mode:
        raise ConfigError(
            "Binding to a non-loopback address requires LAN mode (opt-in). Refusing to start."
        )
