import os

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

    print("Bot Started...")

    best = get_best_symbol()

    if best is None:
        print("No Bullish Trend Found")
        return

    symbol = best["symbol"]

    print(f"Scanning: {symbol}")

    df = get_market_data(symbol, "5m")

    if df is None or df.empty:
        print("Market Data Failed")
        return

    swing_highs, swing_lows = find_swings(df)

    bos = detect_bos(df, swing_highs, swing_lows)
    mss = detect_mss(df, swing_highs, swing_lows)
    choch = detect_choch(df, swing_highs, swing_lows)

    liquidity = detect_liquidity_sweep(df)
    fvg = detect_fvg(df)
    order_block = detect_order_block(df)
    zone = get_premium_discount(df)

    confidence = calculate_confidence(
        bias=True,
        trend=True,
        bos=bool(bos),
        choch=bool(choch),
        mss=bool(mss),
        liquidity=bool(liquidity),
        fvg=bool(fvg),
        order_block=bool(order_block),
        btc=True,
        volume=True
    )

    last = df.iloc[-1]

    signal = {
        "signal": "BUY" if confidence["score"] >= 85 else "NO TRADE",
        "entry": round(last["close"], 2),
        "sl": round(last["close"] * 0.995, 2),
        "tp1": round(last["close"] * 1.015, 2),
        "tp2": round(last["close"] * 1.020, 2),
        "score": confidence["score"],
        "reasons": ", ".join(confidence["reasons"])
    }

    print(signal)

    send_signal(signal)


if __name__ == "__main__":
    run()
