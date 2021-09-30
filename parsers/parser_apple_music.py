# import aiohttp
import asyncio
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from parsers.parse_webdriver import ParseWebDriver
from config import LinkAppleMusic


class ParserAppleMusic:
    """
    class which is dedicated to produce values from the apple music
    and get parameters from the values
    """
    def __init__(self) -> None:
        self.chromedriver = ParseWebDriver().produce_webdriver_values()
        self.link_search_begin = '/'.join([LinkAppleMusic.link_apple_music, 
                                        LinkAppleMusic.link_apple_music_us, 
                                        LinkAppleMusic.link_apple_music_search])
    
    def work_options(self) -> None:
        """
        Method which is dedicated to produce the values of the webdriver
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f"user-agent={UserAgent().random}")

    def get_link_values_album_search(self, value_artist:str, value_album:str) -> set:
        """
        Method which is dedicated to get links of searching
        Input:  value_artist = artist which is going to be searched
                value_album = album which is going to be searched
        Output: set of the values with the link, value artist, value_album
        """
        translated_album = self.get_value_translate(value_album)
        translated_artist = self.get_value_translate(value_artist)
        value_search = LinkAppleMusic.link_apple_music_space.join([translated_artist, translated_album])
        return f"{self.link_search_begin}{value_search}", value_artist, value_album

    @staticmethod
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
                value_str = value_str.replace(case, LinkAppleMusic.link_apple_music_space)
        return value_str.replace(' ', LinkAppleMusic.link_apple_music_space)

    async def get_html_value_analysis_album(self, value_html:str, value_link:str) -> str:
        """
        Method which is dedicated to get from html values to the list of the values for ge
        Input:  value_html = html of the parsed values
                value_link = value of selected link search
        Output: list of the values which were previously used for the values to it
        """
        if len(value_html) < 1000:
            return ''
        soup = BeautifulSoup(value_html, "html.parser")
        # print(soup)
        top_results = soup.find("div", {"class": "search-landing"})
        top_results = top_results.find_all("h2")#, {"class": "search__search-hits"})
        print(top_results)
        return 'che'


    async def parse_apple_manually_link(self, value_name_album:str) -> str:
        """
        Method which is dedicated to produce manuall search of the albums in caes that we are looking by album
        Input:  session = session object for the search
                value_name_album = album name which is going to be parsed
                value_check = value 
        Output: we successfully parsed all names which were used on the genius
        """
        # if value_name_album == 'Undefined':
        #     return value_name_album
        # async with session.get(value_name_album) as r:
        #     if r.status == 200:
        #         return await r.text()
        return value_name_album

    async def make_html_links(self, value_links:str) -> list:
        """
        Async method which is dedicated to asyncronously return 
        Input:  value_links = list with the links values of the values
        Output: list with the html values
        """
        tasks = [asyncio.create_task(self.parse_apple_manually_link(value_link))
                                        for value_link, *_ in value_links]
        return await asyncio.gather(*tasks)
        
    async def get_produce_apple_music_search(self, value_artists:list, value_albums:list, value_year:list) -> dict:
        """
        Method which is dedicated to produce of searching from the apple music about albums
        Input:  value_artists = list of the artists which was searched
                value_albums = list of the albums which is searched
                value_year = list of the years of the seleted values
        Output: dictionary with fully parsed values for the further search
        """
        self.work_options()
        self.driver = webdriver.Chrome(self.chromedriver, options=self.options)
        links = [self.get_link_values_album_search(album, artist) for album, artist in zip(value_albums, value_artists)]
        print(links)
        print('###########################################################')
        semaphore = asyncio.Semaphore(LinkAppleMusic.apple_music_semaphore_threads)
        async with semaphore:
            value_return = await self.make_html_links(links)
        # tasks = [asyncio.create_task(self.get_html_value_analysis_album(value_html, link)) for value_html, link in zip(value_return[:1], links[:1])]
        # results = await asyncio.gather(*tasks)
        
        #TODO think about next scripts !
        # k = requests.get("https://www.deezer.com/search/beatles%20Sgt.%20Pepper's%20Lonely%20Hearts%20Club%20Band/album").text
        # soup = BeautifulSoup(k, "html.parser")
        # print(soup)
        # check = soup.find(id="dzr-app")
        # check = soup.find("div", {"class":"hidden"})#id="naboo_content")# soup.find_all('link')#liYKde g 
        # import json
        # from parser_default_csv import ParserDefaultCSV
        # ParserDefaultCSV().get_values_json(script, 'two.json')
        # script = json.loads(check.find("script").text.split('window.__DZR_APP_STATE__ = ')[-1])
        # print(script)
        # return script

        #TODO get values of the links asyncronously
        #TODO get the html values
        #TODO write the values of getting values
        #TODO get the link and the parse all values from the link
        #TODO get dictionary values 
        self.driver.close()
        self.driver.quit()
        return [], [], [], []