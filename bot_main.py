import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
import sqlite3

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
with open('config.json') as f:
    con = json.load(f)
token = con['BOT_TOKEN']

con = sqlite3.connect('db/tasks.db')
cur = con.cursor()
reply_keyboard = [[KeyboardButton(text='4 номера', callback_data='4_tasks'),
                   KeyboardButton(text='9 номера', callback_data='9_tasks')],
                  [KeyboardButton(text='10 номера', callback_data='10_tasks'),
                   KeyboardButton(text='22 номера', callback_data='22_tasks')],
                  [KeyboardButton(text="Список сложных слов", callback_data='word_list')],
                  [KeyboardButton(text="Добавить слово", callback_data='add_word'),
                   KeyboardButton(text="остановить", callback_data='stop')]]
kb = ReplyKeyboardMarkup(keyboard=reply_keyboard,
                         input_field_placeholder="Воспользуйтесь меню:")

tasks_keyboard = [[KeyboardButton(text='Закончить', callback_data='exit_task')]]
s_kb = ReplyKeyboardMarkup(keyboard=tasks_keyboard)

permit_keyboard = [[KeyboardButton(text='Закончить', callback_data='exit_task'),
                    KeyboardButton(text='Продолжить', callback_data='continue_task')]]
prem_kb = ReplyKeyboardMarkup(keyboard=permit_keyboard)
dp = Dispatcher()


async def main():
    bot = Bot(token=token)
    await dp.start_polling(bot)


@dp.message(F.text == "Закончить")
@dp.message(Command('start'))
async def process_start_command(message: types.Message):
    await message.reply(f"Привет, {message.from_user.full_name}!\nВыбирай, что будешь делать сегодня",
                        reply_markup=kb)
    print(message.text)


@dp.message(F.text == "остановить")
async def stop(message: types.Message):
    await message.reply("Пока:(", reply_markup=ReplyKeyboardRemove())


@dp.message(Command('help'))  # декоратор для обработчика команды help
async def process_help_command(message: types.Message):
    text = ['Я бот по русскому, бегу помогать вам идти к соточке!',
            'введите /start, чтобы начать']
    await message.reply('\n'.join(text))


req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()


# await message.reply("здесь будет викторина по 4", reply_markup=s_kb)
#     que, right, wrong = req
#
#     await message.reply("здесь будет викторина по 4", reply_markup=s_kb)

@dp.message(F.text == "4 номера")
async def four_task(message: types.Message):
    await message.reply("Вам будет дано слово,\nв котором не указано ударение\nВыберите правильный ответ",
                        reply_markup=prem_kb)





@dp.message(F.text == "9 номера")
async def nine_task(message: types.Message):
    await message.reply("здесь будет викторина по 9", reply_markup=s_kb)


@dp.message(F.text == "10 номера")
async def four_task(message: types.Message):
    await message.reply("здесь будет викторина по 10", reply_markup=s_kb)


@dp.message(F.text == "22 номера")
async def four_task(message: types.Message):
    await message.reply("здесь будет викторина по 22", reply_markup=s_kb)


@dp.message(F.text == "Список сложных слов")
async def word_list(message: types.Message):
    await message.reply("здесь будет список слов", reply_markup=s_kb)


@dp.message(F.text == "Добавить слово")
async def add_word(message: types.Message):
    await message.reply("можно добавить слово", reply_markup=s_kb)


if __name__ == '__main__':
    asyncio.run(main())
