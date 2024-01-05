import logging
import os

from aiogram import Bot, Dispatcher, Router
import routers


def add_routers(dp: Dispatcher):
    router_type = type(Router())
    for name in dir(routers):
        probably_router = getattr(routers, name)
        if type(probably_router) == router_type:
            dp.include_router(probably_router)


def main():
    token = os.environ.get("BOT_TOKEN")

    bot = Bot(token=token)
    dp = Dispatcher()

    add_routers(dp)

    dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
