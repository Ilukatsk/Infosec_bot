import random
import datetime
import logging
import pytz
from database.db_control import getusers
from aiogram.methods.send_message import SendMessage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Router, types
from handlers.main_keyboard_handler import fl, holidays
from aiogram import Bot

router = Router()

async def send_text(bot : Bot):
    try:
        users = getusers('./database/data.db', "bot_users")
        txt = random.choice(fl)
        for id in users:
            try:
                await bot.send_message(chat_id=id[0], text=txt)
                today_date = datetime.datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d-%m")
                if today_date in holidays:
                    await bot.send_message(chat_id=id[0], text=("Ура, день не пройдет зря, так как сегодня празднуется " + holidays[today_date].split("-")[1].strip()))
            except:
                logging.info("Bot is blocked by the user {}".format(id[0]))
        logging.info("Sent daily advice and holiday to all bot users")
    except Exception as e:
        logging.exception("An error has occurred while trying to send a daily advice: %s", e)
    

    