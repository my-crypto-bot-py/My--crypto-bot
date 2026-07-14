import os
import telebot

# Sirf credentials aur basic connection check
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("Error: TOKEN or CHAT_ID missing!")
    exit()

bot = telebot.TeleBot(TOKEN)

def test_connection():
    try:
        print(f"Testing connection to CHAT_ID: {CHAT_ID}")
        bot.send_message(int(CHAT_ID), "✅ Base Connection Test: Success!")
        print("Test Message sent successfully.")
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_connection()

import ccxt
import pandas as pd
import requests
import os
import telebot

# --- Setup ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
raw_chat_id = os.environ.get('CHAT_ID')
CHAT_ID = int(raw_chat_id) if raw_chat_id else None
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# --- Functions (Aapke purane functions yahan raheinge) ---
# def get_market_price(s): ...
# def analyze_trade(s): ...
import requests
import os

COINGLASS_KEY = os.environ.get("COINGLASS_API_KEY")

headers = {
    "CG-API-KEY": COINGLASS_KEY
}

url = "https://open-api-v4.coinglass.com/api/futures/liquidation/pair-history"

params = {
    "exchange": "Binance",
    "symbol": "BTCUSDT",
    "interval": "1h",
    "limit": 1
}

r = requests.get(url, headers=headers, params=params)

print(r.status_code)
print(r.text)
