import logging
import asyncio
from asyncio import create_task, gather

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from handlers import tasks
import os
from dotenv import load_dotenv
from keybords.main_keyboard import main_keyb
from keybords.continue_task import cont_or_exit

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
dp = Dispatcher()
router = Router()
dp.include_routers(tasks.router)


async def main():
    bot = Bot(token=os.environ.get('BOT_TOKEN'))
    await dp.start_polling(bot)


@dp.message(F.text == 'Закончить')
@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!\nВыбирай, что будешь делать сегодня",
                        reply_markup=main_keyb())


@dp.message(F.text == "остановить")
async def stop(message: types.Message):
    await message.reply("Пока:(", reply_markup=ReplyKeyboardRemove())


@dp.message(Command('help'))  # декоратор для обработчика команды help
async def process_help_command(message: types.Message):
    text = ['Я бот по русскому, бегу помогать вам идти к соточке!',
            'введите /start, чтобы начать']
    await message.reply('\n'.join(text))


@dp.message(F.text == "9 номера")
async def nine_task(message: types.Message):
    await message.reply("здесь будет викторина по 9")


@dp.message(F.text == "10 номера")
async def four_task(message: types.Message):
    await message.reply("здесь будет викторина по 10")


@dp.message(F.text == "22 номера")
async def four_task(message: types.Message):
    await message.reply("здесь будет викторина по 22")


@dp.message(F.text == "Список сложных слов")
async def word_list(message: types.Message):
    await message.reply("здесь будет список слов")


@dp.message(F.text == "Добавить слово")
async def add_word(message: types.Message):
    await message.reply("можно добавить слово", reply_markup=s_kb)


if __name__ == '__main__':
    asyncio.run(main())
