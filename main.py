import os
import requests
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def get_binance_data(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            price = data['lastPrice']
            change = data['priceChangePercent']
            return f"🔹 {symbol}: ${float(price):,.2f} ({change}%)"
        else:
            # Ye error logs mein print hoga
            print(f"Error for {symbol}: {response.status_code} - {response.text}")
            return f"🔹 {symbol}: Error {response.status_code}"
    except Exception as e:
        print(f"Exception for {symbol}: {e}")
        return f"🔹 {symbol}: Connection Failed"

try:
    symbols = ['BTC', 'XRP', 'SOL']
    report = "🚀 MARKET MONITOR UPDATE:\n\n"
    for s in symbols:
        report += get_binance_data(s) + "\n"
    bot.send_message(CHAT_ID, report)
    print("Success: Message sent!")
except Exception as e:
    print(f"Main Error: {e}")
