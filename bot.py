#Подключение библиотек
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
#Подключение файлов
import keyboars as k
from boltyshka import *
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
async def welcome(message: types.Message):
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

#команды для отправки рассылки об обновлении
@dp.message_handler(commands=['spam'])
async def spam(message: types.Message):
	if (message.chat.id == 650920012):
		subscriptions = db.get_subscriptions()
		for s in subscriptions:
			await bot.send_message(s[1],f'{message.chat.username}, привет!👋🏻\nЕсли ты видишь это сообщение👀, то мой создатель домучился😅\nТеперь о каждом обновлении буду говорить тебе я😊\n🆕Из нового:🆕\n-Тепрь команда "/start" не такая уж и бесполезная, можешь вызвать и попытаться зайти не под собой😏\n-Ну конечно же уведомления об обновлениях🔔🆕\nP.S.: Создатель угрохал на это кучу сил и нервов, но когда получилось, то скакал от счастья. Это надо было видеть🤣\n-В списке команд появилась команда рассылки обновы, но даже не пытайся её использовать - ничего не выйдет😇',
		parse_mode="HTML")
	else:
		await bot.send_message(message.chat.id, 'Прости, но у тебя не достаточно прав для этой команды😔')

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
				if (call.message.chat.id == 650920012):
					await bot.send_message(call.message.chat.id, 'О, мой Повелитель!😇\nПришел редачить меня?😏\nХочу новые функции😢')
				else:
					await bot.send_message(call.message.chat.id, 'Ты не мой создатель!😡\nЯ его знаю, как-никто другой.\nТак кто ты?🤔',reply_markup=k.hello)
			elif call.data == 'H2':
				if (call.message.chat.id == 735542467):
					await bot.send_message(call.message.chat.id, 'Оу-у-у, как долго я тебя ждал❤️\nВкраце:\nЯ версия номер:3️⃣\nВызови 🔡меню🔢 командой, чтобы с мной взаимодействовать😊\n📝P.S.:Нажми или введи "/"📝')
				else:
					await bot.send_message(call.message.chat.id, 'Ты не его невеста!😡\nЯ её знаю, как-никто другой.\nТак кто ты?🤔',reply_markup=k.hello)
			elif call.data == 'H3':
				if (call.message.chat.id != 735542467 and call.message.chat.id != 650920012):
					await bot.send_message(call.message.chat.id, 'Вау, ну и дерзость😯\nЯ тебе ничего не расскажу, сам гадай!😡')
				else:
					await bot.send_message(call.message.chat.id, 'Оу, как дерзко😏\nНо я же знаю, что ты не абы кто😎\nМожет ответишь честно?🤔',reply_markup=k.hello)

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