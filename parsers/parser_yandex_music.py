import os
import json
import asyncio
from pprint import pprint
from time import perf_counter
import aiohttp
import requests
from bs4 import BeautifulSoup
from config import LinkYandex


class ParserYandexMusic:
    """
    class which is dedicated to parse yandex music search for tehreturnal
    """

    def __init__(self) -> None:
        self.link_search_begin = '/'.join([LinkYandex.link_yandex, LinkYandex.link_yandex_search])

    def produce_refresh_values(self, value_list:list) -> set:
        """
        Method which is dedicated to produce refreshing values of the
        Input:  value_list = list of the parsed searches of the 
        Output: set with the values of the refreshings
        """
        #TODO get values of the successfull
        #TODO get values of the successfull all
        #TODO get values of the possible
        #TODO get values of the failed
        pass

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
        return f"{self.link_search_begin}text={value_search}&type=albums", value_artist, value_album

    @staticmethod
    async def produce_manual_link_results(value_string:str) -> str:
        """
        Static method which is dedicated to produce values from the results
        Input:  value_string = value string which needs to be transformed
        Output: string with inputed values
        """
        for value_replaced, value_replace in [['@', LinkYandex.link_yandex_a],
                                            [' ', LinkYandex.link_yandex_space],
                                            ['$', LinkYandex.link_yandex_dollar],
                                            [':', LinkYandex.link_yandex_doublecom]]:
            value_string = value_string.replace(value_replaced, value_replace)
        return value_string

    async def produce_list_selected_links(self, value_artists:list, value_albums:list) -> list:
        """
        Method which is dedicated to produce selected links for the searches
        Input:  value_artists = list of the artists which is searched
                value_albums = list of the albums which were developed
        Output: we developed values of the links for it
        """
        tasks = [asyncio.create_task(self.produce_links(artist, album)) for artist, album in zip(value_artists, value_albums)]
        return await asyncio.gather(*tasks)

    async def parse_yandex_manually_link(self, session:object, value_name_album:str) -> str:
        """
        Method which is dedicated to produce manual search of the albums in cases that we are looking by album
        Input:  session = session object for the search
                value_name_album = album name which is going to be parsed
        Output: we successfully parsed all names which were used on the genius
        """
        if value_name_album == 'Undefined':
            return value_name_album
        async with session.get(value_name_album) as r:
            if r.status == 200:
                return await r.text()
            return value_name_album

    async def make_html_links(self, session:object, links:list, value_multiple:bool=False) -> list:
        """
        Method which is dedicated to make html values from the links
        Input:  session = session object which is from the aiohttp
                links = list with links for getting values
                value_multiple = boolean which signify the status of the sent links
        Output: we developed html for the links
        """
        if not value_multiple:
            tasks = [asyncio.create_task(self.parse_yandex_manually_link(session, link)) for link, *_ in links]
        else:
            tasks = [asyncio.create_task(self.parse_yandex_manually_link(session, link)) for link in links]
        return await asyncio.gather(*tasks)

    @staticmethod
    async def produce_album_song_info(value_html:str) -> dict:
        """
        Method which is dedicated to return info values for the 
        Input:  value_html = html values of the search
        Output: dictionary which is required to get values
        """
        value_dict = {}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, "html.parser")
        soup = soup.find('script', class_="light-data").text
        try:
            soup = json.loads(soup)
        except Exception as e:
            print(e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            soup = {}
        


    @staticmethod
    async def produce_basic_json_results_album(value_html:str, link:str, album:str, artist:str, year:str) -> list:
        """
        Method which is dedicated to produce basic json from the album html search
        Input:  value_html = html string of the beaytiful soup which was developed
                link = link of the search
                album = album of the search
                artist = artist of the album
                year = year of the release
        Output: We developed list of dictionaries of the search 
        """
        value_list = []
        if len(value_html) < 1000:
            return value_list
        soup = BeautifulSoup(value_html, "html.parser")
        soup = soup.find(class_="theme-white")
        soup = soup.find("script").text[7:-1]
        try:
            soup = json.loads(soup)
        except Exception as e:
            soup = {}
            print(e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        page_data = soup.get('pageData', {})
        page_data = page_data.get('result', {})
        page_data = page_data.get('albums', {})
        page_data_alb = page_data.get('items', [])
        
        value_albums = [{
            "Album ID": value_album.get("id"),
            "Album Link Search": link,
            "Album Link": '/'.join([LinkYandex.link_yandex, 
                                    LinkYandex.link_yandex_album, 
                                    str(value_album.get("id"))]) 
                                    if value_album.get("id") else '',
            "Year Searched": year,
            "Album Searched": album, 
            "Year": value_album.get("year"),
            "Year Present": value_album.get('year') == year,
            "Original Release Year": value_album.get("originalReleaseYear"),
            "Album Present": value_album.get('title', '').lower() == album.lower(),
            "Track Number": value_album.get("trackCount", 0),
            "Content Warning": value_album.get("contentWarning", ""),
            "Version": value_album.get("version", ""),
            "Genre": value_album.get("genre", ""),
            "Album Cover": value_album.get("coverUri", ""),
            "Title": value_album.get("title", ''),
            "Labels": value_album.get("labels", []),
            "artists": value_album.get("artists", [])
        }
        for value_album in page_data_alb]
        
        value_artists = [f.pop("artists", []) for f in value_albums]
        value_artists = [{
            "Artist Searched": artist,
            "Artist ID": [f.get('id', 0) for f in value_artist],
            "Artist Name": [f.get('name', '') for f in value_artist],
            "Artist Present": any(f.get('name', '').lower() == artist.lower() for f in value_artist),
            "Artist Cover": [f.get('cover', {}).get('uri', '') for f in value_artist],
            "Artist Composer Boolean": [f.get("composer", False) for f in value_artist],
        } for value_artist in value_artists]

        [album.update(artist) for album, artist in zip(value_albums, value_artists)]
        return value_albums

    async def produce_manual_albums_search_yandex(self, value_artists:list, value_albums:list, value_years:list) -> set:
        """
        Method which is dedicated to produce manual search of the 
        Input:  value_album = list with the albums which were used
                value_artist = list with artists which those album wrote
                value_year = list with years of selected values
        Output: set of selected values of the search within 
        """
        links = await self.produce_list_selected_links(value_artists, value_albums)
        print(links)
        print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
        semaphore = asyncio.Semaphore(LinkYandex.yandex_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links)
        tasks = [asyncio.create_task(self.produce_basic_json_results_album(value_html, link, album, artist, year)) 
                for value_html, (link, album, artist), year in zip(value_return[:1], links[:1], value_years[:1])] 
                # for value_html, (link,{} album, artist), year in zip(value_return, links, value_years)]
        results = await asyncio.gather(*tasks)
        pprint(results)


        # k = requests.get('https://music.yandex.ru/album/3277242').text
        # await self.produce_album_song_info(k)