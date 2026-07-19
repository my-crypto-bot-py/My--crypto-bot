from config import SWING_LEFT, SWING_RIGHT


# ==========================
# FIND SWINGS
# ==========================

def find_swings(df):

    swing_highs = []
    swing_lows = []


    if len(df) < 50:
        return swing_highs, swing_lows


    for i in range(
        SWING_LEFT,
        len(df)-SWING_RIGHT
    ):


        high = float(df["high"].iloc[i])
        low = float(df["low"].iloc[i])


        left_high = df["high"].iloc[
            i-SWING_LEFT:i
        ].max()


        right_high = df["high"].iloc[
            i+1:i+SWING_RIGHT+1
        ].max()



        left_low = df["low"].iloc[
            i-SWING_LEFT:i
        ].min()


        right_low = df["low"].iloc[
            i+1:i+SWING_RIGHT+1
        ].min()



        if high > left_high and high > right_high:

            swing_highs.append({

                "index":i,

                "price":high,

                "type":"SH"

            })



        if low < left_low and low < right_low:

            swing_lows.append({

                "index":i,

                "price":low,

                "type":"SL"

            })


    return swing_highs, swing_lows




# ==========================
# BOS
# ==========================

def detect_bos(df, highs, lows):

    if len(highs)<2 or len(lows)<2:
        return None


    close=float(
        df["close"].iloc[-1]
    )


    last_high=highs[-1]
    last_low=lows[-1]


    if close > last_high["price"]:

        return {

            "direction":"BUY",

            "type":"Bullish BOS",

            "level":last_high["price"]

        }



    if close < last_low["price"]:

        return {

            "direction":"SELL",

            "type":"Bearish BOS",

            "level":last_low["price"]

        }


    return None




# ==========================
# MSS
# ==========================

def detect_mss(df, highs, lows):

    if len(highs)<3 or len(lows)<3:
        return None


    close=float(
        df["close"].iloc[-1]
    )


    # Lower high + break high

    if (

        highs[-1]["price"]
        <
        highs[-2]["price"]

        and

        close >
        highs[-1]["price"]

    ):

        return {

            "direction":"BUY",

            "type":"Bullish MSS",

            "level":highs[-1]["price"]

        }



    # Higher low + break low

    if (

        lows[-1]["price"]
        >
        lows[-2]["price"]

        and

        close <
        lows[-1]["price"]

    ):

        return {

            "direction":"SELL",

            "type":"Bearish MSS",

            "level":lows[-1]["price"]

        }


    return None




# ==========================
# CHOCH
# ==========================

def detect_choch(df, highs, lows):

    if len(highs)<3 or len(lows)<3:
        return None


    close=float(
        df["close"].iloc[-1]
    )


    # Bearish trend reversal

    if (

        highs[-1]["price"]
        <
        highs[-2]["price"]

        and

        close >
        highs[-2]["price"]

    ):

        return {

            "direction":"BUY",

            "type":"Bullish CHoCH"

        }



    # Bullish trend reversal

    if (

        lows[-1]["price"]
        >
        lows[-2]["price"]

        and

        close <
        lows[-2]["price"]

    ):

        return {

            "direction":"SELL",

            "type":"Bearish CHoCH"

        }


    return None




# ==========================
# EQUAL LEVELS
# ==========================

def detect_equal_levels(
    highs,
    lows,
    tolerance=0.001
):

    result={}


    if len(highs)>=2:

        diff=abs(
            highs[-1]["price"]
            -
            highs[-2]["price"]
        )


        if diff/highs[-1]["price"] <= tolerance:

            result["equal_high"]=True



    if len(lows)>=2:

        diff=abs(
            lows[-1]["price"]
            -
            lows[-2]["price"]
        )


        if diff/lows[-1]["price"] <= tolerance:

            result["equal_low"]=True


    return result




# ==========================
# FINAL STRUCTURE
# ==========================

def analyze_structure(df):


    highs,lows=find_swings(df)


    return {

        "swing_highs":highs,

        "swing_lows":lows,

        "bos":detect_bos(
            df,
            highs,
            lows
        ),

        "mss":detect_mss(
            df,
            highs,
            lows
        ),

        "choch":detect_choch(
            df,
            highs,
            lows
        ),

        "equal_levels":detect_equal_levels(
            highs,
            lows
        )

    }
