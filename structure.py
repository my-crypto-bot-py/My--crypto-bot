def find_swings(df, left=3, right=3):

    swing_highs = []
    swing_lows = []

    if len(df) < left + right + 5:
        return swing_highs, swing_lows

    for i in range(left, len(df) - right):

        current_high = float(df["high"].iloc[i])
        current_low = float(df["low"].iloc[i])

        left_high = df["high"].iloc[i-left:i].max()
        right_high = df["high"].iloc[i+1:i+right+1].max()

        left_low = df["low"].iloc[i-left:i].min()
        right_low = df["low"].iloc[i+1:i+right+1].min()

        # Swing High
        if current_high > left_high and current_high > right_high:

            swing_highs.append({
                "index": i,
                "price": current_high,
                "type": "SH"
            })

        # Swing Low
        if current_low < left_low and current_low < right_low:

            swing_lows.append({
                "index": i,
                "price": current_low,
                "type": "SL"
            })

    return swing_highs, swing_lows


def detect_bos(df, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None

    close = float(df["close"].iloc[-1])

    last_high = swing_highs[-1]["price"]
    prev_high = swing_highs[-2]["price"]

    last_low = swing_lows[-1]["price"]
    prev_low = swing_lows[-2]["price"]

    # Bullish BOS
    if last_high > prev_high and close > last_high:

        return {
            "direction": "BUY",
            "type": "Bullish BOS",
            "level": last_high
        }

    # Bearish BOS
    if last_low < prev_low and close < last_low:

        return {
            "direction": "SELL",
            "type": "Bearish BOS",
            "level": last_low
        }

    return None
