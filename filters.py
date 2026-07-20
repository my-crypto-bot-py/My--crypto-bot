import pandas as pd
import numpy as np


# ==========================
# FILTER ENGINE V5
# ==========================

MIN_CONFIDENCE = 80

FILTER_STATE = {

    "approved": False,

    "score": 0,

    "reason": ""

}



# ==========================
# FILTER RESULT
# ==========================

def create_filter_result(

    approved,

    score,

    reason

):

    return {

        "approved": approved,

        "score": score,

        "reason": reason

    }



# ==========================
# RESET FILTERS
# ==========================

def reset_filters():

    FILTER_STATE["approved"] = False

    FILTER_STATE["score"] = 0

    FILTER_STATE["reason"] = ""


    return True
    # ==========================
# CONFIDENCE FILTER
# ==========================

def confidence_filter(

    confidence

):

    return confidence >= MIN_CONFIDENCE



# ==========================
# SCORE VALIDATION
# ==========================

def validate_score(

    score

):

    if score < 0:

        return 0


    if score > 100:

        return 100


    return score



# ==========================
# MINIMUM SCORE CHECK
# ==========================

def minimum_score_check(

    score

):

    score = validate_score(

        score

    )


    if confidence_filter(

        score

    ):

        return create_filter_result(

            True,

            score,

            "Confidence Passed"

        )


    return create_filter_result(

        False,

        score,

        "Confidence Too Low"

    )
    # ==========================
# DAILY BIAS FILTER
# ==========================

def daily_bias_filter(

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
# CORRELATION FILTER
# ==========================

def correlation_filter(

    correlation_confirmed

):

    return correlation_confirmed is True



# ==========================
# DIRECTION MATCH FILTER
# ==========================

def direction_match_filter(

    bias,

    trade_direction,

    correlation_confirmed

):

    if not correlation_filter(

        correlation_confirmed

    ):

        return False


    return daily_bias_filter(

        bias,

        trade_direction

    )
    # ==========================
# ICT POI FILTER
# ==========================

def ict_poi_filter(

    poi_active

):

    return poi_active is True



# ==========================
# MARKET STRUCTURE FILTER
# ==========================

def structure_filter(

    structure

):

    valid = [

        "BULLISH",

        "BEARISH"

    ]


    return structure in valid



# ==========================
# OTE FILTER
# ==========================

def ote_filter(

    ote_valid

):

    return ote_valid is True



# ==========================
# CORE FILTER CHECK
# ==========================

def core_filter_check(

    poi_active,

    structure,

    ote_valid

):

    return (

        ict_poi_filter(

            poi_active

        )

        and

        structure_filter(

            structure

        )

        and

        ote_filter(

            ote_valid

        )

    )
    # ==========================
# SMT FILTER
# ==========================

def smt_filter(

    smt_valid

):

    return smt_valid is True



# ==========================
# SESSION FILTER
# ==========================

def session_filter(

    session_active

):

    return session_active is True



# ==========================
# VOLUME FILTER
# ==========================

def volume_filter(

    volume_confirmed

):

    return volume_confirmed is True



# ==========================
# ADVANCED FILTER CHECK
# ==========================

def advanced_filter_check(

    smt_valid,

    session_active,

    volume_confirmed

):

    return (

        smt_filter(

            smt_valid

        )

        and

        session_filter(

            session_active

        )

        and

        volume_filter(

            volume_confirmed

        )

    )
    # ==========================
# FILTER SCORE
# ==========================

def filter_score(

    confidence,

    core_ok,

    advanced_ok

):

    score = validate_score(

        confidence

    )


    if not core_ok:

        score -= 30


    if not advanced_ok:

        score -= 20


    return max(

        0,

        score

    )



# ==========================
# FINAL TRADE FILTER
# ==========================

def final_trade_filter(

    confidence,

    core_ok,

    advanced_ok

):

    score = filter_score(

        confidence,

        core_ok,

        advanced_ok

    )


    return minimum_score_check(

        score

    )



# ==========================
# TRADE APPROVAL
# ==========================

def approve_trade(

    confidence,

    core_ok,

    advanced_ok

):

    result = final_trade_filter(

        confidence,

        core_ok,

        advanced_ok

    )


    FILTER_STATE["approved"] = result["approved"]

    FILTER_STATE["score"] = result["score"]

    FILTER_STATE["reason"] = result["reason"]


    return FILTER_STATE
    # ==========================
# DEBUG PANEL
# ==========================

def debug_filters():

    print("\n========== FILTERS V5 ==========")

    print(

        "Approved :",

        FILTER_STATE["approved"]

    )

    print(

        "Score :",

        FILTER_STATE["score"]

    )

    print(

        "Reason :",

        FILTER_STATE["reason"]

    )

    print(

        "================================\n"

    )


    return FILTER_STATE



# ==========================
# FILTER REPORT
# ==========================

def filter_report():

    return {

        "approved":

        FILTER_STATE["approved"],

        "score":

        FILTER_STATE["score"],

        "reason":

        FILTER_STATE["reason"]

    }



# ==========================
# SCANNER INTEGRATION
# ==========================

def filters_for_scanner(

    confidence,

    core_ok,

    advanced_ok

):

    result = approve_trade(

        confidence,

        core_ok,

        advanced_ok

    )


    return {

        "approved":

        result["approved"],

        "score":

        result["score"],

        "reason":

        result["reason"]

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def filters_engine(

    confidence,

    core_ok,

    advanced_ok

):

    result = approve_trade(

        confidence,

        core_ok,

        advanced_ok

    )


    return {

        "filter":

        result,

        "ready":

        result["approved"]

    }



# ==========================
# FILTER ENGINE V5
# ==========================

def filters_engine_v5(

    confidence,

    core_ok,

    advanced_ok

):

    result = filters_engine(

        confidence,

        core_ok,

        advanced_ok

    )


    return {

        "approved":

        result["filter"]["approved"],

        "score":

        result["filter"]["score"],

        "reason":

        result["filter"]["reason"],

        "ready":

        result["ready"]

    }



# ==========================
# TEST ENGINE
# ==========================

def test_filters(

    confidence,

    core_ok,

    advanced_ok

):

    return filters_engine_v5(

        confidence,

        core_ok,

        advanced_ok

    )
    # ==========================
# ENGINE STATUS
# ==========================

def filters_status():

    return {

        "approved":

        FILTER_STATE["approved"],

        "score":

        FILTER_STATE["score"],

        "reason":

        FILTER_STATE["reason"]

    }



# ==========================
# MODULE REPORT
# ==========================

def filters_module_report(

    confidence,

    core_ok,

    advanced_ok

):

    result = filters_engine_v5(

        confidence,

        core_ok,

        advanced_ok

    )


    return {

        "status":

        filters_status(),

        "analysis":

        result

    }



# ==========================
# FINAL FILTER CHECK
# ==========================

def final_filter_check(

    confidence,

    core_ok,

    advanced_ok

):

    result = filters_engine_v5(

        confidence,

        core_ok,

        advanced_ok

    )


    return result["ready"]
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "create_filter_result",

    "reset_filters",

    "confidence_filter",

    "validate_score",

    "minimum_score_check",

    "daily_bias_filter",

    "correlation_filter",

    "direction_match_filter",

    "ict_poi_filter",

    "structure_filter",

    "ote_filter",

    "core_filter_check",

    "smt_filter",

    "session_filter",

    "volume_filter",

    "advanced_filter_check",

    "filter_score",

    "final_trade_filter",

    "approve_trade",

    "debug_filters",

    "filter_report",

    "filters_for_scanner",

    "filters_engine",

    "filters_engine_v5",

    "test_filters",

    "filters_status",

    "filters_module_report",

    "final_filter_check"

]
