import os

from market import get_ohlcv
from structure import find_swings, detect_bos, detect_mss
from smartmoney import (
    detect_liquidity_sweep,
    detect_fvg,
    detect_order_block,
    get_premium_discount
)
from signal import generate_signal
from telegram_bot import send_signal


def run_bot(symbol="BTC/USDT"):

    # 5 minute data
    df = get_ohlcv(symbol, "5m")

    if df is None:
        print("No market data")
        return


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


    # Smart Money
    liquidity = detect_liquidity_sweep(df)

    fvg = detect_fvg(df)

    order_block = detect_order_block(df)

    zone = get_premium_discount(df)


    structure = mss if mss else (
        bos[0] if bos else None
    )


    # Entry data
    entry = df["close"].iloc[-1]

    if structure and "Bullish" in str(structure):
        sl = df["low"].tail(10).min()

    else:
        sl = df["high"].tail(10).max()


    result = generate_signal(
        structure,
        liquidity,
        fvg,
        order_block,
        zone,
        entry,
        sl
    )


    print(result)


    if result["signal"] != "NO TRADE":
        send_signal(result)



if __name__ == "__main__":
    run_bot()
