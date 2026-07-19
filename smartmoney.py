import pandas as pd


# ==========================
# LIQUIDITY SWEEP
# ==========================

def detect_liquidity_sweep(df, lookback=20):

    if len(df) < lookback:
        return None


    recent = df.iloc[-lookback:-1]
    current = df.iloc[-1]


    previous_high = float(
        recent["high"].max()
    )

    previous_low = float(
        recent["low"].min()
    )


    open_price = float(
        current["open"]
    )

    close = float(
        current["close"]
    )

    high = float(
        current["high"]
    )

    low = float(
        current["low"]
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



    # Buy Side Liquidity Sweep
    # High taken then rejection

    if (

        high > previous_high

        and

        close < previous_high

        and

        upper_wick > body

    ):

        return {

            "direction":"SELL",

            "type":"Buy Side Liquidity Sweep",

            "level":previous_high

        }



    # Sell Side Liquidity Sweep
    # Low taken then rejection

    if (

        low < previous_low

        and

        close > previous_low

        and

        lower_wick > body

    ):

        return {

            "direction":"BUY",

            "type":"Sell Side Liquidity Sweep",

            "level":previous_low

        }



    return None




# ==========================
# LIQUIDITY GRAB
# ==========================

def detect_liquidity_grab(df):

    if len(df) < 20:
        return None


    recent = df.iloc[-20:-1]
    current = df.iloc[-1]


    high = float(
        recent["high"].max()
    )

    low = float(
        recent["low"].min()
    )



    if (

        float(current["high"]) > high

        and

        float(current["close"]) < high

    ):

        return {

            "direction":"SELL",

            "type":"Buy Side Liquidity Grab"

        }




    if (

        float(current["low"]) < low

        and

        float(current["close"]) > low

    ):

        return {

            "direction":"BUY",

            "type":"Sell Side Liquidity Grab"

        }



    return None




# ==========================
# FAIR VALUE GAP (FVG)
# ==========================

def detect_fvg(df):

    if len(df) < 3:
        return None



    c1 = df.iloc[-3]

    c2 = df.iloc[-2]

    c3 = df.iloc[-1]



    # Bullish FVG

    if (

        float(c3["low"])

        >

        float(c1["high"])

    ):


        return {

            "direction":"BUY",

            "type":"Bullish FVG",

            "top":float(c3["low"]),

            "bottom":float(c1["high"])

        }



    # Bearish FVG

    if (

        float(c3["high"])

        <

        float(c1["low"])

    ):


        return {

            "direction":"SELL",

            "type":"Bearish FVG",

            "top":float(c1["low"]),

            "bottom":float(c3["high"])

        }



    return None




# ==========================
# PREMIUM / DISCOUNT
# ==========================

def get_premium_discount(df):

    if len(df) < 20:
        return None



    high = float(
        df["high"].tail(20).max()
    )


    low = float(
        df["low"].tail(20).min()
    )


    price = float(
        df["close"].iloc[-1]
    )


    if high == low:
        return None



    position = (

        (price - low)

        /

        (high - low)

    ) * 100




    if position >= 75:

        zone = "Deep Premium"


    elif position >= 50:

        zone = "Premium"


    elif position <= 25:

        zone = "Deep Discount"


    else:

        zone = "Discount"



    return {

        "zone":zone,

        "high":high,

        "low":low,

        "price":price,

        "equilibrium":(high+low)/2,

        "position":round(position,2)

    }
    # ==========================
# ORDER BLOCK
# ==========================

def detect_order_block(df, lookback=50):

    if len(df) < lookback:
        return None


    data = df.iloc[-lookback:]


    for i in range(
        len(data)-2,
        0,
        -1
    ):

        candle = data.iloc[i]

        next_candle = data.iloc[i+1]


        high = float(candle["high"])
        low = float(candle["low"])

        open_price = float(candle["open"])
        close = float(candle["close"])



        candle_range = high - low


        if candle_range == 0:
            continue



        next_move = abs(

            float(next_candle["close"])

            -

            float(next_candle["open"])

        )



        # Bullish Order Block
        # Last bearish candle before expansion

        if (

            close < open_price

            and

            float(next_candle["close"]) > high

            and

            next_move > candle_range * 0.5

        ):


            return {

                "direction":"BUY",

                "type":"Bullish Order Block",

                "high":high,

                "low":low

            }




        # Bearish Order Block
        # Last bullish candle before drop


        if (

            close > open_price

            and

            float(next_candle["close"]) < low

            and

            next_move > candle_range * 0.5

        ):


            return {

                "direction":"SELL",

                "type":"Bearish Order Block",

                "high":high,

                "low":low

            }


    return None




# ==========================
# FRESH ORDER BLOCK
# ==========================

def is_fresh_order_block(
    df,
    order_block
):

    if order_block is None:
        return False



    recent = df.tail(5)



    if order_block["direction"] == "BUY":


        if (

            float(recent["low"].min())

            <

            order_block["low"]

        ):

            return False




    if order_block["direction"] == "SELL":


        if (

            float(recent["high"].max())

            >

            order_block["high"]

        ):

            return False



    return True




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



    # Bullish OB failed

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




    # Bearish OB failed


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

        <=

        price

        <=

        order_block["high"]

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
        close - open_price
    )



    upper_wick = (

        high -

        max(
            open_price,
            close
        )

    )



    lower_wick = (

        min(
            open_price,
            close
        )

        -

        low

    )



    # Bearish rejection


    if upper_wick > body * 2:


        return {

            "direction":"SELL",

            "type":"Bearish Rejection Block",

            "high":high,

            "low":low

        }



    # Bullish rejection


    if lower_wick > body * 2:


        return {

            "direction":"BUY",

            "type":"Bullish Rejection Block",

            "high":high,

            "low":low

        }



    return None
    # ==========================
# DISPLACEMENT
# ==========================

def detect_displacement(df):

    if len(df) < 20:
        return None


    current = df.iloc[-1]


    body = abs(
        float(current["close"])
        -
        float(current["open"])
    )


    avg_body = (

        df["close"]
        -
        df["open"]

    ).abs().tail(20).mean()



    if avg_body == 0:
        return None



    strength = body / avg_body



    if strength >= 2:


        if (

            float(current["close"])

            >

            float(current["open"])

        ):


            return {

                "direction":"BUY",

                "type":"Bullish Displacement",

                "strength":round(strength,2)

            }



        else:


            return {

                "direction":"SELL",

                "type":"Bearish Displacement",

                "strength":round(strength,2)

            }



    return None




# ==========================
# TRADE LEVEL GENERATOR
# ==========================

def generate_trade_levels(
    df,
    signal,
    fvg=None,
    order_block=None,
    liquidity=None
):

    price = float(
        df["close"].iloc[-1]
    )



    if signal == "BUY":


        entry = price



        if order_block and order_block["direction"] == "BUY":


            entry = (

                order_block["high"]

                +

                order_block["low"]

            ) / 2



            sl = order_block["low"] * 0.998



        elif fvg and fvg["direction"] == "BUY":


            entry = (

                fvg["top"]

                +

                fvg["bottom"]

            ) / 2



            sl = fvg["bottom"] * 0.998



        else:


            sl = (

                float(
                    df["low"]
                    .tail(30)
                    .min()
                )

                *

                0.998

            )



        risk = entry - sl



        if risk <= 0:
            return None



        tp1 = (

            float(
                df["high"]
                .tail(50)
                .max()
            )

        )



        if tp1 <= entry:

            tp1 = entry + risk * 2



        tp2 = entry + risk * 3




    elif signal == "SELL":


        entry = price



        if order_block and order_block["direction"] == "SELL":


            entry = (

                order_block["high"]

                +

                order_block["low"]

            ) / 2



            sl = order_block["high"] * 1.002



        elif fvg and fvg["direction"] == "SELL":


            entry = (

                fvg["top"]

                +

                fvg["bottom"]

            ) / 2



            sl = fvg["top"] * 1.002



        else:


            sl = (

                float(
                    df["high"]
                    .tail(30)
                    .max()
                )

                *

                1.002

            )



        risk = sl - entry



        if risk <= 0:
            return None



        tp1 = (

            float(
                df["low"]
                .tail(50)
                .min()
            )

        )



        if tp1 >= entry:

            tp1 = entry - risk * 2



        tp2 = entry - risk * 3



    else:

        return None



    return {


        "entry":round(entry,4),

        "sl":round(sl,4),

        "tp1":round(tp1,4),

        "tp2":round(tp2,4)

    }




# ==========================
# SMART MONEY ANALYSIS
# ==========================

def analyze_smart_money(df):


    liquidity = detect_liquidity_sweep(df)


    liquidity_grab = detect_liquidity_grab(df)


    fvg = detect_fvg(df)


    order_block = detect_order_block(df)



    fresh_ob = is_fresh_order_block(
        df,
        order_block
    )



    breaker = detect_breaker_block(
        df,
        order_block
    )



    mitigation = detect_mitigation_block(
        df,
        order_block
    )



    rejection = detect_rejection_block(df)



    zone = get_premium_discount(df)



    displacement = detect_displacement(df)



    return {


        "liquidity":liquidity,


        "liquidity_grab":liquidity_grab,


        "fvg":fvg,


        "order_block":order_block,


        "fresh_ob":fresh_ob,


        "breaker":breaker,


        "mitigation":mitigation,


        "rejection":rejection,


        "zone":zone,


        "displacement":displacement

    }
