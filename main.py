import os
import telebot
from market import get_market_data

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("❌ TELEGRAM_TOKEN ya CHAT_ID missing!")
    exit()

bot = telebot.TeleBot(TOKEN)


def run():

    try:

        df = get_market_data("BTC-USDT-SWAP", "5m")

        if df is None or df.empty:
            bot.send_message(
                int(CHAT_ID),
                "❌ OKX Market Data Fetch Failed."
            )
            return

        last = df.iloc[-1]

        message = f"""
✅ OKX Connected

BTC-USDT-SWAP (5m)

Time: {last['time']}
Open: {last['open']}
High: {last['high']}
Low: {last['low']}
Close: {last['close']}
Volume: {last['volume']}
"""

        bot.send_message(int(CHAT_ID), message)

        print("Success")

    except Exception as e:

        print(e)

        bot.send_message(
            int(CHAT_ID),
            f"❌ Error:\n{e}"
        )


if __name__ == "__main__":
    run()
