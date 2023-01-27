import random
import time

from config import *
import cv2
from time import sleep
import aiogram.utils.markdown as md
from aiogram.types import ContentType, File
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token=TOKEN)

db = Dispatcher(bot, storage=MemoryStorage())

g_d = {1: "Камень",
        2: "Ножницы",
        3: "Бумага"}

s_d = {f"You": 0,
        "Bot": 0,
        "all": 0}


class Input(StatesGroup):
    sub = State()


@db.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, Привет!!!")


@db.message_handler(commands=['spam'])
async def spam(message: types.Message):
    time.sleep(3)
    for i in range(10000):
        await message.answer('Ты лох')


@db.message_handler(commands=['static'])
async def static(message: types.Message):
    if s_d['all'] == 0:
        await message.answer('У тебя нет статистики, мы еще ни разу не играли ')
    else:
        try:
            await message.answer(f'Ты ---> {s_d["You"]}\nБот ---> {s_d["Bot"]}\nВсего игр ---> {s_d["all"]}')
            await message.answer(f"Ваш коэфицент побед: {round(s_d['You'] / s_d['all'])}")
        except ZeroDivisionError:
            await message.answer("Ты пока еще ни разу не выйграл")


@db.message_handler(commands=['list_update'])
async def list_update(message: types.Message):
    with open("list.txt", 'w+') as f:
        f.write(message.text[11:])
    await message.answer('List is update!!!')


@db.message_handler(commands=['game'])
async def cmd_start(message: types.Message):
    await Input.sub.set()
    await message.reply("Давай поиграем")


@db.message_handler(state=Input.sub)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sub'] = message.text
        user_choice = md.bold(data['sub'])

    bot_choose = g_d[random.randint(1, 3)]
    await message.answer(f"Я выбрал {bot_choose}")

    if bot_choose == g_d[1] and user_choice == g_d[2] or bot_choose == g_d[2] and user_choice == g_d[3] or bot_choose == g_d[3] and user_choice == g_d[1]:
        await message.answer("Я выйграл")
        s_d.update(Bot=s_d['Bot']+1)
    elif bot_choose == user_choice:
        await message.answer("Ничья")
    else:
        await message.answer('Ты выйграл')
        s_d.update(You=s_d['You']+1)
    s_d.update(all=s_d['all']+1)

    await state.finish()


@db.message_handler(content_types="video")
async def video_note_sender(message: types.Message):
    # await message.video[-1].download(destination_file=r'C:\Users\PythonV\PycharmProjects\MetBot\tg_video.mp4')
    await message.video.download('tg_video.mp4')

    file = "tg_video.mp4"  # путь к файлу с картинкой
    percent = 20
    cap = cv2.VideoCapture(file)

    ret, frame = cap.read()
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    frame_re = cv2.resize(frame, dim)
    cv2.imshow('frame', frame_re)

    cap.release()
    cv2.destroyAllWindows()

    await bot.send_video_note(message.chat.id, video_note=open('tg_video.mp4', 'rb'))


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=False)
