from pprint import pprint
from scrapers.get_values_deezer import (
    parse_album_songs,
    parse_search_results,
)
from scrapers.get_values_youtube import (
    produce_file_download_internet,
)
from scrapers.get_values_youtube_listing import (
    _produce_duration_inverse,
    get_links_search,
    get_links_filtered,
)
from config import (
    CALLBACK_SONG,
    CALLBACK_ALBUM,
)


def get_list_selection(
    value_string_telegram:str,
    value_search_song:bool=True,
):
    value_return_telegram = {}
    for i, element in enumerate(
        parse_search_results(
            value_string_telegram,
            value_search_song
        )
    ):
        #TODO produce values to insert to list
        # print(element)
        # print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        # print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        value_return_telegram.update(
            {
                f"{CALLBACK_SONG}_{element.get('song_id')}_{element.get('duration')}": {
                    "index": i + 1,
                    "name": f"{element.get('artist_name')} - {element.get('song_title')}",
                    "duration": _produce_duration_inverse(element.get("duration")),
                }
            }
        )
    return value_return_telegram

def get_file_song_server(song_id:int) -> dict:
    value_use = [] #TODO test data

def get_file_album_server(album_id:int, sender:int='test') -> dict:
    value_result = {}
    for index, i in enumerate(
        parse_album_songs(album_id)
    ):
        track_youtube = get_links_filtered(
            get_links_search(
                track_name:=f"{i.get('artist_name')} - {i.get('song_title')}"
            ),
            track_name,
            i.get("duration"),
        )
        track_youtube_downloaded = produce_file_download_internet(
            track_youtube.get("url"),
            sender,
            index,
        )
        if not len(track_youtube_downloaded.keys()) == 1:
            raise 
        track_name_uuid = list(track_youtube_downloaded.keys())[0]
        track_youtube_downloaded[track_name_uuid].update(track_youtube)
        value_result.update(track_youtube_downloaded)
    
    pprint(value_result)

if __name__ == "__main__":
    # dict_return_telegram = get_list_selection(
    #     'killer mike',
    #     True
    # )
    # server_sent = get_file_album_server('64182182')
    # server_sent = get_file_album_server('277494962')
    # server_sent = get_file_album_server('382760377')
    server_sent = get_file_album_server('286758')