import re
import json
from pprint import pprint
from scrapy import (
    Spider, 
    Request,
)
from bot_music.items import (
    SongItem,
    SongAlbumItem,
)


class DeezerListing(Spider):
    name = 'deezer_listing'

    def __init__(self, name="search_album", searches:list=[]):
        self._name = name
        self._urls = self._develop_urls(searches)

    @staticmethod
    def _develop_urls(searches:list) -> list:
        return [
            f"https://www.deezer.com/search/{i.lower()}"
            for i in searches
        ]

    def _develop_callback(self, search:str) -> object:
        match search:
            case("search_song"):
                return self.parse_song
            case("search_album"):
                return self.parse_album
            case("search_test"):
                return self.parse

    def start_requests(self):
        for url in self._urls:
            yield Request(
                url=url,
                method='GET',
                callback=self._develop_callback(self._name),
                headers=None, #TODO add later,
                cb_kwargs=None, #TODO add later
            )

    @staticmethod
    def _develop_json(html:str) -> dict:
        if (dct:=re.search(
            r'(?<=<script>window.__DZR_APP_STATE__ = ).*?(?=<\/script>)',
            html,
        )) and (dct:=dct.group()):
            return json.loads(dct)
        return {}

    def parse_album(self, response, training:bool=False):
        value_list = self._develop_json(response.text)
        for element in value_list.get('ALBUM', []).get('data', []):
            number_track = int(element.get('NUMBER_TRACK', '0'))
            album_id = element.get('ALB_ID', '0')
            album_title = element.get('ALB_TITLE', '')
            for art in element.get('ARTISTS', []):
                yield SongAlbumItem(
                    number_track = number_track,
                    album_id = album_id,
                    album_title = album_title,
                    artist_id = art.get('ART_ID', '0'),
                    artist_name = art.get('ART_NAME', ''),
                    training = training,
                )

    def parse_song(self, response, training:bool=False):
        value_list = self._develop_json(response.text)
        for element in value_list.get('TRACK', []).get('data', []):
            duration = element.get('DURATION', '0')
            album_id = element.get('ALB_ID', '0')
            album_title = element.get('ALB_TITLE', '')
            song_id = element.get("SNG_ID", 0)
            song_title = element.get('SNG_TITLE', '')
            for art in element.get('ARTISTS', []):
                yield SongItem(
                    duration = int(duration),
                    album_id = album_id,
                    album_title = album_title,
                    song_id = song_id,
                    song_title = song_title,
                    artist_id = art.get('ART_ID', '0'),
                    artist_name = art.get('ART_NAME', ''),
                    training = training,
                )


    def parse(self, response):

        #1. Parsing the songs to the files
        self.parse_song(response, True)

        #2. Parsing the albums to the files
        self.parse_album(response, True)