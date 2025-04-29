Создаем функцию, в которой будет происходить запуск наших тасков.
def set_scheduled_jobs(scheduler, bot, config, *args, **kwargs):
    # Добавляем задачи на выполнение

    scheduler.add_job(send_message_to_admin, "interval", seconds=5, args=(bot, config))
    # scheduler.add_job(some_other_regular_task, "interval", seconds=100)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    scheduler = AsyncIOScheduler()
    bot['config'] = config
    register_all_middlewares(dp, scheduler)
    register_all_filters(dp)
    register_all_handlers(dp)

    # Ставим наши таски на запуск, передаем нужные переменные.
     set_scheduled_jobs(scheduler, bot, config)

    # start
    try:
        scheduler.start()
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")