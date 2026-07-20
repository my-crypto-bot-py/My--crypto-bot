import pandas as pd
import numpy as np
import time


# ==========================
# ICT EXECUTION ENGINE V5
# ==========================


# ==========================
# SETTINGS
# ==========================

MAX_TRADES = 1

DEFAULT_RISK = 1.0

MIN_EXECUTION_SCORE = 70



# ==========================
# EXECUTION STATE
# ==========================

execution_state = {

    "active_trade": None,

    "last_signal": None,

    "trade_count": 0

}



# ==========================
# PREPARE DATA
# ==========================

def prepare_execution(df):

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
# SIGNAL OBJECT
# ==========================

def create_signal_object(

    direction,

    entry,

    sl,

    tp,

    score

):

    return {

        "direction": direction,

        "entry": round(

            float(entry),

            2

        ),

        "sl": round(

            float(sl),

            2

        ),

        "tp": round(

            float(tp),

            2

        ),

        "score": score,

        "time": time.time()

    }
    # ==========================
# SIGNAL PARSER
# ==========================

def parse_signal(signal):

    if signal is None:

        return None


    direction = signal.get(

        "direction"

    )


    entry = signal.get(

        "entry"

    )


    sl = signal.get(

        "sl"

    )


    tp = signal.get(

        "tp"

    )


    score = signal.get(

        "score",

        0

    )


    if direction not in [

        "BUY",

        "SELL"

    ]:

        return None


    if entry is None or sl is None or tp is None:

        return None


    return create_signal_object(

        direction,

        entry,

        sl,

        tp,

        score

    )



# ==========================
# SIGNAL VALIDATION
# ==========================

def validate_signal(signal):

    if signal is None:

        return False


    if signal["score"] < MIN_EXECUTION_SCORE:

        return False


    if signal["entry"] <= 0:

        return False


    if signal["sl"] <= 0:

        return False


    if signal["tp"] <= 0:

        return False


    return True



# ==========================
# DIRECTION CHECK
# ==========================

def check_direction(signal):

    if signal is None:

        return None


    return signal["direction"]
    # ==========================
# ENTRY VALIDATION
# ==========================

def validate_entry(

    signal,

    current_price

):

    if signal is None:

        return False


    direction = signal["direction"]


    if direction == "BUY":

        if current_price <= signal["entry"]:

            return True


    if direction == "SELL":

        if current_price >= signal["entry"]:

            return True


    return False



# ==========================
# STOP LOSS CHECK
# ==========================

def validate_stop_loss(signal):

    if signal is None:

        return False


    if signal["direction"] == "BUY":

        return (

            signal["sl"]

            <

            signal["entry"]

        )


    if signal["direction"] == "SELL":

        return (

            signal["sl"]

            >

            signal["entry"]

        )


    return False



# ==========================
# TAKE PROFIT CHECK
# ==========================

def validate_take_profit(signal):

    if signal is None:

        return False


    if signal["direction"] == "BUY":

        return (

            signal["tp"]

            >

            signal["entry"]

        )


    if signal["direction"] == "SELL":

        return (

            signal["tp"]

            <

            signal["entry"]

        )


    return False



# ==========================
# RISK REWARD CHECK
# ==========================

def calculate_rr(signal):

    if signal is None:

        return 0


    risk = abs(

        signal["entry"]

        -

        signal["sl"]

    )


    reward = abs(

        signal["tp"]

        -

        signal["entry"]

    )


    if risk == 0:

        return 0


    return round(

        reward / risk,

        2

    )
    # ==========================
# ORDER PREPARATION
# ==========================

def prepare_order(signal):

    if not validate_signal(signal):

        return None


    rr = calculate_rr(signal)


    if rr < 1:

        return None


    order = {

        "symbol": None,

        "side":

        signal["direction"],

        "entry":

        signal["entry"],

        "stop_loss":

        signal["sl"],

        "take_profit":

        signal["tp"],

        "score":

        signal["score"],

        "risk_reward":

        rr,

        "status":

        "READY"

    }


    return order



# ==========================
# ADD SYMBOL
# ==========================

def attach_symbol(

    order,

    symbol

):

    if order is None:

        return None


    order["symbol"] = symbol


    return order



# ==========================
# EXECUTION QUEUE
# ==========================

execution_queue = []



def add_to_queue(order):

    if order is None:

        return False


    execution_queue.append(

        order

    )


    return True



# ==========================
# GET QUEUED ORDER
# ==========================

def get_next_order():

    if len(execution_queue) == 0:

        return None


    return execution_queue[0]
    # ==========================
# RISK MANAGEMENT
# ==========================

def calculate_risk_amount(

    balance,

    risk_percent=DEFAULT_RISK

):

    if balance <= 0:

        return 0


    risk_amount = (

        balance

        *

        risk_percent

        /

        100

    )


    return round(

        risk_amount,

        2

    )



# ==========================
# POSITION SIZE
# ==========================

def calculate_position_size(

    balance,

    entry,

    sl,

    risk_percent=DEFAULT_RISK

):

    risk_amount = calculate_risk_amount(

        balance,

        risk_percent

    )


    distance = abs(

        entry

        -

        sl

    )


    if distance == 0:

        return 0


    size = (

        risk_amount

        /

        distance

    )


    return round(

        size,

        4

    )



# ==========================
# ACTIVE TRADE CHECK
# ==========================

def has_active_trade():

    return (

        execution_state["active_trade"]

        is not None

    )



# ==========================
# MAX TRADE LIMIT
# ==========================

def can_execute_trade():

    if execution_state["trade_count"] >= MAX_TRADES:

        return False


    if has_active_trade():

        return False


    return True
    # ==========================
# OPEN TRADE
# ==========================

def open_trade(order):

    if order is None:

        return False


    if not can_execute_trade():

        return False


    order["status"] = "OPEN"


    execution_state["active_trade"] = order

    execution_state["last_signal"] = order

    execution_state["trade_count"] += 1


    return True



# ==========================
# CLOSE TRADE
# ==========================

def close_trade():

    if not has_active_trade():

        return False


    execution_state["active_trade"] = None


    return True



# ==========================
# CURRENT TRADE
# ==========================

def get_active_trade():

    return execution_state["active_trade"]



# ==========================
# TRADE STATUS
# ==========================

def trade_status():

    trade = get_active_trade()


    if trade is None:

        return {

            "status":

            "NO ACTIVE TRADE"

        }


    return {

        "status":

        trade["status"],

        "symbol":

        trade["symbol"],

        "side":

        trade["side"],

        "entry":

        trade["entry"],

        "sl":

        trade["stop_loss"],

        "tp":

        trade["take_profit"]

    }
    # ==========================
# POSITION MONITOR
# ==========================

def monitor_position(current_price):

    trade = get_active_trade()


    if trade is None:

        return None


    side = trade["side"]


    # BUY position

    if side == "BUY":

        if current_price <= trade["stop_loss"]:

            return {

                "exit":

                True,

                "reason":

                "STOP LOSS HIT"

            }


        if current_price >= trade["take_profit"]:

            return {

                "exit":

                True,

                "reason":

                "TAKE PROFIT HIT"

            }



    # SELL position

    if side == "SELL":

        if current_price >= trade["stop_loss"]:

            return {

                "exit":

                True,

                "reason":

                "STOP LOSS HIT"

            }


        if current_price <= trade["take_profit"]:

            return {

                "exit":

                True,

                "reason":

                "TAKE PROFIT HIT"

            }


    return {

        "exit":

        False,

        "reason":

        "TRADE ACTIVE"

    }



# ==========================
# AUTO EXIT
# ==========================

def auto_exit(current_price):

    result = monitor_position(

        current_price

    )


    if result and result["exit"]:

        close_trade()


    return result
    # ==========================
# BREAKEVEN MANAGEMENT
# ==========================

def move_to_breakeven(

    current_price

):

    trade = get_active_trade()


    if trade is None:

        return None


    entry = trade["entry"]


    side = trade["side"]


    if side == "BUY":

        if current_price > entry:

            trade["stop_loss"] = entry



    if side == "SELL":

        if current_price < entry:

            trade["stop_loss"] = entry


    return trade



# ==========================
# TRAILING STOP
# ==========================

def trailing_stop(

    current_price,

    distance

):

    trade = get_active_trade()


    if trade is None:

        return None


    side = trade["side"]


    if side == "BUY":

        new_sl = (

            current_price

            -

            distance

        )


        if new_sl > trade["stop_loss"]:

            trade["stop_loss"] = new_sl



    if side == "SELL":

        new_sl = (

            current_price

            +

            distance

        )


        if new_sl < trade["stop_loss"]:

            trade["stop_loss"] = new_sl


    return trade



# ==========================
# MANAGE TRADE
# ==========================

def manage_trade(

    current_price,

    trail_distance=None

):

    result = move_to_breakeven(

        current_price

    )


    if trail_distance:

        result = trailing_stop(

            current_price,

            trail_distance

        )


    return result
    # ==========================
# EXECUTION DEBUG PANEL
# ==========================

def debug_execution():

    status = trade_status()


    print("\n========== EXECUTION V5 ==========")

    print(

        "Status :",

        status

    )

    print(

        "Queue  :",

        len(execution_queue)

    )

    print(

        "Trades :",

        execution_state["trade_count"]

    )

    print(

        "=================================\n"

    )


    return status



# ==========================
# EXECUTION REPORT
# ==========================

def execution_report():

    trade = get_active_trade()


    return {

        "active_trade":

        trade,

        "queue_size":

        len(execution_queue),

        "trade_count":

        execution_state["trade_count"],

        "last_signal":

        execution_state["last_signal"]

    }



# ==========================
# RESET ENGINE
# ==========================

def reset_execution():

    execution_state["active_trade"] = None

    execution_state["last_signal"] = None

    execution_state["trade_count"] = 0


    execution_queue.clear()


    return True
    # ==========================
# MAIN EXECUTION FUNCTION
# ==========================

def execute_trade(

    signal,

    symbol,

    balance=0

):

    parsed = parse_signal(

        signal

    )


    if parsed is None:

        return {

            "executed":

            False,

            "reason":

            "Invalid Signal"

        }


    if not validate_signal(parsed):

        return {

            "executed":

            False,

            "reason":

            "Low Score"

        }


    order = prepare_order(

        parsed

    )


    if order is None:

        return {

            "executed":

            False,

            "reason":

            "Invalid Order"

        }


    order = attach_symbol(

        order,

        symbol

    )


    if open_trade(order):

        return {

            "executed":

            True,

            "order":

            order

        }


    return {

        "executed":

        False,

        "reason":

        "Execution Failed"

    }



# ==========================
# EXECUTION ENGINE V5
# ==========================

def execution_engine_v5(

    signal,

    symbol

):

    return execute_trade(

        signal,

        symbol

    )



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "parse_signal",

    "validate_signal",

    "prepare_order",

    "calculate_rr",

    "calculate_position_size",

    "open_trade",

    "close_trade",

    "get_active_trade",

    "monitor_position",

    "auto_exit",

    "manage_trade",

    "execute_trade",

    "execution_engine_v5",

    "debug_execution",

    "execution_report",

    "reset_execution"

]
