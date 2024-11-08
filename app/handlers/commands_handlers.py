from aiogram import types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from loader import dp
from services.orm.orm import AnimeORM

from .states import UserState


@dp.message(CommandStart())
async def command_start_handler(msg: types.Message, state: FSMContext):
    await msg.delete()
    await state.clear()
    await state.set_state(UserState.msg_to_edit)
    telegram_id = msg.from_user.id
    username = msg.from_user.username
    try:
        await AnimeORM.insert_new_user(
            telegram_id=telegram_id, username=username
        )
    except:
        pass
    finally:
        answer = await msg.answer_animation(
            animation="https://tenor.com/ru/view/hello-gif-26559516",
            caption=(
                f"""Привет, {msg.from_user.full_name}. Бот для поиска аниме! \n"""
                f"""Введите название тайтла"""
            ),
        )
        await state.update_data(msg_id_edit=answer.message_id)
