from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#приветствие
hello_item1 = InlineKeyboardButton('Я твой создатель👨🏼‍💻', callback_data='H1')
hello_item2 = InlineKeyboardButton('Я его невеста👰🏻', callback_data='H2')
hello_item3 = InlineKeyboardButton('Я знаю его и с тебя хватит на этом😏', callback_data='H3')

hello = InlineKeyboardMarkup(row_width=1).add(hello_item1, hello_item2, hello_item3)

#меню
menu_item1 = InlineKeyboardButton('💁🏼‍♂️Режим собеседника💁🏼‍♂️', callback_data='M1')

menu = InlineKeyboardMarkup(row_width=1).add(menu_item1)