import os
import requests
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def get_market_data(symbol):
    try:
        # CryptoCompare Public API (No key needed)
        url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if 'USD' in data:
            return f"🔹 {symbol}: ${data['USD']:,.2f}"
        return f"🔹 {symbol}: Data Unavailable"
    except Exception as e:
        return f"🔹 {symbol}: Connection Failed"

try:
    symbols = ['BTC', 'XRP', 'SOL']
    report = "🚀 MARKET MONITOR UPDATE:\n\n"
    for s in symbols:
        report += get_market_data(s) + "\n"
    bot.send_message(CHAT_ID, report)
    print("Success: Data sent!")
except Exception as e:
    print(f"Main Error: {e}")
