from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def timer_dec():
    inline_kb_list = [
        [InlineKeyboardButton(text='10 минут', callback_data='10')],
        [InlineKeyboardButton(text='30 минут', callback_data='30')],
        [InlineKeyboardButton(text='1 час', callback_data='60')],
        [InlineKeyboardButton(text='3 часа', callback_data='180')],
        [InlineKeyboardButton(text='6 часов', callback_data='360')],
        [InlineKeyboardButton(text='12 часов', callback_data='720')],
        [InlineKeyboardButton(text='Выйти', callback_data='exit')]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
