from config import SYMBOLS
from market import get_market_data
from trend import detect_trend


def scan_market():

    results = []

    for symbol in SYMBOLS:

        try:

            df = get_market_data(symbol, "4H")

            if df is None or df.empty:
                continue

            trend = detect_trend(df)

            results.append({
                "symbol": symbol,
                "trend": trend["trend"],
                "strength": trend["strength"]
            })

        except Exception as e:
            print(symbol, e)

    return results


def get_best_symbol():

    data = scan_market()

    bullish = [
        x for x in data
        if x["trend"] == "BULLISH"
    ]

    if bullish:

        return bullish[0]

    return None
