from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['FAQ 👁', 'Задать свой вопрос ❓']
but = types.KeyboardButton(text='О нас ☎️')

keyboard.add(*buttons)
keyboard.add(but)

keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button_2 = types.KeyboardButton(text='Отмена ❌')

keyboard_2.add(button_2)