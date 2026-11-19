# Binance Futures Testnet Bot

[![CI](https://github.com/atharva-404/Crypto-Trading-Bot/actions/workflows/ci.yml/badge.svg)](https://github.com/atharva-404/Crypto-Trading-Bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)

A small command-line tool for placing and managing orders on the **Binance Futures Testnet**. Practice with fake money, with input validation, clear errors and full request logging.

> **Disclaimer:** This is a learning project built out of curiosity. It has no trading strategy and is not financial advice. It targets the testnet by default. Don't use it with real funds.

## Features

- MARKET, LIMIT and STOP (stop-limit) orders, BUY or SELL
- Subcommands to check price, balance, open orders, order status, and to cancel orders
- `--dry-run` to validate an order without sending it
- Interactive mode for guided input
- Input validation with precise `Decimal` handling (no float rounding)
- Credentials read from environment variables or `.env`, never from source code
- Rotating log file at `logs/bot.log` with every request, response and error
- Unit tests and CI on Python 3.9, 3.11 and 3.12

## Install

```bash
git clone https://github.com/atharva-404/Crypto-Trading-Bot.git
cd Crypto-Trading-Bot
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -e .
```

## Set up credentials

1. Create an account at the [Binance Futures Testnet](https://testnet.binancefuture.com/) and generate an API key and secret.
2. Copy the example file and fill it in:

```bash
cp .env.example .env            # Windows: copy .env.example .env
```

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

`.env` is git-ignored.

## Usage

```bash
# Market order
python -m binance_bot place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Limit order
python -m binance_bot place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 70000

# Stop-limit order
python -m binance_bot place --symbol BTCUSDT --side SELL --type STOP --quantity 0.01 --price 59900 --stop-price 60000

# Validate only
python -m binance_bot place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --dry-run

# Other commands
python -m binance_bot price BTCUSDT
python -m binance_bot balance
python -m binance_bot orders --symbol BTCUSDT
python -m binance_bot status BTCUSDT 123456
python -m binance_bot cancel BTCUSDT 123456
python -m binance_bot interactive
```

After `pip install -e .` you can also use the shorter `binance-bot` command. Add `-v` to print log lines to the console.

## Project structure

```
binance_bot/
  bot.py          # FuturesBot: API wrapper
  cli.py          # argparse command-line interface
  config.py       # loads credentials from env / .env
  logger.py       # rotating file logger
  validation.py   # input validation
tests/            # pytest suite (no network needed)
```

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
