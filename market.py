import requests
import pandas as pd


def get_market_data(symbol="BTC-USDT-SWAP", timeframe="5m", limit=100):

    url = "https://www.okx.com/api/v5/market/candles"

    params = {
        "instId": symbol,
        "bar": timeframe,
        "limit": limit
    }

    try:

        r = requests.get(url, params=params, timeout=20)

        data = r.json()

        if data.get("code") != "0":
            print(data)
            return None

        candles = data["data"]

        df = pd.DataFrame(
            candles,
            columns=[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "volCcy",
                "volCcyQuote",
                "confirm"
            ]
        )

        df = df[["time", "open", "high", "low", "close", "volume"]]

        df["time"] = pd.to_datetime(df["time"].astype("int64"), unit="ms")

        df = df.astype({
            "open": float,
            "high": float,
            "low": float,
            "close": float,
            "volume": float
        })

        df = df.sort_values("time")

        return df

    except Exception as e:
        print(e)
        return None
