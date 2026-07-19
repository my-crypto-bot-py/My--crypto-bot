# ==========================
# ICT LIQUIDITY ENGINE V2
# ==========================


# ==========================
# SWING LIQUIDITY
# ==========================

def find_swing_liquidity(
    df,
    lookback=50
):

    if len(df) < lookback:
        return None


    data = df.tail(
        lookback
    )


    high = float(
        data["high"].max()
    )

    low = float(
        data["low"].min()
    )


    return {

        "BSL": high,

        "SSL": low

    }



# ==========================
# EQUAL HIGH / LOW
# ==========================

def detect_equal_levels(
    df,
    tolerance=0.0015
):


    if len(df) < 20:

        return None



    highs = df["high"].tail(20)

    lows = df["low"].tail(20)



    recent_high = float(
        highs.max()
    )

    previous_high = float(
        highs.iloc[:-5].max()
    )



    recent_low = float(
        lows.min()
    )

    previous_low = float(
        lows.iloc[:-5].min()
    )



    result = {}



    # Equal High = Buy Side Liquidity

    if abs(
        recent_high - previous_high
    ) / previous_high <= tolerance:


        result["equal_high"] = {

            "type":
            "Equal High",

            "direction":
            "SELL",

            "level":
            recent_high

        }



    # Equal Low = Sell Side Liquidity

    if abs(
        recent_low - previous_low
    ) / previous_low <= tolerance:


        result["equal_low"] = {

            "type":
            "Equal Low",

            "direction":
            "BUY",

            "level":
            recent_low

        }



    return result if result else None




# ==========================
# LIQUIDITY SWEEP
# ==========================

def detect_liquidity_sweep(
    df,
    lookback=20
):


    if len(df) < lookback:

        return None



    previous = df.iloc[
        -lookback:-1
    ]

    current = df.iloc[-1]



    high = float(
        previous["high"].max()
    )


    low = float(
        previous["low"].min()
    )



    close = float(
        current["close"]
    )


    candle_high = float(
        current["high"]
    )


    candle_low = float(
        current["low"]
    )



    # BSL taken -> Sell setup

    if (

        candle_high > high

        and

        close < high

    ):

        return {

            "direction":
            "SELL",

            "type":
            "Buy Side Liquidity Sweep",

            "level":
            high

        }



    # SSL taken -> Buy setup

    if (

        candle_low < low

        and

        close > low

    ):

        return {

            "direction":
            "BUY",

            "type":
            "Sell Side Liquidity Sweep",

            "level":
            low

        }



    return None




# ==========================
# LIQUIDITY GRAB
# ==========================

def detect_liquidity_grab(
    df
):

    if len(df) < 10:

        return None



    candle = df.iloc[-1]



    body = abs(

        float(candle["close"])

        -

        float(candle["open"])

    )


    upper_wick = (

        float(candle["high"])

        -

        max(

            float(candle["open"]),

            float(candle["close"])

        )

    )


    lower_wick = (

        min(

            float(candle["open"]),

            float(candle["close"])

        )

        -

        float(candle["low"])

    )



    if upper_wick > body * 2:


        return {

            "direction":
            "SELL",

            "type":
            "Bearish Liquidity Grab"

        }



    if lower_wick > body * 2:


        return {

            "direction":
            "BUY",

            "type":
            "Bullish Liquidity Grab"

        }



    return None




# ==========================
# FINAL LIQUIDITY ANALYSIS
# ==========================

def analyze_liquidity(
    df
):


    return {


        "pool":
        find_swing_liquidity(df),


        "equal_levels":
        detect_equal_levels(df),


        "sweep":
        detect_liquidity_sweep(df),


        "grab":
        detect_liquidity_grab(df)

    }
