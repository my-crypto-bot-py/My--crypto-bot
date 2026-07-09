import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import os
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
        
        price_1w = float(data_1w['Close'].iloc[-1])
        price_5m = float(data_5m['Close'].iloc[-1])
        
        return f"📅 1W Price: {price_1w:.2f} | 🕒 5M Price: {price_5m:.2f}"
    except Exception as e:
        return "TD Data N/A"

def get_market_analysis(symbol):
    try:
        # यहाँ period बदल दिया गया है (6mo)
        data = yf.download(symbol, period='6mo', interval='1h')
        if data.empty:
            return f"❌ {symbol}: डेटा प्राप्त नहीं हुआ।"
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        df = get_indicators(data)
        df = df.dropna()
        
        if df.empty:
            return f"⚠️ {symbol}: इंडिकेटर के लिए पर्याप्त डेटा नहीं है।"

        last_row = df.iloc[-1]
        curr = float(last_row['Close'])
        rsi = float(last_row['RSI'])
        ema50 = float(last_row['EMA50'])
        ema200 = float(last_row['EMA200'])
        
        trend = "BULLISH" if curr > ema200 else "BEARISH"
        signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema200 and rsi > 35) else "WAIT"
        
        sl, tp = (0.0, 0.0)
        if signal == "BUY":
            sl, tp = curr * 0.98, curr * 1.04
        elif signal == "SELL":
            sl, tp = curr * 1.02, curr * 0.96
        
        td_data = get_top_down_info(symbol)
        
        report = f"📊 *{symbol} Report*\n{td_data}\n📈 Trend: {trend}\n🎯 Action: {signal}\n"
        if signal != "WAIT":
            report += f"🟢 Entry: {curr:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
        report += f"💪 RSI: {rsi:.2f}"
        
        return report
    except Exception as e:
        return f"❌ Error in {symbol}: {str(e)}"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(CHAT_ID, "🦅 **SMC ADVANCED ENGINE ACTIVE**")

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    bot.reply_to(m, "⏳ *Analyzing market...*", parse_mode='Markdown')
    assets = ['BTC-USD', 'GC=F', 'SOL-USD']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    bot.send_message(CHAT_ID, f"🚨 **TRED UPDATE!**\n\n{results}", parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling()
