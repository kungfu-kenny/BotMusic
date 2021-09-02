import os
import re
import aiohttp
import asyncio
# import requests
from bs4 import BeautifulSoup
from config import (link_genius,
                    link_genius_albums,
                    link_genius_search_begin,
                    link_genius_search_end,
                    genius_semaphore_threads)


class ParserGenius:
    """
    class which is dedicated to produce basic parsings of the info about songs
    """
    def __init__(self) -> None:
        self.link_genius_albums = '/'.join([link_genius, link_genius_albums])

    @staticmethod
    def combine_link_values(value_link:str, value_artist:str, value_album:str) -> str:
        """
        Static method which is dedicated to produce values of the link
        Input:  value_link = link previously crafted
                value_artist = artist of the value
                value_album = album to search
        Output: link values of the search
        """
        return '/'.join([value_link, value_artist, value_album])

    #TODO rework this in cases of asyncio
    @staticmethod
    def get_values_link_genius(value_inserted:str) -> str:
        """
        Static method which is dedicated 
        Input:  value_inserted = string value which is required to be transformed
        Output: value which would be raedy to search
        """
        value_inserted = value_inserted.strip()
        value_inserted = list(value_inserted)
        for letter in value_inserted:
            if letter in ['?', '(', ')', '"', '!', "'", '`', '+', '.', '_', '&']:
                value_inserted.remove(letter)
        value_inserted = ''.join(value_inserted)
        value_inserted = '-'.join(value_inserted.split(' ')).lower().capitalize()
        for letter in [':', '$', '’','/']:
            if letter in value_inserted:
                value_inserted = value_inserted.replace(letter, '-')
        value_inserted = list(value_inserted)
        for i in range(0, len(value_inserted)):
            if value_inserted[i] == '-' and i < len(value_inserted)-1 and value_inserted[i+1] =='-':
                value_inserted.remove(i)
        for i in [0, -1]:
            if value_inserted[i] == '-':
                value_inserted.pop(i)
        return ''.join(value_inserted)

    #TODO rework this in cases of asyncio
    def produce_links_parse_albums(self, list_artists:list, list_albums:list) -> list:
        """
        Method which is dedicated to produce the links for the parsing of the values
        Input:  list_artists = list with the artists which is required to search theirs album
                list_albums = list with the albums which it would parse to all of this
        Output: list with the links which would be further used for getting parsed
        """
        list_links = []
        for artist, album in zip(list_artists, list_albums):
            new_artist = asyncio.create_task(self.get_values_link_genius(artist))
            new_album = asyncio.create_task(self.get_values_link_genius(album))
            list_links.append(self.combine_link_values(self.link_genius_albums, new_artist, new_album))
        return list_links

    def parse_genius_manually_album_link(self, value_link_album:str) -> dict:
        """
        Method which is dedicated to produce values of the links
        Input:  value_link_album = value foe the link of this album
        Output: we successfully created dictionary with the links of the 
        """
        pass

    @staticmethod
    def produce_genius_manually_link(value_search:str) -> set:
        """
        Static method which is dedicated to produce link for it
        Input:  value_search = value which is searched by us
        Output: we created link values for further parsing
        """
        return ''.join([link_genius, link_genius_search_begin, value_search, link_genius_search_end])

    @staticmethod
    async def produce_genius_above(value_link:str) -> str:
        """
        Async method which is dedicated to return name from the link
        Input:  value_link = link which was from the search
        Output: string values which is dedicated 
        """
        return await value_link.split(link_genius)[0] \
                                .split(link_genius_search_begin)[0] \
                                .split(link_genius_search_end)[0]

    async def parse_genius_manually_link(self, session:object, value_name_album:str) -> str:
        """
        Method which is dedicated to produce manuall search of the albums in caes that we are looking by album
        Input:  value_name_album = album name which is going to be parsed
        Output: we successfully parsed all names which were used on the genius
        """
        async with session.get(value_name_album) as r:
            if r.status == 200:
                return await r.text()
            return await self.produce_genius_above(value_name_album)
    
    async def make_html_links(self, session, value_album_list:list) -> list:
        """
        Asyncio values of the generating html from the links
        Input:  session = session of the aoihttp
                value_album_list = list values to parse
        Output: list values to work with further parsing
        """
        tasks = [asyncio.create_task(self.parse_genius_manually_link(session, value_album_link))
                                                        for value_album_link in value_album_list]
        results = await asyncio.gather(*tasks)
        return results

    async def parse_genius_manually_album_list(self, value_album_list:list) -> list:
        """
        Async method which is dedicated to produce different genius values
        Input:  value_album_list = list of the link which is required to be searched
        Output: list with parsed html values
        """
        links = [self.produce_genius_manually_link(f) for f in value_album_list]
        semaphore = asyncio.Semaphore(genius_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env = True) as session:
                value_return = await self.make_html_links(session, links)
        return value_return

    #TODO work here!
    async def parse_genius_automatic_album_list(self, value_album_list:list) -> list:
        """
        Async method which is dedicated to make automatic album list for further parsing
        Input:  value_album_list = list with the values of the album
        Output: we successfully created values from the parsing
        """
        pass