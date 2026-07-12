import os
import requests
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

# Binance se price aur 24h change lene ka logic (Binance public hai, no API key needed)
def get_binance_data(symbol):
    try:
        # Ticker price endpoint
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        response = requests.get(url).json()
        
        # Price aur price change percentage
        price = response['lastPrice']
        change = response['priceChangePercent']
        return f"🔹 {symbol}: ${float(price):,.2f} ({change}%)"
    except Exception as e:
        return f"🔹 {symbol}: Data Error"

try:
    symbols = ['BTC', 'XRP', 'SOL'] # XAU (Gold) Binance par nahi hai
    report = "🚀 MARKET MONITOR UPDATE:\n\n"
    
    for s in symbols:
        report += get_binance_data(s) + "\n"
        
    bot.send_message(CHAT_ID, report)
    print("Success: Market data sent!")
except Exception as e:
    print(f"Error: {e}")
