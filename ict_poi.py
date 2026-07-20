import pandas as pd
import numpy as np


# ==========================
# ICT POI ENGINE V5
# ==========================


# ==========================
# SETTINGS
# ==========================

LOOKBACK = 20

MIN_IMPULSE = 1.5

ZONE_BUFFER = 0.001



# ==========================
# POI STATE
# ==========================

poi_state = {

    "last_poi": None,

    "bullish_poi": [],

    "bearish_poi": []

}



# ==========================
# PREPARE DATA
# ==========================

def prepare_poi_data(df):

    df = df.copy()

    cols = [

        "open",

        "high",

        "low",

        "close",

        "volume"

    ]

    for col in cols:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )

    df.dropna(inplace=True)

    df.reset_index(

        drop=True,

        inplace=True

    )

    return df



# ==========================
# CREATE POI OBJECT
# ==========================

def create_poi(

    zone_type,

    high,

    low,

    index

):

    return {

        "type": zone_type,

        "high": high,

        "low": low,

        "index": index

    }
    # ==========================
# IMPULSE CANDLE CHECK
# ==========================

def is_impulse_candle(

    candle

):

    body = abs(

        candle["close"]

        -

        candle["open"]

    )


    total = (

        candle["high"]

        -

        candle["low"]

    )


    if total == 0:

        return False


    return (

        body / total

    ) >= 0.60



# ==========================
# BULLISH POI
# ==========================

def detect_bullish_poi(

    df

):

    pois = []


    for i in range(

        LOOKBACK,

        len(df)

    ):

        candle = df.iloc[i]


        if (

            candle["close"]

            >

            candle["open"]

            and

            is_impulse_candle(

                candle

            )

        ):

            pois.append(

                create_poi(

                    "BULLISH",

                    candle["high"],

                    candle["low"],

                    i

                )

            )


    return pois



# ==========================
# BEARISH POI
# ==========================

def detect_bearish_poi(

    df

):

    pois = []


    for i in range(

        LOOKBACK,

        len(df)

    ):

        candle = df.iloc[i]


        if (

            candle["close"]

            <

            candle["open"]

            and

            is_impulse_candle(

                candle

            )

        ):

            pois.append(

                create_poi(

                    "BEARISH",

                    candle["high"],

                    candle["low"],

                    i

                )

            )


    return pois
    # ==========================
# GET LATEST POI
# ==========================

def get_latest_poi(

    pois

):

    if not pois:

        return None


    return pois[-1]



# ==========================
# UPDATE POI STATE
# ==========================

def update_poi_state(

    bullish,

    bearish

):

    poi_state["bullish_poi"] = bullish

    poi_state["bearish_poi"] = bearish


    latest_bull = get_latest_poi(

        bullish

    )

    latest_bear = get_latest_poi(

        bearish

    )


    if latest_bull and latest_bear:

        if latest_bull["index"] > latest_bear["index"]:

            poi_state["last_poi"] = latest_bull

        else:

            poi_state["last_poi"] = latest_bear

    elif latest_bull:

        poi_state["last_poi"] = latest_bull

    elif latest_bear:

        poi_state["last_poi"] = latest_bear

    else:

        poi_state["last_poi"] = None


    return poi_state



# ==========================
# ACTIVE POI
# ==========================

def get_active_poi():

    return poi_state.get(

        "last_poi"

    )
    # ==========================
# POI VALIDATION
# ==========================

def validate_poi(

    poi

):

    if poi is None:

        return False


    if poi["high"] <= poi["low"]:

        return False


    return True



# ==========================
# PREMIUM / DISCOUNT CHECK
# ==========================

def premium_discount_zone(

    current_price,

    swing_high,

    swing_low

):

    if swing_high <= swing_low:

        return "UNKNOWN"


    midpoint = (

        swing_high

        +

        swing_low

    ) / 2


    if current_price > midpoint:

        return "PREMIUM"


    if current_price < midpoint:

        return "DISCOUNT"


    return "EQUILIBRIUM"



# ==========================
# POI STRENGTH
# ==========================

def poi_strength(

    poi

):

    if not validate_poi(

        poi

    ):

        return 0


    zone_size = (

        poi["high"]

        -

        poi["low"]

    )


    if zone_size <= 0:

        return 0


    if zone_size < ZONE_BUFFER:

        return 90


    if zone_size < (

        ZONE_BUFFER * 2

    ):

        return 75


    return 60
    # ==========================
# POI TOUCH DETECTION
# ==========================

def is_poi_touched(

    current_price,

    poi

):

    if poi is None:

        return False


    return (

        poi["low"]

        <=

        current_price

        <=

        poi["high"]

    )



# ==========================
# ENTRY ZONE CONFIRMATION
# ==========================

def confirm_entry_zone(

    current_price,

    poi

):

    if not validate_poi(

        poi

    ):

        return False


    return is_poi_touched(

        current_price,

        poi

    )



# ==========================
# ACTIVE POI FILTER
# ==========================

def active_poi_filter(

    current_price

):

    poi = get_active_poi()


    if poi is None:

        return None


    if confirm_entry_zone(

        current_price,

        poi

    ):

        return poi


    return None
    # ==========================
# POI DIRECTION
# ==========================

def poi_direction(

    poi

):

    if poi is None:

        return "NEUTRAL"


    if poi["type"] == "BULLISH":

        return "BUY"


    if poi["type"] == "BEARISH":

        return "SELL"


    return "NEUTRAL"



# ==========================
# POI SIGNAL
# ==========================

def poi_signal(

    current_price

):

    poi = active_poi_filter(

        current_price

    )


    if poi is None:

        return {

            "signal": False,

            "direction": "NEUTRAL",

            "poi": None

        }


    return {

        "signal": True,

        "direction": poi_direction(

            poi

        ),

        "poi": poi

    }



# ==========================
# FINAL POI ANALYSIS
# ==========================

def analyze_poi(

    current_price

):

    result = poi_signal(

        current_price

    )


    if not result["signal"]:

        return {

            "active": False,

            "direction": "NEUTRAL",

            "strength": 0,

            "poi": None

        }


    strength = poi_strength(

        result["poi"]

    )


    return {

        "active": True,

        "direction": result["direction"],

        "strength": strength,

        "poi": result["poi"]

    }
    # ==========================
# SCANNER INTEGRATION
# ==========================

def poi_for_scanner(

    current_price

):

    result = analyze_poi(

        current_price

    )


    return {

        "active":

        result["active"],

        "direction":

        result["direction"],

        "strength":

        result["strength"]

    }



# ==========================
# CONFIDENCE SCORE
# ==========================

def poi_score(

    current_price

):

    result = analyze_poi(

        current_price

    )


    if not result["active"]:

        return 0


    strength = result["strength"]


    if strength >= 90:

        return 15


    if strength >= 75:

        return 10


    if strength >= 60:

        return 5


    return 0



# ==========================
# POI SUMMARY
# ==========================

def poi_summary(

    current_price

):

    analysis = analyze_poi(

        current_price

    )


    return {

        "active":

        analysis["active"],

        "direction":

        analysis["direction"],

        "score":

        poi_score(

            current_price

        ),

        "strength":

        analysis["strength"]

    }
    # ==========================
# DEBUG PANEL
# ==========================

def debug_poi(

    current_price

):

    report = analyze_poi(

        current_price

    )


    print("\n========== ICT POI V5 ==========")

    print(

        "Active :",

        report["active"]

    )

    print(

        "Direction :",

        report["direction"]

    )

    print(

        "Strength :",

        report["strength"]

    )

    print(

        "POI :",

        report["poi"]

    )

    print(

        "================================\n"

    )


    return report



# ==========================
# REPORT
# ==========================

def poi_report(

    current_price

):

    report = analyze_poi(

        current_price

    )


    return {

        "active":

        report["active"],

        "direction":

        report["direction"],

        "strength":

        report["strength"],

        "score":

        poi_score(

            current_price

        )

    }



# ==========================
# RESET
# ==========================

def reset_poi():

    poi_state["last_poi"] = None

    poi_state["bullish_poi"] = []

    poi_state["bearish_poi"] = []


    return True
    # ==========================
# SCANNER COMPATIBILITY
# ==========================

def scanner_poi_engine(

    current_price

):

    summary = poi_summary(

        current_price

    )


    return {

        "active":

        summary["active"],

        "direction":

        summary["direction"],

        "score":

        summary["score"],

        "strength":

        summary["strength"]

    }



# ==========================
# MAIN ENGINE
# ==========================

def ict_poi_engine(

    current_price

):

    report = poi_report(

        current_price

    )


    return {

        "poi":

        report,

        "ready":

        report["active"]

    }



# ==========================
# TEST ENGINE
# ==========================

def test_poi(

    current_price

):

    return ict_poi_engine(

        current_price

    )
    # ==========================
# MAIN.PY COMPATIBILITY
# ==========================

def ict_poi_engine_v5(

    current_price

):

    result = ict_poi_engine(

        current_price

    )


    return {

        "active":

        result["poi"]["active"],

        "direction":

        result["poi"]["direction"],

        "score":

        result["poi"]["score"],

        "strength":

        result["poi"]["strength"]

    }



# ==========================
# FINAL POI CHECK
# ==========================

def final_poi_check(

    current_price

):

    result = ict_poi_engine_v5(

        current_price

    )


    return (

        result["active"]

    )



# ==========================
# EXPORTS
# ==========================

__all__ = [

    "prepare_poi_data",

    "detect_bullish_poi",

    "detect_bearish_poi",

    "get_active_poi",

    "validate_poi",

    "premium_discount_zone",

    "poi_strength",

    "active_poi_filter",

    "poi_signal",

    "analyze_poi",

    "poi_score",

    "poi_summary",

    "scanner_poi_engine",

    "ict_poi_engine",

    "ict_poi_engine_v5",

    "final_poi_check",

    "poi_report",

    "debug_poi",

    "reset_poi"

]
