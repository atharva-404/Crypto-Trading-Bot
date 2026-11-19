"""Binance Futures Testnet trading bot."""

from .bot import FuturesBot, OrderError
from .validation import ValidationError

__version__ = "1.0.0"
__all__ = ["FuturesBot", "OrderError", "ValidationError", "__version__"]
