import pandas as pd


def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


def detect_trend(df):
    """
    Trend Detection using EMA 50 + EMA 200
    """

    if df is None or len(df) < 200:
        return {
            "trend": "UNKNOWN",
            "strength": "LOW"
        }

    df = df.copy()

    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)

    last = df.iloc[-1]

    if last["EMA50"] > last["EMA200"]:

        return {
            "trend": "BULLISH",
            "strength": "HIGH"
        }

    elif last["EMA50"] < last["EMA200"]:

        return {
            "trend": "BEARISH",
            "strength": "HIGH"
        }

    return {
        "trend": "SIDEWAYS",
        "strength": "LOW"
    }
