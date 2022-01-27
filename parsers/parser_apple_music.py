import time
import asyncio
from pprint import pprint
from unittest import result
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
        self.chromedriver = ParseWebDriver().produce_webdriver_values()
        self.link_search_begin = '/'.join([
            LinkAppleMusic.link_apple_music, 
            LinkAppleMusic.link_apple_music_us, 
            LinkAppleMusic.link_apple_music_search
        ])
    
    def work_options(self) -> None:
        """
        Method which is dedicated to produce the values of the webdriver
        """
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
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
                "Artist": value_list[1]
            }]
        
        check = self.driver.find_elements_by_class_name("lockup__lines [href]")
        text = self.make_list_sublists([f.text for f in check], 2)
        links = self.make_list_sublists([f.get_attribute('href') for f in check], 2)
        
        return [
            {
                "Album Name Searched": names[0],
                "Artist Searched": names[1],
                "Album Link": links[1],
                "Artist Link": links[0],
                "Year": value_list[3],
                "Link": value_list[0],
                "Album Name": value_list[2],
                "Artist": value_list[1]
            }
            for names, links in zip(text, links)
            if len(names) == len(links) == 2
        ]

    #TODO complete this function
    def check_success(self, value_dict:dict) -> bool:
        """
        Method which is dedicated to develop the values of the created values
        Input:  value_dict = dictionary value which was succcessfully parsed from it
        Output: we developed the values 
        """
        value_list_similar = []
        # for similar in 
        return False

    def produce_values_checked_values(self, value_parsed:list) -> set:
        """
        Method which is dedicated to develop values of the giving
        Input:  value_parsed = list of the parsed dictionary to the given values
        Output: set of the matched, similar, possible and failed values
        """
        value_successful, value_possible, value_failed = [], [], []
        for value_got in value_parsed:
            #TODO check the failed values
            if len(value_got) == 1 and len(value_got[0].keys()) == 4:
                value_failed.extend(value_got)
            else:
                for value_parsed in value_got:
                    if self.check_success():
                        value_successful.append(value_parsed)
                    else:
                        value_possible.append(value_parsed)
        return value_successful, value_possible, value_failed

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
        for link, year in zip(links, value_year):
            link.append(year)
        tasks = [asyncio.create_task(self.make_html_links(link)) for link in links]
        results_search = await asyncio.gather(*tasks)
        pprint(results_search[0])
        self.driver.close()
        self.driver.quit()
        return [], [], [], []