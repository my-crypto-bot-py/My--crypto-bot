import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import os
import time
import schedule
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "SMC Advanced Engine is Operational."

def get_indicators(df):
    df['EMA50'] = ta.ema(df['Close'], length=50)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    return df

def get_top_down_info(symbol):
    try:
        data_1w = yf.download(symbol, period='1mo', interval='1wk')
        data_5m = yf.download(symbol, period='1d', interval='5m')
        for df in [data_1w, data_5m]:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
        price_1w = float(data_1w['Close'].ffill().iloc[-1])
        price_5m = float(data_5m['Close'].ffill().iloc[-1])
        return f"📅 1W: {price_1w:.2f} | 🕒 5M: {price_5m:.2f}"
    except:
        return "TD Data N/A"

def get_market_analysis(symbol):
    try:
        data = yf.download(symbol, period='6mo', interval='1h')
        if data.empty: return f"❌ {symbol}: डेटा प्राप्त नहीं हुआ।"
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        df = get_indicators(data).dropna()
        if df.empty: return f"⚠️ {symbol}: डेटा अपर्याप्त है।"
        
        last_row = df.iloc[-1]
        curr, rsi, ema50, ema200 = float(last_row['Close']), float(last_row['RSI']), float(last_row['EMA50']), float(last_row['EMA200'])
        
        trend = "BULLISH" if curr > ema200 else "BEARISH"
        signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema200 and rsi > 35) else "WAIT"
        
        # --- RR RATIO LOGIC START ---
        is_trend = (signal == "BUY" and curr > ema200) or (signal == "SELL" and curr < ema200)
        rr_ratio = 4.5 if is_trend else 3.5  # Trend: 1:4.5, Counter: 1:3.5
        
        if signal == "BUY":
            sl = curr * 0.985 # 1.5% Risk
            tp = curr + (curr - sl) * rr_ratio
        elif signal == "SELL":
            sl = curr * 1.015 # 1.5% Risk
            tp = curr - (sl - curr) * rr_ratio
        else:
            sl, tp = 0.0, 0.0
        # --- RR RATIO LOGIC END ---

        td_data = get_top_down_info(symbol)
        report = f"📊 *{symbol} Report*\n{td_data}\n📈 Trend: {trend}\n🎯 Action: {signal}\n"
        if signal != "WAIT":
            report += f"🟢 Entry: {curr:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
        report += f"💪 RSI: {rsi:.2f}"
        return report, signal
    except Exception as e:
        return f"❌ Error in {symbol}: {str(e)}", "WAIT"

def check_and_alert():
    assets = ['BTC-USD', 'GC=F', 'SOL-USD']
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
    bot.send_message(CHAT_ID, "🦅 **SMC ADVANCED ENGINE ACTIVE**")

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    bot.reply_to(m, "⏳ *Analyzing market...*", parse_mode='Markdown')
    assets = ['BTC-USD', 'GC=F', 'SOL-USD']
    results = "\n\n".join([get_market_analysis(a)[0] for a in assets])
    bot.send_message(CHAT_ID, f"🚨 **TRED UPDATE!**\n\n{results}", parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling()
