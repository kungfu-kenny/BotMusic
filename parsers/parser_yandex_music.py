import os
import json
import asyncio
from pprint import pprint
from time import perf_counter
import aiohttp
import requests
from bs4 import BeautifulSoup
from config import LinkYandex


class ParserYandexMusic:
    """
    class which is dedicated to parse yandex music search for tehreturnal
    """

    def __init__(self) -> None:
        self.link_search_begin = '/'.join([LinkYandex.link_yandex, LinkYandex.link_yandex_search])

    def produce_refresh_values(self, value_list:list) -> set:
        """
        Method which is dedicated to produce refreshing values of the
        Input:  value_list = list of the parsed searches of the 
        Output: set with the values of the refreshings
        """
        values_result, values_successfull, values_possible = [], [], []
        for value_album_searches in value_list:
            value_successfull, value_possible = [], []
            for value_album_search in value_album_searches:
                if value_album_search.get('Album Present', False) and \
                        value_album_search.get('Year Present', False) and \
                        value_album_search.get('Artist Present', False):
                    value_successfull.append(value_album_search)
                    value_possible.append(value_album_search)
                elif (value_album_search.get('Artist Present', False) and \
                        value_album_search.get("Year Present", False) and \
                        not value_album_search.get('Album Present', False)) or \
                        (not value_album_search.get('Artist Present', False) and \
                        value_album_search.get("Year Present", False) and \
                        value_album_search.get('Album Present', False)) or \
                        (value_album_search.get('Artist Present', False) and \
                        not value_album_search.get("Year Present", False) and \
                        value_album_search.get('Album Present', False)):
                    value_possible.append(value_album_search)
            if value_successfull:
                values_result.append(value_successfull[0])
            values_successfull.extend(value_successfull)
            values_possible.extend(value_possible)
        return values_result, values_successfull, values_possible
        
    async def produce_links(self, value_artist:str, value_album:str) -> set:
        """
        Method which is dedicated to produce links for the album
        Input:  value_album = name of the album
                value_artist = name of the artist name
        Output: link which is dedicated to parse values
        """
        value_album_new = await self.produce_manual_link_results(value_album.lower())
        value_artist_new = await self.produce_manual_link_results(value_artist.lower())
        value_search = LinkYandex.link_yandex_space.join([value_artist_new, value_album_new]) 
        return f"{self.link_search_begin}text={value_search}&type=albums", value_artist, value_album

    @staticmethod
    async def produce_manual_link_results(value_string:str) -> str:
        """
        Static method which is dedicated to produce values from the results
        Input:  value_string = value string which needs to be transformed
        Output: string with inputed values
        """
        for value_replaced, value_replace in [['@', LinkYandex.link_yandex_a],
                                            [' ', LinkYandex.link_yandex_space],
                                            ['$', LinkYandex.link_yandex_dollar],
                                            [':', LinkYandex.link_yandex_doublecom]]:
            value_string = value_string.replace(value_replaced, value_replace)
        return value_string

    async def produce_list_selected_links(self, value_artists:list, value_albums:list) -> list:
        """
        Method which is dedicated to produce selected links for the searches
        Input:  value_artists = list of the artists which is searched
                value_albums = list of the albums which were developed
        Output: we developed values of the links for it
        """
        tasks = [asyncio.create_task(self.produce_links(artist, album)) for artist, album in zip(value_artists, value_albums)]
        return await asyncio.gather(*tasks)

    async def parse_yandex_manually_link(self, session:object, value_name_album:str) -> str:
        """
        Method which is dedicated to produce manual search of the albums in cases that we are looking by album
        Input:  session = session object for the search
                value_name_album = album name which is going to be parsed
        Output: we successfully parsed all names which were used on the genius
        """
        if value_name_album == 'Undefined':
            return value_name_album
        async with session.get(value_name_album) as r:
            if r.status == 200:
                return await r.text()
            return value_name_album

    async def make_html_links(self, session:object, links:list, value_multiple:bool=False) -> list:
        """
        Method which is dedicated to make html values from the links
        Input:  session = session object which is from the aiohttp
                links = list with links for getting values
                value_multiple = boolean which signify the status of the sent links
        Output: we developed html for the links
        """
        if not value_multiple:
            tasks = [asyncio.create_task(self.parse_yandex_manually_link(session, link)) for link, *_ in links]
        else:
            tasks = [asyncio.create_task(self.parse_yandex_manually_link(session, link)) for link in links]
        return await asyncio.gather(*tasks)

    @staticmethod
    async def produce_album_song_info(value_html:str) -> dict:
        """
        Method which is dedicated to return info values for the 
        Input:  value_html = html values of the search
        Output: dictionary which is required to get values
        """
        value_dict = {}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, "html.parser")
        soup = soup.find('script', class_="light-data").text
        try:
            soup = json.loads(soup)
        except Exception as e:
            print(e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            soup = {}
        value_dict['Album Description'] = soup.get('description', '')
        value_dict['Album Genre'] = soup.get('genre', '')
        value_dict['Album Name'] = soup.get('name', '')
        value_dict['Number Tracks'] = soup.get('numTracks', 0)
        value_dict['Album Image'] = soup.get('image', '')
        value_dict['Artist Name'] = soup.get("byArtist", {}).get('name', '')
        value_dict['Artist Link'] = soup.get("byArtist", {}).get('url', '')
        value_dict['Album Songs'] = [f.get("name", '') for f in soup.get('track', [])]
        value_dict['Album Songs Number'] = [i + 1 for i in range(len(value_dict.get('Album Songs', [])))]
        value_dict['Album Songs Link'] = [f.get("url", '') for f in soup.get('track', [])]
        value_dict['Album Songs ID'] = [f.get("url", '').split(f'{LinkYandex.link_yandex_track}/')[-1] for f in soup.get('track', [])]
        value_dict['Album Songs Duration'] = [f.get("duration", '') for f in soup.get('track', [])]
        return value_dict

    @staticmethod
    async def produce_basic_json_results_album(value_html:str, link:str, album:str, artist:str, year:str) -> list:
        """
        Method which is dedicated to produce basic json from the album html search
        Input:  value_html = html string of the beaytiful soup which was developed
                link = link of the search
                album = album of the search
                artist = artist of the album
                year = year of the release
        Output: We developed list of dictionaries of the search 
        """
        value_list = []
        if len(value_html) < 1000:
            return value_list
        soup = BeautifulSoup(value_html, "html.parser")
        soup = soup.find(class_="theme-white")
        soup = soup.find("script").text[7:-1]
        try:
            soup = json.loads(soup)
        except Exception as e:
            soup = {}
            print(e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        page_data = soup.get('pageData', {})
        page_data = page_data.get('result', {})
        page_data = page_data.get('albums', {})
        page_data_alb = page_data.get('items', [])
        
        value_albums = [{
            "Album ID": value_album.get("id"),
            "Album Link Search": link,
            "Album Link": '/'.join([LinkYandex.link_yandex, 
                                    LinkYandex.link_yandex_album, 
                                    str(value_album.get("id"))]) 
                                    if value_album.get("id") else '',
            "Year Searched": year,
            "Album Searched": album, 
            "Year": value_album.get("year"),
            "Year Present": value_album.get('year') == year,
            "Original Release Year": value_album.get("originalReleaseYear"),
            "Album Present": value_album.get('title', '').lower() == album.lower(),
            "Track Number": value_album.get("trackCount", 0),
            "Content Warning": value_album.get("contentWarning", ""),
            "Version": value_album.get("version", ""),
            "Genre": value_album.get("genre", ""),
            "Album Cover": value_album.get("coverUri", ""),
            "Title": value_album.get("title", ''),
            "Labels": value_album.get("labels", []),
            "artists": value_album.get("artists", [])
        }
        for value_album in page_data_alb]
        
        value_artists = [f.pop("artists", []) for f in value_albums]
        value_artists = [{
            "Artist Searched": artist,
            "Artist ID": [f.get('id', 0) for f in value_artist],
            "Artist Name": [f.get('name', '') for f in value_artist],
            "Artist Present": any(f.get('name', '').lower() == artist.lower() for f in value_artist),
            "Artist Cover": [f.get('cover', {}).get('uri', '') for f in value_artist],
            "Artist Composer Boolean": [f.get("composer", False) for f in value_artist],
        } for value_artist in value_artists]

        [album.update(artist) for album, artist in zip(value_albums, value_artists)]
        return value_albums

    @staticmethod
    async def produced_detailed_song_info(html:str) -> dict:
        """
        Async method which is dedicated to produce the detailed songs information about the values
        Input:  value_html = html which was parsed from the song information
        Output: dictionary with previously parsed values of the 
        """
        value_dict = {}
        if len(html) < 1000:
            return value_dict
        soup = BeautifulSoup(html, 'html.parser')
        soup = soup.find(class_='theme-white')
        soup = soup.find('script').text[7:-1]
        try:
            soup = json.loads(soup)
        except Exception as e:
            print(e)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            soup = {}
        soup = soup.get('sidebarData', {})
        soup_lyrics = soup.get('lyric', {})
        soup_song_album = soup.get('track', {}).get('albums', [])
        soup_song_artist = soup.get('track', {}).get('artists', [])
        soup_song_similar = soup.get('similarTracks', []) 
        
        value_dict['Song Lyrics'] = soup_lyrics[0].get('fullLyrics', '') if soup_lyrics else ''
        value_dict['Song Lyrics Language'] = soup_lyrics[0].get('textLanguage', 'unknown') if soup_lyrics else 'unknown'
        value_dict['Song IDs'] = [f.get('id', 0) for f in soup_song_album]
        value_dict['Song Contents'] = [f.get('contentWarning', '') for f in soup_song_album]
        value_dict['Song Genres'] = [f.get('genre', '') for f in soup_song_album]
        value_dict['Song Years'] = [f.get('year', 0) for f in soup_song_album]
        value_dict['Song Major ID'] = [f.get('major', {}).get('id', 0) for f in soup_song_album]
        value_dict['Song Major Name'] = [f.get('major', {}).get('name', '') for f in soup_song_album]
        value_dict['Song Duration Milliseconds'] = [f.get("durationMs", 0) for f in soup_song_album]
        value_dict['Song Versions'] = [f.get('version', '') for f in soup_song_album]
        value_dict['Song Positions'] = [f.get('trackPosition', {}).get('index', 0) for f in soup_song_album]
        value_dict['Song Titles'] = [f.get('title', '') for f in soup_song_album]
        value_dict['Song Yandex Important'] = [f.get('veryImportant', False) for f in soup_song_album]
        value_dict['Song Album Tracks'] = [f.get('trackCount', 0) for f in soup_song_album]
        value_dict['Song Label Names'] = [[f.get('name', '') for f in value_f.get('labels', [])] for value_f in soup_song_album]
        value_dict['Song Label IDs'] = [[f.get('id', 0) for f in value_f.get('labels', [])] for value_f in soup_song_album]
        value_dict['Song Artist Ids'] = [[f.get('id', 0) for f in value_f.get('artists', [])] for value_f in soup_song_album]
        value_dict['Song Artist Names'] = [[f.get('name', '') for f in value_f.get('artists', [])] for value_f in soup_song_album]
        
        value_dict['Artist Composer Booleans'] = [f.get('composer', False) for f in soup_song_artist]
        value_dict['Artist IDs'] = [f.get('id', 0) for f in soup_song_artist]
        value_dict['Artist Names'] = [f.get('name', '') for f in soup_song_artist]
        value_dict['Song Similars']= [
            {
                'Song Similar to ID': value_dict.get('Song IDs', []),
                'Song Similar ID': i.get('id', 0),
                'Song Similar Real ID': i.get('realID', 0),
                'Song Similar Title': i.get('title', ''),
                'Song Similar Version': i.get('version', ''),
                'Song Similar Major ID': i.get('major', {}).get('id', ''),
                'Song Similar Major Name': i.get('major', {}).get('name', ''),
                'Song Similar Artist IDs': [f.get('id', 0) for f in i.get("artists", [])],
                'Song Similar Artist Names': [f.get('name', 0) for f in i.get("artists", [])],
                'Song Similar Album IDs': [f.get('id', 0) for f in i.get("albums", [])],
                'Song Similar Album Titles': [f.get('title', '') for f in i.get("albums", [])],
                'Song Similar Album Years': [f.get('year', 0) for f in i.get("albums", [])],
                'Song Similar Album Genres': [f.get('genre', '') for f in i.get("albums", [])],
                'Song Similar Album Track Counts': [f.get("trackCount", 0) for f in i.get("albums", [])],
                'Song Similar Album Track Positions': [f.get("trackPosition", {}).get("index", 0) 
                                                                for f in i.get("albums", [])],
                'Song Similar Album Label IDs': [[k.get('id', 0) for k in f.get('labels', [])] 
                                                                for f in i.get("albums", [])],
                'Song Similar Album Label Names': [[k.get('name', '') for k in f.get('labels', [])] 
                                                                for f in i.get("albums", [])],
            } for i in soup_song_similar]
        return value_dict

    async def produce_manual_albums_search_yandex(self, value_artists:list, value_albums:list, value_years:list, value_text:bool=False) -> set:
        """
        Method which is dedicated to produce manual search of the 
        Input:  value_album = list with the albums which were used
                value_artist = list with artists which those album wrote
                value_year = list with years of selected values
                value_text = boolean values for the getting additional text of the returning it
        Output: set of selected values of the search within 
        """
        links = await self.produce_list_selected_links(value_artists, value_albums)
        semaphore = asyncio.Semaphore(LinkYandex.yandex_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links)
        tasks = [asyncio.create_task(self.produce_basic_json_results_album(value_html, link, album, artist, year)) 
                for value_html, (link, album, artist), year in zip(value_return, links, value_years)]
        results = await asyncio.gather(*tasks)
        value_result, value_successfull, value_possible = self.produce_refresh_values(results)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, [f.get('Album Link', 'Undefined') for f in value_result], True)
        tasks = [asyncio.create_task(self.produce_album_song_info(html)) for html in value_return]
        value_albums = await asyncio.gather(*tasks)
        value_albums_additional = []
        if value_text:
            return value_albums, value_result, value_successfull, value_possible, value_albums_additional
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                for value_album in value_albums:
                    value_return = await self.make_html_links(session, value_album.get('Album Songs Link', []), True)
                    value_albums_additional.append([await self.produced_detailed_song_info(val_return) for val_return in value_return])
        return value_albums, value_result, value_successfull, value_possible, value_albums_additional