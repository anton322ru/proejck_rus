from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_cor_or_wrong(correct, wrong):
    if len(correct) % 2 == 0:
        inline_kb_list = [
            [InlineKeyboardButton(text=correct, callback_data='correct')],
            [InlineKeyboardButton(text=wrong, callback_data='wrong')]]
    else:
        inline_kb_list = [
            [InlineKeyboardButton(text=wrong, callback_data='wrong')],
            [InlineKeyboardButton(text=correct, callback_data='correct')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
