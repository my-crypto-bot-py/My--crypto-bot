import telebot
import os
import requests
from flask import Flask
from threading import Thread
import time

TOKEN = os.environ.get('TOKEN')
# ध्यान दें: हेडर की Key का नाम सही होना चाहिए
COINGLASS_API_KEY = os.environ.get('COINGLASS_API_KEY') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_liquidation_data(symbol):
    coin = symbol.upper()
    url = f"https://open-api.coinglass.com/public/v2/liquidation_data?symbol={coin}&timeType=24h"
    
    # कोइनग्लास की नई पब्लिक API के लिए सही हेडर
    headers = {
        "accept": "application/json",
        "coinglass-api-key": COINGLASS_API_KEY if COINGLASS_API_KEY else ""
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10).json()
        print(f"API Debug: {response}") # लॉग्स में चेक करने के लिए
        
        if response.get('code') == '0':
            data_list = response.get('data', [])
            if data_list and isinstance(data_list, list):
                d = data_list[0]
                return f"🟢 Buy Liq (24h): ${d.get('buyVolUsd', '0')}\n🔴 Sell Liq (24h): ${d.get('sellVolUsd', '0')}"
            return "No liquidation data available for this pair."
        else:
            return f"API Error: {response.get('msg', 'Unknown error')}"
            
    except Exception as e:
        return f"System Error: {str(e)}"

@bot.message_handler(commands=['check'])
def check_liquidation(m):
    msg = bot.reply_to(m, "🔄 Fetching...")
    info = get_liquidation_data('BTC')
    bot.edit_message_text(chat_id=m.chat.id, message_id=msg.message_id, 
                          text=f"🔥 *LIQUIDATION MONITOR: BTC*\n\n{info}", parse_mode='Markdown')

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # पुराने वेबहुक हटाना और पेंडिंग अपडेट्स को ड्रॉप करना ताकि 409 एरर न आए
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except:
        pass
        
    Thread(target=run_flask).start()
    
    print("Bot is running...")
    while True:
        try:
            bot.infinity_polling(none_stop=True, interval=1, timeout=30)
        except Exception as e:
            time.sleep(5) # क्रैश होने पर 5 सेकंड का ब्रेक लें
