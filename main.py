import os
import requests
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def get_market_data(symbol):
    try:
        # CoinGecko Public API (No key needed)
        # BTC, XRP, SOL ke liye id map karni padti hai
        ids = {"BTC": "bitcoin", "XRP": "ripple", "SOL": "solana"}
        coin_id = ids.get(symbol)
        
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if coin_id in data:
            price = data[coin_id]['usd']
            return f"🔹 {symbol}: ${price:,.2f}"
        return f"🔹 {symbol}: Data Unavailable"
    except Exception as e:
        return f"🔹 {symbol}: Error"

try:
    symbols = ['BTC', 'XRP', 'SOL']
    report = "🚀 MARKET MONITOR UPDATE:\n\n"
    for s in symbols:
        report += get_market_data(s) + "\n"
    bot.send_message(CHAT_ID, report)
    print("Success: Data sent!")
except Exception as e:
    print(f"Main Error: {e}")
