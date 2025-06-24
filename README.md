
# 🚀 Binance Futures Trading Bot (Testnet)

A simplified crypto trading bot that uses the Binance Futures **Testnet API** to place **MARKET** and **LIMIT** orders with basic CLI and logging support.

---

## 🛠️ Features

- ✅ Place **Market** and **Limit** orders (BUY/SELL)
- ✅ CLI input interface
- ✅ Logs all API requests, responses, and errors to `logs/bot.log`
- ✅ Clean, reusable, and modular code structure
- ✅ Supports Binance Futures **Testnet**

---

## 📁 Project Structure

```
binance_bot/
├── bot.py               # Core trading logic
├── config.py            # API credentials & base URL
├── logger.py            # Logging setup
├── main.py              # CLI entry point
├── requirements.txt     # Required Python packages
└── logs/
    └── bot.log          # Log file for all orders/errors
```

---

## ⚙️ Installation

```bash
git clone <your-repo-url>
cd binance_bot
python -m venv venv
source venv/bin/activate        # On Linux/Mac
venv\Scripts\activate         # On Windows
pip install -r requirements.txt
```

---

## 🔐 Setup

1. Create a [Binance Futures Testnet](https://testnet.binancefuture.com/) account.
2. Generate API key & secret.
3. Paste them into `config.py`:
```python
API_KEY = 'your_testnet_api_key'
API_SECRET = 'your_testnet_api_secret'
```

---

## ▶️ How to Run

```bash
python main.py
```

You'll be asked to enter:
- Trading pair (e.g. BTCUSDT)
- Side (BUY/SELL)
- Order Type (MARKET/LIMIT)
- Quantity
- Price (only if LIMIT)

---

## 📄 Example CLI Interaction

```
Enter symbol (e.g., BTCUSDT): BTCUSDT
Enter side (BUY/SELL): BUY
Enter order type (MARKET/LIMIT): MARKET
Enter quantity: 0.001
```

---

## 📒 Logging

All activity is logged to `logs/bot.log`. Example:
```
2025-06-22 10:01:23 - INFO - Order placed: {...}
2025-06-22 10:01:24 - ERROR - Order failed: Invalid quantity
```

---



## 🧪 Requirements

```text
python-binance==1.0.17
```

---


