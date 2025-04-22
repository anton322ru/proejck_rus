from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State

router = Router()


class Form(StatesGroup):
    timer = State()


@router.message(F.text == 'Настройки слова дня')
async def (message: Message):
    await message.answer(f'Выберите правильное написание слова: {que}', reply_markup=get_cor_or_wrong(right, wrong, 9))


@router.callback_query(F.data == 'correct_9')
async def right_choice(call: CallbackQuery):
    global que, right, wrong
    await call.message.delete()
    await call.message.answer('Правильно', reply_markup=cont_or_exit(9))
    req = cur.execute("""SELECT * FROM '9_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req


@router.callback_query(F.data == 'wrong_9')
async def wrong_choice(call: CallbackQuery):
    global que, right, wrong
    await call.message.delete()
    await call.message.answer(f'Неправильно. Правильное написание: {right}', reply_markup=cont_or_exit(9))
    req = cur.execute("""SELECT * FROM '9_task' ORDER BY RANDOM();""").fetchone()
    que, right, wrong = req
