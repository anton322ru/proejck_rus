from aiogram import Router, F
from aiogram.types import Message
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/users.db')
cur = con.cursor()

con_task = sqlite3.connect('../db/tasks.db')
cur_task = con_task.cursor()


@router.message(F.text == 'Список ошибок')
async def show_mist(message: Message):
    req_4 = cur.execute(f"SELECT mistakes_4 FROM users_tg WHERE id = {message.from_user.id}").fetchone()[0].split(
        ';')
    res_4 = cur_task.execute(f"SELECT correct FROM '4_task' WHERE id IN ({', '.join(req_4)})").fetchall()
    res_4 = [i[0] for i in res_4]
    await message.answer(f'Ваши ошибки:\n{"\n".join(res_4)}', reply_markup=cont_or_exit('mistakes'))
