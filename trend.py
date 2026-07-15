import pandas as pd


def calculate_ema(df, period):
    return df["close"].ewm(span=period, adjust=False).mean()


def detect_trend(df):
    """
    Trend Detection using EMA 50 + EMA 200
    """

    if df is None or len(df) < 50:
        return {
            "trend": "UNKNOWN",
            "strength": 0
        }

    df = df.copy()

    df["EMA50"] = calculate_ema(df, 50)

    if len(df) >= 200:
        df["EMA200"] = calculate_ema(df, 200)

        ema50 = df["EMA50"].iloc[-1]
        ema200 = df["EMA200"].iloc[-1]

        distance = abs(ema50 - ema200) / ema200 * 100

        if ema50 > ema200:
            return {
                "trend": "BULLISH",
                "strength": round(min(distance * 20, 100), 2)
            }

        elif ema50 < ema200:
            return {
                "trend": "BEARISH",
                "strength": round(min(distance * 20, 100), 2)
            }

    last_close = df["close"].iloc[-1]
    ema50 = df["EMA50"].iloc[-1]

    if last_close > ema50:
        return {
            "trend": "BULLISH",
            "strength": 50
        }

    elif last_close < ema50:
        return {
            "trend": "BEARISH",
            "strength": 50
        }

    return {
        "trend": "SIDEWAYS",
        "strength": 25
    }
