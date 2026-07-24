# ==========================================================
# ICT TRADING BOT V12
# STRUCTURE ENGINE
# PHASE 1
# PART A1
# Foundation Layer
# Production Ready
# ==========================================================

from typing import Dict, List, Optional
import pandas as pd
import numpy as np

# ==========================================================
# GLOBAL MEMORY
# ==========================================================

V12_STRUCTURE_MEMORY: List[str] = []

# ==========================================================
# GLOBAL SETTINGS
# ==========================================================

SWING_LOOKBACK = 5
MAX_STRUCTURE_HISTORY = 10

# ==========================================================
# END OF PART A1
# ==========================================================
# ==========================================================
# SWING POINT DETECTOR
# ==========================================================

def swing_history_v12(df) -> Dict:

    highs = []
    lows = []

    if len(df) < 10:
        return {
            "highs": highs,
            "lows": lows
        }

    for i in range(2, len(df) - 2):

        high = float(df["high"].iloc[i])
        low = float(df["low"].iloc[i])

        if (
            high > float(df["high"].iloc[i - 1])
            and
            high > float(df["high"].iloc[i + 1])
        ):
            highs.append(high)

        if (
            low < float(df["low"].iloc[i - 1])
            and
            low < float(df["low"].iloc[i + 1])
        ):
            lows.append(low)

    return {
        "highs": highs[-MAX_STRUCTURE_HISTORY:],
        "lows": lows[-MAX_STRUCTURE_HISTORY:]
    }


# ==========================================================
# DYNAMIC SWING HIGH
# ==========================================================

def dynamic_swing_high(
    df,
    lookback: int = SWING_LOOKBACK
) -> Optional[Dict]:

    if len(df) < (lookback * 2 + 1):
        return None

    for i in range(
        len(df) - lookback - 1,
        lookback,
        -1
    ):

        high = float(df["high"].iloc[i])

        left = df["high"].iloc[
            i-lookback:i
        ]

        right = df["high"].iloc[
            i+1:i+lookback+1
        ]

        if (
            high > left.max()
            and
            high > right.max()
        ):

            return {
                "price": high,
                "index": i,
                "type": "SWING_HIGH"
            }

    return None


# ==========================================================
# DYNAMIC SWING LOW
# ==========================================================

def dynamic_swing_low(
    df,
    lookback: int = SWING_LOOKBACK
) -> Optional[Dict]:

    if len(df) < (lookback * 2 + 1):
        return None

    for i in range(
        len(df) - lookback - 1,
        lookback,
        -1
    ):

        low = float(df["low"].iloc[i])

        left = df["low"].iloc[
            i-lookback:i
        ]

        right = df["low"].iloc[
            i+1:i+lookback+1
        ]

        if (
            low < left.min()
            and
            low < right.min()
        ):

            return {
                "price": low,
                "index": i,
                "type": "SWING_LOW"
            }

    return None


# ==========================================================
# DYNAMIC SWING MAP
# ==========================================================

def dynamic_swing_map(df) -> Dict:

    return {

        "high": dynamic_swing_high(df),

        "low": dynamic_swing_low(df)

    }


# ==========================================================
# STRUCTURE LEVELS
# ==========================================================

def dynamic_structure_levels(df) -> Dict:

    swings = dynamic_swing_map(df)

    return {

        "resistance":
            swings["high"]["price"]
            if swings["high"]
            else None,

        "support":
            swings["low"]["price"]
            if swings["low"]
            else None
    }


# ==========================================================
# SWING QUALITY SCORE
# ==========================================================

def swing_quality_score(df) -> int:

    score = 0

    swings = dynamic_swing_map(df)

    if swings["high"]:
        score += 40

    if swings["low"]:
        score += 40

    levels = dynamic_structure_levels(df)

    if (
        levels["support"] is not None
        or
        levels["resistance"] is not None
    ):
        score += 20

    return min(score, 100)
  # ==========================================================
# INTERNAL STRUCTURE BREAK (BOS)
# ==========================================================

def internal_structure_break(df) -> Optional[Dict]:

    swing_high = dynamic_swing_high(df)
    swing_low = dynamic_swing_low(df)

    if swing_high is None or swing_low is None:

        swings = swing_history_v12(df)

        if swing_high is None and swings["highs"]:
            swing_high = {
                "price": swings["highs"][-1],
                "type": "SWING_HIGH"
            }

        if swing_low is None and swings["lows"]:
            swing_low = {
                "price": swings["lows"][-1],
                "type": "SWING_LOW"
            }

    if swing_high is None or swing_low is None:
        return None

    close = float(df["close"].iloc[-1])
    high = float(df["high"].iloc[-1])
    low = float(df["low"].iloc[-1])

    if close > swing_high["price"] or high > swing_high["price"]:

        return {
            "type": "BOS",
            "direction": "BUY",
            "level": swing_high["price"]
        }

    if close < swing_low["price"] or low < swing_low["price"]:

        return {
            "type": "BOS",
            "direction": "SELL",
            "level": swing_low["price"]
        }

    return None


# ==========================================================
# BULLISH MSS
# ==========================================================

def bullish_mss(df) -> Optional[Dict]:

    bos = internal_structure_break(df)

    if (
        bos
        and
        bos["direction"] == "BUY"
    ):

        return {
            "type": "MSS",
            "direction": "BUY",
            "level": bos["level"]
        }

    return None


# ==========================================================
# BEARISH MSS
# ==========================================================

def bearish_mss(df) -> Optional[Dict]:

    bos = internal_structure_break(df)

    if (
        bos
        and
        bos["direction"] == "SELL"
    ):

        return {
            "type": "MSS",
            "direction": "SELL",
            "level": bos["level"]
        }

    return None


# ==========================================================
# MSS DETECTOR
# ==========================================================

def detect_mss(df) -> Optional[Dict]:

    bull = bullish_mss(df)

    if bull:
        return bull

    bear = bearish_mss(df)

    if bear:
        return bear

    return None


# ==========================================================
# CHOCH DETECTOR
# ==========================================================

def detect_choch(df) -> Optional[Dict]:

    mss = detect_mss(df)

    if mss is None:
        return None

    return {
        "type": "CHOCH",
        "direction": mss["direction"],
        "level": mss["level"]
    }


# ==========================================================
# STRUCTURE EVENT
# ==========================================================

def get_structure_event_v12(df) -> Dict:

    choch = detect_choch(df)

    if choch:
        return choch

    mss = detect_mss(df)

    if mss:
        return mss

    bos = internal_structure_break(df)

    if bos:
        return bos

    return {
        "type": "NONE",
        "direction": "NONE",
        "level": None
    }
  # ==========================================================
# STRUCTURE MEMORY TRACKER
# ==========================================================

def structure_memory_tracker_v12(df) -> Dict:

    global V12_STRUCTURE_MEMORY

    event = "NONE"

    mss = detect_mss(df)
    isb = internal_structure_break(df)
    choch = detect_choch(df)

    if choch:

        if choch["direction"] == "BUY":
            event = "BULLISH_CHOCH"
        else:
            event = "BEARISH_CHOCH"

    elif mss:

        if mss["direction"] == "BUY":
            event = "BULLISH_MSS"
        else:
            event = "BEARISH_MSS"

    elif isb:

        if isb["direction"] == "BUY":
            event = "BULLISH_BOS"
        else:
            event = "BEARISH_BOS"

    V12_STRUCTURE_MEMORY.append(event)

    if len(V12_STRUCTURE_MEMORY) > MAX_STRUCTURE_HISTORY:
        V12_STRUCTURE_MEMORY = V12_STRUCTURE_MEMORY[
            -MAX_STRUCTURE_HISTORY:
        ]

    return {

        "event": event,

        "history": V12_STRUCTURE_MEMORY.copy()

    }


# ==========================================================
# STRUCTURE MEMORY SCORE
# ==========================================================

def structure_memory_score_v12(df) -> int:

    tracker = structure_memory_tracker_v12(df)

    score = 0

    event = tracker["event"]

    if event != "NONE":
        score += 40

    if "BOS" in event:
        score += 20

    if "MSS" in event:
        score += 20

    if "CHOCH" in event:
        score += 20

    recent = tracker["history"][-5:]

    confirmations = 0

    for item in recent:

        if item != "NONE":
            confirmations += 1

    score += confirmations * 4

    return min(score, 100)


# ==========================================================
# STRUCTURE STRENGTH
# ==========================================================

def structure_strength_v12(df) -> Dict:

    tracker = structure_memory_tracker_v12(df)

    score = structure_memory_score_v12(df)

    strength = "WEAK"

    if score >= 80:

        strength = "VERY_STRONG"

    elif score >= 60:

        strength = "STRONG"

    elif score >= 40:

        strength = "MEDIUM"

    return {

        "strength": strength,

        "score": score,

        "event": tracker["event"]

    }


# ==========================================================
# INSTITUTIONAL STRUCTURE MEMORY
# ==========================================================

def institutional_structure_memory_v12(df) -> Dict:

    tracker = structure_memory_tracker_v12(df)

    strength = structure_strength_v12(df)

    return {

        "structure": tracker,

        "score": strength["score"],

        "strength": strength["strength"]

    }


# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================

def get_structure_memory_v12(df) -> Dict:

    return institutional_structure_memory_v12(df)


# ==========================================================
# STRUCTURE STATUS
# ==========================================================

def structure_status_v12(df) -> Dict:

    memory = institutional_structure_memory_v12(df)

    approved = memory["score"] >= 70

    return {

        "approved": approved,

        "event": memory["structure"]["event"],

        "score": memory["score"],

        "strength": memory["strength"]

    }


# ==========================================================
# STRUCTURE FILTER
# ==========================================================

def structure_filter_v12(df) -> bool:

    return structure_status_v12(df)["approved"]


# ==========================================================
# STRUCTURE REPORT
# ==========================================================

def structure_report_v12(df) -> Dict:

    memory = institutional_structure_memory_v12(df)

    return {

        "engine": "ICT_STRUCTURE_V12",

        "event": memory["structure"]["event"],

        "history": memory["structure"]["history"],

        "score": memory["score"],

        "strength": memory["strength"],

        "approved": memory["score"] >= 70

    }
  # ==========================================================
# STRUCTURE CONFIRMATION ENGINE
# ==========================================================

def structure_confirmation_v12(df) -> Dict:

    memory = institutional_structure_memory_v12(df)

    event = memory["structure"]["event"]
    score = memory["score"]

    direction = "NONE"
    approved = False

    if "BUY" in event:
        direction = "BUY"

    elif "SELL" in event:
        direction = "SELL"

    if score >= 70:
        approved = True

    return {

        "approved": approved,

        "direction": direction,

        "event": event,

        "score": score

    }


# ==========================================================
# STRUCTURE CONFLUENCE ENGINE
# ==========================================================

def structure_confluence_v12(df) -> Dict:

    confirmation = structure_confirmation_v12(df)

    swing_score = swing_quality_score(df)

    memory_score = structure_memory_score_v12(df)

    total = int(
        (
            swing_score +
            memory_score +
            confirmation["score"]
        ) / 3
    )

    return {

        "approved": total >= 70,

        "confidence": total,

        "direction": confirmation["direction"],

        "event": confirmation["event"]

    }


# ==========================================================
# REVERSAL CONFIRMATION
# ==========================================================

def reversal_confirmation_v12(df) -> Dict:

    mss = detect_mss(df)

    choch = detect_choch(df)

    confidence = 0

    signal = "NONE"

    if choch:

        signal = choch["direction"]

        confidence += 60

    if mss:

        signal = mss["direction"]

        confidence += 40

    return {

        "signal": signal,

        "confidence": min(confidence,100),

        "approved": confidence >= 70

    }


# ==========================================================
# ENTRY CONFIRMATION MATRIX
# ==========================================================

def entry_confirmation_matrix_v12(df) -> Dict:

    structure = structure_confluence_v12(df)

    reversal = reversal_confirmation_v12(df)

    score = int(
        (
            structure["confidence"] +
            reversal["confidence"]
        ) / 2
    )

    direction = structure["direction"]

    if direction == "NONE":
        direction = reversal["signal"]

    return {

        "approved": score >= 70,

        "direction": direction,

        "confidence": score,

        "components": {

            "structure": structure,

            "reversal": reversal

        }

    }


# ==========================================================
# FINAL STRUCTURE SIGNAL
# ==========================================================

def structure_signal_v12(df) -> Dict:

    matrix = entry_confirmation_matrix_v12(df)

    signal = "NO_TRADE"

    if matrix["approved"]:

        signal = matrix["direction"]

    return {

        "signal": signal,

        "confidence": matrix["confidence"],

        "approved": matrix["approved"]

    }


# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================

def get_structure_confirmation_v12(df) -> Dict:

    return structure_confirmation_v12(df)


def get_entry_confirmation_matrix_v12(df) -> Dict:

    return entry_confirmation_matrix_v12(df)


def get_structure_signal_v12(df) -> Dict:

    return structure_signal_v12(df)
  
  # ==========================================================
# STRUCTURE MASTER CONTROLLER V12
# ==========================================================


def structure_master_controller_v12(df) -> Dict:

    signal = structure_signal_v12(df)

    confirmation = structure_confirmation_v12(df)

    matrix = entry_confirmation_matrix_v12(df)

    memory = institutional_structure_memory_v12(df)


    approved = False

    final_signal = "NO_TRADE"


    if (
        signal["approved"]
        and
        matrix["approved"]
    ):

        approved = True

        final_signal = signal["signal"]


    return {

        "approved": approved,

        "signal": final_signal,

        "confidence": signal["confidence"],

        "structure": {

            "event":
                memory["structure"]["event"],

            "strength":
                memory["strength"],

            "score":
                memory["score"]

        },

        "confirmation": confirmation,

        "matrix": matrix

    }



# ==========================================================
# STRUCTURE VALIDATION ENGINE V12
# ==========================================================


def validate_structure_v12(df) -> Dict:


    memory = institutional_structure_memory_v12(df)

    matrix = entry_confirmation_matrix_v12(df)

    errors = []


    if memory is None:

        errors.append(
            "MEMORY_EMPTY"
        )


    if matrix is None:

        errors.append(
            "MATRIX_EMPTY"
        )


    if not isinstance(
        memory,
        dict
    ):

        errors.append(
            "MEMORY_INVALID"
        )


    if not isinstance(
        matrix,
        dict
    ):

        errors.append(
            "MATRIX_INVALID"
        )


    return {

        "valid":
            len(errors) == 0,

        "errors":
            errors

    }



# ==========================================================
# STRUCTURE DEBUG REPORT V12
# ==========================================================


def structure_debug_report_v12(df) -> Dict:


    controller = structure_master_controller_v12(df)

    validation = validate_structure_v12(df)


    return {

        "engine":
            "ICT_STRUCTURE_V12",


        "controller":
            controller,


        "validation":
            validation

    }



# ==========================================================
# STRUCTURE DECISION ENGINE V12
# ==========================================================


def structure_decision_v12(df) -> Dict:


    result = structure_master_controller_v12(df)


    decision = "WAIT"


    if result["approved"]:

        if result["signal"] == "BUY":

            decision = "BUY"


        elif result["signal"] == "SELL":

            decision = "SELL"



    return {

        "decision":
            decision,

        "approved":
            result["approved"],

        "signal":
            result["signal"],

        "confidence":
            result["confidence"]

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_structure_master_v12(df) -> Dict:

    return structure_master_controller_v12(df)



def get_structure_decision_v12(df) -> Dict:

    return structure_decision_v12(df)



def get_structure_debug_v12(df) -> Dict:

    return structure_debug_report_v12(df)



# ==========================================================
# END PHASE 1 STRUCTURE CONTROL LAYER
# ==========================================================

# ==========================================================
# STRUCTURE ADAPTIVE FILTER ENGINE V12
# ==========================================================


def adaptive_structure_filter_v12(df) -> Dict:

    master = structure_master_controller_v12(df)

    confidence = master["confidence"]

    signal = master["signal"]


    market_state = "NEUTRAL"


    if confidence >= 80:

        market_state = "HIGH_CONFIDENCE"


    elif confidence >= 60:

        market_state = "VALID"


    elif confidence >= 40:

        market_state = "WEAK"



    approved = False


    if (
        signal != "NO_TRADE"
        and
        confidence >= 70
    ):

        approved = True



    return {

        "approved":
            approved,

        "signal":
            signal,

        "confidence":
            confidence,

        "state":
            market_state

    }



# ==========================================================
# STRUCTURE MOMENTUM CONFIRMATION V12
# ==========================================================


def structure_momentum_confirmation_v12(df) -> Dict:


    tracker = structure_memory_tracker_v12(df)

    history = tracker["history"]


    bullish = 0

    bearish = 0


    for event in history:


        if "BULLISH" in event:

            bullish += 1


        elif "BEARISH" in event:

            bearish += 1



    direction = "NONE"


    if bullish > bearish:

        direction = "BUY"


    elif bearish > bullish:

        direction = "SELL"



    strength = abs(
        bullish - bearish
    )



    return {

        "direction":
            direction,

        "bullish_events":
            bullish,

        "bearish_events":
            bearish,

        "strength":
            strength,

        "approved":
            strength >= 2

    }



# ==========================================================
# STRUCTURE FINAL APPROVAL ENGINE V12
# ==========================================================


def structure_final_approval_v12(df) -> Dict:


    adaptive = adaptive_structure_filter_v12(df)

    momentum = structure_momentum_confirmation_v12(df)


    final_signal = "NO_TRADE"

    approved = False


    if adaptive["approved"]:


        if (
            adaptive["signal"]
            ==
            momentum["direction"]
        ):

            final_signal = adaptive["signal"]

            approved = True



    confidence = int(

        (
            adaptive["confidence"]
            +
            momentum["strength"] * 10

        )
        /
        2

    )


    return {

        "approved":
            approved,

        "signal":
            final_signal,

        "confidence":
            min(confidence,100),

        "adaptive":
            adaptive,

        "momentum":
            momentum

    }



# ==========================================================
# STRUCTURE EXECUTION GATE V12
# ==========================================================


def structure_execution_gate_v12(df) -> Dict:


    final = structure_final_approval_v12(df)


    return {

        "execute":
            final["approved"],

        "signal":
            final["signal"],

        "confidence":
            final["confidence"],

        "reason":

            "STRUCTURE_APPROVED"

            if final["approved"]

            else

            "STRUCTURE_FILTER_FAILED"

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_structure_execution_v12(df) -> Dict:

    return structure_execution_gate_v12(df)



# ==========================================================
# END PHASE 1 PART P7
# ==========================================================
# ==========================================================
# STRUCTURE REPORTING ENGINE V12
# ==========================================================


def structure_live_report_v12(df) -> Dict:

    execution = structure_execution_gate_v12(df)

    master = structure_master_controller_v12(df)

    memory = institutional_structure_memory_v12(df)


    return {

        "engine":
            "ICT_STRUCTURE_V12",


        "signal":
            execution["signal"],


        "execute":
            execution["execute"],


        "confidence":
            execution["confidence"],


        "reason":
            execution["reason"],


        "structure":

            {

                "event":
                    memory["structure"]["event"],


                "strength":
                    memory["strength"],


                "score":
                    memory["score"]

            },


        "master":
            master

    }



# ==========================================================
# STRUCTURE HEALTH MONITOR V12
# ==========================================================


def structure_health_monitor_v12(df) -> Dict:


    report = structure_live_report_v12(df)


    health = "BAD"


    score = report["confidence"]


    if score >= 80:

        health = "EXCELLENT"


    elif score >= 60:

        health = "GOOD"


    elif score >= 40:

        health = "AVERAGE"



    return {

        "health":
            health,

        "confidence":
            score,

        "execute":
            report["execute"],

        "signal":
            report["signal"]

    }



# ==========================================================
# STRUCTURE ALERT FORMATTER V12
# ==========================================================


def structure_alert_v12(df) -> Dict:


    report = structure_live_report_v12(df)

    signal = report["signal"]


    title = "ICT V12 STRUCTURE"


    message = (

        f"{title} | "

        f"SIGNAL: {signal} | "

        f"CONFIDENCE: {report['confidence']} | "

        f"STATUS: "

        f"{'APPROVED' if report['execute'] else 'WAIT'}"

    )


    return {

        "title":
            title,

        "message":
            message,

        "signal":
            signal,

        "confidence":
            report["confidence"],

        "approved":
            report["execute"]

    }



# ==========================================================
# STRUCTURE API CONTROLLER V12
# ==========================================================


def structure_api_controller_v12(df) -> Dict:


    health = structure_health_monitor_v12(df)

    alert = structure_alert_v12(df)


    return {

        "engine":
            "ICT_STRUCTURE_V12",


        "health":
            health,


        "alert":
            alert

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_structure_report_v12(df) -> Dict:

    return structure_live_report_v12(df)



def get_structure_health_v12(df) -> Dict:

    return structure_health_monitor_v12(df)



def get_structure_alert_v12(df) -> Dict:

    return structure_alert_v12(df)



def get_structure_api_v12(df) -> Dict:

    return structure_api_controller_v12(df)



# ==========================================================
# END PHASE 1 PART P8
# ==========================================================
# ==========================================================
# STRUCTURE EXPORT LAYER V12
# FINAL INTERFACE + DUPLICATE PROTECTION
# ==========================================================


def structure_export_v12(df) -> Dict:

    api = structure_api_controller_v12(df)

    report = structure_live_report_v12(df)

    health = structure_health_monitor_v12(df)


    return {

        "engine":
            "ICT_STRUCTURE_V12",


        "status":
            "ONLINE",


        "signal":

            report["signal"],


        "execute":

            report["execute"],


        "confidence":

            report["confidence"],


        "reason":

            report["reason"],


        "health":

            health["health"],


        "components":

            {

                "structure":
                    report["structure"],


                "master":
                    report["master"]

            },


        "api":

            api

    }



# ==========================================================
# SAFE STRUCTURE CALLER V12
# ==========================================================


def safe_structure_engine_v12(df) -> Dict:


    try:

        result = structure_export_v12(df)


        if not isinstance(
            result,
            dict
        ):

            return {

                "signal":
                    "NO_TRADE",

                "execute":
                    False,

                "confidence":
                    0,

                "error":
                    "INVALID_RESPONSE"

            }


        return result



    except Exception as e:


        return {

            "signal":
                "NO_TRADE",

            "execute":
                False,

            "confidence":
                0,

            "error":
                str(e)

        }



# ==========================================================
# STRUCTURE FINAL OUTPUT FORMAT V12
# ==========================================================


def final_structure_output_v12(df) -> Dict:


    result = safe_structure_engine_v12(df)


    return {

        "engine":
            "ICT_V12_STRUCTURE_FINAL",


        "signal":
            result.get(
                "signal",
                "NO_TRADE"
            ),


        "approved":
            result.get(
                "execute",
                False
            ),


        "confidence":
            result.get(
                "confidence",
                0
            ),


        "reason":
            result.get(
                "reason",
                "NONE"
            ),


        "health":
            result.get(
                "health",
                "UNKNOWN"
            )

    }



# ==========================================================
# MAIN.PY COMPATIBILITY FINAL
# ==========================================================


def get_final_structure_v12(df) -> Dict:

    return final_structure_output_v12(df)



def run_structure_v12(df) -> Dict:

    return final_structure_output_v12(df)



# ==========================================================
# END PHASE 1 PART P9
# ==========================================================
# ==========================================================
# STRUCTURE FINAL CLEANUP LAYER V12
# DUPLICATE PROTECTION + IMPORT COMPATIBILITY
# ==========================================================


def structure_duplicate_guard_v12() -> Dict:

    required_functions = [

        "swing_history_v12",

        "dynamic_swing_high",

        "dynamic_swing_low",

        "internal_structure_break",

        "structure_memory_tracker_v12",

        "structure_master_controller_v12",

        "structure_execution_gate_v12",

        "final_structure_output_v12"

    ]


    missing = []


    current_globals = globals()


    for func in required_functions:

        if func not in current_globals:

            missing.append(func)



    return {

        "valid":
            len(missing) == 0,

        "missing":
            missing,

        "total_checked":
            len(required_functions)

    }



# ==========================================================
# STRUCTURE ENGINE STATUS V12
# ==========================================================


def structure_engine_status_v12(df) -> Dict:


    guard = structure_duplicate_guard_v12()


    if not guard["valid"]:

        return {

            "engine":
                "ICT_STRUCTURE_V12",

            "status":
                "ERROR",

            "missing":
                guard["missing"]

        }



    output = final_structure_output_v12(df)



    return {

        "engine":
            "ICT_STRUCTURE_V12",

        "status":
            "RUNNING",

        "signal":
            output["signal"],

        "approved":
            output["approved"],

        "confidence":
            output["confidence"]

    }



# ==========================================================
# MAIN.PY SAFE ENTRY POINT V12
# ==========================================================


def get_v12_structure_signal(df) -> Dict:


    status = structure_engine_status_v12(df)


    if status["status"] != "RUNNING":

        return {

            "signal":
                "NO_TRADE",

            "confidence":
                0,

            "approved":
                False,

            "error":
                status

        }



    return {

        "signal":
            status["signal"],

        "confidence":
            status["confidence"],

        "approved":
            status["approved"],

        "engine":
            "ICT_STRUCTURE_V12"

    }



# ==========================================================
# STRUCTURE CORE EXPORT MAP V12
# ==========================================================


STRUCTURE_V12_EXPORTS = {

    "swing":
        swing_history_v12,

    "swing_high":
        dynamic_swing_high,

    "swing_low":
        dynamic_swing_low,

    "isb":
        internal_structure_break,

    "memory":
        get_structure_memory_v12,

    "confirmation":
        get_structure_confirmation_v12,

    "execution":
        get_structure_execution_v12,

    "final":
        get_final_structure_v12,

    "signal":
        get_v12_structure_signal

}



# ==========================================================
# END PHASE 1 PART P10
# ==========================================================
