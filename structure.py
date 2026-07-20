import pandas as pd
import numpy as np

# ==========================
# ICT STRUCTURE ENGINE V5
# ==========================

SWING_LENGTH = 3


# ==========================
# SWING HIGH
# ==========================

def is_swing_high(

    df,

    index,

    length=SWING_LENGTH

):

    if index < length:

        return False

    if index >= len(df) - length:

        return False

    current = float(

        df["high"].iloc[index]

    )

    left = df["high"].iloc[

        index-length:index

    ]

    right = df["high"].iloc[

        index+1:index+length+1

    ]

    return (

        current > left.max()

        and

        current > right.max()

    )


# ==========================
# SWING LOW
# ==========================

def is_swing_low(

    df,

    index,

    length=SWING_LENGTH

):

    if index < length:

        return False

    if index >= len(df) - length:

        return False

    current = float(

        df["low"].iloc[index]

    )

    left = df["low"].iloc[

        index-length:index

    ]

    right = df["low"].iloc[

        index+1:index+length+1

    ]

    return (

        current < left.min()

        and

        current < right.min()

    )


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

                "price":

                float(df["high"].iloc[i])

            })

        if is_swing_low(df, i):

            swing_lows.append({

                "index": i,

                "price":

                float(df["low"].iloc[i])

            })

    return swing_highs, swing_lows


# ==========================
# DETECT SWINGS
# ==========================

def detect_swing_highs(df):

    highs, _ = get_swings(df)

    return highs


def detect_swing_lows(df):

    _, lows = get_swings(df)

    return lows
    # ==========================
# CLEAN SWINGS
# ==========================

def clean_swings(

    swings,

    min_distance=3

):

    if len(swings) == 0:

        return []

    cleaned = [

        swings[0]

    ]

    for swing in swings[1:]:

        last = cleaned[-1]

        if (

            swing["index"]

            -

            last["index"]

            >=

            min_distance

        ):

            cleaned.append(

                swing

            )

        else:

            if (

                swing["price"]

                >

                last["price"]

            ):

                cleaned[-1] = swing

    return cleaned


# ==========================
# LAST SWING HIGH
# ==========================

def get_last_swing_high(df):

    highs = clean_swings(

        detect_swing_highs(df)

    )

    if len(highs) == 0:

        return None

    return highs[-1]


# ==========================
# LAST SWING LOW
# ==========================

def get_last_swing_low(df):

    lows = clean_swings(

        detect_swing_lows(df)

    )

    if len(lows) == 0:

        return None

    return lows[-1]


# ==========================
# SWING TREND
# ==========================

def swing_trend(df):

    high = get_last_swing_high(df)

    low = get_last_swing_low(df)

    if (

        high is None

        or

        low is None

    ):

        return "UNKNOWN"

    if high["index"] > low["index"]:

        return "UPTREND"

    return "DOWNTREND"


# ==========================
# SWING SUMMARY
# ==========================

def swing_summary(df):

    return {

        "trend":

        swing_trend(df),

        "last_high":

        get_last_swing_high(df),

        "last_low":

        get_last_swing_low(df)
        
    }
    # ==========================
# BULLISH BOS
# ==========================

def detect_bullish_bos(

    df,

    swing_highs

):

    if len(swing_highs) == 0:

        return None

    last_high = swing_highs[-1]

    current_close = float(

        df["close"].iloc[-1]

    )

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

def detect_bearish_bos(

    df,

    swing_lows

):

    if len(swing_lows) == 0:

        return None

    last_low = swing_lows[-1]

    current_close = float(

        df["close"].iloc[-1]

    )

    if current_close < last_low["price"]:

        return {

            "direction": "SELL",

            "type": "Bearish BOS",

            "level": last_low["price"],

            "index": last_low["index"]

        }

    return None


# ==========================
# BOS
# ==========================

def detect_bos(

    df,

    swing_highs,

    swing_lows

):

    bullish = detect_bullish_bos(

        df,

        swing_highs

    )

    if bullish:

        return bullish

    bearish = detect_bearish_bos(

        df,

        swing_lows

    )

    if bearish:

        return bearish

    return None


# ==========================
# BOS CONFIRMATION
# ==========================

def bos_confirmed(df):

    swings = get_swings(df)

    bos = detect_bos(

        df,

        swings[0],

        swings[1]

    )

    return bos is not None
    # ==========================
# CHoCH
# ==========================

def detect_choch(

    df,

    swing_highs,

    swing_lows

):

    if len(swing_highs) < 2:

        return None

    if len(swing_lows) < 2:

        return None

    last_high = swing_highs[-1]

    previous_high = swing_highs[-2]

    last_low = swing_lows[-1]

    previous_low = swing_lows[-2]

    close = float(

        df["close"].iloc[-1]

    )

    # Bullish CHoCH

    if (

        last_high["price"]

        > previous_high["price"]

        and

        close > previous_high["price"]

    ):

        return {

            "direction": "BUY",

            "type": "Bullish CHoCH",

            "level": previous_high["price"]

        }

    # Bearish CHoCH

    if (

        last_low["price"]

        < previous_low["price"]

        and

        close < previous_low["price"]

    ):

        return {

            "direction": "SELL",

            "type": "Bearish CHoCH",

            "level": previous_low["price"]

        }

    return None


# ==========================
# MSS
# ==========================

def detect_mss(

    df,

    swing_highs,

    swing_lows

):

    choch = detect_choch(

        df,

        swing_highs,

        swing_lows

    )

    if choch is None:

        return None

    return {

        "direction": choch["direction"],

        "type": "Market Structure Shift",

        "level": choch["level"]

    }


# ==========================
# STRUCTURE SHIFT
# ==========================

def detect_structure_shift(df):

    highs, lows = get_swings(df)

    mss = detect_mss(

        df,

        highs,

        lows

    )

    if mss:

        return mss

    return detect_choch(

        df,

        highs,

        lows

    )
    # ==========================
# INTERNAL STRUCTURE
# ==========================

def detect_internal_structure(df):

    highs, lows = get_swings(df)

    highs = clean_swings(highs)

    lows = clean_swings(lows)

    return {

        "highs": highs[-5:] if len(highs) >= 5 else highs,

        "lows": lows[-5:] if len(lows) >= 5 else lows

    }


# ==========================
# EXTERNAL STRUCTURE
# ==========================

def detect_external_structure(df):

    highs, lows = get_swings(df)

    highs = clean_swings(highs)

    lows = clean_swings(lows)

    return {

        "major_high":

        highs[-1] if highs else None,

        "major_low":

        lows[-1] if lows else None

    }


# ==========================
# INTERNAL BOS
# ==========================

def detect_internal_bos(df):

    internal = detect_internal_structure(df)

    highs = internal["highs"]

    lows = internal["lows"]

    return detect_bos(

        df,

        highs,

        lows

    )


# ==========================
# EXTERNAL BOS
# ==========================

def detect_external_bos(df):

    external = detect_external_structure(df)

    high = external["major_high"]

    low = external["major_low"]

    if high is None or low is None:

        return None

    return detect_bos(

        df,

        [high],

        [low]

    )


# ==========================
# STRUCTURE LAYER
# ==========================

def structure_layer(df):

    return {

        "internal":

        detect_internal_bos(df),

        "external":

        detect_external_bos(df)

    }
    # ==========================
# EQUAL HIGHS
# ==========================

def detect_equal_highs(

    df,

    tolerance=0.001

):

    highs = clean_swings(

        detect_swing_highs(df)

    )

    equal_highs = []

    for i in range(

        len(highs) - 1

    ):

        p1 = highs[i]["price"]

        p2 = highs[i + 1]["price"]

        if abs(p1 - p2) / p1 <= tolerance:

            equal_highs.append({

                "price": round(

                    (p1 + p2) / 2,

                    2

                ),

                "first": highs[i]["index"],

                "second": highs[i + 1]["index"]

            })

    return equal_highs


# ==========================
# EQUAL LOWS
# ==========================

def detect_equal_lows(

    df,

    tolerance=0.001

):

    lows = clean_swings(

        detect_swing_lows(df)

    )

    equal_lows = []

    for i in range(

        len(lows) - 1

    ):

        p1 = lows[i]["price"]

        p2 = lows[i + 1]["price"]

        if abs(p1 - p2) / p1 <= tolerance:

            equal_lows.append({

                "price": round(

                    (p1 + p2) / 2,

                    2

                ),

                "first": lows[i]["index"],

                "second": lows[i + 1]["index"]

            })

    return equal_lows


# ==========================
# LIQUIDITY LEVELS
# ==========================

def liquidity_levels(df):

    return {

        "equal_highs":

        detect_equal_highs(df),

        "equal_lows":

        detect_equal_lows(df)

    }


# ==========================
# SWING CLUSTERS
# ==========================

def swing_clusters(df):

    highs = detect_equal_highs(df)

    lows = detect_equal_lows(df)

    return {

        "buy_side":

        highs,

        "sell_side":

        lows

    }
    # ==========================
# PREMIUM / DISCOUNT
# ==========================

def premium_discount_structure(df):

    external = detect_external_structure(df)

    high = external["major_high"]

    low = external["major_low"]

    if high is None or low is None:

        return None

    high_price = float(high["price"])
    low_price = float(low["price"])

    equilibrium = (

        high_price + low_price

    ) / 2

    price = float(

        df["close"].iloc[-1]

    )

    if price > equilibrium:

        zone = "PREMIUM"

    elif price < equilibrium:

        zone = "DISCOUNT"

    else:

        zone = "EQUILIBRIUM"

    return {

        "zone": zone,

        "price": price,

        "equilibrium": round(

            equilibrium,

            2

        ),

        "high": high_price,

        "low": low_price

    }


# ==========================
# INTERNAL / EXTERNAL TREND
# ==========================

def structure_trend(df):

    internal = detect_internal_bos(df)

    external = detect_external_bos(df)

    internal_trend = (

        internal["direction"]

        if internal

        else None

    )

    external_trend = (

        external["direction"]

        if external

        else None

    )

    return {

        "internal":

        internal_trend,

        "external":

        external_trend

    }


# ==========================
# STRUCTURE BIAS
# ==========================

def structure_bias(df):

    trend = structure_trend(df)

    pd = premium_discount_structure(df)

    if pd is None:

        return {

            "bias": "NEUTRAL"

        }

    if (

        trend["external"] == "BUY"

        and

        pd["zone"] == "DISCOUNT"

    ):

        return {

            "bias": "BUY"

        }

    if (

        trend["external"] == "SELL"

        and

        pd["zone"] == "PREMIUM"

    ):

        return {

            "bias": "SELL"

        }

    return {

        "bias": "NEUTRAL"

    }
    # ==========================
# STRUCTURE STRENGTH SCORE
# ==========================

def calculate_structure_score(df):

    score = 0

    reasons = []

    highs, lows = get_swings(df)

    bos = detect_bos(

        df,

        highs,

        lows

    )

    choch = detect_choch(

        df,

        highs,

        lows

    )

    mss = detect_mss(

        df,

        highs,

        lows

    )

    bias = structure_bias(df)

    pd_zone = premium_discount_structure(df)


    if bos:

        score += 35

        reasons.append(

            bos["type"]

        )


    if choch:

        score += 20

        reasons.append(

            choch["type"]

        )


    if mss:

        score += 20

        reasons.append(

            mss["type"]

        )


    if (

        bias["bias"]

        !=

        "NEUTRAL"

    ):

        score += 15

        reasons.append(

            "Structure Bias"

        )


    if pd_zone:

        if (

            pd_zone["zone"]

            ==

            "DISCOUNT"

        ):

            score += 5

            reasons.append(

                "Discount"

            )

        elif (

            pd_zone["zone"]

            ==

            "PREMIUM"

        ):

            score += 5

            reasons.append(

                "Premium"

            )


    if score > 100:

        score = 100


    return {

        "score": score,

        "reasons": reasons

    }


# ==========================
# STRUCTURE QUALITY
# ==========================

def structure_quality(df):

    result = calculate_structure_score(df)

    score = result["score"]


    if score >= 80:

        quality = "STRONG"

    elif score >= 60:

        quality = "GOOD"

    elif score >= 40:

        quality = "AVERAGE"

    else:

        quality = "WEAK"


    return {

        "quality": quality,

        "score": score,

        "reasons": result["reasons"]

    }
    # ==========================
# INSTITUTIONAL STRUCTURE
# ==========================

def analyze_structure_v5(df):

    highs = detect_swing_highs(df)

    lows = detect_swing_lows(df)

    bos = detect_bos(

        df,

        highs,

        lows

    )

    choch = detect_choch(

        df,

        highs,

        lows

    )

    mss = detect_mss(

        df,

        highs,

        lows

    )

    bias = structure_bias(df)

    quality = structure_quality(df)

    pd_zone = premium_discount_structure(df)

    liquidity = liquidity_levels(df)

    return {

        "bos": bos,

        "choch": choch,

        "mss": mss,

        "bias": bias,

        "quality": quality,

        "premium_discount": pd_zone,

        "liquidity": liquidity,

        "swing_highs": highs,

        "swing_lows": lows

    }


# ==========================
# DEBUG PANEL
# ==========================

def debug_structure(df):

    result = analyze_structure_v5(df)

    print("\n========== STRUCTURE V5 ==========")

    print("BOS        :", result["bos"])

    print("CHoCH      :", result["choch"])

    print("MSS        :", result["mss"])

    print("Bias       :", result["bias"])

    print("Quality    :", result["quality"]["quality"])

    print("Score      :", result["quality"]["score"])

    print("PD Zone    :", result["premium_discount"])

    print("EQ Highs   :", len(result["liquidity"]["equal_highs"]))

    print("EQ Lows    :", len(result["liquidity"]["equal_lows"]))

    print("Swing High :", len(result["swing_highs"]))

    print("Swing Low  :", len(result["swing_lows"]))

    print("=================================\n")

    return result
    # ==========================
# MAIN BOT COMPATIBILITY
# ==========================

def analyze_structure(df):

    result = analyze_structure_v5(df)

    return {

        "bos": result["bos"],

        "mss": result["mss"],

        "choch": result["choch"],

        "swing_highs": result["swing_highs"],

        "swing_lows": result["swing_lows"],

        "equal_levels": result["liquidity"],

        "bias": result["bias"],

        "quality": result["quality"],

        "premium_discount": result["premium_discount"]

    }


# ==========================
# BOT READY ENGINE
# ==========================

def structure_engine_v5(df):

    result = analyze_structure(df)

    return {

        "direction":

        result["bias"]["bias"],

        "bos":

        result["bos"] is not None,

        "mss":

        result["mss"] is not None,

        "choch":

        result["choch"] is not None,

        "score":

        result["quality"]["score"],

        "quality":

        result["quality"]["quality"]

    }


# ==========================
# EXPORT
# ==========================

__all__ = [

    "detect_swing_highs",

    "detect_swing_lows",

    "get_swings",

    "detect_bos",

    "detect_choch",

    "detect_mss",

    "detect_internal_structure",

    "detect_external_structure",

    "detect_equal_highs",

    "detect_equal_lows",

    "premium_discount_structure",

    "structure_bias",

    "structure_quality",

    "analyze_structure",

    "analyze_structure_v5",

    "structure_engine_v5",

    "debug_structure"

]
