import requests
import pandas as pd


def get_market_data(symbol="BTC-USDT-SWAP", timeframe="5m", limit=300):

    url = "https://www.okx.com/api/v5/market/candles"

    params = {
        "instId": symbol,
        "bar": timeframe,
        "limit": limit
    }

    try:

        response = requests.get(url, params=params, timeout=20)

        data = response.json()

        if data.get("code") != "0":
            print("OKX Error:", data)
            return None

        candles = data["data"]

        if not candles:
            return None

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

        df = df[[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]]

        df["time"] = pd.to_datetime(
            df["time"].astype("int64"),
            unit="ms"
        )

        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = df[col].astype(float)

        df = df.sort_values("time").reset_index(drop=True)

        return df

    except Exception as e:
        print("Market Error:", e)
        return None


def get_multi_timeframe_data(symbol="BTC-USDT-SWAP"):

    return {
        "1D": get_market_data(symbol, "1D", 300),
        "4H": get_market_data(symbol, "4H", 300),
        "1H": get_market_data(symbol, "1H", 300),
        "30m": get_market_data(symbol, "30m", 300),
        "15m": get_market_data(symbol, "15m", 300),
        "5m": get_market_data(symbol, "5m", 300),
    }
