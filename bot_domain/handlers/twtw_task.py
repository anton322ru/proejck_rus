from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()


@router.message(F.text == 'Продолжить 22 номера')
@router.message(F.text == '22 номера')
async def start_twtw_task(message: Message):
    global que, right
    req = cur.execute("""SELECT * FROM '22_task' ORDER BY RANDOM();""").fetchone()
    que, right = req
    right = right.split(';')
    await message.answer(f'Напишите, какое средство выразительности здесь встречается:\n{que}',
                         reply_markup=ReplyKeyboardRemove())


@router.callback_query(F.data == 'correct_4')
async def right_choice(call: CallbackQuery):
    global que, right, wrong
    await call.message.answer('Правильно', reply_markup=cont_or_exit(4))
    req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req
