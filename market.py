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


exchange.load_markets()


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

        print(
            "Market Error:",
            symbol,
            e
        )

        return None



# ==========================
# INDICATORS
# ==========================

def prepare_market(df):

    df = df.copy()


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


    # ATR

    tr1 = df["high"] - df["low"]

    tr2 = (
        df["high"]
        -
        df["close"].shift()
    ).abs()


    tr3 = (
        df["low"]
        -
        df["close"].shift()
    ).abs()


    tr = pd.concat(
        [tr1,tr2,tr3],
        axis=1
    ).max(axis=1)


    df["atr"] = (
        tr
        .rolling(14)
        .mean()
    )


    df["avg_volume"] = (
        df["volume"]
        .rolling(20)
        .mean()
    )


    return df



# ==========================
# TREND
# ==========================

def detect_trend(df, symbol=None):

    df = prepare_market(df)


    if len(df) < 200:

        return {

            "trend":"UNKNOWN",

            "strength":0

        }



    price = float(
        df["close"].iloc[-1]
    )


    ema20 = float(
        df["ema20"].iloc[-1]
    )


    ema50 = float(
        df["ema50"].iloc[-1]
    )


    ema200 = float(
        df["ema200"].iloc[-1]
    )


    if price > ema20 > ema50 > ema200:

        return {

            "trend":"BULLISH",

            "strength":90

        }


    elif price < ema20 < ema50 < ema200:

        return {

            "trend":"BEARISH",

            "strength":90

        }


    return {

        "trend":"SIDEWAYS",

        "strength":40

    }



# ==========================
# VOLUME
# ==========================

def detect_volume_confirmation(df):

    df = prepare_market(df)


    if len(df)<20:

        return False


    return (

        df["volume"].iloc[-1]

        >

        df["avg_volume"].iloc[-1]

    )



# ==========================
# STRONG CANDLE
# ==========================

def strong_candle(df):

    df = prepare_market(df)


    body = abs(

        df["close"].iloc[-1]
        -
        df["open"].iloc[-1]

    )


    atr = df["atr"].iloc[-1]


    return body > atr



# ==========================
# SESSION
# ==========================

def session_filter(df):

    hour = df["timestamp"].iloc[-1].hour

    return 7 <= hour <= 17
