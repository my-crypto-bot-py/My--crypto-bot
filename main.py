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
import ccxt
import pandas as pd
import requests
import os
import telebot

# --- SETUP ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.kucoin({'enableRateLimit': True})

# --- FUNCTIONS ---

def get_liquidation_heatmap(symbol):
    """
    CoinGlass API se Liquidation Level fetch karein
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        # Liquidation Heatmap level endpoint
        url = f"https://open-api.coinglass.com/public/v2/liquidation_pair?pair={symbol}USDT"
        res = requests.get(url, headers=headers, timeout=10).json()
        
        data = res.get('data', [])
        if data:
            # Liquidation value aur Price Level
            liq_val = data[0].get('liquidation', '0')
            return f"🔥 Liq: {liq_val}"
        return "No Data"
    except:
        return "Err"

def generate_and_send():
    try:
        report = "<b>🚀 LIQUIDATION HEATMAP UPDATE</b>\n\n"
        
        for s in ['BTC', 'SOL', 'ETH']:
            liq_info = get_liquidation_heatmap(s)
            report += f"🔹 {s}: {liq_info}\n"
        
        if CHAT_ID:
            bot.send_message(CHAT_ID, report, parse_mode='HTML')
            print("Success!")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    generate_and_send()
