import time

from scanner import get_best_symbol
from market import get_market_data


from structure import (
    find_swings,
    detect_bos,
    detect_mss,
    detect_choch,
    detect_equal_levels,
    detect_displacement,
    detect_liquidity_grab
)


from smartmoney import (
    detect_liquidity_sweep,
    detect_fvg,
    detect_order_block,
    get_premium_discount,
    generate_trade_levels
)


from confidence import calculate_confidence
from telegram_bot import send_signal



def run():

    print("========== BOT STARTED ==========")


    # ==========================
    # SCANNER
    # ==========================

    best = get_best_symbol()

    print("Best Symbol:", best)


    if best is None:

        print("No Trend Found")

        return



    symbol = best["symbol"]

    trend = best["trend"]


    print("Scanning:", symbol)



    # ==========================
    # MARKET DATA
    # ==========================

    df = get_market_data(
        symbol,
        "5m"
    )


    if df is None or df.empty:

        print("Market Data Failed")

        return



    print("Market Data Loaded")



    # ==========================
    # STRUCTURE ANALYSIS
    # ==========================


    swing_highs, swing_lows = find_swings(df)


    bos = detect_bos(
        df,
        swing_highs,
        swing_lows
    )


    mss = detect_mss(
        df,
        swing_highs,
        swing_lows
    )


    choch = detect_choch(
        df,
        swing_highs,
        swing_lows
    )


    equal_levels = detect_equal_levels(
        swing_highs,
        swing_lows
    )


    displacement = detect_displacement(df)


    liquidity_grab = detect_liquidity_grab(
        df,
        swing_highs,
        swing_lows
    )



    # ==========================
    # SMART MONEY
    # ==========================


    liquidity = detect_liquidity_sweep(df)


    fvg = detect_fvg(df)


    order_block = detect_order_block(df)



    zone_data = get_premium_discount(df)


    zone = "UNKNOWN"


    if zone_data:

        zone = zone_data.get(
            "zone",
            "UNKNOWN"
        )
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

        volume=True

    )


    print("Confidence:", confidence)



    direction = confidence["direction"]

    score = confidence["score"]


    signal_type = "NO TRADE"

    # ==========================
    # STRUCTURE FILTER
    # ==========================

    structure_confirm = False

    # BOS / MSS / CHoCH
    if bos or mss or choch:
        structure_confirm = True

    # FVG + Order Block same direction
    elif (
        fvg
        and order_block
        and fvg.get("direction") == order_block.get("direction")
    ):
         structure_confirm = True

    # Liquidity + Order Block same direction
    elif (
        liquidity
        and order_block
        and liquidity.get("direction") == order_block.get("direction")
    ):
        structure_confirm = True


    # ==========================
    # SMART MONEY FILTER (FINAL)
    # ==========================

    smartmoney_confirm = False


    # Liquidity + OB confirmation
    if (
        liquidity
        and order_block
        and liquidity.get("direction") == order_block.get("direction")
    ):
        smartmoney_confirm = True


    # FVG + OB confirmation
    if (
        fvg
        and order_block
        and fvg.get("direction") == order_block.get("direction")
    ):
        smartmoney_confirm = True


    # Liquidity Grab
    if liquidity_grab:
        smartmoney_confirm = True


    # Displacement
    if (
        displacement
        and displacement.get("strength", 0) >= 2
    ):
        smartmoney_confirm = True


    # Trend + Order Block + Zone
    if order_block:

        if (
            direction == "BUY"
            and zone in ["Discount", "Deep Discount"]
        ):
            smartmoney_confirm = True


        if (
            direction == "SELL"
            and zone in ["Premium", "Deep Premium"]
        ):
            smartmoney_confirm = True
    # ==========================
    # ZONE FILTER (UPGRADE)
    # ==========================

    zone_ok = True


    # Normal SELL avoid deep discount
    if (
        direction == "SELL"
        and zone == "Deep Discount"
    ):

        if not (
            mss
            and fvg
            and order_block
        ):
            zone_ok = False


    # Normal BUY avoid deep premium
    if (
        direction == "BUY"
        and zone == "Deep Premium"
    ):

        if not (
            mss
            and fvg
            and order_block
        ):
            zone_ok = False


    # ==========================
    # DEBUG
    # ==========================


    print("\n========== DEBUG ==========")


    print("Trend:", trend)

    print("Direction:", direction)

    print("Score:", score)



    print("\n----- STRUCTURE -----")

    print("BOS:", bos)

    print("MSS:", mss)

    print("CHoCH:", choch)



    print("\n----- SMART MONEY -----")

    print("Liquidity:", liquidity)

    print("FVG:", fvg)

    print("Order Block:", order_block)



    print("\n----- ZONE -----")

    print("Zone:", zone)



    print("\n----- FILTER -----")

    print(
        "Structure Confirm:",
        bool(structure_confirm)
    )

    print(
        "Smart Money Confirm:",
        bool(smartmoney_confirm)
    )

    print(
        "Zone OK:",
        zone_ok
    )


    print("===========================\n")



    # ==========================
    # FINAL SIGNAL
    # ==========================


    if (

        score >= 65

        and

        structure_confirm

        and

        smartmoney_confirm

        and

        zone_ok

    ):


        if direction == "BUY":

            signal_type = "BUY"


        elif direction == "SELL":

            signal_type = "SELL"



    print(
        "Final Direction:",
        direction
    )


    print(
        "Final Signal:",
        signal_type
    )
    # ==========================
    # NO TRADE CHECK
    # ==========================


    if signal_type == "NO TRADE":


        print({

            "symbol": symbol,

            "signal": "NO TRADE",

            "score": score,

            "trend": trend,

            "zone": zone,

            "reasons":
            ", ".join(
                confidence["reasons"]
            )

        })


        print(
            "No Trade Signal - Telegram skipped."
        )


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


        print(
            "Trade Level Failed"
        )


        return

    # ==========================
    # RISK REWARD FILTER
    # ==========================

    risk = abs(
        levels["entry"] - levels["sl"]
    )

    reward = abs(
        levels["tp2"] - levels["entry"]
    )

    if risk == 0:
        print("Invalid Risk")
        return

    rr = reward / risk

    print("Risk:", round(risk, 2))
    print("Reward:", round(reward, 2))
    print("RR:", round(rr, 2))

    if rr < 3:

        print("Rejected: Risk Reward less than 1:3")

        return



    # ==========================
    # FINAL SIGNAL DATA
    # ==========================
        signal = {

        "symbol": symbol,

        "signal": signal_type,

        "entry": levels["entry"],

        "sl": levels["sl"],

        "tp1": levels["tp1"],

        "tp2": levels["tp2"],

        "score": score,

        "trend": trend,

        "zone": zone,

        "rr": round(rr, 2),

        "reasons": ", ".join(
            confidence["reasons"]
        ) 
    }


    print(
        "Generated Signal:"
    )

    print(signal)





    # ==========================
    # TELEGRAM
    # ==========================


    try:


        print(
            "Sending Telegram Message..."
        )


        send_signal(signal)


        print(
            "Telegram Message Sent Successfully."
        )


    except Exception as e:


        print(
            "Telegram Error:",
            e
        )




    # ==========================
    # START BOT
    # ==========================

    if __name__ == "__main__":
        run()
