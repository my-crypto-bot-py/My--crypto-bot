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
     # ==========================
# STRUCTURE ENGINE V12
# PART 2B-1
# Market Structure Shift (MSS)
# Break Of Structure (BOS)
# Internal Structure
# Compatible with main.py
# ==========================

from typing import Optional, Dict


# ==========================
# SWING HIGH
# ==========================

def swing_high(df, index: int, left: int = 2, right: int = 2):

    if index < left:
        return False

    if index + right >= len(df):
        return False

    value = float(df["high"].iloc[index])

    for i in range(index - left, index):
        if float(df["high"].iloc[i]) >= value:
            return False

    for i in range(index + 1, index + right + 1):
        if float(df["high"].iloc[i]) > value:
            return False

    return True


# ==========================
# SWING LOW
# ==========================

def swing_low(df, index: int, left: int = 2, right: int = 2):

    if index < left:
        return False

    if index + right >= len(df):
        return False

    value = float(df["low"].iloc[index])

    for i in range(index - left, index):
        if float(df["low"].iloc[i]) <= value:
            return False

    for i in range(index + 1, index + right + 1):
        if float(df["low"].iloc[i]) < value:
            return False

    return True


# ==========================
# LAST SWING HIGH
# ==========================

def get_last_swing_high(df):

    for i in range(len(df) - 3, 2, -1):

        if swing_high(df, i):

            return {
                "index": i,
                "price": float(df["high"].iloc[i])
            }

    return None


# ==========================
# LAST SWING LOW
# ==========================

def get_last_swing_low(df):

    for i in range(len(df) - 3, 2, -1):

        if swing_low(df, i):

            return {
                "index": i,
                "price": float(df["low"].iloc[i])
            }

    return None


# ==========================
# BULLISH BOS
# ==========================

def bullish_bos(df):

    swing = get_last_swing_high(df)

    if swing is None:
        return None

    close = float(df["close"].iloc[-1])

    if close > swing["price"]:

        return {
            "type": "BOS",
            "direction": "BUY",
            "level": swing["price"],
            "index": swing["index"]
        }

    return None




