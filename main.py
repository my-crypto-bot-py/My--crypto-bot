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
exchange = ccxt.kucoin({'enableRateLimit': True})

def get_market_analysis(symbol):
    try:
        # Timeframes: 1w, 1d, 4h (Swing/Intraday), 15m (Scalping)
        timeframes = {'1w': 100, '1d': 100, '4h': 100, '15m': 100}
        data = {}
        for tf, limit in timeframes.items():
            bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
            # कॉलम नाम सुरक्षित तरीके से सेट करना
            df = pd.DataFrame(bars, columns=['t', 'Open', 'High', 'Low', 'Close', 'Vol'])
            df['EMA200'] = ta.ema(df['Close'], length=50) 
            data[tf] = df.dropna()

        # डेटा चेक
        if any(df.empty for df in data.values()): return f"❌ {symbol}: Data Loading..."

        w1, d1, h4, m15 = data['1w'].iloc[-1], data['1d'].iloc[-1], data['4h'].iloc[-1], data['15m'].iloc[-1]
        
        # 1. SWING/INTRADAY LOGIC (Top-Down)
        highs_4h = data['4h']['Close'].rolling(20).max().iloc[-1]
        lows_4h = data['4h']['Close'].rolling(20).min().iloc[-1]
        poi = "Supply Zone" if m15['Close'] > highs_4h * 0.995 else "Demand Zone" if m15['Close'] < lows_4h * 1.005 else "Neutral"
        
        trend = "🟢 BULLISH" if m15['Close'] > h4['EMA200'] else "🔴 BEARISH"
        
        # 2. SCALPING LOGIC (Indicator-Free Price Action)
        prev_15m = data['15m'].iloc[-2]
        is_sweep = (m15['Low'] < prev_15m['Low']) or (m15['High'] > prev_15m['High'])
        
        # Reporting
        report = f"📊 *{symbol} SMC ENGINE*\n📈 Trend: {trend}\n📍 POI: {poi}\n"
        
        # Swing Setup
        if poi != "Neutral":
            rr = 6.0
            report += f"\n💎 *SWING SETUP*\nAction: {'BUY' if poi == 'Demand Zone' else 'SELL'}\n🎯 TP RR 1:{rr}"
            
        # Scalp Setup (Liquidity Sweep based)
        if is_sweep:
            rr_s = 3.0
            report += f"\n⚡ *SCALP SETUP (Sweep detected)*\nAction: {'BUY' if trend == '🟢 BULLISH' else 'SELL'}\n🎯 TP RR 1:{rr_s}"
            
        return report
    except Exception as e:
        return f"❌ Error in {symbol}: {str(e)}"

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    bot.reply_to(m, f"🚨 **SMC ELITE ENGINE**\n\n{results}", parse_mode='Markdown')

def auto_report():
    if not CHAT_ID: return
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    try: bot.send_message(CHAT_ID, f"⏰ **MARKET UPDATE**\n\n{results}", parse_mode='Markdown')
    except: pass

def run_scheduler():
    schedule.every().hour.do(auto_report)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling(none_stop=True)
