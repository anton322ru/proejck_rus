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


@router.message(F.text == "4 номера")
async def four_start(message: Message):
    await message.answer(
        f'Поставьте ударение в слове: {que}',
        reply_markup=get_cor_or_wrong(right, wrong)
    )


@router.message(F.text == right)
async def answer_yes(message: Message):
    global que, right, wrong
    await message.answer(
        "Это правильный ответ",
        reply_markup=cont_or_exit()
    )
    req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req


@router.message(F.text == wrong)
async def answer_no(message: Message):
    global que, right, wrong
    await message.answer(
        f"Неправильно. Верное ударение: {right}",
        reply_markup=cont_or_exit()
    )
    req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req


@router.message(F.text != wrong and F.text != right)
async def answer_hehe(message: Message):
    await message.answer(
        f"АААА НЕПРАВИЛЬНО {que}, {wrong}, {right}, {F.text}",
        reply_markup=cont_or_exit()
    )
