#Подключение библиотек
import telebot 
import config
from boltyshka import *

from telebot import types

bot = telebot.TeleBot(config.TOKEN) # создание объекта класса бот

#хрень с командами
@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('Stikers/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton('Я твой создатель👨🏼‍💻', callback_data='1')
    item2 = types.InlineKeyboardButton('Я его невеста👰🏻', callback_data='2')
    item3 = types.InlineKeyboardButton('Я знаю его и с тебя хватит на этом😏', callback_data='3')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 'Рад тебя, {0.first_name}, видеть!😍\nЯ - <b>{1.first_name}</b>☀️, создан рыжем программистом👨🏼‍💻, чтобы его невесте👰🏻 было не одиноко, когда он не в сети.\nКем ты приходишься для моего создателя?🤔'.format(message.from_user, bot.get_me()), 
        parse_mode='html',reply_markup=markup)

#хрень с сообщениями
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, pipe.predict([message.text.lower()])[0])

#ответы бота на приветствие
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '1':
                bot.send_message(call.message.chat.id, 'О, мой Повелитель!😇\nПришел редачить меня?😏\nХочу новые функции😢')
            elif call.data == '2':
                bot.send_message(call.message.chat.id, 'Оу-у-у, как долго я тебя ждал❤️\nВкраце:\n-Я первая версия1️⃣\n-Я умею здороваться👋\n-Умею нестичушь😜 но это же лучше, чем ничего?)))\n*напиши что угодно и мои ответы понесуться')
            elif call.data == '3':
                bot.send_message(call.message.chat.id, 'Вау, ну и дерзость😯\nЯ тебе ничего не расскажу, сам гадай!😡')

            #удаление inline сообщений
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))

#Запуск
bot.polling(none_stop=True)