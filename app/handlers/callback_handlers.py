from aiogram.types import CallbackQuery, InputMediaPhoto
from keyboards.inline_keyboards import AnimeRequestData, build_anime_pagination_kb
from loader import dp
from services.api import Animeapi

from .formatters import format_anime_message


@dp.callback_query(AnimeRequestData.filter())
async def next_anime(callback: CallbackQuery, callback_data: AnimeRequestData):
    request = callback_data.message
    offset = callback_data.offset
    anime = Animeapi(request)
    anime_list = anime.fetch_anime_data_by_title()
    if offset > len(anime_list) - 1:
        offset = 0
    elif offset < 0:
        offset = len(anime_list) - 1
    msg, poster = format_anime_message(anime_list[offset])
    await callback.message.edit_media(
        media=InputMediaPhoto(caption=msg, media=poster),
        reply_markup=build_anime_pagination_kb(message=request, offset=offset),
    )
