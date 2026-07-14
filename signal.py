
def calculate_rr(entry, sl, risk_reward=3):
    """
    Risk Reward calculate karta hai.
    """

    risk = abs(entry - sl)

    if risk == 0:
        return None

    if entry > sl:
        tp = entry + (risk * risk_reward)
    else:
        tp = entry - (risk * risk_reward)

    return tp


def generate_signal(
    structure,
    liquidity,
    fvg,
    order_block,
    zone,
    entry,
    sl
):
    """
    Sab confirmations ko combine karke signal banata hai.
    """

    score = 0
    reasons = []

    # Structure
    if structure:
        score += 1
        reasons.append(structure["type"])

    # Liquidity
    if liquidity:
        score += 1
        reasons.append(liquidity["type"])

    # FVG
    if fvg:
        score += 1
        reasons.append(fvg["type"])

    # Order Block
    if order_block:
        score += 1
        reasons.append(order_block["type"])

    # Zone
    if zone:
        score += 1
        reasons.append(zone["zone"])

    if score < 4:
        return {
            "signal": "NO TRADE",
            "score": score,
            "reasons": reasons
        }

    if "Bullish" in str(reasons):
        direction = "BUY"
    else:
        direction = "SELL"

    tp1 = calculate_rr(entry, sl, 3)
    tp2 = calculate_rr(entry, sl, 4)

    return {
        "signal": direction,
        "entry": entry,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "score": score,
        "reasons": reasons
    }
