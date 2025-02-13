from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import re
import section1.keyboards as kb
from constants import THE_ID

rt = Router()

usr_data = {}


class Registr(StatesGroup):
	name = State()
	age = State()
	email = State()
	prfrd_time = State()


@rt.message(CommandStart())
async def strt(message: Message):
	usr_data["user_id"] = message.from_user.id
	await message.answer("""Բարև, նախ պետք է գրանցվել /reg հրամանով,
	ապա ընտրել նախընտրելի հեշթեգերը /tags հրամանով""")


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
		await message.answer("Տարիքը պետք է լինի 15-85 միջակայքում։ Խնդրում եմ կրկին մուտքագրել:")


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
	await message.answer("նախընտրելի ժամ՝ 8:00, 13:00, 21:00")


@rt.message(Registr.prfrd_time)
async def stepfor(message: Message, state: FSMContext):
	await state.update_data(prfrd_time=message.text)
	usr_data.update(await state.get_data())
	await message.answer("Այժմ կարող եք ընտրել հեշթեգերը /tags")
	await state.clear()


@rt.message(Command("tags"))
async def tags(message: Message):
	await message.answer("""Ընտրեք տարբերակներից մինիմում 1ը, 
		ավարտելուց հետո օգտագործեք /finish հրամանը """, reply_markup=kb.inlinetags1())
	global i 
	i = 0


@rt.callback_query()
async def handle_hashtags(callback: CallbackQuery):
	hashtag = callback.data
	global i 
	i += 1
	await callback.answer(f"Դուք ընտրել եք {hashtag}-ը")
	usr_data.update({f"tag {(i)}" : hashtag})


@rt.message(Command('finish'))
async def send_file(message: Message, bot: Bot):
    # Create the txt file based on user data (including hashtags)
    txt_data = "\n".join([f"{key}: {value}" for key, value in usr_data.items()])
    
    txt_file = "userdata.txt"
    with open(txt_file, "w", encoding="utf-8") as file:
        file.write(txt_data)

    input_file = FSInputFile(txt_file)

    nk_id = THE_ID
    
    # Send the file
    await bot.send_document(chat_id=nk_id, document=input_file)

    await message.answer("Տվյաները հաջողությամբ պահպանվել են")

