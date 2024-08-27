import os
import logging
import sys
import asyncio
from dotenv import load_dotenv


from database.db import init_db

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def run_parser_span():
    print('запуск парсера')

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
scheduller = AsyncIOScheduler()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Ну привет мой маленький любитель поучиться!')

# async def on_startup():
#     scheduller.add_job(run_parser_span, 'cron', day=1, hour=0, minute=0)
#     scheduller.start()

async def main() -> None:
    await init_db()
    # await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())