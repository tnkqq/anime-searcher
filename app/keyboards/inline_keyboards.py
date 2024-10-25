from typing import Dict, List, Optional, Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pydantic import ValidationError


class AnimeRequestData(CallbackData, prefix="anime-api-reponse-data"):
    message: str
    offset: int


def build_anime_pagination_kb(
    message: str,
    offset: int = 0,
) -> InlineKeyboardMarkup:
    try:
        builder = InlineKeyboardBuilder()
        cb_data_next = AnimeRequestData(message=message, offset=offset + 1)
        cb_data_prev = AnimeRequestData(message=message, offset=offset - 1)
        builder.button(text="◀️", callback_data=cb_data_prev.pack())
        builder.button(text="▶️", callback_data=cb_data_next.pack())
        return builder.as_markup()
    except ValidationError as e:
        print(e.json())
