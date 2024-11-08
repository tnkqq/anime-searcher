from typing import Dict, List, Optional, Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import ValidationError


class AnimeRequestData(CallbackData, prefix="anime-api-response-data"):
    message: str
    offset: int


class AnimeRateData(CallbackData, prefix="anime-rate-data"):
    message: str
    is_user_rate: bool
    score: int
    anime_id: int
    offset: int
    current_user_rate: int | None


def build_anime_pagination_kb(
    message: str,
    anime_id: int,
    offset: int = 0,
    user_rate: int = None,
) -> InlineKeyboardMarkup:
    # try:
    builder = InlineKeyboardBuilder()
    cb_data_next = AnimeRequestData(message=message, offset=offset + 1)
    cb_data_prev = AnimeRequestData(message=message, offset=offset - 1)
    builder.button(text="◀️", callback_data=cb_data_prev.pack()),
    builder.button(text="▶️", callback_data=cb_data_next.pack())
    for _ in range(1, 11):
        if user_rate == _:
            ur = True
        else:
            ur = False
        rate_data = AnimeRateData(
            message=message,
            is_user_rate=ur,
            score=int(_),
            anime_id=int(anime_id),
            offset=int(offset),
            current_user_rate=user_rate,
        )
        if user_rate == _:
            text = "⭐️"
        else:
            text = str(_)
        builder.button(text=text, callback_data=rate_data.pack())
    builder.adjust(2, 5, 5)
    return builder.as_markup()
    # except ValidationError as e:
    #     print(e.json())


# def build_anime_rate_kb(
#     message: str,
#     user_rate: int | None,
# ) -> InlineKeyboardBuilder:
#     builder = InlineKeyboardBuilder()

#     return builder.as_markup()


# def markup_builder()
