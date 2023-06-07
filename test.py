from scrapers.get_controller import (
    parse_album_songs,
    get_file_song_server,
    get_file_album_server,
)
from pprint import pprint


if __name__ == "__main__":
    # a = parse_album_songs(44267881)
    # pprint(list(a))
    # https://www.deezer.com/us/album/44267881
    a = get_file_album_server('83821012')
    pprint(a)