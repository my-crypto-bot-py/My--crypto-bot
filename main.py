import telebot
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

TOKEN = '8904166729:AAGXAXHqBC452xAixkcLz1xhU7eg27eyGeQ'
bot = telebot.TeleBot(TOKEN)

# 1. ICT Killzone Logic
def get_killzone():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    hr = now.hour + (now.minute / 60)
    if 12.5 <= hr <= 14.5: return "London Killzone 🇬🇧"
    if 17.5 <= hr <= 19.5: return "New York Killzone 🇺🇸"
    if 20.5 <= hr <= 21.5: return "London Close 🕒"
    return None

# 2. SMC/ICT Professional Engine
def smc_ict_analysis(df):
    high = df['high'].max()
    low = df['low'].min()
    eq = (high + low) / 2
    current_price = df['close'].iloc[-1]
    zone = "DISCOUNT (BUYING ZONE)" if current_price < eq else "PREMIUM (SELLING ZONE)"
    liquidity_sweep = "Detected" if df['low'].iloc[-1] < df['low'].rolling(20).min().iloc[-2] else "None"
    rr = "1:6 (Trend Following)" if zone == "DISCOUNT" else "1:4 (Counter-Trend)"
    return f"📊 ANALYSIS:\nZone: {zone}\nEquilibrium: {eq:.2f}\nLiquidity Sweep: {liquidity_sweep}\nSuggested RR: {rr}"

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "🦅 SMC + ICT RENDER ENGINE LIVE! ✅")

@bot.message_handler(commands=['tred'])
def trade(m):
    df = pd.DataFrame({'high': [100, 105, 102], 'low': [95, 98, 97], 'close': [99, 103, 101]})
    kz = get_killzone()
    analysis = smc_ict_analysis(df)
    bot.reply_to(m, f"🚨 {kz if kz else 'Outside Killzone'}\n\n{analysis}")

bot.polling()
