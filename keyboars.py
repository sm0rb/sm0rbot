import telebot
from telebot import types

#приветствие
hello = types.InlineKeyboardMarkup(row_width=1)
hello_item1 = types.InlineKeyboardButton('Я твой создатель👨🏼‍💻', callback_data='H1')
hello_item2 = types.InlineKeyboardButton('Я его невеста👰🏻', callback_data='H2')
hello_item3 = types.InlineKeyboardButton('Я знаю его и с тебя хватит на этом😏', callback_data='H3')

hello.add(hello_item1, hello_item2, hello_item3)

#меню
menu = types.InlineKeyboardMarkup(row_width=1)
menu_item1 = types.InlineKeyboardButton('💁🏼‍♂️Режим собеседника💁🏼‍♂️', callback_data='M1')

menu.add(menu_item1)