import pandas as pd


def find_swings(df, left=5, right=5):

    highs = []
    lows = []

    if len(df) < left + right + 10:
        return highs, lows


    for i in range(left, len(df)-right):

        high = df["high"].iloc[i]
        low = df["low"].iloc[i]

        high_range = df["high"].iloc[i-left:i+right+1]
        low_range = df["low"].iloc[i-left:i+right+1]


        if high == high_range.max():

            highs.append({
                "index": i,
                "price": float(high)
            })


        if low == low_range.min():

            lows.append({
                "index": i,
                "price": float(low)
            })


    return highs, lows




def detect_bos(df, swing_highs, swing_lows):


    if not swing_highs and not swing_lows:
        return None


    close = float(df["close"].iloc[-1])
    previous_close = float(df["close"].iloc[-2])



    # Bullish BOS

    if swing_highs:

        level = swing_highs[-1]["price"]


        if previous_close <= level and close > level:

            return {
                "direction":"BUY",
                "type":"Bullish BOS",
                "level":level
            }




    # Bearish BOS

    if swing_lows:

        level = swing_lows[-1]["price"]


        if previous_close >= level and close < level:

            return {
                "direction":"SELL",
                "type":"Bearish BOS",
                "level":level
            }



    return None





def detect_mss(df, swing_highs, swing_lows):


    if len(swing_highs)<2 or len(swing_lows)<2:
        return None



    close=float(df["close"].iloc[-1])


    last_high=swing_highs[-2]["price"]
    last_low=swing_lows[-2]["price"]



    if close > last_high:

        return {

            "direction":"BUY",
            "type":"Bullish MSS",
            "level":last_high

        }



    if close < last_low:

        return {

            "direction":"SELL",
            "type":"Bearish MSS",
            "level":last_low

        }


    return None





def detect_choch(df, swing_highs, swing_lows):


    if len(swing_highs)<2 or len(swing_lows)<2:
        return None



    close=float(df["close"].iloc[-1])



    last_high=swing_highs[-1]["price"]

    last_low=swing_lows[-1]["price"]



    # Reversal confirmation only

    if close > last_high:

        return {

            "direction":"BUY",
            "type":"Bullish CHoCH",
            "level":last_high

        }



    if close < last_low:

        return {

            "direction":"SELL",
            "type":"Bearish CHoCH",
            "level":last_low

        }



    return None
