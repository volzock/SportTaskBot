from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.orm import Session

from database import db, User
from docmaster import docmaster

start_router = Router()  # [1]


def init_keyboard() -> types.ReplyKeyboardMarkup:  # List[types.KeyboardButton]:
    helper = types.KeyboardButton(text="help")
    user_info = types.KeyboardButton(text="/get_user_info")
    return types.ReplyKeyboardMarkup(keyboard=[[helper, user_info]])


class Form(StatesGroup):
    fullname = State()


@docmaster.docs(name="/start", description="Starting Bot. If user telegram id is not in database, bot "
                                           "requires name and secondname from user, delimiter = ' '", role='user')
@start_router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext) -> None:
    keyboard = init_keyboard()

    await message.reply("Это бот МТУСИ кружка по спортивному программированию "
                                      "для отправки кода на различные проверяющие системы\n"
                                      "После регистрации ознакомьтесь с командой /help", reply_markup=keyboard)
    with Session(db) as session:
        if session.query(User).filter_by(telegram_id=int(message.from_user.id)).first() is None:
            await state.set_state(Form.fullname)
            await message.reply("Для регистрации ведите сначало фамилию, затем имя через пробел")
        else:
            await message.reply("Вы уже зарегестрированы")


@start_router.message(Form.fullname)
async def process_name(message: Message, state: FSMContext) -> None:
    try:
        surname, name = message.text.split()
        await message.reply(f"Привет {surname} {name}!")
        with Session(db) as session:
            user = User(telegram_id=int(message.from_user.id), name=name, surname=surname)
            session.add(user)
            session.commit()
    except ValueError:
        await state.set_state(Form.fullname)
        await message.reply("Ошибка ввода, попробуйте еще раз!")
