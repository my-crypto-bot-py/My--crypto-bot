import os
import telebot

# Sirf credentials aur basic connection check
TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if not TOKEN or not CHAT_ID:
    print("Error: TOKEN or CHAT_ID missing!")
    exit()

bot = telebot.TeleBot(TOKEN)

def test_connection():
    try:
        print(f"Testing connection to CHAT_ID: {CHAT_ID}")
        bot.send_message(int(CHAT_ID), "✅ Base Connection Test: Success!")
        print("Test Message sent successfully.")
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    test_connection()
# --- AUTOMATION & COMMANDS (Paste this at the end of your file) ---

import schedule
import time

# 1. /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Bot is active and running! You will receive updates every hour.")

# 2. Hourly Scheduled Task
def hourly_update():
    print("Running scheduled hourly update...")
    generate_and_send() # Yeh aapka pehle wala function hai

# 3. Background Threading for Polling (Command Handling)
def run_bot_polling():
    print("Bot polling started in background...")
    bot.polling(none_stop=True)

# 4. Main Execution Block
if __name__ == "__main__":
    # Schedule hourly task
    schedule.every(1).hours.do(hourly_update)
    
    # Start polling in a separate thread so it doesn't block the scheduler
    import threading
    polling_thread = threading.Thread(target=run_bot_polling)
    polling_thread.start()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
