import pandas as pd


def detect_liquidity_sweep(df, lookback=20):

    if len(df) < lookback:
        return None

    recent = df.iloc[-lookback:]
    current = df.iloc[-1]

    previous_high = recent["high"][:-1].max()
    previous_low = recent["low"][:-1].min()

    # Buy Side Liquidity Sweep
    if current["high"] > previous_high and current["close"] < previous_high:
        return {
            "direction": "SELL",
            "type": "Buy Side Liquidity Sweep",
            "level": previous_high
        }

    # Sell Side Liquidity Sweep
    if current["low"] < previous_low and current["close"] > previous_low:
        return {
            "direction": "BUY",
            "type": "Sell Side Liquidity Sweep",
            "level": previous_low
        }

    return None


def detect_fvg(df):

    if len(df) < 3:
        return None

    c1 = df.iloc[-3]
    c3 = df.iloc[-1]

    # Bullish FVG
    if c1["high"] < c3["low"]:
        return {
            "direction": "BUY",
            "type": "Bullish FVG",
            "top": c3["low"],
            "bottom": c1["high"]
        }

    # Bearish FVG
    if c1["low"] > c3["high"]:
        return {
            "direction": "SELL",
            "type": "Bearish FVG",
            "top": c1["low"],
            "bottom": c3["high"]
        }

    return None


def detect_order_block(df, lookback=20):

    if len(df) < lookback:
        return None

    data = df.iloc[-lookback:]

    for i in range(len(data) - 2, 0, -1):

        candle = data.iloc[i]
        next_candle = data.iloc[i + 1]

        # Bullish Order Block
        if (
            candle["close"] < candle["open"]
            and next_candle["close"] > candle["high"]
        ):
            return {
                "direction": "BUY",
                "type": "Bullish Order Block",
                "high": candle["high"],
                "low": candle["low"]
            }

        # Bearish Order Block
        if (
            candle["close"] > candle["open"]
            and next_candle["close"] < candle["low"]
        ):
            return {
                "direction": "SELL",
                "type": "Bearish Order Block",
                "high": candle["high"],
                "low": candle["low"]
            }

    return None


def get_premium_discount(df):

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
