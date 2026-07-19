import pandas as pd
import numpy as np

# ==========================
# ICT STRUCTURE ENGINE V2
# ==========================


# ==========================
# SWING SETTINGS
# ==========================

SWING_LENGTH = 3


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

    if current <= left.max():
        return False

    if current <= right.max():
        return False

    return True


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

    if current >= left.min():
        return False

    if current >= right.min():
        return False

    return True


# ==========================
# GET ALL SWINGS
# ==========================

def get_swings(df):

    swing_highs = []

    swing_lows = []

    for i in range(len(df)):

        if is_swing_high(df, i):

            swing_highs.append({

                "index": i,

                "price": float(df["high"].iloc[i])

            })

        if is_swing_low(df, i):

            swing_lows.append({

                "index": i,

                "price": float(df["low"].iloc[i])

            })

    return swing_highs, swing_lows
    # ==========================
# REMOVE DUPLICATE SWINGS
# ==========================

def clean_swings(swings, min_distance=3):

    if not swings:
        return []

    cleaned = [swings[0]]

    for swing in swings[1:]:

        last = cleaned[-1]

        if swing["index"] - last["index"] >= min_distance:

            cleaned.append(swing)

        else:

            if swing["price"] > last["price"]:

                cleaned[-1] = swing

    return cleaned


# ==========================
# LAST SWING HIGH
# ==========================

def get_last_swing_high(swing_highs):

    if len(swing_highs) == 0:
        return None

    return swing_highs[-1]


# ==========================
# LAST SWING LOW
# ==========================

def get_last_swing_low(swing_lows):

    if len(swing_lows) == 0:
        return None

    return swing_lows[-1]


# ==========================
# EQUAL HIGH
# ==========================

def detect_equal_high(swing_highs, tolerance=0.001):

    if len(swing_highs) < 2:
        return None

    h1 = swing_highs[-2]["price"]
    h2 = swing_highs[-1]["price"]

    if abs(h1 - h2) / h1 <= tolerance:

        return {

            "type": "Equal High",

            "price": round((h1 + h2) / 2, 4)

        }

    return None


# ==========================
# EQUAL LOW
# ==========================

def detect_equal_low(swing_lows, tolerance=0.001):

    if len(swing_lows) < 2:
        return None

    l1 = swing_lows[-2]["price"]
    l2 = swing_lows[-1]["price"]

    if abs(l1 - l2) / l1 <= tolerance:

        return {

            "type": "Equal Low",

            "price": round((l1 + l2) / 2, 4)

        }

    return None
    # ==========================
# BULLISH BOS
# ==========================

def detect_bullish_bos(df, swing_highs):

    if len(swing_highs) == 0:
        return None

    last_high = swing_highs[-1]

    current_close = float(df["close"].iloc[-1])

    if current_close > last_high["price"]:

        return {

            "direction": "BUY",

            "type": "Bullish BOS",

            "level": last_high["price"],

            "index": last_high["index"]

        }

    return None


# ==========================
# BEARISH BOS
# ==========================

def detect_bearish_bos(df, swing_lows):

    if len(swing_lows) == 0:
        return None

    last_low = swing_lows[-1]

    current_close = float(df["close"].iloc[-1])

    if current_close < last_low["price"]:

        return {

            "direction": "SELL",

            "type": "Bearish BOS",

            "level": last_low["price"],

            "index": last_low["index"]

        }

    return None
            # ==========================
# CHoCH
# ==========================

def detect_choch(df, swing_highs, swing_lows):

    if len(swing_highs) < 2:
        return None

    if len(swing_lows) < 2:
        return None


    current_close = float(
        df["close"].iloc[-1]
    )


    last_high = swing_highs[-1]["price"]
    previous_high = swing_highs[-2]["price"]


    last_low = swing_lows[-1]["price"]
    previous_low = swing_lows[-2]["price"]


    # Bullish CHoCH

    if (

        last_low < previous_low

        and

        current_close > previous_high

    ):

        return {

            "direction": "BUY",

            "type": "Bullish CHoCH",

            "level": previous_high

        }


    # Bearish CHoCH

    if (

        last_high > previous_high

        and

        current_close < previous_low

    ):

        return {

            "direction": "SELL",

            "type": "Bearish CHoCH",

            "level": previous_low

        }


    return None


# ==========================
# MARKET STRUCTURE SHIFT
# ==========================

def detect_mss(df, bos=None, choch=None):

    if choch:

        return {

            "direction": choch["direction"],

            "type": "Market Structure Shift"

        }


    if bos:

        return {

            "direction": bos["direction"],

            "type": "Market Structure Continuation"

        }


    return None
    # ==========================
# STRONG SWING FILTER
# ==========================

def filter_strong_swings(
    df,
    swings,
    atr_multiplier=0.5
):

    if len(df) < 20:
        return swings

    atr = (
        (
            df["high"] - df["low"]
        )
        .rolling(14)
        .mean()
        .iloc[-1]
    )

    if pd.isna(atr):
        return swings

    filtered = []

    for swing in swings:

        idx = swing["index"]

        if idx <= 0:
            continue

        candle_range = float(
            df.iloc[idx]["high"]
            -
            df.iloc[idx]["low"]
        )

        if candle_range >= atr * atr_multiplier:

            filtered.append(swing)

    return filtered


# ==========================
# INSTITUTIONAL
# EQUAL LEVELS
# ==========================

def detect_equal_levels(
    swing_highs,
    swing_lows,
    tolerance=0.001
):

    return {

        "equal_high":
        detect_equal_high(
            swing_highs,
            tolerance
        ),

        "equal_low":
        detect_equal_low(
            swing_lows,
            tolerance
        )

    }


# ==========================
# STRUCTURE DIRECTION
# ==========================

def get_structure_direction(
    bos=None,
    choch=None,
    mss=None
):

    if choch:
        return choch["direction"]

    if mss:
        return mss["direction"]

    if bos:
        return bos["direction"]

    return None
    # ==========================
# COMPLETE STRUCTURE ANALYSIS
# ==========================

def analyze_structure(df):

    # Raw Swings
    swing_highs = detect_swing_highs(df)
    swing_lows = detect_swing_lows(df)

    # Strong Swings Only
    swing_highs = filter_strong_swings(
        df,
        swing_highs
    )

    swing_lows = filter_strong_swings(
        df,
        swing_lows
    )

    # BOS
    bos = detect_bos(
        df,
        swing_highs,
        swing_lows
    )

    # CHoCH
    choch = detect_choch(
        df,
        swing_highs,
        swing_lows
    )

    # MSS
    mss = detect_mss(
        df,
        bos,
        choch
    )

    # Equal High / Low
    equal_levels = detect_equal_levels(
        swing_highs,
        swing_lows
    )

    # Final Direction
    direction = get_structure_direction(
        bos,
        choch,
        mss
    )

    return {

        "direction": direction,

        "bos": bos,

        "choch": choch,

        "mss": mss,

        "swing_highs": swing_highs,

        "swing_lows": swing_lows,

        "equal_levels": equal_levels

    }


# ==========================
# DEBUG STRUCTURE
# ==========================

def debug_structure(df):

    result = analyze_structure(df)

    print("\n===== STRUCTURE DEBUG =====")

    print("Direction :", result["direction"])

    print("BOS       :", result["bos"])

    print("CHoCH     :", result["choch"])

    print("MSS       :", result["mss"])

    print("Equal Lvls:", result["equal_levels"])

    print("Swing Highs:", len(result["swing_highs"]))

    print("Swing Lows :", len(result["swing_lows"]))

    print("===========================\n")
    # ==========================
# BOS CONFIRMATION
# ==========================

def confirm_bos(df, bos):

    if bos is None:
        return False

    if len(df) < 3:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    if bos["direction"] == "BUY":

        return (

            float(last["close"])
            >
            float(prev["high"])

        )

    if bos["direction"] == "SELL":

        return (

            float(last["close"])
            <
            float(prev["low"])

        )

    return False


# ==========================
# CHOCH CONFIRMATION
# ==========================

def confirm_choch(df, choch):

    if choch is None:
        return False

    return True


# ==========================
# MSS CONFIRMATION
# ==========================

def confirm_mss(df, mss):

    if mss is None:
        return False

    return True


# ==========================
# STRUCTURE SCORE
# ==========================

def structure_score(
    bos=None,
    choch=None,
    mss=None
):

    score = 0

    if bos:
        score += 40

    if choch:
        score += 35

    if mss:
        score += 25

    return min(score, 100)


# ==========================
# FINAL STRUCTURE SIGNAL
# ==========================

def get_structure_signal(df):

    result = analyze_structure(df)

    score = structure_score(

        result["bos"],

        result["choch"],

        result["mss"]

    )

    result["score"] = score

    result["confirmed"] = (

        confirm_bos(df, result["bos"])

        or

        confirm_choch(df, result["choch"])

        or

        confirm_mss(df, result["mss"])

    )

    return result
