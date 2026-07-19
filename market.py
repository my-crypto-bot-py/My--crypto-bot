import ccxt
import pandas as pd

# ==========================
# OKX CONNECTION
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

        return df

    except Exception as e:

        print(f"Market Error ({symbol}):", e)
        return None


# ==========================
# LOAD & PREPARE
# ==========================

def load_market(symbol, timeframe, limit=300):

    df = get_market_data(
        symbol,
        timeframe,
        limit
    )

    if df is None:
        return None

    return df
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
        [
            high_low,
            high_close,
            low_close
        ],
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
# PREPARE MARKET
# ==========================

def prepare_market(df):

    df = add_ema(df)
    df = add_atr(df)
    df = add_volume(df)

    return df
    # ==========================
# TREND
# ==========================

def detect_trend(df):

    df = prepare_market(df)

    if len(df) < 200:
        return {
            "trend": "SIDEWAYS",
            "strength": 0
        }

    price = float(df["close"].iloc[-1])

    ema20 = float(df["ema20"].iloc[-1])
    ema50 = float(df["ema50"].iloc[-1])
    ema200 = float(df["ema200"].iloc[-1])

    if price > ema20 > ema50 > ema200:

        return {
            "trend": "BULLISH",
            "strength": 100
        }

    elif price < ema20 < ema50 < ema200:

        return {
            "trend": "BEARISH",
            "strength": 100
        }

    return {
        "trend": "SIDEWAYS",
        "strength": 40
    }


# ==========================
# VOLUME CONFIRMATION
# ==========================

def detect_volume_confirmation(df):

    df = prepare_market(df)

    if len(df) < 20:
        return False

    volume = float(df["volume"].iloc[-1])
    avg = float(df["avg_volume"].iloc[-1])

    return volume >= avg


# ==========================
# STRONG CANDLE
# ==========================

def strong_candle(df):

    df = prepare_market(df)

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

    return 7 <= hour <= 17


# ==========================
# MARKET VALIDATION
# ==========================

def validate_market(df):

    return {

        "trend": detect_trend(df),

        "volume": detect_volume_confirmation(df),

        "strong_candle": strong_candle(df),

        "session": session_filter(df)

    }
