import asyncio
from aiogram import Dispatcher

from constants import TOKEN
from section1.commands import rt, Bot
import database.database


bot = Bot(token=TOKEN)
dp=Dispatcher()

async def main():
	dp.include_router(rt)
	await dp.start_polling(bot)


if __name__ == "__main__":
	asyncio.run(main())
