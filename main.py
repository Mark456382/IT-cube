import smtplib
from config import *
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from buttons import keyboard, keyboard_2
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
    await message.answer_sticker('CAACAgIAAxkBAAIdjmPjgbaL09A_MXr_rujJkJTfD5owAALOEQACW-6hS0nvqzvOJ-hjLgQ')
    await message.answer(f"{message.from_user.first_name}, Привет!!!(some text)", reply_markup=keyboard)


@db.message_handler(Text('FAQ 👁'))
async def faq(message: types.Message):
    await message.answer(FAQ)


@db.message_handler(Text('Задать свой вопрос ❓'))
async def send_email(message: types.Message):
    await Input.sub.set()
    await message.reply("Опишите проблему максимально подробно. "+
                        "Что именно интересует, что возможно не работает и какие вопросы у вас есть. "+
                        "Прежде чем писать нам, попробуйте найти ответ на свой вопрос или проблему в FAQ", reply_markup=keyboard_2)


@db.message_handler(state=Input.sub)
async def sub_message(message: types.Message, state: FSMContext):
    if message.text != 'Отмена ❌':
        async with state.proxy() as data:
            data['sub'] = message.text
        await Input.num.set()
        await message.answer("Введите номер телефона или ссылку на свою соц. сеть, чтобы мы смогли с вами связаться", reply_markup=keyboard_2)
    else:
        await state.finish()
        await message.answer("Заявка отменена. Если у вас появяться вопросы то мы всегда готовы вам помочь ", reply_markup=keyboard)
        await message.answer_sticker('CAACAgIAAxkBAAIdjGPjgOK7QUf8RMGqOPuu0tMVJBAtAALCFwACpFYJSaadQck7d-CWLgQ')


@db.message_handler(state=Input.num)
async def sub_message(message: types.Message, state: FSMContext):
    if message.text != 'Отмена ❌':
        subject = f"Вопрос от {message.from_user.full_name}"

        async with state.proxy() as data:
            data['num'] = message.text

            msg = f"Subject: {subject}\n Вопрос:\n{md.bold(data['sub'])}\nКонтакт пользователя:\n{md.bold(data['num'])}"

        try:
            smtp = smtplib.SMTP(SERVER, PORT)
            smtp.starttls()
            smtp.login(USER, PASSWD)
            smtp.sendmail(USER, USER, msg.encode('utf-8'))
        except smtplib.SMTPException as err:
            print('Что - то пошло не так...')
            raise err
        finally:
            await state.finish()
            await message.answer("Письмо отправлено, в скором времени мы свяжемся с вами")
    else:
        await state.finish()
        await message.answer("Заявка отменена. Если у вас появяться вопросы то мы всегда готовы вам помочь ", reply_markup=keyboard)
        await message.answer_sticker('CAACAgIAAxkBAAIdjGPjgOK7QUf8RMGqOPuu0tMVJBAtAALCFwACpFYJSaadQck7d-CWLgQ')


# @db.message_handler(Text('Отмена ❌'))
# async def cancel(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Заявка отменена. Если у вас появяться вопросы то мы всегда готовы вам помочь ")
#     await message.answer_sticker('CAACAgIAAxkBAAIdjGPjgOK7QUf8RMGqOPuu0tMVJBAtAALCFwACpFYJSaadQck7d-CWLgQ')


@db.message_handler(Text('О нас ☎️'))
async def we(message: types.Message):
    await message.answer('Мы команда "VektorTeam" и наш проект "deCryptor" '+
                        'направлен на безопасность персональных данных пользователей сети интернет.'+
                        'Благодаря нашей программе возможно шифровать файлы, папки и диски в любом обьме или формате.'+
                        'Система шифрования base64 в связке с нашей технологией решает проблему защиты персональной информации.\n'+
                        'Подробнее можно узнать на сайте проекта https://decryptor.vektor.tilda.ws\nНаша почта: decryptor.vector@gmail.com\n'+
                        'Мы в соц. сетях:\nVK: https://vk.com/decryptor.vektor\nTG: https://t.me/decryptor_vektor.com')


@db.message_handler(content_types=['any'])
async def none_message(message: types.Message):
    await message.answer('У меня нет ответа на ваш вопрос.' +
                        '\nПопробуйте написать нам на почту лично decryptor.vektor@gmail.com или же через бота ' +
                        '(кнопка "Задать свой вопрос"')


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=False)
