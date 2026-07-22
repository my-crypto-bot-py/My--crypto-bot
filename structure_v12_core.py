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

    return structure_engine_v12_final_router(df)
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


    score = c_series_modu





