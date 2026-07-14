import os
import telebot
from market import get_ohlcv

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("❌ TELEGRAM_TOKEN ya CHAT_ID missing!")
    exit()

bot = telebot.TeleBot(TOKEN)

def run_test():
    try:
        df = get_ohlcv("BTC/USDT", "5m")

        if df is None:
            bot.send_message(int(CHAT_ID), "❌ Binance Futures data fetch failed.")
            return

        last = df.iloc[-1]

        msg = (
            "✅ Binance Futures Connected\n\n"
            "BTC/USDT (5m)\n\n"
            f"Time: {last['time']}\n"
            f"Open: {last['open']}\n"
            f"High: {last['high']}\n"
            f"Low: {last['low']}\n"
            f"Close: {last['close']}\n"
            f"Volume: {last['volume']}"
        )

        bot.send_message(int(CHAT_ID), msg)

    except Exception as e:
        bot.send_message(int(CHAT_ID), f"❌ Error:\n{str(e)}")


if __name__ == "__main__":
    run_test()
