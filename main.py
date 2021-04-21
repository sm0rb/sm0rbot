#Подключение библиотек
import telebot
from telebot import types
import sqlite3
#Подключение файлов
import config
import keyboars as k
from boltyshka import *

bot = telebot.TeleBot(config.TOKEN) # создание объекта класса бот

# инициализируем соединение с БД

#хрень с командами
@bot.message_handler(commands=['start'])
def welcome(message):
    config.boboltyshkaBool = False
    config.helloBool = True
    config.menuBool = False

    #добавляем юзера в БД

    sti = open('Stikers/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, '{0.first_name}, рад тебя видеть!😍\nЯ - <b>{1.first_name}</b>☀️, создан рыжим программистом👨🏼‍💻, чтобы его невесте👰🏻 было не одиноко, когда он не в сети.\nКем ты приходишься для моего создателя?🤔'.format(message.from_user, bot.get_me()), 
        parse_mode='html',reply_markup=k.hello)

@bot.message_handler(commands=['menu'])
def menu(message):
    config.boboltyshkaBool = False
    config.helloBool = False
    config.menuBool = True

    bot.send_message(message.chat.id, '🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',
    reply_markup=k.menu)

#хрень с сообщениями
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if config.boboltyshkaBool == True:
        bot.reply_to(message, pipe.predict([message.text.lower()])[0])
    else:
        bot.send_message(message.chat.id, 'Прости, но я не знаю чего ты хочешь от меня😓')

#ответы бота 
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if config.helloBool == True: #ответы на приветствие
                if call.data == 'H1':
                    bot.send_message(call.message.chat.id, 'О, мой Повелитель!😇\nПришел редачить меня?😏\nХочу новые функции😢')
                elif call.data == 'H2':
                    bot.send_message(call.message.chat.id, 'Оу-у-у, как долго я тебя ждал❤️\nВкраце:\nЯ версия номер:2️⃣\nВызови 🔡меню🔢 командой, чтобы с мной взаимодействовать😊\n📝P.S.:Нажми или введи "/"📝')
                elif call.data == 'H3':
                    bot.send_message(call.message.chat.id, 'Вау, ну и дерзость😯\nЯ тебе ничего не расскажу, сам гадай!😡')

                #удаление inline сообщений
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            elif config.menuBool == True: #ответы меню
                if call.data == 'M1':
                    bot.send_message(call.message.chat.id, '💁🏼‍♂️Включен режим собеседника💁🏼‍♂️\n⛔️Если захочешь прекратить⛔️\nто просто вызови 🔡меню🔢\nТеперь можем поболтать😇')
                    config.boboltyshkaBool = True

                    #удаление inline сообщений
                    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

    except Exception as e:
        print(repr(e))

#Запуск
bot.polling(none_stop=True)