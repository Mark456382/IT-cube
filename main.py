import smtplib
from config import *
from buttons import keyboard
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token=TOKEN)
db = Dispatcher(bot, storage=MemoryStorage())


class Input(StatesGroup):
    sub = State()
    num = State()


@db.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, Привет!!!(some text)", reply_markup=keyboard)


@db.message_handler(Text('FAQ'))
async def faq(message: types.Message):
    await message.answer(FAQ)


@db.message_handler(Text('Задать свой вопрос'))
async def send_email(message: types.Message):
    await Input.sub.set()
    await message.reply("Опишите проблему максимально подробно. "+
                        "Что именно интересует, что возможно не работает и какие вопросы у вас есть. "+
                        "Прежде чем писать нам, попробуйте найти ответ на свой вопрос или проблему в FAQ")


@db.message_handler(content_types=['any'])
async def none_message(message: types.Message):
    await message.answer('У меня нет ответа на ваш вопрос.' +
                         '\nПопробуйте написать нам на почту лично decryptor.vektor@gmail.com или же через бота ' +
                         '(кнопка "Задать свой вопрос"')


# user = "support.decryptor@gmail.com"
# passwd = "aq1sw2de3fr4-"
# server = "smtp.yandex.ru"
# port = 587
#
# # тема письма
# subject = "Вопрос от {user}"
# # кому
# to = "decryptor.vektor@gmail.com"
# # кодировка письма
# charset = 'Content-Type: text/plain; charset=utf-8'
# mime = 'MIME-Version: 1.0'
# # текст письма
# text = "{message.text}\n{his phone_number}"
#
# # формируем тело письма
# body = "\r\n".join((f"From: {user}", f"To: {to}",
#        f"Subject: {subject}", mime, charset, "", text))
#
# try:
#     smtp = smtplib.SMTP(server, port)
#     smtp.starttls()
#     smtp.ehlo()
#     smtp.login(user, passwd)
#     smtp.sendmail(user, to, body.encode('utf-8'))
# except smtplib.SMTPException as err:
#     print('Что - то пошло не так...')
#     raise err
# finally:
#     smtp.quit()

#
# @db.message_handler(commands=['state'])
# async def check_state(message: types.Message):
#     await Input.sub.set()
#     await message.reply("Введите трек номер договора")
#
#
# @db.message_handler(state=Input.sub)
# async def process_name(message: types.Message, state: FSMContext):
#     await message.answer('Обрабатываю...')
#
#     async with state.proxy() as data:
#         data['sub'] = message.text
#         user_choice = md.bold(data['sub'])
#
#     await message.answer(f"Состояние заказа: {base.checking_state(user_choice)}")
#     await state.finish()


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=False)
