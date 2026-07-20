import pandas as pd
import numpy as np

# ==========================
# ICT OTE ENGINE V5
# ==========================


# ==========================
# SETTINGS
# ==========================

OTE_LOW = 0.62

OTE_HIGH = 0.79

OTE_LOOKBACK = 100



# ==========================
# PREPARE DATA
# ==========================

def prepare_ote(df):

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
# FIBONACCI LEVEL
# ==========================

def fib_level(

    high,

    low,

    ratio

):

    return (

        high

        -

        (

            (high - low)

            *

            ratio

        )

    )



# ==========================
# OTE OBJECT
# ==========================

def create_ote_object(

    direction,

    high,

    low,

    index

):

    return {

        "direction": direction,

        "type": "OTE Zone",

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
# SWING HIGH
# ==========================

def get_swing_high(df):

    df = prepare_ote(df)

    high_index = (

        df["high"]

        .tail(OTE_LOOKBACK)

        .idxmax()

    )

    return {

        "price":

        float(

            df["high"].iloc[high_index]

        ),

        "index":

        int(high_index)

    }



# ==========================
# SWING LOW
# ==========================

def get_swing_low(df):

    df = prepare_ote(df)

    low_index = (

        df["low"]

        .tail(OTE_LOOKBACK)

        .idxmin()

    )

    return {

        "price":

        float(

            df["low"].iloc[low_index]

        ),

        "index":

        int(low_index)

    }



# ==========================
# RANGE DETECTION
# ==========================

def detect_ote_range(df):

    high = get_swing_high(df)

    low = get_swing_low(df)


    if high["index"] > low["index"]:

        direction = "SELL"

    else:

        direction = "BUY"


    return {

        "high": high,

        "low": low,

        "direction": direction

    }



# ==========================
# RANGE VALIDATION
# ==========================

def valid_ote_range(df):

    result = detect_ote_range(df)


    if (

        result["high"]["price"]

        <=

        result["low"]["price"]

    ):

        return False


    return True
    # ==========================
# BULLISH OTE ZONE
# ==========================

def detect_bullish_ote(df):

    df = prepare_ote(df)

    swing = detect_ote_range(df)

    high = swing["high"]["price"]

    low = swing["low"]["price"]


    if swing["direction"] != "BUY":

        return None


    ote_high = fib_level(

        high,

        low,

        OTE_LOW

    )


    ote_low = fib_level(

        high,

        low,

        OTE_HIGH

    )


    return create_ote_object(

        "BUY",

        ote_high,

        ote_low,

        len(df)-1

    )



# ==========================
# BULLISH OTE ACTIVE
# ==========================

def bullish_ote_active(df):

    ote = detect_bullish_ote(df)


    if ote is None:

        return False


    price = float(

        df["close"].iloc[-1]

    )


    return (

        ote["low"]

        <=

        price

        <=

        ote["high"]

    )
    # ==========================
# BEARISH OTE ZONE
# ==========================

def detect_bearish_ote(df):

    df = prepare_ote(df)

    swing = detect_ote_range(df)

    high = swing["high"]["price"]

    low = swing["low"]["price"]


    if swing["direction"] != "SELL":

        return None


    # Bearish retracement
    ote_low = (

        low

        +

        (

            (high - low)

            *

            OTE_LOW

        )

    )


    ote_high = (

        low

        +

        (

            (high - low)

            *

            OTE_HIGH

        )

    )


    return create_ote_object(

        "SELL",

        ote_high,

        ote_low,

        len(df)-1

    )



# ==========================
# BEARISH OTE ACTIVE
# ==========================

def bearish_ote_active(df):

    ote = detect_bearish_ote(df)


    if ote is None:

        return False


    price = float(

        df["close"].iloc[-1]

    )


    return (

        ote["low"]

        <=

        price

        <=

        ote["high"]

    )



# ==========================
# FINAL OTE ZONE
# ==========================

def get_ote_zone(df):

    bullish = detect_bullish_ote(df)

    if bullish:

        return bullish


    bearish = detect_bearish_ote(df)

    if bearish:

        return bearish


    return None
    # ==========================
# OTE VALIDATION
# ==========================

def validate_ote(df):

    zone = get_ote_zone(df)


    if zone is None:

        return {

            "valid": False,

            "reason": "No OTE Zone"

        }


    price = float(

        df["close"].iloc[-1]

    )


    if (

        zone["low"]

        <=

        price

        <=

        zone["high"]

    ):

        return {

            "valid": True,

            "direction":

            zone["direction"],

            "zone":

            zone

        }


    return {

        "valid": False,

        "direction":

        zone["direction"],

        "zone":

        zone,

        "reason":

        "Price outside OTE"

    }



# ==========================
# OTE DIRECTION
# ==========================

def ote_direction(df):

    result = validate_ote(df)


    if result["valid"]:

        return result["direction"]


    return None



# ==========================
# OTE QUALITY
# ==========================

def ote_quality(df):

    result = validate_ote(df)


    if not result["valid"]:

        return {

            "quality": "WEAK",

            "score": 0

        }


    return {

        "quality": "ACTIVE",

        "score": 50,

        "direction":

        result["direction"]

    }
    # ==========================
# OTE + PD ARRAY CONFLUENCE
# ==========================

def ote_pd_confluence(df):

    try:

        from pd_arrays import (

            get_best_pd_array

        )

    except:

        return {

            "score": 0,

            "reasons": []

        }


    ote = get_ote_zone(df)

    pd_array = get_best_pd_array(df)


    score = 0

    reasons = []


    if ote is None:

        return {

            "score": 0,

            "reasons":

            ["No OTE"]

        }


    if pd_array is not None:

        score += 30

        reasons.append(

            "PD Array"

        )


        if (

            ote["direction"]

            ==

            pd_array["direction"]

        ):

            score += 30

            reasons.append(

                "Direction Match"

            )


    return {

        "score": score,

        "reasons": reasons

    }



# ==========================
# OTE + ORDER BLOCK
# ==========================

def ote_order_block_match(df):

    try:

        from pd_arrays import (

            get_ob_pd_array

        )

    except:

        return False


    ote = get_ote_zone(df)

    ob = get_ob_pd_array(df)


    if ote is None or ob is None:

        return False


    return (

        ote["direction"]

        ==

        ob["direction"]

    )



# ==========================
# OTE CONFLUENCE SCORE
# ==========================

def ote_confluence_score(df):

    result = ote_pd_confluence(df)

    score = result["score"]


    if ote_order_block_match(df):

        score += 20

        result["reasons"].append(

            "OB Match"

        )


    if score > 100:

        score = 100


    return {

        "score": score,

        "reasons": result["reasons"]

    }
    # ==========================
# OTE ENTRY MODEL
# ==========================

def generate_ote_entry(df):

    zone = get_ote_zone(df)


    if zone is None:

        return None


    entry = (

        zone["low"]

        +

        (

            zone["high"]

            -

            zone["low"]

        )

        / 2

    )


    return {

        "direction":

        zone["direction"],

        "entry":

        round(entry, 2),

        "zone_high":

        zone["high"],

        "zone_low":

        zone["low"]

    }



# ==========================
# STOP LOSS
# ==========================

def generate_ote_sl(df):

    entry = generate_ote_entry(df)


    if entry is None:

        return None


    zone = get_ote_zone(df)


    if entry["direction"] == "BUY":

        sl = (

            zone["low"]

            -

            (

                abs(

                    zone["high"]

                    -

                    zone["low"]

                )

                *

                0.2

            )

        )


    else:

        sl = (

            zone["high"]

            +

            (

                abs(

                    zone["high"]

                    -

                    zone["low"]

                )

                *

                0.2

            )

        )


    return round(sl, 2)



# ==========================
# TAKE PROFIT
# ==========================

def generate_ote_tp(df):

    entry = generate_ote_entry(df)

    sl = generate_ote_sl(df)


    if entry is None or sl is None:

        return None


    risk = abs(

        entry["entry"]

        -

        sl

    )


    if entry["direction"] == "BUY":

        tp = (

            entry["entry"]

            +

            (

                risk * 3

            )

        )

    else:

        tp = (

            entry["entry"]

            -

            (

                risk * 3

            )

        )


    return round(tp, 2)
    # ==========================
# FINAL OTE ANALYZER
# ==========================

def analyze_ote_v5(df):

    zone = get_ote_zone(df)

    validation = validate_ote(df)

    confluence = ote_confluence_score(df)

    entry = generate_ote_entry(df)

    sl = generate_ote_sl(df)

    tp = generate_ote_tp(df)


    return {

        "zone": zone,

        "valid":

        validation["valid"],

        "direction":

        validation.get(

            "direction",

            None

        ),

        "confluence":

        confluence,

        "entry":

        entry,

        "sl":

        sl,

        "tp":

        tp

    }



# ==========================
# OTE TRADE SIGNAL
# ==========================

def ote_trade_signal(df):

    result = analyze_ote_v5(df)


    if not result["valid"]:

        return {

            "signal":

            "NO TRADE",

            "reason":

            "OTE not active"

        }


    if result["confluence"]["score"] < 50:

        return {

            "signal":

            "NO TRADE",

            "reason":

            "Low OTE Confluence"

        }


    return {

        "signal":

        result["direction"],

        "entry":

        result["entry"],

        "sl":

        result["sl"],

        "tp":

        result["tp"],

        "score":

        result["confluence"]["score"]

    }
    # ==========================
# OTE DEBUG PANEL
# ==========================

def debug_ote(df):

    result = analyze_ote_v5(df)


    print("\n========== OTE V5 ==========")

    print(

        "Zone        :",

        result["zone"]

    )

    print(

        "Valid       :",

        result["valid"]

    )

    print(

        "Direction   :",

        result["direction"]

    )

    print(

        "Confluence  :",

        result["confluence"]

    )

    print(

        "Entry       :",

        result["entry"]

    )

    print(

        "SL          :",

        result["sl"]

    )

    print(

        "TP          :",

        result["tp"]

    )

    print(

        "============================\n"

    )


    return result



# ==========================
# OTE REPORT
# ==========================

def ote_report(df):

    result = analyze_ote_v5(df)


    return {

        "direction":

        result["direction"],

        "valid":

        result["valid"],

        "entry":

        result["entry"],

        "sl":

        result["sl"],

        "tp":

        result["tp"],

        "score":

        result["confluence"]["score"],

        "reasons":

        result["confluence"]["reasons"]

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_ote(df):

    result = analyze_ote_v5(df)

    return {

        "zone":

        result["zone"],

        "direction":

        result["direction"],

        "valid":

        result["valid"],

        "entry":

        result["entry"],

        "sl":

        result["sl"],

        "tp":

        result["tp"],

        "confluence":

        result["confluence"]

    }



# ==========================
# OTE ENGINE V5
# ==========================

def ote_engine_v5(df):

    result = analyze_ote(df)

    return {

        "signal":

        (

            result["direction"]

            if result["valid"]

            else "NO TRADE"

        ),

        "entry":

        result["entry"],

        "sl":

        result["sl"],

        "tp":

        result["tp"],

        "score":

        result["confluence"]["score"]

    }



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "detect_bullish_ote",

    "detect_bearish_ote",

    "get_ote_zone",

    "validate_ote",

    "ote_direction",

    "ote_quality",

    "ote_confluence_score",

    "generate_ote_entry",

    "generate_ote_sl",

    "generate_ote_tp",

    "analyze_ote",

    "analyze_ote_v5",

    "ote_engine_v5",

    "ote_trade_signal",

    "debug_ote",

    "ote_report"

]
