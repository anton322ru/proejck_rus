from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def timer_exit() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Выйти")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True,
                        input_field_placeholder="Воспользуйтесь меню;)")
