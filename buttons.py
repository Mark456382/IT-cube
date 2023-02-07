from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['FAQ', 'Задать свой вопрос']
but = types.KeyboardButton(text='О нас ☎')

keyboard.add(*buttons)
keyboard.add(but)
