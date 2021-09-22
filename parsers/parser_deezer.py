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

    async def make_html_links(self, session:object, links:list, value_multiple:bool=False) -> list:
        """
        Async method which is dedicated to return values of the html for selected values        
        Input:  session = session of the aiohttp values
                links = list with calculated links
                value_multiple = boolean value for the multiple searches
        Output: list of the presset html values of them
        """
        if not value_multiple:
            tasks = [asyncio.create_task(self.parse_deezer_manually_link(session, link)) for link, *_ in links]
        else:
            tasks = [asyncio.create_task(self.parse_deezer_manually_link(session, link)) for link in links]
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
        check = str(check).split('</script>')[0]  if check else ''
        if check:
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
            value_dates = [int(i.get('ORIGINAL_RELEASE_DATE', '-4000')[:4]) for i in result]
            if search_best:
                value_get = [i for i, date in zip(result, value_dates) if bool(i.get('Checked Album', False) 
                                and i.get('Checked Artist', False) and date == i.get('Year Searched', ''))]
            else:
                value_get = [i for i, date in zip(result, value_dates) if bool(i.get('Checked Artist', False) and date == i.get('Year Searched', ''))]
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

    async def produce_search_album_songs_parameters(self, html:str, link:str) -> dict:
        """
        Async method which is dedicated to get values of the songs to get from it
        Input:  html = parsed html value from the got values
                link = link value which was previously parsed
        Output: dictionary value with all previously got information
        """
        value_dict = {}
        if len(html) < 1000:
            return value_dict
        soup = BeautifulSoup(html, "html.parser")
        soup_head = soup.find(id="naboo_album_head")
        album_name = soup_head.find('h1').text.strip()
        album_track_number = soup.find('meta', {"itemprop":"numTracks"}).get("content", '0')

        album_artist = soup_head.find(id="naboo_album_artist")
        album_artist = [f.text.strip() for f in album_artist.find_all('span')]
        if len(album_artist) > 1:
            album_artist, album_year_artist, *_ = album_artist
        elif len(album_artist) == 1:
            album_artist, album_year_artist = album_artist[0], ''
        else:
            album_artist, album_year_artist = '', ''
        album_label = soup_head.find("div", {"class": "naboo-album-label label"})
        album_label = album_label.text.strip() if album_label else ''

        soup_main = soup.find("div", {"class": "naboo_album_content"})
        album_duration = soup_main.find(id="naboo_album_duration")
        album_duration = album_duration.text.strip() if album_duration else ''
        album_duration = album_duration.split('Total duration:')[-1] if 'Total duration:' in album_duration else album_duration
        
        album_tracks = soup_main.find_all("td", {"class": "track"})
        album_tracks = [(a.text.strip(), a.find("a", {"class":"evt-click"}).get('href', '')) for a in album_tracks]
        
        album_length = [f.text.strip() for f in soup_main.find_all("td", {"class": "added"})]
        album_artist_song = [f.text.strip() for f in soup_main.find_all("td", {"class": "artist"})]
        album_mark = [f.get('title', '0') for f in soup_main.find_all("td", {"class": "popularity"})]
        album_mark = [f.split('By popularity:')[-1] for f in album_mark]

        value_dict['Album Number Tracks'] = album_track_number
        value_dict['Album Name'] = album_name
        value_dict['Album Artist'] = album_artist
        value_dict['Album Year'] = album_year_artist
        value_dict['Album Label'] = album_label
        value_dict['Album Duration'] = album_duration
        
        list_songs = []
        for (name, link), length, author, popularity in zip(album_tracks, album_length, album_artist_song, album_mark):
            tmp_dict = {}
            tmp_dict['Song Name'] = name
            tmp_dict['Song Link'] = link
            tmp_dict['Song Length'] = length
            tmp_dict['Song Author'] = author
            tmp_dict['Song Popularity'] = popularity
            list_songs.append(tmp_dict)
        value_dict['Song Parameters'] = list_songs

        return value_dict

    async def produce_search_albums_deezer(self, value_artists:list, value_albums:list, value_years:list, 
                                        search_best:bool=False, sub_artist:bool=True, sub_album:bool=False) -> set:
        """
        Method which is dedicated to return values of the selected values and transform them further
        Input:  value_artists = lists of selected artists
                value_albums = lists of selected albums
                search_best = return key of the most suitable values
                sub_artists = add value sub check of the selected artists
                sub_album = add sub album operating systems
        Output: list with dictionaries of the selected values
        """
        list_non_found = []
        links = await self.get_links_values_albums(value_artists, value_albums)
        
        #TODO think about adding remaster values of the album concrete here
        semaphore = asyncio.Semaphore(deezer_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links)
        tasks = [asyncio.create_task(self.produce_basic_json_results_album(value_html, link, album, artist, year)) 
                for value_html, (link, album, artist), year in zip(value_return, links, value_years)]
        results = await asyncio.gather(*tasks)
        async with semaphore:
            value_list_successfull, value_list_possible = await self.produce_successfull_failed(results, search_best, sub_artist, sub_album)
            links_successfull = []
            for index, i in enumerate(value_list_successfull):
                if i: 
                    links_successfull.append(i.get('Link Album'))
                else: 
                    list_non_found.append(links[index])
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links_successfull, True)
        tasks = [asyncio.create_task(self.produce_search_album_songs_parameters(html, link)) for html, link in zip(value_return, links_successfull)]
        parsed_albums = await asyncio.gather(*tasks)
        return parsed_albums, value_list_successfull, value_list_possible, list_non_found
