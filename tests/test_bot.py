from unittest.mock import MagicMock

import pytest
from binance.exceptions import BinanceAPIException

from binance_bot import FuturesBot, OrderError, ValidationError
from binance_bot.cli import main
from binance_bot.config import ConfigError, load_config
from binance_bot.validation import validate_order


def make_bot():
    client = MagicMock()
    return FuturesBot("k", "s", client=client), client


def test_market_order_payload():
    bot, client = make_bot()
    client.futures_create_order.return_value = {"orderId": 1}
    assert bot.place_order("btcusdt", "buy", "market", "0.001") == {"orderId": 1}
    client.futures_create_order.assert_called_once_with(
        symbol="BTCUSDT", side="BUY", type="MARKET", quantity="0.001"
    )


def test_limit_order_payload():
    bot, client = make_bot()
    bot.place_order("BTCUSDT", "SELL", "LIMIT", "0.5", price="70000")
    client.futures_create_order.assert_called_once_with(
        symbol="BTCUSDT", side="SELL", type="LIMIT", quantity="0.5", price="70000", timeInForce="GTC"
    )


def test_stop_order_payload():
    bot, client = make_bot()
    bot.place_order("BTCUSDT", "SELL", "STOP", "1", price="59900", stop_price="60000")
    kwargs = client.futures_create_order.call_args.kwargs
    assert kwargs["type"] == "STOP" and kwargs["stopPrice"] == "60000"


def test_api_error_becomes_order_error():
    bot, client = make_bot()
    response = MagicMock(status_code=400, text='{"code": -1121, "msg": "Invalid symbol."}')
    client.futures_create_order.side_effect = BinanceAPIException(response, 400, response.text)
    with pytest.raises(OrderError):
        bot.place_order("BTCUSDT", "BUY", "MARKET", "1")


@pytest.mark.parametrize(
    "args",
    [
        ("BTC", "BUY", "MARKET", "1"),
        ("BTCUSDT", "HOLD", "MARKET", "1"),
        ("BTCUSDT", "BUY", "FOO", "1"),
        ("BTCUSDT", "BUY", "MARKET", "-1"),
        ("BTCUSDT", "BUY", "MARKET", "abc"),
        ("BTCUSDT", "BUY", "MARKET", "nan"),
        ("BTCUSDT", "BUY", "LIMIT", "1"),
        ("BTCUSDT", "BUY", "MARKET", "1", "100"),
        ("BTCUSDT", "BUY", "STOP", "1", "100"),
    ],
)
def test_invalid_orders_rejected(args):
    with pytest.raises(ValidationError):
        validate_order(*args)


def test_invalid_order_never_reaches_api():
    bot, client = make_bot()
    with pytest.raises(ValidationError):
        bot.place_order("BTCUSDT", "BUY", "LIMIT", "1")
    client.futures_create_order.assert_not_called()


def test_balance_filters_zero(monkeypatch):
    bot, client = make_bot()
    client.futures_account_balance.return_value = [
        {"asset": "USDT", "balance": "100"}, {"asset": "BNB", "balance": "0.0"}
    ]
    assert [b["asset"] for b in bot.balance()] == ["USDT"]


def test_missing_credentials(monkeypatch):
    monkeypatch.setattr("binance_bot.config.load_dotenv", None)
    monkeypatch.delenv("BINANCE_API_KEY", raising=False)
    monkeypatch.delenv("BINANCE_API_SECRET", raising=False)
    with pytest.raises(ConfigError):
        load_config()


def test_cli_dry_run_and_bad_input(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["place", "--symbol", "BTCUSDT", "--side", "buy", "--type", "market",
                 "--quantity", "0.01", "--dry-run"]) == 0
    assert "Dry run OK" in capsys.readouterr().out
    assert main(["place", "--symbol", "BTCUSDT", "--side", "buy", "--type", "limit",
                 "--quantity", "0.01", "--dry-run"]) == 2
