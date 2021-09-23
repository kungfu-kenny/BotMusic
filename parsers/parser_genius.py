import ast
import aiohttp
import asyncio
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from config import (link_genius,
                    link_genius_albums,
                    link_genius_search_begin,
                    link_genius_search_end,
                    genius_semaphore_threads)


class ParserGenius:
    """
    class which is dedicated to produce basic parsings of the info about songs
    """
    def __init__(self) -> None:
        self.link_genius_albums = '/'.join([link_genius, link_genius_albums])

    @staticmethod
    def combine_link_values(value_link:str, value_artist:str, value_album:str) -> str:
        """
        Static method which is dedicated to produce values of the link
        Input:  value_link = link previously crafted
                value_artist = artist of the value
                value_album = album to search
        Output: link values of the search
        """
        return '/'.join([value_link, value_artist, value_album])

    @staticmethod
    def get_values_link_genius(value_inserted:str) -> str:
        """
        Static method which is dedicated to make basic genius link for all of this
        Input:  value_inserted = string value which is required to be transformed
        Output: value which would be ready to search
        """
        value_inserted = value_inserted.strip()
        for letter in ['?', '(', ')', '"', '!', '`', '+', '.', '_', '&']:
            if letter in value_inserted:
                value_inserted = value_inserted.replace(letter, '')
        value_inserted = '-'.join(value_inserted.split(' ')).lower().capitalize()
        for letter in [':', "'", '$', '’','/']:
            if letter in value_inserted:
                value_inserted = value_inserted.replace(letter, '-')
        for length in range(len(value_inserted), 1, -1):
            value_replace = ''.join(['-' for _ in range(length)])
            if value_replace in value_inserted:
                value_inserted = value_inserted.replace(value_replace, '-')
        for i in [0, -1]:
            if value_inserted[i] == '-':
                value_inserted.pop(i)
        return ''.join(value_inserted)

    async def get_link_album(self, album:str, artist:str) -> str:
        """
        Method which is dedicated to produce values of the album link via it's usage
        Input:  album = value of the album
                artist = value of the artist
        Output: value of the lonk which was created manually
        """
        return self.combine_link_values(self.link_genius_albums,
                self.get_values_link_genius(artist), 
                self.get_values_link_genius(album))

    async def produce_links_parse_albums(self, list_artists:list, list_albums:list) -> list:
        """
        Method which is dedicated to produce the links for the parsing of the values
        Input:  list_artists = list with the artists which is required to search theirs album
                list_albums = list with the albums which it would parse to all of this
        Output: list with the links which would be further used for getting parsed
        """
        list_links = []
        for artist, album in zip(list_artists, list_albums):
            list_links.append(asyncio.create_task(self.get_link_album(album, artist)))
        return await asyncio.gather(*list_links)

    async def parse_genius_manually_album_link(self, value_html:str, value_link:str, value_bool:bool) -> dict:
        """
        Method which is dedicated to produce info from the genius values
        Input:  value_html = html parsed values from the link
                value_link = value for the link of this album
                value_bool = value which signify to make the repeating values for it
        Output: we successfully created dictionary with the links of the 
        """
        value_dict = {"Song_Link": value_link}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, "html.parser")
        soup_label = [f.text for f in soup.find_all("span", {"class":"metadata_unit-label"})]
        soup_lyrics = soup.find('div', {"class": "lyrics"})
        if soup_lyrics:
            value_dict['Lyrics'] = soup_lyrics.text
        for subcolumn in ['Written By', 'Engineer', 'Produced by', 'Recorded At', 'Release Date']:
            if subcolumn in soup_label:
                label_index = soup_label.index(subcolumn)
                soup_label_value = [f.text.strip() for f in soup.find_all("span", {"class":"metadata_unit-info"})][label_index]
                value_dict[subcolumn] = soup_label_value
        if value_bool and len(list(value_dict.keys())) == 1:
            try:
                return await self.parse_genius_manually_album_link(self.parse_links_iframe(value_link), value_link, value_bool) 
            except Exception as e:
                print(e)
                print('######################################################')
                return value_dict
        return value_dict

    async def parse_genius_automatic_album_link(self, value_html:str, value_link:str) -> dict:
        """
        Method which is dedicated to make values from the album
        Input:  value_html = parsed html value
        Output: dictionary with all values which were used
        """
        value_dict = {"Album_Link": value_link}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, "html.parser")
        soup = soup.find("routable-page")
        soup_name_album = soup.find("h1").text.strip()
        soup_name_artist = soup.find("h2").text.strip()
        soup_release = soup.find("div", {"class":"header_with_cover_art-primary_info_container"})
        soup_release = soup_release.find("div", {"class":"metadata_unit"}).text
        song_number = [f.text.strip() for f in soup.find_all("span", {"class": "chart_row-number_container-number"})]
        song_number = [int(f) for f in song_number if f]
        song_len = song_number[-1]
        soup_songs_check = soup.find_all("h3")
        soup_song_links = soup.find_all('a', {"class": "u-display_block"}, href=True)
        soup_song_links = [f['href'] for f in soup_song_links]
        soup_songs = soup_songs_check[:song_len]
        soup_songs = [f.text.strip().split('\n              Lyrics')[0] for f in soup_songs]
        soup_label = [f.text for f in soup.find_all("span", {"class":"metadata_unit-label"})]
        for subcolumn in ['Label', 'Producer']:
            if subcolumn in soup_label:
                label_index = soup_label.index(subcolumn)
                soup_label_value = [f.text.strip() for f in soup.find_all("span", {"class":"metadata_unit-info"})][label_index]
                value_dict[subcolumn] = soup_label_value
        value_dict['Album_Name'] = soup_name_album
        value_dict['Artist_Name'] = soup_name_artist
        value_dict['Date'] = soup_release
        value_dict['Album_Length'] = song_len
        value_dict['Songs_Tracklist'] = soup_songs 
        value_dict['Songs_Number'] = song_number
        value_dict['Songs_Links'] = soup_song_links
        
        return value_dict
        
    @staticmethod
    def get_values_html(html:str) -> list:
        """
        Static method which is dedicated to produce values of the html iframe
        Input:  html = html which was saved
        Output: list of values which we would currently use
        """
        if len(html) < 1000:
            return ['Undefined', 'Undefined']
        soup = BeautifulSoup(html, "html.parser")
        soup = soup.find_all('iframe')
        soup_check = ['Undefined', 'Undefined']
        if soup:
            soup_check = [f['src'] for f in soup]
        return soup_check

    async def parse_genius_song_length(self, value_html:list, value_link:str) -> str:
        """
        Method which is dedicated to return length of the song via the page 
        within the Genous and apple music subelement which shows that
        Input:  value_html = parsed html value for getting values of the length
                value_link = link to the song with the lyrics
        Output: length of the selected track
        """
        try:
            value_links = self.get_values_html(value_html)
            if value_links != ['Undefined', 'Undefined'] and value_links and len(value_links) > 1:
                return value_links
            value_html = self.parse_links_iframe(value_link)
            return await self.parse_genius_song_length(value_html, value_link)
        except Exception as e:
            #TODO add here some exception
            return ['Undefined', 'Undefined']

    @staticmethod
    def produce_genius_manually_link(value_search:str) -> set:
        """
        Static method which is dedicated to produce link for it
        Input:  value_search = value which is searched by us
        Output: we created link values for further parsing
        """
        return ''.join([link_genius, link_genius_search_begin, value_search, link_genius_search_end])

    @staticmethod
    async def produce_genius_above(value_link:str) -> str:
        """
        Async method which is dedicated to return name from the link
        Input:  value_link = link which was from the search
        Output: string values which is dedicated 
        """
        return await value_link.split(link_genius)[0] \
                                .split(link_genius_search_begin)[0] \
                                .split(link_genius_search_end)[0]

    async def parse_genius_manually_link(self, session:object, value_name_album:str, value_check=False) -> str:
        """
        Method which is dedicated to produce manuall search of the albums in caes that we are looking by album
        Input:  session = session object for the search
                value_name_album = album name which is going to be parsed
                value_check = value 
        Output: we successfully parsed all names which were used on the genius
        """
        if value_name_album == 'Undefined':
            return value_name_album
        async with session.get(value_name_album) as r:
            if r.status == 200:
                return await r.text()
            if not value_check:
                return await self.produce_genius_above(value_name_album)
            return value_name_album
    
    def parse_links_iframe(self, value_link:str) -> str:
        """
        Method which is dedicated to return text of the html for the getting values of the length
        Input:  value_link = link value of the song 
        Output: get value of the link with the song
        """
        with requests.get(value_link) as r:
            if r.status_code == 200:
                return r.content
        return value_link

    @staticmethod
    def parse_subvalues_apple_music(value_string:str) -> dict:
        """
        Static method which is dedicated to take only necessary values for the song which would be used further
        Input:  value_string = string value of the 
        Output: we created dictionary for the further work
        """
        value_dict = {}
        value_list = value_string[2:-1].split(',"')
        for column_name in ['title', 'artist_display_name', 'artwork_url']:
            for column_key, column_value in [v.split('":') for v in value_list]:
                if column_name == column_key:
                    value_dict[column_key] = column_value[1:-1]
        return value_dict

    async def parse_apple_music_song_length(self, value_html:str, value_link:str) -> object:
        """
        Async Method which is dedicated to parse the apple music link for getting all possible values about the song
        Input:  value_html = html which was previously parsed from it
                value_link = link to this html
        Output: values which were succesfully parsed
        """
        value_dict = {}
        soup = BeautifulSoup(value_html, "html.parser")
        soup = soup.find("apple-music-player")
        if soup:
            value_dict.update(ast.literal_eval(soup['apple_music_tracks'])[0])
            value_dict.update({'song_id': int(soup['song_id'])})
            value_dict.pop('country_codes')
            value_dict.update(self.parse_subvalues_apple_music(soup['unmatched_placeholder_track']))
        return value_dict

    async def make_html_links(self, session:object, value_album_list:list, value_bool:bool=False) -> list:
        """
        Asyncio values of the generating html from the links
        Input:  session = session of the aoihttp
                value_album_list = list values to parse
                value_bool = value which is dedicated to return values 
        Output: list values to work with further parsing
        """
        tasks = [asyncio.create_task(self.parse_genius_manually_link(session, value_album_link, value_bool))
                                                                    for value_album_link in value_album_list]
        results = await asyncio.gather(*tasks)
        return results

    async def parse_genius_manually_album_list(self, value_album_list:list) -> list:
        """
        Async method which is dedicated to produce different genius values
        Input:  value_album_list = list of the link which is required to be searched
        Output: list with parsed html values
        """
        links = [self.produce_genius_manually_link(f) for f in value_album_list]
        semaphore = asyncio.Semaphore(genius_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links)
        return value_return

    async def parse_genius_album_link_additional(self, value_album_links:list) -> list:
        """
        Async method which is dedicated to make additional album links
        Input:  value_album_links = value list of the links
        Output: we succesfully created values of the 
        """
        value_album = {}
        semaphore = asyncio.Semaphore(genius_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, value_album_links, True)
            tasks = [asyncio.create_task(self.parse_genius_song_length(f, link)) for f, link in zip(value_return, value_album_links)]
            list_lengthes = await asyncio.gather(*tasks)
                
            list_link_song_youtube = [f[0] for f in list_lengthes]
            list_link_apple_music = [f[1] for f in list_lengthes]
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return_length = await self.make_html_links(session, list_link_apple_music, True)
            tasks = [asyncio.create_task(self.parse_apple_music_song_length(html, link)) for html, link in zip(value_return_length, list_link_apple_music)]
            list_apple_music_values = await asyncio.gather(*tasks)
            value_album.update({'Song': value_album_links})
            value_album.update({'Song_Links_Youtube': list_link_song_youtube})
            value_album.update({'Song_Parameters': list_apple_music_values})
        return value_album

    async def parse_genius_song_additional_info(self, value_album_list:list, value_artist_list:list, value_repeat:bool=False) -> list:
        """
        Async method which is dedicated to work with a song's lyrics and return them later
        Input:  value_album_list = list with the values of the album
                value_artist_list = the same but with the artists name
                value_repeat = boolean value for the repeating values of it
        Output: list of the new values but only with a values 
        """
        links = await self.produce_links_parse_albums(value_artist_list, value_album_list)
        semaphore = asyncio.Semaphore(genius_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links, True)
        tasks = [asyncio.create_task(self.parse_genius_automatic_album_link(value_html, link)) for value_html, link in zip(value_return, links)]
        results = await asyncio.gather(*tasks)
        
        async with semaphore:
            for value_album in results:
                links = value_album.get('Songs_Links', [])
                async with aiohttp.ClientSession(trust_env=True) as session:
                    value_return = await self.make_html_links(session, links, True)

                tasks = [asyncio.create_task(self.parse_genius_manually_album_link(value_html, link, value_repeat)) for value_html, link in zip(value_return, links)]
                value_album.update({"Songs_Values": await asyncio.gather(*tasks)})
        return results

    async def parse_genius_automatic_album_list(self, value_album_list:list, value_artist_list:list) -> list:
        """
        Async method which is dedicated to make automatic album list for further parsing
        Input:  value_album_list = list with the values of the album
        Output: we successfully created values from the parsing
        """
        links = await self.produce_links_parse_albums(value_artist_list, value_album_list)
        semaphore = asyncio.Semaphore(genius_semaphore_threads)
        async with semaphore:
            async with aiohttp.ClientSession(trust_env=True) as session:
                value_return = await self.make_html_links(session, links, True)
        tasks = [asyncio.create_task(self.parse_genius_automatic_album_link(value_html, link)) for value_html, link in zip(value_return, links)]
        results = await asyncio.gather(*tasks)
        async with semaphore:
            for value_album in results:
                links = value_album.get('Songs_Links', [])
                async with aiohttp.ClientSession(trust_env=True) as session:
                    value_return = await self.make_html_links(session, links, True)
                tasks = [asyncio.create_task(self.parse_genius_song_length(f, link)) for f, link in zip(value_return, links)]
                list_lengthes = await asyncio.gather(*tasks)
                
                list_link_song_youtube = [f[0] for f in list_lengthes]
                list_link_apple_music = [f[1] for f in list_lengthes]
                async with aiohttp.ClientSession(trust_env=True) as session:
                    value_return_length = await self.make_html_links(session, list_link_apple_music, True)
                tasks = [asyncio.create_task(self.parse_apple_music_song_length(html, link)) for html, link in zip(value_return_length, list_link_apple_music)]
                list_apple_music_values = await asyncio.gather(*tasks)
                value_album.update({'Song_Links_Youtube': list_link_song_youtube})
                value_album.update({'Song_Parameters': list_apple_music_values})
        return results
                