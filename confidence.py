def calculate_confidence(
    trend=None,
    bos=None,
    choch=None,
    mss=None,
    liquidity=None,
    fvg=None,
    order_block=None,
    zone=None,
    btc=False,
    volume=False
):

    buy_score = 0
    sell_score = 0

    buy_reasons = []
    sell_reasons = []


    # Trend (20)

    if trend == "BULLISH":

        buy_score += 20
        buy_reasons.append("4H Bullish Trend")


    elif trend == "BEARISH":

        sell_score += 20
        sell_reasons.append("4H Bearish Trend")



    # Market Structure (15 each)

    for item in [bos, choch, mss]:

        if item:

            if item["direction"] == "BUY":

                buy_score += 15
                buy_reasons.append(item["type"])


            elif item["direction"] == "SELL":

                sell_score += 15
                sell_reasons.append(item["type"])




    # Liquidity Sweep (15)

    if liquidity:

        if liquidity["direction"] == "BUY":

            buy_score += 15
            buy_reasons.append("Liquidity Sweep")


        elif liquidity["direction"] == "SELL":

            sell_score += 15
            sell_reasons.append("Liquidity Sweep")





    # FVG (10)

    if fvg:

        if fvg["direction"] == "BUY":

            buy_score += 10
            buy_reasons.append("Bullish FVG")


        elif fvg["direction"] == "SELL":

            sell_score += 10
            sell_reasons.append("Bearish FVG")





    # Order Block (10)

    if order_block:

        if order_block["direction"] == "BUY":

            buy_score += 10
            buy_reasons.append("Bullish Order Block")


        elif order_block["direction"] == "SELL":

            sell_score += 10
            sell_reasons.append("Bearish Order Block")





    # Premium Discount Filter

    if zone:

        if zone == "Discount":

            buy_score += 10
            buy_reasons.append("Discount Zone")


        elif zone == "Premium":

            sell_score += 10
            sell_reasons.append("Premium Zone")





    # BTC Confirmation

    if btc:

        buy_score += 5
        sell_score += 5

        buy_reasons.append("BTC Confirmation")
        sell_reasons.append("BTC Confirmation")




    # Volume

    if volume:

        buy_score += 5
        sell_score += 5

        buy_reasons.append("Volume Confirmation")
        sell_reasons.append("Volume Confirmation")





    # Final Direction

    if buy_score > sell_score:

        direction = "BUY"
        score = buy_score
        reasons = buy_reasons


    elif sell_score > buy_score:

        direction = "SELL"
        score = sell_score
        reasons = sell_reasons


    else:

        direction = "NONE"
        score = 0
        reasons = []



    score = min(score,100)



    if score >= 90:

        quality = "A+"


    elif score >= 80:

        quality = "A"


    elif score >= 70:

        quality = "B"


    else:

        quality = "NO TRADE"




    return {

        "direction": direction,

        "score": score,

        "quality": quality,

        "reasons": reasons

    }
