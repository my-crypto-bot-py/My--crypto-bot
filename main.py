import telebot
import ccxt
import pandas as pd
import pandas_ta as ta
import os
from flask import Flask
from threading import Thread
from telebot import types

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# एक्सचेंज सेटअप
exchange = ccxt.kucoin({'enableRateLimit': True})
exchange.load_markets()

def get_volume_imbalance(symbol):
    try:
        order_book = exchange.fetch_order_book(symbol)
        bids = sum([b[1] for b in order_book['bids'][:5]])
        asks = sum([a[1] for a in order_book['asks'][:5]])
        imbalance = (bids - asks) / (bids + asks) * 100
        return f"🔥 Order Flow: {'🟢 Bullish' if imbalance > 0 else '🔴 Bearish'} ({imbalance:.1f}%)"
    except:
        return "🔥 Order Flow: N/A"

def get_market_analysis(symbol):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=200)
        df = pd.DataFrame(bars, columns=['t', 'O', 'H', 'L', 'Close', 'V'])
        df['EMA50'] = ta.ema(df['Close'], length=50)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        last = df.iloc[-1]
        curr, rsi, ema50 = float(last['Close']), float(last['RSI']), float(last['EMA50'])
        
        signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema50 and rsi > 35) else "WAIT"
        
        # ऑटो-कैलकुलेशन: Entry, SL, TP
        rr_ratio = 3.0
        sl, tp = 0.0, 0.0
        if signal == "BUY":
            sl = curr * 0.985 # 1.5% SL
            tp = curr + (curr - sl) * rr_ratio
        elif signal == "SELL":
            sl = curr * 1.015 # 1.5% SL
            tp = curr - (sl - curr) * rr_ratio
            
        flow = get_volume_imbalance(symbol)
        
        report = f"📊 *{symbol}*\n🎯 Action: {signal}\n💰 Price: {curr:.2f}"
        if signal != "WAIT":
            report += f"\n🟢 Entry: {curr:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f}"
        
        report += f"\n{flow}\n💪 RSI: {rsi:.2f}"
        return report
    except:
        return f"❌ Error in {symbol}"

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🔥 View Liquidation Heatmap", url="https://www.coinglass.com/pro/futures/LiquidationHeatMap")
    markup.add(btn)
    
    bot.reply_to(m, f"🚨 **SMC TRED UPDATE**\n\n{results}", parse_mode='Markdown', reply_markup=markup)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling()
