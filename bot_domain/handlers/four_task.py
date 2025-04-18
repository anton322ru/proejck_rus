from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot_domain.keyboards.for_tasks import get_cor_or_wrong
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()
que, right, wrong = 0, 0, 0


@router.message(F.text == 'Продолжить 4 номера')
@router.message(F.text == '4 номера')
async def start_four_task(message: Message):
    global que, right, wrong
    req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req
    await message.answer(f'Поставьте ударение в слове: {que}', reply_markup=get_cor_or_wrong(right, wrong, 4))

@router.callback_query(F.data == 'correct_4')
async def right_choice(call: CallbackQuery):
    await call.message.delete()
    global que, right, wrong
    await call.message.answer('Правильно', reply_markup=cont_or_exit(4))
    req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req


@router.callback_query(F.data == 'wrong_4')
async def wrong_choice(call: CallbackQuery):
    global que, right, wrong
    await call.message.delete()
    await call.message.answer(f'Неправильно. Правильное ударение: {right}', reply_markup=cont_or_exit(4))
    req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req
