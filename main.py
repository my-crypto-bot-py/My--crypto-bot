import telebot
import os
import requests
from flask import Flask
from threading import Thread
import time

TOKEN = os.environ.get('TOKEN')
COINGLASS_API_KEY = os.environ.get('COINGLASS_API_KEY') 

app = Flask(__name__)

# बोट का ऑब्जेक्ट यहाँ न बनाकर नीचे main के अंदर बनाएंगे
bot = None

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

# Flask app route (Railway के हेल्थ चेक के लिए)
@app.route('/')
def home():
    return "Bot is running..."

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    bot = telebot.TeleBot(TOKEN)
    
    # 1. किसी भी पुराने वेबहुक को तुरंत हटा दें (Conflict से बचने के लिए)
    try:
        bot.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        print(f"Webhook error: {e}")

    # 2. Flask को अलग थ्रेड में चलाएं
    Thread(target=run_flask).start()
    
    # 3. मैसेज हैंडलर को यहाँ रजिस्टर करें ताकि बोट ऑब्जेक्ट के साथ सही जुड़ें
    @bot.message_handler(commands=['check'])
    def check_liquidation(m):
        msg = bot.reply_to(m, "🔄 Fetching...")
        info = get_liquidation_data('BTC')
        bot.edit_message_text(chat_id=m.chat.id, message_id=msg.message_id, 
                              text=f"🔥 *LIQUIDATION MONITOR: BTC*\n\n{info}", parse_mode='Markdown')
    
    print("Bot is starting polling...")
    
    # 4. इनफिनिटी पोलिंग को सुरक्षित तरीके से चलाएं
    while True:
        try:
            bot.infinity_polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5) # एरर आने पर 5 सेकंड रुकें
