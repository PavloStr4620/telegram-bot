import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

# Ініціалізація бота та диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

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
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
