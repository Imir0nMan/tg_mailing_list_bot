from aiogram import Dispatcher

from constants import TOKEN
from section1.extendedcommands import asyncio, rt, Bot, send_accumulated_messages

#intializating bot with token
bot = Bot(token=TOKEN)
dp=Dispatcher()

async def main():
	#run message mailing
	asyncio.create_task(send_accumulated_messages(bot))
	dp.include_router(rt)
	await dp.start_polling(bot)


if __name__ == "__main__":
	asyncio.run(main())
