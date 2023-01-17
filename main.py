import random
from config import *
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token=TOKEN)
db = Dispatcher(bot)

g_d = {1: "Камень",
        2: "Ножницы",
        3: "Бумага"}

s_d = {f"You": 0,
        "Bot": 0,
        "all": 0}


@db.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"{message.from_user.first_name}, Привет!!!")


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


@db.message_handler()
async def game(message: types.Message):
    bot_choose = g_d[random.randint(1, 3)]
    user_choose = message.text

    await message.answer(f"Я выбрал {bot_choose}")

    if bot_choose == g_d[1] and user_choose == g_d[2] or bot_choose == g_d[2] and user_choose == g_d[3] or bot_choose == g_d[3] and user_choose == g_d[1]:
        await message.answer("Я выйграл")
        s_d.update(Bot=s_d['Bot']+1)
    elif bot_choose == user_choose:
        await message.answer("Ничья")
    else:
        await message.answer('Ты выйграл')
        s_d.update(You=s_d['You']+1)
    s_d.update(all=s_d['all']+1)


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=False)
