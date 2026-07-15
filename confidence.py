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


    # HTF Trend

    if trend == "BULLISH":

        buy_score += 20
        buy_reasons.append("4H Bullish Trend")


    elif trend == "BEARISH":

        sell_score += 20
        sell_reasons.append("4H Bearish Trend")



    # Market Structure

    for item in [bos, choch, mss]:

        if item:

            direction = item.get("direction")

            name = item.get("type","Structure")


            if direction == "BUY":

                buy_score += 15
                buy_reasons.append(name)


            elif direction == "SELL":

                sell_score += 15
                sell_reasons.append(name)



    # Liquidity

    if liquidity:

        if liquidity.get("direction") == "BUY":

            buy_score += 10
            buy_reasons.append("Liquidity Sweep")


        elif liquidity.get("direction") == "SELL":

            sell_score += 10
            sell_reasons.append("Liquidity Sweep")



    # FVG

    if fvg:

        if fvg.get("direction") == "BUY":

            buy_score += 10
            buy_reasons.append("Bullish FVG")


        elif fvg.get("direction") == "SELL":

            sell_score += 10
            sell_reasons.append("Bearish FVG")



    # Order Block

    if order_block:

        if order_block.get("direction") == "BUY":

            buy_score += 10
            buy_reasons.append("Bullish Order Block")


        elif order_block.get("direction") == "SELL":

            sell_score += 10
            sell_reasons.append("Bearish Order Block")



    # Premium Discount

    if zone == "Discount":

        buy_score += 5
        buy_reasons.append("Discount Zone")


    elif zone == "Premium":

        sell_score += 5
        sell_reasons.append("Premium Zone")



    # Confirmation

    if btc:

        buy_score += 5
        sell_score += 5


        buy_reasons.append("BTC Confirmation")
        sell_reasons.append("BTC Confirmation")



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

        quality="A+"


    elif score >=80:

        quality="A"


    elif score>=70:

        quality="B"


    else:

        quality="NO TRADE"



    return {

        "direction":direction,

        "score":score,

        "quality":quality,

        "reasons":reasons

    }
