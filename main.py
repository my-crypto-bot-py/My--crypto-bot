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
    get_premium_discount
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


    # Structure

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


    zone = None

    if zone_data:
        zone = zone_data["zone"]


    # Confidence

    confidence = calculate_confidence(

        trend=trend,

        bos=bos,

        choch=choch,

        mss=mss,

        liquidity=liquidity,

        fvg=fvg,

        order_block=order_block,

        zone=zone,

        btc=True,

        volume=True
    )


    print(
        "Direction:",
        confidence["direction"]
    )

    print(
        "Confidence:",
        confidence["score"]
    )


    last = df.iloc[-1]

    entry = round(
        float(last["close"]),
        2
    )


    signal_type = "NO TRADE"


    if confidence["score"] >= 80:

        signal_type = confidence["direction"]



    # Risk Management

    if signal_type == "BUY":

        sl = round(
            entry * 0.995,
            2
        )

        tp1 = round(
            entry * 1.015,
            2
        )

        tp2 = round(
            entry * 1.020,
            2
        )


    elif signal_type == "SELL":

        sl = round(
            entry * 1.005,
            2
        )

        tp1 = round(
            entry * 0.985,
            2
        )

        tp2 = round(
            entry * 0.980,
            2
        )


    else:

        sl = None
        tp1 = None
        tp2 = None



    signal = {

        "symbol": symbol,

        "signal": signal_type,

        "entry": entry,

        "sl": sl,

        "tp1": tp1,

        "tp2": tp2,

        "score": confidence["score"],

        "trend": trend,

        "zone": zone if zone else "UNKNOWN",

        "reasons": ", ".join(
            confidence["reasons"]
        )

    }


    print("Generated Signal:")
    print(signal)



    if signal_type == "NO TRADE":

        print(
            "No Trade Signal - Telegram skipped."
        )

        return



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



if __name__ == "__main__":

    run()
