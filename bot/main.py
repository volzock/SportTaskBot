import telebot
from telebot import types
import os

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])

@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id,"Это бот МТУСИ кружка по спортивному программированию "
                                     "для отправки кода на различные проверяющие системы")


@bot.message_handler(commands=['help'])
def help_func(message):
    #TODO Help func
    pass
    bot.send_message(message.chat.id,"")


if __name__ == "__main__":
    bot.infinity_polling()