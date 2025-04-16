from dotenv import load_dotenv
load_dotenv()

import requests
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=os.getenv('token'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    asyncio.create_task(repeated_task(bot))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

