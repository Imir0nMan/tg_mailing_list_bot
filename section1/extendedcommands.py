import datetime
from collections import deque
from aiogram.enums import ContentType
from constants import CHANNEL_ID
from database.database import get_user_data, delete_user
from section1.commands import *

@rt.message(Command("pt"))
async def printme(message: Message):
	user1_data = get_user_data()
	print(user1_data)


@rt.channel_post()
async def handle_channel_post(message: Message, bot: Bot):
	all_users = get_user_data()
	print("are we there yet ?")
	message_content = message.text or message.caption
	for user in all_users:
		user_id = user["user_id"]
		tags = user.get("tags", [])
		if message_content and any(tag in message_content for tag in tags):
			if user["prfrd_time"] == 'Realtime':
				await bot.send_message(user_id, f"New message from channel:\n{message.text}")
			else:
				pass


@rt.message(Command("unfollow"))
async def deletemydata(message: Message):
	user_id = message.from_user.id
	delete_user(user_id)
