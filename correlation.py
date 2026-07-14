import pandas as pd


def calculate_correlation(btc_df, coin_df, period=50):
    """
    BTC aur coin ke beech correlation check karta hai.
    """

    btc_change = btc_df["close"].pct_change()
    coin_change = coin_df["close"].pct_change()

    correlation = btc_change.tail(period).corr(
        coin_change.tail(period)
    )

    return correlation


def check_btc_alignment(btc_df, coin_df):
    """
    BTC direction ke saath coin align hai ya nahi.
    """

    btc_direction = (
        "Bullish"
        if btc_df["close"].iloc[-1] > btc_df["close"].iloc[-10]
        else "Bearish"
    )

    coin_direction = (
        "Bullish"
        if coin_df["close"].iloc[-1] > coin_df["close"].iloc[-10]
        else "Bearish"
    )

    if btc_direction == coin_direction:
        return {
            "aligned": True,
            "btc": btc_direction,
            "coin": coin_direction
        }

    return {
        "aligned": False,
        "btc": btc_direction,
        "coin": coin_direction
    }
