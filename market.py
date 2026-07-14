import ccxt
import pandas as pd

exchange = ccxt.bybit({
    "enableRateLimit": True,
    "options": {
        "defaultType": "linear"
    }
})

def get_ohlcv(symbol, timeframe, limit=500):
    try:
        # Bybit symbol format
        symbol = symbol.replace("/", "")

        ohlcv = exchange.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit
        )

        df = pd.DataFrame(
            ohlcv,
            columns=[
                "time",
                "open",
                "high",
                "low",
                "close",
                "volume"
            ]
        )

        df["time"] = pd.to_datetime(df["time"], unit="ms")

        return df

    except Exception as e:
        print(f"[ERROR] {symbol} {timeframe}: {e}")
        raise
