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
    # इंडिकेटर्स जोड़ें
    df['EMA50'] = ta.ema(df['Close'], length=50)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    return df

def get_market_analysis(symbol):
    try:
        # डेटा डाउनलोड करें
        data = yf.download(symbol, period='5d', interval='1h')
        if data.empty:
            return f"❌ {symbol}: डेटा प्राप्त नहीं हुआ।"
        
        # MultiIndex कॉलम को फ्लैट करें
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        df = get_indicators(data)
        
        # सबसे जरूरी स्टेप: NaN वैल्यूज को हटा दें
        df = df.dropna()
        
        if df.empty:
            return f"⚠️ {symbol}: इंडिकेटर कैलकुलेशन के लिए पर्याप्त डेटा नहीं है।"

        # आखिरी उपलब्ध वैल्यू निकालें
        last_row = df.iloc[-1]
        curr = float(last_row['Close'])
        rsi = float(last_row['RSI'])
        ema50 = float(last_row['EMA50'])
        ema200 = float(last_row['EMA200'])
        
        # सिग्नल लॉजिक
        trend = "BULLISH" if curr > ema200 else "BEARISH"
        signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema50 and rsi > 35) else "WAIT"
        
        # SL/TP कैलकुलेशन
        sl, tp = 0.0, 0.0
        if signal == "BUY":
            sl, tp = curr * 0.98, curr * 1.04
        elif signal == "SELL":
            sl, tp = curr * 1.02, curr * 0.96
        
        report = f"📊 *{symbol} Report*\n📈 Trend: {trend}\n🎯 Action: {signal}\n"
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
    # यूजर को फीडबैक दें
    bot.reply_to(m, "⏳ *Analyzing market...*", parse_mode='Markdown')
    
    # एनालिसिस रन करें
    msg1 = get_market_analysis('BTC-USD')
    msg2 = get_market_analysis('GC=F')
    
    bot.send_message(CHAT_ID, f"🚨 **TRED UPDATE!**\n\n{msg1}\n\n{msg2}", parse_mode='Markdown')

if __name__ == "__main__":
    # Web server thread for Railway
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling()
