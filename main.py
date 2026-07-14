import os
import telebot
from market import get_liquidation_data

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Error: TOKEN or CHAT_ID missing!")
    exit()

bot = telebot.TeleBot(TOKEN)

def run():
    try:
        print(f"Testing connection to CHAT_ID: {CHAT_ID}")

        # CoinGlass API Test
        data = get_liquidation_data("BTCUSDT")

        bot.send_message(
            int(CHAT_ID),
            f"✅ Bot Online\n\nCoinGlass API Connected Successfully\n\nResponse:\n{str(data)[:500]}"
        )

        print("Success!")

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(
            int(CHAT_ID),
            f"❌ Error:\n{e}"
        )

if __name__ == "__main__":
    run()
