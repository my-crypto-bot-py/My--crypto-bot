# ==========================
# ICT PD ARRAYS ENGINE V2
# ==========================


# ==========================
# NORMALIZE ARRAY LEVELS
# ==========================

def normalize_levels(array):

    if array is None:
        return None


    if "high" in array and "low" in array:

        return array


    if "top" in array and "bottom" in array:

        array["high"] = array["top"]
        array["low"] = array["bottom"]

        return array


    return None



# ==========================
# FVG DETECTION
# ==========================

def detect_fvg(df):

    if len(df) < 3:
        return None


    c1 = df.iloc[-3]
    c3 = df.iloc[-1]


    # Bullish FVG

    if float(c3["low"]) > float(c1["high"]):

        return {

            "direction":"BUY",

            "type":"Bullish FVG",

            "top":float(c3["low"]),

            "bottom":float(c1["high"])

        }


    # Bearish FVG

    if float(c3["high"]) < float(c1["low"]):

        return {

            "direction":"SELL",

            "type":"Bearish FVG",

            "top":float(c1["low"]),

            "bottom":float(c3["high"])

        }


    return None



# ==========================
# FVG MID
# ==========================

def fvg_midpoint(fvg):

    if fvg is None:
        return None


    return (
        fvg["top"]
        +
        fvg["bottom"]
    ) / 2
    # ==========================
# BREAKER BLOCK
# ==========================

def detect_breaker_block(
    df,
    order_block=None
):

    if order_block is None:
        return None


    price = float(
        df["close"].iloc[-1]
    )


    # Bullish OB broken downward
    # becomes Bearish Breaker

    if (
        order_block["direction"] == "BUY"
        and
        price < order_block["low"]
    ):

        return {

            "direction":"SELL",

            "type":"Bearish Breaker",

            "high":order_block["high"],

            "low":order_block["low"]

        }


    # Bearish OB broken upward
    # becomes Bullish Breaker

    if (
        order_block["direction"] == "SELL"
        and
        price > order_block["high"]
    ):

        return {

            "direction":"BUY",

            "type":"Bullish Breaker",

            "high":order_block["high"],

            "low":order_block["low"]

        }


    return None



# ==========================
# MITIGATION BLOCK
# ==========================

def detect_mitigation_block(
    df,
    order_block=None
):

    if order_block is None:
        return None


    price = float(
        df["close"].iloc[-1]
    )


    if (
        order_block["low"]
        <= price
        <= order_block["high"]
    ):

        return {

            "direction":
            order_block["direction"],

            "type":
            "Mitigation Block",

            "high":
            order_block["high"],

            "low":
            order_block["low"]

        }


    return None



# ==========================
# REJECTION BLOCK
# ==========================

def detect_rejection_block(df):

    if len(df) < 3:
        return None


    candle = df.iloc[-1]


    high = float(candle["high"])

    low = float(candle["low"])

    open_price = float(candle["open"])

    close = float(candle["close"])


    body = abs(
        close-open_price
    )


    upper_wick = (
        high -
        max(open_price,close)
    )


    lower_wick = (
        min(open_price,close)
        -
        low
    )


    # Avoid zero body problem

    if body == 0:
        body = 0.0001



    # Bearish rejection

    if upper_wick >= body*2:

        return {

            "direction":"SELL",

            "type":
            "Bearish Rejection Block",

            "high":high,

            "low":low

        }



    # Bullish rejection

    if lower_wick >= body*2:

        return {

            "direction":"BUY",

            "type":
            "Bullish Rejection Block",

            "high":high,

            "low":low

        }



    return None
    # ==========================
# PD ARRAY COLLECTION V2
# ==========================

def collect_pd_arrays(df):

    arrays = []


    # FVG

    fvg = detect_fvg(df)

    if fvg:

        fvg["source"] = "FVG"

        arrays.append(fvg)



    # ORDER BLOCK

    ob = detect_order_block(df)

    if ob:

        ob["source"] = "ORDER BLOCK"

        arrays.append(ob)



    # BREAKER

    breaker = detect_breaker_block(
        df,
        ob
    )

    if breaker:

        breaker["source"] = "BREAKER"

        arrays.append(breaker)



    # MITIGATION

    mitigation = detect_mitigation_block(
        df,
        ob
    )

    if mitigation:

        mitigation["source"] = "MITIGATION"

        arrays.append(mitigation)



    # REJECTION

    rejection = detect_rejection_block(
        df
    )

    if rejection:

        rejection["source"] = "REJECTION"

        arrays.append(rejection)



    return arrays



# ==========================
# PD ARRAY SCORE V2
# ==========================

def score_pd_array(array):

    score = 0


    array_type = array.get(
        "type",
        ""
    )


    # Order Block highest

    if "Order Block" in array_type:

        score += 40



    # Breaker

    if "Breaker" in array_type:

        score += 35



    # FVG

    if "FVG" in array_type:

        score += 30



    # Mitigation

    if "Mitigation" in array_type:

        score += 25



    # Rejection

    if "Rejection" in array_type:

        score += 20



    # Fresh zone bonus

    if array.get(
        "fresh",
        False
    ):

        score += 10



    return score



# ==========================
# BEST PD ARRAY
# ==========================

def get_best_pd_array(df):

    arrays = collect_pd_arrays(df)


    if not arrays:

        return None



    for array in arrays:

        array["score"] = score_pd_array(
            array
        )



    best = max(
        arrays,
        key=lambda x:x["score"]
    )


    return best



# ==========================
# PD DEBUG PANEL
# ==========================

def debug_pd_arrays(df):

    arrays = collect_pd_arrays(df)


    print(
        "\n========== PD ARRAYS =========="
    )


    if not arrays:

        print(
            "No PD Array Found"
        )

        return



    for item in arrays:

        print(
            item
        )


    best = get_best_pd_array(df)


    print(
        "\nBEST PD ARRAY:"
    )

    print(
        best
    )


    print(
        "==============================\n"
    )
