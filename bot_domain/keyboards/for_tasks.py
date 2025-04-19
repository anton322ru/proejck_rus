from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_cor_or_wrong(correct, wrong, num):
    if len(correct) % 2 == 0:
        inline_kb_list = [
            [InlineKeyboardButton(text=correct, callback_data=f'correct_{num}')],
            [InlineKeyboardButton(text=wrong, callback_data=f'wrong_{num}')]]
    else:
        inline_kb_list = [
            [InlineKeyboardButton(text=wrong, callback_data=f'wrong_{num}')],
            [InlineKeyboardButton(text=correct, callback_data=f'correct_{num}')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
