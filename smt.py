import pandas as pd
import numpy as np

# ==========================
# ICT SMT ENGINE V5
# ==========================

SMT_LOOKBACK = 50


# ==========================
# PREPARE DATA
# ==========================

def prepare_smt(df):

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
# GET RECENT HIGH
# ==========================

def get_recent_high(df):

    high = df["high"].tail(
        SMT_LOOKBACK
    ).max()

    return float(high)



# ==========================
# GET RECENT LOW
# ==========================

def get_recent_low(df):

    low = df["low"].tail(
        SMT_LOOKBACK
    ).min()

    return float(low)
    # ==========================
# SWING COMPARISON
# ==========================

def compare_highs(df1, df2):

    high1 = get_recent_high(df1)

    high2 = get_recent_high(df2)


    return {

        "market1_high": high1,

        "market2_high": high2,

        "market1_higher":

        high1 > high2

    }



def compare_lows(df1, df2):

    low1 = get_recent_low(df1)

    low2 = get_recent_low(df2)


    return {

        "market1_low": low1,

        "market2_low": low2,

        "market1_lower":

        low1 < low2

    }



# ==========================
# HIGH DIVERGENCE
# ==========================

def high_divergence(df1, df2):

    result = compare_highs(

        df1,

        df2

    )


    # One market makes higher high,
    # other fails

    if (

        result["market1_higher"]

    ):

        return {

            "type":

            "High Divergence",

            "direction":

            "BEARISH"

        }


    return None



# ==========================
# LOW DIVERGENCE
# ==========================

def low_divergence(df1, df2):

    result = compare_lows(

        df1,

        df2

    )


    # One market makes lower low,
    # other fails

    if (

        result["market1_lower"]

    ):

        return {

            "type":

            "Low Divergence",

            "direction":

            "BULLISH"

        }


    return None
    # ==========================
# BULLISH SMT DIVERGENCE
# ==========================

def detect_bullish_smt(df1, df2):

    low1 = get_recent_low(df1)

    low2 = get_recent_low(df2)


    current1 = float(

        df1["low"].iloc[-1]

    )

    current2 = float(

        df2["low"].iloc[-1]

    )


    # Market 1 takes lower low
    # Market 2 fails to take lower low

    if (

        current1 < low1

        and

        current2 > low2

    ):

        return {

            "type":

            "Bullish SMT",

            "direction":

            "BUY",

            "market":

            "Market 1"

        }


    return None



# ==========================
# BEARISH SMT DIVERGENCE
# ==========================

def detect_bearish_smt(df1, df2):

    high1 = get_recent_high(df1)

    high2 = get_recent_high(df2)


    current1 = float(

        df1["high"].iloc[-1]

    )

    current2 = float(

        df2["high"].iloc[-1]

    )


    # Market 1 takes higher high
    # Market 2 fails to take higher high

    if (

        current1 > high1

        and

        current2 < high2

    ):

        return {

            "type":

            "Bearish SMT",

            "direction":

            "SELL",

            "market":

            "Market 1"

        }


    return None



# ==========================
# SMT DETECTOR
# ==========================

def detect_smt(df1, df2):

    bullish = detect_bullish_smt(

        df1,

        df2

    )


    if bullish:

        return bullish


    bearish = detect_bearish_smt(

        df1,

        df2

    )


    if bearish:

        return bearish


    return None
    # ==========================
# MULTI MARKET SMT SCANNER
# ==========================

def scan_smt_pairs(

    markets

):

    signals = []


    names = list(

        markets.keys()

    )


    for i in range(

        len(names)

    ):

        for j in range(

            i + 1,

            len(names)

        ):

            market1 = names[i]

            market2 = names[j]


            df1 = markets[market1]

            df2 = markets[market2]


            smt = detect_smt(

                df1,

                df2

            )


            if smt:

                smt["pair"] = (

                    market1

                    +

                    "_"

                    +

                    market2

                )

                signals.append(smt)


    return signals



# ==========================
# BEST SMT SIGNAL
# ==========================

def get_best_smt_signal(

    markets

):

    signals = scan_smt_pairs(

        markets

    )


    if len(signals) == 0:

        return None


    return signals[0]



# ==========================
# SMT PAIR CHECK
# ==========================

def check_smt_pair(

    df1,

    df2,

    name1="A",

    name2="B"

):

    result = detect_smt(

        df1,

        df2

    )


    if result:

        result["pair"] = (

            name1

            +

            "-"

            +

            name2

        )


    return result
    # ==========================
# SMT SCORE ENGINE
# ==========================

def calculate_smt_score(signal):

    if signal is None:

        return {

            "score": 0,

            "quality": "NONE"

        }


    score = 0

    reasons = []


    if signal["type"] == "Bullish SMT":

        score += 50

        reasons.append(

            "Bullish Divergence"

        )


    if signal["type"] == "Bearish SMT":

        score += 50

        reasons.append(

            "Bearish Divergence"

        )


    if "pair" in signal:

        score += 20

        reasons.append(

            "Pair Confirmation"

        )


    if score >= 70:

        quality = "STRONG"


    elif score >= 50:

        quality = "GOOD"


    else:

        quality = "WEAK"



    return {

        "score": score,

        "quality": quality,

        "reasons": reasons

    }



# ==========================
# SMT VALIDATION
# ==========================

def validate_smt(signal):

    result = calculate_smt_score(

        signal

    )


    return (

        result["score"] >= 50

    )



# ==========================
# SMT SUMMARY
# ==========================

def smt_strength(signal):

    result = calculate_smt_score(

        signal

    )


    return {

        "signal": signal,

        "score": result["score"],

        "quality": result["quality"],

        "reasons": result["reasons"]

    }
    # ==========================
# SMT + STRUCTURE CONFLUENCE
# ==========================

def smt_structure_confluence(

    smt_signal,

    structure=None

):

    score = 0

    reasons = []


    if smt_signal is None:

        return {

            "score": 0,

            "reasons": [

                "No SMT"

            ]

        }


    # SMT Exists

    score += 50

    reasons.append(

        "SMT Divergence"

    )


    # Structure Confirmation

    if structure:

        bos = structure.get(

            "bos"

        )

        mss = structure.get(

            "mss"

        )


        if bos:

            score += 25

            reasons.append(

                "BOS Confirmation"

            )


        if mss:

            score += 25

            reasons.append(

                "MSS Confirmation"

            )


    if score > 100:

        score = 100


    return {

        "score": score,

        "reasons": reasons

    }



# ==========================
# SMT + LIQUIDITY CONFIRM
# ==========================

def smt_liquidity_confirmation(

    smt_signal,

    liquidity=None

):

    score = 0

    reasons = []


    if smt_signal:

        score += 50

        reasons.append(

            "SMT"

        )


    if liquidity:

        score += 30

        reasons.append(

            "Liquidity Sweep"

        )


    return {

        "score": min(score,100),

        "reasons": reasons

    }



# ==========================
# FINAL SMT CONFIRMATION
# ==========================

def institutional_smt_confirmation(

    smt_signal,

    structure=None,

    liquidity=None

):

    structure_result = smt_structure_confluence(

        smt_signal,

        structure

    )


    liquidity_result = smt_liquidity_confirmation(

        smt_signal,

        liquidity

    )


    total = (

        structure_result["score"]

        +

        liquidity_result["score"]

    )


    if total > 100:

        total = 100


    return {

        "score": total,

        "confirmed":

        total >= 70,

        "reasons":

        structure_result["reasons"]

        +

        liquidity_result["reasons"]

    }
    # ==========================
# SMT ENTRY BIAS
# ==========================

def smt_entry_bias(signal):

    if signal is None:

        return {

            "bias": "NEUTRAL",

            "direction": None

        }


    if signal["direction"] == "BUY":

        return {

            "bias": "BULLISH",

            "direction": "BUY"

        }


    if signal["direction"] == "SELL":

        return {

            "bias": "BEARISH",

            "direction": "SELL"

        }


    return {

        "bias": "NEUTRAL",

        "direction": None

    }



# ==========================
# FINAL SMT ANALYSIS
# ==========================

def analyze_smt_v5(

    df1,

    df2,

    structure=None,

    liquidity=None

):

    signal = detect_smt(

        df1,

        df2

    )


    strength = smt_strength(

        signal

    )


    confirmation = institutional_smt_confirmation(

        signal,

        structure,

        liquidity

    )


    return {

        "signal": signal,

        "bias":

        smt_entry_bias(signal),

        "strength":

        strength,

        "confirmation":

        confirmation

    }



# ==========================
# SMT TRADE VALIDATION
# ==========================

def smt_trade_valid(

    df1,

    df2

):

    result = analyze_smt_v5(

        df1,

        df2

    )


    return (

        result["confirmation"]["confirmed"]

    )
    # ==========================
# SMT + OTE CONFLUENCE
# ==========================

def smt_ote_confluence(

    smt_signal,

    ote=None

):

    score = 0

    reasons = []


    if smt_signal is None:

        return {

            "score": 0,

            "reasons": [

                "No SMT"

            ]

        }


    score += 50

    reasons.append(

        "SMT Divergence"

    )


    if ote:

        if (

            smt_signal["direction"]

            ==

            ote.get("direction")

        ):

            score += 30

            reasons.append(

                "OTE Direction Match"

            )


    return {

        "score": min(score,100),

        "reasons": reasons

    }



# ==========================
# SMT + SMART MONEY
# ==========================

def smt_smart_money_confluence(

    smt_signal,

    smart_money=None

):

    score = 0

    reasons = []


    if smt_signal:

        score += 50

        reasons.append(

            "SMT"

        )


    if smart_money:

        direction = smart_money.get(

            "direction"

        )


        if (

            direction

            ==

            smt_signal.get("direction")

        ):

            score += 30

            reasons.append(

                "Smart Money Match"

            )


    return {

        "score": min(score,100),

        "reasons": reasons

    }



# ==========================
# INSTITUTIONAL SMT SIGNAL
# ==========================

def institutional_smt_signal(

    df1,

    df2,

    ote=None,

    smart_money=None

):

    smt = detect_smt(

        df1,

        df2

    )


    ote_result = smt_ote_confluence(

        smt,

        ote

    )


    sm_result = smt_smart_money_confluence(

        smt,

        smart_money

    )


    total = (

        ote_result["score"]

        +

        sm_result["score"]

    )


    if total > 100:

        total = 100


    return {

        "signal": smt,

        "score": total,

        "confirmed":

        total >= 70,

        "reasons":

        ote_result["reasons"]

        +

        sm_result["reasons"]

    }
    # ==========================
# SMT DEBUG PANEL
# ==========================

def debug_smt(

    df1,

    df2

):

    result = analyze_smt_v5(

        df1,

        df2

    )


    print("\n========== SMT V5 ==========")

    print(

        "Signal       :",

        result["signal"]

    )

    print(

        "Bias         :",

        result["bias"]

    )

    print(

        "Strength     :",

        result["strength"]

    )

    print(

        "Confirmation :",

        result["confirmation"]

    )

    print(

        "============================\n"

    )


    return result



# ==========================
# SMT REPORT
# ==========================

def smt_report(

    df1,

    df2

):

    result = analyze_smt_v5(

        df1,

        df2

    )


    return {

        "signal":

        result["signal"],

        "direction":

        result["bias"]["direction"],

        "score":

        result["confirmation"]["score"],

        "confirmed":

        result["confirmation"]["confirmed"],

        "reasons":

        result["confirmation"]["reasons"]

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_smt(

    df1,

    df2

):

    result = analyze_smt_v5(

        df1,

        df2

    )


    return {

        "signal":

        result["signal"],

        "bias":

        result["bias"],

        "strength":

        result["strength"],

        "confirmation":

        result["confirmation"]

    }



# ==========================
# SMT ENGINE V5
# ==========================

def smt_engine_v5(

    df1,

    df2

):

    result = analyze_smt(

        df1,

        df2

    )


    return {

        "direction":

        result["bias"]["direction"],

        "score":

        result["confirmation"]["score"],

        "confirmed":

        result["confirmation"]["confirmed"],

        "signal":

        result["signal"]

    }



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "detect_bullish_smt",

    "detect_bearish_smt",

    "detect_smt",

    "scan_smt_pairs",

    "get_best_smt_signal",

    "calculate_smt_score",

    "validate_smt",

    "smt_strength",

    "analyze_smt",

    "analyze_smt_v5",

    "smt_engine_v5",

    "institutional_smt_signal",

    "debug_smt",

    "smt_report"

]
