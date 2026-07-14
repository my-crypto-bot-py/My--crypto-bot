import pandas as pd


def calculate_atr(df, period=14):
    """
    ATR (Average True Range) calculate karta hai.
    """

    data = df.copy()

    data["previous_close"] = data["close"].shift(1)

    data["tr"] = data.apply(
        lambda x: max(
            x["high"] - x["low"],
            abs(x["high"] - x["previous_close"]),
            abs(x["low"] - x["previous_close"])
        ),
        axis=1
    )

    atr = data["tr"].rolling(period).mean()

    return atr.iloc[-1]


def volume_confirmation(df, period=20):
    """
    Volume confirmation check karta hai.
    """

    avg_volume = df["volume"].rolling(period).mean()
    current_volume = df["volume"].iloc[-1]

    if current_volume > avg_volume.iloc[-1]:
        return True

    return False
