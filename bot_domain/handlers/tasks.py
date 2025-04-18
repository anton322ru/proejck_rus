from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from bot_domain.bot_main import word_list
from bot_domain.keybords.for_tasks import get_cor_or_wrong
from bot_domain.keybords.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()
req = cur.execute("""SELECT * FROM '4_task' ORDER BY RANDOM();""").fetchone()
que, right, wrong = req[0]



@router.message(F.text == "4 номера")
async def four_start(message: Message):
    global que, right, wrong
    await message.answer(
        f'Поставьте ударение в слове: {que}',
        reply_markup=get_cor_or_wrong(right, wrong)
    )



@router.message(F.text == right)
async def answer_yes(message: Message):
    await message.answer(
        "Это правильный ответ",
        reply_markup=cont_or_exit()
    )


@router.message(F.text == wrong)
async def answer_no(message: Message):
    await message.answer(
        f"Неправильно. Верное ударение: {right}",
        reply_markup=cont_or_exit()
    )
