from urllib.parse import urlparse

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from services import service_selector

submit_router = Router()


@submit_router.message(Command("submit"))
async def submit_handler(message: types.Message, state: FSMContext) -> None:
    try:
        _, link = message.html_text.split(" ")

        parsed_url = urlparse(link)
        domain = parsed_url.netloc

        if not domain:
            await message.reply("Проверьте ссылку на правильность")
            return

        service = service_selector[domain]()

        file_id = message.document.file_id
        file = await message.bot.get_file(file_id)
        iostream = await message.bot.download_file(file.file_path)

        await message.reply("Вы успешно загрузили решение")
        result = await service.submit(link, iostream)
        await message.reply(str(result))
    except (ValueError, AttributeError):
        await message.reply("Запрос неправильный, воспользуйтесь /help чтобы узнать как правильно")
    except KeyError:
        await message.reply("Такого сервиса нет в системе")
