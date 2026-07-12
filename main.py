import os
import requests
import telebot

# GitHub Secrets se values fetch karein
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
API_KEY = os.environ.get('COINGLASS_API_KEY')

bot = telebot.TeleBot(TOKEN)

def get_data(symbol):
    # CoinGlass API URL
    url = f"https://open-api.coinglass.com/api/pro/v1/futures/liquidation?symbol={symbol}"
    headers = {"coinglassSecret": API_KEY}
    try:
        response = requests.get(url, headers=headers).json()
        if response['success']:
            # Liquidation data ka text format
            return f"🔥 {symbol}: ${response['data']}"
        return f"{symbol}: No Data"
    except Exception as e:
        return f"{symbol}: Error"

# Message bhejne ka logic
try:
    symbols = ['BTC', 'XRP', 'SOL', 'XAU']
    report = "🚀 LIQUIDATION MONITOR UPDATE:\n\n"
    
    for s in symbols:
        report += get_data(s) + "\n"
        
    bot.send_message(CHAT_ID, report)
    print("Success: Data sent to Telegram!")
except Exception as e:
    print(f"Error: {e}")
