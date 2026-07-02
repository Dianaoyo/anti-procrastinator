# <<<<<<< HEAD
import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import keyb as kb
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiosqlite
from handlers import user
from datab import user_profiles_db, get_user_facts, get_user_stats
from lang import transl

logging.basicConfig(level=logging.INFO)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()
token = os.getenv("BOT_TOKEN")
bot = Bot(token=token)
dp = Dispatcher()

dp = Dispatcher()
dp.include_router(user)
debug_mode = 0

async def text_in_lang(user_id, key:str):
    lang = await get_user_facts(user_id, 'language')
    text = transl[lang][key] or transl['ru'][key]
    return text

async def reminder(user_id):
    text = await text_in_lang(user_id, 'dont procrastinate')
    await bot.send_message(user_id, text, reply_markup= kb.menu)

async def water_reminder(user_id):
    text = await text_in_lang(user_id, 'water reminder')
    await bot.send_message(user_id, text)

async def stretch_reminder(user_id):
    text = await text_in_lang(user_id, 'stretch reminder')
    await bot.send_message(user_id, text)

async def main():
    await user_profiles_db()
    scheduler = AsyncIOScheduler()
    async with aiosqlite.connect('user_profiles.db') as db:
        async with db.execute('SELECT DISTINCT user_id FROM user_stats') as cursor:
            users = await cursor.fetchall()
            for row in users:
                user_id = row[0]
                if await get_user_stats(user_id, 'timer')=='OFF':
                    scheduler.add_job(reminder, 'interval', minutes=20, args=[user_id])

                if await get_user_stats(user_id, 'water reminder')=='ON':
                    scheduler.add_job(water_reminder(user_id), 'interval', minutes=90)

                if await get_user_stats(user_id, 'stretch reminder')=='ON':
                    scheduler.add_job(stretch_reminder(user_id), 'interval', minutes=60)

                if debug_mode:
                    await reminder(user_id)
                    await water_reminder(user_id)
                    await stretch_reminder(user_id)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())