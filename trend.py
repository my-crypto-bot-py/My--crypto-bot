import pandas as pd


def calculate_ema(df, period):
    return df["close"].ewm(
        span=period,
        adjust=False
    ).mean()


def detect_trend(df):

    if df is None or len(df) < 50:
        return {
            "trend": "UNKNOWN",
            "strength": 0
        }

    df = df.copy()

    # EMA
    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)

    close = float(df["close"].iloc[-1])
    ema50 = float(df["EMA50"].iloc[-1])
    ema200 = float(df["EMA200"].iloc[-1])

    # ==========================
    # SWING STRUCTURE
    # ==========================

    recent = df.tail(60)

    last_high = recent["high"].iloc[-15:].max()
    prev_high = recent["high"].iloc[-30:-15].max()

    last_low = recent["low"].iloc[-15:].min()
    prev_low = recent["low"].iloc[-30:-15].min()

    structure = "SIDEWAYS"

    if last_high > prev_high and last_low > prev_low:
        structure = "BULLISH"

    elif last_high < prev_high and last_low < prev_low:
        structure = "BEARISH"

    # ==========================
    # EMA FILTER
    # ==========================

    ema_trend = "SIDEWAYS"

    if ema50 > ema200 and close > ema50:
        ema_trend = "BULLISH"

    elif ema50 < ema200 and close < ema50:
        ema_trend = "BEARISH"

    # ==========================
    # MOMENTUM
    # ==========================

    change = (
        close - float(df["close"].iloc[-20])
    ) / float(df["close"].iloc[-20]) * 100

    # ==========================
    # FINAL TREND
    # ==========================

    if structure == ema_trend:
        trend = structure
        strength = 100

    elif structure != "SIDEWAYS":
        trend = structure
        strength = 80

    elif ema_trend != "SIDEWAYS":
        trend = ema_trend
        strength = 70

    else:
        trend = "SIDEWAYS"
        strength = 40

    # Momentum adjustment
    if trend == "BULLISH" and change < -1:
        strength -= 15

    if trend == "BEARISH" and change > 1:
        strength -= 15

    strength = max(0, min(100, round(strength, 2)))

    return {
        "trend": trend,
        "strength": strength
    }
