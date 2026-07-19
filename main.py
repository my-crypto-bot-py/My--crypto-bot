import pandas as pd

# ==========================
# ICT ADVANCED MODULES
# ==========================

from sessions import (
    analyze_sessions
)


from pd_arrays import (
    get_best_pd_array,
    debug_pd_arrays
)


from ote import (
    institutional_ote_entry
)


from smt import (
    get_smt_confirmation
)


from execution import (
    create_trade_package,
    final_execution_gate
)

from config import *

from market import (
    get_market_data,
    detect_trend,
    detect_volume_confirmation
)

from structure import (
    analyze_structure
)

from smartmoney import (
    analyze_smart_money,
    generate_trade_levels
)

from confidence import (
    calculate_confidence
)

from risk import (
    validate_trade,
    can_take_trade
)

from scanner import (
    scan_market
)

from telegram_bot import (
    send_signal
)


print("========== BOT STARTED ==========")
# ==========================
# MAIN BOT
# ==========================

def run():
    
    # ==========================
    # SCAN MARKET
    # ==========================

    best = scan_market()

    if best is None:

        print("No Best Symbol Found")

        return

    symbol = best["symbol"]
    trend = best["trend"]

    print("Best Symbol:", best)
    print("Scanning:", symbol)

    # ==========================
    # MARKET DATA
    # ==========================

    df = get_market_data(
        symbol,
        TIMEFRAME,
        LIMIT
    )

    if df is None or len(df) < 100:

        print("Market Data Failed")

        return

    print("Market Data Loaded")
    # ==========================
    # ICT DATA PREPARATION
    # ==========================


    print("ICT Analysis Started")


    # Session Analysis

    session_data = analyze_sessions(df)


    print(
        "Session Data:",
        session_data
    )



    # Best PD Array

    best_poi = get_best_pd_array(df)


    print(
        "Best PD Array:",
        best_poi
    )



    # Debug PD Array

    debug_pd_arrays(df)
# ==========================
# OTE + PD ARRAY ANALYSIS
# ==========================

ote_signal = None


if best_poi:

    poi_high = best_poi["high"]

    poi_low = best_poi["low"]

    current_price = float(
        df["close"].iloc[-1]
    )


    ote_signal = institutional_ote_entry(

        price=current_price,

        high=poi_high,

        low=poi_low,

        direction=direction,

        bos=bos,

        mss=mss,

        choch=choch,

        fvg=fvg,

        order_block=order_block

    )


print(
    "OTE Signal:",
    ote_signal
)


# ==========================
# SMT ANALYSIS
# ==========================

smt_result = None


try:

    if symbol == "BTC-USDT-SWAP":

        eth_df = get_market_data(
            "ETH-USDT-SWAP",
            "5m"
        )

        sol_df = get_market_data(
            "SOL-USDT-SWAP",
            "5m"
        )

        smt_result = get_smt_confirmation(
            btc_df=df,
            eth_df=eth_df,
            sol_df=sol_df
        )

    else:

        smt_result = None


except Exception as e:

    print(
        "SMT ERROR:",
        e
    )


print(
    "SMT RESULT:",
    smt_result
)


# ==========================
# EXECUTION VALIDATION
# ==========================


execution_result = execution_signal(

    direction=direction,

    price=float(
        df["close"].iloc[-1]
    ),

    pd_array=best_poi,

    ote=ote_signal,

    structure=bos or mss or choch,

    smt=smt_result

)


print(
    "Execution Result:",
    execution_result
)
# ==========================
# CREATE FINAL TRADE
# ==========================


trade = None


if execution_result["signal"] != "NO TRADE":


    levels = generate_trade_levels(

        df,

        execution_result["signal"],

        fvg,

        order_block,

        liquidity

    )


    if levels:


        trade = create_trade_package(

            direction=execution_result["signal"],

            levels=levels,

            score=execution_result["execution_score"],

            reasons=confidence["reasons"]

        )



print(
    "Trade Package:",
    trade
)



# ==========================
# FINAL EXECUTION GATE
# ==========================


if trade:


    final_result = final_execution_gate(

        trade

    )


    print(
        "Final Execution:",
        final_result
    )


else:


    final_result = {

        "approved": False,

        "reason": "No Trade"

    }


    print(
        final_result
    )
    # ==========================
# TELEGRAM FINAL SIGNAL
# ==========================


if final_result["approved"]:


    approved_trade = final_result["trade"]


    telegram_signal = {


        "symbol": symbol,


        "signal": approved_trade["direction"],


        "entry": approved_trade["entry"],


        "sl": approved_trade["sl"],


        "tp1": approved_trade["tp1"],


        "tp2": approved_trade["tp2"],


        "rr": approved_trade.get(
            "rr",
            None
        ),


        "score": approved_trade["score"],


        "reasons": ", ".join(
            approved_trade["reasons"]
        ),


        "ote": ote_signal,


        "pd_array": best_poi,


        "smt": smt_result

    }



    print(
        "FINAL ICT SIGNAL:"
    )


    print(
        telegram_signal
    )



    try:

        send_signal(
            telegram_signal
        )


        print(
            "Telegram Sent Successfully"
        )


    except Exception as e:


        print(
            "Telegram Error:",
            e
        )



else:


    print(
        "Trade Rejected - Telegram Skipped"
    )
    # ==========================
# FINAL ICT DEBUG PANEL
# ==========================

print("\n========== ICT FINAL DEBUG ==========")


print("Symbol:", symbol)

print("Trend:", trend)

print("Direction:", direction)

print("Confidence Score:", score)

print("Zone:", zone)


print("\n--- Structure ---")

print("BOS:", bos)

print("MSS:", mss)

print("CHoCH:", choch)



print("\n--- PD ARRAY ---")

print("Best POI:", best_poi)



print("\n--- OTE ---")

print("OTE Signal:", ote_signal)



print("\n--- SMT ---")

print("SMT:", smt_result)



print("\n--- EXECUTION ---")

print("Execution Result:", execution_result)



print("\n--- FINAL ---")

print("Final Result:", final_result)


print("====================================\n")



# ==========================
# SAFE EXIT
# ==========================

if not final_result["approved"]:

    print(
        "NO VALID ICT TRADE"
    )

    return



print(
    "VALID ICT TRADE EXECUTED"
)
    # ==========================
    # STRUCTURE
    # ==========================

    structure = analyze_structure(df)

    bos = structure["bos"]
    mss = structure["mss"]
    choch = structure["choch"]

    swing_highs = structure["swing_highs"]
    swing_lows = structure["swing_lows"]

    equal_levels = structure["equal_levels"]

    print("Swing Highs:", swing_highs[-2:])
    print("Swing Lows:", swing_lows[-2:])
    print("BOS:", bos)
        # ==========================
    # SMART MONEY
    # ==========================

    sm = analyze_smart_money(df)

    liquidity = sm["liquidity"]
    fvg = sm["fvg"]
    order_block = sm["order_block"]
    fresh_ob = sm["fresh_ob"]
    zone = sm["zone"]
    displacement = sm["displacement"]
    liquidity_grab = sm["liquidity_grab"]

    # ==========================
    # VOLUME
    # ==========================

    volume = detect_volume_confirmation(df)

    # ==========================
    # CONFIDENCE
    # ==========================

    confidence = calculate_confidence(

        trend=trend,

        bos=bos,

        choch=choch,

        mss=mss,

        liquidity=liquidity,

        fvg=fvg,

        order_block=order_block,

        equal_levels=equal_levels,

        displacement=displacement,

        liquidity_grab=liquidity_grab,

        zone=zone,

        btc=True,

        volume=volume

    )

    print("Confidence:", confidence)

    direction = confidence["direction"]
    score = confidence["score"]

    signal_type = "NO TRADE"

    if score >= 65:

        signal_type = direction

    print("Direction:", direction)
    print("Score:", score)
    print("Signal:", signal_type)
        # ==========================
    # NO TRADE
    # ==========================

    if signal_type == "NO TRADE":

        print("No Trade")
        return

    # ==========================
    # TRADE LEVELS
    # ==========================

    levels = generate_trade_levels(

        df,

        signal_type,

        fvg,

        order_block,

        liquidity

    )

    if levels is None:

        print("Trade Level Failed")

        return

    # ==========================
    # RISK CHECK
    # ==========================

    risk = validate_trade(

        levels["entry"],

        levels["sl"],

        levels["tp2"]

    )

    if not risk["valid"]:

        print("Risk Reward Failed")

        return

    allowed, reason = can_take_trade()

    if not allowed:

        print(reason)

        return

    # ==========================
    # SIGNAL
    # ==========================

    signal = {

        "symbol": symbol,

        "signal": signal_type,

        "entry": levels["entry"],

        "sl": levels["sl"],

        "tp1": levels["tp1"],

        "tp2": levels["tp2"],

        "rr": risk["rr"],

        "score": score,

        "trend": trend,

        "zone": zone["zone"] if zone else "-",

        "reasons": ", ".join(
            confidence["reasons"]
        )

    }

    print(signal)

    # ==========================
    # TELEGRAM
    # ==========================

    try:

        send_signal(signal)

        print("Telegram Sent")

    except Exception as e:

        print("Telegram Error:", e)
