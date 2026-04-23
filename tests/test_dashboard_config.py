"""Tests des paramètres de configuration du dashboard."""
from __future__ import annotations

import importlib
import sys
from unittest.mock import MagicMock

import pytest

pytest.importorskip("streamlit")
pytest.importorskip("snowflake.connector")


DUMMY_SF_ENV = {
    "SNOWFLAKE_ACCOUNT": "x",
    "SNOWFLAKE_USER": "x",
    "SNOWFLAKE_PASSWORD": "x",
    "SNOWFLAKE_WAREHOUSE": "x",
    "SNOWFLAKE_DATABASE": "x",
}


def _reload_dashboard(monkeypatch, env):
    for key, value in {**DUMMY_SF_ENV, **env}.items():
        monkeypatch.setenv(key, value)

    import snowflake.connector  # noqa: PLC0415

    fake_cursor = MagicMock()
    fake_cursor.__enter__.return_value = fake_cursor
    fake_cursor.fetchall.return_value = []
    fake_cursor.description = []
    fake_conn = MagicMock()
    fake_conn.cursor.return_value = fake_cursor
    monkeypatch.setattr(snowflake.connector, "connect", lambda **_: fake_conn)

    sys.modules.pop("dashboard", None)
    import dashboard  # noqa: PLC0415
    return importlib.reload(dashboard)


def test_default_timeouts(monkeypatch):
    for key in (
        "SNOWFLAKE_LOGIN_TIMEOUT",
        "SNOWFLAKE_NETWORK_TIMEOUT",
        "SNOWFLAKE_MAX_RETRIES",
        "SNOWFLAKE_RETRY_BACKOFF",
    ):
        monkeypatch.delenv(key, raising=False)

    dashboard = _reload_dashboard(monkeypatch, {})
    assert dashboard.SNOWFLAKE_LOGIN_TIMEOUT == 30
    assert dashboard.SNOWFLAKE_NETWORK_TIMEOUT == 60
    assert dashboard.SNOWFLAKE_MAX_RETRIES == 3
    assert dashboard.SNOWFLAKE_RETRY_BACKOFF == 2.0


def test_overridden_timeouts(monkeypatch):
    dashboard = _reload_dashboard(
        monkeypatch,
        {
            "SNOWFLAKE_LOGIN_TIMEOUT": "5",
            "SNOWFLAKE_NETWORK_TIMEOUT": "10",
            "SNOWFLAKE_MAX_RETRIES": "7",
            "SNOWFLAKE_RETRY_BACKOFF": "1.5",
        },
    )
    assert dashboard.SNOWFLAKE_LOGIN_TIMEOUT == 5
    assert dashboard.SNOWFLAKE_NETWORK_TIMEOUT == 10
    assert dashboard.SNOWFLAKE_MAX_RETRIES == 7
    assert dashboard.SNOWFLAKE_RETRY_BACKOFF == 1.5
