import os
import aiohttp
import requests
from config import LinkYandex


class ParserYandexMusic:
    """
    class which is dedicated to parse yandex music search for tehreturnal
    """

    def __init__(self) -> None:
        self.link_search_begin = '/'.join([LinkYandex.link_yandex, LinkYandex.link_yandex_search])

    async def produce_links(self, value_artist:str, value_album:str) -> set:
        """
        Method which is dedicated to produce links for the album
        Input:  value_album = name of the album
                value_artist = name of the artist name
        Output: link which is dedicated to parse values
        """
        value_album_new = await self.produce_manual_link_results(value_album.lower())
        value_artist_new = await self.produce_manual_link_results(value_artist.lower())
        value_search = LinkYandex.link_yandex_space.join([value_artist_new, value_album_new])
        return f"{self.link_search_begin}{value_search}&type=albums", value_artist, value_album

    @staticmethod
    async def produce_manual_link_results(value_string:str) -> str:
        """
        Static method which is dedicated to produce values from the results
        Input:  value_string = value string which needs to be transformed
        Output: string with inputed values
        """
        for value_replaced, value_replace in [('@', LinkYandex.link_yandex_a),
                                            (' ', LinkYandex.link_yandex_space),
                                            ('$', LinkYandex.link_yandex_dollar),
                                            (':', LinkYandex.link_yandex_doublecom)]:
            value_string = value_string.replace(value_replaced, value_replace)
        return value_string

    async def produce_list_selected_links(self, value_artists:list, value_albums:list) -> list:
        """
        Method which is dedicated to produce selected links for the searches
        Input:  value_artists = list of the artists which is searched
                value_albums = list of the albums which were developed
        Output: we developed values of the links for it
        """
        #TODO work here on this values 
        pass

    def produce_manual_search(self, value_artists:list, value_albums:list, value_years:list) -> set:
        """
        Method which is dedicated to produce manual search of the 
        Input:  value_album = list with the albums which were used
                value_artist = list with artists which those album wrote
                value_year = list with years of selected values
        Output: set of selected values of the search within 
        """
        #TODO work here on this values
        print(self.link_search_begin)
        # value_links = await
