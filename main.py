import ccxt
import pandas as pd
import pandas_ta as ta
import requests
import os
import telebot

# --- Setup ---
bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))
CHAT_ID = os.environ.get('CHAT_ID')
exchange = ccxt.binance()

# 1. Advanced Technical Analysis Logic
def fetch_data(symbol, timeframe):
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
    df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    return df

def get_coinglass_signal(symbol):
    # Coinglass API call
    url = f"https://open-api.coinglass.com/api/pro/v1/futures/liquidation_chart?symbol={symbol}&timeType=h4"
    headers = {'coinglassSecret': os.environ.get('COINGLASS_API_KEY')}
    try:
        res = requests.get(url, headers=headers, timeout=5).json()
        return "Bullish Flow" if res['data'][0]['buyVol'] > res['data'][0]['sellVol'] else "Bearish Flow"
    except: return "Neutral"

def analyze_trade(symbol):
    df = fetch_data(symbol, '4h')
    flow = get_coinglass_signal(symbol)
    last_close = df['close'].iloc[-1]
    atr = df['atr'].iloc[-1]
    prev_high = df['high'].iloc[-2]
    
    if last_close > prev_high and flow == "Bullish Flow":
        return f"✅ BUY: {last_close} | SL: {last_close - (atr*1.5)} | TP: {last_close + (atr*3)}"
    elif last_close < df['low'].iloc[-2] and flow == "Bearish Flow":
        return f"✅ SELL: {last_close} | SL: {last_close + (atr*1.5)} | TP: {last_close - (atr*3)}"
    return "⏳ WAIT - No setup"

# 2. Simple Market Monitor Logic
def get_market_price(symbol):
    ids = {"BTC": "bitcoin", "XRP": "ripple", "SOL": "solana"}
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids[symbol]}&vs_currencies=usd"
        data = requests.get(url, timeout=5).json()
        return f"${data[ids[symbol]]['usd']:,.2f}"
    except: return "N/A"

# --- Combined Execution ---
try:
    report = "🚀 ADVANCED MARKET MONITOR & SIGNALS:\n\n"
    
    # Prices
    report += "📊 CURRENT PRICES:\n"
    for s in ['BTC', 'XRP', 'SOL']:
        report += f"🔹 {s}: {get_market_price(s)}\n"
    
    # Trade Signals
    report += "\n🎯 ADVANCED SIGNALS:\n"
    for s in ['BTC/USDT', 'SOL/USDT']:
        report += f"🔹 {s}: {analyze_trade(s)}\n"
        
    bot.send_message(CHAT_ID, report)
    print("Success: Combined report sent!")
except Exception as e:
    print(f"Error: {e}")
