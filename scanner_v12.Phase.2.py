# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B1
# BASE SCANNER CORE + MARKET DATA VALIDATION
# Production Ready
# Compatible with main.py
# ==========================================================


from typing import Dict, Optional, List
import pandas as pd



# ==========================================================
# SCANNER MEMORY
# ==========================================================


V12_SCANNER_MEMORY = []



# ==========================================================
# SCANNER CONFIG
# ==========================================================


SCANNER_LOOKBACK = 50

MIN_CANDLES_REQUIRED = 50



# ==========================================================
# MARKET DATA VALIDATOR V12
# ==========================================================


def validate_market_data_v12(df) -> Dict:


    errors = []


    if df is None:

        errors.append(
            "DATA_EMPTY"
        )

        return {

            "valid": False,

            "errors": errors

        }



    if not isinstance(
        df,
        pd.DataFrame
    ):

        errors.append(
            "INVALID_FORMAT"
        )



    required_columns = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]



    for col in required_columns:

        if col not in df.columns:

            errors.append(
                f"MISSING_{col}"
            )



    if len(df) < MIN_CANDLES_REQUIRED:

        errors.append(
            "LOW_CANDLE_COUNT"
        )



    return {

        "valid":
            len(errors) == 0,

        "errors":
            errors,

        "candles":
            len(df)

    }



# ==========================================================
# SCANNER DATA NORMALIZER V12
# ==========================================================


def normalize_scanner_data_v12(df):


    if df is None:

        return None



    data = df.copy()



    for col in [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]:

        data[col] = (

            data[col]

            .astype(float)

        )



    return data



# ==========================================================
# PRICE STATE DETECTOR V12
# ==========================================================


def detect_price_state_v12(df) -> Dict:


    if len(df) < 10:

        return {

            "state":
                "UNKNOWN",

            "confidence":
                0

        }



    close = float(
        df["close"].iloc[-1]
    )


    high = float(
        df["high"].tail(
            SCANNER_LOOKBACK
        ).max()
    )


    low = float(
        df["low"].tail(
            SCANNER_LOOKBACK
        ).min()
    )



    position = (

        (close - low)

        /

        (high - low)

        * 100

        if high != low

        else 50

    )



    state = "MID"



    if position >= 70:

        state = "PREMIUM"



    elif position <= 30:

        state = "DISCOUNT"



    return {

        "state":

            state,


        "position":

            round(position,2),


        "high":

            high,


        "low":

            low

    }



# ==========================================================
# SCANNER BASE ENGINE V12
# ==========================================================


def scanner_base_engine_v12(df) -> Dict:


    validation = validate_market_data_v12(df)


    if not validation["valid"]:


        return {

            "approved":

                False,


            "signal":

                "NO_TRADE",


            "errors":

                validation["errors"]

        }



    data = normalize_scanner_data_v12(df)


    price_state = detect_price_state_v12(data)



    return {

        "approved":

            True,


        "signal":

            "WAIT",


        "price_state":

            price_state,


        "candles":

            len(data)

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_scanner_base_v12(df) -> Dict:

    return scanner_base_engine_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B1
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B2
# LIQUIDITY SCANNER + SWEEP DETECTION
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# LIQUIDITY CONFIG
# ==========================================================


LIQUIDITY_LOOKBACK = 30

LIQUIDITY_TOLERANCE = 0.002



# ==========================================================
# LIQUIDITY MEMORY
# ==========================================================


V12_LIQUIDITY_MEMORY = []



# ==========================================================
# EQUAL HIGH DETECTOR V12
# ==========================================================


def detect_equal_highs_v12(df) -> Dict:


    highs = []


    recent = df["high"].tail(
        LIQUIDITY_LOOKBACK
    )


    for i in range(
        len(recent)-1
    ):

        current = float(
            recent.iloc[i]
        )


        next_high = float(
            recent.iloc[i+1]
        )


        difference = abs(
            current - next_high
        )


        if (
            difference / current
            <= LIQUIDITY_TOLERANCE
        ):

            highs.append(current)



    return {

        "found":
            len(highs) > 0,

        "levels":
            highs[-5:]

    }



# ==========================================================
# EQUAL LOW DETECTOR V12
# ==========================================================


def detect_equal_lows_v12(df) -> Dict:


    lows = []


    recent = df["low"].tail(
        LIQUIDITY_LOOKBACK
    )


    for i in range(
        len(recent)-1
    ):

        current = float(
            recent.iloc[i]
        )


        next_low = float(
            recent.iloc[i+1]
        )


        difference = abs(
            current - next_low
        )


        if (
            difference / current
            <= LIQUIDITY_TOLERANCE
        ):

            lows.append(current)



    return {

        "found":
            len(lows) > 0,

        "levels":
            lows[-5:]

    }



# ==========================================================
# LIQUIDITY POOL DETECTOR V12
# ==========================================================


def detect_liquidity_pools_v12(df) -> Dict:


    equal_highs = detect_equal_highs_v12(df)

    equal_lows = detect_equal_lows_v12(df)



    pools = {


        "buy_side_liquidity":

            equal_highs["levels"],


        "sell_side_liquidity":

            equal_lows["levels"]

    }



    return {

        "found":

            bool(
                equal_highs["found"]
                or
                equal_lows["found"]
            ),


        "pools":

            pools

    }



# ==========================================================
# LIQUIDITY SWEEP DETECTOR V12
# ==========================================================


def detect_liquidity_sweep_v12(df) -> Dict:


    pools = detect_liquidity_pools_v12(df)


    if not pools["found"]:

        return {

            "sweep":
                False,

            "direction":
                "NONE",

            "level":
                None

        }



    current_high = float(
        df["high"].iloc[-1]
    )


    current_low = float(
        df["low"].iloc[-1]
    )



    # Buy side sweep

    for level in pools["pools"]["buy_side_liquidity"]:

        if current_high > level:

            return {

                "sweep":
                    True,

                "direction":
                    "SELL",

                "type":
                    "BUY_SIDE_LIQUIDITY_TAKEN",

                "level":
                    level

            }



    # Sell side sweep

    for level in pools["pools"]["sell_side_liquidity"]:

        if current_low < level:

            return {

                "sweep":
                    True,

                "direction":
                    "BUY",

                "type":
                    "SELL_SIDE_LIQUIDITY_TAKEN",

                "level":
                    level

            }



    return {

        "sweep":
            False,

        "direction":
            "NONE",

        "level":
            None

    }



# ==========================================================
# LIQUIDITY ENGINE V12
# ==========================================================


def liquidity_scanner_v12(df) -> Dict:


    pools = detect_liquidity_pools_v12(df)

    sweep = detect_liquidity_sweep_v12(df)



    V12_LIQUIDITY_MEMORY.append(
        sweep
    )


    if len(V12_LIQUIDITY_MEMORY) > 20:

        del V12_LIQUIDITY_MEMORY[:-20]



    return {

        "liquidity_found":

            pools["found"],


        "pools":

            pools["pools"],


        "sweep":

            sweep

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_liquidity_scanner_v12(df) -> Dict:

    return liquidity_scanner_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B2
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B3
# FVG + IMBALANCE DETECTION ENGINE
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# FVG CONFIG
# ==========================================================

FVG_LOOKBACK = 50



# ==========================================================
# FVG MEMORY
# ==========================================================

V12_FVG_MEMORY = []



# ==========================================================
# BULLISH FVG DETECTOR V12
# ==========================================================


def detect_bullish_fvg_v12(df) -> Dict:


    fvgs = []


    if len(df) < 3:

        return {

            "found":
                False,

            "zones":
                []

        }



    for i in range(
        2,
        len(df)
    ):


        candle_1_high = float(
            df["high"].iloc[i-2]
        )


        candle_3_low = float(
            df["low"].iloc[i]
        )


        candle_2_close = float(
            df["close"].iloc[i-1]
        )



        if candle_3_low > candle_1_high:


            fvgs.append({

                "direction":
                    "BUY",

                "index":
                    i,

                "high":
                    candle_3_low,

                "low":
                    candle_1_high,

                "mid":
                    (
                        candle_3_low
                        +
                        candle_1_high
                    ) / 2,

                "strength":
                    "NORMAL"

            })



    return {

        "found":
            len(fvgs) > 0,

        "zones":
            fvgs[-5:]

    }



# ==========================================================
# BEARISH FVG DETECTOR V12
# ==========================================================


def detect_bearish_fvg_v12(df) -> Dict:


    fvgs = []


    if len(df) < 3:

        return {

            "found":
                False,

            "zones":
                []

        }



    for i in range(
        2,
        len(df)
    ):


        candle_1_low = float(
            df["low"].iloc[i-2]
        )


        candle_3_high = float(
            df["high"].iloc[i]
        )


        if candle_3_high < candle_1_low:


            fvgs.append({

                "direction":
                    "SELL",

                "index":
                    i,

                "high":
                    candle_1_low,

                "low":
                    candle_3_high,

                "mid":
                    (
                        candle_1_low
                        +
                        candle_3_high
                    ) / 2,

                "strength":
                    "NORMAL"

            })



    return {

        "found":
            len(fvgs) > 0,

        "zones":
            fvgs[-5:]

    }



# ==========================================================
# FVG MASTER SCANNER V12
# ==========================================================


def detect_fvg_v12(df) -> Dict:


    bullish = detect_bullish_fvg_v12(df)

    bearish = detect_bearish_fvg_v12(df)



    zones = []


    zones.extend(
        bullish["zones"]
    )


    zones.extend(
        bearish["zones"]
    )



    return {

        "found":
            len(zones) > 0,


        "bullish":
            bullish,


        "bearish":
            bearish,


        "zones":
            zones[-10:]

    }



# ==========================================================
# FVG MITIGATION CHECK V12
# ==========================================================


def check_fvg_mitigation_v12(
    df,
    fvg_zone: Dict
) -> bool:


    current_price = float(
        df["close"].iloc[-1]
    )


    high = fvg_zone["high"]

    low = fvg_zone["low"]



    if low <= current_price <= high:

        return True



    return False



# ==========================================================
# FVG EXECUTION FILTER V12
# ==========================================================


def fvg_scanner_v12(df) -> Dict:


    fvg = detect_fvg_v12(df)


    active = []


    for zone in fvg["zones"]:


        if not check_fvg_mitigation_v12(
            df,
            zone
        ):

            active.append(zone)



    V12_FVG_MEMORY.append(
        fvg
    )


    if len(V12_FVG_MEMORY) > 20:

        del V12_FVG_MEMORY[:-20]



    return {

        "fvg_found":

            fvg["found"],


        "active_zones":

            active,


        "total_zones":

            len(fvg["zones"])


    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_fvg_scanner_v12(df) -> Dict:

    return fvg_scanner_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B3
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B4
# ORDER BLOCK SCANNER + VALIDATION ENGINE
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# ORDER BLOCK CONFIG
# ==========================================================

OB_LOOKBACK = 50



# ==========================================================
# ORDER BLOCK MEMORY
# ==========================================================

V12_OB_MEMORY = []



# ==========================================================
# BULLISH ORDER BLOCK DETECTOR V12
# ==========================================================


def detect_bullish_ob_v12(df) -> Dict:


    order_blocks = []


    if len(df) < 5:

        return {

            "found":
                False,

            "zones":
                []

        }



    for i in range(
        2,
        len(df)-1
    ):


        candle_open = float(
            df["open"].iloc[i]
        )

        candle_close = float(
            df["close"].iloc[i]
        )

        candle_high = float(
            df["high"].iloc[i]
        )

        candle_low = float(
            df["low"].iloc[i]
        )


        next_close = float(
            df["close"].iloc[i+1]
        )

        next_high = float(
            df["high"].iloc[i+1]
        )



        bearish_candle = (
            candle_close <
            candle_open
        )


        bullish_impulse = (
            next_close >
            candle_high
        )



        if (
            bearish_candle
            and
            bullish_impulse
        ):


            order_blocks.append({

                "direction":
                    "BUY",

                "index":
                    i,

                "high":
                    candle_high,

                "low":
                    candle_low,

                "open":
                    candle_open,

                "close":
                    candle_close,

                "strength":
                    "NORMAL"

            })



    return {

        "found":
            len(order_blocks) > 0,

        "zones":
            order_blocks[-5:]

    }



# ==========================================================
# BEARISH ORDER BLOCK DETECTOR V12
# ==========================================================


def detect_bearish_ob_v12(df) -> Dict:


    order_blocks = []


    if len(df) < 5:

        return {

            "found":
                False,

            "zones":
                []

        }



    for i in range(
        2,
        len(df)-1
    ):


        candle_open = float(
            df["open"].iloc[i]
        )


        candle_close = float(
            df["close"].iloc[i]
        )


        candle_high = float(
            df["high"].iloc[i]
        )


        candle_low = float(
            df["low"].iloc[i]
        )


        next_close = float(
            df["close"].iloc[i+1]
        )


        next_low = float(
            df["low"].iloc[i+1]
        )



        bullish_candle = (

            candle_close >
            candle_open

        )


        bearish_impulse = (

            next_close <
            candle_low

        )



        if (
            bullish_candle
            and
            bearish_impulse
        ):


            order_blocks.append({

                "direction":
                    "SELL",

                "index":
                    i,

                "high":
                    candle_high,

                "low":
                    candle_low,

                "open":
                    candle_open,

                "close":
                    candle_close,

                "strength":
                    "NORMAL"

            })



    return {

        "found":
            len(order_blocks) > 0,

        "zones":
            order_blocks[-5:]

    }



# ==========================================================
# ORDER BLOCK MASTER SCANNER V12
# ==========================================================


def detect_order_blocks_v12(df) -> Dict:


    bullish = detect_bullish_ob_v12(df)

    bearish = detect_bearish_ob_v12(df)



    zones = []


    zones.extend(
        bullish["zones"]
    )


    zones.extend(
        bearish["zones"]
    )



    return {

        "found":
            len(zones) > 0,


        "bullish":
            bullish,


        "bearish":
            bearish,


        "zones":
            zones[-10:]

    }



# ==========================================================
# ORDER BLOCK MITIGATION CHECK V12
# ==========================================================


def check_ob_mitigation_v12(
    df,
    zone: Dict
) -> bool:


    price = float(
        df["close"].iloc[-1]
    )


    if (
        zone["low"]
        <=
        price
        <=
        zone["high"]
    ):

        return True



    return False



# ==========================================================
# ORDER BLOCK SCANNER ENGINE V12
# ==========================================================


def order_block_scanner_v12(df) -> Dict:


    obs = detect_order_blocks_v12(df)


    active = []


    for zone in obs["zones"]:


        if not check_ob_mitigation_v12(
            df,
            zone
        ):

            active.append(zone)



    V12_OB_MEMORY.append(
        obs
    )


    if len(V12_OB_MEMORY) > 20:

        del V12_OB_MEMORY[:-20]



    return {

        "ob_found":

            obs["found"],


        "active_blocks":

            active,


        "total_blocks":

            len(obs["zones"])

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_order_block_scanner_v12(df) -> Dict:

    return order_block_scanner_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B4
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B5
# MARKET STRUCTURE + TREND SCANNER ENGINE
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# TREND CONFIG
# ==========================================================

TREND_LOOKBACK = 50


# ==========================================================
# TREND MEMORY
# ==========================================================

V12_TREND_MEMORY = []



# ==========================================================
# HIGHER HIGH / LOWER LOW DETECTOR V12
# ==========================================================


def detect_market_structure_v12(df) -> Dict:


    if len(df) < 10:

        return {

            "trend":
                "UNKNOWN",

            "confidence":
                0

        }



    highs = df["high"].tail(
        TREND_LOOKBACK
    )

    lows = df["low"].tail(
        TREND_LOOKBACK
    )



    recent_high = float(
        highs.iloc[-1]
    )


    previous_high = float(
        highs.iloc[-5]
    )


    recent_low = float(
        lows.iloc[-1]
    )


    previous_low = float(
        lows.iloc[-5]
    )



    trend = "RANGE"

    confidence = 50



    if (
        recent_high > previous_high
        and
        recent_low > previous_low
    ):

        trend = "BULLISH"
        confidence = 75



    elif (
        recent_high < previous_high
        and
        recent_low < previous_low
    ):

        trend = "BEARISH"
        confidence = 75



    return {

        "trend":
            trend,

        "confidence":
            confidence,

        "recent_high":
            recent_high,

        "recent_low":
            recent_low

    }



# ==========================================================
# MOMENTUM SCANNER V12
# ==========================================================


def detect_momentum_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "momentum":
                "UNKNOWN",

            "strength":
                0

        }



    close_now = float(
        df["close"].iloc[-1]
    )


    close_old = float(
        df["close"].iloc[-20]
    )



    change = (

        (close_now - close_old)

        /

        close_old

    ) * 100



    momentum = "NEUTRAL"

    strength = abs(change)



    if change > 1:

        momentum = "BULLISH"



    elif change < -1:

        momentum = "BEARISH"



    return {

        "momentum":

            momentum,


        "strength":

            round(strength,2),


        "change":

            round(change,2)

    }



# ==========================================================
# VOLATILITY SCANNER V12
# ==========================================================


def detect_volatility_v12(df) -> Dict:


    if len(df) < 20:

        return {

            "volatility":
                "UNKNOWN",

            "score":
                0

        }



    ranges = (

        df["high"]

        -

        df["low"]

    ).tail(20)



    avg_range = float(
        ranges.mean()
    )



    current_range = float(
        ranges.iloc[-1]
    )



    volatility = "NORMAL"


    score = 50



    if current_range > avg_range * 1.5:

        volatility = "HIGH"

        score = 80



    elif current_range < avg_range * 0.5:

        volatility = "LOW"

        score = 30



    return {

        "volatility":

            volatility,


        "score":

            score,


        "average_range":

            avg_range

    }



# ==========================================================
# MARKET CONDITION ENGINE V12
# ==========================================================


def market_condition_scanner_v12(df) -> Dict:


    structure = detect_market_structure_v12(df)

    momentum = detect_momentum_v12(df)

    volatility = detect_volatility_v12(df)



    condition = "RANGE"


    confidence = 50



    if (
        structure["trend"]
        ==
        "BULLISH"

        and

        momentum["momentum"]
        ==
        "BULLISH"

    ):

        condition = "UPTREND"

        confidence = 80



    elif (
        structure["trend"]
        ==
        "BEARISH"

        and

        momentum["momentum"]
        ==
        "BEARISH"

    ):

        condition = "DOWNTREND"

        confidence = 80



    return {

        "condition":

            condition,


        "confidence":

            confidence,


        "structure":

            structure,


        "momentum":

            momentum,


        "volatility":

            volatility

    }



# ==========================================================
# MARKET SCANNER MASTER V12
# ==========================================================


def market_scanner_v12(df) -> Dict:


    result = market_condition_scanner_v12(df)



    V12_TREND_MEMORY.append(
        result
    )



    if len(V12_TREND_MEMORY) > 20:

        del V12_TREND_MEMORY[:-20]



    return result



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_market_scanner_v12(df) -> Dict:

    return market_scanner_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B5
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B6
# SCANNER CONFLUENCE FUSION ENGINE
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# CONFIDENCE MEMORY
# ==========================================================

V12_SCANNER_CONFIDENCE_MEMORY = []



# ==========================================================
# SCANNER COMPONENT WEIGHT
# ==========================================================

SCANNER_WEIGHTS = {

    "market":
        20,

    "liquidity":
        25,

    "fvg":
        20,

    "order_block":
        20,

    "trend":
        15

}



# ==========================================================
# LIQUIDITY SCORE ENGINE
# ==========================================================


def liquidity_score_v12(df) -> Dict:


    liquidity = liquidity_scanner_v12(df)


    score = 0

    direction = "NONE"



    if liquidity["liquidity_found"]:

        score += 30



    sweep = liquidity["sweep"]



    if sweep["sweep"]:

        score += 40

        direction = sweep["direction"]



    return {

        "score":
            min(score,100),

        "direction":
            direction,

        "data":
            liquidity

    }



# ==========================================================
# FVG SCORE ENGINE
# ==========================================================


def fvg_score_v12(df) -> Dict:


    fvg = fvg_scanner_v12(df)


    score = 0

    direction = "NONE"



    if fvg["fvg_found"]:

        score += 40



        if fvg["active_zones"]:

            score += 30


            direction = (
                fvg["active_zones"][-1]
                ["direction"]
            )



    return {

        "score":
            min(score,100),

        "direction":
            direction,

        "data":
            fvg

    }



# ==========================================================
# ORDER BLOCK SCORE ENGINE
# ==========================================================


def order_block_score_v12(df) -> Dict:


    ob = order_block_scanner_v12(df)


    score = 0

    direction = "NONE"



    if ob["ob_found"]:

        score += 50



        if ob["active_blocks"]:

            score += 30


            direction = (
                ob["active_blocks"][-1]
                ["direction"]
            )



    return {

        "score":
            min(score,100),

        "direction":
            direction,

        "data":
            ob

    }



# ==========================================================
# MARKET SCORE ENGINE
# ==========================================================


def market_score_v12(df) -> Dict:


    market = market_scanner_v12(df)


    score = market["confidence"]


    direction = "NONE"



    if market["condition"] == "UPTREND":

        direction = "BUY"



    elif market["condition"] == "DOWNTREND":

        direction = "SELL"



    return {

        "score":
            score,

        "direction":
            direction,

        "data":
            market

    }



# ==========================================================
# TREND CONFIRMATION ENGINE
# ==========================================================


def trend_confirmation_v12(df) -> Dict:


    market = detect_market_structure_v12(df)


    trend = market["trend"]


    direction = "NONE"

    score = 0



    if trend == "BULLISH":

        direction = "BUY"

        score = 70



    elif trend == "BEARISH":

        direction = "SELL"

        score = 70



    return {

        "direction":
            direction,

        "score":
            score

    }



# ==========================================================
# MASTER SCANNER FUSION ENGINE
# ==========================================================


def scanner_confluence_engine_v12(df) -> Dict:


    market = market_score_v12(df)

    liquidity = liquidity_score_v12(df)

    fvg = fvg_score_v12(df)

    ob = order_block_score_v12(df)

    trend = trend_confirmation_v12(df)



    buy_score = 0

    sell_score = 0



    components = [

        market,

        liquidity,

        fvg,

        ob,

        trend

    ]



    for item in components:


        if item["direction"] == "BUY":

            buy_score += item["score"]


        elif item["direction"] == "SELL":

            sell_score += item["score"]



    final_signal = "WAIT"

    confidence = max(
        buy_score,
        sell_score
    )



    if buy_score > sell_score:

        final_signal = "BUY"



    elif sell_score > buy_score:

        final_signal = "SELL"



    result = {

        "signal":

            final_signal,


        "buy_score":

            buy_score,


        "sell_score":

            sell_score,


        "confidence":

            min(
                confidence,
                100
            ),


        "components":

            {

                "market":
                    market,

                "liquidity":
                    liquidity,

                "fvg":
                    fvg,

                "order_block":
                    ob,

                "trend":
                    trend

            }

    }



    V12_SCANNER_CONFIDENCE_MEMORY.append(
        result
    )



    if len(V12_SCANNER_CONFIDENCE_MEMORY) > 20:

        del V12_SCANNER_CONFIDENCE_MEMORY[:-20]



    return result



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_scanner_confluence_v12(df) -> Dict:

    return scanner_confluence_engine_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B6
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B7
# FINAL SCANNER APPROVAL GATE
# NO TRADE FILTER + SIGNAL OUTPUT
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# FINAL SCANNER MEMORY
# ==========================================================

V12_FINAL_SCANNER_MEMORY = []



# ==========================================================
# SCANNER THRESHOLD CONFIG
# ==========================================================

MIN_SCANNER_CONFIDENCE = 70

MIN_SIGNAL_SCORE = 100



# ==========================================================
# SIGNAL DIRECTION VALIDATOR V12
# ==========================================================


def validate_scanner_direction_v12(
    scan: Dict
) -> Dict:


    signal = scan.get(
        "signal",
        "WAIT"
    )


    buy = scan.get(
        "buy_score",
        0
    )


    sell = scan.get(
        "sell_score",
        0
    )


    approved = False


    if signal == "BUY":

        approved = buy > sell



    elif signal == "SELL":

        approved = sell > buy



    return {

        "approved":

            approved,

        "signal":

            signal,

        "buy_score":

            buy,

        "sell_score":

            sell

    }



# ==========================================================
# SCANNER RISK FILTER V12
# ==========================================================


def scanner_risk_filter_v12(
    df,
    scan: Dict
) -> Dict:


    market = scan["components"]["market"]

    volatility = (
        market["data"]
        ["volatility"]
    )


    blocked = False

    reason = "OK"



    if volatility["volatility"] == "HIGH":

        blocked = True

        reason = "HIGH_VOLATILITY"



    if scan["confidence"] < MIN_SCANNER_CONFIDENCE:

        blocked = True

        reason = "LOW_CONFIDENCE"



    return {

        "blocked":

            blocked,

        "reason":

            reason

    }



# ==========================================================
# SCANNER FINAL DECISION ENGINE V12
# ==========================================================


def scanner_final_decision_v12(df) -> Dict:


    scan = scanner_confluence_engine_v12(df)


    direction = validate_scanner_direction_v12(
        scan
    )


    risk = scanner_risk_filter_v12(
        df,
        scan
    )


    approved = False

    signal = "NO_TRADE"



    if (
        direction["approved"]

        and

        not risk["blocked"]

        and

        scan["confidence"]
        >=
        MIN_SCANNER_CONFIDENCE
    ):

        approved = True

        signal = scan["signal"]



    result = {

        "approved":

            approved,


        "signal":

            signal,


        "confidence":

            scan["confidence"],


        "buy_score":

            scan["buy_score"],


        "sell_score":

            scan["sell_score"],


        "risk":

            risk,


        "components":

            scan["components"]

    }



    V12_FINAL_SCANNER_MEMORY.append(
        result
    )



    if len(V12_FINAL_SCANNER_MEMORY) > 20:

        del V12_FINAL_SCANNER_MEMORY[:-20]



    return result



# ==========================================================
# SCANNER STATUS ENGINE V12
# ==========================================================


def scanner_status_v12(df) -> Dict:


    result = scanner_final_decision_v12(df)


    status = "WAIT"


    if result["approved"]:

        status = "APPROVED"



    return {

        "status":

            status,


        "signal":

            result["signal"],


        "confidence":

            result["confidence"],


        "approved":

            result["approved"]

    }



# ==========================================================
# MAIN.PY COMPATIBILITY
# ==========================================================


def get_scanner_final_v12(df) -> Dict:

    return scanner_final_decision_v12(df)



def get_scanner_status_v12(df) -> Dict:

    return scanner_status_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B7
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B8
# FINAL EXPORT + TELEGRAM ALERT FORMATTER
# Production Ready
# Compatible with main.py
# ==========================================================


# ==========================================================
# SCANNER REPORT FORMATTER V12
# ==========================================================


def scanner_report_formatter_v12(df) -> Dict:


    result = scanner_final_decision_v12(df)


    signal = result["signal"]


    status = (
        "APPROVED"
        if result["approved"]
        else
        "WAIT"
    )


    return {

        "title":
            "ICT V12 SCANNER",


        "signal":
            signal,


        "status":
            status,


        "confidence":
            result["confidence"],


        "message":

            (
                f"ICT V12 SCANNER | "
                f"SIGNAL: {signal} | "
                f"CONFIDENCE: {result['confidence']} | "
                f"STATUS: {status}"
            )

    }



# ==========================================================
# SCANNER HEALTH MONITOR V12
# ==========================================================


def scanner_health_monitor_v12(df) -> Dict:


    result = scanner_final_decision_v12(df)


    confidence = result["confidence"]


    health = "BAD"


    if confidence >= 80:

        health = "EXCELLENT"


    elif confidence >= 60:

        health = "GOOD"


    elif confidence >= 40:

        health = "AVERAGE"



    return {

        "health":

            health,


        "confidence":

            confidence,


        "approved":

            result["approved"],


        "signal":

            result["signal"]

    }



# ==========================================================
# SCANNER COMPONENT SUMMARY V12
# ==========================================================


def scanner_component_summary_v12(df) -> Dict:


    result = scanner_final_decision_v12(df)


    components = result["components"]


    return {

        "market":

            components["market"]["data"],


        "liquidity":

            components["liquidity"]["data"],


        "fvg":

            components["fvg"]["data"],


        "order_block":

            components["order_block"]["data"],


        "trend":

            components["trend"]

    }



# ==========================================================
# SCANNER MASTER EXPORT V12
# ==========================================================


def scanner_export_v12(df) -> Dict:


    final = scanner_final_decision_v12(df)

    report = scanner_report_formatter_v12(df)

    health = scanner_health_monitor_v12(df)


    return {

        "engine":

            "ICT_SCANNER_V12",


        "status":

            "ONLINE",


        "signal":

            final["signal"],


        "approved":

            final["approved"],


        "confidence":

            final["confidence"],


        "buy_score":

            final["buy_score"],


        "sell_score":

            final["sell_score"],


        "risk":

            final["risk"],


        "health":

            health,


        "alert":

            report,


        "components":

            scanner_component_summary_v12(df)

    }



# ==========================================================
# SAFE SCANNER CALLER V12
# ==========================================================


def safe_scanner_engine_v12(df) -> Dict:


    try:


        result = scanner_export_v12(df)


        if not isinstance(
            result,
            dict
        ):

            return {

                "signal":
                    "NO_TRADE",

                "approved":
                    False,

                "confidence":
                    0,

                "error":
                    "INVALID_SCANNER_RESPONSE"

            }



        return result



    except Exception as e:


        return {

            "signal":
                "NO_TRADE",

            "approved":
                False,

            "confidence":
                0,

            "error":
                str(e)

        }



# ==========================================================
# FINAL SCANNER OUTPUT V12
# ==========================================================


def final_scanner_output_v12(df) -> Dict:


    result = safe_scanner_engine_v12(df)


    return {

        "engine":

            "ICT_V12_SCANNER_FINAL",


        "signal":

            result.get(
                "signal",
                "NO_TRADE"
            ),


        "approved":

            result.get(
                "approved",
                False
            ),


        "confidence":

            result.get(
                "confidence",
                0
            ),


        "status":

            result.get(
                "health",
                {}
            ),


        "alert":

            result.get(
                "alert",
                {}
            )

    }



# ==========================================================
# MAIN.PY COMPATIBILITY FINAL
# ==========================================================


def get_scanner_report_v12(df) -> Dict:

    return scanner_export_v12(df)



def run_scanner_v12(df) -> Dict:

    return final_scanner_output_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B8
# ==========================================================
# ==========================================================
# SCANNER ENGINE V12
# PHASE 2 - PART B9
# FINAL CLEANUP + EXPORT MAP + DUPLICATE GUARD
# Production Ready
# Compatible with main.py
# ==========================================================



# ==========================================================
# SCANNER DUPLICATE GUARD V12
# ==========================================================


def scanner_duplicate_guard_v12() -> Dict:


    required_functions = [

        "validate_market_data_v12",

        "scanner_base_engine_v12",

        "liquidity_scanner_v12",

        "fvg_scanner_v12",

        "order_block_scanner_v12",

        "market_scanner_v12",

        "scanner_confluence_engine_v12",

        "scanner_final_decision_v12",

        "run_scanner_v12"

    ]


    missing = []


    current_globals = globals()



    for func in required_functions:


        if func not in current_globals:

            missing.append(func)



    return {

        "valid":

            len(missing) == 0,


        "missing":

            missing,


        "checked":

            len(required_functions)

    }



# ==========================================================
# SCANNER ENGINE STATUS V12
# ==========================================================


def scanner_engine_status_v12(df) -> Dict:


    guard = scanner_duplicate_guard_v12()



    if not guard["valid"]:


        return {

            "engine":

                "ICT_SCANNER_V12",


            "status":

                "ERROR",


            "missing":

                guard["missing"]

        }



    output = final_scanner_output_v12(df)



    return {

        "engine":

            "ICT_SCANNER_V12",


        "status":

            "RUNNING",


        "signal":

            output["signal"],


        "approved":

            output["approved"],


        "confidence":

            output["confidence"]

    }



# ==========================================================
# SAFE MAIN.PY ENTRY V12
# ==========================================================


def get_v12_scanner_signal(df) -> Dict:


    status = scanner_engine_status_v12(df)



    if status["status"] != "RUNNING":


        return {

            "signal":

                "NO_TRADE",


            "confidence":

                0,


            "approved":

                False,


            "error":

                status

        }



    return {

        "signal":

            status["signal"],


        "confidence":

            status["confidence"],


        "approved":

            status["approved"],


        "engine":

            "ICT_SCANNER_V12"

    }



# ==========================================================
# SCANNER FINAL API CONTROLLER V12
# ==========================================================


def scanner_api_controller_v12(df) -> Dict:


    final = final_scanner_output_v12(df)

    health = scanner_health_monitor_v12(df)

    report = scanner_report_formatter_v12(df)



    return {

        "engine":

            "ICT_SCANNER_V12",


        "status":

            "ONLINE",


        "signal":

            final["signal"],


        "approved":

            final["approved"],


        "confidence":

            final["confidence"],


        "health":

            health,


        "alert":

            report

    }



# ==========================================================
# SCANNER EXPORT MAP V12
# ==========================================================


SCANNER_V12_EXPORTS = {


    "base":

        get_scanner_base_v12,


    "liquidity":

        get_liquidity_scanner_v12,


    "fvg":

        get_fvg_scanner_v12,


    "order_block":

        get_order_block_scanner_v12,


    "market":

        get_market_scanner_v12,


    "confluence":

        get_scanner_confluence_v12,


    "final":

        get_scanner_final_v12,


    "signal":

        get_v12_scanner_signal,


    "run":

        run_scanner_v12

}



# ==========================================================
# FINAL SCANNER RUNNER V12
# ==========================================================


def execute_scanner_v12(df) -> Dict:


    try:


        result = scanner_api_controller_v12(df)


        return result



    except Exception as e:


        return {


            "engine":

                "ICT_SCANNER_V12",


            "status":

                "ERROR",


            "signal":

                "NO_TRADE",


            "approved":

                False,


            "confidence":

                0,


            "error":

                str(e)

        }



# ==========================================================
# MAIN.PY FINAL COMPATIBILITY
# ==========================================================


def get_final_scanner_v12(df) -> Dict:

    return execute_scanner_v12(df)



# ==========================================================
# END SCANNER V12 PHASE 2 PART B9
# ==========================================================
