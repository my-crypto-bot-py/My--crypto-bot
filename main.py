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

def get_market_analysis(symbol):
    try:
        # Top-Down Analysis के लिए अलग-अलग टाइमफ्रेम
        data_1d = yf.download(symbol, period='1mo', interval='1d')
        data_1h = yf.download(symbol, period='5d', interval='1h')
        data_5m = yf.download(symbol, period='1d', interval='5m')

        # डेटा साफ करें
        for df in [data_1d, data_1h, data_5m]:
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        # ट्रेंड निर्धारण
        curr = float(data_1h['Close'].iloc[-1])
        ema200 = float(ta.ema(data_1h['Close'], length=200).iloc[-1])
        
        # Top-Down Logic
        trend_daily = "🐂 BULLISH" if data_1d['Close'].iloc[-1] > data_1d['Close'].iloc[-30] else "🐻 BEARISH"
        trend_hourly = "🐂 BULLISH" if curr > ema200 else "🐻 BEARISH"
        
        # सिग्नल लॉजिक
        rsi = float(ta.rsi(data_1h['Close'], length=14).iloc[-1])
        signal = "BUY" if (curr > ema200 and rsi < 60) else "SELL" if (curr < ema200 and rsi > 40) else "WAIT"
        
        # SL/TP
        sl = curr * 0.97 if signal == "BUY" else curr * 1.03
        tp = curr * 1.06 if signal == "BUY" else curr * 0.94
        
        report = (f"📊 *{symbol} Advanced Report*\n"
                  f"📅 Daily Trend: {trend_daily}\n"
                  f"🕒 Hourly Trend: {trend_hourly}\n"
                  f"🎯 Action: {signal}\n"
                  f"🟢 Entry: {curr:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
                  f"💪 RSI: {rsi:.2f}")
        return report
    except Exception as e:
        return f"❌ Error {symbol}: {str(e)}"

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    bot.reply_to(m, "📡 *Scanning Multi-Timeframe...*", parse_mode='Markdown')
    # अब BTC, Gold और Solana तीनों का एनालिसिस
    assets = ['BTC-USD', 'GC=F', 'SOL-USD']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    bot.send_message(CHAT_ID, f"🚨 **LIVE MARKET UPDATE**\n\n{results}", parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling()
