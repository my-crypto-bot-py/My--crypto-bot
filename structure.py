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
