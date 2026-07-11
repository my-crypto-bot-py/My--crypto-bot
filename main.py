import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Railway variable se URL lein, hardcode na karein
WEBHOOK_URL = os.environ.get('WEBHOOK_URL') 

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        return '!', 403

@app.route('/')
def index():
    return "Bot is running", 200

# Gunicorn is file ko 'app' object ke liye use karega
