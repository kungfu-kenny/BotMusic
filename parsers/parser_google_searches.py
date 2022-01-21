import json
import aiohttp
import asyncio
import requests
from pprint import pprint
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class ParserGoogleSearch:
    """
    class which is dedicated to get values from the Google search
    """
    def __init__(self) -> None:
        pass

    @classmethod
    def develop_random_headers(cls) -> object:
        """
        Class method which is dedicated to get the random headers for it
        Input:  None
        Output: we developed values of the random headers
        """
        return {'user-agent': UserAgent().random,}

    @staticmethod
    def develop_link_google(value_name:str, value_album:str) -> str:
        """
        Static method which is dedicated to develop values of the link
        Input:  value_name = name required search
                value_album = name of album required search
        Output: we developed values of the google
        """
        value_search = ' '.join([value_name, value_album])#.lower()
        for replace, replaced in [(' ', '+'), 
                                ('$', '%24')]:
            value_search = value_search.replace(replace, replaced)
        return ''.join(['https://www.google.com/search?',
                        'channel=fs&client=ubuntu&',
                        f'q={value_search}'])

    def produce_manual_search_link_google(self) -> str:
        """
        Method which is dedicated to develop values of the link to the youtube album link
        Input:  previously developed values of the name and link
        Output: we developed values of the string to it
        """
        pass

    def produce_manually_search_albums_google(self, albums:list, artists:list, years:list) -> list:
        """
        Method which is dedicated to produce firstly some testings
        Input:  albums = list with the selected 
        Output: we developed list values
        """
        link = self.develop_link_google(artists[0], albums[0])
        # link = 'https://music.youtube.com/search?q=testing%20asap%20rocky'
        k = requests.get(link, headers=self.develop_random_headers()).text
        soup = BeautifulSoup(k, 'html.parser')
        soup = soup.find("div", {"id": "main"})
        soup_a = soup.find_all('a')
        