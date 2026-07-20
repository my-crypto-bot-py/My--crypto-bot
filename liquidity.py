import pandas as pd
import numpy as np

# ==========================
# ICT LIQUIDITY ENGINE V5
# ==========================

SWING_LENGTH = 3
EQUAL_TOLERANCE = 0.001
LOOKBACK = 100


# ==========================
# SWING HIGH
# ==========================

def is_swing_high(df, index, length=SWING_LENGTH):

    if index < length:
        return False

    if index >= len(df) - length:
        return False

    current = float(df["high"].iloc[index])

    left = df["high"].iloc[index-length:index]
    right = df["high"].iloc[index+1:index+length+1]

    return current > left.max() and current > right.max()


# ==========================
# SWING LOW
# ==========================

def is_swing_low(df, index, length=SWING_LENGTH):

    if index < length:
        return False

    if index >= len(df) - length:
        return False

    current = float(df["low"].iloc[index])

    left = df["low"].iloc[index-length:index]
    right = df["low"].iloc[index+1:index+length+1]

    return current < left.min() and current < right.min()


# ==========================
# GET SWINGS
# ==========================

def get_liquidity_swings(df):

    highs = []
    lows = []

    for i in range(len(df)):

        if is_swing_high(df, i):

            highs.append({

                "index": i,

                "price": float(df["high"].iloc[i])

            })

        if is_swing_low(df, i):

            lows.append({

                "index": i,

                "price": float(df["low"].iloc[i])

            })

    return highs, lows


# ==========================
# EQUAL HIGHS
# ==========================

def detect_equal_highs(highs):

    result = []

    for i in range(len(highs)-1):

        a = highs[i]
        b = highs[i+1]

        if abs(a["price"] - b["price"]) <= a["price"] * EQUAL_TOLERANCE:

            result.append({

                "type": "Equal High",

                "price": a["price"],

                "first": a["index"],

                "second": b["index"]

            })

    return result


# ==========================
# EQUAL LOWS
# ==========================

def detect_equal_lows(lows):

    result = []

    for i in range(len(lows)-1):

        a = lows[i]
        b = lows[i+1]

        if abs(a["price"] - b["price"]) <= a["price"] * EQUAL_TOLERANCE:

            result.append({

                "type": "Equal Low",

                "price": a["price"],

                "first": a["index"],

                "second": b["index"]

            })

    return result
    # ==========================
# BUY SIDE LIQUIDITY (BSL)
# ==========================

def detect_buy_side_liquidity(df):

    swing_highs, _ = get_liquidity_swings(df)

    equal_highs = detect_equal_highs(swing_highs)

    pools = []

    for eq in equal_highs:

        pools.append({

            "direction": "SELL",

            "type": "Buy Side Liquidity",

            "price": eq["price"],

            "first": eq["first"],

            "second": eq["second"]

        })

    return pools


# ==========================
# SELL SIDE LIQUIDITY (SSL)
# ==========================

def detect_sell_side_liquidity(df):

    _, swing_lows = get_liquidity_swings(df)

    equal_lows = detect_equal_lows(swing_lows)

    pools = []

    for eq in equal_lows:

        pools.append({

            "direction": "BUY",

            "type": "Sell Side Liquidity",

            "price": eq["price"],

            "first": eq["first"],

            "second": eq["second"]

        })

    return pools


# ==========================
# GET LIQUIDITY POOLS
# ==========================

def get_liquidity_pools(df):

    buy_side = detect_buy_side_liquidity(df)

    sell_side = detect_sell_side_liquidity(df)

    return {

        "buy_side": buy_side,

        "sell_side": sell_side

    }


# ==========================
# LAST BUY SIDE LIQUIDITY
# ==========================

def get_last_buy_side(df):

    pools = detect_buy_side_liquidity(df)

    if len(pools) == 0:
        return None

    return pools[-1]


# ==========================
# LAST SELL SIDE LIQUIDITY
# ==========================

def get_last_sell_side(df):

    pools = detect_sell_side_liquidity(df)

    if len(pools) == 0:
        return None

    return pools[-1]
    # ==========================
# EXTERNAL LIQUIDITY
# ==========================

def detect_external_liquidity(df):

    pools = get_liquidity_pools(df)

    current_price = float(df["close"].iloc[-1])

    signals = []

    for bsl in pools["buy_side"]:

        if current_price < bsl["price"]:

            signals.append({

                "direction": "SELL",

                "type": "External Buy Side Liquidity",

                "price": bsl["price"]

            })

    for ssl in pools["sell_side"]:

        if current_price > ssl["price"]:

            signals.append({

                "direction": "BUY",

                "type": "External Sell Side Liquidity",

                "price": ssl["price"]

            })

    return signals


# ==========================
# INTERNAL LIQUIDITY
# ==========================

def detect_internal_liquidity(df):

    swing_highs, swing_lows = get_liquidity_swings(df)

    result = []

    if len(swing_highs) >= 2:

        last = swing_highs[-1]

        prev = swing_highs[-2]

        result.append({

            "direction": "SELL",

            "type": "Internal High Liquidity",

            "current": last["price"],

            "previous": prev["price"]

        })

    if len(swing_lows) >= 2:

        last = swing_lows[-1]

        prev = swing_lows[-2]

        result.append({

            "direction": "BUY",

            "type": "Internal Low Liquidity",

            "current": last["price"],

            "previous": prev["price"]

        })

    return result


# ==========================
# GET ALL LIQUIDITY
# ==========================

def get_all_liquidity(df):

    return {

        "external": detect_external_liquidity(df),

        "internal": detect_internal_liquidity(df),

        "pools": get_liquidity_pools(df)

    }


# ==========================
# LIQUIDITY SUMMARY
# ==========================

def liquidity_summary(df):

    data = get_all_liquidity(df)

    return {

        "buy_side":

        len(data["pools"]["buy_side"]),

        "sell_side":

        len(data["pools"]["sell_side"]),

        "external":

        len(data["external"]),

        "internal":

        len(data["internal"])

    }
    # ==========================
# LIQUIDITY SWEEP V5
# ==========================

def detect_liquidity_sweep(df, lookback=20):

    if len(df) < lookback:
        return None

    recent = df.iloc[-lookback:-1]
    current = df.iloc[-1]

    previous_high = float(recent["high"].max())
    previous_low = float(recent["low"].min())

    high = float(current["high"])
    low = float(current["low"])

    close = float(current["close"])
    open_price = float(current["open"])

    body = abs(close - open_price)

    upper_wick = high - max(close, open_price)
    lower_wick = min(close, open_price) - low

    # Buy Side Sweep
    if (
        high > previous_high
        and close < previous_high
        and upper_wick > body * 1.5
    ):

        return {

            "direction": "SELL",

            "type": "Buy Side Liquidity Sweep",

            "level": previous_high,

            "strength": round(upper_wick / (body + 0.00001), 2)

        }

    # Sell Side Sweep
    if (
        low < previous_low
        and close > previous_low
        and lower_wick > body * 1.5
    ):

        return {

            "direction": "BUY",

            "type": "Sell Side Liquidity Sweep",

            "level": previous_low,

            "strength": round(lower_wick / (body + 0.00001), 2)

        }

    return None


# ==========================
# LIQUIDITY GRAB V5
# ==========================

def detect_liquidity_grab(df):

    sweep = detect_liquidity_sweep(df)

    if sweep is None:
        return None

    return {

        "direction": sweep["direction"],

        "type": "Liquidity Grab",

        "level": sweep["level"],

        "strength": sweep["strength"]

    }


# ==========================
# SWEEP CONFIRMATION
# ==========================

def confirm_liquidity_sweep(df):

    sweep = detect_liquidity_sweep(df)

    if sweep is None:

        return {

            "valid": False

        }

    if sweep["strength"] >= 2:

        return {

            "valid": True,

            "signal": sweep

        }

    return {

        "valid": False

    }


# ==========================
# LIQUIDITY EVENT
# ==========================

def get_liquidity_event(df):

    grab = detect_liquidity_grab(df)

    if grab:

        return grab

    return detect_liquidity_sweep(df)
    # ==========================
# INDUCEMENT DETECTION
# ==========================

def detect_inducement(df, lookback=30):

    if len(df) < lookback:
        return None

    recent = df.tail(lookback)

    high = float(recent["high"].max())
    low = float(recent["low"].min())

    current = recent.iloc[-1]

    close = float(current["close"])

    if close > high * 0.998:

        return {

            "direction": "SELL",

            "type": "Buy Side Inducement",

            "level": high

        }

    if close < low * 1.002:

        return {

            "direction": "BUY",

            "type": "Sell Side Inducement",

            "level": low

        }

    return None


# ==========================
# LIQUIDITY RAID
# ==========================

def detect_liquidity_raid(df):

    sweep = detect_liquidity_sweep(df)

    if sweep is None:
        return None

    candle = df.iloc[-1]

    body = abs(

        float(candle["close"])

        -

        float(candle["open"])

    )

    rng = (

        float(candle["high"])

        -

        float(candle["low"])

    )

    if rng == 0:
        return None

    ratio = body / rng

    if ratio < 0.35:

        return {

            "direction": sweep["direction"],

            "type": "Liquidity Raid",

            "level": sweep["level"]

        }

    return None


# ==========================
# BULL TRAP
# ==========================

def detect_bull_trap(df):

    raid = detect_liquidity_raid(df)

    if raid is None:
        return None

    if raid["direction"] == "SELL":

        return {

            "direction": "SELL",

            "type": "Bull Trap"

        }

    return None


# ==========================
# BEAR TRAP
# ==========================

def detect_bear_trap(df):

    raid = detect_liquidity_raid(df)

    if raid is None:
        return None

    if raid["direction"] == "BUY":

        return {

            "direction": "BUY",

            "type": "Bear Trap"

        }

    return None


# ==========================
# SMART TRAP
# ==========================

def detect_smart_trap(df):

    bull = detect_bull_trap(df)

    if bull:
        return bull

    bear = detect_bear_trap(df)

    if bear:
        return bear

    return None
    # ==========================
# SESSION SETTINGS
# ==========================

ASIAN_START = 0
ASIAN_END = 8

LONDON_START = 7
LONDON_END = 16

NEWYORK_START = 13
NEWYORK_END = 22


# ==========================
# CURRENT SESSION
# ==========================

def get_current_session(df):

    hour = int(df["timestamp"].iloc[-1].hour)

    if ASIAN_START <= hour < ASIAN_END:
        return "ASIAN"

    if LONDON_START <= hour < LONDON_END:
        return "LONDON"

    if NEWYORK_START <= hour < NEWYORK_END:
        return "NEWYORK"

    return "OFF"


# ==========================
# SESSION HIGH / LOW
# ==========================

def get_session_range(df, session):

    if session == "ASIAN":

        data = df[
            (df["timestamp"].dt.hour >= ASIAN_START)
            &
            (df["timestamp"].dt.hour < ASIAN_END)
        ]

    elif session == "LONDON":

        data = df[
            (df["timestamp"].dt.hour >= LONDON_START)
            &
            (df["timestamp"].dt.hour < LONDON_END)
        ]

    elif session == "NEWYORK":

        data = df[
            (df["timestamp"].dt.hour >= NEWYORK_START)
            &
            (df["timestamp"].dt.hour < NEWYORK_END)
        ]

    else:

        return None

    if len(data) == 0:
        return None

    return {

        "high": float(data["high"].max()),

        "low": float(data["low"].min())

    }


# ==========================
# SESSION LIQUIDITY
# ==========================

def detect_session_liquidity(df):

    session = get_current_session(df)

    levels = get_session_range(df, session)

    if levels is None:
        return None

    return {

        "session": session,

        "high": levels["high"],

        "low": levels["low"]

    }


# ==========================
# SESSION SWEEP
# ==========================

def detect_session_sweep(df):

    info = detect_session_liquidity(df)

    if info is None:
        return None

    candle = df.iloc[-1]

    high = float(candle["high"])

    low = float(candle["low"])

    close = float(candle["close"])

    if high > info["high"] and close < info["high"]:

        return {

            "direction": "SELL",

            "type": info["session"] + " Buy Side Sweep"

        }

    if low < info["low"] and close > info["low"]:

        return {

            "direction": "BUY",

            "type": info["session"] + " Sell Side Sweep"

        }

    return None
    # ==========================
# MULTI TIMEFRAME LIQUIDITY
# ==========================

def get_htf_liquidity(htf_df):

    sweep = detect_liquidity_sweep(htf_df)
    grab = detect_liquidity_grab(htf_df)
    trap = detect_smart_trap(htf_df)

    return {

        "sweep": sweep,

        "grab": grab,

        "trap": trap

    }


# ==========================
# LOWER TIMEFRAME LIQUIDITY
# ==========================

def get_ltf_liquidity(ltf_df):

    sweep = detect_liquidity_sweep(ltf_df)
    grab = detect_liquidity_grab(ltf_df)
    trap = detect_smart_trap(ltf_df)

    return {

        "sweep": sweep,

        "grab": grab,

        "trap": trap

    }


# ==========================
# HTF + LTF CONFIRMATION
# ==========================

def liquidity_timeframe_confirmation(

    htf_df,
    ltf_df

):

    htf = get_htf_liquidity(htf_df)

    ltf = get_ltf_liquidity(ltf_df)


    if (

        htf["sweep"]

        and

        ltf["sweep"]

    ):

        if (

            htf["sweep"]["direction"]

            ==

            ltf["sweep"]["direction"]

        ):

            return {

                "confirm": True,

                "direction":

                htf["sweep"]["direction"],

                "type":

                "HTF + LTF Sweep"

            }


    if (

        htf["grab"]

        and

        ltf["grab"]

    ):

        if (

            htf["grab"]["direction"]

            ==

            ltf["grab"]["direction"]

        ):

            return {

                "confirm": True,

                "direction":

                htf["grab"]["direction"],

                "type":

                "HTF + LTF Grab"

            }


    return {

        "confirm": False

    }


# ==========================
# FINAL MULTI TF LIQUIDITY
# ==========================

def get_multi_tf_liquidity(

    htf_df,
    ltf_df

):

    confirmation = liquidity_timeframe_confirmation(

        htf_df,
        ltf_df

    )


    if confirmation["confirm"]:

        return confirmation


    return None
    # ==========================
# LIQUIDITY STRENGTH
# ==========================

def calculate_liquidity_strength(df):

    score = 0
    reasons = []

    sweep = detect_liquidity_sweep(df)

    if sweep:

        score += 30
        reasons.append(sweep["type"])

    grab = detect_liquidity_grab(df)

    if grab:

        score += 20
        reasons.append(grab["type"])

    inducement = detect_inducement(df)

    if inducement:

        score += 15
        reasons.append(inducement["type"])

    raid = detect_liquidity_raid(df)

    if raid:

        score += 15
        reasons.append(raid["type"])

    trap = detect_smart_trap(df)

    if trap:

        score += 10
        reasons.append(trap["type"])

    session = detect_session_sweep(df)

    if session:

        score += 10
        reasons.append(session["type"])

    if score > 100:
        score = 100

    return {

        "score": score,

        "reasons": reasons

    }


# ==========================
# DISPLACEMENT CONFIRMATION
# ==========================

def liquidity_displacement_confirmation(

    liquidity,

    displacement

):

    if liquidity is None:
        return False

    if displacement is None:
        return False

    return (

        liquidity["direction"]

        ==

        displacement["direction"]

    )


# ==========================
# FINAL LIQUIDITY SCORE
# ==========================

def get_final_liquidity_score(

    df,

    displacement=None

):

    strength = calculate_liquidity_strength(df)

    liquidity = get_liquidity_event(df)

    confirmed = liquidity_displacement_confirmation(

        liquidity,

        displacement

    )

    score = strength["score"]

    if confirmed:

        score += 20

    if score > 100:

        score = 100

    return {

        "score": score,

        "confirmed": confirmed,

        "liquidity": liquidity,

        "reasons": strength["reasons"]

    }
    # ==========================
# FINAL LIQUIDITY ANALYZER
# ==========================

def analyze_liquidity_v5(

    df,

    displacement=None

):

    buy_side = detect_buy_side_liquidity(df)

    sell_side = detect_sell_side_liquidity(df)

    external = detect_external_liquidity(df)

    internal = detect_internal_liquidity(df)

    sweep = detect_liquidity_sweep(df)

    grab = detect_liquidity_grab(df)

    inducement = detect_inducement(df)

    raid = detect_liquidity_raid(df)

    trap = detect_smart_trap(df)

    session = detect_session_sweep(df)

    score = get_final_liquidity_score(

        df,

        displacement

    )

    return {

        "buy_side": buy_side,

        "sell_side": sell_side,

        "external": external,

        "internal": internal,

        "sweep": sweep,

        "grab": grab,

        "inducement": inducement,

        "raid": raid,

        "trap": trap,

        "session": session,

        "score": score

    }


# ==========================
# LIQUIDITY DIRECTION
# ==========================

def get_liquidity_direction(result):

    if result["score"]["liquidity"]:

        return result["score"]["liquidity"]["direction"]

    return None


# ==========================
# DEBUG PANEL
# ==========================

def debug_liquidity(df, displacement=None):

    result = analyze_liquidity_v5(

        df,

        displacement

    )

    print("\n========== LIQUIDITY V5 ==========")

    print("Buy Side :", len(result["buy_side"]))

    print("Sell Side:", len(result["sell_side"]))

    print("External :", len(result["external"]))

    print("Internal :", len(result["internal"]))

    print("Sweep    :", result["sweep"])

    print("Grab     :", result["grab"])

    print("Inducement:", result["inducement"])

    print("Raid     :", result["raid"])

    print("Trap     :", result["trap"])

    print("Session  :", result["session"])

    print("Score    :", result["score"]["score"])

    print("Confirmed:", result["score"]["confirmed"])

    print("=================================\n")

    return result
    # ==========================
# FINAL LIQUIDITY SIGNAL
# ==========================

def get_liquidity_signal(

    df,

    displacement=None

):

    result = analyze_liquidity_v5(

        df,

        displacement

    )

    score = result["score"]["score"]

    liquidity = result["score"]["liquidity"]


    if liquidity is None:

        return {

            "confirm": False,

            "direction": None,

            "score": score,

            "reason": "No Liquidity Event"

        }


    if score < 60:

        return {

            "confirm": False,

            "direction": liquidity["direction"],

            "score": score,

            "reason": "Weak Liquidity"

        }


    return {

        "confirm": True,

        "direction": liquidity["direction"],

        "score": score,

        "reason": liquidity["type"]

    }


# ==========================
# BOT READY FUNCTION
# ==========================

def liquidity_engine_v5(

    df,

    displacement=None

):

    signal = get_liquidity_signal(

        df,

        displacement

    )


    return {

        "direction": signal["direction"],

        "confirm": signal["confirm"],

        "score": signal["score"],

        "reason": signal["reason"]

    }


# ==========================
# MAIN BOT COMPATIBILITY
# ==========================

def analyze_liquidity(df, displacement=None):

    return liquidity_engine_v5(

        df,

        displacement

    )


# ==========================
# EXPORT READY
# ==========================

__all__ = [

    "analyze_liquidity",

    "liquidity_engine_v5",

    "get_liquidity_signal",

    "analyze_liquidity_v5",

    "debug_liquidity"

]
