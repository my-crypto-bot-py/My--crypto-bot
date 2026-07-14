import os
import telebot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = telebot.TeleBot(TOKEN)

def send_signal(data):
    if not CHAT_ID:
        return

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

    bot.send_message(int(CHAT_ID), message)
