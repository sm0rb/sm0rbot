from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#Кнопка назад и закрыть
backButton = InlineKeyboardButton('◀️Назад◀️', callback_data='Back')
closeButton = InlineKeyboardButton('❌Выход❌', callback_data='Сlose')

#приветствие
hello_item1 = InlineKeyboardButton('Я твой создатель👨🏼‍💻', callback_data='Hel1')
hello_item2 = InlineKeyboardButton('Я его невеста👰🏻', callback_data='Hel2')
hello_item3 = InlineKeyboardButton('Я знаю его😏\nЯ его знакомый😇', callback_data='Hel3')
hello_item4 = InlineKeyboardButton('Я его даже не знаю 😅', callback_data='Hel4')

hello = InlineKeyboardMarkup(row_width=1).add(hello_item1, hello_item2, hello_item3, hello_item4)

#меню
menu_item1 = InlineKeyboardButton('💁🏼‍♂️Режим собеседника💁🏼‍♂️', callback_data='Men1')
menu_item2 = InlineKeyboardButton('🔊Cвязь🔊', callback_data='Men2')

menu = InlineKeyboardMarkup(row_width=1).add(menu_item1, menu_item2, closeButton)

#связь
connection_item1 = InlineKeyboardButton('📞Контакты создателя📞', callback_data='Con1')
connection_item2 = InlineKeyboardButton('❗️Предложить идею❗️', callback_data='Con2')

connection = InlineKeyboardMarkup(row_width=1).add(connection_item1, connection_item2, backButton)

#подверждение отправки идеи
forwardOk = InlineKeyboardButton('Да, всё верно🤓\nЯ проверил😎', callback_data='fOk')
forwardNo = InlineKeyboardButton('Нет, я ошибся немного😅', callback_data='fNo')

forward = InlineKeyboardMarkup(row_width=1).add(forwardOk, forwardNo)

backKeyboard = InlineKeyboardMarkup(row_width=1).add(backButton)