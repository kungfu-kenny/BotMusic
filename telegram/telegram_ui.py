from aiogram.types import Message, CallbackQuery

from telegram.telegram_usage import dp, bot
from scrapers.get_controller import get_list_selection
from telegram.filters import (
    CheckMessageSelectSongFilter,
    CheckMessageSelectAlbumFilter,
    CheckSongNextFilter,
    CheckAlbumNextFilter,
)
from scrapers.get_controller import (
    parse_album_songs,
    get_file_song_server,
    get_file_album_server,
)
from utilities.utilities_file import _get_music_file
from utilities.utilities_ui import (
    get_menu_song,
    get_menu_album,
    _get_reply_keyboard_basic,
)


@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    """
    """
    await message.reply(
        "Hi!\nI'm EchoBot!\nPowered by aiogram.",
        reply_markup=_get_reply_keyboard_basic(),
    )


@dp.message_handler(commands=['album'])
async def send_album(message: Message):
    """
    Function to get the selected albums to the 
    """
    if (
        message.text and message.text.startswith("/album")
        and len(message.text) > 7
    ):
        text_use = message.text[7:]
        value_tst = get_list_selection(text_use, False)
        #TODO add to the database
        await message.reply(
            f"Check album `{text_use}`",
            reply_markup = get_menu_album(value_tst, 0),
        )


@dp.message_handler(commands=['song'])
async def send_song(message: Message):
    """
    """
    if (
        message.text and message.text.startswith("/song")
        and len(message.text) > 6
    ):
        text_use = message.text[6:]
        value_search = get_list_selection(text_use)
        #TODO add here the database
        await message.reply(
            f"Check song `{text_use}`",
            reply_markup= get_menu_song(value_search, 0)
        )


@dp.message_handler(commands=['settings'])
async def send_settings(message: Message):
    """
    """
    await message.reply(
        "Used "
    )


@dp.message_handler(commands=['help'])
async def send_help(message: Message):
    """
    """
    await message.reply(
        "Hi!\nI'm EchoBot!\nPowered by aiogram."
    )


@dp.callback_query_handler(CheckAlbumNextFilter())
async def update_reply_markup_album_next(call:CallbackQuery) -> None:
    value_index = int(call.data.split('_')[-1])
    text_use = call.message.text.replace('Check album `', '')[:-1]
    value_search = get_list_selection(text_use, False)
    #TODO add here the database
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_menu_album(value_search, value_index),
    )


@dp.callback_query_handler(CheckSongNextFilter())
async def update_reply_markup_song_next(call:CallbackQuery) -> None:
    value_index = int(call.data.split('_')[-1])
    text_use = call.message.text.replace('Check song `', '')[:-1]
    value_search = get_list_selection(text_use)
    #TODO add here the database
    await bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=get_menu_song(value_search, value_index),
    )

@dp.callback_query_handler(CheckMessageSelectSongFilter())
async def send_song_value(call:CallbackQuery) -> None:
    print(call.data)
    print('555555555555555555555555555555555555555555555555')
    value_index = call.data.split('_')[-1]
    song_value = get_file_song_server(value_index)
    print(song_value)
    print('66666666666666666666666666666666666666666666666666666666')


@dp.callback_query_handler(CheckMessageSelectAlbumFilter())
async def send_album_value(call: CallbackQuery) -> None:
    print(call.data)
    print('555555555555555555555555555555555555555555555555')
    print(call.message.chat.id)
    print('66666666666666666666666666666666666666666666666666')
    value_id = call.data.split('_')[-1]
    await bot.send_message(
        call.message.chat.id,
        f"Your album: \nhttps://www.deezer.com/us/album/{value_id}"
    )
    value_dict_songs = get_file_album_server(value_id, call.message.chat.id)

    for file_name_ext, file_value_dict in value_dict_songs.items():
        title = file_value_dict['title'] \
            if not file_value_dict.get('name_searched') else file_value_dict['name_searched']
        with open(_get_music_file(file_name_ext), "rb") as music_file:
            await bot.send_audio(
                file_value_dict['sender'],
                audio=music_file,
                title=title,
            )
        #TODO remove values
    for file_name_ext in value_dict_songs.keys():
        _get_music_file(file_name_ext, False)
