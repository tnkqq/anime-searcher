import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv("BOT_TOKEN"))

bot = Bot(
    token=TOKEN,
)


dp = Dispatcher(
    bot=bot,
)
