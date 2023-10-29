import telebot
from telebot import types
import os

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, "Это бот МТУСИ кружка по спортивному программированию "
                                      "для отправки кода на различные проверяющие системы")
    bot.send_message(message.chat.id, "Введите сначало имя, затем фамилию через пробел")
    name = ""
    surname = ""

    @bot.message_handler(content_types=['text'])
    def init_name(message):
        name, surname = message.text.split()
        bot.send_message(message.chat.id, f"Привет {surname} {name}")


@bot.message_handler(commands=['help'])
def help_func(message):
    pass
    bot.send_message(message.chat.id, "")


if __name__ == "__main__":
    bot.infinity_polling()
