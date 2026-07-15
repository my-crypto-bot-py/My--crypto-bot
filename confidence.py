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


    # Trend
    if trend == "BULLISH":
        buy_score += 20
        buy_reasons.append("4H Bullish Trend")

    elif trend == "BEARISH":
        sell_score += 20
        sell_reasons.append("4H Bearish Trend")


    # Structure
    structures = [bos, choch, mss]

    for item in structures:

        if item:

            if item["direction"] == "BUY":
                buy_score += 10
                buy_reasons.append(item["type"])

            elif item["direction"] == "SELL":
                sell_score += 10
                sell_reasons.append(item["type"])


    # Liquidity
    if liquidity:
        if "Sell" in liquidity["type"]:
            sell_score += 10
            sell_reasons.append("Liquidity Sweep")

        else:
            buy_score += 10
            buy_reasons.append("Liquidity Sweep")


    # FVG
    if fvg:

        if "Bullish" in fvg["type"]:
            buy_score += 10
            buy_reasons.append("FVG")

        elif "Bearish" in fvg["type"]:
            sell_score += 10
            sell_reasons.append("FVG")


    # Order Block
    if order_block:

        if "Bullish" in order_block["type"]:
            buy_score += 10
            buy_reasons.append("Order Block")

        elif "Bearish" in order_block["type"]:
            sell_score += 10
            sell_reasons.append("Order Block")


    # Premium Discount
    if zone:

        if zone == "Discount":
            buy_score += 10
            buy_reasons.append("Discount Zone")

        elif zone == "Premium":
            sell_score += 10
            sell_reasons.append("Premium Zone")


    # BTC + Volume
    if btc:
        buy_score += 5
        sell_score += 5

    if volume:
        buy_score += 5
        sell_score += 5


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
        "direction": direction,
        "score": score,
        "quality": quality,
        "reasons": reasons
    }
