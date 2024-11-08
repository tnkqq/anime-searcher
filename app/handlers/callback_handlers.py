from aiogram.types import CallbackQuery, InputMediaPhoto
from keyboards.inline_keyboards import (AnimeRateData, AnimeRequestData,
                                        build_anime_pagination_kb)
from loader import dp
from services.api import Animeapi
from services.orm.orm import AnimeORM

from .formatters import format_anime_message


@dp.callback_query(AnimeRequestData.filter())
async def pagination(callback: CallbackQuery, callback_data: AnimeRequestData):
    request = callback_data.message
    offset = callback_data.offset
    anime = Animeapi(request)
    anime_list = anime.fetch_anime_data_by_title()
    if offset > len(anime_list) - 1:
        offset = 0
    elif offset < 0:
        offset = len(anime_list) - 1
    user_anime_rate = await AnimeORM.select_anime_rate_by_telegram_user(
        telegram_user_id=callback.from_user.id,
        anime_id=int(anime_list[offset].get("id")),
    )
    msg, poster = format_anime_message(anime_list[offset])
    await callback.message.edit_media(
        media=InputMediaPhoto(caption=msg, media=poster),
        reply_markup=build_anime_pagination_kb(
            message=request,
            offset=offset,
            user_rate=user_anime_rate,
            anime_id=anime_list[offset].get("id"),
        ),
    )


@dp.callback_query(AnimeRateData.filter())
async def rate(callback: CallbackQuery, callback_data: AnimeRateData):

    user_anime_rate = callback_data.current_user_rate

    if user_anime_rate:
        await AnimeORM.update_anime_rate_by_user(
            anime_id=callback_data.anime_id,
            score=callback_data.score,
            telegram_user_id=callback.from_user.id,
        )
    else:
        await AnimeORM.insert_anime_rate_by_user(
            anime_id=callback_data.anime_id,
            score=callback_data.score,
            telegram_user_id=callback.from_user.id,
        )

    await callback.message.edit_reply_markup(
        reply_markup=build_anime_pagination_kb(
            message=callback_data.message,
            anime_id=callback_data.anime_id,
            offset=callback_data.offset,
            user_rate=callback_data.score,
        )
    )
