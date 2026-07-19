# ==========================
# ICT CONFIDENCE ENGINE V2
# ==========================


def calculate_confidence(

    trend,

    bos,

    choch,

    mss,

    liquidity,

    fvg,

    order_block,

    equal_levels,

    displacement,

    liquidity_grab,

    zone,

    btc=True,

    volume=True

):


    score = 0

    reasons = []


    buy_points = 0

    sell_points = 0



    # ==========================
    # TREND
    # ==========================

    if trend == "BULLISH":

        buy_points += 20

        reasons.append(
            "4H Bullish Trend"
        )


    elif trend == "BEARISH":

        sell_points += 20

        reasons.append(
            "4H Bearish Trend"
        )




    # ==========================
    # STRUCTURE
    # ==========================

    structures = [

        bos,

        mss,

        choch

    ]


    for item in structures:


        if item:


            if item["direction"] == "BUY":

                buy_points += 15


            elif item["direction"] == "SELL":

                sell_points += 15



            reasons.append(
                item["type"]
            )




    # ==========================
    # LIQUIDITY
    # ==========================

    if liquidity:


        if liquidity["direction"] == "BUY":

            buy_points += 10


        else:

            sell_points += 10



        reasons.append(
            liquidity["type"]
        )
            # ==========================
    # FVG
    # ==========================

    if fvg:

        if fvg["direction"] == "BUY":

            buy_points += 10

        else:

            sell_points += 10


        reasons.append(
            fvg["type"]
        )



    # ==========================
    # ORDER BLOCK
    # ==========================

    if order_block:

        if order_block["direction"] == "BUY":

            buy_points += 10

        else:

            sell_points += 10


        reasons.append(
            order_block["type"]
        )



    # ==========================
    # DISPLACEMENT
    # ==========================

    if displacement:


        if displacement["direction"] == "BUY":

            buy_points += 5

        else:

            sell_points += 5


        reasons.append(
            "Displacement"
        )



    # ==========================
    # LIQUIDITY GRAB
    # ==========================

    if liquidity_grab:


        if liquidity_grab["direction"] == "BUY":

            buy_points += 5

        else:

            sell_points += 5


        reasons.append(
            liquidity_grab["type"]
        )



    # ==========================
    # EQUAL LEVELS
    # ==========================

    if equal_levels:


        if equal_levels.get(
            "equal_high"
        ):

            sell_points += 3

            reasons.append(
                "Equal High Liquidity"
            )



        if equal_levels.get(
            "equal_low"
        ):

            buy_points += 3

            reasons.append(
                "Equal Low Liquidity"
            )



    # ==========================
    # BTC FILTER
    # ==========================

    if btc:

        score += 5

        reasons.append(
            "BTC Confirmation"
        )



    # ==========================
    # VOLUME FILTER
    # ==========================

    if volume:

        score += 5

        reasons.append(
            "Volume Confirmation"
        )



    # ==========================
    # FINAL DIRECTION
    # ==========================

    if buy_points > sell_points:

        direction = "BUY"

        score += buy_points



    elif sell_points > buy_points:

        direction = "SELL"

        score += sell_points



    else:

        direction = None

        score = 0



    # ==========================
    # SCORE LIMIT
    # ==========================

    score = min(
        score,
        100
    )



    # ==========================
    # QUALITY
    # ==========================

    if score >= 90:

        quality = "A+"



    elif score >= 80:

        quality = "A"



    elif score >= 70:

        quality = "B"



    elif score >= 60:

        quality = "C"



    else:

        quality = "NO TRADE"



    # ==========================
    # RETURN
    # ==========================

    return {


        "direction":
        direction,


        "score":
        score,


        "quality":
        quality,


        "buy_score":
        buy_points,


        "sell_score":
        sell_points,


        "reasons":
        reasons

    }
