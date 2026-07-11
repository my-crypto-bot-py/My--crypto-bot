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
    # CoinGlass का सही एंडपॉइंट
    url = f"https://open-api.coinglass.com/api/pro/v1/futures/liquidation_chart?symbol={coin}"
    
    headers = {
        "coinglassSecret": COINGLASS_API_KEY # Railway Variable से की उठाएगा
    }
    
    try:
        response = requests.get(url, headers=headers).json()
        # डेटा के लिए रिस्पॉन्स चेक करें
        if response.get('code') == '0' and response.get('data'):
            data = response['data']
            # चार्ट डेटा में से लेटेस्ट वैल्यू निकालें
            return f"🟢 Buy Liq (24h): ${data.get('buyVol', 'N/A')}\n🔴 Sell Liq (24h): ${data.get('sellVol', 'N/A')}"
        
        return f"Data Error: {response.get('msg', 'Unavailable')}"
    except Exception as e:
        return f"Error: {str(e)}"

@bot.message_handler(commands=['check'])
def check_liquidation(m):
    msg = bot.reply_to(m, "Fetching live liquidation data...")
    info = get_liquidation_data('BTC')
    
    response = f"🔥 *LIQUIDATION MONITOR: BTC*\n\n{info}"
    bot.edit_message_text(chat_id=m.chat.id, message_id=msg.message_id, text=response, parse_mode='Markdown')

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    # 409 Conflict एरर रोकने के लिए Webhook हटाना जरूरी है
    try:
        bot.remove_webhook()
    except:
        pass
        
    Thread(target=run_flask).start()
    print("Bot is running...")
    
    # none_stop=True जोड़ने से बोट क्रैश नहीं होगा
    bot.infinity_polling(none_stop=True, timeout=30)
