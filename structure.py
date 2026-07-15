import pandas as pd

def find_swings(df, left=2, right=2):

    highs = []
    lows = []

    for i in range(left, len(df) - right):

        if df["high"].iloc[i] == max(df["high"].iloc[i-left:i+right+1]):
            highs.append((i, df["high"].iloc[i]))

        if df["low"].iloc[i] == min(df["low"].iloc[i-left:i+right+1]):
            lows.append((i, df["low"].iloc[i]))

    return highs, lows


def detect_bos(df, swing_highs, swing_lows):

    last_close = df["close"].iloc[-1]

    if swing_highs:
        last_high = swing_highs[-1][1]

        if last_close > last_high:
            return {
                "direction": "BUY",
                "type": "Bullish BOS",
                "level": last_high
            }

    if swing_lows:
        last_low = swing_lows[-1][1]

        if last_close < last_low:
            return {
                "direction": "SELL",
                "type": "Bearish BOS",
                "level": last_low
            }

    return None


def detect_mss(df, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None

    last_close = df["close"].iloc[-1]

    prev_high = swing_highs[-2][1]
    prev_low = swing_lows[-2][1]

    if last_close > prev_high:
        return {
            "direction": "BUY",
            "type": "Bullish MSS",
            "level": prev_high
        }

    if last_close < prev_low:
        return {
            "direction": "SELL",
            "type": "Bearish MSS",
            "level": prev_low
        }

    return None


def detect_choch(df, swing_highs, swing_lows):

    if not swing_highs or not swing_lows:
        return None

    last_close = df["close"].iloc[-1]

    last_high = swing_highs[-1][1]
    last_low = swing_lows[-1][1]

    if last_close > last_high:
        return {
            "direction": "BUY",
            "type": "Bullish CHoCH",
            "level": last_high
        }

    if last_close < last_low:
        return {
            "direction": "SELL",
            "type": "Bearish CHoCH",
            "level": last_low
        }

    return None
