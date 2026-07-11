import telebot
import os
import requests
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Coinglass API से लिक्विडेशन डेटा लेने का फंक्शन
def get_liquidation_data(symbol):
    # सिंबल को coinglass फॉर्मेट में बदलें (जैसे BTC/USDT -> BTC)
    coin = symbol.split('/')[0]
    url = f"https://open-api.coinglass.com/public/v2/liquidation_data?symbol={coin}"
    
    # नोट: अगर जरूरत हो तो Coinglass API key यहाँ जोड़ें, 
    # लेकिन पब्लिक डेटा के लिए यह बिना की के भी काम करता है
    try:
        response = requests.get(url).json()
        if response['code'] == '0':
            data = response['data']
            # यहाँ हम लेटेस्ट लिक्विडेशन डेटा निकाल रहे हैं
            return f"💰 24h Liq: {data[0].get('buyOrder', 0)} Buy / {data[0].get('sellOrder', 0)} Sell"
        return "Data Unavailable"
    except Exception as e:
        return f"Error: {str(e)}"

@bot.message_handler(commands=['check'])
def check_liquidation(m):
    symbol = 'BTC/USDT'
    info = get_liquidation_data(symbol)
    
    response = f"🔥 *LIQUIDATION MONITOR: {symbol}*\n\n🏢 *Coinglass Source:*\n{info}"
    bot.reply_to(m, response, parse_mode='Markdown')

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    bot.remove_webhook()
    Thread(target=run_flask).start()
    bot.infinity_polling()
