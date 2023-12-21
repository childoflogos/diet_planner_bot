from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='🥦Menus'),
        KeyboardButton(text='🍽Meals'),
        KeyboardButton(text='➕Create menu')
    )
    return builder.as_markup(resize_keyboard=True)
