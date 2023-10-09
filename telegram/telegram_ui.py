from aiogram.types import Message, CallbackQuery

from telegram.telegram_usage import dp, bot
from scrapers.get_controller import get_list_selection
from telegram.filters import (
    CheckMessageChangeSearch,
    CheckMessageSelectSongFilter,
    CheckMessageSelectAlbumFilter,
    CheckSongNextFilter,
    CheckAlbumNextFilter,
)
from scrapers.get_controller import (
    get_file_song_server,
    get_file_album_server,
)
from models.database import (
    insert_user,
    select_album_search,
    change_album_search,
)
from utilities.utilities_file import _get_music_file
from utilities.utilities_ui import (
    get_menu_song,
    get_menu_album,
    _get_reply_keyboard_basic,
)


async def _send_files_telegram(value_dict_songs: dict):
    for file_name_ext, file_value_dict in value_dict_songs.items():
        title = (
            file_value_dict["title"]
            if not file_value_dict.get("name_searched")
            else file_value_dict["name_searched"]
        )
        with open(_get_music_file(file_name_ext), "rb") as music_file:
            await bot.send_audio(
                file_value_dict["sender"],
                audio=music_file,
                title=title,
            )
    for file_name_ext in value_dict_songs.keys():
        _get_music_file(file_name_ext, False)


@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    insert_user(message.chat.id)
    await message.reply(
        "Hi!\nI'm TestBot!\nDownload any music for `free`!",
        reply_markup=_get_reply_keyboard_basic(),
    )


@dp.message_handler(commands=["album"])
async def send_album(message: Message):
    insert_user(message.chat.id)
    if message.text and message.text.startswith("/album") and len(message.text) > 7:
        text_use = message.text[7:]
        value_tst = get_list_selection(text_use, False)
        await message.reply(
            f"Check album `{text_use}`",
            reply_markup=get_menu_album(value_tst, 0),
        )


@dp.message_handler(commands=["song"])
async def send_song(message: Message):
    insert_user(message.chat.id)
    if message.text and message.text.startswith("/song") and len(message.text) > 6:
        text_use = message.text[6:]
        value_search = get_list_selection(text_use)
        await message.reply(
            f"Check song `{text_use}`", reply_markup=get_menu_song(value_search, 0)
        )


@dp.message_handler(commands=["help"])
async def send_help(message: Message):
    insert_user(message.chat.id)
    await message.reply("Help is not available")


@dp.callback_query_handler(CheckAlbumNextFilter())
async def update_reply_markup_album_next(call: CallbackQuery) -> None:
    value_index = int(call.data.split("_")[-1])
    text_use = call.message.text.replace("Check album `", "")[:-1]
    value_search = get_list_selection(text_use, False)
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_menu_album(value_search, value_index),
    )


@dp.callback_query_handler(CheckSongNextFilter())
async def update_reply_markup_song_next(call: CallbackQuery) -> None:
    value_index = int(call.data.split("_")[-1])
    text_use = call.message.text.replace("Check song `", "")[:-1]
    value_search = get_list_selection(text_use)
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_menu_song(value_search, value_index),
    )


@dp.callback_query_handler(CheckMessageSelectSongFilter())
async def send_song_value(call: CallbackQuery) -> None:
    value_id, duration = call.data.split("_")[1:]
    duration = int(duration)
    track_name = None
    for element_inline in call.message.reply_markup["inline_keyboard"][1:-1]:
        for name in element_inline[:1]:
            if name.callback_data == call.data:
                track_name = name.text.strip()
                break
    if track_name:
        await bot.send_message(
            call.message.chat.id,
            f"Your song: \nhttps://www.deezer.com/us/track/{value_id}",
        )
        value_dict_songs = get_file_song_server(
            value_id,
            track_name,
            duration,
            call.message.chat.id,
        )
        await _send_files_telegram(value_dict_songs)


@dp.callback_query_handler(CheckMessageSelectAlbumFilter())
async def send_album_value(call: CallbackQuery) -> None:
    value_id = call.data.split("_")[-1]
    await bot.send_message(
        call.message.chat.id,
        f"Your album: \nhttps://www.deezer.com/us/album/{value_id}",
    )
    value_dict_songs = get_file_album_server(value_id, call.message.chat.id)
    await _send_files_telegram(value_dict_songs)


@dp.message_handler(CheckMessageChangeSearch())
async def change_search_value(message: Message) -> None:
    value_new = True if (value_song := message.text == "Search only song") else False
    change_album_search(message.chat.id, value_new)
    await message.reply(
        "We changed search from albums to songs"
        if value_song
        else "We changed search from songs to albums"
    )


@dp.message_handler()
async def send_random_text(message: Message) -> None:
    insert_user(message.chat.id)
    text_use = i if (i := message.text.strip()) else None
    if text_use:
        value_song = select_album_search(message.chat.id)
        value_search = get_list_selection(text_use, value_song)
        await message.reply(
            f"Check song `{text_use}`" if value_song else f"Check album `{text_use}`",
            reply_markup=get_menu_song(value_search, 0)
            if value_song
            else get_menu_album(value_search, 0),
        )
