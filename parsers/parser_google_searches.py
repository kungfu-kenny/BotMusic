import json
import asyncio
from urllib import parse
from pprint import pprint
from selenium import webdriver
from parsers.parse_webdriver import ParseWebDriver
from config import LinkGoogle


class ParserGoogleSearch:
    """
    class which is dedicated to get values from the Google search
    """
    def __init__(self) -> None:
        self.webdriver = ParseWebDriver()
        self.chrome_options = self.get_chrome_options()

    @staticmethod
    def develop_link_google(value_name:str, value_album:str) -> str:
        """
        Static method which is dedicated to develop values of the link
        Input:  value_name = name required search
                value_album = name of album required search
        Output: we developed values of the google
        """
        value_search = ' '.join([value_name, value_album]).lower()
        for replace, replaced in [['@', LinkGoogle.link_google_a],
                                [' ', LinkGoogle.link_google_space],
                                ['$', LinkGoogle.link_google_dollar],
                                [':', LinkGoogle.link_google_doublecom]]:
            value_search = value_search.replace(replace, replaced)
        return ''.join(['https://www.google.com/search?',
                        'channel=fs&client=ubuntu&',
                        f'q={value_search}'])

    @staticmethod
    def get_chrome_options():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        return chrome_options

    async def produce_manual_search_link_google(self, link:str) -> dict:
        """
        Method which is dedicated to develop values of the link to the youtube album link
        Input:  link = value of the link which was created 
        Output: we developed values of the string to it
        """
        value_get = {}

        self.driver.get(link)
        check = self.driver.find_elements_by_css_selector(".ellip [href]")
        text = [f.text for f in check]
        links = [f.get_attribute('href') for f in check]
        if LinkGoogle.google_search_deezer in text:
            value_get[LinkGoogle.google_search_deezer] = \
                links[text.index(LinkGoogle.google_search_deezer)]
        if LinkGoogle.google_search_youtube_music in text:
            value_link = links[text.index(LinkGoogle.google_search_youtube_music)]
            
            value_get[LinkGoogle.google_search_youtube_music] = value_link
            value_parse = parse.urlsplit(value_link)
            value_parse_dict = dict(parse.parse_qsl(parse.urlsplit(value_link).query))
            value_parse_dict.pop('feature')
            value_list = '&'.join(f"{k}={v}" for k, v in value_parse_dict.items())
            value_link_new = f"{value_parse.scheme}://youtube.com{value_parse.path}"
            if value_list:
                value_link_new = '?'.join([value_link_new, value_list])
        
            value_get[LinkGoogle.google_search_youtube] = value_link_new
        return value_get
    
    async def produce_manually_search_albums_google(self, ids:list, albums:list, artists:list, years:list) -> set:
        """
        Method which is dedicated to produce results from the google search
        Input:  ids = list with the selected id
                albums = list with the selected
                artists = list with selected artists
                years = list with selected years
        Output: we developed list values
        """
        self.webdriver.produce_webdriver_values()
        self.driver = webdriver.Chrome(
            executable_path=self.webdriver.path_webdriver_direct, 
            chrome_options=self.chrome_options
            )
        semaphore = asyncio.Semaphore(LinkGoogle.google_semaphore_threads)
        async with semaphore:
            links = [
                self.develop_link_google(
                    artist, 
                    album
                ) 
                for artist, album in zip(artists, albums)]
            value_get = [
                await self.produce_manual_search_link_google(link) for link in links]
        value_present, value_empty = [], []
        for id, dct, link, album, artist, year in zip(ids, value_get, links, albums, artists, years):
            if not dct:
                dct.update({
                    "Album_ID": id,
                    "Link": link,
                    "Album_Name": album,
                    "Artist": artist,
                    "Year": year})
                value_empty.append(dct)
            else:
                dct.update({
                    "Album_ID": id,
                    "Link": link,
                    "Album_Name": album,
                    "Artist": artist,
                    "Year": year})
                value_present.append(dct)

        self.driver.close()
        self.driver.quit()
        return value_present, value_empty