import pandas as pd


def calculate_ema(df, period):
    return df["close"].ewm(
        span=period,
        adjust=False
    ).mean()


def detect_trend(df, symbol):

    if df is None or len(df) < 200:
        return {
            "trend": "UNKNOWN",
            "strength": 0
        }

    daily_bias = get_daily_bias(symbol)

    df = df.copy()

    df["EMA50"] = calculate_ema(df, 50)
    df["EMA200"] = calculate_ema(df, 200)

    close = float(df["close"].iloc[-1])
    ema50 = float(df["EMA50"].iloc[-1])
    ema200 = float(df["EMA200"].iloc[-1])

    highs = df["high"]
    lows = df["low"]

    last_high = highs.iloc[-20:].max()
    prev_high = highs.iloc[-40:-20].max()

    last_low = lows.iloc[-20:].min()
    prev_low = lows.iloc[-40:-20].min()

    buy_score = 0
    sell_score = 0

    # EMA
    if ema50 > ema200:
        buy_score += 30
    else:
        sell_score += 30

    # Price Position
    if close > ema50:
        buy_score += 20
    else:
        sell_score += 20

    # Market Structure
    if last_high > prev_high:
        buy_score += 15
    else:
        sell_score += 15

    if last_low > prev_low:
        buy_score += 15
    else:
        sell_score += 15

    # Momentum
    change = (
        close - float(df["close"].iloc[-15])
    ) / float(df["close"].iloc[-15]) * 100

    if change > 1:
        buy_score += 20

    elif change < -1:
        sell_score += 20

    # Daily Bias Filter
    if daily_bias == "BULLISH":
        buy_score += 15

    elif daily_bias == "BEARISH":
        sell_score += 15

    # Final Decision
    if buy_score > sell_score:

        trend = "BULLISH"
        strength = buy_score

    elif sell_score > buy_score:

        trend = "BEARISH"
        strength = sell_score

    else:

        trend = "SIDEWAYS"
        strength = 50

    strength = min(100, strength)

    return {
        "trend": trend,
        "strength": round(strength, 2)
    }
