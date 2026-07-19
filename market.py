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


try:
    exchange.load_markets()

except Exception as e:

    print("OKX Market Load Error:", e)



# ==========================
# LOAD MARKET DATA
# ==========================

def get_market_data(
    symbol,
    timeframe,
    limit=300
):

    try:

        ohlcv = exchange.fetch_ohlcv(

            symbol,

            timeframe=timeframe.lower(),

            limit=limit

        )


        if not ohlcv:

            return None


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
            f"Market Error {symbol}:",
            e
        )

        return None




# ==========================
# INDICATORS
# ==========================

def prepare_market(df):

    if df is None or df.empty:

        return None


    df = df.copy()


    # EMA

    df["ema20"] = (

        df["close"]

        .ewm(
            span=20,
            adjust=False
        )

        .mean()

    )


    df["ema50"] = (

        df["close"]

        .ewm(
            span=50,
            adjust=False
        )

        .mean()

    )


    df["ema200"] = (

        df["close"]

        .ewm(
            span=200,
            adjust=False
        )

        .mean()

    )



    # ATR

    high_low = (

        df["high"]

        -

        df["low"]

    )


    high_close = (

        df["high"]

        -

        df["close"].shift()

    ).abs()



    low_close = (

        df["low"]

        -

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

        .rolling(14)

        .mean()

    )



    # Volume

    df["avg_volume"] = (

        df["volume"]

        .rolling(20)

        .mean()

    )


    return df




# ==========================
# TREND DETECTION
# ==========================

def detect_trend(
    df,
    symbol=None
):

    df = prepare_market(df)


    if df is None or len(df) < 200:

        return {

            "trend":"SIDEWAYS",

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



    if price < ema20 < ema50 < ema200:

        return {

            "trend":"BEARISH",

            "strength":90

        }



    return {

        "trend":"SIDEWAYS",

        "strength":40

    }




# ==========================
# VOLUME CONFIRMATION
# ==========================

def detect_volume_confirmation(df):

    df = prepare_market(df)


    if df is None or len(df) < 20:

        return False



    volume = float(
        df["volume"].iloc[-1]
    )


    avg = float(
        df["avg_volume"].iloc[-1]
    )


    if pd.isna(avg):

        return False



    return volume >= avg




# ==========================
# STRONG CANDLE
# ==========================

def strong_candle(df):

    df = prepare_market(df)


    if df is None:

        return False



    body = abs(

        float(df["close"].iloc[-1])

        -

        float(df["open"].iloc[-1])

    )


    atr = float(
        df["atr"].iloc[-1]
    )


    if pd.isna(atr):

        return False



    return body >= atr * 0.8




# ==========================
# SESSION FILTER
# ==========================

def session_filter(df):

    if df is None or df.empty:

        return False



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
