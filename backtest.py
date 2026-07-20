import pandas as pd
import numpy as np


# ==========================
# BACKTEST ENGINE V5
# ==========================

INITIAL_BALANCE = 10000

RISK_PER_TRADE = 0.01

COMMISSION = 0.0005



# ==========================
# BACKTEST STATE
# ==========================

BACKTEST_STATE = {

    "balance": INITIAL_BALANCE,

    "wins": 0,

    "losses": 0,

    "trades": 0,

    "profit": 0,

    "win_rate": 0

}



# ==========================
# PREPARE DATA
# ==========================

def prepare_backtest_data(

    df

):

    df = df.copy()


    cols = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]


    for col in cols:

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
# RESET ENGINE
# ==========================

def reset_backtest():

    BACKTEST_STATE["balance"] = INITIAL_BALANCE

    BACKTEST_STATE["wins"] = 0

    BACKTEST_STATE["losses"] = 0

    BACKTEST_STATE["trades"] = 0

    BACKTEST_STATE["profit"] = 0

    BACKTEST_STATE["win_rate"] = 0


    return True
    # ==========================
# CREATE TRADE
# ==========================

def create_trade(

    direction,

    entry,

    sl,

    tp

):

    return {

        "direction": direction,

        "entry": float(entry),

        "sl": float(sl),

        "tp": float(tp),

        "status": "OPEN",

        "result": None

    }



# ==========================
# BUY TRADE
# ==========================

def create_buy_trade(

    entry,

    sl,

    tp

):

    return create_trade(

        "BUY",

        entry,

        sl,

        tp

    )



# ==========================
# SELL TRADE
# ==========================

def create_sell_trade(

    entry,

    sl,

    tp

):

    return create_trade(

        "SELL",

        entry,

        sl,

        tp

    )



# ==========================
# TRADE LOGGER
# ==========================

def log_trade(

    trade

):

    BACKTEST_STATE["trades"] += 1

    return trade
    # ==========================
# TAKE PROFIT CHECK
# ==========================

def tp_hit(

    trade,

    candle

):

    if trade["direction"] == "BUY":

        return candle["high"] >= trade["tp"]


    return candle["low"] <= trade["tp"]



# ==========================
# STOP LOSS CHECK
# ==========================

def sl_hit(

    trade,

    candle

):

    if trade["direction"] == "BUY":

        return candle["low"] <= trade["sl"]


    return candle["high"] >= trade["sl"]



# ==========================
# CLOSE TRADE
# ==========================

def close_trade(

    trade,

    result

):

    trade["status"] = "CLOSED"

    trade["result"] = result


    if result == "WIN":

        BACKTEST_STATE["wins"] += 1

    else:

        BACKTEST_STATE["losses"] += 1


    return trade
    # ==========================
# TRADE SIMULATION
# ==========================

def simulate_trade(

    trade,

    df

):

    for _, candle in df.iterrows():

        if tp_hit(

            trade,

            candle

        ):

            return close_trade(

                trade,

                "WIN"

            )


        if sl_hit(

            trade,

            candle

        ):

            return close_trade(

                trade,

                "LOSS"

            )


    trade["status"] = "EXPIRED"

    trade["result"] = "NO_RESULT"

    return trade



# ==========================
# SINGLE TRADE BACKTEST
# ==========================

def backtest_trade(

    trade,

    df

):

    log_trade(

        trade

    )


    return simulate_trade(

        trade,

        df

    )



# ==========================
# TRADE RESULT
# ==========================

def trade_result(

    trade

):

    return {

        "status":

        trade["status"],

        "result":

        trade["result"]

    }
    # ==========================
# UPDATE BALANCE
# ==========================

def update_balance(

    trade

):

    risk = (

        BACKTEST_STATE["balance"]

        *

        RISK_PER_TRADE

    )


    if trade["result"] == "WIN":

        BACKTEST_STATE["balance"] += risk

        BACKTEST_STATE["profit"] += risk


    elif trade["result"] == "LOSS":

        BACKTEST_STATE["balance"] -= risk

        BACKTEST_STATE["profit"] -= risk


    return BACKTEST_STATE["balance"]



# ==========================
# WIN RATE
# ==========================

def calculate_win_rate():

    trades = BACKTEST_STATE["trades"]


    if trades == 0:

        return 0


    rate = (

        BACKTEST_STATE["wins"]

        /

        trades

    ) * 100


    BACKTEST_STATE["win_rate"] = round(

        rate,

        2

    )


    return BACKTEST_STATE["win_rate"]



# ==========================
# PROCESS RESULT
# ==========================

def process_trade_result(

    trade

):

    update_balance(

        trade

    )

    calculate_win_rate()


    return {

        "balance":

        BACKTEST_STATE["balance"],

        "profit":

        BACKTEST_STATE["profit"],

        "win_rate":

        BACKTEST_STATE["win_rate"]

    }
    # ==========================
# MULTIPLE TRADES
# ==========================

def run_backtest(

    trades,

    df

):

    results = []


    for trade in trades:

        completed = backtest_trade(

            trade,

            df

        )


        process_trade_result(

            completed

        )


        results.append(

            completed

        )


    return results



# ==========================
# PERFORMANCE SUMMARY
# ==========================

def performance_summary():

    return {

        "balance":

        BACKTEST_STATE["balance"],

        "profit":

        BACKTEST_STATE["profit"],

        "wins":

        BACKTEST_STATE["wins"],

        "losses":

        BACKTEST_STATE["losses"],

        "trades":

        BACKTEST_STATE["trades"],

        "win_rate":

        BACKTEST_STATE["win_rate"]

    }



# ==========================
# STATISTICS ENGINE
# ==========================

def backtest_statistics():

    return performance_summary()
    # ==========================
# DEBUG PANEL
# ==========================

def debug_backtest():

    stats = backtest_statistics()


    print("\n========== BACKTEST V5 ==========")

    print("Balance :", stats["balance"])

    print("Profit :", stats["profit"])

    print("Trades :", stats["trades"])

    print("Wins :", stats["wins"])

    print("Losses :", stats["losses"])

    print("Win Rate :", stats["win_rate"], "%")

    print("=================================\n")


    return stats



# ==========================
# BACKTEST REPORT
# ==========================

def backtest_report():

    stats = backtest_statistics()


    return {

        "balance": stats["balance"],

        "profit": stats["profit"],

        "trades": stats["trades"],

        "wins": stats["wins"],

        "losses": stats["losses"],

        "win_rate": stats["win_rate"]

    }



# ==========================
# SCANNER INTEGRATION
# ==========================

def backtest_for_scanner():

    report = backtest_report()


    return {

        "win_rate": report["win_rate"],

        "profit": report["profit"],

        "approved": report["win_rate"] >= 60

    }
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def backtest_engine(

    trades,

    df

):

    results = run_backtest(

        trades,

        df

    )


    return {

        "results":

        results,

        "summary":

        backtest_report()

    }



# ==========================
# BACKTEST ENGINE V5
# ==========================

def backtest_engine_v5(

    trades,

    df

):

    report = backtest_engine(

        trades,

        df

    )


    return {

        "summary":

        report["summary"],

        "ready":

        report["summary"]["trades"] > 0

    }



# ==========================
# TEST ENGINE
# ==========================

def test_backtest(

    trades,

    df

):

    return backtest_engine_v5(

        trades,

        df

    )
    # ==========================
# ENGINE STATUS
# ==========================

def backtest_status():

    return {

        "balance":

        BACKTEST_STATE["balance"],

        "profit":

        BACKTEST_STATE["profit"],

        "wins":

        BACKTEST_STATE["wins"],

        "losses":

        BACKTEST_STATE["losses"],

        "trades":

        BACKTEST_STATE["trades"],

        "win_rate":

        BACKTEST_STATE["win_rate"]

    }



# ==========================
# MODULE REPORT
# ==========================

def backtest_module_report(

    trades,

    df

):

    result = backtest_engine_v5(

        trades,

        df

    )


    return {

        "status":

        backtest_status(),

        "summary":

        result["summary"]

    }



# ==========================
# FINAL BACKTEST CHECK
# ==========================

def final_backtest_check():

    return (

        BACKTEST_STATE["trades"] > 0

    )
    # ==========================
# EXPORTS
# ==========================

__all__ = [

    "prepare_backtest_data",

    "reset_backtest",

    "create_trade",

    "create_buy_trade",

    "create_sell_trade",

    "log_trade",

    "tp_hit",

    "sl_hit",

    "close_trade",

    "simulate_trade",

    "backtest_trade",

    "trade_result",

    "update_balance",

    "calculate_win_rate",

    "process_trade_result",

    "run_backtest",

    "performance_summary",

    "backtest_statistics",

    "debug_backtest",

    "backtest_report",

    "backtest_for_scanner",

    "backtest_engine",

    "backtest_engine_v5",

    "test_backtest",

    "backtest_status",

    "backtest_module_report",

    "final_backtest_check"

]
