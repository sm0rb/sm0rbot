# This Python file uses the following encoding: utf-8

# Подключение библиотек
import logging

from aiogram import Bot, Dispatcher, executor, types

# Подключение файлов
import config
import keyboars as k
from boltyshka import *
from city import *
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
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id, message.from_user.username)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    db.update_bool(message.from_user.id, 'helloBool')

    await message.answer_sticker(r'CAACAgIAAxkBAAECNgRggH-JCqNBrmdIg5WSs75FVA0OfwACTwADrWW8FGuRHI2HrK-THwQ')

    await bot.send_message(message.chat.id,
                           f'{message.chat.username}, рад тебя видеть!😍\nЯ - <b>Рыжик</b>☀️, создан рыжим '
                           f'программистом👨🏼‍💻, чтобы его невесте👰🏻 было не одиноко, когда он не в сети.\nКем ты '
                           f'приходишься для моего создателя?🤔',
                           parse_mode="HTML", reply_markup=k.hello)


@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    db.update_bool(message.chat.id, 'menuBool')

    await bot.send_message(message.chat.id, '🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',
                           reply_markup=k.menu)


# администраторская
@dp.message_handler(commands=['admin'])
async def spam(message: types.Message):
    if message.chat.id == 650920012:
        db.update_bool(message.from_user.id, 'adminBool')

        await bot.send_message(message.chat.id,
                               '👨🏼‍💻Добро пожаловать в администраторскую👨🏼‍💻\nЧто ты хочешь чтобы я сделал?🤔',
                               reply_markup=k.admin)

    else:
        await bot.send_message(message.chat.id, 'Прости, но у тебя не достаточно прав для этой команды😔')


# хрень с сообщениями
@dp.message_handler()
async def echo_message(message: types.Message):
    if db.check_bool(message.chat.id, 'boboltyshkaBool'):
        await message.reply(pipe.predict([message.text.lower()])[0])

    elif db.check_bool(message.chat.id, 'forwardMessage'):
        await bot.edit_message_reply_markup(message.chat.id, message_id=config.MessageId)  # удаление inline сообщений
        # временная переменная для переотправки сообщения
        config.MessageId = message.message_id

        await message.reply(text=f'Это твоя идея?🤔\nПроверь. Всё верно написал?📝', reply_markup=k.forward)

    elif db.check_bool(message.chat.id, 'gameBool'):
        response = get_city(message.text)
        await bot.send_message(message.chat.id, text=response)
        if config.winerBool:
            db.update_valuebool(message.chat.id, 'gameBool', False)
            await message.answer_sticker(r'CAACAgIAAxkBAAECQnJgkSrJ7PQXHO8ng0pcubvB-GZ0vgACWQADrWW8FPS7RxeJ4S0JHwQ')
            config.winerBool = False

    elif db.check_bool(message.chat.id, 'forwardSpam'):
        config.textspam = message.text
        await bot.send_message(message.chat.id, text=config.textspam + '\nТак?', reply_markup=k.forward)

    elif db.check_bool(message.chat.id, 'forwardOtvet'):
        string = message.text
        razdelitel = string.find('!')
        config.UserId = int(string[:razdelitel])
        config.UserText = string[razdelitel + 1:]
        await bot.send_message(message.chat.id, text='Пользователю:{0}\nОтправить сообщение:\n{1}'.format(config.UserId,
                                                                                                          config.UserText),
                               reply_markup=k.forward)

    else:
        await message.answer(
            'Прости, но я не знаю чего ты хочешь от меня😓\nВоспользуйся 🔡меню🔢, чтобы включить, то что тебе нужно🤓')


# ответы бота
@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    if call.message:
        if db.check_bool(call.message.chat.id, 'helloBool'):  # ответы на приветствие
            if call.data == 'Hel1':
                if call.message.chat.id == 650920012:
                    await bot.send_message(call.message.chat.id,
                                           'О, мой Повелитель!😇\nПришел редачить меня?😏\nХочу новые функции😢')
                else:
                    await bot.send_message(call.message.chat.id,
                                           'Ты не мой создатель!😡\nЯ его знаю, как-никто другой.Так кто ты?🤔',
                                           reply_markup=k.hello)
            elif call.data == 'Hel2':
                if call.message.chat.id == 735542467:
                    await bot.send_message(call.message.chat.id,
                                           'Оу-у-у, как долго я тебя ждал❤️\nВкраце:\nЯ версия номер:4️⃣\nВызови '
                                           '🔡меню🔢 командой, чтобы с мной взаимодействовать😊\n📝P.S.:Нажми или '
                                           'введи "/"📝')
                else:
                    await bot.send_message(call.message.chat.id,
                                           'Ты не его невеста!😡\nЯ её знаю, как-никто другой.Так кто ты?🤔',
                                           reply_markup=k.hello)
            elif call.data == 'Hel3':
                if call.message.chat.id != 735542467 and call.message.chat.id != 650920012:
                    await bot.send_message(call.message.chat.id,
                                           'Здорово!🤗\nНадеюсь мы с тобой подружимся☺️\nПравда, я ещё не много чего '
                                           'умею😅\nНо в 🔡меню🔢 ты можешь предложить идею моему создателю, '
                                           'если выберешь 🔊связь🔊\nЧтобы пройти в 🔡меню🔢 с моими функциями, '
                                           'введи команду /menu')
                else:
                    await bot.send_message(call.message.chat.id,
                                           'Оу, как дерзко😏\nНо я же знаю, что ты не абы кто😎\nМожет ответишь честно?🤔',
                                           reply_markup=k.hello)
            elif call.data == 'Hel4':
                if call.message.chat.id != 735542467 and call.message.chat.id != 650920012:
                    await bot.send_message(call.message.chat.id,
                                           'Ого, значит тебе обо мне кто-то рассказал😯\nЯ рад, что становлюсь '
                                           'популярным🥰\nПереходи в 🔡меню🔢 командой /menu, чтобы познакомиться с '
                                           'моим функционалом\nЕсли будет что не понятно, то пиши моему '
                                           'создателю👨🏼‍💻\nЕго контакты можно найти в:\n🔡меню🔢->🔊связь🔊')
                else:
                    await bot.send_message(call.message.chat.id,
                                           'Оу, как дерзко😏\nНо я же знаю, что ты не абы кто😎\nМожет ответишь честно?🤔',
                                           reply_markup=k.hello)

            await bot.edit_message_reply_markup(call.message.chat.id,
                                                call.message.message_id)  # удаление inline сообщений

        elif db.check_bool(call.message.chat.id, 'menuBool'):  # ответы меню menuBool
            if call.data == 'Men1':
                await bot.edit_message_text(
                    text='💁🏼‍♂️Включен режим собеседника💁🏼‍♂️\n⛔️Если захочешь прекратить⛔️\nто просто вызови '
                         '🔡меню🔢\nТеперь можем поболтать😇',
                    chat_id=call.message.chat.id, message_id=call.message.message_id)
                db.update_valuebool(call.message.chat.id, 'boboltyshkaBool', True)
            elif call.data == 'Men2':
                await bot.edit_message_text(
                    text='🔊Добро пожаловать в связь🔊\nЗдесь можно предложить свою идею или узнать контакты моего '
                         'создателя',
                    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.connection)
                db.update_valuebool(call.message.chat.id, 'connectionBool', True)
            elif call.data == 'Men3':
                await bot.edit_message_text(
                    text='🎲Добро пожаловать в игры🎲\nЗдесь можно с мной в что-нибудь поиграть, для этого выбери игру🙃',
                    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.game)
                db.update_valuebool(call.message.chat.id, 'gameBool', True)
            elif call.data == 'Сlose':
                await bot.edit_message_text(text='🔡Меню🔢\n❌Закрыто❌', chat_id=call.message.chat.id,
                                            message_id=call.message.message_id)

            db.update_valuebool(call.message.chat.id, 'menuBool', False)

        elif db.check_bool(call.message.chat.id, 'gameBool'):  # ответы игр
            if call.data == 'Gam1':
                refresh()
                await bot.edit_message_text(
                    text='Это классическая игра в 🌆города🌆, которую все знают.\nНо я знаю только города России, '
                         'так что у тебя есть фора😏\nПросьба писать только существующие города, '
                         'т.к. их существование я не проверю😅\n⛔️Если захочешь прекратить⛔️\nто просто вызови '
                         '🔡меню🔢\nТеперь можем поиграть, ты начинаешь😉',
                    chat_id=call.message.chat.id, message_id=call.message.message_id)
                
            elif call.data == 'Back':
                await bot.edit_message_text(text='🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',
                                            chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=k.menu)
                db.update_valuebool(call.message.chat.id, 'menuBool', True)
                db.update_valuebool(call.message.chat.id, 'gameBool', False)

        elif db.check_bool(call.message.chat.id, 'forwardMessage'):  # подтверждение отправки идеи
            if call.data == 'fOk':
                await bot.send_message(call.message.chat.id,
                                       text=f'Всё OK👌🏻\nКак создатель будет в сети, я с ним покумекаю😉')
                await bot.forward_message(chat_id=650920012, from_chat_id=call.message.chat.id,
                                          message_id=config.MessageId)
                await bot.send_message(chat_id=650920012, text=f'{call.message.chat.id}', parse_mode="HTML")
                await bot.edit_message_reply_markup(call.message.chat.id,
                                                    call.message.message_id)  # удаление inline сообщений
                db.update_valuebool(call.message.chat.id, 'forwardMessage', False)
            elif call.data == 'fNo':
                await bot.send_message(call.message.chat.id, text=f'Жалко😔\n🔁Тогда заново🔁')
                await bot.send_message(call.message.chat.id,
                                       text=f'Напиши мне следующим сообщением свою идею, которую хочешь, чтобы была '
                                            f'реализована🤔\nЯ покмекую с создателем😉\nИ он попытается её '
                                            f'реализовать, если это возможно☺️',
                                       reply_markup=k.backKeyboard)
                config.MessageId = call.message.message_id + 2
                await bot.edit_message_reply_markup(call.message.chat.id,
                                                    call.message.message_id)  # удаление inline сообщений

            if call.data == 'Back':
                await bot.edit_message_text(
                    text='🔊Добро пожаловать в связь🔊\nЗдесь можно предложить свою идею или узнать контакты моего '
                         'создателя',
                    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.connection)
                db.update_valuebool(call.message.chat.id, 'forwardMessage', False)
                db.update_valuebool(call.message.chat.id, 'connectionBool', True)

        elif db.check_bool(call.message.chat.id, 'connectionBool'):  # ответы связи
            if call.data == 'Con1':
                await bot.send_message(call.message.chat.id,
                                       'Телеграм создателя: @Sm0rb\nФ.И.О: Яньков Егор Сергеевич\nПрошу быть с ним '
                                       'вежливым😇\nP.S.: Он иногда долго отвечает😅')
                await bot.edit_message_reply_markup(call.message.chat.id,
                                                    call.message.message_id)  # удаление inline сообщений
            elif call.data == 'Con2':
                await bot.edit_message_text(
                    text=f'Напиши мне следующим сообщением свою идею, которую хочешь, чтобы была реализована🤔\nЯ '
                         f'покмекую с создателем😉\nИ он попытается её реализовать, если это возможно☺️',
                    chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=k.backKeyboard)
                config.MessageId = call.message.message_id
                db.update_valuebool(call.message.chat.id, 'forwardMessage', True)
            elif call.data == 'Back':
                await bot.edit_message_text(text='🔡Добро пожаловать в меню🔢\nЧто ты хочешь чтобы я сделал?🤔',
                                            chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=k.menu)
                db.update_valuebool(call.message.chat.id, 'menuBool', True)

            db.update_valuebool(call.message.chat.id, 'connectionBool', False)

        elif db.check_bool(call.message.chat.id, 'adminBool'):  # ответы администраторской
            if call.data == 'Adm1':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Добро пожаловать в 🆕Рассылку обновлений🆕\nХочешь разослать '
                                                 'следующее уведомление об обновлении?🤔')
                await bot.send_message(call.message.chat.id, text=config.textspam + '\n\nВсё правильно?',
                                       reply_markup=k.forward)
                db.update_valuebool(call.message.chat.id, 'forwardSpam', True)
            elif call.data == 'Adm2':
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text='Добро пожаловать в ✉️Ответы пользователю✉️\nКому хочешь ответить и '
                                                 'что?🤔\nФормат:\n(id пользователя!сообщение)')
                db.update_valuebool(call.message.chat.id, 'forwardOtvet', True)
            elif call.data == 'Сlose':
                await bot.edit_message_text(text='👨🏼‍💻Администраторская👨🏼‍💻\n❌Закрыто❌',
                                            chat_id=call.message.chat.id,
                                            message_id=call.message.message_id)

            db.update_valuebool(call.message.chat.id, 'adminBool', False)

        elif db.check_bool(call.message.chat.id, 'forwardSpam'):  # подтверждение отправки уведомления
            if call.data == 'fOk':
                await bot.send_message(call.message.chat.id, 'Понял создатель👌🏼\nОтправляю📩')

                subscriptions = db.get_subscriptions()
                for s in subscriptions:
                    try:
                        await bot.send_message(s[1],
                                               text=config.textspam,
                                               parse_mode="HTML")
                    except:
                        continue

                db.update_valuebool(call.message.chat.id, 'forwardSpam', False)

            elif call.data == 'fNo':
                await bot.send_message(call.message.chat.id, text='Жалко😔\nНапиши мне его')

            await bot.edit_message_reply_markup(call.message.chat.id,
                                                message_id=call.message.message_id)  # удаление inline сообщений

        elif db.check_bool(call.message.chat.id, 'forwardOtvet'):  # подтверждение отправки ответа
            if call.data == 'fOk':
                await bot.send_message(call.message.chat.id, 'Понял создатель👌🏼\nОтправляю📩')
                try:
                    await bot.send_message(chat_id=config.UserId,
                                           text=config.UserText,
                                           parse_mode="HTML")
                except:
                    await bot.send_message(call.message.chat.id, 'К сожалению я ему не могу написать😔')

                db.update_valuebool(call.message.chat.id, 'forwardOtvet', False)

            elif call.data == 'fNo':
                await bot.send_message(call.message.chat.id,
                                       text='Жалко😔\nНапиши мне заново\nФормат:\n(id пользователя!сообщение)')

            await bot.edit_message_reply_markup(call.message.chat.id,
                                                message_id=call.message.message_id)  # удаление inline сообщений


# запускаем лонг поллинг
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
