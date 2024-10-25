import asyncio
import logging
import sys

from aiogram import Dispatcher
from loader import bot, dp


async def main(Dispatcher):
    from handlers import commands_handlers, callback_handlers, message_handlers

    await dp.start_polling(bot)


if __name__ == "__main__":
    from loader import dp

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main(Dispatcher))
