# 🚀 Binance Futures Testnet Trading Bot

A robust, modular Python CLI application built for the Primetrade.ai technical assessment. This bot interacts with the Binance Futures Testnet API to execute market and limit orders using signed HMAC SHA256 payloads, featuring custom interactive terminal telemetry.

## 🛠️ System Architecture

The project utilizes a completely flat, modular script architecture optimized for direct script execution and execution performance:

* `cli.py` — Main execution entry point; manages interactive wizard fallbacks, CLI argument routing, and custom terminal UI rendering.
* `client.py` — Low-level HTTP client tasked with payload signing, cryptographic HMAC-SHA256 timestamp hashing, and networking.
* `orders.py` — High-level order builder and execution manager.
* `validators.py` — Defensive boundary input validation rules.
* `logging_config.py` — Centralized logging layout writing to `bot.log`.

---

## 🚀 Quick Start Guide

### 1. Configure Credentials
Open `cli.py` and assign your Binance Futures Testnet credentials:
```python
API_KEY = "your_testnet_api_key_here"
API_SECRET = "your_testnet_secret_key_here"

Run a MARKET BUY order directly from your terminal:

Bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01


Run a LIMIT BUY order:

Bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000


3. Interactive Mode Fallback
If you execute the script without any trailing terminal flags, the bot automatically boots an intuitive, multi-step interactive step wizard:

Bash
python cli.py
