import pandas as pd

def find_swings(df, left=2, right=2):
    """
    Swing High aur Swing Low detect karta hai.
    """

    highs = []
    lows = []

    for i in range(left, len(df) - right):

        high = df["high"].iloc[i]
        low = df["low"].iloc[i]

        # Swing High
        if high == max(df["high"].iloc[i-left:i+right+1]):
            highs.append((i, high))

        # Swing Low
        if low == min(df["low"].iloc[i-left:i+right+1]):
            lows.append((i, low))

    return highs, lows
def detect_bos(df, swing_highs, swing_lows):
    """
    BOS (Break of Structure) detect karta hai.
    """

    signals = []

    # Bullish BOS
    for i, high in swing_highs:
        if i + 1 < len(df):
            if df["close"].iloc[-1] > high:
                signals.append({
                    "type": "Bullish BOS",
                    "level": high
                })

    # Bearish BOS
    for i, low in swing_lows:
        if i + 1 < len(df):
            if df["close"].iloc[-1] < low:
                signals.append({
                    "type": "Bearish BOS",
                    "level": low
                })

    return signals

def detect_mss(df, swing_highs, swing_lows):
    """
    MSS (Market Structure Shift)
    """

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None

    last_close = df["close"].iloc[-1]

    last_high = swing_highs[-1][1]
    prev_high = swing_highs[-2][1]

    last_low = swing_lows[-1][1]
    prev_low = swing_lows[-2][1]

    # Bullish MSS
    if last_close > prev_high:
        return {
            "type": "Bullish MSS",
            "level": prev_high
        }

    # Bearish MSS
    if last_close < prev_low:
        return {
            "type": "Bearish MSS",
            "level": prev_low
        }

    return None
def detect_choch(df, swing_highs, swing_lows):
    """
    CHoCH (Change of Character) detect karta hai.
    """

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None

    last_close = df["close"].iloc[-1]

    last_high = swing_highs[-1][1]
    last_low = swing_lows[-1][1]

    # Bullish CHoCH
    if last_close > last_high:
        return {
            "type": "Bullish CHoCH",
            "level": last_high
        }

    # Bearish CHoCH
    if last_close < last_low:
        return {
            "type": "Bearish CHoCH",
            "level": last_low
        }

    return None
