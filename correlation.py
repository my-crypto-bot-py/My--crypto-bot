import pandas as pd
import numpy as np


# ==========================
# CORRELATION ENGINE V5
# ==========================

LOOKBACK = 50

CORRELATION_STATE = {

    "value": 0,

    "strength": "UNKNOWN",

    "direction": "NEUTRAL"

}



# ==========================
# PREPARE DATA
# ==========================

def prepare_correlation_data(

    df

):

    df = df.copy()

    cols = [

        "close"

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
# PRICE SERIES
# ==========================

def get_price_series(

    df

):

    return df["close"]
    # ==========================
# PEARSON CORRELATION
# ==========================

def calculate_correlation(

    df1,

    df2

):

    df1 = prepare_correlation_data(

        df1

    )

    df2 = prepare_correlation_data(

        df2

    )


    s1 = get_price_series(

        df1

    )

    s2 = get_price_series(

        df2

    )


    length = min(

        len(s1),

        len(s2),

        LOOKBACK

    )


    if length < 10:

        return 0


    corr = s1.tail(

        length

    ).corr(

        s2.tail(

            length

        )

    )


    if pd.isna(corr):

        return 0


    return round(

        float(corr),

        3

    )



# ==========================
# CORRELATION STRENGTH
# ==========================

def correlation_strength(

    value

):

    if value >= 0.80:

        return "VERY_STRONG"


    elif value >= 0.60:

        return "STRONG"


    elif value >= 0.40:

        return "MEDIUM"


    elif value >= 0.20:

        return "WEAK"


    return "NONE"



# ==========================
# CORRELATION DIRECTION
# ==========================

def correlation_direction(

    value

):

    if value > 0:

        return "POSITIVE"


    elif value < 0:

        return "NEGATIVE"


    return "NEUTRAL"
    # ==========================
# UPDATE CORRELATION STATE
# ==========================

def update_correlation_state(

    value

):

    CORRELATION_STATE["value"] = value

    CORRELATION_STATE["strength"] = (

        correlation_strength(

            value

        )

    )

    CORRELATION_STATE["direction"] = (

        correlation_direction(

            value

        )

    )

    return CORRELATION_STATE



# ==========================
# BTC CONFIRMATION
# ==========================

def btc_confirmation(

    btc_df,

    asset_df

):

    value = calculate_correlation(

        btc_df,

        asset_df

    )

    state = update_correlation_state(

        value

    )

    return {

        "confirmed":

        value >= 0.60,

        "correlation":

        value,

        "strength":

        state["strength"],

        "direction":

        state["direction"]

    }



# ==========================
# FINAL CORRELATION ANALYSIS
# ==========================

def analyze_correlation(

    btc_df,

    asset_df

):

    return btc_confirmation(

        btc_df,

        asset_df

    )
    # ==========================
# CORRELATION SCORE
# ==========================

def correlation_score(

    btc_df,

    asset_df

):

    result = analyze_correlation(

        btc_df,

        asset_df

    )


    value = abs(

        result["correlation"]

    )


    if value >= 0.80:

        return 15


    elif value >= 0.60:

        return 10


    elif value >= 0.40:

        return 5


    return 0



# ==========================
# SCANNER INTEGRATION
# ==========================

def correlation_for_scanner(

    btc_df,

    asset_df

):

    result = analyze_correlation(

        btc_df,

        asset_df

    )


    return {

        "confirmed":

        result["confirmed"],

        "direction":

        result["direction"],

        "strength":

        result["strength"],

        "score":

        correlation_score(

            btc_df,

            asset_df

        )

    }



# ==========================
# CONFIDENCE BONUS
# ==========================

def correlation_confidence_bonus(

    btc_df,

    asset_df

):

    result = correlation_for_scanner(

        btc_df,

        asset_df

    )


    if result["confirmed"]:

        return result["score"]


    return 0
    # ==========================
# BTC LEAD CONFIRMATION
# ==========================

def btc_leads_market(

    btc_df

):

    if len(

        btc_df

    ) < 2:

        return False


    last = btc_df.iloc[-1]

    prev = btc_df.iloc[-2]


    return (

        abs(

            last["close"]

            -

            prev["close"]

        )

        >

        0

    )



# ==========================
# FOLLOW CONFIRMATION
# ==========================

def asset_follow_confirmation(

    btc_df,

    asset_df

):

    corr = analyze_correlation(

        btc_df,

        asset_df

    )


    if (

        btc_leads_market(

            btc_df

        )

        and

        corr["confirmed"]

    ):

        return True


    return False



# ==========================
# CORRELATION FILTER
# ==========================

def correlation_filter(

    btc_df,

    asset_df

):

    return {

        "allowed":

        asset_follow_confirmation(

            btc_df,

            asset_df

        ),

        "score":

        correlation_score(

            btc_df,

            asset_df

        )

    }
    # ==========================
# DEBUG PANEL
# ==========================

def debug_correlation(

    btc_df,

    asset_df

):

    report = analyze_correlation(

        btc_df,

        asset_df

    )


    print("\n========== CORRELATION V5 ==========")

    print(

        "Confirmed :",

        report["confirmed"]

    )

    print(

        "Correlation :",

        report["correlation"]

    )

    print(

        "Strength :",

        report["strength"]

    )

    print(

        "Direction :",

        report["direction"]

    )

    print(

        "====================================\n"

    )


    return report



# ==========================
# CORRELATION REPORT
# ==========================

def correlation_report(

    btc_df,

    asset_df

):

    result = analyze_correlation(

        btc_df,

        asset_df

    )


    return {

        "confirmed":

        result["confirmed"],

        "correlation":

        result["correlation"],

        "strength":

        result["strength"],

        "direction":

        result["direction"],

        "score":

        correlation_score(

            btc_df,

            asset_df

        )

    }



# ==========================
# SUMMARY
# ==========================

def correlation_summary(

    btc_df,

    asset_df

):

    report = correlation_report(

        btc_df,

        asset_df

    )


    return {

        "confirmed":

        report["confirmed"],

        "score":

        report["score"],

        "direction":

        report["direction"]

    }
    # ==========================
# SCANNER COMPATIBILITY
# ==========================

def scanner_correlation(

    btc_df,

    asset_df

):

    summary = correlation_summary(

        btc_df,

        asset_df

    )


    return {

        "confirmed":

        summary["confirmed"],

        "direction":

        summary["direction"],

        "score":

        summary["score"]

    }



# ==========================
# MAIN ENGINE
# ==========================

def correlation_engine(

    btc_df,

    asset_df

):

    report = correlation_report(

        btc_df,

        asset_df

    )


    return {

        "correlation":

        report,

        "ready":

        report["confirmed"]

    }



# ==========================
# TEST ENGINE
# ==========================

def test_correlation(

    btc_df,

    asset_df

):

    return correlation_engine(

        btc_df,

        asset_df

    )
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def correlation_engine_v5(

    btc_df,

    asset_df

):

    result = correlation_engine(

        btc_df,

        asset_df

    )


    return {

        "confirmed":

        result["correlation"]["confirmed"],

        "correlation":

        result["correlation"]["correlation"],

        "strength":

        result["correlation"]["strength"],

        "direction":

        result["correlation"]["direction"],

        "score":

        result["correlation"]["score"],

        "ready":

        result["ready"]

    }



# ==========================
# FINAL CHECK
# ==========================

def final_correlation_check(

    btc_df,

    asset_df

):

    result = correlation_engine_v5(

        btc_df,

        asset_df

    )


    return result["ready"]
    # ==========================
# RESET STATE
# ==========================

def reset_correlation():

    CORRELATION_STATE["value"] = 0

    CORRELATION_STATE["strength"] = "UNKNOWN"

    CORRELATION_STATE["direction"] = "NEUTRAL"


    return True



# ==========================
# ENGINE STATUS
# ==========================

def correlation_status():

    return {

        "value":

        CORRELATION_STATE["value"],

        "strength":

        CORRELATION_STATE["strength"],

        "direction":

        CORRELATION_STATE["direction"]

    }



# ==========================
# MODULE REPORT
# ==========================

def correlation_module_report(

    btc_df,

    asset_df

):

    result = correlation_engine_v5(

        btc_df,

        asset_df

    )


    return {

        "status":

        correlation_status(),

        "analysis":

        result

    }
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "prepare_correlation_data",

    "get_price_series",

    "calculate_correlation",

    "correlation_strength",

    "correlation_direction",

    "update_correlation_state",

    "btc_confirmation",

    "analyze_correlation",

    "correlation_score",

    "correlation_for_scanner",

    "correlation_confidence_bonus",

    "btc_leads_market",

    "asset_follow_confirmation",

    "correlation_filter",

    "debug_correlation",

    "correlation_report",

    "correlation_summary",

    "scanner_correlation",

    "correlation_engine",

    "test_correlation",

    "correlation_engine_v5",

    "final_correlation_check",

    "reset_correlation",

    "correlation_status",

    "correlation_module_report"

]
