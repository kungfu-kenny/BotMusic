import os
import time
import asyncio
from pprint import pprint
import json
import numpy as np
import pandas as pd
from parsers.parser_genius import ParserGenius
from parsers.parser_deezer import ParserDeezer
from parsers.parser_apple_music import ParserAppleMusic
from config import (csv_year,
                    csv_basic,
                    csv_genre,
                    csv_edges,
                    csv_albums,
                    csv_artist,
                    csv_subgenre,
                    csv_basic_song,
                    csv_basic_genre,
                    csv_basic_song_fail,
                    csv_basic_song_apple,
                    csv_basic_song_deezer,
                    csv_basic_song_genius,
                    folder_current,
                    folder_storage,
                    folder_defaults)


class ParserDefaultCSV:
    """
    class which is dedicated to produce from the open source csv
    and to insert them into the database
    """
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.columns = ['Album_ID', 'Album_Name', "Artist_ID", 'Artist', 'Genre', 'Year']
        self.columns_songs = ['Album_ID', 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Album_Length', 
                        'Album_Link', 'Album_Name', 'Artist_Name', 'Date', 'Label', 'Song_Links_Youtube', 
                        'Songs_Links', 'Songs_Number', 'Songs_Tracklist','Apple_ID', 
                        'Artwork_Url', 'Duration', 'Artist_Display_Name', 'Song_Genius_ID', 'Title']
        self.columns_songs_genius = ['Album_ID', 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Album_Length',
                                'Album_Link', 'Album_Name_Genius', 'Artist_Name_Genius', 'Album_Date_Genius',
                                'Album_Label_Genius', 'Songs_Lyrics', 'Song_Engineer', 'Song_Link', 'Song_Written',
                                'Album_Producer', 'Song_Place_Recorded', 'Song_Release_Genius']
        self.folder_defaults = os.path.join(folder_current, folder_defaults)
        # self.produce_basic_values_genius()
        self.produce_basic_values_deezer()
        
    def check_presence_files(self) -> bool:
        """
        Method which is dedicated to check presence of necessary files for further work
        Input:  presented dataframes from open sources
        Output: boolean values which signify to continue
        """
        value_check = [os.path.join(self.folder_defaults, x) for x in [
                        csv_year, csv_genre, csv_edges, csv_albums, csv_artist, csv_subgenre]]
        return all([os.path.exists(x) and os.path.isfile(x) for x in value_check])

    def check_presence_work_previous(self) -> bool:
        """
        Method which is dedicated to check that 
        Input:  Input values in folder
        Output: boolean values which 
        """
        value_check = [os.path.join(self.folder_defaults, x) for x in [csv_basic, csv_basic_genre]]
        return all([os.path.exists(x) and os.path.isfile(x) for x in value_check])

    @staticmethod
    def get_values_list_df(df_used:pd.DataFrame, df_index:list, column:str='name', column_index:str="~id") -> list:
        """
        Method which is dedicated to get values list of the df
        Input:  df_used = dataframe of values where to take values
                df_index = index where to take values
        Output: list with values of the 
        """
        value_return = []
        for index in df_index:
            value_return.extend(df_used.loc[df_used[column_index]==index, column].values)
        return value_return

    @staticmethod
    def produce_genre(value_genre:list, value_subgenre:list) -> list:
        """
        Static method which is dedicated to produce from the original data genre + subgenre
        Input:  value_genre = genre from the dataframe
                value_subgenre = subgenre from the dataframe
        Output: list with all previously used values 
        """
        value_genre.extend(value_subgenre)
        value_genre = list(set(value_genre))
        return [f for f in value_genre if f !='None']

    @staticmethod
    def produce_duplicates(value_list:list, value_len:int) -> list:
        """
        Method which is dedicated to make the duplicated values for it
        Input:  value_list = list with values which we have
                value_len = length which list needs to archieve
        Output: we made duplicates within the list
        """
        if len(value_list) == 1 and value_len > 1:
            value_take = value_list[0]
            for i in range(value_len-1):
                value_list.append(value_take)
        return value_list

    @staticmethod
    def produce_basic_genres(df_genre:pd.DataFrame, df_subgenre:pd.DataFrame) -> pd.DataFrame:
        """
        Method which is dedicated to create dataframe for genre values
        Input:  df_genre = genre dataframe
                df_subgenre = subgenre dataframe 
        Output: we created values of the groups id
        """
        values_groups = df_genre['name'].unique()
        values_groups = np.append(values_groups, df_subgenre['name'].unique(), 0)
        values_groups = np.unique(values_groups)
        values_index = [i+1 for i in range(len(values_groups))]
        return pd.DataFrame(list(zip(values_index, values_groups)), columns=['~id', 'name'])

    def produce_manual_changes(self, df_calculated:pd.DataFrame, df_genre_id:pd.DataFrame) -> set:
        """
        Method which is dedicated to manual change values for more comfortable usage
        Input:  df_calculated = calculated dataframe for further work
                df_genre_id = dataframe of the genre and it's id
        Output: set of the same dataframes values
        """
        df_genre_id.replace({'name':{"& Country": "Country"}}, inplace=True)
        df_genre_id_name = np.sort(df_genre_id['name'].unique())
        df_genre_id_id = [i for i in range(1, len(df_genre_id_name) + 1)]
        df_genre_id = pd.DataFrame(list(zip(df_genre_id_id, df_genre_id_name)), columns=['~id', 'name'])
        df_calculated = df_calculated.replace({'Genre':{"& Country": "Country"}})
        df_calculated.drop_duplicates(subset=['Genre', 'Album_ID'], keep='first', inplace=True)
        df_genre_id_name = df_calculated['Genre'].values
        value_list_id = self.get_values_list_df(df_genre_id, df_calculated['Genre'].values, '~id', 'name')
        df_calculated.insert(4, 'Genre_ID', value_list_id)
        df_genre_id.replace({'name':{"Musique Concr?te": "Musique Concrete"}}, inplace=True)
        df_calculated.replace({'Genre':{"Musique Concr?te": "Musique Concrete"},
                            'Artist': {"John Lennon / Plastic Ono Band": "John Lennon"},
                            "Album_Name": {'Sign \\"Peace\\" the Times': "Sign O’ the Times", 
                            'Live at the Apollo, 1962':'Live at the Apollo',
                            'The Great Twenty_Eight':'The Great Twenty Eight',
                            "(pronounced 'leh-'nerd 'skin-'nerd)": "(Pronounced 'leh-'nerd 'skin-'nerd)",}}, inplace=True)
        for i in ['[', ']', "\\"]:
            df_calculated.Album_Name=df_calculated.Album_Name.str.replace(i, '', regex=True)
        return df_calculated, df_genre_id

    def produce_basic_value(self) -> None:
        """
        Method which is dedicated to produce basic value of the dataframe for the 
        Input:  values of the parser
        Output: we created fully parsed dataframe with some parameters
        """
        if not self.check_presence_files():
            #TODO add here print or log
            return
        if self.check_presence_work_previous():
            #TODO add here print or log
            return
        df_albums = pd.read_csv(os.path.join(self.folder_defaults, csv_albums))
        df_genre = pd.read_csv(os.path.join(self.folder_defaults, csv_genre))
        df_artist = pd.read_csv(os.path.join(self.folder_defaults, csv_artist))
        df_subgenre = pd.read_csv(os.path.join(self.folder_defaults, csv_subgenre))
        df_year = pd.read_csv(os.path.join(self.folder_defaults, csv_year))
        df_edges = pd.read_csv(os.path.join(self.folder_defaults, csv_edges))
        df_genre_id = self.produce_basic_genres(df_genre, df_subgenre)
        
        values_id = df_edges['~from'].unique()
        df_artist['Artist_ID'] = [f for f in range(1, df_artist['name'].nunique() + 1)]
        return_index, return_album, return_artist_id = [], [], [] 
        return_artist, return_genre, return_year = [], [], []
        for index, value_id in enumerate(values_id):
            df_slice = df_edges.loc[df_edges["~from"]==value_id]
            df_id_year = df_slice.loc[df_slice["~label"]=='hasYear', '~to'].values
            df_id_artist = df_slice.loc[df_slice["~label"]=='hasArtist', '~to'].values
            df_id_genre = df_slice.loc[df_slice["~label"]=='hasGenre', '~to'].values
            df_id_subgenre = df_slice.loc[df_slice["~label"]=='hasSubgenre', '~to'].values
            
            df_res_album = self.get_values_list_df(df_albums, [value_id], 'title') 
            df_res_year = self.get_values_list_df(df_year, df_id_year)
            df_res_artist = self.get_values_list_df(df_artist, df_id_artist)
            df_res_artist_id = self.get_values_list_df(df_artist, df_id_artist, 'Artist_ID')
            df_res_genre = self.get_values_list_df(df_genre, df_id_genre)
            df_res_subgenre = self.get_values_list_df(df_subgenre, df_id_subgenre)
            df_res_genre = self.produce_genre(df_res_genre, df_res_subgenre)
            value_max = max([len(df_res_album), len(df_res_year), len(df_res_artist), len(df_res_genre)])
            
            df_res_index = self.produce_duplicates([index + 1], value_max)
            df_res_album = self.produce_duplicates(df_res_album, value_max)
            df_res_year = self.produce_duplicates(df_res_year, value_max)
            df_res_artist_id = self.produce_duplicates(df_res_artist_id, value_max)
            df_res_artist = self.produce_duplicates(df_res_artist, value_max)
            df_res_genre = self.produce_duplicates(df_res_genre, value_max)
           
            return_year.extend(df_res_year)
            return_index.extend(df_res_index)
            return_album.extend(df_res_album)
            return_genre.extend(df_res_genre)
            return_artist.extend(df_res_artist)
            return_artist_id.extend(df_res_artist_id)
        
        df_calculated = pd.DataFrame(list(zip(return_index, return_album, return_artist_id, 
                        return_artist, return_genre, return_year)), columns=self.columns)
        
        df_calculated, df_genre_id = self.produce_manual_changes(df_calculated, df_genre_id)

        for df_value, value_name in zip([df_calculated, df_genre_id], [csv_basic, csv_basic_genre]):
            self.produce_basic_csv_save(df_value, os.path.join(self.folder_defaults, value_name))
        
    @staticmethod
    def produce_basic_csv_save(df_value:pd.DataFrame, value_path:str) -> None:
        """
        Method which is dedicated to 
        Input:  df_value = pandas DataFrame which needs to be stored
                value_path = path to the csv values which was used
        Output: we saved the dataframes to all of it
        """
        df_value.to_csv(value_path, index=False)
        
    def produce_merge_dataframe(self, value_df:pd.DataFrame, columns:list, name:str, submerge:bool=False, subset:list=[]) -> pd.DataFrame:
        """
        Method which is dedicated to produce merging of the dataframes for the 
        Input:  value_df = value dataframe which is required for work
                value_columns = columns which are required for the subset
                value_name = name of the of the dataframe
                value_submerge = boolean value which is dedicated to work with values
        Output: DataFrame value was successfully saved and merged if it has to
        """
        keep = 'last' if submerge else 'first'
        subset = subset if subset else columns
        value_df_path = os.path.join(self.folder_defaults, name)
        if not os.path.exists(value_df_path):
            return self.produce_basic_csv_save(value_df, value_df_path)
        value_df_file = pd.read_csv(value_df_path)
        result = pd.concat([value_df_file, value_df], keys=columns)
        result.drop_duplicates(subset=subset, keep=keep, inplace=True)
        self.produce_basic_csv_save(result, value_df_path)

    def produce_merge_dataframe_old(self, value_df:pd.DataFrame, value_bool:bool=False, value_submerge=False) -> pd.DataFrame:
        """
        Old Method which is dedicated to produce values of the dataframe values
        Input:  value_df = value dataframe which user got
        Output: we merged values of the dataframe
        """
        keep = 'last' if value_submerge else 'first'
        if not value_bool:
            csv_taken = csv_basic_song
            columns = self.columns_songs
            subset = ['Album_ID', 'Album_Length', 'Album_Link', 'Album_Name', 
                    'Artist_Name', 'Date', 'Label','Song_Links_Youtube', 
                    'Songs_Links', 'Songs_Number', 'Songs_Tracklist']
        else:
            csv_taken = csv_basic_song_fail
            columns = ['Album_ID', 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Album_Link_Previous']
            subset = columns
        df_path = os.path.join(self.folder_defaults, csv_taken)
        if not os.path.exists(df_path) and not os.path.isfile(df_path):
            result = value_df
        else:
            value_df_file = pd.read_csv(df_path)
            result = pd.concat([value_df_file, value_df], keys=columns)
        result.drop_duplicates(subset=subset, keep=keep, inplace=True)
        self.produce_basic_csv_save(result, df_path)

    def produce_song_remake_values_genius(self, value_song_dict={}, value_check:bool=False) -> list:
        """
        Method which is dedicated to produce values of dictionary to one from the 
        Input:  value_song_dict = value of the parsed values from the genius
                value_check = value which is dedicated to work with default values
        Output: list of values which would be comfortable 
        """
        # TODO think about another boolean variable
        value_path = os.path.join(folder_current, folder_storage, 'check.json')
        if not value_song_dict and not value_check and not os.path.exists(value_path) and not os.path.isfile(value_path):
            return
        elif not value_song_dict and not value_check:
            with open(value_path, 'r') as value_file:
                value_song_dict = json.load(value_file)
            if value_path == os.path.join(folder_current, folder_storage, 'one.json'):
                value_song_dict = [value_song_dict]
            else:
                pass
        
        for value_song in value_song_dict:
            if 'Album_Length' in value_song.keys():
                value_album_id = [value_song.get('Album_ID', '') for _ in range(value_song['Album_Length'])]
                value_album_name_df = [value_song.get('Album_Name_df', '') for _ in range(value_song['Album_Length'])]
                value_artist_name_df = [value_song.get('Artist_Name_df', '') for _ in range(value_song['Album_Length'])]
                value_year_df = [value_song.get('Year_df', '') for _ in range(value_song['Album_Length'])]
                value_album_len = [value_song.get('Album_Length', '') for _ in range(value_song['Album_Length'])]
                value_album_link = [value_song['Album_Link'] for _ in range(value_song['Album_Length'])]
                value_album_name = [value_song['Album_Name'] for _ in range(value_song['Album_Length'])]
                value_artist_name = [value_song['Artist_Name'] for _ in range(value_song['Album_Length'])]
                value_album_date = [value_song['Date'] for _ in range(value_song['Album_Length'])]
                value_album_label = [value_song.get('Label', '') for _ in range(value_song['Album_Length'])]
                
                value_album_lyrics = [song.get('Lyrics', '') for song in value_song.get('Songs_Values', [])]
                value_album_engineer = [song.get('Engineer', '') for song in value_song.get('Songs_Values', [])]
                value_album_link_song = [song.get('Song_Link', '') for song in value_song.get('Songs_Values', [])]
                value_album_written = [song.get('Written By', '') for song in value_song.get('Songs_Values', [])]
                value_album_produced = [song.get('Produced by', '') for song in value_song.get('Songs_Values', [])]
                value_album_recorded = [song.get('Recorded At', '') for song in value_song.get('Songs_Values', [])]
                value_album_released = [song.get('Release Date', '') for song in value_song.get('Songs_Values', [])]
        
                value_df = pd.DataFrame(list(zip(value_album_id, value_album_name_df, value_artist_name_df, 
                                        value_year_df, value_album_len, value_album_link, value_album_name,
                                        value_artist_name, value_album_date, value_album_label, value_album_lyrics, 
                                        value_album_engineer, value_album_link_song, value_album_written, 
                                        value_album_produced, value_album_recorded, value_album_released)), 
                                        columns=self.columns_songs_genius)
                self.produce_merge_dataframe(value_df, self.columns_songs_genius, csv_basic_song_genius)

    def produce_song_remake_values_old(self, value_song_dict:dict={}, value_check:bool=False) -> list:
        """
        Old Method which is dedicated to produce values of the 
        Input:  value_song_dict = dictionary values 
                value_check = boolean values
        Output: we created value of the dataframe for the songs and successfully developed values after
        """
        value_path = os.path.join(folder_current, folder_storage, 'check.json')
        if not value_song_dict and not value_check and not os.path.exists(value_path) and not os.path.isfile(value_path):
            return
        elif not value_song_dict and not value_check:
            with open(value_path, 'r') as value_file:
                value_song_dict = json.load(value_file)
            if value_path == os.path.join(folder_current, folder_storage, 'value_one.json'):
                value_song_dict = value_song_dict
            else:
                pass
        for value_song in value_song_dict:
            if 'Album_Length' in value_song.keys():
                value_album_id = [value_song.get('Album_ID', '') for _ in range(value_song['Album_Length'])]
                value_album_name_df = [value_song.get('Album_Name_df', '') for _ in range(value_song['Album_Length'])]
                value_artist_name_df = [value_song.get('Artist_Name_df', '') for _ in range(value_song['Album_Length'])]
                value_year_df = [value_song.get('Year_df', '') for _ in range(value_song['Album_Length'])]
                value_album_len = [value_song.get('Album_Length', '') for _ in range(value_song['Album_Length'])]
                value_album_link = [value_song['Album_Link'] for _ in range(value_song['Album_Length'])]
                value_album_name = [value_song['Album_Name'] for _ in range(value_song['Album_Length'])]
                value_artist_name = [value_song['Artist_Name'] for _ in range(value_song['Album_Length'])]
                value_album_date = [value_song['Date'] for _ in range(value_song['Album_Length'])]
                value_album_label = [value_song.get('Label', '') for _ in range(value_song['Album_Length'])]
                value_song_link_youtube = value_song['Song_Links_Youtube']
                value_song_link_genius = value_song['Songs_Links']
                value_song_number = value_song['Songs_Number']
                value_song_name = value_song['Songs_Tracklist']

                value_song_apple_id = [f.get('apple_id', '') for f in value_song['Song_Parameters']]
                value_song_artwork = [f.get('artwork_url', '') for f in value_song['Song_Parameters']]
                value_song_duration = [f.get('duration', '') for f in value_song['Song_Parameters']]
                value_song_artist_dislay_name = [f.get('artist_display_name', '') for f in value_song['Song_Parameters']]
                value_song_id_add = [f.get('song_id', '') for f in value_song['Song_Parameters']]
                value_song_title = [f.get('title', '') for f in value_song['Song_Parameters']]
                
                value_df = pd.DataFrame(list(zip(value_album_id, value_album_name_df, value_artist_name_df, 
                                        value_year_df, value_album_len, value_album_link, value_album_name,
                                        value_artist_name, value_album_date, value_album_label, 
                                        value_song_link_youtube, value_song_link_genius, value_song_number,
                                        value_song_name, value_song_apple_id, value_song_artwork, 
                                        value_song_duration, value_song_artist_dislay_name,
                                        value_song_id_add, value_song_title)), columns=self.columns_songs)
                self.produce_merge_dataframe_old(value_df)
            else:
                value_album_id = [value_song.get('Album_ID', '')]
                value_album_name_df = [value_song.get('Album_Name_df', '')]
                value_artist_name_df = [value_song.get('Artist_Name_df', '')]
                value_year_df = [value_song.get('Year_df', '')]
                value_link_prev = [value_song.get('Album_Link', '')]
                value_df = pd.DataFrame(list(zip(value_album_id, value_album_name_df, 
                    value_artist_name_df, value_year_df, value_link_prev)),
                    columns=['Album_ID', 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Album_Link_Previous'])
                self.produce_merge_dataframe_old(value_df, True)                

    def reproduce_search_songs(self) -> None:
        """
        Method which is dedicated to get secondary values of the songs which were not got from the 
        Input:  value_song_list = value songs list of the 
        Output: get list values of the returnal of the returnal for the subsearch of it
        """
        pass
        #TODO work here
        #TODO firstly; to check on the default, and to get after that from them html
        #TODO secondly; after the check of it, if shw must to get from it data manually
        #TODO thirdly; 

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

    def get_values_songs_usage(self, csv_name:str) -> list:
        """
        Method which is dedicated to get automated sorting of the songs
        Input:  csv_name = name which is required to be checked of the values
        Output: value list of the lists to get values
        """
        df_calculated = pd.read_csv(os.path.join(self.folder_defaults, csv_basic))
        values_id, values_album, values_artist, values_year = list(zip(
            *df_calculated.drop_duplicates(subset=['Album_ID'], 
            keep='first')[['Album_ID', 'Album_Name', 'Artist', 'Year']].values[:40]))
        file_songs = os.path.join(self.folder_defaults, csv_name)
        value_bool = os.path.exists(file_songs) and os.path.isfile(file_songs)
        if value_bool:
            df_songs = pd.read_csv(file_songs)
            values_id_created = df_songs.drop_duplicates(subset=['Album_ID'], keep='first').Album_ID.values
            value_id_used = [i for i, value in enumerate(values_id) if value in values_id_created]
            values_id = [value for i, value in enumerate(values_id) if i not in value_id_used]
            values_album = [value for i, value in enumerate(values_album) if i not in value_id_used]
            values_artist = [value for i, value in enumerate(values_artist) if i not in value_id_used]
            values_year = [value for i, value in enumerate(values_year) if i not in value_id_used]
        values_id, values_album = self.make_list_sublists(values_id), self.make_list_sublists(values_album)
        values_artist, values_year =  self.make_list_sublists(values_artist), self.make_list_sublists(values_year)
        return values_id, values_album, values_artist, values_year

    def produce_basic_values_genius(self, df_calculated:pd.DataFrame=pd.DataFrame()) -> None:
        """
        Method which is dedicated to produce values of the songs to the data insertion and to return values of the
        Input:  pd_calculated = basic dataframe which was fully commited from the
        Output: we created new dataframe values for the insertion; for the label and for the 
        """
        self.produce_basic_value()
        parser_genius = ParserGenius()
        if df_calculated.empty:
            df_calculated = pd.read_csv(os.path.join(self.folder_defaults, csv_basic))
        values_id, values_album, values_artist, values_year = self.get_values_songs_usage(csv_basic_song_genius)
        
        for value_id, value_album, value_artist, value_year in zip(values_id[:1], values_album[:1], values_artist[:1], values_year[:1]):
            start = time.time()
            loop = asyncio.get_event_loop()
            value_songs = loop.run_until_complete(parser_genius.parse_genius_song_additional_info(value_album, value_artist, True))
            [f.update({'Album_ID':i, 'Album_Name_df':n, 'Artist_Name_df':a, 'Year_df':y}) 
                for f, i, n, a, y in zip(value_songs, value_id, value_album, value_artist, value_year)]
            self.get_values_json(value_songs[0], 'one.json')
            self.get_values_json(value_songs)
            value_msg = '\n'.join([f"+ {i}" for i in value_album])
            print(f'We parsed albums:\n{value_msg}')
            print('=============================================================================')
            print(f'It took time: {time.time() - start}')
            print('#############################################################################')
            self.produce_song_remake_values_genius({})

    def produce_basic_values_deezer(self, df_calculated:pd.DataFrame=pd.DataFrame()) -> None:
        """
        Method which is dedicated to produce values of the songs to the data insertion
        Input:  df_calculated = dataframe which was previously calculated to it
        Output: we created new dataframe which is fully compatible with the previous dataframes and returns to us values
        """
        self.produce_basic_value()
        # parser_apple = ParserAppleMusic()
        parser_deezer = ParserDeezer()
        if df_calculated.empty:
            df_calculated = pd.read_csv(os.path.join(self.folder_defaults, csv_basic))
        values_id, values_album, values_artist, values_year = self.get_values_songs_usage(csv_basic_song_deezer)
        for value_id, value_album, value_artist, value_year in zip(values_id[:1], values_album[:1], values_artist[:1], values_year[:1]):
            start = time.time()
            #TODO add here values
            loop = asyncio.get_event_loop()
            value_songs = loop.run_until_complete(parser_deezer.produce_search_albums_deezer(value_album, value_artist, value_year))
            self.get_values_json(value_songs, 'checkings.json')
            value_msg = '\n'.join([f"+ {i}" for i in value_album])
            # print(f'We found albums:\n{value_msg}')
            # print('=============================================================================')
            print(f'It took time: {time.time() - start}')
            print('#############################################################################')

    def get_values_json(self, value_dict:dict, value_name:str='check.json') -> None:
        """
        Method which is dedicated to develop json values for the testing
        Input:  value_dict = dictionary values of the taken of the it
        Output: we created test.json values for the inserting        
        """
        value_folder = os.path.join(folder_current, folder_storage)
        os.path.exists(value_folder) or os.mkdir(value_folder)
        value_path = os.path.join(value_folder, value_name)
        if os.path.exists(value_path) and os.path.isfile(value_path):
            return
        with open(value_path, 'w') as fp:
            json.dump(value_dict, fp, indent=4)

    def get_values_db_insert_all(self) -> list:
        """
        Method which is dedicated to produce list for multiple insertions
        Input:  values of the basic csv which was taken for it
        Output: list of dictionaries for taking values of it
        """
        self.produce_basic_value()
        list_insertion = []
        df_basic = pd.read_csv(os.path.join(self.folder_defaults, csv_basic))
        df_album_id = df_basic['Album_ID'].values
        df_album_name = df_basic['Album'].values
        df_artist_id = df_basic['Artist_ID'].values
        df_artist_username = df_basic['Artist'].values
        df_genre_id = df_basic['Genre_ID'].values
        df_genre_name = df_basic['Genre'].values
        df_year = df_basic['Year'].values
        for album_id, album, artist_id, artist, genre_id, genre, year in zip(df_album_id, 
                df_album_name, df_artist_id, df_artist_username, df_genre_id, df_genre_name, df_year):
            list_insertion.append({
                "album_id": album_id,
                "album_name": album,
                "artist_id": artist_id,
                "artist_username": artist,
                "genre_id": genre_id,
                "genre_name": genre,
                "year_album": year,                
            })
        return list_insertion