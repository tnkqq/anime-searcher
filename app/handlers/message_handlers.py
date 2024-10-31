from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, Message
from keyboards.inline_keyboards import build_anime_pagination_kb
from loader import bot, dp
from services.api import Animeapi

from .formatters import format_anime_message


@dp.message()
async def anime_by_title(message: Message, state: FSMContext) -> None:
    await message.delete()
    try:
        anime = Animeapi(title=message.text)
        anime_list = anime.fetch_anime_data_by_title()
        msg, poster = format_anime_message(anime_data=anime_list[0])
        msg_to_edit = (await state.get_data()).get("msg_id_edit")
        answer = await bot.edit_message_media(
            media=InputMediaPhoto(media=poster, caption=msg),
            reply_markup=build_anime_pagination_kb(message=message.text),
            chat_id=message.chat.id,
            message_id=msg_to_edit,
        )
    except IndexError:
        answer = await message.answer(text="Anime Not found")
    except TelegramBadRequest:
        answer = await message.answer(text="Перезапустите бота для корректной!")
    finally:
        await state.update_data(msg_to_edit=answer.message_id)
