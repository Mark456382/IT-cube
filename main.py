from config import *
from _ORM import _ORM
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token=TOKEN)
base = _ORM()
db = Dispatcher(bot, storage=MemoryStorage())


class Input(StatesGroup):
    sub = State()


@db.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, Привет!!!(some text)")
    base.add_user(message.from_user.id)


@db.message_handler(commands=['state'])
async def check_state(message: types.Message):
    await Input.sub.set()
    await message.reply("Введите трек номер договора")


@db.message_handler(state=Input.sub)
async def process_name(message: types.Message, state: FSMContext):
    await message.answer('Обрабатываю...')

    async with state.proxy() as data:
        data['sub'] = message.text
        user_choice = md.bold(data['sub'])

    await message.answer(f"Состояние заказа: {base.checking_state(user_choice)}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=False)
