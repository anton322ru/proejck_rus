from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot_domain.keyboards.for_tasks import get_cor_or_wrong
from bot_domain.keyboards.continue_task import cont_or_exit
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()


class Form(StatesGroup):  # создаем статусы, через которые будет проходить пользователь
    word = State()


@router.message(F.text == 'Добавить слово')
async def start(message: Message):
    await message.answer(f'Напишите правильно слово, которое вы хотите запомнить', reply_markup=ReplyKeyboardRemove())