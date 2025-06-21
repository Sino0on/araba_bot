import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
# from app.config import settings
from decouple import config
from app.handlers import start, evacuator, client

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config('BOT_TOKEN'), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    # Register handlers
    dp.include_routers(
        start.router,
        evacuator.router,
        client.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
