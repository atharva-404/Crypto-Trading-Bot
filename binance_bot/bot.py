from __future__ import annotations

import logging

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

from .logger import LOGGER_NAME
from .validation import validate_order, validate_symbol

log = logging.getLogger(LOGGER_NAME)


class OrderError(Exception):
    """Raised when Binance rejects a request or the network fails."""


class FuturesBot:
    """Thin wrapper around the Binance Futures API (testnet by default)."""

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True, client: Client | None = None):
        # testnet=True makes python-binance use https://testnet.binancefuture.com
        self.client = client or Client(api_key, api_secret, testnet=testnet)
        self.testnet = testnet
        log.info("Bot initialized (%s).", "testnet" if testnet else "LIVE")

    def _call(self, description: str, func, **kwargs):
        log.info("Request: %s %s", description, kwargs)
        try:
            result = func(**kwargs)
        except (BinanceAPIException, BinanceRequestException) as exc:
            log.error("%s failed: %s", description, exc)
            raise OrderError(f"{description} failed: {exc}") from exc
        except Exception as exc:  # network errors, timeouts
            log.error("%s failed: %s", description, exc)
            raise OrderError(f"{description} failed: {exc}") from exc
        log.info("Response: %s", result)
        return result

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None) -> dict:
        """Place a MARKET, LIMIT or STOP (stop-limit) order and return Binance's response."""
        o = validate_order(symbol, side, order_type, quantity, price, stop_price)
        params = {
            "symbol": o["symbol"],
            "side": o["side"],
            "type": o["order_type"],
            "quantity": format(o["quantity"], "f"),
        }
        if o["order_type"] in ("LIMIT", "STOP"):
            params["price"] = format(o["price"], "f")
            params["timeInForce"] = "GTC"
        if o["order_type"] == "STOP":
            params["stopPrice"] = format(o["stop_price"], "f")
        return self._call("Place order", self.client.futures_create_order, **params)

    def get_order(self, symbol: str, order_id: int) -> dict:
        return self._call("Get order", self.client.futures_get_order, symbol=validate_symbol(symbol), orderId=order_id)

    def cancel_order(self, symbol: str, order_id: int) -> dict:
        return self._call("Cancel order", self.client.futures_cancel_order, symbol=validate_symbol(symbol), orderId=order_id)

    def open_orders(self, symbol: str | None = None) -> list:
        kwargs = {"symbol": validate_symbol(symbol)} if symbol else {}
        return self._call("List open orders", self.client.futures_get_open_orders, **kwargs)

    def price(self, symbol: str) -> str:
        data = self._call("Get price", self.client.futures_symbol_ticker, symbol=validate_symbol(symbol))
        return data["price"]

    def balance(self) -> list:
        """Return balances for assets with a non-zero wallet balance."""
        rows = self._call("Get balance", self.client.futures_account_balance)
        return [r for r in rows if float(r.get("balance", 0)) > 0]
