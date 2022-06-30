import os
from attr import dataclass
from dotenv import load_dotenv

load_dotenv()
###########################BLOCK WEBDRIVER#################################

link_webdriver = os.getenv("LINK_WEBDRIVER")
######################BLOCK TELEGRAM BASIC#################################

@dataclass
class BotDefault:
    key = os.getenv('BOT_KEY')
    chat_id = os.getenv('CHAT_ID_DEFAULT')
#######################BLOCK TELEGRAM ROUTES###############################

@dataclass
class Telegram:
    start = 'start'
    history = 'history'
    settings = 'settings'
######################BLOCK FOLDERS########################################

@dataclass
class FolderProject:
    folder_db = "db"
    folder_storage = "storage"
    folder_defaults = "defaults"
    folder_telegram = "telegram"
    folder_current = os.getcwd()    
######################CRED DATABASE########################################

@dataclass
class DataBaseCredentials:
    db_file = "local.db"
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_base = os.getenv("DB_BASE")
    db_pass = os.getenv("DB_PASSWORD")
######################CSV PARAMS###########################################

@dataclass
class CSVNames:
    csv_basic = "Basic.csv"
    csv_year = "Year.csv"
    csv_edges = "Edges.csv"
    csv_genre = "Genre.csv"
    csv_albums = "Albums.csv"
    csv_artist = "Artist.csv"
    csv_subgenre = "Subgenre.csv"
    csv_basic_song = "Basic_Song.csv"
    csv_basic_label = "Basic_Label.csv"
    csv_basic_genre = "Basic_Genre.csv"
    csv_basic_song_fail = "Basic_Song_Failed.csv"
    csv_basic_song_apple = "Basic_Song_Apple.csv"
    csv_basic_song_deezer = "Basic_Song_Deezer.csv"
    csv_basic_song_genius = "Basic_Song_Genius.csv"
    csv_basic_song_yandex = "Basic_Song_Yandex.csv"
    csv_advanced_song_yandex = "Advanced_Song_Yandex.csv"
    csv_basic_album_google = "Basic_Album_Google_Successful.csv"
    csv_basic_album_google_failed = "Basic_Album_Google_Failed.csv"
    csv_basic_album_deezer_failed = "Basic_Album_Deezer_Failed.csv"
    csv_basic_album_deezer_possible = "Basic_Album_Deezer_Possible.csv"
    csv_basic_album_deezer_success = "Basic_Album_Deezer_Successful.csv"  
    #TODO continue work from here
    csv_basic_album_apple_failed = 'Basic_Album_Apple_Failed.csv'
    csv_basic_album_apple_possible = 'Basic_Album_Apple_Possible.csv'
    csv_basic_album_apple_success = 'Basic_Album_Apple_Successful.csv'
######################NAME DATABASE########################################

table_user = 'user'
table_song = 'song'
table_label = 'label'
table_album = 'album'
table_genre = 'genre'
table_artist = 'artist'
table_song_year = 'song_year'
table_song_genre = 'song_genre'
table_song_label = 'song_label'
table_album_song = 'album_song'
table_album_year = 'album_year'
table_album_label = 'album_label'
table_album_genre = 'album_genre'
table_artist_song = 'artist_song'
table_genre_label = 'genre_label'
table_artist_genre = 'artist_genre'
table_artist_label = 'artist_label'
table_artist_album = 'artist_album'
table_song_youtube = 'song_youtube'
table_user_history_song = 'user_history_song'
table_user_history_album = 'user_history_album'
table_user_favourite_song = 'user_favourite_song'
table_user_favourite_album = 'user_favourite_album'
#######################PARSE GENIUS########################################

@dataclass
class LinkGenius:
    genius_semaphore_threads = 10
    link_genius = "https://genius.com"
    link_genius_albums = "albums"
    link_genius_search_begin = "/search?q="
    link_genius_search_end= "%20"
#######################PARSE APPLE MUSIC###################################

@dataclass
class LinkAppleMusic:
    apple_music_album_wait = 10
    apple_music_semaphore_threads = 10
    link_apple_music = 'https://music.apple.com'
    link_apple_music_us = 'us'
    link_apple_music_space = '%20'
    link_apple_music_search = 'search?term='    
    list_used_check = [' (Original Mono & Stereo Mix Versions)', " (Remastered)"]
#######################PARSE DEEZER########################################

@dataclass
class LinkDeezer:
    deezer_semaphore_threads = 10
    link_deezer = 'https://www.deezer.com'
    link_deezer_us = 'us'
    link_deezer_album = 'album'
    link_deezer_track = 'track'
    link_deezer_search = 'search'
    link_deezer_space = '%20'
    link_deezer_dollar = '%24'
    link_deezer_doublecom = '%3A'
    link_deezer_a = '%40'
    link_deezer_box = "%23"
    link_deezer_comsep = '%3B'
#######################PARSE YANDEX########################################

@dataclass
class LinkYandex:
    yandex_semaphore_threads = 10
    link_yandex = 'https://music.yandex.ru'
    link_yandex_album = 'album'
    link_yandex_track = 'track'
    link_yandex_search = 'search?'
    link_yandex_a = '%40'
    link_yandex_box = "%23"
    link_yandex_comsep = '%3B'
    link_yandex_space = '%20'
    link_yandex_dollar = '%24'
    link_yandex_doublecom = '%3A'
#######################PARSE GOOGLE########################################

@dataclass
class LinkGoogle:
    google_semaphore_threads = 10
    google_search_youtube = 'YouTube'
    google_search_youtube_music = 'YouTube Music'
    google_search_deezer = 'Deezer'
    link_google_a = "%40"
    link_google_comsep = '%3B'
    link_google_space = '%20'
    link_google_dollar = '%24'
    link_google_doublecom = '%3A'


@dataclass
class ParserColumnsCSV:
    columns = ['Album_ID', 'Album_Name', "Artist_ID", 'Artist', 'Genre', 'Year']
    columns_songs = ['Album_ID', 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Album_Length', 
                    'Album_Link', 'Album_Name', 'Artist_Name', 'Date', 'Label', 'Song_Links_Youtube', 
                    'Songs_Links', 'Songs_Number', 'Songs_Tracklist','Apple_ID', 
                    'Artwork_Url', 'Duration', 'Artist_Display_Name', 'Song_Genius_ID', 'Title']
    columns_songs_genius = ['Album_ID', 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Album_Length',
                            'Album_Link', 'Album_Name_Genius', 'Artist_Name_Genius', 'Album_Date_Genius',
                            'Album_Label_Genius', 'Album_Song_Number', 'Album_Song_Name', 'Album_Song_Link']
    columns_deezer_songs = ["Album_ID", "Album_Name_Deezer", "Artist_Name_Deezer", "Year_Deezer", 
                        "Label_Deezer", "Album_Duration", "Song_Order", "Album_Number_Tracks", "Song_Name_Deezer", 
                        "Song_Author_Deezer", "Song_Length", "Song_Popularity_Deezer", "Song_Link_Deezer"]
    columns_deezer_successful = ['Album_ID', 'Album_ID_Deezer', 'Album_Name_df', 'Artist_Name_df', 'Year_df',
                    'Album_Name_Deezer', 'Artist_Name_Deezer', 'Artist_ID_Deezer', 'Release_Date_Physical',
                    'Release_Date_Original', 'Album_Picture_Deezer', 'Album_Available_Deezer', 
                    'Album_Version_Deezer','Explicit_Lyrics_Deezer', 'Explicit_Cover_Deezer', 'Type_INT_Deezer', 
                    'Artist_Dummy_Deezer', 'Album_Number_Track_Deezer', 'Type_Deezer', 'Link_Searched_Deezer', 
                    'Link_Album_Deezer', 'Checked_Album_Deezer', 'Checked_Artist_Deezer']
    columns_deezer_failed = ["Album_ID", 'Album_Name_df', 'Artist_Name_df', 'Year_df', 'Link_Search_Failed_Deezer']
    columns_google_successful = ["Album_ID", "Album_Name", "Artist", "Link", "YouTube", "YouTube Music", "Deezer", "Year"]
    columns_google_failed = ["Album_ID", "Album_Name", "Artist", "Link", "Year"]
    deezer_options = ['songs', 'successful', 'possible', 'failed']
    json_deezer_names = ['deezer_songs.json', 'deezer_successfull.json', 'deezer_possible.json', 'deezer_failed.json']