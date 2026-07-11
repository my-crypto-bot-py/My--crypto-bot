from flask import Flask, request
import telebot
import os

TOKEN = os.environ.get('TOKEN')
# Is baat ka dhyan rakhein ki Railway Variables mein TOKEN sahi se save ho
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/health')
def health():
    return "OK", 200

# Gunicorn ke liye 'app' variable chahiye hota hai
# Webhook set karne ka kaam hum alag se karenge
if __name__ == "__main__":
    WEBHOOK_URL = "https://easygoing-possibility-production.up.railway.app" 
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
