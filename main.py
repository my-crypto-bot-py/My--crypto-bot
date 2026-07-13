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

def generate_and_send():
    try:
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        if CHAT_ID:
            bot.send_message(CHAT_ID, report)
            print(f"Success: Message sent to {CHAT_ID}!")
    except Exception as e:
        print(f"FAILED to send message: {e}")

if __name__ == "__main__":
    # GitHub Action ise har ghante chalayega, humein sirf ek baar report bhejni hai.
    generate_and_send()
