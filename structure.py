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
