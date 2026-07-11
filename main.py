import telebot
import os
import requests
from flask import Flask
from threading import Thread
import time

TOKEN = os.environ.get('TOKEN')
COINGLASS_API_KEY = os.environ.get('COINGLASS_API_KEY') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_liquidation_data(symbol):
    coin = symbol.upper()
    # यह नया PUBLIC V2 एंडपॉइंट है (यह बिना 'pro' के है, जो फ्री है)
    url = f"https://open-api.coinglass.com/public/v2/liquidation_data?symbol={coin}&timeType=24h"
    
    headers = {
        "accept": "application/json",
        "coinglassSecret": COINGLASS_API_KEY if COINGLASS_API_KEY else ""
    }
    
    try:
        response = requests.get(url, headers=headers).json()
        # रिस्पॉन्स को डीबग करने के लिए प्रिंट करें
        print(f"API Response: {response}") 
        
        # V2 का डेटा स्ट्रक्चर लिस्ट के अंदर होता है
        if response.get('code') == '0' and response.get('data'):
            data_list = response['data']
            if isinstance(data_list, list) and len(data_list) > 0:
                d = data_list[0]
                return f"🟢 Buy Liq (24h): ${d.get('buyVolUsd', '0')}\n🔴 Sell Liq (24h): ${d.get('sellVolUsd', '0')}"
        
        return "Data currently unavailable or API Key limits reached."
    except Exception as e:
        return f"Error: {str(e)}"

@bot.message_handler(commands=['check'])
def check_liquidation(m):
    msg = bot.reply_to(m, "Fetching live data from V2 API...")
    info = get_liquidation_data('BTC')
    bot.edit_message_text(chat_id=m.chat.id, message_id=msg.message_id, 
                          text=f"🔥 *LIQUIDATION MONITOR: BTC*\n\n{info}", parse_mode='Markdown')

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    try:
        bot.delete_webhook()
    except:
        pass
        
    Thread(target=run_flask).start()
    
    print("Bot is running...")
    # Polling stability के लिए none_stop=True और timeout का सही उपयोग
    bot.infinity_polling(none_stop=True, interval=2, timeout=60)
