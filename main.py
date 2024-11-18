import asyncio
from aiogram import Bot, Dispatcher
import logging

from config import TOKEN
from logger import configure_logging
from handlers import router

print('Running')

logger = logging.getLogger(__name__)
configure_logging(logging.DEBUG)

try:
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
except Exception as e:
    logger.exception(e)


async def main():
    logger.info('Start')
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Exit')
        print('Exit')