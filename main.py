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

# --- 1. SETUP ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
raw_chat_id = os.environ.get('CHAT_ID')
CHAT_ID = int(raw_chat_id) if raw_chat_id else None

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# --- 2. FUNCTIONS (Inhe hamesha sabse upar rakhein) ---

def get_market_price(s):
    # Apna existing logic yahan rakhein
    return "Price Data"

def analyze_trade(s):
    # Apna existing logic yahan rakhein
    return "Signal Data"

def get_coinglass_data(symbol):
    # CoinGlass Data Logic
    try:
        url = f"https://open-api.coinglass.com/public/v2/liquidation_pair?pair={symbol}USDT"
        res = requests.get(url).json()
        liq = res.get('data', [{}])[0].get('liquidation', 'N/A')
        return f"🔥 Liq: {liq}"
    except:
        return "N/A"

def get_market_updates():
    assets = ['BTC', 'XRP', 'SOL', 'XAU']
    report = "\n💎 COINGLASS INSIGHTS:\n"
    for asset in assets:
        report += f"🔹 {asset}: {get_coinglass_data(asset)}\n"
    return report

# --- 3. MAIN LOGIC (Yeh saare functions ke niche hona chahiye) ---

def generate_and_send():
    try:
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        # CoinGlass update add karna
        report += get_market_updates()
        
        if CHAT_ID:
            bot.send_message(CHAT_ID, report)
            print(f"Success: Message sent to {CHAT_ID}!")
    except Exception as e:
        print(f"FAILED to send message: {e}")

# --- 4. EXECUTION ---
if __name__ == "__main__":
    generate_and_send()


