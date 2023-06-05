import re
import json
import requests
from pprint import pprint


def _develop_urls(searches:list, link_type:str='search') -> str:
    match link_type:
        case('search'):
            return f"https://www.deezer.com/search/{searches.lower()}"
        case("search_album"):
            return f"https://www.deezer.com/us/album/{searches}"

def _develop_json(html:str, data_type:str) -> dict:
    if (dct:=re.search(
        r'(?<=<script>window.__DZR_APP_STATE__ = ).*?(?=<\/script>)',
        html,
    )) and (dct:=dct.group()):
        return json.loads(dct).get(data_type, {}).get('data', [])
    return {}

def parse_album_songs(album_id:str) -> list:
    url = _develop_urls(album_id, 'search_album')
    response = requests.get(url)
    songs = []
    value_list = _develop_json(response.text, "SONGS")
    for element in value_list:#.get('SONGS', {}).get('data', []):
        # pprint(element)
        # print()
        # print()
        duration = element.get('DURATION', '0')
        number_track = int(element.get('TRACK_NUMBER', '0'))
        album_id = element.get('ALB_ID', '0')
        album_title = element.get('ALB_TITLE', '')
        song_id = element.get("SNG_ID", 0)
        song_title = element.get('SNG_TITLE', '')
        for art in element.get('ARTISTS', []):
            if song_id in songs:
                continue
            else: 
                songs.append(song_id)
            yield {
                "number_track": number_track,
                "duration": int(duration),
                "album_id": album_id,
                "album_title": album_title,
                "song_id": song_id,
                "song_title": song_title,
                "artist_id": art.get('ART_ID', '0'),
                "artist_name": art.get('ART_NAME', ''),
            }
    
def parse_album(response) -> object:
    albums = []
    value_list = _develop_json(response.text, 'ALBUM')
    for element in value_list:
        number_track = int(element.get('NUMBER_TRACK', '0'))
        album_id = element.get('ALB_ID', '0')
        album_title = element.get('ALB_TITLE', '')
        for art in element.get('ARTISTS', []):
            if album_id in albums:
                continue
            else:
                albums.append(album_id)
            yield {
                "number_track": number_track,
                "album_id": album_id,
                "album_title": album_title,
                "artist_id": art.get('ART_ID', '0'),
                "artist_name": art.get('ART_NAME', ''),
            }

def parse_song(response) -> dict:
    songs = []
    value_list = _develop_json(response.text, 'TRACK')
    for element in value_list:
        duration = element.get('DURATION', '0')
        album_id = element.get('ALB_ID', '0')
        album_title = element.get('ALB_TITLE', '')
        song_id = element.get("SNG_ID", 0)
        song_title = element.get('SNG_TITLE', '')
        for art in element.get('ARTISTS', []):
            if song_id in songs:
                continue
            else: 
                songs.append(song_id)
            yield {
                "duration": int(duration),
                "album_id": album_id,
                "album_title": album_title,
                "song_id": song_id,
                "song_title": song_title,
                "artist_id": art.get('ART_ID', '0'),
                "artist_name": art.get('ART_NAME', ''),
            }

def parse_search_results(search:str, parse_song_bool:bool=True):
    url = _develop_urls(search)
    response = requests.get(url)
    if parse_song_bool:
        return parse_song(response)
    return parse_album(response)


if __name__ == "__main__":
    a = parse_search_results('asap rocky')
    # a = parse_album_songs('382760377')
    pprint(list(a))
    # "https://www.deezer.com/us/album/382760377"