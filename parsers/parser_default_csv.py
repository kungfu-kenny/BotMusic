from genericpath import isfile
import os
import pandas as pd
from config import (csv_year,
                    csv_basic,
                    csv_genre,
                    csv_edges,
                    csv_albums,
                    csv_artist,
                    csv_subgenre,
                    folder_current,
                    folder_defaults)


class ParserDefaultCSV:
    """
    class which is dedicated to produce from the open source csv
    and to insert them into the database
    """
    def __init__(self) -> None:
        self.columns = ['Album_ID', 'Album_Name', "Artist_ID", 'Artist', 'Genre', 'Year']
        self.folder_defaults = os.path.join(folder_current, folder_defaults)
        self.produce_basic_value()
        
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
        value_file = os.path.join(self.folder_defaults, csv_basic)
        return os.path.join(value_file) and os.path.isfile(value_file)

    @staticmethod
    def get_values_list_df(df_used:pd.DataFrame, df_index:list, column:str='name') -> list:
        """
        Method which is dedicated to get values list of the df
        Input:  df_used = dataframe of values where to take values
                df_index = index where to take values
        Output: list with values of the 
        """
        value_return = []
        for index in df_index:
            value_return.extend(df_used.loc[df_used["~id"]==index, column].values)
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
        #TODO add here values of the group id calculation in cases of id
        df_albums = pd.read_csv(os.path.join(self.folder_defaults, csv_albums))
        df_genre = pd.read_csv(os.path.join(self.folder_defaults, csv_genre))
        df_artist = pd.read_csv(os.path.join(self.folder_defaults, csv_artist))
        df_subgenre = pd.read_csv(os.path.join(self.folder_defaults, csv_subgenre))
        df_year = pd.read_csv(os.path.join(self.folder_defaults, csv_year))
        df_edges = pd.read_csv(os.path.join(self.folder_defaults, csv_edges))
        values_id = df_edges['~from'].unique()
        df_artist['Artist_ID'] = [f for f in range(1, df_artist['name'].nunique() + 1)]
        return_index, return_album, return_artist_id, return_artist, return_genre, return_year = [], [], [], [], [], []
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
        
        df_calculated = pd.DataFrame(list(zip(return_index, return_album, return_artist_id, return_artist, return_genre, return_year)), 
                                    columns=self.columns)
        df_calculated.to_csv(os.path.join(self.folder_defaults, csv_basic), index=False)
        
        
    def get_values_usage(self) -> list:
        """
        Method which is dedicated to produce list for multiple insertions
        Input:  values of the basic csv which was taken for it
        Output: list of dictionaries for taking values of it
        """
        pass