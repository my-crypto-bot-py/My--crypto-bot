import telebot
import os
import requests
from flask import Flask
from threading import Thread
import time

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Coinglass API का नया स्ट्रक्चर
def get_liquidation_data(symbol):
    coin = symbol.split('/')[0]
    # CoinGlass का नया पब्लिक एंडपॉइंट
    url = f"https://open-api.coinglass.com/public/v2/liquidation_data?symbol={coin}&timeType=24h"
    
    try:
        # Headers जोड़ना जरूरी है ताकि API ब्लॉक न करे
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers).json()
        
        if response.get('code') == '0' and response.get('data'):
            # डेटा लिस्ट में होता है, सुरक्षित तरीके से निकालें
            liq_list = response['data']
            if len(liq_list) > 0:
                d = liq_list[0]
                return f"🟢 Buy Liq: {d.get('buyVolUsd', '0')} \n🔴 Sell Liq: {d.get('sellVolUsd', '0')}"
        return "Data currently unavailable"
    except Exception as e:
        return f"API Error: {str(e)}"

@bot.message_handler(commands=['check'])
def check_liquidation(m):
    # प्रोसेसिंग का मैसेज भेजें
    msg = bot.reply_to(m, "Fetching data from Coinglass...")
    symbol = 'BTC'
    info = get_liquidation_data(symbol)
    
    response = f"🔥 *LIQUIDATION MONITOR: {symbol}*\n\n{info}"
    bot.edit_message_text(chat_id=m.chat.id, message_id=msg.message_id, text=response, parse_mode='Markdown')

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # Flask सर्वर शुरू करें
    Thread(target=run_flask).start()
    
    # बोट को रन करें
    print("Bot is running...")
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            time.sleep(5) # एरर आने पर 5 सेकंड रुकें और फिर दोबारा शुरू करें
