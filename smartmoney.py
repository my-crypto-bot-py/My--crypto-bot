import pandas as pd


def detect_liquidity_sweep(df, lookback=20):
    """
    Liquidity sweep detect karta hai.
    """

    if len(df) < lookback:
        return None

    recent = df.iloc[-lookback:]
    current = df.iloc[-1]

    previous_high = recent["high"].max()
    previous_low = recent["low"].min()

    # Buy side liquidity sweep
    if current["high"] > previous_high and current["close"] < previous_high:
        return {
            "type": "Buy Side Liquidity Sweep",
            "level": previous_high
        }

    # Sell side liquidity sweep
    if current["low"] < previous_low and current["close"] > previous_low:
        return {
            "type": "Sell Side Liquidity Sweep",
            "level": previous_low
        }

    return None
