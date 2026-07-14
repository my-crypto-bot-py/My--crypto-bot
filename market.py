import os
import requests
import pandas as pd

COINGLASS_API_KEY = os.environ.get("COINGLASS_API_KEY")

HEADERS = {
    "CG-API-KEY": COINGLASS_API_KEY,
    "Accept": "application/json"
}


def get_market_data(symbol="BTCUSDT"):
    """
    Future market data.
    फिलहाल CoinGlass Free API पर test करेंगे.
    बाद में KuCoin / OKX / Paid CoinGlass आसानी से add होंगे.
    """

    try:

        url = "https://open-api-v4.coinglass.com/api/futures/open-interest/history"

        params = {
            "symbol": symbol,
            "interval": "5m",
            "limit": 50
        }

        r = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=20
        )

        print("Status:", r.status_code)

        if r.status_code != 200:
            print(r.text)
            return None

        return r.json()

    except Exception as e:
        print(e)
        return None
