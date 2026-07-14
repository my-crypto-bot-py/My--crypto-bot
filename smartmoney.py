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
def detect_fvg(df):
    """
    Fair Value Gap detect karta hai.
    """

    if len(df) < 3:
        return None

    c1 = df.iloc[-3]
    c2 = df.iloc[-2]
    c3 = df.iloc[-1]

    # Bullish FVG
    if c1["high"] < c3["low"]:
        return {
            "type": "Bullish FVG",
            "top": c3["low"],
            "bottom": c1["high"]
        }

    # Bearish FVG
    if c1["low"] > c3["high"]:
        return {
            "type": "Bearish FVG",
            "top": c1["low"],
            "bottom": c3["high"]
        }

    return None

def detect_order_block(df, lookback=20):
    """
    Basic Order Block detection.
    """

    if len(df) < lookback:
        return None

    data = df.iloc[-lookback:]

    for i in range(len(data)-2, 0, -1):

        candle = data.iloc[i]
        next_candle = data.iloc[i+1]

        # Bullish Order Block
        if (
            candle["close"] < candle["open"]
            and next_candle["close"] > candle["high"]
        ):
            return {
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
                "type": "Bearish Order Block",
                "high": candle["high"],
                "low": candle["low"]
            }

    return None
