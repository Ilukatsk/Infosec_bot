import asyncio
import aioschedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.methods.send_message import SendMessage
import logging
from database.db_control import adduser, removeuser, getusers
import stuff
from handlers import command_handler, main_keyboard_handler

import asyncio
from aiogram import Bot, Dispatcher, types, Router

logging.basicConfig(level=logging.INFO, filename=".\logs\main.log", format='%(name)s :: %(asctime)s :: %(levelname)s :: %(message)s')


async def scheduler(bot : Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(stuff.send_text, trigger='cron', args=[bot], hour=6, minute=22)
    scheduler.start()

async def on_startup(bot : Bot):
    asyncio.create_task(scheduler(bot))

async def main():
    bot = Bot('')
    dp = Dispatcher()
    dp.include_routers(command_handler.router, main_keyboard_handler.router, stuff.router)
    await on_startup(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




