import os
import ast
import re
import json
import aiohttp
import asyncio
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from config import (link_deezer, 
                    link_deezer_us,
                    link_deezer_album,
                    link_deezer_space,
                    link_deezer_dollar,
                    link_deezer_search,
                    deezer_semaphore_threads)


class ParserDeezer:
    """
    class which is dedicated to return values from the Deezer website information about the music
    """
    def __init__(self):
        self.link_search_begin = '/'.join([link_deezer, link_deezer_search])

    async def get_link_values_album_search(self, value_artist:str, value_album:str) -> set:
        """
        Method which is dedicated to get links of searching
        Input:  value_artist = artist which is going to be searched
                value_album = album which is going to be searched
        Output: set of the values with the link, value artist, value_album
        """
        translated_album = await self.get_value_translate(value_album)
        translated_artist = await self.get_value_translate(value_artist)
        value_search = ' '.join([translated_album, translated_artist])
        value_link = "/".join([self.link_search_begin, value_search, link_deezer_album]).strip()
        return value_link.replace(' ', link_deezer_space), value_artist, value_album

    @staticmethod
    async def get_value_translate(value_insert:str) -> str:
        """
        Static method which is dedicated to get values to the link
        Input:  value_insert = inserted values for the change
        Output: inserted values with minor change of the string
        """
        for value_replace in ['$']:
            value_insert = value_insert.replace(value_replace, link_deezer_dollar)
        return value_insert

    async def get_links_values_albums(self, value_artists:list, value_albums:list) -> list:
        """
        Method which is dedicated to asynchronously return values of the links where to search
        Input:  value_artists = list of the selected artists
                value_albums = list of the selected albums
        Output: value links which would further be used for all of that
        """
        tasks = [asyncio.create_task(self.get_link_values_album_search(artist, album))
                 for artist, album in zip(value_artists, value_albums)]
        return await asyncio.gather(*tasks)

    async def parse_deezer_manually_link(self, session:object, link:str) -> str:
        """
        Async method which is dedicated to fully return values of the link's html
        Input:  session = session of the aiohttp to produce returnal
                link = link where to search search results
        Output: we returned html values of it 
        """
        if link == 'Undefined':
            return link
        async with session.get(link) as r:
            if r.status == 200:
                return await r.text()
        return link

    async def make_html_links(self, session:object, links:list) -> list:
        """
        Async method which is dedicated to return values of the html for selected values        
        Input:  session = session of the aiohttp values
                links = list with calculated links
        Output: list of the presset html values of them
        """
        tasks = [asyncio.create_task(self.parse_deezer_manually_link(session, link)) for link, *_ in links]
        return await asyncio.gather(*tasks)

    @staticmethod
    def get_additional_albums(value_string:str) -> list:
        """
        Method which is dedicated to return additional values 
        Input:  value_string = string value to search
        Output: list of possible values
        """
        value_return = [value_string]
        if " (Remastered)" in value_string and value_string[-13:] == " (Remastered)":
            # print(value_string[:-13])
            # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            value_return.append(value_string[:-13])
        elif " (Remastered)" not in value_string or  (" (Remastered)" in value_string and value_string[-13:] != " (Remastered)"):
            value_return.append(value_string + " (Remastered)")
        return value_return

    async def produce_basic_json_results_album(self, html:str, link:str, album:str, artist:str, year:str) -> list:
        """
        Async which is dedicated to return values of the search of the selected albums
        Input:  html = html value where to search
                link = link which provided those results
                album = album which is searched
                artist = artists which is searched
                sub_artist = 
                sub_album = 
        Output: We created dictionary from the selected values 
        """
        value_list = []
        if len(html) < 1000:
            return value_list
        soup = BeautifulSoup(html, "html.parser")
        check = soup.find("div", {"class":"hidden"})
        check = check.find("script")
        check = check.text if check else ''
        if 'window.__DZR_APP_STATE__ = ' in check:
            value_list = json.loads(check.split('window.__DZR_APP_STATE__ = ')[-1])
            value_list = value_list.get("ALBUM", {})
            value_list = value_list.get('data', [])
            [i.update({"Album Searched": album, "Artist Searched": artist, 
                    "Year Searched":year, "Link Searched": link}) for i in value_list]
            [i.update({"Link Album": '/'.join([link_deezer, link_deezer_us, 
                    link_deezer_album, i.get("ALB_ID", '')])}) for i in value_list]
            
            [i.update({'Checked Album': i.get('Album Searched', '') in self.get_additional_albums(i['ALB_TITLE'])}) for i in value_list]
            [i.update({'Checked Artist': i.get('Artist Searched', '') == i.get('ART_NAME', '')}) for i in value_list]
            
            #TODO think here about the removal
            [i.pop('ARTISTS', None) for i in value_list]
            [i.pop('SUBTYPES', None) for i in value_list]
        return value_list

    async def produce_successfull_failed(self, results:list, search_best:bool, sub_artist:bool, sub_album) -> set:
        """
        Method which is dedicated to filter and return values to the searches for the further songs
        Input:  results = previously calculated values
                search_best = boolean value for the most simplified algorithm of the getting
                sub_artist = boolean which is dedicated to get from the 
                sub_album = boolean which is dedicated to remove from the non used
        Output: two lists with successful and non successfull values which were sorted how is provided
        """
        append_successful, append_bad = [], []
        for result in results:
            if search_best:
                value_dates = [i.get('ORIGINAL_RELEASE_DATE')[:3] for i in result]
                value_get = [i for i, date in zip(result, value_dates) if bool(i.get('Checked Album', False) 
                                and i.get('Checked Artist', False) and date == i.get('Year Searched', ''))]
            else:
                value_get = [i for i in result if bool(i.get('Checked Album', False) 
                                                and i.get('Checked Artist', False))]
            value_get = {} if not value_get else value_get[0]
            if sub_artist and not sub_album:
                value_fail = [f for f in result if f != value_get and f.get('Checked Artist', False)]
            elif sub_artist and sub_album:
                value_fail = [f for f in result if f != value_get and f.get('Checked Artist', False) 
                                                                    and f.get('Checked Album', False)]
            elif not sub_artist and sub_album:
                value_fail = [f for f in result if f != value_get and f.get('Checked Album', False)]
            else:
                value_fail = [f for f in result if f != value_get]
            append_successful.append(value_get)
            append_bad.append(value_fail)
        return append_successful, append_bad

    

    async def produce_search_albums_deezer(self, value_artists:list, value_albums:list, value_years:list, 
                                        search_best:bool=False, sub_artist:bool=True, sub_album:bool=False) -> list:
        """
        Method which is dedicated to return values of the selected values and transform them further
        Input:  value_artists = lists of selected artists
                value_albums = lists of selected albums
                search_best = return key of the most suitable values
                sub_artists = add value sub check of the selected artists
                sub_album = add sub album operating systems
        Output: list with dictionaries of the selected values
        """
        links = await self.get_links_values_albums(value_artists, value_albums)
        
        #TODO think about adding remaster values of the album concrete here
        semaphore = asyncio.Semaphore(deezer_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links)
        tasks = [asyncio.create_task(self.produce_basic_json_results_album(value_html, link, album, artist, year)) 
                for value_html, (link, album, artist), year in zip(value_return[:1], links[:1], value_years[:1])]
        results = await asyncio.gather(*tasks)
        # pprint(results)
        # print('44444444444444444444444444444444444444444444444444')
        # async with semaphore:
        async with semaphore:
            value_list_successfull, value_list_possible = await self.produce_successfull_failed(results, search_best, sub_artist, sub_album)
            pprint(value_list_successfull[0])
            k = requests.get(value_list_successfull[0].get('Link Album', 'Untitled')).text
            soup = BeautifulSoup(k, "html.parser")
            # print(soup)
