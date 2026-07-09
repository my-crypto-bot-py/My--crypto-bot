import telebot
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import os
from flask import Flask
from threading import Thread

# Railway Variables से टोकन और चैट आईडी लेंगे
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
    df = pd.concat([df, macd], axis=1)
    return df

def get_market_analysis(symbol):
    df = yf.download(symbol, period='5d', interval='1h')
    if df.empty: return f"❌ {symbol} डेटा उपलब्ध नहीं।"
    
    df = get_indicators(df)
    curr = df['Close'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    ema50 = df['EMA50'].iloc[-1]
    ema200 = df['EMA200'].iloc[-1]
    
    # SMC + Indicators Logic
    trend = "BULLISH" if curr > ema200 else "BEARISH"
    signal = "BUY" if (curr > ema50 and rsi < 65) else "SELL" if (curr < ema50 and rsi > 35) else "WAIT"
    
    return f"📊 *{symbol} Report*\n📈 Trend: {trend}\n🎯 Action: {signal}\n💪 RSI: {rsi:.2f}\n💰 Current Price: {curr:.2f}"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(CHAT_ID, "🦅 **SMC ADVANCED ENGINE ACTIVE**")

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    msg = get_market_analysis('BTC-USD') + "\n\n" + get_market_analysis('GC=F')
    bot.send_message(CHAT_ID, f"🚨 **TRED MILA!**\n\n{msg}", parse_mode='Markdown')

@bot.message_handler(commands=['updates'])
def updates(m):
    bot.send_message(CHAT_ID, "🔄 **SYSTEM MONITORING...**")

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    bot.infinity_polling()
