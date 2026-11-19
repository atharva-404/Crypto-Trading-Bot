"""Load API credentials from environment variables or a local .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv is optional at runtime
    load_dotenv = None

PLACEHOLDERS = {"", "your_api_key", "your_secret_key", "your_testnet_api_key", "your_testnet_api_secret"}


class ConfigError(Exception):
    """Raised when credentials are missing."""


@dataclass(frozen=True)
class Config:
    api_key: str = field(repr=False)
    api_secret: str = field(repr=False)
    testnet: bool = True


def load_config() -> Config:
    if load_dotenv is not None:
        load_dotenv()
    key = os.getenv("BINANCE_API_KEY", "").strip()
    secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if key.lower() in PLACEHOLDERS or secret.lower() in PLACEHOLDERS:
        raise ConfigError(
            "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET "
            "in your environment or in a .env file (see .env.example)."
        )
    return Config(api_key=key, api_secret=secret)
