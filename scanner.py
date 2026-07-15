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

            strength = trend.get("strength", 0)

            results.append({
                "symbol": symbol,
                "trend": trend.get("trend", "UNKNOWN"),
                "strength": strength
            })

        except Exception as e:
            print(symbol, e)

    results = sorted(
        results,
        key=lambda x: x["strength"],
        reverse=True
    )

    return results


def get_best_symbol():

    data = scan_market()

    if len(data) == 0:
        return None

    print("Scanner Results:")

    for coin in data:
        print(
            coin["symbol"],
            coin["trend"],
            coin["strength"]
        )

    # Sabse strong coin return karega
    return data[0]
