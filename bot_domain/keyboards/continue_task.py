from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cont_or_exit(num) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"Продолжить {num} номера")
    kb.button(text="Закончить")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True,
                        input_field_placeholder="Воспользуйтесь меню;)")
