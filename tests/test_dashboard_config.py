"""Tests des paramètres de configuration Snowflake."""
from __future__ import annotations

from config import get_snowflake_config


def test_default_timeouts(monkeypatch):
    for key in (
        "SNOWFLAKE_LOGIN_TIMEOUT",
        "SNOWFLAKE_NETWORK_TIMEOUT",
        "SNOWFLAKE_MAX_RETRIES",
        "SNOWFLAKE_RETRY_BACKOFF",
    ):
        monkeypatch.delenv(key, raising=False)

    cfg = get_snowflake_config()
    assert cfg["login_timeout"] == 30
    assert cfg["network_timeout"] == 60
    assert cfg["max_retries"] == 3
    assert cfg["retry_backoff"] == 2.0


def test_overridden_timeouts(monkeypatch):
    monkeypatch.setenv("SNOWFLAKE_LOGIN_TIMEOUT", "5")
    monkeypatch.setenv("SNOWFLAKE_NETWORK_TIMEOUT", "10")
    monkeypatch.setenv("SNOWFLAKE_MAX_RETRIES", "7")
    monkeypatch.setenv("SNOWFLAKE_RETRY_BACKOFF", "1.5")

    cfg = get_snowflake_config()
    assert cfg["login_timeout"] == 5
    assert cfg["network_timeout"] == 10
    assert cfg["max_retries"] == 7
    assert cfg["retry_backoff"] == 1.5
