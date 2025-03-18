import asyncio
from aiogram import Bot, Dispatcher
from main import dp, bot  # Імпорт dp та bot з main.py
import os

async def main():
    print("Бот запущено...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
