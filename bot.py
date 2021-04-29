# This Python file uses the following encoding: utf-8

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
	connectionBool = False 
	forwardMessage = False 

	subscriptions = db.get_subscriptions()

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
	connectionBool = False 
	forwardMessage = False 

	await bot.send_message(message.chat.id, '🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',reply_markup=k.menu)

#команды для отправки рассылки об обновлении
@dp.message_handler(commands=['spam'])
async def spam(message: types.Message):
	if (message.chat.id == 650920012):
		subscriptions = db.get_subscriptions()
		for s in subscriptions:
			await bot.send_message(s[1],f'{message.chat.username}, привет!👋🏻\nЕсли ты видишь это сообщение👀, то мой создатель домучился😅\nОн выпустил новое обновление, о котором я тебе расскажу😊\n🆕Из нового:🆕\n-Тепрь команда "/start" более дружелюбная и теперь обо мне можно рассказать друзьям😏\n-Теперь функция 🔡меню🔢 не спамит кучу сообщений, а всё делает в одном😱\nP.S.: Звучит сложно, но просто вызови 🔡меню🔢 и полазь по нему, должно понравиться😏\n-Появилась новая кнопка в 🔡меню🔢 и это 🔊Cвязь🔊, подробнее в ней\n\n Если найдёте какие-то ошибки, то пишите моему создателю👨🏼‍💻\nОн хочет чтобы я был идеален😇😎',
		parse_mode="HTML")
	else:
		await bot.send_message(message.chat.id, 'Прости, но у тебя не достаточно прав для этой команды😔')

#хрень с сообщениями
@dp.message_handler()
async def echo_message(message: types.Message):
	if config.boboltyshkaBool == True: 
		await message.reply(pipe.predict([message.text.lower()])[0])
	elif config.forwardMessage:
		await bot.edit_message_reply_markup(message.chat.id, message_id=config.MessageId)#удаление inline сообщений 
		#временная переменная для переотправки сообщения
		config.MessageId = message.message_id

		await message.reply('Это твоя идея?🤔\nПроверь. Всё верно написал?📝', reply_markup=k.forward)
	else:
		await message.answer('Прости, но я не знаю чего ты хочешь от меня😓\nВоспользуйся 🔡меню🔢, чтобы включить, то что тебе нужно🤓')

#ответы бота
@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
	if call.message:
		if config.helloBool: #ответы на приветствие
			if call.data == 'Hel1':
				if (call.message.chat.id == 650920012):
					await bot.send_message(call.message.chat.id, 'О, мой Повелитель!😇\nПришел редачить меня?😏\nХочу новые функции😢')
				else:
					await bot.send_message(call.message.chat.id, 'Ты не мой создатель!😡\nЯ его знаю, как-никто другой.Так кто ты?🤔',reply_markup=k.hello)
			elif call.data == 'Hel2':
				if (call.message.chat.id == 735542467):
					await bot.send_message(call.message.chat.id, 'Оу-у-у, как долго я тебя ждал❤️\nВкраце:\nЯ версия номер:4️⃣\nВызови 🔡меню🔢 командой, чтобы с мной взаимодействовать😊\n📝P.S.:Нажми или введи "/"📝')
				else:
					await bot.send_message(call.message.chat.id, 'Ты не его невеста!😡\nЯ её знаю, как-никто другой.Так кто ты?🤔',reply_markup=k.hello)
			elif call.data == 'Hel3':
				if (call.message.chat.id != 735542467 and call.message.chat.id != 650920012):
					await bot.send_message(call.message.chat.id, 'Здорово!🤗\nНадеюсь мы с тобой подружимся☺️\nПравда, я ещё не много чего умею😅\nНо в 🔡меню🔢 ты можешь предложить идею моему создателю, если выберешь 🔊связь🔊\nЧтобы пройти в 🔡меню🔢 с моими функциями, введи команду /menu')
				else:
					await bot.send_message(call.message.chat.id, 'Оу, как дерзко😏\nНо я же знаю, что ты не абы кто😎\nМожет ответишь честно?🤔',reply_markup=k.hello)
			elif call.data == 'Hel4':
				if (call.message.chat.id != 735542467 and call.message.chat.id != 650920012):
					await bot.send_message(call.message.chat.id, 'Ого, значит тебе обо мне кто-то рассказал😯\nЯ рад, что становлюсь популярным🥰\nПереходи в 🔡меню🔢 командой /menu, чтобы познакомиться с моим функционалом\nЕсли будет что не понятно, то пиши моему создателю👨🏼‍💻\nЕго контакты можно найти в:\n🔡меню🔢->🔊связь🔊')
				else:
					await bot.send_message(call.message.chat.id, 'Оу, как дерзко😏\nНо я же знаю, что ты не абы кто😎\nМожет ответишь честно?🤔',reply_markup=k.hello)
 
			await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)#удаление inline сообщений

		elif config.menuBool: #ответы меню
			if call.data == 'Men1':
				await bot.edit_message_text(text='💁🏼‍♂️Включен режим собеседника💁🏼‍♂️\n⛔️Если захочешь прекратить⛔️\nто просто вызови 🔡меню🔢\nТеперь можем поболтать😇', chat_id=call.message.chat.id, message_id=call.message.message_id)
				config.boboltyshkaBool = True
			elif call.data == 'Men2':
				await bot.edit_message_text(text='🔊Добро пожаловать в связь🔊\nЗдесь можно предложить свою идею или узнать контакты моего создателя', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.connection)
				config.connectionBool = True
			elif call.data == 'Сlose':
				await bot.edit_message_text(text='🔡Меню🔢\n❌Закрыто❌', chat_id=call.message.chat.id, message_id=call.message.message_id)
			
			config.menuBool = False

		elif config.forwardMessage: #подтверждение отправки
			if call.data == 'fOk':
				#await bot.edit_message_text(text='', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.)
				await bot.send_message(call.message.chat.id, 'Всё OK👌🏻\nКак создатель будет в сети, я с ним покумекаю😉')
				await bot.forward_message(chat_id=650920012, from_chat_id=call.message.chat.id, message_id=config.MessageId)
				await bot.send_message(chat_id=650920012, text= f'{call.message.chat.id}', parse_mode="HTML")
				await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)#удаление inline сообщений
				config.forwardMessage = False
			elif call.data == 'fNo':
				await bot.send_message(call.message.chat.id, 'Жалко😔\n🔁Тогда заново🔁')
				await bot.send_message(call.message.chat.id, 'Напиши мне следующим сообщением свою идею, которую хочешь, чтобы была реализована🤔\nЯ покмекую с создателем😉\nИ он попытается её реализовать, если это возможно☺️', reply_markup=k.backKeyboard)
				await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)#удаление inline сообщений

			if call.data == 'Back':
				await bot.edit_message_text(text='🔊Добро пожаловать в связь🔊\nЗдесь можно предложить свою идею или узнать контакты моего создателя', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.connection)
				config.forwardMessage = False
				config.connectionBool = True

		elif config.connectionBool: #ответы связи
			if call.data == 'Con1':
				await bot.send_message(call.message.chat.id, 'Телеграм создателя: @Sm0rb\nФ.И.О: Яньков Егор Сергеевич\nПрошу быть с ним вежливым😇\nP.S.: Он иногда долго отвечает😅')
				await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)#удаление inline сообщений
			elif call.data == 'Con2':
				await bot.edit_message_text(text='Напиши мне следующим сообщением свою идею, которую хочешь, чтобы была реализована🤔\nЯ покмекую с создателем😉\nИ он попытается её реализовать, если это возможно☺️', chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.backKeyboard)
				config.MessageId = call.message.message_id
				config.forwardMessage = True
			elif call.data == 'Back':
				await bot.edit_message_text(text='🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.menu)
				config.menuBool = True

			config.connectionBool = False

# запускаем лонг поллинг
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)