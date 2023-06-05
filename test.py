from scrapers.get_controller import (
    get_file_song_server,
    get_file_album_server,
)



if __name__ == "__main__":
    # https://www.deezer.com/us/album/44267881
    a = get_file_album_server(44267881)