import pandas as pd



def detect_liquidity_sweep(df, lookback=20):

    if len(df) < lookback:
        return None


    recent = df.iloc[-lookback:-1]
    current = df.iloc[-1]


    high = recent["high"].max()
    low = recent["low"].min()



    if current["high"] > high and current["close"] < high:

        return {
            "direction":"SELL",
            "type":"Buy Side Liquidity Sweep",
            "level":float(high)
        }



    if current["low"] < low and current["close"] > low:

        return {
            "direction":"BUY",
            "type":"Sell Side Liquidity Sweep",
            "level":float(low)
        }



    return None





def detect_fvg(df):

    if len(df)<3:
        return None


    c1=df.iloc[-3]
    c3=df.iloc[-1]



    if c1["high"] < c3["low"]:

        return {

            "direction":"BUY",
            "type":"Bullish FVG",
            "top":float(c3["low"]),
            "bottom":float(c1["high"])

        }



    if c1["low"] > c3["high"]:

        return {

            "direction":"SELL",
            "type":"Bearish FVG",
            "top":float(c1["low"]),
            "bottom":float(c3["high"])

        }



    return None





def detect_order_block(df, lookback=30):


    if len(df)<lookback:
        return None



    data=df.iloc[-lookback:]



    for i in range(len(data)-2,0,-1):


        candle=data.iloc[i]
        next_candle=data.iloc[i+1]



        # Bullish OB

        if (

            candle["close"] < candle["open"]

            and

            next_candle["close"] > candle["high"]

        ):


            return {

                "direction":"BUY",

                "type":"Bullish Order Block",

                "high":float(candle["high"]),

                "low":float(candle["low"])

            }




        # Bearish OB


        if (

            candle["close"] > candle["open"]

            and

            next_candle["close"] < candle["low"]

        ):


            return {

                "direction":"SELL",

                "type":"Bearish Order Block",

                "high":float(candle["high"]),

                "low":float(candle["low"])

            }



    return None






def get_premium_discount(df):


    if len(df)<20:
        return None



    high=float(df["high"].tail(20).max())

    low=float(df["low"].tail(20).min())



    eq=(high+low)/2

    price=float(df["close"].iloc[-1])



    zone="Premium" if price>eq else "Discount"



    return {

        "zone":zone,

        "high":high,

        "low":low,

        "equilibrium":eq,

        "price":price

    }







# ==========================
# ENTRY ENGINE
# ==========================

def generate_trade_levels(df, signal, fvg=None, order_block=None):


    price=float(df["close"].iloc[-1])



    if signal=="BUY":


        entry=price



        if order_block and order_block["direction"]=="BUY":

            entry=(
                order_block["high"]
                +
                order_block["low"]
            )/2



        elif fvg and fvg["direction"]=="BUY":

            entry=(
                fvg["top"]
                +
                fvg["bottom"]
            )/2




        swing_low=float(df["low"].tail(30).min())


        sl=swing_low*0.997



        risk=entry-sl



        tp1=entry+(risk*2)

        tp2=entry+(risk*3)





    elif signal=="SELL":



        entry=price



        if order_block and order_block["direction"]=="SELL":


            entry=(

                order_block["high"]

                +

                order_block["low"]

            )/2




        elif fvg and fvg["direction"]=="SELL":


            entry=(

                fvg["top"]

                +

                fvg["bottom"]

            )/2





        swing_high=float(df["high"].tail(30).max())


        sl=swing_high*1.003



        risk=sl-entry



        tp1=entry-(risk*2)

        tp2=entry-(risk*3)




    else:


        return None




    return {


        "entry":round(entry,4),

        "sl":round(sl,4),

        "tp1":round(tp1,4),

        "tp2":round(tp2,4)

    }
