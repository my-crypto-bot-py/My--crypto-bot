# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D1
# BASE RISK MANAGEMENT CORE ENGINE
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# RISK MEMORY V12
# ==========================================================

V12_RISK_MEMORY = []

MAX_RISK_HISTORY = 200



# ==========================================================
# RISK CONFIGURATION V12
# ==========================================================

RISK_CONFIG_V12 = {


    "default_risk_percent":

        1.0,


    "max_risk_percent":

        2.0,


    "min_risk_percent":

        0.25,


    "max_daily_loss":

        5.0

}



# ==========================================================
# RISK SCORE LIMITER V12
# ==========================================================


def normalize_risk_percent_v12(
    risk: float
) -> float:


    if risk < RISK_CONFIG_V12["min_risk_percent"]:

        return RISK_CONFIG_V12["min_risk_percent"]



    if risk > RISK_CONFIG_V12["max_risk_percent"]:

        return RISK_CONFIG_V12["max_risk_percent"]



    return round(
        risk,
        2
    )



# ==========================================================
# ACCOUNT RISK INPUT VALIDATOR V12
# ==========================================================


def validate_account_data_v12(
    account: Dict
) -> Dict:


    required = [

        "balance",

        "risk_percent"

    ]


    missing = []



    for key in required:


        if key not in account:

            missing.append(key)



    return {


        "valid":

            len(missing) == 0,


        "missing":

            missing

    }



# ==========================================================
# BASE RISK CALCULATOR V12
# ==========================================================


def calculate_base_risk_v12(
    account_balance: float,
    risk_percent: float
) -> Dict:


    risk_percent = normalize_risk_percent_v12(
        risk_percent
    )


    risk_amount = (

        account_balance

        *

        risk_percent

        /

        100

    )



    return {


        "balance":

            account_balance,


        "risk_percent":

            risk_percent,


        "risk_amount":

            round(
                risk_amount,
                2
            )

    }



# ==========================================================
# POSITION SIZE BASE ENGINE V12
# ==========================================================


def calculate_position_size_v12(
    risk_amount: float,
    entry: float,
    stop_loss: float
) -> Dict:


    distance = abs(

        entry

        -

        stop_loss

    )



    if distance == 0:


        return {


            "position_size":

                0,


            "error":

                "INVALID_SL"

        }



    size = (

        risk_amount

        /

        distance

    )



    return {


        "entry":

            entry,


        "stop_loss":

            stop_loss,


        "risk_distance":

            distance,


        "position_size":

            round(
                size,
                4
            )

    }



# ==========================================================
# BASE RISK ENGINE V12
# ==========================================================


def base_risk_engine_v12(
    account: Dict,
    trade: Dict
) -> Dict:


    try:


        validation = validate_account_data_v12(
            account
        )



        if not validation["valid"]:


            return {


                "engine":

                    "ICT_BASE_RISK_V12",


                "status":

                    "ERROR",


                "missing":

                    validation["missing"]

            }



        risk = calculate_base_risk_v12(

            account["balance"],

            account["risk_percent"]

        )



        position = calculate_position_size_v12(

            risk["risk_amount"],

            trade.get(
                "entry",
                0
            ),

            trade.get(
                "stop_loss",
                0
            )

        )



        result = {


            "engine":

                "ICT_BASE_RISK_V12",


            "status":

                "ONLINE",


            "risk":

                risk,


            "position":

                position

        }



        V12_RISK_MEMORY.append(
            result
        )



        if len(
            V12_RISK_MEMORY
        ) > MAX_RISK_HISTORY:


            del V12_RISK_MEMORY[
                :-
                MAX_RISK_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_BASE_RISK_V12",


            "status":

                "ERROR",


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_base_risk_v12(
    account: Dict,
    trade: Dict
) -> Dict:


    return base_risk_engine_v12(
        account,
        trade
    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D1
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D2
# ADVANCED RISK ADAPTATION ENGINE
# CONFIDENCE + VOLATILITY BASED RISK OPTIMIZER
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# ADVANCED RISK MEMORY V12
# ==========================================================

V12_ADVANCED_RISK_MEMORY = []

MAX_ADVANCED_RISK_HISTORY = 200



# ==========================================================
# ADVANCED RISK CONFIGURATION V12
# ==========================================================

ADVANCED_RISK_CONFIG_V12 = {


    "high_confidence_risk":

        1.5,


    "medium_confidence_risk":

        1.0,


    "low_confidence_risk":

        0.5,


    "high_volatility_reduce":

        0.5,


    "low_volatility_boost":

        0.25

}



# ==========================================================
# CONFIDENCE BASED RISK ADJUSTER V12
# ==========================================================


def confidence_risk_adjustment_v12(
    confidence: int
) -> float:


    if confidence >= 90:


        return ADVANCED_RISK_CONFIG_V12[
            "high_confidence_risk"
        ]



    elif confidence >= 70:


        return ADVANCED_RISK_CONFIG_V12[
            "medium_confidence_risk"
        ]



    return ADVANCED_RISK_CONFIG_V12[
        "low_confidence_risk"
    ]



# ==========================================================
# VOLATILITY RISK ADJUSTER V12
# ==========================================================


def volatility_risk_adjustment_v12(
    volatility: str,
    risk_percent: float
) -> float:



    if volatility == "HIGH":


        risk_percent -= ADVANCED_RISK_CONFIG_V12[
            "high_volatility_reduce"
        ]



    elif volatility == "LOW":


        risk_percent += ADVANCED_RISK_CONFIG_V12[
            "low_volatility_boost"
        ]



    return normalize_risk_percent_v12(
        risk_percent
    )



# ==========================================================
# MARKET CONDITION RISK FILTER V12
# ==========================================================


def market_condition_risk_filter_v12(
    market: Dict,
    risk_percent: float
) -> Dict:



    condition = market.get(
        "condition",
        "UNKNOWN"
    )


    volatility = market.get(
        "volatility",
        "NORMAL"
    )



    adjusted = volatility_risk_adjustment_v12(
        volatility,
        risk_percent
    )



    if condition == "SIDEWAYS":


        adjusted = min(
            adjusted,
            0.75
        )



    return {


        "original_risk":

            risk_percent,


        "adjusted_risk":

            adjusted,


        "condition":

            condition,


        "volatility":

            volatility

    }



# ==========================================================
# ADVANCED RISK CALCULATOR V12
# ==========================================================


def calculate_advanced_risk_v12(
    confidence: int,
    market: Dict
) -> Dict:



    base_risk = confidence_risk_adjustment_v12(
        confidence
    )



    market_adjustment = market_condition_risk_filter_v12(
        market,
        base_risk
    )



    final_risk = normalize_risk_percent_v12(
        market_adjustment["adjusted_risk"]
    )



    return {


        "confidence":

            confidence,


        "base_risk":

            base_risk,


        "final_risk_percent":

            final_risk,


        "market":

            market_adjustment

    }



# ==========================================================
# ADVANCED POSITION SIZE ENGINE V12
# ==========================================================


def advanced_position_size_v12(
    balance: float,
    risk_percent: float,
    entry: float,
    stop_loss: float
) -> Dict:



    risk_amount = (

        balance

        *

        risk_percent

        /

        100

    )



    position = calculate_position_size_v12(
        risk_amount,
        entry,
        stop_loss
    )



    return {


        "risk_amount":

            round(
                risk_amount,
                2
            ),


        "position":

            position

    }



# ==========================================================
# ADVANCED RISK ENGINE V12
# ==========================================================


def advanced_risk_engine_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict
) -> Dict:


    try:


        confidence_score = confidence.get(
            "confidence",
            0
        )


        risk = calculate_advanced_risk_v12(
            confidence_score,
            market
        )



        position = advanced_position_size_v12(

            account.get(
                "balance",
                0
            ),

            risk["final_risk_percent"],

            trade.get(
                "entry",
                0
            ),

            trade.get(
                "stop_loss",
                0
            )

        )



        result = {


            "engine":

                "ICT_ADVANCED_RISK_V12",


            "status":

                "ONLINE",


            "risk":

                risk,


            "position":

                position

        }



        V12_ADVANCED_RISK_MEMORY.append(
            result
        )



        if len(
            V12_ADVANCED_RISK_MEMORY
        ) > MAX_ADVANCED_RISK_HISTORY:


            del V12_ADVANCED_RISK_MEMORY[
                :-
                MAX_ADVANCED_RISK_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_ADVANCED_RISK_V12",


            "status":

                "ERROR",


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_advanced_risk_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict
) -> Dict:


    return advanced_risk_engine_v12(
        account,
        trade,
        confidence,
        market
    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D2
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D3
# DYNAMIC DRAWDOWN + DAILY LOSS PROTECTION ENGINE
# ACCOUNT SAFETY CONTROL SYSTEM
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# DRAWDOWN MEMORY V12
# ==========================================================

V12_DRAWDOWN_MEMORY = []

MAX_DRAWDOWN_HISTORY = 200



# ==========================================================
# DRAWDOWN CONFIGURATION V12
# ==========================================================

DRAWDOWN_CONFIG_V12 = {


    "max_daily_loss_percent":

        5.0,


    "max_total_drawdown_percent":

        15.0,


    "warning_drawdown_percent":

        10.0,


    "safe_risk_reduce":

        50

}



# ==========================================================
# DAILY LOSS CALCULATOR V12
# ==========================================================


def calculate_daily_loss_v12(
    starting_balance: float,
    current_balance: float
) -> Dict:


    if starting_balance <= 0:


        return {


            "loss_percent":

                100,


            "loss_amount":

                0

        }



    loss_amount = (

        starting_balance

        -

        current_balance

    )



    loss_percent = (

        loss_amount

        /

        starting_balance

    ) * 100



    return {


        "loss_amount":

            round(
                loss_amount,
                2
            ),


        "loss_percent":

            round(
                loss_percent,
                2
            )

    }



# ==========================================================
# DRAWDOWN STATUS CHECK V12
# ==========================================================


def check_drawdown_status_v12(
    drawdown_percent: float
) -> Dict:


    status = "NORMAL"

    risk_multiplier = 1.0



    if drawdown_percent >= DRAWDOWN_CONFIG_V12[
        "max_total_drawdown_percent"
    ]:


        status = "ACCOUNT_LOCK"


        risk_multiplier = 0



    elif drawdown_percent >= DRAWDOWN_CONFIG_V12[
        "warning_drawdown_percent"
    ]:


        status = "WARNING"


        risk_multiplier = (

            DRAWDOWN_CONFIG_V12[
                "safe_risk_reduce"
            ]

            /

            100

        )



    return {


        "status":

            status,


        "risk_multiplier":

            risk_multiplier

    }



# ==========================================================
# RISK REDUCTION ENGINE V12
# ==========================================================


def apply_drawdown_risk_control_v12(
    risk_percent: float,
    drawdown_status: Dict
) -> float:



    multiplier = drawdown_status.get(
        "risk_multiplier",
        1.0
    )



    adjusted = (

        risk_percent

        *

        multiplier

    )



    if adjusted == 0:


        return 0



    return normalize_risk_percent_v12(
        adjusted
    )



# ==========================================================
# EQUITY PROTECTION ENGINE V12
# ==========================================================


def equity_protection_engine_v12(
    account: Dict,
    risk_percent: float
) -> Dict:


    starting_balance = account.get(
        "starting_balance",
        account.get(
            "balance",
            0
        )
    )


    current_balance = account.get(
        "balance",
        0
    )



    loss = calculate_daily_loss_v12(
        starting_balance,
        current_balance
    )



    protection = check_drawdown_status_v12(
        loss["loss_percent"]
    )



    final_risk = apply_drawdown_risk_control_v12(
        risk_percent,
        protection
    )



    return {


        "drawdown":

            loss,


        "protection":

            protection,


        "final_risk":

            final_risk

    }



# ==========================================================
# TRADE SAFETY VALIDATOR V12
# ==========================================================


def trade_safety_validator_v12(
    protection: Dict
) -> Dict:


    status = protection.get(
        "status",
        "NORMAL"
    )



    if status == "ACCOUNT_LOCK":


        return {


            "allowed":

                False,


            "reason":

                "MAX_DRAWDOWN_REACHED"

        }



    return {


        "allowed":

            True,


        "reason":

            "RISK_ALLOWED"

    }



# ==========================================================
# DRAWDOWN RISK ENGINE V12
# ==========================================================


def drawdown_risk_engine_v12(
    account: Dict,
    risk_percent: float
) -> Dict:


    try:


        equity = equity_protection_engine_v12(
            account,
            risk_percent
        )



        safety = trade_safety_validator_v12(
            equity["protection"]
        )



        result = {


            "engine":

                "ICT_DRAWDOWN_RISK_V12",


            "status":

                "ONLINE",


            "equity":

                equity,


            "trade_allowed":

                safety["allowed"],


            "reason":

                safety["reason"]

        }



        V12_DRAWDOWN_MEMORY.append(
            result
        )



        if len(
            V12_DRAWDOWN_MEMORY
        ) > MAX_DRAWDOWN_HISTORY:


            del V12_DRAWDOWN_MEMORY[
                :-
                MAX_DRAWDOWN_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_DRAWDOWN_RISK_V12",


            "status":

                "ERROR",


            "trade_allowed":

                False,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_drawdown_risk_v12(
    account: Dict,
    risk_percent: float
) -> Dict:


    return drawdown_risk_engine_v12(
        account,
        risk_percent
    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D3
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D4
# TRADE RISK VALIDATION + POSITION PROTECTION ENGINE
# STOP LOSS + TAKE PROFIT SAFETY CONTROLLER
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# TRADE PROTECTION MEMORY V12
# ==========================================================

V12_TRADE_PROTECTION_MEMORY = []

MAX_TRADE_PROTECTION_HISTORY = 200



# ==========================================================
# TRADE PROTECTION CONFIG V12
# ==========================================================

TRADE_PROTECTION_CONFIG_V12 = {


    "minimum_rr":

        2.0,


    "maximum_risk_distance_percent":

        5.0,


    "minimum_stop_distance":

        0.1,


    "max_position_exposure":

        10.0

}



# ==========================================================
# STOP LOSS VALIDATOR V12
# ==========================================================


def validate_stop_loss_v12(
    entry: float,
    stop_loss: float
) -> Dict:


    distance = abs(

        entry

        -

        stop_loss

    )



    if distance <= TRADE_PROTECTION_CONFIG_V12[
        "minimum_stop_distance"
    ]:


        return {


            "valid":

                False,


            "reason":

                "INVALID_STOP_DISTANCE"

        }



    return {


        "valid":

            True,


        "distance":

            distance

    }



# ==========================================================
# TAKE PROFIT VALIDATOR V12
# ==========================================================


def validate_take_profit_v12(
    entry: float,
    stop_loss: float,
    take_profit: float
) -> Dict:


    risk = abs(

        entry

        -

        stop_loss

    )


    reward = abs(

        take_profit

        -

        entry

    )



    if risk == 0:


        return {


            "valid":

                False,


            "reason":

                "ZERO_RISK"

        }



    rr = reward / risk



    return {


        "valid":

            rr >= TRADE_PROTECTION_CONFIG_V12[
                "minimum_rr"
            ],


        "rr":

            round(
                rr,
                2
            )

    }



# ==========================================================
# POSITION EXPOSURE CHECK V12
# ==========================================================


def check_position_exposure_v12(
    position_value: float,
    balance: float
) -> Dict:


    if balance <= 0:


        return {


            "allowed":

                False,


            "exposure":

                100

        }



    exposure = (

        position_value

        /

        balance

    ) * 100



    return {


        "allowed":

            exposure <= TRADE_PROTECTION_CONFIG_V12[
                "max_position_exposure"
            ],


        "exposure":

            round(
                exposure,
                2
            )

    }



# ==========================================================
# TRADE SAFETY CHECK ENGINE V12
# ==========================================================


def trade_protection_engine_v12(
    trade: Dict
) -> Dict:


    try:


        entry = trade.get(
            "entry",
            0
        )


        stop_loss = trade.get(
            "stop_loss",
            0
        )


        take_profit = trade.get(
            "take_profit",
            0
        )



        stop_check = validate_stop_loss_v12(
            entry,
            stop_loss
        )



        if not stop_check["valid"]:


            return {


                "engine":

                    "ICT_TRADE_PROTECTION_V12",


                "approved":

                    False,


                "reason":

                    stop_check["reason"]

            }



        tp_check = validate_take_profit_v12(
            entry,
            stop_loss,
            take_profit
        )



        approved = tp_check["valid"]



        result = {


            "engine":

                "ICT_TRADE_PROTECTION_V12",


            "status":

                "ONLINE",


            "approved":

                approved,


            "risk_distance":

                stop_check.get(
                    "distance",
                    0
                ),


            "risk_reward":

                tp_check.get(
                    "rr",
                    0
                ),


            "reason":

                (
                    "TRADE_SAFE"
                    if approved
                    else
                    "LOW_RR"
                )

        }



        V12_TRADE_PROTECTION_MEMORY.append(
            result
        )



        if len(
            V12_TRADE_PROTECTION_MEMORY
        ) > MAX_TRADE_PROTECTION_HISTORY:


            del V12_TRADE_PROTECTION_MEMORY[
                :-
                MAX_TRADE_PROTECTION_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_TRADE_PROTECTION_V12",


            "approved":

                False,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_trade_protection_v12(
    trade: Dict
) -> Dict:


    return trade_protection_engine_v12(
        trade
    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D4
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D5
# SMART RISK ALLOCATION + CONFIDENCE FUSION ENGINE
# CONFIDENCE + MARKET + ACCOUNT BASED RISK OPTIMIZER
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# SMART RISK MEMORY V12
# ==========================================================

V12_SMART_RISK_MEMORY = []

MAX_SMART_RISK_HISTORY = 200



# ==========================================================
# SMART RISK CONFIGURATION V12
# ==========================================================

SMART_RISK_CONFIG_V12 = {


    "elite_confidence":

        90,


    "strong_confidence":

        85,


    "minimum_confidence":

        70,


    "elite_risk":

        2.0,


    "strong_risk":

        1.5,


    "normal_risk":

        1.0,


    "weak_risk":

        0.5

}



# ==========================================================
# CONFIDENCE RISK MAPPER V12
# ==========================================================


def map_confidence_to_risk_v12(
    confidence: int
) -> float:


    if confidence >= SMART_RISK_CONFIG_V12[
        "elite_confidence"
    ]:


        return SMART_RISK_CONFIG_V12[
            "elite_risk"
        ]



    elif confidence >= SMART_RISK_CONFIG_V12[
        "strong_confidence"
    ]:


        return SMART_RISK_CONFIG_V12[
            "strong_risk"
        ]



    elif confidence >= SMART_RISK_CONFIG_V12[
        "minimum_confidence"
    ]:


        return SMART_RISK_CONFIG_V12[
            "normal_risk"
        ]



    return SMART_RISK_CONFIG_V12[
        "weak_risk"
    ]



# ==========================================================
# MARKET RISK ADJUSTER V12
# ==========================================================


def smart_market_risk_adjustment_v12(
    risk_percent: float,
    market: Dict
) -> Dict:


    volatility = market.get(
        "volatility",
        "NORMAL"
    )


    condition = market.get(
        "condition",
        "UNKNOWN"
    )


    adjusted = risk_percent



    if volatility == "HIGH":


        adjusted -= 0.5



    elif volatility == "LOW":


        adjusted += 0.25



    if condition == "SIDEWAYS":


        adjusted = min(
            adjusted,
            0.75
        )



    adjusted = normalize_risk_percent_v12(
        adjusted
    )



    return {


        "original":

            risk_percent,


        "adjusted":

            adjusted,


        "volatility":

            volatility,


        "condition":

            condition

    }



# ==========================================================
# ACCOUNT SAFETY RISK REDUCER V12
# ==========================================================


def account_safety_risk_adjustment_v12(
    risk_percent: float,
    drawdown: Dict
) -> Dict:


    status = drawdown.get(
        "status",
        "NORMAL"
    )


    final = risk_percent



    if status == "WARNING":


        final *= 0.5



    elif status == "ACCOUNT_LOCK":


        final = 0



    final = normalize_risk_percent_v12(
        final
    )



    return {


        "risk":

            final,


        "status":

            status

    }



# ==========================================================
# SMART POSITION RISK CALCULATOR V12
# ==========================================================


def calculate_smart_position_risk_v12(
    balance: float,
    risk_percent: float,
    entry: float,
    stop_loss: float
) -> Dict:



    risk_amount = (

        balance

        *

        risk_percent

        /

        100

    )



    position = calculate_position_size_v12(
        risk_amount,
        entry,
        stop_loss
    )



    return {


        "risk_amount":

            round(
                risk_amount,
                2
            ),


        "position":

            position

    }



# ==========================================================
# SMART RISK ENGINE V12
# ==========================================================


def smart_risk_engine_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    try:


        confidence_score = confidence.get(
            "confidence",
            0
        )



        base_risk = map_confidence_to_risk_v12(
            confidence_score
        )



        market_risk = smart_market_risk_adjustment_v12(
            base_risk,
            market
        )



        account_risk = account_safety_risk_adjustment_v12(
            market_risk["adjusted"],
            drawdown
        )



        position = calculate_smart_position_risk_v12(

            account.get(
                "balance",
                0
            ),

            account_risk["risk"],

            trade.get(
                "entry",
                0
            ),

            trade.get(
                "stop_loss",
                0
            )

        )



        result = {


            "engine":

                "ICT_SMART_RISK_V12",


            "status":

                "ONLINE",


            "confidence":

                confidence_score,


            "risk_percent":

                account_risk["risk"],


            "market":

                market_risk,


            "account":

                account_risk,


            "position":

                position

        }



        V12_SMART_RISK_MEMORY.append(
            result
        )



        if len(
            V12_SMART_RISK_MEMORY
        ) > MAX_SMART_RISK_HISTORY:


            del V12_SMART_RISK_MEMORY[
                :-
                MAX_SMART_RISK_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_SMART_RISK_V12",


            "status":

                "ERROR",


            "risk_percent":

                0,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_smart_risk_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    return smart_risk_engine_v12(
        account,
        trade,
        confidence,
        market,
        drawdown
    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D5
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D6
# FINAL RISK DECISION CONTROLLER + TRADE APPROVAL GATE
# SMART RISK + CONFIDENCE + DRAWDOWN FUSION
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# FINAL RISK DECISION MEMORY V12
# ==========================================================

V12_FINAL_RISK_MEMORY = []

MAX_FINAL_RISK_HISTORY = 200



# ==========================================================
# FINAL RISK CONFIGURATION V12
# ==========================================================

FINAL_RISK_RULES_V12 = {


    "minimum_confidence":

        70,


    "maximum_risk":

        2.0,


    "blocked_risk":

        0,


    "minimum_rr":

        2.0

}



# ==========================================================
# CONFIDENCE RISK VALIDATOR V12
# ==========================================================


def validate_risk_confidence_v12(
    confidence: Dict
) -> Dict:


    score = confidence.get(
        "confidence",
        0
    )


    if score < FINAL_RISK_RULES_V12[
        "minimum_confidence"
    ]:


        return {


            "allowed":

                False,


            "reason":

                "LOW_CONFIDENCE"

        }



    return {


        "allowed":

            True,


        "reason":

            "CONFIDENCE_OK"

    }



# ==========================================================
# RISK PERCENT VALIDATOR V12
# ==========================================================


def validate_risk_percent_v12(
    risk_percent: float
) -> Dict:


    if risk_percent <= FINAL_RISK_RULES_V12[
        "blocked_risk"
    ]:


        return {


            "valid":

                False,


            "reason":

                "RISK_BLOCKED"

        }



    if risk_percent > FINAL_RISK_RULES_V12[
        "maximum_risk"
    ]:


        return {


            "valid":

                False,


            "reason":

                "RISK_TOO_HIGH"

        }



    return {


        "valid":

            True,


        "reason":

            "RISK_ACCEPTED"

    }



# ==========================================================
# RR VALIDATOR V12
# ==========================================================


def validate_final_rr_v12(
    trade: Dict
) -> Dict:


    entry = trade.get(
        "entry",
        0
    )


    stop_loss = trade.get(
        "stop_loss",
        0
    )


    take_profit = trade.get(
        "take_profit",
        0
    )



    risk = abs(

        entry

        -

        stop_loss

    )


    reward = abs(

        take_profit

        -

        entry

    )



    if risk == 0:


        return {


            "valid":

                False,


            "rr":

                0,


            "reason":

                "INVALID_SL"

        }



    rr = reward / risk



    return {


        "valid":

            rr >= FINAL_RISK_RULES_V12[
                "minimum_rr"
            ],


        "rr":

            round(
                rr,
                2
            ),


        "reason":

            (
                "RR_OK"
                if rr >= FINAL_RISK_RULES_V12["minimum_rr"]
                else
                "LOW_RR"
            )

    }



# ==========================================================
# FINAL TRADE APPROVAL GATE V12
# ==========================================================


def final_trade_approval_gate_v12(
    risk: Dict,
    confidence: Dict,
    trade: Dict
) -> Dict:



    confidence_check = validate_risk_confidence_v12(
        confidence
    )


    risk_check = validate_risk_percent_v12(
        risk.get(
            "risk_percent",
            0
        )
    )


    rr_check = validate_final_rr_v12(
        trade
    )



    approved = (

        confidence_check["allowed"]

        and

        risk_check["valid"]

        and

        rr_check["valid"]

    )



    return {


        "approved":

            approved,


        "reason":

            (
                "TRADE_APPROVED"
                if approved
                else
                "TRADE_BLOCKED"
            ),


        "confidence":

            confidence_check,


        "risk":

            risk_check,


        "rr":

            rr_check

    }



# ==========================================================
# FINAL RISK DECISION ENGINE V12
# ==========================================================


def final_risk_decision_engine_v12(
    smart_risk: Dict,
    confidence: Dict,
    trade: Dict
) -> Dict:


    try:


        gate = final_trade_approval_gate_v12(

            smart_risk,

            confidence,

            trade

        )



        result = {


            "engine":

                "ICT_FINAL_RISK_DECISION_V12",


            "status":

                "ONLINE",


            "approved":

                gate["approved"],


            "risk_percent":

                smart_risk.get(
                    "risk_percent",
                    0
                ),


            "confidence":

                confidence.get(
                    "confidence",
                    0
                ),


            "reason":

                gate["reason"],


            "validation":

                gate

        }



        V12_FINAL_RISK_MEMORY.append(
            result
        )



        if len(
            V12_FINAL_RISK_MEMORY
        ) > MAX_FINAL_RISK_HISTORY:


            del V12_FINAL_RISK_MEMORY[
                :-
                MAX_FINAL_RISK_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_FINAL_RISK_DECISION_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "risk_percent":

                0,


            "error":

                str(e)

        }



# ==========================================================
# SAFE FINAL RISK CONTROLLER V12
# ==========================================================


def execute_final_risk_v12(
    smart_risk: Dict,
    confidence: Dict,
    trade: Dict
) -> Dict:


    try:


        return final_risk_decision_engine_v12(
            smart_risk,
            confidence,
            trade
        )


    except Exception as e:


        return {


            "engine":

                "ICT_FINAL_RISK_DECISION_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "risk_percent":

                0,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL RISK ENTRY V12
# ==========================================================


def get_final_risk_v12(
    smart_risk: Dict,
    confidence: Dict,
    trade: Dict
) -> Dict:


    return execute_final_risk_v12(
        smart_risk,
        confidence,
        trade
    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D6
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D7
# RISK MASTER PIPELINE ORCHESTRATOR
# CONFIDENCE + SMART RISK + FINAL APPROVAL FUSION
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# RISK MASTER PIPELINE MEMORY V12
# ==========================================================

V12_RISK_PIPELINE_MEMORY = []

MAX_RISK_PIPELINE_HISTORY = 200



# ==========================================================
# RISK PIPELINE VALIDATOR V12
# ==========================================================


def validate_risk_pipeline_input_v12(
    data: Dict
) -> Dict:


    required = [

        "risk_percent",

        "approved"

    ]


    missing = []



    for key in required:


        if key not in data:

            missing.append(key)



    return {


        "valid":

            len(missing) == 0,


        "missing":

            missing

    }



# ==========================================================
# MASTER RISK FUSION ENGINE V12
# ==========================================================


def master_risk_pipeline_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    try:


        base = get_base_risk_v12(
            account,
            trade
        )



        advanced = get_advanced_risk_v12(

            account,

            trade,

            confidence,

            market

        )



        drawdown_result = get_drawdown_risk_v12(

            account,

            advanced.get(
                "risk",
                {}).get(
                    "final_risk_percent",
                    0
                )

        )



        smart = get_smart_risk_v12(

            account,

            trade,

            confidence,

            market,

            drawdown_result.get(
                "equity",
                {}
            )

        )



        final = get_final_risk_v12(

            smart,

            confidence,

            trade

        )



        result = {


            "engine":

                "ICT_MASTER_RISK_PIPELINE_V12",


            "status":

                "ONLINE",


            "approved":

                final.get(
                    "approved",
                    False
                ),


            "risk_percent":

                final.get(
                    "risk_percent",
                    0
                ),


            "confidence":

                final.get(
                    "confidence",
                    0
                ),


            "base":

                base,


            "advanced":

                advanced,


            "drawdown":

                drawdown_result,


            "smart":

                smart,


            "final":

                final

        }



        V12_RISK_PIPELINE_MEMORY.append(
            result
        )



        if len(
            V12_RISK_PIPELINE_MEMORY
        ) > MAX_RISK_PIPELINE_HISTORY:


            del V12_RISK_PIPELINE_MEMORY[
                :-
                MAX_RISK_PIPELINE_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_MASTER_RISK_PIPELINE_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "risk_percent":

                0,


            "error":

                str(e)

        }



# ==========================================================
# SAFE MASTER RISK EXECUTOR V12
# ==========================================================


def safe_master_risk_pipeline_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    try:


        return master_risk_pipeline_v12(

            account,

            trade,

            confidence,

            market,

            drawdown

        )


    except Exception as e:


        return {


            "engine":

                "ICT_MASTER_RISK_PIPELINE_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "risk_percent":

                0,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL RISK ENGINE ENTRY V12
# ==========================================================


def run_risk_engine_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    return safe_master_risk_pipeline_v12(

        account,

        trade,

        confidence,

        market,

        drawdown

    )



# ==========================================================
# RISK ENGINE HEALTH CHECK V12
# ==========================================================


def risk_engine_health_v12() -> Dict:


    return {


        "engine":

            "ICT_RISK_ENGINE_V12",


        "status":

            "ONLINE",


        "phase":

            "PHASE_4_D7",


        "memory":

            len(
                V12_RISK_PIPELINE_MEMORY
            )

    }



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D7
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D8
# FINAL RISK REPORT + TELEGRAM ROUTER + MAIN.PY BRIDGE
# RISK ENGINE COMPLETE COMMUNICATION LAYER
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# FINAL RISK REPORT MEMORY V12
# ==========================================================

V12_RISK_REPORT_MEMORY = []

MAX_RISK_REPORT_HISTORY = 200



# ==========================================================
# RISK REPORT FORMATTER V12
# ==========================================================


def risk_final_report_formatter_v12(
    risk_result: Dict
) -> Dict:


    approved = risk_result.get(
        "approved",
        False
    )


    risk_percent = risk_result.get(
        "risk_percent",
        0
    )


    confidence = risk_result.get(
        "confidence",
        0
    )


    status = (

        "APPROVED"

        if approved

        else

        "BLOCKED"

    )



    return {


        "title":

            "ICT V12 FINAL RISK REPORT",


        "engine":

            "RISK_ENGINE_V12",


        "status":

            status,


        "risk_percent":

            risk_percent,


        "confidence":

            confidence,


        "message":

            (
                f"ICT V12 RISK STATUS\n"
                f"Approval: {status}\n"
                f"Risk: {risk_percent}%\n"
                f"Confidence: {confidence}%"
            )

    }



# ==========================================================
# RISK TELEGRAM ROUTER V12
# ==========================================================


def risk_telegram_router_v12(
    risk_result: Dict
) -> Dict:


    report = risk_final_report_formatter_v12(
        risk_result
    )


    return {


        "send":

            risk_result.get(
                "approved",
                False
            ),


        "telegram":

            report

    }



# ==========================================================
# FINAL RISK BRIDGE V12
# ==========================================================


def risk_main_bridge_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    master = run_risk_engine_v12(

        account,

        trade,

        confidence,

        market,

        drawdown

    )



    telegram = risk_telegram_router_v12(
        master
    )



    result = {


        "engine":

            "ICT_RISK_BRIDGE_V12",


        "approved":

            master.get(
                "approved",
                False
            ),


        "risk_percent":

            master.get(
                "risk_percent",
                0
            ),


        "confidence":

            master.get(
                "confidence",
                0
            ),


        "telegram":

            telegram,


        "master":

            master

    }



    V12_RISK_REPORT_MEMORY.append(
        result
    )



    if len(
        V12_RISK_REPORT_MEMORY
    ) > MAX_RISK_REPORT_HISTORY:


        del V12_RISK_REPORT_MEMORY[
            :-
            MAX_RISK_REPORT_HISTORY
        ]



    return result



# ==========================================================
# SAFE RISK BRIDGE V12
# ==========================================================


def safe_risk_bridge_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    try:


        return risk_main_bridge_v12(

            account,

            trade,

            confidence,

            market,

            drawdown

        )


    except Exception as e:


        return {


            "engine":

                "ICT_RISK_BRIDGE_V12",


            "approved":

                False,


            "risk_percent":

                0,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL RISK CALL V12
# ==========================================================


def run_final_risk_v12(
    account: Dict,
    trade: Dict,
    confidence: Dict,
    market: Dict,
    drawdown: Dict
) -> Dict:


    return safe_risk_bridge_v12(

        account,

        trade,

        confidence,

        market,

        drawdown

    )



# ==========================================================
# RISK ENGINE FINAL STATUS V12
# ==========================================================


def risk_v12_status() -> Dict:


    return {


        "engine":

            "ICT_RISK_ENGINE_V12",


        "status":

            "ONLINE",


        "phase":

            "PHASE_4_COMPLETED",


        "memory":

            len(
                V12_RISK_REPORT_MEMORY
            )

    }



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D8
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D9
# FINAL RISK MASTER VALIDATION + ERROR RECOVERY ENGINE
# ACCOUNT SAFETY + TRADE EXECUTION CONTROL
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# FINAL RISK VALIDATION MEMORY V12
# ==========================================================

V12_FINAL_RISK_VALIDATION_MEMORY = []

MAX_FINAL_RISK_VALIDATION_HISTORY = 200



# ==========================================================
# FINAL RISK VALIDATION RULES V12
# ==========================================================

FINAL_RISK_VALIDATION_RULES_V12 = {


    "max_risk_percent":

        2.0,


    "minimum_confidence":

        70,


    "minimum_rr":

        2.0,


    "account_lock":

        False

}



# ==========================================================
# RISK SIGNAL VALIDATOR V12
# ==========================================================


def validate_risk_signal_v12(
    signal: str
) -> Dict:


    allowed = [

        "BUY",

        "SELL",

        "NO_TRADE",

        "WAIT"

    ]



    return {


        "valid":

            signal in allowed,


        "signal":

            signal

    }



# ==========================================================
# RISK PERCENT FINAL CHECK V12
# ==========================================================


def validate_final_risk_percent_v12(
    risk_percent: float
) -> Dict:


    if risk_percent <= 0:


        return {


            "valid":

                False,


            "reason":

                "RISK_ZERO"

        }



    if risk_percent > FINAL_RISK_VALIDATION_RULES_V12[
        "max_risk_percent"
    ]:


        return {


            "valid":

                False,


            "reason":

                "RISK_LIMIT_EXCEEDED"

        }



    return {


        "valid":

            True,


        "reason":

            "RISK_OK"

    }



# ==========================================================
# CONFIDENCE FINAL CHECK V12
# ==========================================================


def validate_final_confidence_v12(
    confidence: int
) -> Dict:


    if confidence < FINAL_RISK_VALIDATION_RULES_V12[
        "minimum_confidence"
    ]:


        return {


            "valid":

                False,


            "reason":

                "CONFIDENCE_LOW"

        }



    return {


        "valid":

            True,


        "reason":

            "CONFIDENCE_OK"

    }



# ==========================================================
# FINAL ACCOUNT SAFETY GATE V12
# ==========================================================


def final_account_safety_gate_v12(
    drawdown: Dict
) -> Dict:


    status = drawdown.get(
        "status",
        "NORMAL"
    )



    if status == "ACCOUNT_LOCK":


        return {


            "allowed":

                False,


            "reason":

                "ACCOUNT_LOCKED"

        }



    return {


        "allowed":

            True,


        "reason":

            "ACCOUNT_SAFE"

    }



# ==========================================================
# MASTER RISK VALIDATION ENGINE V12
# ==========================================================


def master_risk_validation_v12(
    risk_result: Dict,
    confidence: Dict,
    drawdown: Dict
) -> Dict:


    try:


        risk_check = validate_final_risk_percent_v12(

            risk_result.get(
                "risk_percent",
                0
            )

        )



        confidence_check = validate_final_confidence_v12(

            confidence.get(
                "confidence",
                0
            )

        )



        account_check = final_account_safety_gate_v12(

            drawdown

        )



        approved = (

            risk_check["valid"]

            and

            confidence_check["valid"]

            and

            account_check["allowed"]

        )



        result = {


            "engine":

                "ICT_FINAL_RISK_VALIDATION_V12",


            "status":

                "ONLINE",


            "approved":

                approved,


            "reason":

                (
                    "FINAL_RISK_APPROVED"
                    if approved
                    else
                    "FINAL_RISK_BLOCKED"
                ),


            "risk":

                risk_check,


            "confidence":

                confidence_check,


            "account":

                account_check

        }



        V12_FINAL_RISK_VALIDATION_MEMORY.append(
            result
        )



        if len(
            V12_FINAL_RISK_VALIDATION_MEMORY
        ) > MAX_FINAL_RISK_VALIDATION_HISTORY:


            del V12_FINAL_RISK_VALIDATION_MEMORY[
                :-
                MAX_FINAL_RISK_VALIDATION_HISTORY
            ]



        return result



    except Exception as e:


        return risk_validation_error_recovery_v12(
            e
        )



# ==========================================================
# RISK ERROR RECOVERY V12
# ==========================================================


def risk_validation_error_recovery_v12(
    error: Exception
) -> Dict:


    return {


        "engine":

            "ICT_RISK_RECOVERY_V12",


        "status":

            "RECOVERED",


        "approved":

            False,


        "risk_percent":

            0,


        "error":

            str(error)

    }



# ==========================================================
# MAIN.PY RISK VALIDATION ENTRY V12
# ==========================================================


def get_final_risk_validation_v12(
    risk_result: Dict,
    confidence: Dict,
    drawdown: Dict
) -> Dict:


    return master_risk_validation_v12(

        risk_result,

        confidence,

        drawdown

    )



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D9
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D10
# FINAL RISK EXECUTION CONTROLLER + MAIN.PY MASTER BRIDGE
# COMPLETE RISK AUTHORIZATION SYSTEM
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# FINAL EXECUTION MEMORY V12
# ==========================================================

V12_RISK_EXECUTION_MEMORY = []

MAX_EXECUTION_HISTORY = 200



# ==========================================================
# EXECUTION CONFIGURATION V12
# ==========================================================

RISK_EXECUTION_CONFIG_V12 = {


    "require_approval":

        True,


    "allow_trade":

        True,


    "blocked_signal":

        "NO_TRADE"

}



# ==========================================================
# EXECUTION INPUT VALIDATOR V12
# ==========================================================


def validate_execution_input_v12(
    risk_validation: Dict
) -> Dict:


    required = [

        "approved",

        "reason"

    ]


    missing = []



    for key in required:


        if key not in risk_validation:

            missing.append(key)



    return {


        "valid":

            len(missing) == 0,


        "missing":

            missing

    }



# ==========================================================
# FINAL TRADE AUTHORIZATION ENGINE V12
# ==========================================================


def final_trade_authorization_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    try:


        validation = validate_execution_input_v12(
            risk_validation
        )



        if not validation["valid"]:


            return {


                "approved":

                    False,


                "signal":

                    "NO_TRADE",


                "reason":

                    "INVALID_VALIDATION"

            }



        approved = risk_validation.get(
            "approved",
            False
        )



        if not approved:


            return {


                "engine":

                    "ICT_RISK_EXECUTION_V12",


                "status":

                    "BLOCKED",


                "approved":

                    False,


                "signal":

                    "NO_TRADE",


                "reason":

                    risk_validation.get(
                        "reason",
                        "RISK_BLOCKED"
                    )

            }



        return {


            "engine":

                "ICT_RISK_EXECUTION_V12",


            "status":

                "AUTHORIZED",


            "approved":

                True,


            "signal":

                trade.get(
                    "signal",
                    "NO_TRADE"
                ),


            "entry":

                trade.get(
                    "entry",
                    0
                ),


            "stop_loss":

                trade.get(
                    "stop_loss",
                    0
                ),


            "take_profit":

                trade.get(
                    "take_profit",
                    0
                ),


            "reason":

                "TRADE_AUTHORIZED"

        }



    except Exception as e:


        return {


            "engine":

                "ICT_RISK_EXECUTION_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "signal":

                "NO_TRADE",


            "error":

                str(e)

        }



# ==========================================================
# EXECUTION SAFETY CONTROLLER V12
# ==========================================================


def risk_execution_controller_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    result = final_trade_authorization_v12(

        risk_validation,

        trade

    )



    V12_RISK_EXECUTION_MEMORY.append(
        result
    )



    if len(
        V12_RISK_EXECUTION_MEMORY
    ) > MAX_EXECUTION_HISTORY:


        del V12_RISK_EXECUTION_MEMORY[
            :-
            MAX_EXECUTION_HISTORY
        ]



    return result



# ==========================================================
# SAFE EXECUTION WRAPPER V12
# ==========================================================


def safe_risk_execution_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    try:


        return risk_execution_controller_v12(

            risk_validation,

            trade

        )


    except Exception as e:


        return {


            "engine":

                "ICT_RISK_EXECUTION_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "signal":

                "NO_TRADE",


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL EXECUTION ENTRY V12
# ==========================================================


def run_risk_execution_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    return safe_risk_execution_v12(

        risk_validation,

        trade

    )



# ==========================================================
# RISK EXECUTION HEALTH CHECK V12
# ==========================================================


def risk_execution_health_v12() -> Dict:


    return {


        "engine":

            "ICT_RISK_EXECUTION_V12",


        "status":

            "ONLINE",


        "phase":

            "PHASE_4_D10",


        "memory":

            len(
                V12_RISK_EXECUTION_MEMORY
            )

    }



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D10
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D11
# RISK MASTER FINAL REPORT + TELEGRAM SIGNAL CONTROL
# EXECUTION RESULT AGGREGATION ENGINE
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# FINAL RISK RESULT MEMORY V12
# ==========================================================

V12_FINAL_RISK_RESULT_MEMORY = []

MAX_FINAL_RESULT_HISTORY = 200



# ==========================================================
# FINAL RISK REPORT CONFIG V12
# ==========================================================

FINAL_RISK_REPORT_CONFIG_V12 = {


    "approved_message":

        "TRADE APPROVED",


    "blocked_message":

        "TRADE BLOCKED",


    "default_signal":

        "NO_TRADE"

}



# ==========================================================
# RISK EXECUTION RESULT FORMATTER V12
# ==========================================================


def format_risk_execution_report_v12(
    execution_result: Dict
) -> Dict:


    approved = execution_result.get(
        "approved",
        False
    )


    status = (

        "APPROVED"

        if approved

        else

        "BLOCKED"

    )


    signal = execution_result.get(
        "signal",
        "NO_TRADE"
    )



    return {


        "engine":

            "ICT_RISK_FINAL_REPORT_V12",


        "status":

            status,


        "signal":

            signal,


        "entry":

            execution_result.get(
                "entry",
                0
            ),


        "stop_loss":

            execution_result.get(
                "stop_loss",
                0
            ),


        "take_profit":

            execution_result.get(
                "take_profit",
                0
            ),


        "message":

            (
                FINAL_RISK_REPORT_CONFIG_V12[
                    "approved_message"
                ]
                if approved
                else
                FINAL_RISK_REPORT_CONFIG_V12[
                    "blocked_message"
                ]
            )

    }



# ==========================================================
# TELEGRAM RISK SIGNAL BUILDER V12
# ==========================================================


def build_risk_telegram_signal_v12(
    report: Dict
) -> Dict:


    return {


        "send":

            report.get(
                "status"
            )
            ==
            "APPROVED",


        "message":

            (
                f"📊 ICT V12 RISK SIGNAL\n"
                f"Status: {report.get('status')}\n"
                f"Signal: {report.get('signal')}\n"
                f"Entry: {report.get('entry')}\n"
                f"SL: {report.get('stop_loss')}\n"
                f"TP: {report.get('take_profit')}"
            )

    }



# ==========================================================
# FINAL RISK MASTER CONTROLLER V12
# ==========================================================


def final_risk_master_controller_v12(
    execution_result: Dict
) -> Dict:


    try:


        report = format_risk_execution_report_v12(
            execution_result
        )


        telegram = build_risk_telegram_signal_v12(
            report
        )



        result = {


            "engine":

                "ICT_FINAL_RISK_MASTER_V12",


            "status":

                "ONLINE",


            "approved":

                execution_result.get(
                    "approved",
                    False
                ),


            "report":

                report,


            "telegram":

                telegram

        }



        V12_FINAL_RISK_RESULT_MEMORY.append(
            result
        )



        if len(
            V12_FINAL_RISK_RESULT_MEMORY
        ) > MAX_FINAL_RESULT_HISTORY:


            del V12_FINAL_RISK_RESULT_MEMORY[
                :-
                MAX_FINAL_RESULT_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_FINAL_RISK_MASTER_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "error":

                str(e)

        }



# ==========================================================
# SAFE FINAL RISK MASTER V12
# ==========================================================


def safe_final_risk_master_v12(
    execution_result: Dict
) -> Dict:


    try:


        return final_risk_master_controller_v12(
            execution_result
        )


    except Exception as e:


        return {


            "engine":

                "ICT_FINAL_RISK_MASTER_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL RISK MASTER ENTRY V12
# ==========================================================


def run_final_risk_master_v12(
    execution_result: Dict
) -> Dict:


    return safe_final_risk_master_v12(
        execution_result
    )



# ==========================================================
# RISK MASTER HEALTH CHECK V12
# ==========================================================


def risk_master_health_v12() -> Dict:


    return {


        "engine":

            "ICT_RISK_MASTER_V12",


        "status":

            "ONLINE",


        "phase":

            "PHASE_4_D11",


        "memory":

            len(
                V12_FINAL_RISK_RESULT_MEMORY
            )

    }



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D11
# ==========================================================
# ==========================================================
# RISK ENGINE V12
# PHASE 4 - PART D12
# RISK ENGINE FINAL INTEGRATION + MAIN.PY ORCHESTRATOR BRIDGE
# COMPLETE RISK PIPELINE CLOSURE SYSTEM
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict



# ==========================================================
# FINAL INTEGRATION MEMORY V12
# ==========================================================

V12_RISK_INTEGRATION_MEMORY = []

MAX_INTEGRATION_HISTORY = 200



# ==========================================================
# RISK INTEGRATION CONFIG V12
# ==========================================================

RISK_INTEGRATION_CONFIG_V12 = {


    "engine":

        "ICT_RISK_ENGINE_V12",


    "phase":

        "PHASE_4_COMPLETE",


    "default_signal":

        "NO_TRADE",


    "fail_safe":

        True

}



# ==========================================================
# COMPLETE RISK PIPELINE VALIDATOR V12
# ==========================================================


def validate_complete_risk_pipeline_v12(
    result: Dict
) -> Dict:


    required = [

        "approved",

        "signal"

    ]


    missing = []



    for key in required:


        if key not in result:

            missing.append(key)



    return {


        "valid":

            len(missing) == 0,


        "missing":

            missing

    }



# ==========================================================
# FINAL RISK DECISION SUMMARY V12
# ==========================================================


def generate_risk_decision_summary_v12(
    execution: Dict,
    report: Dict
) -> Dict:


    approved = execution.get(
        "approved",
        False
    )


    return {


        "decision":

            (
                "EXECUTE"
                if approved
                else
                "BLOCK"
            ),


        "signal":

            execution.get(
                "signal",
                "NO_TRADE"
            ),


        "entry":

            execution.get(
                "entry",
                0
            ),


        "stop_loss":

            execution.get(
                "stop_loss",
                0
            ),


        "take_profit":

            execution.get(
                "take_profit",
                0
            ),


        "message":

            report.get(
                "message",
                "RISK CHECK COMPLETE"
            )

    }



# ==========================================================
# MASTER RISK INTEGRATION ENGINE V12
# ==========================================================


def risk_master_integration_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    try:


        execution = run_risk_execution_v12(

            risk_validation,

            trade

        )



        final_report = run_final_risk_master_v12(
            execution
        )



        summary = generate_risk_decision_summary_v12(

            execution,

            final_report.get(
                "report",
                {}
            )

        )



        result = {


            "engine":

                "ICT_RISK_MASTER_INTEGRATION_V12",


            "status":

                "ONLINE",


            "approved":

                execution.get(
                    "approved",
                    False
                ),


            "execution":

                execution,


            "report":

                final_report,


            "summary":

                summary

        }



        V12_RISK_INTEGRATION_MEMORY.append(
            result
        )



        if len(
            V12_RISK_INTEGRATION_MEMORY
        ) > MAX_INTEGRATION_HISTORY:


            del V12_RISK_INTEGRATION_MEMORY[
                :-
                MAX_INTEGRATION_HISTORY
            ]



        return result



    except Exception as e:


        return {


            "engine":

                "ICT_RISK_MASTER_INTEGRATION_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "signal":

                "NO_TRADE",


            "error":

                str(e)

        }



# ==========================================================
# SAFE RISK INTEGRATION WRAPPER V12
# ==========================================================


def safe_risk_master_integration_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    try:


        return risk_master_integration_v12(

            risk_validation,

            trade

        )


    except Exception as e:


        return {


            "engine":

                "ICT_RISK_MASTER_INTEGRATION_V12",


            "status":

                "ERROR",


            "approved":

                False,


            "signal":

                "NO_TRADE",


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL RISK PIPELINE ENTRY V12
# ==========================================================


def run_complete_risk_engine_v12(
    risk_validation: Dict,
    trade: Dict
) -> Dict:


    return safe_risk_master_integration_v12(

        risk_validation,

        trade

    )



# ==========================================================
# RISK ENGINE COMPLETE HEALTH CHECK V12
# ==========================================================


def complete_risk_engine_health_v12() -> Dict:


    return {


        "engine":

            "ICT_COMPLETE_RISK_ENGINE_V12",


        "status":

            "ONLINE",


        "phase":

            "PHASE_4_D12_COMPLETE",


        "memory":

            len(
                V12_RISK_INTEGRATION_MEMORY
            ),


        "modules":

            [

                "BASE_RISK",

                "ADVANCED_RISK",

                "DRAWDOWN_CONTROL",

                "TRADE_PROTECTION",

                "SMART_RISK",

                "FINAL_DECISION",

                "PIPELINE",

                "REPORT",

                "VALIDATION",

                "EXECUTION",

                "TELEGRAM",

                "INTEGRATION"

            ]

    }



# ==========================================================
# END RISK ENGINE V12
# PHASE 4 PART D12
# ==========================================================
