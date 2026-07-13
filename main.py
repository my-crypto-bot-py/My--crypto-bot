import ccxt
import pandas as pd
import requests
import os
import telebot

# --- Setup ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# ... (Aapke baaki functions: calculate_atr, fetch_data, get_coinglass_signal, analyze_trade, get_market_price wahi rahenge) ...

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is active! Your Chat ID is: " + str(message.chat.id))

@bot.message_handler(commands=['report'])
def manual_report(message):
    generate_and_send()

def generate_and_send():
    try:
        # 1. Identity Check
        me = bot.get_me()
        print(f"Bot connected: {me.username}")
        
        # 2. Report Generation
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        # 3. Sending Message
        print(f"Attempting to send to CHAT_ID: {CHAT_ID}")
        bot.send_message(CHAT_ID, report)
        print("Success: Message sent!")
        
    except Exception as e:
        print(f"FAILED to send message. Error Details: {e}")

if __name__ == "__main__":
    generate_and_send()
