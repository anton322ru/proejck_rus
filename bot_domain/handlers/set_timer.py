from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from bot_domain.keyboards.timer_dec import timer_dec
from bot_domain.keyboards.exit_for_timer import timer_exit
from aiogram import BaseMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


class Form(StatesGroup):
    timer = State()


@router.message(F.text == 'Настройки слова дня')
async def start_word(message: Message, ):
    await message.answer(f'Выберите, когда вам присылать слово дня',
                         reply_markup=timer_dec())
    scheduler.add_job(bot.send_message, 'interval', seconds=30, args=(id, "Я напоминаю каждые 30 секунд"))
    # задаём выполнение задачи по cron - гибкий способ задавать расписание.
    scheduler.add_job(bot.send_message, 'cron', hour=00, minute=34, args=(id, "Я напомнил в 00.32 по Москве"))
