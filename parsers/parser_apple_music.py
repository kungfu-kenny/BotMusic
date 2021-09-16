import os
import aiohttp
import asyncio
from pprint import pprint
from bs4 import BeautifulSoup
from config import (link_apple_music,
                    link_apple_music_us,
                    link_apple_music_space,
                    link_apple_music_search,
                    apple_music_semaphore_threads)

class ParserAppleMusic:
    """
    class which is dedicated to produce values from the apple music
    and get parameters from the values
    """
    def __init__(self) -> None:
        self.link_search_begin = '/'.path.join([link_apple_music, link_apple_music_us, link_apple_music_search])
        
    def get_link_values_album_search(self, value_artist:str, value_album:str) -> set:
        """
        Method which is dedicated to get links of searching
        Input:  value_artist = artist which is going to be searched
                value_album = album which is going to be searched
        Output: set of the values with the link, value artist, value_album
        """
        translated_album = self.get_value_translate(value_album)
        translated_artist = self.get_value_translate(value_artist)
        value_search = link_apple_music_space.join([translated_artist, translated_album])
        return f"{self.link_search_begin}{value_search}", value_artist, value_album

    def get_value_translate(value_str:str) -> str:
        """
        Static method which is dedicated to transpose values from the
        Input:  value_str = string of album/artist to get values
        Output: string value to work as link after
        """
        value_str = value_str.strip()
        value_str = value_str.lower()
        for case in ['$']:
            if case in value_str:
                value_str = value_str.replace(case, link_apple_music_space)
        return value_str.replace(' ', link_apple_music_space)

    def get_html_value_analysis_album(self, value_html:str) -> list:
        """
        Method which is dedicated to get from html values to the list of the values for ge
        Input:  value_html = html of the parsed values
        Output: list of the values which were previously used for the values to it
        """
        pass

    def get_produce_apple_music_search(self, value_artists:list, value_albums:list, value_year:list) -> dict:
        """
        Method which is dedicated to produce of searching from the apple music about albums
        Input:  value_artists = list of the artists which was searched
                value_albums = list of the albums which is searched
                value_year = list of the years of the seleted values
        Output: dictionary with fully parsed values for the further search
        """
        #TODO get values of the links asyncronously
        #TODO get the html values
        #TODO write the values of getting values
        #TODO get the link and the parse all values from the link
        #TODO get dictionary values 
        pass