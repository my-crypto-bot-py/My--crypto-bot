import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import os
from flask import Flask
from threading import Thread

# Railway Variables
TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "SMC Advanced Bot is Running!"

def get_indicators(df):
    # RSI, EMA, MACD Calculations
    df['EMA50'] = ta.ema(df['Close'], length=50)
    df['EMA200'] = ta.ema(df['Close'], length=200)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    macd = ta.macd(df['Close'])
    return pd.concat([df, macd], axis=1)

def get_market_analysis(symbol):
    try:
        # डेटा डाउनलोड करें
        data = yf.download(symbol, period='5d', interval='1h')
        if data.empty: return f"❌ {symbol} डेटा उपलब्ध नहीं।"
        
        # yfinance के MultiIndex एरर को ठीक करना
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
            
        df = get_indicators(data)
        
        # आखिरी वैल्यू को शुद्ध नंबर में बदलना
        curr = float(df['Close'].iloc[-1].item() if hasattr(df['Close'].iloc[-1], 'item') else df['Close'].iloc[-1])
        rsi = float(df['RSI'].iloc[-1].item() if hasattr(df['RSI'].iloc[-1], 'item') else df['RSI'].iloc[-1])
        ema50 = float(df['EMA50'].iloc[-1].item() if hasattr(df['EMA50'].iloc[-1], 'item') else df['EMA50'].iloc[-1])
        ema200 = float(df['EMA200'].iloc[-1].item() if hasattr(df['EMA200'].iloc[-1], 'item') else df['EMA200'].iloc[-1])
        
        # Trend and Signal Logic
        trend = "BULLISH" if curr > ema200 else "BEARISH"
        signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema50 and rsi > 35) else "WAIT"
        
        # Calculate SL and TP (1:2 Risk Reward)
        if signal == "BUY":
            sl = curr * 0.98
            tp = curr * 1.04
        elif signal == "SELL":
            sl = curr * 1.02
            tp = curr * 0.96
        else:
            sl, tp = 0.0, 0.0
        
        report = f"📊 *{symbol} Report*\n📈 Trend: {trend}\n🎯 Action: {signal}\n"
        if signal != "WAIT":
            report += f"🟢 Entry: {curr:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f}\n"
        report += f"💪 RSI: {rsi:.2f}"
        
        return report
    except Exception as e:
        return f"❌ Error analyzing {symbol}: {str(e)}"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(CHAT_ID, "🦅 **SMC ADVANCED ENGINE ACTIVE**")

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    bot.reply_to(m, "⏳ *Analyzing market... please wait!*", parse_mode='Markdown')
    msg1 = get_market_analysis('BTC-USD')
    msg2 = get_market_analysis('GC=F')
    bot.send_message(CHAT_ID, f"🚨 **TRED UPDATE!**\n\n{msg1}\n\n{msg2}", parse_mode='Markdown')

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling()
