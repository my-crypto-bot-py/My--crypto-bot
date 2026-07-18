import pandas as pd

# ==========================
# LIQUIDITY SWEEP
# ==========================

def detect_liquidity_sweep(df, lookback=20):

    if len(df) < lookback:
        return None

    recent = df.iloc[-lookback:-1]
    current = df.iloc[-1]

    previous_high = float(recent["high"].max())
    previous_low = float(recent["low"].min())

    body = abs(float(current["close"]) - float(current["open"]))

    upper_wick = float(current["high"]) - max(
        float(current["open"]),
        float(current["close"])
    )

    lower_wick = min(
        float(current["open"]),
        float(current["close"])
    ) - float(current["low"])

    # Buy-side liquidity sweep
    if (
        float(current["high"]) > previous_high
        and float(current["close"]) < previous_high
        and upper_wick > body
    ):
        return {
            "direction": "SELL",
            "type": "Buy Side Liquidity Sweep",
            "level": previous_high
        }

    # Sell-side liquidity sweep
    if (
        float(current["low"]) < previous_low
        and float(current["close"]) > previous_low
        and lower_wick > body
    ):
        return {
            "direction": "BUY",
            "type": "Sell Side Liquidity Sweep",
            "level": previous_low
        }

    return None


# ==========================
# FAIR VALUE GAP
# ==========================

def detect_fvg(df):

    if len(df) < 5:
        return None

    c1 = df.iloc[-3]
    c2 = df.iloc[-2]
    c3 = df.iloc[-1]

    # Bullish FVG
    if (
        float(c1["high"]) < float(c3["low"])
        and float(c2["close"]) > float(c2["open"])
    ):
        return {
            "direction": "BUY",
            "type": "Bullish FVG",
            "top": float(c3["low"]),
            "bottom": float(c1["high"])
        }

    # Bearish FVG
    if (
        float(c1["low"]) > float(c3["high"])
        and float(c2["close"]) < float(c2["open"])
    ):
        return {
            "direction": "SELL",
            "type": "Bearish FVG",
            "top": float(c1["low"]),
            "bottom": float(c3["high"])
        }

    return None


# ==========================
# ORDER BLOCK
# ==========================

def detect_order_block(df, lookback=50):

    if len(df) < lookback:
        return None

    data = df.iloc[-lookback:]

    for i in range(len(data) - 2, 0, -1):

        candle = data.iloc[i]
        next_candle = data.iloc[i + 1]

        candle_range = float(candle["high"]) - float(candle["low"])

        if candle_range == 0:
            continue

        next_move = abs(
            float(next_candle["close"]) -
            float(next_candle["open"])
        )

        # Bullish Order Block
        if (
            float(candle["close"]) < float(candle["open"])
            and float(next_candle["close"]) > float(candle["high"])
            and next_move > candle_range * 0.5
        ):
            return {
                "direction": "BUY",
                "type": "Bullish Order Block",
                "high": float(candle["high"]),
                "low": float(candle["low"])
            }

        # Bearish Order Block
        if (
            float(candle["close"]) > float(candle["open"])
            and float(next_candle["close"]) < float(candle["low"])
            and next_move > candle_range * 0.5
        ):
            return {
                "direction": "SELL",
                "type": "Bearish Order Block",
                "high": float(candle["high"]),
                "low": float(candle["low"])
            }

    return None
    # ==========================
# PREMIUM / DISCOUNT ZONE
# ==========================

def get_premium_discount(df):

    if len(df) < 20:
        return None

    high = float(df["high"].tail(20).max())
    low = float(df["low"].tail(20).min())
    price = float(df["close"].iloc[-1])

    range_size = high - low

    if range_size == 0:
        return None

    position = ((price - low) / range_size) * 100

    if position >= 75:
        zone = "Deep Premium"

    elif position >= 50:
        zone = "Premium"

    elif position <= 25:
        zone = "Deep Discount"

    else:
        zone = "Discount"

    equilibrium = (high + low) / 2

    return {
        "zone": zone,
        "high": high,
        "low": low,
        "equilibrium": equilibrium,
        "price": price,
        "position": round(position, 2)
    }


# ==========================
# FRESH ORDER BLOCK
# ==========================

def is_fresh_order_block(df, order_block):

    if order_block is None:
        return False

    high = order_block["high"]
    low = order_block["low"]

    recent = df.tail(5)

    if order_block["direction"] == "BUY":
        if recent["low"].min() < low:
            return False

    elif order_block["direction"] == "SELL":
        if recent["high"].max() > high:
            return False

    return True


# ==========================
# TRADE LEVEL ENGINE
# ==========================

def generate_trade_levels(
    df,
    signal,
    fvg=None,
    order_block=None,
    liquidity=None
):

    price = float(df["close"].iloc[-1])

    if signal == "BUY":

        entry = price

        if order_block and order_block["direction"] == "BUY":

            entry = (
                order_block["high"] +
                order_block["low"]
            ) / 2

            sl = order_block["low"] * 0.998

        elif fvg and fvg["direction"] == "BUY":

            entry = (
                fvg["top"] +
                fvg["bottom"]
            ) / 2

            sl = fvg["bottom"] * 0.998

        else:

            swing_low = float(df["low"].tail(30).min())
            sl = swing_low * 0.998

        risk = entry - sl

        if risk <= 0:
            return None

        recent_high = float(df["high"].tail(50).max())

        tp1 = recent_high

        if tp1 <= entry:
            tp1 = entry + (risk * 2)

        tp2 = entry + (risk * 3) 
     
    elif signal == "SELL":

        entry = price

        if order_block and order_block["direction"] == "SELL":

            entry = (
                order_block["high"] +
                order_block["low"]
            ) / 2

            sl = order_block["high"] * 1.002

        elif fvg and fvg["direction"] == "SELL":

            entry = (
                fvg["top"] +
                fvg["bottom"]
            ) / 2

            sl = fvg["top"] * 1.002

        else:

            swing_high = float(df["high"].tail(30).max())
            sl = swing_high * 1.002

        risk = sl - entry

        if risk <= 0:
            return None

        recent_low = float(df["low"].tail(50).min())

        tp1 = recent_low

        if tp1 >= entry:
            tp1 = entry - (risk * 2)

        tp2 = entry - (risk * 3)

    else:
        return None

    return {
        "entry": round(entry, 4),
        "sl": round(sl, 4),
        "tp1": round(tp1, 4),
        "tp2": round(tp2, 4)
    }
