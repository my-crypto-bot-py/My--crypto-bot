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

def detect_choch(df) -> Optional[Dict]:

    bos = detect_bos(df)
    mss = detect_mss(df)

    if bos is None or mss is None:
        return None

    if bos["direction"] == mss["direction"]:

        return {
            "type": "CHOCH",
            "direction": bos["direction"],
            "level": bos["level"]
        }

    return None


# ==========================
# IMPULSE STRENGTH
# ==========================

def impulse_strength(df) -> float:

    if len(df) < 15:
        return 0.0

    high = float(df["high"].tail(10).max())
    low = float(df["low"].tail(10).min())

    move = high - low

    atr = 0.0

    for i in range(-11, -1):

        atr += (
            float(df["high"].iloc[i]) -
            float(df["low"].iloc[i])
        )

    atr /= 10

    if atr == 0:
        return 0.0

    return round(move / atr, 2)


# ==========================
# STRUCTURE SCORE
# ==========================

def structure_score(df) -> int:

    score = 0

    if detect_bos(df):
        score += 25

    if detect_mss(df):
        score += 25

    if detect_choch(df):
        score += 20

    if detect_internal_bos(df):
        score += 15

    if detect_displacement(df):
        score += 15

    return min(score, 100)


# ==========================
# STRUCTURE SUMMARY
# ==========================

def structure_summary(df):

    return {
        "bos": detect_bos(df),
        "mss": detect_mss(df),
        "choch": detect_choch(df),
        "internal_bos": detect_internal_bos(df),
        "displacement": detect_displacement(df),
        "score": structure_score(df),
        "impulse": impulse_strength(df)
    }


# ==========================
# STRUCTURE CONFIRMATION
# ==========================

def structure_confirmation(df) -> bool:

    summary = structure_summary(df)

    return summary["score"] >= 60
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-4
# Swing Failure Pattern (SFP)
# Breaker Block
# Mitigation Block
# Structure Strength
# Production Ready
# ==========================

from typing import Optional, Dict


# ==========================
# SWING FAILURE PATTERN
# ==========================

def detect_sfp(df) -> Optional[Dict]:

    if len(df) < 20:
        return None

    last_high = float(df["high"].iloc[-2])
    last_low = float(df["low"].iloc[-2])

    high = float(df["high"].iloc[-1])
    low = float(df["low"].iloc[-1])
    close = float(df["close"].iloc[-1])

    if high > last_high and close < last_high:

        return {
            "type": "SFP",
            "direction": "SELL",
            "level": last_high
        }

    if low < last_low and close > last_low:

        return {
            "type": "SFP",
            "direction": "BUY",
            "level": last_low
        }

    return None


# ==========================
# BREAKER BLOCK
# ==========================

def detect_breaker_block(df) -> Optional[Dict]:

    ob = detect_order_block(df)

    if ob is None:
        return None

    bos = detect_bos(df)

    if bos is None:
        return None

    if ob["direction"] != bos["direction"]:

        return {
            "type": "BREAKER_BLOCK",
            "direction": bos["direction"],
            "high": ob["high"],
            "low": ob["low"]
        }

    return None


# ==========================
# MITIGATION BLOCK
# ==========================

def detect_mitigation_block(df) -> Optional[Dict]:

    ob = detect_order_block(df)

    if ob is None:
        return None

    if order_block_retest(df, ob):

        return {
            "type": "MITIGATION_BLOCK",
            "direction": ob["direction"],
            "high": ob["high"],
            "low": ob["low"]
        }

    return None


# ==========================
# STRUCTURE STRENGTH
# ==========================

def structure_strength(df) -> int:

    score = 0

    if detect_bos(df):
        score += 20

    if detect_mss(df):
        score += 20

    if detect_internal_bos(df):
        score += 15

    if detect_displacement(df):
        score += 15

    if detect_sfp(df):
        score += 10

    if detect_breaker_block(df):
        score += 10

    if detect_mitigation_block(df):
        score += 10

    return min(score, 100)


# ==========================
# STRUCTURE TREND
# ==========================

def structure_trend(df) -> str:

    structure = detect_structure(df)

    if structure is None:
        return "RANGE"

    return structure["direction"]


# ==========================
# STRUCTURE REPORT
# ==========================

def structure_report(df) -> Dict:

    return {
        "trend": structure_trend(df),
        "strength": structure_strength(df),
        "bos": detect_bos(df),
        "mss": detect_mss(df),
        "choch": detect_choch(df),
        "sfp": detect_sfp(df),
        "breaker": detect_breaker_block(df),
        "mitigation": detect_mitigation_block(df)
    }


# ==========================
# FINAL STRUCTURE SIGNAL
# ==========================

def final_structure_signal(df) -> Optional[Dict]:

    report = structure_report(df)

    if report["strength"] < 60:
        return None

    return {
        "direction": report["trend"],
        "strength": report["strength"],
        "report": report
    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-5
# Structure Confluence Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Optional, Dict


# ==========================
# STRUCTURE CONFLUENCE
# ==========================

def structure_confluence(df) -> Dict:

    structure = detect_structure(df)
    bos = detect_bos(df)
    mss = detect_mss(df)
    choch = detect_choch(df)
    internal = detect_internal_bos(df)
    displacement = detect_displacement(df)
    liquidity = detect_liquidity_sweep(df)
    mitigation = detect_mitigation_block(df)
    breaker = detect_breaker_block(df)
    sfp = detect_sfp(df)

    score = 0

    if structure:
        score += 15

    if bos:
        score += 15

    if mss:
        score += 15

    if choch:
        score += 10

    if internal:
        score += 10

    if displacement:
        score += 10

    if liquidity:
        score += 10

    if mitigation:
        score += 5

    if breaker:
        score += 5

    if sfp:
        score += 5

    score = min(score, 100)

    direction = "RANGE"

    signals = []

    for item in [
        structure,
        bos,
        mss,
        choch,
        internal,
        displacement,
        liquidity,
        mitigation,
        breaker,
        sfp,
    ]:

        if item is None:
            continue

        if "direction" in item:
            signals.append(item["direction"])

    buy = signals.count("BUY")
    sell = signals.count("SELL")

    if buy > sell:
        direction = "BUY"

    elif sell > buy:
        direction = "SELL"

    return {
        "direction": direction,
        "score": score,
        "signals": len(signals)
    }


# ==========================
# HIGH PROBABILITY STRUCTURE
# ==========================

def high_probability_structure(df) -> bool:

    result = structure_confluence(df)

    return (
        result["score"] >= 70 and
        result["direction"] != "RANGE"
    )


# ==========================
# STRUCTURE ENTRY FILTER
# ==========================

def structure_entry_filter(df) -> bool:

    if not high_probability_structure(df):
        return False

    ob = detect_order_block(df)

    if ob is None:
        return False

    if not order_block_retest(df, ob):
        return False

    return True


# ==========================
# STRUCTURE EXIT FILTER
# ==========================

def structure_exit_filter(df) -> bool:

    sweep = detect_liquidity_sweep(df)

    if sweep is not None:
        return True

    sfp = detect_sfp(df)

    if sfp is not None:
        return True

    return False


# ==========================
# STRUCTURE DECISION
# ==========================

def structure_decision(df) -> Dict:

    confluence = structure_confluence(df)

    return {
        "entry": structure_entry_filter(df),
        "exit": structure_exit_filter(df),
        "direction": confluence["direction"],
        "score": confluence["score"]
    }


# ==========================
# PUBLIC API
# ==========================

def analyze_structure(df) -> Dict:

    return {
        "structure": detect_structure(df),
        "order_block": detect_order_block(df),
        "decision": structure_decision(df),
        "confluence": structure_confluence(df),
        "strength": structure_strength(df),
        "summary": structure_summary(df)
    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-6
# Final Validation Layer
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DIRECTION AGREEMENT
# ==========================

def structure_direction_agreement(df) -> Optional[str]:

    directions = []

    checks = [
        detect_structure(df),
        detect_bos(df),
        detect_mss(df),
        detect_choch(df),
        detect_internal_bos(df),
        detect_displacement(df),
        detect_liquidity_sweep(df),
    ]

    for item in checks:
        if item and "direction" in item:
            directions.append(item["direction"])

    if not directions:
        return None

    buy = directions.count("BUY")
    sell = directions.count("SELL")

    if buy > sell:
        return "BUY"

    if sell > buy:
        return "SELL"

    return None


# ==========================
# STRUCTURE QUALITY
# ==========================

def structure_quality(df) -> int:

    score = 0

    if detect_bos(df):
        score += 15

    if detect_mss(df):
        score += 20

    if detect_choch(df):
        score += 15

    if detect_internal_bos(df):
        score += 10

    if detect_displacement(df):
        score += 15

    if detect_order_block(df):
        score += 10

    if detect_liquidity_sweep(df):
        score += 10

    if detect_sfp(df):
        score += 5

    return min(score, 100)


# ==========================
# ENTRY CONFIRMATION
# ==========================

def structure_entry_confirmation(df) -> bool:

    direction = structure_direction_agreement(df)

    if direction is None:
        return False

    if structure_quality(df) < 70:
        return False

    ob = detect_order_block(df)

    if ob is None:
        return False

    if ob["direction"] != direction:
        return False

    if not order_block_retest(df, ob):
        return False

    return True


# ==========================
# STRUCTURE STATUS
# ==========================

def structure_status(df) -> str:

    if structure_entry_confirmation(df):
        return "VALID"

    if structure_quality(df) >= 50:
        return "WAIT"

    return "INVALID"


# ==========================
# COMPLETE STRUCTURE ENGINE
# ==========================

def run_structure_engine(df) -> Dict:

    return {
        "status": structure_status(df),
        "direction": structure_direction_agreement(df),
        "quality": structure_quality(df),
        "strength": structure_strength(df),
        "summary": structure_summary(df),
        "report": structure_report(df),
        "confluence": structure_confluence(df),
        "decision": structure_decision(df),
    }


# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_signal(df) -> Dict:

    result = run_structure_engine(df)

    return {
        "valid": result["status"] == "VALID",
        "direction": result["direction"],
        "score": result["quality"],
        "data": result
    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-7
# Institutional Structure Filter
# Final Optimization Layer
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# TREND ALIGNMENT
# ==========================

def structure_trend_alignment(df) -> bool:

    structure = detect_structure(df)
    bos = detect_bos(df)

    if structure is None or bos is None:
        return False

    return structure["direction"] == bos["direction"]


# ==========================
# MOMENTUM CONFIRMATION
# ==========================

def structure_momentum_confirmation(df) -> bool:

    displacement = detect_displacement(df)

    if displacement is None:
        return False

    return impulse_strength(df) >= 2.0


# ==========================
# SMART MONEY CONFIRMATION
# ==========================

def smart_money_confirmation(df) -> bool:

    liquidity = detect_liquidity_sweep(df)
    mitigation = detect_mitigation_block(df)

    if liquidity is None:
        return False

    if mitigation is None:
        return False

    return liquidity["direction"] == mitigation["direction"]


# ==========================
# INSTITUTIONAL STRUCTURE
# ==========================

def institutional_structure(df) -> Dict:

    score = 0

    if structure_trend_alignment(df):
        score += 25

    if structure_momentum_confirmation(df):
        score += 25

    if smart_money_confirmation(df):
        score += 25

    if structure_entry_confirmation(df):
        score += 25

    score = min(score, 100)

    return {
        "institutional_score": score,
        "institutional_valid": score >= 75
    }


# ==========================
# FINAL STRUCTURE FILTER
# ==========================

def final_structure_filter(df) -> bool:

    institutional = institutional_structure(df)

    if not institutional["institutional_valid"]:
        return False

    if structure_quality(df) < 75:
        return False

    return True


# ==========================
# STRUCTURE CONFIDENCE
# ==========================

def structure_confidence(df) -> int:

    confidence = structure_quality(df)

    institutional = institutional_structure(df)

    confidence += institutional["institutional_score"] // 4

    return min(confidence, 100)


# ==========================
# FINAL STRUCTURE OUTPUT
# ==========================

def structure_engine_v12(df) -> Dict:

    signal = get_structure_signal(df)

    signal["institutional"] = institutional_structure(df)
    signal["confidence"] = structure_confidence(df)
    signal["approved"] = final_structure_filter(df)

    return signal


# ==========================
# MAIN.PY ENTRY POINT
# ==========================

def analyze_market_structure(df) -> Dict:

    return structure_engine_v12(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-8
# Multi-Timeframe Structure
# Final Institutional Layer
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# HTF STRUCTURE
# ==========================

def htf_structure_bias(htf_df) -> str:

    signal = detect_structure(htf_df)

    if signal is None:
        return "RANGE"

    return signal["direction"]


# ==========================
# LTF STRUCTURE
# ==========================

def ltf_structure_bias(ltf_df) -> str:

    signal = detect_structure(ltf_df)

    if signal is None:
        return "RANGE"

    return signal["direction"]


# ==========================
# MTF ALIGNMENT
# ==========================

def mtf_structure_alignment(htf_df, ltf_df) -> bool:

    htf = htf_structure_bias(htf_df)
    ltf = ltf_structure_bias(ltf_df)

    if htf == "RANGE":
        return False

    if ltf == "RANGE":
        return False

    return htf == ltf


# ==========================
# MTF SCORE
# ==========================

def mtf_structure_score(htf_df, ltf_df) -> int:

    score = structure_quality(ltf_df)

    if mtf_structure_alignment(htf_df, ltf_df):
        score += 20

    if detect_displacement(htf_df):
        score += 10

    if detect_bos(htf_df):
        score += 10

    return min(score, 100)


# ==========================
# MTF CONFIRMATION
# ==========================

def mtf_structure_confirmation(htf_df, ltf_df) -> bool:

    if not mtf_structure_alignment(htf_df, ltf_df):
        return False

    if mtf_structure_score(htf_df, ltf_df) < 80:
        return False

    return True


# ==========================
# ENTRY PERMISSION
# ==========================

def allow_structure_entry(htf_df, ltf_df) -> bool:

    if not mtf_structure_confirmation(htf_df, ltf_df):
        return False

    if not structure_entry_confirmation(ltf_df):
        return False

    return True


# ==========================
# FINAL MTF ENGINE
# ==========================

def structure_engine_mtf(htf_df, ltf_df) -> Dict:

    return {
        "htf_bias": htf_structure_bias(htf_df),
        "ltf_bias": ltf_structure_bias(ltf_df),
        "alignment": mtf_structure_alignment(htf_df, ltf_df),
        "score": mtf_structure_score(htf_df, ltf_df),
        "entry": allow_structure_entry(htf_df, ltf_df)
    }


# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_structure_mtf(htf_df, ltf_df) -> Dict:

    return structure_engine_mtf(htf_df, ltf_df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-9
# Advanced ICT Validation Layer
# Liquidity + OB + FVG + Structure Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# FAIR VALUE GAP DETECTION
# ==========================

def detect_fvg(df) -> Optional[Dict]:

    if len(df) < 5:
        return None

    for i in range(len(df) - 3, 1, -1):

        high_1 = float(df["high"].iloc[i - 1])
        low_1 = float(df["low"].iloc[i - 1])

        high_3 = float(df["high"].iloc[i + 1])
        low_3 = float(df["low"].iloc[i + 1])

        if low_3 > high_1:

            return {
                "type": "BULLISH_FVG",
                "direction": "BUY",
                "high": low_3,
                "low": high_1,
                "index": i
            }

        if high_3 < low_1:

            return {
                "type": "BEARISH_FVG",
                "direction": "SELL",
                "high": low_1,
                "low": high_3,
                "index": i
            }

    return None


# ==========================
# FVG RETEST
# ==========================

def fvg_retest(df, fvg) -> bool:

    if fvg is None:
        return False

    price = float(df["close"].iloc[-1])

    return (
        price <= fvg["high"] and
        price >= fvg["low"]
    )


# ==========================
# ICT ENTRY ALIGNMENT
# ==========================

def ict_alignment(df) -> Dict:

    structure = detect_structure(df)
    ob = detect_order_block(df)
    fvg = detect_fvg(df)
    liquidity = detect_liquidity_sweep(df)

    score = 0
    direction = "RANGE"

    if structure:
        score += 20
        direction = structure["direction"]

    if ob:
        score += 20

        if direction == "RANGE":
            direction = ob["direction"]

    if fvg:
        score += 20

        if direction == "RANGE":
            direction = fvg["direction"]

    if liquidity:
        score += 25

        if direction == "RANGE":
            direction = liquidity["direction"]

    if fvg_retest(df, fvg):
        score += 15


    return {
        "direction": direction,
        "score": min(score,100),
        "structure": structure,
        "order_block": ob,
        "fvg": fvg,
        "liquidity": liquidity
    }


# ==========================
# ICT HIGH PROBABILITY SETUP
# ==========================

def ict_high_probability_setup(df) -> bool:

    result = ict_alignment(df)

    if result["score"] < 75:
        return False

    if result["direction"] == "RANGE":
        return False

    return True


# ==========================
# FINAL ICT STRUCTURE FILTER
# ==========================

def ict_structure_filter(df) -> Dict:

    result = ict_alignment(df)

    return {
        "valid": ict_high_probability_setup(df),
        "direction": result["direction"],
        "score": result["score"],
        "data": result
    }


# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_ict_structure_signal(df) -> Dict:

    return ict_structure_filter(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-10
# Advanced Market Delivery Engine
# Liquidity Target + Entry Validation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# LIQUIDITY TARGET DETECTION
# ==========================

def detect_liquidity_target(df) -> Optional[Dict]:

    if len(df) < 20:
        return None

    recent_high = float(df["high"].tail(20).max())
    recent_low = float(df["low"].tail(20).min())

    price = float(df["close"].iloc[-1])

    distance_high = abs(recent_high - price)
    distance_low = abs(recent_low - price)

    if distance_high < distance_low:

        return {
            "target": "BUY_SIDE",
            "price": recent_high,
            "distance": distance_high
        }

    return {
        "target": "SELL_SIDE",
        "price": recent_low,
        "distance": distance_low
    }


# ==========================
# PREMIUM DISCOUNT ENTRY
# ==========================

def entry_zone_validation(df) -> Dict:

    zone = premium_discount_zone(df)

    structure = detect_structure(df)

    if structure is None:

        return {
            "valid": False,
            "zone": zone["zone"]
        }


    if structure["direction"] == "BUY":

        valid = zone["zone"] == "DISCOUNT"

    else:

        valid = zone["zone"] == "PREMIUM"


    return {
        "valid": valid,
        "zone": zone["zone"]
    }


# ==========================
# SMART MONEY DELIVERY
# ==========================

def smart_money_delivery(df) -> Dict:

    liquidity = detect_liquidity_target(df)
    entry_zone = entry_zone_validation(df)
    structure = detect_structure(df)

    score = 0


    if structure:
        score += 25


    if liquidity:
        score += 25


    if entry_zone["valid"]:
        score += 25


    if detect_liquidity_sweep(df):

        score += 25


    direction = "RANGE"

    if structure:

        direction = structure["direction"]


    return {

        "direction": direction,

        "score": min(score,100),

        "liquidity_target": liquidity,

        "entry_zone": entry_zone

    }



# ==========================
# INSTITUTIONAL ENTRY CHECK
# ==========================

def institutional_entry_check(df) -> bool:

    delivery = smart_money_delivery(df)


    if delivery["score"] < 75:
        return False


    if delivery["direction"] == "RANGE":
        return False


    return True



# ==========================
# FINAL DELIVERY REPORT
# ==========================

def market_delivery_report(df) -> Dict:


    return {

        "delivery": smart_money_delivery(df),

        "institutional_entry":
            institutional_entry_check(df),

        "structure":
            detect_structure(df),

        "order_block":
            detect_order_block(df),

        "fvg":
            detect_fvg(df),

        "liquidity":
            detect_liquidity_sweep(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_structure_v12(df) -> Dict:

    report = market_delivery_report(df)

    return {

        "valid":
            report["institutional_entry"],

        "direction":
            report["delivery"]["direction"],

        "score":
            report["delivery"]["score"],

        "data":
            report

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-11
# Advanced ICT Execution Layer
# Killzone + Liquidity Raid + Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# LIQUIDITY RAID CONFIRMATION
# ==========================

def liquidity_raid_confirmation(df) -> Optional[Dict]:

    sweep = detect_liquidity_sweep(df)

    if sweep is None:
        return None

    structure = detect_structure(df)

    if structure is None:
        return None

    if sweep["direction"] == structure["direction"]:

        return {
            "confirmed": True,
            "direction": sweep["direction"],
            "type": "LIQUIDITY_RAID"
        }

    return None


# ==========================
# MARKET SHIFT CONFIRMATION
# ==========================

def market_shift_confirmation(df) -> Optional[Dict]:

    mss = detect_mss(df)
    choch = detect_choch(df)

    if mss:

        return {
            "confirmed": True,
            "direction": mss["direction"],
            "type": "MSS"
        }

    if choch:

        return {
            "confirmed": True,
            "direction": choch["direction"],
            "type": "CHOCH"
        }

    return None


# ==========================
# EXECUTION CONFLUENCE
# ==========================

def execution_confluence(df) -> Dict:

    score = 0

    direction = "RANGE"

    raid = liquidity_raid_confirmation(df)
    shift = market_shift_confirmation(df)
    ob = detect_order_block(df)
    fvg = detect_fvg(df)
    displacement = detect_displacement(df)


    if raid:

        score += 25
        direction = raid["direction"]


    if shift:

        score += 25
        direction = shift["direction"]


    if ob:

        score += 20

        if direction == "RANGE":
            direction = ob["direction"]


    if fvg:

        score += 15


    if displacement:

        score += 15


    return {

        "direction": direction,

        "score": min(score,100),

        "liquidity_raid": raid,

        "market_shift": shift,

        "order_block": ob,

        "fvg": fvg,

        "displacement": displacement

    }



# ==========================
# EXECUTION VALIDATION
# ==========================

def execution_validation(df) -> bool:

    result = execution_confluence(df)


    if result["score"] < 80:
        return False


    if result["direction"] == "RANGE":
        return False


    return True



# ==========================
# FINAL EXECUTION SIGNAL
# ==========================

def execution_signal(df) -> Dict:

    result = execution_confluence(df)


    return {

        "valid":
            execution_validation(df),

        "direction":
            result["direction"],

        "score":
            result["score"],

        "data":
            result

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_structure(df) -> Dict:

    return execution_signal(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-12
# Advanced ICT Risk & Trade Location Layer
# Entry Quality + Stop Hunt Protection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# TRUE RANGE CALCULATION
# ==========================

def structure_true_range(df) -> float:

    if len(df) < 5:
        return 0.0

    high = float(df["high"].iloc[-1])
    low = float(df["low"].iloc[-1])

    return high - low


# ==========================
# ATR STRUCTURE VOLATILITY
# ==========================

def structure_atr(df, period: int = 14) -> float:

    if len(df) < period + 1:
        return 0.0

    total = 0.0

    for i in range(-period, 0):

        high = float(df["high"].iloc[i])
        low = float(df["low"].iloc[i])
        prev = float(df["close"].iloc[i-1])

        tr = max(
            high - low,
            abs(high - prev),
            abs(low - prev)
        )

        total += tr

    return total / period


# ==========================
# SMART STOP LOSS LEVEL
# ==========================

def calculate_structure_sl(df, direction: str) -> Optional[float]:

    atr = structure_atr(df)

    if atr == 0:
        return None


    if direction == "BUY":

        swing = get_last_swing_low(df)

        if swing:

            return round(
                swing["price"] - atr * 0.5,
                4
            )


    if direction == "SELL":

        swing = get_last_swing_high(df)

        if swing:

            return round(
                swing["price"] + atr * 0.5,
                4
            )


    return None



# ==========================
# SMART TARGET LEVEL
# ==========================

def calculate_structure_tp(df, direction: str) -> Optional[float]:

    liquidity = detect_liquidity_target(df)

    if liquidity is None:
        return None


    if direction == "BUY":

        if liquidity["target"] == "BUY_SIDE":

            return liquidity["price"]


    if direction == "SELL":

        if liquidity["target"] == "SELL_SIDE":

            return liquidity["price"]


    return None



# ==========================
# RISK REWARD VALIDATION
# ==========================

def risk_reward_validation(
        df,
        direction: str,
        entry: float
):

    sl = calculate_structure_sl(df, direction)

    tp = calculate_structure_tp(df, direction)


    if sl is None or tp is None:
        return None


    risk = abs(entry - sl)

    reward = abs(tp - entry)


    if risk == 0:
        return None


    rr = round(
        reward / risk,
        2
    )


    return {

        "entry": entry,

        "sl": sl,

        "tp": tp,

        "rr": rr,

        "valid": rr >= 2

    }



# ==========================
# FINAL TRADE LOCATION
# ==========================

def trade_location_engine(df) -> Dict:

    execution = execution_confluence(df)

    direction = execution["direction"]

    entry = float(df["close"].iloc[-1])


    risk = None


    if direction != "RANGE":

        risk = risk_reward_validation(
            df,
            direction,
            entry
        )


    return {

        "direction": direction,

        "execution_score":
            execution["score"],

        "risk_reward":
            risk

    }



# ==========================
# FINAL V12 STRUCTURE APPROVAL
# ==========================

def structure_trade_approval(df) -> Dict:

    location = trade_location_engine(df)


    approved = False


    if location["risk_reward"]:

        if (
            location["execution_score"] >= 80
            and
            location["risk_reward"]["valid"]
        ):

            approved = True


    return {

        "approved": approved,

        "direction":
            location["direction"],

        "data": location

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_trade_signal(df) -> Dict:

    return structure_trade_approval(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-13
# Advanced ICT Entry Timing Layer
# OTE + Retracement + Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# OTE ZONE CALCULATION
# ==========================

def calculate_ote_zone(df) -> Optional[Dict]:

    high = get_last_swing_high(df)

    low = get_last_swing_low(df)


    if high is None or low is None:
        return None


    high_price = high["price"]
    low_price = low["price"]


    diff = high_price - low_price


    return {

        "high": high_price,

        "low": low_price,

        "ote_62":

            high_price - (diff * 0.62),

        "ote_79":

            high_price - (diff * 0.79)

    }



# ==========================
# OTE VALIDATION
# ==========================

def validate_ote_entry(df, direction: str) -> bool:

    ote = calculate_ote_zone(df)


    if ote is None:
        return False


    price = float(df["close"].iloc[-1])


    if direction == "BUY":

        return (
            price <= ote["ote_62"]
            and
            price >= ote["ote_79"]
        )


    if direction == "SELL":

        return (
            price >= ote["ote_62"]
            and
            price <= ote["ote_79"]
        )


    return False



# ==========================
# RETRACEMENT DEPTH
# ==========================

def calculate_retracement(df) -> float:

    high = float(df["high"].tail(20).max())

    low = float(df["low"].tail(20).min())

    price = float(df["close"].iloc[-1])


    if high == low:
        return 0


    return round(
        ((high - price) /
        (high - low)) * 100,
        2
    )



# ==========================
# ENTRY TIMING SCORE
# ==========================

def entry_timing_score(df) -> int:

    score = 0


    structure = detect_structure(df)

    displacement = detect_displacement(df)

    fvg = detect_fvg(df)

    ob = detect_order_block(df)


    if structure:
        score += 25


    if displacement:
        score += 20


    if fvg:
        score += 20


    if ob:
        score += 20


    if validate_ote_entry(
        df,
        structure["direction"]
    ) if structure else False:

        score += 15


    return min(score,100)



# ==========================
# ICT ENTRY TIMING ENGINE
# ==========================

def ict_entry_timing(df) -> Dict:


    structure = detect_structure(df)

    direction = "RANGE"


    if structure:

        direction = structure["direction"]


    return {

        "direction": direction,

        "timing_score":
            entry_timing_score(df),

        "ote":
            calculate_ote_zone(df),

        "retracement":
            calculate_retracement(df)

    }



# ==========================
# ENTRY READY CHECK
# ==========================

def entry_ready(df) -> bool:


    timing = ict_entry_timing(df)


    if timing["direction"] == "RANGE":
        return False


    if timing["timing_score"] < 75:
        return False


    return True



# ==========================
# FINAL EXECUTION OUTPUT
# ==========================

def get_entry_timing_signal(df) -> Dict:


    result = ict_entry_timing(df)


    return {

        "valid":
            entry_ready(df),

        "direction":
            result["direction"],

        "score":
            result["timing_score"],

        "data":
            result

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-14
# Advanced ICT Final Confluence Layer
# Structure + Liquidity + OTE + Execution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# FINAL CONFLUENCE SCORE
# ==========================

def final_confluence_score(df) -> int:

    score = 0


    structure = detect_structure(df)
    bos = detect_bos(df)
    mss = detect_mss(df)
    liquidity = detect_liquidity_sweep(df)
    ob = detect_order_block(df)
    fvg = detect_fvg(df)
    displacement = detect_displacement(df)


    if structure:
        score += 15


    if bos:
        score += 10


    if mss:
        score += 15


    if liquidity:
        score += 15


    if ob:
        score += 10


    if fvg:
        score += 10


    if displacement:
        score += 10


    if structure and validate_ote_entry(
        df,
        structure["direction"]
    ):
        score += 15


    return min(score,100)



# ==========================
# FINAL MARKET DIRECTION
# ==========================

def final_market_direction(df) -> str:

    signals = []


    checks = [

        detect_structure(df),

        detect_bos(df),

        detect_mss(df),

        detect_liquidity_sweep(df),

        detect_order_block(df),

    ]


    for item in checks:

        if item and "direction" in item:

            signals.append(
                item["direction"]
            )


    if not signals:

        return "RANGE"


    buy = signals.count("BUY")

    sell = signals.count("SELL")


    if buy > sell:

        return "BUY"


    if sell > buy:

        return "SELL"


    return "RANGE"



# ==========================
# FALSE BREAK PROTECTION
# ==========================

def false_break_protection(df) -> bool:


    sfp = detect_sfp(df)

    sweep = detect_liquidity_sweep(df)


    if sfp:

        return False


    if sweep:

        return False


    return True



# ==========================
# FINAL ICT VALIDATION
# ==========================

def final_ict_validation(df) -> Dict:


    direction = final_market_direction(df)

    score = final_confluence_score(df)


    valid = True


    if direction == "RANGE":

        valid = False


    if score < 80:

        valid = False


    if not false_break_protection(df):

        valid = False



    return {

        "valid": valid,

        "direction": direction,

        "score": score,

        "false_break_filter":
            false_break_protection(df)

    }



# ==========================
# V12 FINAL STRUCTURE SIGNAL
# ==========================

def structure_v12_signal(df) -> Dict:


    validation = final_ict_validation(df)


    return {

        "signal":

            "VALID"
            if validation["valid"]
            else "WAIT",


        "direction":

            validation["direction"],


        "confidence":

            validation["score"],


        "data":

            validation

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_v12_structure_signal(df) -> Dict:

    return structure_v12_signal(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-15
# Advanced ICT Market State Engine
# Trend Phase + Accumulation + Distribution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# MARKET PHASE DETECTION
# ==========================

def detect_market_phase(df) -> str:

    if len(df) < 30:
        return "UNKNOWN"


    high = float(df["high"].tail(30).max())

    low = float(df["low"].tail(30).min())

    price = float(df["close"].iloc[-1])


    range_size = high - low


    if range_size == 0:
        return "RANGE"


    position = (
        (price - low) /
        range_size
    )


    if position > 0.75:

        return "MARKUP"


    if position < 0.25:

        return "MARKDOWN"


    return "ACCUMULATION"



# ==========================
# VOLATILITY STATE
# ==========================

def volatility_state(df) -> str:


    atr = structure_atr(df)


    if atr == 0:

        return "NORMAL"


    candle = structure_true_range(df)


    ratio = candle / atr


    if ratio > 2:

        return "HIGH"


    if ratio < 0.5:

        return "LOW"


    return "NORMAL"



# ==========================
# TREND STRENGTH
# ==========================

def trend_strength(df) -> int:


    score = 0


    if detect_bos(df):

        score += 25


    if detect_mss(df):

        score += 25


    if detect_displacement(df):

        score += 20


    if impulse_strength(df) >= 2:

        score += 15


    if detect_order_block(df):

        score += 15


    return min(score,100)



# ==========================
# MARKET STATE ENGINE
# ==========================

def market_state(df) -> Dict:


    direction = final_market_direction(df)


    return {

        "phase":

            detect_market_phase(df),


        "direction":

            direction,


        "trend_strength":

            trend_strength(df),


        "volatility":

            volatility_state(df)

    }



# ==========================
# SMART MONEY CONDITION
# ==========================

def smart_money_condition(df) -> bool:


    state = market_state(df)


    if state["trend_strength"] < 60:

        return False


    if state["phase"] == "UNKNOWN":

        return False


    if state["direction"] == "RANGE":

        return False


    return True



# ==========================
# MARKET BIAS OUTPUT
# ==========================

def get_market_bias(df) -> Dict:


    state = market_state(df)


    return {

        "bias":

            state["direction"],


        "phase":

            state["phase"],


        "strength":

            state["trend_strength"],


        "trade_allowed":

            smart_money_condition(df),


        "data":

            state

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_market_state(df) -> Dict:

    return get_market_bias(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-16
# Advanced ICT Session & Liquidity Timing Layer
# Killzone + Session Bias + Liquidity Window
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict
from datetime import datetime, timezone


# ==========================
# SESSION DETECTION
# ==========================

def get_market_session(hour: int) -> str:

    if 0 <= hour < 7:

        return "ASIA"


    if 7 <= hour < 12:

        return "LONDON"


    if 12 <= hour < 17:

        return "NEW_YORK"


    if 17 <= hour < 21:

        return "NY_CLOSE"


    return "OFF"



# ==========================
# KILLZONE DETECTION
# ==========================

def detect_killzone() -> Dict:

    hour = datetime.now(
        timezone.utc
    ).hour


    session = get_market_session(hour)


    active = session in [
        "LONDON",
        "NEW_YORK"
    ]


    return {

        "session": session,

        "active": active,

        "hour": hour

    }



# ==========================
# SESSION LIQUIDITY BIAS
# ==========================

def session_liquidity_bias(df) -> Dict:


    liquidity = detect_liquidity_sweep(df)


    if liquidity:

        return {

            "direction":
                liquidity["direction"],

            "type":
                "LIQUIDITY_TAKEN"

        }


    return {

        "direction":
            "NONE",

        "type":
            "WAIT"

    }



# ==========================
# SESSION STRUCTURE SCORE
# ==========================

def session_structure_score(df) -> int:


    score = 0


    killzone = detect_killzone()

    structure = detect_structure(df)

    liquidity = detect_liquidity_sweep(df)


    if killzone["active"]:

        score += 20


    if structure:

        score += 30


    if liquidity:

        score += 30


    if detect_displacement(df):

        score += 20


    return min(score,100)



# ==========================
# ICT SESSION VALIDATION
# ==========================

def session_trade_validation(df) -> bool:


    score = session_structure_score(df)


    if score < 70:

        return False


    direction = final_market_direction(df)


    if direction == "RANGE":

        return False


    return True



# ==========================
# SESSION ENGINE OUTPUT
# ==========================

def session_structure_engine(df) -> Dict:


    return {

        "killzone":

            detect_killzone(),


        "liquidity":

            session_liquidity_bias(df),


        "score":

            session_structure_score(df),


        "direction":

            final_market_direction(df),


        "valid":

            session_trade_validation(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_session_structure(df) -> Dict:

    return session_structure_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-17
# Advanced ICT Premium Execution Filter
# Liquidity + OB + FVG + OTE Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# ORDER BLOCK QUALITY
# ==========================

def order_block_quality(df) -> int:

    ob = detect_order_block(df)

    if ob is None:
        return 0


    score = 0


    if ob["strength"] == "NORMAL":

        score += 20


    if order_block_retest(df, ob):

        score += 30


    displacement = detect_displacement(df)

    if displacement:

        if displacement["direction"] == ob["direction"]:

            score += 25


    structure = detect_structure(df)

    if structure:

        if structure["direction"] == ob["direction"]:

            score += 25


    return min(score,100)



# ==========================
# FVG QUALITY
# ==========================

def fvg_quality(df) -> int:

    fvg = detect_fvg(df)


    if fvg is None:

        return 0


    score = 20


    if fvg_retest(df, fvg):

        score += 30


    structure = detect_structure(df)


    if structure:

        if structure["direction"] == fvg["direction"]:

            score += 30


    if detect_displacement(df):

        score += 20


    return min(score,100)



# ==========================
# LIQUIDITY QUALITY
# ==========================

def liquidity_quality(df) -> int:

    sweep = detect_liquidity_sweep(df)


    if sweep is None:

        return 0


    score = 50


    structure = detect_structure(df)


    if structure:

        if structure["direction"] == sweep["direction"]:

            score += 30


    if detect_sfp(df):

        score += 20


    return min(score,100)



# ==========================
# ICT PREMIUM SCORE
# ==========================

def ict_premium_score(df) -> int:

    total = 0


    total += order_block_quality(df) * 0.35

    total += fvg_quality(df) * 0.25

    total += liquidity_quality(df) * 0.25

    total += structure_quality(df) * 0.15


    return int(min(total,100))



# ==========================
# PREMIUM ENTRY FILTER
# ==========================

def premium_entry_filter(df) -> bool:


    score = ict_premium_score(df)


    direction = final_market_direction(df)


    if direction == "RANGE":

        return False


    if score < 80:

        return False


    return True



# ==========================
# PREMIUM EXECUTION REPORT
# ==========================

def premium_execution_report(df) -> Dict:


    return {

        "valid":

            premium_entry_filter(df),


        "direction":

            final_market_direction(df),


        "score":

            ict_premium_score(df),


        "order_block":

            order_block_quality(df),


        "fvg":

            fvg_quality(df),


        "liquidity":

            liquidity_quality(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_premium_structure_signal(df) -> Dict:

    return premium_execution_report(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-18
# Advanced ICT Final Entry Engine
# Bias + Confluence + Execution Approval
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# ENTRY DIRECTION CONFIRMATION
# ==========================

def entry_direction_confirmation(df) -> Optional[str]:

    signals = []


    checks = [

        detect_structure(df),

        detect_bos(df),

        detect_mss(df),

        detect_order_block(df),

        detect_fvg(df),

        detect_liquidity_sweep(df)

    ]


    for item in checks:

        if item and "direction" in item:

            signals.append(
                item["direction"]
            )


    if not signals:

        return None


    buy = signals.count("BUY")

    sell = signals.count("SELL")


    if buy > sell:

        return "BUY"


    if sell > buy:

        return "SELL"


    return None



# ==========================
# ENTRY CONFLUENCE MATRIX
# ==========================

def entry_confluence_matrix(df) -> Dict:

    direction = entry_direction_confirmation(df)

    score = 0


    if detect_structure(df):

        score += 15


    if detect_bos(df):

        score += 10


    if detect_mss(df):

        score += 15


    if detect_liquidity_sweep(df):

        score += 15


    if detect_order_block(df):

        score += 15


    if detect_fvg(df):

        score += 10


    if detect_displacement(df):

        score += 10


    if direction and validate_ote_entry(
        df,
        direction
    ):

        score += 10



    return {

        "direction":
            direction or "RANGE",

        "score":
            min(score,100)

    }



# ==========================
# ENTRY QUALITY CHECK
# ==========================

def entry_quality_check(df) -> bool:


    result = entry_confluence_matrix(df)


    if result["direction"] == "RANGE":

        return False


    if result["score"] < 85:

        return False


    return True



# ==========================
# FINAL ENTRY ENGINE
# ==========================

def final_entry_engine(df) -> Dict:


    matrix = entry_confluence_matrix(df)


    return {

        "approved":

            entry_quality_check(df),


        "direction":

            matrix["direction"],


        "confidence":

            matrix["score"],


        "structure":

            detect_structure(df),


        "order_block":

            detect_order_block(df),


        "fvg":

            detect_fvg(df),


        "liquidity":

            detect_liquidity_sweep(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_final_entry_signal(df) -> Dict:

    return final_entry_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-19
# Advanced ICT Trade Management Layer
# Entry Protection + Target Mapping
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# ENTRY PRICE ENGINE
# ==========================

def get_structure_entry_price(df) -> float:

    return float(
        df["close"].iloc[-1]
    )



# ==========================
# STOP LOSS PROTECTION
# ==========================

def protected_structure_sl(
        df,
        direction: str
) -> Optional[float]:


    atr = structure_atr(df)


    if atr == 0:

        return None


    if direction == "BUY":

        swing = get_last_swing_low(df)


        if swing:

            return round(
                swing["price"] -
                (atr * 0.3),
                4
            )


    if direction == "SELL":

        swing = get_last_swing_high(df)


        if swing:

            return round(
                swing["price"] +
                (atr * 0.3),
                4
            )


    return None



# ==========================
# LIQUIDITY TARGET MAP
# ==========================

def liquidity_target_map(
        df,
        direction: str
) -> Optional[float]:


    high = float(
        df["high"].tail(50).max()
    )


    low = float(
        df["low"].tail(50).min()
    )


    if direction == "BUY":

        return high


    if direction == "SELL":

        return low


    return None



# ==========================
# MULTI TARGET ENGINE
# ==========================

def calculate_targets(
        df,
        direction: str
) -> Dict:


    entry = get_structure_entry_price(df)

    sl = protected_structure_sl(
        df,
        direction
    )


    if sl is None:

        return {}


    risk = abs(
        entry - sl
    )


    if direction == "BUY":

        tp1 = entry + risk
        tp2 = entry + (risk * 2)
        tp3 = entry + (risk * 3)


    else:

        tp1 = entry - risk
        tp2 = entry - (risk * 2)
        tp3 = entry - (risk * 3)



    liquidity = liquidity_target_map(
        df,
        direction
    )


    return {

        "entry": entry,

        "sl": sl,

        "tp1": round(tp1,4),

        "tp2": round(tp2,4),

        "tp3": round(tp3,4),

        "liquidity_target": liquidity

    }



# ==========================
# TRADE MANAGEMENT SCORE
# ==========================

def trade_management_score(df) -> int:


    score = 0


    if protected_structure_sl(
        df,
        final_market_direction(df)
    ):

        score += 30


    if liquidity_target_map(
        df,
        final_market_direction(df)
    ):

        score += 30


    if calculate_targets(
        df,
        final_market_direction(df)
    ):

        score += 40


    return min(
        score,
        100
    )



# ==========================
# FINAL TRADE PLAN
# ==========================

def structure_trade_plan(df) -> Dict:


    direction = final_market_direction(df)


    return {

        "direction":
            direction,


        "targets":
            calculate_targets(
                df,
                direction
            ),


        "management_score":
            trade_management_score(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_management(df) -> Dict:

    return structure_trade_plan(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-20
# Advanced ICT Final Decision Layer
# Signal Approval + Risk Filter
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL BIAS CALCULATION
# ==========================

def final_bias_score(df) -> Dict:

    score = 0

    direction_votes = []


    checks = [

        detect_structure(df),

        detect_bos(df),

        detect_mss(df),

        detect_choch(df),

        detect_order_block(df),

        detect_fvg(df),

        detect_liquidity_sweep(df),

        detect_displacement(df)

    ]


    for item in checks:

        if item:

            score += 10

            if "direction" in item:

                direction_votes.append(
                    item["direction"]
                )


    buy = direction_votes.count(
        "BUY"
    )

    sell = direction_votes.count(
        "SELL"
    )


    direction = "RANGE"


    if buy > sell:

        direction = "BUY"


    elif sell > buy:

        direction = "SELL"


    return {

        "direction":
            direction,

        "score":
            min(score,100)

    }



# ==========================
# RISK FILTER
# ==========================

def final_risk_filter(df) -> bool:


    direction = final_market_direction(df)


    if direction == "RANGE":

        return False


    rr = risk_reward_validation(
        df,
        direction,
        float(df["close"].iloc[-1])
    )


    if rr is None:

        return False


    if rr["rr"] < 2:

        return False


    return True



# ==========================
# FINAL ICT APPROVAL
# ==========================

def final_ict_approval(df) -> Dict:


    bias = final_bias_score(df)

    premium = premium_execution_report(df)

    trade_plan = structure_trade_plan(df)


    approved = True


    if bias["score"] < 70:

        approved = False


    if not premium["valid"]:

        approved = False


    if not final_risk_filter(df):

        approved = False



    return {

        "approved":
            approved,


        "signal":

            "TRADE"
            if approved
            else "NO_TRADE",


        "direction":
            bias["direction"],


        "confidence":
            bias["score"],


        "premium":
            premium,


        "trade_plan":
            trade_plan

    }



# ==========================
# V12 FINAL STRUCTURE ENGINE
# ==========================

def structure_engine_v12_final(df) -> Dict:

    return final_ict_approval(df)



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_signal_v12(df) -> Dict:

    result = structure_engine_v12_final(df)


    return {

        "valid":
            result["approved"],


        "direction":
            result["direction"],


        "score":
            result["confidence"],


        "data":
            result

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-21
# Advanced ICT Institutional Confirmation
# Market Maker Model + Final Bias Lock
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# MARKET MAKER MODEL
# ==========================

def detect_market_maker_model(df) -> Optional[Dict]:

    if len(df) < 30:
        return None


    high = float(
        df["high"].tail(30).max()
    )

    low = float(
        df["low"].tail(30).min()
    )


    current = float(
        df["close"].iloc[-1]
    )


    range_size = high - low


    if range_size == 0:

        return None


    position = (
        current - low
    ) / range_size



    if position < 0.25:

        return {

            "phase":
                "ACCUMULATION",

            "direction":
                "BUY"

        }


    if position > 0.75:

        return {

            "phase":
                "DISTRIBUTION",

            "direction":
                "SELL"

        }


    return {

        "phase":
            "MANIPULATION",

        "direction":
            "WAIT"

    }



# ==========================
# DISPLACEMENT CONFIRMATION
# ==========================

def displacement_confirmation(df) -> bool:


    displacement = detect_displacement(df)


    if displacement is None:

        return False


    structure = detect_structure(df)


    if structure is None:

        return False



    return (
        displacement["direction"]
        ==
        structure["direction"]
    )



# ==========================
# INSTITUTIONAL BIAS LOCK
# ==========================

def institutional_bias_lock(df) -> Dict:


    score = 0


    direction_votes = []


    model = detect_market_maker_model(df)

    structure = detect_structure(df)

    liquidity = detect_liquidity_sweep(df)

    displacement = detect_displacement(df)



    if model:

        score += 20

        if model["direction"] != "WAIT":

            direction_votes.append(
                model["direction"]
            )


    if structure:

        score += 25

        direction_votes.append(
            structure["direction"]
        )


    if liquidity:

        score += 25

        direction_votes.append(
            liquidity["direction"]
        )


    if displacement:

        score += 30

        direction_votes.append(
            displacement["direction"]
        )



    buy = direction_votes.count(
        "BUY"
    )

    sell = direction_votes.count(
        "SELL"
    )


    direction = "RANGE"


    if buy > sell:

        direction = "BUY"


    elif sell > buy:

        direction = "SELL"



    return {

        "direction":
            direction,

        "score":
            min(score,100)

    }



# ==========================
# BIAS LOCK VALIDATION
# ==========================

def validate_bias_lock(df) -> bool:


    result = institutional_bias_lock(df)


    if result["score"] < 80:

        return False


    if result["direction"] == "RANGE":

        return False


    return True



# ==========================
# FINAL INSTITUTIONAL REPORT
# ==========================

def institutional_structure_report(df) -> Dict:


    bias = institutional_bias_lock(df)


    return {

        "valid":
            validate_bias_lock(df),

        "direction":
            bias["direction"],

        "score":
            bias["score"],

        "market_model":
            detect_market_maker_model(df),

        "displacement":
            displacement_confirmation(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_institutional_structure(df) -> Dict:

    return institutional_structure_report(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-22
# Advanced ICT Liquidity Map Engine
# Internal + External Liquidity Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# EXTERNAL LIQUIDITY
# ==========================

def detect_external_liquidity(df) -> Optional[Dict]:

    if len(df) < 30:
        return None


    high = float(
        df["high"].tail(30).max()
    )

    low = float(
        df["low"].tail(30).min()
    )


    price = float(
        df["close"].iloc[-1]
    )


    if abs(high - price) < abs(price - low):

        return {

            "type":
                "EXTERNAL_BUY_LIQUIDITY",

            "side":
                "BUY",

            "level":
                high

        }


    return {

        "type":
            "EXTERNAL_SELL_LIQUIDITY",

        "side":
            "SELL",

        "level":
            low

    }



# ==========================
# INTERNAL LIQUIDITY
# ==========================

def detect_internal_liquidity(df) -> Optional[Dict]:

    if len(df) < 10:
        return None


    high = float(
        df["high"].tail(10).max()
    )

    low = float(
        df["low"].tail(10).min()
    )


    price = float(
        df["close"].iloc[-1]
    )


    mid = (
        high + low
    ) / 2



    if price > mid:

        return {

            "type":
                "INTERNAL_LOW_LIQUIDITY",

            "side":
                "SELL",

            "level":
                low

        }


    return {

        "type":
            "INTERNAL_HIGH_LIQUIDITY",

        "side":
            "BUY",

        "level":
            high

    }



# ==========================
# LIQUIDITY HIERARCHY
# ==========================

def liquidity_hierarchy(df) -> Dict:


    external = detect_external_liquidity(df)

    internal = detect_internal_liquidity(df)


    return {

        "external":
            external,

        "internal":
            internal

    }



# ==========================
# LIQUIDITY DRAW
# ==========================

def liquidity_draw(df) -> Dict:


    structure = detect_structure(df)

    external = detect_external_liquidity(df)


    direction = "NONE"


    if structure:

        direction = structure["direction"]



    target = None


    if external:

        target = external["level"]



    return {

        "direction":
            direction,

        "target":
            target

    }



# ==========================
# LIQUIDITY ALIGNMENT
# ==========================

def liquidity_alignment(df) -> bool:


    structure = detect_structure(df)

    draw = liquidity_draw(df)


    if structure is None:

        return False


    if draw["direction"] == "NONE":

        return False



    return (
        structure["direction"]
        ==
        draw["direction"]
    )



# ==========================
# LIQUIDITY SCORE
# ==========================

def liquidity_map_score(df) -> int:


    score = 0


    if detect_external_liquidity(df):

        score += 30


    if detect_internal_liquidity(df):

        score += 20


    if detect_liquidity_sweep(df):

        score += 30


    if liquidity_alignment(df):

        score += 20



    return min(score,100)



# ==========================
# FINAL LIQUIDITY REPORT
# ==========================

def liquidity_map_engine(df) -> Dict:


    return {

        "score":
            liquidity_map_score(df),


        "draw":
            liquidity_draw(df),


        "hierarchy":
            liquidity_hierarchy(df),


        "aligned":
            liquidity_alignment(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_map(df) -> Dict:

    return liquidity_map_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-23
# Advanced ICT Dealing Range Engine
# Premium / Discount + Equilibrium
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DEALING RANGE DETECTION
# ==========================

def detect_dealing_range(df) -> Optional[Dict]:

    if len(df) < 20:
        return None


    swing_high = get_last_swing_high(df)

    swing_low = get_last_swing_low(df)


    if swing_high is None or swing_low is None:

        return None



    high = swing_high["price"]

    low = swing_low["price"]


    if high <= low:

        return None



    equilibrium = (
        high + low
    ) / 2



    return {

        "high":
            high,

        "low":
            low,

        "equilibrium":
            equilibrium

    }



# ==========================
# PREMIUM DISCOUNT CALCULATION
# ==========================

def calculate_pd_zone(df) -> Dict:


    dealing = detect_dealing_range(df)


    if dealing is None:

        return {

            "zone":
                "UNKNOWN"

        }



    price = float(
        df["close"].iloc[-1]
    )


    if price > dealing["equilibrium"]:

        zone = "PREMIUM"


    elif price < dealing["equilibrium"]:

        zone = "DISCOUNT"


    else:

        zone = "EQUILIBRIUM"



    return {

        "zone":
            zone,

        "price":
            price,

        "high":
            dealing["high"],

        "low":
            dealing["low"],

        "equilibrium":
            dealing["equilibrium"]

    }



# ==========================
# OTE ALIGNMENT
# ==========================

def pd_ote_alignment(df) -> bool:


    structure = detect_structure(df)


    if structure is None:

        return False


    zone = calculate_pd_zone(df)


    if structure["direction"] == "BUY":

        return zone["zone"] == "DISCOUNT"



    if structure["direction"] == "SELL":

        return zone["zone"] == "PREMIUM"



    return False



# ==========================
# DEALING RANGE SCORE
# ==========================

def dealing_range_score(df) -> int:


    score = 0


    if detect_dealing_range(df):

        score += 30


    if pd_ote_alignment(df):

        score += 30


    if detect_order_block(df):

        score += 20


    if detect_fvg(df):

        score += 20



    return min(score,100)



# ==========================
# RANGE BIAS
# ==========================

def dealing_range_bias(df) -> Dict:


    structure = detect_structure(df)

    zone = calculate_pd_zone(df)


    direction = "RANGE"


    if structure:

        direction = structure["direction"]



    return {

        "direction":
            direction,

        "zone":
            zone["zone"],

        "score":
            dealing_range_score(df)

    }



# ==========================
# DEALING RANGE VALIDATION
# ==========================

def validate_dealing_range(df) -> bool:


    result = dealing_range_bias(df)


    if result["direction"] == "RANGE":

        return False


    if result["score"] < 70:

        return False


    return True



# ==========================
# FINAL RANGE REPORT
# ==========================

def dealing_range_engine(df) -> Dict:


    return {

        "valid":
            validate_dealing_range(df),

        "bias":
            dealing_range_bias(df),

        "pd_zone":
            calculate_pd_zone(df),

        "range":
            detect_dealing_range(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_dealing_range_signal(df) -> Dict:

    return dealing_range_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-24
# Advanced ICT Entry Trigger Engine
# BOS + MSS + OB + FVG Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# CANDLE CONFIRMATION
# ==========================

def candle_confirmation(df, direction: str) -> bool:

    if len(df) < 3:
        return False


    open_price = float(
        df["open"].iloc[-1]
    )

    close_price = float(
        df["close"].iloc[-1]
    )


    if direction == "BUY":

        return close_price > open_price


    if direction == "SELL":

        return close_price < open_price


    return False



# ==========================
# MOMENTUM CONFIRMATION
# ==========================

def momentum_confirmation(df) -> bool:

    displacement = detect_displacement(df)


    if displacement is None:

        return False


    return True



# ==========================
# ORDER FLOW CONFIRMATION
# ==========================

def order_flow_confirmation(df) -> Dict:


    structure = detect_structure(df)

    ob = detect_order_block(df)

    fvg = detect_fvg(df)

    score = 0


    direction = "RANGE"



    if structure:

        score += 25

        direction = structure["direction"]



    if ob:

        score += 25



    if fvg:

        score += 20



    if momentum_confirmation(df):

        score += 15



    if candle_confirmation(
        df,
        direction
    ):

        score += 15



    return {

        "direction":
            direction,

        "score":
            min(score,100)

    }



# ==========================
# ENTRY TRIGGER
# ==========================

def detect_entry_trigger(df) -> Dict:


    result = order_flow_confirmation(df)


    valid = False


    if result["score"] >= 80:

        if result["direction"] != "RANGE":

            valid = True



    return {

        "trigger":
            valid,

        "direction":
            result["direction"],

        "score":
            result["score"]

    }



# ==========================
# PRE ENTRY CHECK
# ==========================

def pre_entry_validation(df) -> bool:


    trigger = detect_entry_trigger(df)


    if not trigger["trigger"]:

        return False


    if not liquidity_alignment(df):

        return False


    if not pd_ote_alignment(df):

        return False


    return True



# ==========================
# FINAL ICT ENTRY TRIGGER
# ==========================

def ict_entry_trigger_engine(df) -> Dict:


    trigger = detect_entry_trigger(df)


    return {

        "valid":

            pre_entry_validation(df),


        "direction":

            trigger["direction"],


        "confidence":

            trigger["score"],


        "trigger":

            trigger

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_entry_trigger_signal(df) -> Dict:

    return ict_entry_trigger_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-25
# Advanced ICT Final Execution Gateway
# Signal Routing + Confirmation Lock
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EXECUTION SCORE ENGINE
# ==========================

def execution_score_v12(df) -> int:

    score = 0


    checks = [

        structure_quality(df),

        liquidity_map_score(df),

        dealing_range_score(df),

        ict_premium_score(df),

        entry_timing_score(df),

        trade_management_score(df)

    ]


    for value in checks:

        if value >= 70:

            score += 15


    if final_market_direction(df) != "RANGE":

        score += 10


    return min(score,100)



# ==========================
# CONFIRMATION LOCK
# ==========================

def confirmation_lock(df) -> Dict:


    direction = final_market_direction(df)

    score = execution_score_v12(df)


    confirmations = 0


    if detect_structure(df):

        confirmations += 1


    if detect_order_block(df):

        confirmations += 1


    if detect_fvg(df):

        confirmations += 1


    if detect_liquidity_sweep(df):

        confirmations += 1


    if detect_displacement(df):

        confirmations += 1



    return {

        "direction":
            direction,

        "score":
            score,

        "confirmations":
            confirmations,

        "locked":
            score >= 85
            and
            confirmations >= 4

    }



# ==========================
# FINAL SIGNAL ROUTER
# ==========================

def final_signal_router(df) -> Dict:


    lock = confirmation_lock(df)


    signal = "NO_TRADE"


    if lock["locked"]:

        if lock["direction"] == "BUY":

            signal = "BUY"


        elif lock["direction"] == "SELL":

            signal = "SELL"



    return {

        "signal":
            signal,

        "direction":
            lock["direction"],

        "confidence":
            lock["score"],

        "confirmations":
            lock["confirmations"]

    }



# ==========================
# V12 STRUCTURE FINAL OUTPUT
# ==========================

def structure_engine_v12_output(df) -> Dict:


    return {

        "final_signal":
            final_signal_router(df),


        "market_bias":
            get_market_bias(df),


        "liquidity":
            get_liquidity_map(df),


        "entry":
            get_entry_trigger_signal(df),


        "trade_plan":
            get_trade_management(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def analyze_v12_structure(df) -> Dict:

    return structure_engine_v12_output(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-26
# Advanced ICT Final Market Intelligence Layer
# Smart Money Flow + Institutional Bias
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# SMART MONEY FLOW
# ==========================

def smart_money_flow(df) -> Dict:

    score = 0

    direction_votes = []


    structure = detect_structure(df)

    liquidity = detect_liquidity_sweep(df)

    ob = detect_order_block(df)

    fvg = detect_fvg(df)

    displacement = detect_displacement(df)



    if structure:

        score += 20

        direction_votes.append(
            structure["direction"]
        )


    if liquidity:

        score += 25

        direction_votes.append(
            liquidity["direction"]
        )


    if ob:

        score += 20

        direction_votes.append(
            ob["direction"]
        )


    if fvg:

        score += 15

        direction_votes.append(
            fvg["direction"]
        )


    if displacement:

        score += 20

        direction_votes.append(
            displacement["direction"]
        )



    buy = direction_votes.count("BUY")

    sell = direction_votes.count("SELL")


    direction = "RANGE"


    if buy > sell:

        direction = "BUY"


    elif sell > buy:

        direction = "SELL"



    return {

        "direction":
            direction,

        "score":
            min(score,100),

        "flow":
            direction_votes

    }



# ==========================
# INSTITUTIONAL BIAS ENGINE
# ==========================

def institutional_bias_engine(df) -> Dict:


    flow = smart_money_flow(df)


    bias = flow["direction"]


    strength = flow["score"]



    return {

        "bias":
            bias,

        "strength":
            strength,

        "institutional":
            strength >= 80

    }



# ==========================
# MARKET MANIPULATION FILTER
# ==========================

def manipulation_filter(df) -> bool:


    sfp = detect_sfp(df)

    sweep = detect_liquidity_sweep(df)


    if sfp and sweep:

        return False


    return True



# ==========================
# FINAL SMART MONEY APPROVAL
# ==========================

def smart_money_approval(df) -> Dict:


    bias = institutional_bias_engine(df)


    approved = True


    if not bias["institutional"]:

        approved = False


    if not manipulation_filter(df):

        approved = False



    if bias["bias"] == "RANGE":

        approved = False



    return {

        "approved":
            approved,

        "direction":
            bias["bias"],

        "confidence":
            bias["strength"],

        "manipulation_safe":
            manipulation_filter(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_smart_money_signal(df) -> Dict:

    return smart_money_approval(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-27
# Advanced ICT Market Maker Delivery Layer
# Accumulation + Manipulation + Distribution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DELIVERY PHASE DETECTION
# ==========================

def detect_delivery_phase(df) -> str:

    if len(df) < 40:
        return "UNKNOWN"


    high = float(
        df["high"].tail(40).max()
    )

    low = float(
        df["low"].tail(40).min()
    )

    price = float(
        df["close"].iloc[-1]
    )


    if high == low:
        return "RANGE"



    location = (
        price - low
    ) / (high - low)



    if location <= 0.30:

        return "ACCUMULATION"


    if location >= 0.70:

        return "DISTRIBUTION"


    return "MANIPULATION"



# ==========================
# ACCUMULATION CHECK
# ==========================

def accumulation_confirmation(df) -> bool:


    phase = detect_delivery_phase(df)


    if phase != "ACCUMULATION":

        return False


    liquidity = detect_liquidity_sweep(df)


    if liquidity:

        if liquidity["direction"] == "BUY":

            return True


    return False



# ==========================
# DISTRIBUTION CHECK
# ==========================

def distribution_confirmation(df) -> bool:


    phase = detect_delivery_phase(df)


    if phase != "DISTRIBUTION":

        return False


    liquidity = detect_liquidity_sweep(df)


    if liquidity:

        if liquidity["direction"] == "SELL":

            return True


    return False



# ==========================
# MANIPULATION REVERSAL
# ==========================

def manipulation_reversal(df) -> Optional[Dict]:


    sweep = detect_liquidity_sweep(df)

    mss = detect_mss(df)


    if sweep and mss:


        if sweep["direction"] == mss["direction"]:

            return {

                "valid": True,

                "direction":
                    sweep["direction"],

                "type":
                    "REVERSAL"

            }


    return None



# ==========================
# DELIVERY SCORE
# ==========================

def delivery_score(df) -> int:


    score = 0


    if detect_delivery_phase(df) != "UNKNOWN":

        score += 20


    if detect_liquidity_sweep(df):

        score += 25


    if detect_mss(df):

        score += 20


    if detect_displacement(df):

        score += 20


    if detect_order_block(df):

        score += 15



    return min(score,100)



# ==========================
# MARKET DELIVERY ENGINE
# ==========================

def market_delivery_engine(df) -> Dict:


    phase = detect_delivery_phase(df)

    reversal = manipulation_reversal(df)


    direction = final_market_direction(df)


    if reversal:

        direction = reversal["direction"]



    return {

        "phase":
            phase,

        "direction":
            direction,

        "score":
            delivery_score(df),

        "reversal":
            reversal

    }



# ==========================
# DELIVERY VALIDATION
# ==========================

def validate_delivery(df) -> bool:


    result = market_delivery_engine(df)


    if result["score"] < 75:

        return False


    if result["direction"] == "RANGE":

        return False


    return True



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_delivery(df) -> Dict:

    result = market_delivery_engine(df)


    return {

        "valid":
            validate_delivery(df),

        "data":
            result

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-28
# Advanced ICT Institutional Entry Model
# AMD + Liquidity + Structure + Execution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# AMD CYCLE DETECTION
# ==========================

def detect_amd_cycle(df) -> str:

    phase = detect_delivery_phase(df)


    if phase == "ACCUMULATION":

        return "ACCUMULATION"


    if phase == "MANIPULATION":

        return "MANIPULATION"


    if phase == "DISTRIBUTION":

        return "DISTRIBUTION"


    return "UNKNOWN"



# ==========================
# MANIPULATION CONFIRMATION
# ==========================

def amd_manipulation_check(df) -> bool:


    if detect_amd_cycle(df) != "MANIPULATION":

        return False


    sweep = detect_liquidity_sweep(df)


    if sweep is None:

        return False


    return True



# ==========================
# DISTRIBUTION CONFIRMATION
# ==========================

def amd_distribution_check(df) -> bool:


    if detect_amd_cycle(df) != "DISTRIBUTION":

        return False


    structure = detect_structure(df)


    if structure is None:

        return False


    return True



# ==========================
# INSTITUTIONAL ENTRY MODEL
# ==========================

def institutional_entry_model(df) -> Dict:


    score = 0

    direction = "RANGE"



    structure = detect_structure(df)

    liquidity = detect_liquidity_sweep(df)

    ob = detect_order_block(df)

    fvg = detect_fvg(df)

    displacement = detect_displacement(df)



    if structure:

        score += 25

        direction = structure["direction"]



    if liquidity:

        score += 25

        direction = liquidity["direction"]



    if ob:

        score += 15



    if fvg:

        score += 15



    if displacement:

        score += 20



    return {

        "direction":

            direction,

        "score":

            min(score,100),

        "amd":

            detect_amd_cycle(df)

    }



# ==========================
# INSTITUTIONAL ENTRY FILTER
# ==========================

def institutional_entry_filter(df) -> bool:


    result = institutional_entry_model(df)


    if result["score"] < 85:

        return False


    if result["direction"] == "RANGE":

        return False


    if not amd_manipulation_check(df):

        return False


    return True



# ==========================
# FINAL INSTITUTIONAL SIGNAL
# ==========================

def institutional_entry_signal(df) -> Dict:


    result = institutional_entry_model(df)


    return {

        "valid":

            institutional_entry_filter(df),


        "direction":

            result["direction"],


        "confidence":

            result["score"],


        "phase":

            result["amd"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_institutional_entry(df) -> Dict:

    return institutional_entry_signal(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-29
# Advanced ICT Market Profile Layer
# Session Bias + Range Expansion + Liquidity Objective
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# RANGE EXPANSION DETECTION
# ==========================

def detect_range_expansion(df) -> bool:

    if len(df) < 20:
        return False


    current_range = (
        float(df["high"].iloc[-1]) -
        float(df["low"].iloc[-1])
    )


    avg_range = 0


    for i in range(-20, -1):

        avg_range += (
            float(df["high"].iloc[i]) -
            float(df["low"].iloc[i])
        )


    avg_range /= 19


    if avg_range == 0:

        return False


    return current_range >= avg_range * 1.5



# ==========================
# RANGE COMPRESSION
# ==========================

def detect_range_compression(df) -> bool:

    if len(df) < 20:
        return False


    current_range = (
        float(df["high"].iloc[-1]) -
        float(df["low"].iloc[-1])
    )


    avg_range = 0


    for i in range(-20, -1):

        avg_range += (
            float(df["high"].iloc[i]) -
            float(df["low"].iloc[i])
        )


    avg_range /= 19


    if avg_range == 0:

        return False


    return current_range <= avg_range * 0.6



# ==========================
# LIQUIDITY OBJECTIVE ENGINE
# ==========================

def liquidity_objective(df) -> Dict:


    external = detect_external_liquidity(df)

    internal = detect_internal_liquidity(df)


    target = None

    side = "NONE"


    if external:

        target = external["level"]

        side = external["side"]


    elif internal:

        target = internal["level"]

        side = internal["side"]



    return {

        "target":

            target,

        "side":

            side

    }



# ==========================
# MARKET PROFILE SCORE
# ==========================

def market_profile_score(df) -> int:


    score = 0


    if detect_structure(df):

        score += 20


    if detect_range_expansion(df):

        score += 20


    if detect_liquidity_sweep(df):

        score += 20


    if detect_displacement(df):

        score += 20


    if liquidity_objective(df)["target"]:

        score += 20



    return min(score,100)



# ==========================
# MARKET PROFILE ENGINE
# ==========================

def market_profile_engine(df) -> Dict:


    direction = final_market_direction(df)


    return {

        "direction":

            direction,


        "score":

            market_profile_score(df),


        "expansion":

            detect_range_expansion(df),


        "compression":

            detect_range_compression(df),


        "objective":

            liquidity_objective(df)

    }



# ==========================
# PROFILE VALIDATION
# ==========================

def validate_market_profile(df) -> bool:


    result = market_profile_engine(df)


    if result["score"] < 75:

        return False


    if result["direction"] == "RANGE":

        return False


    return True



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_profile(df) -> Dict:


    result = market_profile_engine(df)


    return {

        "valid":

            validate_market_profile(df),

        "data":

            result

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2B-30
# Advanced ICT Final Confluence Router
# Complete Structure Decision Layer
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL CONFLUENCE MATRIX
# ==========================

def final_confluence_matrix(df) -> Dict:

    score = 0

    confirmations = []


    checks = [

        detect_structure(df),

        detect_bos(df),

        detect_mss(df),

        detect_choch(df),

        detect_order_block(df),

        detect_fvg(df),

        detect_liquidity_sweep(df),

        detect_displacement(df),

    ]


    for item in checks:

        if item:

            score += 10

            if "type" in item:

                confirmations.append(
                    item["type"]
                )


    if liquidity_alignment(df):

        score += 10

        confirmations.append(
            "LIQUIDITY_ALIGNMENT"
        )


    if pd_ote_alignment(df):

        score += 10

        confirmations.append(
            "OTE_ALIGNMENT"
        )


    direction = final_market_direction(df)


    return {

        "direction":

            direction,

        "score":

            min(score,100),

        "confirmations":

            confirmations

    }



# ==========================
# FINAL BIAS LOCK
# ==========================

def final_bias_lock(df) -> Dict:


    matrix = final_confluence_matrix(df)


    approved = True


    if matrix["direction"] == "RANGE":

        approved = False


    if matrix["score"] < 85:

        approved = False



    return {

        "approved":

            approved,

        "direction":

            matrix["direction"],

        "confidence":

            matrix["score"],

        "confirmations":

            matrix["confirmations"]

    }



# ==========================
# FINAL STRUCTURE ENGINE V12
# ==========================

def structure_engine_v12_final_router(df) -> Dict:


    bias = final_bias_lock(df)


    trade_plan = structure_trade_plan(df)


    return {

        "signal":

            "BUY"
            if
            bias["approved"]
            and
            bias["direction"] == "BUY"

            else

            "SELL"
            if
            bias["approved"]
            and
            bias["direction"] == "SELL"

            else

            "NO_TRADE",


        "confidence":

            bias["confidence"],


        "bias":

            bias,


        "trade_plan":

            trade_plan

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_engine_v12(df) -> Dict:

    return structure_engine_v12_final_router(df) 35
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-1
# Advanced Optimization Layer
# Structure Cache + Unified Data Validation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DATA VALIDATION ENGINE
# ==========================

def validate_structure_data(df) -> bool:

    if df is None:
        return False


    if len(df) < 50:
        return False


    required = [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]


    for col in required:

        if col not in df.columns:

            return False


    return True



# ==========================
# PRICE STATE SNAPSHOT
# ==========================

def get_price_snapshot(df) -> Dict:


    if not validate_structure_data(df):

        return {}


    return {

        "open":
            float(df["open"].iloc[-1]),

        "high":
            float(df["high"].iloc[-1]),

        "low":
            float(df["low"].iloc[-1]),

        "close":
            float(df["close"].iloc[-1]),

        "volume":
            float(df["volume"].iloc[-1])

    }



# ==========================
# STRUCTURE CACHE ENGINE
# ==========================

def structure_cache(df) -> Dict:


    snapshot = get_price_snapshot(df)


    if not snapshot:

        return {

            "valid":
                False

        }



    return {

        "valid":
            True,

        "snapshot":
            snapshot,

        "length":
            len(df)

    }



# ==========================
# DATA QUALITY SCORE
# ==========================

def structure_data_quality(df) -> int:


    score = 0


    if validate_structure_data(df):

        score += 40


    if len(df) >= 100:

        score += 20


    if df["volume"].iloc[-1] > 0:

        score += 20


    if structure_atr(df) > 0:

        score += 20



    return min(score,100)



# ==========================
# OPTIMIZED STRUCTURE CHECK
# ==========================

def optimized_structure_check(df) -> Dict:


    cache = structure_cache(df)


    return {

        "ready":

            cache["valid"],


        "quality":

            structure_data_quality(df),


        "cache":

            cache

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_data_v12(df) -> Dict:

    return optimized_structure_check(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-2
# Advanced Optimization Layer
# Unified Swing Engine + Dynamic Levels
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DYNAMIC SWING HIGH
# ==========================

def dynamic_swing_high(df, lookback: int = 5) -> Optional[Dict]:

    if len(df) < lookback * 2 + 1:
        return None


    for i in range(
        len(df) - lookback - 1,
        lookback,
        -1
    ):

        high = float(
            df["high"].iloc[i]
        )


        left = df["high"].iloc[
            i-lookback:i
        ]


        right = df["high"].iloc[
            i+1:i+lookback+1
        ]


        if (
            high > left.max()
            and
            high > right.max()
        ):

            return {

                "price":
                    high,

                "index":
                    i,

                "type":
                    "SWING_HIGH"

            }


    return None



# ==========================
# DYNAMIC SWING LOW
# ==========================

def dynamic_swing_low(df, lookback: int = 5) -> Optional[Dict]:

    if len(df) < lookback * 2 + 1:
        return None


    for i in range(
        len(df) - lookback - 1,
        lookback,
        -1
    ):

        low = float(
            df["low"].iloc[i]
        )


        left = df["low"].iloc[
            i-lookback:i
        ]


        right = df["low"].iloc[
            i+1:i+lookback+1
        ]


        if (
            low < left.min()
            and
            low < right.min()
        ):

            return {

                "price":
                    low,

                "index":
                    i,

                "type":
                    "SWING_LOW"

            }


    return None



# ==========================
# UPDATED SWING MAP
# ==========================

def dynamic_swing_map(df) -> Dict:


    high = dynamic_swing_high(df)

    low = dynamic_swing_low(df)


    return {

        "high":

            high,


        "low":

            low

    }



# ==========================
# STRUCTURE LEVEL ENGINE
# ==========================

def dynamic_structure_levels(df) -> Dict:


    swings = dynamic_swing_map(df)


    levels = {


        "resistance":

            swings["high"]["price"]

            if swings["high"]

            else None,


        "support":

            swings["low"]["price"]

            if swings["low"]

            else None

    }


    return levels



# ==========================
# SWING QUALITY SCORE
# ==========================

def swing_quality_score(df) -> int:


    score = 0


    swings = dynamic_swing_map(df)


    if swings["high"]:

        score += 40


    if swings["low"]:

        score += 40


    if dynamic_structure_levels(df):

        score += 20


    return min(score,100)



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_dynamic_structure_levels(df) -> Dict:

    return {

        "levels":

            dynamic_structure_levels(df),


        "score":

            swing_quality_score(df)

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-3
# Advanced Optimization Layer
# Unified BOS + CHOCH + MSS Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# INTERNAL STRUCTURE BREAK
# ==========================

def internal_structure_break(df) -> Optional[Dict]:

    swing_high = dynamic_swing_high(df)

    swing_low = dynamic_swing_low(df)


    if swing_high is None or swing_low is None:

        return None


    price = float(
        df["close"].iloc[-1]
    )


    if price > swing_high["price"]:

        return {

            "type":
                "BOS",

            "direction":
                "BUY",

            "level":
                swing_high["price"]

        }



    if price < swing_low["price"]:

        return {

            "type":
                "BOS",

            "direction":
                "SELL",

            "level":
                swing_low["price"]

        }


    return None



# ==========================
# MARKET STRUCTURE SHIFT
# ==========================

def optimized_mss(df) -> Optional[Dict]:


    previous = float(
        df["close"].iloc[-2]
    )


    current = float(
        df["close"].iloc[-1]
    )


    high = float(
        df["high"].tail(10).max()
    )


    low = float(
        df["low"].tail(10).min()
    )


    if previous < high and current > high:

        return {

            "type":
                "MSS",

            "direction":
                "BUY",

            "level":
                high

        }


    if previous > low and current < low:

        return {

            "type":
                "MSS",

            "direction":
                "SELL",

            "level":
                low

        }


    return None



# ==========================
# CHOCH ENGINE
# ==========================

def optimized_choch(df) -> Optional[Dict]:


    bos = internal_structure_break(df)

    mss = optimized_mss(df)


    if bos and mss:


        if bos["direction"] != mss["direction"]:

            return {

                "type":
                    "CHOCH",

                "direction":
                    mss["direction"],

                "level":
                    mss["level"]

            }


    return None



# ==========================
# STRUCTURE EVENT ROUTER
# ==========================

def structure_event_engine(df) -> Dict:


    bos = internal_structure_break(df)

    mss = optimized_mss(df)

    choch = optimized_choch(df)



    event = None


    if choch:

        event = choch


    elif mss:

        event = mss


    elif bos:

        event = bos



    return {

        "event":

            event,


        "bos":

            bos,


        "mss":

            mss,


        "choch":

            choch

    }



# ==========================
# STRUCTURE EVENT SCORE
# ==========================

def structure_event_score(df) -> int:


    score = 0


    result = structure_event_engine(df)


    if result["bos"]:

        score += 30


    if result["mss"]:

        score += 35


    if result["choch"]:

        score += 35


    return min(score,100)



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_events_v12(df) -> Dict:

    return {

        "data":

            structure_event_engine(df),


        "score":

            structure_event_score(df)

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-4
# Advanced Optimization Layer
# Unified Liquidity Detection Engine
# Internal + External + Sweep Mapping
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# LIQUIDITY POOL DETECTION
# ==========================

def detect_liquidity_pools(df) -> Dict:

    if len(df) < 20:

        return {}


    high = float(
        df["high"].tail(20).max()
    )


    low = float(
        df["low"].tail(20).min()
    )


    return {

        "buy_side":

            high,


        "sell_side":

            low

    }



# ==========================
# LIQUIDITY SWEEP ENGINE
# ==========================

def optimized_liquidity_sweep(df) -> Optional[Dict]:


    pools = detect_liquidity_pools(df)


    if not pools:

        return None



    high = pools["buy_side"]

    low = pools["sell_side"]



    current_high = float(
        df["high"].iloc[-1]
    )


    current_low = float(
        df["low"].iloc[-1]
    )


    close = float(
        df["close"].iloc[-1]
    )



    if current_high > high and close < high:

        return {

            "type":
                "BUY_SIDE_SWEEP",

            "direction":
                "SELL",

            "level":
                high

        }



    if current_low < low and close > low:

        return {

            "type":
                "SELL_SIDE_SWEEP",

            "direction":
                "BUY",

            "level":
                low

        }



    return None



# ==========================
# LIQUIDITY GRAB CONFIRMATION
# ==========================

def liquidity_grab_confirmation(df) -> bool:


    sweep = optimized_liquidity_sweep(df)


    if sweep is None:

        return False


    if detect_mss(df):

        return True


    return False



# ==========================
# LIQUIDITY DIRECTION ENGINE
# ==========================

def liquidity_direction(df) -> str:


    sweep = optimized_liquidity_sweep(df)


    if sweep:

        return sweep["direction"]


    return "NONE"



# ==========================
# LIQUIDITY SCORE
# ==========================

def optimized_liquidity_score(df) -> int:


    score = 0


    if detect_liquidity_pools(df):

        score += 30


    if optimized_liquidity_sweep(df):

        score += 40


    if liquidity_grab_confirmation(df):

        score += 30



    return min(score,100)



# ==========================
# LIQUIDITY ENGINE OUTPUT
# ==========================

def optimized_liquidity_engine(df) -> Dict:


    return {

        "pools":

            detect_liquidity_pools(df),


        "sweep":

            optimized_liquidity_sweep(df),


        "direction":

            liquidity_direction(df),


        "score":

            optimized_liquidity_score(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_engine_v12(df) -> Dict:

    return optimized_liquidity_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-5
# Advanced Optimization Layer
# Unified FVG + Imbalance Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# FAIR VALUE GAP DETECTION
# ==========================

def optimized_fvg_detection(df) -> Optional[Dict]:

    if len(df) < 5:
        return None


    for i in range(
        len(df) - 3,
        1,
        -1
    ):

        candle1_high = float(
            df["high"].iloc[i-1]
        )

        candle1_low = float(
            df["low"].iloc[i-1]
        )


        candle3_high = float(
            df["high"].iloc[i+1]
        )

        candle3_low = float(
            df["low"].iloc[i+1]
        )


        current_close = float(
            df["close"].iloc[i]
        )


        # Bullish FVG

        if candle3_low > candle1_high:

            return {

                "type":
                    "BULLISH_FVG",

                "direction":
                    "BUY",

                "high":
                    candle3_low,

                "low":
                    candle1_high,

                "index":
                    i

            }



        # Bearish FVG

        if candle3_high < candle1_low:

            return {

                "type":
                    "BEARISH_FVG",

                "direction":
                    "SELL",

                "high":
                    candle1_low,

                "low":
                    candle3_high,

                "index":
                    i

            }


    return None



# ==========================
# FVG RETEST CHECK
# ==========================

def optimized_fvg_retest(
        df,
        fvg: Dict
) -> bool:


    if fvg is None:

        return False


    price = float(
        df["close"].iloc[-1]
    )


    return (
        price >= fvg["low"]
        and
        price <= fvg["high"]
    )



# ==========================
# IMBALANCE STRENGTH
# ==========================

def imbalance_strength(df) -> int:


    fvg = optimized_fvg_detection(df)


    if fvg is None:

        return 0


    score = 30


    if optimized_fvg_retest(
        df,
        fvg
    ):

        score += 40


    if detect_displacement(df):

        score += 30



    return min(score,100)



# ==========================
# FVG DIRECTION FILTER
# ==========================

def fvg_direction_filter(df) -> str:


    fvg = optimized_fvg_detection(df)


    if fvg:

        return fvg["direction"]


    return "NONE"



# ==========================
# FVG ENGINE OUTPUT
# ==========================

def optimized_fvg_engine(df) -> Dict:


    return {

        "fvg":

            optimized_fvg_detection(df),


        "direction":

            fvg_direction_filter(df),


        "strength":

            imbalance_strength(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_fvg_engine_v12(df) -> Dict:

    return optimized_fvg_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-6
# Advanced Optimization Layer
# Unified Order Block + Breaker Block Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# OPTIMIZED ORDER BLOCK DETECTION
# ==========================

def optimized_order_block(df) -> Optional[Dict]:

    if len(df) < 10:

        return None


    for i in range(
        len(df) - 3,
        2,
        -1
    ):


        open_price = float(
            df["open"].iloc[i]
        )

        close_price = float(
            df["close"].iloc[i]
        )

        high = float(
            df["high"].iloc[i]
        )

        low = float(
            df["low"].iloc[i]
        )



        next_close = float(
            df["close"].iloc[i+1]
        )

        next_high = float(
            df["high"].iloc[i+1]
        )

        next_low = float(
            df["low"].iloc[i+1]
        )



        # Bullish Order Block

        if (
            close_price < open_price
            and
            next_close > next_high
        ):

            return {

                "type":
                    "BULLISH_OB",

                "direction":
                    "BUY",

                "high":
                    high,

                "low":
                    low,

                "index":
                    i

            }



        # Bearish Order Block

        if (
            close_price > open_price
            and
            next_close < next_low
        ):

            return {

                "type":
                    "BEARISH_OB",

                "direction":
                    "SELL",

                "high":
                    high,

                "low":
                    low,

                "index":
                    i

            }


    return None



# ==========================
# ORDER BLOCK MITIGATION
# ==========================

def order_block_mitigation(
        df,
        ob: Dict
) -> bool:


    if ob is None:

        return False


    price = float(
        df["close"].iloc[-1]
    )


    return (

        price >= ob["low"]

        and

        price <= ob["high"]

    )



# ==========================
# BREAKER BLOCK DETECTION
# ==========================

def detect_breaker_block(df) -> Optional[Dict]:


    ob = optimized_order_block(df)


    if ob is None:

        return None



    structure = optimized_choch(df)


    if structure is None:

        return None



    if (
        ob["direction"]
        !=
        structure["direction"]
    ):


        return {

            "type":
                "BREAKER_BLOCK",

            "direction":
                structure["direction"],

            "level":
                ob["high"]

        }



    return None



# ==========================
# ORDER BLOCK QUALITY SCORE
# ==========================

def order_block_quality_v12(df) -> int:


    score = 0


    ob = optimized_order_block(df)


    if ob:

        score += 40


    if order_block_mitigation(
        df,
        ob
    ):

        score += 30


    if detect_displacement(df):

        score += 20


    if detect_breaker_block(df):

        score += 10



    return min(score,100)



# ==========================
# ORDER BLOCK ENGINE OUTPUT
# ==========================

def optimized_order_block_engine(df) -> Dict:


    return {

        "order_block":

            optimized_order_block(df),


        "breaker":

            detect_breaker_block(df),


        "quality":

            order_block_quality_v12(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_order_block_engine_v12(df) -> Dict:

    return optimized_order_block_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-7
# Advanced Optimization Layer
# Unified Premium / Discount + OTE Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DEALING RANGE ENGINE
# ==========================

def optimized_dealing_range(df) -> Optional[Dict]:

    high_swing = dynamic_swing_high(df)

    low_swing = dynamic_swing_low(df)


    if high_swing is None or low_swing is None:

        return None



    high = high_swing["price"]

    low = low_swing["price"]


    if high <= low:

        return None



    equilibrium = (
        high + low
    ) / 2



    return {

        "high":

            high,


        "low":

            low,


        "equilibrium":

            equilibrium

    }



# ==========================
# PREMIUM / DISCOUNT ZONE
# ==========================

def optimized_pd_zone(df) -> Dict:


    dealing = optimized_dealing_range(df)


    if dealing is None:

        return {

            "zone":
                "UNKNOWN"

        }



    price = float(
        df["close"].iloc[-1]
    )


    if price > dealing["equilibrium"]:

        zone = "PREMIUM"


    elif price < dealing["equilibrium"]:

        zone = "DISCOUNT"


    else:

        zone = "EQUILIBRIUM"



    return {

        "zone":

            zone,


        "price":

            price,


        "equilibrium":

            dealing["equilibrium"]

    }



# ==========================
# OTE CALCULATION
# ==========================

def optimized_ote_zone(df) -> Optional[Dict]:


    dealing = optimized_dealing_range(df)


    if dealing is None:

        return None



    high = dealing["high"]

    low = dealing["low"]


    difference = high - low



    return {

        "ote_62":

            high - (
                difference * 0.62
            ),


        "ote_70":

            high - (
                difference * 0.70
            ),


        "ote_79":

            high - (
                difference * 0.79
            )

    }



# ==========================
# OTE ENTRY VALIDATION
# ==========================

def optimized_ote_validation(
        df,
        direction: str
) -> bool:


    ote = optimized_ote_zone(df)


    if ote is None:

        return False



    price = float(
        df["close"].iloc[-1]
    )



    if direction == "BUY":

        return (

            price <= ote["ote_62"]

            and

            price >= ote["ote_79"]

        )



    if direction == "SELL":

        return (

            price >= ote["ote_62"]

            and

            price <= ote["ote_79"]

        )


    return False



# ==========================
# PREMIUM DISCOUNT SCORE
# ==========================

def pd_ote_score(df) -> int:


    score = 0


    if optimized_dealing_range(df):

        score += 30


    structure = detect_structure(df)


    if structure:

        if optimized_ote_validation(
            df,
            structure["direction"]
        ):

            score += 40



    if optimized_order_block(df):

        score += 15


    if optimized_fvg_detection(df):

        score += 15



    return min(score,100)



# ==========================
# PD OTE ENGINE OUTPUT
# ==========================

def optimized_pd_ote_engine(df) -> Dict:


    return {

        "zone":

            optimized_pd_zone(df),


        "ote":

            optimized_ote_zone(df),


        "score":

            pd_ote_score(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_pd_ote_engine_v12(df) -> Dict:

    return optimized_pd_ote_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-8
# Advanced Optimization Layer
# Unified Multi Confirmation Engine
# Structure + Liquidity + OB + FVG Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# CONFIRMATION COUNTER
# ==========================

def confirmation_counter_v12(df) -> Dict:

    confirmations = []

    direction_votes = []


    structure = structure_event_engine(df)

    liquidity = optimized_liquidity_engine(df)

    ob = optimized_order_block_engine(df)

    fvg = optimized_fvg_engine(df)

    pd_zone = optimized_pd_ote_engine(df)



    if structure["event"]:

        confirmations.append(
            "STRUCTURE"
        )

        direction_votes.append(
            structure["event"]["direction"]
        )



    if liquidity["sweep"]:

        confirmations.append(
            "LIQUIDITY"
        )

        direction_votes.append(
            liquidity["direction"]
        )



    if ob["order_block"]:

        confirmations.append(
            "ORDER_BLOCK"
        )

        direction_votes.append(
            ob["order_block"]["direction"]
        )



    if fvg["fvg"]:

        confirmations.append(
            "FVG"
        )

        direction_votes.append(
            fvg["direction"]
        )



    if pd_zone["score"] >= 70:

        confirmations.append(
            "OTE_ALIGNMENT"
        )



    buy = direction_votes.count(
        "BUY"
    )

    sell = direction_votes.count(
        "SELL"
    )


    direction = "RANGE"


    if buy > sell:

        direction = "BUY"


    elif sell > buy:

        direction = "SELL"



    return {

        "direction":

            direction,


        "count":

            len(confirmations),


        "confirmations":

            confirmations

    }



# ==========================
# CONFIDENCE CALCULATION
# ==========================

def confirmation_confidence_v12(df) -> int:


    result = confirmation_counter_v12(df)


    score = 0


    score += result["count"] * 15


    if liquidity_alignment(df):

        score += 10


    if detect_displacement(df):

        score += 15



    return min(score,100)



# ==========================
# CONFIRMATION FILTER
# ==========================

def confirmation_filter_v12(df) -> bool:


    result = confirmation_counter_v12(df)


    confidence = confirmation_confidence_v12(df)



    if result["direction"] == "RANGE":

        return False


    if result["count"] < 4:

        return False


    if confidence < 80:

        return False



    return True



# ==========================
# FINAL CONFIRMATION ENGINE
# ==========================

def unified_confirmation_engine(df) -> Dict:


    result = confirmation_counter_v12(df)


    return {

        "valid":

            confirmation_filter_v12(df),


        "direction":

            result["direction"],


        "confidence":

            confirmation_confidence_v12(df),


        "confirmations":

            result["confirmations"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_confirmation_engine_v12(df) -> Dict:

    return unified_confirmation_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-9
# Advanced Optimization Layer
# Dynamic Risk + Entry Quality Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# DYNAMIC ENTRY PRICE
# ==========================

def dynamic_entry_price(df) -> float:

    return float(
        df["close"].iloc[-1]
    )



# ==========================
# VOLATILITY RISK ENGINE
# ==========================

def volatility_risk(df) -> Dict:


    atr = structure_atr(df)


    candle = structure_true_range(df)


    state = "NORMAL"


    if atr > 0:

        ratio = candle / atr


        if ratio > 2:

            state = "HIGH"


        elif ratio < 0.5:

            state = "LOW"



    return {

        "atr":

            atr,


        "state":

            state

    }



# ==========================
# DYNAMIC STOP LOSS
# ==========================

def dynamic_stop_loss(
        df,
        direction: str
) -> Optional[float]:


    atr = structure_atr(df)


    if atr == 0:

        return None



    if direction == "BUY":

        swing = dynamic_swing_low(df)


        if swing:

            return round(
                swing["price"]
                -
                atr * 0.5,
                4
            )



    if direction == "SELL":

        swing = dynamic_swing_high(df)


        if swing:

            return round(
                swing["price"]
                +
                atr * 0.5,
                4
            )


    return None



# ==========================
# DYNAMIC TAKE PROFIT
# ==========================

def dynamic_targets(
        df,
        direction: str
) -> Dict:


    entry = dynamic_entry_price(df)


    sl = dynamic_stop_loss(
        df,
        direction
    )


    if sl is None:

        return {}



    risk = abs(
        entry - sl
    )


    if direction == "BUY":

        tp1 = entry + risk

        tp2 = entry + (
            risk * 2
        )

        tp3 = entry + (
            risk * 3
        )



    elif direction == "SELL":

        tp1 = entry - risk

        tp2 = entry - (
            risk * 2
        )

        tp3 = entry - (
            risk * 3
        )


    else:

        return {}



    return {

        "entry":

            entry,

        "sl":

            sl,

        "tp1":

            round(tp1,4),

        "tp2":

            round(tp2,4),

        "tp3":

            round(tp3,4)

    }



# ==========================
# RISK REWARD SCORE
# ==========================

def dynamic_rr_score(df) -> int:


    direction = final_market_direction(df)


    targets = dynamic_targets(
        df,
        direction
    )


    if not targets:

        return 0



    risk = abs(
        targets["entry"]
        -
        targets["sl"]
    )


    reward = abs(
        targets["tp2"]
        -
        targets["entry"]
    )


    if risk == 0:

        return 0



    rr = reward / risk


    if rr >= 3:

        return 100


    if rr >= 2:

        return 80


    return 50



# ==========================
# RISK ENGINE OUTPUT
# ==========================

def dynamic_risk_engine(df) -> Dict:


    direction = final_market_direction(df)


    return {

        "direction":

            direction,


        "targets":

            dynamic_targets(
                df,
                direction
            ),


        "volatility":

            volatility_risk(df),


        "rr_score":

            dynamic_rr_score(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_dynamic_risk_v12(df) -> Dict:

    return dynamic_risk_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-10
# Advanced Optimization Layer
# Final Structure Optimization Router
# Module Merge + Clean Interface
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# V12 OPTIMIZED SCORE ENGINE
# ==========================

def v12_optimization_score(df) -> int:


    score = 0


    modules = [

        structure_data_quality(df),

        swing_quality_score(df),

        structure_event_score(df),

        optimized_liquidity_score(df),

        imbalance_strength(df),

        order_block_quality_v12(df),

        pd_ote_score(df),

        confirmation_confidence_v12(df),

        dynamic_rr_score(df)

    ]


    for value in modules:

        if value >= 70:

            score += 11



    return min(score,100)



# ==========================
# FINAL OPTIMIZED DIRECTION
# ==========================

def optimized_direction_v12(df) -> str:


    votes = []


    modules = [

        structure_event_engine(df),

        optimized_liquidity_engine(df),

        optimized_order_block_engine(df),

        optimized_fvg_engine(df)

    ]


    for item in modules:


        if "event" in item:

            if item["event"]:

                votes.append(
                    item["event"]["direction"]
                )



        if "direction" in item:

            if item["direction"] not in [
                None,
                "NONE",
                "RANGE"
            ]:

                votes.append(
                    item["direction"]
                )



        if "order_block" in item:

            if item["order_block"]:

                votes.append(
                    item["order_block"]["direction"]
                )



    buy = votes.count(
        "BUY"
    )

    sell = votes.count(
        "SELL"
    )


    if buy > sell:

        return "BUY"


    if sell > buy:

        return "SELL"


    return "RANGE"



# ==========================
# V12 OPTIMIZED DECISION
# ==========================

def v12_optimized_decision(df) -> Dict:


    direction = optimized_direction_v12(df)


    score = v12_optimization_score(df)


    approved = False


    if (
        direction != "RANGE"
        and
        score >= 80
    ):

        approved = True



    return {

        "approved":

            approved,


        "signal":

            direction
            if approved
            else "NO_TRADE",


        "confidence":

            score,


        "modules":

            {

            "structure":

                structure_event_engine(df),


            "liquidity":

                optimized_liquidity_engine(df),


            "order_block":

                optimized_order_block_engine(df),


            "fvg":

                optimized_fvg_engine(df),


            "pd_ote":

                optimized_pd_ote_engine(df),


            "risk":

                dynamic_risk_engine(df)

            }

    }



# ==========================
# FINAL STRUCTURE ENGINE V12
# ==========================

def structure_engine_v12(df) -> Dict:

    return v12_optimized_decision(df)



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_v12_signal(df) -> Dict:

    return structure_engine_v12(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-11
# Advanced Optimization Layer
# Duplicate Function Resolver + Safe Execution Wrapper
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Any


# ==========================
# SAFE FUNCTION EXECUTION
# ==========================

def safe_structure_call(
        func,
        *args,
        default=None
):

    try:

        return func(*args)

    except Exception:

        return default



# ==========================
# MODULE HEALTH CHECK
# ==========================

def structure_module_health(df) -> Dict:


    modules = {

        "data":

            validate_structure_data(df),


        "swing":

            safe_structure_call(
                dynamic_swing_map,
                df,
                default={}
            ),


        "liquidity":

            safe_structure_call(
                optimized_liquidity_engine,
                df,
                default={}
            ),


        "order_block":

            safe_structure_call(
                optimized_order_block_engine,
                df,
                default={}
            ),


        "fvg":

            safe_structure_call(
                optimized_fvg_engine,
                df,
                default={}
            )

    }


    active = 0


    for value in modules.values():

        if value:

            active += 1



    return {

        "active_modules":

            active,


        "modules":

            modules,


        "healthy":

            active >= 4

    }



# ==========================
# ERROR PROTECTION FILTER
# ==========================

def structure_error_filter(df) -> bool:


    health = structure_module_health(df)


    if not health["healthy"]:

        return False


    return True



# ==========================
# OPTIMIZED SIGNAL WRAPPER
# ==========================

def optimized_signal_wrapper(df) -> Dict:


    if not structure_error_filter(df):

        return {

            "signal":
                "NO_TRADE",

            "reason":
                "MODULE_ERROR"

        }



    result = safe_structure_call(
        v12_optimized_decision,
        df,
        default={}
    )


    if not result:

        return {

            "signal":
                "NO_TRADE",

            "reason":
                "NO_DATA"

        }



    return result



# ==========================
# FINAL SAFE ROUTER
# ==========================

def structure_v12_safe_engine(df) -> Dict:


    result = optimized_signal_wrapper(df)


    return {

        "status":

            "READY"
            if result
            else
            "FAILED",


        "engine":

            result

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_safe_structure_signal(df) -> Dict:

    return structure_v12_safe_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-12
# Advanced Optimization Layer
# Multi Timeframe Structure Sync
# HTF + LTF Alignment Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# TIMEFRAME BIAS CHECK
# ==========================

def timeframe_structure_bias(df) -> str:


    structure = detect_structure(df)


    if structure is None:

        return "RANGE"


    return structure["direction"]



# ==========================
# HTF LTF ALIGNMENT
# ==========================

def multi_timeframe_alignment(
        htf_df,
        ltf_df
) -> Dict:


    htf_bias = timeframe_structure_bias(
        htf_df
    )


    ltf_bias = timeframe_structure_bias(
        ltf_df
    )


    aligned = False


    if (
        htf_bias != "RANGE"
        and
        htf_bias == ltf_bias
    ):

        aligned = True



    return {

        "htf":

            htf_bias,


        "ltf":

            ltf_bias,


        "aligned":

            aligned

    }



# ==========================
# HTF DIRECTION LOCK
# ==========================

def htf_direction_lock(df) -> str:


    structure = detect_structure(df)


    if structure:

        return structure["direction"]


    return "RANGE"



# ==========================
# LTF ENTRY CONFIRMATION
# ==========================

def ltf_execution_confirmation(df) -> bool:


    confirmations = 0


    if optimized_mss(df):

        confirmations += 1


    if optimized_order_block(df):

        confirmations += 1


    if optimized_fvg_detection(df):

        confirmations += 1


    if optimized_liquidity_sweep(df):

        confirmations += 1



    return confirmations >= 3



# ==========================
# MTF SCORE ENGINE
# ==========================

def mtf_structure_score(
        htf_df,
        ltf_df
) -> int:


    score = 0


    alignment = multi_timeframe_alignment(
        htf_df,
        ltf_df
    )


    if alignment["aligned"]:

        score += 50


    if ltf_execution_confirmation(
        ltf_df
    ):

        score += 30


    if detect_displacement(
        ltf_df
    ):

        score += 20



    return min(score,100)



# ==========================
# MTF FINAL ENGINE
# ==========================

def multi_timeframe_structure_engine(
        htf_df,
        ltf_df
) -> Dict:


    alignment = multi_timeframe_alignment(
        htf_df,
        ltf_df
    )


    score = mtf_structure_score(
        htf_df,
        ltf_df
    )


    return {

        "direction":

            alignment["htf"],


        "aligned":

            alignment["aligned"],


        "score":

            score,


        "entry_ready":

            score >= 80

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_mtf_structure_signal(
        htf_df,
        ltf_df
) -> Dict:

    return multi_timeframe_structure_engine(
        htf_df,
        ltf_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-13
# Advanced Optimization Layer
# Institutional Session Timing Engine
# Killzone + Volatility + Timing Filter
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict
from datetime import datetime


# ==========================
# SESSION DETECTION
# ==========================

def detect_trading_session(
        timestamp=None
) -> str:


    if timestamp is None:

        timestamp = datetime.utcnow()



    hour = timestamp.hour



    # ICT London Session

    if 7 <= hour < 10:

        return "LONDON_KILLZONE"



    # ICT New York Session

    if 12 <= hour < 15:

        return "NEW_YORK_KILLZONE"



    # Asian Session

    if 0 <= hour < 6:

        return "ASIA"



    return "OFF_SESSION"



# ==========================
# KILLZONE VALIDATION
# ==========================

def killzone_validation(
        timestamp=None
) -> bool:


    session = detect_trading_session(
        timestamp
    )


    return session in [

        "LONDON_KILLZONE",

        "NEW_YORK_KILLZONE"

    ]



# ==========================
# SESSION VOLATILITY ENGINE
# ==========================

def session_volatility_score(df) -> int:


    score = 0


    if detect_displacement(df):

        score += 40


    if detect_range_expansion(df):

        score += 30


    if optimized_liquidity_sweep(df):

        score += 30



    return min(score,100)



# ==========================
# TIMING QUALITY ENGINE
# ==========================

def timing_quality_engine(
        df,
        timestamp=None
) -> Dict:


    session = detect_trading_session(
        timestamp
    )


    score = session_volatility_score(
        df
    )


    if killzone_validation(
        timestamp
    ):

        score += 20



    return {

        "session":

            session,


        "score":

            min(score,100),


        "valid":

            score >= 70

    }



# ==========================
# ENTRY TIME FILTER
# ==========================

def session_entry_filter(
        df,
        timestamp=None
) -> bool:


    timing = timing_quality_engine(
        df,
        timestamp
    )


    if not timing["valid"]:

        return False


    return True



# ==========================
# SESSION ENGINE OUTPUT
# ==========================

def session_timing_engine(
        df,
        timestamp=None
) -> Dict:


    return {

        "timing":

            timing_quality_engine(
                df,
                timestamp
            ),


        "entry_allowed":

            session_entry_filter(
                df,
                timestamp
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_session_engine_v12(
        df,
        timestamp=None
) -> Dict:

    return session_timing_engine(
        df,
        timestamp
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-14
# Advanced Optimization Layer
# Volume + Momentum Confirmation Engine
# Institutional Participation Filter
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# VOLUME AVERAGE ENGINE
# ==========================

def volume_average_v12(df, period: int = 20) -> float:

    if len(df) < period:

        return 0


    return float(
        df["volume"]
        .tail(period)
        .mean()
    )



# ==========================
# VOLUME SPIKE DETECTION
# ==========================

def detect_volume_spike(df) -> bool:


    avg_volume = volume_average_v12(
        df
    )


    current_volume = float(
        df["volume"].iloc[-1]
    )


    if avg_volume == 0:

        return False



    return current_volume >= (
        avg_volume * 1.5
    )



# ==========================
# BUY SELL VOLUME FLOW
# ==========================

def volume_direction_flow(df) -> str:


    close = float(
        df["close"].iloc[-1]
    )

    open_price = float(
        df["open"].iloc[-1]
    )


    if close > open_price:

        return "BUY"



    if close < open_price:

        return "SELL"



    return "NONE"



# ==========================
# MOMENTUM STRENGTH ENGINE
# ==========================

def momentum_strength_v12(df) -> int:


    score = 0


    if detect_displacement(df):

        score += 40


    if detect_volume_spike(df):

        score += 30


    if structure_atr(df) > 0:

        score += 30



    return min(score,100)



# ==========================
# VOLUME CONFIRMATION
# ==========================

def volume_confirmation_v12(df) -> Dict:


    direction = volume_direction_flow(
        df
    )


    return {

        "volume_spike":

            detect_volume_spike(df),


        "direction":

            direction,


        "momentum":

            momentum_strength_v12(df)

    }



# ==========================
# PARTICIPATION FILTER
# ==========================

def institutional_volume_filter(df) -> bool:


    result = volume_confirmation_v12(
        df
    )


    if not result["volume_spike"]:

        return False


    if result["momentum"] < 70:

        return False


    return True



# ==========================
# FINAL VOLUME ENGINE
# ==========================

def volume_momentum_engine_v12(df) -> Dict:


    return {

        "data":

            volume_confirmation_v12(df),


        "approved":

            institutional_volume_filter(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_volume_engine_v12(df) -> Dict:

    return volume_momentum_engine_v12(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-15
# Advanced Optimization Layer
# Final Institutional Confluence Matrix
# All Module Synchronization Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MODULE CONFIRMATION SCORE
# ==========================

def institutional_confluence_score(df) -> int:


    score = 0


    modules = {


        "structure":

            structure_event_score(df),


        "liquidity":

            optimized_liquidity_score(df),


        "order_block":

            order_block_quality_v12(df),


        "fvg":

            imbalance_strength(df),


        "pd_ote":

            pd_ote_score(df),


        "volume":

            momentum_strength_v12(df),


        "risk":

            dynamic_rr_score(df)

    }



    for value in modules.values():

        if value >= 70:

            score += 14



    return min(score,100)



# ==========================
# DIRECTION AGREEMENT ENGINE
# ==========================

def institutional_direction_sync(df) -> str:


    votes = []


    structure = structure_event_engine(df)

    liquidity = optimized_liquidity_engine(df)

    order_block = optimized_order_block_engine(df)

    fvg = optimized_fvg_engine(df)



    if structure["event"]:

        votes.append(
            structure["event"]["direction"]
        )


    if liquidity["direction"] not in [
        "NONE",
        None
    ]:

        votes.append(
            liquidity["direction"]
        )


    if order_block["order_block"]:

        votes.append(
            order_block["order_block"]["direction"]
        )


    if fvg["direction"] != "NONE":

        votes.append(
            fvg["direction"]
        )



    buy = votes.count(
        "BUY"
    )

    sell = votes.count(
        "SELL"
    )


    if buy > sell:

        return "BUY"


    if sell > buy:

        return "SELL"


    return "RANGE"



# ==========================
# INSTITUTIONAL APPROVAL
# ==========================

def institutional_trade_approval(df) -> Dict:


    score = institutional_confluence_score(
        df
    )


    direction = institutional_direction_sync(
        df
    )


    approved = False



    if (

        score >= 85

        and

        direction != "RANGE"

    ):

        approved = True



    return {

        "approved":

            approved,


        "direction":

            direction,


        "confidence":

            score

    }



# ==========================
# V12 CYCLE COMPLETION CHECK
# ==========================

def structure_v12_cycle_status(df) -> Dict:


    approval = institutional_trade_approval(
        df
    )


    return {

        "status":

            "READY"
            if approval["approved"]
            else
            "WAIT",


        "signal":

            approval["direction"]
            if approval["approved"]
            else
            "NO_TRADE",


        "confidence":

            approval["confidence"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_institutional_signal_v12(df) -> Dict:

    return structure_v12_cycle_status(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-16
# Advanced Optimization Layer
# Market Regime Detection Engine
# Trend + Range + Volatility Classification
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# TREND STRENGTH ENGINE
# ==========================

def trend_strength_v12(df) -> int:


    score = 0


    structure = structure_event_engine(df)


    if structure["event"]:

        score += 40


    if detect_displacement(df):

        score += 30


    if detect_range_expansion(df):

        score += 30



    return min(score,100)



# ==========================
# RANGE MARKET DETECTION
# ==========================

def detect_range_market_v12(df) -> bool:


    if len(df) < 30:

        return True



    high = float(
        df["high"].tail(30).max()
    )


    low = float(
        df["low"].tail(30).min()
    )


    current = float(
        df["close"].iloc[-1]
    )


    total_range = high - low


    if total_range == 0:

        return True



    position = (
        current - low
    ) / total_range



    compression = detect_range_compression(
        df
    )


    if compression:

        return True


    return False



# ==========================
# VOLATILITY REGIME
# ==========================

def volatility_regime_v12(df) -> str:


    volatility = volatility_risk(
        df
    )


    return volatility["state"]



# ==========================
# MARKET REGIME CLASSIFIER
# ==========================

def market_regime_classifier(df) -> Dict:


    trend_score = trend_strength_v12(
        df
    )


    is_range = detect_range_market_v12(
        df
    )


    volatility = volatility_regime_v12(
        df
    )


    regime = "NEUTRAL"



    if is_range:

        regime = "RANGE"



    elif trend_score >= 70:

        regime = "TREND"



    elif volatility == "HIGH":

        regime = "EXPANSION"



    return {

        "regime":

            regime,


        "trend_score":

            trend_score,


        "volatility":

            volatility

    }



# ==========================
# REGIME TRADE FILTER
# ==========================

def regime_trade_filter(df) -> bool:


    result = market_regime_classifier(
        df
    )


    if result["regime"] == "RANGE":

        return False


    return True



# ==========================
# MARKET REGIME ENGINE
# ==========================

def market_regime_engine_v12(df) -> Dict:


    return {

        "data":

            market_regime_classifier(
                df
            ),


        "trade_allowed":

            regime_trade_filter(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_regime_v12(df) -> Dict:

    return market_regime_engine_v12(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-17
# Advanced Optimization Layer
# Liquidity Target Mapping Engine
# Internal + External Draw On Liquidity
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# EXTERNAL LIQUIDITY MAP
# ==========================

def external_liquidity_map(df) -> Dict:


    if len(df) < 50:

        return {}



    high = float(
        df["high"].tail(50).max()
    )


    low = float(
        df["low"].tail(50).min()
    )



    return {

        "buy_side":

            high,


        "sell_side":

            low

    }



# ==========================
# INTERNAL LIQUIDITY MAP
# ==========================

def internal_liquidity_map(df) -> Dict:


    if len(df) < 20:

        return {}



    high = float(
        df["high"].tail(20).max()
    )


    low = float(
        df["low"].tail(20).min()
    )



    return {

        "internal_high":

            high,


        "internal_low":

            low

    }



# ==========================
# DRAW ON LIQUIDITY ENGINE
# ==========================

def draw_on_liquidity(df) -> Optional[Dict]:


    direction = optimized_direction_v12(
        df
    )


    external = external_liquidity_map(
        df
    )


    internal = internal_liquidity_map(
        df
    )



    if direction == "BUY":


        return {

            "target":

                external.get(
                    "buy_side"
                ),


            "type":

                "EXTERNAL_BUY_LIQUIDITY"

        }



    if direction == "SELL":


        return {

            "target":

                external.get(
                    "sell_side"
                ),


            "type":

                "EXTERNAL_SELL_LIQUIDITY"

        }



    return None



# ==========================
# LIQUIDITY DISTANCE CHECK
# ==========================

def liquidity_distance_score(df) -> int:


    target = draw_on_liquidity(
        df
    )


    if target is None:

        return 0



    price = float(
        df["close"].iloc[-1]
    )


    distance = abs(
        target["target"]
        -
        price
    )



    atr = structure_atr(
        df
    )


    if atr == 0:

        return 0



    ratio = distance / atr



    if ratio <= 3:

        return 100


    if ratio <= 5:

        return 70



    return 40



# ==========================
# TARGET VALIDATION
# ==========================

def liquidity_target_validation(df) -> bool:


    target = draw_on_liquidity(
        df
    )


    if target is None:

        return False


    return liquidity_distance_score(
        df
    ) >= 70



# ==========================
# LIQUIDITY TARGET ENGINE
# ==========================

def liquidity_target_engine_v12(df) -> Dict:


    return {

        "external":

            external_liquidity_map(df),


        "internal":

            internal_liquidity_map(df),


        "draw":

            draw_on_liquidity(df),


        "score":

            liquidity_distance_score(df)

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_target_v12(df) -> Dict:

    return liquidity_target_engine_v12(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-18
# Advanced Optimization Layer
# Institutional Trade Narrative Engine
# Bias + Reason + Execution Logic
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET STORY BUILDER
# ==========================

def build_market_narrative_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    regime = market_regime_classifier(
        df
    )


    liquidity = liquidity_target_engine_v12(
        df
    )


    structure = structure_event_engine(
        df
    )


    ob = optimized_order_block_engine(
        df
    )


    fvg = optimized_fvg_engine(
        df
    )



    reasons = []



    if structure["event"]:

        reasons.append(
            structure["event"]["type"]
        )



    if liquidity["draw"]:

        reasons.append(
            "LIQUIDITY_TARGET"
        )



    if ob["order_block"]:

        reasons.append(
            "ORDER_BLOCK"
        )



    if fvg["fvg"]:

        reasons.append(
            "FVG"
        )



    if regime["regime"] != "RANGE":

        reasons.append(
            regime["regime"]
        )



    return {

        "direction":

            direction,


        "reasons":

            reasons,


        "regime":

            regime["regime"]

    }



# ==========================
# NARRATIVE CONFIDENCE
# ==========================

def narrative_confidence_v12(df) -> int:


    narrative = build_market_narrative_v12(
        df
    )


    score = 0


    score += len(
        narrative["reasons"]
    ) * 15



    if narrative["direction"] != "RANGE":

        score += 20



    return min(score,100)



# ==========================
# TRADE STORY VALIDATION
# ==========================

def validate_trade_story(df) -> bool:


    narrative = build_market_narrative_v12(
        df
    )


    confidence = narrative_confidence_v12(
        df
    )


    if narrative["direction"] == "RANGE":

        return False


    if confidence < 75:

        return False


    return True



# ==========================
# INSTITUTIONAL NARRATIVE ENGINE
# ==========================

def institutional_narrative_engine(df) -> Dict:


    return {

        "narrative":

            build_market_narrative_v12(
                df
            ),


        "confidence":

            narrative_confidence_v12(
                df
            ),


        "valid":

            validate_trade_story(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_narrative_v12(df) -> Dict:

    return institutional_narrative_engine(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-19
# Advanced Optimization Layer
# Trade Execution Readiness Engine
# Final Entry Permission Filter
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EXECUTION CHECKLIST
# ==========================

def execution_checklist_v12(df) -> Dict:


    checks = {


        "structure":

            bool(
                structure_event_engine(df)
                ["event"]
            ),


        "liquidity":

            bool(
                optimized_liquidity_sweep(df)
            ),


        "order_block":

            bool(
                optimized_order_block(df)
            ),


        "fvg":

            bool(
                optimized_fvg_detection(df)
            ),


        "pd_ote":

            pd_ote_score(df) >= 70,


        "volume":

            institutional_volume_filter(df),


        "session":

            session_entry_filter(df),


        "regime":

            regime_trade_filter(df)

    }



    passed = 0


    for value in checks.values():

        if value:

            passed += 1



    return {

        "checks":

            checks,


        "passed":

            passed

    }



# ==========================
# ENTRY READINESS SCORE
# ==========================

def execution_readiness_score(df) -> int:


    result = execution_checklist_v12(
        df
    )


    score = (
        result["passed"]
        /
        len(result["checks"])
    ) * 100



    return int(score)



# ==========================
# FINAL ENTRY PERMISSION
# ==========================

def final_execution_permission(df) -> Dict:


    score = execution_readiness_score(
        df
    )


    direction = optimized_direction_v12(
        df
    )


    approved = False



    if (

        score >= 80

        and

        direction != "RANGE"

    ):

        approved = True



    return {

        "approved":

            approved,


        "direction":

            direction,


        "score":

            score

    }



# ==========================
# EXECUTION ENGINE OUTPUT
# ==========================

def execution_engine_v12(df) -> Dict:


    return {

        "permission":

            final_execution_permission(
                df
            ),


        "checklist":

            execution_checklist_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_signal_v12(df) -> Dict:

    return execution_engine_v12(df)
    # ==========================
# STRUCTURE ENGINE V12
# PART 2C-20
# Advanced Optimization Layer
# Final Structure Intelligence Aggregator
# Complete C-Series Integration
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# V12 CYCLE MODULE SCORE
# ==========================

def c_series_module_score_v12(df) -> int:


    modules = [

        structure_data_quality(df),

        swing_quality_score(df),

        structure_event_score(df),

        optimized_liquidity_score(df),

        imbalance_strength(df),

        order_block_quality_v12(df),

        pd_ote_score(df),

        confirmation_confidence_v12(df),

        dynamic_rr_score(df),

        trend_strength_v12(df),

        institutional_confluence_score(df),

        execution_readiness_score(df)

    ]


    total = 0


    active = 0


    for value in modules:


        if value >= 70:

            total += value

            active += 1



    if active == 0:

        return 0



    return int(
        total / active
    )



# ==========================
# FINAL C-SERIES BIAS
# ==========================

def c_series_bias_engine(df) -> str:


    votes = []


    sources = [

        structure_event_engine(df),

        optimized_liquidity_engine(df),

        optimized_order_block_engine(df),

        optimized_fvg_engine(df)

    ]


    for source in sources:


        if "event" in source:

            if source["event"]:

                votes.append(
                    source["event"]["direction"]
                )



        if "direction" in source:


            if source["direction"] not in [

                "NONE",

                "RANGE",

                None

            ]:

                votes.append(
                    source["direction"]
                )



        if "order_block" in source:


            if source["order_block"]:

                votes.append(
                    source["order_block"]["direction"]
                )



    buy = votes.count(
        "BUY"
    )


    sell = votes.count(
        "SELL"
    )



    if buy > sell:

        return "BUY"



    if sell > buy:

        return "SELL"



    return "RANGE"



# ==========================
# C-SERIES FINAL INTELLIGENCE
# ==========================

def c_series_intelligence_engine(df) -> Dict:


    score = c_series_module_score_v12(
        df
    )


    bias = c_series_bias_engine(
        df
    )


    execution = final_execution_permission(
        df
    )



    approved = False



    if (

        score >= 80

        and

        bias != "RANGE"

        and

        execution["approved"]

    ):

        approved = True



    return {

        "approved":

            approved,


        "signal":

            bias
            if approved
            else
            "NO_TRADE",


        "confidence":

            score,


        "execution":

            execution,


        "bias":

            bias

    }



# ==========================
# STRUCTURE ENGINE V12 C FINAL
# ==========================

def structure_engine_v12_c_series(df) -> Dict:


    return c_series_intelligence_engine(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_c_series_v12(df) -> Dict:

    return structure_engine_v12_c_series(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-1
# Multi Timeframe Intelligence Layer
# HTF Bias + LTF Execution Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# TIMEFRAME WEIGHT SYSTEM
# ==========================

def timeframe_weight_v12(tf: str) -> int:


    weights = {

        "1D": 40,

        "4H": 30,

        "1H": 20,

        "15M": 10,

        "5M": 5

    }


    return weights.get(
        tf,
        0
    )



# ==========================
# HTF BIAS ENGINE
# ==========================

def htf_bias_engine_v12(df) -> Dict:


    structure = structure_event_engine(
        df
    )


    direction = "RANGE"

    score = 0



    if structure["event"]:


        direction = structure["event"]["direction"]

        score += 40



    if optimized_liquidity_engine(df)["sweep"]:

        score += 20



    if detect_displacement(df):

        score += 20



    if optimized_order_block(df):

        score += 20



    return {

        "bias":

            direction,


        "score":

            min(score,100)

    }



# ==========================
# LTF EXECUTION BIAS
# ==========================

def ltf_bias_engine_v12(df) -> Dict:


    score = 0

    direction = optimized_direction_v12(
        df
    )



    if detect_mss(df):

        score += 30



    if optimized_fvg_detection(df):

        score += 20



    if optimized_liquidity_sweep(df):

        score += 25



    if detect_displacement(df):

        score += 25



    return {

        "bias":

            direction,


        "score":

            min(score,100)

    }



# ==========================
# MTF ALIGNMENT ENGINE
# ==========================

def mtf_alignment_v12(
        htf_df,
        ltf_df
) -> Dict:


    htf = htf_bias_engine_v12(
        htf_df
    )


    ltf = ltf_bias_engine_v12(
        ltf_df
    )



    aligned = (

        htf["bias"]
        ==
        ltf["bias"]

        and

        htf["bias"]
        !=
        "RANGE"

    )



    return {

        "aligned":

            aligned,


        "direction":

            htf["bias"],


        "htf_score":

            htf["score"],


        "ltf_score":

            ltf["score"]

    }



# ==========================
# MTF CONFIDENCE SCORE
# ==========================

def mtf_confidence_v12(
        htf_df,
        ltf_df
) -> int:


    result = mtf_alignment_v12(
        htf_df,
        ltf_df
    )


    score = 0


    if result["aligned"]:

        score += 50



    score += int(
        (
            result["htf_score"]
            +
            result["ltf_score"]
        )
        /4
    )


    return min(score,100)



# ==========================
# FINAL MTF ENGINE
# ==========================

def multi_timeframe_intelligence_v12(
        htf_df,
        ltf_df
) -> Dict:


    confidence = mtf_confidence_v12(
        htf_df,
        ltf_df
    )


    result = mtf_alignment_v12(
        htf_df,
        ltf_df
    )


    return {

        "direction":

            result["direction"],


        "confidence":

            confidence,


        "approved":

            confidence >= 80

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_mtf_intelligence_v12(
        htf_df,
        ltf_df
) -> Dict:

    return multi_timeframe_intelligence_v12(
        htf_df,
        ltf_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-2
# Multi Timeframe Intelligence Layer
# HTF Liquidity Mapping + LTF Entry Zone Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# HTF LIQUIDITY MAP
# ==========================

def htf_liquidity_map_v12(df) -> Dict:


    if len(df) < 50:

        return {}



    high = float(
        df["high"].tail(50).max()
    )


    low = float(
        df["low"].tail(50).min()
    )



    return {

        "external_high":

            high,


        "external_low":

            low

    }



# ==========================
# HTF DRAW ON LIQUIDITY
# ==========================

def htf_draw_on_liquidity(df) -> Dict:


    direction = htf_bias_engine_v12(
        df
    )["bias"]


    liquidity = htf_liquidity_map_v12(
        df
    )



    target = None



    if direction == "BUY":

        target = liquidity.get(
            "external_high"
        )



    elif direction == "SELL":

        target = liquidity.get(
            "external_low"
        )



    return {

        "direction":

            direction,


        "target":

            target

    }



# ==========================
# LTF ENTRY ZONE DETECTION
# ==========================

def ltf_entry_zone_v12(df) -> Optional[Dict]:


    ob = optimized_order_block(
        df
    )


    fvg = optimized_fvg_detection(
        df
    )



    if ob:


        return {

            "type":

                "ORDER_BLOCK",


            "direction":

                ob["direction"],


            "high":

                ob["high"],


            "low":

                ob["low"]

        }



    if fvg:


        return {

            "type":

                "FVG",


            "direction":

                fvg["direction"],


            "high":

                fvg["high"],


            "low":

                fvg["low"]

        }



    return None



# ==========================
# ZONE ALIGNMENT ENGINE
# ==========================

def htf_ltf_zone_alignment(
        htf_df,
        ltf_df
) -> Dict:


    htf = htf_bias_engine_v12(
        htf_df
    )


    zone = ltf_entry_zone_v12(
        ltf_df
    )



    aligned = False



    if zone:


        if zone["direction"] == htf["bias"]:

            aligned = True



    return {

        "aligned":

            aligned,


        "htf_bias":

            htf["bias"],


        "zone":

            zone

    }



# ==========================
# MTF ZONE SCORE
# ==========================

def mtf_zone_score(
        htf_df,
        ltf_df
) -> int:


    result = htf_ltf_zone_alignment(
        htf_df,
        ltf_df
    )


    score = 0



    if result["aligned"]:

        score += 60



    if detect_liquidity_sweep(
        ltf_df
    ):

        score += 20



    if detect_displacement(
        ltf_df
    ):

        score += 20



    return min(score,100)



# ==========================
# FINAL MTF ZONE ENGINE
# ==========================

def mtf_zone_engine_v12(
        htf_df,
        ltf_df
) -> Dict:


    return {

        "alignment":

            htf_ltf_zone_alignment(
                htf_df,
                ltf_df
            ),


        "score":

            mtf_zone_score(
                htf_df,
                ltf_df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_mtf_zone_v12(
        htf_df,
        ltf_df
) -> Dict:

    return mtf_zone_engine_v12(
        htf_df,
        ltf_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-3
# Multi Timeframe Intelligence Layer
# HTF Market Structure Shift Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# HTF STRUCTURE SHIFT
# ==========================

def htf_mss_detection_v12(df) -> Optional[Dict]:


    swing_high = dynamic_swing_high(
        df
    )


    swing_low = dynamic_swing_low(
        df
    )



    if (
        swing_high is None
        or
        swing_low is None
    ):

        return None



    close = float(
        df["close"].iloc[-1]
    )



    if close > swing_high["price"]:


        return {

            "type":

                "HTF_MSS",


            "direction":

                "BUY",


            "level":

                swing_high["price"]

        }



    if close < swing_low["price"]:


        return {

            "type":

                "HTF_MSS",


            "direction":

                "SELL",


            "level":

                swing_low["price"]

        }



    return None



# ==========================
# HTF BOS CONFIRMATION
# ==========================

def htf_bos_confirmation_v12(df) -> bool:


    bos = internal_structure_break(
        df
    )


    if bos:

        return True


    return False



# ==========================
# HTF STRUCTURE QUALITY
# ==========================

def htf_structure_quality_v12(df) -> int:


    score = 0


    if htf_mss_detection_v12(df):

        score += 40



    if htf_bos_confirmation_v12(df):

        score += 30



    if detect_displacement(df):

        score += 30



    return min(score,100)



# ==========================
# HTF STRUCTURE ENGINE
# ==========================

def htf_structure_engine_v12(df) -> Dict:


    mss = htf_mss_detection_v12(
        df
    )


    direction = "RANGE"



    if mss:

        direction = mss["direction"]



    return {

        "direction":

            direction,


        "mss":

            mss,


        "quality":

            htf_structure_quality_v12(
                df
            )

    }



# ==========================
# HTF STRUCTURE FILTER
# ==========================

def htf_structure_filter_v12(df) -> bool:


    result = htf_structure_engine_v12(
        df
    )


    if result["quality"] < 70:

        return False



    if result["direction"] == "RANGE":

        return False



    return True



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_htf_structure_v12(df) -> Dict:

    return {

        "structure":

            htf_structure_engine_v12(
                df
            ),


        "valid":

            htf_structure_filter_v12(
                df
            )

    }
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-4
# Multi Timeframe Intelligence Layer
# HTF Order Flow + LTF Execution Synchronization
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# HTF ORDER FLOW ENGINE
# ==========================

def htf_order_flow_v12(df) -> Dict:


    flow = []


    structure = htf_structure_engine_v12(
        df
    )


    liquidity = optimized_liquidity_engine(
        df
    )


    ob = optimized_order_block_engine(
        df
    )


    fvg = optimized_fvg_engine(
        df
    )



    if structure["direction"] != "RANGE":

        flow.append(
            structure["direction"]
        )



    if liquidity["direction"] not in [
        "NONE",
        None
    ]:

        flow.append(
            liquidity["direction"]
        )



    if ob["order_block"]:

        flow.append(
            ob["order_block"]["direction"]
        )



    if fvg["direction"] != "NONE":

        flow.append(
            fvg["direction"]
        )



    buy = flow.count(
        "BUY"
    )


    sell = flow.count(
        "SELL"
    )



    direction = "RANGE"



    if buy > sell:

        direction = "BUY"



    elif sell > buy:

        direction = "SELL"



    return {

        "direction":

            direction,


        "confirmations":

            len(flow),


        "flow":

            flow

    }



# ==========================
# LTF EXECUTION SYNC
# ==========================

def ltf_execution_sync_v12(
        htf_df,
        ltf_df
) -> Dict:


    htf_flow = htf_order_flow_v12(
        htf_df
    )


    ltf_direction = optimized_direction_v12(
        ltf_df
    )



    aligned = False



    if (

        htf_flow["direction"]
        ==
        ltf_direction

        and

        htf_flow["direction"]
        !=
        "RANGE"

    ):

        aligned = True



    return {

        "aligned":

            aligned,


        "direction":

            htf_flow["direction"],


        "ltf":

            ltf_direction

    }



# ==========================
# ORDER FLOW CONFIDENCE
# ==========================

def order_flow_confidence_v12(
        htf_df,
        ltf_df
) -> int:


    result = ltf_execution_sync_v12(
        htf_df,
        ltf_df
    )


    score = 0



    if result["aligned"]:

        score += 60



    if ltf_execution_confirmation(
        ltf_df
    ):

        score += 25



    if detect_displacement(
        ltf_df
    ):

        score += 15



    return min(score,100)



# ==========================
# FINAL ORDER FLOW ENGINE
# ==========================

def mtf_order_flow_engine_v12(
        htf_df,
        ltf_df
) -> Dict:


    return {

        "sync":

            ltf_execution_sync_v12(
                htf_df,
                ltf_df
            ),


        "confidence":

            order_flow_confidence_v12(
                htf_df,
                ltf_df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_mtf_order_flow_v12(
        htf_df,
        ltf_df
) -> Dict:

    return mtf_order_flow_engine_v12(
        htf_df,
        ltf_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-5
# Multi Timeframe Intelligence Layer
# Liquidity Sweep + Reversal Confirmation Engine
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# LIQUIDITY SWEEP DETECTION
# ==========================

def mtf_liquidity_sweep_v12(df) -> Optional[Dict]:


    if len(df) < 20:

        return None



    previous_high = float(
        df["high"]
        .iloc[-20:-1]
        .max()
    )


    previous_low = float(
        df["low"]
        .iloc[-20:-1]
        .min()
    )


    current_high = float(
        df["high"].iloc[-1]
    )


    current_low = float(
        df["low"].iloc[-1]
    )


    close = float(
        df["close"].iloc[-1]
    )



    # Buy Side Liquidity Sweep

    if (

        current_high > previous_high

        and

        close < previous_high

    ):

        return {

            "type":

                "BUY_SIDE_SWEEP",


            "direction":

                "SELL",


            "level":

                previous_high

        }



    # Sell Side Liquidity Sweep

    if (

        current_low < previous_low

        and

        close > previous_low

    ):

        return {

            "type":

                "SELL_SIDE_SWEEP",


            "direction":

                "BUY",


            "level":

                previous_low

        }



    return None



# ==========================
# SWEEP + STRUCTURE CONFIRM
# ==========================

def sweep_structure_confirmation_v12(df) -> bool:


    sweep = mtf_liquidity_sweep_v12(
        df
    )


    if sweep is None:

        return False



    mss = htf_mss_detection_v12(
        df
    )


    if mss is None:

        return False



    return (
        sweep["direction"]
        ==
        mss["direction"]
    )



# ==========================
# LIQUIDITY REVERSAL SCORE
# ==========================

def liquidity_reversal_score_v12(df) -> int:


    score = 0


    sweep = mtf_liquidity_sweep_v12(
        df
    )


    if sweep:

        score += 40



    if sweep_structure_confirmation_v12(
        df
    ):

        score += 30



    if detect_displacement(df):

        score += 20



    if optimized_fvg_detection(df):

        score += 10



    return min(score,100)



# ==========================
# LIQUIDITY REVERSAL ENGINE
# ==========================

def liquidity_reversal_engine_v12(df) -> Dict:


    sweep = mtf_liquidity_sweep_v12(
        df
    )


    return {

        "sweep":

            sweep,


        "score":

            liquidity_reversal_score_v12(
                df
            ),


        "confirmed":

            liquidity_reversal_score_v12(
                df
            ) >= 80

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_reversal_v12(df) -> Dict:

    return liquidity_reversal_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-6
# Multi Timeframe Intelligence Layer
# Premium Entry Model + Institutional POI Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# INSTITUTIONAL POI DETECTION
# ==========================

def institutional_poi_v12(df) -> Optional[Dict]:


    ob = optimized_order_block(
        df
    )


    fvg = optimized_fvg_detection(
        df
    )


    poi = None



    if ob:


        poi = {

            "type":

                "ORDER_BLOCK",


            "direction":

                ob["direction"],


            "high":

                ob["high"],


            "low":

                ob["low"]

        }



    elif fvg:


        poi = {

            "type":

                "FVG",


            "direction":

                fvg["direction"],


            "high":

                fvg["high"],


            "low":

                fvg["low"]

        }



    return poi



# ==========================
# POI PRICE LOCATION
# ==========================

def poi_location_check_v12(df) -> bool:


    poi = institutional_poi_v12(
        df
    )


    if poi is None:

        return False



    price = float(
        df["close"].iloc[-1]
    )



    return (

        price >= poi["low"]

        and

        price <= poi["high"]

    )



# ==========================
# PREMIUM ENTRY VALIDATION
# ==========================

def premium_entry_validation_v12(
        df,
        direction: str
) -> int:


    score = 0


    poi = institutional_poi_v12(
        df
    )


    if poi:

        score += 30



    if poi_location_check_v12(
        df
    ):

        score += 30



    if optimized_ote_validation(
        df,
        direction
    ):

        score += 20



    if detect_liquidity_sweep(
        df
    ):

        score += 20



    return min(score,100)



# ==========================
# ENTRY MODEL ENGINE
# ==========================

def institutional_entry_model_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    score = premium_entry_validation_v12(
        df,
        direction
    )


    return {

        "direction":

            direction,


        "poi":

            institutional_poi_v12(
                df
            ),


        "score":

            score,


        "approved":

            score >= 80

    }



# ==========================
# MTF ENTRY SYNCHRONIZATION
# ==========================

def mtf_entry_sync_v12(
        htf_df,
        ltf_df
) -> Dict:


    htf = htf_bias_engine_v12(
        htf_df
    )


    entry = institutional_entry_model_v12(
        ltf_df
    )



    return {

        "aligned":

            htf["bias"]
            ==
            entry["direction"],


        "direction":

            htf["bias"],


        "entry_score":

            entry["score"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_institutional_entry_v12(df) -> Dict:

    return institutional_entry_model_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-7
# Multi Timeframe Intelligence Layer
# Smart Money Trap Detection Engine
# Liquidity Grab + Fake Breakout Filter
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# FAKE BREAKOUT DETECTION
# ==========================

def fake_breakout_detection_v12(df) -> Optional[Dict]:


    if len(df) < 15:

        return None



    recent_high = float(
        df["high"]
        .iloc[-15:-1]
        .max()
    )


    recent_low = float(
        df["low"]
        .iloc[-15:-1]
        .min()
    )


    high = float(
        df["high"].iloc[-1]
    )


    low = float(
        df["low"].iloc[-1]
    )


    close = float(
        df["close"].iloc[-1]
    )



    # Bull trap

    if (

        high > recent_high

        and

        close < recent_high

    ):

        return {

            "type":

                "BULL_TRAP",


            "direction":

                "SELL",


            "level":

                recent_high

        }



    # Bear trap

    if (

        low < recent_low

        and

        close > recent_low

    ):

        return {

            "type":

                "BEAR_TRAP",


            "direction":

                "BUY",


            "level":

                recent_low

        }



    return None



# ==========================
# SMART MONEY TRAP SCORE
# ==========================

def smart_money_trap_score_v12(df) -> int:


    score = 0


    trap = fake_breakout_detection_v12(
        df
    )


    if trap:

        score += 40



    if mtf_liquidity_sweep_v12(df):

        score += 25



    if detect_displacement(df):

        score += 20



    if optimized_fvg_detection(df):

        score += 15



    return min(score,100)



# ==========================
# TRAP REVERSAL VALIDATION
# ==========================

def trap_reversal_validation_v12(df) -> bool:


    trap = fake_breakout_detection_v12(
        df
    )


    if trap is None:

        return False



    score = smart_money_trap_score_v12(
        df
    )


    return score >= 70



# ==========================
# SMART MONEY TRAP ENGINE
# ==========================

def smart_money_trap_engine_v12(df) -> Dict:


    return {

        "trap":

            fake_breakout_detection_v12(
                df
            ),


        "score":

            smart_money_trap_score_v12(
                df
            ),


        "confirmed":

            trap_reversal_validation_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_smart_money_trap_v12(df) -> Dict:

    return smart_money_trap_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-8
# Multi Timeframe Intelligence Layer
# Institutional Entry Trigger Engine
# MSS + BOS + Liquidity + POI Execution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EXECUTION TRIGGER DETECTION
# ==========================

def execution_trigger_v12(df) -> Dict:


    confirmations = []


    direction = optimized_direction_v12(
        df
    )



    # Market Structure Shift

    if detect_mss(df):

        confirmations.append(
            "MSS"
        )



    # Break Of Structure

    if internal_structure_break(df):

        confirmations.append(
            "BOS"
        )



    # Liquidity Sweep

    if mtf_liquidity_sweep_v12(df):

        confirmations.append(
            "LIQUIDITY_SWEEP"
        )



    # Order Block

    if optimized_order_block(df):

        confirmations.append(
            "ORDER_BLOCK"
        )



    # Fair Value Gap

    if optimized_fvg_detection(df):

        confirmations.append(
            "FVG"
        )



    return {

        "direction":

            direction,


        "confirmations":

            confirmations,


        "count":

            len(confirmations)

    }



# ==========================
# TRIGGER SCORE
# ==========================

def execution_trigger_score_v12(df) -> int:


    result = execution_trigger_v12(
        df
    )


    score = (
        result["count"]
        *
        20
    )


    if detect_displacement(df):

        score += 20



    return min(score,100)



# ==========================
# ENTRY TRIGGER FILTER
# ==========================

def execution_trigger_filter_v12(df) -> bool:


    result = execution_trigger_v12(
        df
    )


    score = execution_trigger_score_v12(
        df
    )



    if result["direction"] == "RANGE":

        return False



    if result["count"] < 4:

        return False



    if score < 80:

        return False



    return True



# ==========================
# FINAL ENTRY TRIGGER ENGINE
# ==========================

def institutional_execution_trigger_v12(df) -> Dict:


    result = execution_trigger_v12(
        df
    )


    return {

        "direction":

            result["direction"],


        "confirmations":

            result["confirmations"],


        "score":

            execution_trigger_score_v12(
                df
            ),


        "approved":

            execution_trigger_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_trigger_v12(df) -> Dict:

    return institutional_execution_trigger_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-9
# Multi Timeframe Intelligence Layer
# Institutional Trade Management Engine
# Dynamic SL + TP + Position Logic
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# ENTRY LEVEL ENGINE
# ==========================

def institutional_entry_level_v12(df) -> float:


    return float(
        df["close"].iloc[-1]
    )



# ==========================
# SWING BASED STOP LOSS
# ==========================

def institutional_stop_loss_v12(
        df,
        direction: str
) -> Optional[float]:


    atr = structure_atr(
        df
    )


    if atr == 0:

        return None



    if direction == "BUY":


        swing = dynamic_swing_low(
            df
        )


        if swing:

            return round(

                swing["price"]
                -
                atr * 0.3,

                4

            )



    if direction == "SELL":


        swing = dynamic_swing_high(
            df
        )


        if swing:

            return round(

                swing["price"]
                +
                atr * 0.3,

                4

            )



    return None



# ==========================
# INSTITUTIONAL TARGET MAP
# ==========================

def institutional_targets_v12(
        df,
        direction: str
) -> Dict:


    entry = institutional_entry_level_v12(
        df
    )


    sl = institutional_stop_loss_v12(
        df,
        direction
    )


    if sl is None:

        return {}



    risk = abs(
        entry - sl
    )



    if direction == "BUY":


        return {

            "entry":

                entry,


            "sl":

                sl,


            "tp1":

                round(
                    entry + risk,
                    4
                ),


            "tp2":

                round(
                    entry + risk*2,
                    4
                ),


            "tp3":

                round(
                    entry + risk*3,
                    4
                )

        }



    if direction == "SELL":


        return {

            "entry":

                entry,


            "sl":

                sl,


            "tp1":

                round(
                    entry - risk,
                    4
                ),


            "tp2":

                round(
                    entry - risk*2,
                    4
                ),


            "tp3":

                round(
                    entry - risk*3,
                    4
                )

        }



    return {}



# ==========================
# TRADE MANAGEMENT SCORE
# ==========================

def trade_management_score_v12(df) -> int:


    direction = optimized_direction_v12(
        df
    )


    targets = institutional_targets_v12(
        df,
        direction
    )


    score = 0



    if targets:

        score += 50



    if dynamic_rr_score(df) >= 80:

        score += 30



    if liquidity_target_validation(df):

        score += 20



    return min(score,100)



# ==========================
# TRADE MANAGEMENT ENGINE
# ==========================

def institutional_trade_management_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    return {

        "direction":

            direction,


        "targets":

            institutional_targets_v12(
                df,
                direction
            ),


        "score":

            trade_management_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_management_v12(df) -> Dict:

    return institutional_trade_management_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-10
# Multi Timeframe Intelligence Layer
# Institutional Final Signal Fusion Engine
# Structure + Liquidity + Execution + Risk
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL MODULE WEIGHT ENGINE
# ==========================

def final_module_weight_v12(df) -> Dict:


    modules = {


        "structure":

            structure_event_score(df),


        "mtf":

            mtf_confidence_v12_score(df),


        "liquidity":

            liquidity_reversal_score_v12(df),


        "entry":

            execution_trigger_score_v12(df),


        "poi":

            premium_entry_validation_v12(
                df,
                optimized_direction_v12(df)
            ),


        "risk":

            trade_management_score_v12(df)

    }



    return modules



# ==========================
# FINAL CONFIDENCE CALCULATION
# ==========================

def final_confidence_v12(df) -> int:


    modules = final_module_weight_v12(
        df
    )


    total = 0


    count = 0



    for value in modules.values():

        total += value

        count += 1



    if count == 0:

        return 0



    return int(
        total / count
    )



# ==========================
# FINAL SIGNAL DIRECTION
# ==========================

def final_signal_direction_v12(df) -> str:


    direction = optimized_direction_v12(
        df
    )


    trigger = execution_trigger_v12(
        df
    )


    if (

        trigger["direction"]
        ==
        direction

    ):

        return direction



    return "RANGE"



# ==========================
# FINAL TRADE APPROVAL
# ==========================

def final_trade_approval_v12(df) -> Dict:


    confidence = final_confidence_v12(
        df
    )


    direction = final_signal_direction_v12(
        df
    )


    approved = False



    if (

        confidence >= 85

        and

        direction != "RANGE"

    ):

        approved = True



    return {


        "signal":

            direction
            if approved
            else
            "NO_TRADE",


        "approved":

            approved,


        "confidence":

            confidence,


        "modules":

            final_module_weight_v12(
                df
            )

    }



# ==========================
# V12 D-SERIES ROUTER
# ==========================

def structure_engine_v12_d_series(df) -> Dict:


    return final_trade_approval_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_d_series_v12(df) -> Dict:

    return structure_engine_v12_d_series(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-11
# Multi Timeframe Intelligence Layer
# Institutional Signal Protection Engine
# Noise Filter + False Signal Rejection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET NOISE DETECTION
# ==========================

def market_noise_filter_v12(df) -> Dict:


    score = 0


    reasons = []



    # Low volatility filter

    atr = structure_atr(df)


    if atr > 0:

        recent_range = structure_true_range(
            df
        )


        ratio = recent_range / atr


        if ratio < 0.5:

            score += 30

            reasons.append(
                "LOW_VOLATILITY"
            )



    # Small candle compression

    if detect_range_compression(df):

        score += 30

        reasons.append(
            "COMPRESSION"
        )



    # Weak displacement

    if not detect_displacement(df):

        score += 20

        reasons.append(
            "NO_DISPLACEMENT"
        )



    # Missing liquidity

    if not optimized_liquidity_sweep(df):

        score += 20

        reasons.append(
            "NO_LIQUIDITY"
        )



    return {

        "noise_score":

            min(score,100),


        "reasons":

            reasons

    }



# ==========================
# FALSE BREAK FILTER
# ==========================

def false_break_filter_v12(df) -> bool:


    trap = fake_breakout_detection_v12(
        df
    )


    if trap:

        return False



    return True



# ==========================
# SIGNAL QUALITY CHECK
# ==========================

def signal_quality_filter_v12(df) -> Dict:


    noise = market_noise_filter_v12(
        df
    )


    quality = 100 - noise["noise_score"]



    return {

        "quality":

            max(quality,0),


        "valid":

            quality >= 70,


        "noise":

            noise["reasons"]

    }



# ==========================
# FINAL PROTECTION LAYER
# ==========================

def institutional_protection_engine_v12(df) -> Dict:


    quality = signal_quality_filter_v12(
        df
    )


    false_break = false_break_filter_v12(
        df
    )



    approved = (

        quality["valid"]

        and

        false_break

    )



    return {

        "approved":

            approved,


        "quality":

            quality["quality"],


        "noise":

            quality["noise"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_signal_protection_v12(df) -> Dict:

    return institutional_protection_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-12
# Multi Timeframe Intelligence Layer
# Institutional Market State Engine
# Trend Phase + Expansion + Reversal Detection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET PHASE DETECTION
# ==========================

def market_phase_v12(df) -> str:


    if detect_range_market_v12(df):

        return "ACCUMULATION"



    if detect_displacement(df):

        direction = optimized_direction_v12(
            df
        )


        if direction != "RANGE":

            return "EXPANSION"



    trap = fake_breakout_detection_v12(
        df
    )


    if trap:

        return "MANIPULATION"



    return "DISTRIBUTION"



# ==========================
# TREND CONTINUATION ENGINE
# ==========================

def trend_continuation_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    score = 0


    if direction != "RANGE":

        score += 30



    if internal_structure_break(df):

        score += 25



    if detect_displacement(df):

        score += 25



    if optimized_fvg_detection(df):

        score += 20



    return {

        "direction":

            direction,


        "score":

            min(score,100)

    }



# ==========================
# REVERSAL PROBABILITY
# ==========================

def reversal_probability_v12(df) -> int:


    score = 0


    if mtf_liquidity_sweep_v12(df):

        score += 40



    if fake_breakout_detection_v12(df):

        score += 30



    if detect_mss(df):

        score += 30



    return min(score,100)



# ==========================
# MARKET STATE ENGINE
# ==========================

def market_state_engine_v12(df) -> Dict:


    phase = market_phase_v12(
        df
    )


    continuation = trend_continuation_v12(
        df
    )


    reversal = reversal_probability_v12(
        df
    )



    return {

        "phase":

            phase,


        "trend":

            continuation,


        "reversal_score":

            reversal

    }



# ==========================
# TRADE PHASE FILTER
# ==========================

def market_phase_filter_v12(df) -> bool:


    state = market_state_engine_v12(
        df
    )


    if state["phase"] == "ACCUMULATION":

        return False



    return True



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_state_v12(df) -> Dict:

    return market_state_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-13
# Multi Timeframe Intelligence Layer
# Institutional Confluence Ranking Engine
# Setup Ranking + Priority Selection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# SETUP COMPONENT RANKING
# ==========================

def rank_setup_components_v12(df) -> Dict:


    components = {


        "HTF_STRUCTURE":

            htf_structure_quality_v12(df),


        "LIQUIDITY":

            liquidity_reversal_score_v12(df),


        "ORDER_BLOCK":

            order_block_quality_v12(df),


        "FVG":

            imbalance_strength(df),


        "ENTRY_TRIGGER":

            execution_trigger_score_v12(df),


        "MARKET_STATE":

            trend_strength_v12(df),


        "RISK":

            trade_management_score_v12(df)

    }



    return components



# ==========================
# SETUP GRADE CALCULATOR
# ==========================

def setup_grade_v12(df) -> str:


    components = rank_setup_components_v12(
        df
    )


    total = 0


    for value in components.values():

        total += value



    average = total / len(
        components
    )



    if average >= 90:

        return "A+"


    if average >= 80:

        return "A"



    if average >= 70:

        return "B"



    return "C"



# ==========================
# PRIORITY SCORE
# ==========================

def setup_priority_score_v12(df) -> int:


    components = rank_setup_components_v12(
        df
    )


    priority = 0



    for value in components.values():

        if value >= 80:

            priority += 14



    return min(priority,100)



# ==========================
# BEST SETUP SELECTOR
# ==========================

def select_best_setup_v12(df) -> Dict:


    grade = setup_grade_v12(
        df
    )


    score = setup_priority_score_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )



    return {

        "grade":

            grade,


        "priority":

            score,


        "direction":

            direction,


        "trade_ready":

            (
                score >= 80

                and

                direction != "RANGE"

            )

    }



# ==========================
# CONFLUENCE RANK ENGINE
# ==========================

def confluence_ranking_engine_v12(df) -> Dict:


    return {

        "components":

            rank_setup_components_v12(
                df
            ),


        "setup":

            select_best_setup_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_confluence_rank_v12(df) -> Dict:

    return confluence_ranking_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-14
# Multi Timeframe Intelligence Layer
# Institutional Entry Precision Engine
# Sniper Entry + Candle Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# CANDLE CONFIRMATION ENGINE
# ==========================

def candle_confirmation_v12(df) -> Dict:


    if len(df) < 3:

        return {

            "confirmed":

                False

        }



    open_price = float(
        df["open"].iloc[-1]
    )


    close_price = float(
        df["close"].iloc[-1]
    )


    high = float(
        df["high"].iloc[-1]
    )


    low = float(
        df["low"].iloc[-1]
    )



    body = abs(
        close_price - open_price
    )


    upper_wick = (
        high
        -
        max(
            open_price,
            close_price
        )
    )


    lower_wick = (
        min(
            open_price,
            close_price
        )
        -
        low
    )



    signal = "NONE"



    if (

        close_price > open_price

        and

        lower_wick > body

    ):

        signal = "BUY_REJECTION"



    elif (

        close_price < open_price

        and

        upper_wick > body

    ):

        signal = "SELL_REJECTION"



    elif detect_displacement(df):

        signal = "IMPULSE"



    return {

        "signal":

            signal,


        "confirmed":

            signal != "NONE"

    }



# ==========================
# SNIPER ENTRY SCORE
# ==========================

def sniper_entry_score_v12(df) -> int:


    score = 0



    if candle_confirmation_v12(df)["confirmed"]:

        score += 30



    if poi_location_check_v12(df):

        score += 25



    if mtf_liquidity_sweep_v12(df):

        score += 20



    if detect_mss(df):

        score += 25



    return min(score,100)



# ==========================
# SNIPER ENTRY FILTER
# ==========================

def sniper_entry_filter_v12(df) -> bool:


    direction = optimized_direction_v12(
        df
    )


    score = sniper_entry_score_v12(
        df
    )


    if direction == "RANGE":

        return False



    if score < 80:

        return False



    return True



# ==========================
# PRECISION ENTRY ENGINE
# ==========================

def precision_entry_engine_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    return {

        "direction":

            direction,


        "candle":

            candle_confirmation_v12(
                df
            ),


        "score":

            sniper_entry_score_v12(
                df
            ),


        "approved":

            sniper_entry_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_precision_entry_v12(df) -> Dict:

    return precision_entry_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-15
# Multi Timeframe Intelligence Layer
# Institutional Final Execution Router
# Signal Merge + Final Decision Layer
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL ENGINE INPUT FUSION
# ==========================

def final_engine_fusion_v12(df) -> Dict:


    modules = {


        "structure":

            htf_structure_quality_v12(df),


        "liquidity":

            liquidity_reversal_score_v12(df),


        "entry":

            sniper_entry_score_v12(df),


        "confluence":

            setup_priority_score_v12(df),


        "protection":

            signal_quality_filter_v12(df)
            ["quality"],


        "management":

            trade_management_score_v12(df)

    }



    total = 0


    for value in modules.values():

        total += value



    confidence = int(
        total /
        len(modules)
    )



    return {

        "modules":

            modules,


        "confidence":

            confidence

    }



# ==========================
# FINAL DIRECTION ROUTER
# ==========================

def final_direction_router_v12(df) -> str:


    direction = optimized_direction_v12(
        df
    )


    trigger = execution_trigger_v12(
        df
    )


    precision = precision_entry_engine_v12(
        df
    )



    votes = []



    if direction != "RANGE":

        votes.append(
            direction
        )



    if trigger["direction"] != "RANGE":

        votes.append(
            trigger["direction"]
        )



    if precision["direction"] != "RANGE":

        votes.append(
            precision["direction"]
        )



    buy = votes.count(
        "BUY"
    )


    sell = votes.count(
        "SELL"
    )



    if buy > sell:

        return "BUY"



    if sell > buy:

        return "SELL"



    return "RANGE"



# ==========================
# FINAL TRADE ROUTER
# ==========================

def final_execution_router_v12(df) -> Dict:


    fusion = final_engine_fusion_v12(
        df
    )


    direction = final_direction_router_v12(
        df
    )


    protection = institutional_protection_engine_v12(
        df
    )



    approved = False



    if (

        fusion["confidence"] >= 85

        and

        direction != "RANGE"

        and

        protection["approved"]

    ):

        approved = True



    return {

        "signal":

            direction
            if approved
            else
            "NO_TRADE",


        "approved":

            approved,


        "confidence":

            fusion["confidence"],


        "direction":

            direction,


        "modules":

            fusion["modules"]

    }



# ==========================
# STRUCTURE ENGINE V12 D FINAL
# ==========================

def structure_engine_v12_d_series_final(df) -> Dict:

    return final_execution_router_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_final_structure_signal_v12(df) -> Dict:

    return structure_engine_v12_d_series_final(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-16
# Multi Timeframe Intelligence Layer
# Institutional Signal Memory Engine
# Historical Pattern + Performance Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# SIGNAL MEMORY STORAGE
# ==========================

V12_SIGNAL_MEMORY = []



# ==========================
# STORE SIGNAL SNAPSHOT
# ==========================

def store_signal_memory_v12(
        signal: Dict
) -> None:


    if not signal:

        return



    snapshot = {

        "signal":

            signal.get(
                "signal",
                "NONE"
            ),


        "direction":

            signal.get(
                "direction",
                "NONE"
            ),


        "confidence":

            signal.get(
                "confidence",
                0
            )

    }



    V12_SIGNAL_MEMORY.append(
        snapshot
    )



    # Keep latest 100 records

    if len(
        V12_SIGNAL_MEMORY
    ) > 100:

        del V12_SIGNAL_MEMORY[0]



# ==========================
# MEMORY ANALYSIS
# ==========================

def analyze_signal_memory_v12() -> Dict:


    if not V12_SIGNAL_MEMORY:

        return {

            "total":

                0

        }



    buy = 0

    sell = 0

    avg_confidence = 0



    for item in V12_SIGNAL_MEMORY:


        if item["direction"] == "BUY":

            buy += 1



        elif item["direction"] == "SELL":

            sell += 1



        avg_confidence += item["confidence"]



    total = len(
        V12_SIGNAL_MEMORY
    )



    return {

        "total":

            total,


        "buy":

            buy,


        "sell":

            sell,


        "average_confidence":

            int(
                avg_confidence / total
            )

    }



# ==========================
# MEMORY CONFIDENCE BOOST
# ==========================

def memory_confidence_boost_v12() -> int:


    analysis = analyze_signal_memory_v12()



    if analysis["total"] < 10:

        return 0



    if analysis["average_confidence"] >= 85:

        return 10



    return 0



# ==========================
# FINAL MEMORY FILTER
# ==========================

def signal_memory_filter_v12(
        signal: Dict
) -> Dict:


    boost = memory_confidence_boost_v12()



    confidence = (

        signal.get(
            "confidence",
            0
        )

        +

        boost

    )



    return {

        "signal":

            signal.get(
                "signal"
            ),


        "confidence":

            min(
                confidence,
                100
            ),


        "memory_boost":

            boost

    }



# ==========================
# MEMORY ENGINE OUTPUT
# ==========================

def signal_memory_engine_v12(
        signal: Dict
) -> Dict:


    store_signal_memory_v12(
        signal
    )


    return signal_memory_filter_v12(
        signal
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_signal_memory_v12(
        signal: Dict
) -> Dict:

    return signal_memory_engine_v12(
        signal
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-17
# Multi Timeframe Intelligence Layer
# Institutional Adaptive Scoring Engine
# Dynamic Weight Adjustment
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# DYNAMIC MODULE WEIGHTS
# ==========================

def dynamic_weights_v12(df) -> Dict:


    state = market_state_engine_v12(
        df
    )


    phase = state["phase"]



    weights = {


        "structure":

            25,


        "liquidity":

            20,


        "entry":

            20,


        "confluence":

            15,


        "risk":

            10,


        "protection":

            10

    }



    if phase == "EXPANSION":


        weights["structure"] = 30

        weights["entry"] = 25



    elif phase == "MANIPULATION":


        weights["liquidity"] = 35

        weights["protection"] = 20



    elif phase == "ACCUMULATION":


        weights["risk"] = 25

        weights["protection"] = 25



    return weights



# ==========================
# ADAPTIVE CONFIDENCE ENGINE
# ==========================

def adaptive_confidence_v12(df) -> int:


    modules = {


        "structure":

            htf_structure_quality_v12(df),


        "liquidity":

            liquidity_reversal_score_v12(df),


        "entry":

            sniper_entry_score_v12(df),


        "confluence":

            setup_priority_score_v12(df),


        "risk":

            trade_management_score_v12(df),


        "protection":

            signal_quality_filter_v12(df)
            ["quality"]

    }



    weights = dynamic_weights_v12(
        df
    )


    score = 0



    for key,value in modules.items():


        score += (

            value
            *
            weights[key]
            /
            100

        )



    return min(
        int(score),
        100
    )



# ==========================
# ADAPTIVE SIGNAL FILTER
# ==========================

def adaptive_signal_filter_v12(df) -> Dict:


    confidence = adaptive_confidence_v12(
        df
    )


    direction = final_direction_router_v12(
        df
    )


    approved = False



    if (

        confidence >= 85

        and

        direction != "RANGE"

    ):

        approved = True



    return {

        "signal":

            direction
            if approved
            else
            "NO_TRADE",


        "confidence":

            confidence,


        "approved":

            approved

    }



# ==========================
# ADAPTIVE ENGINE
# ==========================

def adaptive_intelligence_engine_v12(df) -> Dict:


    return {

        "signal":

            adaptive_signal_filter_v12(
                df
            ),


        "weights":

            dynamic_weights_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_adaptive_signal_v12(df) -> Dict:

    return adaptive_intelligence_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-18
# Multi Timeframe Intelligence Layer
# Institutional Market Delivery Engine
# Accumulation -> Manipulation -> Expansion Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# DELIVERY PHASE ENGINE
# ==========================

def market_delivery_phase_v12(df) -> Dict:


    phase = market_phase_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )


    liquidity = mtf_liquidity_sweep_v12(
        df
    )


    displacement = detect_displacement(
        df
    )



    delivery = "WAIT"



    if phase == "ACCUMULATION":

        delivery = "BUILD_UP"



    elif phase == "MANIPULATION":

        delivery = "LIQUIDITY_GRAB"



    elif (

        phase == "EXPANSION"

        and

        displacement

    ):

        delivery = "DELIVERY"



    elif phase == "DISTRIBUTION":

        delivery = "EXIT"



    return {

        "phase":

            phase,


        "delivery":

            delivery,


        "direction":

            direction,


        "liquidity":

            liquidity is not None

    }



# ==========================
# DELIVERY STRENGTH SCORE
# ==========================

def delivery_strength_v12(df) -> int:


    state = market_delivery_phase_v12(
        df
    )


    score = 0



    if state["delivery"] == "DELIVERY":

        score += 40



    if state["liquidity"]:

        score += 25



    if detect_displacement(df):

        score += 20



    if internal_structure_break(df):

        score += 15



    return min(score,100)



# ==========================
# DELIVERY DIRECTION FILTER
# ==========================

def delivery_direction_filter_v12(df) -> str:


    state = market_delivery_phase_v12(
        df
    )


    if state["delivery"] != "DELIVERY":

        return "RANGE"



    return state["direction"]



# ==========================
# MARKET DELIVERY ENGINE
# ==========================

def institutional_delivery_engine_v12(df) -> Dict:


    return {

        "state":

            market_delivery_phase_v12(
                df
            ),


        "strength":

            delivery_strength_v12(
                df
            ),


        "direction":

            delivery_direction_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_delivery_v12(df) -> Dict:

    return institutional_delivery_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-19
# Multi Timeframe Intelligence Layer
# Institutional Final Validation Engine
# Last Gate Before Signal Generation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL VALIDATION CHECKLIST
# ==========================

def final_validation_check_v12(df) -> Dict:


    checks = {


        "market_structure":

            htf_structure_quality_v12(df) >= 70,


        "liquidity":

            liquidity_reversal_score_v12(df) >= 70,


        "entry":

            sniper_entry_score_v12(df) >= 70,


        "confluence":

            setup_priority_score_v12(df) >= 70,


        "market_state":

            market_phase_filter_v12(df),


        "protection":

            institutional_protection_engine_v12(df)
            ["approved"],


        "delivery":

            delivery_strength_v12(df) >= 70

    }



    passed = 0



    for value in checks.values():

        if value:

            passed += 1



    return {

        "checks":

            checks,


        "passed":

            passed,


        "total":

            len(checks)

    }



# ==========================
# VALIDATION SCORE
# ==========================

def final_validation_score_v12(df) -> int:


    result = final_validation_check_v12(
        df
    )


    return int(

        (
            result["passed"]

            /

            result["total"]

        )

        *

        100

    )



# ==========================
# FINAL SIGNAL GATE
# ==========================

def final_signal_gate_v12(df) -> Dict:


    score = final_validation_score_v12(
        df
    )


    direction = final_direction_router_v12(
        df
    )


    approved = False



    if (

        score >= 85

        and

        direction != "RANGE"

    ):

        approved = True



    return {

        "approved":

            approved,


        "signal":

            direction
            if approved
            else
            "NO_TRADE",


        "validation_score":

            score

    }



# ==========================
# VALIDATION ENGINE
# ==========================

def institutional_validation_engine_v12(df) -> Dict:


    return {

        "gate":

            final_signal_gate_v12(
                df
            ),


        "checklist":

            final_validation_check_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_final_validation_v12(df) -> Dict:

    return institutional_validation_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2D-20
# Multi Timeframe Intelligence Layer
# Institutional Final Output Formatter
# Signal Packaging + Main.py Interface
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# SIGNAL DATA FORMATTER
# ==========================

def format_signal_output_v12(df) -> Dict:


    final = final_signal_gate_v12(
        df
    )


    direction = final.get(
        "signal",
        "NO_TRADE"
    )


    confidence = final.get(
        "validation_score",
        0
    )



    trade = institutional_trade_management_v12(
        df
    )



    return {

        "signal":

            direction,


        "direction":

            direction,


        "confidence":

            confidence,


        "approved":

            final["approved"],


        "entry":

            trade["targets"].get(
                "entry"
            )
            if trade["targets"]
            else None,


        "sl":

            trade["targets"].get(
                "sl"
            )
            if trade["targets"]
            else None,


        "tp1":

            trade["targets"].get(
                "tp1"
            )
            if trade["targets"]
            else None,


        "tp2":

            trade["targets"].get(
                "tp2"
            )
            if trade["targets"]
            else None,


        "tp3":

            trade["targets"].get(
                "tp3"
            )
            if trade["targets"]
            else None

    }



# ==========================
# SIGNAL REASON ENGINE
# ==========================

def signal_reason_builder_v12(df) -> list:


    reasons = []



    if htf_structure_quality_v12(df) >= 70:

        reasons.append(
            "HTF_STRUCTURE"
        )



    if liquidity_reversal_score_v12(df) >= 70:

        reasons.append(
            "LIQUIDITY"
        )



    if optimized_order_block(df):

        reasons.append(
            "ORDER_BLOCK"
        )



    if optimized_fvg_detection(df):

        reasons.append(
            "FVG"
        )



    if detect_displacement(df):

        reasons.append(
            "DISPLACEMENT"
        )



    if detect_mss(df):

        reasons.append(
            "MSS"
        )



    return reasons



# ==========================
# COMPLETE SIGNAL ENGINE
# ==========================

def complete_signal_engine_v12(df) -> Dict:


    output = format_signal_output_v12(
        df
    )


    output["reasons"] = signal_reason_builder_v12(
        df
    )


    return output



# ==========================
# STRUCTURE ENGINE V12 FINAL ROUTER
# ==========================

def structure_engine_v12_final(df) -> Dict:

    return complete_signal_engine_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_v12_structure_signal(df) -> Dict:

    return structure_engine_v12_final(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-1
# Execution Intelligence Layer
# Institutional Entry Timing Engine
# Candle Timing + Market Momentum Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ENTRY TIMING ANALYSIS
# ==========================

def entry_timing_analysis_v12(df) -> Dict:


    momentum = detect_displacement(
        df
    )


    candle = candle_confirmation_v12(
        df
    )


    structure = detect_mss(
        df
    )


    timing = "WAIT"


    score = 0



    if structure:

        score += 30



    if momentum:

        score += 30



    if candle["confirmed"]:

        score += 20



    if optimized_liquidity_sweep(df):

        score += 20



    if score >= 80:

        timing = "EXECUTE"



    return {

        "timing":

            timing,


        "score":

            score,


        "momentum":

            momentum,


        "candle":

            candle["signal"]

    }



# ==========================
# ENTRY DELAY FILTER
# ==========================

def entry_delay_filter_v12(df) -> bool:


    timing = entry_timing_analysis_v12(
        df
    )


    if timing["timing"] == "EXECUTE":

        return True



    return False



# ==========================
# EXECUTION WINDOW ENGINE
# ==========================

def execution_window_v12(df) -> Dict:


    timing = entry_timing_analysis_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )



    return {

        "direction":

            direction,


        "window":

            timing["timing"],


        "confidence":

            timing["score"],


        "allowed":

            entry_delay_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_window_v12(df) -> Dict:

    return execution_window_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-2
# Execution Intelligence Layer
# Institutional Entry Precision Filter
# Retracement + Confirmation + Timing Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# RETRACEMENT VALIDATION
# ==========================

def retracement_validation_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    score = 0


    if direction == "RANGE":

        return {

            "valid":

                False,

            "score":

                0

        }



    if poi_location_check_v12(df):

        score += 35



    if optimized_ote_validation(
        df,
        direction
    ):

        score += 35



    if mtf_liquidity_sweep_v12(df):

        score += 30



    return {

        "valid":

            score >= 70,


        "score":

            score,


        "direction":

            direction

    }



# ==========================
# ENTRY PRECISION SCORE
# ==========================

def precision_filter_score_v12(df) -> int:


    retracement = retracement_validation_v12(
        df
    )


    timing = entry_timing_analysis_v12(
        df
    )


    score = 0



    score += retracement["score"] * 0.6


    score += timing["score"] * 0.4



    return int(
        min(score,100)
    )



# ==========================
# PRECISION ENTRY FILTER
# ==========================

def precision_entry_filter_v12(df) -> bool:


    score = precision_filter_score_v12(
        df
    )


    if score >= 85:

        return True



    return False



# ==========================
# EXECUTION PRECISION ENGINE
# ==========================

def execution_precision_engine_v12(df) -> Dict:


    return {

        "direction":

            optimized_direction_v12(
                df
            ),


        "retracement":

            retracement_validation_v12(
                df
            ),


        "score":

            precision_filter_score_v12(
                df
            ),


        "approved":

            precision_entry_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_precision_v12(df) -> Dict:

    return execution_precision_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-3
# Execution Intelligence Layer
# Institutional Entry Trigger Synchronizer
# MSS + Liquidity + POI + Momentum Alignment
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# TRIGGER COMPONENT ANALYSIS
# ==========================

def trigger_component_analysis_v12(df) -> Dict:


    components = {


        "MSS":

            bool(
                detect_mss(df)
            ),


        "BOS":

            bool(
                internal_structure_break(df)
            ),


        "LIQUIDITY_SWEEP":

            bool(
                mtf_liquidity_sweep_v12(df)
            ),


        "POI":

            bool(
                institutional_poi_v12(df)
            ),


        "DISPLACEMENT":

            bool(
                detect_displacement(df)
            ),


        "CANDLE":

            bool(
                candle_confirmation_v12(df)
                ["confirmed"]
            )

    }



    return components



# ==========================
# TRIGGER ALIGNMENT SCORE
# ==========================

def trigger_alignment_score_v12(df) -> int:


    components = trigger_component_analysis_v12(
        df
    )


    score = 0



    for value in components.values():

        if value:

            score += 16



    return min(
        score,
        100
    )



# ==========================
# DIRECTION CONFIRMATION
# ==========================

def trigger_direction_confirmation_v12(df) -> str:


    direction = optimized_direction_v12(
        df
    )


    trigger = execution_trigger_v12(
        df
    )


    if (

        direction
        ==
        trigger["direction"]

    ):

        return direction



    return "RANGE"



# ==========================
# FINAL TRIGGER ENGINE
# ==========================

def institutional_trigger_sync_v12(df) -> Dict:


    score = trigger_alignment_score_v12(
        df
    )


    direction = trigger_direction_confirmation_v12(
        df
    )



    return {

        "direction":

            direction,


        "score":

            score,


        "components":

            trigger_component_analysis_v12(
                df
            ),


        "approved":

            (

                score >= 85

                and

                direction != "RANGE"

            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trigger_sync_v12(df) -> Dict:

    return institutional_trigger_sync_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-4
# Execution Intelligence Layer
# Institutional Entry Zone Precision Engine
# POI Reaction + Order Block + FVG Validation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, Optional


# ==========================
# ENTRY ZONE DETECTOR
# ==========================

def entry_zone_detector_v12(df) -> Optional[Dict]:


    ob = optimized_order_block(
        df
    )


    fvg = optimized_fvg_detection(
        df
    )



    zone = None



    if ob:


        zone = {

            "type":

                "ORDER_BLOCK",


            "direction":

                ob["direction"],


            "high":

                ob["high"],


            "low":

                ob["low"]

        }



    elif fvg:


        zone = {

            "type":

                "FVG",


            "direction":

                fvg["direction"],


            "high":

                fvg["high"],


            "low":

                fvg["low"]

        }



    return zone



# ==========================
# ZONE REACTION CHECK
# ==========================

def zone_reaction_check_v12(df) -> bool:


    zone = entry_zone_detector_v12(
        df
    )


    if zone is None:

        return False



    price = float(
        df["close"].iloc[-1]
    )



    return (

        zone["low"]

        <=

        price

        <=

        zone["high"]

    )



# ==========================
# ENTRY ZONE QUALITY
# ==========================

def entry_zone_quality_v12(df) -> int:


    score = 0


    zone = entry_zone_detector_v12(
        df
    )



    if zone:

        score += 30



    if zone_reaction_check_v12(
        df
    ):

        score += 30



    if mtf_liquidity_sweep_v12(df):

        score += 20



    if detect_displacement(df):

        score += 20



    return min(
        score,
        100
    )



# ==========================
# PRECISION ZONE ENGINE
# ==========================

def precision_zone_engine_v12(df) -> Dict:


    return {

        "zone":

            entry_zone_detector_v12(
                df
            ),


        "score":

            entry_zone_quality_v12(
                df
            ),


        "valid":

            entry_zone_quality_v12(
                df
            ) >= 80

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_precision_zone_v12(df) -> Dict:

    return precision_zone_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-5
# Execution Intelligence Layer
# Institutional Entry Confirmation Engine
# Volume + Momentum + Structure Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# VOLUME CONFIRMATION
# ==========================

def volume_confirmation_v12(df) -> bool:


    if len(df) < 20:

        return False



    current_volume = float(
        df["volume"].iloc[-1]
    )


    average_volume = float(
        df["volume"]
        .tail(20)
        .mean()
    )



    if average_volume == 0:

        return False



    return (

        current_volume
        >
        average_volume * 1.2

    )



# ==========================
# MOMENTUM CONFIRMATION
# ==========================

def momentum_confirmation_v12(df) -> int:


    score = 0



    if detect_displacement(df):

        score += 40



    if volume_confirmation_v12(df):

        score += 30



    if internal_structure_break(df):

        score += 30



    return min(
        score,
        100
    )



# ==========================
# ENTRY CONFIRMATION STACK
# ==========================

def entry_confirmation_stack_v12(df) -> Dict:


    structure = bool(
        detect_mss(df)
    )


    momentum = momentum_confirmation_v12(
        df
    )


    liquidity = bool(
        mtf_liquidity_sweep_v12(df)
    )



    score = 0



    if structure:

        score += 35



    if momentum >= 70:

        score += 35



    if liquidity:

        score += 30



    return {

        "structure":

            structure,


        "momentum":

            momentum,


        "liquidity":

            liquidity,


        "score":

            score

    }



# ==========================
# FINAL CONFIRMATION FILTER
# ==========================

def final_entry_confirmation_v12(df) -> Dict:


    result = entry_confirmation_stack_v12(
        df
    )


    return {

        "confirmed":

            result["score"] >= 85,


        "score":

            result["score"],


        "details":

            result

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_entry_confirmation_v12(df) -> Dict:

    return final_entry_confirmation_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-6
# Execution Intelligence Layer
# Institutional Entry Risk Filter Engine
# Volatility + Spread + Market Condition Control
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# VOLATILITY CONTROL
# ==========================

def volatility_control_v12(df) -> Dict:


    atr = structure_atr(
        df
    )


    if atr <= 0:

        return {

            "state":

                "UNKNOWN",

            "score":

                0

        }



    recent_range = structure_true_range(
        df
    )


    ratio = recent_range / atr



    if ratio > 2:

        return {

            "state":

                "HIGH",

            "score":

                30

        }



    if ratio < 0.5:

        return {

            "state":

                "LOW",

            "score":

                20

        }



    return {

        "state":

            "NORMAL",

        "score":

            40

    }



# ==========================
# CANDLE RISK CHECK
# ==========================

def candle_risk_check_v12(df) -> int:


    if len(df) < 3:

        return 0



    high = float(
        df["high"].iloc[-1]
    )


    low = float(
        df["low"].iloc[-1]
    )


    close = float(
        df["close"].iloc[-1]
    )


    candle_size = high - low



    if candle_size == 0:

        return 0



    body_ratio = abs(
        close -
        float(df["open"].iloc[-1])
    ) / candle_size



    if body_ratio > 0.8:

        return 30



    if body_ratio < 0.3:

        return 10



    return 20



# ==========================
# MARKET CONDITION FILTER
# ==========================

def market_condition_filter_v12(df) -> Dict:


    volatility = volatility_control_v12(
        df
    )


    candle = candle_risk_check_v12(
        df
    )


    score = (

        volatility["score"]

        +

        candle

    )



    return {

        "condition_score":

            min(score,100),


        "volatility":

            volatility["state"],


        "safe":

            score >= 50

    }



# ==========================
# RISK APPROVAL ENGINE
# ==========================

def entry_risk_filter_v12(df) -> Dict:


    condition = market_condition_filter_v12(
        df
    )


    execution = final_entry_confirmation_v12(
        df
    )



    approved = (

        condition["safe"]

        and

        execution["confirmed"]

    )



    return {

        "approved":

            approved,


        "market":

            condition,


        "confirmation":

            execution

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_entry_risk_filter_v12(df) -> Dict:

    return entry_risk_filter_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-7
# Execution Intelligence Layer
# Institutional Position Sizing Engine
# Risk % + ATR Based Calculation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# RISK CAPITAL ENGINE
# ==========================

def risk_capital_v12(
        balance: float,
        risk_percent: float
) -> float:


    if balance <= 0:

        return 0



    return (

        balance
        *
        risk_percent
        /
        100

    )



# ==========================
# STOP DISTANCE ENGINE
# ==========================

def stop_distance_v12(df) -> float:


    atr = structure_atr(
        df
    )


    if atr <= 0:

        return 0



    return atr * 1.5



# ==========================
# POSITION SIZE CALCULATOR
# ==========================

def position_size_v12(
        balance: float,
        risk_percent: float,
        df
) -> float:


    risk_amount = risk_capital_v12(
        balance,
        risk_percent
    )


    stop_distance = stop_distance_v12(
        df
    )



    if stop_distance == 0:

        return 0



    size = (

        risk_amount
        /
        stop_distance

    )



    return round(
        size,
        4
    )



# ==========================
# LEVERAGE SAFETY FILTER
# ==========================

def leverage_safety_v12(
        leverage: int
) -> Dict:


    if leverage <= 5:

        return {

            "risk":

                "LOW",

            "allowed":

                True

        }



    if leverage <= 20:

        return {

            "risk":

                "MEDIUM",

            "allowed":

                True

        }



    return {

        "risk":

            "HIGH",

        "allowed":

            False

    }



# ==========================
# POSITION RISK ENGINE
# ==========================

def position_risk_engine_v12(
        balance: float,
        risk_percent: float,
        leverage: int,
        df
) -> Dict:


    size = position_size_v12(
        balance,
        risk_percent,
        df
    )


    leverage_check = leverage_safety_v12(
        leverage
    )



    return {

        "position_size":

            size,


        "risk_amount":

            risk_capital_v12(
                balance,
                risk_percent
            ),


        "leverage":

            leverage,


        "leverage_status":

            leverage_check

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_position_risk_v12(
        balance,
        risk_percent,
        leverage,
        df
) -> Dict:

    return position_risk_engine_v12(
        balance,
        risk_percent,
        leverage,
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-8
# Execution Intelligence Layer
# Institutional Trade Protection Engine
# Break Even + Trailing + Partial Exit Logic
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# BREAK EVEN CALCULATOR
# ==========================

def break_even_level_v12(
        entry: float,
        direction: str
) -> float:


    if direction == "BUY":

        return entry



    if direction == "SELL":

        return entry



    return 0



# ==========================
# PARTIAL PROFIT ENGINE
# ==========================

def partial_profit_levels_v12(
        entry: float,
        sl: float,
        direction: str
) -> Dict:


    risk = abs(
        entry - sl
    )


    if risk == 0:

        return {}



    if direction == "BUY":


        return {

            "tp1":

                entry + risk,


            "tp2":

                entry + (risk * 2),


            "secure":

                entry + (risk * 0.5)

        }



    if direction == "SELL":


        return {

            "tp1":

                entry - risk,


            "tp2":

                entry - (risk * 2),


            "secure":

                entry - (risk * 0.5)

        }



    return {}



# ==========================
# TRAILING STOP ENGINE
# ==========================

def trailing_stop_v12(
        price: float,
        entry: float,
        sl: float,
        direction: str
) -> float:


    risk = abs(
        entry - sl
    )


    if risk == 0:

        return sl



    if direction == "BUY":


        if price >= entry + risk:


            return entry



    if direction == "SELL":


        if price <= entry - risk:


            return entry



    return sl



# ==========================
# TRADE PROTECTION SCORE
# ==========================

def trade_protection_score_v12(df) -> int:


    score = 0



    if trade_management_score_v12(df):

        score += 40



    if liquidity_target_validation(df):

        score += 30



    if final_entry_confirmation_v12(df)["confirmed"]:

        score += 30



    return min(
        score,
        100
    )



# ==========================
# PROTECTION ENGINE
# ==========================

def institutional_trade_protection_v12(
        df,
        entry: float,
        sl: float,
        direction: str,
        price: float
) -> Dict:


    return {

        "break_even":

            break_even_level_v12(
                entry,
                direction
            ),


        "partial":

            partial_profit_levels_v12(
                entry,
                sl,
                direction
            ),


        "trailing_sl":

            trailing_stop_v12(
                price,
                entry,
                sl,
                direction
            ),


        "score":

            trade_protection_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_protection_v12(
        df,
        entry,
        sl,
        direction,
        price
) -> Dict:

    return institutional_trade_protection_v12(
        df,
        entry,
        sl,
        direction,
        price
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-9
# Execution Intelligence Layer
# Institutional Signal Alert Engine
# Telegram/Main.py Ready Output
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# SIGNAL MESSAGE BUILDER
# ==========================

def signal_message_builder_v12(
        signal: Dict
) -> str:


    direction = signal.get(
        "signal",
        "NO_TRADE"
    )


    confidence = signal.get(
        "confidence",
        0
    )


    entry = signal.get(
        "entry",
        None
    )


    sl = signal.get(
        "sl",
        None
    )


    tp1 = signal.get(
        "tp1",
        None
    )


    tp2 = signal.get(
        "tp2",
        None
    )


    tp3 = signal.get(
        "tp3",
        None
    )


    reasons = signal.get(
        "reasons",
        []
    )



    if direction == "NO_TRADE":


        return (

            "⚪ NO TRADE\n"

            f"Confidence: {confidence}%"

        )



    return (

        "🚀 ICT V12 SIGNAL\n\n"

        f"Direction: {direction}\n"

        f"Entry: {entry}\n"

        f"SL: {sl}\n"

        f"TP1: {tp1}\n"

        f"TP2: {tp2}\n"

        f"TP3: {tp3}\n\n"

        f"Confidence: {confidence}%\n"

        f"Reasons: {', '.join(reasons)}"

    )



# ==========================
# ALERT PRIORITY ENGINE
# ==========================

def alert_priority_v12(
        confidence: int
) -> str:


    if confidence >= 90:

        return "HIGH"



    if confidence >= 80:

        return "MEDIUM"



    return "LOW"



# ==========================
# COMPLETE ALERT ENGINE
# ==========================

def signal_alert_engine_v12(
        df
) -> Dict:


    signal = complete_signal_engine_v12(
        df
    )


    priority = alert_priority_v12(
        signal.get(
            "confidence",
            0
        )
    )



    return {

        "signal":

            signal,


        "message":

            signal_message_builder_v12(
                signal
            ),


        "priority":

            priority

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_signal_alert_v12(df) -> Dict:

    return signal_alert_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-10
# Execution Intelligence Layer
# Institutional Final Execution Manager
# Complete Entry -> Management Pipeline
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EXECUTION PIPELINE BUILDER
# ==========================

def execution_pipeline_v12(df) -> Dict:


    signal = complete_signal_engine_v12(
        df
    )


    validation = institutional_validation_engine_v12(
        df
    )


    risk = get_entry_risk_filter_v12(
        df
    )


    protection = get_signal_protection_v12(
        df
    )


    management = institutional_trade_management_v12(
        df
    )



    return {


        "signal":

            signal,


        "validation":

            validation,


        "risk":

            risk,


        "protection":

            protection,


        "management":

            management

    }



# ==========================
# FINAL EXECUTION DECISION
# ==========================

def final_execution_manager_v12(df) -> Dict:


    pipeline = execution_pipeline_v12(
        df
    )


    signal = pipeline["signal"]


    validation = pipeline["validation"]["gate"]


    risk = pipeline["risk"]["approved"]


    protection = pipeline["protection"]["approved"]



    approved = (

        validation["approved"]

        and

        risk

        and

        protection

    )



    return {

        "approved":

            approved,


        "signal":

            signal["signal"]
            if approved
            else
            "NO_TRADE",


        "confidence":

            signal["confidence"],


        "entry":

            signal.get(
                "entry"
            ),


        "sl":

            signal.get(
                "sl"
            ),


        "tp1":

            signal.get(
                "tp1"
            ),


        "tp2":

            signal.get(
                "tp2"
            ),


        "tp3":

            signal.get(
                "tp3"
            ),


        "pipeline":

            pipeline

    }



# ==========================
# AUTO EXECUTION ROUTER
# ==========================

def institutional_execution_manager_v12(df) -> Dict:

    return final_execution_manager_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_manager_v12(df) -> Dict:

    return institutional_execution_manager_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-11
# Execution Intelligence Layer
# Institutional Trade Lifecycle Engine
# Signal Tracking + State Management
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# TRADE STATE MEMORY
# ==========================

V12_TRADE_STATE = {

    "status":

        "IDLE",

    "direction":

        None,

    "entry":

        None,

    "sl":

        None,

    "tp1":

        None,

    "tp2":

        None,

    "tp3":

        None

}



# ==========================
# OPEN TRADE REGISTER
# ==========================

def register_trade_v12(
        trade: Dict
) -> Dict:


    global V12_TRADE_STATE


    V12_TRADE_STATE = {


        "status":

            "OPEN",


        "direction":

            trade.get(
                "signal"
            ),


        "entry":

            trade.get(
                "entry"
            ),


        "sl":

            trade.get(
                "sl"
            ),


        "tp1":

            trade.get(
                "tp1"
            ),


        "tp2":

            trade.get(
                "tp2"
            ),


        "tp3":

            trade.get(
                "tp3"
            )

    }


    return V12_TRADE_STATE



# ==========================
# PRICE MONITOR ENGINE
# ==========================

def monitor_trade_v12(
        price: float
) -> Dict:


    trade = V12_TRADE_STATE


    if trade["status"] != "OPEN":

        return trade



    direction = trade["direction"]



    result = "RUNNING"



    if direction == "BUY":


        if price <= trade["sl"]:

            result = "SL_HIT"



        elif price >= trade["tp3"]:

            result = "TP3_HIT"



        elif price >= trade["tp1"]:

            result = "TP1_HIT"



    elif direction == "SELL":


        if price >= trade["sl"]:

            result = "SL_HIT"



        elif price <= trade["tp3"]:

            result = "TP3_HIT"



        elif price <= trade["tp1"]:

            result = "TP1_HIT"



    return {

        "state":

            result,


        "trade":

            trade

    }



# ==========================
# TRADE CLOSE ENGINE
# ==========================

def close_trade_v12(
        reason: str
) -> Dict:


    global V12_TRADE_STATE


    V12_TRADE_STATE = {

        "status":

            "CLOSED",


        "reason":

            reason

    }


    return V12_TRADE_STATE



# ==========================
# LIFECYCLE ENGINE
# ==========================

def trade_lifecycle_engine_v12(
        trade: Dict,
        price: float
) -> Dict:


    if V12_TRADE_STATE["status"] == "IDLE":

        register_trade_v12(
            trade
        )



    monitor = monitor_trade_v12(
        price
    )



    if monitor["state"] in [

        "SL_HIT",

        "TP3_HIT"

    ]:

        close_trade_v12(
            monitor["state"]
        )



    return {

        "monitor":

            monitor,


        "current":

            V12_TRADE_STATE

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_lifecycle_v12(
        trade,
        price
) -> Dict:

    return trade_lifecycle_engine_v12(
        trade,
        price
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-12
# Execution Intelligence Layer
# Institutional Multi Position Manager
# Scaling + Multiple Signal Control
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# ACTIVE POSITION STORAGE
# ==========================

V12_ACTIVE_POSITIONS = []



# ==========================
# ADD POSITION
# ==========================

def add_position_v12(
        trade: Dict
) -> Dict:


    position = {


        "id":

            len(V12_ACTIVE_POSITIONS)+1,


        "direction":

            trade.get(
                "signal"
            ),


        "entry":

            trade.get(
                "entry"
            ),


        "sl":

            trade.get(
                "sl"
            ),


        "tp1":

            trade.get(
                "tp1"
            ),


        "tp2":

            trade.get(
                "tp2"
            ),


        "tp3":

            trade.get(
                "tp3"
            ),


        "status":

            "ACTIVE"

    }



    V12_ACTIVE_POSITIONS.append(
        position
    )


    return position



# ==========================
# POSITION MONITOR
# ==========================

def monitor_positions_v12(
        price: float
) -> List:


    results = []



    for position in V12_ACTIVE_POSITIONS:


        state = "RUNNING"



        if position["direction"] == "BUY":


            if price <= position["sl"]:

                state = "SL_HIT"



            elif price >= position["tp3"]:

                state = "TP3_HIT"



            elif price >= position["tp1"]:

                state = "TP1_HIT"



        elif position["direction"] == "SELL":


            if price >= position["sl"]:

                state = "SL_HIT"



            elif price <= position["tp3"]:

                state = "TP3_HIT"



            elif price <= position["tp1"]:

                state = "TP1_HIT"



        results.append({

            "id":

                position["id"],


            "state":

                state

        })



    return results



# ==========================
# POSITION LIMIT FILTER
# ==========================

def position_limit_filter_v12(
        max_positions: int = 3
) -> bool:


    active = len(
        V12_ACTIVE_POSITIONS
    )


    return active < max_positions



# ==========================
# SCALE IN ENGINE
# ==========================

def scale_in_validation_v12(
        df
) -> bool:


    confidence = adaptive_confidence_v12(
        df
    )


    return (

        confidence >= 90

        and

        position_limit_filter_v12()

    )



# ==========================
# POSITION MANAGER ENGINE
# ==========================

def institutional_position_manager_v12(
        trade: Dict,
        price: float
) -> Dict:



    monitoring = monitor_positions_v12(
        price
    )



    return {


        "positions":

            V12_ACTIVE_POSITIONS,


        "monitor":

            monitoring,


        "can_add":

            position_limit_filter_v12()

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_position_manager_v12(
        trade,
        price
) -> Dict:

    return institutional_position_manager_v12(
        trade,
        price
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-13
# Execution Intelligence Layer
# Institutional Market Protection Controller
# Emergency Exit + Capital Preservation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EMERGENCY MARKET CHECK
# ==========================

def emergency_market_check_v12(df) -> Dict:


    volatility = volatility_control_v12(
        df
    )


    phase = market_phase_v12(
        df
    )


    displacement = detect_displacement(
        df
    )



    danger = False

    reasons = []



    if volatility["state"] == "HIGH":

        danger = True

        reasons.append(
            "HIGH_VOLATILITY"
        )



    if phase == "MANIPULATION":

        danger = True

        reasons.append(
            "MARKET_MANIPULATION"
        )



    if not displacement:

        reasons.append(
            "NO_MOMENTUM"
        )



    return {


        "danger":

            danger,


        "reasons":

            reasons

    }



# ==========================
# CAPITAL PROTECTION SCORE
# ==========================

def capital_protection_score_v12(df) -> int:


    result = emergency_market_check_v12(
        df
    )


    score = 100



    if result["danger"]:

        score -= 40



    if len(
        result["reasons"]
    ) > 2:

        score -= 20



    return max(
        score,
        0
    )



# ==========================
# POSITION EXIT DECISION
# ==========================

def emergency_exit_filter_v12(df) -> Dict:


    check = emergency_market_check_v12(
        df
    )


    score = capital_protection_score_v12(
        df
    )


    exit_trade = False



    if score < 50:

        exit_trade = True



    return {


        "exit":

            exit_trade,


        "protection_score":

            score,


        "reason":

            check["reasons"]

    }



# ==========================
# PROTECTION CONTROLLER
# ==========================

def institutional_protection_controller_v12(df) -> Dict:


    return {


        "market":

            emergency_market_check_v12(
                df
            ),


        "capital":

            capital_protection_score_v12(
                df
            ),


        "exit":

            emergency_exit_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_protection_controller_v12(df) -> Dict:

    return institutional_protection_controller_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-14
# Execution Intelligence Layer
# Institutional Trade Analytics Engine
# Performance + Signal Quality Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# PERFORMANCE MEMORY
# ==========================

V12_PERFORMANCE_MEMORY = []



# ==========================
# STORE TRADE RESULT
# ==========================

def store_trade_result_v12(
        result: Dict
) -> None:


    if not result:

        return



    V12_PERFORMANCE_MEMORY.append({

        "signal":

            result.get(
                "signal",
                "NONE"
            ),


        "result":

            result.get(
                "result",
                "UNKNOWN"
            ),


        "profit":

            result.get(
                "profit",
                0
            ),


        "confidence":

            result.get(
                "confidence",
                0
            )

    })



    if len(
        V12_PERFORMANCE_MEMORY
    ) > 200:

        del V12_PERFORMANCE_MEMORY[0]



# ==========================
# WIN RATE CALCULATOR
# ==========================

def performance_stats_v12() -> Dict:


    if not V12_PERFORMANCE_MEMORY:

        return {

            "trades":

                0

        }



    wins = 0

    losses = 0

    total_profit = 0



    for trade in V12_PERFORMANCE_MEMORY:


        if trade["result"] == "WIN":

            wins += 1



        elif trade["result"] == "LOSS":

            losses += 1



        total_profit += trade["profit"]



    total = len(
        V12_PERFORMANCE_MEMORY
    )



    return {


        "trades":

            total,


        "wins":

            wins,


        "losses":

            losses,


        "win_rate":

            round(
                (wins / total) * 100,
                2
            ),


        "profit":

            total_profit

    }



# ==========================
# CONFIDENCE ADJUSTMENT
# ==========================

def performance_confidence_adjustment_v12() -> int:


    stats = performance_stats_v12()



    if stats.get(
        "trades",
        0
    ) < 20:

        return 0



    if stats["win_rate"] >= 70:

        return 10



    if stats["win_rate"] < 40:

        return -10



    return 0



# ==========================
# ANALYTICS ENGINE
# ==========================

def institutional_trade_analytics_v12() -> Dict:


    return {


        "statistics":

            performance_stats_v12(),


        "confidence_adjustment":

            performance_confidence_adjustment_v12()

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_analytics_v12() -> Dict:

    return institutional_trade_analytics_v12()
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-15
# Execution Intelligence Layer
# Institutional Market Scanner Router
# Multi Symbol + Multi Timeframe Execution Control
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# SYMBOL SCAN ENGINE
# ==========================

def scan_symbol_execution_v12(
        symbol: str,
        df
) -> Dict:


    signal = institutional_execution_manager_v12(
        df
    )


    confidence = signal.get(
        "confidence",
        0
    )


    return {

        "symbol":

            symbol,


        "signal":

            signal.get(
                "signal",
                "NO_TRADE"
            ),


        "confidence":

            confidence,


        "approved":

            signal.get(
                "approved",
                False
            ),


        "entry":

            signal.get(
                "entry"
            ),


        "sl":

            signal.get(
                "sl"
            ),


        "tp1":

            signal.get(
                "tp1"
            )

    }



# ==========================
# MULTI SYMBOL RANKER
# ==========================

def rank_symbols_v12(
        results: List[Dict]
) -> List[Dict]:


    return sorted(

        results,

        key=lambda x:

            x.get(
                "confidence",
                0
            ),

        reverse=True

    )



# ==========================
# BEST OPPORTUNITY SELECTOR
# ==========================

def best_execution_setup_v12(
        results: List[Dict]
) -> Dict:


    ranked = rank_symbols_v12(
        results
    )


    if not ranked:

        return {

            "signal":

                "NO_TRADE"

        }



    best = ranked[0]



    if best["confidence"] < 85:

        return {

            "signal":

                "NO_TRADE",


            "reason":

                "LOW_CONFIDENCE"

        }



    return best



# ==========================
# MARKET SCANNER ENGINE
# ==========================

def institutional_market_scanner_v12(
        symbols: List[str],
        data_map: Dict
) -> Dict:


    results = []



    for symbol in symbols:


        if symbol in data_map:


            result = scan_symbol_execution_v12(

                symbol,

                data_map[symbol]

            )


            results.append(
                result
            )



    return {


        "all_signals":

            results,


        "best_setup":

            best_execution_setup_v12(
                results
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_scanner_v12(
        symbols,
        data_map
) -> Dict:

    return institutional_market_scanner_v12(
        symbols,
        data_map
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-16
# Execution Intelligence Layer
# Institutional Trade Correlation Engine
# BTC Dominance + Market Pair Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET CORRELATION CHECK
# ==========================

def market_correlation_check_v12(
        primary_df,
        confirm_df
) -> Dict:


    if len(primary_df) < 20 or len(confirm_df) < 20:

        return {

            "correlated":

                False,

            "score":

                0

        }



    primary_change = (

        primary_df["close"].iloc[-1]

        -

        primary_df["close"].iloc[-20]

    )


    confirm_change = (

        confirm_df["close"].iloc[-1]

        -

        confirm_df["close"].iloc[-20]

    )



    score = 0



    if (

        primary_change > 0

        and

        confirm_change > 0

    ):

        score += 50



    elif (

        primary_change < 0

        and

        confirm_change < 0

    ):

        score += 50



    if abs(primary_change) > 0:

        score += 50



    return {

        "correlated":

            score >= 70,


        "score":

            score

    }



# ==========================
# BTC CONFIRMATION ENGINE
# ==========================

def btc_confirmation_v12(
        asset_df,
        btc_df
) -> Dict:


    correlation = market_correlation_check_v12(
        asset_df,
        btc_df
    )


    direction = optimized_direction_v12(
        asset_df
    )


    btc_direction = optimized_direction_v12(
        btc_df
    )



    alignment = (

        direction == btc_direction

        and

        direction != "RANGE"

    )



    score = correlation["score"]



    if alignment:

        score += 20



    return {

        "direction":

            direction,


        "btc_direction":

            btc_direction,


        "score":

            min(
                score,
                100
            ),


        "confirmed":

            score >= 80

    }



# ==========================
# CORRELATION FILTER
# ==========================

def correlation_filter_v12(
        asset_df,
        btc_df
) -> bool:


    result = btc_confirmation_v12(
        asset_df,
        btc_df
    )


    return result["confirmed"]



# ==========================
# FINAL CORRELATION ENGINE
# ==========================

def institutional_correlation_engine_v12(
        asset_df,
        btc_df
) -> Dict:


    return btc_confirmation_v12(
        asset_df,
        btc_df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_correlation_confirmation_v12(
        asset_df,
        btc_df
) -> Dict:

    return institutional_correlation_engine_v12(
        asset_df,
        btc_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-17
# Execution Intelligence Layer
# Institutional Liquidity Target Engine
# External Liquidity + Internal Target Mapping
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# LIQUIDITY TARGET DETECTOR
# ==========================

def liquidity_target_detector_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "targets":

                [],

            "score":

                0

        }



    highs = []

    lows = []



    for i in range(
        2,
        len(df)-2
    ):


        high = df["high"].iloc[i]


        low = df["low"].iloc[i]



        if (

            high >
            df["high"].iloc[i-1]

            and

            high >
            df["high"].iloc[i+1]

        ):

            highs.append(
                float(high)
            )



        if (

            low <
            df["low"].iloc[i-1]

            and

            low <
            df["low"].iloc[i+1]

        ):

            lows.append(
                float(low)
            )



    return {

        "high_liquidity":

            highs[-3:],


        "low_liquidity":

            lows[-3:],


        "score":

            80
            if highs or lows
            else
            0

    }



# ==========================
# TARGET DIRECTION ENGINE
# ==========================

def liquidity_target_direction_v12(df) -> Dict:


    direction = optimized_direction_v12(
        df
    )


    liquidity = liquidity_target_detector_v12(
        df
    )



    target = None



    if direction == "BUY" and liquidity["high_liquidity"]:

        target = liquidity["high_liquidity"][-1]



    elif direction == "SELL" and liquidity["low_liquidity"]:

        target = liquidity["low_liquidity"][-1]



    return {

        "direction":

            direction,


        "target":

            target,


        "score":

            liquidity["score"]

    }



# ==========================
# LIQUIDITY TARGET VALIDATOR
# ==========================

def liquidity_target_validation_v12(df) -> bool:


    result = liquidity_target_direction_v12(
        df
    )


    return (

        result["target"] is not None

        and

        result["score"] >= 70

    )



# ==========================
# FINAL TARGET ENGINE
# ==========================

def institutional_liquidity_target_engine_v12(df) -> Dict:


    return liquidity_target_direction_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_target_v12(df) -> Dict:

    return institutional_liquidity_target_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-18
# Execution Intelligence Layer
# Institutional Premium Discount Engine
# OTE + Dealing Range Entry Filter
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# DEALING RANGE CALCULATOR
# ==========================

def dealing_range_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "high":

                None,

            "low":

                None

        }



    high = float(
        df["high"].tail(20).max()
    )


    low = float(
        df["low"].tail(20).min()
    )


    equilibrium = (

        high + low

    ) / 2



    return {

        "high":

            high,


        "low":

            low,


        "equilibrium":

            equilibrium

    }



# ==========================
# PREMIUM DISCOUNT CHECK
# ==========================

def premium_discount_zone_v12(df) -> Dict:


    range_data = dealing_range_v12(
        df
    )


    if not range_data["high"]:

        return {

            "zone":

                "UNKNOWN"

        }



    price = float(
        df["close"].iloc[-1]
    )


    equilibrium = range_data["equilibrium"]



    if price < equilibrium:

        zone = "DISCOUNT"



    elif price > equilibrium:

        zone = "PREMIUM"



    else:

        zone = "EQUILIBRIUM"



    return {

        "zone":

            zone,


        "price":

            price,


        "equilibrium":

            equilibrium

    }



# ==========================
# OTE VALIDATION ENGINE
# ==========================

def optimized_ote_validation(
        df,
        direction: str
) -> bool:


    zone = premium_discount_zone_v12(
        df
    )


    if direction == "BUY":


        return zone["zone"] == "DISCOUNT"



    if direction == "SELL":


        return zone["zone"] == "PREMIUM"



    return False



# ==========================
# ENTRY LOCATION SCORE
# ==========================

def premium_discount_score_v12(df) -> int:


    direction = optimized_direction_v12(
        df
    )


    score = 0



    if optimized_ote_validation(
        df,
        direction
    ):

        score += 50



    if poi_location_check_v12(df):

        score += 25



    if liquidity_target_validation(df):

        score += 25



    return min(
        score,
        100
    )



# ==========================
# PREMIUM DISCOUNT ENGINE
# ==========================

def institutional_premium_discount_engine_v12(df) -> Dict:


    return {

        "zone":

            premium_discount_zone_v12(
                df
            ),


        "score":

            premium_discount_score_v12(
                df
            ),


        "valid":

            premium_discount_score_v12(
                df
            ) >= 80

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_premium_discount_v12(df) -> Dict:

    return institutional_premium_discount_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-19
# Execution Intelligence Layer
# Institutional Session Intelligence Engine
# London + New York + Asia Liquidity Timing
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict
from datetime import datetime, timezone


# ==========================
# SESSION DETECTOR
# ==========================

def trading_session_v12() -> str:


    hour = datetime.now(
        timezone.utc
    ).hour



    # Asia Session

    if 0 <= hour < 8:

        return "ASIA"



    # London Session

    if 8 <= hour < 13:

        return "LONDON"



    # New York Session

    if 13 <= hour < 21:

        return "NEW_YORK"



    return "OFF_SESSION"



# ==========================
# SESSION QUALITY SCORE
# ==========================

def session_quality_v12() -> int:


    session = trading_session_v12()



    if session == "LONDON":

        return 90



    if session == "NEW_YORK":

        return 95



    if session == "ASIA":

        return 60



    return 30



# ==========================
# SESSION LIQUIDITY FILTER
# ==========================

def session_liquidity_filter_v12() -> Dict:


    session = trading_session_v12()


    score = session_quality_v12()



    return {

        "session":

            session,


        "score":

            score,


        "allowed":

            score >= 70

    }



# ==========================
# SESSION EXECUTION ENGINE
# ==========================

def institutional_session_engine_v12() -> Dict:


    return session_liquidity_filter_v12()



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_session_intelligence_v12() -> Dict:

    return institutional_session_engine_v12()
    # ==========================
# STRUCTURE ENGINE V12
# PART 2E-20
# Execution Intelligence Layer
# Institutional Final Entry Synchronizer
# Complete Confluence Gate Before Execution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EXECUTION COMPONENT FUSION
# ==========================

def execution_component_fusion_v12(df) -> Dict:


    components = {


        "trigger":

            get_trigger_sync_v12(df)
            ["score"],


        "zone":

            get_precision_zone_v12(df)
            ["score"],


        "confirmation":

            get_entry_confirmation_v12(df)
            ["score"],


        "risk":

            get_entry_risk_filter_v12(df)
            ["approved"],


        "correlation":

            True,


        "session":

            get_session_intelligence_v12()
            ["allowed"]

    }



    score = 0



    score += components["trigger"] * 0.25


    score += components["zone"] * 0.20


    score += components["confirmation"] * 0.25


    score += 15 if components["risk"] else 0


    score += 10 if components["correlation"] else 0


    score += 5 if components["session"] else 0



    return {

        "components":

            components,


        "execution_score":

            int(
                min(
                    score,
                    100
                )
            )

    }



# ==========================
# FINAL ENTRY APPROVAL
# ==========================

def final_entry_synchronizer_v12(df) -> Dict:


    fusion = execution_component_fusion_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )



    approved = (

        fusion["execution_score"] >= 85

        and

        direction != "RANGE"

    )



    return {


        "signal":

            direction
            if approved
            else
            "NO_TRADE",


        "approved":

            approved,


        "score":

            fusion["execution_score"],


        "details":

            fusion["components"]

    }



# ==========================
# EXECUTION INTELLIGENCE CORE
# ==========================

def execution_intelligence_core_v12(df) -> Dict:


    return final_entry_synchronizer_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_intelligence_v12(df) -> Dict:

    return execution_intelligence_core_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-1
# Final Intelligence Layer
# Institutional Signal Fusion Engine
# Execution + Risk + Market Intelligence Merge
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL MODULE FUSION
# ==========================

def final_module_fusion_v12(df) -> Dict:


    modules = {


        "structure":

            get_final_validation_v12(df)
            ["gate"]
            ["validation_score"],


        "execution":

            get_execution_intelligence_v12(df)
            ["score"],


        "market_state":

            delivery_strength_v12(df),


        "liquidity":

            get_liquidity_target_v12(df)
            ["score"],


        "premium_discount":

            get_premium_discount_v12(df)
            ["score"],


        "session":

            get_session_intelligence_v12()
            ["score"]

    }



    total = 0



    for value in modules.values():

        total += value



    confidence = int(

        total /

        len(modules)

    )



    return {

        "modules":

            modules,


        "confidence":

            min(
                confidence,
                100
            )

    }



# ==========================
# FINAL DIRECTION ENGINE
# ==========================

def final_direction_engine_v12(df) -> str:


    execution = get_execution_intelligence_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )



    if (

        execution["signal"]

        !=

        "NO_TRADE"

    ):

        return direction



    return "RANGE"



# ==========================
# FINAL APPROVAL GATE
# ==========================

def final_approval_gate_v12(df) -> Dict:


    fusion = final_module_fusion_v12(
        df
    )


    direction = final_direction_engine_v12(
        df
    )



    approved = (

        fusion["confidence"] >= 85

        and

        direction != "RANGE"

    )



    return {

        "signal":

            direction
            if approved
            else
            "NO_TRADE",


        "confidence":

            fusion["confidence"],


        "approved":

            approved,


        "modules":

            fusion["modules"]

    }



# ==========================
# FINAL INTELLIGENCE ENGINE
# ==========================

def final_intelligence_engine_v12(df) -> Dict:


    return final_approval_gate_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_final_intelligence_v12(df) -> Dict:

    return final_intelligence_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-2
# Final Intelligence Layer
# Institutional Signal Ranking Engine
# A+ Setup Selection + Opportunity Scoring
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# SIGNAL QUALITY RANKER
# ==========================

def signal_quality_rank_v12(df) -> Dict:


    intelligence = get_final_intelligence_v12(
        df
    )


    modules = intelligence.get(
        "modules",
        {}
    )



    score = intelligence.get(
        "confidence",
        0
    )


    grade = "C"



    if score >= 95:

        grade = "A+"



    elif score >= 85:

        grade = "A"



    elif score >= 75:

        grade = "B"



    return {


        "score":

            score,


        "grade":

            grade,


        "modules":

            modules

    }



# ==========================
# SETUP RANKING MEMORY
# ==========================

V12_SETUP_MEMORY = []



# ==========================
# STORE SETUP QUALITY
# ==========================

def store_setup_rank_v12(
        setup: Dict
) -> None:


    V12_SETUP_MEMORY.append({

        "signal":

            setup.get(
                "signal",
                "NONE"
            ),


        "score":

            setup.get(
                "score",
                0
            ),


        "grade":

            setup.get(
                "grade",
                "C"
            )

    })



    if len(
        V12_SETUP_MEMORY
    ) > 100:

        del V12_SETUP_MEMORY[0]



# ==========================
# BEST SETUP SELECTOR
# ==========================

def best_setup_selector_v12(
        df
) -> Dict:


    rank = signal_quality_rank_v12(
        df
    )


    store_setup_rank_v12(
        rank
    )


    return {

        "quality":

            rank,


        "trade_ready":

            rank["grade"]
            in
            [
                "A+",
                "A"
            ]

    }



# ==========================
# FINAL OPPORTUNITY ENGINE
# ==========================

def institutional_opportunity_engine_v12(df) -> Dict:


    setup = best_setup_selector_v12(
        df
    )


    final = get_final_intelligence_v12(
        df
    )



    return {

        "signal":

            final["signal"],


        "confidence":

            final["confidence"],


        "grade":

            setup["quality"]["grade"],


        "approved":

            setup["trade_ready"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_opportunity_rank_v12(df) -> Dict:

    return institutional_opportunity_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-3
# Final Intelligence Layer
# Institutional Market Regime Engine
# Trend + Range + Volatility Adaptation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# REGIME DETECTION
# ==========================

def market_regime_v12(df) -> Dict:


    trend_score = trend_strength_v12(
        df
    )


    volatility = volatility_control_v12(
        df
    )


    phase = market_phase_v12(
        df
    )



    regime = "NEUTRAL"



    if (

        trend_score >= 80

        and

        volatility["state"] == "NORMAL"

    ):

        regime = "TREND"



    elif (

        phase == "ACCUMULATION"

    ):

        regime = "RANGE"



    elif (

        volatility["state"] == "HIGH"

    ):

        regime = "VOLATILE"



    return {

        "regime":

            regime,


        "trend_score":

            trend_score,


        "volatility":

            volatility["state"],


        "phase":

            phase

    }



# ==========================
# REGIME WEIGHT ADJUSTER
# ==========================

def regime_weight_adjustment_v12(df) -> Dict:


    regime = market_regime_v12(
        df
    )["regime"]



    weights = {


        "structure":

            25,


        "liquidity":

            25,


        "execution":

            25,


        "risk":

            25

    }



    if regime == "TREND":


        weights["structure"] = 35

        weights["execution"] = 30



    elif regime == "RANGE":


        weights["liquidity"] = 40

        weights["risk"] = 35



    elif regime == "VOLATILE":


        weights["risk"] = 50

        weights["execution"] = 20



    return weights



# ==========================
# REGIME FILTER
# ==========================

def regime_trade_filter_v12(df) -> bool:


    regime = market_regime_v12(
        df
    )


    if regime["regime"] == "VOLATILE":

        return False



    return True



# ==========================
# MARKET REGIME ENGINE
# ==========================

def institutional_market_regime_engine_v12(df) -> Dict:


    return {

        "state":

            market_regime_v12(
                df
            ),


        "weights":

            regime_weight_adjustment_v12(
                df
            ),


        "allowed":

            regime_trade_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_regime_v12(df) -> Dict:

    return institutional_market_regime_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-4
# Final Intelligence Layer
# Institutional Smart Money Bias Engine
# HTF Bias + Liquidity + Delivery Direction
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# HTF BIAS CALCULATOR
# ==========================

def htf_bias_v12(df) -> str:


    if len(df) < 50:

        return "NEUTRAL"



    current = float(
        df["close"].iloc[-1]
    )


    previous = float(
        df["close"].iloc[-50]
    )



    if current > previous:

        return "BULLISH"



    elif current < previous:

        return "BEARISH"



    return "NEUTRAL"



# ==========================
# SMART MONEY DIRECTION
# ==========================

def smart_money_direction_v12(df) -> Dict:


    bias = htf_bias_v12(
        df
    )


    structure = optimized_direction_v12(
        df
    )


    liquidity = mtf_liquidity_sweep_v12(
        df
    )



    score = 0



    if bias == "BULLISH" and structure == "BUY":

        score += 40



    elif bias == "BEARISH" and structure == "SELL":

        score += 40



    if liquidity:

        score += 30



    if detect_displacement(df):

        score += 30



    direction = "NEUTRAL"



    if score >= 70:


        if bias == "BULLISH":

            direction = "BUY"



        elif bias == "BEARISH":

            direction = "SELL"



    return {

        "bias":

            bias,


        "direction":

            direction,


        "score":

            min(
                score,
                100
            )

    }



# ==========================
# BIAS FILTER
# ==========================

def smart_money_bias_filter_v12(df) -> bool:


    result = smart_money_direction_v12(
        df
    )


    return (

        result["score"] >= 80

        and

        result["direction"] != "NEUTRAL"

    )



# ==========================
# SMART MONEY ENGINE
# ==========================

def institutional_smart_money_engine_v12(df) -> Dict:


    return {

        "bias":

            smart_money_direction_v12(
                df
            ),


        "approved":

            smart_money_bias_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_smart_money_bias_v12(df) -> Dict:

    return institutional_smart_money_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-5
# Final Intelligence Layer
# Institutional Liquidity Map Engine
# Equal High/Low + Sweep + Target Mapping
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# EQUAL HIGH LOW DETECTOR
# ==========================

def equal_level_detector_v12(df) -> Dict:


    if len(df) < 30:

        return {

            "equal_highs":

                [],


            "equal_lows":

                []

        }



    equal_highs = []

    equal_lows = []



    tolerance = (
        df["close"].iloc[-1]
        *
        0.001
    )



    for i in range(
        5,
        len(df)-5
    ):


        high = float(
            df["high"].iloc[i]
        )


        low = float(
            df["low"].iloc[i]
        )



        if (

            abs(
                high -
                float(df["high"].iloc[i-5])
            )

            <=

            tolerance

        ):

            equal_highs.append(
                high
            )



        if (

            abs(
                low -
                float(df["low"].iloc[i-5])
            )

            <=

            tolerance

        ):

            equal_lows.append(
                low
            )



    return {

        "equal_highs":

            equal_highs[-5:],


        "equal_lows":

            equal_lows[-5:]

    }



# ==========================
# LIQUIDITY SWEEP MAP
# ==========================

def liquidity_sweep_map_v12(df) -> Dict:


    levels = equal_level_detector_v12(
        df
    )


    price = float(
        df["close"].iloc[-1]
    )



    swept = []



    for high in levels["equal_highs"]:


        if price > high:

            swept.append(
                "HIGH_LIQUIDITY_TAKEN"
            )



    for low in levels["equal_lows"]:


        if price < low:

            swept.append(
                "LOW_LIQUIDITY_TAKEN"
            )



    return {

        "levels":

            levels,


        "sweeps":

            swept,


        "score":

            80
            if swept
            else
            0

    }



# ==========================
# LIQUIDITY TARGET MAP
# ==========================

def liquidity_map_engine_v12(df) -> Dict:


    sweep = liquidity_sweep_map_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )



    return {

        "direction":

            direction,


        "sweep":

            sweep,


        "ready":

            sweep["score"] >= 70

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_map_v12(df) -> Dict:

    return liquidity_map_engine_v12(
        df
    )
    
# ==========================
# STRUCTURE ENGINE V12
# PART 2F-6
# Final Intelligence Layer
# Institutional Order Flow Engine
# Buyer/Seller Pressure + Smart Money Flow
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ORDER FLOW PRESSURE
# ==========================

def order_flow_pressure_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "buyers":

                0,

            "sellers":

                0

        }



    buyers = 0

    sellers = 0



    for i in range(
        len(df)-20,
        len(df)
    ):


        open_price = float(
            df["open"].iloc[i]
        )


        close_price = float(
            df["close"].iloc[i]
        )


        volume = float(
            df["volume"].iloc[i]
        )



        if close_price > open_price:

            buyers += volume



        elif close_price < open_price:

            sellers += volume



    total = buyers + sellers



    if total == 0:

        return {

            "buyers":

                0,

            "sellers":

                0,

            "pressure":

                "NEUTRAL"

        }



    buy_percent = (

        buyers / total

    ) * 100



    sell_percent = (

        sellers / total

    ) * 100



    pressure = "NEUTRAL"



    if buy_percent > 60:

        pressure = "BUY"



    elif sell_percent > 60:

        pressure = "SELL"



    return {

        "buyers":

            round(
                buy_percent,
                2
            ),


        "sellers":

            round(
                sell_percent,
                2
            ),


        "pressure":

            pressure

    }



# ==========================
# SMART MONEY FLOW SCORE
# ==========================

def smart_money_flow_score_v12(df) -> int:


    flow = order_flow_pressure_v12(
        df
    )


    score = 0



    if flow["pressure"] != "NEUTRAL":

        score += 50



    if volume_confirmation_v12(df):

        score += 25



    if detect_displacement(df):

        score += 25



    return min(
        score,
        100
    )



# ==========================
# FLOW DIRECTION ENGINE
# ==========================

def order_flow_direction_v12(df) -> Dict:


    flow = order_flow_pressure_v12(
        df
    )


    return {

        "direction":

            flow["pressure"],


        "score":

            smart_money_flow_score_v12(
                df
            )

    }



# ==========================
# INSTITUTIONAL FLOW ENGINE
# ==========================

def institutional_order_flow_engine_v12(df) -> Dict:


    return order_flow_direction_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_order_flow_v12(df) -> Dict:

    return institutional_order_flow_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-7
# Final Intelligence Layer
# Institutional Momentum Regime Engine
# Momentum Burst + Exhaustion Detection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MOMENTUM CALCULATOR
# ==========================

def momentum_regime_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "state":

                "UNKNOWN",

            "score":

                0

        }



    current_close = float(
        df["close"].iloc[-1]
    )


    previous_close = float(
        df["close"].iloc[-20]
    )



    move = abs(

        current_close
        -
        previous_close

    )



    avg_range = (

        df["high"]
        -
        df["low"]

    ).tail(20).mean()



    score = 0



    if move > avg_range * 5:

        score += 60



    elif move > avg_range * 2:

        score += 40



    if volume_confirmation_v12(df):

        score += 25



    if detect_displacement(df):

        score += 15



    state = "WEAK"



    if score >= 80:

        state = "STRONG"



    elif score >= 50:

        state = "ACTIVE"



    return {

        "state":

            state,


        "score":

            min(
                score,
                100
            )

    }



# ==========================
# MOMENTUM DIRECTION
# ==========================

def momentum_direction_v12(df) -> Dict:


    regime = momentum_regime_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )



    return {

        "direction":

            direction,


        "momentum":

            regime["state"],


        "score":

            regime["score"]

    }



# ==========================
# MOMENTUM FILTER
# ==========================

def momentum_filter_v12(df) -> bool:


    result = momentum_direction_v12(
        df
    )


    return (

        result["score"] >= 70

        and

        result["direction"] != "RANGE"

    )



# ==========================
# MOMENTUM ENGINE
# ==========================

def institutional_momentum_engine_v12(df) -> Dict:


    return {

        "momentum":

            momentum_direction_v12(
                df
            ),


        "approved":

            momentum_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_momentum_engine_v12(df) -> Dict:

    return institutional_momentum_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-8
# Final Intelligence Layer
# Institutional Volatility Intelligence Engine
# ATR Expansion + Compression Detection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# VOLATILITY STATE ENGINE
# ==========================

def volatility_state_v12(df) -> Dict:


    if len(df) < 30:

        return {

            "state":

                "UNKNOWN",

            "score":

                0

        }



    current_atr = structure_atr(
        df
    )



    previous_atr = (

        df["high"]
        -
        df["low"]

    ).tail(30).mean()



    if previous_atr == 0:

        return {

            "state":

                "UNKNOWN",

            "score":

                0

        }



    ratio = current_atr / previous_atr



    score = 0

    state = "NORMAL"



    if ratio > 1.5:


        state = "EXPANSION"

        score = 90



    elif ratio < 0.7:


        state = "COMPRESSION"

        score = 60



    else:


        state = "NORMAL"

        score = 75



    return {

        "state":

            state,


        "ratio":

            round(
                ratio,
                2
            ),


        "score":

            score

    }



# ==========================
# VOLATILITY ENTRY FILTER
# ==========================

def volatility_entry_filter_v12(df) -> bool:


    result = volatility_state_v12(
        df
    )


    return (

        result["state"]

        !=

        "UNKNOWN"

        and

        result["score"] >= 70

    )



# ==========================
# VOLATILITY ADAPTATION
# ==========================

def volatility_adaptation_v12(df) -> Dict:


    state = volatility_state_v12(
        df
    )


    mode = "NORMAL"



    if state["state"] == "EXPANSION":

        mode = "MOMENTUM_MODE"



    elif state["state"] == "COMPRESSION":

        mode = "BREAKOUT_WAIT"



    return {

        "volatility":

            state,


        "mode":

            mode,


        "allowed":

            volatility_entry_filter_v12(
                df
            )

    }



# ==========================
# VOLATILITY ENGINE
# ==========================

def institutional_volatility_engine_v12(df) -> Dict:


    return volatility_adaptation_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_volatility_intelligence_v12(df) -> Dict:

    return institutional_volatility_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-9
# Final Intelligence Layer
# Institutional Market Inefficiency Engine
# FVG + Imbalance + Price Delivery Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# FVG DETECTION ENGINE
# ==========================

def institutional_fvg_detector_v12(df) -> List[Dict]:


    fvgs = []


    if len(df) < 5:

        return fvgs



    for i in range(
        2,
        len(df)
    ):


        candle_1_high = float(
            df["high"].iloc[i-2]
        )


        candle_1_low = float(
            df["low"].iloc[i-2]
        )


        candle_3_high = float(
            df["high"].iloc[i]
        )


        candle_3_low = float(
            df["low"].iloc[i]
        )



        # Bullish imbalance

        if candle_3_low > candle_1_high:


            fvgs.append({

                "type":

                    "BULLISH_FVG",


                "high":

                    candle_3_low,


                "low":

                    candle_1_high

            })



        # Bearish imbalance

        elif candle_3_high < candle_1_low:


            fvgs.append({

                "type":

                    "BEARISH_FVG",


                "high":

                    candle_1_low,


                "low":

                    candle_3_high

            })



    return fvgs[-5:]



# ==========================
# FVG REACTION CHECK
# ==========================

def fvg_reaction_check_v12(df) -> Dict:


    fvgs = institutional_fvg_detector_v12(
        df
    )


    price = float(
        df["close"].iloc[-1]
    )


    reaction = False

    active = None



    for fvg in fvgs:


        if (

            fvg["low"]

            <=

            price

            <=

            fvg["high"]

        ):

            reaction = True

            active = fvg



    return {

        "active":

            reaction,


        "zone":

            active

    }



# ==========================
# IMBALANCE QUALITY SCORE
# ==========================

def imbalance_quality_score_v12(df) -> int:


    score = 0



    fvgs = institutional_fvg_detector_v12(
        df
    )


    reaction = fvg_reaction_check_v12(
        df
    )



    if fvgs:

        score += 40



    if reaction["active"]:

        score += 30



    if detect_displacement(df):

        score += 30



    return min(
        score,
        100
    )



# ==========================
# PRICE DELIVERY ENGINE
# ==========================

def institutional_imbalance_engine_v12(df) -> Dict:


    return {

        "fvg":

            institutional_fvg_detector_v12(
                df
            ),


        "reaction":

            fvg_reaction_check_v12(
                df
            ),


        "score":

            imbalance_quality_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_imbalance_engine_v12(df) -> Dict:

    return institutional_imbalance_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-10
# Final Intelligence Layer
# Institutional Volume Profile Intelligence
# Volume Distribution + Smart Money Activity
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# VOLUME PROFILE ENGINE
# ==========================

def volume_profile_v12(df) -> Dict:


    if len(df) < 50:

        return {

            "poc":

                None,

            "high_volume":

                [],

            "score":

                0

        }



    data = df.tail(50).copy()



    data["volume_price"] = (

        data["close"]

        *

        data["volume"]

    )



    poc_index = (

        data["volume_price"]

        .idxmax()

    )


    poc = float(
        data.loc[
            poc_index,
            "close"
        ]
    )



    high_volume_nodes = (

        data

        .sort_values(
            "volume",
            ascending=False
        )

        ["close"]

        .head(5)

        .tolist()

    )



    return {

        "poc":

            poc,


        "high_volume":

            high_volume_nodes,


        "score":

            80

    }



# ==========================
# PRICE VS POC ANALYSIS
# ==========================

def poc_position_v12(df) -> Dict:


    profile = volume_profile_v12(
        df
    )


    if profile["poc"] is None:

        return {

            "position":

                "UNKNOWN"

        }



    price = float(
        df["close"].iloc[-1]
    )


    if price > profile["poc"]:

        position = "ABOVE_POC"



    elif price < profile["poc"]:

        position = "BELOW_POC"



    else:

        position = "AT_POC"



    return {

        "position":

            position,


        "poc":

            profile["poc"]

    }



# ==========================
# VOLUME CONFIRMATION SCORE
# ==========================

def volume_profile_score_v12(df) -> int:


    profile = volume_profile_v12(
        df
    )


    score = profile["score"]



    if volume_confirmation_v12(df):

        score += 20



    if detect_displacement(df):

        score += 20



    return min(
        score,
        100
    )



# ==========================
# INSTITUTIONAL VOLUME ENGINE
# ==========================

def institutional_volume_engine_v12(df) -> Dict:


    return {

        "profile":

            volume_profile_v12(
                df
            ),


        "position":

            poc_position_v12(
                df
            ),


        "score":

            volume_profile_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_volume_intelligence_v12(df) -> Dict:

    return institutional_volume_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-11
# Final Intelligence Layer
# Institutional Market Structure Memory Engine
# BOS + MSS + Swing History Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# STRUCTURE MEMORY
# ==========================

V12_STRUCTURE_MEMORY = []



# ==========================
# SWING POINT DETECTOR
# ==========================

def swing_history_v12(df) -> Dict:


    highs = []

    lows = []



    if len(df) < 10:

        return {

            "highs":

                highs,

            "lows":

                lows

        }



    for i in range(
        2,
        len(df)-2
    ):


        high = float(
            df["high"].iloc[i]
        )


        low = float(
            df["low"].iloc[i]
        )



        if (

            high >

            float(df["high"].iloc[i-1])

            and

            high >

            float(df["high"].iloc[i+1])

        ):

            highs.append(high)



        if (

            low <

            float(df["low"].iloc[i-1])

            and

            low <

            float(df["low"].iloc[i+1])

        ):

            lows.append(low)



    return {

        "highs":

            highs[-10:],


        "lows":

            lows[-10:]

    }



# ==========================
# BOS MEMORY TRACKER
# ==========================

def structure_memory_tracker_v12(df) -> Dict:


    swings = swing_history_v12(
        df
    )


    current = float(
        df["close"].iloc[-1]
    )


    event = "NONE"



    if swings["highs"]:


        if current > max(
            swings["highs"]
        ):

            event = "BULLISH_BOS"



    if swings["lows"]:


        if current < min(
            swings["lows"]
        ):

            event = "BEARISH_BOS"



    V12_STRUCTURE_MEMORY.append(
        event
    )



    if len(
        V12_STRUCTURE_MEMORY
    ) > 50:

        del V12_STRUCTURE_MEMORY[0]



    return {

        "event":

            event,


        "history":

            V12_STRUCTURE_MEMORY[-10:]

    }



# ==========================
# STRUCTURE QUALITY SCORE
# ==========================

def structure_memory_score_v12(df) -> int:


    tracker = structure_memory_tracker_v12(
        df
    )


    score = 0



    if tracker["event"] != "NONE":

        score += 50



    if detect_mss(df):

        score += 25



    if internal_structure_break(df):

        score += 25



    return min(
        score,
        100
    )



# ==========================
# STRUCTURE MEMORY ENGINE
# ==========================

def institutional_structure_memory_v12(df) -> Dict:


    return {

        "structure":

            structure_memory_tracker_v12(
                df
            ),


        "score":

            structure_memory_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_structure_memory_v12(df) -> Dict:

    return institutional_structure_memory_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-12
# Final Intelligence Layer
# Institutional Smart Money Footprint Engine
# Order Block + Displacement + Institutional Activity
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# SMART MONEY FOOTPRINT MEMORY
# ==========================

V12_SMART_MONEY_MEMORY = []



# ==========================
# INSTITUTIONAL FOOTPRINT DETECTOR
# ==========================

def institutional_footprint_detector_v12(df) -> Dict:


    if len(df) < 10:

        return {

            "found":

                False,

            "type":

                None

        }



    last = df.iloc[-1]

    previous = df.iloc[-2]



    body = abs(

        float(last["close"])

        -

        float(last["open"])

    )



    previous_body = abs(

        float(previous["close"])

        -

        float(previous["open"])

    )



    footprint = False

    footprint_type = None



    if (

        body > previous_body * 2

        and

        float(last["volume"])

        >

        float(previous["volume"])

    ):



        footprint = True



        if last["close"] > last["open"]:

            footprint_type = "BUYER_ACCUMULATION"



        else:

            footprint_type = "SELLER_DISTRIBUTION"



    return {

        "found":

            footprint,


        "type":

            footprint_type

    }



# ==========================
# FOOTPRINT SCORE
# ==========================

def footprint_score_v12(df) -> int:


    footprint = institutional_footprint_detector_v12(
        df
    )


    score = 0



    if footprint["found"]:

        score += 50



    if detect_displacement(df):

        score += 25



    if volume_confirmation_v12(df):

        score += 25



    return min(
        score,
        100
    )



# ==========================
# SMART MONEY MEMORY UPDATE
# ==========================

def update_smart_money_memory_v12(df) -> Dict:


    footprint = institutional_footprint_detector_v12(
        df
    )


    if footprint["found"]:


        V12_SMART_MONEY_MEMORY.append(
            footprint
        )



    if len(
        V12_SMART_MONEY_MEMORY
    ) > 50:

        del V12_SMART_MONEY_MEMORY[0]



    return {

        "current":

            footprint,


        "history":

            V12_SMART_MONEY_MEMORY[-10:]

    }



# ==========================
# SMART MONEY ENGINE
# ==========================

def institutional_smart_money_footprint_v12(df) -> Dict:


    return {

        "footprint":

            update_smart_money_memory_v12(
                df
            ),


        "score":

            footprint_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_smart_money_footprint_v12(df) -> Dict:

    return institutional_smart_money_footprint_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-13
# Final Intelligence Layer
# Institutional Entry Probability Engine
# Bayesian Confluence + Confidence Calculation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# PROBABILITY COMPONENT ENGINE
# ==========================

def probability_components_v12(df) -> Dict:


    components = {


        "structure":

            get_structure_memory_v12(df)
            ["score"],


        "smart_money":

            get_smart_money_footprint_v12(df)
            ["score"],


        "liquidity":

            get_liquidity_map_v12(df)
            ["sweep"]
            ["score"],


        "momentum":

            get_momentum_engine_v12(df)
            ["momentum"]
            ["score"],


        "volume":

            get_volume_intelligence_v12(df)
            ["score"],


        "volatility":

            get_volatility_intelligence_v12(df)
            ["volatility"]
            ["score"]

    }



    return components



# ==========================
# PROBABILITY CALCULATOR
# ==========================

def entry_probability_v12(df) -> Dict:


    components = probability_components_v12(
        df
    )



    weights = {


        "structure":

            0.25,


        "smart_money":

            0.20,


        "liquidity":

            0.20,


        "momentum":

            0.15,


        "volume":

            0.10,


        "volatility":

            0.10

    }



    probability = 0



    for key, value in components.items():


        probability += (

            value

            *

            weights[key]

        )



    return {

        "probability":

            int(
                min(
                    probability,
                    100
                )
            ),


        "components":

            components

    }



# ==========================
# CONFIDENCE CLASSIFIER
# ==========================

def confidence_class_v12(
        probability: int
) -> str:


    if probability >= 95:

        return "A+"



    if probability >= 85:

        return "A"



    if probability >= 75:

        return "B"



    return "C"



# ==========================
# FINAL PROBABILITY ENGINE
# ==========================

def institutional_probability_engine_v12(df) -> Dict:


    result = entry_probability_v12(
        df
    )


    return {

        "confidence":

            result["probability"],


        "grade":

            confidence_class_v12(
                result["probability"]
            ),


        "components":

            result["components"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_entry_probability_v12(df) -> Dict:

    return institutional_probability_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-14
# Final Intelligence Layer
# Institutional Trade Decision Matrix
# Buy/Sell/No Trade Final Filtering
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# DIRECTION SCORE ENGINE
# ==========================

def direction_score_v12(df) -> Dict:


    smart_money = get_smart_money_bias_v12(
        df
    )


    order_flow = get_order_flow_v12(
        df
    )


    momentum = get_momentum_engine_v12(
        df
    )



    buy_score = 0

    sell_score = 0



    if smart_money["bias"]["direction"] == "BUY":

        buy_score += 40



    elif smart_money["bias"]["direction"] == "SELL":

        sell_score += 40



    if order_flow["direction"] == "BUY":

        buy_score += 30



    elif order_flow["direction"] == "SELL":

        sell_score += 30



    if momentum["momentum"]["direction"] == "BUY":

        buy_score += 30



    elif momentum["momentum"]["direction"] == "SELL":

        sell_score += 30



    return {

        "BUY":

            buy_score,


        "SELL":

            sell_score

    }



# ==========================
# FINAL DIRECTION DECISION
# ==========================

def final_direction_decision_v12(df) -> Dict:


    scores = direction_score_v12(
        df
    )


    direction = "NO_TRADE"

    confidence = max(
        scores.values()
    )



    if scores["BUY"] > scores["SELL"]:


        if scores["BUY"] >= 70:

            direction = "BUY"



    elif scores["SELL"] > scores["BUY"]:


        if scores["SELL"] >= 70:

            direction = "SELL"



    return {

        "direction":

            direction,


        "confidence":

            confidence,


        "scores":

            scores

    }



# ==========================
# DECISION MATRIX ENGINE
# ==========================

def institutional_decision_matrix_v12(df) -> Dict:


    decision = final_direction_decision_v12(
        df
    )


    probability = get_entry_probability_v12(
        df
    )


    approved = (

        decision["direction"]

        !=

        "NO_TRADE"

        and

        probability["confidence"]

        >= 85

    )



    return {

        "signal":

            decision["direction"]
            if approved
            else
            "NO_TRADE",


        "confidence":

            probability["confidence"],


        "direction_score":

            decision["scores"],


        "approved":

            approved

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_decision_matrix_v12(df) -> Dict:

    return institutional_decision_matrix_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-15
# Final Intelligence Layer
# Institutional Entry Model Generator
# Entry + SL + TP Automatic Calculation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ENTRY PRICE ENGINE
# ==========================

def institutional_entry_price_v12(
        df,
        direction: str
) -> float:


    zone = get_precision_zone_v12(
        df
    )


    price = float(
        df["close"].iloc[-1]
    )



    if zone["zone"]:


        high = zone["zone"]["high"]


        low = zone["zone"]["low"]



        if direction == "BUY":

            return round(
                low,
                4
            )



        elif direction == "SELL":

            return round(
                high,
                4
            )



    return round(
        price,
        4
    )



# ==========================
# STOP LOSS ENGINE
# ==========================

def institutional_sl_v12(
        df,
        entry: float,
        direction: str
) -> float:


    atr = structure_atr(
        df
    )


    if direction == "BUY":


        return round(

            entry - (atr * 1.5),

            4

        )



    elif direction == "SELL":


        return round(

            entry + (atr * 1.5),

            4

        )



    return entry



# ==========================
# TARGET ENGINE
# ==========================

def institutional_tp_v12(
        entry: float,
        sl: float,
        direction: str
) -> Dict:


    risk = abs(
        entry - sl
    )



    if direction == "BUY":


        return {

            "tp1":

                round(
                    entry + risk,
                    4
                ),


            "tp2":

                round(
                    entry + (risk*2),
                    4
                ),


            "tp3":

                round(
                    entry + (risk*3),
                    4
                )

        }



    if direction == "SELL":


        return {

            "tp1":

                round(
                    entry - risk,
                    4
                ),


            "tp2":

                round(
                    entry - (risk*2),
                    4
                ),


            "tp3":

                round(
                    entry - (risk*3),
                    4
                )

        }



    return {}



# ==========================
# ENTRY MODEL GENERATOR
# ==========================

def institutional_entry_model_v12(df) -> Dict:


    decision = get_decision_matrix_v12(
        df
    )


    direction = decision["signal"]



    if direction == "NO_TRADE":

        return {

            "signal":

                "NO_TRADE"

        }



    entry = institutional_entry_price_v12(
        df,
        direction
    )


    sl = institutional_sl_v12(
        df,
        entry,
        direction
    )


    targets = institutional_tp_v12(
        entry,
        sl,
        direction
    )



    return {

        "signal":

            direction,


        "entry":

            entry,


        "sl":

            sl,


        "tp1":

            targets["tp1"],


        "tp2":

            targets["tp2"],


        "tp3":

            targets["tp3"],


        "confidence":

            decision["confidence"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_entry_model_v12(df) -> Dict:

    return institutional_entry_model_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-16
# Final Intelligence Layer
# Institutional Signal Packaging Engine
# Complete Trade Object Generator
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# TRADE OBJECT BUILDER
# ==========================

def build_trade_object_v12(df) -> Dict:


    entry_model = get_entry_model_v12(
        df
    )


    if entry_model.get(
        "signal"
    ) == "NO_TRADE":


        return {

            "status":

                "NO_TRADE",

            "signal":

                "NO_TRADE"

        }



    protection = get_trade_protection_v12(
        df,
        entry_model["entry"],
        entry_model["sl"],
        entry_model["signal"],
        float(df["close"].iloc[-1])
    )



    probability = get_entry_probability_v12(
        df
    )



    return {


        "status":

            "READY",


        "signal":

            entry_model["signal"],


        "entry":

            entry_model["entry"],


        "sl":

            entry_model["sl"],


        "tp1":

            entry_model["tp1"],


        "tp2":

            entry_model["tp2"],


        "tp3":

            entry_model["tp3"],


        "confidence":

            probability["confidence"],


        "grade":

            probability["grade"],


        "protection":

            protection

    }



# ==========================
# SIGNAL VALIDATION
# ==========================

def validate_trade_object_v12(
        trade: Dict
) -> bool:


    required = [

        "signal",

        "entry",

        "sl",

        "tp1",

        "tp2",

        "tp3"

    ]



    for key in required:


        if key not in trade:

            return False



    return (

        trade["signal"]

        in

        [

            "BUY",

            "SELL"

        ]

    )



# ==========================
# FINAL SIGNAL ROUTER
# ==========================

def institutional_signal_router_v12(df) -> Dict:


    trade = build_trade_object_v12(
        df
    )


    valid = validate_trade_object_v12(
        trade
    )



    if not valid:


        return {

            "signal":

                "NO_TRADE",


            "approved":

                False

        }



    return {

        "signal":

            trade["signal"],


        "approved":

            True,


        "trade":

            trade

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_signal_router_v12(df) -> Dict:

    return institutional_signal_router_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-17
# Final Intelligence Layer
# Institutional Signal Confidence Booster
# Multi Engine Agreement + Quality Enhancement
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ENGINE AGREEMENT CHECK
# ==========================

def engine_agreement_v12(df) -> Dict:


    engines = {


        "decision":

            get_decision_matrix_v12(df)
            ["signal"],


        "smart_money":

            get_smart_money_bias_v12(df)
            ["bias"]
            ["direction"],


        "flow":

            get_order_flow_v12(df)
            ["direction"],


        "momentum":

            get_momentum_engine_v12(df)
            ["momentum"]
            ["direction"]

    }



    buy_votes = 0

    sell_votes = 0



    for value in engines.values():


        if value == "BUY":

            buy_votes += 1



        elif value == "SELL":

            sell_votes += 1



    agreement = max(
        buy_votes,
        sell_votes
    )



    return {

        "engines":

            engines,


        "agreement":

            agreement,


        "aligned":

            agreement >= 3

    }



# ==========================
# CONFIDENCE BOOST ENGINE
# ==========================

def confidence_boost_v12(df) -> Dict:


    base = get_entry_probability_v12(
        df
    )


    agreement = engine_agreement_v12(
        df
    )


    confidence = base["confidence"]



    if agreement["aligned"]:

        confidence += 10



    if agreement["agreement"] == 4:

        confidence += 5



    return {

        "base":

            base["confidence"],


        "boosted":

            min(
                confidence,
                100
            ),


        "agreement":

            agreement

    }



# ==========================
# QUALITY FILTER
# ==========================

def signal_quality_filter_v12(df) -> Dict:


    result = confidence_boost_v12(
        df
    )


    return {


        "confidence":

            result["boosted"],


        "approved":

            result["boosted"] >= 85,


        "agreement":

            result["agreement"]

    }



# ==========================
# FINAL CONFIDENCE ENGINE
# ==========================

def institutional_confidence_booster_v12(df) -> Dict:


    return signal_quality_filter_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_confidence_booster_v12(df) -> Dict:

    return institutional_confidence_booster_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-18
# Final Intelligence Layer
# Institutional Trade Execution Guard
# Final Safety Gate Before Signal Release
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# EXECUTION SAFETY CHECK
# ==========================

def execution_safety_check_v12(df) -> Dict:


    confidence = get_confidence_booster_v12(
        df
    )


    regime = get_market_regime_v12(
        df
    )


    volatility = get_volatility_intelligence_v12(
        df
    )


    protection = get_protection_controller_v12(
        df
    )



    reasons = []

    approved = True



    if confidence["confidence"] < 85:


        approved = False

        reasons.append(
            "LOW_CONFIDENCE"
        )



    if not regime["allowed"]:


        approved = False

        reasons.append(
            "BAD_MARKET_REGIME"
        )



    if not volatility["allowed"]:


        approved = False

        reasons.append(
            "VOLATILITY_BLOCK"
        )



    if protection["exit"]["exit"]:


        approved = False

        reasons.append(
            "RISK_PROTECTION"
        )



    return {

        "approved":

            approved,


        "confidence":

            confidence["confidence"],


        "reasons":

            reasons

    }



# ==========================
# FINAL SIGNAL RELEASE
# ==========================

def final_signal_release_v12(df) -> Dict:


    safety = execution_safety_check_v12(
        df
    )


    trade = get_signal_router_v12(
        df
    )



    if not safety["approved"]:


        return {

            "signal":

                "NO_TRADE",


            "approved":

                False,


            "reason":

                safety["reasons"]

        }



    if not trade["approved"]:


        return {

            "signal":

                "NO_TRADE",


            "approved":

                False

        }



    return {


        "signal":

            trade["signal"],


        "approved":

            True,


        "confidence":

            safety["confidence"],


        "trade":

            trade["trade"]

    }



# ==========================
# INSTITUTIONAL EXECUTION GUARD
# ==========================

def institutional_execution_guard_v12(df) -> Dict:


    return final_signal_release_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_execution_guard_v12(df) -> Dict:

    return institutional_execution_guard_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-19
# Final Intelligence Layer
# Institutional Trade Journal Engine
# Signal History + Performance Learning
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List
from datetime import datetime


# ==========================
# TRADE JOURNAL MEMORY
# ==========================

V12_TRADE_JOURNAL = []



# ==========================
# RECORD SIGNAL
# ==========================

def record_trade_signal_v12(
        trade: Dict
) -> Dict:


    journal_entry = {


        "time":

            datetime.utcnow().isoformat(),


        "signal":

            trade.get(
                "signal",
                "NONE"
            ),


        "entry":

            trade.get(
                "entry"
            ),


        "sl":

            trade.get(
                "sl"
            ),


        "tp1":

            trade.get(
                "tp1"
            ),


        "tp2":

            trade.get(
                "tp2"
            ),


        "tp3":

            trade.get(
                "tp3"
            ),


        "confidence":

            trade.get(
                "confidence",
                0
            ),


        "status":

            "OPEN"

    }



    V12_TRADE_JOURNAL.append(
        journal_entry
    )



    if len(
        V12_TRADE_JOURNAL
    ) > 500:

        del V12_TRADE_JOURNAL[0]



    return journal_entry



# ==========================
# UPDATE TRADE RESULT
# ==========================

def update_trade_result_v12(
        index: int,
        result: str,
        pnl: float
) -> Dict:


    if index >= len(
        V12_TRADE_JOURNAL
    ):

        return {}



    V12_TRADE_JOURNAL[index]["status"] = result


    V12_TRADE_JOURNAL[index]["pnl"] = pnl



    return V12_TRADE_JOURNAL[index]



# ==========================
# JOURNAL STATISTICS
# ==========================

def trade_journal_stats_v12() -> Dict:


    total = len(
        V12_TRADE_JOURNAL
    )


    wins = 0

    losses = 0



    for trade in V12_TRADE_JOURNAL:


        if trade.get("status") == "WIN":

            wins += 1



        elif trade.get("status") == "LOSS":

            losses += 1



    win_rate = 0



    if total:

        win_rate = round(

            (wins / total) * 100,

            2

        )



    return {


        "total":

            total,


        "wins":

            wins,


        "losses":

            losses,


        "win_rate":

            win_rate

    }



# ==========================
# LEARNING FEEDBACK ENGINE
# ==========================

def journal_learning_v12() -> Dict:


    stats = trade_journal_stats_v12()



    adjustment = 0



    if stats["win_rate"] >= 70:

        adjustment = 5



    elif stats["win_rate"] < 40:

        adjustment = -5



    return {

        "stats":

            stats,


        "confidence_adjustment":

            adjustment

    }



# ==========================
# TRADE JOURNAL ENGINE
# ==========================

def institutional_trade_journal_v12() -> Dict:


    return journal_learning_v12()



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_journal_v12() -> Dict:

    return institutional_trade_journal_v12()
    # ==========================
# STRUCTURE ENGINE V12
# PART 2F-20
# Final Intelligence Layer
# Institutional Master Signal Controller
# Complete V12 Execution Integration
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MASTER SIGNAL GENERATOR
# ==========================

def master_signal_controller_v12(df) -> Dict:


    execution = get_execution_guard_v12(
        df
    )


    journal = get_trade_journal_v12()



    if not execution["approved"]:


        return {

            "status":

                "BLOCKED",


            "signal":

                "NO_TRADE",


            "reason":

                execution.get(
                    "reason",
                    []
                )

        }



    trade = execution["trade"]



    record_trade_signal_v12(
        trade
    )



    return {


        "status":

            "EXECUTED",


        "signal":

            trade["signal"],


        "entry":

            trade["entry"],


        "sl":

            trade["sl"],


        "tp1":

            trade["tp1"],


        "tp2":

            trade["tp2"],


        "tp3":

            trade["tp3"],


        "confidence":

            execution["confidence"],


        "journal":

            journal

    }



# ==========================
# TELEGRAM FORMATTER
# ==========================

def telegram_signal_formatter_v12(
        signal: Dict
) -> str:


    if signal.get(
        "signal"
    ) == "NO_TRADE":


        return (

            "⚪ V12 NO TRADE\n"

            "Market conditions not approved."

        )



    return (

        "🚀 ICT V12 MASTER SIGNAL\n\n"

        f"Direction: {signal['signal']}\n"

        f"Entry: {signal['entry']}\n"

        f"SL: {signal['sl']}\n"

        f"TP1: {signal['tp1']}\n"

        f"TP2: {signal['tp2']}\n"

        f"TP3: {signal['tp3']}\n\n"

        f"Confidence: {signal['confidence']}%"

    )



# ==========================
# V12 FINAL ENGINE
# ==========================

def institutional_master_engine_v12(df) -> Dict:


    signal = master_signal_controller_v12(
        df
    )


    return {


        "data":

            signal,


        "message":

            telegram_signal_formatter_v12(
                signal
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_master_signal_v12(df) -> Dict:

    return institutional_master_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-1
# Global Intelligence Layer
# Institutional Multi Timeframe Synchronization Engine
# HTF Bias + LTF Entry Alignment
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# TIMEFRAME ALIGNMENT ENGINE
# ==========================

def timeframe_alignment_v12(
        htf_df,
        mtf_df,
        ltf_df
) -> Dict:


    htf_direction = optimized_direction_v12(
        htf_df
    )


    mtf_direction = optimized_direction_v12(
        mtf_df
    )


    ltf_direction = optimized_direction_v12(
        ltf_df
    )



    buy_votes = 0

    sell_votes = 0



    directions = [

        htf_direction,

        mtf_direction,

        ltf_direction

    ]



    for direction in directions:


        if direction == "BUY":

            buy_votes += 1



        elif direction == "SELL":

            sell_votes += 1



    alignment = max(
        buy_votes,
        sell_votes
    )



    final_direction = "NO_TRADE"



    if alignment >= 2:


        if buy_votes > sell_votes:

            final_direction = "BUY"



        elif sell_votes > buy_votes:

            final_direction = "SELL"



    return {


        "HTF":

            htf_direction,


        "MTF":

            mtf_direction,


        "LTF":

            ltf_direction,


        "direction":

            final_direction,


        "alignment":

            alignment

    }



# ==========================
# MTF CONFIDENCE BOOST
# ==========================

def mtf_confidence_v12(
        htf_df,
        mtf_df,
        ltf_df
) -> Dict:


    alignment = timeframe_alignment_v12(
        htf_df,
        mtf_df,
        ltf_df
    )



    score = 0



    score += alignment["alignment"] * 30



    if alignment["direction"] != "NO_TRADE":

        score += 20



    return {


        "direction":

            alignment["direction"],


        "score":

            min(
                score,
                100
            ),


        "alignment":

            alignment

    }



# ==========================
# GLOBAL SYNCHRONIZATION
# ==========================

def institutional_mtf_sync_engine_v12(
        htf_df,
        mtf_df,
        ltf_df
) -> Dict:


    return mtf_confidence_v12(
        htf_df,
        mtf_df,
        ltf_df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_mtf_sync_v12(
        htf_df,
        mtf_df,
        ltf_df
) -> Dict:

    return institutional_mtf_sync_engine_v12(
        htf_df,
        mtf_df,
        ltf_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-2
# Global Intelligence Layer
# Institutional Liquidity Cycle Engine
# Accumulation + Manipulation + Distribution Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# LIQUIDITY CYCLE DETECTOR
# ==========================

def liquidity_cycle_v12(df) -> Dict:


    if len(df) < 50:

        return {

            "phase":

                "UNKNOWN",

            "score":

                0

        }



    highs = df["high"].tail(50)

    lows = df["low"].tail(50)

    closes = df["close"].tail(50)



    high_range = float(
        highs.max()
    )


    low_range = float(
        lows.min()
    )


    current = float(
        closes.iloc[-1]
    )



    position = (

        current - low_range

    ) / (

        high_range - low_range

    ) * 100



    phase = "RANGE"

    score = 50



    # Accumulation zone

    if position < 35:


        phase = "ACCUMULATION"

        score = 80



    # Distribution zone

    elif position > 65:


        phase = "DISTRIBUTION"

        score = 80



    # Manipulation detection

    if detect_liquidity_sweep_v12(df):


        phase = "MANIPULATION"

        score = 90



    return {

        "phase":

            phase,


        "position":

            round(
                position,
                2
            ),


        "score":

            score

    }



# ==========================
# CYCLE DIRECTION ENGINE
# ==========================

def liquidity_cycle_direction_v12(df) -> Dict:


    cycle = liquidity_cycle_v12(
        df
    )


    direction = "NEUTRAL"



    if cycle["phase"] == "ACCUMULATION":

        direction = "BUY"



    elif cycle["phase"] == "DISTRIBUTION":

        direction = "SELL"



    elif cycle["phase"] == "MANIPULATION":


        direction = optimized_direction_v12(
            df
        )



    return {


        "phase":

            cycle["phase"],


        "direction":

            direction,


        "score":

            cycle["score"]

    }



# ==========================
# CYCLE VALIDATION FILTER
# ==========================

def liquidity_cycle_filter_v12(df) -> bool:


    result = liquidity_cycle_direction_v12(
        df
    )


    return (

        result["score"] >= 70

        and

        result["direction"] != "NEUTRAL"

    )



# ==========================
# GLOBAL LIQUIDITY CYCLE ENGINE
# ==========================

def institutional_liquidity_cycle_engine_v12(df) -> Dict:


    return {

        "cycle":

            liquidity_cycle_direction_v12(
                df
            ),


        "approved":

            liquidity_cycle_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_cycle_v12(df) -> Dict:

    return institutional_liquidity_cycle_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-3
# Global Intelligence Layer
# Institutional Bias Aggregation Engine
# Daily + Weekly + Monthly Market Bias
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# HIGHER TIMEFRAME BIAS
# ==========================

def higher_timeframe_bias_v12(df) -> Dict:


    if len(df) < 100:

        return {

            "bias":

                "NEUTRAL",

            "score":

                0

        }



    current = float(
        df["close"].iloc[-1]
    )


    daily_base = float(
        df["close"].iloc[-50]
    )


    weekly_base = float(
        df["close"].iloc[-100]
    )



    daily_bias = "NEUTRAL"

    weekly_bias = "NEUTRAL"



    if current > daily_base:

        daily_bias = "BULLISH"



    elif current < daily_base:

        daily_bias = "BEARISH"



    if current > weekly_base:

        weekly_bias = "BULLISH"



    elif current < weekly_base:

        weekly_bias = "BEARISH"



    score = 0



    if daily_bias == weekly_bias:

        score += 70



    else:

        score += 40



    return {

        "daily":

            daily_bias,


        "weekly":

            weekly_bias,


        "score":

            score

    }



# ==========================
# GLOBAL BIAS ENGINE
# ==========================

def global_bias_engine_v12(df) -> Dict:


    bias = higher_timeframe_bias_v12(
        df
    )


    final_bias = "NEUTRAL"



    if (

        bias["daily"]

        ==

        "BULLISH"

        and

        bias["weekly"]

        ==

        "BULLISH"

    ):

        final_bias = "BUY"



    elif (

        bias["daily"]

        ==

        "BEARISH"

        and

        bias["weekly"]

        ==

        "BEARISH"

    ):

        final_bias = "SELL"



    return {


        "bias":

            final_bias,


        "score":

            bias["score"],


        "details":

            bias

    }



# ==========================
# BIAS FILTER
# ==========================

def global_bias_filter_v12(df) -> bool:


    result = global_bias_engine_v12(
        df
    )


    return (

        result["score"] >= 70

        and

        result["bias"]

        !=

        "NEUTRAL"

    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_global_bias_v12(df) -> Dict:

    return global_bias_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-4
# Global Intelligence Layer
# Institutional Market Condition Engine
# Trend + Range + Reversal Classification
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET CONDITION DETECTOR
# ==========================

def market_condition_v12(df) -> Dict:


    if len(df) < 50:

        return {

            "condition":

                "UNKNOWN",

            "score":

                0

        }



    trend = trend_strength_v12(
        df
    )


    volatility = get_volatility_intelligence_v12(
        df
    )


    structure = get_structure_memory_v12(
        df
    )



    condition = "RANGE"

    score = 50



    # Strong trend environment

    if (

        trend >= 75

        and

        structure["score"] >= 60

    ):

        condition = "TREND"

        score = 85



    # High volatility condition

    if (

        volatility["volatility"]["state"]

        ==

        "EXPANSION"

    ):

        condition = "MOMENTUM"

        score = 90



    # Weak structure

    if trend < 40:


        condition = "RANGE"

        score = 60



    return {


        "condition":

            condition,


        "trend_score":

            trend,


        "structure_score":

            structure["score"],


        "score":

            score

    }



# ==========================
# MARKET MODE SELECTOR
# ==========================

def market_mode_selector_v12(df) -> Dict:


    market = market_condition_v12(
        df
    )


    mode = "WAIT"



    if market["condition"] == "TREND":


        mode = "TREND_FOLLOW"



    elif market["condition"] == "MOMENTUM":


        mode = "BREAKOUT"



    elif market["condition"] == "RANGE":


        mode = "MEAN_REVERSION"



    return {


        "condition":

            market["condition"],


        "mode":

            mode,


        "score":

            market["score"]

    }



# ==========================
# GLOBAL MARKET ENGINE
# ==========================

def institutional_market_condition_engine_v12(df) -> Dict:


    return market_mode_selector_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_condition_v12(df) -> Dict:

    return institutional_market_condition_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-5
# Global Intelligence Layer
# Institutional Market Phase Engine
# Accumulation + Expansion + Distribution + Reversal
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET PHASE DETECTOR
# ==========================

def market_phase_detector_v12(df) -> Dict:


    if len(df) < 50:

        return {

            "phase":

                "UNKNOWN",

            "score":

                0

        }



    high = float(
        df["high"].tail(50).max()
    )


    low = float(
        df["low"].tail(50).min()
    )


    close = float(
        df["close"].iloc[-1]
    )



    range_size = high - low



    if range_size == 0:

        return {

            "phase":

                "UNKNOWN",

            "score":

                0

        }



    position = (

        (close - low)

        /

        range_size

    ) * 100



    volume = float(
        df["volume"].tail(20).mean()
    )


    current_volume = float(
        df["volume"].iloc[-1]
    )



    phase = "BALANCE"

    score = 50



    # Accumulation

    if (

        position < 35

        and

        current_volume > volume

    ):

        phase = "ACCUMULATION"

        score = 85



    # Expansion

    elif (

        position > 35

        and

        position < 65

        and

        current_volume > volume

    ):

        phase = "EXPANSION"

        score = 90



    # Distribution

    elif (

        position > 65

    ):

        phase = "DISTRIBUTION"

        score = 80



    return {

        "phase":

            phase,


        "position":

            round(
                position,
                2
            ),


        "score":

            score

    }



# ==========================
# PHASE DIRECTION ENGINE
# ==========================

def phase_direction_v12(df) -> Dict:


    phase = market_phase_detector_v12(
        df
    )


    direction = "NEUTRAL"



    if phase["phase"] in [

        "ACCUMULATION",

        "EXPANSION"

    ]:

        direction = "BUY"



    elif phase["phase"] == "DISTRIBUTION":

        direction = "SELL"



    return {

        "phase":

            phase["phase"],


        "direction":

            direction,


        "score":

            phase["score"]

    }



# ==========================
# PHASE VALIDATION FILTER
# ==========================

def phase_filter_v12(df) -> bool:


    result = phase_direction_v12(
        df
    )


    return (

        result["score"] >= 75

        and

        result["direction"]

        !=

        "NEUTRAL"

    )



# ==========================
# GLOBAL MARKET PHASE ENGINE
# ==========================

def institutional_market_phase_engine_v12(df) -> Dict:


    return {

        "phase":

            phase_direction_v12(
                df
            ),


        "approved":

            phase_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_phase_v12(df) -> Dict:

    return institutional_market_phase_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-6
# Global Intelligence Layer
# Institutional Multi Asset Correlation Engine
# BTC + ETH + Market Leader Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ASSET CORRELATION CHECK
# ==========================

def asset_correlation_v12(
        primary_df,
        leader_df
) -> Dict:


    if len(primary_df) < 30 or len(leader_df) < 30:

        return {

            "correlated":

                False,

            "score":

                0

        }



    primary_move = (

        float(primary_df["close"].iloc[-1])

        -

        float(primary_df["close"].iloc[-30])

    )


    leader_move = (

        float(leader_df["close"].iloc[-1])

        -

        float(leader_df["close"].iloc[-30])

    )



    score = 0



    if (

        primary_move > 0

        and

        leader_move > 0

    ) or (

        primary_move < 0

        and

        leader_move < 0

    ):

        score += 60



    if abs(leader_move) > 0:

        score += 20



    if abs(primary_move) > 0:

        score += 20



    return {


        "correlated":

            score >= 70,


        "score":

            score

    }



# ==========================
# MARKET LEADER CONFIRMATION
# ==========================

def market_leader_confirmation_v12(
        asset_df,
        btc_df
) -> Dict:


    correlation = asset_correlation_v12(
        asset_df,
        btc_df
    )


    asset_direction = optimized_direction_v12(
        asset_df
    )


    btc_direction = optimized_direction_v12(
        btc_df
    )



    alignment = (

        asset_direction

        ==

        btc_direction

        and

        asset_direction != "RANGE"

    )



    score = correlation["score"]



    if alignment:

        score += 20



    return {


        "asset_direction":

            asset_direction,


        "leader_direction":

            btc_direction,


        "score":

            min(
                score,
                100
            ),


        "confirmed":

            score >= 80

    }



# ==========================
# CORRELATION FILTER
# ==========================

def correlation_filter_global_v12(
        asset_df,
        btc_df
) -> bool:


    result = market_leader_confirmation_v12(
        asset_df,
        btc_df
    )


    return result["confirmed"]



# ==========================
# GLOBAL CORRELATION ENGINE
# ==========================

def institutional_asset_correlation_engine_v12(
        asset_df,
        btc_df
) -> Dict:


    return market_leader_confirmation_v12(
        asset_df,
        btc_df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_asset_correlation_v12(
        asset_df,
        btc_df
) -> Dict:

    return institutional_asset_correlation_engine_v12(
        asset_df,
        btc_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-7
# Global Intelligence Layer
# Institutional Macro Liquidity Engine
# Global Liquidity Pool + Sweep Detection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# GLOBAL LIQUIDITY POOL FINDER
# ==========================

def global_liquidity_pools_v12(df) -> Dict:


    if len(df) < 50:

        return {

            "buy_side":

                [],

            "sell_side":

                []

        }



    buy_side = []

    sell_side = []



    for i in range(
        5,
        len(df)-5
    ):


        high = float(
            df["high"].iloc[i]
        )


        low = float(
            df["low"].iloc[i]
        )



        if (

            high >

            float(df["high"].iloc[i-1])

            and

            high >

            float(df["high"].iloc[i+1])

        ):

            buy_side.append(
                high
            )



        if (

            low <

            float(df["low"].iloc[i-1])

            and

            low <

            float(df["low"].iloc[i+1])

        ):

            sell_side.append(
                low
            )



    return {


        "buy_side":

            buy_side[-10:],


        "sell_side":

            sell_side[-10:]

    }



# ==========================
# LIQUIDITY RAID DETECTOR
# ==========================

def liquidity_raid_detector_v12(df) -> Dict:


    pools = global_liquidity_pools_v12(
        df
    )


    price = float(
        df["close"].iloc[-1]
    )



    raids = []



    for level in pools["buy_side"]:


        if price > level:

            raids.append(
                "BUY_SIDE_TAKEN"
            )



    for level in pools["sell_side"]:


        if price < level:

            raids.append(
                "SELL_SIDE_TAKEN"
            )



    return {


        "raids":

            raids,


        "score":

            90
            if raids
            else
            0

    }



# ==========================
# LIQUIDITY TARGET PRIORITY
# ==========================

def liquidity_target_priority_v12(df) -> Dict:


    pools = global_liquidity_pools_v12(
        df
    )


    direction = optimized_direction_v12(
        df
    )


    target = None



    if direction == "BUY":

        if pools["buy_side"]:

            target = max(
                pools["buy_side"]
            )



    elif direction == "SELL":

        if pools["sell_side"]:

            target = min(
                pools["sell_side"]
            )



    return {


        "direction":

            direction,


        "target":

            target

    }



# ==========================
# MACRO LIQUIDITY ENGINE
# ==========================

def institutional_macro_liquidity_engine_v12(df) -> Dict:


    return {


        "pools":

            global_liquidity_pools_v12(
                df
            ),


        "raid":

            liquidity_raid_detector_v12(
                df
            ),


        "target":

            liquidity_target_priority_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_macro_liquidity_v12(df) -> Dict:

    return institutional_macro_liquidity_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-8
# Global Intelligence Layer
# Institutional Market Sentiment Engine
# Fear/Greed + Positioning + Flow Bias
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# SENTIMENT PRESSURE ENGINE
# ==========================

def sentiment_pressure_v12(df) -> Dict:


    if len(df) < 30:

        return {

            "pressure":

                "NEUTRAL",

            "score":

                50

        }



    bullish = 0

    bearish = 0



    for i in range(
        len(df)-30,
        len(df)
    ):


        open_price = float(
            df["open"].iloc[i]
        )


        close_price = float(
            df["close"].iloc[i]
        )


        volume = float(
            df["volume"].iloc[i]
        )



        if close_price > open_price:

            bullish += volume



        elif close_price < open_price:

            bearish += volume



    total = bullish + bearish



    if total == 0:

        return {

            "pressure":

                "NEUTRAL",

            "score":

                50

        }



    bull_ratio = (

        bullish / total

    ) * 100



    pressure = "NEUTRAL"

    score = 50



    if bull_ratio >= 65:


        pressure = "BULLISH"

        score = 85



    elif bull_ratio <= 35:


        pressure = "BEARISH"

        score = 85



    else:


        score = 60



    return {


        "pressure":

            pressure,


        "bull_ratio":

            round(
                bull_ratio,
                2
            ),


        "score":

            score

    }



# ==========================
# SENTIMENT ALIGNMENT
# ==========================

def sentiment_alignment_v12(df) -> Dict:


    sentiment = sentiment_pressure_v12(
        df
    )


    structure = optimized_direction_v12(
        df
    )


    aligned = False



    if (

        sentiment["pressure"] == "BULLISH"

        and

        structure == "BUY"

    ):

        aligned = True



    elif (

        sentiment["pressure"] == "BEARISH"

        and

        structure == "SELL"

    ):

        aligned = True



    score = sentiment["score"]



    if aligned:

        score += 15



    return {


        "sentiment":

            sentiment["pressure"],


        "structure":

            structure,


        "score":

            min(
                score,
                100
            ),


        "aligned":

            aligned

    }



# ==========================
# SENTIMENT FILTER
# ==========================

def sentiment_filter_v12(df) -> bool:


    result = sentiment_alignment_v12(
        df
    )


    return (

        result["score"] >= 80

    )



# ==========================
# GLOBAL SENTIMENT ENGINE
# ==========================

def institutional_sentiment_engine_v12(df) -> Dict:


    return sentiment_alignment_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_sentiment_v12(df) -> Dict:

    return institutional_sentiment_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-9
# Global Intelligence Layer
# Institutional Price Delivery Engine
# Market Intent + Expansion Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# PRICE DELIVERY ANALYSIS
# ==========================

def price_delivery_analysis_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "delivery":

                "UNKNOWN",

            "score":

                0

        }



    recent_move = (

        float(df["close"].iloc[-1])

        -

        float(df["close"].iloc[-20])

    )


    avg_move = (

        df["close"]

        .diff()

        .tail(20)

        .abs()

        .mean()

    )



    score = 50

    delivery = "BALANCED"



    if recent_move > avg_move * 5:


        delivery = "BULLISH_EXPANSION"

        score = 90



    elif recent_move < -(avg_move * 5):


        delivery = "BEARISH_EXPANSION"

        score = 90



    elif abs(recent_move) < avg_move:


        delivery = "COMPRESSION"

        score = 70



    return {


        "delivery":

            delivery,


        "score":

            score

    }



# ==========================
# DELIVERY DIRECTION ENGINE
# ==========================

def delivery_direction_v12(df) -> Dict:


    delivery = price_delivery_analysis_v12(
        df
    )


    direction = "NEUTRAL"



    if delivery["delivery"] == "BULLISH_EXPANSION":

        direction = "BUY"



    elif delivery["delivery"] == "BEARISH_EXPANSION":

        direction = "SELL"



    return {


        "direction":

            direction,


        "delivery":

            delivery["delivery"],


        "score":

            delivery["score"]

    }



# ==========================
# DELIVERY VALIDATION
# ==========================

def delivery_filter_v12(df) -> bool:


    result = delivery_direction_v12(
        df
    )


    return (

        result["score"] >= 75

        and

        result["direction"]

        !=

        "NEUTRAL"

    )



# ==========================
# GLOBAL PRICE DELIVERY ENGINE
# ==========================

def institutional_price_delivery_engine_v12(df) -> Dict:


    return {


        "delivery":

            delivery_direction_v12(
                df
            ),


        "approved":

            delivery_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_price_delivery_v12(df) -> Dict:

    return institutional_price_delivery_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-10
# Global Intelligence Layer
# Institutional Market Narrative Engine
# Smart Money Story + Current Scenario Mapping
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# MARKET STORY BUILDER
# ==========================

def market_story_builder_v12(df) -> Dict:


    bias = get_global_bias_v12(
        df
    )


    phase = get_market_phase_v12(
        df
    )


    liquidity = get_macro_liquidity_v12(
        df
    )


    delivery = get_price_delivery_v12(
        df
    )


    sentiment = get_market_sentiment_v12(
        df
    )



    story = []

    score = 0



    # Global Bias

    if bias["bias"] == "BUY":

        story.append(
            "Higher timeframe bullish bias"
        )

        score += 20



    elif bias["bias"] == "SELL":

        story.append(
            "Higher timeframe bearish bias"
        )

        score += 20



    # Market Phase

    if phase["approved"]:


        story.append(

            phase["phase"]["phase"]

        )

        score += 20



    # Liquidity

    if liquidity["raid"]["score"] > 0:


        story.append(
            "Liquidity event detected"
        )

        score += 20



    # Delivery

    if delivery["approved"]:


        story.append(

            delivery["delivery"]["delivery"]

        )

        score += 20



    # Sentiment

    if sentiment["aligned"]:


        story.append(
            "Sentiment aligned"
        )

        score += 20



    return {


        "story":

            story,


        "score":

            min(
                score,
                100
            )

    }



# ==========================
# NARRATIVE DECISION
# ==========================

def narrative_decision_v12(df) -> Dict:


    result = market_story_builder_v12(
        df
    )


    direction = "NO_TRADE"



    bias = get_global_bias_v12(
        df
    )["bias"]



    if result["score"] >= 70:


        if bias == "BUY":

            direction = "BUY"



        elif bias == "SELL":

            direction = "SELL"



    return {


        "direction":

            direction,


        "confidence":

            result["score"],


        "story":

            result["story"]

    }



# ==========================
# GLOBAL NARRATIVE ENGINE
# ==========================

def institutional_market_narrative_engine_v12(df) -> Dict:


    return narrative_decision_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_market_narrative_v12(df) -> Dict:

    return institutional_market_narrative_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-11
# Global Intelligence Layer
# Institutional Trade Timing Engine
# Killzone + Session + Volatility Timing
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict
from datetime import datetime, timezone


# ==========================
# MARKET SESSION DETECTOR
# ==========================

def market_session_v12() -> Dict:


    hour = datetime.now(
        timezone.utc
    ).hour



    session = "OFF_HOURS"

    score = 40



    # London Session

    if 7 <= hour < 12:


        session = "LONDON"

        score = 85



    # New York Session

    elif 12 <= hour < 17:


        session = "NEW_YORK"

        score = 90



    # Asia Session

    elif 0 <= hour < 7:


        session = "ASIA"

        score = 60



    return {


        "session":

            session,


        "score":

            score

    }



# ==========================
# KILLZONE DETECTION
# ==========================

def ict_killzone_v12() -> Dict:


    session = market_session_v12()


    killzone = False



    if session["session"] in [

        "LONDON",

        "NEW_YORK"

    ]:


        killzone = True



    return {


        "killzone":

            killzone,


        "session":

            session["session"],


        "score":

            session["score"]

    }



# ==========================
# ENTRY TIME QUALITY
# ==========================

def timing_quality_v12(df) -> Dict:


    killzone = ict_killzone_v12()


    volatility = get_volatility_intelligence_v12(
        df
    )



    score = 0



    score += killzone["score"] * 0.5



    score += volatility["volatility"]["score"] * 0.5



    return {


        "score":

            int(
                min(
                    score,
                    100
                )
            ),


        "killzone":

            killzone["killzone"],


        "session":

            killzone["session"]

    }



# ==========================
# TIMING FILTER
# ==========================

def timing_filter_v12(df) -> bool:


    result = timing_quality_v12(
        df
    )


    return (

        result["score"] >= 75

    )



# ==========================
# GLOBAL TIMING ENGINE
# ==========================

def institutional_trade_timing_engine_v12(df) -> Dict:


    return {


        "timing":

            timing_quality_v12(
                df
            ),


        "approved":

            timing_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_timing_v12(df) -> Dict:

    return institutional_trade_timing_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-12
# Global Intelligence Layer
# Institutional Confluence Matrix Engine
# All V12 Modules Final Alignment
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# GLOBAL CONFLUENCE SCORER
# ==========================

def global_confluence_score_v12(df) -> Dict:


    scores = {


        "bias":

            get_global_bias_v12(df)
            ["score"],


        "phase":

            get_market_phase_v12(df)
            ["phase"]
            ["score"],


        "liquidity":

            get_macro_liquidity_v12(df)
            ["raid"]
            ["score"],


        "delivery":

            get_price_delivery_v12(df)
            ["delivery"]
            ["score"],


        "sentiment":

            get_market_sentiment_v12(df)
            ["score"],


        "timing":

            get_trade_timing_v12(df)
            ["timing"]
            ["score"]

    }



    total = 0



    for value in scores.values():

        total += value



    confidence = int(

        total /

        len(scores)

    )



    return {


        "confidence":

            confidence,


        "components":

            scores

    }



# ==========================
# CONFLUENCE DIRECTION
# ==========================

def confluence_direction_v12(df) -> Dict:


    bias = get_global_bias_v12(
        df
    )


    phase = get_market_phase_v12(
        df
    )


    delivery = get_price_delivery_v12(
        df
    )



    buy = 0

    sell = 0



    sources = [

        bias["bias"],


        phase["phase"]["direction"],


        delivery["delivery"]["direction"]

    ]



    for source in sources:


        if source == "BUY":

            buy += 1



        elif source == "SELL":

            sell += 1



    direction = "NO_TRADE"



    if buy >= 2:

        direction = "BUY"



    elif sell >= 2:

        direction = "SELL"



    return {


        "direction":

            direction,


        "buy_votes":

            buy,


        "sell_votes":

            sell

    }



# ==========================
# FINAL GLOBAL FILTER
# ==========================

def global_confluence_filter_v12(df) -> bool:


    score = global_confluence_score_v12(
        df
    )


    direction = confluence_direction_v12(
        df
    )



    return (

        score["confidence"] >= 80

        and

        direction["direction"]

        !=

        "NO_TRADE"

    )



# ==========================
# MASTER GLOBAL CONFLUENCE
# ==========================

def institutional_global_confluence_engine_v12(df) -> Dict:


    score = global_confluence_score_v12(
        df
    )


    direction = confluence_direction_v12(
        df
    )



    return {


        "direction":

            direction["direction"],


        "confidence":

            score["confidence"],


        "approved":

            global_confluence_filter_v12(
                df
            ),


        "components":

            score["components"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_global_confluence_v12(df) -> Dict:

    return institutional_global_confluence_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-13
# Global Intelligence Layer
# Institutional Market Bias Fusion Engine
# HTF + Liquidity + Structure + Flow Integration
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# BIAS FUSION CALCULATOR
# ==========================

def bias_fusion_v12(df) -> Dict:


    signals = {


        "global":

            get_global_bias_v12(df)
            ["bias"],


        "phase":

            get_market_phase_v12(df)
            ["phase"]
            ["direction"],


        "liquidity":

            get_macro_liquidity_v12(df)
            ["target"]
            ["direction"],


        "structure":

            get_structure_memory_v12(df)
            ["structure"]
            ["event"],


        "flow":

            get_order_flow_v12(df)
            ["direction"]

    }



    buy_score = 0

    sell_score = 0



    for key, value in signals.items():


        if value in [

            "BUY",

        ]:

            buy_score += 20



        elif value in [

            "SELL",

        ]:

            sell_score += 20



        elif value == "BULLISH_BOS":

            buy_score += 20



        elif value == "BEARISH_BOS":

            sell_score += 20



    direction = "NEUTRAL"



    if buy_score > sell_score:

        direction = "BUY"



    elif sell_score > buy_score:

        direction = "SELL"



    return {


        "direction":

            direction,


        "buy_score":

            buy_score,


        "sell_score":

            sell_score,


        "sources":

            signals

    }



# ==========================
# FUSED BIAS CONFIDENCE
# ==========================

def fused_bias_confidence_v12(df) -> Dict:


    fusion = bias_fusion_v12(
        df
    )


    confidence = max(

        fusion["buy_score"],

        fusion["sell_score"]

    )



    return {


        "direction":

            fusion["direction"],


        "confidence":

            min(
                confidence,
                100
            ),


        "details":

            fusion["sources"]

    }



# ==========================
# BIAS FUSION FILTER
# ==========================

def bias_fusion_filter_v12(df) -> bool:


    result = fused_bias_confidence_v12(
        df
    )


    return (

        result["confidence"] >= 70

        and

        result["direction"]

        !=

        "NEUTRAL"

    )



# ==========================
# GLOBAL BIAS FUSION ENGINE
# ==========================

def institutional_bias_fusion_engine_v12(df) -> Dict:


    return {


        "bias":

            fused_bias_confidence_v12(
                df
            ),


        "approved":

            bias_fusion_filter_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_bias_fusion_v12(df) -> Dict:

    return institutional_bias_fusion_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-14
# Global Intelligence Layer
# Institutional Liquidity Entry Alignment Engine
# POI + Liquidity + Bias Synchronization
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# LIQUIDITY ENTRY ALIGNMENT
# ==========================

def liquidity_entry_alignment_v12(df) -> Dict:


    liquidity = get_macro_liquidity_v12(
        df
    )


    bias = get_bias_fusion_v12(
        df
    )


    poi = get_precision_zone_v12(
        df
    )



    direction = bias["bias"]["direction"]



    alignment = False

    score = 0



    if direction == "BUY":


        if liquidity["target"]["direction"] == "BUY":

            score += 40



        if poi["zone"]:

            score += 30



        alignment = score >= 60



    elif direction == "SELL":


        if liquidity["target"]["direction"] == "SELL":

            score += 40



        if poi["zone"]:

            score += 30



        alignment = score >= 60



    return {


        "direction":

            direction,


        "score":

            score,


        "aligned":

            alignment,


        "poi":

            poi["zone"]

    }



# ==========================
# ENTRY LOCATION QUALITY
# ==========================

def entry_location_quality_v12(df) -> Dict:


    alignment = liquidity_entry_alignment_v12(
        df
    )


    score = alignment["score"]



    if detect_displacement(df):

        score += 20



    if volume_confirmation_v12(df):

        score += 20



    return {


        "quality":

            min(
                score,
                100
            ),


        "direction":

            alignment["direction"],


        "approved":

            score >= 80

    }



# ==========================
# LIQUIDITY ENTRY ENGINE
# ==========================

def institutional_liquidity_entry_engine_v12(df) -> Dict:


    return entry_location_quality_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_liquidity_entry_v12(df) -> Dict:

    return institutional_liquidity_entry_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-15
# Global Intelligence Layer
# Institutional Final Entry Confirmation Engine
# Last Confirmation Before Trade Trigger
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# FINAL CONFIRMATION SCORER
# ==========================

def final_confirmation_score_v12(df) -> Dict:


    scores = {


        "bias":

            get_bias_fusion_v12(df)
            ["bias"]
            ["confidence"],


        "liquidity":

            get_liquidity_entry_v12(df)
            ["quality"],


        "confluence":

            get_global_confluence_v12(df)
            ["confidence"],


        "timing":

            get_trade_timing_v12(df)
            ["timing"]
            ["score"],


        "structure":

            get_structure_memory_v12(df)
            ["score"]

    }



    total = 0



    for value in scores.values():

        total += value



    final_score = int(

        total /

        len(scores)

    )



    return {


        "score":

            final_score,


        "components":

            scores

    }



# ==========================
# FINAL DIRECTION CHECK
# ==========================

def final_confirmation_direction_v12(df) -> Dict:


    bias = get_bias_fusion_v12(
        df
    )


    liquidity = get_liquidity_entry_v12(
        df
    )


    confluence = get_global_confluence_v12(
        df
    )



    votes = [

        bias["bias"]["direction"],

        liquidity["direction"],

        confluence["direction"]

    ]



    buy = votes.count(
        "BUY"
    )


    sell = votes.count(
        "SELL"
    )



    direction = "NO_TRADE"



    if buy >= 2:

        direction = "BUY"



    elif sell >= 2:

        direction = "SELL"



    return {


        "direction":

            direction,


        "buy_votes":

            buy,


        "sell_votes":

            sell

    }



# ==========================
# FINAL TRADE APPROVAL
# ==========================

def final_trade_confirmation_v12(df) -> Dict:


    score = final_confirmation_score_v12(
        df
    )


    direction = final_confirmation_direction_v12(
        df
    )



    approved = (

        score["score"] >= 85

        and

        direction["direction"]

        !=

        "NO_TRADE"

    )



    return {


        "approved":

            approved,


        "direction":

            direction["direction"],


        "confidence":

            score["score"],


        "components":

            score["components"]

    }



# ==========================
# MASTER CONFIRMATION ENGINE
# ==========================

def institutional_final_confirmation_engine_v12(df) -> Dict:


    return final_trade_confirmation_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_final_confirmation_v12(df) -> Dict:

    return institutional_final_confirmation_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-16
# Global Intelligence Layer
# Institutional Smart Money Entry Trigger Engine
# Final BOS + MSS + Liquidity + POI Trigger
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ENTRY TRIGGER DETECTOR
# ==========================

def smart_money_trigger_v12(df) -> Dict:


    structure = get_structure_memory_v12(
        df
    )


    liquidity = get_liquidity_entry_v12(
        df
    )


    confirmation = get_final_confirmation_v12(
        df
    )



    trigger = False

    reason = []



    if structure["structure"]["event"] in [

        "BULLISH_BOS",

        "BEARISH_BOS"

    ]:


        trigger = True


        reason.append(
            "STRUCTURE_BREAK"
        )



    if liquidity["approved"]:


        trigger = True


        reason.append(
            "LIQUIDITY_ALIGNMENT"
        )



    if confirmation["approved"]:


        trigger = True


        reason.append(
            "FINAL_CONFIRMATION"
        )



    return {


        "trigger":

            trigger,


        "direction":

            confirmation["direction"],


        "confidence":

            confirmation["confidence"],


        "reason":

            reason

    }



# ==========================
# ENTRY ACTIVATION FILTER
# ==========================

def entry_activation_filter_v12(df) -> bool:


    result = smart_money_trigger_v12(
        df
    )


    return (

        result["trigger"]

        and

        result["confidence"]

        >=

        85

    )



# ==========================
# SMART MONEY ENTRY ENGINE
# ==========================

def institutional_smart_money_entry_engine_v12(df) -> Dict:


    trigger = smart_money_trigger_v12(
        df
    )


    return {


        "signal":

            trigger["direction"]
            if entry_activation_filter_v12(df)

            else

            "NO_TRADE",


        "confidence":

            trigger["confidence"],


        "trigger":

            trigger["trigger"],


        "reason":

            trigger["reason"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_smart_money_entry_v12(df) -> Dict:

    return institutional_smart_money_entry_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-17
# Global Intelligence Layer
# Institutional Adaptive Risk Engine
# Dynamic SL + Position Risk Adjustment
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# VOLATILITY RISK ADAPTER
# ==========================

def adaptive_risk_factor_v12(df) -> Dict:


    volatility = get_volatility_intelligence_v12(
        df
    )


    state = volatility["volatility"]["state"]



    factor = 1.5

    mode = "NORMAL"



    if state == "EXPANSION":


        factor = 2.0

        mode = "HIGH_VOLATILITY"



    elif state == "COMPRESSION":


        factor = 1.2

        mode = "LOW_VOLATILITY"



    return {


        "atr_factor":

            factor,


        "mode":

            mode

    }



# ==========================
# DYNAMIC STOP LOSS ENGINE
# ==========================

def adaptive_stop_loss_v12(
        df,
        entry: float,
        direction: str
) -> float:


    atr = structure_atr(
        df
    )


    risk = adaptive_risk_factor_v12(
        df
    )


    multiplier = risk["atr_factor"]



    if direction == "BUY":


        return round(

            entry -

            (atr * multiplier),

            4

        )



    elif direction == "SELL":


        return round(

            entry +

            (atr * multiplier),

            4

        )



    return entry



# ==========================
# POSITION RISK SCORE
# ==========================

def position_risk_score_v12(df) -> Dict:


    volatility = get_volatility_intelligence_v12(
        df
    )


    confidence = get_final_confirmation_v12(
        df
    )



    risk = 50



    if confidence["confidence"] >= 90:

        risk += 25



    if volatility["volatility"]["state"] == "EXPANSION":

        risk -= 20



    return {


        "risk_score":

            max(
                min(
                    risk,
                    100
                ),
                0
            )

    }



# ==========================
# ADAPTIVE RISK ENGINE
# ==========================

def institutional_adaptive_risk_engine_v12(df) -> Dict:


    return {


        "factor":

            adaptive_risk_factor_v12(
                df
            ),


        "risk":

            position_risk_score_v12(
                df
            )

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_adaptive_risk_v12(df) -> Dict:

    return institutional_adaptive_risk_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-18
# Global Intelligence Layer
# Institutional Smart Money Exit Engine
# TP Management + Partial Exit + Protection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# PROFIT TARGET CALCULATOR
# ==========================

def smart_money_targets_v12(
        entry: float,
        sl: float,
        direction: str
) -> Dict:


    risk = abs(
        entry - sl
    )



    if risk == 0:

        return {}



    if direction == "BUY":


        return {


            "tp1":

                round(
                    entry + risk,
                    4
                ),


            "tp2":

                round(
                    entry + (risk * 2),
                    4
                ),


            "tp3":

                round(
                    entry + (risk * 3),
                    4
                )

        }



    elif direction == "SELL":


        return {


            "tp1":

                round(
                    entry - risk,
                    4
                ),


            "tp2":

                round(
                    entry - (risk * 2),
                    4
                ),


            "tp3":

                round(
                    entry - (risk * 3),
                    4
                )

        }



    return {}



# ==========================
# PARTIAL EXIT MANAGER
# ==========================

def partial_exit_manager_v12(
        current_price: float,
        entry: float,
        tp: Dict,
        direction: str
) -> Dict:


    reached = []


    if direction == "BUY":


        if current_price >= tp["tp1"]:

            reached.append(
                "TP1"
            )


        if current_price >= tp["tp2"]:

            reached.append(
                "TP2"
            )


        if current_price >= tp["tp3"]:

            reached.append(
                "TP3"
            )



    elif direction == "SELL":


        if current_price <= tp["tp1"]:

            reached.append(
                "TP1"
            )


        if current_price <= tp["tp2"]:

            reached.append(
                "TP2"
            )


        if current_price <= tp["tp3"]:

            reached.append(
                "TP3"
            )



    return {


        "hit":

            reached,


        "count":

            len(reached)

    }



# ==========================
# SMART EXIT PROTECTION
# ==========================

def smart_exit_protection_v12(df) -> Dict:


    structure = get_structure_memory_v12(
        df
    )


    volatility = get_volatility_intelligence_v12(
        df
    )



    exit_signal = False

    reason = []



    if structure["structure"]["event"] in [

        "BEARISH_BOS",

        "BULLISH_BOS"

    ]:


        exit_signal = True

        reason.append(
            "STRUCTURE_CHANGE"
        )



    if volatility["volatility"]["state"] == "EXPANSION":


        reason.append(
            "HIGH_VOLATILITY"
        )



    return {


        "exit":

            exit_signal,


        "reason":

            reason

    }



# ==========================
# FINAL EXIT ENGINE
# ==========================

def institutional_exit_engine_v12(
        df,
        entry: float,
        sl: float,
        direction: str
) -> Dict:


    current = float(
        df["close"].iloc[-1]
    )


    targets = smart_money_targets_v12(
        entry,
        sl,
        direction
    )


    partial = partial_exit_manager_v12(
        current,
        entry,
        targets,
        direction
    )


    protection = smart_exit_protection_v12(
        df
    )



    return {


        "targets":

            targets,


        "partial":

            partial,


        "protection":

            protection

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_exit_engine_v12(
        df,
        entry,
        sl,
        direction
) -> Dict:

    return institutional_exit_engine_v12(
        df,
        entry,
        sl,
        direction
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-19
# Global Intelligence Layer
# Institutional Trade Lifecycle Engine
# Signal -> Entry -> Management -> Exit Tracking
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict
from datetime import datetime, timezone


# ==========================
# ACTIVE TRADE MEMORY
# ==========================

V12_ACTIVE_TRADES = []



# ==========================
# OPEN TRADE REGISTER
# ==========================

def register_trade_v12(trade: Dict) -> Dict:


    position = {


        "id":

            len(
                V12_ACTIVE_TRADES
            ) + 1,


        "time":

            datetime.now(
                timezone.utc
            ).isoformat(),


        "direction":

            trade.get(
                "signal"
            ),


        "entry":

            trade.get(
                "entry"
            ),


        "sl":

            trade.get(
                "sl"
            ),


        "tp1":

            trade.get(
                "tp1"
            ),


        "tp2":

            trade.get(
                "tp2"
            ),


        "tp3":

            trade.get(
                "tp3"
            ),


        "status":

            "OPEN"

    }



    V12_ACTIVE_TRADES.append(
        position
    )



    return position



# ==========================
# TRADE MONITOR
# ==========================

def monitor_trade_v12(
        current_price: float
) -> Dict:


    updates = []



    for trade in V12_ACTIVE_TRADES:


        direction = trade["direction"]



        if direction == "BUY":


            if current_price <= trade["sl"]:

                trade["status"] = "STOP_LOSS"

                updates.append(
                    trade
                )


            elif current_price >= trade["tp3"]:

                trade["status"] = "TP3_HIT"

                updates.append(
                    trade
                )



        elif direction == "SELL":


            if current_price >= trade["sl"]:

                trade["status"] = "STOP_LOSS"

                updates.append(
                    trade
                )


            elif current_price <= trade["tp3"]:

                trade["status"] = "TP3_HIT"

                updates.append(
                    trade
                )



    return {


        "updates":

            updates,


        "active":

            len(
                V12_ACTIVE_TRADES
            )

    }



# ==========================
# TRADE CLEANUP
# ==========================

def cleanup_closed_trades_v12() -> int:


    global V12_ACTIVE_TRADES



    V12_ACTIVE_TRADES = [

        trade

        for trade in V12_ACTIVE_TRADES

        if trade["status"] == "OPEN"

    ]



    return len(
        V12_ACTIVE_TRADES
    )



# ==========================
# LIFECYCLE STATUS
# ==========================

def trade_lifecycle_status_v12() -> Dict:


    return {


        "open_trades":

            len(
                V12_ACTIVE_TRADES
            ),


        "trades":

            V12_ACTIVE_TRADES[-10:]

    }



# ==========================
# INSTITUTIONAL LIFECYCLE ENGINE
# ==========================

def institutional_trade_lifecycle_engine_v12() -> Dict:


    return trade_lifecycle_status_v12()



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_trade_lifecycle_v12() -> Dict:

    return institutional_trade_lifecycle_engine_v12()
    # ==========================
# STRUCTURE ENGINE V12
# PART 2G-20
# Global Intelligence Layer
# Institutional Master Intelligence Router
# Complete Global Engine Integration
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# GLOBAL ENGINE STATUS
# ==========================

def global_engine_status_v12(df) -> Dict:


    modules = {


        "bias":

            get_global_bias_v12(df),


        "phase":

            get_market_phase_v12(df),


        "liquidity":

            get_macro_liquidity_v12(df),


        "sentiment":

            get_market_sentiment_v12(df),


        "timing":

            get_trade_timing_v12(df),


        "confluence":

            get_global_confluence_v12(df),


        "confirmation":

            get_final_confirmation_v12(df)

    }



    return modules



# ==========================
# FINAL GLOBAL DECISION
# ==========================

def global_master_decision_v12(df) -> Dict:


    status = global_engine_status_v12(
        df
    )


    confirmation = status["confirmation"]



    signal = "NO_TRADE"



    if confirmation["approved"]:


        signal = confirmation["direction"]



    return {


        "signal":

            signal,


        "confidence":

            confirmation["confidence"],


        "modules":

            status

    }



# ==========================
# MASTER V12 ROUTER
# ==========================

def institutional_global_master_engine_v12(df) -> Dict:


    decision = global_master_decision_v12(
        df
    )



    return {


        "version":

            "V12",


        "layer":

            "GLOBAL_INTELLIGENCE",


        "signal":

            decision["signal"],


        "confidence":

            decision["confidence"],


        "engine_data":

            decision["modules"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_global_master_v12(df) -> Dict:

    return institutional_global_master_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-1
# Advanced Execution Intelligence Layer
# Institutional Entry Precision Engine
# POI + Trigger + Timing Synchronization
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# PRECISION ENTRY SCORER
# ==========================

def precision_entry_score_v12(df) -> Dict:


    poi = get_precision_zone_v12(
        df
    )


    confirmation = get_final_confirmation_v12(
        df
    )


    timing = get_trade_timing_v12(
        df
    )


    liquidity = get_liquidity_entry_v12(
        df
    )



    scores = {


        "poi":

            0,


        "confirmation":

            confirmation["confidence"],


        "timing":

            timing["timing"]["score"],


        "liquidity":

            liquidity["quality"]

    }



    if poi.get("zone"):

        scores["poi"] = 90



    total = sum(
        scores.values()
    )



    final_score = int(

        total /

        len(scores)

    )



    return {


        "score":

            final_score,


        "components":

            scores

    }



# ==========================
# ENTRY PRECISION DECISION
# ==========================

def precision_entry_decision_v12(df) -> Dict:


    result = precision_entry_score_v12(
        df
    )


    direction = get_final_confirmation_v12(
        df
    )["direction"]



    approved = (

        result["score"]

        >=

        85

        and

        direction

        !=

        "NO_TRADE"

    )



    return {


        "approved":

            approved,


        "direction":

            direction,


        "confidence":

            result["score"],


        "components":

            result["components"]

    }



# ==========================
# ADVANCED ENTRY ENGINE
# ==========================

def institutional_precision_entry_engine_v12(df) -> Dict:


    return precision_entry_decision_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_precision_entry_v12(df) -> Dict:

    return institutional_precision_entry_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-2
# Advanced Execution Intelligence Layer
# Institutional Breakout Validation Engine
# BOS + Displacement + Volume Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# BREAKOUT VALIDATION ENGINE
# ==========================

def breakout_validation_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "valid":

                False,

            "score":

                0

        }



    current_close = float(
        df["close"].iloc[-1]
    )


    previous_high = float(
        df["high"].iloc[-10:-1].max()
    )


    previous_low = float(
        df["low"].iloc[-10:-1].min()
    )



    volume_avg = float(
        df["volume"].tail(20).mean()
    )


    current_volume = float(
        df["volume"].iloc[-1]
    )



    direction = "NONE"

    score = 0



    # Bullish breakout

    if current_close > previous_high:


        direction = "BUY"

        score += 40



    # Bearish breakout

    elif current_close < previous_low:


        direction = "SELL"

        score += 40



    # Volume confirmation

    if current_volume > volume_avg:


        score += 30



    # Displacement confirmation

    candle_size = abs(

        float(df["close"].iloc[-1])

        -

        float(df["open"].iloc[-1])

    )


    avg_candle = (

        abs(df["close"] - df["open"])

        .tail(20)

        .mean()

    )



    if candle_size > avg_candle:


        score += 30



    return {


        "direction":

            direction,


        "score":

            min(
                score,
                100
            ),


        "valid":

            score >= 70

    }



# ==========================
# FALSE BREAKOUT FILTER
# ==========================

def false_breakout_filter_v12(df) -> bool:


    result = breakout_validation_v12(
        df
    )


    return result["valid"]



# ==========================
# BREAKOUT EXECUTION ENGINE
# ==========================

def institutional_breakout_engine_v12(df) -> Dict:


    result = breakout_validation_v12(
        df
    )


    return {


        "signal":

            result["direction"]
            if result["valid"]

            else

            "NO_TRADE",


        "confidence":

            result["score"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_breakout_engine_v12(df) -> Dict:

    return institutional_breakout_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-3
# Advanced Execution Intelligence Layer
# Institutional Reversal Detection Engine
# Liquidity Sweep + MSS + Reversal Confirmation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# LIQUIDITY SWEEP DETECTOR
# ==========================

def reversal_liquidity_sweep_v12(df) -> Dict:


    if len(df) < 30:

        return {

            "sweep":

                False,

            "direction":

                "NONE",

            "score":

                0

        }



    recent_high = float(
        df["high"].tail(20).max()
    )


    recent_low = float(
        df["low"].tail(20).min()
    )


    current_close = float(
        df["close"].iloc[-1]
    )


    current_high = float(
        df["high"].iloc[-1]
    )


    current_low = float(
        df["low"].iloc[-1]
    )



    direction = "NONE"

    score = 0

    sweep = False



    # Buy side liquidity sweep

    if (

        current_high > recent_high

        and

        current_close < recent_high

    ):

        direction = "SELL"

        sweep = True

        score += 50



    # Sell side liquidity sweep

    elif (

        current_low < recent_low

        and

        current_close > recent_low

    ):

        direction = "BUY"

        sweep = True

        score += 50



    return {


        "sweep":

            sweep,


        "direction":

            direction,


        "score":

            score

    }



# ==========================
# REVERSAL CONFIRMATION
# ==========================

def reversal_confirmation_v12(df) -> Dict:


    sweep = reversal_liquidity_sweep_v12(
        df
    )


    structure = get_structure_memory_v12(
        df
    )



    score = sweep["score"]



    if structure["structure"]["event"] in [

        "BULLISH_MSS",

        "BEARISH_MSS"

    ]:

        score += 40



    approved = score >= 70



    return {


        "direction":

            sweep["direction"],


        "confidence":

            min(
                score,
                100
            ),


        "approved":

            approved

    }



# ==========================
# REVERSAL ENGINE
# ==========================

def institutional_reversal_engine_v12(df) -> Dict:


    result = reversal_confirmation_v12(
        df
    )


    return {


        "signal":

            result["direction"]
            if result["approved"]

            else

            "NO_TRADE",


        "confidence":

            result["confidence"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_reversal_engine_v12(df) -> Dict:

    return institutional_reversal_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-4
# Advanced Execution Intelligence Layer
# Institutional Order Flow Execution Engine
# Delta Pressure + Aggressive Buying/Selling Detection
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ORDER FLOW PRESSURE
# ==========================

def order_flow_pressure_v12(df) -> Dict:


    if len(df) < 30:

        return {

            "pressure":

                "NEUTRAL",

            "score":

                0

        }



    buy_pressure = 0

    sell_pressure = 0



    for i in range(
        len(df)-30,
        len(df)
    ):


        candle = (

            float(df["close"].iloc[i])

            -

            float(df["open"].iloc[i])

        )


        volume = float(
            df["volume"].iloc[i]
        )



        if candle > 0:

            buy_pressure += (

                candle *

                volume

            )



        elif candle < 0:

            sell_pressure += abs(

                candle *

                volume

            )



    total = (

        buy_pressure +

        sell_pressure

    )



    if total == 0:

        return {

            "pressure":

                "NEUTRAL",

            "score":

                50

        }



    buy_ratio = (

        buy_pressure /

        total

    ) * 100



    pressure = "NEUTRAL"

    score = 50



    if buy_ratio >= 65:


        pressure = "BUY"

        score = 85



    elif buy_ratio <= 35:


        pressure = "SELL"

        score = 85



    return {


        "pressure":

            pressure,


        "buy_ratio":

            round(
                buy_ratio,
                2
            ),


        "score":

            score

    }



# ==========================
# FLOW DIRECTION CONFIRMATION
# ==========================

def order_flow_confirmation_v12(df) -> Dict:


    flow = order_flow_pressure_v12(
        df
    )


    structure = optimized_direction_v12(
        df
    )



    confidence = flow["score"]



    if flow["pressure"] == structure:

        confidence += 15



    return {


        "direction":

            flow["pressure"],


        "confidence":

            min(
                confidence,
                100
            )

    }



# ==========================
# ORDER FLOW ENGINE
# ==========================

def institutional_order_flow_engine_v12(df) -> Dict:


    result = order_flow_confirmation_v12(
        df
    )


    return {


        "direction":

            result["direction"],


        "score":

            result["confidence"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_order_flow_v12(df) -> Dict:

    return institutional_order_flow_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-5
# Advanced Execution Intelligence Layer
# Institutional Fair Value Execution Engine
# FVG + Imbalance + Price Delivery
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# FVG DETECTION ENGINE
# ==========================

def detect_fvg_v12(df) -> List[Dict]:


    fvgs = []



    if len(df) < 5:

        return fvgs



    for i in range(
        2,
        len(df)
    ):


        candle1_high = float(
            df["high"].iloc[i-2]
        )


        candle1_low = float(
            df["low"].iloc[i-2]
        )


        candle3_high = float(
            df["high"].iloc[i]
        )


        candle3_low = float(
            df["low"].iloc[i]
        )



        # Bullish imbalance

        if candle3_low > candle1_high:


            fvgs.append({


                "type":

                    "BULLISH_FVG",


                "high":

                    candle3_low,


                "low":

                    candle1_high

            })



        # Bearish imbalance

        elif candle3_high < candle1_low:


            fvgs.append({


                "type":

                    "BEARISH_FVG",


                "high":

                    candle1_low,


                "low":

                    candle3_high

            })



    return fvgs



# ==========================
# FVG QUALITY SCORER
# ==========================

def fvg_quality_v12(df) -> Dict:


    fvgs = detect_fvg_v12(
        df
    )


    score = 0

    direction = "NONE"



    if fvgs:


        latest = fvgs[-1]


        if latest["type"] == "BULLISH_FVG":


            direction = "BUY"



        elif latest["type"] == "BEARISH_FVG":


            direction = "SELL"



        score = 75



        if detect_displacement(df):

            score += 15



    return {


        "direction":

            direction,


        "score":

            min(
                score,
                100
            ),


        "fvg":

            fvgs[-1]
            if fvgs

            else

            None

    }



# ==========================
# FVG ENTRY VALIDATION
# ==========================

def fvg_entry_validation_v12(df) -> Dict:


    fvg = fvg_quality_v12(
        df
    )


    liquidity = get_liquidity_entry_v12(
        df
    )



    confidence = fvg["score"]



    if (

        fvg["direction"]

        ==

        liquidity["direction"]

    ):

        confidence += 15



    return {


        "approved":

            confidence >= 80,


        "direction":

            fvg["direction"],


        "confidence":

            min(
                confidence,
                100
            )

    }



# ==========================
# FAIR VALUE EXECUTION ENGINE
# ==========================

def institutional_fvg_execution_engine_v12(df) -> Dict:


    return fvg_entry_validation_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_fvg_execution_v12(df) -> Dict:

    return institutional_fvg_execution_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-6
# Advanced Execution Intelligence Layer
# Institutional Order Block Execution Engine
# OB + Mitigation + Reaction Validation
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# ORDER BLOCK DETECTION
# ==========================

def detect_order_blocks_v12(df) -> List[Dict]:


    order_blocks = []



    if len(df) < 10:

        return order_blocks



    for i in range(
        2,
        len(df)-2
    ):


        current_open = float(
            df["open"].iloc[i]
        )


        current_close = float(
            df["close"].iloc[i]
        )


        next_close = float(
            df["close"].iloc[i+1]
        )


        next_high = float(
            df["high"].iloc[i+1]
        )


        next_low = float(
            df["low"].iloc[i+1]
        )



        # Bullish Order Block

        if (

            current_close < current_open

            and

            next_close > current_open

            and

            next_high > float(
                df["high"].iloc[i]
            )

        ):


            order_blocks.append({


                "type":

                    "BULLISH_OB",


                "high":

                    current_open,


                "low":

                    float(
                        df["low"].iloc[i]
                    )

            })



        # Bearish Order Block

        elif (

            current_close > current_open

            and

            next_close < current_open

            and

            next_low < float(
                df["low"].iloc[i]
            )

        ):


            order_blocks.append({


                "type":

                    "BEARISH_OB",


                "high":

                    float(
                        df["high"].iloc[i]
                    ),


                "low":

                    current_open

            })



    return order_blocks



# ==========================
# ORDER BLOCK QUALITY
# ==========================

def order_block_quality_v12(df) -> Dict:


    blocks = detect_order_blocks_v12(
        df
    )


    score = 0

    direction = "NONE"



    if blocks:


        latest = blocks[-1]



        if latest["type"] == "BULLISH_OB":

            direction = "BUY"



        elif latest["type"] == "BEARISH_OB":

            direction = "SELL"



        score = 70



        if detect_displacement(df):

            score += 20



    return {


        "direction":

            direction,


        "score":

            min(
                score,
                100
            ),


        "block":

            blocks[-1]
            if blocks

            else

            None

    }



# ==========================
# OB MITIGATION CHECK
# ==========================

def order_block_mitigation_v12(df) -> Dict:


    ob = order_block_quality_v12(
        df
    )


    if not ob["block"]:

        return {


            "mitigated":

                False,


            "confidence":

                0

        }



    price = float(
        df["close"].iloc[-1]
    )


    block = ob["block"]



    mitigated = (

        block["low"]

        <=

        price

        <=

        block["high"]

    )



    confidence = ob["score"]



    if mitigated:

        confidence += 15



    return {


        "mitigated":

            mitigated,


        "direction":

            ob["direction"],


        "confidence":

            min(
                confidence,
                100
            )

    }



# ==========================
# ORDER BLOCK EXECUTION ENGINE
# ==========================

def institutional_order_block_execution_engine_v12(df) -> Dict:


    result = order_block_mitigation_v12(
        df
    )


    return {


        "approved":

            result["confidence"] >= 80,


        "direction":

            result.get(
                "direction",
                "NONE"
            ),


        "confidence":

            result["confidence"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_order_block_execution_v12(df) -> Dict:

    return institutional_order_block_execution_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-7
# Advanced Execution Intelligence Layer
# Institutional Breaker Block Engine
# Failed OB + Structure Flip + Reversal Execution
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict, List


# ==========================
# BREAKER BLOCK DETECTOR
# ==========================

def detect_breaker_blocks_v12(df) -> List[Dict]:


    breakers = []



    if len(df) < 20:

        return breakers



    for i in range(
        5,
        len(df)-2
    ):


        high = float(
            df["high"].iloc[i]
        )


        low = float(
            df["low"].iloc[i]
        )


        close = float(
            df["close"].iloc[i]
        )


        next_close = float(
            df["close"].iloc[i+1]
        )



        # Bullish breaker

        if (

            next_close > high

            and

            close < float(
                df["open"].iloc[i]
            )

        ):


            breakers.append({


                "type":

                    "BULLISH_BREAKER",


                "high":

                    high,


                "low":

                    low

            })



        # Bearish breaker

        elif (

            next_close < low

            and

            close > float(
                df["open"].iloc[i]
            )

        ):


            breakers.append({


                "type":

                    "BEARISH_BREAKER",


                "high":

                    high,


                "low":

                    low

            })



    return breakers



# ==========================
# BREAKER VALIDATION
# ==========================

def breaker_validation_v12(df) -> Dict:


    breakers = detect_breaker_blocks_v12(
        df
    )


    direction = "NONE"

    score = 0



    if breakers:


        latest = breakers[-1]


        if latest["type"] == "BULLISH_BREAKER":

            direction = "BUY"



        elif latest["type"] == "BEARISH_BREAKER":

            direction = "SELL"



        score = 75



        if detect_displacement(df):

            score += 15



    return {


        "direction":

            direction,


        "score":

            min(
                score,
                100
            ),


        "breaker":

            breakers[-1]
            if breakers

            else

            None

    }



# ==========================
# BREAKER ENTRY FILTER
# ==========================

def breaker_entry_filter_v12(df) -> Dict:


    breaker = breaker_validation_v12(
        df
    )


    confirmation = get_final_confirmation_v12(
        df
    )



    confidence = breaker["score"]



    if (

        breaker["direction"]

        ==

        confirmation["direction"]

    ):

        confidence += 15



    return {


        "approved":

            confidence >= 80,


        "direction":

            breaker["direction"],


        "confidence":

            min(
                confidence,
                100
            )

    }



# ==========================
# BREAKER BLOCK ENGINE
# ==========================

def institutional_breaker_engine_v12(df) -> Dict:


    return breaker_entry_filter_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_breaker_block_v12(df) -> Dict:

    return institutional_breaker_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-8
# Advanced Execution Intelligence Layer
# Institutional Premium/Discount Execution Engine
# Dealing Range + Equilibrium Analysis
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# DEALING RANGE ENGINE
# ==========================

def dealing_range_v12(df) -> Dict:


    if len(df) < 50:

        return {

            "high":

                None,

            "low":

                None,

            "equilibrium":

                None

        }



    range_high = float(
        df["high"].tail(50).max()
    )


    range_low = float(
        df["low"].tail(50).min()
    )



    equilibrium = (

        range_high +

        range_low

    ) / 2



    return {


        "high":

            range_high,


        "low":

            range_low,


        "equilibrium":

            equilibrium

    }



# ==========================
# PREMIUM DISCOUNT CALCULATOR
# ==========================

def premium_discount_zone_v12(df) -> Dict:


    range_data = dealing_range_v12(
        df
    )


    if not range_data["high"]:

        return {

            "zone":

                "UNKNOWN",

            "score":

                0

        }



    price = float(
        df["close"].iloc[-1]
    )


    high = range_data["high"]

    low = range_data["low"]

    eq = range_data["equilibrium"]



    zone = "EQUILIBRIUM"

    score = 50



    if price < eq:


        zone = "DISCOUNT"

        score = 85



    elif price > eq:


        zone = "PREMIUM"

        score = 85



    return {


        "zone":

            zone,


        "price":

            price,


        "equilibrium":

            eq,


        "score":

            score

    }



# ==========================
# ENTRY LOCATION VALIDATOR
# ==========================

def premium_discount_validation_v12(df) -> Dict:


    zone = premium_discount_zone_v12(
        df
    )


    bias = get_global_bias_v12(
        df
    )



    confidence = zone["score"]



    direction = "NONE"



    if (

        zone["zone"]

        ==

        "DISCOUNT"

        and

        bias["bias"]

        ==

        "BUY"

    ):


        direction = "BUY"

        confidence += 15



    elif (

        zone["zone"]

        ==

        "PREMIUM"

        and

        bias["bias"]

        ==

        "SELL"

    ):


        direction = "SELL"

        confidence += 15



    return {


        "direction":

            direction,


        "confidence":

            min(
                confidence,
                100
            )

    }



# ==========================
# PREMIUM DISCOUNT ENGINE
# ==========================

def institutional_premium_discount_engine_v12(df) -> Dict:


    result = premium_discount_validation_v12(
        df
    )


    return {


        "approved":

            result["confidence"] >= 80,


        "direction":

            result["direction"],


        "confidence":

            result["confidence"]

    }



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_premium_discount_v12(df) -> Dict:

    return institutional_premium_discount_engine_v12(
        df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-9
# Advanced Execution Intelligence Layer
# Institutional Multi-Timeframe Alignment Engine
# HTF Bias + LTF Trigger Synchronization
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# TIMEFRAME ALIGNMENT ENGINE
# ==========================

def timeframe_alignment_v12(
        htf_df,
        ltf_df
) -> Dict:


    if len(htf_df) < 50 or len(ltf_df) < 50:

        return {


            "aligned":

                False,


            "direction":

                "NONE",


            "score":

                0

        }



    htf_direction = optimized_direction_v12(
        htf_df
    )


    ltf_direction = optimized_direction_v12(
        ltf_df
    )



    score = 0



    if (

        htf_direction

        ==

        ltf_direction

    ):

        score += 70



    else:

        score += 30



    direction = "NONE"



    if htf_direction == "BUY":


        direction = "BUY"



    elif htf_direction == "SELL":


        direction = "SELL"



    return {


        "htf":

            htf_direction,


        "ltf":

            ltf_direction,


        "direction":

            direction,


        "score":

            score,


        "aligned":

            score >= 70

    }



# ==========================
# MULTI TF CONFIRMATION
# ==========================

def mtf_confirmation_v12(
        htf_df,
        ltf_df
) -> Dict:


    alignment = timeframe_alignment_v12(
        htf_df,
        ltf_df
    )


    execution = get_precision_entry_v12(
        ltf_df
    )



    confidence = alignment["score"]



    if execution["approved"]:

        confidence += 20



    return {


        "direction":

            alignment["direction"],


        "confidence":

            min(
                confidence,
                100
            ),


        "approved":

            confidence >= 80

    }



# ==========================
# MTF EXECUTION ENGINE
# ==========================

def institutional_mtf_execution_engine_v12(
        htf_df,
        ltf_df
) -> Dict:


    return mtf_confirmation_v12(
        htf_df,
        ltf_df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_mtf_alignment_v12(
        htf_df,
        ltf_df
) -> Dict:

    return institutional_mtf_execution_engine_v12(
        htf_df,
        ltf_df
    )
    # ==========================
# STRUCTURE ENGINE V12
# PART 2H-10
# Advanced Execution Intelligence Layer
# Institutional Entry Confirmation Matrix
# BOS + MSS + OB + FVG + Liquidity Final Sync
# Production Ready
# Compatible with main.py
# ==========================

from typing import Dict


# ==========================
# ENTRY MATRIX CALCULATOR
# ==========================

def entry_confirmation_matrix_v12(df) -> Dict:


    components = {


        "structure":

            get_structure_memory_v12(df)
            ["score"],


        "order_block":

            get_order_block_execution_v12(df)
            ["confidence"],


        "fvg":

            get_fvg_execution_v12(df)
            ["confidence"],


        "liquidity":

            get_liquidity_entry_v12(df)
            ["quality"],


        "timing":

            get_trade_timing_v12(df)
            ["timing"]
            ["score"]

    }



    total = 0



    for value in components.values():

        total += value



    confidence = int(

        total /

        len(components)

    )



    return {


        "confidence":

            confidence,


        "components":

            components

    }



# ==========================
# MATRIX DIRECTION ENGINE
# ==========================

def entry_matrix_direction_v12(df) -> Dict:


    directions = [

        get_order_block_execution_v12(df)
        ["direction"],


        get_fvg_execution_v12(df)
        ["direction"],


        get_liquidity_entry_v12(df)
        ["direction"]

    ]



    buy = directions.count(
        "BUY"
    )


    sell = directions.count(
        "SELL"
    )



    direction = "NO_TRADE"



    if buy >= 2:

        direction = "BUY"



    elif sell >= 2:

        direction = "SELL"



    return {


        "direction":

            direction,


        "buy_votes":

            buy,


        "sell_votes":

            sell

    }



# ==========================
# FINAL MATRIX APPROVAL
# ==========================

def entry_matrix_approval_v12(df) -> Dict:


    score = entry_confirmation_matrix_v12(
        df
    )


    direction = entry_matrix_direction_v12(
        df
    )



    approved = (

        score["confidence"] >= 85

        and

        direction["direction"]

        !=

        "NO_TRADE"

    )



    return {


        "approved":

            approved,


        "direction":

            direction["direction"],


        "confidence":

            score["confidence"],


        "components":

            score["components"]

    }



# ==========================
# INSTITUTIONAL ENTRY MATRIX
# ==========================

def institutional_entry_matrix_engine_v12(df) -> Dict:


    return entry_matrix_approval_v12(
        df
    )



# ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def get_entry_matrix_v12(df) -> Dict:

    return institutional_entry_matrix_engine_v12(
        df
    )
