import os
import telebot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TOKEN:
    raise Exception("TELEGRAM_TOKEN missing!")

if not CHAT_ID:
    raise Exception("CHAT_ID missing!")

bot = telebot.TeleBot(TOKEN)


def send_signal(data):

    reasons = data.get("reasons", "")
    reasons = reasons.replace(", ", "\n✔ ")

    message = f"""
🚀 SMART MONEY SIGNAL

🪙 Symbol: {data.get("symbol", "N/A")}

📈 Direction: {data.get("signal", "N/A")}
📊 Trend: {data.get("trend", "N/A")}
📍 Zone: {data.get("zone", "N/A")}

🎯 Entry: {data.get("entry", "N/A")}
🛑 Stop Loss: {data.get("sl", "N/A")}

✅ TP1: {data.get("tp1", "N/A")}
✅ TP2: {data.get("tp2", "N/A")}

🔥 Confidence: {data.get("score", "N/A")}%

📋 Reasons:
✔ {reasons}
"""

    try:
        print("Sending message to Telegram...")
        print("CHAT_ID:", CHAT_ID)
        print("Symbol:", data.get("symbol"))
        print("Trend:", data.get("trend"))
        print("Zone:", data.get("zone"))

        result = bot.send_message(int(CHAT_ID), message)

        print("Telegram Success")
        print(result)

    except Exception as e:
        print("Telegram Failed")
        print(e)
        raise
