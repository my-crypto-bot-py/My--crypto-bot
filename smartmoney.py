import pandas as pd


def detect_liquidity_sweep(df, lookback=20):

    if len(df) < lookback:
        return None

    recent = df.iloc[-lookback:]
    current = df.iloc[-1]

    previous_high = recent["high"][:-1].max()
    previous_low = recent["low"][:-1].min()


    # Buy side liquidity sweep (sell signal)
    if current["high"] > previous_high and current["close"] < previous_high:

        return {
            "direction": "SELL",
            "type": "Buy Side Liquidity Sweep",
            "level": previous_high
        }


    # Sell side liquidity sweep (buy signal)
    if current["low"] < previous_low and current["close"] > previous_low:

        return {
            "direction": "BUY",
            "type": "Sell Side Liquidity Sweep",
            "level": previous_low
        }


    return None




def detect_fvg(df):

    if len(df) < 3:
        return None


    c1 = df.iloc[-3]
    c3 = df.iloc[-1]


    # Bullish FVG

    if c1["high"] < c3["low"]:

        return {

            "direction":"BUY",
            "type":"Bullish FVG",
            "top":c3["low"],
            "bottom":c1["high"]

        }



    # Bearish FVG

    if c1["low"] > c3["high"]:

        return {

            "direction":"SELL",
            "type":"Bearish FVG",
            "top":c1["low"],
            "bottom":c3["high"]

        }


    return None





def detect_order_block(df, lookback=20):

    if len(df) < lookback:
        return None


    data=df.iloc[-lookback:]


    for i in range(len(data)-2,0,-1):

        candle=data.iloc[i]
        next_candle=data.iloc[i+1]


        # Bullish OB

        if (
            candle["close"] < candle["open"]
            and next_candle["close"] > candle["high"]
        ):

            return {

                "direction":"BUY",
                "type":"Bullish Order Block",
                "high":candle["high"],
                "low":candle["low"]

            }



        # Bearish OB

        if (
            candle["close"] > candle["open"]
            and next_candle["close"] < candle["low"]
        ):

            return {

                "direction":"SELL",
                "type":"Bearish Order Block",
                "high":candle["high"],
                "low":candle["low"]

            }


    return None






def get_premium_discount(df):

    if len(df)<20:
        return None


    high=df["high"].tail(20).max()

    low=df["low"].tail(20).min()


    equilibrium=(high+low)/2

    price=df["close"].iloc[-1]


    if price > equilibrium:
        zone="Premium"

    else:
        zone="Discount"



    return {

        "zone":zone,
        "high":high,
        "low":low,
        "equilibrium":equilibrium,
        "price":price

    }






# ==============================
# SMART MONEY ENTRY ENGINE
# ==============================

def generate_trade_levels(df, signal, fvg=None, order_block=None):


    price=float(df["close"].iloc[-1])


    if signal=="BUY":


        entry=price


        if order_block and order_block["direction"]=="BUY":

            entry=float(order_block["high"])


        elif fvg and fvg["direction"]=="BUY":

            entry=float(fvg["bottom"])



        swing_low=float(df["low"].tail(20).min())


        sl=swing_low*0.998


        risk=entry-sl


        tp1=entry+(risk*2)

        tp2=entry+(risk*3)




    elif signal=="SELL":


        entry=price


        if order_block and order_block["direction"]=="SELL":

            entry=float(order_block["low"])


        elif fvg and fvg["direction"]=="SELL":

            entry=float(fvg["top"])



        swing_high=float(df["high"].tail(20).max())


        sl=swing_high*1.002


        risk=sl-entry


        tp1=entry-(risk*2)

        tp2=entry-(risk*3)




    else:


        return {

            "entry":None,
            "sl":None,
            "tp1":None,
            "tp2":None

        }




    return {


        "entry":round(entry,2),

        "sl":round(sl,2),

        "tp1":round(tp1,2),

        "tp2":round(tp2,2)

    }
