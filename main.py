import smtplib
from config import *
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
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

@db.message_handler(state=Input.sub)
async def sub_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sub'] = message.text
    await Input.num.set()
    await message.answer("Введите номер телефона или ссылку на свою соц. сеть, чтобы мы смогли с вами связаться")

@db.message_handler(state=Input.num)
async def sub_message(message: types.Message, state: FSMContext):
    # тема письма
    subject = f"Вопрос от {message.from_user.full_name}"
    # кодировка письма
    charset = 'Content-Type: text/plain; charset=utf-8'
    mime = 'MIME-Version: 1.0'

    async with state.proxy() as data:
        data['num'] = message.text
        # текст письма
        text = f"{md.bold(data['sub'])}\n{md.bold(data['num'])}"

    # формируем тело письма
    body = "\r\n".join((f"From: {USER}", f"To: {USER}",
            f"Subject: {subject}", mime, charset, "", text))

    try:
        smtp = smtplib.SMTP(SERVER, PORT)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(USER, PASSWD)
        smtp.sendmail(USER, USER, body.encode('utf-8'))
    except smtplib.SMTPException as err:
        print('Что - то пошло не так...')
        raise err
    finally:
        smtp.quit()
        await state.finish()
        await message.answer("Письмо отправлено, в скором времени мы свяжемся с вами")

@db.message_handler(Text('О нас ☎'))
async def we(message: types.Message):
    await message.answer('Мы команда "VektorTeam" и наш проект "deCryptor" '+
                        'направлен на безопасность персональных данных пользователей сети интернет.'+
                        'Благодаря нашей программе возможно шифровать файлы, папки и диски в любом обьме или формате.'+
                        'Система шифрования base64 в связке с нашей технологией решает проблему защиты персональной информации.\n'+
                        'Подробнее можно узнать на сайте проекта https://decryptor.vektor.tilda.ws\nНаша почта: decryptor.vector@gmail.com\n'+
                        'Мы в соц. сетях:\nVK: https://vk.com/decryptor.vektor\nTG: https://t.me/decryptor_vektor.com')
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

@db.message_handler(content_types=['any'])
async def none_message(message: types.Message):
    await message.answer('У меня нет ответа на ваш вопрос.' +
                        '\nПопробуйте написать нам на почту лично decryptor.vektor@gmail.com или же через бота ' +
                        '(кнопка "Задать свой вопрос"')

if __name__ == "__main__":
    executor.start_polling(db, skip_updates=False)
