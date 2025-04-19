from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="4 номера")
    kb.button(text="9 номера")
    kb.button(text='10 номера')
    kb.button(text='22 номера')
    kb.button(text='Список сложных слов')
    kb.button(text='Добавить слово')
    kb.button(text='остановить')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:")
