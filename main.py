import os
import requests
import telebot

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

def get_market_data(symbol):
    try:
        # CryptoCompare API call
        url = f"https://min-api.cryptocompare.com/data/price?fsym={symbol}&tsyms=USD"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Yahan hum check kar rahe hain ki data mein kya hai
        if data and 'USD' in data:
            return f"🔹 {symbol}: ${data['USD']:,.2f}"
        else:
            # Agar USD nahi mila, toh poora data return karenge takki hum samajh sakein
            return f"🔹 {symbol}: Raw Data={data}"
            
    except Exception as e:
        return f"🔹 {symbol}: Error {str(e)}"

try:
    symbols = ['BTC', 'XRP', 'SOL']
    report = "🚀 DEBUG MODE UPDATE:\n\n"
    for s in symbols:
        report += get_market_data(s) + "\n"
    bot.send_message(CHAT_ID, report)
except Exception as e:
    print(f"Main Error: {e}")
