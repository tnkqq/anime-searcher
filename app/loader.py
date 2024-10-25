import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv("BOT_TOKEN"))

url = "redis://redis:6379/0"

storage = RedisStorage.from_url(url)

bot = Bot(
    token=TOKEN,
)


dp = Dispatcher(
    bot=bot,
    storage=storage,
)
