import pandas as pd


def find_swings(df, left=3, right=3):

    highs = []
    lows = []


    for i in range(left, len(df)-right):

        high_range = df["high"].iloc[i-left:i+right+1]
        low_range = df["low"].iloc[i-left:i+right+1]


        if df["high"].iloc[i] == high_range.max():

            highs.append(
                {
                    "index": i,
                    "price": float(df["high"].iloc[i])
                }
            )


        if df["low"].iloc[i] == low_range.min():

            lows.append(
                {
                    "index": i,
                    "price": float(df["low"].iloc[i])
                }
            )


    return highs, lows





def detect_bos(df, swing_highs, swing_lows):


    if not swing_highs and not swing_lows:
        return None


    close = float(df["close"].iloc[-1])


    # Bullish BOS

    if swing_highs:

        last_high = swing_highs[-1]["price"]


        if close > last_high:

            return {

                "direction":"BUY",

                "type":"Bullish BOS",

                "level":last_high

            }




    # Bearish BOS

    if swing_lows:

        last_low = swing_lows[-1]["price"]


        if close < last_low:

            return {

                "direction":"SELL",

                "type":"Bearish BOS",

                "level":last_low

            }


    return None






def detect_mss(df, swing_highs, swing_lows):


    if len(swing_highs)<2 or len(swing_lows)<2:

        return None



    close=float(df["close"].iloc[-1])


    previous_high=swing_highs[-2]["price"]

    previous_low=swing_lows[-2]["price"]




    # Bullish Market Structure Shift

    if close > previous_high:


        return {

            "direction":"BUY",

            "type":"Bullish MSS",

            "level":previous_high

        }




    # Bearish Market Structure Shift

    if close < previous_low:


        return {

            "direction":"SELL",

            "type":"Bearish MSS",

            "level":previous_low

        }



    return None







def detect_choch(df, swing_highs, swing_lows):


    if len(swing_highs)<2 or len(swing_lows)<2:

        return None



    close=float(df["close"].iloc[-1])


    last_high=swing_highs[-1]["price"]

    last_low=swing_lows[-1]["price"]




    # Trend reversal up

    if close > last_high:


        return {

            "direction":"BUY",

            "type":"Bullish CHoCH",

            "level":last_high

        }





    # Trend reversal down

    if close < last_low:


        return {

            "direction":"SELL",

            "type":"Bearish CHoCH",

            "level":last_low

        }




    return None
