from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot_domain.keyboards.for_tasks import get_cor_or_wrong
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()
que, right, wrong = 0, 0, 0


@router.message(F.text == 'Продолжить 10 номера')
@router.message(F.text == '10 номера')
async def start_ten_task(message: Message):
    global que, right, wrong
    req = cur.execute("""SELECT * FROM '10_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req
    await message.answer(f'Выберите правильное написание слова: {que}',
                         reply_markup=get_cor_or_wrong(right, wrong, 10))


@router.callback_query(F.data == 'correct_10')
async def right_choice(call: CallbackQuery):
    global que, right, wrong
    await call.message.delete()
    await call.message.answer('Правильно', reply_markup=cont_or_exit(10))
    req = cur.execute("""SELECT * FROM '10_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req


@router.callback_query(F.data == 'wrong_10')
async def wrong_choice(call: CallbackQuery):
    global que, right, wrong
    await call.message.delete()
    await call.message.answer(f'Неправильно. Правильное написание: {right}',
                              reply_markup=cont_or_exit(10))
    req = cur.execute("""SELECT * FROM '10_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req
