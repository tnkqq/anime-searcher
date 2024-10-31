import asyncio
import logging
import os
import sys

from aiogram import Dispatcher
from loader import bot, dp


sys.path.insert(1, os.path.join(sys.path[0], ".."))


async def main(Dispatcher):
    from handlers import callback_handlers, commands_handlers, message_handlers

    await dp.start_polling(bot)


if __name__ == "__main__":
    from loader import dp

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(Dispatcher))
