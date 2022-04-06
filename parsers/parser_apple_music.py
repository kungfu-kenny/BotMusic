# import time
import aiohttp
import asyncio
from pprint import pprint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from fake_useragent import UserAgent
from parsers.parse_webdriver import ParseWebDriver
# from parsers.parser_default_csv import ParserDefaultCSV
from config import LinkAppleMusic


class ParserAppleMusic:
    """
    class which is dedicated to produce values from the apple music
    and get parameters from the values
    """
    def __init__(self) -> None:
        self.work_options()
        self.chromedriver = ParseWebDriver().produce_webdriver_values()
        self.link_search_begin = '/'.join(
            [
                LinkAppleMusic.link_apple_music, 
                LinkAppleMusic.link_apple_music_us, 
                LinkAppleMusic.link_apple_music_search
            ]
        )
    
    def work_options(self) -> None:
        """
        Method which is dedicated to produce the values of the webdriver
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        self.options.add_argument(f"user-agent={UserAgent().random}")

    def get_link_values_album_search(self, value_artist:str, value_album:str, year:int, id:int) -> set:
        """
        Method which is dedicated to get links of searching
        Input:  value_artist = artist which is going to be searched
                value_album = album which is going to be searched
                year = year value for the selected album
                id = id value of the searched
        Output: set of the values with the link, value artist, value_album
        """
        value_search = LinkAppleMusic.link_apple_music_space.join(
            [
                self.get_value_translate(f)
                for f in
                [
                    value_artist,
                    value_album
                ]
            ]
        )
        return [
            f"{self.link_search_begin}{value_search}", 
            value_artist, 
            value_album, 
            year, 
            id
        ]

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
    
    @staticmethod
    def make_list_sublists(value_list:list, default_val:int=10) -> list:
        """
        Static method which is dedicated to produce values of the sublists of dafault_val size
        Input:  value_list = list of the values
                default_val = size of the lists
        Output: list of the sublists
        """
        def chunk(value_list:list, value_len:int):
            """
            Function for chunking values of the
            Input:  value_list = original list
                    value_len = length of the sublists
            Output: len on which to chunk values
            """
            for i in range(0, len(value_list), value_len):
                yield value_list[i:i + value_len]
        return list(chunk(value_list, default_val))

    async def make_html_links(self, value_list:list) -> list:
        """
        Async method which is dedicated to develop the dict values from the album 
        Input:  value_list = list value of the album
        Output: we developed 
        """
        self.driver.get(value_list[0])
        try:
            WebDriverWait(self.driver, LinkAppleMusic.apple_music_album_wait).until(
                EC.presence_of_element_located(
                        (
                        By.CLASS_NAME, 
                        'search__search-hits'
                        )
                    )
                )
        except TimeoutException:
            return [{
                "Year": value_list[3],
                "Link": value_list[0],
                "Album Name": value_list[2],
                "Artist": value_list[1],
                "ID": value_list[4]
            }]
        
        check = self.driver.find_elements_by_class_name("lockup__lines [href]")
        text = self.make_list_sublists([f.text for f in check], 2)
        links = self.make_list_sublists([f.get_attribute('href') for f in check], 2)
        
        return [
            {
                "Album Name Searched": names[1],
                "Artist Searched": names[0],
                "Album Link": links[1],
                "Artist Link": links[0],
                "Year": value_list[3],
                "Link": value_list[0],
                "Album Name": value_list[2],
                "Artist": value_list[1],
                "ID": value_list[4]
            }
            for names, links in zip(text, links)
            if len(names) == len(links) == 2
        ]

    @staticmethod
    def check_success(value_dict:dict) -> bool:
        """
        Method which is dedicated to develop the values of the created values
        Input:  value_dict = dictionary value which was succcessfully parsed from it
        Output: we developed the values 
        """
        value_list_similar = [f"{value_dict.get('Album Name', '')}{value_elem}".lower() 
            for value_elem in LinkAppleMusic.list_used_check]
        if value_dict.get('Artist', '').lower() != value_dict.get('Artist Searched', '').lower():
            return False
        value_list_similar.append(value_dict.get('Album Name', '').lower())
        value_album = value_dict.get('Album Name Searched', '').lower()
        for value_similar in value_list_similar:
            if value_album == value_similar:
                return True
        return False

    def produce_check_parsed(self, value_parsed:list) -> set:
        """
        Method which is dedicated to develop values of the giving
        Input:  value_parsed = list of the parsed dictionary to the given values
        Output: set of the matched, similar, possible and failed values
        """
        value_successful, value_possible, value_failed = [], [], []
        for value_got in value_parsed:
            if len(value_got) == 1 and len(value_got[0].keys()) == 4:
                value_failed.extend(value_got)
            else:
                for value_p in value_got:
                    if self.check_success(value_p):
                        value_successful.append(value_p)
                    else:
                        value_possible.append(value_p)
        return value_successful, value_possible, value_failed

    async def get_produce_apple_music_songs(self, session:object, link:str) -> str:
        """
        Async method which is dedicated to produce values
        Input:  session = object of the aiohttp
                link = link which is required to get values
        Output: we developed dictionary with developed values for the song 
        """
        if not link:
            return '', ''
        async with session.get(link) as r:
            if r.status == 200:
                return await r.text(), link
            return '', ''

    # async 
    def produce_basic_json_results_album(self, value_dict:dict, value_html:str, link:str) -> dict:
        """
        Async method which is dedicated to produce values of the getting values for the 
        Input:  value_dict = dictionary of the previously parsed values
                value_html = text values of the html
                link = link which was previously parsed
        Output: we developed values of the dictionary of the
        """
        if len(value_html) < 1000:
            print(value_html)
            print("EMPTY@@@@@")
            return value_dict
        soup = BeautifulSoup(value_html, 'html.parser')
        # soup_json = soup.find_all('meta')#, content="summary")
        soup_json = soup.find_all("script", type="application/ld+json")#attrs={'name':"schema"})#
        print(soup_json)
        print('ffffffffffffffffffffffffffffffffffffffffffffffffffff')
        

    async def make_html_links_song(self, session:object, links:list) -> list:
        """
        Method which is dedicated to make html values from the links
        Input:  session = session object which is from the aiohttp
                links = list with links for getting values
                value_multiple = boolean which signify the status of the sent links
        Output: we developed html for the links
        """
        tasks = [
            asyncio.create_task(
                self.get_produce_apple_music_songs(
                    session, 
                    link.get('Link')
                    )
                ) 
            for link in links]
        return await asyncio.gather(*tasks)

    async def get_produce_apple_music_search(self, value_artists:list, value_albums:list, value_year:list, value_id:list) -> dict:
        """
        Method which is dedicated to produce of searching from the apple music about albums
        Input:  value_artists = list of the artists which was searched
                value_albums = list of the albums which is searched
                value_year = list of the years of the seleted values
        Output: dictionary with fully parsed values for the further search
        """
        self.driver = webdriver.Chrome(self.chromedriver, options=self.options)
        links = [
            self.get_link_values_album_search(
                album, 
                artist, 
                year, 
                ids
            ) 
            for album, artist, year, ids in 
            zip(
                value_albums, 
                value_artists, 
                value_year, 
                value_id
            )
        ]
        print(links)
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        tasks = [asyncio.create_task(self.make_html_links(link)) for link in links]
        results_search = await asyncio.gather(*tasks)
        self.driver.close()
        self.driver.quit()
        pprint(results_search)
        print('???????????????????????????????????????????????????????????????')
        value_successful, value_possible, value_failed = self.produce_check_parsed(results_search)
        pprint(value_successful)
        print('dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        pprint(value_possible)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        pprint(value_failed)
        print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
        #TODO continue from here
        
        # semaphore = asyncio.Semaphore(LinkAppleMusic.apple_music_semaphore_threads)
        # async with semaphore:
        #     async with aiohttp.ClientSession(trust_env=True, connector=aiohttp.TCPConnector(force_close=True)) as session:
        #         value_return = await self.make_html_links_song(session, value_successful)
        #     # print(value_return[0])
        # print(len(value_return))
        # if not value_return:
        #     return [], [], [], []
        # self.produce_basic_json_results_album(value_successful[0], value_return[0][0], value_return[0][1])
        # tasks = [asyncio.create_task(self.produce_basic_json_results_album(value_html, link, album, artist, year)) 
        #         for value_html, (link, album, artist), year in zip(value_return, links, value_years)]
        # results = await asyncio.gather(*tasks)
        return [], [], [], []