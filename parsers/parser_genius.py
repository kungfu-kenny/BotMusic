import os
import re
import aiohttp
import asyncio
from config import (link_genius,
                    link_genius_albums)


class ParserGenius:
    """
    class which is dedicated to produce basic parsings of the info about songs
    """
    def __init__(self) -> None:
        self.link_genius_albums = '/'.join([link_genius, link_genius_albums])

    #TODO rework this in cases of asyncio
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

    