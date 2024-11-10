from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config import settings


TOKEN = settings.BOT_TOKEN

url = "redis://redis:6379/0"

storage = RedisStorage.from_url(url)

bot = Bot(
    token=TOKEN,
)


dp = Dispatcher(
    bot=bot,
    storage=storage,
)
