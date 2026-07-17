import pandas as pd


def calculate_ema(df, period):
    return df["close"].ewm(
        span=period,
        adjust=False
    ).mean()



  def detect_trend(df):

    if df is None or len(df) < 30:
        return {
            "trend": "UNKNOWN",
            "strength": 0
        }

    highs = df["high"].tolist()
    lows = df["low"].tolist()

    last_high = max(highs[-10:])
    prev_high = max(highs[-20:-10])

    last_low = min(lows[-10:])
    prev_low = min(lows[-20:-10])

    if last_high > prev_high and last_low > prev_low:
        trend = "BULLISH"
        strength = 100

    elif last_high < prev_high and last_low < prev_low:
        trend = "BEARISH"
        strength = 100

    elif last_high > prev_high:
        trend = "BULLISH"
        strength = 70

    elif last_low < prev_low:
        trend = "BEARISH"
        strength = 70

    else:
        trend = "SIDEWAYS"
        strength = 40

    return {
        "trend": trend,
        "strength": strength
    }


    df=df.copy()


    df["EMA50"]=calculate_ema(df,50)


    if len(df)>=200:

        df["EMA200"]=calculate_ema(df,200)



    close=float(df["close"].iloc[-1])
    ema50=float(df["EMA50"].iloc[-1])


    ema_score=0
    structure_score=0
    momentum_score=0



    # ======================
    # EMA ANALYSIS
    # ======================

    if len(df)>=200:

        ema200=float(df["EMA200"].iloc[-1])

        distance=abs(
            ema50-ema200
        )/ema200*100


        ema_score=min(
            distance*15,
            40
        )


        if ema50>ema200:

            ema_trend="BULLISH"

        elif ema50<ema200:

            ema_trend="BEARISH"

        else:

            ema_trend="SIDEWAYS"


    else:


        if close>ema50:

            ema_trend="BULLISH"

        else:

            ema_trend="BEARISH"


        ema_score=20




    # ======================
    # MARKET STRUCTURE
    # ======================

    recent=df.tail(50)


    high_now=float(recent["high"].iloc[-1])
    high_old=float(recent["high"].iloc[10])


    low_now=float(recent["low"].iloc[-1])
    low_old=float(recent["low"].iloc[10])



    if high_now>high_old and low_now>low_old:

        structure="BULLISH"
        structure_score=40



    elif high_now<high_old and low_now<low_old:

        structure="BEARISH"
        structure_score=40



    else:

        structure="SIDEWAYS"
        structure_score=15




    # ======================
    # MOMENTUM
    # ======================

    change=(
        close -
        float(df["close"].iloc[-20])
    ) / float(df["close"].iloc[-20]) * 100



    if abs(change)>1:

        momentum_score=20

    elif abs(change)>0.5:

        momentum_score=10

    else:

        momentum_score=5



    # ======================
    # FINAL TREND
    # ======================

    if ema_trend == structure:

        trend = ema_trend

    else:

        if change > 1:

            trend = "BULLISH"

        elif change < -1:

            trend = "BEARISH"

        else:

            trend = "SIDEWAYS"


    strength=round(
        min(
            ema_score+
            structure_score+
            momentum_score,
            100
        ),
        2
    )



    return {

        "trend":trend,

        "strength":strength

    }
