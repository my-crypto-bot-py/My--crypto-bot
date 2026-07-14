import os
import telebot
from market import get_market_data

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

def run():

    try:

        data = get_market_data("BTCUSDT")

        if data is None:
            bot.send_message(
                int(CHAT_ID),
                "❌ Market Data Fetch Failed."
            )
            return

        bot.send_message(
            int(CHAT_ID),
            f"✅ Market Connected\n\n{str(data)[:1000]}"
        )

        print("Success")

    except Exception as e:

        print(e)

        bot.send_message(
            int(CHAT_ID),
            f"❌ Error\n\n{e}"
        )


if __name__ == "__main__":
    run()
