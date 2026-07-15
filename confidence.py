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

    checks = [
        (bias, 15, "1D Bias"),
        (trend, 15, "4H Trend"),
        (bos, 10, "BOS"),
        (choch, 10, "CHoCH"),
        (mss, 10, "MSS"),
        (liquidity, 10, "Liquidity Sweep"),
        (fvg, 10, "FVG"),
        (order_block, 10, "Order Block"),
        (btc, 5, "BTC Confirmation"),
        (volume, 5, "Volume Confirmation"),
    ]

    for condition, points, reason in checks:
        if condition:
            score += points
            reasons.append(reason)

    score = min(score, 100)

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
