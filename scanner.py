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

            direction = trend.get("trend", "UNKNOWN")
            strength = trend.get("strength", 0)

            # Sideways ignore
            if direction == "SIDEWAYS":
                continue

            results.append({
                "symbol": symbol,
                "trend": direction,
                "strength": strength
            })

        except Exception as e:
            print(symbol, e)

    # Strongest first
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
            f'{coin["symbol"]} | '
            f'{coin["trend"]} | '
            f'{coin["strength"]}'
        )

    print("=============================\n")

    return data[0]
