import telebot
import ccxt
import os
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# एक्सचेंज सेटअप
bybit = ccxt.bybit()
binance = ccxt.binance()

def get_liquidation_data(symbol):
    results = {}
    # लिक्विडेशन डेटा के लिए एक्सचेंज के पब्लिक एंडपॉइंट्स का उपयोग
    exchanges = {'Bybit': bybit, 'Binance': binance}
    
    for name, exchange in exchanges.items():
        try:
            # लिक्विडेशन डेटा फेच करने का प्रयास (Public API)
            # नोट: कई एक्सचेंज लिक्विडेशन डेटा के लिए अलग एंडपॉइंट रखते हैं
            data = exchange.fetch_liquidations(symbol, limit=1)
            if data:
                liq = data[0]
                results[name] = f"Side: {liq['side']} | Amount: {liq['amount']} | Price: {liq['price']}"
            else:
                results[name] = "No recent liquidation"
        except Exception:
            results[name] = "Data Unavailable"
    return results

@bot.message_handler(commands=['check'])
def check_liquidation(m):
    symbol = 'BTC/USDT'
    data = get_liquidation_data(symbol)
    
    response = f"🔥 *LIQUIDATION MONITOR: {symbol}*\n\n"
    for ex, info in data.items():
        response += f"🏢 *{ex}:* {info}\n"
    
    bot.reply_to(m, response, parse_mode='Markdown')

if __name__ == "__main__":
    bot.remove_webhook()
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling(none_stop=True, drop_pending_updates=True)
