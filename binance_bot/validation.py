"""Input validation. Numbers are handled as Decimal to avoid float rounding."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation

SIDES = ("BUY", "SELL")
ORDER_TYPES = ("MARKET", "LIMIT", "STOP")  # STOP = stop-limit
_SYMBOL_RE = re.compile(r"^[A-Z0-9]{5,20}$")


class ValidationError(ValueError):
    """Raised for invalid user input."""


def validate_symbol(symbol: str) -> str:
    symbol = (symbol or "").strip().upper()
    if not _SYMBOL_RE.match(symbol):
        raise ValidationError(f"Invalid symbol {symbol!r}. Example: BTCUSDT")
    return symbol


def validate_side(side: str) -> str:
    side = (side or "").strip().upper()
    if side not in SIDES:
        raise ValidationError(f"Invalid side {side!r}. Use one of: {', '.join(SIDES)}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = (order_type or "").strip().upper()
    if order_type not in ORDER_TYPES:
        raise ValidationError(f"Invalid order type {order_type!r}. Use one of: {', '.join(ORDER_TYPES)}")
    return order_type


def validate_positive(value, name: str) -> Decimal:
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError):
        raise ValidationError(f"{name} must be a number, got {value!r}") from None
    if not number.is_finite() or number <= 0:
        raise ValidationError(f"{name} must be greater than 0, got {value!r}")
    return number


def validate_order(symbol, side, order_type, quantity, price=None, stop_price=None) -> dict:
    """Validate a full order request and return the cleaned values."""
    order_type = validate_order_type(order_type)
    clean = {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": order_type,
        "quantity": validate_positive(quantity, "quantity"),
        "price": None,
        "stop_price": None,
    }
    if order_type in ("LIMIT", "STOP"):
        if price is None:
            raise ValidationError(f"price is required for {order_type} orders")
        clean["price"] = validate_positive(price, "price")
    elif price is not None:
        raise ValidationError("price is only allowed for LIMIT and STOP orders")
    if order_type == "STOP":
        if stop_price is None:
            raise ValidationError("stop price is required for STOP orders")
        clean["stop_price"] = validate_positive(stop_price, "stop price")
    elif stop_price is not None:
        raise ValidationError("stop price is only allowed for STOP orders")
    return clean
