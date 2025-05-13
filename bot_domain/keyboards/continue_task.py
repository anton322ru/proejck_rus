from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cont_or_exit(num) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    if isinstance(num, int):
        kb.button(text=f"Продолжить {num} номер")
    kb.button(text="Закончить")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True,
                        input_field_placeholder="Воспользуйтесь меню;)")
