import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

# Отримання токена бота з змінної середовища
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Додавання middleware для логування
dp.middleware.setup(LoggingMiddleware())

# Обробник команди /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привіт! Це тестовий бот на aiogram!")

# Обробник всіх текстових повідомлень
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(f"Ти написав: {message.text}")

# Основна функція для запуску бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
