import ccxt
import pandas as pd
from config import *

# ==========================
# OKX EXCHANGE
# ==========================

exchange = ccxt.okx({
    "enableRateLimit": True,
    "options": {
        "defaultType": "swap"
    }
})

# ==========================
# LOAD MARKET DATA
# ==========================

def get_market_data(symbol, timeframe, limit=300):

    try:

        ohlcv = exchange.fetch_ohlcv(
            symbol,
            timeframe=timeframe,
            limit=limit
        )

        df = pd.DataFrame(
            ohlcv,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            unit="ms"
        )

        print("\n========== MARKET DEBUG ==========")
        print("Symbol:", symbol)
        print("Timeframe:", timeframe)
        print("Candles:", len(df))
        print("First Candle:", df["timestamp"].iloc[0])
        print("Last Candle:", df["timestamp"].iloc[-1])
        print("Last Close:", df["close"].iloc[-1])
        print("==================================\n")

        return df

    except Exception as e:

        print("Market Error:", e)
        return None
        # ==========================
# EMA
# ==========================

def add_ema(df):

    df["ema20"] = df["close"].ewm(span=20).mean()
    df["ema50"] = df["close"].ewm(span=50).mean()
    df["ema200"] = df["close"].ewm(span=200).mean()

    return df


# ==========================
# ATR
# ==========================

def add_atr(df, period=14):

    high_low = df["high"] - df["low"]

    high_close = (
        df["high"] - df["close"].shift()
    ).abs()

    low_close = (
        df["low"] - df["close"].shift()
    ).abs()

    tr = pd.concat(
        [high_low, high_close, low_close],
        axis=1
    ).max(axis=1)

    df["atr"] = tr.rolling(period).mean()

    return df


# ==========================
# VOLUME
# ==========================

def add_volume(df):

    df["avg_volume"] = (
        df["volume"]
        .rolling(20)
        .mean()
    )

    return df


# ==========================
# INDICATORS
# ==========================

def prepare_market(df):

    df = add_ema(df)
    df = add_atr(df)
    df = add_volume(df)

    return df
    # ==========================
# TREND
# ==========================

def get_trend(df):

    if len(df) < 200:
        return "SIDEWAYS"

    price = float(df["close"].iloc[-1])

    ema20 = float(df["ema20"].iloc[-1])
    ema50 = float(df["ema50"].iloc[-1])
    ema200 = float(df["ema200"].iloc[-1])

    if price > ema20 > ema50 > ema200:
        return "BULLISH"

    elif price < ema20 < ema50 < ema200:
        return "BEARISH"

    return "SIDEWAYS"


# ==========================
# VOLUME CONFIRMATION
# ==========================

def volume_confirmation(df):

    if len(df) < 20:
        return False

    volume = float(df["volume"].iloc[-1])
    avg = float(df["avg_volume"].iloc[-1])

    return volume >= avg


# ==========================
# STRONG CANDLE
# ==========================

def strong_candle(df):

    if len(df) < 20:
        return False

    body = abs(
        float(df["close"].iloc[-1]) -
        float(df["open"].iloc[-1])
    )

    atr = float(df["atr"].iloc[-1])

    return body >= atr * 0.8


# ==========================
# SESSION FILTER
# ==========================

def session_filter(df):

    hour = df["timestamp"].iloc[-1].hour

    if 7 <= hour <= 17:
        return True

    return False


# ==========================
# MARKET FILTER
# ==========================

def validate_market(df):

    return {

        "trend": get_trend(df),

        "volume": volume_confirmation(df),

        "strong_candle": strong_candle(df),

        "session": session_filter(df)

    }
