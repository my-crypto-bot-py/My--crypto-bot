from scanner import get_best_symbol
from market import get_market_data

from structure import (
    find_swings,
    detect_bos,
    detect_mss,
    detect_choch
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


    best = get_best_symbol()

    print("Best Symbol:", best)


    if best is None:
        print("No Trend Found")
        return


    symbol = best["symbol"]
    trend = best["trend"]


    print("Scanning:", symbol)



    df = get_market_data(symbol, "5m")


    if df is None or df.empty:
        print("Market Data Failed")
        return


    print("Market Data Loaded")



    # Structure Detection

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



    # Smart Money

    liquidity = detect_liquidity_sweep(df)

    fvg = detect_fvg(df)

    order_block = detect_order_block(df)


    zone_data = get_premium_discount(df)

    zone = "UNKNOWN"

    if zone_data:
        zone = zone_data["zone"]



    # Confidence Calculation

    confidence = calculate_confidence(

        trend=trend,

        bos=bos,

        choch=choch,

        mss=mss,

        liquidity=liquidity,

        fvg=fvg,

        order_block=order_block,

        btc={
            "direction": trend
        },

        volume={
            "direction": trend
        }

    )


    print("Confidence:", confidence)



    signal_type = "NO TRADE"



    if confidence["score"] >= 80:


        if confidence.get("direction"):

            signal_type = confidence["direction"]


        else:

            if trend == "BULLISH":
                signal_type = "BUY"

            elif trend == "BEARISH":
                signal_type = "SELL"





    # Smart Money Entry / SL / TP

    levels = generate_trade_levels(

        df,

        signal_type,

        fvg,

        order_block

    )



    signal = {


        "symbol": symbol,


        "signal": signal_type,


        "entry": levels["entry"],


        "sl": levels["sl"],


        "tp1": levels["tp1"],


        "tp2": levels["tp2"],


        "score": confidence["score"],


        "trend": trend,


        "zone": zone,


        "reasons": ", ".join(
            confidence["reasons"]
        )

    }



    print("Generated Signal:")

    print(signal)



    if signal_type == "NO TRADE":

        print("No Trade Signal - Telegram skipped.")

        return




    try:

        print("Sending Telegram Message...")


        send_signal(signal)


        print("Telegram Message Sent Successfully.")



    except Exception as e:

        print("Telegram Error:", e)




if __name__ == "__main__":

    run()
