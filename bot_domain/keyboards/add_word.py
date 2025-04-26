from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def add_words():
    inline_kb_list = [
        [InlineKeyboardButton(text='4 номер(ударение)', callback_data='4')],
        [InlineKeyboardButton(text='9 номер(словарные слова)', callback_data='9')],
        [InlineKeyboardButton(text='10 номер(правописание приставок)', callback_data='10')],
        [InlineKeyboardButton(text='другое', callback_data='another')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
