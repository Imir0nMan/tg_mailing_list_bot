from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import pandas as pd
import re
import section1.keyboards as kb
from section1.keyboards import timelist
from constants import THE_ID

rt = Router()

usr_data = {}
all_users_data = []


class Registr(StatesGroup):
	name = State()
	age = State()
	email = State()
	prfrd_time = State()
	hashtags = State()


@rt.message(CommandStart())
async def strt(message: Message, state: FSMContext):
	await message.answer("""Բարև, նախ պետք է գրանցվել /reg հրամանով""")


@rt.message(Command("reg"))
async def reg(message: Message, state: FSMContext):
	await state.set_state(Registr.name)
	await message.answer("Անուն Ազգանուն")
	

@rt.message(Registr.name)
async def stepone(message: Message, state: FSMContext):
	await state.update_data(name=message.text)
	await state.set_state(Registr.age)
	await message.answer("Տարիք")


@rt.message(Registr.age)
async def steptwo(message: Message, state: FSMContext):
	if not message.text.isdigit():
		await message.answer("Խնդրում եմ մուտքագրել միայն թվեր")
		return
	age = int(message.text)
	if 14 <= age <= 85:
		await state.update_data(age=age)
		await state.set_state(Registr.email)
		await message.answer("էլեկտրոնային հասցե «email»")
	else:
		await message.answer("Տարիքը պետք է լինի 14-85 միջակայքում։ Խնդրում եմ կրկին մուտքագրել:")


@rt.message(Registr.email)
async def steptre(message: Message, state: FSMContext):
	email = message.text.strip()
	allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "mail.ru"]
	email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.(?:com|net|org|edu|gov|mil|biz|info|ru|am)$"
	if not re.match(email_pattern, email):
		await message.answer("Խնդրում եմ մուտքագրել վավեր email (օրինակ՝ example@gmail.com)")
		return
	domain = email.split("@")[-1]
	if domain not in allowed_domains:
		await message.answer(f"Email-ը պետք է ավարտվի {', '.join(allowed_domains)}-ով։ Փորձեք կրկին:")
		return
	await state.update_data(email=email)
	await state.set_state(Registr.prfrd_time)
	await message.answer("նախընտրելի ժամ՝ 8:00, 13:00, 21:00", reply_markup=kb.settime())


@rt.callback_query(F.data.in_(timelist))
async def stepfor(callback: CallbackQuery, state: FSMContext):
	await state.update_data(prfrd_time=callback.data)
	await callback.message.answer("Այժմ կարող եք ընտրել հեշթեգերը /tags")
	await callback.answer("ընտրությունը պահպանված է")


@rt.message(Command("tags"))
async def tags(message: Message, state: FSMContext):
	await state.set_state(Registr.hashtags)
	await state.update_data(tags=[])
	await message.answer("""
		Ընտրեք տարբերակներից մինիմում 1ը,
		ընտրված հեշթեգերը տեսնելու համար կիրառեք /list_tags հրամանը,
		սխալ հեշթեգ ընտրելու դեպքում կրկին սեղմեք /tags հրամանին 
		այնուհետև նորից ընտրեք անհրաժեշտները,
		ավարտելուց հետո օգտագործեք /finish հրամանը """, reply_markup=kb.inlinetags1())
	global i
	i = 0


@rt.callback_query()
async def handle_hashtags(callback: CallbackQuery, state: FSMContext):
	hashtag = callback.data
	global i
	i += 1
	usr_data = await state.get_data()
	tags = usr_data.get("tags", [])
	if hashtag not in tags:
		tags.append(hashtag)
		await state.update_data(tags=tags)
	
	await callback.answer(f"Դուք ընտրել եք {hashtag}-ը")


@rt.message(Command("list_tags"))
async def list_tags(message: Message, state: FSMContext):
	usr_data = await state.get_data()
	tags = usr_data.get("tags", [])
	strtags = ", ".join(tags)
	if not tags:
		await message.answer("Դուք դեռ հեշթեգեր չեք ընտրել")
	else:
		await message.answer(f"Ձեր ընտրած հեշթեգերը հետևյալն են {strtags}")
		await message.answer("եթե ավարտել եք սեղմեք /finish հրամանին")


async def save_to_excel():
	df = pd.DataFrame(all_users_data)
	df.to_excel("userdata.xlsx", index=False, engine="openpyxl")


@rt.message(Command('finish'))
async def send_file(message: Message, state: FSMContext):
	usr_data = {"user_id": message.from_user.id}
	for i in all_users_data:
		if i["user_id"] == usr_data["user_id"]:
			all_users_data.remove(i)
	usr_data.update(await state.get_data())
	all_users_data.append(usr_data.copy())
	await state.clear()
	await save_to_excel()

	await message.answer("Տվյաները հաջողությամբ պահպանվել են")


@rt.message(Command('getdata'))
async def send_excel(message: Message, bot: Bot):
	excel_file = "userdata.xlsx"
	input_file = FSInputFile(excel_file)
	nk_id = THE_ID
	await bot.send_document(chat_id=nk_id, document=input_file)


