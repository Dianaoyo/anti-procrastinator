import asyncio
import logging
from aiogram import Dispatcher, Bot
import keyb as kb
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiosqlite
from handlers import user
from datab import user_profiles_db

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()

dp.include_router(user)

debug_mode = False


# async def reminder(user_id):
#     await bot.send_message(chat_id=user_id, text='are you going to achieve something?', reply_markup=kb.menu)
#
# async def main():
#     await user_profiles_db()
#     scheduler = AsyncIOScheduler()
#     scheduler.add_job(reminder, 'interval', minutes=20)
#     scheduler.start()
#     if debug_mode:
#         await reminder()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())