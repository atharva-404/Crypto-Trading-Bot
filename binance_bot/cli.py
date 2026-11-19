from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .bot import FuturesBot, OrderError
from .config import ConfigError, load_config
from .logger import setup_logger
from .validation import ORDER_TYPES, SIDES, ValidationError, validate_order


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="binance_bot", description="Binance Futures Testnet trading bot."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="also print info logs to the console")
    sub = parser.add_subparsers(dest="command", required=True)

    place = sub.add_parser("place", help="place an order")
    place.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    place.add_argument("--side", required=True, choices=SIDES, type=str.upper)
    place.add_argument("--type", dest="order_type", required=True, choices=ORDER_TYPES, type=str.upper)
    place.add_argument("--quantity", required=True)
    place.add_argument("--price", help="required for LIMIT and STOP")
    place.add_argument("--stop-price", help="trigger price, required for STOP")
    place.add_argument("--dry-run", action="store_true", help="validate only, send nothing")

    sub.add_parser("interactive", help="prompt for order details")

    price = sub.add_parser("price", help="show latest price")
    price.add_argument("symbol")

    orders = sub.add_parser("orders", help="list open orders")
    orders.add_argument("--symbol")

    status = sub.add_parser("status", help="show one order")
    status.add_argument("symbol")
    status.add_argument("order_id", type=int)

    cancel = sub.add_parser("cancel", help="cancel an order")
    cancel.add_argument("symbol")
    cancel.add_argument("order_id", type=int)

    sub.add_parser("balance", help="show futures wallet balance")
    return parser


def _prompt_order() -> dict:
    symbol = input("Symbol (e.g. BTCUSDT): ")
    side = input("Side (BUY/SELL): ")
    order_type = input("Order type (MARKET/LIMIT/STOP): ").strip().upper()
    quantity = input("Quantity: ")
    price = input("Limit price: ") if order_type in ("LIMIT", "STOP") else None
    stop_price = input("Stop (trigger) price: ") if order_type == "STOP" else None
    return {
        "symbol": symbol, "side": side, "order_type": order_type,
        "quantity": quantity, "price": price, "stop_price": stop_price,
    }


def _show(data) -> None:
    print(json.dumps(data, indent=2, default=str))


def run(args: argparse.Namespace) -> int:
    if args.command == "place" and args.dry_run:
        clean = validate_order(args.symbol, args.side, args.order_type, args.quantity, args.price, args.stop_price)
        print("Dry run OK. Order would be:")
        _show(clean)
        return 0

    request = None
    if args.command == "interactive":
        request = _prompt_order()
        validate_order(**request)  # fail early, before connecting
    elif args.command == "place":
        request = {
            "symbol": args.symbol, "side": args.side, "order_type": args.order_type,
            "quantity": args.quantity, "price": args.price, "stop_price": args.stop_price,
        }

    cfg = load_config()
    bot = FuturesBot(cfg.api_key, cfg.api_secret, testnet=cfg.testnet)

    if request is not None:
        order = bot.place_order(**request)
        print("Order placed:")
        _show(order)
    elif args.command == "price":
        print(bot.price(args.symbol))
    elif args.command == "orders":
        _show(bot.open_orders(args.symbol))
    elif args.command == "status":
        _show(bot.get_order(args.symbol, args.order_id))
    elif args.command == "cancel":
        _show(bot.cancel_order(args.symbol, args.order_id))
    elif args.command == "balance":
        _show(bot.balance())
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    setup_logger(verbose=args.verbose)
    try:
        return run(args)
    except (ValidationError, ConfigError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except OrderError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        return 130
