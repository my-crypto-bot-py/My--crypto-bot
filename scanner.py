from config import SYMBOLS
from market import get_market_data, detect_trend


def scan_market():

    results = []

    for symbol in SYMBOLS:

        try:

            df = get_market_data(symbol, "4H")

            if df is None or df.empty:
                continue

            trend_data = detect_trend(df)

            direction = trend_data["trend"]
            strength = trend_data["strength"]

            if direction == "SIDEWAYS":
                continue

            results.append({

                "symbol": symbol,

                "trend": direction,

                "strength": strength

            })

        except Exception as e:

            print(symbol, e)

    results.sort(

        key=lambda x: x["strength"],

        reverse=True

    )

    return results


def get_best_symbol():

    data = scan_market()

    if not data:
        return None

    print("\n========== SCANNER ==========")

    for coin in data:

        print(

            coin["symbol"],

            coin["trend"],

            coin["strength"]

        )

    print("=============================\n")

    return data[0]
