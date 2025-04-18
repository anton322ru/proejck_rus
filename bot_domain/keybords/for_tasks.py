from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_cor_or_wrong(correct, wrong) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    if len(correct) % 2 == 0:
        kb.button(text=wrong)
        kb.button(text=correct)
    else:
        kb.button(text=correct)
        kb.button(text=wrong)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
