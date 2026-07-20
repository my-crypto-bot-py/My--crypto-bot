import pandas as pd
import numpy as np

# ==========================
# ICT PD ARRAY ENGINE V5
# ==========================

from smartmoney import (

    detect_order_block,

    detect_fvg,

    detect_pd_zone

)


# ==========================
# SETTINGS
# ==========================

PD_LOOKBACK = 100


# ==========================
# PREPARE DATA
# ==========================

def prepare_pd_arrays(df):

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
# PD ARRAY OBJECT
# ==========================

def create_pd_object(

    array_type,

    direction,

    high,

    low,

    index

):

    return {

        "type": array_type,

        "direction": direction,

        "high": round(

            float(high),

            2

        ),

        "low": round(

            float(low),

            2

        ),

        "index": index

    }
    # ==========================
# ORDER BLOCK PD ARRAY
# ==========================

def get_ob_pd_array(df):

    ob = detect_order_block(df)

    if ob is None:

        return None

    return create_pd_object(

        array_type="ORDER_BLOCK",

        direction=ob["direction"],

        high=ob["high"],

        low=ob["low"],

        index=ob["index"]

    )


# ==========================
# FVG PD ARRAY
# ==========================

def get_fvg_pd_array(df):

    fvg = detect_fvg(df)

    if fvg is None:

        return None

    return create_pd_object(

        array_type="FVG",

        direction=fvg["direction"],

        high=fvg["high"],

        low=fvg["low"],

        index=fvg["index"]

    )


# ==========================
# PD ARRAY COLLECTOR
# ==========================

def collect_pd_arrays(df):

    arrays = []

    ob = get_ob_pd_array(df)

    fvg = get_fvg_pd_array(df)


    if ob:

        arrays.append(ob)


    if fvg:

        arrays.append(fvg)


    return arrays


# ==========================
# ACTIVE PD ARRAY
# ==========================

def active_pd_array(df):

    arrays = collect_pd_arrays(df)

    if len(arrays) == 0:

        return None

    price = float(

        df["close"].iloc[-1]

    )

    for array in arrays:

        if (

            array["low"]

            <=

            price

            <=

            array["high"]

        ):

            return array

    return None
    # ==========================
# BREAKER BLOCK ENGINE
# ==========================

def detect_breaker_block(df):

    df = prepare_pd_arrays(df)

    if len(df) < 5:

        return None

    for i in range(

        len(df) - 2,

        max(

            1,

            len(df) - PD_LOOKBACK

        ),

        -1

    ):

        candle = df.iloc[i]

        next_candle = df.iloc[i + 1]


        # Bullish Breaker
        if (

            candle["low"]

            <

            df["low"].iloc[i-1]

            and

            next_candle["close"]

            >

            candle["high"]

        ):

            return create_pd_object(

                "BULLISH_BREAKER",

                "BUY",

                candle["high"],

                candle["low"],

                i

            )


        # Bearish Breaker
        if (

            candle["high"]

            >

            df["high"].iloc[i-1]

            and

            next_candle["close"]

            <

            candle["low"]

        ):

            return create_pd_object(

                "BEARISH_BREAKER",

                "SELL",

                candle["high"],

                candle["low"],

                i

            )


    return None


# ==========================
# BREAKER ACTIVE CHECK
# ==========================

def breaker_active(df):

    breaker = detect_breaker_block(df)

    if breaker is None:

        return False


    price = float(

        df["close"].iloc[-1]

    )


    return (

        breaker["low"]

        <=

        price

        <=

        breaker["high"]

    )


# ==========================
# FAILED ORDER BLOCK
# ==========================

def failed_order_block(df):

    ob = get_ob_pd_array(df)

    if ob is None:

        return None


    price = float(

        df["close"].iloc[-1]

    )


    if ob["direction"] == "BUY":

        if price < ob["low"]:

            return {

                "type": "Failed Bullish OB",

                "direction": "SELL",

                "level": ob["low"]

            }


    if ob["direction"] == "SELL":

        if price > ob["high"]:

            return {

                "type": "Failed Bearish OB",

                "direction": "BUY",

                "level": ob["high"]

            }


    return None
    # ==========================
# MITIGATION BLOCK ENGINE
# ==========================

def detect_mitigation_block(df):

    df = prepare_pd_arrays(df)

    if len(df) < 5:

        return None


    for i in range(

        len(df) - 2,

        max(

            1,

            len(df) - PD_LOOKBACK

        ),

        -1

    ):

        candle = df.iloc[i]

        next_candle = df.iloc[i + 1]


        # Bullish Mitigation

        if (

            candle["close"]

            <

            candle["open"]

            and

            next_candle["close"]

            >

            candle["high"]

        ):

            return create_pd_object(

                "BULLISH_MITIGATION",

                "BUY",

                candle["high"],

                candle["low"],

                i

            )


        # Bearish Mitigation

        if (

            candle["close"]

            >

            candle["open"]

            and

            next_candle["close"]

            <

            candle["low"]

        ):

            return create_pd_object(

                "BEARISH_MITIGATION",

                "SELL",

                candle["high"],

                candle["low"],

                i

            )


    return None



# ==========================
# REJECTION BLOCK ENGINE
# ==========================

def detect_rejection_block(df):

    df = prepare_pd_arrays(df)

    if len(df) < 3:

        return None


    candle = df.iloc[-1]


    body = abs(

        candle["close"]

        -

        candle["open"]

    )


    upper_wick = (

        candle["high"]

        -

        max(

            candle["open"],

            candle["close"]

        )

    )


    lower_wick = (

        min(

            candle["open"],

            candle["close"]

        )

        -

        candle["low"]

    )


    # Bearish rejection

    if upper_wick > body * 2:

        return create_pd_object(

            "BEARISH_REJECTION",

            "SELL",

            candle["high"],

            candle["low"],

            len(df)-1

        )


    # Bullish rejection

    if lower_wick > body * 2:

        return create_pd_object(

            "BULLISH_REJECTION",

            "BUY",

            candle["high"],

            candle["low"],

            len(df)-1

        )


    return None
    # ==========================
# BALANCED PRICE RANGE (BPR)
# ==========================

def detect_bpr(df):

    df = prepare_pd_arrays(df)

    if len(df) < 6:

        return None


    bullish_fvg = None

    bearish_fvg = None


    for i in range(

        len(df)-3,

        max(

            0,

            len(df)-PD_LOOKBACK

        ),

        -1

    ):

        c1 = df.iloc[i]

        c3 = df.iloc[i+2]


        # Bullish imbalance

        if (

            c1["high"]

            <

            c3["low"]

        ):

            bullish_fvg = {

                "high": c3["low"],

                "low": c1["high"]

            }


        # Bearish imbalance

        if (

            c1["low"]

            >

            c3["high"]

        ):

            bearish_fvg = {

                "high": c1["low"],

                "low": c3["high"]

            }


    if (

        bullish_fvg

        and

        bearish_fvg

    ):

        high = min(

            bullish_fvg["high"],

            bearish_fvg["high"]

        )

        low = max(

            bullish_fvg["low"],

            bearish_fvg["low"]

        )


        if high > low:

            return create_pd_object(

                "BALANCED_PRICE_RANGE",

                "NEUTRAL",

                high,

                low,

                len(df)-1

            )


    return None



# ==========================
# PD ARRAY OVERLAP
# ==========================

def pd_overlap(

    array1,

    array2

):

    if array1 is None or array2 is None:

        return False


    return not (

        array1["low"]

        >

        array2["high"]

        or

        array2["low"]

        >

        array1["high"]

    )



# ==========================
# COMBINED PD ARRAYS
# ==========================

def combined_pd_arrays(df):

    return {

        "order_block":

        get_ob_pd_array(df),

        "fvg":

        get_fvg_pd_array(df),

        "breaker":

        detect_breaker_block(df),

        "mitigation":

        detect_mitigation_block(df),

        "rejection":

        detect_rejection_block(df),

        "bpr":

        detect_bpr(df)

    }
    # ==========================
# PD ARRAY PRIORITY
# ==========================

def pd_array_priority(array):

    if array is None:

        return 0


    priority = {

        "ORDER_BLOCK": 5,

        "FVG": 4,

        "BULLISH_BREAKER": 4,

        "BEARISH_BREAKER": 4,

        "BULLISH_MITIGATION": 3,

        "BEARISH_MITIGATION": 3,

        "BALANCED_PRICE_RANGE": 3,

        "BULLISH_REJECTION": 2,

        "BEARISH_REJECTION": 2

    }


    return priority.get(

        array["type"],

        1

    )



# ==========================
# BEST PD ARRAY
# ==========================

def get_best_pd_array(df):

    arrays = combined_pd_arrays(df)

    best = None

    highest = 0


    for key, array in arrays.items():

        score = pd_array_priority(array)


        if score > highest:

            highest = score

            best = array


    return best



# ==========================
# PD ARRAY DIRECTION
# ==========================

def pd_array_direction(df):

    best = get_best_pd_array(df)


    if best is None:

        return None


    return best["direction"]



# ==========================
# PD ARRAY ACTIVE
# ==========================

def pd_array_active(df):

    best = get_best_pd_array(df)


    if best is None:

        return False


    price = float(

        df["close"].iloc[-1]

    )


    return (

        best["low"]

        <=

        price

        <=

        best["high"]

    )
    # ==========================
# PD ARRAY SCORE ENGINE
# ==========================

def calculate_pd_score(df):

    score = 0

    reasons = []


    arrays = combined_pd_arrays(df)


    # Order Block
    if arrays["order_block"]:

        score += 30

        reasons.append(

            "Order Block"

        )


    # FVG

    if arrays["fvg"]:

        score += 20

        reasons.append(

            "FVG"

        )


    # Breaker

    if arrays["breaker"]:

        score += 20

        reasons.append(

            "Breaker Block"

        )


    # Mitigation

    if arrays["mitigation"]:

        score += 15

        reasons.append(

            "Mitigation"

        )


    # BPR

    if arrays["bpr"]:

        score += 15

        reasons.append(

            "BPR"

        )


    if score > 100:

        score = 100


    return {

        "score": score,

        "reasons": reasons

    }



# ==========================
# PD ARRAY QUALITY
# ==========================

def pd_array_quality(df):

    result = calculate_pd_score(df)

    score = result["score"]


    if score >= 80:

        quality = "INSTITUTIONAL"


    elif score >= 60:

        quality = "STRONG"


    elif score >= 40:

        quality = "NORMAL"


    else:

        quality = "WEAK"


    return {

        "quality": quality,

        "score": score,

        "reasons": result["reasons"]

    }



# ==========================
# POI CONFIRMATION
# ==========================

def confirm_poi(df):

    quality = pd_array_quality(df)


    return quality["score"] >= 60
    # ==========================
# ENTRY ZONE
# ==========================

def get_entry_zone(df):

    poi = get_best_pd_array(df)

    if poi is None:

        return None


    return {

        "type": poi["type"],

        "direction": poi["direction"],

        "entry_high": poi["high"],

        "entry_low": poi["low"],

        "index": poi["index"]

    }



# ==========================
# PD ARRAY BIAS
# ==========================

def pd_array_bias(df):

    direction = pd_array_direction(df)


    if direction == "BUY":

        return {

            "bias": "BULLISH"

        }


    if direction == "SELL":

        return {

            "bias": "BEARISH"

        }


    return {

        "bias": "NEUTRAL"

    }



# ==========================
# FINAL PD ANALYSIS
# ==========================

def analyze_pd_arrays_v5(df):

    quality = pd_array_quality(df)

    return {

        "best_poi":

        get_best_pd_array(df),

        "entry_zone":

        get_entry_zone(df),

        "bias":

        pd_array_bias(df),

        "active":

        pd_array_active(df),

        "quality":

        quality

    }
    # ==========================
# PD ARRAY DEBUG PANEL
# ==========================

def debug_pd_arrays(df):

    result = analyze_pd_arrays_v5(df)


    print("\n========== PD ARRAY V5 ==========")

    print(

        "Best POI   :",

        result["best_poi"]

    )

    print(

        "Entry Zone :",

        result["entry_zone"]

    )

    print(

        "Bias       :",

        result["bias"]

    )

    print(

        "Active     :",

        result["active"]

    )

    print(

        "Quality    :",

        result["quality"]["quality"]

    )

    print(

        "Score      :",

        result["quality"]["score"]

    )

    print(

        "Reasons    :",

        ", ".join(

            result["quality"]["reasons"]

        )

    )

    print(

        "================================\n"

    )


    return result



# ==========================
# INSTITUTIONAL REPORT
# ==========================

def pd_array_report(df):

    result = analyze_pd_arrays_v5(df)


    return {

        "poi":

        result["best_poi"],

        "entry":

        result["entry_zone"],

        "bias":

        result["bias"]["bias"],

        "active":

        result["active"],

        "score":

        result["quality"]["score"],

        "quality":

        result["quality"]["quality"],

        "reasons":

        result["quality"]["reasons"]

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_pd_arrays(df):

    result = analyze_pd_arrays_v5(df)

    return {

        "poi":

        result["best_poi"],

        "entry_zone":

        result["entry_zone"],

        "bias":

        result["bias"],

        "active":

        result["active"],

        "quality":

        result["quality"]

    }



# ==========================
# BOT READY ENGINE
# ==========================

def pd_array_engine_v5(df):

    result = analyze_pd_arrays(df)

    return {

        "direction":

        result["bias"]["bias"],

        "poi":

        result["poi"],

        "entry":

        result["entry_zone"],

        "score":

        result["quality"]["score"],

        "quality":

        result["quality"]["quality"]

    }



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "get_ob_pd_array",

    "get_fvg_pd_array",

    "detect_breaker_block",

    "detect_mitigation_block",

    "detect_rejection_block",

    "detect_bpr",

    "combined_pd_arrays",

    "get_best_pd_array",

    "pd_array_active",

    "calculate_pd_score",

    "pd_array_quality",

    "analyze_pd_arrays",

    "analyze_pd_arrays_v5",

    "pd_array_engine_v5",

    "debug_pd_arrays",

    "pd_array_report"

]
