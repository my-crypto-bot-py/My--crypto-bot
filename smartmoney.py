import pandas as pd


def detect_liquidity_sweep(df, lookback=20):
    """
    Improved Liquidity Sweep Detection
    """

    if len(df) < lookback:
        return None

    data = df.tail(lookback)

    previous_high = data["high"][:-1].max()
    previous_low = data["low"][:-1].min()

    current = data.iloc[-1]

    if current["high"] > previous_high and current["close"] < previous_high:
        return {
            "type": "Buy Side Liquidity Sweep",
            "level": previous_high
        }

    if current["low"] < previous_low and current["close"] > previous_low:
        return {
            "type": "Sell Side Liquidity Sweep",
            "level": previous_low
        }

    return None


def detect_fvg(df, lookback=20):
    """
    Improved Fair Value Gap Detection
    """

    if len(df) < lookback:
        return None

    data = df.tail(lookback)

    for i in range(2, len(data)):

        c1 = data.iloc[i - 2]
        c2 = data.iloc[i - 1]
        c3 = data.iloc[i]

        if c1["high"] < c3["low"]:
            return {
                "type": "Bullish FVG",
                "top": c3["low"],
                "bottom": c1["high"],
                "size": round(c3["low"] - c1["high"], 2)
            }

        if c1["low"] > c3["high"]:
            return {
                "type": "Bearish FVG",
                "top": c1["low"],
                "bottom": c3["high"],
                "size": round(c1["low"] - c3["high"], 2)
            }

    return None


def detect_order_block(df, lookback=20):
    """
    Improved Order Block Detection
    """

    if len(df) < lookback:
        return None

    data = df.tail(lookback)

    for i in range(len(data) - 2):

        candle = data.iloc[i]
        next_candle = data.iloc[i + 1]

        if (
            candle["close"] < candle["open"]
            and next_candle["close"] > candle["high"]
        ):
            return {
                "type": "Bullish Order Block",
                "high": candle["high"],
                "low": candle["low"]
            }

        if (
            candle["close"] > candle["open"]
            and next_candle["close"] < candle["low"]
        ):
            return {
                "type": "Bearish Order Block",
                "high": candle["high"],
                "low": candle["low"]
            }

    return None


def get_premium_discount(df):
    """
    Premium / Discount Zone
    """

    if len(df) < 20:
        return None

    high = df["high"].tail(20).max()
    low = df["low"].tail(20).min()

    equilibrium = (high + low) / 2
    price = df["close"].iloc[-1]

    zone = "Premium" if price > equilibrium else "Discount"

    return {
        "zone": zone,
        "high": high,
        "low": low,
        "equilibrium": equilibrium,
        "price": price
    }
