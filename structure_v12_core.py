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
    # ==========================
# BEARISH BOS
# ==========================

def bearish_bos(df):

    swing = get_last_swing_low(df)

    if swing is None:
        return None

    close = float(df["close"].iloc[-1])

    if close < swing["price"]:

        return {
            "type": "BOS",
            "direction": "SELL",
            "level": swing["price"],
            "index": swing["index"]
        }

    return None


# ==========================
# BOS
# ==========================

def detect_bos(df):

    bull = bullish_bos(df)
    bear = bearish_bos(df)

    if bull:
        return bull

    if bear:
        return bear

    return None


# ==========================
# BULLISH MSS
# ==========================

def bullish_mss(df):

    if len(df) < 10:
        return None

    last_low = get_last_swing_low(df)

    last_high = get_last_swing_high(df)

    if last_low is None or last_high is None:
        return None

    close = float(df["close"].iloc[-1])

    if close > last_high["price"]:

        return {
            "type": "MSS",
            "direction": "BUY",
            "level": last_high["price"]
        }

    return None


# ==========================
# BEARISH MSS
# ==========================

def bearish_mss(df):

    if len(df) < 10:
        return None

    last_low = get_last_swing_low(df)

    last_high = get_last_swing_high(df)

    if last_low is None or last_high is None:
        return None

    close = float(df["close"].iloc[-1])

    if close < last_low["price"]:

        return {
            "type": "MSS",
            "direction": "SELL",
            "level": last_low["price"]
        }

    return None


# ==========================
# MSS
# ==========================

def detect_mss(df):

    bull = bullish_mss(df)

    bear = bearish_mss(df)

    if bull:
        return bull

    if bear:
        return bear

    return None


# ==========================
# STRUCTURE
# ==========================

def detect_structure(df):

    mss = detect_mss(df)

    if mss:
        return mss

    bos = detect_bos(df)

    if bos:
        return bos

    return None


# ==========================
# STRUCTURE BIAS
# ==========================

def structure_bias(df):

    structure = detect_structure(df)

    if structure is None:
        return "RANGE"

    return structure["direction"]


# ==========================
# STRUCTURE VALID
# ==========================

def structure_valid(df):

    return detect_structure(df) is not None
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-2
# Liquidity Sweep
# Equal High / Low
# Premium / Discount
# ==========================


# ==========================
# EQUAL HIGH
# ==========================

def detect_equal_high(df, tolerance=0.0015):

    if len(df) < 10:
        return None

    highs = df["high"].values

    for i in range(len(highs) - 2, 3, -1):

        h1 = float(highs[i])
        h2 = float(highs[i - 1])

        if abs(h1 - h2) / max(h1, h2) <= tolerance:

            return {
                "type": "EQH",
                "price": (h1 + h2) / 2,
                "index": i
            }

    return None
    
# ==========================
# EQUAL LOW
# ==========================

def detect_equal_low(df, tolerance=0.0015):

    if len(df) < 10:
        return None

    lows = df["low"].values

    for i in range(len(lows) - 2, 3, -1):

        l1 = float(lows[i])
        l2 = float(lows[i - 1])

        if abs(l1 - l2) / max(l1, l2) <= tolerance:

            return {
                "type": "EQL",
                "price": (l1 + l2) / 2,
                "index": i
            }

    return None


# ==========================
# BUY SIDE LIQUIDITY
# ==========================

def detect_buy_side_liquidity(df):

    eqh = detect_equal_high(df)

    if eqh:

        return {
            "side": "BUY",
            "price": eqh["price"],
            "index": eqh["index"]
        }

    return None


# ==========================
# SELL SIDE LIQUIDITY
# ==========================

def detect_sell_side_liquidity(df):

    eql = detect_equal_low(df)

    if eql:

        return {
            "side": "SELL",
            "price": eql["price"],
            "index": eql["index"]
        }

    return None


# ==========================
# LIQUIDITY SWEEP
# ==========================

def detect_liquidity_sweep(df):

    buy = detect_buy_side_liquidity(df)
    sell = detect_sell_side_liquidity(df)

    close = float(df["close"].iloc[-1])
    high = float(df["high"].iloc[-1])
    low = float(df["low"].iloc[-1])

    if buy:

        if high > buy["price"] and close < buy["price"]:

            return {
                "direction": "SELL",
                "type": "BUY_SIDE_SWEEP",
                "level": buy["price"]
            }

    if sell:

        if low < sell["price"] and close > sell["price"]:

            return {
                "direction": "BUY",
                "type": "SELL_SIDE_SWEEP",
                "level": sell["price"]
            }

    return None

# ==========================
# DEALING RANGE
# ==========================

def get_dealing_range(df, lookback=50):

    if len(df) < lookback:
        lookback = len(df)

    high = float(df["high"].tail(lookback).max())
    low = float(df["low"].tail(lookback).min())

    return {
        "high": high,
        "low": low,
        "mid": (high + low) / 2
    }


# ==========================
# PREMIUM / DISCOUNT
# ==========================

def premium_discount_zone(df):

    dealing = get_dealing_range(df)

    price = float(df["close"].iloc[-1])

    if price > dealing["mid"]:

        return {
            "zone": "PREMIUM",
            "mid": dealing["mid"]
        }

    return {
        "zone": "DISCOUNT",
        "mid": dealing["mid"]
    }


# ==========================
# STRUCTURE CONTEXT
# ==========================

def structure_context(df):

    return {
        "structure": detect_structure(df),
        "liquidity": detect_liquidity_sweep(df),
        "zone": premium_discount_zone(df)
    }


# ==========================
# SMART MONEY VALIDATION
# ==========================

def smart_money_structure_valid(df):

    structure = detect_structure(df)
    liquidity = detect_liquidity_sweep(df)

    if structure and liquidity:

        if structure["direction"] == liquidity["direction"]:
            return True

    return False
# ==========================
# STRUCTURE ENGINE V12
# PART 2B-3
# CHoCH • Displacement • Internal BOS
# Production Ready
# ==========================

from typing import Optional, Dict


# ==========================
# DISPLACEMENT CANDLE
# ==========================

def detect_displacement(df, body_multiplier: float = 1.5) -> Optional[Dict]:

    if len(df) < 25:
        return None

    body = abs(
        float(df["close"].iloc[-1]) -
        float(df["open"].iloc[-1])
    )

    avg_body = 0.0

    for i in range(-21, -1):
        avg_body += abs(
            float(df["close"].iloc[i]) -
            float(df["open"].iloc[i])
        )

    avg_body /= 20

    if avg_body == 0:
        return None

    if body >= avg_body * body_multiplier:

        direction = (
            "BUY"
            if float(df["close"].iloc[-1]) >
               float(df["open"].iloc[-1])
            else "SELL"
        )

        return {
            "type": "DISPLACEMENT",
            "direction": direction,
            "body": body,
            "average_body": avg_body
        }

    return None


# ==========================
# INTERNAL BOS
# ==========================

def detect_internal_bos(df) -> Optional[Dict]:

    if len(df) < 15:
        return None

    last_high = max(df["high"].tail(6).iloc[:-1])
    last_low = min(df["low"].tail(6).iloc[:-1])

    close = float(df["close"].iloc[-1])

    if close > float(last_high):

        return {
            "type": "INTERNAL_BOS",
            "direction": "BUY",
            "level": float(last_high)
        }

    if close < float(last_low):

        return {
            "type": "INTERNAL_BOS",
            "direction": "SELL",
            "level": float(last_low)
        }

    return None


# ==========================
# CHoCH
# ==========================





