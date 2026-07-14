import pandas as pd


def run_backtest(df, signals):
    """
    Basic backtest engine.
    """

    total_trades = len(signals)

    wins = 0
    losses = 0

    total_rr = 0

    for trade in signals:

        entry = trade["entry"]
        sl = trade["sl"]
        tp = trade["tp1"]

        direction = trade["signal"]

        future = df[df["time"] > trade["time"]]

        result = None

        for _, candle in future.iterrows():

            if direction == "BUY":

                if candle["low"] <= sl:
                    result = "LOSS"
                    break

                if candle["high"] >= tp:
                    result = "WIN"
                    break

            elif direction == "SELL":

                if candle["high"] >= sl:
                    result = "LOSS"
                    break

                if candle["low"] <= tp:
                    result = "WIN"
                    break

        if result == "WIN":
            wins += 1
            total_rr += 3

        elif result == "LOSS":
            losses += 1

    if total_trades == 0:
        winrate = 0
    else:
        winrate = round((wins / total_trades) * 100, 2)

    return {
        "Total Trades": total_trades,
        "Wins": wins,
        "Losses": losses,
        "Win Rate": winrate,
        "Total RR": total_rr
    }
