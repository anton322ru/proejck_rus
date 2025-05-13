import sqlite3
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from bot_domain.keyboards.add_word import add_words
from bot_domain.keyboards.continue_task import cont_or_exit
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()
con = sqlite3.connect('../db/users.db')
cur = con.cursor()


class Form(StatesGroup):  # создаем статусы, через которые будет проходить пользователь
    word = State()


@router.message(F.text == 'Добавить слово')
async def start(message: Message, state: FSMContext):
    text = ['Напишите слово, в котором допустили ошибку',
            'Если ошиблись в написании, то обратись к сайту, чтобы исправить:)']
    await state.set_state(Form.word)
    await message.answer('\n'.join(text), reply_markup=ReplyKeyboardRemove())


@router.message(Form.word)  # обработчик для определенного статуса
async def giving_answer(message: Message, state: FSMContext):
    await state.clear()
    ans = message.text
    req = cur.execute(f"""SELECT words FROM users_tg WHERE id = {message.from_user.id}""").fetchone()[0]
    if req:
        req += f';{ans}'
    else:
        req = ans
    req1 = cur.execute(f"""UPDATE users_tg
    SET words = '{req}'
    WHERE id = {message.from_user.id}""")
    con.commit()
    await message.answer(f"Ваше слово было сохранено, ожидайте его в уведомлениях)",
                         reply_markup=cont_or_exit(22))
