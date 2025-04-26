from pyexpat.errors import messages

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot_domain.keyboards.add_word import add_words
from bot_domain.keyboards.continue_task import cont_or_exit
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


class Form(StatesGroup):  # создаем статусы, через которые будет проходить пользователь
    word = State()
    task = State()


@router.message(F.text == 'Добавить слово')
async def start(message: Message):
    await message.answer(f'В каком задании встретилось данное слово?', reply_markup=add_words())
