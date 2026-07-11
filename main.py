import telebot
import os
import requests
from flask import Flask
from threading import Thread
import time

# रेलवे वेरिएबल से सीधे टोकन लोड करें
TOKEN = os.environ.get('TOKEN')
COINGLASS_API_KEY = os.environ.get('COINGLASS_API_KEY') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def get_liquidation_data(symbol):
    coin = symbol.upper()
    url = f"https://open-api.coinglass.com/public/v2/liquidation_data?symbol={coin}&timeType=24h"
    
    headers = {
        "accept": "application/json",
        "coinglass-api-key": COINGLASS_API_KEY if COINGLASS_API_KEY else ""
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10).json()
        if response.get('code') == '0':
            data_list = response.get('data', [])
            if data_list and isinstance(data_list, list):
                d = data_list[0]
                return f"🟢 Buy Liq (24h): ${d.get('buyVolUsd', '0')}\n🔴 Sell Liq (24h): ${d.get('sellVolUsd', '0')}"
            return "No data for this pair."
        return f"API Error: {response.get('msg', 'Error')}"
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
    # पुराने वेबहुक और पेंडिंग अपडेट्स को पूरी तरह साफ़ करना
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        print(f"Webhook error: {e}")
        
    Thread(target=run_flask).start()
    
    print("Bot is starting...")
    # Polling stability
    bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=60)
