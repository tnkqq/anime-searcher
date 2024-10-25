from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from loader import dp

from .states import UserState


@dp.message(CommandStart())
async def command_start_handler(msg: types.Message, state: FSMContext):

    await msg.delete()
    await state.set_state(UserState.msg_to_edit)
    answer = await msg.answer_photo(
        photo="https://i.pinimg.com/736x/fb/75/e2/fb75e2c65d88b7c19f99a6dd458cf7d8.jpg",
        caption=(
            f"""Привет, {msg.from_user.full_name}. Бот для поиска аниме! \n"""
            f"""Введите название тайтла"""
        ),
    )
    await state.update_data(msg_id_edit=answer.message_id)
