import logging

from aiogram import Bot, Dispatcher
from routers import *


def main():
    bot = Bot(token="2005031664:AAFoT5J8xmjsNFF-npDPlrEjS2viViMRtqQ")
    dp = Dispatcher()
    dp.include_router(start_router)

    dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
