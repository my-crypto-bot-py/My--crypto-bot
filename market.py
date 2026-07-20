import ccxt
import pandas as pd
import numpy as np

# ==========================
# ICT MARKET ENGINE V5
# ==========================

exchange = ccxt.okx({

    "enableRateLimit": True,

    "options": {

        "defaultType": "swap"

    }

})

exchange.load_markets()


# ==========================
# MARKET DATA
# ==========================

def get_market_data(

    symbol,

    timeframe,

    limit=300

):

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
# PREPARE DATA
# ==========================

def prepare_market(df):

    df = df.copy()

    numeric = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]

    for col in numeric:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )

    df.dropna(inplace=True)

    df.reset_index(

        drop=True,

        inplace=True

    )

    return df


# ==========================
# EMA
# ==========================

def add_ema(

    df,

    period

):

    df[f"ema{period}"] = (

        df["close"]

        .ewm(

            span=period,

            adjust=False

        )

        .mean()

    )

    return df


# ==========================
# LOAD ALL EMA
# ==========================

def load_emas(df):

    df = add_ema(df, 20)

    df = add_ema(df, 50)

    df = add_ema(df, 100)

    df = add_ema(df, 200)

    return df
    # ==========================
# EMA TREND ENGINE V5
# ==========================

def detect_trend(df):

    df = prepare_market(df)

    df = load_emas(df)

    if len(df) < 200:

        return {

            "trend": "UNKNOWN",

            "strength": 0

        }

    price = float(df["close"].iloc[-1])

    ema20 = float(df["ema20"].iloc[-1])

    ema50 = float(df["ema50"].iloc[-1])

    ema100 = float(df["ema100"].iloc[-1])

    ema200 = float(df["ema200"].iloc[-1])

    strength = 0

    # Strong Bullish

    if (

        price > ema20 >

        ema50 >

        ema100 >

        ema200

    ):

        strength = 95

        trend = "BULLISH"

    # Strong Bearish

    elif (

        price < ema20 <

        ema50 <

        ema100 <

        ema200

    ):

        strength = 95

        trend = "BEARISH"

    # Medium Bullish

    elif (

        price > ema20 >

        ema50

    ):

        strength = 75

        trend = "BULLISH"

    # Medium Bearish

    elif (

        price < ema20 <

        ema50

    ):

        strength = 75

        trend = "BEARISH"

    else:

        trend = "SIDEWAYS"

        strength = 40

    return {

        "trend": trend,

        "strength": strength,

        "price": price,

        "ema20": ema20,

        "ema50": ema50,

        "ema100": ema100,

        "ema200": ema200

    }


# ==========================
# TREND DIRECTION
# ==========================

def trend_direction(df):

    return detect_trend(df)["trend"]


# ==========================
# TREND STRENGTH
# ==========================

def trend_strength(df):

    return detect_trend(df)["strength"]


# ==========================
# EMA ALIGNMENT
# ==========================

def ema_alignment(df):

    trend = detect_trend(df)

    return (

        trend["trend"] != "SIDEWAYS"

    )
    # ==========================
# EMA TREND ENGINE V5
# ==========================

def detect_trend(df):

    df = prepare_market(df)

    df = load_emas(df)

    if len(df) < 200:

        return {

            "trend": "UNKNOWN",

            "strength": 0

        }

    price = float(df["close"].iloc[-1])

    ema20 = float(df["ema20"].iloc[-1])

    ema50 = float(df["ema50"].iloc[-1])

    ema100 = float(df["ema100"].iloc[-1])

    ema200 = float(df["ema200"].iloc[-1])

    strength = 0

    # Strong Bullish

    if (

        price > ema20 >

        ema50 >

        ema100 >

        ema200

    ):

        strength = 95

        trend = "BULLISH"

    # Strong Bearish

    elif (

        price < ema20 <

        ema50 <

        ema100 <

        ema200

    ):

        strength = 95

        trend = "BEARISH"

    # Medium Bullish

    elif (

        price > ema20 >

        ema50

    ):

        strength = 75

        trend = "BULLISH"

    # Medium Bearish

    elif (

        price < ema20 <

        ema50

    ):

        strength = 75

        trend = "BEARISH"

    else:

        trend = "SIDEWAYS"

        strength = 40

    return {

        "trend": trend,

        "strength": strength,

        "price": price,

        "ema20": ema20,

        "ema50": ema50,

        "ema100": ema100,

        "ema200": ema200

    }


# ==========================
# TREND DIRECTION
# ==========================

def trend_direction(df):

    return detect_trend(df)["trend"]


# ==========================
# TREND STRENGTH
# ==========================

def trend_strength(df):

    return detect_trend(df)["strength"]


# ==========================
# EMA ALIGNMENT
# ==========================

def ema_alignment(df):

    trend = detect_trend(df)

    return (

        trend["trend"] != "SIDEWAYS"

    )
    # ==========================
# VOLUME ENGINE V5
# ==========================

def add_average_volume(

    df,

    period=20

):

    df["avg_volume"] = (

        df["volume"]

        .rolling(period)

        .mean()

    )

    return df


# ==========================
# VOLUME CONFIRMATION
# ==========================

def detect_volume_confirmation(df):

    df = prepare_market(df)

    df = add_average_volume(df)

    if len(df) < 20:

        return False

    current = float(

        df["volume"].iloc[-1]

    )

    average = float(

        df["avg_volume"].iloc[-1]

    )

    return current > average


# ==========================
# HIGH VOLUME CANDLE
# ==========================

def high_volume_candle(df):

    df = prepare_market(df)

    df = add_average_volume(df)

    if len(df) < 20:

        return False

    current = float(

        df["volume"].iloc[-1]

    )

    average = float(

        df["avg_volume"].iloc[-1]

    )

    return current > average * 1.5


# ==========================
# VOLUME SPIKE
# ==========================

def detect_volume_spike(df):

    df = prepare_market(df)

    df = add_average_volume(df)

    if len(df) < 20:

        return {

            "spike": False,

            "ratio": 0

        }

    current = float(

        df["volume"].iloc[-1]

    )

    average = float(

        df["avg_volume"].iloc[-1]

    )

    ratio = current / average if average > 0 else 0

    return {

        "spike": ratio >= 2,

        "ratio": round(ratio, 2)

    }


# ==========================
# FINAL VOLUME ANALYSIS
# ==========================

def analyze_volume(df):

    confirmation = detect_volume_confirmation(df)

    high = high_volume_candle(df)

    spike = detect_volume_spike(df)

    return {

        "confirmed": confirmation,

        "high_volume": high,

        "spike": spike["spike"],

        "ratio": spike["ratio"]

    }
    # ==========================
# VWAP ENGINE V5
# ==========================

def add_vwap(df):

    df = prepare_market(df)

    typical_price = (

        df["high"]

        +

        df["low"]

        +

        df["close"]

    ) / 3

    cumulative_tp_volume = (

        typical_price

        *

        df["volume"]

    ).cumsum()

    cumulative_volume = (

        df["volume"]

    ).cumsum()

    df["vwap"] = (

        cumulative_tp_volume

        /

        cumulative_volume

    )

    return df


# ==========================
# VWAP DIRECTION
# ==========================

def detect_vwap_direction(df):

    df = add_vwap(df)

    price = float(

        df["close"].iloc[-1]

    )

    vwap = float(

        df["vwap"].iloc[-1]

    )

    if price > vwap:

        return {

            "trend": "BULLISH",

            "price": price,

            "vwap": round(vwap, 2)

        }

    elif price < vwap:

        return {

            "trend": "BEARISH",

            "price": price,

            "vwap": round(vwap, 2)

        }

    return {

        "trend": "NEUTRAL",

        "price": price,

        "vwap": round(vwap, 2)

    }


# ==========================
# VWAP DISTANCE
# ==========================

def vwap_distance(df):

    data = detect_vwap_direction(df)

    distance = abs(

        data["price"]

        -

        data["vwap"]

    )

    return round(distance, 2)


# ==========================
# VWAP CONFIRMATION
# ==========================

def confirm_vwap(df):

    trend = detect_trend(df)

    vwap = detect_vwap_direction(df)

    return (

        trend["trend"]

        ==

        vwap["trend"]

    )


# ==========================
# FINAL VWAP ANALYSIS
# ==========================

def analyze_vwap(df):

    info = detect_vwap_direction(df)

    return {

        "trend": info["trend"],

        "price": info["price"],

        "vwap": info["vwap"],

        "distance": vwap_distance(df),

        "confirmed": confirm_vwap(df)

    }
    # ==========================
# SESSION ENGINE V5
# ==========================

ASIAN_START = 0
ASIAN_END = 8

LONDON_START = 7
LONDON_END = 16

NEWYORK_START = 13
NEWYORK_END = 22


# ==========================
# CURRENT SESSION
# ==========================

def get_current_session(df):

    hour = int(

        df["timestamp"].iloc[-1].hour

    )

    if ASIAN_START <= hour < ASIAN_END:

        return "ASIAN"

    elif LONDON_START <= hour < LONDON_END:

        return "LONDON"

    elif NEWYORK_START <= hour < NEWYORK_END:

        return "NEWYORK"

    return "OFF"


# ==========================
# SESSION FILTER
# ==========================

def session_filter(df):

    session = get_current_session(df)

    return session != "OFF"


# ==========================
# ACTIVE SESSION
# ==========================

def active_session(df):

    return {

        "session": get_current_session(df),

        "active": session_filter(df)

    }


# ==========================
# KILL ZONE
# ==========================

def in_kill_zone(df):

    session = get_current_session(df)

    return session in [

        "LONDON",

        "NEWYORK"

    ]


# ==========================
# SESSION ANALYSIS
# ==========================

def analyze_session(df):

    return {

        "session": get_current_session(df),

        "active": session_filter(df),

        "kill_zone": in_kill_zone(df)

    }
    # ==========================
# MOMENTUM ENGINE V5
# ==========================

def add_rsi(df, period=14):

    delta = df["close"].diff()

    gain = delta.clip(lower=0)

    loss = (-delta).clip(lower=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    df["rsi"] = 100 - (100 / (1 + rs))

    return df


# ==========================
# RSI SIGNAL
# ==========================

def detect_rsi_signal(df):

    df = prepare_market(df)

    df = add_rsi(df)

    if len(df) < 20:

        return {

            "signal": "UNKNOWN",

            "rsi": 0

        }

    rsi = float(df["rsi"].iloc[-1])

    if rsi >= 70:

        signal = "OVERBOUGHT"

    elif rsi <= 30:

        signal = "OVERSOLD"

    else:

        signal = "NORMAL"

    return {

        "signal": signal,

        "rsi": round(rsi, 2)

    }


# ==========================
# MOMENTUM STRENGTH
# ==========================

def momentum_strength(df):

    df = prepare_market(df)

    if len(df) < 10:

        return 0

    current = float(df["close"].iloc[-1])

    previous = float(df["close"].iloc[-10])

    change = abs(

        (current - previous)

        / previous

    ) * 100

    return round(change, 2)


# ==========================
# FINAL MOMENTUM
# ==========================

def analyze_momentum(df):

    rsi = detect_rsi_signal(df)

    strength = momentum_strength(df)

    return {

        "rsi": rsi["rsi"],

        "signal": rsi["signal"],

        "strength": strength

    }
    # ==========================
# MULTI TIMEFRAME MARKET V5
# ==========================

def get_htf_market(htf_df):

    trend = detect_trend(htf_df)

    volume = analyze_volume(htf_df)

    vwap = analyze_vwap(htf_df)

    momentum = analyze_momentum(htf_df)

    return {

        "trend": trend,

        "volume": volume,

        "vwap": vwap,

        "momentum": momentum

    }


# ==========================
# LOWER TF MARKET
# ==========================

def get_ltf_market(ltf_df):

    trend = detect_trend(ltf_df)

    volume = analyze_volume(ltf_df)

    vwap = analyze_vwap(ltf_df)

    momentum = analyze_momentum(ltf_df)

    return {

        "trend": trend,

        "volume": volume,

        "vwap": vwap,

        "momentum": momentum

    }


# ==========================
# HTF + LTF CONFIRMATION
# ==========================

def market_timeframe_confirmation(

    htf_df,

    ltf_df

):

    htf = get_htf_market(htf_df)

    ltf = get_ltf_market(ltf_df)

    if (

        htf["trend"]["trend"]

        ==

        ltf["trend"]["trend"]

    ):

        return {

            "confirm": True,

            "direction":

            htf["trend"]["trend"]

        }

    return {

        "confirm": False,

        "direction": None

    }


# ==========================
# FINAL MULTI TF ANALYSIS
# ==========================

def analyze_multi_tf_market(

    htf_df,

    ltf_df

):

    confirmation = market_timeframe_confirmation(

        htf_df,

        ltf_df

    )

    return confirmation
    # ==========================
# MARKET STRENGTH SCORE V5
# ==========================

def calculate_market_strength(df):

    score = 0

    reasons = []

    trend = detect_trend(df)

    volume = analyze_volume(df)

    vwap = analyze_vwap(df)

    momentum = analyze_momentum(df)

    session = analyze_session(df)


    # Trend
    if trend["trend"] != "SIDEWAYS":

        score += 35

        reasons.append(trend["trend"])


    # Volume
    if volume["confirmed"]:

        score += 20

        reasons.append("Volume")


    # VWAP
    if vwap["confirmed"]:

        score += 20

        reasons.append("VWAP")


    # Momentum
    if momentum["strength"] >= 1:

        score += 15

        reasons.append("Momentum")


    # Kill Zone
    if session["kill_zone"]:

        score += 10

        reasons.append(session["session"])


    if score > 100:

        score = 100


    return {

        "score": score,

        "reasons": reasons

    }


# ==========================
# MARKET HEALTH
# ==========================

def market_health(df):

    result = calculate_market_strength(df)

    score = result["score"]


    if score >= 80:

        health = "STRONG"

    elif score >= 60:

        health = "GOOD"

    elif score >= 40:

        health = "NORMAL"

    else:

        health = "WEAK"


    return {

        "health": health,

        "score": score

    }


# ==========================
# DEBUG PANEL
# ==========================

def debug_market(df):

    trend = detect_trend(df)

    volume = analyze_volume(df)

    vwap = analyze_vwap(df)

    momentum = analyze_momentum(df)

    session = analyze_session(df)

    health = market_health(df)


    print("\n========== MARKET V5 ==========")

    print("Trend      :", trend["trend"])

    print("Strength   :", trend["strength"])

    print("Volume     :", volume["confirmed"])

    print("VWAP       :", vwap["trend"])

    print("Momentum   :", momentum["strength"])

    print("Session    :", session["session"])

    print("Kill Zone  :", session["kill_zone"])

    print("Health     :", health["health"])

    print("Score      :", health["score"])

    print("================================\n")


    return health
    # ==========================
# FINAL MARKET ANALYZER V5
# ==========================

def analyze_market(df):

    trend = detect_trend(df)

    volume = analyze_volume(df)

    vwap = analyze_vwap(df)

    momentum = analyze_momentum(df)

    session = analyze_session(df)

    health = market_health(df)

    return {

        "trend": trend,

        "volume": volume,

        "vwap": vwap,

        "momentum": momentum,

        "session": session,

        "health": health

    }


# ==========================
# BOT READY FUNCTION
# ==========================

def market_engine_v5(df):

    result = analyze_market(df)

    return {

        "trend": result["trend"]["trend"],

        "trend_strength": result["trend"]["strength"],

        "market_score": result["health"]["score"],

        "market_health": result["health"]["health"],

        "volume_confirmed": result["volume"]["confirmed"],

        "vwap_confirmed": result["vwap"]["confirmed"],

        "momentum_strength": result["momentum"]["strength"],

        "session": result["session"]["session"],

        "kill_zone": result["session"]["kill_zone"]

    }


# ==========================
# EXPORTS
# ==========================

__all__ = [

    "get_market_data",

    "prepare_market",

    "detect_trend",

    "trend_direction",

    "trend_strength",

    "detect_volatility",

    "strong_candle",

    "expansion_candle",

    "analyze_volume",

    "analyze_vwap",

    "analyze_session",

    "analyze_momentum",

    "analyze_multi_tf_market",

    "calculate_market_strength",

    "market_health",

    "analyze_market",

    "market_engine_v5",

    "debug_market"

]
