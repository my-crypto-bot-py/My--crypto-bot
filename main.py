import os
import telebot

# GitHub Secrets se values fetch karein
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# Bot initialize karein
bot = telebot.TeleBot(TOKEN)

# Message bhejne ka logic
try:
    # Yahan aap apna liquidation logic add kar sakte hain
    message_text = "🚀 Liquidation Bot active hai aur check kar raha hai!"
    bot.send_message(CHAT_ID, message_text)
    print("Success: Message sent to Telegram!")
except Exception as e:
    print(f"Error: {e}")
