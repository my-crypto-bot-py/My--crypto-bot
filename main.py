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

# मार्केट लोड करना जरूरी है ताकि एक्सचेंज डेटा फेच कर सके
bybit.load_markets()
binance.load_markets()

def get_liquidation_data(symbol):
    results = {}
    exchanges = {'Bybit': bybit, 'Binance': binance}
    
    for name, exchange in exchanges.items():
        try:
            # लिक्विडेशन डेटा फेच करना
            data = exchange.fetch_liquidations(symbol, limit=1)
            if data:
                liq = data[0]
                results[name] = f"Side: {liq['side']} | Amt: {liq['amount']} | Price: {liq['price']}"
            else:
                results[name] = "No recent liquidation"
        except Exception as e:
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

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    bot.remove_webhook()
    # Flask को अलग थ्रेड में चलाएं
    Thread(target=run_flask).start()
    # बिना किसी पैरामीटर के infinity_polling चलाएं ताकि कोई एरर न आए
    bot.infinity_polling()
