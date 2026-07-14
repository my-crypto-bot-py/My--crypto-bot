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

    message = f"""
🚀 TRADING SIGNAL

Direction: {data.get('signal')}
Entry: {data.get('entry')}
SL: {data.get('sl')}

TP1: {data.get('tp1')}
TP2: {data.get('tp2')}

Score: {data.get('score')}

Reasons:
{data.get('reasons')}
"""

    try:
        print("Sending message to Telegram...")
        print("CHAT_ID:", CHAT_ID)

        result = bot.send_message(int(CHAT_ID), message)

        print("Telegram Success")
        print(result)

    except Exception as e:
        print("Telegram Failed")
        print(e)
        raise
