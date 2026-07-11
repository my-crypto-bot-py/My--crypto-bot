import os
import telebot

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bot is running in Polling Mode!")

print("Bot is polling...")
# Bracket band kar diya aur timeout set kar diya taaki connection loose na ho
bot.infinity_polling(timeout=60, long_polling_timeout=60)
