import telebot
import ccxt
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
# Bybit Exchange Setup
exchange = ccxt.bybit({'enableRateLimit': True})

def get_market_analysis(symbol):
    try:
        # 1. Price Data
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        
        # 2. Dataframes (100 कैंडल्स का डेटा लिया गया है)
        time.sleep(1.5)
        bars = exchange.fetch_ohlcv(symbol, timeframe='4h', limit=150)
        df = pd.DataFrame(bars, columns=['t', 'Open', 'High', 'Low', 'Close', 'Vol'])
        
        # 3. Order Flow Indicators (100 कैंडल्स की लिक्विडिटी के साथ)
        df['EMA200'] = ta.ema(df['Close'], length=200)
        df['EMA50'] = ta.ema(df['Close'], length=50)
        
        # Liquidity Sweep Logic (100 कैंडल्स का रोलिंग विंडो)
        high_liquidity = df['High'].rolling(100).max().iloc[-1]
        low_liquidity = df['Low'].rolling(100).min().iloc[-1]
        
        is_buy_liquidity = current_price < low_liquidity
        is_sell_liquidity = current_price > high_liquidity
        
        # Trend based on Order Flow
        trend = "🟢 BULLISH" if df['EMA50'].iloc[-1] > df['EMA200'].iloc[-1] else "🔴 BEARISH"
        
        report = f"📊 *{symbol} SMC ORDER FLOW*\n📈 Flow: {trend}\n📍 Liquidity: {'Sweep Found' if (is_buy_liquidity or is_sell_liquidity) else 'Normal'}\n"
        
        # Advanced Setup Logic
        if is_buy_liquidity and trend == "🟢 BULLISH":
            report += f"\n💎 *SMART ENTRY (BUY)*\nEntry: {current_price:.2f}\n🎯 TP: {current_price * 1.05:.2f}\n🛡 SL: {current_price * 0.97:.2f}"
        elif is_sell_liquidity and trend == "🔴 BEARISH":
            report += f"\n💎 *SMART ENTRY (SELL)*\nEntry: {current_price:.2f}\n🎯 TP: {current_price * 0.95:.2f}\n🛡 SL: {current_price * 1.03:.2f}"
        else:
            report += f"\n⏳ Status: Waiting for Order Flow Alignment"
            
        return report
    except Exception as e:
        return f"⚠️ {symbol}: Data Error"

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    bot.reply_to(m, f"🚨 **ORDER FLOW ENGINE**\n\n{results}", parse_mode='Markdown')

def auto_report():
    if not CHAT_ID: return
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    try: bot.send_message(CHAT_ID, f"⏰ **ORDER FLOW UPDATE**\n\n{results}", parse_mode='Markdown')
    except: pass

def run_scheduler():
    schedule.every().hour.do(auto_report)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    bot.remove_webhook()
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling(none_stop=True)
