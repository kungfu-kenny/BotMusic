from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from config import CALLBACKS


def get_text_message(message: object) -> str:
    pass


def _split_list_selected(value_list: list, chunk: int=5) -> list:
    "Return list of lists with selected chunks"
    return [
        value_list[i:i+chunk] for i in range(0, len(value_list), chunk)
    ]


def _get_reply_keyboard_basic() -> object:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=False,
        keyboard=[
            [
                InlineKeyboardButton(
                    text='Search song'
                ),
                InlineKeyboardButton(
                    text='Search Album'
                ),
            ],
            [
                InlineKeyboardButton(
                    text='History',
                ),
                InlineKeyboardButton(
                    text='Settings',
                ),
            ],
        ]
    )


def _get_inline_keyboard(value_dict: dict, keyboard_type: str, value_index: int = 0) -> object:
    inline_keyboard = _split_list_selected(
        [
            [
                InlineKeyboardButton(
                    text=callback_dict[key],
                    callback_data=callback_data,
                )
                for key, callback_data in zip(
                    [
                        "name",
                        "duration",
                    ],
                    [
                        callback,
                        "None",
                    ],
                )
            ]
            for callback, callback_dict in value_dict.items()
        ]
    )
    value_prev = value_index - 1
    value_next = value_index + 1
    if value_next > len(inline_keyboard) - 1:
        value_next = value_next % len(inline_keyboard)
    if value_prev < 0:
        value_prev = value_prev % len(inline_keyboard)
    value_number = f"{value_index + 1} / {len(inline_keyboard)}"
    inline_keyboard = inline_keyboard[value_index]
    if keyboard_type == 'album':
        inline_keyboard.insert(
            0,
            [
                InlineKeyboardButton(
                    text="Album Name | Track Number",
                    callback_data="None",
                )
            ],
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f"{CALLBACKS['CALLBACK_ALBUM_MENU_PREV']}_{value_prev}",
                ),
                InlineKeyboardButton(
                    text=value_number,
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f"{CALLBACKS['CALLBACK_ALBUM_MENU_NEXT']}_{value_next}",
                ),
            ]
        )
    elif keyboard_type == 'song':
        inline_keyboard.insert(
            0,
            [
                InlineKeyboardButton(
                    text="Song Name | Track Duration",
                    callback_data="None",
                )
            ],
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=f"{CALLBACKS['CALLBACK_SONG_MENU_PREV']}_{value_prev}",
                ),
                InlineKeyboardButton(
                    text=value_number,
                    callback_data="None",
                ),
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=f"{CALLBACKS['CALLBACK_SONG_MENU_NEXT']}_{value_next}",
                ),
            ]
        )
    return inline_keyboard


def get_menu_album(value_dict: dict, value_index: int) -> object:
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=_get_inline_keyboard(value_dict, 'album', value_index),
    )


def get_menu_song(value_dict: dict, value_index: int) -> object:
    return InlineKeyboardMarkup(
        row_width=3,
        inline_keyboard=_get_inline_keyboard(value_dict, 'song', value_index),
    )
