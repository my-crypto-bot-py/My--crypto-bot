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

def generate_and_send():
    try:
        report = "🚀 ADVANCED MARKET MONITOR:\n\n📊 PRICES:\n"
        for s in ['BTC', 'XRP', 'SOL']:
            report += f"🔹 {s}: {get_market_price(s)}\n"
        report += "\n🎯 SIGNALS:\n"
        for s in ['BTC/USDT', 'SOL/USDT']:
            report += f"🔹 {s}: {analyze_trade(s)}\n"
        
        if CHAT_ID:
            bot.send_message(CHAT_ID, report)
            print(f"Success: Message sent to {CHAT_ID}!")
    except Exception as e:
        print(f"FAILED to send message: {e}")

if __name__ == "__main__":
    # GitHub Action ise har ghante chalayega, humein sirf ek baar report bhejni hai.
    generate_and_send()
# --- COINGLASS DATA MODULE ---

def get_coinglass_data(symbol):
    """
    CoinGlass API se Liquidation aur Order Flow data fetch karne ka function.
    """
    # Note: CoinGlass Public API ke endpoints
    headers = {
        'coinglassSecret': 'PASTE_YOUR_COINGLASS_API_KEY_IF_YOU_HAVE' # Agar free use kar rahe hain toh header ki zaroorat nahi hoti
    }
    
    try:
        # Liquidation Data (Heatmap mock/public)
        liq_url = f"https://open-api.coinglass.com/public/v2/liquidation_pair?pair={symbol}USDT"
        liq_res = requests.get(liq_url).json()
        
        # Order Book / Order Flow summary
        order_url = f"https://open-api.coinglass.com/public/v2/order_book?pair={symbol}USDT"
        order_res = requests.get(order_url).json()
        
        # Data processing
        liq_val = liq_res['data'][0]['liquidation'] if 'data' in liq_res else "N/A"
        order_val = order_res['data']['buyVol'] if 'data' in order_res else "N/A"
        
        return f"🔥 Liq: {liq_val} | 📊 Flow: {order_val}"
    
    except Exception as e:
        return "Data Fetch Error"

def get_market_updates():
    """
    Yeh function aapke main report mein add hoga.
    """
    assets = ['BTC', 'XRP', 'SOL', 'XAU'] # XAU (Gold) ke liye pair check karein
    report = "\n💎 COINGLASS INSIGHTS:\n"
    for asset in assets:
        data = get_coinglass_data(asset)
        report += f"🔹 {asset}: {data}\n"
    return report

# --- UPDATE GENERATE_AND_SEND FUNCTION ---
# Apne purane generate_and_send mein niche wali line add karein:
# report += get_market_updates()
