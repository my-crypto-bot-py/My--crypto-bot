import ccxt
import pandas as pd
import requests
import os
import telebot

# --- Setup ---
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
bot = telebot.TeleBot(TOKEN)
exchange = ccxt.binance()

# Manual ATR calculation
def calculate_atr(df, length=14):
    df['h-l'] = df['high'] - df['low']
    df['h-pc'] = abs(df['high'] - df['close'].shift(1))
    df['l-pc'] = abs(df['low'] - df['close'].shift(1))
    df['tr'] = df[['h-l', 'h-pc', 'l-pc']].max(axis=1)
    return df['tr'].rolling(window=length).mean()

def fetch_data(symbol, timeframe):
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
    df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
    df['atr'] = calculate_atr(df, 14)
    return df

def get_coinglass_signal(symbol):
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
    prev_low = df['low'].iloc[-2]
    
    if last_close > prev_high and flow == "Bullish Flow":
        return f"✅ BUY: {last_close:.2f} | SL: {(last_close - (atr*1.5)):.2f} | TP: {(last_close + (atr*3)):.2f}"
    elif last_close < prev_low and flow == "Bearish Flow":
        return f"✅ SELL: {last_close:.2f} | SL: {(last_close + (atr*1.5)):.2f} | TP: {(last_close - (atr*3)):.2f}"
    return "⏳ WAIT - No setup"

def get_market_price(symbol):
    ids = {"BTC": "bitcoin", "XRP": "ripple", "SOL": "solana"}
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids[symbol]}&vs_currencies=usd"
        data = requests.get(url, timeout=5).json()
        return f"${data[ids[symbol]]['usd']:,.2f}"
    except: return "N/A"

# --- COMMANDS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot is active and ready to monitor markets!")

@bot.message_handler(commands=['report'])
def manual_report(message):
    generate_and_send()

def generate_and_send():
    try:
        print("Generating report...")
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        bot.send_message(CHAT_ID, report)
        print("Success: Message sent!")
    except Exception as e:
        print(f"FAILED to send message. Error: {e}")

# --- Combined Execution ---
if __name__ == "__main__":
    # GitHub Action ke liye direct run
    generate_and_send()
