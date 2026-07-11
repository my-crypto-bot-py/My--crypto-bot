import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bot is running!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        try:
            json_str = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_str)
            bot.process_new_updates([update])
            return '', 200
        except Exception as e:
            return str(e), 500
    return 'Forbidden', 403

if __name__ == "__main__":
    # Local development ke liye
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
