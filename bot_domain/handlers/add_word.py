from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot_domain.keyboards.for_tasks import get_cor_or_wrong
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()
req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
que, right, wrong = req


@router.message(F.text == '4 номера')
async def start_four_task(message: Message):
    await message.answer(f'Поставьте ударение в слове: {que}', reply_markup=get_cor_or_wrong(right, wrong))

@router.callback_query(F.data == 'correct')
async def right_choice(call: CallbackQuery):
    await call.message.answer('Правильно', reply_markup=cont_or_exit())