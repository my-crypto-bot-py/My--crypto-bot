from market import get_market_data


def get_daily_bias(symbol):

    df = get_market_data(symbol, "1D")

    if df is None or len(df) < 30:
        return "UNKNOWN"

    highs = df["high"].tolist()
    lows = df["low"].tolist()

    last_high = max(highs[-10:])
    prev_high = max(highs[-20:-10])

    last_low = min(lows[-10:])
    prev_low = min(lows[-20:-10])

    if last_high > prev_high and last_low > prev_low:
        return "BULLISH"

    elif last_high < prev_high and last_low < prev_low:
        return "BEARISH"

    return "SIDEWAYS"
