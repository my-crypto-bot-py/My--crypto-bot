import telebot
import os
import requests
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN')
COINGLASS_API_KEY = os.environ.get('COINGLASS_API_KEY') 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Railway Healthcheck
@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def home():
    return "Bot is running..."

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

def run_bot():
    # Purane connections saaf karein
    bot.remove_webhook()
    # Polling shuru karein
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    # Bot ko alag thread mein chalayein (daemon=True taaki app band hone par bot bhi band ho)
    Thread(target=run_bot, daemon=True).start()
    # Flask main thread mein
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
