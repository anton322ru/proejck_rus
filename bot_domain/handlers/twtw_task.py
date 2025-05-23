from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()
que, right = 0, 0


class Form(StatesGroup):
    ans = State()


@router.message(F.text == 'Продолжить 22 номер')
@router.message(F.text == '22 номер')
async def start_twtw_task(message: Message, state: FSMContext):
    global id_req, que, right
    req = cur.execute("""SELECT * FROM '22_task' ORDER BY RANDOM();""").fetchone()
    id_req, que, right = req
    right = right.split(';')
    await state.set_state(Form.ans)
    que = que.replace(r"\n", "\n")
    await message.answer(f'Напишите, какое средство выразительности здесь встречается:\n{que}',
                         reply_markup=ReplyKeyboardRemove())


@router.message(Form.ans)  # обработчик для определенного статуса
async def giving_answer(message: Message, state: FSMContext):
    await state.clear()
    ans = message.text
    if ans in right:
        await message.answer(f"Да. В этом отрывке были такие средства как {', '.join(right)}",
                             reply_markup=cont_or_exit(22))
    else:
        await message.answer(f'Нет. Здесь были следующие средства: {", ".join(right)}',
                             reply_markup=cont_or_exit(22))
