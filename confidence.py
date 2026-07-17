def calculate_confidence(
    trend=None,
    bos=None,
    choch=None,
    mss=None,
    liquidity=None,
    fvg=None,
    order_block=None,
    equal_levels=None,
    displacement=None,
    liquidity_grab=None,
    zone=None,
    btc=False,
    volume=False
):

    buy_score = 0
    sell_score = 0

    buy_reasons = []
    sell_reasons = []

    # ======================
    # HTF TREND
    # ======================

    if trend == "BULLISH":
        buy_score += 15
        buy_reasons.append("4H Bullish Trend")

    elif trend == "BEARISH":
        sell_score += 15
        sell_reasons.append("4H Bearish Trend")

    # ======================
    # BOS
    # ======================

    if bos:

        if bos["direction"] == "BUY":
            buy_score += 20
            buy_reasons.append("Bullish BOS")

        else:
            sell_score += 20
            sell_reasons.append("Bearish BOS")

    # ======================
    # MSS
    # ======================

    if mss:

        if mss["direction"] == "BUY":
            buy_score += 20
            buy_reasons.append("Bullish MSS")

        else:
            sell_score += 20
            sell_reasons.append("Bearish MSS")

    # ======================
    # CHOCH
    # ======================

    if choch:

        if choch["direction"] == "BUY":
            buy_score += 20
            buy_reasons.append("Bullish CHoCH")

        else:
            sell_score += 20
            sell_reasons.append("Bearish CHoCH")

    # ======================
    # LIQUIDITY
    # ======================

    if liquidity:

        if liquidity["direction"] == "BUY":
            buy_score += 10
            buy_reasons.append("Liquidity Sweep")

        else:
            sell_score += 10
            sell_reasons.append("Liquidity Sweep")

    # ======================
    # FVG
    # ======================

    if fvg:

        if fvg["direction"] == "BUY":
            buy_score += 10
            buy_reasons.append("Bullish FVG")

        else:
            sell_score += 10
            sell_reasons.append("Bearish FVG")

    # ======================
    # ORDER BLOCK
    # ======================

    if order_block:

        if order_block["direction"] == "BUY":
            buy_score += 15
            buy_reasons.append("Bullish Order Block")

        else:
            sell_score += 15
            sell_reasons.append("Bearish Order Block")

    # ======================
    # ZONE
    # ======================

    if zone in ["Discount", "Deep Discount"]:
        buy_score += 10
        buy_reasons.append(zone)

    elif zone in ["Premium", "Deep Premium"]:
        sell_score += 10
        sell_reasons.append(zone)

    # ======================
    # BTC
    # ======================

    if btc:
        buy_score += 5
        sell_score += 5

    # ======================
    # VOLUME
    # ======================

    if volume:
        buy_score += 5
        sell_score += 5

    # ======================
    # FINAL
    # ======================

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

    score = min(score, 100)

    if score >= 80:
        quality = "A"

    elif score >= 65:
        quality = "B"

    elif score >= 50:
        quality = "C"

    else:
        quality = "NO TRADE"

    return {
        "direction": direction,
        "score": score,
        "quality": quality,
        "reasons": reasons
    }
