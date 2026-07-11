import os
import telebot
from flask import Flask, request

# Railway Variables se TOKEN lein
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook URL setup
WEBHOOK_URL = "https://easygoing-possibility-production.up.railway.app"

# App start hote hi Webhook set ho jayega
bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/health')
def health():
    return "OK", 200

# Gunicorn is 'app' ko directly import karega
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
