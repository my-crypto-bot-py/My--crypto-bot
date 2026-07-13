import ccxt
import pandas as pd
import requests
import os
import telebot
import time  # <--- Yeh add kiya hai

# --- Setup ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
raw_chat_id = os.environ.get('CHAT_ID')
CHAT_ID = int(raw_chat_id) if raw_chat_id else None

bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# ... (Aapke baaki functions: get_market_price, analyze_trade wahi rahenge) ...

def generate_and_send():
    try:
        # Report Generation logic
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        # Message sending with explicit ID handling
        if CHAT_ID:
            bot.send_message(CHAT_ID, report)
            time.sleep(2) # <--- Telegram server ko process karne ke liye 2 second ka gap
            print(f"Success: Message sent to {CHAT_ID}!")
        else:
            print("Error: CHAT_ID is not defined in environment variables.")
            
    except Exception as e:
        print(f"FAILED to send message. Error: {e}")

if __name__ == "__main__":
    generate_and_send()
