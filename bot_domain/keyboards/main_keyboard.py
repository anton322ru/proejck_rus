from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyb():
    kb = ReplyKeyboardBuilder()
    kb.button(text="4 номер")
    kb.button(text="9 номер")
    kb.button(text='10 номер')
    kb.button(text='22 номер')
    kb.button(text='Список ошибок')
    kb.button(text='Добавить слово')
    kb.button(text='Остановить')
    kb.button(text='Настройки слова дня')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True, input_field_placeholder="Воспользуйтесь меню:)")
