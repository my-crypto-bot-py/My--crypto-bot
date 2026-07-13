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

# Timeout aur connection retry settings
exchange = ccxt.binance({'timeout': 30000, 'enableRateLimit': True})

# --- FUNCTIONS ---

def get_market_price(s):
    try:
        ticker = exchange.fetch_ticker(f"{s}/USDT")
        price = ticker.get('last')
        return f"${float(price):,.2f}"
    except Exception as e:
        return f"Err: {type(e).__name__}"

def analyze_trade(symbol):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=25)
        df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'vol'])
        
        # RSI Calculation
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss)))
        
        # ATR Calculation
        df['tr'] = pd.concat([df['high']-df['low'], abs(df['high']-df['close'].shift()), abs(df['low']-df['close'].shift())], axis=1).max(axis=1)
        atr = df['tr'].rolling(window=14).mean().iloc[-1]
        
        rsi_val = rsi.iloc[-1]
        signal = "🟡 Neutral"
        if rsi_val < 30: signal = "🟢 BUY"
        elif rsi_val > 70: signal = "🔴 SELL"
        
        return f"{signal} | RSI: {rsi_val:.0f} | ATR: {atr:.2f}"
    except Exception as e:
        return f"Err: {type(e).__name__}"

def get_coinglass_data(symbol):
    try:
        if symbol == 'XAU': return "Manual"
        # Public API request
        url = f"https://open-api.coinglass.com/public/v2/liquidation_pair?pair={symbol}USDT"
        res = requests.get(url, timeout=10).json()
        data = res.get('data', [])
        return f"🔥 Liq: {data[0].get('liquidation', '0')}" if data else "No Data"
    except: return "Conn Err"

def generate_and_send():
    try:
        report = "<b>🚀 MARKET ANALYSIS (RSI + ATR)</b>\n\n<b>📊 PRICES:</b>\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        
        report += "\n<b>🎯 SIGNALS (1H):</b>\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        report += "\n<b>💎 COINGLASS INSIGHTS:</b>\n"
        for s in ['BTC', 'XRP', 'SOL', 'XAU']:
            report += f"🔹 {s}: {get_coinglass_data(s)}\n"
        
        if CHAT_ID:
            bot.send_message(CHAT_ID, report, parse_mode='HTML')
            print("Success!")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    generate_and_send()

