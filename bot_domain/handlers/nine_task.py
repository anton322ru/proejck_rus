from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot_domain.keyboards.for_tasks import get_cor_or_wrong
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/tasks.db')
cur = con.cursor()
que, right, wrong = 0, 0, 0


@router.message(F.text == 'Продолжить 9 номера')
@router.message(F.text == '9 номера')
async def start_nine_task(message: Message):
    global id_req, que, right, wrong
    req = cur.execute("""SELECT * FROM '9_task' ORDER BY RANDOM();""").fetchone()
    id_req, que, right, wrong = req
    await message.answer(f'Выберите правильное написание слова: {que}', reply_markup=get_cor_or_wrong(right, wrong, 9))


@router.callback_query(F.data == 'correct_9')
async def right_choice(call: CallbackQuery):
    global id_req, que, right, wrong
    await call.message.delete()
    await call.message.answer('Правильно', reply_markup=cont_or_exit(9))
    req = cur.execute("""SELECT * FROM '9_task' ORDER BY RANDOM();""").fetchone()
    id_req, que, right, wrong = req


con_user = sqlite3.connect('../db/users.db')
cur_user = con_user.cursor()


@router.callback_query(F.data == 'wrong_9')
async def wrong_choice(call: CallbackQuery):
    global id_req, que, right, wrong
    await call.message.delete()
    req_all_mistakes = \
        cur_user.execute(f"""SELECT mistakes_9 FROM users_tg WHERE id = {call.from_user.id}""").fetchone()[0]
    if req_all_mistakes is not None:
        res_mistakes = f"{req_all_mistakes};{id_req}"
    else:
        res_mistakes = f'{id_req}'
    req = cur_user.execute(f"""UPDATE users_tg 
                                 SET mistakes_9 = '{res_mistakes}'
                                 WHERE id = {call.from_user.id};""")
    con_user.commit()

    await call.message.answer(f'Неправильно. Правильное написание: {right}', reply_markup=cont_or_exit(9))
    req = cur.execute("""SELECT * FROM '9_task' ORDER BY RANDOM();""").fetchone()
    id_req, que, right, wrong = req
