import json
import aiohttp
import asyncio
import requests
from pprint import pprint
from bs4 import BeautifulSoup


class ParserGoogleSearch:
    """
    class which is dedicated to get values from the Google search
    """
    def __init__(self) -> None:
        pass

    # , value_artists, value_name, value_year
    def produce_manually_search_albums_google(self) -> list:
        """
        
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json'}
        link = 'https://music.youtube.com/search?q=testing%20asap%20rocky'
        k = requests.get(link, headers=headers).text
        soup = BeautifulSoup(k, 'html.parser')
        soup = soup.find_all("a")
        print(len(soup))
        # print(soup[2])
        print('111111111111111111111111111111111111111111111111111111111111111111111111111111')