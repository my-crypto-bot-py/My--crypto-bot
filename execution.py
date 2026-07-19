# ==========================
# ICT EXECUTION ENGINE
# ==========================


# ==========================
# CHECK DIRECTION
# ==========================

def check_direction(
    signal_direction,
    structure=None,
    smt=None,
    pd_array=None
):

    confirmations = 0


    if structure:

        if structure.get("direction") == signal_direction:

            confirmations += 1



    if smt:

        if smt.get("direction") == signal_direction:

            confirmations += 1



    if pd_array:

        if pd_array.get("direction") == signal_direction:

            confirmations += 1



    return confirmations



# ==========================
# ENTRY VALIDATION
# ==========================

def validate_entry(

    direction,

    price,

    pd_array=None,

    ote=None,

    structure=None,

    smt=None

):

    score = 0


    # PD Array

    if pd_array:

        if pd_array.get("direction") == direction:

            score += 30



    # OTE

    if ote:

        if ote.get("valid"):

            score += 30



    # Structure

    if structure:

        if structure.get("direction") == direction:

            score += 25



    # SMT

    if smt:

        if smt.get("confirm"):

            if smt.get("direction") == direction:

                score += 15



    return {

        "valid": score >= 70,

        "score": score

    }



# ==========================
# EXECUTION DECISION
# ==========================

def execution_signal(

    direction,

    price,

    pd_array=None,

    ote=None,

    structure=None,

    smt=None

):

    result = validate_entry(

        direction,

        price,

        pd_array,

        ote,

        structure,

        smt

    )


    if result["valid"]:

        return {

            "signal": direction,

            "execution_score":
            result["score"]

        }


    return {

        "signal": "NO TRADE",

        "execution_score":
        result["score"]

    }
  # ==========================
# SIGNAL MEMORY
# ==========================

last_signal = None

last_signal_time = None



# ==========================
# COOLDOWN SETTINGS
# ==========================

COOLDOWN_MINUTES = 60



# ==========================
# CHECK DUPLICATE SIGNAL
# ==========================

def is_duplicate_signal(
    new_signal
):

    global last_signal


    if last_signal is None:

        return False


    if (

        last_signal["direction"]
        ==
        new_signal["direction"]

        and

        last_signal["entry"]
        ==
        new_signal["entry"]

    ):

        return True


    return False



# ==========================
# SAVE SIGNAL
# ==========================

def save_signal(
    signal
):

    global last_signal
    global last_signal_time


    last_signal = signal


    from datetime import datetime

    last_signal_time = datetime.utcnow()



# ==========================
# CHECK COOLDOWN
# ==========================

def check_cooldown():

    global last_signal_time


    if last_signal_time is None:

        return False


    from datetime import datetime


    now = datetime.utcnow()


    diff = (
        now - last_signal_time
    ).total_seconds() / 60



    if diff < COOLDOWN_MINUTES:

        return True


    return False



# ==========================
# FINAL DUPLICATE FILTER
# ==========================

def final_signal_filter(
    signal
):


    if signal.get("direction") == "NO TRADE":
     
    
    return False



    if is_duplicate_signal(
        signal
    ):

        print(
            "Duplicate Signal Blocked"
        )

        return False



    if check_cooldown():

        print(
            "Cooldown Active"
        )

        return False



    save_signal(
        signal
    )


    return True
  # ==========================
# FINAL TRADE PACKAGE
# ==========================

def create_trade_package(

    direction,

    levels,

    score,

    reasons=None

):

    if levels is None:

        return None



    return {

        "direction": direction,

        "entry": levels["entry"],

        "sl": levels["sl"],

        "tp1": levels["tp1"],

        "tp2": levels["tp2"],

        "score": score,

        "reasons": reasons or []

    }



# ==========================
# RISK REWARD CHECK
# ==========================

def check_risk_reward(

    trade,

    minimum_rr=3

):

    entry = trade["entry"]

    sl = trade["sl"]

    tp = trade["tp2"]



    risk = abs(
        entry - sl
    )


    reward = abs(
        tp - entry
    )


    if risk == 0:

        return False



    rr = reward / risk



    trade["rr"] = round(
        rr,
        2
    )


    if rr >= minimum_rr:

        return True


    return False



# ==========================
# FINAL EXECUTION GATE
# ==========================

def final_execution_gate(

    trade

):

    if trade is None:

        return {

            "approved": False,

            "reason":
            "No Trade Data"

        }



    if not check_risk_reward(
        trade
    ):

        return {

            "approved": False,

            "reason":
            "Low Risk Reward"

        }



    if not final_signal_filter(
        trade
    ):

        return {

            "approved": False,

            "reason":
            "Duplicate/Cooldown"

        }



    return {

        "approved": True,

        "trade": trade

    }
