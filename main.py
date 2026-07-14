import os
from market import get_liquidation_data
from telegram_bot import send_signal


def run_bot():

    try:
        data = get_liquidation_data("BTCUSDT")

        print(data)

        send_signal({
            "signal": "COINGLASS TEST",
            "entry": "-",
            "sl": "-",
            "tp1": "-",
            "tp2": "-",
            "score": "10/10",
            "reasons": "CoinGlass API Connected Successfully"
        })

    except Exception as e:
        print(e)


if __name__ == "__main__":
    run_bot()
