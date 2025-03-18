import os
import telebot
from flask import Flask, request


BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK = os.getenv("WEBHOOK_URL")
WEBHOOK_URL = f"{WEBHOOK}/{BOT_TOKEN}"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    print(f"Вебхук: {WEBHOOK_URL}")
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    print(update)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(commands=['start'])
def start_command(message):
    print(f"Start command received from {message.from_user.username}")
    bot.reply_to(message, "Hello, welcome to the bot!")


@app.route('/')
def home():
    return "Bot is running!", 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=5000)
