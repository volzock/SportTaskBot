import logging
import os

from aiogram import Bot, Dispatcher
from routers import *


def main():
    token = os.environ.get("BOT_TOKEN")

    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(start_router)

    dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
