import pandas as pd
import numpy as np

# ==========================
# ICT SMART MONEY ENGINE V5
# ==========================

FVG_LOOKBACK = 80

OB_LOOKBACK = 80

LIQUIDITY_LOOKBACK = 50

DISPLACEMENT_MULTIPLIER = 1.5


# ==========================
# PREPARE DATA
# ==========================

def prepare_smart_money(df):

    df = df.copy()

    numeric = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]

    for col in numeric:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )

    df.dropna(inplace=True)

    df.reset_index(

        drop=True,

        inplace=True

    )

    return df


# ==========================
# CANDLE BODY
# ==========================

def candle_body(

    candle

):

    return abs(

        float(candle["close"])

        -

        float(candle["open"])

    )


# ==========================
# CANDLE RANGE
# ==========================

def candle_range(

    candle

):

    return (

        float(candle["high"])

        -

        float(candle["low"])

    )


# ==========================
# BULLISH CANDLE
# ==========================

def bullish(

    candle

):

    return (

        candle["close"]

        >

        candle["open"]

    )


# ==========================
# BEARISH CANDLE
# ==========================

def bearish(

    candle

):

    return (

        candle["close"]

        <

        candle["open"]

    )
    # ==========================
# DISPLACEMENT ENGINE
# ==========================

def detect_displacement(

    df,

    multiplier=DISPLACEMENT_MULTIPLIER

):

    df = prepare_smart_money(df)

    if len(df) < 20:

        return None

    ranges = (

        df["high"]

        -

        df["low"]

    )

    average_range = (

        ranges

        .tail(20)

        .mean()

    )

    last = df.iloc[-1]

    last_range = (

        float(last["high"])

        -

        float(last["low"])

    )

    if last_range >= average_range * multiplier:

        return {

            "valid": True,

            "direction":

            "BUY"

            if bullish(last)

            else "SELL",

            "range":

            round(last_range, 2),

            "average":

            round(average_range, 2)

        }

    return {

        "valid": False,

        "direction": None,

        "range":

        round(last_range, 2),

        "average":

        round(average_range, 2)

    }


# ==========================
# IMPULSE CANDLE
# ==========================

def strong_impulse_candle(df):

    result = detect_displacement(df)

    if result is None:

        return False

    return result["valid"]


# ==========================
# INSTITUTIONAL CANDLE
# ==========================

def institutional_candle(df):

    if len(df) < 2:

        return False

    last = df.iloc[-1]

    body = candle_body(last)

    rng = candle_range(last)

    if rng == 0:

        return False

    body_ratio = body / rng

    displacement = detect_displacement(df)

    return (

        body_ratio >= 0.7

        and

        displacement

        and

        displacement["valid"]

    )
    # ==========================
# FAIR VALUE GAP (FVG)
# ==========================

def detect_fvg(df):

    df = prepare_smart_money(df)

    if len(df) < 3:

        return None

    for i in range(

        len(df) - 2,

        max(-1, len(df) - FVG_LOOKBACK),

        -1

    ):

        c1 = df.iloc[i - 2]

        c2 = df.iloc[i - 1]

        c3 = df.iloc[i]

        # Bullish FVG
        if (

            float(c1["high"])

            <

            float(c3["low"])

        ):

            return {

                "direction": "BUY",

                "type": "Bullish FVG",

                "high": float(c3["low"]),

                "low": float(c1["high"]),

                "index": i

            }

        # Bearish FVG
        if (

            float(c1["low"])

            >

            float(c3["high"])

        ):

            return {

                "direction": "SELL",

                "type": "Bearish FVG",

                "high": float(c1["low"]),

                "low": float(c3["high"]),

                "index": i

            }

    return None


# ==========================
# FVG STATUS
# ==========================

def fvg_open(df):

    fvg = detect_fvg(df)

    if fvg is None:

        return False

    price = float(

        df["close"].iloc[-1]

    )

    return (

        fvg["low"]

        <=

        price

        <=

        fvg["high"]

    )


# ==========================
# FVG SUMMARY
# ==========================

def analyze_fvg(df):

    fvg = detect_fvg(df)

    return {

        "fvg": fvg,

        "active": fvg_open(df)

    }
    # ==========================
# ORDER BLOCK ENGINE V5
# ==========================

def detect_order_block(df):

    df = prepare_smart_money(df)

    if len(df) < 5:

        return None

    start = max(

        1,

        len(df) - OB_LOOKBACK

    )

    for i in range(

        len(df) - 2,

        start - 1,

        -1

    ):

        candle = df.iloc[i]

        nxt = df.iloc[i + 1]

        # Bullish Order Block
        if (

            bearish(candle)

            and

            bullish(nxt)

        ):

            return {

                "direction": "BUY",

                "type": "Bullish Order Block",

                "high": float(candle["high"]),

                "low": float(candle["low"]),

                "index": i

            }

        # Bearish Order Block
        if (

            bullish(candle)

            and

            bearish(nxt)

        ):

            return {

                "direction": "SELL",

                "type": "Bearish Order Block",

                "high": float(candle["high"]),

                "low": float(candle["low"]),

                "index": i

            }

    return None


# ==========================
# ORDER BLOCK ACTIVE
# ==========================

def order_block_active(df):

    ob = detect_order_block(df)

    if ob is None:

        return False

    price = float(

        df["close"].iloc[-1]

    )

    return (

        ob["low"]

        <=

        price

        <=

        ob["high"]

    )


# ==========================
# ORDER BLOCK SUMMARY
# ==========================

def analyze_order_block(df):

    ob = detect_order_block(df)

    return {

        "order_block": ob,

        "active": order_block_active(df)

    }
    # ==========================
# BUY SIDE LIQUIDITY
# ==========================

def detect_buy_side_liquidity(df):

    highs = df["high"].tail(

        LIQUIDITY_LOOKBACK

    )

    level = float(

        highs.max()

    )

    return {

        "direction": "BUY",

        "level": level

    }


# ==========================
# SELL SIDE LIQUIDITY
# ==========================

def detect_sell_side_liquidity(df):

    lows = df["low"].tail(

        LIQUIDITY_LOOKBACK

    )

    level = float(

        lows.min()

    )

    return {

        "direction": "SELL",

        "level": level

    }


# ==========================
# LIQUIDITY SWEEP
# ==========================

def detect_liquidity_sweep(df):

    buy = detect_buy_side_liquidity(df)

    sell = detect_sell_side_liquidity(df)

    candle = df.iloc[-1]

    # Buy Side Sweep
    if (

        float(candle["high"])

        >

        buy["level"]

    ):

        return {

            "direction": "SELL",

            "type": "Buy Side Sweep",

            "level": buy["level"]

        }

    # Sell Side Sweep
    if (

        float(candle["low"])

        <

        sell["level"]

    ):

        return {

            "direction": "BUY",

            "type": "Sell Side Sweep",

            "level": sell["level"]

        }

    return None


# ==========================
# LIQUIDITY GRAB
# ==========================

def detect_liquidity_grab(df):

    sweep = detect_liquidity_sweep(df)

    if sweep is None:

        return None

    return {

        "direction": sweep["direction"],

        "type": "Liquidity Grab",

        "level": sweep["level"]

    }
    # ==========================
# PREMIUM / DISCOUNT ZONE
# ==========================

def detect_pd_zone(df):

    high = float(

        df["high"].tail(50).max()

    )

    low = float(

        df["low"].tail(50).min()

    )

    price = float(

        df["close"].iloc[-1]

    )

    equilibrium = (

        high + low

    ) / 2

    if price > equilibrium:

        zone = "PREMIUM"

    elif price < equilibrium:

        zone = "DISCOUNT"

    else:

        zone = "EQUILIBRIUM"

    return {

        "zone": zone,

        "high": round(high, 2),

        "low": round(low, 2),

        "equilibrium": round(equilibrium, 2),

        "price": round(price, 2)

    }


# ==========================
# SMART MONEY ZONE
# ==========================

def detect_smart_money_zone(df):

    ob = detect_order_block(df)

    fvg = detect_fvg(df)

    pd = detect_pd_zone(df)

    return {

        "order_block": ob,

        "fvg": fvg,

        "pd_zone": pd

    }


# ==========================
# BEST POI
# ==========================

def best_poi(df):

    ob = detect_order_block(df)

    if ob:

        return ob

    fvg = detect_fvg(df)

    if fvg:

        return fvg

    return None


# ==========================
# SMART MONEY SUMMARY
# ==========================

def smart_money_summary(df):

    return {

        "poi": best_poi(df),

        "zone": detect_pd_zone(df),

        "liquidity": detect_liquidity_grab(df)

    }
    # ==========================
# SMART MONEY CONFLUENCE
# ==========================

def smart_money_confluence(df):

    ob = detect_order_block(df)

    fvg = detect_fvg(df)

    liquidity = detect_liquidity_grab(df)

    displacement = detect_displacement(df)

    score = 0

    reasons = []

    # Order Block
    if ob is not None:

        score += 30

        reasons.append("Order Block")

    # Fair Value Gap
    if fvg is not None:

        score += 25

        reasons.append("FVG")

    # Liquidity Grab
    if liquidity is not None:

        score += 25

        reasons.append("Liquidity Grab")

    # Displacement
    if (

        displacement is not None

        and

        displacement["valid"]

    ):

        score += 20

        reasons.append("Displacement")

    if score > 100:

        score = 100

    return {

        "score": score,

        "reasons": reasons

    }


# ==========================
# SMART MONEY STRENGTH
# ==========================

def smart_money_strength(df):

    result = smart_money_confluence(df)

    score = result["score"]

    if score >= 80:

        strength = "STRONG"

    elif score >= 60:

        strength = "GOOD"

    elif score >= 40:

        strength = "AVERAGE"

    else:

        strength = "WEAK"

    return {

        "strength": strength,

        "score": score,

        "reasons": result["reasons"]

    }


# ==========================
# CONFLUENCE CHECK
# ==========================

def institutional_confirmation(df):

    result = smart_money_strength(df)

    return result["score"] >= 60
    # ==========================
# INSTITUTIONAL ENTRY FILTER
# ==========================

def institutional_entry_filter(df):

    ob = detect_order_block(df)

    fvg = detect_fvg(df)

    displacement = detect_displacement(df)

    liquidity = detect_liquidity_grab(df)

    pd_zone = detect_pd_zone(df)

    if ob is None:

        return False

    if displacement is None or not displacement["valid"]:

        return False

    if liquidity is None:

        return False

    return True


# ==========================
# TRADE DIRECTION
# ==========================

def smart_money_direction(df):

    ob = detect_order_block(df)

    if ob is not None:

        return ob["direction"]

    fvg = detect_fvg(df)

    if fvg is not None:

        return fvg["direction"]

    liquidity = detect_liquidity_grab(df)

    if liquidity is not None:

        return liquidity["direction"]

    return None


# ==========================
# FINAL SMART MONEY ANALYSIS
# ==========================

def analyze_smart_money_v5(df):

    return {

        "direction": smart_money_direction(df),

        "entry_valid": institutional_entry_filter(df),

        "order_block": detect_order_block(df),

        "fvg": detect_fvg(df),

        "liquidity": detect_liquidity_grab(df),

        "displacement": detect_displacement(df),

        "pd_zone": detect_pd_zone(df),

        "strength": smart_money_strength(df)

    }
    # ==========================
# SMART MONEY DEBUG PANEL
# ==========================

def debug_smart_money(df):

    result = analyze_smart_money_v5(df)

    print("\n========== SMART MONEY V5 ==========")

    print("Direction     :", result["direction"])

    print("Entry Valid   :", result["entry_valid"])

    print("Order Block   :", result["order_block"])

    print("FVG           :", result["fvg"])

    print("Liquidity     :", result["liquidity"])

    print("Displacement  :", result["displacement"])

    print("PD Zone       :", result["pd_zone"])

    print("Strength      :", result["strength"]["strength"])

    print("Score         :", result["strength"]["score"])

    print("Reasons       :", ", ".join(result["strength"]["reasons"]))

    print("====================================\n")

    return result


# ==========================
# SMART MONEY REPORT
# ==========================

def smart_money_report(df):

    result = analyze_smart_money_v5(df)

    return {

        "direction": result["direction"],

        "entry_valid": result["entry_valid"],

        "score": result["strength"]["score"],

        "strength": result["strength"]["strength"],

        "reasons": result["strength"]["reasons"],

        "order_block": result["order_block"],

        "fvg": result["fvg"],

        "liquidity": result["liquidity"],

        "pd_zone": result["pd_zone"]

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_smart_money(df):

    result = analyze_smart_money_v5(df)

    return {

        "liquidity": result["liquidity"],

        "fvg": result["fvg"],

        "order_block": result["order_block"],

        "fresh_ob": result["order_block"],

        "zone": result["pd_zone"],

        "displacement": result["displacement"],

        "liquidity_grab": result["liquidity"]

    }


# ==========================
# TRADE LEVELS
# ==========================

def generate_trade_levels(

    df,

    direction,

    fvg,

    order_block,

    liquidity

):

    price = float(df["close"].iloc[-1])

    atr = (

        df["high"]

        -

        df["low"]

    ).tail(14).mean()

    if direction == "BUY":

        entry = price

        sl = price - atr

        tp1 = price + (atr * 2)

        tp2 = price + (atr * 3)

    elif direction == "SELL":

        entry = price

        sl = price + atr

        tp1 = price - (atr * 2)

        tp2 = price - (atr * 3)

    else:

        return None

    return {

        "entry": round(entry, 2),

        "sl": round(sl, 2),

        "tp1": round(tp1, 2),

        "tp2": round(tp2, 2)

    }


# ==========================
# EXPORTS
# ==========================

__all__ = [

    "detect_order_block",

    "detect_fvg",

    "detect_liquidity_grab",

    "detect_displacement",

    "detect_pd_zone",

    "smart_money_strength",

    "analyze_smart_money",

    "analyze_smart_money_v5",

    "generate_trade_levels",

    "debug_smart_money",

    "smart_money_report"

]
