# ==========================
# ICT RISK MANAGEMENT V2
# ==========================

from config import (
    MIN_RR,
    RISK_PERCENT,
    MAX_TRADES_PER_DAY,
    MAX_DAILY_LOSS,
    MAX_CONSECUTIVE_LOSSES
)


# ==========================
# RR CALCULATION
# ==========================

def calculate_rr(
    entry,
    sl,
    tp
):

    risk = abs(
        entry - sl
    )

    reward = abs(
        tp - entry
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

    risk_percent,

    entry,

    sl

):


    risk_amount = (
        balance *
        risk_percent /
        100
    )


    stop_distance = abs(
        entry - sl
    )


    if stop_distance == 0:

        return 0



    size = (
        risk_amount /
        stop_distance
    )


    return round(
        size,
        4
    )




# ==========================
# TRADE VALIDATION
# ==========================

def validate_trade(

    entry,

    sl,

    tp,

    direction,

    min_rr=MIN_RR

):


    rr = calculate_rr(

        entry,

        sl,

        tp

    )


    # BUY check

    if direction == "BUY":

        if not (
            tp > entry
            and
            sl < entry
        ):

            return {

                "valid":False,

                "reason":
                "Invalid BUY levels",

                "rr":rr

            }



    # SELL check

    if direction == "SELL":

        if not (
            tp < entry
            and
            sl > entry
        ):

            return {

                "valid":False,

                "reason":
                "Invalid SELL levels",

                "rr":rr

            }



    if rr < min_rr:

        return {

            "valid":False,

            "reason":
            "Low RR",

            "rr":rr

        }



    return {

        "valid":True,

        "rr":rr

    }
    # ==========================
# TRADE LIMIT MEMORY
# ==========================

daily_loss = 0

trade_count = 0

consecutive_losses = 0



# ==========================
# CHECK TRADE PERMISSION
# ==========================

def can_take_trade():


    global daily_loss

    global trade_count

    global consecutive_losses



    if daily_loss >= MAX_DAILY_LOSS:


        return False, "Daily Loss Limit Reached"



    if trade_count >= MAX_TRADES_PER_DAY:


        return False, "Maximum Trades Reached"



    if consecutive_losses >= MAX_CONSECUTIVE_LOSSES:


        return False, "Consecutive Loss Limit Reached"



    return True, "OK"




# ==========================
# UPDATE TRADE RESULT
# ==========================

def update_trade_result(

    result,

    loss_percent=RISK_PERCENT

):


    global daily_loss

    global trade_count

    global consecutive_losses



    trade_count += 1



    if result == "LOSS":


        daily_loss += loss_percent


        consecutive_losses += 1




    elif result == "WIN":


        consecutive_losses = 0




# ==========================
# DAILY RESET
# ==========================

def reset_daily_stats():


    global daily_loss

    global trade_count

    global consecutive_losses



    daily_loss = 0

    trade_count = 0

    consecutive_losses = 0



    print(
        "Risk Stats Reset"
    )




# ==========================
# RISK SUMMARY
# ==========================

def risk_status():


    return {


        "daily_loss":

        daily_loss,


        "trade_count":

        trade_count,


        "consecutive_losses":

        consecutive_losses


    }
