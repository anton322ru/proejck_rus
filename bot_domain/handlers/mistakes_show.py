from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from bot_domain.keyboards.continue_task import cont_or_exit
import sqlite3

router = Router()
con = sqlite3.connect('../db/users.db')
cur = con.cursor()

con_task = sqlite3.connect('../db/tasks.db')
cur_task = con_task.cursor()


@router.message(F.text == 'Список ошибок')
async def show_mist(message: Message):
    reres = {}
    for i in (4, 9, 10):
        req = cur.execute(f"SELECT mistakes_{i} FROM users_tg WHERE id = {message.from_user.id}").fetchone()[0].split(
            ';')
        res = cur_task.execute(f"SELECT correct FROM '{i}_task' WHERE id IN ({', '.join(req)})").fetchall()
        res = [i[0] for i in res]
        reres[i] = res
    res_text = ''
    for num, i in reres.items():
        res_text += f'\n<b>{num} НОМЕР</b>\n'
        res_text += '\n'.join(i)
    await message.answer(f'Ваши ошибки:\n{res_text}', reply_markup=cont_or_exit('mistakes'), parse_mode=ParseMode.HTML)
