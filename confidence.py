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


    # ==========================
    # HTF TREND (25)
    # ==========================

    if trend == "BULLISH":

        buy_score += 25
        buy_reasons.append("4H Bullish Trend")


    elif trend == "BEARISH":

        sell_score += 25
        sell_reasons.append("4H Bearish Trend")



    # ==========================
    # MARKET STRUCTURE
    # ==========================

    if bos:

        if bos.get("direction") == "BUY":

            buy_score += 15
            buy_reasons.append(
                bos.get("type","Bullish BOS")
            )


        elif bos.get("direction") == "SELL":

            sell_score += 15
            sell_reasons.append(
                bos.get("type","Bearish BOS")
            )



    if choch:

        if choch.get("direction") == "BUY":

            buy_score += 15
            buy_reasons.append(
                choch.get("type","Bullish CHoCH")
            )


        elif choch.get("direction") == "SELL":

            sell_score += 15
            sell_reasons.append(
                choch.get("type","Bearish CHoCH")
            )



    if mss:

        if mss.get("direction") == "BUY":

            buy_score += 10
            buy_reasons.append(
                mss.get("type","Bullish MSS")
            )


        elif mss.get("direction") == "SELL":

            sell_score += 10
            sell_reasons.append(
                mss.get("type","Bearish MSS")
            )



    # ==========================
    # LIQUIDITY
    # ==========================

    if liquidity:

        if liquidity.get("direction") == "BUY":

            buy_score += 15
            buy_reasons.append(
                "Liquidity Sweep"
            )


        elif liquidity.get("direction") == "SELL":

            sell_score += 15
            sell_reasons.append(
                "Liquidity Sweep"
            )



    # ==========================
    # FVG
    # ==========================

    if fvg:

        if fvg.get("direction") == "BUY":

            buy_score += 10
            buy_reasons.append(
                "Bullish FVG"
            )


        elif fvg.get("direction") == "SELL":

            sell_score += 10
            sell_reasons.append(
                "Bearish FVG"
            )



    # ==========================
    # ORDER BLOCK
    # ==========================

    if order_block:

        if order_block.get("direction") == "BUY":

            buy_score += 10
            buy_reasons.append(
                "Bullish Order Block"
            )


        elif order_block.get("direction") == "SELL":

            sell_score += 10
            sell_reasons.append(
                "Bearish Order Block"
            )



    # ==========================
    # PREMIUM DISCOUNT
    # ==========================

    if zone == "Discount":

        buy_score += 5
        buy_reasons.append(
            "Discount Zone"
        )


    elif zone == "Premium":

        sell_score += 5
        sell_reasons.append(
            "Premium Zone"
        )



    # ==========================
    # CONFIRMATION
    # ==========================

    if btc:

        buy_score += 3
        sell_score += 3


        buy_reasons.append(
            "BTC Confirmation"
        )

        sell_reasons.append(
            "BTC Confirmation"
        )



    if volume:

        buy_score += 2
        sell_score += 2


        buy_reasons.append(
            "Volume Confirmation"
        )

        sell_reasons.append(
            "Volume Confirmation"
        )



    # ==========================
    # FINAL DECISION
    # ==========================

    difference = abs(
        buy_score - sell_score
    )



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
        score = max(
            buy_score,
            sell_score
        )

        reasons = []



    score = min(
        score,
        100
    )



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
