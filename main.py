import os
import requests
import telebot

# GitHub Secrets se values fetch karein
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
API_KEY = os.environ.get('COINGLASS_API_KEY')

bot = telebot.TeleBot(TOKEN)

def get_data(symbol):
    # CoinGlass API Endpoint
    url = f"https://open-api.coinglass.com/api/pro/v1/futures/liquidation?symbol={symbol}"
    headers = {"coinglassSecret": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Data milne par return karein
                return f"🔥 {symbol}: {data['data']}"
            else:
                # API error message dikhayein
                return f"{symbol}: Error - {data.get('msg', 'Unknown')}"
        else:
            return f"{symbol}: HTTP Error {response.status_code}"
    except Exception as e:
        return f"{symbol}: Connection Failed"

# Bot Logic
try:
    symbols = ['BTC', 'XRP', 'SOL', 'XAU']
    report = "🚀 LIQUIDATION MONITOR UPDATE:\n\n"
    
    for s in symbols:
        report += get_data(s) + "\n"
        
    bot.send_message(CHAT_ID, report)
    print("Success: Report sent to Telegram!")
except Exception as e:
    print(f"Main Error: {e}")
