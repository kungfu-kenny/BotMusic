import re
import json
from pprint import pprint
from scrapy import (
    Spider, 
    Request,
)


#TODO add here several names

class DeezerListing(Spider):
    """
    
    """
    name = 'deezer_listing'
    def __init__(self, name="search_test", search_type:str="track"):
        self._name = name
        self._urls = [
            "https://www.deezer.com/search/bones",
        ] #TODO change it later

    def _develop_() -> object:
        pass

    def start_requests(self):
        for url in self._urls:
            yield Request(
                url=url,
                method='GET',
                callback=self.parse,
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

    def parse_album(self, response, query):
        pass

    def parse_artist(self, response, query):
        pass

    def parse(self, response):
        if response.status == 200:
            dct = self._develop_json(response.text)
        elif response.status == 403:
            dct = self._develop_json('')
        print(dct.keys())
        # print(k:=dct.get("TRACK"))
        # print(k.keys())
        print(k:=dct.get("ALBUM"))