import pandas as pd
import numpy as np


# ==========================
# TREND ENGINE V5
# ==========================

TREND_STATE = {

    "trend": "NEUTRAL",

    "strength": 0,

    "direction": None

}



# ==========================
# TREND RESET
# ==========================

def reset_trend():

    TREND_STATE["trend"] = "NEUTRAL"

    TREND_STATE["strength"] = 0

    TREND_STATE["direction"] = None


    return True



# ==========================
# PREPARE DATA
# ==========================

def prepare_trend_data(

    df

):

    df = df.copy()


    for col in [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )


    df.dropna(

        inplace=True

    )


    return df
    # ==========================
# EMA CALCULATION
# ==========================

def calculate_ema(

    df,

    period=50

):

    return (

        df["close"]

        .ewm(

            span=period,

            adjust=False

        )

        .mean()

    )



# ==========================
# BASIC TREND DETECTION
# ==========================

def detect_trend(

    df

):

    ema50 = calculate_ema(

        df,

        50

    )


    ema200 = calculate_ema(

        df,

        200

    )


    last_price = df["close"].iloc[-1]


    if (

        last_price > ema50.iloc[-1]

        and

        ema50.iloc[-1] > ema200.iloc[-1]

    ):

        return "BULLISH"



    if (

        last_price < ema50.iloc[-1]

        and

        ema50.iloc[-1] < ema200.iloc[-1]

    ):

        return "BEARISH"



    return "NEUTRAL"



# ==========================
# UPDATE TREND STATE
# ==========================

def update_trend_state(

    df

):

    trend = detect_trend(

        df

    )


    TREND_STATE["trend"] = trend

    TREND_STATE["direction"] = trend


    return TREND_STATE
    # ==========================
# TREND STRENGTH
# ==========================

def trend_strength(

    df

):

    ema50 = calculate_ema(

        df,

        50

    )


    ema200 = calculate_ema(

        df,

        200

    )


    diff = abs(

        ema50.iloc[-1]

        -

        ema200.iloc[-1]

    )


    price = df["close"].iloc[-1]


    if price == 0:

        return 0


    strength = (

        diff / price

    ) * 100


    return round(

        strength,

        2

    )



# ==========================
# MOMENTUM CHECK
# ==========================

def momentum_check(

    df,

    period=10

):

    change = (

        df["close"].iloc[-1]

        -

        df["close"].iloc[-period]

    )


    if change > 0:

        return "BULLISH"


    if change < 0:

        return "BEARISH"


    return "NEUTRAL"



# ==========================
# TREND SCORE
# ==========================

def trend_score(

    df

):

    score = 0


    trend = detect_trend(

        df

    )


    momentum = momentum_check(

        df

    )


    if trend == momentum:

        score += 20


    strength = trend_strength(

        df

    )


    if strength > 1:

        score += 10


    return score
    # ==========================
# MULTI TIMEFRAME TREND
# ==========================

def multi_timeframe_trend(

    htf_df,

    ltf_df

):

    htf_trend = detect_trend(

        htf_df

    )


    ltf_trend = detect_trend(

        ltf_df

    )


    if htf_trend == ltf_trend:

        return htf_trend


    return "CONFLICT"



# ==========================
# HTF CONFIRMATION
# ==========================

def htf_confirmation(

    htf_df,

    direction

):

    trend = detect_trend(

        htf_df

    )


    return trend == direction



# ==========================
# TREND FILTER
# ==========================

def trend_filter(

    df,

    direction

):

    trend = detect_trend(

        df

    )


    return trend == direction
    # ==========================
# TREND REPORT
# ==========================

def trend_report():

    return {

        "trend":

        TREND_STATE["trend"],

        "strength":

        TREND_STATE["strength"],

        "direction":

        TREND_STATE["direction"]

    }



# ==========================
# DEBUG TREND
# ==========================

def debug_trend():

    report = trend_report()


    print("\n========== TREND V5 ==========")

    print("Trend :", report["trend"])

    print("Strength :", report["strength"])

    print("Direction :", report["direction"])

    print("================================\n")


    return report



# ==========================
# SCANNER INTEGRATION
# ==========================

def trend_for_scanner(

    df

):

    state = update_trend_state(

        df

    )


    state["strength"] = trend_strength(

        df

    )


    return {

        "trend":

        state["trend"],

        "strength":

        state["strength"]

    }
    # ==========================
# TREND ENGINE
# ==========================

def trend_engine(

    df

):

    state = update_trend_state(

        df

    )


    state["strength"] = trend_strength(

        df

    )


    return {

        "trend":

        state["trend"],

        "strength":

        state["strength"],

        "direction":

        state["direction"]

    }



# ==========================
# TREND ENGINE V5
# ==========================

def trend_engine_v5(

    df

):

    result = trend_engine(

        df

    )


    return {

        "trend":

        result["trend"],

        "strength":

        result["strength"],

        "confirmed":

        result["trend"] != "NEUTRAL"

    }



# ==========================
# TEST ENGINE
# ==========================

def test_trend(

    df

):

    return trend_engine_v5(

        df

    )
    # ==========================
# TREND STATUS
# ==========================

def trend_status():

    return {

        "trend":

        TREND_STATE["trend"],

        "strength":

        TREND_STATE["strength"],

        "direction":

        TREND_STATE["direction"]

    }



# ==========================
# MODULE REPORT
# ==========================

def trend_module_report():

    return {

        "status":

        trend_status(),

        "report":

        trend_report()

    }



# ==========================
# FINAL TREND CHECK
# ==========================

def final_trend_check(

    direction

):

    return (

        TREND_STATE["trend"]

        ==

        direction

    )
    # ==========================
# ADVANCED TREND CONFIRMATION
# ==========================

def advanced_trend_confirmation(

    df,

    direction

):

    trend = detect_trend(

        df

    )


    strength = trend_strength(

        df

    )


    if trend != direction:

        return False


    if strength < 0.5:

        return False


    return True



# ==========================
# TREND CONFIDENCE
# ==========================

def trend_confidence(

    df

):

    score = trend_score(

        df

    )


    strength = trend_strength(

        df

    )


    if strength > 1:

        score += 10


    return min(

        score,

        100

    )



# ==========================
# MARKET DIRECTION FILTER
# ==========================

def market_direction_filter(

    df,

    direction

):

    confidence = trend_confidence(

        df

    )


    if confidence >= 20:

        return advanced_trend_confirmation(

            df,

            direction

        )


    return False
    # ==========================
# RESET FINAL TREND
# ==========================

def reset_trend_final():

    TREND_STATE["trend"] = "NEUTRAL"

    TREND_STATE["strength"] = 0

    TREND_STATE["direction"] = None


    return True



# ==========================
# FINAL DEBUG
# ==========================

def final_trend_debug():

    report = trend_report()


    print("\n========== FINAL TREND V5 ==========")

    print("Trend :", report["trend"])

    print("Strength :", report["strength"])

    print("Direction :", report["direction"])

    print("====================================\n")


    return report



# ==========================
# TREND SUMMARY
# ==========================

def trend_summary():

    report = trend_report()


    return {

        "trend":

        report["trend"],

        "strength":

        report["strength"],

        "direction":

        report["direction"]

    }
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "reset_trend",

    "prepare_trend_data",

    "calculate_ema",

    "detect_trend",

    "update_trend_state",

    "trend_strength",

    "momentum_check",

    "trend_score",

    "multi_timeframe_trend",

    "htf_confirmation",

    "trend_filter",

    "trend_report",

    "debug_trend",

    "trend_for_scanner",

    "trend_engine",

    "trend_engine_v5",

    "test_trend",

    "trend_status",

    "trend_module_report",

    "final_trend_check",

    "advanced_trend_confirmation",

    "trend_confidence",

    "market_direction_filter",

    "reset_trend_final",

    "final_trend_debug",

    "trend_summary"

]
