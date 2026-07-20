import pandas as pd
import numpy as np


# ==========================
# DAILY BIAS ENGINE V5
# ==========================

LOOKBACK = 10

BIAS_STATE = {

    "bias": "NEUTRAL",

    "strength": 0,

    "last_update": None

}



# ==========================
# PREPARE DATA
# ==========================

def prepare_bias_data(df):

    df = df.copy()

    cols = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]

    for col in cols:

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
# CREATE BIAS OBJECT
# ==========================

def create_bias(

    bias,

    strength

):

    return {

        "bias": bias,

        "strength": strength

    }
    # ==========================
# BULLISH BIAS
# ==========================

def detect_bullish_bias(

    df

):

    if len(df) < LOOKBACK:

        return False


    last = df.iloc[-1]

    prev = df.iloc[-2]


    return (

        last["close"]

        >

        prev["high"]

    )



# ==========================
# BEARISH BIAS
# ==========================

def detect_bearish_bias(

    df

):

    if len(df) < LOOKBACK:

        return False


    last = df.iloc[-1]

    prev = df.iloc[-2]


    return (

        last["close"]

        <

        prev["low"]

    )



# ==========================
# PREVIOUS DAY RANGE
# ==========================

def previous_day_range(

    df

):

    if len(df) < 2:

        return None


    prev = df.iloc[-2]


    return {

        "high":

        prev["high"],

        "low":

        prev["low"]

    }
    # ==========================
# BIAS STRENGTH
# ==========================

def calculate_bias_strength(

    df

):

    if len(df) < LOOKBACK:

        return 0


    last = df.iloc[-1]


    body = abs(

        last["close"]

        -

        last["open"]

    )


    range_size = (

        last["high"]

        -

        last["low"]

    )


    if range_size == 0:

        return 0


    strength = (

        body / range_size

    ) * 100


    return round(

        strength,

        2

    )



# ==========================
# DAILY BIAS
# ==========================

def calculate_daily_bias(

    df

):

    bullish = detect_bullish_bias(

        df

    )

    bearish = detect_bearish_bias(

        df

    )

    strength = calculate_bias_strength(

        df

    )


    if bullish:

        return create_bias(

            "BULLISH",

            strength

        )


    if bearish:

        return create_bias(

            "BEARISH",

            strength

        )


    return create_bias(

        "NEUTRAL",

        strength

    )



# ==========================
# UPDATE STATE
# ==========================

def update_bias_state(

    bias

):

    BIAS_STATE["bias"] = bias["bias"]

    BIAS_STATE["strength"] = bias["strength"]


    return BIAS_STATE
    # ==========================
# BIAS VALIDATION
# ==========================

def validate_bias(

    bias

):

    if bias is None:

        return False


    if bias["bias"] not in [

        "BULLISH",

        "BEARISH",

        "NEUTRAL"

    ]:

        return False


    return True



# ==========================
# PREMIUM / DISCOUNT FILTER
# ==========================

def bias_zone(

    current_price,

    swing_high,

    swing_low

):

    if swing_high <= swing_low:

        return "UNKNOWN"


    midpoint = (

        swing_high

        +

        swing_low

    ) / 2


    if current_price > midpoint:

        return "PREMIUM"


    elif current_price < midpoint:

        return "DISCOUNT"


    return "EQUILIBRIUM"



# ==========================
# ACTIVE BIAS
# ==========================

def get_active_bias():

    return {

        "bias":

        BIAS_STATE["bias"],

        "strength":

        BIAS_STATE["strength"]

    }
    # ==========================
# BIAS SIGNAL
# ==========================

def bias_signal(

    df

):

    bias = calculate_daily_bias(

        df

    )


    update_bias_state(

        bias

    )


    return {

        "signal":

        bias["bias"],

        "strength":

        bias["strength"]

    }



# ==========================
# BIAS SCORE
# ==========================

def bias_score(

    df

):

    signal = bias_signal(

        df

    )


    strength = signal["strength"]


    if strength >= 80:

        return 15


    elif strength >= 60:

        return 10


    elif strength >= 40:

        return 5


    return 0



# ==========================
# FINAL BIAS ANALYSIS
# ==========================

def analyze_daily_bias(

    df

):

    signal = bias_signal(

        df

    )


    return {

        "bias":

        signal["signal"],

        "strength":

        signal["strength"],

        "score":

        bias_score(

            df

        )

    }
    # ==========================
# SCANNER INTEGRATION
# ==========================

def daily_bias_for_scanner(

    df

):

    result = analyze_daily_bias(

        df

    )


    return {

        "bias":

        result["bias"],

        "strength":

        result["strength"],

        "score":

        result["score"]

    }



# ==========================
# DIRECTION FILTER
# ==========================

def bias_direction_filter(

    bias,

    trade_direction

):

    if bias == "NEUTRAL":

        return False


    if bias == "BULLISH" and trade_direction == "BUY":

        return True


    if bias == "BEARISH" and trade_direction == "SELL":

        return True


    return False



# ==========================
# CONFIDENCE BONUS
# ==========================

def bias_confidence_bonus(

    df,

    trade_direction

):

    result = analyze_daily_bias(

        df

    )


    if bias_direction_filter(

        result["bias"],

        trade_direction

    ):

        return result["score"]


    return 0
    # ==========================
# DEBUG PANEL
# ==========================

def debug_daily_bias(

    df

):

    report = analyze_daily_bias(

        df

    )


    print("\n========== DAILY BIAS V5 ==========")

    print(

        "Bias :",

        report["bias"]

    )

    print(

        "Strength :",

        report["strength"]

    )

    print(

        "Score :",

        report["score"]

    )

    print(

        "===================================\n"

    )


    return report



# ==========================
# BIAS REPORT
# ==========================

def daily_bias_report(

    df

):

    report = analyze_daily_bias(

        df

    )


    return {

        "bias":

        report["bias"],

        "strength":

        report["strength"],

        "score":

        report["score"]

    }



# ==========================
# SUMMARY
# ==========================

def bias_summary(

    df

):

    report = daily_bias_report(

        df

    )


    return {

        "direction":

        report["bias"],

        "confidence_bonus":

        report["score"]

    }
    # ==========================
# SCANNER COMPATIBILITY
# ==========================

def scanner_daily_bias(

    df

):

    summary = bias_summary(

        df

    )


    return {

        "direction":

        summary["direction"],

        "bonus":

        summary["confidence_bonus"]

    }



# ==========================
# MAIN ENGINE
# ==========================

def daily_bias_engine(

    df

):

    report = daily_bias_report(

        df

    )


    return {

        "bias":

        report,

        "ready":

        report["bias"]

        !=

        "NEUTRAL"

    }



# ==========================
# TEST ENGINE
# ==========================

def test_daily_bias(

    df

):

    return daily_bias_engine(

        df

    )
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def daily_bias_engine_v5(

    df

):

    result = daily_bias_engine(

        df

    )


    return {

        "bias":

        result["bias"]["bias"],

        "strength":

        result["bias"]["strength"],

        "score":

        result["bias"]["score"],

        "ready":

        result["ready"]

    }



# ==========================
# FINAL BIAS CHECK
# ==========================

def final_daily_bias_check(

    df,

    trade_direction

):

    result = daily_bias_engine_v5(

        df

    )


    if not result["ready"]:

        return False


    return bias_direction_filter(

        result["bias"],

        trade_direction

    )



# ==========================
# RESET BIAS
# ==========================

def reset_daily_bias():

    BIAS_STATE["bias"] = "NEUTRAL"

    BIAS_STATE["strength"] = 0

    BIAS_STATE["last_update"] = None


    return True
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "prepare_bias_data",

    "detect_bullish_bias",

    "detect_bearish_bias",

    "previous_day_range",

    "calculate_bias_strength",

    "calculate_daily_bias",

    "update_bias_state",

    "get_active_bias",

    "validate_bias",

    "bias_zone",

    "bias_signal",

    "bias_score",

    "analyze_daily_bias",

    "daily_bias_for_scanner",

    "bias_direction_filter",

    "bias_confidence_bonus",

    "debug_daily_bias",

    "daily_bias_report",

    "bias_summary",

    "scanner_daily_bias",

    "daily_bias_engine",

    "daily_bias_engine_v5",

    "final_daily_bias_check",

    "reset_daily_bias"

]
