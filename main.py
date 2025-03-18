import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import os

from apiary import create_apiary, check_beehive_exists, view_apiary
from jwt_token import *
from login import process_login
from registration import process_registration
from app import keep_alive

keep_alive()
# SERVER_URL = "https://smart-beehive-server.onrender.com/getdata"
# SERVER_CREATE_APIARY = "https://smart-beehive-server.onrender.com/api/"
BOT_TOKEN = os.environ.get("BOT_TOKEN")

last_data = None
creating_apiary = False  # блокування кнопок під час створення пасіки

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    # builder = InlineKeyboardBuilder()
    await message.answer("Ласкаво просимо!")

    # if get_token(chat_id) is None:
    #     builder.button(text='Вхід', callback_data='login')
    #     builder.button(text='Реєстрація', callback_data='registration')
    # else:
    #     if check_beehive_exists():
    #         builder.button(text='Переглянути пасіку', callback_data='view_apiary')
    #         builder.button(text='Створити пасіку', callback_data='create_apiary')
    #     else:
    #         builder.button(text='Створити пасіку', callback_data='create_apiary')

    # await message.answer("Ласкаво просимо!", reply_markup=builder.as_markup())


# @dp.callback_query(F.data.in_(['login', 'registration', 'create_apiary', 'view_apiary', 'back_in_menu']))
# async def callback_handler(call: types.CallbackQuery):
#     chat_id = call.message.chat.id
#     message_id = call.message.message_id

#     if call.data == 'login':
#         await bot.delete_message(chat_id, message_id)
#         await process_login(call.message)
#     elif call.data == 'registration':
#         await bot.delete_message(chat_id, message_id)
#         await process_registration(call.message)
#     elif call.data == 'create_apiary':
#         await bot.delete_message(chat_id, message_id)
#         await create_apiary(call.message)
#     elif call.data == 'view_apiary':
#         await bot.delete_message(chat_id, message_id)
#         await view_apiary(call.message)
#     elif call.data == 'back_in_menu':
#         await bot.delete_message(chat_id, message_id)
#         await send_welcome(call.message)
#     await call.answer() # Important to answer callback queries

async def main():
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
