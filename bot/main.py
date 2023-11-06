import telebot
from sqlalchemy.orm import Session
from telebot import types
import os
from BotDB import *

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
db = create_engine("sqlite+pysqlite:///database")
Base.metadata.create_all(db)


class Docmaster:
    _docs = None

    def __init__(self):
        self._docs = []

    def docs(self, name, description, role):
        self._docs.append({"name": name, "description": description, "role": role})

        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator


docs = Docmaster()


@docs.docs(name="/start", description="Starting Bot. If user telegram id is not in database, bot"
                                      "requires name and secondname from user, delimiter = ' '", role='All')
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
        # db.insert_into_table(User, [{'telegram_id': int(message.from_user.id), 'name': name, 'surname': sname}])
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка ввода!")


# @bot.message_handler(commands=['help'])
# def help_func(message):


if __name__ == "__main__":
    bot.infinity_polling()
