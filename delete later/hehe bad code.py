import asyncio
import aioschedule
import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from bot_domain.keyboards.main_keyboard import main_keyb
from aiogram.types import ReplyKeyboardRemove

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
dp = Dispatcher()


# сделать main клавиатуру одноразовой
async def main():
    bot = Bot(token='')
    await dp.start_polling(bot)


@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name.capitalize()}!\nВыбирай, что будешь делать сегодня",
                        reply_markup=main_keyb())


@dp.message(Command('stop'))
async def stop(message: types.Message):
    await message.reply("Пока:(", reply_markup=ReplyKeyboardRemove())


@dp.message(Command('hehe'))
async def stop(message: types.Message):
    await message.reply("Пока:(", reply_markup=ReplyKeyboardRemove())
