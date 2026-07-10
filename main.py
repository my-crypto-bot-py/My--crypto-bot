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
        # 1. सुरक्षित तरीके से लाइव प्राइस फेच करें
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']
        
        # 2. BTC Trend (थोड़ा delay ताकि API क्रैश न हो)
        time.sleep(1.5)
        btc_bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='4h', limit=50)
        btc_df = pd.DataFrame(btc_bars, columns=['t', 'Open', 'High', 'Low', 'Close', 'Vol'])
        btc_trend = "🟢 BULLISH" if btc_df['Close'].iloc[-1] > btc_df['Close'].rolling(50).mean().iloc[-1] else "🔴 BEARISH"

        # 3. डेटा लोड करना
        time.sleep(1.5)
        bars_4h = exchange.fetch_ohlcv(symbol, timeframe='4h', limit=50)
        df_4h = pd.DataFrame(bars_4h, columns=['t', 'Open', 'High', 'Low', 'Close', 'Vol'])
        df_4h['EMA200'] = ta.ema(df_4h['Close'], length=50)
        
        time.sleep(1.5)
        bars_15m = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=50)
        df_15m = pd.DataFrame(bars_15m, columns=['t', 'Open', 'High', 'Low', 'Close', 'Vol'])
        
        if df_4h.empty or df_15m.empty: return f"❌ {symbol}: Data error"

        h4 = df_4h.iloc[-1]
        
        # 4. Logic
        highs_4h = df_4h['Close'].rolling(20).max().iloc[-1]
        lows_4h = df_4h['Close'].rolling(20).min().iloc[-1]
        poi = "Supply Zone" if current_price > highs_4h * 0.995 else "Demand Zone" if current_price < lows_4h * 1.005 else "Neutral"
        trend = "🟢 BULLISH" if current_price > h4['EMA200'] else "🔴 BEARISH"
        
        prev_15m = df_15m.iloc[-2]
        is_sweep = (current_price < prev_15m['Low']) or (current_price > prev_15m['High'])
        
        report = f"📊 *{symbol} SMC ENGINE*\n📈 Trend: {trend} (BTC: {btc_trend})\n📍 POI: {poi}\n"
        
        # Swing Setup
        if poi != "Neutral":
            action = 'BUY' if (poi == 'Demand Zone' and btc_trend == "🟢 BULLISH") else \
                     'SELL' if (poi == 'Supply Zone' and btc_trend == "🔴 BEARISH") else "WAIT"
            if action != "WAIT":
                sl = current_price * 0.98 if action == 'BUY' else current_price * 1.02
                tp = current_price + (abs(current_price - sl) * 6) if action == 'BUY' else current_price - (abs(current_price - sl) * 6)
                report += f"\n💎 *SWING SETUP*\nAction: {action}\nEntry: {current_price:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f} (RR 1:6)"
            
        # Scalp Setup
        if is_sweep:
            action = 'BUY' if (trend == "🟢 BULLISH" and btc_trend == "🟢 BULLISH") else \
                     'SELL' if (trend == "🔴 BEARISH" and btc_trend == "🔴 BEARISH") else "WAIT"
            if action != "WAIT":
                sl = current_price * 0.99 if action == 'BUY' else current_price * 1.01
                tp = current_price + (abs(current_price - sl) * 3) if action == 'BUY' else current_price - (abs(current_price - sl) * 3)
                report += f"\n⚡ *SCALP SETUP*\nAction: {action}\nEntry: {current_price:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f} (RR 1:3)"
            
        return report if ("SWING" in report or "SCALP" in report) else f"📉 {symbol}: Waiting..."
    except Exception as e:
        return f"⚠️ {symbol}: Retrying..."

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
    # Conflict एरर को रोकने के लिए यह लाइन सबसे जरूरी है
    bot.remove_webhook()
    
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling(none_stop=True)
