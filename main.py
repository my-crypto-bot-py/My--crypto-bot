import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

WEBHOOK_URL = "https://easygoing-possibility-production.up.railway.app"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def index():
    return "Bot is running", 200

if __name__ == "__main__":
    # Webhook sirf tab set hoga agar aap local run karenge
    # Production (Gunicorn) mein ise manually Telegram se set karna best hai
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
