import os
import requests
import pandas as pd

COINGLASS_API_KEY = os.environ.get("COINGLASS_API_KEY")

HEADERS = {
    "CG-API-KEY": COINGLASS_API_KEY
}


def get_liquidation_data(symbol="BTCUSDT"):
    url = "https://open-api-v4.coinglass.com/api/futures/liquidation/pair-history"

    params = {
        "exchange": "Binance",
        "symbol": symbol,
        "interval": "5m",
        "limit": 20
    }

    r = requests.get(url, headers=HEADERS, params=params, timeout=15)

    if r.status_code != 200:
        raise Exception(f"CoinGlass Error {r.status_code}: {r.text}")

    return r.json()
