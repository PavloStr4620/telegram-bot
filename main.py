import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time

from apiary import create_apiary, check_beehive_exists, view_apiary
from jwt_token import *
from telebot import types
from login import process_login
from registration import process_registration
from bot_config import bot

SERVER_URL = "https://smart-beehive-server.onrender.com/getdata"
SERVER_CREATE_APIARY = "https://smart-beehive-server.onrender.com/api/"

last_data = None
creating_apiary = False  # блокування кнопок під час створення пасіки


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()

    if get_token(chat_id) is None:
        markup.add(types.InlineKeyboardButton('Вхід', callback_data='login'))
        markup.add(types.InlineKeyboardButton(
            'Реєстрація', callback_data='registration'))

    else:
        if check_beehive_exists():
            markup.add(types.InlineKeyboardButton(
                'Переглянути пасіку', callback_data='view_apiary'))
            markup.add(types.InlineKeyboardButton(
                'Створити пасіку', callback_data='create_apiary'))
        else:
            markup.add(types.InlineKeyboardButton(
                'Створити пасіку', callback_data='create_apiary'))

    bot.send_message(chat_id, "Ласкаво просимо!", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda call: call.data in ['login', 'registration', 'create_apiary', 'view_apiary', 'back_in_menu'])
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'login':
        bot.delete_message(chat_id, message_id)
        process_login(call.message)
    elif call.data == 'registration':
        bot.delete_message(chat_id, message_id)
        process_registration(call.message)
    elif call.data == 'create_apiary':
        # todo 5 Добавити заборону натискати кнопки коли вибрано варіант "Створити пасіку"
        bot.delete_message(chat_id, message_id)
        create_apiary(call.message)
    elif call.data == 'view_apiary':
        bot.delete_message(chat_id, message_id)
        view_apiary(call.message)
    elif call.data == 'back_in_menu':
        bot.delete_message(chat_id, message_id)
        send_welcome(call.message)


if __name__ == "__main__":
    print("Бот запущено...")
    bot.delete_webhook()
    bot.polling(none_stop=True)

# import os
# import json
# from flask import Flask, request
# from telebot import TeleBot, types
#
# # Завантаження змінних середовища
# TOKEN = "7967723128:AAGgP1d1FyuZYxdfPd45d1t081TfNDOECPQ"
# WEBHOOK_URL = "https://smart-beehive-telegram-bot.onrender.com"
# WEBHOOK_PATH = f"/webhook/{TOKEN}"
#
# # Ініціалізація бота
# bot = TeleBot(TOKEN)
#
# app = Flask(__name__)
#
#
# @app.route('/webhook', methods=['POST'])
# def webhook():
#     print(f"🔑 BOT_TOKEN: {TOKEN}, webhook {WEBHOOK_URL}")  # Лог для перевірки
#
#     print("🔥 Запит на /webhook отримано")
#     try:
#         json_str = request.get_data().decode('UTF-8')
#         print(f"📩 Отримано запит: {json_str}")
#
#         update = types.Update.de_json(json_str)
#         print(f"🔄 Декодоване оновлення: {update}")  # Лог оновлення
#
#         print("✅ Обробка оновлення...")  # Лог перед передачею оновлення в бот
#         bot.process_new_updates([update])
#         print(f"✅ Оновлення передано боту")
#
#         return 'OK', 200
#     except Exception as e:
#         print(f"❌ Помилка: {e}")
#         return 'Internal Server Error', 500
#
#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     chat_id = message.chat.id
#     print(f"📬 Надсилаю привітальне повідомлення до чату {chat_id}")  # Логування
#
#     try:
#         bot.send_chat_action(chat_id, "Привіт! Це тестове повідомлення.")
#         print("✅ Повідомлення надіслано")
#     except Exception as e:
#         print(f"❌ Помилка при надсиланні повідомлення: {e}")
#
# if __name__ == "__main__":
#     print("✅ Запуск Flask-сервера...")
#
#     # Встановлення вебхука
#     bot.remove_webhook()
#     bot.set_webhook(url=f"{WEBHOOK_URL}")
#
#     port = int(os.environ.get("PORT", 10000))  # Використовуємо змінну середовища PORT
#     app.run(host="0.0.0.0", port=port)

# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     print(f"🚀 Отримано команду /start від {message.chat.id}")
#     chat_id = message.chat.id
#     markup = types.InlineKeyboardMarkup()

#     bot.send_message(chat_id, "Ласкаво просимо!")

#     if get_token(chat_id) is None:
#         markup.add(types.InlineKeyboardButton('Вхід', callback_data='login'))
#         markup.add(types.InlineKeyboardButton('Реєстрація', callback_data='registration'))
#     else:
#         if check_beehive_exists(chat_id):  # Передаємо chat_id
#             markup.add(types.InlineKeyboardButton('Переглянути пасіку', callback_data='view_apiary'))
#             markup.add(types.InlineKeyboardButton('Створити пасіку', callback_data='create_apiary'))
#         else:
#             markup.add(types.InlineKeyboardButton('Створити пасіку', callback_data='create_apiary'))

#     bot.send_message(chat_id, "Виберіть опцію:", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data in ['login', 'registration', 'create_apiary', 'view_apiary', 'back_in_menu'])
# def callback_handler(call):
#     chat_id = call.message.chat.id
#     message_id = call.message.message_id
#
#     bot.delete_message(chat_id, message_id)
#
#     if call.data == 'login':
#         process_login(call.message)
#     elif call.data == 'registration':
#         process_registration(call.message)
#     elif call.data == 'create_apiary':
#         create_apiary(call.message)
#     elif call.data == 'view_apiary':
#         view_apiary(call.message)
#     elif call.data == 'back_in_menu':
#         send_welcome(call.message)



