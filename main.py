# ==========================
# ICT SMART MONEY BOT V2
# MAIN ENGINE
# ==========================


from config import *

from market import (
    get_market_data,
    detect_volume_confirmation
)

from scanner import (
    get_best_symbol
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

from pd_arrays import (
    get_best_pd_array
)

from ote import (
    institutional_ote_entry
)

from smt import (
    get_smt_confirmation
)

from execution import (
    execution_signal,
    create_trade_package,
    final_execution_gate
)

from risk import (
    validate_trade,
    can_take_trade
)

from telegram_bot import (
    send_signal
)


print("========== ICT BOT V2 STARTED ==========")



# ==========================
# MAIN FUNCTION
# ==========================


def run():


    print("\n===== SCANNING MARKET =====")


    # ==========================
    # FIND BEST SYMBOL
    # ==========================


    best = get_best_symbol()


    if best is None:

        print("No suitable symbol found")

        return



    symbol = best["symbol"]

    trend = best["trend"]


    print(
        "Selected:",
        symbol,
        trend
    )



    # ==========================
    # LOAD DATA
    # ==========================


    df = get_market_data(

        symbol,

        ENTRY_TF,

        LIMIT

    )


    if df is None or df.empty:

        print("Market data failed")

        return



    print(
        "Data Loaded:",
        len(df),
        "candles"
    )
        # ==========================
    # STRUCTURE ANALYSIS
    # ==========================


    print("\n===== STRUCTURE =====")


    structure = analyze_structure(df)


    bos = structure.get("bos")

    mss = structure.get("mss")

    choch = structure.get("choch")

    equal_levels = structure.get(
        "equal_levels"
    )


    print(
        "BOS:",
        bos
    )

    print(
        "MSS:",
        mss
    )

    print(
        "CHoCH:",
        choch
    )



    # ==========================
    # SMART MONEY ANALYSIS
    # ==========================


    print("\n===== SMART MONEY =====")


    smart = analyze_smart_money(df)


    liquidity = smart.get(
        "liquidity"
    )

    liquidity_grab = smart.get(
        "liquidity_grab"
    )

    fvg = smart.get(
        "fvg"
    )

    order_block = smart.get(
        "order_block"
    )

    displacement = smart.get(
        "displacement"
    )

    zone = smart.get(
        "zone"
    )


    print(
        "Liquidity:",
        liquidity
    )

    print(
        "FVG:",
        fvg
    )

    print(
        "Order Block:",
        order_block
    )

    print(
        "Zone:",
        zone
    )



    # ==========================
    # VOLUME CONFIRMATION
    # ==========================


    volume = detect_volume_confirmation(
        df
    )


    print(
        "Volume:",
        volume
    )
        # ==========================
    # CONFIDENCE ENGINE
    # ==========================


    print("\n===== CONFIDENCE =====")


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


    direction = confidence.get(
        "direction"
    )

    score = confidence.get(
        "score"
    )


    print(
        "Direction:",
        direction
    )

    print(
        "Confidence:",
        score
    )



    if direction is None or score < MIN_SCORE:

        print(
            "Low confidence - NO TRADE"
        )

        return



    # ==========================
    # PD ARRAY
    # ==========================


    print("\n===== PD ARRAY =====")


    best_poi = get_best_pd_array(
        df
    )


    print(
        "Best POI:",
        best_poi
    )



    # ==========================
    # OTE CONFIRMATION
    # ==========================


    ote_result = None


    if best_poi:


        poi_high = best_poi.get(
            "high"
        )

        poi_low = best_poi.get(
            "low"
        )


        if poi_high and poi_low:


            current_price = float(
                df["close"].iloc[-1]
            )


            ote_result = institutional_ote_entry(

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
        "OTE:",
        ote_result
    )



    # ==========================
    # SMT CONFIRMATION
    # ==========================


    smt_result = None


    try:


        if symbol == "BTC-USDT-SWAP":


            eth_df = get_market_data(

                "ETH-USDT-SWAP",

                ENTRY_TF,

                LIMIT

            )


            sol_df = get_market_data(

                "SOL-USDT-SWAP",

                ENTRY_TF,

                LIMIT

            )


            smt_result = get_smt_confirmation(

                btc_df=df,

                eth_df=eth_df,

                sol_df=sol_df

            )


    except Exception as e:


        print(
            "SMT Error:",
            e
        )


    print(
        "SMT:",
        smt_result
    )
        # ==========================
    # EXECUTION ENGINE
    # ==========================


    print("\n===== EXECUTION =====")


    execution = execution_signal(

        direction=direction,

        price=float(
            df["close"].iloc[-1]
        ),

        pd_array=best_poi,

        ote=ote_result,

        structure=bos or mss or choch,

        smt=smt_result

    )


    print(
        "Execution:",
        execution
    )



    if execution.get("signal") == "NO TRADE":

        print(
            "Execution rejected"
        )

        return



    # ==========================
    # TRADE LEVELS
    # ==========================


    levels = generate_trade_levels(

        df,

        execution["signal"],

        fvg,

        order_block,

        liquidity

    )


    if levels is None:

        print(
            "Trade levels failed"
        )

        return



    print(
        "Levels:",
        levels
    )



    # ==========================
    # RISK CHECK
    # ==========================


    risk = validate_trade(

        levels["entry"],

        levels["sl"],

        levels["tp2"]

    )


    if not risk["valid"]:

        print(
            "Risk reward failed"
        )

        return



    allowed, reason = can_take_trade()


    if not allowed:

        print(
            reason
        )

        return



    # ==========================
    # CREATE TRADE PACKAGE
    # ==========================


    trade = create_trade_package(

        direction=execution["signal"],

        levels=levels,

        score=score,

        reasons=confidence["reasons"]

    )


    print(
        "Trade Package:",
        trade
    )



    # ==========================
    # FINAL GATE
    # ==========================


    final_result = final_execution_gate(

        trade

    )


    print(
        "Final Result:",
        final_result
    )
        # ==========================
    # TELEGRAM SIGNAL
    # ==========================


    if final_result.get("approved"):


        approved = final_result["trade"]


        signal = {

            "symbol": symbol,

            "signal": approved["direction"],

            "entry": approved["entry"],

            "sl": approved["sl"],

            "tp1": approved["tp1"],

            "tp2": approved["tp2"],

            "score": approved["score"],

            "rr": approved.get(
                "rr",
                risk["rr"]
            ),

            "trend": trend,

            "zone": (
                zone["zone"]
                if zone
                else "N/A"
            ),

            "reasons": ", ".join(
                approved["reasons"]
            )

        }


        print(
            "\n===== FINAL SIGNAL ====="
        )

        print(
            signal
        )


        try:

            send_signal(
                signal
            )


            print(
                "Telegram Sent"
            )


        except Exception as e:


            print(
                "Telegram Error:",
                e
            )


    else:


        print(
            "NO VALID ICT TRADE"
        )



    # ==========================
    # DEBUG PANEL
    # ==========================


    print(
        "\n========== DEBUG =========="
    )


    print(
        "Symbol:",
        symbol
    )

    print(
        "Trend:",
        trend
    )

    print(
        "Direction:",
        direction
    )

    print(
        "Score:",
        score
    )

    print(
        "BOS:",
        bos
    )

    print(
        "MSS:",
        mss
    )

    print(
        "CHoCH:",
        choch
    )

    print(
        "POI:",
        best_poi
    )

    print(
        "OTE:",
        ote_result
    )

    print(
        "SMT:",
        smt_result
    )

    print(
        "=========================="
    )



# ==========================
# RUN BOT
# ==========================


if __name__ == "__main__":

    run()
