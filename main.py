import pandas as pd

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
