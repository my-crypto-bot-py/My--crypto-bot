import math


# ==========================
# ICT RISK MANAGEMENT V5
# ==========================


# ==========================
# SETTINGS
# ==========================

DEFAULT_RISK_PERCENT = 1.0

MAX_LEVERAGE = 10

MIN_RR = 2.0



# ==========================
# RISK STATE
# ==========================

risk_state = {

    "daily_loss": 0,

    "trades": 0,

    "active_risk": 0

}



# ==========================
# CREATE RISK OBJECT
# ==========================

def create_risk_object(

    balance,

    risk_percent,

    entry,

    sl,

    tp

):

    return {

        "balance": balance,

        "risk_percent": risk_percent,

        "entry": entry,

        "sl": sl,

        "tp": tp

    }



# ==========================
# RISK AMOUNT
# ==========================

def calculate_risk_amount(

    balance,

    risk_percent=DEFAULT_RISK_PERCENT

):

    if balance <= 0:

        return 0


    return round(

        balance

        *

        risk_percent

        /

        100,

        2

    )
    # ==========================
# STOP LOSS DISTANCE
# ==========================

def calculate_sl_distance(

    entry,

    sl

):

    return abs(

        entry

        -

        sl

    )



# ==========================
# REWARD DISTANCE
# ==========================

def calculate_reward_distance(

    entry,

    tp

):

    return abs(

        tp

        -

        entry

    )



# ==========================
# RISK REWARD
# ==========================

def calculate_rr(

    entry,

    sl,

    tp

):

    risk = calculate_sl_distance(

        entry,

        sl

    )


    reward = calculate_reward_distance(

        entry,

        tp

    )


    if risk == 0:

        return 0


    return round(

        reward / risk,

        2

    )



# ==========================
# POSITION SIZE
# ==========================

def calculate_position_size(

    balance,

    entry,

    sl,

    risk_percent=DEFAULT_RISK_PERCENT

):

    risk_amount = calculate_risk_amount(

        balance,

        risk_percent

    )


    sl_distance = calculate_sl_distance(

        entry,

        sl

    )


    if sl_distance == 0:

        return 0


    size = (

        risk_amount

        /

        sl_distance

    )


    return round(

        size,

        4

    )
    # ==========================
# LEVERAGE SAFETY CHECK
# ==========================

def validate_leverage(

    leverage

):

    if leverage <= 0:

        return False


    if leverage > MAX_LEVERAGE:

        return False


    return True



# ==========================
# MARGIN CALCULATION
# ==========================

def calculate_margin(

    position_size,

    leverage

):

    if not validate_leverage(

        leverage

    ):

        return 0


    if leverage == 0:

        return 0


    margin = (

        position_size

        /

        leverage

    )


    return round(

        margin,

        4

    )



# ==========================
# LIQUIDATION RISK
# ==========================

def liquidation_risk(

    entry,

    sl,

    leverage

):

    distance = calculate_sl_distance(

        entry,

        sl

    )


    if distance == 0:

        return {

            "risk":

            "HIGH"

        }


    if leverage >= 5:

        return {

            "risk":

            "HIGH"

        }


    return {

        "risk":

        "NORMAL"

    }
    # ==========================
# TRADE RISK VALIDATION
# ==========================

def validate_trade_risk(

    entry,

    sl,

    tp

):

    rr = calculate_rr(

        entry,

        sl,

        tp

    )


    if rr < MIN_RR:

        return {

            "valid":

            False,

            "reason":

            "Low Risk Reward"

        }


    return {

        "valid":

        True,

        "rr":

        rr

    }



# ==========================
# CAPITAL PROTECTION
# ==========================

def check_capital_protection(

    balance,

    risk_percent

):

    if balance <= 0:

        return False


    if risk_percent > 2:

        return False


    return True



# ==========================
# DAILY LOSS CHECK
# ==========================

def check_daily_loss():

    if risk_state["daily_loss"] > 0:

        return True


    return False
    # ==========================
# FINAL RISK ANALYZER
# ==========================

def analyze_risk(

    balance,

    entry,

    sl,

    tp,

    leverage=1,

    risk_percent=DEFAULT_RISK_PERCENT

):

    rr = calculate_rr(

        entry,

        sl,

        tp

    )


    position_size = calculate_position_size(

        balance,

        entry,

        sl,

        risk_percent

    )


    margin = calculate_margin(

        position_size,

        leverage

    )


    liquidation = liquidation_risk(

        entry,

        sl,

        leverage

    )


    trade_check = validate_trade_risk(

        entry,

        sl,

        tp

    )


    return {

        "rr":

        rr,

        "position_size":

        position_size,

        "margin":

        margin,

        "liquidation":

        liquidation,

        "trade_valid":

        trade_check["valid"]

    }



# ==========================
# RISK SCORE
# ==========================

def risk_score(

    result

):

    score = 100


    if result["rr"] < MIN_RR:

        score -= 30


    if result["liquidation"]["risk"] == "HIGH":

        score -= 30


    if not result["trade_valid"]:

        score -= 40


    if score < 0:

        score = 0


    return score
    # ==========================
# RISK + CONFIDENCE FILTER
# ==========================

def risk_confidence_filter(

    confidence,

    risk_result

):

    if risk_result is None:

        return False


    if confidence < 85:

        return False


    if not risk_result["trade_valid"]:

        return False


    if risk_result["liquidation"]["risk"] == "HIGH":

        return False


    return True



# ==========================
# FINAL TRADE PERMISSION
# ==========================

def trade_permission(

    confidence,

    balance,

    entry,

    sl,

    tp,

    leverage=1

):

    risk_result = analyze_risk(

        balance,

        entry,

        sl,

        tp,

        leverage

    )


    allowed = risk_confidence_filter(

        confidence,

        risk_result

    )


    return {

        "allowed":

        allowed,

        "confidence":

        confidence,

        "risk":

        risk_result

    }



# ==========================
# ACTIVE RISK UPDATE
# ==========================

def update_active_risk(

    amount

):

    risk_state["active_risk"] = amount


    return risk_state
    # ==========================
# DYNAMIC RISK MANAGEMENT
# ==========================

def adjust_risk_by_confidence(

    confidence

):

    if confidence >= 95:

        return 2.0


    if confidence >= 85:

        return 1.0


    if confidence >= 75:

        return 0.5


    return 0



# ==========================
# DYNAMIC POSITION SIZE
# ==========================

def dynamic_position_size(

    balance,

    entry,

    sl,

    confidence

):

    risk_percent = adjust_risk_by_confidence(

        confidence

    )


    if risk_percent == 0:

        return 0


    return calculate_position_size(

        balance,

        entry,

        sl,

        risk_percent

    )



# ==========================
# RISK STATUS
# ==========================

def risk_status():

    return {

        "daily_loss":

        risk_state["daily_loss"],

        "trades":

        risk_state["trades"],

        "active_risk":

        risk_state["active_risk"]

    }
    # ==========================
# DAILY RISK LIMIT
# ==========================

MAX_DAILY_LOSS = 3.0



def update_daily_loss(

    loss_percent

):

    risk_state["daily_loss"] += loss_percent


    return risk_state["daily_loss"]



# ==========================
# DAILY LOSS PROTECTION
# ==========================

def daily_loss_protection():

    if (

        risk_state["daily_loss"]

        >=

        MAX_DAILY_LOSS

    ):

        return False


    return True



# ==========================
# TRADE COUNTER
# ==========================

def register_trade():

    risk_state["trades"] += 1


    return risk_state["trades"]



# ==========================
# RESET DAILY RISK
# ==========================

def reset_daily_risk():

    risk_state["daily_loss"] = 0

    risk_state["trades"] = 0


    return True
    # ==========================
# RISK DEBUG PANEL
# ==========================

def debug_risk(

    result=None

):

    print("\n========== RISK V5 ==========")


    if result:

        print(

            "RR :",

            result.get("rr")

        )

        print(

            "Position Size :",

            result.get("position_size")

        )

        print(

            "Margin :",

            result.get("margin")

        )

        print(

            "Liquidation :",

            result.get("liquidation")

        )


    print(

        "State :",

        risk_state

    )


    print(

        "=============================\n"

    )


    return risk_state



# ==========================
# RISK REPORT
# ==========================

def risk_report(

    balance,

    entry,

    sl,

    tp,

    leverage=1

):

    result = analyze_risk(

        balance,

        entry,

        sl,

        tp,

        leverage

    )


    return {

        "risk_score":

        risk_score(result),

        "rr":

        result["rr"],

        "position_size":

        result["position_size"],

        "safe":

        result["trade_valid"]

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def risk_engine_v5(

    balance,

    entry,

    sl,

    tp,

    leverage=1,

    confidence=0

):

    risk_result = analyze_risk(

        balance,

        entry,

        sl,

        tp,

        leverage

    )


    permission = trade_permission(

        confidence,

        balance,

        entry,

        sl,

        tp,

        leverage

    )


    return {

        "risk":

        risk_result,

        "permission":

        permission["allowed"],

        "risk_score":

        risk_score(risk_result)

    }



# ==========================
# FINAL RISK CHECK
# ==========================

def final_risk_check(

    balance,

    entry,

    sl,

    tp,

    leverage,

    confidence

):

    result = risk_engine_v5(

        balance,

        entry,

        sl,

        tp,

        leverage,

        confidence

    )


    return (

        result["permission"]

    )



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "calculate_risk_amount",

    "calculate_position_size",

    "calculate_rr",

    "validate_leverage",

    "calculate_margin",

    "analyze_risk",

    "risk_score",

    "trade_permission",

    "dynamic_position_size",

    "daily_loss_protection",

    "risk_engine_v5",

    "final_risk_check",

    "risk_report",

    "debug_risk",

    "reset_daily_risk"

]
