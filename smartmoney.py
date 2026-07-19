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

    body = abs(
        float(current["close"]) -
        float(current["open"])
    )

    upper_wick = (
        float(current["high"]) -
        max(
            float(current["open"]),
            float(current["close"])
        )
    )

    lower_wick = (
        min(
            float(current["open"]),
            float(current["close"])
        )
        -
        float(current["low"])
    )

    # Buy Side Liquidity Sweep
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

    # Sell Side Liquidity Sweep
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

        candle_range = (
            float(candle["high"]) -
            float(candle["low"])
        )

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
# FRESH ORDER BLOCK
# ==========================

def is_fresh_order_block(df, order_block):

    if order_block is None:
        return False

    recent = df.tail(5)

    if order_block["direction"] == "BUY":

        if recent["low"].min() < order_block["low"]:
            return False

    elif order_block["direction"] == "SELL":

        if recent["high"].max() > order_block["high"]:
            return False

    return True


# ==========================
# PREMIUM / DISCOUNT
# ==========================

def get_premium_discount(df):

    if len(df) < 20:
        return None

    high = float(df["high"].tail(20).max())
    low = float(df["low"].tail(20).min())

    price = float(df["close"].iloc[-1])

    rng = high - low

    if rng == 0:
        return None

    position = ((price - low) / rng) * 100

    if position >= 75:
        zone = "Deep Premium"

    elif position >= 50:
        zone = "Premium"

    elif position <= 25:
        zone = "Deep Discount"

    else:
        zone = "Discount"

    return {
        "zone": zone,
        "high": high,
        "low": low,
        "price": price,
        "equilibrium": (high + low) / 2,
        "position": round(position, 2)
    }
    # ==========================
# LIQUIDITY GRAB
# ==========================

def detect_liquidity_grab(df):

    if len(df) < 20:
        return None

    recent = df.iloc[-20:-1]
    current = df.iloc[-1]

    high = float(recent["high"].max())
    low = float(recent["low"].min())

    # Buy Side Grab
    if (
        float(current["high"]) > high
        and float(current["close"]) < high
    ):
        return {
            "direction": "SELL",
            "type": "Buy Side Liquidity Grab"
        }

    # Sell Side Grab
    if (
        float(current["low"]) < low
        and float(current["close"]) > low
    ):
        return {
            "direction": "BUY",
            "type": "Sell Side Liquidity Grab"
        }

    return None


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

    if avg_body == 0:
        return None

    if body >= avg_body * 2:

        if float(df["close"].iloc[-1]) > float(df["open"].iloc[-1]):

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
# BREAKER BLOCK
# ==========================

def detect_break
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

            sl = float(df["low"].tail(30).min()) * 0.998

        risk = entry - sl

        if risk <= 0:
            return None

        tp1 = float(df["high"].tail(50).max())

        if tp1 <= entry:
            tp1 = entry + risk * 2

        tp2 = entry + risk * 3

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

            sl = float(df["high"].tail(30).max()) * 1.002

        risk = sl - entry

        if risk <= 0:
            return None

        tp1 = float(df["low"].tail(50).min())

        if tp1 >= entry:
            tp1 = entry - risk * 2

        tp2 = entry - risk * 3

    else:
        return None

    return {

        "entry": round(entry,4),

        "sl": round(sl,4),

        "tp1": round(tp1,4),

        "tp2": round(tp2,4)

    }


# ==========================
# SMART MONEY SUMMARY
# ==========================

def analyze_smart_money(df):

    liquidity = detect_liquidity_sweep(df)

    fvg = detect_fvg(df)

    order_block = detect_order_block(df)

    fresh_ob = is_fresh_order_block(
        df,
        order_block
    )

    zone = get_premium_discount(df)

    displacement = detect_displacement(df)

    liquidity_grab = detect_liquidity_grab(df)

    breaker = detect_breaker_block(
        df,
        order_block
    )

    mitigation = detect_mitigation_block(
        df,
        order_block
    )

    rejection = detect_rejection_block(df)

    return {

        "liquidity": liquidity,

        "fvg": fvg,

        "order_block": order_block,

        "fresh_ob": fresh_ob,

        "zone": zone,

        "displacement": displacement,

        "liquidity_grab": liquidity_grab,

        "breaker": breaker,

        "mitigation": mitigation,

        "rejection": rejection

    }
