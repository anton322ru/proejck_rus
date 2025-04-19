from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from bot_domain.keyboards.for_tasks import get_cor_or_wrong
from bot_domain.keyboards.continue_task import cont_or_exit

router = Router()


@router.message(F.text == 'Добавить слово')
async def start(message: Message):
    await message.answer(f'В каком слове вы допустили ошибку?', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Какое это было задание?', reply_markup=ReplyKeyboardRemove())
