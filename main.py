import telebot
import ccxt
import pandas as pd
import pandas_ta as ta
import os
import time
import schedule
from flask import Flask
from threading import Thread

# पर्यावरण वेरिएबल्स
TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Bybit एक्सचेंज सेटअप
exchange = ccxt.bybit()

@app.route('/')
def home():
    return "SMC Advanced Engine (Bybit Powered) is Operational."

def fetch_ohlcv(symbol, timeframe='1h', limit=200):
    """Bybit से डेटा फेच करने का फंक्शन"""
    # Bybit सिम्बल्स को CCXT फॉर्मेट में फेच करें
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return df

def get_indicators(df):
    df['EMA50'] = ta.ema(df['Close'], length=50)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    return df

def get_market_analysis(symbol):
    try:
        # डेटा फेचिंग
        df = fetch_ohlcv(symbol)
        df = get_indicators(df).dropna()
        
        last_row = df.iloc[-1]
        curr, rsi, ema50, ema200 = float(last_row['Close']), float(last_row['RSI']), float(last_row['EMA50']), float(last_row['EMA200'])
        
        trend = "BULLISH" if curr > ema200 else "BEARISH"
        signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema200 and rsi > 35) else "WAIT"
        
        # RR RATIO लॉजिक
        is_trend = (signal == "BUY" and curr > ema200) or (signal == "SELL" and curr < ema200)
        rr_ratio = 4.5 if is_trend else 3.5 
        
        if signal == "BUY":
            sl = curr * 0.985
            tp = curr + (curr - sl) * rr_ratio
        elif signal == "SELL":
            sl = curr * 1.015
            tp = curr - (sl - curr) * rr_ratio
        else:
            sl, tp = 0.0, 0.0

        report = f"📊 *{symbol} Report*\n📈 Trend: {trend}\n🎯 Action: {signal}\n"
        if signal != "WAIT":
            report += f"🟢 Entry: {curr:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
        report += f"💪 RSI: {rsi:.2f}"
        return report, signal
    except Exception as e:
        return f"❌ Error in {symbol}: {str(e)}", "WAIT"

def check_and_alert():
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT', 'XAU/USDT', 'XAG/USDT']
    for symbol in assets:
        report, signal = get_market_analysis(symbol)
        if signal != "WAIT":
            bot.send_message(CHAT_ID, f"🚨 **SIGNAL ALERT!**\n\n{report}", parse_mode='Markdown')

def run_scheduler():
    schedule.every(1).hours.do(check_and_alert)
    while True:
        schedule.run_pending()
        time.sleep(1)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(CHAT_ID, "🦅 **SMC ADVANCED ENGINE (BYBIT) ACTIVE**")

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    bot.reply_to(m, "⏳ *Analyzing market via Bybit...*", parse_mode='Markdown')
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT', 'XAU/USDT', 'XAG/USDT']
    results = "\n\n".join([get_market_analysis(a)[0] for a in assets])
    bot.send_message(CHAT_ID, f"🚨 **TRED UPDATE!**\n\n{results}", parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling()
