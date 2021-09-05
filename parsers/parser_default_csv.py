import os
import asyncio
from pprint import pprint
import json
import numpy as np
import pandas as pd
from parsers.parser_genius import ParserGenius
from config import (csv_year,
                    csv_basic,
                    csv_genre,
                    csv_edges,
                    csv_albums,
                    csv_artist,
                    csv_subgenre,
                    csv_basic_genre,
                    folder_current,
                    folder_defaults)


class ParserDefaultCSV:
    """
    class which is dedicated to produce from the open source csv
    and to insert them into the database
    """
    def __init__(self) -> None:
        # self.loop = asyncio.get_event_loop()
        self.columns = ['Album_ID', 'Album_Name', "Artist_ID", 'Artist', 'Genre', 'Year']
        self.folder_defaults = os.path.join(folder_current, folder_defaults)
        self.produce_basic_values_genius()
        
    def check_presence_files(self) -> bool:
        """
        Method which is dedicated to check presence of necessary files for further work
        Input:  presented dataframes from open sources
        Output: boolean values which signify to continue
        """
        value_check = [os.path.join(self.folder_defaults, x) for x in [csv_year, csv_genre, csv_edges, csv_albums, csv_artist, csv_subgenre]]
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
                            "Album_Name": {'Sign \\"Peace\\" the Times': "Sign O’ the Times",
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
        return_index, return_album, return_artist_id, return_artist, return_genre_id, return_genre, return_year = [], [], [], [], [], [], []
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

    @staticmethod
    def get_song_values_automatic(value_names) -> list:
        """
        Method which is dedicated to produce values of the 
        Input:  value_names = list with names of an albums which we are going to search
        Output: list with parsed html values which are going to be further produced
        """
        pass
        # parser_genius = ParserGenius()
        #TODO work here
        #TODO firstly; to check on the default, and to get after that from them html
        #TODO secondly; after the check of it, if shw must to get from it data manually
        #TODO thirdly; 

    def produce_song_remake_values(self, value_song_dict:dict) -> list:
        """
        
        """
        pass

    #TODO check here after values
    def reproduce_search_songs(self) -> None:
        """"""
        pass

    def produce_basic_values_genius(self, df_calculated:pd.DataFrame=pd.DataFrame()) -> None:
        """
        Method which is dedicated to produce values of the songs to the data insertion and to return values of the
        Input:  pd_calculated = basic dataframe which was fully commited from the
        Output: we created new dataframe values for the insertion; for the label and for the 
        """
        self.produce_basic_value()
        parser_genius = ParserGenius()
        df_calculated = pd.read_csv('/home/oshevchenko/FolderProjects/BotMusic/defaults/Basic.csv')
        value_id, value_album, value_artist, value_year = list(zip(
            *df_calculated.drop_duplicates(subset=['Album_ID'], keep='first')[['Album_ID', 'Album_Name', 'Artist', 'Year']].values[:5]))
        # loop = asyncio.get_event_loop()
        value_songs = self.loop.run_until_complete(parser_genius.parse_genius_automatic_album_list(value_album, value_artist))
        pprint(value_songs[0])
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        
    #TODO work here !!!
    def get_values_json(self, value_dict:dict, value_name:str='check.json') -> None:
        """
        Method which is dedicated to develop
        Input:  value_dict = dictionary values of the 
        Output: we created test.json values for the inserting        
        """
        pass

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