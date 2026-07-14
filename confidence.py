def calculate_confidence(
    bias=False,
    trend=False,
    bos=False,
    choch=False,
    mss=False,
    liquidity=False,
    fvg=False,
    order_block=False,
    btc=False,
    volume=False
):
    score = 0
    reasons = []

    if bias:
        score += 15
        reasons.append("1D Bias")

    if trend:
        score += 15
        reasons.append("4H Trend")

    if bos:
        score += 10
        reasons.append("BOS")

    if choch:
        score += 10
        reasons.append("CHoCH")

    if mss:
        score += 10
        reasons.append("MSS")

    if liquidity:
        score += 10
        reasons.append("Liquidity Sweep")

    if fvg:
        score += 10
        reasons.append("FVG")

    if order_block:
        score += 10
        reasons.append("Order Block")

    if btc:
        score += 5
        reasons.append("BTC Confirmation")

    if volume:
        score += 5
        reasons.append("Volume Confirmation")

    if score >= 90:
        quality = "A+"
    elif score >= 80:
        quality = "A"
    elif score >= 70:
        quality = "B"
    else:
        quality = "NO TRADE"

    return {
        "score": score,
        "quality": quality,
        "reasons": reasons
    }
