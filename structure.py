def find_swings(df, left=5, right=5):

    swing_highs = []
    swing_lows = []

    if len(df) < left + right + 20:
        return swing_highs, swing_lows

    for i in range(left, len(df) - right):

        high = float(df["high"].iloc[i])
        low = float(df["low"].iloc[i])

        left_high = df["high"].iloc[i-left:i].max()
        right_high = df["high"].iloc[i+1:i+right+1].max()

        left_low = df["low"].iloc[i-left:i].min()
        right_low = df["low"].iloc[i+1:i+right+1].min()

        # Strong Swing High
        if (
            high > left_high
            and high > right_high
            and (high - low) > df["high"].iloc[i] * 0.002
        ):

            swing_highs.append({
                "index": i,
                "price": high,
                "type": "SH"
            })

        # Strong Swing Low
        if (
            low < left_low
            and low < right_low
            and (high - low) > df["low"].iloc[i] * 0.002
        ):

            swing_lows.append({
                "index": i,
                "price": low,
                "type": "SL"
            })

    return swing_highs, swing_lows

    def detect_bos(df, swing_highs, swing_lows):

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return None

    close = float(df["close"].iloc[-1])

    last_high = swing_highs[-1]
    prev_high = swing_highs[-2]

    last_low = swing_lows[-1]
    prev_low = swing_lows[-2]

    # Bullish BOS
    if (
        last_high["price"] > prev_high["price"]
        and close > last_high["price"]
        and last_high["index"] > prev_high["index"]
    ):
        return {
            "direction": "BUY",
            "type": "Bullish BOS",
            "level": last_high["price"]
        }

    # Bearish BOS
    if (
        last_low["price"] < prev_low["price"]
        and close < last_low["price"]
        and last_low["index"] > prev_low["index"]
    ):
        return {
            "direction": "SELL",
            "type": "Bearish BOS",
            "level": last_low["price"]
        }

    return None
