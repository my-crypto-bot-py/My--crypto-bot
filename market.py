import ccxt
import pandas as pd
from config import *

# ==========================
# OKX EXCHANGE
# ==========================

exchange = ccxt.okx(
    {
        "enableRateLimit": True,
        "options": {
            "defaultType": "swap"
        }
    }
)

# ==========================
# LOAD MARKET DATA
# ==========================

def get_market_data(

    symbol,
    timeframe,
    limit=LIMIT

):

    try:

        candles = exchange.fetch_ohlcv(

            symbol,

            timeframe=timeframe,

            limit=limit

        )


        df = pd.DataFrame(

            candles,

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


        numeric = [

            "open",

            "high",

            "low",

            "close",

            "volume"

        ]


        for col in numeric:

            df[col] = df[col].astype(float)


        return df


    except Exception as e:

        print(

            "Market Error:",

            e

        )

        return None


# ==========================
# MARKET DEBUG
# ==========================

def market_debug(

    df,

    symbol,

    timeframe

):

    print()

    print("========== MARKET DEBUG ==========")

    print("Symbol:", symbol)

    print("Timeframe:", timeframe)

    print("Candles:", len(df))

    print("First Candle:", df["timestamp"].iloc[0])

    print("Last Candle:", df["timestamp"].iloc[-1])

    print("Last Close:", df["close"].iloc[-1])

    print("==================================")

    print()
    # ==========================
# EMA
# ==========================

def add_ema(df):

    df["ema20"] = (
        df["close"]
        .ewm(span=20, adjust=False)
        .mean()
    )

    df["ema50"] = (
        df["close"]
        .ewm(span=50, adjust=False)
        .mean()
    )

    df["ema200"] = (
        df["close"]
        .ewm(span=200, adjust=False)
        .mean()
    )

    return df


# ==========================
# ATR
# ==========================

def add_atr(df, period=ATR_PERIOD):

    high_low = df["high"] - df["low"]

    high_close = (
        df["high"] -
        df["close"].shift()
    ).abs()

    low_close = (
        df["low"] -
        df["close"].shift()
    ).abs()

    tr = pd.concat(

        [

            high_low,

            high_close,

            low_close

        ],

        axis=1

    ).max(axis=1)

    df["atr"] = (

        tr

        .rolling(period)

        .mean()

    )

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
# RSI
# ==========================

def add_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    df["rsi"] = 100 - (

        100 / (1 + rs)

    )

    return df


# ==========================
# VWAP
# ==========================

def add_vwap(df):

    tp = (

        df["high"]

        + df["low"]

        + df["close"]

    ) / 3

    cumulative_tp = (

        tp * df["volume"]

    ).cumsum()

    cumulative_volume = (

        df["volume"]

    ).cumsum()

    df["vwap"] = (

        cumulative_tp /

        cumulative_volume

    )

    return df
    # ==========================
# PREPARE MARKET
# ==========================

def prepare_market(df):

    df = add_ema(df)
    df = add_atr(df)
    df = add_volume(df)
    df = add_rsi(df)
    df = add_vwap(df)

    return df


# ==========================
# TREND
# ==========================

def detect_trend(df):

    df = prepare_market(df)

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

def detect_volume_confirmation(df):

    df = add_volume(df)

    if len(df) < 20:
        return False

    volume = float(df["volume"].iloc[-1])
    avg = float(df["avg_volume"].iloc[-1])

    return volume >= avg


# ==========================
# STRONG CANDLE
# ==========================

def detect_strong_candle(df):

    df = add_atr(df)

    if len(df) < ATR_PERIOD + 5:
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

def detect_session(df):

    hour = int(df["timestamp"].iloc[-1].hour)

    london = 7 <= hour <= 16
    newyork = 13 <= hour <= 22

    return london or newyork


# ==========================
# MARKET VALIDATION
# ==========================

def validate_market(df):

    return {

        "trend": detect_trend(df),

        "volume": detect_volume_confirmation(df),

        "strong_candle": detect_strong_candle(df),

        "session": detect_session(df)

    }
