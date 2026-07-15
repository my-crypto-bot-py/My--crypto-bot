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


    # Higher Timeframe Trend

    if trend == "BULLISH":
        buy_score += 25
        buy_reasons.append("4H Bullish Trend")

    elif trend == "BEARISH":
        sell_score += 25
        sell_reasons.append("4H Bearish Trend")



    # Structure

    for item in [bos, choch, mss]:

        if item:

            if item.get("direction") == "BUY":

                buy_score += 15
                buy_reasons.append(item.get("type","Structure"))


            elif item.get("direction") == "SELL":

                sell_score += 15
                sell_reasons.append(item.get("type","Structure"))



    # Liquidity Sweep

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



    # BTC Confirmation

    if btc:

        buy_score += 3
        sell_score += 3


    # Volume Confirmation

    if volume:

        buy_score += 3
        sell_score += 3



    # Final Direction

    difference = abs(buy_score - sell_score)


    if buy_score > sell_score and difference >= 15:

        direction = "BUY"
        score = buy_score
        reasons = buy_reasons


    elif sell_score > buy_score and difference >= 15:

        direction = "SELL"
        score = sell_score
        reasons = sell_reasons


    else:

        direction = "NONE"
        score = max(buy_score, sell_score)
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
