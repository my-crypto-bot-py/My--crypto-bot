# ==========================
# ORDER BLOCK ENGINE V12
# ==========================

def detect_bullish_order_block(df):

    if len(df) < 6:
        return None

    for i in range(len(df) - 3, 1, -1):

        bearish = (
            df["close"].iloc[i] <
            df["open"].iloc[i]
        )

        impulse = (
            df["close"].iloc[i + 1] >
            df["high"].iloc[i]
        )

        if bearish and impulse:

            return {
                "direction": "BUY",
                "index": i,
                "high": float(df["high"].iloc[i]),
                "low": float(df["low"].iloc[i]),
                "open": float(df["open"].iloc[i]),
                "close": float(df["close"].iloc[i]),
                "strength": "NORMAL"
            }

    return None
