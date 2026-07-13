import os
import telebot

# Sirf credentials aur basic connection check
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("Error: TOKEN or CHAT_ID missing!")
    exit()

bot = telebot.TeleBot(TOKEN)

def test_connection():
    try:
        print(f"Testing connection to CHAT_ID: {CHAT_ID}")
        bot.send_message(int(CHAT_ID), "✅ Base Connection Test: Success!")
        print("Test Message sent successfully.")
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_connection()

import ccxt
import pandas as pd
import requests
import os
import telebot

# --- Setup ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
raw_chat_id = os.environ.get('CHAT_ID')
CHAT_ID = int(raw_chat_id) if raw_chat_id else None
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# --- Functions (Aapke purane functions yahan raheinge) ---
# def get_market_price(s): ...
# def analyze_trade(s): ...
import ccxt
import pandas as pd
import requests
import os
import telebot

# --- SETUP ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# --- FUNCTIONS ---

def get_market_price(s):
    try:
        ticker = exchange.fetch_ticker(f"{s}/USDT")
        return f"${ticker['last']}"
    except: return "N/A"

def analyze_trade(symbol):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=20)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
        
        # RSI Calculation
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss)))
        
        # ATR Calculation
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=14).mean().iloc[-1]
        
        rsi_val = rsi.iloc[-1]
        signal = "🟡 Wait"
        if rsi_val < 30: signal = "🟢 BUY"
        elif rsi_val > 70: signal = "🔴 SELL"
        
        return f"{signal} | RSI: {rsi_val:.1f} | ATR: {atr:.2f}"
    except: return "Error"

def get_coinglass_data(symbol):
    try:
        if symbol == 'XAU': return "N/A"
        url = f"https://open-api.coinglass.com/public/v2/liquidation_pair?pair={symbol}USDT"
        res = requests.get(url).json()
        liq = res.get('data', [{}])[0].get('liquidation', '0')
        return f"🔥 Liq: {liq}"
    except: return "N/A"

def get_market_updates():
    report = "\n💎 COINGLASS INSIGHTS:\n"
    for asset in ['BTC', 'XRP', 'SOL', 'XAU']:
        report += f"🔹 {asset}: {get_coinglass_data(asset)}\n"
    return report

def generate_and_send():
    report = "🚀 MARKET ANALYSIS (RSI + ATR):\n\n📊 PRICES:\n"
    for s in ['BTC', 'XRP', 'SOL']:
        report += f"🔹 {s}: {get_market_price(s)}\n"
    
    report += "\n🎯 SIGNALS:\n"
    for s in ['BTC/USDT', 'SOL/USDT']:
        report += f"🔹 {s}: {analyze_trade(s)}\n"
    
    report += get_market_updates()
    
    if CHAT_ID:
        bot.send_message(CHAT_ID, report)
        print("Success!")

if __name__ == "__main__":
    generate_and_send()
