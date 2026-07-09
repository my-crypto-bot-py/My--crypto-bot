import telebot
import ccxt
import pandas as pd
import pandas_ta as ta
import os
import time
import schedule
from flask import Flask
from threading import Thread
from telebot import types

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

exchange = ccxt.kucoin({'enableRateLimit': True})
exchange.load_markets()

def get_poi_status(df):
    """Simple POI Detection: Price near recent Order Block zone"""
    last_close = df['Close'].iloc[-1]
    # अगर क्लोजिंग पिछले 20 कैंडल्स के हाई/लो के पास है तो उसे POI माना जाएगा
    if last_close > df['Close'].rolling(20).max().iloc[-1] * 0.995: return "Supply Zone"
    if last_close < df['Close'].rolling(20).min().iloc[-1] * 1.005: return "Demand Zone"
    return "Neutral"

def get_market_analysis(symbol):
    try:
        timeframes = {'1w': 100, '1d': 100, '4h': 100, '5m': 100}
        data = {}
        for tf, limit in timeframes.items():
            bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=limit)
            df = pd.DataFrame(bars, columns=['t', 'O', 'H', 'L', 'Close', 'V'])
            df['EMA200'] = ta.ema(df['Close'], length=200)
            data[tf] = df

        w1, d1, h4, c5 = data['1w'].iloc[-1], data['1d'].iloc[-1], data['4h'].iloc[-1], data['5m'].iloc[-1]
        
        # POI Analysis
        poi = get_poi_status(data['4h'])
        w_liq = (c5['Close'] < w1['L']) or (c5['Close'] > w1['H'])
        d_liq = (c5['Close'] < d1['L']) or (c5['Close'] > d1['H'])
        
        trend = "🟢 BULLISH" if c5['Close'] > h4['EMA200'] else "🔴 BEARISH"
        
        # Top-down logic: Trend + Liquidity + POI
        signal = "BUY" if (trend == "🟢 BULLISH" and (w_liq or d_liq) and poi == "Demand Zone") else \
                 "SELL" if (trend == "🔴 BEARISH" and (w_liq or d_liq) and poi == "Supply Zone") else "WAIT"
        
        rr = 6.0 if (trend == "🟢 BULLISH" and signal == "BUY") or (trend == "🔴 BEARISH" and signal == "SELL") else 4.0
        
        sl = c5['Close'] * 0.985 if signal == "BUY" else c5['Close'] * 1.015
        risk = abs(c5['Close'] - sl)
        tp = c5['Close'] + (risk * rr) if signal == "BUY" else c5['Close'] - (risk * rr)

        report = f"📊 *{symbol} SMC PRO Analysis*\n📈 Trend: {trend}\n📍 POI: {poi}\n🎯 Action: {signal}"
        if signal != "WAIT":
            report += f"\n🟢 Entry: {c5['Close']:.2f}\n🔴 SL: {sl:.2f}\n🎯 TP: {tp:.2f} (RR: 1:{rr:.1f})"
        report += f"\n💎 Liquidity: {'Active' if (w_liq or d_liq) else 'Neutral'}"
        return report
    except Exception as e:
        return f"❌ Error in {symbol}: {str(e)}"

@bot.message_handler(commands=['tred'])
def trade_signal(m):
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔥 View Liquidation Heatmap", url="https://www.coinglass.com/pro/futures/LiquidationHeatMap"))
    bot.reply_to(m, f"🚨 **SMC ELITE ENGINE**\n\n{results}", parse_mode='Markdown', reply_markup=markup)

def auto_report():
    assets = ['BTC/USDT', 'SOL/USDT', 'XRP/USDT']
    results = "\n\n".join([get_market_analysis(a) for a in assets])
    bot.send_message(CHAT_ID, f"⏰ **HOURLY SMC ELITE UPDATE**\n\n{results}", parse_mode='Markdown')

def run_scheduler():
    schedule.every().hour.do(auto_report)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()
    Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling()
