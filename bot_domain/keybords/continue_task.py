from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cont_or_exit() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Продолжить")
    kb.button(text="Закончить")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
