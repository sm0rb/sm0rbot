import config
import logging

import keyboars as k

from boltyshka import *

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

# задаем уровень логов
logging.basicConfig(level=logging.INFO)

# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# инициализируем соединение с БД
db = SQLighter('db.db')
# Команда активации подписки
@dp.message_handler(commands=['start'])
async def subscribe(message: types.Message):
	config.boboltyshkaBool = False
	config.helloBool = True
	config.menuBool = False

	await message.answer_sticker(r'CAACAgIAAxkBAAECNgRggH-JCqNBrmdIg5WSs75FVA0OfwACTwADrWW8FGuRHI2HrK-THwQ')	

	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	
	await bot.send_message(message.chat.id, f'{message.chat.username}, рад тебя видеть!😍\nЯ - <b>Рыжик</b>☀️, создан рыжим программистом👨🏼‍💻, чтобы его невесте👰🏻 было не одиноко, когда он не в сети.\nКем ты приходишься для моего создателя?🤔',
		parse_mode="HTML",reply_markup=k.hello)

@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    config.boboltyshkaBool = False
    config.helloBool = False
    config.menuBool = True

    await bot.send_message(message.chat.id, '🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',
    reply_markup=k.menu)

#хрень с сообщениями
@dp.message_handler()
async def echo_message(message: types.Message):
    if config.boboltyshkaBool == True: 
        await message.reply(pipe.predict([message.text.lower()])[0])
    else:
        await message.answer('Прости, но я не знаю чего ты хочешь от меня😓')

#ответы бота
@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
	if call.message:
		if config.helloBool == True: #ответы на приветствие
			if call.data == 'H1':
				await bot.send_message(call.message.chat.id, 'О, мой Повелитель!😇\nПришел редачить меня?😏\nХочу новые функции😢')
			elif call.data == 'H2':
				await bot.send_message(call.message.chat.id, 'Оу-у-у, как долго я тебя ждал❤️\nВкраце:\nЯ версия номер:2️⃣\nВызови 🔡меню🔢 командой, чтобы с мной взаимодействовать😊\n📝P.S.:Нажми или введи "/"📝')
			elif call.data == 'H3':
				await bot.send_message(call.message.chat.id, 'Вау, ну и дерзость😯\nЯ тебе ничего не расскажу, сам гадай!😡')

			#удаление inline сообщений
			await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

		elif config.menuBool == True: #ответы меню
			if call.data == 'M1':
				await bot.send_message(call.message.chat.id, '💁🏼‍♂️Включен режим собеседника💁🏼‍♂️\n⛔️Если захочешь прекратить⛔️\nто просто вызови 🔡меню🔢\nТеперь можем поболтать😇')
				config.boboltyshkaBool = True

				#удаление inline сообщений
				await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)