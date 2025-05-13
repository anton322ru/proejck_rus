import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router, BaseMiddleware
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.sql.functions import random
from random import randint

from handlers import four_task, nine_task, ten_task, twtw_task, add_word, set_timer, mistakes_show
import os
from dotenv import load_dotenv
from keyboards.main_keyboard import main_keyb
import sqlite3

load_dotenv()
bot = Bot(token=os.environ.get('BOT_TOKEN'))
dp = Dispatcher()

router = Router()
con = sqlite3.connect('../db/users.db')
cur = con.cursor()


# позволяет доставать scheduler из агрументов фунции
class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


@dp.message(CommandStart())
@dp.message(F.text == 'Закончить')
@dp.message(F.text == 'Выйти')
async def process_start_command(message: types.Message):
    name = message.from_user.full_name
    req = cur.execute(f"""SELECT nickname FROM users_tg WHERE nickname = '{name}';""").fetchone()
    if req is None:
        cur.execute(f"""INSERT INTO users_tg(id, nickname) VALUES ({message.from_user.id}, '{name}')""")
        con.commit()
    await message.reply(f"Привет, {name.capitalize()}!\nВыбирай, что будешь делать сегодня",
                        reply_markup=main_keyb())


@dp.message(F.text == "Остановить")
async def stop(message: types.Message):
    await message.reply("Пока:(", reply_markup=ReplyKeyboardRemove())


@dp.message(Command('help'))
async def process_help_command(message: types.Message):
    text = ['Я бот по русскому, бегу помогать вам идти к соточке!',
            'введите /start, чтобы начать']
    await message.reply('\n'.join(text))


@dp.message(F.text == 'Настройки слова дня')
async def hello(message: types.Message, bot: Bot, scheduler: AsyncIOScheduler):
    await message.answer(
        text="Бот будет присылать слова, в которых была допущена ошибка, каждый день в 12:40 и 16:40 МСК"
    )
    req = cur.execute(f"""SELECT words FROM users_tg WHERE id = {message.from_user.id}""").fetchone()[0].split(';')
    scheduler.add_job(bot.send_message, 'cron', hour=12, minute=40,
                      args=(message.from_user.id, f"Слово дня: {req[randint(0, len(req) - 1)]}"))
    scheduler.add_job(bot.send_message, 'cron', hour=16, minute=40,
                      args=(message.from_user.id, f"Слово дня: {req[randint(0, len(req) - 1)]}"))


async def main():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    dp.include_routers(four_task.router, nine_task.router, ten_task.router,
                       twtw_task.router, add_word.router, mistakes_show.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    asyncio.run(main())
