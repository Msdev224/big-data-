"""Snowflake connection / retry configuration, read from environment."""
from __future__ import annotations

import os


def get_snowflake_config() -> dict[str, float | int]:
    return {
        "login_timeout": int(os.getenv("SNOWFLAKE_LOGIN_TIMEOUT", "30")),
        "network_timeout": int(os.getenv("SNOWFLAKE_NETWORK_TIMEOUT", "60")),
        "max_retries": int(os.getenv("SNOWFLAKE_MAX_RETRIES", "3")),
        "retry_backoff": float(os.getenv("SNOWFLAKE_RETRY_BACKOFF", "2")),
    }
