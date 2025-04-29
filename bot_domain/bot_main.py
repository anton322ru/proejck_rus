import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F, Router, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from random import randint

from handlers import four_task, nine_task, ten_task, twtw_task, add_word, set_timer, mistakes_show
import os
from dotenv import load_dotenv
from keyboards.main_keyboard import main_keyb
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler


# позволяет доставать scheduler из агрументов фунции
class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
dp = Dispatcher()
router = Router()

dp.include_routers(four_task.router, nine_task.router, ten_task.router,
                   twtw_task.router, set_timer.router, mistakes_show.router)
bot = Bot(token=os.environ.get('BOT_TOKEN'))
con = sqlite3.connect('../db/users.db')
cur = con.cursor()

con_task = sqlite3.connect('../db/tasks.db')
cur_task = con_task.cursor()


# сделать main клавиатуру одноразовой
# таймер
# добавление слова - оно может появиться в слове дня/ будет висеть на сайте/
async def main():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.start()
    dp.update.middleware(SchedulerMiddleware(scheduler=scheduler))
    await dp.start_polling(bot)


@dp.message(F.text == 'Закончить')
@dp.message(Command('start'))
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
async def set_timer(message: types.Message, scheduler: AsyncIOScheduler):
    await  message.answer('Я пришлю вам сейчас скобочку))')
    reres = []
    for i in (4, 9, 10):
        req = cur.execute(f"SELECT mistakes_{i} FROM users_tg WHERE id = {message.from_user.id}").fetchone()[0].split(
            ';')
        res = cur_task.execute(f"SELECT correct FROM '{i}_task' WHERE id IN ({', '.join(req)})").fetchall()
        res = [i[0] for i in res]
        reres += res
    # задаём выполнение задачи в равные промежутки времени
    scheduler.add_job(bot.send_message, 'interval', seconds=5,
                      args=(message.from_user.id, f"Ваше слово дня: {reres[randint(0, len(reres))]}"))


if __name__ == '__main__':
    asyncio.run(main())
