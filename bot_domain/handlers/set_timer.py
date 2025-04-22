from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from bot_domain.keyboards.timer_dec import timer_dec
from bot_domain.keyboards.exit_for_timer import timer_exit

router = Router()


class Form(StatesGroup):
    timer = State()


@router.message(F.text == 'Настройки слова дня')
async def start_word(message: Message):
    await message.answer(f'Выберите, когда вам присылать слово дня',
                         reply_markup=timer_dec())
