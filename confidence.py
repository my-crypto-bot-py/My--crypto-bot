# ==========================
# CONFIDENCE ENGINE
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
    direction = None

    # ==========================
    # TREND
    # ==========================

    if trend == "BULLISH":

        score += 20
        direction = "BUY"
        reasons.append("4H Bullish Trend")

    elif trend == "BEARISH":

        score += 20
        direction = "SELL"
        reasons.append("4H Bearish Trend")

    # ==========================
    # BOS
    # ==========================

    if bos:

        score += 15
        direction = bos["direction"]
        reasons.append(bos["type"])

    # ==========================
    # MSS
    # ==========================

    if mss:

        score += 15
        direction = mss["direction"]
        reasons.append(mss["type"])

    # ==========================
    # CHOCH
    # ==========================

    if choch:

        score += 10
        direction = choch["direction"]
        reasons.append(choch["type"])
            # ==========================
    # LIQUIDITY
    # ==========================

    if liquidity:

        score += 10
        direction = liquidity["direction"]
        reasons.append(liquidity["type"])

    # ==========================
    # FVG
    # ==========================

    if fvg:

        score += 10
        direction = fvg["direction"]
        reasons.append(fvg["type"])

    # ==========================
    # ORDER BLOCK
    # ==========================

    if order_block:

        score += 10
        direction = order_block["direction"]
        reasons.append(order_block["type"])

    # ==========================
    # DISPLACEMENT
    # ==========================

    if displacement:

        score += 5
        direction = displacement["direction"]
        reasons.append("Displacement")

    # ==========================
    # LIQUIDITY GRAB
    # ==========================

    if liquidity_grab:

        score += 5
        direction = liquidity_grab["direction"]
        reasons.append(liquidity_grab["type"])

    # ==========================
    # EQUAL LEVELS
    # ==========================

    if equal_levels:

        if equal_levels.get("equal_high"):
            score += 3
            reasons.append("Equal High")

        if equal_levels.get("equal_low"):
            score += 3
            reasons.append("Equal Low")

    # ==========================
    # PREMIUM / DISCOUNT
    # ==========================

    if zone:

        zone_name = zone["zone"]

        if direction == "BUY":

            if zone_name in ["Discount", "Deep Discount"]:
                score += 5
                reasons.append(zone_name)

        elif direction == "SELL":

            if zone_name in ["Premium", "Deep Premium"]:
                score += 5
                reasons.append(zone_name)

    # ==========================
    # BTC CONFIRMATION
    # ==========================

    if btc:

        score += 5
        reasons.append("BTC Confirmation")

    # ==========================
    # VOLUME CONFIRMATION
    # ==========================

    if volume:

        score += 4
        reasons.append("Volume Confirmation")
            # ==========================
    # SCORE LIMIT
    # ==========================

    if score > 100:
        score = 100

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
    # FINAL RETURN
    # ==========================

    return {

        "direction": direction,

        "score": score,

        "quality": quality,

        "reasons": reasons

    }
