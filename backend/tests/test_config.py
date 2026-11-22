import pytest

from app.config import ConfigError, Settings, is_loopback_host, load_settings, validate_settings


def test_defaults_are_loopback_and_lan_off() -> None:
    s = load_settings({})
    assert s.host == "127.0.0.1" and s.lan_mode is False and s.allowed_origins == ()


def test_lan_mode_refuses_without_access_control() -> None:  # AT-NET-02 (config level)
    s = load_settings({"TUBESOMALI_LAN_MODE": "true", "TUBESOMALI_HOST": "0.0.0.0"})
    with pytest.raises(ConfigError):
        validate_settings(s, access_control_ready=False)


def test_non_loopback_without_lan_mode_refused() -> None:  # AT-NET-01 (config level)
    with pytest.raises(ConfigError):
        validate_settings(Settings(host="0.0.0.0"), access_control_ready=True)


def test_loopback_default_valid() -> None:
    validate_settings(Settings(), access_control_ready=False)


@pytest.mark.parametrize(
    "env",
    [
        {"TUBESOMALI_PORT": "abc"},
        {"TUBESOMALI_PORT": "0"},
        {"TUBESOMALI_PORT": "70000"},
        {"TUBESOMALI_LAN_MODE": "maybe"},
        {"TUBESOMALI_ENV": "prod"},
        {"TUBESOMALI_ALLOWED_ORIGINS": "*"},
    ],
)
def test_invalid_config_rejected(env: dict[str, str]) -> None:
    with pytest.raises(ConfigError):
        load_settings(env)


@pytest.mark.parametrize(
    "h,ok",
    [
        ("127.0.0.1", True),
        ("localhost", True),
        ("::1", True),
        ("192.168.1.5", False),
        ("0.0.0.0", False),
        ("example.com", False),
    ],
)
def test_is_loopback(h: str, ok: bool) -> None:
    assert is_loopback_host(h) is ok
