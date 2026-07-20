# ==========================
# SIGNAL ENGINE V5
# ==========================

SIGNAL_STATE = {

    "direction": "NO TRADE",

    "entry": None,

    "sl": None,

    "tp1": None,

    "tp2": None,

    "confidence": 0,

    "reason": []

}



# ==========================
# SIGNAL RESET
# ==========================

def reset_signal():

    SIGNAL_STATE["direction"] = "NO TRADE"

    SIGNAL_STATE["entry"] = None

    SIGNAL_STATE["sl"] = None

    SIGNAL_STATE["tp1"] = None

    SIGNAL_STATE["tp2"] = None

    SIGNAL_STATE["confidence"] = 0

    SIGNAL_STATE["reason"] = []


    return True



# ==========================
# CREATE SIGNAL OBJECT
# ==========================

def create_signal(

    direction,

    entry,

    sl,

    tp1,

    tp2,

    confidence,

    reason

):

    return {

        "direction": direction,

        "entry": entry,

        "sl": sl,

        "tp1": tp1,

        "tp2": tp2,

        "confidence": confidence,

        "reason": reason

    }
    # ==========================
# BUY SIGNAL
# ==========================

def create_buy_signal(

    entry,

    sl,

    tp1,

    tp2,

    confidence,

    reason

):

    return create_signal(

        "BUY",

        entry,

        sl,

        tp1,

        tp2,

        confidence,

        reason

    )



# ==========================
# SELL SIGNAL
# ==========================

def create_sell_signal(

    entry,

    sl,

    tp1,

    tp2,

    confidence,

    reason

):

    return create_signal(

        "SELL",

        entry,

        sl,

        tp1,

        tp2,

        confidence,

        reason

    )



# ==========================
# NO TRADE
# ==========================

def no_trade_signal(

    reason

):

    return create_signal(

        "NO TRADE",

        None,

        None,

        None,

        None,

        0,

        reason

    )
    # ==========================
# ENTRY CALCULATION
# ==========================

def calculate_entry(

    price

):

    return round(

        float(price),

        2

    )



# ==========================
# STOP LOSS CALCULATION
# ==========================

def calculate_sl(

    entry,

    atr,

    multiplier=1.5

):

    sl_distance = atr * multiplier


    return round(

        entry - sl_distance,

        2

    )



# ==========================
# TAKE PROFIT CALCULATION
# ==========================

def calculate_tp(

    entry,

    sl,

    risk_reward=3

):

    risk = entry - sl


    tp1 = entry + risk * risk_reward


    tp2 = entry + risk * (risk_reward + 1)


    return (

        round(tp1, 2),

        round(tp2, 2)

    )
    # ==========================
# RISK REWARD CHECK
# ==========================

def check_risk_reward(

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

        return False


    rr = reward / risk


    return rr >= 2



# ==========================
# SIGNAL VALIDATION
# ==========================

def validate_signal(

    direction,

    confidence,

    filters_passed

):

    if direction == "NO TRADE":

        return False


    if confidence < 80:

        return False


    if filters_passed is not True:

        return False


    return True



# ==========================
# FINAL SIGNAL BUILDER
# ==========================

def build_signal(

    direction,

    price,

    atr,

    confidence,

    reason,

    filters_passed=True

):

    entry = calculate_entry(

        price

    )


    if direction == "BUY":

        sl = calculate_sl(

            entry,

            atr

        )

        tp1, tp2 = calculate_tp(

            entry,

            sl

        )


        if validate_signal(

            direction,

            confidence,

            filters_passed

        ):

            return create_buy_signal(

                entry,

                sl,

                tp1,

                tp2,

                confidence,

                reason

            )


    return no_trade_signal(

        "Validation Failed"

    )
    # ==========================
# SELL SIGNAL BUILDER
# ==========================

def build_sell_signal(

    direction,

    price,

    atr,

    confidence,

    reason,

    filters_passed=True

):

    entry = calculate_entry(

        price

    )


    if direction == "SELL":

        sl = entry + (

            atr * 1.5

        )


        risk = abs(

            sl - entry

        )


        tp1 = entry - (

            risk * 3

        )


        tp2 = entry - (

            risk * 4

        )


        if validate_signal(

            direction,

            confidence,

            filters_passed

        ):

            return create_sell_signal(

                entry,

                round(sl, 2),

                round(tp1, 2),

                round(tp2, 2),

                confidence,

                reason

            )


    return no_trade_signal(

        "Validation Failed"

    )



# ==========================
# UPDATE SIGNAL STATE
# ==========================

def update_signal_state(

    signal

):

    SIGNAL_STATE["direction"] = signal["direction"]

    SIGNAL_STATE["entry"] = signal["entry"]

    SIGNAL_STATE["sl"] = signal["sl"]

    SIGNAL_STATE["tp1"] = signal["tp1"]

    SIGNAL_STATE["tp2"] = signal["tp2"]

    SIGNAL_STATE["confidence"] = signal["confidence"]

    SIGNAL_STATE["reason"] = signal["reason"]


    return SIGNAL_STATE



# ==========================
# STORE SIGNAL
# ==========================

def store_signal(

    signal

):

    update_signal_state(

        signal

    )


    return SIGNAL_STATE
    # ==========================
# SIGNAL REPORT
# ==========================

def signal_report():

    return {

        "direction":

        SIGNAL_STATE["direction"],

        "entry":

        SIGNAL_STATE["entry"],

        "sl":

        SIGNAL_STATE["sl"],

        "tp1":

        SIGNAL_STATE["tp1"],

        "tp2":

        SIGNAL_STATE["tp2"],

        "confidence":

        SIGNAL_STATE["confidence"],

        "reason":

        SIGNAL_STATE["reason"]

    }



# ==========================
# DEBUG SIGNAL
# ==========================

def debug_signal():

    report = signal_report()


    print("\n========== SIGNAL V5 ==========")

    print("Direction :", report["direction"])

    print("Entry :", report["entry"])

    print("SL :", report["sl"])

    print("TP1 :", report["tp1"])

    print("TP2 :", report["tp2"])

    print("Confidence :", report["confidence"])

    print("Reason :", report["reason"])

    print("================================\n")


    return report



# ==========================
# SCANNER INTEGRATION
# ==========================

def signal_for_scanner(

    signal

):

    stored = store_signal(

        signal

    )


    return {

        "direction":

        stored["direction"],

        "entry":

        stored["entry"],

        "sl":

        stored["sl"],

        "tp1":

        stored["tp1"],

        "tp2":

        stored["tp2"],

        "confidence":

        stored["confidence"]

    }
    # ==========================
# SIGNAL TEXT FORMAT
# ==========================

def signal_text(

    signal

):

    return (

        f"🚀 SIGNAL\n"

        f"Direction: {signal['direction']}\n"

        f"Entry: {signal['entry']}\n"

        f"SL: {signal['sl']}\n"

        f"TP1: {signal['tp1']}\n"

        f"TP2: {signal['tp2']}\n"

        f"Confidence: {signal['confidence']}\n"

        f"Reason: {signal['reason']}"

    )



# ==========================
# TELEGRAM FORMAT
# ==========================

def telegram_signal_format(

    signal

):

    return signal_text(

        signal

    )



# ==========================
# FINAL OUTPUT
# ==========================

def final_signal_output(

    signal

):

    return {

        "data":

        signal,

        "message":

        signal_text(

            signal

        )

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def signal_engine(

    signal

):

    stored = store_signal(

        signal

    )


    return {

        "signal":

        stored,

        "message":

        signal_text(

            stored

        )

    }



# ==========================
# SIGNAL ENGINE V5
# ==========================

def signal_engine_v5(

    signal

):

    result = signal_engine(

        signal

    )


    return {

        "direction":

        result["signal"]["direction"],

        "entry":

        result["signal"]["entry"],

        "sl":

        result["signal"]["sl"],

        "tp1":

        result["signal"]["tp1"],

        "tp2":

        result["signal"]["tp2"],

        "confidence":

        result["signal"]["confidence"],

        "message":

        result["message"]

    }



# ==========================
# TEST ENGINE
# ==========================

def test_signal(

    signal

):

    return signal_engine_v5(

        signal

    )
    # ==========================
# SIGNAL STATUS
# ==========================

def signal_status():

    return {

        "direction":

        SIGNAL_STATE["direction"],

        "entry":

        SIGNAL_STATE["entry"],

        "sl":

        SIGNAL_STATE["sl"],

        "tp1":

        SIGNAL_STATE["tp1"],

        "tp2":

        SIGNAL_STATE["tp2"],

        "confidence":

        SIGNAL_STATE["confidence"]

    }



# ==========================
# MODULE REPORT
# ==========================

def signal_module_report():

    return {

        "status":

        signal_status(),

        "report":

        signal_report()

    }



# ==========================
# FINAL SIGNAL CHECK
# ==========================

def final_signal_check():

    return (

        SIGNAL_STATE["direction"]

        !=

        "NO TRADE"

    )
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "reset_signal",

    "create_signal",

    "create_buy_signal",

    "create_sell_signal",

    "no_trade_signal",

    "calculate_entry",

    "calculate_sl",

    "calculate_tp",

    "check_risk_reward",

    "validate_signal",

    "build_signal",

    "build_sell_signal",

    "update_signal_state",

    "store_signal",

    "signal_report",

    "debug_signal",

    "signal_for_scanner",

    "signal_text",

    "telegram_signal_format",

    "final_signal_output",

    "signal_engine",

    "signal_engine_v5",

    "test_signal",

    "signal_status",

    "signal_module_report",

    "final_signal_check"

]
