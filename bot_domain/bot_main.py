import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from handlers import four_task, nine_task, ten_task
import os
from dotenv import load_dotenv
from keyboards.main_keyboard import main_keyb

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
dp = Dispatcher()
router = Router()
dp.include_routers(four_task.router, nine_task.router, ten_task.router)


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


@dp.message(Command('help'))
async def process_help_command(message: types.Message):
    text = ['Я бот по русскому, бегу помогать вам идти к соточке!',
            'введите /start, чтобы начать']
    await message.reply('\n'.join(text))


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
