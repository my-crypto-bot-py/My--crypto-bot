import os
import telebot

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bot is running in Polling Mode!")

# Infinite polling: Bot kabhi band nahi hoga, Railway bas script chalaye rakhega
print("Bot is polling...")
bot.infinity_polling()
