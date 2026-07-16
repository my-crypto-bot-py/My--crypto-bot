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

def detect_mss(df, swing_highs, swing_lows):

    if len(swing_highs) < 3 or len(swing_lows) < 3:
        return None

    close = float(df["close"].iloc[-1])

    last_high = swing_highs[-1]["price"]
    prev_high = swing_highs[-2]["price"]

    last_low = swing_lows[-1]["price"]
    prev_low = swing_lows[-2]["price"]

    # Bullish MSS
    if (
        last_low > prev_low
        and
        close > last_high
    ):

        return {

            "direction": "BUY",

            "type": "Bullish MSS",

            "level": last_high

        }

    # Bearish MSS
    if (
        last_high < prev_high
        and
        close < last_low
    ):

        return {

            "direction": "SELL",

            "type": "Bearish MSS",

            "level": last_low

        }

    return None

def detect_choch(df, swing_highs, swing_lows):

    if len(swing_highs) < 3 or len(swing_lows) < 3:
        return None

    close = float(df["close"].iloc[-1])

    last_high = swing_highs[-1]["price"]
    prev_high = swing_highs[-2]["price"]

    last_low = swing_lows[-1]["price"]
    prev_low = swing_lows[-2]["price"]

    # Bullish CHoCH
    if (

        last_high < prev_high

        and

        close > last_high

    ):

        return {

            "direction": "BUY",

            "type": "Bullish CHoCH",

            "level": last_high

        }

    # Bearish CHoCH
    if (

        last_low > prev_low

        and

        close < last_low

    ):

        return {

            "direction": "SELL",

            "type": "Bearish CHoCH",

            "level": last_low

        }

    return None

# ==========================
# EQUAL HIGH / EQUAL LOW
# ==========================

def detect_equal_levels(
    swing_highs,
    swing_lows,
    tolerance=0.001
):

    result = {}

    if len(swing_highs) >= 2:

        h1 = swing_highs[-1]["price"]
        h2 = swing_highs[-2]["price"]

        if abs(h1 - h2) / h2 <= tolerance:

            result["equal_high"] = h1

    if len(swing_lows) >= 2:

        l1 = swing_lows[-1]["price"]
        l2 = swing_lows[-2]["price"]

        if abs(l1 - l2) / l2 <= tolerance:

            result["equal_low"] = l1

    return result



# ==========================
# DISPLACEMENT
# ==========================

def detect_displacement(df):

    if len(df) < 20:
        return None

    body = abs(
        float(df["close"].iloc[-1]) -
        float(df["open"].iloc[-1])
    )

    avg_body = (
        df["close"] -
        df["open"]
    ).abs().tail(20).mean()

    if body >= avg_body * 2:

        if df["close"].iloc[-1] > df["open"].iloc[-1]:

            return {
                "direction": "BUY",
                "strength": round(body / avg_body, 2)
            }

        else:

            return {
                "direction": "SELL",
                "strength": round(body / avg_body, 2)
            }

    return None



# ==========================
# LIQUIDITY GRAB
# ==========================

def detect_liquidity_grab(
    df,
    swing_highs,
    swing_lows
):

    if len(swing_highs) < 1 or len(swing_lows) < 1:
        return None

    last = df.iloc[-1]

    last_high = swing_highs[-1]["price"]
    last_low = swing_lows[-1]["price"]

    # Buy-side liquidity grab
    if (
        float(last["high"]) > last_high
        and
        float(last["close"]) < last_high
    ):

        return {
            "direction": "SELL",
            "type": "Buy Side Liquidity Grab"
        }

    # Sell-side liquidity grab
    if (
        float(last["low"]) < last_low
        and
        float(last["close"]) > last_low
    ):

        return {
            "direction": "BUY",
            "type": "Sell Side Liquidity Grab"
        }

    return None
