import ccxt
import pandas as pd
import requests
import os
import telebot
import threading
import time

# --- Setup ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# ... (Apne sabhi functions: calculate_atr, fetch_data, get_coinglass_signal, analyze_trade, get_market_price yahan rakhein) ...

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is active! Use /report to get current signals.")

@bot.message_handler(commands=['report'])
def manual_report(message):
    generate_and_send()

def generate_and_send():
    try:
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        bot.send_message(CHAT_ID, report)
        print("Success: Message sent!")
    except Exception as e:
        print(f"FAILED to send message. Error: {e}")

# --- Combined Execution ---
if __name__ == "__main__":
    # 1. Agar hum GitHub Action chala rahe hain (jahan automation zaruri hai)
    # Hum 'IS_GITHUB' environment variable check kar sakte hain ya sirf run karein.
    print("Running scheduled report...")
    generate_and_send()
    
    # 2. Agar aap ise 24/7 server pe daalna chahein, toh ye uncomment karein:
    # print("Bot polling started...")
    # bot.polling(none_stop=True)
