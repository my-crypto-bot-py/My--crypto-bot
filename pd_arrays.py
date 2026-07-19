# ==========================
# ICT PD ARRAYS ENGINE
# ==========================


# ==========================
# FAIR VALUE GAP (FVG)
# ==========================

def detect_fvg(df):

    if len(df) < 3:
        return None


    c1 = df.iloc[-3]
    c3 = df.iloc[-1]


    # Bullish FVG

    if float(c3["low"]) > float(c1["high"]):

        return {

            "direction": "BUY",

            "type": "Bullish FVG",

            "top": float(c3["low"]),

            "bottom": float(c1["high"])

        }


    # Bearish FVG

    if float(c3["high"]) < float(c1["low"]):

        return {

            "direction": "SELL",

            "type": "Bearish FVG",

            "top": float(c1["low"]),

            "bottom": float(c3["high"])

        }


    return None



# ==========================
# FVG MIDPOINT
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
# PD ARRAY OBJECT
# ==========================

def create_pd_array(

    fvg=None,

    order_block=None,

    breaker=None,

    mitigation=None

):

    return {

        "fvg": fvg,

        "order_block": order_block,

        "breaker": breaker,

        "mitigation": mitigation

    }
  # ==========================
# BREAKER BLOCK
# ==========================

def detect_breaker_block(
    df,
    order_block=None
):

    if order_block is None:
        return None


    last_price = float(
        df["close"].iloc[-1]
    )


    # Bullish OB failed -> Bearish Breaker

    if (
        order_block["direction"] == "BUY"
        and
        last_price <
        order_block["low"]
    ):

        return {

            "direction": "SELL",

            "type": "Bearish Breaker",

            "high": order_block["high"],

            "low": order_block["low"]

        }


    # Bearish OB failed -> Bullish Breaker

    if (
        order_block["direction"] == "SELL"
        and
        last_price >
        order_block["high"]
    ):

        return {

            "direction": "BUY",

            "type": "Bullish Breaker",

            "high": order_block["high"],

            "low": order_block["low"]

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


    # Price returns inside OB

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


    high = float(
        candle["high"]
    )

    low = float(
        candle["low"]
    )

    open_price = float(
        candle["open"]
    )

    close = float(
        candle["close"]
    )


    body = abs(
        close - open_price
    )

    upper_wick = high - max(
        open_price,
        close
    )

    lower_wick = min(
        open_price,
        close
    ) - low


    # Bearish rejection

    if upper_wick > body * 2:

        return {

            "direction":
            "SELL",

            "type":
            "Bearish Rejection Block",

            "high":
            high,

            "low":
            low

        }


    # Bullish rejection

    if lower_wick > body * 2:

        return {

            "direction":
            "BUY",

            "type":
            "Bullish Rejection Block",

            "high":
            high,

            "low":
            low

        }


    return None
  # ==========================
# PD ARRAY COLLECTION
# ==========================

def collect_pd_arrays(df):

    arrays = []


    fvg = detect_fvg(df)

    if fvg:
        arrays.append(fvg)


    ob = detect_order_block(df)

    if ob:
        arrays.append(ob)


    breaker = detect_breaker_block(
        df,
        ob
    )

    if breaker:
        arrays.append(breaker)


    mitigation = detect_mitigation_block(
        df,
        ob
    )

    if mitigation:
        arrays.append(mitigation)


    rejection = detect_rejection_block(
        df
    )

    if rejection:
        arrays.append(rejection)


    return arrays



# ==========================
# PD ARRAY SCORE
# ==========================

def score_pd_array(array):

    score = 0


    if array["type"].find("Order Block") >= 0:

        score += 40


    if array["type"].find("FVG") >= 0:

        score += 30


    if array["type"].find("Breaker") >= 0:

        score += 35


    if array["type"].find("Mitigation") >= 0:

        score += 25


    if array["type"].find("Rejection") >= 0:

        score += 20


    return score



# ==========================
# BEST PD ARRAY
# ==========================

def get_best_pd_array(df):

    arrays = collect_pd_arrays(df)


    if len(arrays) == 0:

        return None


    for array in arrays:

        array["score"] = score_pd_array(
            array
        )


    best = max(
        arrays,
        key=lambda x: x["score"]
    )


    return best



# ==========================
# PD ARRAY DEBUG
# ==========================

def debug_pd_arrays(df):

    arrays = collect_pd_arrays(df)


    print(
        "===== PD ARRAYS ====="
    )


    for a in arrays:

        print(
            a
        )


    print(
        "====================="
    )
