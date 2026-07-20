import pandas as pd
import numpy as np


# ==========================
# ICT CONFIDENCE ENGINE V5
# ==========================


# ==========================
# SETTINGS
# ==========================

MAX_SCORE = 100

MIN_TRADE_SCORE = 85



# ==========================
# SCORE WEIGHTS
# ==========================

WEIGHTS = {

    "market": 20,

    "structure": 20,

    "smart_money": 20,

    "pd_array": 15,

    "ote": 15,

    "smt": 10

}



# ==========================
# PREPARE DATA
# ==========================

def prepare_confidence(df):

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


    df.dropna(

        inplace=True

    )


    df.reset_index(

        drop=True,

        inplace=True

    )


    return df



# ==========================
# SCORE OBJECT
# ==========================

def create_score(

    name,

    score,

    reason

):

    return {

        "name": name,

        "score": score,

        "reason": reason

    }
    # ==========================
# MARKET SCORE ENGINE
# ==========================

def calculate_market_score(

    market_data=None

):

    score = 0

    reasons = []


    if market_data is None:

        return create_score(

            "market",

            0,

            "No market data"

        )


    # Trend confirmation

    trend = market_data.get(

        "trend"

    )


    if trend in [

        "BULLISH",

        "BEARISH"

    ]:

        score += 10

        reasons.append(

            "Trend Confirmed"

        )


    # Higher timeframe bias

    bias = market_data.get(

        "bias"

    )


    if bias:

        score += 10

        reasons.append(

            "HTF Bias"

        )


    if score > WEIGHTS["market"]:

        score = WEIGHTS["market"]


    return create_score(

        "market",

        score,

        reasons

    )



# ==========================
# MARKET DIRECTION
# ==========================

def market_direction(

    market_data=None

):

    if market_data is None:

        return "NEUTRAL"


    if market_data.get("trend"):

        return market_data["trend"]


    return "NEUTRAL"
    # ==========================
# STRUCTURE SCORE ENGINE
# ==========================

def calculate_structure_score(

    structure_data=None

):

    score = 0

    reasons = []


    if structure_data is None:

        return create_score(

            "structure",

            0,

            "No structure data"

        )


    # BOS Confirmation

    if structure_data.get(

        "bos"

    ):

        score += 10

        reasons.append(

            "BOS"

        )


    # MSS Confirmation

    if structure_data.get(

        "mss"

    ):

        score += 10

        reasons.append(

            "MSS"

        )


    # CHoCH Confirmation

    if structure_data.get(

        "choch"

    ):

        score += 5

        reasons.append(

            "CHoCH"

        )


    if score > WEIGHTS["structure"]:

        score = WEIGHTS["structure"]


    return create_score(

        "structure",

        score,

        reasons

    )



# ==========================
# STRUCTURE DIRECTION
# ==========================

def structure_direction(

    structure_data=None

):

    if structure_data is None:

        return "NEUTRAL"


    if structure_data.get(

        "direction"

    ):

        return structure_data["direction"]


    return "NEUTRAL"
    # ==========================
# SMART MONEY SCORE ENGINE
# ==========================

def calculate_smart_money_score(

    smart_money_data=None

):

    score = 0

    reasons = []


    if smart_money_data is None:

        return create_score(

            "smart_money",

            0,

            "No smart money data"

        )


    # Order Block

    if smart_money_data.get(

        "order_block"

    ):

        score += 10

        reasons.append(

            "Order Block"

        )


    # Liquidity Sweep

    if smart_money_data.get(

        "liquidity"

    ):

        score += 10

        reasons.append(

            "Liquidity Sweep"

        )


    # Volume Confirmation

    if smart_money_data.get(

        "volume"

    ):

        score += 5

        reasons.append(

            "Volume"

        )


    if score > WEIGHTS["smart_money"]:

        score = WEIGHTS["smart_money"]


    return create_score(

        "smart_money",

        score,

        reasons

    )



# ==========================
# SMART MONEY DIRECTION
# ==========================

def smart_money_direction(

    smart_money_data=None

):

    if smart_money_data is None:

        return "NEUTRAL"


    return smart_money_data.get(

        "direction",

        "NEUTRAL"

    )
    # ==========================
# PD ARRAY SCORE ENGINE
# ==========================

def calculate_pd_array_score(

    pd_data=None

):

    score = 0

    reasons = []


    if pd_data is None:

        return create_score(

            "pd_array",

            0,

            "No PD Array data"

        )


    if pd_data.get(

        "active"

    ):

        score += 10

        reasons.append(

            "Active PD Array"

        )


    if pd_data.get(

        "quality"

    ) == "STRONG":

        score += 5

        reasons.append(

            "Strong PD Quality"

        )


    if score > WEIGHTS["pd_array"]:

        score = WEIGHTS["pd_array"]


    return create_score(

        "pd_array",

        score,

        reasons

    )



# ==========================
# OTE SCORE ENGINE
# ==========================

def calculate_ote_score(

    ote_data=None

):

    score = 0

    reasons = []


    if ote_data is None:

        return create_score(

            "ote",

            0,

            "No OTE data"

        )


    if ote_data.get(

        "valid"

    ):

        score += 10

        reasons.append(

            "OTE Active"

        )


    if ote_data.get(

        "confluence"

    ):

        score += 5

        reasons.append(

            "OTE Confluence"

        )


    if score > WEIGHTS["ote"]:

        score = WEIGHTS["ote"]


    return create_score(

        "ote",

        score,

        reasons

    )
    # ==========================
# SMT SCORE ENGINE
# ==========================

def calculate_smt_score(

    smt_data=None

):

    score = 0

    reasons = []


    if smt_data is None:

        return create_score(

            "smt",

            0,

            "No SMT data"

        )


    if smt_data.get(

        "signal"

    ):

        score += 5

        reasons.append(

            "SMT Divergence"

        )


    if smt_data.get(

        "confirmed"

    ):

        score += 5

        reasons.append(

            "SMT Confirmed"

        )


    if score > WEIGHTS["smt"]:

        score = WEIGHTS["smt"]


    return create_score(

        "smt",

        score,

        reasons

    )



# ==========================
# TOTAL SCORE CALCULATION
# ==========================

def calculate_total_score(

    scores

):

    total = 0

    details = []


    for item in scores:

        total += item["score"]

        details.append(

            item

        )


    if total > MAX_SCORE:

        total = MAX_SCORE


    return {

        "score":

        total,

        "details":

        details

    }
    # ==========================
# FINAL CONFIDENCE ANALYZER
# ==========================

def analyze_confidence(

    market=None,

    structure=None,

    smart_money=None,

    pd_array=None,

    ote=None,

    smt=None

):

    scores = []


    scores.append(

        calculate_market_score(

            market

        )

    )


    scores.append(

        calculate_structure_score(

            structure

        )

    )


    scores.append(

        calculate_smart_money_score(

            smart_money

        )

    )


    scores.append(

        calculate_pd_array_score(

            pd_array

        )

    )


    scores.append(

        calculate_ote_score(

            ote

        )

    )


    scores.append(

        calculate_smt_score(

            smt

        )

    )


    total = calculate_total_score(

        scores

    )


    decision = (

        "TRADE"

        if

        total["score"]

        >=

        MIN_TRADE_SCORE

        else

        "NO TRADE"

    )


    return {

        "score":

        total["score"],

        "decision":

        decision,

        "details":

        total["details"]

    }



# ==========================
# TRADE CHECK
# ==========================

def is_high_confidence(

    result

):

    if result is None:

        return False


    return (

        result["score"]

        >=

        MIN_TRADE_SCORE

    )
    # ==========================
# DIRECTION ALIGNMENT
# ==========================

def check_direction_alignment(

    market=None,

    structure=None,

    smart_money=None,

    ote=None,

    smt=None

):

    directions = []


    if market:

        directions.append(

            market_direction(

                market

            )

        )


    if structure:

        directions.append(

            structure_direction(

                structure

            )

        )


    if smart_money:

        directions.append(

            smart_money_direction(

                smart_money

            )

        )


    if ote:

        if ote.get("direction"):

            directions.append(

                ote["direction"]

            )


    if smt:

        if smt.get("direction"):

            directions.append(

                smt["direction"]

            )


    buy = directions.count(

        "BUY"

    )


    sell = directions.count(

        "SELL"

    )


    if buy > sell:

        return {

            "direction":

            "BUY",

            "aligned":

            True

        }


    if sell > buy:

        return {

            "direction":

            "SELL",

            "aligned":

            True

        }


    return {

        "direction":

        "NEUTRAL",

        "aligned":

        False

    }



# ==========================
# CONFIDENCE REPORT
# ==========================

def confidence_report(

    **kwargs

):

    result = analyze_confidence(

        **kwargs

    )


    alignment = check_direction_alignment(

        kwargs.get("market"),

        kwargs.get("structure"),

        kwargs.get("smart_money"),

        kwargs.get("ote"),

        kwargs.get("smt")

    )


    return {

        "score":

        result["score"],

        "decision":

        result["decision"],

        "direction":

        alignment["direction"],

        "aligned":

        alignment["aligned"],

        "details":

        result["details"]

    }
    # ==========================
# CONFIDENCE DEBUG PANEL
# ==========================

def debug_confidence(

    **kwargs

):

    result = confidence_report(

        **kwargs

    )


    print("\n========== CONFIDENCE V5 ==========")

    print(

        "Score     :",

        result["score"]

    )

    print(

        "Decision  :",

        result["decision"]

    )

    print(

        "Direction :",

        result["direction"]

    )

    print(

        "Aligned   :",

        result["aligned"]

    )


    print(

        "Details   :",

        result["details"]

    )

    print(

        "===================================\n"

    )


    return result



# ==========================
# SCORE SUMMARY
# ==========================

def score_summary(

    **kwargs

):

    result = analyze_confidence(

        **kwargs

    )


    summary = {}


    for item in result["details"]:

        summary[item["name"]] = {

            "score":

            item["score"],

            "reason":

            item["reason"]

        }


    return {

        "total":

        result["score"],

        "decision":

        result["decision"],

        "modules":

        summary

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def confidence_engine_v5(

    market=None,

    structure=None,

    smart_money=None,

    pd_array=None,

    ote=None,

    smt=None

):

    result = analyze_confidence(

        market,

        structure,

        smart_money,

        pd_array,

        ote,

        smt

    )


    return {

        "confidence":

        result["score"],

        "signal":

        result["decision"],

        "details":

        result["details"]

    }



# ==========================
# FINAL DECISION
# ==========================

def final_trade_decision(

    **kwargs

):

    result = confidence_report(

        **kwargs

    )


    if (

        result["decision"]

        ==

        "TRADE"

        and

        result["aligned"]

    ):

        return {

            "trade":

            True,

            "direction":

            result["direction"],

            "confidence":

            result["score"]

        }


    return {

        "trade":

        False,

        "direction":

        "NO TRADE",

        "confidence":

        result["score"]

    }



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "calculate_market_score",

    "calculate_structure_score",

    "calculate_smart_money_score",

    "calculate_pd_array_score",

    "calculate_ote_score",

    "calculate_smt_score",

    "calculate_total_score",

    "analyze_confidence",

    "confidence_report",

    "confidence_engine_v5",

    "final_trade_decision",

    "debug_confidence",

    "score_summary"

]
