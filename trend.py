import pandas as pd


def calculate_ema(df, period):

    return df["close"].ewm(
        span=period,
        adjust=False
    ).mean()



def detect_trend(df):

    """
    Trend Detection:
    EMA + Market Structure
    Output same format for scanner.py
    """

    if df is None or len(df) < 50:

        return {
            "trend":"UNKNOWN",
            "strength":0
        }



    df = df.copy()



    df["EMA50"] = calculate_ema(df,50)



    if len(df) >= 200:

        df["EMA200"] = calculate_ema(df,200)



    close = float(
        df["close"].iloc[-1]
    )

    ema50 = float(
        df["EMA50"].iloc[-1]
    )



    ema_score = 0
    structure_score = 0



    # ==========================
    # EMA TREND
    # ==========================

    if len(df) >= 200:

        ema200 = float(
            df["EMA200"].iloc[-1]
        )


        distance = abs(
            ema50-ema200
        ) / ema200 * 100


        if ema50 > ema200:

            ema_trend="BULLISH"

            ema_score=min(
                distance*25,
                50
            )


        elif ema50 < ema200:

            ema_trend="BEARISH"

            ema_score=min(
                distance*25,
                50
            )


        else:

            ema_trend="SIDEWAYS"



    else:


        if close > ema50:

            ema_trend="BULLISH"

            ema_score=25


        elif close < ema50:

            ema_trend="BEARISH"

            ema_score=25


        else:

            ema_trend="SIDEWAYS"

            ema_score=10





    # ==========================
    # MARKET STRUCTURE
    # ==========================


    recent = df.tail(50)


    highs = recent["high"].values
    lows = recent["low"].values



    last_high = highs[-1]
    previous_high = highs[-10]


    last_low = lows[-1]
    previous_low = lows[-10]




    if (
        last_high > previous_high
        and
        last_low > previous_low
    ):

        structure="BULLISH"

        structure_score=50



    elif (

        last_high < previous_high
        and
        last_low < previous_low

    ):

        structure="BEARISH"

        structure_score=50



    else:

        structure="SIDEWAYS"

        structure_score=20





    # ==========================
    # FINAL TREND
    # ==========================


    if (
        ema_trend=="BULLISH"
        and
        structure=="BULLISH"
    ):

        trend="BULLISH"



    elif (

        ema_trend=="BEARISH"
        and
        structure=="BEARISH"

    ):

        trend="BEARISH"



    elif ema_trend!="SIDEWAYS":

        trend=ema_trend



    else:

        trend="SIDEWAYS"




    strength = round(
        min(
            ema_score + structure_score,
            100
        ),
        2
    )



    return {

        "trend":trend,

        "strength":strength

    }
