фimport os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK = os.getenv("WEBHOOK_URL")
WEBHOOK_URL = f"{WEBHOOK}/{BOT_TOKEN}"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

# Вебхук
async def on_start():
    await bot.set_webhook(WEBHOOK_URL)

# Обробка команд
@dp.message_handler(commands=['qwe'])
async def handle_qwe(message: types.Message):
    # Використовуємо форматування без ParseMode
    await message.reply("Ваша команда була отримана!")

# Обробка запитів на вебхук
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = types.Update.parse_raw(json_str)
    dp.process_update(update)
    return "!", 200

# Домашня сторінка
@app.route('/')
def home():
    return "Bot is running!", 200

if __name__ == '__main__':
    # Налаштування вебхука перед запуском
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

    # Запуск Flask-сервера і aiogram webhook
    start_webhook(
        dispatcher=dp,
        webhook_path=f'/{BOT_TOKEN}',
        on_start=on_start,
        host="0.0.0.0",
        port=5000,
    )
