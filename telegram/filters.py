from aiogram.dispatcher.filters import Filter
from aiogram.types import Message, CallbackQuery

from config import CALLBACKS


class CheckMessageFilter(Filter):
    key = "is_basic_filter"

    async def check(self, message: Message) -> bool:
        return True


class CheckMessageChangeSearch(Filter):
    key = "is_message_to_change_search"

    async def check(self, message: Message) -> bool:
        return True if message.text.strip() in [
            'Search only song',
            'Search only albums',
        ] else False


class CheckAlbumNextFilter(Filter):
    key = "is_album_next_filter"

    async def check(self, call: CallbackQuery) -> bool:
        data = call.data.split("_")
        if data[0] in [
            CALLBACKS["CALLBACK_ALBUM_MENU_PREV"],
            CALLBACKS["CALLBACK_ALBUM_MENU_NEXT"],
        ]:
            return True
        return False


class CheckSongNextFilter(Filter):
    key = "is_song_next_filter"

    async def check(self, call: CallbackQuery) -> bool:
        data = call.data.split("_")
        if data[0] in [
            CALLBACKS["CALLBACK_SONG_MENU_PREV"],
            CALLBACKS["CALLBACK_SONG_MENU_NEXT"],
        ]:
            return True
        return False


class CheckMessageSelectSongFilter(Filter):
    key = "song_download_filter"

    async def check(self, call: CallbackQuery) -> bool:
        data = call.data.split("_")
        if data[0] in [
            CALLBACKS["CALLBACK_SONG"],
        ]:
            return True
        return False


class CheckMessageSelectAlbumFilter(Filter):
    key = "album_download_filter"

    async def check(self, call: CallbackQuery) -> bool:
        data = call.data.split("_")
        if data[0] in [
            CALLBACKS["CALLBACK_ALBUM"],
        ]:
            return True
        return False
