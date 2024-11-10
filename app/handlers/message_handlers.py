from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaAnimation, InputMediaPhoto, Message
from keyboards.inline_keyboards import build_anime_pagination_kb
from loader import bot, dp
from services.api import Animeapi
from services.orm.orm import AnimeORM

from .formatters import format_anime_message


@dp.message()
async def anime_by_title(message: Message, state: FSMContext) -> None:
    await message.delete()
    msg_to_edit = (await state.get_data()).get("msg_id_edit")
    answer = None
    try:
        anime_list = await Animeapi.get_anime_by_title(message.text)

        user_anime_rate = await AnimeORM.select_anime_rate_by_telegram_user(
            telegram_user_id=message.from_user.id,
            anime_id=int(anime_list[0].get("id")),
        )

        if user_anime_rate is not None:
            user_anime_rate = int(user_anime_rate)

        msg, poster = format_anime_message(anime_data=anime_list[0])
        kb_data = {
            "message": message.text,
            "offset": 0,
            "user_rate": user_anime_rate,
            "anime_id": anime_list[0].get("id"),
        }

        try:
            answer = await bot.edit_message_media(
                media=InputMediaPhoto(media=poster, caption=msg),
                reply_markup=build_anime_pagination_kb(**kb_data),
                chat_id=message.chat.id,
                message_id=msg_to_edit,
            )
        except TelegramBadRequest:
            pass

    except IndexError:
        try:
            answer = await bot.edit_message_media(
                media=InputMediaAnimation(
                    media="https://media1.tenor.com/m/3ZCZb2Jtf0QAAAAd/error-what.gif",
                    caption=f'Anime "{message.text}" not found',
                ),
                chat_id=message.chat.id,
                message_id=msg_to_edit,
            )
        except TelegramBadRequest:
            pass

    finally:
        if answer is not None:
            await state.update_data(msg_to_edit=answer.message_id)
