from dotenv import load_dotenv
import os
import asyncio

from aiogram import Bot, Dispatcher
from handlers import router

load_dotenv()

TOKEN = os.getenv("TOKEN")

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is switched off.")
