import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher

import config
from handlers.main_handler import main_router

dp = Dispatcher()
dp.include_router(main_router)


async def main() -> None:
    bot = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот выключен")
    except Exception as e:
        logging.error(e)
