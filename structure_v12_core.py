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
# ==========================
# BEARISH ORDER BLOCK
# ==========================

def detect_bearish_order_block(df):

    if len(df) < 6:
        return None

    for i in range(len(df) - 3, 1, -1):

        bullish = (
            df["close"].iloc[i] >
            df["open"].iloc[i]
        )

        impulse = (
            df["close"].iloc[i + 1] <
            df["low"].iloc[i]
        )

        if bullish and impulse:

            return {
                "direction": "SELL",
                "index": i,
                "high": float(df["high"].iloc[i]),
                "low": float(df["low"].iloc[i]),
                "open": float(df["open"].iloc[i]),
                "close": float(df["close"].iloc[i]),
                "strength": "NORMAL"
            }

    return None


# ==========================
# LAST ORDER BLOCK
# ==========================

def detect_order_block(df):

    buy = detect_bullish_order_block(df)

    sell = detect_bearish_order_block(df)

    if buy and sell:

        if buy["index"] > sell["index"]:
            return buy
        else:
            return sell

    if buy:
        return buy

    if sell:
        return sell

    return None


# ==========================
# ORDER BLOCK RETEST
# ==========================

def order_block_retest(df, ob):

    if ob is None:
        return False

    price = float(df["close"].iloc[-1])

    if ob["direction"] == "BUY":

        return (
            price >= ob["low"] and
            price <= ob["high"]
        )

    return (
        price <= ob["high"] and
        price >= ob["low"]
    )


# ==========================
# ORDER BLOCK VALIDITY
# ==========================

def order_block_valid(df):

    ob = detect_order_block(df)

    if ob is None:
        return False

    return order_block_retest(df, ob)
