import telebot
from sqlalchemy.orm import Session
from sqlalchemy import select
from telebot import types, util
import os
from BotDB import *

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db = create_engine("sqlite+pysqlite:///database")
Base.metadata.create_all(db)


class Docmaster:
    __docs = None

    def __init__(self):
        self.__docs = []

    def docs(self, name, description, role):
        self.__docs.append({"name": name, "description": description, "role": role})

        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def print_user_funcs(self):
        res = ""
        for row in self.__docs:
            if row["role"] == "user":
                res += "<b>" + row["name"] + "</b>"
                res += ' - '
                res += row["description"]
                res += '\n'
        return res

    def print_admin_funcs(self):
        res = ""
        for row in self.__docs:
            res += "<b>" + row["name"] + "</b>"
            res += ' - '
            res += row["description"]
            res += '\n'
        return res


docums = Docmaster()


@docums.docs(name="/start", description="Starting Bot. If user telegram id is not in database, bot "
                                        "requires name and secondname from user, delimiter = ' '", role='user')
@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, "Это бот МТУСИ кружка по спортивному программированию "
                                      "для отправки кода на различные проверяющие системы")
    with Session(db) as session:
        if session.query(User).filter_by(telegram_id=int(message.from_user.id)).first() is None:
            msg = bot.send_message(message.chat.id, "Для регистрации ведите сначало имя, затем фамилию через пробел")
            bot.register_next_step_handler(msg, __register)


def __register(message):
    try:
        name, sname = message.text.split()
        bot.send_message(message.chat.id, f"Привет {name} {sname}!")
        with Session(db) as session:
            user = User(telegram_id=int(message.from_user.id), name=name, surname=sname)
            session.add(user)
            session.commit()
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка ввода!")


@bot.message_handler(commands=['get_user_info'])
def get_user_info(message):
    with Session(db) as session:
        if session.query(User).filter_by(telegram_id=int(message.from_user.id)).first() is not None:
            name, sname = [x for x in session.execute(select(User.name, User.surname)).first()]
            bot.send_message(message.chat.id, f"Ваше фамилия и имя: {sname} {name}")


@docums.docs(name="/help", description='Print description all func for your role', role='user')
@bot.message_handler(commands=['help'])
def help_func(message):
    # Проверка на роль пользователя
    if True:
        for row in util.smart_split(docums.print_user_funcs(), 3000):
            bot.send_message(message.chat.id, row, parse_mode='html')
    # else:
    #     for row in util.smart_split(docums.print_admin_funcs(), 3000):
    #         bot.send_message(message.chat.id, row, parse_mode='html')


if __name__ == "__main__":
    bot.infinity_polling()
