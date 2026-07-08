
import time
import requests
import telebot
import threading
import numpy as np
from datetime import datetime

TOKEN = "8904166729:AAGXAXHqBC452xAixkcLz1xhU7eg27eyGeQ"
CHAT_ID = "5125912823"
bot = telebot.TeleBot(TOKEN, threaded=False, num_threads=1)

SYMBOLS = ["BTCUSDT", "XAUUSDT"]
ACTIVE_OB_MATRIX = {s: [] for s in SYMBOLS}
ACTIVE_FVG_MATRIX = {s: [] for s in SYMBOLS}
LIQUIDITY_VOIDS = {s: [] for s in SYMBOLS}

def get_public_klines(symbol, interval, limit=100):
    base_url = "https://api.binance.com/api/v3/klines"
    if symbol == "XAUUSDT":
        symbol = "PAXGUSDT"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        response = requests.get(base_url, params=params, timeout=12)
        if response.status_code == 200: 
            return response.json()
    except:
        pass
    return None

def is_silver_bullet_hour():
    current_hour = datetime.utcnow().hour
    return current_hour in [3, 10, 14]

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1: return [50] * len(prices)
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100. / (1. + rs)
    for i in range(period, len(prices)):
        delta = deltas[i - 1]
        if delta > 0: upval, downval = delta, 0.
        else: upval, downval = 0., -delta
        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)
    return rsi.tolist()

def analyze_institutional_matrix(symbol):
    global ACTIVE_OB_MATRIX, ACTIVE_FVG_MATRIX, LIQUIDITY_VOIDS
    d_data = get_public_klines(symbol, "1D", 15)
    h4_data = get_public_klines(symbol, "4h", 35)
    if not (d_data and h4_data): return None
    cp = float(h4_data[-1][4])
    d_b = float(d_data[-1][4]) > float(d_data[-2][4])
    h4_b = float(h4_data[-1][4]) > float(h4_data[-2][4])
    bias = "STRONG_BULLISH" if (d_b and h4_b) else ("STRONG_BEARISH" if (not d_b and not h4_b) else "NEUTRAL")
    highs = [float(x[2]) for x in h4_data]
    lows = [float(x[3]) for x in h4_data]
    swing_high, swing_low = max(highs[:-1]), min(lows[:-1])
    eq_level = (swing_high + swing_low) / 2
    discount_zone = cp < eq_level
    premium_zone = cp > eq_level
    
    for i in range(len(h4_data)-3, 1, -1):
        c_prev, o_prev = float(h4_data[i][4]), float(h4_data[i][1])
        c_next = float(h4_data[i+1][4])
        if c_prev < o_prev and c_next > o_prev:
            ob = {"type": "BULLISH_OB", "high": float(h4_data[i][2]), "low": float(h4_data[i][3])}
            if ob not in ACTIVE_OB_MATRIX[symbol]: ACTIVE_OB_MATRIX[symbol].append(ob)
        elif c_prev > o_prev and c_next < o_prev:
            ob = {"type": "BEARISH_OB", "high": float(h4_data[i][2]), "low": float(h4_data[i][3])}
            if ob not in ACTIVE_OB_MATRIX[symbol]: ACTIVE_OB_MATRIX[symbol].append(ob)
    
    ACTIVE_OB_MATRIX[symbol] = [ob for ob in ACTIVE_OB_MATRIX[symbol] if not (ob["type"] == "BULLISH_OB" and cp < ob["low"]) and not (ob["type"] == "BEARISH_OB" and cp > ob["high"])]
    return {
        "symbol": symbol, "bias": bias, "discount_zone": discount_zone, "premium_zone": premium_zone, 
        "swing_high": swing_high, "swing_low": swing_low,
        "htf_ob": ACTIVE_OB_MATRIX[symbol][-1] if ACTIVE_OB_MATRIX[symbol] else None, "current_price": cp
    }

def check_ltf_signals(matrix):
    symbol = matrix["symbol"]
    m5_data = get_public_klines(symbol, "5m", 40)
    m1_data = get_public_klines(symbol, "1m", 40)
    if not m5_data or not m1_data: return None
    cp = float(m1_data[-1][4])
    m5_closes = [float(x[4]) for x in m5_data]
    rsi_vals = calculate_rsi(m5_closes)

    if cp > matrix["swing_high"] and len(rsi_vals) > 0 and rsi_vals[-1] > 65:
        sl = cp * 1.0025
        return {"side": "SELL", "type": "SMC_SWING_HIGH_LIQ_HUNT", "entry": cp, "sl": sl, "tp": cp - ((sl - cp) * 5), "rr": "1:5"}
    if cp < matrix["swing_low"] and len(rsi_vals) > 0 and rsi_vals[-1] < 35:
        sl = cp * 0.9975
        return {"side": "BUY", "type": "SMC_SWING_LOW_LIQ_HUNT", "entry": cp, "sl": sl, "tp": cp + ((cp - sl) * 5), "rr": "1:5"}
    return None

def core_scanner():
    while True:
        for symbol in SYMBOLS:
            try:
                matrix = analyze_institutional_matrix(symbol)
                if matrix:
                    signal = check_ltf_signals(matrix)
                    if signal:
                        msg = f"⚡ *SMC/ICT SIGNAL* ⚡\n\nAsset: {symbol}\nType: {signal['type']}\nDirection: {signal['side']}\nEntry: {signal['entry']:.2f}\nSL: {signal['sl']:.2f}\nTP: {signal['tp']:.2f}"
                        try: bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                        except: pass
                        time.sleep(60)
                time.sleep(3)
            except: time.sleep(4)

@bot.message_handler(commands=['start'])
def welcome(message):
    try: bot.reply_to(message, "🦅 *SMC + ICT RENDER ENGINE LIVE!* ✅\n\nNo Proxy, Direct Pipelines running!", parse_mode="Markdown")
    except: pass

@bot.message_handler(func=lambda m: any(w in m.text.lower() for w in ["tred", "trade", "status", "mila"]))
def check_status_on_demand(message):
    try:
        reply = "🔍 *SMC / ICT Live Structural Report:*\n\n"
        for symbol in SYMBOLS:
            matrix = analyze_institutional_matrix(symbol)
            if matrix:
                zone_print = "Discount" if matrix['discount_zone'] else "Premium"
                reply += f"🔹 *{symbol}* -> Price: {matrix['current_price']:.2f}\n• Structure: {matrix['bias']} ({zone_print})\n• Limits: H:{matrix['swing_high']:.2f} | L:{matrix['swing_low']:.2f}\n\n"
            else: reply += f"⚠️ *{symbol}* -> API Sync pending.\n\n"
        bot.reply_to(message, reply, parse_mode="Markdown")
    except: pass

if __name__ == "__main__":
    threading.Thread(target=core_scanner, daemon=True).start()
    while True:
        try: bot.infinity_polling(timeout=20)
        except: time.sleep(5)
