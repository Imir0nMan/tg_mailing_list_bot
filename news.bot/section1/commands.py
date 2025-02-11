from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import section1.keyboards as kb

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
	await message.answer("""Բարև, նախ պետք է գրանցվել /reg հրամանով,\n
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
	await state.update_data(age=message.text)
	await state.set_state(Registr.email)
	await message.answer("էլեկտրոնային հասցե «email»")


@rt.message(Registr.email)
async def steptwo(message: Message, state: FSMContext):
	await state.update_data(email=message.text)
	await state.set_state(Registr.prfrd_time)
	await message.answer("նախընտրելի ժամ՝ 8:00, 13:00, 21:00")


@rt.message(Registr.prfrd_time)
async def steptwo(message: Message, state: FSMContext):
	await state.update_data(prfrd_time=message.text)
	usr_data.update(await state.get_data())
	await message.answer("Այժմ կարող եք ընտրել հեշթեգերը /tags")
	await state.clear()


@rt.message(Command("tags"))
async def tags(message: Message):
	await message.answer("Ընտրեք տարբերակներից մինիմում 1ը", reply_markup=kb.inlinetags1())
	global i 
	i = 0


@rt.callback_query()
async def handle_hashtags(callback: CallbackQuery):
	hashtag = callback.data
	global i 
	i += 1
	await callback.answer(f"you have selected {hashtag}")
	usr_data.update({f"tag {(i)}" : hashtag})
